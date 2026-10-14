"""半成品新领用细码分配；保留历史和明确录入细码，生成对应单独登记。"""
from collections import defaultdict
from decimal import Decimal
from django.apps import apps
from django.db.models import Q
from django.db.models.functions import Upper, RTrim
from .business import persist, record
from .source_context import SourceDocumentContext
from .source_calculations import decimal, store_value
from .source_stock_services import raw, detail_rows


def code(value):
    return None if value is None else value.rstrip(' ').upper()


def add(pool, key, value, direction=1):
    if value is not None:
        pool[key] = (Decimal(0) if pool[key] is None else pool[key]) + decimal(value) * direction


def allocate(item, context, actor):
    lines = list(detail_rows(item, 'SemiOutDetail'))
    receipts = {code(raw(line, 'ReceSheetNo')) for line in lines if raw(line, 'ReceSheetNo') is not None}
    incoming = apps.get_model('erp_warehouse.SourceDyeSemiInRecord')
    outgoing = apps.get_model('erp_warehouse.SourceDyeSemiOutRecord')
    pools = defaultdict(lambda: {'rolls': None, 'weight': None, 'packs': None, 'original_rolls': None,
                                 'receipt': None, 'barcode': None, 'roll_no': None})
    received = incoming.objects.alias(receipt=Upper(RTrim('old_rece_sheet_no')), original=Upper(RTrim('old_ori_rece_sheet_no'))).filter(
        Q(receipt__in=receipts) | Q(original__in=receipts)).select_related('source_parent_1__source_parent_1').order_by('pk')
    for source in received:
        parent = source.source_parent_1
        header = None if parent is None else parent.source_parent_1
        returned = header is not None and raw(header, 'SheetKind') == 16
        receipt = raw(source, 'OriReceSheetNo') if returned else raw(source, 'ReceSheetNo')
        barcode = raw(source, 'OriBarCode') if returned else raw(source, 'BarCode')
        if code(receipt) not in receipts:
            continue
        key = (code(receipt), code(barcode), raw(source, 'RollNo'))
        pool = pools[key]
        pool.update(receipt=receipt, barcode=barcode, roll_no=raw(source, 'RollNo'))
        direction = -1 if returned else 1
        for target, field in [('rolls', 'Rolls'), ('weight', 'WeightQty'), ('packs', 'Packs')]:
            add(pool, target, raw(source, field), direction)
        if not returned:
            add(pool, 'original_rolls', raw(source, 'Rolls'))
    issued = outgoing.objects.alias(receipt=Upper(RTrim('old_rece_sheet_no'))).filter(receipt__in=receipts).exclude(
        source_parent_1__source_parent_1=item).order_by('pk')
    for source in issued:
        key = (code(raw(source, 'ReceSheetNo')), code(raw(source, 'BarCode')), raw(source, 'RollNo'))
        if key not in pools:
            continue
        pool = pools[key]
        add(pool, 'rolls', raw(source, 'Rolls'), -1)
        add(pool, 'weight', raw(source, 'WeightQty'), -1)
        add(pool, 'packs', raw(source, 'Packs'), -1)
    generated = []; results = []
    for line in lines:
        manual = list(outgoing.objects.filter(source_parent_1=line).order_by('pk'))
        if manual:
            for source in manual:
                key = (code(raw(source, 'ReceSheetNo')), code(raw(source, 'BarCode')), raw(source, 'RollNo'))
                if key in pools:
                    for target, field in [('rolls', 'Rolls'), ('weight', 'WeightQty'), ('packs', 'Packs')]:
                        add(pools[key], target, raw(source, field), -1)
            results.append({'detail_id': line.pk, 'mode': 'explicit_records', 'record_ids': [source.pk for source in manual]})
            continue
        needed_rolls = decimal(raw(line, 'Rolls')); needed_weight = decimal(raw(line, 'WeightQty'))
        receipt = code(raw(line, 'ReceSheetNo'))
        selected = []
        matching = [(key, pool) for key, pool in pools.items() if key[0] == receipt]
        matching.sort(key=lambda pair: (pair[0][1] is not None, pair[0][1] or '', str(pair[0][2])))
        for key, pool in matching:
            if pool['rolls'] is None or pool['rolls'] <= 0:
                continue  # 原过程只从剩余粒数大于0的细码生成；原收料行仍完整保存。
            rolls = None if needed_rolls is None else min(max(needed_rolls, 0), pool['rolls'])
            weight = None if needed_weight is None or pool['weight'] is None else min(max(needed_weight, 0), max(pool['weight'], 0))
            if not ((rolls is not None and rolls > 0) or (weight is not None and weight > 0)):
                continue
            packs = 0 if pool['packs'] == 0 or (pool['original_rolls'] is not None and rolls is not None and pool['original_rolls'] > rolls) else 1
            original = {'SheetSeries': raw(item, 'SheetSeries'), 'AssignedNo': raw(line, 'AssignedNo'),
                'RollNo': pool['roll_no'], 'BarCode': pool['barcode'], 'ReceSheetNo': pool['receipt'],
                'Rolls': rolls, 'WeightQty': weight, 'Packs': packs, 'LengthQty': None,
                'StorageUnitID': None, 'Status': None, 'Remarks': None, 'GUnit': None, 'JobSheetNo': None}
            values = dict(store_value(outgoing(), old, value) for old, value in original.items())
            source = persist(outgoing(source_parent_1=line, **values), actor)
            SourceDocumentContext.objects.create(entity=source._meta.label, object_id=source.pk, entry_name='SemiOutRecord',
                creator=actor, modifier=actor, dept_belong_id=item.dept_belong_id,
                effects={'derived_from': {'entity': item._meta.label, 'id': item.pk}})
            record(source, 'allocate_semi_record', {'exists': False}, actor, '按收料单、条码与细码分配实际剩余粒数和重量')
            generated.append(source.pk); selected.append(source.pk)
            if rolls is not None:
                needed_rolls -= rolls; pool['rolls'] -= rolls
            if weight is not None:
                needed_weight -= weight; pool['weight'] -= weight
            if pool['packs'] is not None:
                pool['packs'] -= packs
        results.append({'detail_id': line.pk, 'mode': 'allocated', 'record_ids': selected,
            'unallocated_rolls': None if needed_rolls is None else str(needed_rolls),
            'unallocated_weight': None if needed_weight is None else str(needed_weight)})
    context.effects = {**context.effects, 'semi_records': {outgoing._meta.label: generated}, 'semi_allocation': results}
    persist(context, actor)
