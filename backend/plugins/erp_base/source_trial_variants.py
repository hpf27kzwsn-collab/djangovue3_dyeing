"""原测试单各入口及加色产量接续；试验原值和被替换报工均留档。"""
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from .business import persist,record,snapshot,locked
from .source_stock_services import raw
from .source_quality_reports import key
from .source_business_updates import matching
from .source_package_operations import reader,scoped,check_scope,effect
from .source_execution_state import active,require_available
from .source_continuation import origin,save_effect
from .source_chain_reverse import capture
from .source_operation_effects import restore
from .source_sequences import SourceIdentitySequence


def saved(item,entry,actor):
    if entry!='ProdTest_AddColorProduct':return
    at=timezone.now();reason='采用原加色产量登记AfterSaveSQL'
    previous=effect(item,'trial_work')
    if previous is not None and previous['state']=='applied':undo(item,actor,at,reason)
    apply(item,actor,at,reason)


def preview(item,query=reader):
    candidates=[];sources=[item]
    trials=matching(reader('ProdTest','erp_quality'),SheetSeries=raw(item,'SheetSeries')).filter(old_sheet_kind=7).order_by('pk')
    for trial in trials:
        sources.append(trial)
        members=list(matching(active(reader('PShiftEmp','erp_base')),EmpID=raw(trial,'EmpID') or '').order_by('pk'));sources.extend(members)
        for member in members:
            for shift in matching(reader('PShift','erp_base'),ShiftID=raw(member,'ShiftID'),StationID='02').order_by('pk'):
                sources.append(shift)
                candidates.append({'trial_id':trial.pk,'member_id':member.pk,'shift_id':shift.pk,
                    'eligible':key(raw(trial,'Value40')) not in [None,''],'ShiftID':raw(shift,'ShiftID'),'ClassID':raw(shift,'ClassID')})
    works=list(matching(active(reader('WProcess','erp_production')),OrderSheetNo=raw(item,'SheetSeries')).order_by('pk'))
    children=[]
    for work in works:
        for table in ['JobShiftEmp','WProcessStep']:
            children.extend(matching(active(reader(table,'erp_production')),WProcessNo=raw(work,'WProcessNo')).order_by('pk'))
    children=list({(row._meta.label,row.pk):row for row in children}.values())
    check_scope([*sources,*works,*children],query)
    left,right=raw(item,'StuffID'),raw(item,'CompareStuffID')
    report={'report':'试验及加色产量来源','rows':[{'record_id':item.pk,'SheetKind':raw(item,'SheetKind'),
        'StuffID':left,'CompareStuffID':right,'original_comparison_passed':left is None or right is None or key(left)==key(right),
        'ProcessID':raw(item,'Value38'),'MachineID':raw(item,'Value39'),'PhaseID':raw(item,'Value40')}],
        'candidate_rows':candidates,'supplemental_rows':[{'entity':row._meta.label,'record_id':row.pk,'issue':'本次实际生成时替换留档'} for row in [*works,*children]],
        'notes':['七类试验入口沿用原默认字段，全部Value原结果保留。原不同物料禁止保存改为明确比较结果，异常试验可录入，见E81。',
            '7类且Value40非空并有02工位班组才生成；旧游标反复覆盖改为明确最后ID候选，全部候选留档。']}
    return report,candidates,works,children


def identifier(at,namespace):
    prefix=timezone.localtime(at).strftime('%y%m%d%H%M%S')
    sequence,_=SourceIdentitySequence.objects.get_or_create(namespace=namespace+prefix)
    sequence=locked(sequence);sequence.last_number+=1;persist(sequence)
    return prefix+str(sequence.last_number).zfill(5)


