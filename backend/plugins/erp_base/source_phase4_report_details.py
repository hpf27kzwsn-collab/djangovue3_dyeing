"""第四阶段多结果集与日历骨架；固定业务查询，不接受客户端SQL片段。"""
from datetime import timedelta
from decimal import Decimal
from math import ceil
from random import randint
from sqlglot import exp,parse_one
from .source_phase4_sql import query as sql_query
from .source_phase2_reports import date
from .source_foundation_app_reports import shift_month
from .source_business_updates import matching
from .source_stock_services import raw
from .source_trial_steps import equal


def business_card_numbers(result,p):
    from uuid import uuid4
    from decimal import ROUND_HALF_UP
    start=date(p['startdate']);end=date(p['enddate']);months=[]
    if start is not None and end is not None:
        months=list(dict.fromkeys((start+timedelta(days=i)).strftime('%Y-%m') for i in range(min(2048,(end.date()-start.date()).days))))
    sets=[result['rows'],*(s['rows'] for s in result['result_sets'])];output=[]
    for month in months:
        row={'id':str(uuid4()),'rq':month}
        for i,data in enumerate(sets,1):
            for col,field in [('qty','sumassignedweightqty'),('lengthqty','sumassignedlengthqty')]:
                values=[r[field] for r in data if r['rq']==month and r[field] is not None]
                row[f't{i}{col}']=Decimal(str(sum(values))).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
        row['tqty']=row['t1qty']+row['t2qty']
        row.update(dict.fromkeys(['f1qty','f1lengthqty','f2qty','f2lengthqty','fqty','trate','frate']))
        output.append(row)
    return {'report':result['report'],'rows':output,'result_sets':[{'title':'01/02/03原分类来源'+str(i+1),'rows':data} for i,data in enumerate(sets)],
        'notes':['三类工卡数量与原月骨架已计算；应收F1/F2及财务比率暂缓，其列为NULL，不以0表示已核算。原错误重复列名T3LengthQty明确区分为F2LengthQty。']}


def values_sql(fields,values):
    """带原类型的临时关系；UNION ALL保留重复，空集仍保留列类型。"""
    def one(value):
        return 'SELECT '+','.join('CAST('+exp.convert(value.get(k)).sql(dialect='tsql')+' AS '+t+') AS ['+k+']' for k,t in fields.items())
    return ' UNION ALL '.join(one(r) for r in values) if values else one({})+' WHERE 1=0'


def run(sql,p,temps,reader):return sql_query(sql,p,temps,reader)


