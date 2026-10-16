"""原工序机台列表与进缸机台查询；仅投影，不替用户改报工机台。"""
from plugins.erp_base.source_provenance import reference as source_reference
from datetime import datetime,timedelta
from django.utils import timezone
from .source_quality_reports import rows,key
from .source_stock_services import raw
from .source_business_updates import matching
from .source_package_labels import varchar
from .source_trial_steps import equal
from .source_shift_calendar import source,wall


def split_machines(value):
    # New_StringSplit(';')逐个去首尾空格，保留中间空段，不产生末尾分号后的空段。
    if value is None or not value.rstrip(' '):return []
    text=value.rstrip(' ');parts=text.split(';')
    if text.endswith(';'):parts.pop()
    return [part.strip(' ') for part in parts]


def entered_machine(number,query=rows):
    number=varchar(number,100)
    work=list(matching(query('WProcess','erp_production'),JobSheetNo=number,ProcessID='GX07').exclude(old_machine_id=None).order_by('pk'))
    work=[r for r in work if raw(r,'MachineID').rstrip(' ')]
    jobs=list(matching(query('JobSheet','erp_production'),SheetNo=number).order_by('pk'))
    a=varchar(raw(work[0],'MachineID'),100) if work else None
    b=None if not jobs or raw(jobs[-1],'StereotypesName') is None else varchar(raw(jobs[-1],'StereotypesName')[:3],100)
    return {'report':'Fn_Get_Machine','rows':[{'JobSheetNo':number,'MachineID':b if not a else a}],
        'candidate_rows':[{'record_id':r.pk,'source': source_reference(r),'MachineID':raw(r,'MachineID'),'selected':r==work[0]} for r in work],
        'result_rows':[{'record_id':r.pk,'source': source_reference(r),'StereotypesName':raw(r,'StereotypesName'),'selected':r==jobs[-1]} for r in jobs],
        'notes':['GX07非空机台TOP1原无排序，明确取本项目ID第一条，全部候选保留。没有报工机台时取最后工卡StereotypesName前三个字符，不查排程。']}


