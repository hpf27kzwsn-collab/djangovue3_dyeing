"""订单变更到工卡、调价到确价；保存触发与审核动作按原程序分别办理。"""
from plugins.erp_base.source_provenance import is_historical
from datetime import datetime
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from .business import locked
from .source_stock_services import raw
from .source_business_updates import matching, update_rows


def rows(table, module='erp_sales'):
    from .source_execution_state import active
    return active(apps.get_model(module + '.SourceDye' + table).objects.all())


def change(query, values, actor):
    update_rows(query, values, actor, 'sales_source_update', '采用旧订单/调价程序的明确关联字段')


def numeric_color(value):
    from .source_foundation_functions import extract_number
    return extract_number(value,10)


def same_numeric_color(query, value):
    from .source_foundation_functions import number_matches
    return number_matches(query,value,10)


def order_saved(item, fields, actor):
    table = item.SOURCE_TABLE
    combinations = rows('JobCombineOrder', 'erp_production')
    jobs = rows('JobSheet', 'erp_production')
    if table == 'OrderMain':
        updates = {old: raw(item, old) for old in ['CustomerID', 'CustSelfNo'] if old in fields}
        if not updates:
            return
        for color in matching(rows('OrderColor'), SheetSeries=raw(item, 'SheetSeries')).order_by('pk'):
            key = raw(color, 'CheckNo')
            change(matching(combinations, CheckNo=key), updates, actor)
            if 'CustomerID' in updates:
                change(matching(jobs, CheckNo=key), {'CustomerID': updates['CustomerID']}, actor)
    elif table == 'OrderColor':
        # 原触发器通过 OrderMain 内连接取值；孤立原行保留，不制造父单。
        if not matching(rows('OrderMain'), SheetSeries=raw(item, 'SheetSeries')).exists():
            return
        key = raw(item, 'CheckNo')
        combo = matching(combinations, CheckNo=key)
        updates = {old: raw(item, old) for old in [
            'OrderQty', 'Remarks', 'ColorRemarks', 'CustFabricName', 'ProdID', 'ColorNum', 'ContractNo'] if old in fields}
        change(combo, updates, actor)
        job_updates = {target: raw(item, old) for old, target in [
            ('Remarks', 'Remarks'), ('CustFabricName', 'CustSelfProduct'), ('ProdID', 'ProdID')] if old in fields}
        change(matching(jobs, CheckNo=key), job_updates, actor)
        if 'ColorRemarks' in fields:
            # 原 SELECT 变量只留下一个工卡；这里逐个实际关联工卡采用全部成员备注。
            series = list(combo.values_list('old_sheet_series', flat=True).distinct())
            for code in series:
                members = matching(combinations, SheetSeries=code).order_by('old_check_no', 'pk')
                remarks = [member.old_color_remarks for member in members if member.old_color_remarks is not None]
                combined = ','.join(remarks) if remarks else None
                for job in matching(jobs, SheetSeries=code):
                    change(matching(rows('GrayMaterialDetail', 'erp_warehouse'), JobSheetNo=raw(job, 'SheetNo')),
                           {'ColorRemarks': combined}, actor)


def adjustment_saved(item, actor):
    heads = matching(rows('PriceAdjust'), SheetSeries=raw(item, 'SheetSeries'))
    # 原主键唯一；原表历史身份与新库主键独立。明确排序使同码接续结果可重现。
    head = heads.order_by(F('old_start_date').desc(nulls_last=True), '-pk').first()
    values = {'AdjustPrice': raw(item, 'AdjustPrice'), 'JobSheetNo': raw(item, 'DetailNo'),
              'DateType': None if head is None else raw(head, 'DateType'),
              'StartDate': None if head is None else raw(head, 'StartDate')}
    change(same_numeric_color(rows('QuoteDetail'), raw(item, 'ColorNum')), values, actor)


def saved(item, data, created, actor):
    if item.SOURCE_TABLE in ['QuoteDetail','FixedPriceDetail']:
        from .source_quote_rules import saved as quote_saved
        quote_saved(item,data,created,actor)
    if is_historical(item):
        return
    fields = set(item.SOURCE_FIELDS) if created else {old for old, key in item.SOURCE_FIELDS.items() if key in data}
    if item.SOURCE_TABLE in ['OrderMain', 'OrderColor']:
        order_saved(item, fields, actor)
    elif item.SOURCE_TABLE == 'PriceAdjustDetail':
        adjustment_saved(item, actor)


def adjustment_audit(item, actor, approved):
    if item.SOURCE_TABLE != 'PriceAdjust' or is_historical(item):
        return
    for line in matching(rows('PriceAdjustDetail'), SheetSeries=raw(item, 'SheetSeries')).order_by('pk'):
        values = {'AdjustPrice': raw(line, 'AdjustPrice'), 'StartDate': raw(item, 'StartDate'), 'DateType': raw(item, 'DateType')} if approved else {
            # 原SQL DateType='' 写入tinyint字段，SQL Server隐式转换后的实际值为0。
            'AdjustPrice': 0, 'StartDate': timezone.make_aware(datetime(1900, 1, 1)), 'DateType': 0}
        change(matching(rows('QuoteDetail'), DetailNo=raw(line, 'QuoteDetailNo')), values, actor)


def removing(item):
    if item.SOURCE_TABLE in ['QuoteDetail','FixedPriceDetail']:
        from .source_quote_rules import removing as quote_removing
        quote_removing(item)
    if item.SOURCE_TABLE == 'OrderMain':
        for line in matching(rows('OrderColor'), SheetSeries=raw(item, 'SheetSeries')):
            if matching(rows('JobCombineOrder', 'erp_production'), CheckNo=raw(line, 'CheckNo'),
                        OrderSheetNo=raw(item, 'SheetNo')).exists():
                raise ValidationError({'source': '此订单已有对应开卡分配，按原订单入口规则不能删除。'})


def removed(item, actor):
    if item.SOURCE_TABLE != 'PriceAdjustDetail':
        return
    candidates = []
    for line in same_numeric_color(rows('PriceAdjustDetail'), raw(item, 'ColorNum')):
        for head in matching(rows('PriceAdjust'), SheetSeries=raw(line, 'SheetSeries')):
            at = raw(head, 'StartDate')
            candidates.append((at is not None, at, head.pk, line.pk, line))
    previous = max(candidates, key=lambda row: row[:4])[-1] if candidates else None
    values = {'AdjustPrice': None if previous is None else raw(previous, 'AdjustPrice'),
              'JobSheetNo': None if previous is None else raw(previous, 'DetailNo')}
    targets = matching(same_numeric_color(rows('QuoteDetail'), raw(item, 'ColorNum')), JobSheetNo=raw(item, 'DetailNo'))
    # 旧删除触发器不回退 DateType/StartDate；不能伪称恢复审核前快照。
    change(targets, values, actor)


@transaction.atomic
def close_expired(item, actor, as_of):
    if item.SOURCE_TABLE != 'OrderMain':
        raise ValidationError({'source': '超期结单仅适用于原销售订单。'})
    item = locked(item)
    at = raw(item, 'SheetDate')
    if at is None or (as_of - timezone.localtime(at).date()).days <= 180 or raw(item, 'SheetStatus') not in [None, 0]:
        raise ValidationError({'old_sheet_status': '原条件为单据日期超过180天且状态为空或0。'})
    change(type(item).objects.filter(pk=item.pk), {'SheetStatus': 10}, actor)
    item.refresh_from_db()
    return item