def prepare(name,p,temps,statements,query,now):
    if name in ['sp_App_S_QueryJobCardSpeedList','sp_App_S_QueryJobSheetReceiveList']:
        p['dtend']=date(p['enddate']) or now+timedelta(days=1)
        p['dtstart']=date(p['startdate']) or shift_month(p['dtend'],-12)
        if p['current'] is None or p['current']<1:p['current']=1
        if p['size'] is None or p['size']<1:p['size']=10
    if name=='sp_App_QueryMachinePlanList':
        p['ischecked1']='1' if not p['handlerids'] else '2'
        if p['delivery'] not in [0,1]:statements=['SELECT 1 AS OriginalNoResult WHERE 1=0']
    if name=='Sp_JobSheetNum':
        # 业务三个分类原聚合全部返回，应收F1/F2和财务比率按用户本轮范围延后。
        pass
    if name=='20260731':
        from .source_phase2_reports import temporary_views
        for key in ['t6','t7']:
            tree=parse_one(temps[key],read='tsql');with_=tree.args.get('with_')
            definitions={c.alias_or_name.lower():c.this.sql(dialect='tsql') for c in with_.expressions}
            tree.set('with_',None);temps[key]=temporary_views(tree,definitions).sql(dialect='tsql')
        start=date(p['startdate']);end=date(p['enddate'])
        days=[]
        if start is not None:
            day=start.replace(hour=0,minute=0,second=0,microsecond=0);days=[{'rq':day.strftime('%Y-%m-%d')}]
            while end is not None and day.date()<end.date():day+=timedelta(days=1);days.append({'rq':day.strftime('%Y-%m-%d')})
        temps['t0']=values_sql({'rq':'VARCHAR(10)'},days)
        month=None if start is None else start.replace(day=1,hour=0,minute=0,second=0,microsecond=0)
        p.update(lastmonthstart=None if month is None else shift_month(month,-1),lastmonthend=None if month is None else month-timedelta(milliseconds=3),lastmonthdays=None if month is None else (month-timedelta(days=1)).day,
            lastyear=None if start is None else shift_month(start,-12)) # 原DATEADD(YEAR,-1.5)截去小数，实际减一年。
    if name in ['Sp_OLD_QueryWagesStatisticsInfo1','Sp_OLD_QueryWagesStatisticsInfo2','Sp_QueryWagesStatisticsInfo','Sp_WorkQtySum']:
        from .source_phase4_functions import calculate
        t=date(p['newstime']);p['nn']=Decimal('8.5') if t is not None and t.strftime('%H:%M:%S')=='08:30:00' else Decimal('7.5')
        tree=parse_one(temps['t_wp'],read='tsql')
        tree.set('expressions',[x for x in tree.selects if x.alias_or_name.lower()!='processidpire'])
        data=run(tree.sql(dialect='tsql'),p,temps,query)
        for r in data:r['processidpire']=calculate('fn_ProcessIDPire',{'jobsheetno':r['jobsheetno'],'processid':r['processid'],'num':r['rsqty'] if name=='Sp_QueryWagesStatisticsInfo' else r['qty']},query)['rows'][0]['result']
        fields={k:'VARCHAR(100)' for k in ['wprocessno','jobsheetno','processid','stationid','shiftid','empid','colorid','colornum','customerid']}
        fields.update({k:'FLOAT' for k in ['currkg','currmeter','qty','currdosage','processidpire']});fields['createdate']='DATETIME'
        if name=='Sp_QueryWagesStatisticsInfo':fields['rsqty']='FLOAT'
        if name=='Sp_WorkQtySum':fields.update(kgqty='FLOAT',meterqty='FLOAT')
        temps['t_wp']=values_sql(fields,data)
    return statements


