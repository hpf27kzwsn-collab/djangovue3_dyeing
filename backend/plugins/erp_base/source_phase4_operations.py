"""第四阶段工卡、配缸和标签人员明确办理。原替换行留档，不删异常来源。"""
from decimal import Decimal,ROUND_HALF_UP
from datetime import datetime,timedelta
from html import escape
from django.db import transaction
from django.db.models import Sum,Count,Max
from django.utils import timezone
from .source_phase3_operations import source,create,change as update_original,retire,result,query
from .source_business_updates import matching
from .source_stock_services import raw
from .source_trial_steps import equal,sql_like
from .source_package_labels import varchar

NAMES=['Sp_JobGrayRecord_JobSheet_Update','Sp_Update_JobSheet_Structure','Sp_JobPackRemarks',
       'sp_JobProcess_New','sp_JobProcess_New1','Sp_JobProcessUpdate','Sp_JobProcessUpdate_Curr2',
       'Up_RecordEmp','Up_RecordEmp1','UpdateJobSheet_Field','Sp_StuffIDPrice','GetCustProdstandcraft','DyeUseOver_UPDTEA',
       'Sp_UpdateJobSheetAndJobProcess','Sp_UpdateJobSheetAndJobProcessNT','Sp_UpdateJobOutAC','sp_ProduseBarCode','Sp_StuffRegisterAutoOutPut']


def change(targets,values,actor):
    from .source_phase4_triggers import saved
    ids=list(targets.values_list('pk',flat=True));update_original(targets,values,actor)
    for item in targets.model.objects.filter(pk__in=ids).order_by('pk'):
        saved(item,{item.SOURCE_FIELDS[k]:v for k,v in values.items()},False,actor)


def barcode(now=None):
    now=timezone.localtime() if now is None else now
    day=now.replace(hour=0,minute=0,second=0,microsecond=0)
    previous=source('JobSheet').filter(old_create_date__gte=day,old_create_date__lt=day+timedelta(days=1)).aggregate(value=Max('old_bar_code'))['value']
    index=1 if previous is None or previous.rstrip(' ')=='' else int(previous[-3:])+1
    return now.strftime('%y%m%d')+('000'+str(index))[-3:]


def gray_totals(series,actor):
    records=matching(source('JobGrayRecord'),SheetSeries=series)
    assigned=records.exclude(old_assigned_no__isnull=True).exclude(old_assigned_no='')
    targets=matching(source('JobSheet'),SheetSeries=series)
    def sums(q):return q.aggregate(rolls=Count('pk'),weight=Sum('old_weight_qty'),length=Sum('old_length_qty'))
    if assigned.exists():
        a=sums(assigned);change(targets,dict(SumAssignedRolls=a['rolls'],SumAssignedWeightQty=a['weight'],SumProcessRolls=a['rolls'],SumProcessWeightQty=a['weight'],SumAssignedLengthQty=a['length']),actor)
    if records.exists():
        a=sums(records);change(targets,dict(PreRolls=a['rolls'],PreVatQty=a['length'] if (a['length'] or 0)>0 else a['weight']),actor)
    return list(targets)


def structure(series,actor):
    targets=matching(source('JobSheet'),SheetSeries=series);assigns=list(matching(source('JobAssign'),SheetSeries=series).order_by('pk')) if targets.exists() else []
    def grouped(field,separator,width=None):
        distinct=[]
        for item in assigns:
            value=raw(item,field)
            if value is not None and not any(equal(value,v) for v in distinct):distinct.append(value)
        text=separator.join(escape(v,quote=False) for v in distinct) if distinct else None
        return text if text is None or width is None else text[:width]
    atte=list(matching(source('JobAtte'),SheetSeries=series,FieldType='01').order_by('old_atte_code','pk'))
    pack=','.join(escape(raw(r,'AtteValue'),quote=False) for r in atte if raw(r,'AtteValue') is not None)
    change(targets,dict(Structure=grouped('PreField1',';',10),AssignInfo=grouped('PreField5','@',220),StorageUnitIDs=grouped('Area',';'),
        MachineID=grouped('MachineID',';'),FabricNO3=None if not assigns else raw(assigns[0],'PreField5'),PackRemarks=pack+'。' if pack else None),actor)
    return list(targets)


def fields(series,actor):
    values={}
    for field,sql,width in [
        ('ProcessName',"SELECT STRING_AGG(p.Name,'→') AS value FROM dye.JobProcess a JOIN dye.p_Process p ON a.ProcessID=p.ProcessID WHERE a.SheetSeries=@series",255),
        ('PBXX',"SELECT STRING_AGG(ISNULL(LotNo,'')+',匹数'+CONVERT(VARCHAR(20),CONVERT(DECIMAL(6,1),Rolls))+'条',';') AS value FROM dye.JobAssign WHERE SheetSeries=@series",500),
        ('GYYQ',"SELECT STRING_AGG(ISNULL(AtteValue,'')+IIF(ISNULL(Description,'')='','',':'+Description),';') AS value FROM dye.JobAtte WHERE SheetSeries=@series",500)]:
        values[field]=varchar(query(sql,{'series':series})[0]['value'],width)
    targets=matching(source('JobSheet'),SheetSeries=series);change(targets,values,actor);return list(targets)


