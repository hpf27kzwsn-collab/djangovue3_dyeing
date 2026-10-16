"""机台方案到巡检/保养项目，保留旧APP两个保存过程的不同字段行为。"""
import re
import math
from django.core.exceptions import ValidationError
from django.db import transaction
from .business import locked
from .source_stock_services import raw
from .source_quality_reports import rows
from .source_package_operations import reader,check_scope
from .source_business_updates import matching
from .source_trial_steps import equal,sql_like
from .source_package_labels import varchar
from .source_shift_calendar import source,int32
from .source_context import SourceBusinessParameter
from .source_equipment_operations import Operation


def param(name):
    return SourceBusinessParameter.objects.filter(name=name).values_list('value',flat=True).first()


def employee_name(employee,query=rows):
    matches=list(matching(query('HEmployee','erp_base'),EmpID=employee).order_by('pk'))
    return None if not matches else raw(matches[-1],'Name')


def employee_names(ids,query=rows):
    names=None
    for employee in query('HEmployee','erp_base').only('id','old_emp_id','old_name').order_by('pk'):
        code=raw(employee,'EmpID')
        if ids is not None and code is not None and sql_like(';'+ids+';','%;'+code+';%'):
            name=raw(employee,'Name')
            names=None if name is None else ('' if names is None else names+';')+name
    return names or ''


def split_rows(value,separator='`'):
    if value is None:return []
    text=value.replace('\t','').replace('\n','').replace('\r','').strip(' ')
    parts=text.split(separator)
    if parts[-1]=='\\':parts.pop()
    # 原函数varchar(100)返回列；异常长原串仍由预览展示错误，不截成另一个项目。
    if any(len(p.encode('cp936',errors='replace'))>100 for p in parts):
        raise ValueError('原f_splitWithRowNo的varchar(100)结果列溢出。')
    return parts


def number_for(model,field,entry,actor,at):
    from .source_numbers import generate
    from .source_entry_registry import ENTRY_RULES
    return generate(model(),field,ENTRY_RULES[model._meta.label][entry]['number_fields'][field],actor,at)


def project_plan(case,changed_ids,changed_values,changed_results,query=rows):
    case=varchar(case,50);result={'report':'设备方案项目生成','rows':[],'candidate_rows':[],'supplemental_rows':[],'blocked':False,
        'notes':['原保存用方案流水直接匹配，不按机台或保养计划明细猜测方案。重复变更ID保留左连接倍增。',
            '旧无序UPDATE编号明确按来源项目ID、变更行序；三位RIGHT从000开始，1000后原后缀仍会重复，原行照存。']}
    if not case or not case.rstrip(' '):return result
    try:
        ids=split_rows(changed_ids);values=split_rows(changed_values);outcomes=split_rows(changed_results)
        edits=[{'CaseDetailNo':code,'Value':values[i] if i<len(values) else None,
            'Result':int32(outcomes[i]) if i<len(outcomes) else None,'change_index':i+1} for i,code in enumerate(ids)]
    except ValueError as exc:
        result['blocked']=True;result['supplemental_rows'].append({'issue':str(exc),'changed_ids':changed_ids,'changed_values':changed_values,'changed_results':changed_results});return result
    result['candidate_rows']=edits
    for project in matching(query('MachineCaseProject','erp_production'),SheetSeries=case).order_by('pk'):
        selected=[e for e in edits if equal(e['CaseDetailNo'],raw(project,'DetailNo'))]
        for edit in selected or [None]:
            value=raw(project,'DefaultValue') if edit is None or edit['Value'] is None else edit['Value']
            result['rows'].append({'source_id':project.pk,'legacy_id':project.legacy_id,'suffix':str(len(result['rows'])).zfill(3)[-3:],
                **{n:raw(project,n) for n in ['SortNo','SerialNum','ProjectInfo','DefaultValue','Remarks','IsInputText']},
                'Value':value,'CaseDetailNo':raw(project,'DetailNo'),'Result':None if edit is None else edit['Result']})
    matched={r['CaseDetailNo'].rstrip(' ').upper() for r in result['rows'] if r['CaseDetailNo'] is not None}
    result['supplemental_rows'] += [{**e,'issue':'变更ID未匹配方案项目，原值保留，不另造方案项目。'} for e in edits if e['CaseDetailNo'].rstrip(' ').upper() not in matched]
    return result


