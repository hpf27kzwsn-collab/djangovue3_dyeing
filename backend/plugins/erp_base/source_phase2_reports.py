"""第二阶段原视图和APP查询；固定SQL在本地原字段及授权范围内运行。"""
import json
from pathlib import Path
from datetime import datetime, timedelta
from math import ceil
from sqlglot import exp, parse_one
from django.utils import timezone
from .source_static_lookup import execute
from .source_quality_reports import rows
from .source_business_updates import matching
from .source_stock_services import raw
from .source_foundation_app_reports import shift_month
from .source_foundation_view_reports import statement

QUERIES=json.loads(Path(__file__).with_name('source_phase2_queries.json').read_text(encoding='utf8'))


def bind(sql,parameters):
    tree=parse_one(sql,read='tsql')
    values={k.lower():v for k,v in parameters.items()}
    for parameter in list(tree.find_all(exp.Parameter)):
        value=values[parameter.name.lower()]
        if isinstance(value,datetime):
            if timezone.is_aware(value):value=timezone.localtime(value)
            value=value.replace(tzinfo=None).isoformat(' ')
        if isinstance(value,bool):value=int(value)
        parameter.replace(exp.convert(value))
    return tree.sql(dialect='tsql')


def date(value):
    if value is None or value=='':return None
    value=value if isinstance(value,datetime) else datetime.fromisoformat(value)
    return timezone.localtime(value).replace(tzinfo=None) if timezone.is_aware(value) else value


def temporary_views(tree,definitions):
    for table in list(tree.find_all(exp.Table)):
        name=table.name.lower().lstrip('#')
        if name in definitions:
            source=parse_one(definitions[name],read='tsql')
            temporary_views(source,definitions)
            table.replace(source.subquery(table.alias or name))
    for column in tree.find_all(exp.Column):
        if column.table.lower().lstrip('#') in definitions:
            column.set('table',exp.to_identifier(column.table.lstrip('#')))
            column.set('db',None)
    return tree


def report(name,parameters,query=rows,now=None):
    spec=QUERIES[name]
    if spec['kind']=='sales_limit':
        from .source_phase2_limits import report as sales_limit
        return sales_limit(query,now)
    if spec['kind']=='dyeing_daily':
        from .source_phase2_daily import report as dyeing_daily
        return dyeing_daily(parameters,query)
    if spec['kind']=='printing':
        from .source_phase2_printing import pastedetails,print_weight
        return pastedetails(parameters['sheetseries'],parameters['sheetno'],query) if name=='sp_PrintOrderToPasteDosageDetail' else print_weight(parameters['sheetno'],query)
    if spec['kind']=='view':
        return {'report':name,'rows':execute(statement(name,parameters.get('filters',[])),query)}
    p={k.lower():v for k,v in parameters.items()}
    now=(timezone.localtime() if now is None else now).replace(tzinfo=None)
    if spec['kind']=='query':
        if name=='Sp_QueryNotEndOrder':
            start=date(p['startdate']).replace(day=1,hour=0,minute=0,second=0,microsecond=0)
            p.update(thisstratdate=start,thisenddate=shift_month(start,1),prstartdate=shift_month(start,-1),prenddatetime=start)
        sql=temporary_views(parse_one(spec['sql'],read='tsql'),spec.get('temps',{})).sql(dialect='tsql')
        return {'report':name,'rows':execute(bind(sql,p),query)}
    current=int(p['current']);size=p['size']
    if name in ['Sp_AppQueryColorQuote','SP_APP_UrgentOrderInfo']:current=1 if current<1 else current
    if name!='Sp_AppQueryOrderInfo':size=10 if size is None or size<1 else size
    if name in ['Sp_AppQueryColorQuote','SP_APP_UrgentOrderInfo']:
        end=date(p['enddate']) or now+timedelta(days=1)
        p['dtend']=end;p['dtstart']=date(p['startdate']) or (shift_month(end,-12) if name=='Sp_AppQueryColorQuote' else end-timedelta(days=1))
    elif name=='Sp_AppOrderQuery':
        p['dtstart']=date(p['startdate']) or now.replace(hour=0,minute=0,second=0,microsecond=0)-timedelta(days=1)
        p['dtend']=date(p['enddate']) or p['dtstart'].replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(days=1)
    elif name=='Sp_AppQueryOrderInfo':
        start=now.replace(day=1,hour=0,minute=0,second=0,microsecond=0)
        p['startdate']=date(p['startdate']) or start
        p['enddate']=date(p['enddate']) or shift_month(start,1)-timedelta(seconds=1)
    elif name=='SP_APP_QueryOrderMain':
        p['ischecked1']='N' if not p['sheetseries'] else 'Y'
        for field,flag in [('startdate','ischecked2'),('enddate','ischecked3')]:
            value=date(p[field]);p[field]=value
            p[flag]='N' if value is None or value<=datetime(1911,11,11) else 'Y'
        p['ischecked4']='Y' if p['bisaccept'] else 'N'
        if p['empid'] not in [None,'','admin','超级管理员']:
            for employee in matching(query('HEmployee','erp_base'),EmpID=p['empid']).filter(old_is_customer=True).order_by('pk'):
                p['customerid']=raw(employee,'CustomerID')
            if p['customerid']:p['ischecked1']='Y'
    result=execute(bind(spec['sql'],p),query)
    selected=sorted((r for r in result if r['rowindex']>(current-1)*size),key=lambda r:r['rowindex'])[:size]
    pagination={'current':current,'size':size,'pages':ceil(len(result)/size),'total':len(result)}
    if name=='Sp_AppOrderQuery':pagination['SumOrderQty']=sum(r['orderqty'] or 0 for r in result) if result else None
    response={'report':name,'rows':selected,'pagination':pagination,'result_sets':[]}
    for child in spec.get('children',[]):
        scope=result if child['scope']=='all' else selected
        values=[r[child['key'].lower()] for r in scope]
        tree=parse_one(child['sql'],read='tsql')
        tree=tree.where(exp.In(this=parse_one(child['field']),expressions=[exp.convert(v) for v in values])) if values else tree.where(exp.false())
        response['result_sets'].append({'title':child['title'],'rows':execute(tree.sql(dialect='tsql'),query)})
    return response
