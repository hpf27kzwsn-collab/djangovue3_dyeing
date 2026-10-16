"""DPJobStep_Test的候选称料、班组已做次数和原相关子查询。"""
from collections import Counter
import re
from .source_stock_services import raw
from .source_business_updates import matching
from .source_quality_reports import rows,key
from .source_package_labels import varchar


def equal(left,right):return left is not None and right is not None and key(left)==key(right)


def sql_like(value,pattern):
    if value is None or pattern is None:return False
    tokens=[];i=0
    while i<len(pattern):
        c=pattern[i]
        if c=='%':tokens.append('.*')
        elif c=='_':tokens.append('.')
        elif c=='[':
            end=pattern.find(']',i+2)
            if end<0:return False
            content=pattern[i+1:end];tokens.append('['+content.replace('\\','\\\\')+']');i=end
        else:tokens.append(re.escape(c))
        i+=1
    return re.fullmatch(''.join(tokens),value,flags=re.IGNORECASE|re.DOTALL) is not None


def preview(job,process,process_no,employee,query=rows,variant='test'):
    number=varchar(raw(job,'SheetNo'),50);process=varchar(process,50);employee=varchar(employee,20)
    candidates=[]
    source=matching(query('StuffWeight','erp_production'),ProcessID=process).filter(old_sheet_kind=2,old_recipe_type__in=[0,2]).order_by('pk')
    for item in source.only('id','legacy_id','old_job_sheet_no','old_combine_sheet_nos','old_sheet_status').iterator():
        if variant=='formal' and (raw(item,'SheetStatus') or 0)!=0:continue
        if equal(raw(item,'JobSheetNo'),number) or sql_like(raw(item,'CombineSheetNos'),None if number is None else '%'+number+'%'):candidates.append(item)
    actual=varchar(raw(candidates[-1],'JobSheetNo'),50) if candidates else None
    steps=list(matching(query('WProcessStep','erp_production'),JobSheetNo=actual).order_by('pk'))
    joined=[]
    for step in steps:
        for person in matching(query('JobShiftEmp','erp_production'),JobSheetNo=actual,WProcessNo=raw(step,'WProcessNo'),EmpID=raw(step,'RecordID'),ProcessID=raw(step,'ProcessID')).filter(old_process_no=raw(step,'ProcessNo')).order_by('pk') if raw(step,'ProcessNo') is not None else []:
            joined.append((step,person))
    done=Counter()
    for step,person in joined:
        shift=raw(person,'ShiftID')
        if process_no is not None and raw(step,'ProcessNo')==process_no and equal(raw(step,'ProcessID'),process) and shift is not None and employee is not None and key(shift)!=key(employee):
            identity=(key(raw(step,'ProgramID')),key(raw(step,'DyeProcessID')))
            done[identity]+=int(raw(step,'RealValue') is not None)
    expected=[];unmatched=[]
    for weight in matching(query('StuffWeight','erp_production'),JobSheetNo=actual,ProcessID=process).order_by('old_sheet_series','pk'):
        if (raw(weight,'SheetStatus') or 0) in [8,9,10] or (raw(weight,'SheetKind') or 0) not in [0,2] or (raw(weight,'RecipeType') or 0) not in [0,2]:
            unmatched.append({'weight_id':weight.pk,'legacy_id':weight.legacy_id,'issue':'原第二轮状态/类型/配方条件不进入步骤'});continue
        phases=list(matching(query('StuffWeightPhase','erp_production'),SheetSeries=raw(weight,'SheetSeries')).order_by('old_phase_no','pk'))
        if not phases:unmatched.append({'weight_id':weight.pk,'issue':'原称料没有匹配阶段'})
        for phase in phases:
            curves=list(matching(query('PDyeCurve','erp_base'),PhaseID=raw(phase,'PhaseID')).order_by('pk'))
            if not curves:unmatched.append({'weight_id':weight.pk,'phase_id':phase.pk,'PhaseID':raw(phase,'PhaseID'),'issue':'原阶段与染色曲线无对应，保留原阶段'})
            for curve in curves:
                if (raw(curve,'IsStop') or 0)!=0 or (raw(curve,'DyePhase') or 0)!=1:
                    unmatched.append({'phase_id':phase.pk,'curve_id':curve.pk,'issue':'原曲线停用或不是染色曲线'});continue
                curve_steps=list(matching(query('PDyeCurveDetail','erp_base'),CurveID=raw(curve,'CurveID')).order_by('old_step_no','pk'))
                if not curve_steps:unmatched.append({'phase_id':phase.pk,'curve_id':curve.pk,'issue':'原曲线没有步骤明细'})
                for step in curve_steps:
                    program=raw(phase,'ProgramID');dye=raw(step,'DyeProcessID')
                    count=done[(key(program),key(dye))] if program is not None and dye is not None else 0
                    default=raw(step,'DefaultValue');limit=None if default is None else max(default-count,0)
                    expected.append({'weight':weight,'phase':phase,'curve':curve,'step':step,'DoneValue':count,'LimitValue':limit})
    # SQL只声明的四列：#t里没有ProgramID/JobSheetNo，这两个未限定名称绑定到外层#wps。
    temp=[]
    for step in steps:
        matched=[row for row in expected if equal(raw(step,'ProgramID'),raw(row['step'],'CurveID')) and equal(raw(step,'DyeProcessID'),raw(row['step'],'DyeProcessID'))]
        for row in matched:temp.append((raw(step,'ProcessNo'),raw(row['step'],'DyeProcessID')))
    def order(value):return (value is not None,value)
    expected.sort(key=lambda r:(order(key(raw(r['weight'],'SheetSeries'))),order(raw(r['phase'],'PhaseNo')),order(key(raw(r['step'],'CurveID'))),order(raw(r['step'],'StepNo')),r['weight'].pk,r['phase'].pk,r['step'].pk))
    result=[];excluded=unmatched
    for index,row in enumerate(expected,1):
        step=row['step'];curve=raw(step,'CurveID');dye=raw(step,'DyeProcessID');blockers=[]
        first=process_no is not None and any(no==process_no and equal(value,dye) for no,value in temp)
        second=process_no is not None and any(raw(other,'ProcessNo')==process_no and equal(raw(other,'ProgramID'),curve) and equal(raw(other,'DyeProcessID'),dye) for other in steps)
        for other,person in joined:
            if not equal(raw(other,'ProgramID'),curve) or not equal(raw(other,'DyeProcessID'),dye) or not equal(raw(other,'ProcessID'),process):continue
            no=raw(other,'ProcessNo');shift=raw(person,'ShiftID');compared=employee if second else ''
            eligible_no=(process_no is not None and no==process_no) if variant=='formal' else no is not None and (not first or no==process_no)
            if eligible_no and shift is not None and compared is not None and key(shift)!=key(compared):
                blockers.append({'step_id':other.pk,'person_id':person.pk})
        values={name:raw(step,name) for name in step.SOURCE_FIELDS}
        values.update(RowNum=index,DoneValue=row['DoneValue'],LimitValue=row['LimitValue'],record_id=step.pk,legacy_id=step.legacy_id,
            weight_id=row['weight'].pk,phase_id=row['phase'].pk,curve_id=row['curve'].pk)
        if blockers:excluded.append({**values,'blockers':blockers,'issue':'原NOT EXISTS排除，保留来源'})
        else:result.append(values)
    return {'report':'DPJobStep' if variant=='formal' else 'DPJobStep_Test','rows':result,'supplemental_rows':excluded,
        'candidate_rows':[{'record_id':r.pk,'legacy_id':r.legacy_id,'JobSheetNo':raw(r,'JobSheetNo'),'CombineSheetNos':raw(r,'CombineSheetNos'),'selected':r.pk==candidates[-1].pk} for r in candidates],
        'notes':[('正式版首轮要求状态0；NOT EXISTS只按指定工序号，不套用试验版跨曲线#t条件。' if variant=='formal' else '试验版首轮不限制状态，保留跨曲线#t条件。'),
            '保留原合卡字符串LIKE、2类称料首轮及第二轮0/2类范围；无ORDER BY的称料赋值按项目ID最后候选。',
            '已做量是COUNT(RealValue)，不是SUM；原EmpID参数实际和ShiftID比较，不能换成人员工号。',
            '本查询不生成设备完成回传，也不把LimitValue为0自动当作设备已完成。']}