def choices(number,shift,employee,process,as_of,query=rows):
    number=varchar(number,20);shift=varchar(shift,40);employee=varchar(employee,60);process=varchar(process,40)
    as_of=timezone.make_aware(wall(as_of))
    report={'report':'qry_ProcessMachine','rows':[],'candidate_rows':[],'result_rows':[],
        'supplemental_rows':[],'blocked':False,
        'notes':['原标量多候选按项目ID确定最后行；最新报工时间并列按项目ID最后行。全部候选列出。',
            '06工位按机型、员工机台名单、近30天进缸状态和2026年以来最后复版审核状态筛选；其他工位按StationID与原AA规则筛选。',
            '停用机台不额外删除；NULL排除名单按原NOT IN语义影响全部候选。筛掉的机台及原因列在补充明细。']}
    machines=list(query('PMachine','erp_base').order_by('pk'));jobs=list(matching(query('JobSheet','erp_production'),SheetNo=number).order_by('pk'))
    for job in jobs:
        text=raw(job,'StereotypesName')
        if text is not None and not text.rstrip(' '):
            report['blocked']=True;report['supplemental_rows'].append({'job_id':job.pk,'StereotypesName':text,'issue':'原LEFT(StereotypesName,LEN-1)长度为负，旧查询报错；原工卡保留。'})
            continue
        machine_code=None if text is None else text[:len(text.rstrip(' '))-1]
        assigned=[m for m in machines if equal(raw(m,'MachineID'),machine_code)]
        schedules=list(matching(query('ProcessSchedule','erp_production'),JobSheetNo=raw(job,'SheetNo')).order_by('pk'))
        for schedule in schedules or [None]:
            for machine in assigned or [None]:
                planned=None if schedule is None else raw(schedule,'StereotypesName')
                kind=(None if machine is None else raw(machine,'KindName')) if planned is None else planned
                report['candidate_rows'].append({'job_id':job.pk,'schedule_id':None if schedule is None else schedule.pk,
                    'machine_id':None if machine is None else machine.pk,'StereotypesName':varchar(kind,50)})
    for i,row in enumerate(report['candidate_rows']):row['selected']=i==len(report['candidate_rows'])-1
    kind=report['candidate_rows'][-1]['StereotypesName'] if report['candidate_rows'] else None
    processes=list(matching(query('PProcess','erp_base'),ProcessID=process).order_by('pk'))
    people=list(matching(query('PShiftEmp','erp_base'),EmpID=employee,ShiftID=shift).order_by('pk'))
    station=None if not processes else varchar(raw(processes[-1],'StationID'),50)
    allowed=None if not people else varchar(raw(people[-1],'MachineID'),500)
    members=split_machines(allowed)
    report['summary']={'StationID':station,'StereotypesName':kind,'MachineIDs':allowed,'as_of':wall(as_of)}
    report['seed_rows']=[{'table':'p_Process','record_id':r.pk,'StationID':raw(r,'StationID'),'selected':r==processes[-1]} for r in processes]
    report['seed_rows'] += [{'table':'p_ShiftEmp','record_id':r.pk,'MachineIDs':raw(r,'MachineID'),'selected':r==people[-1]} for r in people]
    if any(len(s.encode('utf-16-le'))>400 for s in members):
        report['blocked']=True;report['supplemental_rows'].append({'issue':'原New_StringSplit返回列nvarchar(200)溢出；名单原值保留。'})
    if report['blocked']:return report
    busy=[];reprint=[]
    if equal(station,'06'):
        recent=matching(query('WProcess','erp_production'),StationID=station).filter(old_start_time__gt=max(as_of-timedelta(days=30),timezone.make_aware(datetime(2025,2,28)))).order_by('old_start_time','pk')
        latest={}
        for w in recent.only('id','old_machine_id','old_dye_state','old_start_time').iterator():
            for machine in machines:
                if equal(raw(machine,'MachineID'),raw(w,'MachineID')) and equal(raw(machine,'KindName'),kind):
                    latest[key(raw(w,'MachineID'))]=w
                    report['result_rows'].append({'source':'recent_start','record_id':w.pk,'MachineID':raw(w,'MachineID'),
                        'DyeState':raw(w,'DyeState'),'StartTime':raw(w,'StartTime'),'joined_machine_id':machine.pk})
        busy=[raw(w,'MachineID') for w in latest.values() if raw(w,'DyeState') is not None and key(raw(w,'DyeState')) not in ['3','4','5','7']]
        latest_created={}
        for w in matching(query('WProcess','erp_production'),StationID='06').filter(old_create_date__gt=timezone.make_aware(datetime(2026,1,1))).order_by('old_create_date','pk').only('id','old_machine_id','old_dye_state','old_right_status','old_create_date').iterator():
            latest_created[key(raw(w,'MachineID'))]=w
        for w in latest_created.values():
            report['result_rows'].append({'source':'last_created','record_id':w.pk,'MachineID':raw(w,'MachineID'),
                'DyeState':raw(w,'DyeState'),'RightStatus':raw(w,'RightStatus'),'CreateDate':raw(w,'CreateDate')})
            if (raw(w,'RightStatus') or 0)==0 and equal(raw(w,'DyeState'),'5'):reprint.append(raw(w,'MachineID'))
        for r in report['result_rows']:
            r['selected']=r['source']=='last_created' or r['record_id']==latest[key(r['MachineID'])].pk
    for machine in machines:
        code=raw(machine,'MachineID');reasons=[]
        if equal(station,'06'):
            if not equal(raw(machine,'KindName'),kind):reasons.append('原机型不匹配')
            if not any(equal(code,s) for s in members):reasons.append('不在原员工机台名单')
            if None in busy or any(equal(code,s) for s in busy):reasons.append('原最近进缸状态未释放')
            if None in reprint or any(equal(code,s) for s in reprint):reasons.append('原最后复版未审核（含NULL名单的NOT IN效应）')
        else:
            if not equal(raw(machine,'StationID'),station):reasons.append('原工位不匹配')
            if allowed is not None and not equal(allowed,'AA') and not any(equal(code,s) for s in members):reasons.append('不在原员工机台名单')
        data=source(machine)
        if reasons:report['supplemental_rows'].append({**data,'issue':'；'.join(reasons)})
        else:report['rows'].append(data)
    return report
