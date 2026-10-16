"""刷卡删除触发器、班次校验及独立删除维护过程。"""
from datetime import timedelta
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from .business import locked, record, snapshot
from .source_business_updates import matching, update_rows
from .source_context import SourceBusinessParameter
from .source_stock_services import raw
from .source_execution_state import active
import re


def rows(name, module='erp_production'):
    return active(apps.get_model(module + '.SourceDye' + name).objects.all())


def change(query, values, actor, procedure):
    update_rows(query, values, actor, 'work_delete_reverse', procedure)


def same_process(query, item):
    number = raw(item, 'ProcessNo')
    return matching(query, JobSheetNo=raw(item, 'JobSheetNo'), ProcessID=raw(item, 'ProcessID')).filter(
        old_process_no=number) if number is not None else query.none()


def status(item):
    value = raw(item, 'Status')
    if value is None:return None
    value=value.strip() or '0'
    return int(value) if re.fullmatch(r'[+-]?[0-9]+',value) else value


def remove_children(query, actor, procedure):
    for child in query.order_by('pk'):
        child = locked(child)
        # 原行留档；新增关联行按原过程删除，两者都记录实际命中对象。
        historical = child.legacy_id is not None or child.source_batch_id is not None
        record(child, 'work_delete_keep_source' if historical else 'work_delete_child', snapshot(child), actor, procedure)
        if not historical:
            child.delete()


def joined_names(work):
    workers, teams = [], []
    for value in work:
        shifts = list(matching(rows('PShift', 'erp_base'), ShiftID=raw(value, 'ShiftID'))) or [None]
        employees = list(matching(rows('HEmployee', 'erp_base'), EmpID=raw(value, 'EmpID'))) or [None]
        for shift in shifts:
            for employee in employees:
                if shift is not None and raw(shift, 'Name') is not None:
                    teams.append(raw(shift, 'Name'))
                if employee is not None and raw(employee, 'Name') is not None:
                    workers.append(raw(employee, 'Name'))
    return ';'.join(workers) if workers else None, ';'.join(teams) if teams else None


def prepare_delete(item, actor):
    # 原表靠业务码连接；Django附加外键不能把原可执行删除变成PROTECT错误。
    for job in matching(rows('JobSheet'), SheetNo=raw(item, 'JobSheetNo')).order_by('pk'):
        locked(job)
    for table, fields in [('JobShiftEmp', ['source_parent_1', 'source_parent_2']), ('WProcessStep', ['source_parent_1'])]:
        for field in fields:
            for child in rows(table).filter(**{field: item}).order_by('pk'):
                child = locked(child)
                before = snapshot(child)
                setattr(child, field, None)
                child.save(update_fields=[field])
                record(child, 'work_delete_unlink', before, actor, '撤回刷卡，仅解除Django附加外键；全部原字段和旧erpID保留')


def trigger_removed(item, actor, retain_children=False):
    if item.SOURCE_TABLE != 'WProcess':
        return
    procedure = 'WProcess_DELETE'
    survivors = same_process(rows('WProcess'), item)
    latest = survivors.order_by(F('old_create_date').desc(nulls_last=True), '-pk').first()
    workers, teams = joined_names(survivors.order_by('pk'))
    for job in matching(rows('JobSheet'), SheetNo=raw(item, 'JobSheetNo')).order_by('pk'):
        job = locked(job)
        processes = matching(rows('JobProcess'), SheetSeries=raw(job, 'SheetSeries'))
        active = [p for p in processes if status(p) not in [None, 0] and raw(p, 'ProcessNo') is not None]
        before_max = max((raw(p, 'ProcessNo') for p in active), default=None)
        target = matching(processes, ProcessID=raw(item, 'ProcessID')).filter(old_process_no=raw(item, 'ProcessNo')) if raw(item, 'ProcessNo') is not None else processes.none()
        if latest is None:
            values = dict.fromkeys(['StartTime', 'EndTime', 'WPWorker', 'WProcessNo', 'MachineID', 'TeamName'])
            values['Status'] = 0
        else:
            values = {'EndTime': None, 'WPWorker': workers, 'WProcessNo': raw(latest, 'WProcessNo')}
            if raw(item, 'StationID') in ['02', '05']:
                values['TeamName'] = teams
        change(target, values, actor, procedure)
        ordered = list(processes.order_by('old_process_no', 'pk'))
        active = [p for p in ordered if status(p) not in [None, 0] and raw(p, 'ProcessNo') is not None]
        current = active[-1] if active else None
        stations = [p for p in ordered if raw(p, 'StationID') is not None and raw(p, 'StationID').rstrip(' ') != '']
        # 原SQL用删除前最大工序号匹配ROW_NUMBER，并非下一工序号。
        following = next((p for index, p in enumerate(stations, 1) if index == before_max), None)
        if following is not None:
            change(rows('JobSheet').filter(pk=job.pk), {
                'CurrProcessID': None if current is None else raw(current, 'ProcessID'),
                'CurrStationID': None if current is None else raw(current, 'StationID'),
                'CurrProcessNo': None if current is None else raw(current, 'ProcessNo'),
                'NextProcessID': raw(following, 'ProcessID'), 'NextStationID': raw(following, 'StationID')}, actor, procedure)
    children = same_process(rows('JobShiftEmp'), item)
    if not retain_children:remove_children(matching(children, ShiftID=raw(item, 'ShiftID'), WProcessNo=raw(item, 'WProcessNo')), actor, procedure)


