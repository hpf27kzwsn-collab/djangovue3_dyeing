"""班组排班审核、原报工人员重建及明确撤回；替换原行继续留档。"""
from decimal import Decimal,ROUND_HALF_UP,ROUND_DOWN
from uuid import uuid4
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from .business import locked
from .source_stock_services import raw
from .source_quality_reports import key,total,rows
from .source_package_labels import varchar
from .source_business_updates import matching
from .source_package_operations import reader,scoped,check_scope,effect
from .source_execution_state import active,require_available
from .source_continuation import origin,save_effect


def proportion(employee,number,query=rows):
    employee=varchar(employee,10);number=varchar(number,20)
    members=list(matching(query('JobShiftEmp','erp_production'),WProcessNo=number).order_by('pk'))
    selected=[m for m in members if key(raw(m,'EmpID'))==key(employee) and employee is not None]
    def rate(m):return Decimal(1) if raw(m,'EffiRate') is None else raw(m,'EffiRate')
    rounding=lambda value:None if value is None else value.quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
    numerator=rounding(rate(selected[-1])) if selected else None
    denominator=rounding(total([rate(m) for m in members]));issues=[]
    if any(v is not None and abs(v)>Decimal('999.99') for v in [numerator,denominator]):
        value=None;issues.append({'issue':'原decimal(5,2)变量溢出，原数保留，比例不能等价求得'})
    elif denominator==0 and numerator is not None:
        value=None;issues.append({'issue':'原比例分母为0会报除零，保留原人员及费率，比例列为NULL'})
    else:
        value=None if numerator is None or denominator is None else (numerator/denominator).quantize(Decimal('.00000001'),rounding=ROUND_DOWN).quantize(Decimal('.0001'),rounding=ROUND_HALF_UP)
        if value is not None and abs(value)>Decimal('99.9999'):
            value=None;issues.append({'issue':'原decimal(6,4)返回值溢出，比例列为NULL'})
    return {'report':'GetPropOfJobShiftEmp','rows':[{'EmpID':employee,'WProcessNo':number,'EmpRate':numerator,'SumRate':denominator,'Prop':value}],
        'candidate_rows':[{'record_id':m.pk,'legacy_id':m.legacy_id,'EmpID':raw(m,'EmpID'),'EffiRate':raw(m,'EffiRate'),'selected':bool(selected) and m.pk==selected[-1].pk} for m in members],
        'supplemental_rows':issues,'notes':['原参数截断为工号10字节/报工号20字节；个人率和总率先转两位小数再求四位比例。',
            '同员工多行按最后来源ID取个人率，总率仍包含全部人员行；NULL率取1，零率、负率原值保留。']}


def group_members(values):
    query=matching(active(reader('JobShiftEmp','erp_production')),**{name:values[name] for name in ['JobSheetNo','ShiftID','ProcessID','WProcessNo']})
    return query.none() if values['ProcessNo'] is None else query.filter(old_process_no=values['ProcessNo']).order_by('pk')