@transaction.atomic
def apply(item,actor,at,reason,query=reader):
    from .source_services import write
    from .source_work_delete import trigger_removed
    item=scoped(item,query);previous=effect(item,'trial_work')
    if previous is not None and previous['state']=='applied':raise ValidationError({'source':'先撤回当前试验报工，再重新生成。'})
    report,candidates,works,children=preview(item,query)
    states=[];created=[]
    eligible=[row for row in candidates if row['eligible']]
    with capture() as changes:
        if eligible:
            for row in [*works,*children]:
                states.append({'source':origin(row),'previous':effect(row,'trial_retained')})
                save_effect(row,'trial_retained',{'active':True,'trial_id':item.pk,'at':at},actor,reason)
            if works:trigger_removed(works[-1],actor,retain_children=True)
            candidate=eligible[-1];source=reader('ProdTest','erp_quality').get(pk=candidate['trial_id'])
            process=raw(source,'Value38');special=key(process)=='GX41'
            number=identifier(at,'ProdTest.WProcess.');end=raw(source,'CreateDate')
            data={'WProcessNo':number,'JobSheetNo':raw(source,'JobSheetNo'),'OrderSheetNo':raw(source,'SheetSeries'),
                'ProcessNo':67 if special else 68,'ProcessID':process,'EmpID':raw(source,'EmpID'),
                'ClassID':candidate['ClassID'],'ShiftID':candidate['ShiftID'],'StationID':'02','MachineID':raw(source,'Value39'),
                'PrevProcessID':raw(source,'Value40'),'StartTime':end,'EndTime':end,'CurrVats':1,'WorkQty':1}
            def create(name,values):
                model=reader(name,'erp_production').model
                row=write(model,{model.SOURCE_FIELDS[name]:value for name,value in values.items()},actor=actor,apply_effects=False)
                save_effect(row,'trial_origin',{'trial_id':item.pk,'source':origin(item),'at':at,'reason':reason},actor,reason)
                created.append(origin(row));return row
            work=create('WProcess',data)
            common={name:data[name] for name in ['WProcessNo','JobSheetNo','ProcessNo','ProcessID']}
            create('JobShiftEmp',{**common,'ShiftID':candidate['ShiftID'],'EmpID':data['EmpID'],'EffiRate':1})
            create('WProcessStep',{**common,'WPStepNo':identifier(at,'ProdTest.WProcessStep.'),'DyeProcessID':'加色' if special else '返加色',
                'RealValue':1,'RecordID':data['EmpID'],'CurrTime':end,'ProgramID':'933' if special else '934'})
    # 新建对象不进入逐字段restore；原行留档事实由states恢复。
    changes=[row for row in changes if row['entity']!='erp_base.SourceDocumentContext' and (row['entity'],row['id']) not in {(entry['entity'],entry['source']['id']) for entry in created}]
    check_scope([apps.get_model(row['entity']).objects.get(pk=row['id']) for row in changes],query)
    save_effect(item,'trial_work',{'state':'applied','at':at,'reason':reason,'report':report,'states':states,'created':created,'changes':changes},actor,reason)
    return {**report,'result_rows':[{'entity':entry['entity'],'record_id':entry['source']['id']} for entry in created]}


@transaction.atomic
def undo(item,actor,at,reason,query=reader):
    item=scoped(item,query);value=effect(item,'trial_work')
    if value is None or value['state']!='applied':raise ValidationError({'source':'没有可撤回的试验报工。'})
    targets=[]
    for entry in value['created']:
        target=locked(apps.get_model(entry['entity']).objects.get(pk=entry['source']['id']))
        require_available(target)
        retired=effect(target,'trial_retained')
        if retired is not None and retired['active']:
            raise ValidationError({'source':'此试验报工已被后续试验替换，请先撤回后续办理。'})
        if any(getattr(target,field)!=target._meta.get_field(field).to_python(entry['source'][field]) for field in target.SOURCE_FIELDS.values()):
            raise ValidationError({'source':'试验生成报工已有后续字段变化，请先处理对应业务。'})
        targets.append(target)
    originals=[apps.get_model(entry['source']['entity']).objects.get(pk=entry['source']['source']['id']) for entry in value['states']]
    check_scope([*targets,*originals,*[apps.get_model(row['entity']).objects.get(pk=row['id']) for row in value['changes']]],query)
    restore(value['changes'],actor,reason)
    for target in targets:save_effect(target,'trial_retained',{'active':True,'trial_id':item.pk,'reversed_at':at},actor,reason)
    for entry,target in zip(value['states'],originals):save_effect(target,'trial_retained',entry['previous'] or {'active':False,'reversed_at':at},actor,reason)
    save_effect(item,'trial_work',{**value,'state':'reversed','reversed_at':at,'reverse_reason':reason},actor,reason)
    return item
