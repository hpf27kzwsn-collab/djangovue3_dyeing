"""三版计件日报保留人员明细，并返回原20列日历交叉表。"""
from datetime import timedelta
from .source_phase2_reports import date
from .source_foundation_app_reports import shift_month
from .source_phase4_sql import query as sql_query


def decorate(name,result,p,temps,reader):
    data=result['rows'];employees=sorted(set(r['empid'] for r in data if r['empid'] is not None))
    indices={e:'emp'+('000'+str(i+1))[-2:] for i,e in enumerate(employees)}
    from .source_foundation_utilities import employee_columns
    header=employee_columns([{'EmpID':r['empid'],'Years':r['years'],'ShiftID':r['shiftid']} for r in data],'Sp_WagesRowDenormaliser')
    shared=['years','rqday','shiftid','shifamount','shifscamount','supplements','shifsystemamount','subtotal','sumnum']
    if name!='Sp_OLD_QueryWagesStatisticsInfo1':shared.insert(6,'shifotheramount')
    groups={};pivot_rows=data;daily_columns=[]
    if name=='Sp_OLD_QueryWagesStatisticsInfo1':
        # 原第一版按日期及班组金额重新编号，同一员工跨日不固定列。
        grouped={}
        for r in data:
            key=(r['empid'],r['rq'],*(r[f] for f in shared),r['empidsubtotal'])
            if key not in grouped:grouped[key]={**r,'empidsubtotal':0}
            grouped[key]['empidsubtotal']+=r['empidsubtotal'] or 0
        pivot_rows=sorted(grouped.values(),key=lambda r:(r['empid'] is not None,r['empid'] or ''))
        sequence={}
        for r in pivot_rows:
            partition=(r['rqday'],r['shifamount']);sequence[partition]=sequence.get(partition,0)+1
            r['pivot_column']='emp'+('000'+str(sequence[partition]))[-2:]
            daily_columns.append({'rq':r['rq'],'shifamount':r['shifamount'],'column':r['pivot_column'],'empid':r['empid']})
    for r in pivot_rows:
        key=(r['rq'],*(r[f] for f in shared));group=groups.setdefault(key,{'rq':r['rq'],**{f:r[f] for f in shared},**{'emp'+str(i).zfill(2):None for i in range(1,21)}})
        col=r['pivot_column'] if name=='Sp_OLD_QueryWagesStatisticsInfo1' else indices.get(r['empid'])
        if col in group:group[col]=(group[col] or 0)+(r['empidsubtotal'] or 0)
    start=date(p['newstime']);calendar=[]
    if start is not None:
        day=start.replace(day=1);end=shift_month(day,1)
        while day<end:
            rq=day.strftime('%Y-%m-%d');selected=[r for r in groups.values() if r['rq']==rq]
            calendar.extend(selected or [{'rq':rq,'years':day.strftime('%Y-%m'),'rqday':day.strftime('%d'),'shiftid':p['shiftid'],**{f:None for f in shared if f not in ['years','rqday','shiftid']},**{'emp'+str(i).zfill(2):None for i in range(1,21)}}]);day+=timedelta(days=1)
    work=sql_query('SELECT * FROM #T_Work',p,temps,reader)
    result['result_sets']=[{'title':'人员列对应','rows':header['rows']},{'title':'原20列计件日报','rows':calendar},
        *([{'title':'第一版每日列对应','rows':daily_columns}] if daily_columns else []),{'title':'报工和包装分摊明细','rows':work}]
    result['notes']=['完整人员明细均返回。原20列报表之外的人员仍保留在明细及列对应中；未实际发放工资或生成财务凭证。',*header['notes']]
    return result
