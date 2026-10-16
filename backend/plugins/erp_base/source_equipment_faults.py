"""原设备报修、流转、签到、配件提交轮次和维修结果触发。"""
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from .business import locked
from .source_stock_services import raw
from .source_quality_reports import rows
from .source_business_updates import matching
from .source_package_operations import reader,check_scope
from .source_trial_steps import equal,sql_like
from .source_package_labels import varchar
from .source_equipment_projects import param,employee_name,employee_names,number_for
from .source_equipment_operations import Operation
from .source_shift_calendar import source,int32,wall


ACTIONS=['受理','指派','签到','取消签到','提交','退回','确认','拒绝','评价','评论','关闭','恢复','重新提交']
PROCEDURES={'受理':'Accept','指派':'Accept','签到':'SignIn','取消签到':'SignIn','提交':'Commit','退回':'Commit',
    '确认':'Confirm','拒绝':'Confirm','评价':'Evaluate','评论':'Remark','关闭':'Close','恢复':'Close','重新提交':'Close'}


def blank(value):return value is None or value.rstrip(' ')==''


def heads(item,query=rows):
    return list(matching(query('MachineFault','erp_production'),SheetSeries=varchar(raw(item,'SheetSeries'),50)).order_by('pk'))


def check_action(item,action,fixers,query=rows):
    selected=heads(item,query);target=selected[-1] if selected else None
    status=None if target is None else raw(target,'FlowStatus');start=None if target is None else raw(target,'StartTime')
    states=list(matching(query('PMachineFaultStatus','erp_base'),StatusName=status).order_by('pk'))
    kind=None if not states else raw(states[-1],'StatusType');code=0;message=''
    if blank(action):code,message=-1,'动作(Action)不能为空！'
    elif action=='签到':
        if status is not None and not equal(status,'待维修'):code,message=-111,'[待维修]状态下才能签到，请检查！'
        if start is not None:code,message=-112,'当前单据已于['+wall(start).strftime('%Y-%m-%d %H:%M')[-11:]+']签到，请勿重复操作！'
    elif action=='取消签到':
        if status is not None and not equal(status,'待维修'):code,message=-121,'待维修状态下才能取消签到，请检查！'
        if start is None:code,message=-112,'当前单据尚未签到，请检查！'
    elif action=='恢复' and not equal(kind,'已关闭'):code,message=-101,'当前工单未关闭，无需恢复！'
    elif action=='关闭' and equal(kind,'已关闭'):code,message=-201,'当前工单已关闭，请勿重复操作！'
    elif action=='指派' and blank(fixers):code,message=-802,'指派的维修工不能为空！'
    elif action not in [*ACTIONS,'修改']:code,message=-10086,'没有【'+action+'】这个动作，请检查或联系管理员！'
    return {'report':'sp_App_FalutAction_Check','rows':[{'Code':code,'Msg':message}],
        'candidate_rows':[{'record_id':r.pk,'FlowStatus':raw(r,'FlowStatus'),'StartTime':raw(r,'StartTime'),'selected':r==target} for r in selected],
        'notes':['只恢复原有效检查；原提交/确认/拒绝/受理等状态检查已被注释，不新增状态限制。']}


