"""明确翻译工卡保存、工序进度和成品入库的上游回写。"""
from plugins.erp_base.source_provenance import is_historical
from django.apps import apps
from django.db.models import Sum
from .business import locked, persist, record, snapshot
from .source_context import SourceBusinessParameter
from .source_entry_services import entry_for
from .source_stock_services import raw


JOB_KIND_ENTRIES = {'JobSheet', 'PrintJobSheet', 'SaleJobSheet', 'TwiJobSheet'}


def process_status(line):
    value = raw(line, 'Status')
    return 0 if value is None or value.strip() == '' else int(value)


def apply_changes(item, values, actor, action):
    changed = {item.SOURCE_FIELDS[key]: value for key, value in values.items() if raw(item, key) != value}
    if changed:
        before = snapshot(item)
        for key, value in changed.items():
            setattr(item, key, value)
        persist(item, actor)
        record(item, action, before, actor, '按明确旧工卡过程回写')


def refresh_job(job, actor):
    if is_historical(job):
        return
    job = locked(job)
    entry = entry_for(job)
    if entry in JOB_KIND_ENTRIES:
        from .source_phase3_operations import source,change
        from .source_business_updates import matching
        targets=matching(source('JobSheet'),SheetSeries=raw(job,'SheetSeries'))
        change(targets.filter(old_sheet_kind=40),{'JobKindID':'03'},actor)
        change(targets.filter(old_job_kind_id__isnull=True),{'JobKindID':'01'},actor)
    if entry == 'JobSheet':
        # 原保存动作明确调用此过程，不能另用父ID及工序号排序缩小其原LIKE范围。
        from .source_phase4_operations import progress
        progress('Sp_JobProcessUpdate',raw(job,'SheetSeries'),actor)
    job.refresh_from_db()
    return job


def refresh_product_inbound(item, actor):
    number = raw(item, 'JobSheetNo')
    if number is None:
        return
    job_model = apps.get_model('erp_production.SourceDyeJobSheet')
    jobs = list(job_model.objects.filter(old_sheet_no__iexact=number).order_by('pk'))
    if not jobs:
        return
    from .source_execution_state import active
    inbound = active(apps.get_model('erp_warehouse.SourceDyeProdIn').objects.filter(old_job_sheet_no__iexact=number))
    parameter = SourceBusinessParameter.objects.filter(name='JobReProdIn').first()
    # 原SELECT中的ISNULL作用于存在的参数行；没有参数行时变量仍为NULL并进入else。
    mode = None if parameter is None else '1' if parameter.value is None else parameter.value.rstrip(' ')
    rolls = inbound.aggregate(value=Sum('old_rolls'))['value']
    total = 0 if rolls is None else rolls  # 旧过程明确 ISNULL(SUM(Rolls),0)。
    for job in jobs:
        job = locked(job)
        planned = raw(job, 'PreRolls')
        planned = 0 if planned is None else planned
        if mode == '1':
            approved = inbound.filter(old_right_status=10)
            returned = approved.filter(old_sheet_kind=16).exists()
            received = approved.filter(old_sheet_kind__isnull=False).exclude(old_sheet_kind=16).exists()
            finished = not returned and received and total <= planned
        else:
            finished = planned <= total
        apply_changes(job, {'IsProdInFinished': finished}, actor, 'product_inbound_progress')


def refresh_chain(items, actor):
    for item in items:
        if is_historical(item):
            continue
        if item.SOURCE_TABLE == 'JobSheet':
            updated = refresh_job(item, actor)
            for old in ['JobKindID', 'NextProcessID', 'CurrProcessID']:
                setattr(item, item.SOURCE_FIELDS[old], raw(updated, old))
        elif item.SOURCE_TABLE == 'ProdIn':
            refresh_product_inbound(item, actor)
        elif item.SOURCE_TABLE in ['GrayOut', 'SemiOut']:
            from .source_stock_job_services import refresh
            refresh(item, actor)


def refresh_removed(item, actor):
    if item.SOURCE_TABLE == 'ProdIn':
        refresh_product_inbound(item, actor)
