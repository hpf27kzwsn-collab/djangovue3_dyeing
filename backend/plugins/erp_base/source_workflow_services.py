"""明确翻译工卡保存、工序进度和成品入库的上游回写。"""
from django.apps import apps
from django.db.models import Sum
from .business import locked, persist, record, snapshot
from .source_context import SourceBusinessParameter
from .source_entry_services import entry_for
from .source_stock_services import raw


JOB_KIND_ENTRIES = {'JobSheet', 'JobSheetQuery', 'PrintJobSheet', 'SaleJobSheet', 'TwiJobSheet'}


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
    if job.source_batch_id is not None or job.legacy_id is not None:
        return
    job = locked(job)
    entry = entry_for(job)
    if entry in JOB_KIND_ENTRIES:
        if raw(job, 'SheetKind') == 40:
            apply_changes(job, {'JobKindID': '03'}, actor, 'job_kind')
        elif raw(job, 'JobKindID') is None:
            apply_changes(job, {'JobKindID': '01'}, actor, 'job_kind')
    if entry != 'JobSheet' or raw(job, 'SheetStatus') not in [None, 0]:
        return job
    process = apps.get_model('erp_production.SourceDyeJobProcess')
    lines = list(process.objects.filter(source_parent_1=job).order_by('old_process_no', 'pk'))
    done = [line for line in lines if process_status(line) == 1]
    if not done:
        pending = [line for line in lines if process_status(line) != 1]
        values = {'NextProcessID': raw(pending[0], 'ProcessID') if pending else None}
    else:
        pending = [line for line in lines if process_status(line) == 0]
        values = {'NextProcessID': raw(pending[0], 'ProcessID') if pending else None,
                  'CurrProcessID': raw(done[-1], 'ProcessID')}
    apply_changes(job, values, actor, 'job_process_progress')
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
        if item.source_batch_id is not None or item.legacy_id is not None:
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
