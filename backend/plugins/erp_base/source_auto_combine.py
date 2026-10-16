"""原称料/排程合卡选路、工序同步与剩余染程步骤判断。"""
from datetime import timedelta
import re
from django.apps import apps
from django.db import transaction
from .business import locked
from .source_stock_services import raw
from .source_business_updates import matching, update_rows
from .source_continuation import save_effect, origin
from .source_job_flow import sync_combined_process
from .source_quality_flow import refresh_current_process


def rows(name,module='erp_production'):
    from .source_execution_state import active
    return active(apps.get_model(module+'.SourceDye'+name).objects.all())


def equal(left,right):
    return left is not None and right is not None and left.rstrip(' ').upper()==right.rstrip(' ').upper()


def choose_route(item, plan_have_time, as_of, query=rows):
    result={'report':'原自动合卡选路','rows':[],'sources':[],'notes':[], 'targets':[],'jobs':[],'step_processes':[]}
    jobs=matching(query('JobSheet','erp_production'),SheetSeries=raw(item,'SheetSeries')).order_by('pk')
    for job in jobs:
        from .source_card_reverse import require_current_plan
        require_current_plan(job)
        result['jobs'].append(job.pk)
        number=raw(job,'SheetNo');process=raw(item,'ProcessID');chosen=None;mode='schedule';candidates=[];process_id=None
        if any(equal(process,code) for code in ['G-06','G-07']):
            candidates=list(matching(query('StuffWeight','erp_production'),JobSheetNo=number,ProcessID=process).order_by('pk'))
            chosen=candidates[0] if candidates else None
            if chosen is not None:process_id=raw(chosen,'ProcessID')
            tokens=[] if chosen is None else (raw(chosen,'CombineSheetNos') or '').split('|')
            if not any(tokens):
                reverse_query=query('StuffWeight','erp_production')
                reverse_query=reverse_query.none() if number is None else reverse_query.filter(old_combine_sheet_nos__icontains=number)
                reverse=[row for row in reverse_query.order_by('pk')
                         if any(equal(token,number) for token in (raw(row,'CombineSheetNos') or '').split('|'))]
                candidates=reverse
                chosen=reverse[0] if reverse else None
                if chosen is not None:
                    process_id=raw(chosen,'ProcessID')
                    tokens=[token for token in (raw(chosen,'CombineSheetNos') or '').split('|') if not equal(token,number)]
                    tokens.append(raw(chosen,'JobSheetNo') or '')
            if chosen is not None and any(tokens) and raw(chosen,'ProcessID') not in [None,'']:
                mode='stuff';process_id=raw(chosen,'ProcessID')
        if mode=='schedule':
            candidates=[]
            schedules=matching(query('ProcessSchedule','erp_production'),JobSheetNo=number)
            schedules=schedules.none() if raw(item,'ProcessNo') is None else schedules.filter(old_process_no=raw(item,'ProcessNo'))
            for plan in schedules.order_by('pk'):
                if raw(plan,'CombineSheetNos') in [None,'']:continue
                definitions=list(matching(query('PProcess','erp_base'),ProcessID=raw(plan,'ProcessID')).order_by('pk'))
                delays=[raw(row,'DelayHours') for row in definitions] if definitions else [None]
                if not plan_have_time or any(raw(plan,'StartTime') is not None and raw(plan,'StartTime')>=as_of-timedelta(hours=0 if delay is None else float(delay)) for delay in delays):
                    candidates.append(plan)
            chosen=candidates[-1] if candidates else None
            tokens=[] if chosen is None else (raw(chosen,'CombineSheetNos') or '').split('|')
        result['step_processes'].append({'job_id':job.pk,'process_id':process_id})
        result['sources'].append({'job':origin(job),'mode':mode,'selected':None if chosen is None else origin(chosen),
            'candidate_ids':[row.pk for row in candidates]})
        for token in tokens:
            if token=='':continue
            entry={'source_job':number,'mode':mode,'token':token,'target_id':None,'candidate_ids':[],'issue':None}
            if mode=='schedule':
                parts=token.split(':',1)
                if len(parts)!=2 or re.fullmatch(r'\s*[+-]?[0-9]+\s*',parts[1]) is None:
                    entry['issue']='原卡号:工序号文本不能转换，原片段保留';result['rows'].append(entry);continue
                target_number,ordinal=parts[0],int(parts[1])
                if not -2147483648<=ordinal<=2147483647:
                    entry['issue']='原工序号超出SQL int范围，原片段保留';result['rows'].append(entry);continue
            else:
                target_number,ordinal=token,None
            targets=[]
            for target_job in matching(query('JobSheet','erp_production'),SheetNo=target_number).order_by('pk'):
                from .source_context import SourceDocumentContext
                if SourceDocumentContext.objects.filter(entity=target_job._meta.label,object_id=target_job.pk,effects__card_adoption__state='reversed').exists():
                    result['rows'].append({**entry,'job_id':target_job.pk,'issue':'此新拆合计划已撤回，原行仍保留'});continue
                process_query=matching(query('JobProcess','erp_production'),SheetSeries=raw(target_job,'SheetSeries'))
                process_query=matching(process_query,ProcessID=process_id) if mode=='stuff' else process_query.filter(old_process_no=ordinal)
                targets.extend(process_query.order_by('pk'))
            entry['candidate_ids']=[row.pk for row in targets]
            selected=targets[:1] if mode=='stuff' else targets
            if not selected:entry['issue']='原目标工卡或工序未匹配'
            for target in selected:
                if mode=='stuff' and (raw(target,'ProcessNo') is None or raw(target,'ProcessNo')<=0):
                    entry['issue']='原称料分支要求工序号大于0';continue
                result['targets'].append(target.pk)
                entry['target_id']=target.pk
            result['rows'].append(entry)
    if not result['jobs']:
        result['notes'].append('来源工序缺少当前工卡表头，原工序保留，可继续使用明确目标同步。')
    result['supplemental_rows']=[{'source_job_id':source['job']['source']['id'],'mode':source['mode'],
        'selected_source_id':None if source['selected'] is None else source['selected']['source']['id'],
        'candidate_ids':source['candidate_ids']} for source in result['sources']]
    result['notes'].append('无序TOP 1按记录ID最小、无序标量末值按记录ID最大明确选择；全部候选ID及未匹配片段保留。')
    return result


