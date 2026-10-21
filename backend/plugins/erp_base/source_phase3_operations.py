"""原收发转仓的明确办理。SQL仅取固定投影，写入及留档由Django事务完成。"""
import json
from pathlib import Path
from django.apps import apps
from django.db import transaction
from django.utils import timezone
from sqlglot import parse_one
from .source_phase2_reports import temporary_views
from .source_phase3_sql import bind
from .source_static_lookup import execute
from .source_quality_reports import rows
from .source_business_updates import matching,update_rows
from .source_stock_services import raw
from .source_calculations import store_value
from .source_sequences import allocate
from .source_master_data import retain
from .business import persist,record,snapshot

SPECS=json.loads(Path(__file__).with_name('source_phase3_operation_queries.json').read_text(encoding='utf8'))


def model(table):
    return next(m for m in apps.get_models() if getattr(m,'SOURCE_TABLE',None)==table)


def source(table):
    from .source_execution_state import active
    return active(model(table).objects.all())


def query(sql,p,temps=None,reader=rows):
    tree=temporary_views(parse_one(sql,read='tsql'),temps or {})
    return execute(bind(tree.sql(dialect='tsql'),p),reader)


def create(table,values,actor):
    from .source_services import apply_defaults
    from .source_phase3_triggers import saved
    item=model(table)();data=dict(store_value(item,k,v) for k,v in values.items())
    apply_defaults(item,data)
    for key,value in data.items():
        if item._meta.get_field(key).get_internal_type()=='DateTimeField' and value is not None and timezone.is_naive(value):
            value=timezone.make_aware(value)
        setattr(item,key,value)
    allocate(item,actor);persist(item,actor)
    record(item,'phase3_original_create',{'exists':False},actor,'原过程投影逐行写入；重复业务键不去重')
    saved(item,data,True,actor)
    from .source_phase4_triggers import saved as production_saved
    production_saved(item,data,True,actor)
    from .source_phase5_triggers import saved as delivery_saved
    delivery_saved(item,data,True,actor)
    return item


def insert(spec,p,actor,temps=None):
    values=query(spec['sql'],p,temps)
    fields={key.lower():key for key in model(spec['table']).SOURCE_FIELDS}
    return [create(spec['table'],{fields[k]:v for k,v in value.items()},actor) for value in values]


def change(targets,values,actor):
    update_rows(targets,values,actor,'phase3_original_update','第三阶段原业务明确回写，前值留档')


def retire(targets,actor,note):
    result=[]
    for item in targets.order_by('pk'):
        result.append({'entity':item._meta.label,'id':item.pk,'before':snapshot(item)})
        retain(item,actor,note)
    return result


def result(name,items,retained=()):
    return {'report':name,'rows':[{'entity':r._meta.label,'id':r.pk} for r in items],'retained':list(retained)}


def numbers(table,entry,actor):
    from .source_entry_registry import ENTRY_RULES
    from .source_numbers import generate
    item=model(table)();definition=ENTRY_RULES[item._meta.label][entry];at=timezone.localtime()
    values={old:generate(item,old,definition['number_fields'][old],actor,at) for old in ['SheetSeries','SheetNo']}
    return values['SheetSeries'],values['SheetNo']


@transaction.atomic
def staging(code,actor,staging_rows=None):
    from .source_phase3_posting import post
    spec=SPECS[code];created=[];temps=dict(spec['temps'])
    if code=='235':
        # 最新库已无GrayInRecord_Test；调用者提交原过程明确使用的暂存行，逐行留存在办理审计中。
        temps['t']=staging_sql(staging_rows)
    for definition in spec['inserts']:created.extend(insert(definition,{},actor,temps))
    table='GrayIn' if code=='235' else 'ProdIn'
    for item in [r for r in created if r.SOURCE_TABLE==table]:
        post(table,raw(item,'SheetSeries'),actor)
        if code=='235':record(item,'phase3_staging_source',snapshot(item),actor,'原缺失暂存表输入：'+str(staging_rows))
    return result('sp_AuTo_GrayIn' if code=='235' else 'sp_AuTo_ProdIn_to',created)


STAGING_FIELDS={'SheetSeries':'VARCHAR(50)','CustJobNo':'VARCHAR(100)','SheetDate':'DATETIME','CustomerID':'VARCHAR(50)',
 'GrayID':'VARCHAR(50)','PreField1':'VARCHAR(100)','MachineID':'VARCHAR(50)','PreField3':'VARCHAR(100)',
 'PreField5':'VARCHAR(100)','Area':'VARCHAR(200)','StorageUnitIDs':'VARCHAR(200)','GUnit':'VARCHAR(10)',
 'Rolls':'DECIMAL(18,4)','WeightQty':'DECIMAL(18,4)','LengthQty':'DECIMAL(18,4)','RollNo':'VARCHAR(100)','BarCode':'VARCHAR(200)'}


