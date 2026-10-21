"""生产保存联动。原拒绝异常的检查改为逐行审计，来源事实不丢弃。"""
from decimal import Decimal,ROUND_HALF_UP
from django.utils import timezone
from django.db.models import Q,Sum,Max
from .source_phase3_operations import source,create,change,retire,query
from .source_business_updates import matching
from .source_stock_services import raw
from .source_trial_steps import equal,sql_like
from .source_provenance import is_historical
from .business import record,snapshot


def issue(item,actor,procedure,text):
    record(item,'phase4_original_exception',snapshot(item),actor,procedure+'：'+text+'；保留本行，未跳过或删除。')


def saved(item,data,created,actor):
    if is_historical(item):return
    table=item.SOURCE_TABLE;series=raw(item,'SheetSeries') if 'SheetSeries' in item.SOURCE_FIELDS else None
    changed={old for old,field in item.SOURCE_FIELDS.items() if field in data}
    if table=='p_Customer' and not created and 'LabelID' in changed:
        for target in ['JobSheet','OrderMain']:change(matching(source(target),CustomerID=raw(item,'CustomerID')),{'LabelID':raw(item,'LabelID')},actor)
    elif table=='UrgentInStructDetail':
        change(matching(source('JobSheet'),SheetNo=raw(item,'JobSheetNo')),{'HurryInfo':raw(item,'Remarks'),'IsHurry':True},actor)
    elif table=='JobAssign' and (created or 'Rolls' in changed):
        assigned=matching(source('JobAssign'),ReceSheetNo=raw(item,'ReceSheetNo')).filter(Q(old_status=0)|Q(old_status__isnull=True))
        total=Decimal(str(assigned.aggregate(value=Sum('old_rolls'))['value'] or 0)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
        values=query('SELECT ReRolls FROM dye.vwGrayStockBook_ReceSheetNo WHERE ReceSheetNo=@number',{'number':raw(item,'ReceSheetNo')})
        stock=None if not values else Decimal(str(values[-1]['rerolls'] or 0)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
        if stock is not None and total>stock:issue(item,actor,'JobAssignModify',f'原开卡条数{total}超过可用条数{stock}')
    elif table=='JobProcess':
        same=matching(source(table),SheetSeries=series,ProcessID=raw(item,'ProcessID'))
        if same.count()>1:issue(item,actor,'JobProcess_Insert' if created else 'JobProcess_Update','同工卡工序重复')
        if not created:
            jobs=list(matching(source('JobSheet'),SheetSeries=series).order_by('pk'));job=None if not jobs else jobs[-1]
            if job is not None:
                number=raw(job,'SheetNo');no=raw(item,'ProcessNo');process=raw(item,'ProcessID');status=raw(item,'Status')
                if process in ['GX06','GX07'] and equal(status,'1'):
                    retire(matching(source('ProcessSchedule'),JobSheetNo=number,ProcessID=process).filter(old_process_no=no) if no is not None else source('ProcessSchedule').none(),actor,'JobProcess_Update完成工序移出排程，原排程留档')
                if no==1 and equal(status,'5'):
                    for head in matching(source('JobSheet'),SheetNo=number):
                        change(source('JobSheet').filter(pk=head.pk),{'SumProcessRolls':raw(head,'SumAssignedRolls'),'SumProcessWeightQty':raw(head,'SumAssignedWeightQty')},actor)
                if 'Status' in changed:
                    def minute(value):return None if value is None else timezone.localtime(value).strftime('%Y-%m-%d %H:%M')
                    a,b=minute(raw(job,'CreateDate')),minute(raw(item,'CreateDate'))
                    if raw(item,'ModifyDate') is not None or a is not None and b is not None and a!=b:
                        change(matching(source('WProcess'),WProcessNo=raw(item,'WProcessNo')).filter(old_process_no=no) if no is not None else source('WProcess').none(),{'Memo':1},actor)
    elif table=='JobSheet':
        from .source_phase4_operations import barcode
        number=raw(item,'SheetNo');targets=matching(source(table),SheetNo=number)
        if sql_like(number,'%R%' if created else '%T%'):change(targets,{'SheetKind':10,'JobKindID':'02'},actor)
        if created and (raw(item,'BarCode') is None or equal(raw(item,'BarCode'),'')):
            change(targets,{'BarCode':barcode()},actor)
        if not created:
            customers=list(matching(source('p_Customer'),CustomerID=raw(item,'CustomerID')).order_by('pk'))
            if customers and raw(customers[-1],'EnableOrders') and (raw(item,'OrderSheetNo') is None or equal(raw(item,'OrderSheetNo'),'')):
                issue(item,actor,'JobSheetModify','客户启用先下订单，工卡原订单号为空')
    elif table=='JobGrayRecord':
        from .source_phase4_operations import gray_totals
        assigned,barcode_value,receipt=[raw(item,k) for k in ['AssignedNo','BarCode','ReceSheetNo']]
        if all(v is not None and not equal(v,'') for v in [assigned,barcode_value,receipt]):
            change(matching(source('GrayInRecord'),BarCode=barcode_value,ReceSheetNo=receipt),{'AssignedNo':assigned,'JobSheetNo':series},actor)
        gray_totals(series,actor)
        if matching(source('RecordYield'),GrayBarCode=raw(item,'GrayBarCode')).exists():
            from .source_package_labels import synchronize
            jobs=list(matching(source('JobSheet'),SheetSeries=series).order_by('pk'))
            if jobs:synchronize(jobs[-1],actor,timezone.now(),'JobGrayRecordInsert自动标签同步',series=series,automatic=True)
    elif table=='ProcessSchedule' and created:
        p=raw(item,'ProcessNo');targets=matching(source('DyeStartDateTime'),JobSheetNo=raw(item,'JobSheetNo'),ProcessID=raw(item,'ProcessID'))
        retire(targets.filter(old_process_no=p) if p is not None else targets.none(),actor,'ProcessScheduleInsert同工卡工序开始计划替换留档')
        create('DyeStartDateTime',{f:raw(item,f) for f in ['JobSheetNo','ProcessNo','ProcessID','MachineID','PlanDate','JobSheetSeries','CombineSheetNos']},actor)
        for plan in source('ProcessSchedule').order_by('pk'):
            number=raw(plan,'JobSheetNo');jobs=matching(source('JobSheet'),SheetNo=number)
            if not jobs.exists() or jobs.exclude(old_sheet_status__isnull=True).exclude(old_sheet_status=0).exists() or any(matching(source(t),JobSheetNo=number).exists() for t in ['ProdIn','JobSheetRegister']):
                retire(source('ProcessSchedule').filter(pk=plan.pk),actor,'ProcessScheduleInsert按原全库条件退出排程；孤立/完成排程原行留档')
    elif table=='StuffWeight':
        # 原触发器先存变量再大写；后面的匹配仍按原大小写不敏感规则。
        targets=matching(source(table),SheetSeries=series)
        change(targets,{k:None if raw(item,k) is None else raw(item,k).upper() for k in ['JobSheetNo','CombineSheetNos']},actor)
        number=raw(item,'JobSheetNo');kind=raw(item,'SheetKind');recipe=raw(item,'RecipeType')
        if kind==2 and recipe in [0,2]:
            count=0
            for weight in matching(source(table),ProcessID=raw(item,'ProcessID')).filter(old_sheet_kind=2,old_recipe_type__in=[0,2]):
                if (raw(weight,'SheetStatus') or 0)!=0:continue
                codes=[raw(weight,'JobSheetNo'),*(raw(weight,'CombineSheetNos') or '').split('|')]
                if raw(weight,'SheetNo') is not None and any(equal(number,c) for c in codes):count+=1
            if count>1:issue(item,actor,'CheckPrintTimes' if created else 'StuffWeight_UPDATE','同主/副卡染色工序有多张有效领料单')
        if kind==2 and (created or changed.intersection(['JobSheetNo','CombineSheetNos'])):
            if not created:retire(matching(source('StuffCombineSheets'),StuffSheetNo=raw(item,'SheetNo')),actor,'StuffWeight_UPDATE重新建立主副卡关联，旧关联留档')
            values=[]
            combined=raw(item,'CombineSheetNos');parts=[] if combined is None or combined.rstrip(' ')=='' else combined.split('|')
            if parts and parts[-1].rstrip(' ')=='' :parts.pop() # 原分拆函数不返回最后的空段，中间空段保留。
            for code in [number,*parts]:
                if not any(code is None and v is None or equal(code,v) for v in values):values.append(code)
            for code in values:create('StuffCombineSheets',{'StuffSheetNo':raw(item,'SheetNo'),'SheetDate':timezone.now(),'JobSheetNo':code},actor)
        if created and kind==2 and recipe==1:
            value=matching(source(table),JobSheetNo=number).filter(old_sheet_kind=2,old_recipe_type=1).aggregate(value=Max('old_add_color_num'))['value']
            change(targets.filter(old_sheet_kind=2,old_recipe_type=1),{'AddColorNum':(value or 0)+1},actor)
    elif table=='StuffWeightDetail':
        if matching(source('p_Stuff'),StuffID=raw(item,'StuffID')).filter(old_status=1).exists():issue(item,actor,'StuffWeightDetail_INSERT','使用原已停用染化料')
    elif table=='StuffWeightPhase' and created:
        heads=list(matching(source('StuffWeight'),SheetSeries=series).order_by('pk'))
        if heads:
            head=heads[-1]
            for phase in matching(source(table),SheetSeries=series).order_by('pk'):
                remarks=raw(phase,'Remarks')
                if sql_like(remarks,"%'"):change(source(table).filter(pk=phase.pk),{'Remarks':remarks.replace("'",'’')},actor)
            if raw(head,'SheetKind')==2 and (raw(item,'BathRatio') or 0)>=30:issue(item,actor,'StuffWeightPhaseInsert','原判定浴比>=30，旧提示却写超过20')
            number=raw(head,'JobSheetNo');phase=raw(item,'PhaseID');recipe=raw(head,'RecipeType') or 0
            if number and phase and raw(head,'SheetKind')==2 and recipe in [0,2]:
                count=0
                for h in matching(source('StuffWeight'),ProcessID=raw(head,'ProcessID')).filter(old_recipe_type=recipe):
                    if (raw(h,'SheetStatus') or 0)==9:continue
                    if any(equal(number,n) for n in [raw(h,'JobSheetNo'),*(raw(h,'CombineSheetNos') or '').split('|')]):
                        count+=matching(source(table),SheetSeries=raw(h,'SheetSeries'),PhaseID=phase).count()
                if count>1:issue(item,actor,'StuffWeightPhaseInsert','同工卡、工序、配方类型的染程重复')
    elif table=='WProcess':
        number=raw(item,'JobSheetNo');no=raw(item,'ProcessNo');station=raw(item,'StationID');wno=raw(item,'WProcessNo')
        targets=matching(source(table),JobSheetNo=number,WProcessNo=wno)
        if matching(source(table),JobSheetNo=number,StationID='06').count()>1 and equal(station,'06') and raw(item,'DyeState') not in ['1','6']:
            candidates=matching(source(table),JobSheetNo=number,StationID='06').filter(old_process_no=no,old_dye_state__in=['1','6']).exclude(old_wprocess_no=wno).order_by('-old_start_time','pk') if no is not None and wno is not None else source(table).none()
            selected=list(candidates[:1]);change(targets,{'MachineID':None if not selected else raw(selected[0],'MachineID')},actor)
        processes=list(matching(source('p_Process'),ProcessID=raw(item,'ProcessID')).order_by('pk')[:1])
        if station in ['01','02','08'] and processes and raw(processes[0],'IsCanAddWorkQty') and raw(processes[0],'InputQtyCheckWay')==0:
            change(targets,{k:0 for k in ['CurrRolls','CurrMeter','CurrKg','CurrVats','CurrEffirate','WorkQty']},actor)
        end=raw(item,'EndTime')
        if created and (end is None or timezone.localtime(end).replace(tzinfo=None)==__import__('datetime').datetime(1900,1,1)):
            change(matching(source(table),WProcessNo=wno),{'EndTime':timezone.now()},actor)
    elif table=='GetJobSheetReceive':
        candidates=list(matching(source(table),SheetSeries=series).order_by('pk'));head=None if not candidates else candidates[-1]
        if head is not None:
            dept=raw(head,'DeptID');departments=list(matching(source('p_Dept'),DeptID=dept).order_by('pk'))
            parent=None if not departments else raw(departments[-1],'ParentCode')
            process='染部收单' if equal(parent,'DT003') or equal(dept,'DT036') else '定型部收单' if equal(dept,'DT004') else '品检部收单' if equal(dept,'DT005') else None
            if process is not None:change(matching(source('JobSheet'),SheetNo=raw(head,'JobSheetNo')),{'CurrProcessID':process,'PlanDate':raw(item,'CreateDate')},actor)
            value=raw(item,'CreateDate');change(matching(source(table),SheetSeries=series),{'Days':None if value is None else timezone.localtime(value).date().isoformat()},actor)
        retire(source(table).filter(Q(old_job_sheet_no__isnull=True)|Q(old_job_sheet_no='')),actor,'GetJobSheetReceive_Insert原清理空工卡收单，改留档')
    # JobAtteModify/JobSheetReceive_Insert/ProcessSchedule_Update/StuffWeightPhaseModify原有效体无写入，不添逻辑。
    item.refresh_from_db(fields=list(item.SOURCE_FIELDS.values()))