def case_projects(number,query=rows):
    number=varchar(number,50);cases=list(matching(query('MachineCase','erp_production'),SheetSeries=number).order_by('pk'));candidates=[]
    selected=cases[-1] if cases else None
    if selected is None or not (raw(selected,'SheetSeries') or '').rstrip(' '):
        for link in matching(query('MachineCaseDetail','erp_production'),MachineID=number).order_by('pk'):
            for case in matching(query('MachineCase','erp_production'),SheetSeries=raw(link,'SheetSeries')).order_by('pk'):
                candidates.append((case,link))
        candidates.sort(key=lambda pair:(raw(pair[0],'SheetDate') is not None,str(raw(pair[0],'SheetDate')),pair[0].pk,pair[1].pk))
        selected=candidates[-1][0] if candidates else None
    series=number if selected is None or raw(selected,'SheetSeries') is None else raw(selected,'SheetSeries')
    result=[]
    for p in matching(query('MachineCaseProject','erp_production'),SheetSeries=series).order_by('old_sort_no','pk'):
        serial=raw(p,'SerialNum');numeric=sql_numeric(serial)
        result.append({'caseDetailNo':raw(p,'DetailNo'),'SerialNum':serial or '','ProjectInfo':raw(p,'ProjectInfo') or '',
            'DefaultValue':raw(p,'DefaultValue') or '','VALUE':'','OriValue':raw(p,'DefaultValue') or '',
            'Result':0 if numeric else 4,'IsInputText':int(raw(p,'IsInputText') or 0),'record_id':p.pk,'legacy_id':p.legacy_id})
    return {'report':'sp_App_GetMachineCaseProject','rows':result,
        'candidate_rows':[{'record_id':c.pk,'SheetSeries':raw(c,'SheetSeries'),'selected':c==selected} for c in cases]+[
            {'record_id':c.pk,'link_id':l.pk,'SheetSeries':raw(c,'SheetSeries'),'selected':c==selected} for c,l in candidates],
        'notes':['直接方案优先，否则按机台选最新SheetDate方案；日期并列取最后项目ID。原ISNUMERIC的货币/科学记数不能简化为isdigit。']}


def sql_numeric(value):
    if value is None:return False
    text=value.strip()
    if text in ['+','-','$','￥','¥','.',',','\\']:return True
    text=re.sub(r'^([+-]?)[$￥¥]',r'\1',text).replace(',','')
    if not re.fullmatch(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eEdD][+-]?[0-9]+)?',text):return False
    return math.isfinite(float(text.replace('d','e').replace('D','e')))