def staging_sql(values):
    from .source_phase2_reports import date
    sql='SELECT '+','.join('CAST(@'+k+' AS '+t+') AS ['+k+']' for k,t in STAGING_FIELDS.items())
    output=[]
    for value in values:
        p={k:value.get(k) for k in STAGING_FIELDS};p['SheetDate']=date(p['SheetDate'])
        output.append(bind(sql,p))
    return ' UNION ALL '.join(output) if output else bind(sql,{k:None for k in STAGING_FIELDS})+' WHERE 1=0'


@transaction.atomic
def records(code,p,actor):
    spec=SPECS[code];retained=[]
    if code=='302':
        values=query('SELECT * FROM #t_detail',p,spec['temps']);targets=matching(source('ProdInRecord'),SheetSeries=p['sheetseries'])
        from .source_trial_steps import equal
        for item in targets.order_by('pk'):
            candidates=[r for r in values if equal(r['sheetseries'],raw(item,'SheetSeries')) and equal(r['barcode'],raw(item,'BarCode'))]
            selected=None if not candidates else candidates[-1]
            change(targets.filter(pk=item.pk),{f:None if selected is None else selected[f.lower()] for f in ['LengthQty','GrayQty']},actor)
            if len(candidates)>1:record(item,'phase3_ambiguous_join',snapshot(item),actor,'同流水/条码有多条计算结果：'+str(candidates))
        return result('Sp_InProdInRecord',targets)
    if code=='304':
        assignments=matching(source('SemiOutDetail'),SheetSeries=p['semioutsheetseries']).values_list('old_assigned_no',flat=True)
        retained=retire(source('SemiOutRecord').filter(old_assigned_no__in=assignments),actor,'Sp_InSertSemiOutRecord重新分配细码，原行留档')
    created=insert(spec['inserts'][0],p,actor,spec['temps'])
    return result('Sp_InSertGrayOutRecord' if code=='303' else 'Sp_InSertSemiOutRecord',created,retained)


@transaction.atomic
def transfer(code,series,actor,state=1):
    from .source_phase3_posting import post
    spec=SPECS[code];created=[];retained=[]
    forward=code in ['299','372']
    origin,target,kind,link,entry=(('GrayOut','SemiIn',26,'GrayOutSheetNo','TurnSemiIn') if code=='299' else
        ('SemiOut','GrayIn',30,'SemiOutSheetNo','SemiToGrayIn') if code=='372' else
        ('GrayIn','SemiOut',20,'SemiOutSheetNo','SemiOut') if code=='338' else
        ('SemiIn','GrayOut',24,'GrayOutSheetNo','GrayOut'))
    sources=list(matching(source(origin),SheetSeries=series).filter(old_sheet_kind=kind).order_by('pk'))
    if not sources:return result(spec.get('name',code),[])
    head=sources[-1];ss=sn=None;when=timezone.now()
    p={origin.lower()+'sheetseries':series}
    if forward:
        old=list(matching(source(target),**{link:series}).order_by('pk'))
        ss,sn=numbers(target,entry,actor)
        p.update(sheetseriesout=ss,sheetnoout=sn,customerid=raw(head,'CustomerID'),sheetdate=raw(head,'SheetDate'),
            creater=raw(head,'Creater'),supplierid=raw(head,'SupplierID') if code=='299' else None)
        # 原372的SupplierID声明后没有赋值，保持NULL。
    else:
        old=[] if state==1 else list(matching(source(target),SheetSeries=raw(head,link)).order_by('pk'))
        if old:ss=raw(old[-1],'SheetSeries');sn=raw(old[-1],'SheetNo');when=raw(old[-1],'SheetDate')
        else:ss,sn=numbers(target,entry,actor)
        p.update(ss=ss,sn=sn,sheetdate=when,sheetkind=30 if code=='338' else 26)
    for previous in old:
        oldseries=raw(previous,'SheetSeries')
        for name in [target+'Detail',target.removesuffix('In').removesuffix('Out')+'StockBook',target]:
            retained.extend(retire(matching(source(name),SheetSeries=oldseries),actor,'原转仓先删后增，旧版本留档'))
    for definition in spec['inserts']:
        created.extend(insert(definition,p,actor,spec['temps']))
    if forward:post(entry,ss,actor)
    elif state==1:change(matching(source(origin),SheetSeries=series),{link:ss},actor)
    if len(sources)>1:record(head,'phase3_ambiguous_header',snapshot(head),actor,'原标量表头候选全部保留：'+str([r.pk for r in sources]))
    return result({'299':'Sp_GrayOutTurn_SemiStockBook','372':'Sp_SemiOutTurn_GrayStockBook','338':'Sp_ProdSemiOutStockInfo','394':'Sp_TurnGrayOutStockInfo'}[code],created,retained)
