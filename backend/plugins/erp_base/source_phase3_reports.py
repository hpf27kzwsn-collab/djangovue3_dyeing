"""采购、外协及库存原查询；仅在本地原字段和调用者授权范围内计算。"""
import json
from pathlib import Path
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP
from math import ceil
from django.utils import timezone
from sqlglot import parse_one
from .source_static_lookup import execute
from .source_phase2_reports import date, temporary_views
from .source_phase3_sql import bind
from .source_foundation_view_reports import statement
from .source_foundation_app_reports import shift_month
from .source_quality_reports import rows
from .source_business_updates import matching
from .source_stock_services import raw
from .source_package_labels import varchar

QUERIES=json.loads(Path(__file__).with_name('source_phase3_queries.json').read_text(encoding='utf8'))
TEXT_PARAMETERS=['confilter','customerid','grayid','lotno','recesheetno','prodid','colornum','jobsheetno',
    'sheetno','sheetseries','supplierid','stuffid','prodname','empid','articleid','articlecode','articlekindid',
    'warehouseid','stuffcode','rowllno','machineid','nlotno','fathergrayid','barcode']
DATE_PARAMETERS=['startdate','enddate','dtinputdate','dtinputenddate','ymdate']


def report(name,parameters,query=rows,now=None):
    now=timezone.localtime() if now is None else now
    now=now.replace(tzinfo=None)
    p={key:'' for key in TEXT_PARAMETERS};p.update(parameters)
    p.update({f'ischecked{i}':parameters.get(f'ischecked{i}','N') for i in range(1,7)})
    for key in DATE_PARAMETERS:p[key]=date(p.get(key))
    if name in ['Sp_GrayStockToJobOut','Sp_SemiStockToJobOut']:
        from .source_phase3_scan import report as scan
        return scan('301' if name=='Sp_GrayStockToJobOut' else '373',p['barcode'],p['jobsheetno'],query)
    if name=='fn_GetEmpID':
        source=list(matching(query('RecordYield','erp_warehouse'),JobSheetNo=varchar(p['sheetno'],30)).order_by('pk')[:1])
        people=[] if not source else list(matching(query('HEmployee','erp_base'),EmpID=varchar(raw(source[0],'EmpID'),10)).order_by('pk'))
        value='' if not people else varchar(raw(people[-1],'Name'),100)
        return {'report':name,'rows':[{'result':value}]}
    if name=='QueryQC_NewRecordInfo':
        jobs=execute(bind('SELECT AssignUnit,OrderSheetNo,ColorNum FROM dye.vw_jobSheet WHERE SheetNo=@jobsheetno',p),query)
        job=None if not jobs else jobs[-1]
        if job is not None and job['assignunit'] in [0,2]:
            sql='SELECT * FROM dye.RecordYield WHERE OrderSheetNo=@ordersheetno AND ColorNum=@colornum AND RollNo=@rowllno'
            p.update(ordersheetno=job['ordersheetno'],colornum=job['colornum'])
        else:sql='SELECT * FROM dye.RecordYield WHERE JobSheetNo=@jobsheetno AND RollNo=@rowllno'
        return {'report':name,'rows':execute(bind(sql,p),query)}
    spec=QUERIES[name]
    if spec['kind']=='day_totals':
        day=(p['ymdate'] or now).replace(hour=7,minute=50,second=0,microsecond=0)
        p.update(dt0=day,dt1=day+timedelta(days=1))
        result={'rq':day.date().isoformat(),'yf':day.strftime('%Y-%m')}
        for sql in spec['aggregates']:result.update(execute(bind(sql,p),query)[0])
        return {'report':name,'rows':[result]}
    if spec['kind']=='machine_parts':
        from html import escape
        from .source_trial_steps import equal
        p.update(startdate=shift_month(now,-3),enddate=now)
        parts=execute(bind(spec['parts'],p),query);detail=execute(bind(spec['details'],p),query)
        groups={}
        for r in detail:groups.setdefault(tuple(r[f] for f in ['sheetdate','name','sheetseries','sheetno']),[]).append(r)
        output=[]
        for (day,employee,series,number),items in groups.items():
            selected=[r['detailinfo'] for r in detail if day is not None and r['sheetdate']==day and equal(r['name'],employee) and r['detailinfo'] is not None]
            text=None if not selected else ('\t'.join(escape(s,quote=False)+'#br/#' for s in selected)).replace('#br/#','<br/>')
            amounts=[r['total'] for r in items if r['total'] is not None]
            output.append({'sheetdate':None if day is None else day.strftime('%Y-%m-%d %H:%M'),'name':employee,'sheetseries':series,
                'sheetno':number,'details':text,'totolmoney':sum(amounts) if amounts else None})
        return {'report':name,'rows':parts,'result_sets':[{'title':'近三个月领用明细','rows':output}]}
    if spec['kind']=='view':return {'report':name,'rows':execute(statement(name,parameters.get('filters',[])),query)}
    p.update(dtstart=p['startdate'] or now.replace(day=1,hour=0,minute=0,second=0,microsecond=0),
             dtend=p['enddate'] or shift_month(now.replace(day=1,hour=0,minute=0,second=0,microsecond=0),1)-timedelta(days=1),
             dsdate=(now-timedelta(days=7)).date().isoformat(),dtdate=now.date().isoformat(),hasfilter=int(bool(p['confilter'])))
    if name=='Sp_AppQueryGrayIn':
        p['dtstart']=p['startdate'] or now.replace(hour=0,minute=0,second=0,microsecond=0)-timedelta(days=1)
        p['dtend']=p['enddate'] or p['dtstart'].replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(days=1)
    if name.startswith('SP_StuffOut_Query') or name=='SP_YUNFEITONGJI':
        p['days']=None if p['startdate'] is None or p['enddate'] is None else p['startdate'].date().isoformat()+'至'+p['enddate'].date().isoformat()
    if spec['kind']=='steps':
        from .source_phase3_report_steps import run
        return run(name,spec,p,query,now)
    tree=temporary_views(parse_one(spec['sql'],read='tsql'),spec.get('temps',{}))
    result=execute(bind(tree.sql(dialect='tsql'),p),query)
    if spec['kind']=='price':
        item=result[0];money=Decimal(str(item['money'] or 0));qty=Decimal(str(item['qty'] or 0))
        if name!='fn_StuffPrice':
            money=money.quantize(Decimal(10)**-spec['money_scale'],rounding=ROUND_HALF_UP)
            qty=qty.quantize(Decimal(10)**-spec['qty_scale'],rounding=ROUND_HALF_UP)
        if name=='fn_StuffPriceMovingAverage':qty=qty.quantize(Decimal('.0001'),rounding=ROUND_HALF_UP)
        value=(Decimal(0) if qty==0 else money/qty).quantize(Decimal(10)**-spec['result_scale'],rounding=ROUND_HALF_UP)
        return {'report':name,'rows':[{'result':value,'money':money,'qty':qty}]}
    if spec['kind']=='article_text':
        value=None
        for item in result:
            value=None if item['value'] is None else ('' if value is None else value+'\n')+item['value']
        return {'report':name,'rows':[{'result':value}],'source_rows':result}
    if spec['kind']=='article_total':
        value=None if not result or result[-1]['value'] is None else str(result[-1]['value'])
        return {'report':name,'rows':[{'result':value}]}
    if spec['kind']!='paged':return {'report':name,'rows':result}
    current=int(p.get('current',1));size=p.get('size',20)
    if name=='sp_App_GetArticleInfoByPage':
        return {'report':name,'rows':sorted(result,key=lambda r:r['rowindex']),
                'pagination':{'current':1,'pages':1,'size':len(result),'total':len(result)}}
    if name!='Sp_AppQueryGrayStock' and (size is None or size<1):size=10
    selected=sorted((r for r in result if r['rowindex']>(current-1)*size),key=lambda r:r['rowindex'])[:size]
    page={'current':current,'size':size,'pages':ceil(len(result)/size),'total':len(result)}
    totals={'Sp_AppQueryGrayIn':['weightqty','rolls'],'Sp_AppQueryGrayStock':['weightqty','rolls'],
        'Sp_AppQueryProdStock':['rolls','weightqty','lengthqty'],'Sp_AppQuerySemiOut':['weightqty','rolls'],
        'Sp_AppQuerySemiStock':['weightqty','rolls'],'Sp_AppQueryStuffOutAccount':['outqty']}
    for field in totals.get(name,[]):page['sum'+field]=sum(r[field] or 0 for r in result) if result else None
    return {'report':name,'rows':selected,'pagination':page}