def actions(item,employee,version=2,query=rows):
    employee=varchar(employee,50);selected=heads(item,query);target=selected[-1] if selected else None
    people=list(matching(query('HEmployee','erp_base'),EmpID=employee).order_by('pk'));person=people[-1] if people else None
    status=None if target is None else raw(target,'FlowStatus')
    reportman=None if target is None else varchar(raw(target,'EmpID'),50)
    fixers=None if target is None else varchar(raw(target,'HandlerIDs'),128)
    level=None if person is None else raw(person,'MFLevel');give=None if person is None else raw(person,'MFGiveOut')
    isreport=equal(reportman,employee);isfix=employee is not None and fixers is not None and (';'+employee+';').upper() in (';'+fixers+';').upper()
    flags={k:0 for k in ['修改','关闭','受理','指派','提交','退回','确认','拒绝','评价','恢复','评论']+(['签到','取消签到'] if version==2 else [])}
    result=[];issues=[]
    try:claim=int32(param('MachineFault_FixManGetBill'));confirm=int32(param('MachineFault_ReportManConfirm'));simple=int32(param('MachineFault_FlowType'))
    except ValueError as exc:
        return {'report':'sp_App_GetFaultActions'+('2' if version==2 else ''),'rows':[], 'supplemental_rows':[{'issue':str(exc)}],'blocked':True}
    def allow(*names):
        for name in names:flags[name]=1;result.append(name)
    if equal(status,'待指派'):
        if isreport:allow('修改','关闭')
        elif level is not None and level>=2 and claim==1:allow('受理')
        if give:allow('指派')
        if simple==1 and (isreport or level==3):allow('确认','拒绝')
    elif equal(status,'待维修'):
        if isfix or level==3:
            allow('提交','退回')
            if version==2:
                result.append('签到');flags['签到' if raw(target,'StartTime') is None else '取消签到']=1
        if give:allow('指派')
    elif equal(status,'待确认'):
        if confirm==0 and (isreport or level==3) or confirm==1 and isreport:allow('确认','拒绝')
    elif equal(status,'已确认'):
        if isreport or level==3:allow('评价')
    elif equal(status,'已关闭'):
        if level==3:allow('恢复')
    if level==3 and status is not None and not equal(status,'已关闭'):allow('关闭')
    allow('评论')
    return {'report':'sp_App_GetFaultActions'+('2' if version==2 else ''),
        'rows':[{'Action':','.join(result),'isFixMan':int(isfix),'isReportMan':int(isreport),'MFLevel':level,'FlowStatus':status,**flags}],
        'candidate_rows':[{'record_id':p.pk,'EmpID':raw(p,'EmpID'),'MFLevel':raw(p,'MFLevel'),'MFGiveOut':raw(p,'MFGiveOut'),'selected':p==person} for p in people],
        'supplemental_rows':issues,'notes':['原按钮列表与动作检查分别展示；新版Action文字仍可能写签到而取消签到标志为1，保留原差异。管理者关闭文字可重复。']}


def fault_check(values):
    code=0;message=''
    if blank(values['fault']):code,message=-102,'故障描述不能为空！'
    if blank(values['machine']) and blank(values['machine_name']):code,message=-100,'设备编号和设备名称不能为空！'
    if param('MachineFault_UseFaultClass')=='2' and blank(values['fault_class']):code,message=-103,'故障分类不能为空！'
    if param('MachineFault_UseSendTo')=='2' and blank(values['group']):code,message=-103,'维修分组不能为空！'
    return {'report':'sp_App_CheckMachineFaultBill','rows':[{'Code':code,'Msg':message}],
        'notes':['按原IF顺序后项覆盖前项；被注释的经营单位、地点和单据类型检查不新增。普通原表录入仍可留存不满足APP保存检查的异常资料。']}


def triggered_values(item,values,at):
    result=values['ResultID'] if 'ResultID' in values else raw(item,'ResultID')
    return {**values,'EndTime':at} if equal(result,'3') or sql_like(result,'%已修%') else values


def trigger(item,actor,at=None):
    at=timezone.now() if at is None else at
    if not triggered_values(item,{},at):return
    from .source_operation_effects import change
    for target in matching(reader('MachineFault','erp_production'),SheetSeries=varchar(raw(item,'SheetSeries'),100)).order_by('pk'):
        change(target,{'EndTime':at},[],actor,'原MachineFault_Update结束时间回写')
    item.refresh_from_db()


def record(op,series,employee,action,remarks,fixers='',handlers='',score=None):
    return op.create('MachineFaultRecord','erp_production',{'SheetSeries':series,'Operator':employee,'Action':action,
        'ActionType':'评论' if action=='评论' else '流转','HandlerIDs':fixers,'Handlers':handlers,'Remark':remarks,'RecordDate':op.at,'Score':score})


