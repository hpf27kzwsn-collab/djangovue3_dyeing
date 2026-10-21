"""包装条码、GX98开工与QC汇总。与破坏原始事实的旧触发行为差异见异常E44。"""
from plugins.erp_base.source_provenance import is_historical
import re
from datetime import datetime
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db.models import Count, Sum
from django.db import transaction
from django.utils import timezone
from .business import locked, persist
from .source_business_updates import matching, update_rows
from .source_stock_services import raw
from .source_entry_services import entry_for
from .source_sequences import SourceIdentitySequence


def rows(name, module='erp_warehouse'):
    from .source_execution_state import active
    return active(apps.get_model(module+'.SourceDye'+name).objects.all())


def change(query, values, actor):
    update_rows(query,values,actor,'packaging_flow','包装开工及本次记录回写；差异见E44')


def barcode(actor):
    prefix=timezone.localtime().strftime('%y%m%d')
    sequence,_=SourceIdentitySequence.objects.get_or_create(namespace='RecordYield.BarCode.'+prefix)
    sequence=locked(sequence)
    values=apps.get_model('erp_warehouse.SourceDyeRecordYield').objects.filter(old_bar_code__regex='^'+prefix+'[0-9]{5}$').values_list('old_bar_code',flat=True)
    sequence.last_number=max([sequence.last_number,*[int(value[-5:]) for value in values]])+1
    persist(sequence,actor)
    # 超过五位继续扩位，避免旧RIGHT(...,5)回绕为重复自动号码；手填重复码继续保留。
    return prefix+str(sequence.last_number).zfill(5)


def start_packing(item,actor):
    from .source_quality_flow import refresh_current_process
    jobs=matching(rows('JobSheet','erp_production'),SheetNo=raw(item,'JobSheetNo'))
    employee=matching(rows('HEmployee','erp_base'),EmpID=raw(item,'EmpID')).order_by('pk').first()
    for job in jobs.order_by('pk'):
        job=locked(job)
        process=matching(rows('JobProcess','erp_production'),SheetSeries=raw(job,'SheetSeries'),ProcessID='GX98').order_by('old_process_no','pk').first()
        if process is None or raw(process,'ProcessNo') is None or raw(process,'ProcessNo')<=0:
            continue
        process=locked(process)
        start=raw(process,'StartTime')
        if start is None or timezone.localtime(start).replace(tzinfo=None)==datetime(1900,1,1):
            change(matching(rows('JobProcess','erp_production'),SheetSeries=raw(job,'SheetSeries')).filter(old_process_no=raw(process,'ProcessNo')),
                {'StartTime':timezone.now(),'WPWorker':None if employee is None else raw(employee,'Name'),'Status':'1'},actor)
            refresh_current_process(job,actor)


def qc_totals(item,actor):
    codes=matching(rows('RecordYield'),BarCode=raw(item,'BarCode')).values_list('old_job_sheet_no',flat=True).distinct()
    for number in codes:
        source=matching(rows('RecordYield'),JobSheetNo=number)
        totals=source.aggregate(count=Count('old_job_sheet_no'),PDots=Sum('old_dots'),Pkg=Sum('old_kg'),
            PRolls=Count('old_bar_code'),PlengthQyt=Sum('old_yard'))
        count=totals.pop('count')
        if count>0:
            change(matching(rows('JobSheet','erp_production'),SheetNo=number),totals,actor)


def saved(item, created, actor):
    if item.SOURCE_TABLE!='RecordYield' or is_historical(item):
        return
    values={}
    if created and (raw(item,'BarCode') is None or raw(item,'BarCode').rstrip(' ')==''):
        values['BarCode']=barcode(actor)
    roll=raw(item,'RollNo')
    if roll is not None and re.fullmatch(r'\s*[+-]?[0-9]+\s*',roll) and -2147483648<=int(roll)<=2147483647:
        values['Scroll']=int(roll)
    if (raw(item,'JobSheetNo') or '') != (raw(item,'JobDetailNo') or ''):
        values['JobDetailNo']=raw(item,'JobSheetNo')
    change(type(item).objects.filter(pk=item.pk),values,actor)
    item.refresh_from_db()
    start_packing(item,actor)


def after_saved(item,actor):
    """原 AfterSaveSQL 在本次明细汇总完成后回写工卡。"""
    if item.SOURCE_TABLE=='RecordYield' and not is_historical(item) and entry_for(item) in ['QC_Record','QFQC_Record']:
        qc_totals(item,actor)


def removing(item):
    if item.SOURCE_TABLE=='RecordYield' and entry_for(item)=='WeighRecordYield' and matching(
            rows('ProdInRecord'),ProdBarCode=raw(item,'BarCode')).exists():
        raise ValidationError({'source':'原实称入口：此包装条码已有成品入库细码，不能删除。'})


@transaction.atomic
def adopt_gray_record(item, actor, source, at, reason):
    """Sp_RecordYieldQuery的字段采用，按明确原行替代有歧义的排序配对。"""
    from .source_gray_split_merge import require_active
    from .source_execution_state import require_available
    from .source_package_operations import effect
    from .source_operation_effects import change as field_change
    from .source_continuation import origin, save_effect
    item,source=locked(item),locked(source)
    require_available(item)
    require_active(source)
    before=origin(item)
    previous=effect(item,'package_gray_origin')
    changes=[]
    field_change(item,{'GrayWeight':raw(source,'WeightQty'),'GrayBarCode':raw(source,'GrayBarCode')},changes,actor,reason)
    save_effect(item,'package_gray_origin',{'state':'applied','mode':'explicit','package_before':before,
        'source':origin(source),'at':at,'reason':reason,'previous':previous,'changes':changes},actor,reason)
    item.refresh_from_db()
    return item


@transaction.atomic
def undo_gray_record(item, actor, at, reason):
    from .source_execution_state import require_available
    from .source_package_operations import effect
    from .source_operation_effects import restore
    from .source_continuation import save_effect
    item=locked(item);require_available(item)
    value=effect(item,'package_gray_origin')
    if value is None or value.get('mode')!='explicit' or value.get('state')!='applied':
        raise ValidationError({'source':'本包装没有可撤回的明确投坯采用；排序配对请从对应工卡撤回。'})
    restore(value['changes'],actor,reason)
    save_effect(item,'package_gray_origin',value['previous'] or {'state':'reversed','reversed_at':at,'reason':reason},actor,reason)
    item.refresh_from_db()
    return item
