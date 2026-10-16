"""正式染色扫码选卡与三个备料步骤视图；外部中控来源独立留明。"""
from plugins.erp_base.source_provenance import reference as source_reference
from itertools import product
from django.db.models import Q
from .source_stock_services import raw
from .source_quality_reports import rows,key
from .source_business_updates import matching
from .source_package_labels import varchar
from .source_trial_steps import equal,sql_like

JOB_FIELDS='SheetSeries SheetNo BarCode OrderSheetNo CustomerID ProdID LotNo Spec SheetStatus DlvDate PreRolls PreVatQty CurrProcessID CurrProcessNo CurrStationID NextProcessID NextStationID SumAssignedRolls SumAssignedLengthQty SumAssignedWeightQty SumProcessRolls SumProcessLengthQty SumProcessWeightQty ColorID ColorNum OriOrderSeries SheetKind DesignNo IsHurry IsContinue IsSpecColor IsSpecVat OriJobSheetNo AssignUnit CheckNo IsSplited WeightDn'.split()


def scan(barcode,query=rows):
    barcode=varchar(barcode,50);candidates=[]
    source=query('StuffWeight','erp_production').filter(Q(old_sheet_status=0)|Q(old_sheet_status__isnull=True),old_sheet_kind=2,old_recipe_type__in=[0,2]).order_by('pk')
    for weight in source.only('id','source_batch','source_row',*[source.model.SOURCE_FIELDS[k] for k in source.model.SOURCE_KEY],'old_job_sheet_no','old_combine_sheet_nos').iterator():
        if equal(raw(weight,'JobSheetNo'),barcode) or sql_like(raw(weight,'CombineSheetNos'),None if barcode is None else '%'+barcode+'%'):candidates.append(weight)
    actual=varchar(raw(candidates[-1],'JobSheetNo'),50) if candidates else None
    jobs=(matching(query('JobSheet','erp_production'),SheetNo=actual) | matching(query('JobSheet','erp_production'),BarCode=actual)).order_by('pk')
    results=[]
    for job in jobs:
        processes=matching(query('JobProcess','erp_production'),SheetSeries=raw(job,'SheetSeries')).filter(old_process_no=raw(job,'CurrProcessNo')) if raw(job,'CurrProcessNo') is not None else query('JobProcess','erp_production').none()
        customers=matching(query('PCustomer','erp_base'),CustomerID=raw(job,'CustomerID'))
        materials=matching(query('PGray','erp_base'),GrayID=raw(job,'ProdID'))
        originals=matching(query('JobSheet','erp_production'),SheetNo="'" if raw(job,'OriJobsheetNo') is None else raw(job,'OriJobsheetNo'))
        weights=matching(query('StuffWeight','erp_production'),JobSheetNo=raw(job,'SheetNo')).filter(old_sheet_kind=2,old_recipe_type__in=[0,2])
        for process,customer,material,original,weight in product(*[list(q.order_by('pk')) or [None] for q in [processes,customers,materials,originals,weights]]):
            def value(obj,field):return None if obj is None else raw(obj,field)
            result={name:raw(job,'OriJobsheetNo' if name=='OriJobSheetNo' else name) for name in JOB_FIELDS}
            result.update(CustomerID_R=value(customer,'NameC'),ProdID_R=value(material,'NameC'),FabricKindID=value(material,'FabricKindID'),
                VehicleNo=value(process,'VehicleNo'),Place=value(process,'Place'),ProcessNo=value(process,'ProcessNo'),
                StuffRolls=value(weight,'Rolls'),StuffLengthQty=0,StuffWeightQty=value(weight,'ClothQtyKg'),
                **{'Ori'+name:value(original,name) for name in ['SumAssignedRolls','SumAssignedLengthQty','SumAssignedWeightQty']})
            result.update(record_id=job.pk,source=source_reference(job),weight_id=None if weight is None else weight.pk,
                joined_ids=[None if obj is None else obj.pk for obj in [process,customer,material,original,weight]])
            results.append(result)
    return {'report':'DPJobSheet','rows':results[:1],'candidate_rows':results,
        'result_rows':[{'record_id':w.pk,'source': source_reference(w),'JobSheetNo':raw(w,'JobSheetNo'),'CombineSheetNos':raw(w,'CombineSheetNos'),'selected':w.pk==candidates[-1].pk} for w in candidates],
        'notes':['原入口先由0状态2类称料的主/副卡字符串寻找主卡，不能直接用工卡条码绕过称料选择。',
            '最终称料左连接没有状态限制；NULL原卡号按原SQL变成单引号字符，不能替换为空串。',
            '无序标量按项目ID最后候选，TOP 1按连接来源ID第一候选；全部候选另列，见E85。']}


