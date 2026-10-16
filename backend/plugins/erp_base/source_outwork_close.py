"""外协实际收发核对、损耗确认与结案；不覆盖旧申请字段或库存。"""
import json
from collections import defaultdict
from django.core.exceptions import ValidationError
from django.db import transaction
from .business import FactsEncoder, locked, persist, record, snapshot
from .source_business_updates import matching
from .source_context import SourceDocumentContext
from .source_quality_reports import rows, total
from .source_stock_services import raw

MEASURES = ['Rolls', 'WeightQty', 'LengthQty']


def facts(value):
    return json.loads(json.dumps(value, cls=FactsEncoder))


def reconciliation(dispatched, received, losses, query=rows, returned_material=(), returned_product=()):
    groups = defaultdict(lambda: {'dispatch': [], 'receipt': [], 'material_return': [], 'product_return': [], 'loss': []})
    sources = []
    for direction, selected in [('dispatch', dispatched), ('receipt', received),('material_return',returned_material),('product_return',returned_product)]:
        # 同一记录重复选择只核对一次；不同原行即使业务码相同仍全部保留。
        for item in {(item._meta.label,item.pk): item for item in selected}.values():
            if item.SOURCE_TABLE.endswith('Detail'):
                from .source_ownership import OWNERS
                rule=OWNERS[item._meta.label][0]
                parents=query(item.SOURCE_TABLE.removesuffix('Detail'),'erp_warehouse')
                parent_id=getattr(item,rule['field']+'_id')
                parents=list(parents.filter(pk=parent_id) if parent_id is not None else matching(parents,SheetSeries=raw(item,'SheetSeries')))
            else:
                parents = [item]
            # 无表头/重复表头不猜单位，保留所有候选并归入未确定单位。
            unit = raw(item, 'StockUnit') if item.SOURCE_TABLE == 'ProdOutDetail' else raw(parents[0], 'StockUnit') if len(parents) == 1 else None
            sources.append({'direction': direction, 'entity': item._meta.label, 'source': snapshot(item),
                            'headers': [snapshot(parent) for parent in parents], 'unit': unit})
            for measure in MEASURES:
                value = raw(item, measure) if measure in item.SOURCE_FIELDS else None
                identity = f'{item._meta.label}/{item.pk}' if unit is None else None
                groups[(unit, measure, identity)][direction].append(value)
    for index, loss in enumerate(losses):
        identity = 'loss/' + str(index + 1) if loss['unit'] is None else None
        groups[(loss['unit'], loss['measure'], identity)]['loss'].append(loss['quantity'])
    result = []
    for (unit, measure, identity), values in groups.items():
        outgoing, incoming, loss = (total(values[key]) for key in ['dispatch', 'receipt', 'loss'])
        material_return=total(values['material_return']) if values['material_return'] else 0
        product_return=total(values['product_return']) if values['product_return'] else 0
        net_dispatched=None if outgoing is None or material_return is None else outgoing-material_return
        net_received=None if incoming is None or product_return is None else incoming-product_return
        difference = None if net_dispatched is None or net_received is None else net_dispatched-net_received
        result.append({'unit': unit, 'measure': measure, 'unresolved_unit_source': identity, 'dispatched': outgoing, 'received': incoming,
            'difference': difference, 'confirmed_loss': loss,
            'material_return':material_return,'product_return':product_return,'net_dispatched':net_dispatched,'net_received':net_received,
            'unexplained_difference': None if difference is None or loss is None else difference - loss,
            'dispatch_nulls': values['dispatch'].count(None), 'receipt_nulls': values['receipt'].count(None)})
    return {'report': '外协结案核对', 'rows': result, 'sources': sources,
        'supplemental_rows': [{'direction': source['direction'], 'entity': source['entity'],
            'id': source['source']['id'], 'source_batch': source['source']['source_batch'], 'source_row': source['source']['source_row'], 'unit': source['unit'],
            'header_count': len(source['headers']), **{key:value for key,value in source['source'].items() if key.startswith('old_')}} for source in sources],
        'notes': ['按明确选定的实际收发记录作本单数量汇总；单位不同不相加，单位未定逐行列示，空值不改成零，负值保留。',
            '损耗由本次确认填写，收发差额不自动认定为损耗；数量汇总保留空值条数。']}


@transaction.atomic
def close(item, actor, dispatched, received, losses, closed_at, reason, query=rows, returned_material=(), returned_product=(), received_gray=(), received_semi=()):
    item = locked(item)
    dispatched = [locked(row) for row in dispatched]
    received = [locked(row) for row in [*received,*received_gray,*received_semi]]
    returned_material=[locked(row) for row in returned_material];returned_product=[locked(row) for row in returned_product]
    result = reconciliation(dispatched, received, losses, query,returned_material,returned_product)
    context, _ = SourceDocumentContext.objects.get_or_create(entity=item._meta.label, object_id=item.pk,
        defaults={'entry_name': 'explicit_outwork_closure'})
    before = snapshot(context)
    if 'outwork_closure' in context.effects:
        context.effects.setdefault('outwork_closure_history',[]).append(context.effects['outwork_closure'])
    context.effects['outwork_closure'] = facts({'state': 'closed', 'closed_at': closed_at, 'reason': reason,
        'losses': losses, 'application': snapshot(item), 'reconciliation': result,
        'movement_count':len(context.effects.get('outwork_movements',[]))})
    persist(context, actor)
    record(context, 'outwork_closed', before, actor, reason)
    return result


@transaction.atomic
def reopen(item, actor, reason):
    item = locked(item)
    context = SourceDocumentContext.objects.filter(entity=item._meta.label, object_id=item.pk).first()
    if context is None or 'outwork_closure' not in context.effects or context.effects['outwork_closure']['state'] not in ['closed','needs_review']:
        raise ValidationError({'closure': '本单当前没有可撤回的外协结案。'})
    before = snapshot(context)
    context.effects['outwork_closure']['state'] = 'open'
    context.effects['outwork_closure']['reopen_reason'] = reason
    persist(context, actor)
    record(context, 'outwork_closure_reopened', before, actor, reason)
    return context.effects['outwork_closure']


def closure(item):
    context = SourceDocumentContext.objects.filter(entity=item._meta.label, object_id=item.pk).first()
    return None if context is None else context.effects.get('outwork_closure')
