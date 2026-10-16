"""现场报工入口的原主从关联；不同入口保留不同连接宽度。"""
from plugins.erp_base.source_provenance import reference as source_reference
from .source_stock_services import raw
from .source_business_updates import matching
from .source_quality_reports import rows

LINKS={
    'DPWProcess': [('JobShiftEmp','JobShiftEmp',['WProcessNo']),('WProcessStep','DPWProcessStep',['WProcessNo'])],
    'DPWProcessEdit': [('JobShiftEmp','DPJobShiftEmpEdit',['WProcessNo'])],
    'AddWProcessEdit': [('JobShiftEmp','AddJobShiftEmpEdit',['WProcessNo','JobSheetNo','ProcessNo','ProcessID','ShiftID'])],
    'WProcessEdit': [('JobShiftEmp','JobShiftEmpEdit',['WProcessNo','JobSheetNo','ProcessNo','ProcessID','ShiftID'])],
}
COPY_FIELDS={'DPJobShiftEmpEdit':['JobSheetNo','ProcessID','ProcessNo','ShiftID'],
    'JobShiftEmpEdit':['JobSheetNo','ProcessID','ProcessNo','ShiftID'],
    'AddJobShiftEmpEdit':['JobSheetNo','ProcessNo','ProcessID','ShiftID']}


def bind(item,data,entry):
    if entry=='AddWProcessEdit' and 'old_end_time' not in data:item.old_end_time=item.old_start_time
    if entry not in COPY_FIELDS or item.source_parent_1_id is None:return
    parent=item.source_parent_1
    for name in COPY_FIELDS[entry]:
        field=item.SOURCE_FIELDS[name]
        if field not in data:setattr(item,field,raw(parent,name))


def linked(item,entry,query=rows):
    result=[];issues=[]
    for table,child_entry,fields in LINKS[entry]:
        source=matching(query(table,'erp_production'),WProcessNo=raw(item,'WProcessNo')).order_by('pk')
        for child in source:
            matched=all(raw(item,name) is not None and raw(child,name) is not None and
                (raw(item,name).rstrip(' ').upper()==raw(child,name).rstrip(' ').upper() if isinstance(raw(item,name),str) else raw(item,name)==raw(child,name)) for name in fields)
            row={'record_id':child.pk,'source': source_reference(child),'entity':child._meta.label,'entry':child_entry,
                **{name:raw(child,name) for name in child.SOURCE_FIELDS}}
            if matched:result.append(row)
            else:issues.append({**row,'issue':'同报工流水但不满足本入口原多列主从关系；原行保留'})
    return {'report':'现场报工主从：'+entry,'rows':result,'supplemental_rows':issues,
        'notes':['DP刷卡入口按报工流水关联；一般登记和刷卡补录按工卡、工序序号、工序、班组及流水关联。',
            '新增明确关联的员工明细继承原主从字段/Parent公式；主动填写的不同原码保留并列明，不强制归并。',
            'AddDyeWProcessStep为独立染色补录原表，资料没有其自动生成WProcessStep的保存过程；保留独立录入，不补造转写。']}


def job_records(job,query=rows):
    from .source_shift_calendar import source
    number=raw(job,'SheetNo');work=list(matching(query('WProcess','erp_production'),JobSheetNo=number).order_by('pk'))
    return {'report':'工卡现场报工及独立染色补录','rows':[source(r) for r in work],
        'candidate_rows':[source(r) for r in matching(query('WProcessStep','erp_production'),JobSheetNo=number).order_by('pk')],
        'supplemental_rows':[source(r) for r in matching(query('AddDyeWProcessStep','erp_sampling'),JobSheetNo=number).order_by('pk')],
        'notes':['WProcess与WProcessStep逐条列示；独立AddDyeWProcessStep在补充页保留，不合并计量或自动转成正式工步。',
            '原现场入口的1=2用于空白录入窗初始化，不代表这些业务不能录入。异常原码、NULL、负数及重复记录全部保留。']}


def create_record(job,entry,values,actor):
    from .source_package_operations import reader
    from .source_services import write
    from .source_execution_state import require_available
    require_available(job)
    independent=entry=='AddDyeWProcessStep'
    model=reader('AddDyeWProcessStep' if independent else 'WProcess','erp_sampling' if independent else 'erp_production').model
    data={'JobSheetNo':raw(job,'SheetNo'),'ProcessID':values['process'],'ProcessNo':values['process_no']}
    if independent:
        data.update(RecordID=values['employee'],CurrTime=values['start'],RealValue=values['real_value'],ProgramID=values['program'],
            DyeProcessID=values['dye_process'],MachineNo=values['machine'],Rolls=values['rolls'],WeightQty=values['weight'],Remarks=values['remarks'])
    else:
        data.update(EmpID=values['employee'],StartTime=values['start'],MachineID=values['machine'],ShiftID=values['shift'],
            ClassID=values['class_id'],StationID=values['station'],CurrRolls=values['rolls'],CurrKg=values['weight'],
            CurrMeter=values['length'],DyeState=values['dye_state'],Memo=values['remarks'])
        if values['end'] is not None:data['EndTime']=values['end']
    return write(model,{'_entry':entry,**{model.SOURCE_FIELDS[k]:v for k,v in data.items()}},actor=actor)
