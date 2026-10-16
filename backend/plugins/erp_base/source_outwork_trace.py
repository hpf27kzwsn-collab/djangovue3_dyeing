"""外协申请、发出、回货、退回及质量处置的逐条来源查询。"""
from plugins.erp_base.source_provenance import reference as source_reference
from django.apps import apps
from .source_stock_services import raw
from .source_context import SourceDocumentContext
from .source_chain_reverse import related
from .source_ownership import OWNERS
from .source_execution_state import active

LINKS=['outwork_dispatch_origin','outwork_receipt_origin','material_return_origin','product_dispatch_origin','outwork_return_origin']


def trace(item, query):
    pending=[item];seen=set();result=[];links=[];unresolved=[]
    while pending:
        row=pending.pop(0);key=(row._meta.label,row.pk)
        if key in seen:continue
        seen.add(key)
        context=SourceDocumentContext.objects.filter(entity=row._meta.label,object_id=row.pk).first()
        effects={} if context is None else context.effects
        result.append({'entity':row._meta.label,'record_id':row.pk,'source': source_reference(row),
            'active':active(type(row).objects.filter(pk=row.pk)).exists(),
            **{field:raw(row,field) for field in ['SheetNo','SheetSeries','SheetKind','JobSheetNo','CheckNo','Rolls','WeightQty','LengthQty','Qty','StockUnit'] if field in row.SOURCE_FIELDS},
            **{name:None if name not in effects else {key:effects[name][key] for key in
                ['result','factory','receiver','at','reason'] if key in effects[name]}
                for name in ['factory_quality','delivery_confirmation']}})
        for label,rules in OWNERS.items():
            for rule in rules:
                if rule['target']!=row._meta.label:continue
                model=apps.get_model(label)
                for child in related(query(model.SOURCE_TABLE,model._meta.app_label),rule,row).order_by('pk'):
                    pending.append(child);links.append({'source_id':row.pk,'source_entity':row._meta.label,
                        'target_id':child.pk,'target_entity':child._meta.label,'relation':'原主从'})
        found=False
        for name in LINKS:
            contexts=SourceDocumentContext.objects.filter(**{f'effects__{name}__entity':row._meta.label,
                f'effects__{name}__source__id':row.pk}).order_by('pk')
            for linked in contexts:
                model=apps.get_model(linked.entity)
                for target in query(model.SOURCE_TABLE,model._meta.app_label).filter(pk=linked.object_id):
                    pending.append(target);found=True
                    links.append({'source_id':row.pk,'source_entity':row._meta.label,'target_id':target.pk,
                        'target_entity':target._meta.label,'relation':name})
        if not found and row.SOURCE_TABLE in ['OutWorkApplyDetail','SemiOutWorkApplyDetail','GrayOutDetail','SemiOutDetail']:
            unresolved.append({'entity':row._meta.label,'record_id':row.pk,'source': source_reference(row),
                'issue':'没有已登记的后续来源；不据此断言从未发出/收回，也不以同码猜接。'})
    return {'report':'外协完整来源与质量处置追溯','rows':result,'result_rows':links,'supplemental_rows':unresolved,
        'notes':['同时列出活动及已撤回留档记录；申请量、实际发出、实际回货、退回及质量处置分别显示，不合并为一种数量。',
            '沿明确来源记录ID追溯，原历史未登记对应的明细单列，不按低频或异常排除。']}