@transaction.atomic
def perform(item,action,employee,fixers,remarks,score,actor,at,reason,query=reader):
    item=locked(item);check_scope([item],query);employee=varchar(employee,20);remarks=None if remarks is None else remarks[:200]
    fixers=fixers[:200] if action in ['签到','取消签到'] and fixers is not None else varchar(fixers,100)
    check=check_action(item,action,fixers,query)
    if check['rows'][0]['Code']!=0:raise ValidationError({'source':check['rows'][0]['Msg']})
    targets=heads(item,reader);check_scope(targets,query);op=Operation(actor,at,reason,query)
    series=varchar(raw(item,'SheetSeries'),50);name=employee_name(employee,query);name=None if name is None else name[:10]
    data={};log_fixers='';handlers='';log_score=None;notices=[]
    if action in ['受理','指派']:
        fixers=None if blank(fixers) else fixers
        actual=employee if fixers is None else fixers
        data={'HandlerIDs':actual,'ApplyTime':at,'FlowStatus':'待维修','Handlers':employee_names(actual,query),'ApplyMan':employee if name is None else name,'ApplyIdea':remarks}
        log_fixers=fixers
    elif action in ['提交','退回']:
        if blank(fixers):fixers=varchar(raw(targets[-1],'HandlerIDs'),100) if targets else fixers
        log_fixers=fixers
        if action=='退回':data={'HandlerIDs':'','HandleIdea':'','FlowStatus':'待指派','Handlers':''}
        else:
            data={'HandlerIDs':fixers,'HandleIdea':remarks,'EndTime':at,'FlowStatus':'待确认','Handlers':employee_names(fixers,query)}
            parts=list(matching(rows('MachineFaultArticleInfo','erp_production'),SheetSeries=series).order_by('pk'));check_scope(parts,query)
            log_score=max([raw(p,'Rounds') for p in parts if raw(p,'Rounds')>=0],default=0)+1
            for part in parts:
                if raw(part,'Rounds')==-1:op.update(part,{'Rounds':log_score})
    elif action in ['确认','拒绝']:
        data={'FlowStatus':'已确认' if action=='确认' or int32(param('MachineFault_FlowType'))==1 else '待维修'}
    elif action=='评价':data={'FlowStatus':'已评价'};log_score=score
    elif action=='评论':op.create('MachineFaultComment','erp_production',{'SheetSeries':series,'SheetDate':at,'Creater':employee,'Remark':remarks})
    elif action in ['签到','取消签到']:
        # 原变量同一SELECT被FaultID覆盖，不能擅自改回HandlerIDs。
        if blank(fixers):fixers=(varchar(raw(targets[-1],'FaultID'),100) or '') if targets else ''
        log_fixers=fixers;handlers=employee_names(fixers,query)
        data={'StartTime':at if action=='签到' else None,'SeverityID':employee if action=='签到' else None}
    elif action=='关闭':data={'RightStatus':10,'FlowStatus':'已关闭'}
    elif action=='重新提交':
        data={'RightStatus':10,'FlowStatus':'待指派'}
        notices=[{'ReceiverID':raw(targets[-1],'EmpID'),'SenderID':employee,'Sender':name,'NoticeKind':3,'NoticeWay':9,'FlowID':'000001',
            'Subject':None if raw(targets[-1],'SheetNo') is None else '维修单【'+raw(targets[-1],'SheetNo')+'】有问题，已重新提交，请修改！','Content':remarks}] if targets else []
    elif action=='恢复':data={'RightStatus':0,'FlowStatus':'待指派','ApplyMan':'','ApplyIdea':'','ApplyTime':None,'HandlerIDs':'','Handlers':'','HandleIdea':''}
    for target in targets:
        if data:op.update(target,triggered_values(target,data,at))
    record(op,series,employee,action,remarks,log_fixers,handlers,log_score)
    op.finish(item,'sp_App_FalutAction_'+PROCEDURES[action],notification_sources=notices,notification_delivery='not_connected')
    item.refresh_from_db();return item