def progress(name,series,actor):
    jobs=list(source('JobSheet').order_by('pk'))
    if name=='Sp_JobProcessUpdate':
        heads=list(matching(source('JobSheet'),SheetSeries=series).order_by('pk'));number=None if not heads else raw(heads[-1],'SheetNo')
        jobs=[r for r in jobs if (raw(r,'SheetStatus') or 0)==0 and sql_like(raw(r,'SheetNo'),None if number is None else '%'+number+'%')]
    process=current=station=start=end=None;result_rows=[]
    for job in jobs:
        current_series=raw(job,'SheetSeries');steps=list(matching(source('JobProcess'),SheetSeries=current_series).order_by('pk'))
        completed=[r for r in steps if equal(raw(r,'Status'),'1')]
        if not completed:
            todo=[r for r in steps if not equal(raw(r,'Status'),'1')]
            if todo:process=raw(todo[0],'ProcessID');station=raw(todo[0],'StationID')
            values={'NextProcessID':process}
            if name.endswith('Curr2'):values.update(NextStationID=station,CurrProcessID=None,CurrProcessNo=None,CurrStationID=None)
        else:
            numbers=[raw(r,'ProcessNo') for r in completed if raw(r,'ProcessNo') is not None];maxno=max(numbers) if numbers else None
            todo=[r for r in steps if (raw(r,'Status') is None or (raw(r,'Status').strip() or '0')=='0') and (name=='Sp_JobProcessUpdate' or maxno is not None and raw(r,'ProcessNo') is not None and raw(r,'ProcessNo')>maxno)]
            numbers=[raw(r,'ProcessNo') for r in todo if raw(r,'ProcessNo') is not None];minno=min(numbers) if numbers else None
            running=[r for r in steps if any(equal(raw(r,'Status'),v) for v in ['4','5']) and maxno is not None and raw(r,'ProcessNo') is not None and raw(r,'ProcessNo')>maxno] if name.endswith('Curr2') else []
            if not running:
                for r in todo:
                    if minno is not None and raw(r,'ProcessNo')==minno:process=raw(r,'ProcessID')
            targetno=max(raw(r,'ProcessNo') for r in running) if running else maxno
            for r in steps:
                if targetno is not None and raw(r,'ProcessNo')==targetno:current=raw(r,'ProcessID');start=raw(r,'StartTime');end=raw(r,'EndTime')
            values={'NextProcessID':current if running else process,'CurrProcessID':current}
            if name.endswith('Curr2'):values['PlanDate']=end if end is not None and timezone.localtime(end).replace(tzinfo=None)!=datetime(1900,1,1) else start
        targets=matching(source('JobSheet'),SheetSeries=current_series);change(targets,values,actor);result_rows.extend(targets)
    return result_rows


def combine_progress(name,p,actor):
    sql="SELECT ps.CombineSheetNos FROM dye.ProcessSchedule ps LEFT JOIN dye.p_Process p ON p.ProcessID=ps.ProcessID WHERE ps.JobSheetNo=@sheetno AND ps.ProcessNo=@processno AND ISNULL(ps.CombineSheetNos,'')<>''"
    if name=='Sp_UpdateJobSheetAndJobProcess':sql+=' AND ps.StartTime>=DATEADD(HOUR,ISNULL(-p.DelayHours,0),GETDATE())'
    candidates=query(sql,p);combined=None if not candidates else varchar(candidates[-1]['combinesheetnos'],200);items=[]
    for token in (combined or '').split(';'):
        token=varchar(token,20)
        if ':' not in token:continue # 原循环只办理包含冒号的卡号:工序号，原排程串不改写。
        number,step=token.split(':',1);step=int(step)
        jobs=list(matching(source('JobSheet'),SheetNo=number).order_by('pk'))
        for job in jobs:
            if len(jobs)>1:
                from .business import record,snapshot
                record(job,'phase4_duplicate_combined_card',snapshot(job),actor,'原标量工卡查询存在多候选，按全部原工卡办理，候选ID：'+str([j.pk for j in jobs]))
            series=raw(job,'SheetSeries');steps=matching(source('JobProcess'),SheetSeries=series)
            current=list(steps.filter(old_process_no=step).order_by('pk'));following=list(steps.filter(old_process_no=step+1).order_by('pk'))
            if current and following:
                a,b=current[-1],following[-1]
                change(source('JobSheet').filter(pk=job.pk),{'CurrStationID':raw(a,'StationID'),'CurrProcessNo':raw(a,'ProcessNo'),'CurrProcessID':raw(a,'ProcessID'),
                    'NextProcessID':raw(b,'ProcessID'),'NextStationID':raw(b,'StationID')},actor)
            if p['dpkind'] in [0,1,2]:
                values={'MachineID':p['machineid'],'Status':p['workstatus']}
                if p['dpkind'] in [0,1]:values['StartTime']=p['worktime']
                if p['dpkind'] in [0,2]:values['EndTime']=p['worktime']
                change(steps.filter(old_process_no=step),values,actor)
                for r in current:
                    r.refresh_from_db();items.append(r)
            items.append(job)
    return items


