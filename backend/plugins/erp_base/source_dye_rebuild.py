"""vwDyeWorkQty/vw_DyeWorkQtyQuer和自动合卡染色质量重建尾段。"""
from collections import defaultdict
from datetime import timedelta,time
from decimal import Decimal,ROUND_HALF_UP
import re
from django.db import transaction
from django.utils import timezone
from .business import locked
from .source_stock_services import raw
from .source_business_updates import matching,update_rows
from .source_continuation import origin,save_effect
from .source_auto_combine import rows,equal
from .source_context import SourceDocumentContext
from .source_calculations import store_value


def active(query):
    return query.exclude(pk__in=SourceDocumentContext.objects.filter(entity=query.model._meta.label,
        effects__quality_replaced__active=True).values('object_id'))


def total(values):
    values=[value for value in values if value is not None]
    return sum(values) if values else None


def decimal2(value):
    return None if value is None else Decimal(str(value)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)


def dye_sources(number,query=rows):
    work=list(matching(query('WProcess','erp_production'),JobSheetNo=number).order_by('pk'))
    groups=defaultdict(list);notes=[];excluded=[]
    for row in work:
        code=raw(row,'ProcessID')
        if any(equal(code,value) for value in ['GX06','GX07']):groups[code.rstrip(' ').upper()].append(row)
    if not groups:return [],[],[]
    selected=min(groups);bucket=groups[selected]
    ends=[raw(row,'EndTime') for row in bucket if raw(row,'EndTime') is not None]
    latest=max(ends) if ends else None
    qty=decimal2(total([raw(row,'CurrKg') for row in bucket]));rolls=total([raw(row,'CurrRolls') for row in bucket])
    rolls=None if rolls is None else int(rolls)
    # AddNumber1的字典StuffType与尾段JTimes的明细StuffType是两个不同条件。
    extra=set()
    for weight in matching(query('StuffWeight','erp_production'),JobSheetNo=number).filter(old_sheet_kind=2,old_recipe_type=1):
        for detail in matching(query('StuffWeightDetail','erp_production'),SheetSeries=raw(weight,'SheetSeries')):
            if matching(query('PStuff','erp_base'),StuffID=raw(detail,'StuffID'),StuffType='S').exists() and raw(weight,'SheetNo') is not None:
                extra.add(raw(weight,'SheetNo').rstrip(' ').upper())
    jobs=list(matching(query('JobSheet','erp_production'),SheetNo=number).order_by('pk'))
    if len(jobs)>1:notes.append('原工卡标量子查询多行会失败；按每个实际工卡原行及其JobKindID展开，全部来源ID保留。')
    result=[]
    for row in work:
        if not equal(raw(row,'ProcessID'),selected) or latest is None or raw(row,'EndTime')!=latest:
            excluded.append({'work_id':row.pk,'ProcessID':raw(row,'ProcessID'),'issue':'原视图仅选最小工序编码组及该组最大结束时间'});continue
        machines=list(matching(query('PMachine','erp_base'),MachineID=raw(row,'MachineID')).order_by('pk')) or [None]
        for job in jobs:
            if not matching(query('JobProcess','erp_production'),SheetSeries=raw(job,'SheetSeries'),ProcessID=selected).filter(old_end_time__isnull=False).exists():
                excluded.append({'work_id':row.pk,'job_id':job.pk,'issue':'原视图要求存在已填结束时间的同工序'});continue
            defects=list(matching(query('WDefect','erp_quality'),SheetNo=raw(job,'LossStr')).order_by('pk')) or [None]
            if len(defects)>1:notes.append('原责任评审标量子查询多行会失败；按全部评审原行展开，数量重复连接另列来源。')
            for machine in machines:
                if machine is not None and raw(machine,'bit4') not in [None,False,0]:
                    excluded.append({'work_id':row.pk,'machine_id':machine.pk,'issue':'原机台bit4筛选排除，刷卡原行保留'});continue
                for defect in defects:
                    end=timezone.localtime(raw(row,'EndTime'));day=(end-timedelta(hours=8)).strftime('%Y-%m-%d')
                    values={name:raw(row,name) for name in ['WProcessNo','JobSheetNo','ShiftID','ClassID','StationID','EndTime','MachineID','ColorMatching']}
                    values.update({name:raw(job,name) for name in ['ProdID','ColorNum','ColorID','CustomerID']})
                    normal=equal(raw(job,'JobKindID'),'01');added=len(extra)>0
                    values.update(DAYS=day,TMonth=day[:7],Class='白班' if time(7,30)<=end.time().replace(tzinfo=None,microsecond=0)<=time(19,30) else '晚班',
                        JobProdKind=raw(job,'JobKindID'),ZNum=0 if added else 1,ZKg=Decimal(0) if added else qty,
                        JNum=1 if added else 0,JKg=qty if added else Decimal(0),RNum=0 if normal else 1,
                        RTKg=Decimal(0) if normal else qty,TNum=1,Rolls=rolls,ClothQtyKg=qty,NumNo='汇总',ProcessID=raw(row,'ProcessID'),
                        AddNumber1=len(extra),AddNumber2=0,WDNum=None if defect is None else int(any(equal(raw(defect,'DefectDept'),code) for code in ['02','03','04'])),
                        DefectClassID=None if defect is None else raw(defect,'DefectClassID'),DefectEmpID=None if defect is None else raw(defect,'DefectEmpID'))
                    result.append({'values':values,'work_ids':[item.pk for item in bucket],'last_work_id':row.pk,
                        'job_id':job.pk,'machine_id':None if machine is None else machine.pk,'defect_id':None if defect is None else defect.pk})
    return result,excluded,list(dict.fromkeys(notes))


