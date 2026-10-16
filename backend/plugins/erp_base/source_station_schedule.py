"""旧排程重复检查与工位顺序/时间检查；原无序多候选逐项列出。"""
from collections import defaultdict
from datetime import datetime,timedelta
from itertools import product
from django.db.models import F,Window
from django.db.models.functions import DenseRank,Upper,RTrim
from django.utils import timezone
from .source_quality_reports import rows,key
from .source_stock_services import raw
from .source_business_updates import matching
from .source_station_quality import reference
from .source_station_yield import code_index


def existing_schedules(numbers,query=rows):
    codes={key(number) for number in numbers}
    selected=query('ProcessSchedule','erp_production').alias(code=Upper(RTrim('old_job_sheet_no'))).filter(code__in=codes).order_by('pk')
    result=[reference(item,JobSheetNo=raw(item,'JobSheetNo')) for item in selected]
    return {'report':'Sp_CheckProcessRS','rows':[{'Code':1 if result else 0,
        'Msg':'已存在排程：'+','.join(row['JobSheetNo'] for row in result) if result else None}],
        'result_rows':result,'notes':['保留原排程重复行；按明确编码列表匹配，不拼接执行SQL。此检查不删除或覆盖排程。']}


def schedule_rank(as_of,query=rows):
    schedules=list(query('ProcessSchedule','erp_production').order_by('pk'))
    numbers={key(raw(item,'JobSheetNo')) for item in schedules if raw(item,'JobSheetNo') is not None}
    jobs=code_index(query('JobSheet','erp_production').alias(code=Upper(RTrim('old_sheet_no'))).filter(code__in=numbers),['SheetNo'])
    works=query('WProcess','erp_production').filter(old_station_id='06',old_start_time__gt=as_of-timedelta(days=60)).filter(
        old_start_time__gt=timezone.make_aware(datetime(2025,1,1))).exclude(old_machine_id__isnull=True).exclude(old_machine_id__regex=r'^ *$')
    works=works.annotate(job_code=Upper(RTrim('old_job_sheet_no'))).filter(job_code__in=numbers)
    works=works.annotate(latest=Window(expression=DenseRank(),partition_by=[F('job_code')],order_by=F('old_start_time').desc())).filter(latest=1)
    latest=code_index(works.order_by('pk'),['JobSheetNo'])
    weights=code_index(query('StuffWeight','erp_production').filter(old_sheet_kind=2,old_recipe_type=1).exclude(
        old_wprocess_no__isnull=True).exclude(old_wprocess_no__regex=r'^ *$'),['WProcessNo'])
    result=[];supplement=[]
    for schedule in schedules:
        number=key(raw(schedule,'JobSheetNo'))
        for job,work in product(jobs[(number,)] or [None],latest[(number,)] or [None]):
            state='' if work is None or raw(work,'DyeState') is None else key(raw(work,'DyeState'))
            status=0 if job is None or raw(job,'SheetStatus') is None else raw(job,'SheetStatus')
            if status!=0 or state not in ['', '5']:
                supplement.append(reference(schedule,job_id=None if job is None else job.pk,work_id=None if work is None else work.pk,
                    issue='原T_PSD只包含未结工卡及空/5状态'));continue
            adds=[] if work is None else weights[(key(raw(work,'WProcessNo')),)]
            for weight in adds or [None]:
                date=as_of if state=='5' and weight is None else raw(schedule,'PlanDate') or as_of
                day=timezone.localtime(date).date()
                result.append(reference(schedule,JobSheetNo=raw(schedule,'JobSheetNo'),StereotypesName=raw(schedule,'StereotypesName'),
                    PlanDate=str(day),IsNot=raw(schedule,'IsNot') or 0,DyeState=state,STWProcessNo='' if weight is None else raw(weight,'WProcessNo'),
                    job_id=None if job is None else job.pk,work_id=None if work is None else work.pk,
                    weight_id=None if weight is None else weight.pk,latest_time_tied=len(latest[(number,)])>1))
    dates=defaultdict(set)
    for item in result:dates[key(item['StereotypesName'])].add(item['PlanDate'])
    for item in result:
        rank=sorted(dates[key(item['StereotypesName'])]).index(item['PlanDate'])+1
        item['NUM']=1 if (item['DyeState']=='5' and item['STWProcessNo']!='') or item['IsNot']==1 else rank
    return result,supplement


def process_status(number,process,state,as_of,query=rows):
    process=key(process);state=key(state)
    plans=list(matching(query('ProcessSchedule','erp_production'),JobSheetNo=number))
    notes=['只复刻原检查结果；现存入口元数据未证明此过程统一绑定所有刷卡，不擅自给所有录入新增拦截。',
        '原无ORDER BY变量赋值、TOP 1或相同最新时间可能任选；新报告逐候选列结果并标记歧义，不任选或丢弃。']
    if process=='GX03' and not plans:
        return {'report':'CheckProcessStatus','rows':[{'CmOk':1,'rule':'A','Mesge':'该工卡未进行染色排程'}],'notes':notes}
    if process not in ['GX03','GX07']:
        return {'report':'CheckProcessStatus','rows':[{'CmOk':0,'rule':None,'Mesge':''}],'notes':notes}
    ranked,supplement=schedule_rank(as_of,query)
    own=[row for row in ranked if key(row['JobSheetNo'])==key(number)]
    result=[]
    if process=='GX07':
        received=matching(query('GetJobSheetReceive','erp_base'),JobSheetNo=number).exists()
        starts=[]
        for job in matching(query('JobSheet','erp_production'),SheetNo=number):
            starts.extend(matching(query('JobProcess','erp_production'),SheetSeries=raw(job,'SheetSeries'),ProcessID=process))
        for item,plan in product(starts or [None],own or [None]):
            begin=None if item is None else raw(item,'StartTime')
            interval=None if begin is None else int((as_of.replace(second=0,microsecond=0)-begin.replace(second=0,microsecond=0)).total_seconds()//60)
            rule=None
            if begin is not None and timezone.localtime(begin).replace(tzinfo=None)!=datetime(1900,1,1) and interval<(0 if received else 240) and state in ['3','4','7']:rule='B'
            elif plan is not None and plan['NUM']!=1 and state in ['1','6']:rule='C'
            result.append({'CmOk':int(rule is not None),'rule':rule,'Mesge':{'B':'距离开始不足原规定间隔','C':'非第1缸染色顺序',None:''}[rule],
                'job_process_id':None if item is None else item.pk,'schedule_id':None if plan is None else plan['record_id'],
                'Interval':interval,'required_minutes':0 if received else 240,'NUM':None if plan is None else plan['NUM']})
    else:
        used={key(value) for value in matching(query('WProcess','erp_production'),ProcessID='GX03').values_list('old_job_sheet_no',flat=True) if value is not None}
        for plan in own or [None]:
            candidates=[] if plan is None or plan['StereotypesName'] is None else [row for row in ranked if key(row['StereotypesName'])==key(plan['StereotypesName']) and key(row['JobSheetNo']) not in used]
            minimum=min([row['NUM'] for row in candidates]) if candidates else None
            num=None if plan is None else plan['NUM'];failed=(num or 0)>(minimum or 0)
            result.append({'CmOk':int(failed),'rule':'D' if failed else None,'Mesge':'非最早装笼顺序' if failed else '',
                'schedule_id':None if plan is None else plan['record_id'],'NUM':num,'MinNUM':minimum})
    return {'report':'CheckProcessStatus','rows':result,'result_rows':ranked,'supplemental_rows':supplement,
        'ambiguous':len(result)>1 or any(item['latest_time_tied'] for item in ranked),'notes':notes}