def special(name,p,temps,statements,reader,now):
    def q(sql):return run(sql,p,temps,reader)
    def output(sets,**extra):return {'report':name,'rows':sets[0] if sets else [],'result_sets':[{'title':str(i+2),'rows':v} for i,v in enumerate(sets[1:])],**extra}
    if name in ['sp_App_GetInspectionLogBySheetSeries','sp_App_GetMachineCareRecordsBySheetSeries']:
        from .source_equipment_projects import record_projects
        from .source_phase3_operations import model
        inspection=name=='sp_App_GetInspectionLogBySheetSeries';table='InspectionLog' if inspection else 'MachineCareRecords';module='erp_quality' if inspection else 'erp_production'
        heads=list(matching(reader(table,module),SheetSeries=p['sheetseries']).order_by('pk'))
        item=heads[-1] if heads else model(table)(old_sheet_series=p['sheetseries'])
        projects=record_projects(item,reader);p['isusemachinecase']=projects['summary']['IsUseMachineCase']
        return output([q(statements[0]),projects['rows']],notes=projects['notes'])
    if name=='QueryJobSheetNoIsClosed':
        # 接口用逗号列表代替原动态SQL IN表达式，保留带引号的旧输入。
        numbers=[s.strip().strip("'").replace("''", "'") for s in (p['jobsheetno'] or '').split(',')]
        found=reader('JobSheet','erp_production').filter(old_sheet_no__in=numbers,old_sheet_status__in=[9,10]).exists()
        return output([[{'cmdok':99 if found else 0,'messge':'缸号状态存在已终止，请刷新数据后重试！' if found else ''}]])
    if name=='sp_APP_GetMachineFaultFlowStatusRecord':
        heads=q('SELECT TOP 1 SheetSeries FROM dye.MachineFault WHERE SheetSeries=@sheetseries OR SheetNo=@sheetseries')
        if heads:p['sheetseries']=heads[0]['sheetseries'] or p['sheetseries']
        records=q('SELECT * FROM #t');contacts=[]
        for record in records:
            if not equal(record['action'],'指派'):continue
            for code in [] if record['handlerids'] is None else record['handlerids'].split(';'):
                people=list(matching(reader('HEmployee','erp_base'),EmpID=code).order_by('pk'))
                contacts.extend({'recordid':record['recordid'],'name':None if h is None else raw(h,'Name'),'mobile':None if h is None else raw(h,'Mobile')} for h in people or [None])
        return output([records,sorted(contacts,key=lambda r:r['recordid'] or '')])
    if name=='sp_App_MachineArticleGroupSum':
        fields=[s.strip() for s in (p['groupfields'] or '').split(',') if s.strip()]
        from .source_static_lookup import compile_query
        available=compile_query('SELECT * FROM dye.v_App_ArticleOutDetail')[2]
        for f in fields:
            if f.lower().removeprefix('d.') not in available:raise KeyError(f)
        fields=['d.['+f.removeprefix('d.')+']' for f in fields]
        return output([q('SELECT '+(' ,'.join(fields)+',' if fields else '')+'CONVERT(DECIMAL(12,2),SUM(d.OutQty)) AS Qty,CONVERT(DECIMAL(12,2),SUM(d.Total)) AS Total FROM dye.v_App_ArticleOutDetail d LEFT JOIN dye.v_App_ArticleOut m ON m.SheetSeries=d.SheetSeries WHERE d.MachineID=@machineid AND m.SheetDate>=@starttime AND m.SheetDate<=@endtime'+(' GROUP BY '+','.join(fields) if fields else ''))])
    if name=='sp_app_QueryEmployees_ForMachineFault':
        from .source_foundation_view_reports import statement
        sql=statement('sp_app_QueryEmployees',p.get('filters',[]));temps['employees']=sql
        return output([q('SELECT * FROM #employees WHERE ISNULL(MFLevel,0)>0 AND ISNULL(IsOut,0)=0 ORDER BY EmpID')])
    if name=='Sp_GetSZRollNoByPackMachine':
        from .source_phase4_reports import setting
        value=''
        if equal(setting('SZPackMachine',reader),p['machineid']):
            heads=q('SELECT a.ColorNum,b.SheetNo,CASE WHEN a.AssignUnit IN (0,2) THEN 1 ELSE 2 END AS kind FROM dye.JobSheet a LEFT JOIN dye.OrderMain b ON b.SheetNo=a.OrderSheetNo WHERE a.SheetNo=@jobsheetno')
            if heads and heads[-1]['kind']==1:
                p.update(color=heads[-1]['colornum'],order=heads[-1]['sheetno'])
                value=q("SELECT ISNULL(MAX(RollNo),'0') AS value FROM dye.RecordYield WHERE OrderSheetNo=@order AND ColorNum=@color")[0]['value']
        return output([[{'maxrollno':value}]])
    if name=='SP_GetXMInfoToXML':
        heads=q('SELECT XMLFolder FROM dye.p_Customer WHERE ShortName=@customerid');folder=None if not heads else heads[-1]['xmlfolder']
        if folder is None or folder.rstrip(' ')=='' :return output([[]])
        suffix=('0000'+p['rollno'])[-4:] if p['rollno'] else ('00000000'+str(randint(1,100000000)))[-8:]
        p['xmlfilename']=folder+('' if folder.endswith('\\') else '\\')+now.strftime('%Y%m%d%H%M%S')+suffix+'.xml'
        return output([q("SELECT TOP 100 @xmlfilename AS XMLFileName,'Barcode' AS TableName,'029' AS TemplateNumber,'抬头' AS BarcodeTitle,CustomerGrayName AS ProductName,CONVERT(VARCHAR(100),ISNULL(a.CustColorNum,''))+CONVERT(VARCHAR(100),ISNULL(a.ColorID,'')) AS ColorCode,a.ColorNum AS ColorNumber,a.JobSheetNo AS BatchNO,CustQty AS Quantity,'公斤' AS ProductUnit,RollNo AS VolumeNumber,a.Width AS Breadth,a.Weight AS Grammage,'' AS Composition,PackTime AS DateMark,a.CustSelfNo AS OrderNumber,'' AS FirstRemark,CONVERT(VARCHAR(100),a.Width)+CONVERT(VARCHAR(100),a.Weight) AS Remark FROM dye.RecordYield a LEFT JOIN dye.JobSheet b ON a.JobSheetNo=b.SheetNo WHERE a.JobSheetNo=@jobsheetno AND a.RollNo=@rollno")],notes=['原过程仅返回XML路径及标签字段，不写文件、不确认标签打印成功。'])
    if name=='sp_App_QueryFigMachinePlanByPage':
        data=q('SELECT MachineID,Name AS MachineName,MachineNo FROM dye.p_Machine ORDER BY MachineNo')
        labels=['运行','停机','待机运行','待机停机','离线'];colors=['#00ff00','#ff0000','#66d7ff','#ff00ff','#ffff66'];counts=[0]*5
        for r in data:
            kind=randint(0,4);minutes=randint(0,2499);counts[kind]+=1
            elapsed=f'{minutes//1440}天{minutes//60%24}时' if minutes>1440 else f'{minutes//60}时{minutes%60}分'
            r.update(istatus=kind,machinestatus=labels[kind],statuscolor=colors[kind],runtime=now-timedelta(minutes=minutes),runtimeshow='运行'+elapsed)
        return output([[dict(zip(['run','stop','standby','shutdown','offline'],counts))],data],simulation=True,notes=['原过程用随机数生成状态和运行时间，属于演示看板；未连接真实设备。'])
    if name=='sp_App_QueryMachineArticleUseTotal':
        p['machineid']=p['machineid'] or '全部';p.update(q('SELECT SUM(OutQty) AS sumcount FROM #source')[0])
        return output([q(statements[2*i] if p['totalmode'] in [0,i+1] else statements[2*i+1]) for i in range(8)])
    if name=='sp_App_QueryMachineArticleUseList':
        p.update(startdate=shift_month(now,-3),enddate=now)
        temps['t']=statements[0]
        # 原XML PATH聚合保留转义和重复行，分组只用日期+员工，跨单据同日会重复展现。
        from html import escape
        summary=q(statements[1]);details=q('SELECT * FROM #s');groups={}
        for r in details:groups.setdefault((r['sheetdate'],r['name'],r['sheetseries'],r['sheetno']),[]).append(r)
        result=[]
        for (dt,emp,series,number),items in groups.items():
            texts=[r['detailinfo'] for r in details if dt is not None and emp is not None and r['sheetdate']==dt and r['name']==emp and r['detailinfo'] is not None]
            totals=[r['total'] for r in items if r['total'] is not None]
            result.append({'sheetdate':None if dt is None else dt.strftime('%Y-%m-%d %H:%M'),'name':emp,'sheetseries':series,'sheetno':number,'details':'\n'.join(escape(t,quote=False) for t in texts) if texts else None,'totolmoney':sum(totals) if totals else None})
        return output([summary,sorted(result,key=lambda r:r['sheetdate'] or '',reverse=True)])
    if name=='sp_App_QueryOutputSumChart':
        count=p['datecount'];count=15 if count is None or count<=0 else count
        end=date(p['enddate']) or now.replace(hour=0,minute=0,second=0,microsecond=0);start=end-timedelta(days=count)
        p.update(dtstart=start,dtend=end,postid=None)
        posts=q("SELECT Code FROM dye.p_FieldValid WHERE FieldType='Station' AND Name=@postname")
        if posts:p['postid']=posts[-1]['code']
        temps['dtlist']=values_sql({'dtname':'VARCHAR(50)'},[{'dtname':(start+timedelta(days=i)).strftime('%Y-%m-%d')} for i in range(count)])
        p.update(dict(zip(['linename','linecolor','fieldname'],{1:('疋数','#ff9933','SumRolls'),2:('重量','#ff0000','SumKg'),3:('长度','#3333ff','sumLength')}.get(p['kind'],('其他','#ffffff','SumRolls')))))
        return output([q(statements[-2]),q(statements[-1])])
    if name=='sp_App_S_QueryJobCardSpeedList':
        # 原结果集依次为分页、工卡、工序、收发含汇总、附加项目。
        base=q('SELECT * FROM #t');heads=q('SELECT * FROM #Output');steps=q('SELECT * FROM #q WHERE ISNULL(ProcessNo,0)>0')
        outbound=temps['ps'];inbound=statements[4]
        temps['ps0']=outbound;temps['psin']=inbound
        cols='JobSheetNo,SheetDate,SheetKind,Rolls,WeightQty,SheetNo,ShowSheetDate'
        temps['ps']='SELECT '+cols+' FROM #ps0 UNION ALL SELECT '+cols+' FROM #psin UNION ALL SELECT JobSheetNo,DATEADD(DAY,-1,MIN(SheetDate)),SheetKind,SUM(Rolls),SUM(WeightQty),NULL,\'汇总\' FROM (SELECT * FROM #ps0 UNION ALL SELECT * FROM #psin) s GROUP BY JobSheetNo,SheetKind'
        summary={'current':p['current'],'size':p['size'],'total':len(base),'pages':ceil(len(base)/p['size'])}
        return output([heads,steps,q('SELECT * FROM #ps ORDER BY JobSheetNo,SheetKind,SheetDate DESC'),q(statements[-1])],pagination=summary)
    if name=='sp_App_GetMachineInfo':
        return machine_info(p,reader,now)
    if name=='SP_APP_QueryFaultBillCount':
        return fault_counts(p,reader,now)
    raise KeyError(name)


