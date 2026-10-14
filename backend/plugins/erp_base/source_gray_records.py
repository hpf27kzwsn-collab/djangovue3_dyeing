"""坯料实际细码单位和工卡领用对应，按明确收料及细码归属回写。"""
from django.apps import apps
from django.db.models.functions import Upper, RTrim
from .business import locked, persist
from .source_stock_services import raw, detail_rows
from .source_workflow_services import apply_changes


def matching(query, field, value):
    return query.none() if value is None else query.alias(match=Upper(RTrim(field))).filter(match=value.rstrip(' ').upper())


def refresh(item, context, actor):
    records = apps.get_model('erp_warehouse.SourceDyeGrayInRecord')
    if item.SOURCE_TABLE == 'GrayIn':
        for line in detail_rows(item, 'GrayInDetail'):
            for tag in records.objects.filter(source_parent_1=line).order_by('pk'):
                apply_changes(locked(tag), {'GUnit': raw(item, 'StockUnit')}, actor, 'gray_receipt_unit')
        return
    jobs = apps.get_model('erp_production.SourceDyeJobSheet')
    job_records = apps.get_model('erp_production.SourceDyeJobGrayRecord')
    outgoing = apps.get_model('erp_warehouse.SourceDyeGrayOutRecord')
    unresolved = []
    for line in detail_rows(item, 'GrayOutDetail'):
        number = raw(line, 'JobSheetNo')
        if number in [None, '']:
            continue
        job_matches = matching(jobs.objects.all(), 'old_sheet_no', number)
        for job in job_matches.order_by('pk'):
            allocated = matching(job_records.objects.filter(source_parent_1=job), 'old_rece_sheet_no', raw(line, 'ReceSheetNo'))
            for output in outgoing.objects.filter(source_parent_1=line).order_by('pk'):
                selected = matching(allocated, 'old_gray_bar_code', raw(output, 'BarCode'))
                for allocation in selected.order_by('pk'):
                    apply_changes(locked(allocation), {'AssignedNo': raw(line, 'AssignedNo')}, actor, 'gray_job_record_assignment')
                tags = matching(records.objects.all(), 'old_rece_sheet_no', raw(line, 'ReceSheetNo'))
                tags = matching(tags, 'old_bar_code', raw(output, 'BarCode'))
                # 条码可重复，实际出库细码号明确时必须同时匹配，避免把另一箱回写为本次领用。
                if raw(output, 'RollNo') not in [None, '']:
                    tags = matching(tags, 'old_roll_no', raw(output, 'RollNo'))
                if not selected.exists():
                    unresolved.append({'outgoing_record': output.pk, 'job': job.pk,
                                       'reason': '没有明确对应的工卡细码，保留原出库细码及原值'})
                    continue
                for tag in tags.order_by('pk'):
                    apply_changes(locked(tag), {'AssignedNo': raw(line, 'AssignedNo'),
                        'JobSheetNo': raw(job, 'SheetSeries')}, actor, 'gray_receipt_assignment')
    context.effects = {**context.effects, 'gray_record_unresolved': unresolved}
    persist(context, actor)
