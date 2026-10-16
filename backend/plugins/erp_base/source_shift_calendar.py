"""原循环排班、跨午夜班次及部门机台选择；计算与办理分开。"""
from plugins.erp_base.source_provenance import reference as source_reference
from datetime import datetime, timedelta
from uuid import uuid4
import re
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from .business import locked
from .source_stock_services import raw
from .source_quality_reports import rows
from .source_package_operations import reader, check_scope, effect
from .source_execution_state import active, require_available
from .source_continuation import origin, save_effect
from .source_package_labels import varchar
from .source_trial_steps import equal, sql_like


def wall(value):
    return timezone.localtime(value).replace(tzinfo=None) if isinstance(value,datetime) and timezone.is_aware(value) else value


def source(row):
    return {'record_id':row.pk,'source': source_reference(row),
        **{name:wall(raw(row,name)) for name in row.SOURCE_FIELDS if name not in ['Password']}}


def int32(value):
    if value is None:return None
    text=value.strip()
    if text and re.fullmatch(r'[+-]?[0-9]+',text) is None:
        raise ValueError('CycleDays不能按旧SQL转换为INT：'+repr(value))
    number=int(text) if text else 0
    if not -2147483648<=number<=2147483647:raise ValueError('原INT周期溢出：'+repr(value))
    return number


def add32(left,right):
    if left is None or right is None:return None
    return int32(str(left+right))


def slots(row,count=3):
    return {f'{prefix}{n:02}':varchar(row[f'{prefix}{n:02}'] or '',100 if prefix=='DateBetween' else 10)
        for n in range(1,count+1) for prefix in ['ShiftID','ClassID','DateBetween']}


def calendar_plan(configs,details,create_days):
    """输入为本地时间原字段字典；不写库，不修改输入，不丢弃未入选来源。"""
    report={'report':'Sp_CreateShiftAndClassDetail','rows':[],'candidate_rows':[],
        'result_rows':[],'supplemental_rows':[],'blocked':False,'retired_ids':[],
        'notes':['原GROUP BY无ORDER BY，按原ID、BeginDate升序取最后组；并列来源以本项目ID确定。全部候选列示。',
            '仅含“天”的周期参与总周期，游标仍读取全部最新配置；Mode不参与旧过程。',
            '零/负生成天数仍执行旧换版替换范围；生成与撤回原行留档。']}
    latest=max((r['BeginDate'] for r in configs if r['BeginDate'] is not None),default=None)
    current=sorted([r for r in configs if latest is not None and r['BeginDate']==latest],key=lambda r:(r['ID'],r['record_id']))
    groups={}
    for row in details:groups.setdefault((row['ID'],row['BeginDate']),[]).append(row)
    ordered=sorted(groups,key=lambda g:(g[0],g[1] or datetime.min))
    for identity in ordered:
        report['candidate_rows'].append({'ID':identity[0],'BeginDate':identity[1],
            'CurrDate':max(r['CurrDate'] or datetime(1900,1,1) for r in groups[identity]),
            'source_ids':[r['record_id'] for r in groups[identity]],'selected':identity==ordered[-1]})
    report['result_rows']=[{**r,'selected':r in current} for r in configs]
    try:
        all_days=0
        for row in current:
            if row['CycleDays'] is not None and '天' in row['CycleDays']:
                all_days=add32(all_days,int32(row['CycleDays'].replace('天','')))
        last=report['candidate_rows'][-1] if ordered else None
        last_date=last['CurrDate'] if last else datetime(2010,1,1)
        last_begin=last['BeginDate'] if last else None
        last_id=last['ID'] if last else 0
        seeds=[]
        if last is None:
            previous=max((r['BeginDate'] for r in configs if latest is not None and r['BeginDate'] is not None and r['BeginDate']<latest),default=None)
            seeds=sorted([r for r in configs if previous is not None and r['BeginDate']==previous],key=lambda r:(r['ID'],r['record_id']))
        elif last_begin is not None and latest is not None and last_begin!=latest:
            seeds=sorted([r for r in details if r['CurrDate']==latest],key=lambda r:r['record_id'])
            if seeds:last_id=seeds[-1]['ID']-1
            report['retired_ids']=[r['record_id'] for r in details if r['CurrDate'] is not None and r['CurrDate']>=latest]
        else:
            seed_date=last_date+timedelta(days=1-all_days)
            seeds=sorted([r for r in details if r['CurrDate']==seed_date],key=lambda r:r['record_id'])
        report['seed_rows']=[{**r,'selected':r==seeds[-1]} for r in seeds]
        last_shift=last_class=None
        if seeds:
            for n in [3,2,1]:
                if (seeds[-1][f'ShiftID{n:02}'] or '').rstrip(' '):
                    last_shift=varchar(seeds[-1][f'ShiftID{n:02}'],10)
                    last_class=varchar(seeds[-1][f'ClassID{n:02}'] or '',10);break
        report['summary']={'BeginDate':latest,'AllDays':all_days,'LastCreateDate':last_date,
            'LastBeginDate':last_begin,'LastMaxID':last_id,'CreateDays':create_days}
        for index in range(0 if create_days is None else max(0,create_days)):
            date=(last_date+timedelta(days=index+1) if last_date!=datetime(2010,1,1) and latest is not None and last_begin==latest
                else None if latest is None else latest+timedelta(days=index))
            diff=None if latest is None or date is None else (date.date()-latest.date()).days
            if diff is not None and all_days==0:raise ValueError('原总周期为0，DATEDIFF % AllDays发生除零，不能生成排班。')
            remain=None if diff is None else (abs(diff)%abs(all_days))*(-1 if diff<0 else 1)
            days=0
            for row in current:
                cycle=varchar(row['CycleDays'],10)
                days=add32(days,int32(None if cycle is None else cycle.replace('天','')))
                if remain is None or days is None or remain>=days:continue
                values=slots(row)
                values.update({f'{prefix}04':'' for prefix in ['ShiftID','ClassID','DateBetween']})
                for n in range(1,4):
                    shift,cls,window=[f'{prefix}{n:02}' for prefix in ['ShiftID','ClassID','DateBetween']]
                    value=values[window]
                    if not value.rstrip(' '):continue
                    start,end=value[:5],value[6:11]
                    if start=='00:00' or start.rstrip(' ')>end.rstrip(' '):
                        if start!='00:00':
                            values.update(ShiftID04=values[shift],ClassID04=values[cls],DateBetween04=start+'-23:59:59')
                            values[window]='00:00-'+end
                        values[shift],last_shift=last_shift,values[shift]
                        values[cls],last_class=last_class,values[cls]
                report['rows'].append({'ID':last_id+1+index,'CurrDate':date,'BeginDate':latest,**values,
                    'config_id':row['record_id'],'CycRemain':remain})
                break
            else:
                report['supplemental_rows'].append({'CurrDate':date,'CycRemain':remain,'issue':'原游标无命中；当天不插行，原索引仍递增。'})
    except (ValueError,OverflowError) as exc:
        report['blocked']=True
        report['supplemental_rows'].append({'issue':str(exc),'generated_before_error':len(report['rows'])})
    return report