@transaction.atomic
def save_projects(kind,item,values,case,changed_ids,changed_values,changed_results,actor,at,reason,query=reader):
    name,module,child,link=('InspectionLog','erp_quality','InspectionProject','InspectDetailNo') if kind=='inspection' else ('MachineCareRecords','erp_production','MachineCareProject','CarePlanDetailNo')
    model=reader(name,module).model;plan=project_plan(case,changed_ids,changed_values,changed_results,query)
    if plan['blocked']:raise ValidationError({'source':[r['issue'] for r in plan['supplemental_rows']]})
    check_scope(list(matching(reader('MachineCaseProject','erp_production'),SheetSeries=varchar(case,50))),query)
    op=Operation(actor,at,reason,query);created=item is None
    employee=varchar(values['employee'],50);empname=employee_name(employee,query)
    empname=(None if empname is None else empname[:10]) if kind=='inspection' else varchar(empname,60)
    data={link:varchar(case,50),'EmpID':employee,'MachineID':varchar(values['machine'],50),'MachineName':values['machine_name'],
        'MachineLocation':values['location'],'Remarks':values['remarks']}
    if kind=='inspection':data.update(SheetDate=values['sheet_date'],Inspector=employee,InspectorList=varchar(values['people'],200),InspectionSurvey=values['survey'])
    else:data.update(HandlerIDs=varchar(values['people'],50),HandleIdea=varchar(values['idea'],50),ResultID=varchar(values['result'],200))
    if created:
        series=number_for(model,'SheetSeries',name,actor,at)
        data.update(SheetSeries=series,SheetNo=series,CreateDate=at,Creater=empname)
        if kind=='inspection':data.update(SheetKind=0,InspectDate=values['performed_at'],Modifyer=None,ModifyDate=None)
        else:data.update(SheetDate=at,CareDate=values['performed_at'])
        item=op.create(name,module,data)
    else:
        item=locked(item);check_scope([item],query);series=raw(item,'SheetSeries')
        # 原保养@nowDate只在新增分支赋值，修改时为NULL；两个UPDATE都不写实际巡检/保养日期。
        data.update(Modifyer=empname,ModifyDate=at if kind=='inspection' else None)
        heads=list(matching(reader(name,module),SheetSeries=series).order_by('pk'))
        for head in heads:op.update(head,data)
    for old in matching(rows(child,module),SheetSeries=series).order_by('pk'):op.retire(old)
    for row in plan['rows']:
        data={k:row[k] for k in ['SortNo','SerialNum','ProjectInfo','Value','DefaultValue','Remarks','CaseDetailNo','Result','IsInputText']}
        for k in ['SerialNum','ProjectInfo','Value','DefaultValue']:data[k]='' if data[k] is None else data[k]
        for k in ['Result','IsInputText']:data[k]=0 if data[k] is None else data[k]
        op.create(child,module,{'SheetSeries':series,'DetailNo':series+'-'+row['suffix'],**data})
    op.finish(item,'sp_App_SaveInspectionLog' if kind=='inspection' else 'sp_App_SaveMachineCareRecords',project_plan=plan)
    return item


def record_projects(item,query=rows):
    inspection=item.SOURCE_TABLE=='InspectionLog';module='erp_quality' if inspection else 'erp_production'
    child='InspectionProject' if inspection else 'MachineCareProject';series=raw(item,'SheetSeries')
    projects=list(matching(query(child,module),SheetSeries=series).order_by('pk'))
    data=[]
    for row in projects:
        d=source(row);d.update(Result=raw(row,'Result') or 0,IsInputText=int(raw(row,'IsInputText') or 0),OriValue=raw(row,'Value'));data.append(d)
    if not projects and param('IsUseMachineInspectionCase' if inspection else 'IsUseMachineCase')=='Y':
        case=raw(item,'InspectDetailNo' if inspection else 'CarePlanDetailNo')
        heads=list(matching(query('MachineCase','erp_production'),SheetSeries=case).order_by('pk'))
        chosen=raw(heads[-1],'SheetSeries') if heads else None
        for row in matching(query('MachineCaseProject','erp_production'),SheetSeries=chosen).order_by('pk'):
            data.append({'SheetSeries':series,'DetailNo':'','SortNo':raw(row,'SortNo'),'SerialNum':raw(row,'SerialNum') or '',
                'ProjectInfo':raw(row,'ProjectInfo') or '','Value':'','DefaultValue':raw(row,'DefaultValue') or '',
                'Remarks':raw(row,'Remarks'),'CaseDetailNo':raw(row,'DetailNo'),'OriValue':raw(row,'DefaultValue') or '',
                'Result':0,'IsInputText':int(raw(row,'IsInputText') or 0),'source_id':row.pk})
    return {'report':'sp_App_GetInspectionLogBySheetSeries' if inspection else 'sp_App_GetMachineCareRecordsBySheetSeries','rows':data,
        'summary':{'IsUseMachineCase':int(bool(projects)),'SheetSeries':series},
        'notes':['原已有项目优先；启用方案且无项目时只从记录指定方案带出，原按机台猜测方案的代码已被注释。']}