@transaction.atomic
def save_fault(item,values,actor,at,reason,query=reader):
    checked=fault_check(values)
    if checked['rows'][0]['Code']!=0:raise ValidationError({'source':checked['rows'][0]['Msg']})
    model=reader('MachineFault','erp_production').model;created=item is None;op=Operation(actor,at,reason,query)
    employee=varchar(values['employee'],50);name=employee_name(employee,query);name=None if name is None else name[:10]
    machine=varchar(values['machine'],50);machine_name=values['machine_name'][:64] if values['machine_name'] is not None else None
    machines=[m for m in query('PMachine','erp_base').order_by('pk') if equal(raw(m,'MachineID'),machine) or equal(raw(m,'Name'),machine_name)]
    dept=raw(machines[-1],'DeptID') if machines else None
    business=raw(machines[-1],'BusinessUnitID') if machines else values['business_unit']
    data={'MachineID':machine,'MachineName':machine_name,'MachineLocation':values['location'],'EmpID':employee,'ShiftID':varchar(values['shift'],20),
        'Urgent':values['urgent'],'FaultRemarks':values['fault'],'DeptID':dept,'BusinessUnitID':varchar(business,20),'FaultClass':values['fault_class'],
        'EmpGroup':values['group'],'MachineClass':values['machine_class']}
    if created:
        series=number_for(model,'SheetSeries','MachineFault',actor,at);number=number_for(model,'SheetNo','MachineFault',actor,at)
        data.update(SheetSeries=series,SheetNo=number,SheetDate=at,SheetKind='普通报修' if blank(values['sheet_kind']) else values['sheet_kind'],
            HappenTime=at,FaultID='',Remarks=varchar(values['remarks'],512),Creater=name,CreateDate=at,RightStatus=0,PhotoAddress=None,FlowStatus='待指派')
        item=op.create('MachineFault','erp_production',data)
    else:
        item=locked(item);check_scope([item],query);series=raw(item,'SheetSeries');data.update(Modifyer=name,ModifyDate=at)
        for target in heads(item,reader):op.update(target,triggered_values(target,data,at))
    record(op,series,employee,'创建' if created else '修改',varchar(values['remarks'],512))
    uploads=values['uploads'];bound=[]
    if not blank(uploads):
        guids=uploads.split(';')
        for attachment in reader('APPUploadFilesInfo','erp_base').order_by('pk'):
            if any(equal(raw(attachment,'Guid'),guid) for guid in guids):
                op.update(attachment,{'SheetSeries':series});bound.append(attachment.pk)
    notices=[]
    if created:
        for employee_row in matching(query('HEmployee','erp_base'),EmpKind='设备部主管').order_by('pk'):
            if raw(employee_row,'IsOut') in [None,False,0]:
                notices.append({'ReceiverID':raw(employee_row,'EmpID'),'SenderID':employee,'Sender':name,'NoticeKind':3,'NoticeWay':9,'FlowID':'000001',
                    'Subject':None if machine is None else '机台【'+machine+'】有新的维修单产生，需要指派维修工','NoticeUrl':'/pages/user/rests/equipmentRepairDetails?id='+series+'&isApp=1'})
    op.finish(item,'sp_App_SaveMachineFaultBill',bound_attachment_ids=bound,notification_sources=notices,notification_delivery='not_connected')
    return item


def history(item,query=rows):
    from .source_package_operations import effect
    series=raw(item,'SheetSeries')
    operation=effect(item,'equipment_operation')
    return {'report':'设备维修流转与原评论','rows':[source(r) for r in matching(query('MachineFaultRecord','erp_production'),SheetSeries=series).order_by('-old_record_date','pk')],
        'supplemental_rows':[source(r) for r in matching(query('MachineFaultComment','erp_production'),SheetSeries=series).order_by('pk')],
        'candidate_rows':[] if operation is None else [{**n,'delivery':operation['notification_delivery']} for n in operation['notification_sources']],
        'notes':['逐条展示原流转和评论；备注、重复记录、未知动作及原Score均保留。Score在提交动作中为配件轮次，在评价中为评分。']}
