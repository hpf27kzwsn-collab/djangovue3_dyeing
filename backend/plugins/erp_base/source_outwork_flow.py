"""外协申请的原订单余额及明确数量采用，不把计划当成实际收发。"""
from django.apps import apps
from django.db import transaction
from .business import locked, persist, record, snapshot
from .source_stock_services import raw
from .source_business_updates import matching
from .source_sample_flow import copy_values
from .source_context import SourceDocumentContext
from .source_calculations import store_value, product


def rows(table, module='erp_production'):
    from .source_execution_state import active
    return active(apps.get_model(module + '.SourceDye' + table).objects.all())


def zero(value):
    return 0 if value is None else value  # 原视图明确ISNULL(...,0)。


def remaining(item):
    import re
    heads = list(matching(rows('OrderMain', 'erp_sales'), SheetSeries=raw(item, 'SheetSeries')).order_by('pk'))
    results = []
    applications = []
    for line in matching(rows('SemiOutWorkApplyDetail'), CheckNo=raw(item, 'CheckNo')).order_by('pk'):
        for head in matching(rows('SemiOutWorkApply'), SheetSeries=raw(line, 'SheetSeries')):
            applications.append({'id': line.pk, 'header_id': head.pk, 'qty': raw(line, 'Qty')})
    for head in heads:
        allocations = []
        for line in matching(rows('JobCombineOrder'), OrderSheetNo=raw(head, 'SheetNo'), CheckNo=raw(item, 'CheckNo')):
            for job in matching(rows('JobSheet'), SheetSeries=raw(line, 'SheetSeries')):
                no = raw(job, 'SheetNo')
                if raw(job, 'SheetKind') is None or raw(job, 'SheetKind') == 10 or no is None or re.search(r'X[1-9]$', no.rstrip(' '), re.I) or raw(job, 'SheetStatus') == 9:
                    continue
                allocations.append({'id': line.pk, 'job_id': job.pk, 'qty': raw(line, 'CombineQty')})
        eligible = (zero(raw(item, 'PrepareVats')) <= 0 and zero(raw(item, 'IsFinished')) == 0
            and zero(raw(head, 'IsFinished')) == 0 and raw(item, 'CheckNo') is not None
            and raw(item, 'CheckNo').rstrip(' ') != '' and (raw(item, 'Remarks02') is None or raw(item, 'Remarks02').rstrip(' ') == ''))
        results.append({'order_id': head.pk, 'old_selection_available': eligible,
            'last_vats': zero(raw(item, 'CardQty')), 'last_rolls': zero(raw(item, 'OrderRolls')),
            'last_qty': zero(raw(item, 'OrderQty')) + zero(raw(item, 'OutQty'))
                - sum(zero(row['qty']) for row in allocations) - sum(zero(row['qty']) for row in applications),
            'allocations': allocations, 'applications': applications})
    return results


@transaction.atomic
def apply(item, actor, quantity, rolls, factory, process, applied_at, entry='SemiOutWorkApply'):
    from . import source_services as services
    item = locked(item)
    from .source_execution_state import require_available
    require_available(item)
    head_model, detail_model = rows(entry).model, rows(entry + 'Detail').model
    heads = list(matching(rows('OrderMain', 'erp_sales'), SheetSeries=raw(item, 'SheetSeries')).order_by('pk'))
    parent = heads[0] if len(heads) == 1 else None
    header = {'_entry': entry, 'old_sheet_date': applied_at, 'old_fact_id': factory, 'old_process_id': process}
    if entry == 'SemiOutWorkApply':
        header['old_customer_id'] = None if parent is None else raw(parent, 'CustomerID')
    head = services.write(head_model, header, actor=actor, apply_effects=False)
    values = copy_values(item, detail_model, ['SheetSeries', 'DetailNo', 'Qty', 'Rolls', 'Amount', 'Remarks'])
    values.update(source_parent_1=head, old_qty=quantity, old_rolls=rolls,
        old_customer_id=None if parent is None else raw(parent, 'CustomerID'),
        old_remarks=(raw(item, 'Remarks03') or '') + (raw(item, 'Remarks') or ''))
    if entry == 'SemiOutWorkApply':
        values['old_order_sheet_no'] = None if parent is None else raw(parent, 'SheetNo')
    values.update(dict(store_value(detail_model(), key, value) for key, value in [
        ('Qty', quantity), ('Rolls', rolls), ('Amount', product(raw(item, 'Price'), quantity))]))
    services.write(detail_model, values, actor=actor, apply_effects=False)
    context = SourceDocumentContext.objects.get(entity=head._meta.label, object_id=head.pk)
    context.effects['outwork_origin'] = {'entity': item._meta.label, 'source': snapshot(item),
        'headers': [snapshot(value) for value in heads]}
    persist(context, actor)
    services.finish([head], actor)
    record(head, 'outwork_apply_adopted', {'exists': False}, actor, f'外协申请来源订单颜色：{item.pk}')
    return head


