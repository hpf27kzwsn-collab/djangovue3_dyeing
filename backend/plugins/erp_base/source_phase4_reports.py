"""生产、称料、包装和设备原查询。固定原投影，按当前用户数据权限执行。"""
import json
from datetime import timedelta
from pathlib import Path
from math import ceil
from sqlglot import exp,parse_one
from .source_quality_reports import rows
from .source_static_lookup import execute
from .source_phase3_sql import bind
from .source_foundation_view_reports import statement
from .source_business_updates import matching
from .source_stock_services import raw
from django.utils import timezone
from .source_phase2_reports import date,temporary_views
from .source_foundation_app_reports import shift_month


def setting(name,query):
    selected=list(matching(query('SSysParams','erp_base'),ParamName=name).order_by('pk'))
    return None if not selected else raw(selected[-1],'ParamValue')

QUERIES=json.loads(Path(__file__).with_name('source_phase4_queries.json').read_text(encoding='utf8'))


def with_employee_names(sql,p,query):
    return execute(bind(sql,p),query)


def report(name,p,query=rows,now=None):
    spec=QUERIES[name];p={**p};result_sets=[];temps=dict(spec.get('temps',{}));statements=spec.get('sql',[])
    now=(timezone.localtime() if now is None else now).replace(tzinfo=None)
    from .source_phase4_report_details import prepare,special
    statements=prepare(name,p,temps,statements,query,now)
    if spec['kind']=='special':return special(name,p,temps,statements,query,now)
    if name in ['Sp_APP_QueryGetClothNotice','Sp_AppQueryJobSheetProgress','SP_Sp_QueryGetClothNoticeInfo']:
        month=now.replace(day=1,hour=0,minute=0,second=0,microsecond=0)
        p.update(dtstart=date(p['startdate']) or month,dtend=date(p['enddate']) or shift_month(month,1)-timedelta(days=1))
    if name in ['Sp_JobSheetNum2','Sp_ProductionReports3','Sp_ProductionReports4','Sp_APP_QueryJobSheetState']:
        base=now if name=='Sp_APP_QueryJobSheetState' else date(p['ymdate'])
        day=None if base is None else base.replace(hour=0,minute=0,second=0,microsecond=0)
        shift=timedelta(hours=7.5) if name in ['Sp_ProductionReports3','Sp_ProductionReports4'] else timedelta()
        p.update(daystartdate=None if day is None else day+shift,dayenddate=None if day is None else day+timedelta(days=1,milliseconds=-3)+shift,
            monthstartdate=None if day is None else day.replace(day=1)+shift,monthenddate=None if day is None else day+timedelta(days=1,milliseconds=-3)+shift)
        p.update({k:None for k in ['a1','a2','a3','a4','a5','a6','b1','b2','b3','b4','b5','b6','alldaykg','allmonthkg']})
    if name=='SP_DPWorkQty' and p['startdate'] is not None and p['enddate'] is not None:
        if (date(p['startdate']).date()-date(p['enddate']).date()).days>31:p['enddate']=shift_month(date(p['startdate']),-1)
    p['stereotypesname1']=p.get('stereotypesname') or ''
    if name in ['Sp_WorkQty_AvueDate_Query']:
        p.update(dsdate=(now-timedelta(days=7)).date().isoformat(),dtdate=now.date().isoformat())
    if name in ['SP_APP_QueryFaultAVGTime','SP_APP_QueryFaultMonthByEmp']:
        day=date(p['dtdate']);day=now if day is None or day.year==1900 else day;day=day.replace(hour=0,minute=0,second=0,microsecond=0)
        p.update(dtdate=day,dtstart=day-timedelta(days=p['countday']),dtend=day)
        if name=='SP_APP_QueryFaultAVGTime':
            temps['dtlist']=' UNION ALL '.join("SELECT CAST('"+shift_month(day,i).strftime('%Y-%m')+"' AS VARCHAR(50)) AS dtName" for i in range(-5,1))
    if name in ['sp_App_QueryInspectionLogByPage','sp_App_QueryMachineCareRecordList']:
        p.update(enddate=now+timedelta(days=1),startdate=shift_month(now+timedelta(days=1),-12),size=20)
    if name=='sp_App_QueryMachineFaultByPage':
        flow=setting('MachineFault_FlowType',query)
        candidates=list(matching(query('MachineFaultFilter','erp_production'),FlowType=flow,TabID=str(p['searchmode'])).order_by('pk'))
        p.update(flowtypefiller=None if not candidates else raw(candidates[-1],'FilterSQL'),hasfilter=int(bool(p['confilter'])),size=20)
        p['flowtypefiller']=p['flowtypefiller'] or ''
    if name in ['sp_App_GetMachineFault','sp_App_QueryMachineList']:
        p.update(contmachine=int(bool(p.get('machineid') if name=='sp_App_GetMachineFault' else p['confilter'])),contstatus=int(bool(p.get('status'))))
        if name=='sp_App_GetMachineFault':temps['v_app_resultstatus']="SELECT Code,Name AS FaultStatus FROM dye.p_FieldValid WHERE FieldType='Result'"
    if spec['kind']=='machine_choices':
        selected=0 if setting('IsUseMachineCase',query) in ['Y','1'] else 1
        p.update(contmachine=int(bool(p['confilter'])),size=20)
        statements=['SELECT ROW_NUMBER() OVER(ORDER BY MachineID DESC) AS rowindex,* FROM ('+statements[selected]+') _choices']
    if name=='sp_APP_GetSingleMachineFaultInfo':
        fault=list((matching(query('MachineFault','erp_production'),SheetNo=p['sheetno']) | matching(query('MachineFault','erp_production'),SheetSeries=p['sheetno'])).order_by('pk'))
        p['sheetseries']=None if not fault else raw(fault[-1],'SheetSeries')
        for action,fields in [('提交',{'fixman':"dye.ChangeIDListToEmpName(md.HandlerIDs,';')",'fixremarks':'md.Remark','fixtime':'CONVERT(VARCHAR(16),md.RecordDate,21)','rounds':'md.Score'}),
              ('确认',{'grade':"''",'feedbackman':'h.Name','feedbackremarks':'md.Remark','feedbacktime':'CONVERT(VARCHAR(16),md.RecordDate,21)'}),
              ('评价',{'score':'md.Score','evaluateman':'h.Name','evaluateinfo':'md.Remark','evaluatetime':'CONVERT(VARCHAR(16),md.RecordDate,21)'})]:
            sql='SELECT TOP 1 '+','.join(v+' AS '+k for k,v in fields.items())+' FROM dye.MachineFaultRecord md LEFT JOIN dye.h_Employee h ON h.EmpID=md.Operator WHERE md.SheetSeries=@sheetseries AND md.Action=@action ORDER BY md.RecordDate DESC'
            found=with_employee_names(sql,{**p,'action':action},query);p.update(found[0] if found else dict.fromkeys(fields))
        scores=query('PFieldValid','erp_base').filter(old_field_type='FaultScore',old_num_value=p['score']).order_by('pk') if p['score'] is not None else query('PFieldValid','erp_base').none()
        scores=list(scores);p['scorename']=None if not scores else raw(scores[-1],'Name')
    if name=='v_StuffWeightQuery_To_LX':
        from .source_static_lookup import VIEWS
        fields=['ProgNo','ProgId','MachineId'];parts=[]
        for item in p.get('machine_programs',[]):
            parts.append('SELECT '+','.join('CAST('+exp.convert(item.get(f)).sql(dialect='tsql')+' AS VARCHAR(100)) AS '+f for f in fields))
        definition=' UNION ALL '.join(parts) if parts else 'SELECT '+','.join('CAST(NULL AS VARCHAR(100)) AS '+f for f in fields)+' WHERE 1=0'
        tree=temporary_views(parse_one(VIEWS[name.lower()],read='tsql').expression,{'v_machine_processid':definition})
        return {'report':name,'rows':execute(tree.sql(dialect='tsql'),query),
            'external_verification':'待现场中控程序核验','notes':['外部中控程序由machine_programs提供，逐行连接且不去重；未提供时本地称料记录仍返回，ProgId/MachineId为空。']}
    if spec['kind']=='view':
        return {'report':name,'rows':execute(statement(name,p.get('filters',[])),query)}
    if name in ['sp_App_GetFaultArticleListBySheetSeries','sp_App_GetFilesInfoBySheetSeries','sp_APP_GetMachineFaultComment']:
        from django.db.models import Q
        selected=list((matching(query('MachineFault','erp_production'),SheetSeries=p['sheetseries']) | matching(query('MachineFault','erp_production'),SheetNo=p['sheetseries'])).order_by('pk'))
        if selected:p['sheetseries']=raw(selected[0] if name=='sp_APP_GetMachineFaultComment' else selected[-1],'SheetSeries') or p['sheetseries']
        if name=='sp_App_GetFaultArticleListBySheetSeries' and (p['rounds']==0 or p['rounds']<-1):
            from django.db.models import Max
            p['rounds']=matching(query('MachineFaultArticleInfo','erp_production'),SheetSeries=p['sheetseries']).aggregate(value=Max('old_rounds'))['value']
    if name=='sp_App_sysGetMachineFaultTab':
        settings=list(matching(query('SSysParams','erp_base'),ParamName='MachineFault_FlowType').order_by('pk'))
        p['flowtype']=None if not settings else raw(settings[-1],'ParamValue')
        if p['flowtype'] is None or p['flowtype'].rstrip(' ')=='' :p['flowtype']='0'
    for sql in spec.get('assignments',[]):
        from .source_phase4_sql import query as fixed_query
        assigned=fixed_query(sql,p,temps,query)
        if assigned:p.update(assigned[-1])
    if name=='SP_DPWorkQty':statements=[statements[0 if p['shiftid'] in ['04003','04004'] else 1]]
    for sql in statements:
        from .source_phase4_sql import query as fixed_query
        result_sets.append({'title':str(len(result_sets)+1),'rows':fixed_query(sql,p,temps,query)})
    result={'report':name,'rows':result_sets[0]['rows'],'result_sets':result_sets[1:]}
    if spec.get('difference'):result['notes']=[spec['difference']]
    if name=='Sp_JobSheetNum':
        from .source_phase4_report_details import business_card_numbers
        result=business_card_numbers(result,p)
    if name in ['Sp_OLD_QueryWagesStatisticsInfo1','Sp_OLD_QueryWagesStatisticsInfo2','Sp_QueryWagesStatisticsInfo']:
        from .source_phase4_wages import decorate
        result=decorate(name,result,p,temps,query)
    if name=='sp_APP_GetSingleMachineFaultInfo':
        for item in result['rows']:item['handleidea']=item['handleidea'] or p['fixremarks'] or ''
        contacts=[];head=result['rows'][-1] if result['rows'] else None
        if head is not None:
            for kind,field,value in [(0,'empid',head['empid']),(1,'name',head['applyman']),(2,'empid',head['handlerids']),(3,'name',p['feedbackman'])]:
                text='SELECT '+('DISTINCT ' if kind==1 else 'TOP 1 ' if kind==3 else '')+str(kind)+' AS empKind,Name,Mobile AS phone FROM dye.h_Employee WHERE '+field+' IN ('+','.join(exp.convert(s).sql(dialect='tsql') for s in (value or '').split(';'))+')'
                contacts.extend(execute(text,query))
        result['result_sets'].insert(0,{'title':'联系人','rows':contacts})
    if name=='sp_App_QueryMachineCareRecordList':
        for item in result['rows']:
            for field in ['machineid','machinename','machinelocation']:item[field]=item[field] or ''
    if spec['kind'] in ['paged','machine_choices']:
        size=p['size'] if p['size'] is not None and p['size']>=1 else 10;current=p['current'];items=result['rows']
        result['rows']=sorted((r for r in items if r['rowindex']>(current-1)*size),key=lambda r:r['rowindex'])[:size]
        result['pagination']={'current':current,'size':size,'pages':ceil(len(items)/size),'total':len(items)}
        if name=='sp_App_S_QueryJobSheetReceiveList':
            from decimal import Decimal,ROUND_HALF_UP
            sums={k:sum((r[k] or 0 for r in items),Decimal(0)).quantize(Decimal(d),rounding=ROUND_HALF_UP) for k,d in [('rolls','.1'),('weightqty','.01'),('lengthqty','.01')]}
            result['pagination']['TotalInfo']=f"汇总：{len(items)}缸|{sums['rolls']}匹|{sums['weightqty']}kg|{sums['lengthqty']}m"
        if spec['kind']=='machine_choices':result['pagination'].update(MachineTotal=None,RepairTotal=None,MaintainTotal=None)
    return result
