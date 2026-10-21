"""交付原查询与装缸/络筒统计。全部连接、负数及重复源行参与计算。"""
import json
from pathlib import Path
from datetime import timedelta
from math import ceil
from collections import defaultdict
from uuid import uuid4
from sqlglot import exp
from django.utils import timezone
from django.core.exceptions import ValidationError
from .source_quality_reports import rows,total,key
from .source_phase4_sql import query as fixed
from .source_static_lookup import execute
from .source_foundation_view_reports import statement
from .source_phase2_reports import date
from .source_foundation_app_reports import shift_month

QUERIES=json.loads(Path(__file__).with_name('source_phase5_queries.json').read_text(encoding='utf8'))


def loading(name,p,temps,reader):
    p={**p,'starttime':date(p['newstime']),'endtime':date(p['newetime'])}
    if name=='Sp_QueryYarnLoading':
        from .source_phase4_functions import calculate
        candidates=fixed("SELECT DISTINCT JobSheetNo,ProcessID FROM dye.A_PTGX WHERE StationID='03' AND RQDate>=@starttime AND RQDate<@endtime",p,reader=reader)
        prices=[]
        for r in candidates:
            value=calculate('fn_ProcessIDPrice',{'jobsheetno':r['jobsheetno'],'processid':r['processid'],'kind':1},reader)['rows'][0]['result']
            prices.append('SELECT '+','.join('CAST('+exp.convert(v).sql(dialect='tsql')+' AS '+t+') AS '+f for v,t,f in [(r['jobsheetno'],'VARCHAR(50)','JobSheetNo'),(r['processid'],'VARCHAR(50)','ProcessID'),(value,'FLOAT','Price')]))
        temps['p5_prices']=' UNION ALL '.join(prices) if prices else 'SELECT CAST(NULL AS VARCHAR(50)) JobSheetNo,CAST(NULL AS VARCHAR(50)) ProcessID,CAST(NULL AS FLOAT) Price WHERE 1=0'
        temps['t_worksumnew']=temps['t_worksumnew'].replace('[dye].[fn_ProcessIDPrice](A.JobSheetNo,A.ProcessID,1)','(SELECT Price FROM #p5_prices P5 WHERE P5.JobSheetNo=A.JobSheetNo AND P5.ProcessID=A.ProcessID)')
    data=fixed('SELECT * FROM #T_WorkSumNew',p,temps,reader)
    from .source_foundation_utilities import employee_columns
    header=employee_columns([{k:r[k.lower()] for k in (['Kind','EmpID','Years','ShiftID'] if name=='Sp_QueryDyeLoading' else ['EmpID','Years','ShiftID'])} for r in data],
        'Sp_DyeRowDenormaliser' if name=='Sp_QueryDyeLoading' else 'Sp_WagesRowDenormaliser')
    dimensions=['kind','empid'] if name=='Sp_QueryDyeLoading' else ['empid']
    identities=sorted({tuple(key(r[k]) for k in dimensions) for r in data},key=lambda t:tuple((v is not None,v or '') for v in t))
    columns={identity:'emp'+str(i).zfill(2) for i,identity in enumerate(identities,1)}
    mapping=[{'column':column,**dict(zip(dimensions,identity))} for identity,column in columns.items()]
    groups={};base_columns=30 if name=='Sp_QueryDyeLoading' else 20
    for r in data:
        groupkey=tuple(r[k] for k in (['years','shiftid','rq','jobsheetno'] if name=='Sp_QueryDyeLoading' else ['years','shiftid','rq']))
        g=groups.setdefault(groupkey,{k:r[k] for k in (['years','shiftid','rq','jobsheetno'] if name=='Sp_QueryDyeLoading' else ['years','shiftid','rq'])})
        column=columns[tuple(key(r[k]) for k in dimensions)];measure='sk_qty' if name=='Sp_QueryDyeLoading' else 'sum_a'
        g.setdefault('_values',defaultdict(list))[column].append(r[measure])
    for g in groups.values():
        values=g.pop('_values');g.update({'emp'+str(i).zfill(2):None for i in range(1,base_columns+1)})
        g.update({c:total(v) for c,v in values.items()})
    output=[]
    if name=='Sp_QueryDyeLoading':
        heads=fixed('SELECT * FROM #T_B',p,temps,reader)
        empty_head={k:None for k in ['colorid','colornum','laodu','pinzhong','daihao','prodid','rolls','weightqty','gushechishu','jiashechishu','indate','outdate','shiftid','colormatching','gangxing']}
        for g in groups.values():
            selected=[r for r in heads if key(r['jobsheetno'])==key(g['jobsheetno']) and r['jobsheetno'] is not None]
            for head in selected or [empty_head]:output.append({**head,**g,'id':str(uuid4()),'rq':'00','register_shiftid':head['shiftid']})
        output.sort(key=lambda r:(r.get('outdate') is not None,r.get('outdate')))
    else:
        measures=['c01_q','c02_q','c03_q','c01_a','c02_a','c03_a','t_q','t_a','sum_a']
        start,end=p['starttime'],p['endtime']
        if start is not None and end is not None:
            for i in range((end.date()-start.date()).days+1):
                rq=(start+timedelta(days=i)).strftime('%Y-%m-%d');day=[r for r in data if r['rq']==rq]
                aggregates={f:total(r[f] for r in day) for f in measures}
                selected=[g for g in groups.values() if g['rq']==rq]
                output.extend({**aggregates,**g} for g in selected or [{'rq':rq,'years':None,'shiftid':None,**{'emp'+str(j).zfill(2):None for j in range(1,21)}}])
    return {'report':name,'rows':output,'result_sets':[{'title':'原人员表头及扩展列','rows':header['rows']},
        {'title':'计算明细（全部员工）','rows':data},{'title':'数量列与人员对应','rows':mapping}],
        'notes':header['notes']+['原20/30列以外人员另扩展列，原明细全部保留。装缸原ShiftID入参未使用，络筒原过程主动清空ShiftID；计件金额仅作业务统计，不生成财务数据。']}


