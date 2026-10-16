"""对色、疵布入库及刷卡原触发规则；历史来源不自动重演。"""
from plugins.erp_base.source_provenance import is_historical
from datetime import datetime
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db.models import Sum, F
from django.utils import timezone
from .business import persist, record, snapshot
from .source_business_updates import matching, update_rows
from .source_stock_services import raw
from .source_context import SourceDocumentContext
from .source_entry_services import entry_for


def rows(table, module='erp_quality'):
    from .source_execution_state import active
    return active(apps.get_model(module + '.SourceDye' + table).objects.all())


def change(query, values, actor):
    update_rows(query, values, actor, 'original_quality_flow', '按当前原对色、疵布及生产触发规则回写')


def clear_staff(item):
    context = SourceDocumentContext.objects.filter(entity=item._meta.label, object_id=item.pk).first()
    if context is not None:
        rows('ColorShiftEmp', 'erp_production').filter(pk__in=context.effects.get('color_staff', [])).delete()
        context.effects['color_staff'] = []
        context.save(update_fields=['effects'])


def coloring(item, actor):
    curve = matching(rows('PDyeCurveDetail', 'erp_base'), CurveID=raw(item, 'CurveID'))
    step = matching(curve, DyeProcessID=raw(item, 'DyeProcessID')).order_by('-old_step_no', '-pk').first()
    total = None if step is None or raw(step, 'StepNo') is None else curve.filter(
        old_step_no__lte=raw(step, 'StepNo')).aggregate(value=Sum('old_default_value'))['value']
    change(matching(rows('ColoringCheck'), WProcessNo=raw(item, 'WProcessNo'), JobSheetNo=raw(item, 'JobSheetNo')),
           {'RealValue': total}, actor)
    clear_staff(item)
    staff = rows('ColorShiftEmp', 'erp_production').model
    ids = []
    for member in matching(rows('PShiftEmp', 'erp_base'), ShiftID=raw(item, 'ShiftID')).order_by('pk'):
        value = persist(staff(old_job_sheet_no=raw(item, 'JobSheetNo'), old_shift_id=raw(item, 'ShiftID'),
            old_emp_id=raw(member, 'EmpID'), old_process_id=raw(item, 'ProcessID'), old_wprocess_no=raw(item, 'WProcessNo')), actor)
        ids.append(value.pk)
        record(value, 'color_staff_created', {'exists': False}, actor, f'对色记录{item.pk}；班组原行{member.pk}')
    context, _ = SourceDocumentContext.objects.get_or_create(entity=item._meta.label, object_id=item.pk)
    context.effects['color_staff'] = ids
    persist(context, actor)


def work_record(item, created, actor):
    work = rows('WProcess', 'erp_production')
    number, job, station = (raw(item, key) for key in ['WProcessNo', 'JobSheetNo', 'StationID'])
    targets = matching(work, WProcessNo=number, JobSheetNo=job)
    if station == '06' and matching(work, JobSheetNo=job, StationID='06').count() > 1 and raw(item, 'DyeState') not in ['1', '6']:
        source = matching(work, JobSheetNo=job, StationID='06').filter(old_process_no=raw(item, 'ProcessNo'),
            old_dye_state__in=['1', '6']).exclude(old_wprocess_no=number).order_by(F('old_start_time').desc(nulls_last=True), '-pk').first()
        change(targets, {'MachineID': None if source is None else raw(source, 'MachineID')}, actor)
    process = matching(rows('PProcess', 'erp_base'), ProcessID=raw(item, 'ProcessID')).order_by('pk').first()
    if station in ['01', '02', '08'] and process is not None and raw(process, 'IsCanAddWorkQty') and raw(process, 'InputQtyCheckWay') == 0:
        change(targets, {key: 0 for key in ['CurrRolls', 'CurrMeter', 'CurrKg', 'CurrVats', 'CurrEffirate', 'WorkQty']}, actor)
    end = raw(item, 'EndTime')
    if created and (end is None or timezone.localtime(end).replace(tzinfo=None) == datetime(1900, 1, 1)):
        change(matching(work, WProcessNo=number), {'EndTime': timezone.now()}, actor)