def machine_info(p,reader,now):
    """旧列Staus等已无，按最新设备、故障及组织字典明确连接。"""
    sql="""SELECT m.*,m.UnitStr AS UnitName,b.Name AS BusinessName,CAST(NULL AS VARCHAR(100)) AS EmpName,
      CASE WHEN EXISTS(SELECT 1 FROM dye.v_APP_MachineFault f WHERE f.MachineID=m.MachineID AND ISNULL(f.CompleteStatus,'')<>'已关闭') THEN '维修' ELSE '正常' END AS Staus,
      CASE WHEN EXISTS(SELECT 1 FROM dye.MachineCarePlan a JOIN dye.MachineCarePlanDetail d ON a.SheetSeries=d.SheetSeries WHERE d.MachineID=m.MachineID AND StartTime<=@now AND EndTime>=@now) THEN 1 ELSE 0 END AS Maintain
      FROM dye.p_Machine m
      LEFT JOIN dye.p_FieldValid b ON b.FieldType='BusinessUnit' AND b.Code=m.BusinessUnitID
      """
    data=run(sql,{**p,'now':now},{},reader);counts={'MachineTotal':len(data),'RepairTotal':sum(r['staus']!='正常' for r in data),'MaintainTotal':sum(r['maintain'] for r in data)}
    key=(p['confilter'] or '').split('&')[0];mode=p['searchmode']
    from .source_trial_steps import sql_like
    data=[r for r in data if (not key or any(sql_like(r.get(f),'%'+key+'%') for f in ['machineid','name','place','unitname','spec','supplier','businessname','empname'])) and (mode==0 or mode==1 and r['staus']!='正常' or mode==10 and equal(r['machineid'],key) or mode==2 and r['maintain'])]
    data.sort(key=lambda r:r['machineid'] or '',reverse=True);current=p['current'];size=20
    return {'report':'sp_App_GetMachineInfo','rows':data[(current-1)*size:current*size], 'pagination':{'current':current,'size':size,'total':len(data),'pages':ceil(len(data)/size),**counts},'notes':['旧Staus/组织名称已不在最新视图，使用当前设备、故障、保养计划和字典重建；状态规则待历史对照及现场核验。']}