def prepare(weight,mode,query=rows):
    series=raw(weight,'SheetSeries');output=[];issues=[];phase_choices=[]
    details=matching(query('StuffWeightDetail','erp_production'),SheetSeries=series).order_by('pk')
    for detail in details:
        if mode=='standard':
            carry=raw(detail,'CarryIndex')
            if key('0' if carry is None else carry)!='0':
                output.append({name:raw(detail,name) for name in ['SheetSeries','PhaseNo','CarryIndex','StepName']})
            continue
        number=raw(detail,'PhaseNo')
        phases=matching(query('StuffWeightPhase','erp_production'),SheetSeries=series).filter(old_phase_no=number) if number is not None else query('StuffWeightPhase','erp_production').none()
        heads=list(matching(query('StuffWeight','erp_production'),SheetSeries=series).order_by('pk'))
        phases=list(phases.order_by('pk'))
        if not phases or not heads:issues.append({'record_id':detail.pk,'source': source_reference(detail),'issue':'原阶段/称料内连接无匹配'})
        for phase,head in product(phases,heads):
            base={'SheetSeries':raw(detail,'SheetSeries'),'JobSheetNo':raw(head,'JobSheetNo'),**{name:raw(phase,name) for name in ['ProgramID','BathRatio','WaterQty']},
                'CarryIndex':raw(detail,'CarryIndex'),'StepName':raw(detail,'StepName')}
            if mode=='lx':output.append({**base,'StuffNo':raw(detail,'StuffNo'),'PhaseNo':number});continue
            choices=list(matching(query('StuffWeightPhase','erp_production'),SheetSeries=varchar(series,100),ProgramID=varchar(raw(phase,'ProgramID'),50)).order_by('pk'))
            selected=None if not choices else raw(choices[0],'PhaseNo')
            selected=None if selected is None else varchar(str(selected),10)
            phase_choices.extend({'record_id':p.pk,'source': source_reference(p),'ProgramID':raw(p,'ProgramID'),'PhaseNo':raw(p,'PhaseNo'),'selected':p.pk==choices[0].pk} for p in choices)
            materials=list(matching(query('PStuff','erp_base'),StuffID=raw(detail,'StuffID')).order_by('pk'))
            if not materials:issues.append({'record_id':detail.pk,'source': source_reference(detail),'issue':'原染料/助剂字典内连接无匹配'})
            for material in materials:
                tank=raw(material,'TankNo');kind=raw(material,'StuffType')
                if (tank or 0)==0 and key(kind) in ['S','A']:tank=1 if key(kind)=='S' else 2
                def suffix(value):return None if value is None or selected is None else value+'-'+selected
                output.append({**base,'StuffSheetNo':suffix(raw(head,'SheetNo')),'StuffJobSheetNo':suffix(raw(head,'JobSheetNo')),
                    'PhaseNo':selected,'StuffType':kind,'TankNo':tank})
    # 原DISTINCT按SQL字符串等值去重，不包含项目ID。
    distinct={}
    for row in output:distinct.setdefault(tuple(key(v) if isinstance(v,str) else v for v in row.values()),row)
    output=list(distinct.values())
    if mode in ['standard','lx']:
        def order(value):return (value is not None,key(value) if isinstance(value,str) else value)
        output.sort(key=lambda row:(order(row['PhaseNo']),order(row['StepName'])) if mode=='standard' else (order(row['PhaseNo']),))
        for index,row in enumerate(output,1):row['uiTransIndex']=index
    return {'report':{'standard':'v_StuffWeightStep','lx':'v_StuffWeightStep_LX','to_lx':'v_StuffWeightStep_TO_LX'}[mode],
        'rows':output,'supplemental_rows':issues,'candidate_rows':phase_choices,
        'notes':['普通备料排除NULL/0的CarryIndex；两种立信准备视图原过滤已注释，0/空值仍参与。',
            '按原字段DISTINCT保留不同物料号、浴比、水量和槽号；TO_LX取同程序第一阶段而非当前阶段。',
            '无序TOP 1和ROW_NUMBER并列按来源ID确定，全部阶段候选另列。这里只生成原数据投影，不冒充已写入或收到中控回执。',
            'V_Progs_Step依赖192.168.23.254的ccs_erp七张外部表，当前本地资料不能复刻真实中控查询，见E89。']}