@transaction.atomic
def dispatch(item, actor, quantity, rolls, warehouse, unit, sheet_kind, happened_at, job_number):
    from . import source_services as services
    item = locked(item)
    from .source_execution_state import require_available
    require_available(item)
    table = 'GrayOut' if item.SOURCE_TABLE == 'OutWorkApplyDetail' else 'SemiOut'
    head_model, detail_model = rows(table, 'erp_warehouse').model, rows(table + 'Detail', 'erp_warehouse').model
    source_heads = list(matching(rows(item.SOURCE_TABLE.removesuffix('Detail')), SheetSeries=raw(item, 'SheetSeries')).order_by('pk'))
    header = {'_entry': table + 'Work', 'old_sheet_date': happened_at,
        'old_sheet_kind': sheet_kind, 'old_ware_house_id': warehouse, 'old_stock_unit': unit,
        'old_customer_id': raw(item, 'CustomerID')}
    if table == 'GrayOut':
        header['old_fact_id'] = raw(source_heads[0], 'FactID') if len(source_heads) == 1 else None
    head = services.write(head_model, header, actor=actor, apply_effects=False)
    values = copy_values(item, detail_model, ['SheetSeries', 'DetailNo', 'AssignedNo', 'Rolls', 'WeightQty', 'Amount'])
    values.update(source_parent_1=head, old_job_sheet_no=job_number)
    if table == 'GrayOut':
        values['old_gray_id'] = raw(item, 'ProdID')  # 原GrayOutWorkDetail明确GrayID AS ProdID。
    values.update(dict(store_value(detail_model(), key, value) for key, value in [
        ('WeightQty', quantity), ('Rolls', rolls), ('Amount', product(raw(item, 'Price'), quantity))]))
    detail = services.write(detail_model, values, actor=actor, apply_effects=False)
    context = SourceDocumentContext.objects.get(entity=head._meta.label, object_id=head.pk)
    context.effects['outwork_dispatch_origin'] = {'entity': item._meta.label, 'source': snapshot(item),
        'headers': [snapshot(value) for value in source_heads], 'line_id': detail.pk}
    persist(context, actor)
    services.finish([head], actor)
    record(head, 'outwork_dispatch', {'exists': False}, actor, f'实际发外采用申请明细：{item._meta.label}/{item.pk}')
    from .source_outwork_followup import movement
    movement(item,head,actor,'dispatch',happened_at,'外协实际发出')
    return head


@transaction.atomic
def receive_product(item, actor, quantity, rolls, warehouse, unit, sheet_kind, happened_at, job_number):
    from . import source_services as services
    item = locked(item)
    from .source_execution_state import require_available
    require_available(item)
    model = rows('ProdIn', 'erp_warehouse').model
    values = copy_values(item, model, ['SheetSeries', 'SheetNo', 'SheetDate', 'SheetKind', 'Rolls', 'WeightQty', 'Amount', 'Total', 'JobSheetNo'])
    values.update(_entry='ProdInWork', old_sheet_date=happened_at, old_sheet_kind=sheet_kind,
        old_ware_house_id=warehouse, old_stock_unit=unit, old_job_sheet_no=job_number)
    if item.SOURCE_TABLE == 'GrayOutDetail':
        values['old_prod_id'] = raw(item, 'GrayID')
    values.update(dict(store_value(model(), key, value) for key, value in [
        ('WeightQty', quantity), ('Rolls', rolls), ('Amount', product(raw(item, 'Price'), quantity)),
        ('Total', product(raw(item, 'Price'), quantity))]))
    target = services.write(model, values, actor=actor, apply_effects=False)
    context = SourceDocumentContext.objects.get(entity=target._meta.label, object_id=target.pk)
    context.effects['outwork_receipt_origin'] = {'entity': item._meta.label, 'source': snapshot(item)}
    persist(context, actor)
    services.finish([target], actor)
    record(target, 'outwork_receipt', {'exists': False}, actor, f'实际外协回货采用发出明细：{item._meta.label}/{item.pk}')
    from .source_outwork_followup import movement
    movement(item,target,actor,'receipt',happened_at,'外协实际回货')
    return target
