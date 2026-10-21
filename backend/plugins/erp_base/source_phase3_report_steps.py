"""原固定报表的临时查询和标量赋值，不写入历史业务表。"""
from datetime import timedelta
from sqlglot import parse_one
from .source_phase2_reports import temporary_views
from .source_phase3_sql import bind
from .source_foundation_app_reports import shift_month
from .source_static_lookup import execute


def run(name,spec,parameters,query,now):
    p={**spec.get('variables',{}),**parameters}
    day=(p['ymdate'] or now).replace(hour=0,minute=0,second=0,microsecond=0)
    month=day.replace(day=1)
    p.update(daystartdate=day,dayenddate=day+timedelta(days=1,milliseconds=-3),monthstartdate=month,
        monthenddate=day+timedelta(days=1,milliseconds=-3),lastmonthstartdate=shift_month(month,-1),lastmonthenddate=month-timedelta(milliseconds=3))
    if name=='Sp_WLXHHZDetail':p['monthenddate']=shift_month(month,1)-timedelta(milliseconds=3)
    if name=='Sp_ProductionReports1':p['monthenddate']=shift_month(month,1)-timedelta(milliseconds=3)
    if name in ['Sp_ProductionReports2','Sp_ProductionReports5']:
        for field in ['daystartdate','dayenddate','monthstartdate','monthenddate','lastmonthstartdate','lastmonthenddate']:p[field]+=timedelta(minutes=450)
    if name=='Sp_PDGroup':
        p['dsdate']=None if p['startdate'] is None else p['startdate'].date().isoformat()
        p['dtdate']=None if p['enddate'] is None else p['enddate'].date().isoformat()
    def evaluate(sql):
        tree=temporary_views(parse_one(sql,read='tsql'),spec['temps'])
        return execute(bind(tree.sql(dialect='tsql'),p),query)
    for step in spec['steps']:
        values=evaluate(step['sql'])
        if values:
            for i,variable in enumerate(step['variables']):p[variable]=values[-1]['v'+str(i)]
    outputs=[{'title':name+' / '+str(i+1),'rows':evaluate(sql)} for i,sql in enumerate(spec['outputs'])]
    return {'report':name,'rows':outputs[0]['rows'],'result_sets':outputs[1:]}