def report(name,p,reader=rows,now=None):
    if name=='SP_ProdOutCheck':return {'report':name,'rows':[{'IsPass':True,'Msg':''}],'notes':['原过程最终无条件设置通过；没有启用财务额度拦截。']}
    spec=QUERIES[name];p={**p};temps=dict(spec.get('temps',{}));now=(timezone.localtime() if now is None else now).replace(tzinfo=None)
    if spec['kind']=='view':return {'report':name,'rows':execute(statement(name,p.get('filters',[])),reader)}
    if spec['kind']=='loading':return loading(name,p,temps,reader)
    statements=spec['sql'];notes=[]
    if name=='SP_APP_QueryClothGetMoney':
        month=now.replace(day=1,hour=0,minute=0,second=0,microsecond=0)
        p.update(dtstart=date(p['startdate']) or month,dtend=date(p['enddate']) or shift_month(month,1)-timedelta(days=1))
    elif name=='Sp_App_QueryDriverLoading':
        day=now.replace(hour=0,minute=0,second=0,microsecond=0);p.update(dtstart=day,dtend=day+timedelta(days=1))
    elif name=='Sp_AppQueryProdOut':
        start=date(p['startdate']) or now.replace(hour=0,minute=0,second=0,microsecond=0)-timedelta(days=1)
        # 原非空endDate分支漏赋值使整个查询无结果；合理修复为采用用户实际截止时间。
        end=date(p['enddate']) or start.replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(days=1)
        p.update(dtstart=start,dtend=end)
        if str(p['searchmode']) not in ['1','2']:return {'report':name,'rows':[],'notes':['原searchMode仅1和2有结果集。']}
        statements=[statements[int(p['searchmode'])-1]]
        notes.append('原非空截止日期漏赋值，按输入日期补齐；模式1为已审核装车，模式2为全部送货。')
    elif name=='Sp_ProdOut_Query':p.update(dsdate=(now-timedelta(days=7)).date().isoformat(),dtdate=now.date().isoformat())
    sets=[{'title':str(i),'rows':fixed(sql,p,temps,reader)} for i,sql in enumerate(statements,1)]
    result={'report':name,'rows':sets[0]['rows'],'result_sets':sets[1:],'notes':notes}
    if spec['kind'] in ['paged','all_paged']:
        values=result['rows'];size=p['size'];current=p['current']
        if size<1:raise ValidationError({'size':'每页条数必须大于0，请按实际查询要求填写。'})
        result['pagination']={'current':current,'size':size,'pages':ceil(len(values)/size),'total':len(values)}
        if spec['kind']=='paged':result['rows']=sorted((r for r in values if r['rowindex']>(current-1)*size),key=lambda r:r['rowindex'])[:size]
        else:notes.append('原明细查询不分页，仍返回全部行。')
        for f in ['rolls','weightqty']:
            if name=='Sp_AppQueryProdOut' or name=='Sp_App_QueryDriverLoading' and f=='rolls':result['pagination']['sum'+f]=total(r[f] for r in values)
    return result