def initialize_current(job,actor,query=rows):
    """Sp_JobProcessUpdate_Curr的空进度分支，范围限于本次涉及工卡。"""
    if raw(job,'SheetStatus') not in [None,0] or raw(job,'CurrProcessID') not in [None,''] or raw(job,'NextProcessID') not in [None,'']:return
    from .source_workflow_services import process_status
    processes=list(matching(query('JobProcess','erp_production'),SheetSeries=raw(job,'SheetSeries')).order_by('pk'))
    done=[row for row in processes if process_status(row)==1 and raw(row,'ProcessNo') is not None]
    if not done:
        pending=next((row for row in processes if process_status(row)!=1),None)
        values={'NextProcessID':None if pending is None else raw(pending,'ProcessID'),
            'NextStationID':None if pending is None else raw(pending,'StationID'),
            'CurrProcessID':None,'CurrProcessNo':None,'CurrStationID':None}
    else:
        last=max(raw(row,'ProcessNo') for row in done)
        later=[row for row in processes if raw(row,'ProcessNo') is not None and raw(row,'ProcessNo')>last]
        running=[row for row in later if process_status(row) in [4,5]]
        if running:
            current=max(running,key=lambda row:(raw(row,'ProcessNo'),row.pk))
            values={'NextProcessID':raw(current,'ProcessID'),'CurrProcessID':raw(current,'ProcessID')}
        else:
            current=[row for row in done if raw(row,'ProcessNo')==last][-1]
            pending=sorted([row for row in later if process_status(row)==0],key=lambda row:(raw(row,'ProcessNo'),-row.pk))
            values={'CurrProcessID':raw(current,'ProcessID'),'NextProcessID':None if not pending else raw(pending[0],'ProcessID')}
    update_rows(type(job).objects.filter(pk=job.pk),values,actor,'initialize_combined_progress','自动合卡所涉空进度工卡初始化')


def remaining_steps(job,process_id,process_no,actor,query=rows):
    number=raw(job,'SheetNo');expected=[]
    weights=matching(query('StuffWeight','erp_production'),JobSheetNo=number,ProcessID=process_id)
    for weight in weights.order_by('pk'):
        if (raw(weight,'SheetStatus') or 0) in [8,9,10] or (raw(weight,'SheetKind') or 0) not in [0,2] or (raw(weight,'RecipeType') or 0) not in [0,2]:continue
        for phase in matching(query('StuffWeightPhase','erp_production'),SheetSeries=raw(weight,'SheetSeries')).order_by('pk'):
            for curve in matching(query('PDyeCurve','erp_base'),PhaseID=raw(phase,'PhaseID')).order_by('pk'):
                for step in matching(query('PDyeCurveDetail','erp_base'),CurveID=raw(curve,'CurveID')).order_by('pk'):
                    done=matching(query('WProcessStep','erp_production'),JobSheetNo=number,ProcessID=process_id,
                        DyeProcessID=raw(step,'DyeProcessID'),ProgramID=raw(step,'CurveID')).exists()
                    if not done:expected.append({'weight_id':weight.pk,'phase_id':phase.pk,'curve_id':curve.pk,'step_id':step.pk})
    if not expected:
        targets=matching(query('JobProcess','erp_production'),SheetSeries=raw(job,'SheetSeries'),ProcessID=process_id).filter(old_process_no=process_no)
        update_rows(targets,{'Status':'1'},actor,'remaining_steps_finished','原DPJobStep_UPDATE剩余步骤为0')
    return expected


@transaction.atomic
def automatic_sync(item,actor,machine,time_way,plan_have_time,as_of,at,reason,query=rows,completion_status=None):
    item=locked(item)
    result=choose_route(item,plan_have_time,as_of,query)
    targets=list(query('JobProcess','erp_production').filter(pk__in=result['targets']).order_by('pk'))
    sync_combined_process(item,actor,targets,machine,time_way,at,reason)
    from .source_progress_maintenance import maintain
    progress=maintain(actor,True,at,reason,query)
    result['global_progress']={'examined_count':len(progress['rows']),'changed_count':progress['changed_count'],
        'rows':progress['rows'],'issues':progress['supplemental_rows']}
    result['remaining_steps']=[]
    for step in result['step_processes']:
        job=locked(query('JobSheet','erp_production').get(pk=step['job_id']))
        refresh_current_process(job,actor)
        missing=remaining_steps(job,step['process_id'],raw(item,'ProcessNo'),actor,query)
        result['remaining_steps'].append({'job_id':job.pk,'process_id':step['process_id'],'missing':missing})
    result['at']=at;result['reason']=reason
    from .source_dye_rebuild import rebuild
    quality=rebuild(item,actor,completion_status,at,reason,query)
    result['quality_rebuild']=quality
    result['result_rows']=quality['rows']
    result['notes'].extend(['已执行权限范围内全库空进度维护；质量重建使用本次传入完成状态，区别于来源工序Status。',*quality['notes']])
    save_effect(item,'automatic_combine',result,actor,reason)
    return result