def dye_result(number,actor):
    p={'vatno':number,'combine':None};heads=list(matching(source('JobSheet'),SheetNo=None if number is None else number.upper()).order_by('pk'))
    kind=None if not heads else raw(heads[-1],'SheetKind');targets=matching(source('JobSheetReceive'),JobSheetNo=number)
    if kind is not None and kind!=0:change(targets,{'Remarks':'回修','RTVat':1},actor)
    if kind==0:
        weights=[r for r in source('StuffWeight').order_by('pk') if sql_like(raw(r,'CombineSheetNos'),None if number is None else '%'+number+'%')]
        main=any(raw(r,'RecipeType')==0 and raw(r,'SheetKind')==2 for r in weights)
        if main:p['combine']=varchar(raw(weights[-1],'CombineSheetNos'),500)
        fb=query("SELECT COUNT(*) AS n FROM dye.v_DyeUse_FB WHERE JobSheetNo=@vatno OR CombineSheetNos LIKE '%'+@vatno+'%'",p)[0]['n']
        jl=query("SELECT COUNT(*) AS n FROM dye.v_DyeUse_JL WHERE JobSheetNo=@vatno"+(' OR @combine LIKE \'%\'+JobSheetNo+\'%\'' if main else ''),p)[0]['n']
        if fb or jl:
            count=query("SELECT COUNT(*) AS n FROM (SELECT DISTINCT a.SheetSeries FROM dye.StuffWeight a JOIN dye.StuffWeightDetail b ON a.SheetSeries=b.SheetSeries WHERE a.SheetKind=2 AND a.RecipeType=1 AND b.StuffType='S' AND (a.JobSheetNo=@vatno OR @combine LIKE '%'+a.JobSheetNo+'%')) counts",p)[0]['n']
            for r in targets:change(targets.filter(pk=r.pk),{'Remarks':'加色'+str(count),'AddVat':1 if (raw(r,'WeightQty') or 0)>250 else 0},actor)
        else:change(targets,{'Remarks':'直通','PassVat':1},actor)
    return list(targets)


def standard_craft(actor):
    from uuid import uuid4
    from .business import record,snapshot
    retained=[];items=[]
    for table in ['StandCraft','StandCraftDetail']:retained.extend(retire(source(table),actor,'GetCustProdstandcraft重建全部标准工艺，旧版本完整留档'))
    groups=query('SELECT j.ProdID,j.CustomerID,MAX(j.SheetSeries) AS MaxSeries,MAX(oc.AssignNo) AS MaxNo,j.ColorNum FROM dye.JobSheet j JOIN dye.JobAssign oc ON j.SheetSeries=oc.SheetSeries JOIN dye.JobProcess op ON j.SheetSeries=op.SheetSeries GROUP BY j.ProdID,j.CustomerID,j.ColorNum',{})
    for group in groups:
        series=str(uuid4())
        head=create('StandCraft',dict(SheetSeries=series,CustomerID=group['customerid'],ProdID=group['prodid'],ColorNum=group['colornum'],ColorID='\\',Spec=None if group['maxno'] is None else str(group['maxno'])),actor);items.append(head)
        for step in matching(source('JobProcess'),SheetSeries=group['maxseries']).order_by('pk'):
            values={'SheetSeries':series,'ProcessNo':raw(step,'ProcessNo'),'ProcessID':raw(step,'ProcessID')}
            for i in range(1,21):values.update({f'PPName{i:02}':raw(step,f'PPName{i:02}'),f'Value{i:02}':raw(step,f'TheoryValue{i:02}')})
            items.append(create('StandCraftDetail',values,actor))
        record(head,'phase4_craft_source',snapshot(head),actor,'原分组最大工卡流水和最大配坯号分别计算：'+str(group))
    return items,retained