def tail_values(number,query):
    groups=set()
    for weight in matching(query('StuffWeight','erp_production'),JobSheetNo=number).filter(old_sheet_kind=2,old_recipe_type=1):
        if raw(weight,'SheetStatus') not in [None,0]:continue
        if matching(query('StuffWeightDetail','erp_production'),SheetSeries=raw(weight,'SheetSeries'),StuffType='S').exists():
            series=raw(weight,'SheetSeries');groups.add(None if series is None else series.rstrip(' ').upper())
    jobs=list(matching(query('JobSheet','erp_production'),SheetNo=number).order_by('pk'))
    color=None if not jobs else raw(jobs[-1],'ColorNum')
    digits=lambda value:None if value is None else ''.join(ch for ch in value[:100] if '0'<=ch<='9')[:20]
    candidates=[row for row in query('PColorNum','erp_base').order_by('pk') if digits(color) is not None and digits(raw(row,'ColorNum'))==digits(color)]
    depth=None if not candidates else raw(candidates[-1],'ColorDepthID')
    return {'JTimes':len(groups),'ColorDepthID':'05' if depth is None else depth},[row.pk for row in candidates]


def preview(item,completion_status,query=rows):
    data={'report':'自动合卡染色质量重建','rows':[],'supplemental_rows':[],'sources':[],'jobs':[],
        'notes':['原质量行与异常来源均保留；原删除范围采用留档退出统计，NULL删除条件不匹配任何原行。']}
    if not any(equal(raw(item,'ProcessID'),code) for code in ['GX06','GX07']) or completion_status!=1:
        data['notes'].append('未满足原GX06/GX07且传入Status=1的质量重建条件。');return data
    seen=set()
    for job in matching(query('JobSheet','erp_production'),SheetSeries=raw(item,'SheetSeries')).order_by('pk'):
        number=raw(job,'SheetNo');normalized=None if number is None else number.rstrip(' ').upper()
        if normalized in seen:continue
        seen.add(normalized)
        unfinished=[]
        for sibling in matching(query('JobSheet','erp_production'),SheetNo=number):
            for process in matching(query('JobProcess','erp_production'),SheetSeries=raw(sibling,'SheetSeries')):
                state=(raw(process,'Status') or '').strip()
                completed=re.fullmatch(r'[+-]?[0-9]+',state) is not None and int(state)==1
                if any(equal(raw(process,'ProcessID'),code) for code in ['GX06','GX07']) and not completed:
                    unfinished.append(raw(process,'ProcessNo'))
        if unfinished and max(unfinished)!=0:
            data['supplemental_rows'].append({'job_id':job.pk,'JobSheetNo':number,'issue':'仍有未完成GX06/GX07，原尾段不重建'});continue
        values,excluded,notes=dye_sources(number,query);tail,candidates=tail_values(number,query)
        data['jobs'].append({'job_id':job.pk,'number':number,'tail':tail,'color_candidate_ids':candidates})
        for source in values:
            source['values']['ProcessID']=raw(item,'ProcessID')
            data['sources'].append(source);data['rows'].append({**source['values'],**tail,'source_work_id':source['last_work_id']})
        data['supplemental_rows'].extend(excluded);data['notes'].extend(notes)
    return data


@transaction.atomic
def rebuild(item,actor,completion_status,at,reason,query=rows,process_variable=None):
    from .source_services import write
    item=locked(item);data=preview(item,completion_status,query);model=query('DyeCheckout','erp_quality').model
    retired=[];created=[]
    for job in data['jobs']:
        previous=matching(active(query('DyeCheckout','erp_quality')),JobSheetNo=job['number'],ProcessID=process_variable)
        for row in previous.order_by('pk'):
            row=locked(row);save_effect(row,'quality_replaced',{'active':True,'source_process_id':item.pk,'before':origin(row),'at':at,'reason':reason},actor,reason);retired.append(row.pk)
    for source in data['sources']:
        values=dict(store_value(model(),old,value) for old,value in source['values'].items())
        row=write(model,values,actor=actor,apply_effects=False)
        save_effect(row,'quality_rebuild_origin',{'process':origin(item),'source':source,'at':at,'reason':reason},actor,reason);created.append(row.pk)
    for job in data['jobs']:
        update_rows(matching(active(query('DyeCheckout','erp_quality')),JobSheetNo=job['number']),job['tail'],actor,'dye_quality_tail',reason)
    data.update(created_ids=created,retired_ids=retired,at=at,reason=reason,completion_status=completion_status)
    save_effect(item,'quality_rebuild',data,actor,reason)
    return data
