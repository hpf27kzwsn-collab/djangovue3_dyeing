"""原考勤和包装计件重算。替换的中间表保留历史；原重复员工逐行参与。"""
import json
from pathlib import Path
from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from .source_phase3_operations import source,create,retire,model
from .source_phase4_sql import query
from .source_phase2_reports import date
from .source_stock_services import raw

SPECS=json.loads(Path(__file__).with_suffix('.json').read_text(encoding='utf8'))
NAMES=list(SPECS)


def pivot(items,groups,day,value):
    dates=sorted(set(r[day] for r in items if r[day] is not None));output={}
    for row in items:
        key=tuple(row[f] for f in groups)
        target=output.setdefault(key,{**dict(zip(groups,key)),**dict.fromkeys(dates)})
        if row[day] is not None and row[value] is not None:target[row[day]]=(target[row[day]] or 0)+row[value]
    return list(output.values())


@transaction.atomic
def perform(name,p,actor,now=None):
    spec=SPECS[name];p={**p};now=timezone.localtime() if now is None else now
    start=date(p['dtdate']);end=start if name=='sp_Static_Emp' else date(p['eddate'])
    if name in ['sp_EmpID_CHECK_Query','sp_DPWorkQty_Query']:end-=timedelta(hours=9)
    last=min(end.date(),now.date());begin=start.date();month=begin.strftime('%Y-%m');p.update(ddays=month,dtnew=begin.isoformat())
    retained=[]
    for table in ['EmpShiftClock','KQ']:retained.extend(retire(source(table),actor,name+'原全表重建，被替换记录完整留档'))
    clause="(ISNULL(EmpID,'')<>'' AND ISNULL(IsOut,0)=0"+(' AND ISNULL(IsNotKQ,0)=0' if name=='sp_EmpID_CHECKINOUT' else '')+')'
    if name!='sp_Static_Emp':clause+=' AND (DeptID=@deptids OR DeptID IS NOT NULL) AND (EmpID=@empids OR EmpID IS NOT NULL)'
    employees=query('SELECT EmpID,DeptID FROM dye.h_Employee WHERE '+clause+' OR OutDate>=@dtnew',p)
    # 原fn_GetDays含起始日且在结束早于开始时为空，不按员工编码去重。
    for employee in employees:
        for offset in range(min(2048,(last-begin).days+1)):
            create('EmpShiftClock',{'EmpID':employee['empid'],'DeptID':employee['deptid'],'dtDate':begin+timedelta(days=offset),'BeginTime':None,'EndTime':None,'IsHoliday':None,'ShiftName':month,'CopyClassID':None},actor)
    filters=[]
    if p['empids']:filters.append('EmpID=@empids')
    if p['deptids']:filters.append('DeptID=@deptids')
    where=' WHERE '+' AND '.join(filters) if filters else ''
    if name=='sp_DPWorkQty_Query':
        for insert in spec['inserts']:
            table=insert['table'];retained.extend(retire(source(table),actor,name+'原计件中间表替换留档'))
            rows=query(insert['sql'],p);fields={k.lower():k for k in model(table).SOURCE_FIELDS}
            for r in rows:create(table,{fields[k]:v for k,v in r.items()},actor)
        data=query('SELECT * FROM dye.DP_WorkQty'+where+' ORDER BY YEARS,DeptID,ShiftID,EmpID',p)
        result=pivot(data,['years','shiftid','deptid','empid','summoney'],'tday','workmoney')
    else:
        temps=spec['temps'];data=query(spec['calculation'],p,temps)
        if spec['target']:
            table=spec['target'];retained.extend(retire(source(table),actor,name+'原考勤结果替换留档'));fields={k.lower():k for k in model(table).SOURCE_FIELDS}
            for row in data:
                values={fields[k]:v for k,v in row.items()}
                values['dtDate']=values['dtDate'].isoformat() if hasattr(values['dtDate'],'isoformat') else values['dtDate']
                create(table,values,actor)
            data=query('SELECT * FROM dye.'+table+where+' ORDER BY EmpID,dtDate',p)
            result=pivot(data,['shiftname','deptid','empid'],'days','workcount') if name=='sp_EmpID_CHECK_Query' else data
        elif name=='sp_Static_Emp':result=query(spec['outputs'][0],p,temps)
        else:
            index=2 if p['deptids'] and p['empids'] else 1 if p['deptids'] else 3 if p['empids'] else 0
            result=query(spec['outputs'][index],p,temps)
    return {'report':name,'rows':result,'result_sets':[{'title':'原重算逐行结果','rows':data}],'retained':retained,
        'notes':['只重算新系统当前来源数据。旧SQL Server没有执行过程；被原DELETE替换的中间表记录仍可在留档中追溯。']}