def check_shift_delete(item, now):
    local = timezone.localtime(now)
    shift = raw(item, 'ClassID')
    if shift in ['03', '04']:
        start = local.replace(hour=8 if shift == '03' else 20, minute=0, second=0, microsecond=0)
        if shift == '04' and local.hour < 8:
            start -= timedelta(days=1)
        end = start + timedelta(hours=12)
        work = matching(rows('WProcess'), WProcessNo=raw(item, 'WProcessNo'), JobSheetNo=raw(item, 'JobSheetNo'), ClassID=shift)
        if not work.filter(old_end_time__gte=start, old_end_time__lt=end).exists():
            raise ValidationError({'shift': '只能删除当前白班产量！' if shift == '03' else '只能删除当前晚班产量！'})
        if local > end:
            raise ValidationError({'shift': '已经下班不能删除！'})
        if local < start:
            raise ValidationError({'shift': '白班未到上班时间' if shift == '03' else '夜班未到上班时间'})
    if raw(item, 'StationID') == '06':
        latest = matching(same_process(rows('WProcess'), item), StationID='06').order_by(F('old_end_time').desc(nulls_last=True), '-pk').first()
        if latest is not None and raw(latest, 'WProcessNo') is not None and raw(item, 'WProcessNo') is not None and raw(latest, 'WProcessNo').rstrip(' ').upper() != raw(item, 'WProcessNo').rstrip(' ').upper():
            raise ValidationError({'source': '请先删除最新一条染色状态产量！'})


def maintain_removed(item, actor, retain_children=False):
    procedure = 'Sp_MaintainForWProcessDel'
    if not retain_children:
        for table in ['JobShiftEmp', 'WProcessStep']:
            remove_children(matching(rows(table), WProcessNo=raw(item, 'WProcessNo')), actor, procedure)
    for job in matching(rows('JobSheet'), SheetNo=raw(item, 'JobSheetNo')).order_by('pk'):
        job = locked(job)
        processes = matching(rows('JobProcess'), SheetSeries=raw(job, 'SheetSeries'))
        values = {'EndTime': None, 'Status': 0}
        if raw(item, 'ProcessID') not in ['GX07', 'GX16']:
            values.update(StartTime=None, WProcessNo=None, WPWorker=None)
        target = matching(processes, ProcessID=raw(item, 'ProcessID')).filter(old_process_no=raw(item, 'ProcessNo')) if raw(item, 'ProcessNo') is not None else processes.none()
        change(target, values, actor, procedure)
        candidates = [p for p in processes.order_by('old_process_no', 'pk') if status(p) not in [None, 0, 4]
            and raw(p, 'ProcessNo') is not None and raw(item, 'ProcessNo') is not None and raw(p, 'ProcessNo') != raw(item, 'ProcessNo')]
        current = candidates[-1] if candidates else None
        if current is None or raw(current, 'ProcessNo') <= 0:
            values = dict.fromkeys(['CurrProcessID', 'CurrProcessNo', 'CurrStationID', 'NextProcessID', 'NextStationID',
                                   'SumProcessRolls', 'SumProcessLengthQty', 'SumProcessWeightQty'])
            values['SheetStatus'] = 0
        else:
            survivors = same_process(rows('WProcess'), item)
            if raw(item, 'WProcessNo') is not None and any(raw(p, 'WProcessNo') is not None
                    and raw(p, 'WProcessNo').rstrip(' ').upper() != raw(item, 'WProcessNo').rstrip(' ').upper()
                    and status(p) not in [None, 0] for p in survivors):
                continue
            following = processes.filter(old_process_no=raw(current, 'ProcessNo') + 1).order_by('pk').last()
            parameter = SourceBusinessParameter.objects.filter(name='EndProcessID').first()
            end_ids = '' if parameter is None or parameter.value is None else parameter.value
            finished = raw(current, 'ProcessID') is not None and (raw(current, 'ProcessID') + ';').upper() in end_ids.upper()
            values = {'CurrProcessID': raw(current, 'ProcessID'), 'CurrProcessNo': raw(current, 'ProcessNo'),
                'CurrStationID': raw(current, 'StationID'), 'NextProcessID': None if following is None else raw(following, 'ProcessID'),
                'NextStationID': None if following is None else raw(following, 'StationID'), 'SheetStatus': 10 if finished else 0}
        change(rows('JobSheet').filter(pk=job.pk), values, actor, procedure)


@transaction.atomic
def delete_shift_record(item, actor, mode, reason):
    from . import source_services
    item = locked(item)
    check_shift_delete(item, timezone.now())
    record(item, 'shift_delete_requested', snapshot(item), actor, reason + '；模式=' + mode)
    source_services.delete_documents(type(item).objects.filter(pk=item.pk), actor)
    if mode == 'trigger_then_maintenance':
        maintain_removed(item, actor)