def plan(item,query=reader):
    heads=list(matching(reader('ShiftArrange','erp_production'),SheetSeries=varchar(raw(item,'SheetSeries'),30)).order_by('pk'))
    head=heads[-1] if heads else None;groups={};sources=[item,*heads]
    details=[]
    if head is not None:
        details=list(matching(reader('ShiftArrangeDetail','erp_production'),Sheetseries=raw(head,'SheetSeries')).order_by('pk'));sources.extend(details)
        start,end=raw(head,'StartTime'),raw(head,'EndTime')
        work=matching(active(reader('WProcess','erp_production')),ShiftID=varchar(raw(head,'ShiftID'),10))
        work=work.none() if start is None or end is None else work.filter(old_create_date__gte=start,old_create_date__lt=end)
        for record in work.order_by('pk'):
            sources.append(record)
            values={name:raw(record,name) for name in ['JobSheetNo','ShiftID','ProcessNo','ProcessID','WProcessNo']}
            members=list(group_members(values));sources.extend(members)
            for member in members or [None]:
                extra={name:None if member is None else raw(member,name) for name in ['EffiRate','Remarks','Modifyer','ModifyDate']}
                groupkey=tuple(key(v) if isinstance(v,str) else v for v in [*values.values(),*extra.values()])
                group=groups.setdefault(groupkey,{**values,**extra,'SumCount':0,'work_ids':[]});group['SumCount']+=1;group['work_ids'].append(record.pk)
    check_scope(sources,query)
    return {'report':'UpdateJobShiftEmp','rows':list(groups.values()),
        'candidate_rows':[{'record_id':h.pk,'legacy_id':h.legacy_id,'selected':h==head} for h in heads],
        'result_rows':[{'record_id':d.pk,'legacy_id':d.legacy_id,'ShiftID':raw(d,'ShiftID'),'EmpID':raw(d,'EmpID')} for d in details],
        'notes':['按WProcess.CreateDate首含尾不含筛选，不能改成开始/结束报工时间。',
            '原GROUP BY含费率、备注、修改人和时间，不按工卡去重；每组删原班组再插入本排班全部明细，异班组及重复明细继续保留。',
            '原INSERT不写EffiRate/Post/Remarks，不继承旧率；新行采用原表默认。未匹配员工的报工仍参与一次左连接。']},details


def retire(row,operation,actions,actor,reason,query):
    row=locked(row);check_scope([row],query)
    actions.append({'kind':'retire','origin':origin(row),'previous':effect(row,'shift_retained')})
    save_effect(row,'shift_retained',{'active':True,'operation':operation},actor,reason)


def create(name,module,data,operation,actions,actor,reason):
    from .source_services import write
    model=reader(name,module).model
    row=write(model,{model.SOURCE_FIELDS[k]:v for k,v in data.items()},actor=actor,apply_effects=False)
    save_effect(row,'shift_origin',{'operation':operation},actor,reason)
    actions.append({'kind':'create','origin':origin(row)})
    return row


@transaction.atomic
def apply(item,actor,at,reason,query=reader):
    item=scoped(item,query);require_available(item)
    report,details=plan(item,query);operation=str(uuid4());actions=[]
    previous=effect(item,'shift_work')
    for group in report['rows']:
        # FETCH INTO原参数长度在这里生效；保留隐藏分组造成的重复迭代。
        values={name:varchar(group[name],size) for name,size in [('JobSheetNo',50),('ShiftID',10),('ProcessID',10),('WProcessNo',50)]}
        values['ProcessNo']=group['ProcessNo']
        for member in group_members(values):retire(member,operation,actions,actor,reason,query)
        for detail in details:
            create('JobShiftEmp','erp_production',{**values,'ShiftID':raw(detail,'ShiftID'),'EmpID':raw(detail,'EmpID'),'ModifyDate':at,'Modifyer':None},operation,actions,actor,reason)
    value={'state':'applied','operation':operation,'at':at,'reason':reason,'actions':actions,'previous':previous}
    save_effect(item,'shift_work',value,actor,reason)
    return {**report,'result_rows':[{'kind':a['kind'],'entity':a['origin']['entity'],'record_id':a['origin']['source']['id']} for a in actions]}


@transaction.atomic
def undo(item,actor,at,reason,query=reader):
    item=scoped(item,query);value=effect(item,'shift_work')
    if value is None or value['state']!='applied':raise ValidationError({'source':'没有可撤回的排班报工调整。'})
    for action in reversed(value['actions']):
        source=action['origin'];target=locked(apps.get_model(source['entity']).objects.get(pk=source['source']['id']));check_scope([target],query)
        if action['kind']=='create':require_available(target)
        elif effect(target,'shift_retained')!={'active':True,'operation':value['operation']}:
            raise ValidationError({'source':'本人员已被后续班组调整处理，请先撤回后续调整。'})
        if any(getattr(target,f)!=target._meta.get_field(f).to_python(source['source'][f]) for f in target.SOURCE_FIELDS.values()):
            raise ValidationError({'source':'本次人员已有后续字段变动，请先撤回对应后续办理。'})
        state={'active':True,'operation':value['operation'],'reversed_at':at} if action['kind']=='create' else action['previous'] or {'active':False}
        save_effect(target,'shift_retained',state,actor,reason)
    save_effect(item,'shift_work',value['previous'] or {**value,'state':'reversed','reversed_at':at,'reverse_reason':reason},actor,reason)
    return item


