"""全库空进度维护：逐卡计算、预览及有审计的回写。"""
from collections import defaultdict
import re
from django.db import transaction
from django.db.models import Q
from django.db.models.functions import Upper,RTrim
from .business import locked
from .source_stock_services import raw
from .source_business_updates import update_rows
from .source_auto_combine import rows
from .source_context import SourceDocumentContext
from .source_continuation import save_effect


def key(value):
    return None if value is None else value.rstrip(' ').upper()


def planned_values(processes):
    states={};issues=[]
    for row in processes:
        value=raw(row,'Status')
        if value is None or value.strip()=='':states[row.pk]=0
        elif re.fullmatch(r'[+-]?[0-9]+',value.strip()):states[row.pk]=int(value)
        else:
            states[row.pk]=None
            issues.append({'process_id':row.pk,'status':value,'issue':'原状态不能转整数，保留原值，按未完成工序参与首道选择'})
    done=[row for row in processes if states[row.pk]==1]
    if not done:
        pending=next(iter(processes),None)
        return {'NextProcessID':None if pending is None else raw(pending,'ProcessID'),
            'NextStationID':None if pending is None else raw(pending,'StationID'),
            'CurrProcessID':None,'CurrProcessNo':None,'CurrStationID':None},issues
    last=max(raw(row,'ProcessNo') for row in done)
    later=[row for row in processes if raw(row,'ProcessNo')>last]
    running=[row for row in later if states[row.pk] in [4,5]]
    if running:
        current=max(running,key=lambda row:(raw(row,'ProcessNo'),row.pk))
        return {'NextProcessID':raw(current,'ProcessID'),'CurrProcessID':raw(current,'ProcessID')},issues
    current=[row for row in done if raw(row,'ProcessNo')==last][-1]
    pending=sorted([row for row in later if states[row.pk]==0],key=lambda row:(raw(row,'ProcessNo'),-row.pk))
    return {'CurrProcessID':raw(current,'ProcessID'),'NextProcessID':None if not pending else raw(pending[0],'ProcessID')},issues


@transaction.atomic
def maintain(actor,apply,at,reason,query=rows):
    jobs=query('JobSheet','erp_production').filter(Q(old_sheet_status__isnull=True)|Q(old_sheet_status=0))
    jobs=jobs.alias(curr=Upper(RTrim('old_curr_process_id')),nxt=Upper(RTrim('old_next_process_id'))).filter(
        Q(curr__isnull=True)|Q(curr='')).filter(Q(nxt__isnull=True)|Q(nxt=''))
    retired=SourceDocumentContext.objects.filter(Q(effects__card_adoption__state='reversed')|Q(effects__execution_chain__state='applied'),entity=jobs.model._meta.label).values('object_id')
    retired_ids=list(jobs.filter(pk__in=retired).values_list('pk',flat=True))
    jobs=jobs.exclude(pk__in=retired).order_by('pk')
    if apply:jobs=jobs.select_for_update()
    series=jobs.annotate(series_key=Upper(RTrim('old_sheet_series'))).values('series_key')
    process_query=query('JobProcess','erp_production').alias(series_key=Upper(RTrim('old_sheet_series'))).filter(series_key__in=series)
    if apply:process_query=process_query.select_for_update()
    grouped=defaultdict(list)
    for process in process_query.only('old_sheet_series','old_process_no','old_process_id','old_status','old_station_id').order_by('pk'):
        grouped[key(raw(process,'SheetSeries'))].append(process)
    result={'report':'全库空工序进度维护','rows':[],'supplemental_rows':[],'retired_ids':retired_ids,'applied':apply,
        'notes':['覆盖当前查询权限内全部原待维护工卡；原状态、空表和少用工序均保留。',
            '无序选择按记录ID确定，不将前一卡局部变量残值带到下一卡；已撤回的新计划单列留档。']}
    for job in jobs:
        processes=[] if raw(job,'SheetSeries') is None else grouped[key(raw(job,'SheetSeries'))]
        values,issues=planned_values(processes)
        changes={name:value for name,value in values.items() if raw(job,name)!=value}
        result['rows'].append({'job_id':job.pk,'legacy_id':job.legacy_id,'JobSheetNo':raw(job,'SheetNo'),
            'process_count':len(processes),'changes':changes,'result':'已回写' if apply and changes else '待回写' if changes else '无需改变'})
        result['supplemental_rows'].extend({'job_id':job.pk,**issue} for issue in issues)
        if apply and changes:
            update_rows(type(job).objects.filter(pk=job.pk),changes,actor,'global_process_maintenance',reason)
            save_effect(job,'progress_maintenance',{'changes':changes,'at':at,'reason':reason},actor,reason)
    result.update(at=at,reason=reason,changed_count=sum(bool(row['changes']) for row in result['rows']))
    return result