@transaction.atomic
def perform(name,p,actor):
    retained=[];items=[]
    if name=='sp_ProduseBarCode':return {'report':name,'rows':[{'barcode':barcode()}]}
    if name=='Sp_StuffRegisterAutoOutPut':return {'report':name,'rows':[{'msgmark':1}],'notes':['最新原过程的出库语句已被注释，实际仅返回msgmark=1。']}
    if name=='Sp_UpdateJobOutAC':
        if p['upkind'] in [1,2]:
            table='SemiOutDetail' if p['upkind']==1 else 'GrayOutDetail'
            values=query('SELECT JobSheetNo,SUM(WeightQty) AS weight,SUM(Rolls) AS rolls,SUM(Packs) AS packs FROM dye.'+table+' WHERE SheetSeries=@upsheetseries GROUP BY JobSheetNo',p)
            if values:
                row=values[-1];targets=matching(source('JobSheet'),SheetNo=row['jobsheetno']);change(targets,{'SumAssignedWeightQty':row['weight'],'SumAssignedRolls':row['rolls'],'SumAssignedPacks':row['packs'],'CurrProcessID':'胚纱出库' if p['upkind']==1 else '发纱出库'},actor);items.extend(targets)
                from .business import record,snapshot
                for item in targets:record(item,'phase4_cursor_candidates',snapshot(item),actor,'原分组变量只回写最后候选工卡；全部候选：'+str(values))
    elif name=='Sp_JobGrayRecord_JobSheet_Update':items=gray_totals(p['sheetseries'],actor)
    elif name=='Sp_Update_JobSheet_Structure':items=structure(p['sheetseries'],actor)
    elif name=='Sp_JobPackRemarks':
        for job in source('JobSheet').order_by('pk'):items.extend(structure(raw(job,'SheetSeries'),actor))
    elif name=='UpdateJobSheet_Field':items=fields(p['sheetseries'],actor)
    elif name in ['Sp_JobProcessUpdate','Sp_JobProcessUpdate_Curr2']:items=progress(name,p['sheetseries'],actor)
    elif name in ['Sp_UpdateJobSheetAndJobProcess','Sp_UpdateJobSheetAndJobProcessNT']:items=combine_progress(name,p,actor)
    elif name=='DyeUseOver_UPDTEA':items=dye_result(p['jobsheetno'],actor)
    elif name=='GetCustProdstandcraft':items,retained=standard_craft(actor)
    elif name in ['sp_JobProcess_New','sp_JobProcess_New1']:
        new=name.endswith('New');code='GX99' if new else 'GX98';station='29' if new else '07'
        number=None
        for job in matching(source('JobSheet'),SheetNo=p['jobsheetno']).filter(old_sheet_status=0).order_by('pk'):
            series=raw(job,'SheetSeries');steps=matching(source('JobProcess'),SheetSeries=series)
            if matching(steps,ProcessID=code).exists():continue # 原过程只在没有该工序时添加；原有重复行不处理。
            if new:
                number=steps.aggregate(value=Max('old_process_no'))['value'];number=None if number is None else number+1
            else:
                for step in matching(steps,ProcessID='GX99').order_by('pk'):number=raw(step,'ProcessNo')
                change(matching(steps,ProcessID='GX99'),{'ProcessNo':None if number is None else number+1},actor)
            if number is not None and number>0:items.append(create('JobProcess',dict(SheetSeries=series,ProcessNo=number,ProcessID=code,StationID=station),actor))
    elif name in ['Up_RecordEmp','Up_RecordEmp1']:
        labels=source('RecordYield') if name=='Up_RecordEmp' else matching(source('RecordYield'),BarCode=p['barcode'])
        for label in labels.order_by('pk'):
            employees=list(matching(source('p_ShiftEmp'),ShiftID=raw(label,'ShiftID')).order_by('pk'));barcode_value=raw(label,'BarCode')
            targets=matching(source('RecordEmp'),BarCode=barcode_value).filter(old_emp_id__in=[raw(r,'EmpID') for r in employees if raw(r,'EmpID') is not None])
            retained.extend(retire(targets,actor,name+'按原班组替换包装人员；被替换行留档'))
            items.extend(create('RecordEmp',{'BarCode':barcode_value,'EmpID':raw(person,'EmpID')},actor) for person in employees)
    elif name=='Sp_StuffIDPrice':
        price=None
        for stuff in source('p_Stuff').order_by('pk'):
            code=raw(stuff,'StuffID')
            candidates=query("SELECT TOP 1 a.Price FROM dye.StuffInDetail a JOIN dye.StuffIn b ON b.SheetSeries=a.SheetSeries WHERE b.SheetKind=13 AND b.WareHouseID='12' AND a.StuffID=@code ORDER BY b.SheetDate DESC",{'code':code})
            if candidates:price=candidates[0]['price']
            target=matching(source('p_Stuff'),StuffID=code);change(target,{'Price':price},actor);items.extend(target)
    return result(name,items,retained)