def saved(item, created, actor):
    if is_historical(item):
        return
    if item.SOURCE_TABLE == 'ColoringCheck':
        coloring(item, actor)
    elif item.SOURCE_TABLE == 'WProcess':
        work_record(item, created, actor)
    elif item.SOURCE_TABLE == 'DefectiveInDetail' and created:
        job, rolls = raw(item, 'JobSheetNo'), raw(item, 'Rolls')
        if job is not None and job.rstrip(' ') and rolls is not None and rolls > 0 and matching(
                rows('DefectiveIn'), SheetSeries=raw(item, 'SheetSeries')).exists():
            change(matching(rows('JobSheet', 'erp_production'), SheetNo=job),
                   {'CurrProcessID': '疵布入库处理', 'SheetStatus': 9}, actor)
    if item.SOURCE_TABLE in ['ColoringCheck', 'WProcess']:
        item.refresh_from_db()


def removing(item):
    if item.SOURCE_TABLE == 'WDefect' and entry_for(item) in ['WDefectJudgeBack', 'WDefectJudgeInterior']:
        if matching(rows('JobSheet', 'erp_production'), LossStr=raw(item, 'SheetNo')).exists():
            raise ValidationError({'source': '原评审规则：已根据此评审单开回修卡，不能删除。'})
    if item.SOURCE_TABLE == 'ColoringCheck':
        clear_staff(item)


def removed(item, actor):
    if item.SOURCE_TABLE != 'DefectiveInDetail':
        return
    jobs = matching(rows('JobSheet', 'erp_production'), SheetNo=raw(item, 'JobSheetNo'))
    for job in jobs.order_by('pk'):
        change(type(job).objects.filter(pk=job.pk), {'SheetStatus': 0, 'CurrProcessID': ''}, actor)
        refresh_current_process(job, actor)


def refresh_current_process(job, actor):
    # Sp_JobProcessUpdate_Curr1，包装开工与疵布删除共用。
    if matching(rows('ProdIn', 'erp_warehouse'), JobSheetNo=raw(job, 'SheetNo')).exists():
        return
    processes = list(matching(rows('JobProcess', 'erp_production'), SheetSeries=raw(job, 'SheetSeries')).order_by('old_process_no', 'pk'))
    from .source_workflow_services import process_status
    done = [p for p in processes if process_status(p) == 1 and raw(p, 'ProcessNo') is not None]
    if not done:
        pending = next((p for p in processes if process_status(p) != 1), None)
        values = {'CurrProcessID': None, 'CurrProcessNo': None, 'CurrStationID': None,
            'NextProcessID': None if pending is None else raw(pending, 'ProcessID'),
            'NextStationID': None if pending is None else raw(pending, 'StationID')}
    else:
        last = done[-1]
        later = [p for p in processes if raw(p, 'ProcessNo') is not None and raw(p, 'ProcessNo') > raw(last, 'ProcessNo')]
        active = [p for p in later if process_status(p) in [4, 5]]
        pending = next((p for p in later if process_status(p) == 0), None)
        current = active[-1] if active else last
        end = raw(current, 'EndTime')
        values = {'CurrProcessID': raw(current, 'ProcessID'), 'CurrProcessNo': raw(current, 'ProcessNo'),
            'CurrStationID': raw(current, 'StationID'),
            'NextProcessID': raw(current, 'ProcessID') if active else None if pending is None else raw(pending, 'ProcessID'),
            'PlanDate': raw(current, 'StartTime') if end is None or timezone.localtime(end).replace(tzinfo=None) == datetime(1900, 1, 1) else end}
    change(type(job).objects.filter(pk=job.pk), values, actor)

def defective_balance(item):
    number = raw(item, 'DetailNo')
    incoming = matching(rows('DefectiveInDetail'), DetailNo=number)
    outgoing = matching(rows('DefectiveOutDetail'), DefectiveInDetailNo=number)
    result = {}
    for old in ['Rolls', 'WeightQty', 'LengthQty']:
        values = list(incoming.values_list(incoming.model.SOURCE_FIELDS[old], flat=True))
        values += [-value if value is not None else None for value in outgoing.values_list(outgoing.model.SOURCE_FIELDS[old], flat=True)]
        values = [value for value in values if value is not None]
        result[old] = sum(values) if values else None
    result['old_stock_visible'] = any(result[key] is not None and result[key] > 0 for key in ['Rolls', 'WeightQty'])
    result['incoming_ids'] = list(incoming.values_list('pk', flat=True))
    result['outgoing_ids'] = list(outgoing.values_list('pk', flat=True))
    return result