def trigger(item,data,created,actor,at=None):
    if created:return
    at=timezone.now() if at is None else at;shift=varchar(raw(item,'ShiftID'),20);series=varchar(raw(item,'SheetSeries'),20)
    date=raw(item,'SheetDate');status=raw(item,'RightStatus');notes=[]
    if 'old_right_status' in data:
        if status==10:
            matches=matching(reader('ShiftArrange','erp_production'),ShiftID=shift,SheetSeries=series)
            count=sum(raw(h,'SheetNo') is not None and raw(h,'SheetDate') is not None and
                (timezone.localtime(at).replace(minute=0,second=0,microsecond=0)-timezone.localtime(raw(h,'SheetDate')).replace(minute=0,second=0,microsecond=0)).total_seconds()/3600<12 for h in matches)
            if count<1:raise ValidationError({'old_right_status':'原排班审核要求DATEDIFF(HOUR,SheetDate,当前时间)<12；本单不满足。'})
            details=list(matching(reader('ShiftArrangeDetail','erp_production'),Sheetseries=raw(item,'SheetSeries')).order_by('pk'))
            operation=str(uuid4());actions=[];reason='原ShiftArrange_Update审核同步班组人员'
            for member in matching(active(reader('PShiftEmp','erp_base')),ShiftID=shift).order_by('pk'):
                if not any(raw(d,'EmpID') is not None and raw(d,'ShiftID') is not None and key(raw(d,'EmpID'))==key(raw(member,'EmpID')) and key(raw(d,'ShiftID'))==key(raw(member,'ShiftID')) for d in details):retire(member,operation,actions,actor,reason,reader)
            # 原INSERT SELECT的NOT EXISTS基于语句执行前状态，重复明细可同时插入。
            existing=list(active(reader('PShiftEmp','erp_base')))
            copies=matching(reader('ShiftArrange','erp_production'),SheetSeries=raw(item,'SheetSeries')).count()
            for detail in details:
                if not any(raw(detail,'EmpID') is not None and raw(detail,'ShiftID') is not None and key(raw(detail,'EmpID'))==key(raw(m,'EmpID')) and key(raw(detail,'ShiftID'))==key(raw(m,'ShiftID')) for m in existing):
                    from .source_trial_variants import identifier
                    for _ in range(copies):create('PShiftEmp','erp_base',{'SerialNumber':identifier(at,'ShiftArrange.PShiftEmp.'),
                        **{name:raw(detail,name) for name in ['ShiftID','EmpID']}},operation,actions,actor,reason)
            save_effect(item,'shift_master_sync',{'state':'applied','at':at,'actions':actions},actor,reason)
        elif status==0 and date is not None:
            newer=matching(reader('ShiftArrange','erp_production'),ShiftID=shift).filter(old_sheet_date__gt=date,old_sheet_no__isnull=False).exists()
            if newer:raise ValidationError({'old_right_status':'该班组存在更晚排班，原规则不允许反审。'})
    if {'old_sheet_date','old_shift_id'}.intersection(data) and date is not None:
        same=matching(reader('ShiftArrange','erp_production'),ShiftID=shift).filter(old_sheet_date__date=timezone.localtime(date).date(),old_sheet_no__isnull=False)
        if same.count()>1:notes.append({'issue':'原触发器禁止同班组同日重复排班；按项目要求原值保留，不删重。','record_ids':list(same.values_list('pk',flat=True))})
    if notes:save_effect(item,'shift_trigger_check',{'rows':notes},actor,'原重复排班检查结果留档')
