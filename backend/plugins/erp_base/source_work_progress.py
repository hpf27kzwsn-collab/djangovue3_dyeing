"""普通报工保存接入计划工序、合卡及质量；原行和重复报工均保留。"""
from django.db.models import F
from django.utils import timezone
from datetime import datetime
from .source_phase3_operations import source
from .source_stock_services import raw
from .source_business_updates import matching,update_rows
from .source_provenance import is_historical
from .source_continuation import save_effect,origin

INPUTS={'old_job_sheet_no','old_process_no','old_process_id','old_start_time','old_end_time','old_status','old_machine_id','old_station_id','old_emp_id','old_shift_id','old_curr_kg','old_curr_rolls'}


def actual_time(value):
    return value is not None and timezone.localtime(value).replace(tzinfo=None)!=datetime(1900,1,1)


def refresh(work,actor,remember=True):
    from .source_work_delete import same_process,joined_names
    jobs=matching(source('JobSheet'),SheetNo=raw(work,'JobSheetNo')).order_by('pk')
    # 原JOIN的NULL不代表同一张卡/同一工序；缺码原行留档，不能关联全部空码记录。
    if raw(work,'JobSheetNo') in [None,''] or raw(work,'ProcessID') is None or raw(work,'ProcessNo') is None:
        jobs=jobs.none()
    works=same_process(source('WProcess'),work).order_by('old_create_date','pk')
    all_works=list(works);workers,teams=joined_names(all_works)
    # 具体轮次以实际原行定位；多次报工只更新相同工卡/工序号/工序的计划行。
    latest=works.order_by(F('old_create_date').desc(nulls_last=True),'-pk').first()
    result=[]
    for job in jobs:
        if is_historical(job):continue
        plans=matching(source('JobProcess'),SheetSeries=raw(job,'SheetSeries'),ProcessID=raw(work,'ProcessID')).filter(old_process_no=raw(work,'ProcessNo'))
        for plan in plans.order_by('pk'):
            if is_historical(plan):continue
            starts=[raw(row,'StartTime') for row in all_works if actual_time(raw(row,'StartTime'))]
            ends=[raw(row,'EndTime') for row in all_works if actual_time(raw(row,'EndTime'))]
            explicit=None if latest is None else raw(latest,'Status')
            plan_status='1' if ends else explicit if explicit in ['4','5'] else '4' if starts else '0'
            values={'StartTime':min(starts) if starts else None,'EndTime':max(ends) if ends else None,
                'Status':plan_status,'WPWorker':workers,'TeamName':teams,
                'WProcessNo':None if latest is None else raw(latest,'WProcessNo'),'MachineID':None if latest is None else raw(latest,'MachineID')}
            update_rows(type(plan).objects.filter(pk=plan.pk),values,actor,'work_plan_progress','普通报工保存/撤回重建本工序实绩')
            plan.refresh_from_db();result.append(plan.pk)
            from .source_context import SourceDocumentContext
            contexts=SourceDocumentContext.objects.filter(entity=model_label('dyeCheckout'),effects__quality_rebuild_origin__process__source__id=plan.pk)
            for context in contexts:
                from .source_phase3_operations import model
                row=model('dyeCheckout').objects.get(pk=context.object_id)
                save_effect(row,'quality_replaced',{'active':True,'source_process_id':plan.pk,'at':timezone.now()},actor,'普通报工变化重建质量；前版原行留档')
            from .source_auto_combine import automatic_sync,choose_route
            # 明确有合卡配置才调用原自动合卡；没有配置也要生成本卡染色质量来源。
            routes=choose_route(plan,False,timezone.now())
            if routes['targets'] or any(row['issue'] for row in routes['rows']):
                automatic_sync(plan,actor,raw(plan,'MachineID'),2,False,timezone.now(),timezone.now(),
                    '普通报工保存自动同步',completion_status=int(plan_status),process_variable=raw(plan,'ProcessID'))
            else:
                if ends:
                    from .source_dye_rebuild import rebuild
                    rebuild(plan,actor,1,timezone.now(),'普通报工完成生成出缸质量',process_variable=raw(plan,'ProcessID'))
        from .source_quality_flow import refresh_current_process
        refresh_current_process(job,actor)
    if remember:
        save_effect(work,'work_plan_progress',{'work':origin(work),'work_ids':[row.pk for row in all_works],
            'plan_ids':result,'unmatched':not result,'at':timezone.now()},actor,'普通报工自动进度；未匹配来源原行保留')


def model_label(table):
    from .source_phase3_operations import model
    return model(table)._meta.label


def saved(item,data,creating,actor,previous=None):
    if item.SOURCE_TABLE!='WProcess' or is_historical(item) or (not creating and not INPUTS.intersection(data)):return
    if previous is not None and any(previous.SOURCE_FIELDS[k] in data and raw(previous,k)!=raw(item,k) for k in ['JobSheetNo','ProcessID','ProcessNo']):
        refresh(previous,actor)
    refresh(item,actor)