def fault_counts(p,reader,now):
    start=date(p['starttime']);end=date(p['endtime']);end=None if end is None else end+timedelta(days=1,minutes=-1)
    machines=p['machinelist'] or '全部';kind=p['counttype'] or '月';width={'月':7,'日':10,'年':4,'机台':4}[kind]
    params={**p,'begin':start,'finish':end,'all':int(machines=='全部'),'machines':machines,'width':width}
    where="m.SheetDate>=@begin AND m.SheetDate<=@finish AND (@all=1 OR CHARINDEX(','+m.MachineID+',',','+@machines+',')>0)"
    key='m.MachineID' if kind=='机台' else 'SUBSTRING(CONVERT(VARCHAR(10),m.SheetDate,120),1,@width)'
    groups=run('SELECT '+key+' AS reportdate,CompleteStatus AS cs,COUNT(*) AS billcount FROM dye.v_APP_MachineFault m WHERE '+where+' GROUP BY '+key+',CompleteStatus',params,{},reader)
    # 原机台分支的配件金额仍按年份归集，不能擅自改成机台金额。
    amounts=run('SELECT SUBSTRING(CONVERT(VARCHAR(10),m.SheetDate,120),1,@width) AS reportdate,CONVERT(INT,SUM(ISNULL(b.Total,0))) AS total FROM dye.v_APP_ArticleOutDetail b LEFT JOIN dye.v_APP_ArticleOut m ON m.SheetSeries=b.SheetSeries WHERE '+where.replace('m.MachineID','b.MachineID')+' GROUP BY SUBSTRING(CONVERT(VARCHAR(10),m.SheetDate,120),1,@width)',params,{},reader)
    states=run("SELECT DISTINCT CompleteStatus FROM dye.p_MachineFaultStatus WHERE @containclosed=1 OR CompleteStatus<>'已关闭'",params,{},reader)
    dates=[]
    if kind=='机台':
        dates=list(dict.fromkeys(r['reportdate'] for r in groups)) if machines=='全部' else [r['machineid'] for r in run("SELECT MachineID FROM dye.p_Machine WHERE CHARINDEX(','+MachineID+',',','+@machines+',')>0",params,{},reader)]
    elif start is not None and end is not None:
        count=(end.year-start.year)*12+end.month-start.month+1 if kind=='月' else end.year-start.year+1 if kind=='年' else (end.date()-start.date()).days+1
        dates=[(shift_month(start,i*(12 if kind=='年' else 1)) if kind!='日' else start+timedelta(days=i)).strftime('%Y-%m-%d')[:width] for i in range(count)]
    sums={};totals={r['reportdate']:r['total'] for r in amounts}
    for r in groups:sums[r['reportdate']]=sums.get(r['reportdate'],0)+r['billcount']
    ranks={key:i+1 for i,(key,_) in enumerate(sorted(sums.items(),key=lambda x:x[1],reverse=True))};data=[];grand=[]
    for day in dates:
        for state in states:
            matching_rows=[r for r in groups if equal(r['reportdate'],day) and equal(r['cs'],state['completestatus'])];count=sum(r['billcount'] for r in matching_rows) if matching_rows else None
            grand.append((state['completestatus'],count))
            if kind=='机台' and not sums.get(day):continue
            item={'dtname':day,'sumcount':sums.get(day),'total':totals.get(day),'title1':day,'title2':f"{sums.get(day,0)}单 {totals.get(day,0)}元",'completestatus':state['completestatus'],'billcount':count or 0}
            if kind=='机台':item['rowindex']=ranks.get(day)
            data.append(item)
    summary=[]
    for state in dict.fromkeys(s for s,_ in grand):
        counts=[n for s,n in grand if equal(s,state) and n is not None];summary.append({'completestatus':state,'billcount':sum(counts) if counts else None})
    allcounts=[n for _,n in grand if n is not None];summary.append({'completestatus':'总报修','billcount':sum(allcounts) if allcounts else None})
    data.sort(key=lambda r:r['completestatus'] or '')
    if kind=='机台':data.sort(key=lambda r:(r.get('rowindex',0) or 999,r['dtname'] or ''))
    else:data.sort(key=lambda r:r['dtname'] or '',reverse=True)
    return {'report':'SP_APP_QueryFaultBillCount','rows':data,'result_sets':[{'title':'状态汇总','rows':summary}]}