def preview(create_days,query=rows):
    return calendar_plan([source(r) for r in query('PShiftArrange','erp_base').order_by('pk')],
        [source(r) for r in query('PShiftArrangeDetail','erp_base').order_by('pk')],create_days)


def select_shift(details,curr_time,machine,machines,departments,shifts):
    curr_time=wall(curr_time);machine=varchar(machine,100)
    if curr_time is not None:
        ticks=(curr_time.microsecond*300+500000)//1000000
        curr_time=curr_time.replace(microsecond=0)+timedelta(milliseconds=(ticks*1000+150)//300)
    candidates=sorted([r for r in details if curr_time is not None and r['CurrDate'] is not None and r['CurrDate'].date()==curr_time.date()],key=lambda r:r['record_id'])
    selected=candidates[-1] if candidates else None
    report={'report':'Sp_GetShiftAndClass3','rows':[],
        'candidate_rows':[{**r,'selected':r==selected} for r in candidates],
        'result_rows':[],'supplemental_rows':[],'needs_generation':not candidates,'blocked':False,
        'notes':['时分比较首含尾不含，秒不参与；四段依次判断，后命中段覆盖前段。',
            '结束文字严格RIGHT(5)：19:50-23:59:59得到59:59；ClassName原样返回选中班组名，ClassID来自p_Shift。',
            '同日无序多行按本项目ID取最后，全部候选保留；机台停用状态与班组审核状态不参与原过滤。']}
    last_shift=last_class=None
    if selected:
        values=slots(selected,4);hm=curr_time.strftime('%H:%M')
        for n in range(1,5):
            shift,cls,window=[values[f'{prefix}{n:02}'] for prefix in ['ShiftID','ClassID','DateBetween']]
            matched=bool(shift.rstrip(' ')) and hm>=window[:5].rstrip(' ') and hm<window[-5:].rstrip(' ')
            report['result_rows'].append({'slot':n,'ShiftID':shift,'ClassID':cls,'DateBetween':window,
                'DateStart':window[:5],'DateEnd':window[-5:],'GatherHM':hm,'matched':matched})
            if matched:last_shift,last_class=shift,cls
    report['summary']={'LastShiftID':last_shift,'LastClassID':last_class}
    for m in machines:
        if not equal(m['MachineID'],machine):continue
        depts=[d for d in departments if equal(d['DeptID'],m['DeptID'])]
        if not depts:report['supplemental_rows'].append({'machine_id':m['record_id'],'issue':'原机台部门没有匹配p_Dept，原查询不返回；机台资料保留。'})
        for d in depts:
            members=[s for s in shifts if equal(s['DeptID'],d['DeptID'])]
            for s in members or [None]:
                name=None if s is None else s['Name']
                if name is None:
                    report['supplemental_rows'].append({'machine_id':m['record_id'],'department_id':d['record_id'],
                        'shift_id':None if s is None else s['record_id'],'issue':'当前旧SQL的PATINDEX空名称返回NULL，原条件不命中；来源留档。'})
                elif last_shift is not None and sql_like(name,'%'+last_shift+'%'):
                    report['rows'].append({'ShiftID':s['ShiftID'],'ShiftName':name,'ClassID':s['ClassID'],'ClassName':last_shift,
                        'machine_id':m['record_id'],'department_id':d['record_id'],'shift_id':s['record_id']})
    return report


def lookup(curr_time,machine,query=rows):
    return select_shift([source(r) for r in query('PShiftArrangeDetail','erp_base').order_by('pk')],curr_time,machine,
        *[[source(r) for r in query(name,'erp_base').order_by('pk')] for name in ['PMachine','PDept','PShift']])


def lock_calendar(query):
    # 同一全局日历共享配置行锁，不按入口机台分别分配流水。
    configs=list(reader('PShiftArrange','erp_base').select_for_update().order_by('pk'))
    details=list(active(reader('PShiftArrangeDetail','erp_base')).select_for_update().order_by('pk'))
    check_scope([*configs,*details],query)
    return configs,details


@transaction.atomic
def generate(item,create_days,actor,at,reason,query=reader):
    configs,details=lock_calendar(query);check_scope([item],query);item=locked(item);require_available(item)
    report=calendar_plan([source(r) for r in configs],[source(r) for r in details],create_days)
    if report['blocked']:raise ValidationError({'source':[r['issue'] for r in report['supplemental_rows']]})
    from .source_services import write
    operation=str(uuid4());actions=[]
    previous=effect(item,'calendar_generation')
    for row in details:
        if row.pk in report['retired_ids']:
            actions.append({'kind':'retire','origin':origin(row),'previous':effect(row,'calendar_retained')})
            save_effect(row,'calendar_retained',{'active':True,'operation':operation},actor,reason)
    model=reader('PShiftArrangeDetail','erp_base').model
    for values in report['rows']:
        data={field:(timezone.make_aware(values[name]) if name in ['CurrDate','BeginDate'] and values[name] is not None else values[name])
            for name,field in model.SOURCE_FIELDS.items()}
        row=write(model,data,actor=actor,apply_effects=False)
        save_effect(row,'calendar_origin',{'operation':operation,'config_id':values['config_id']},actor,reason)
        actions.append({'kind':'create','origin':origin(row)});values['record_id']=row.pk
    save_effect(item,'calendar_generation',{'state':'applied','operation':operation,'at':at,'reason':reason,
        'actions':actions,'consumed_ids':[r.pk for r in details],'previous':previous},actor,reason)
    return report


@transaction.atomic
def resolve(item,curr_time,machine,actor,at,reason,query=reader):
    lock_calendar(query)
    result=lookup(curr_time,machine,query=lambda name,module:active(query(name,module)))
    if result['needs_generation']:
        generation=generate(item,365,actor,at,reason,query)
        result=lookup(curr_time,machine,query=lambda name,module:active(query(name,module)))
        result['generation']=generation
        result['supplemental_rows'].append({'issue':'已按原逻辑仅生成一次365天；目标日期仍缺失时不重复生成。','generated_count':len(generation['rows'])})
    return result


@transaction.atomic
def undo(item,actor,at,reason,query=reader):
    lock_calendar(query);check_scope([item],query);item=locked(item);value=effect(item,'calendar_generation')
    if value is None or value['state']!='applied':raise ValidationError({'source':'没有可撤回的日历生成。'})
    from .source_context import SourceDocumentContext
    created={a['origin']['source']['id'] for a in value['actions'] if a['kind']=='create'}
    for context in SourceDocumentContext.objects.filter(effects__has_key='calendar_generation'):
        other=context.effects['calendar_generation']
        if other['state']=='applied' and other['operation']!=value['operation'] and created.intersection(other['consumed_ids']):
            raise ValidationError({'source':'后续日历生成已采用本次明细，请先撤回后续生成。'})
    from django.apps import apps
    for action in reversed(value['actions']):
        saved=action['origin'];target=locked(apps.get_model(saved['entity']).objects.get(pk=saved['source']['id']));check_scope([target],query)
        if action['kind']=='create':require_available(target)
        elif effect(target,'calendar_retained')!={'active':True,'operation':value['operation']}:
            raise ValidationError({'source':'该日历行已参与后续替换，请先撤回后续办理。'})
        if any(getattr(target,f)!=target._meta.get_field(f).to_python(saved['source'][f]) for f in target.SOURCE_FIELDS.values()):
            raise ValidationError({'source':'本次日历已有字段变更，请先撤回对应修改。'})
        state={'active':True,'operation':value['operation'],'reversed_at':at} if action['kind']=='create' else action['previous'] or {'active':False}
        save_effect(target,'calendar_retained',state,actor,reason)
    save_effect(item,'calendar_generation',value['previous'] or {**value,'state':'reversed','reversed_at':at},actor,reason)
    return item
