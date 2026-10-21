"""自动领料和坯料出库的原变体。数量来源分别保留，显式调用后办理。"""
from django.db import transaction
from django.utils import timezone
from .source_phase3_operations import SPECS,source,model,query,create,insert,change,retire,result,numbers
from .source_business_updates import matching
from .source_stock_services import raw
from .source_phase3_posting import post
from .source_daily_numbers import allocate
from .source_quality_reports import total
from .business import record,snapshot


def new_code(table,width,actor):
    number=allocate(table,width,False,actor)['rows'][0]['code']
    return None if number is None else 'AO'+number


@transaction.atomic
def gray(job,actor):
    spec=SPECS['236'];heads=list(matching(source('JobSheet'),SheetNo=job).order_by('pk'))
    if not heads:return result('Sp_AUTO_GrayOut',[])
    head=heads[-1];assigned=matching(source('JobGrayRecord'),SheetSeries=raw(head,'SheetSeries'))
    if raw(head,'AssignUnit') not in [0,2] or not any(raw(r,'AssignedNo') in [None,''] for r in assigned):return result('Sp_AUTO_GrayOut',[])
    previous=matching(source('GrayOutDetail'),JobSheetNo=job);series=list(previous.values_list('old_sheet_series',flat=True));retained=[]
    for table in ['GrayOut','GrayOutRecord']:retained.extend(retire(source(table).filter(old_sheet_series__in=series),actor,'Sp_AUTO_GrayOut重新出库，原单据留档'))
    retained.extend(retire(previous,actor,'自动出库原明细留档'));retained.extend(retire(matching(source('GrayStockBook'),JobSheetNo=job),actor,'自动出库原流水留档'))
    ss=new_code('GrayOut',3,actor);p={'sheetseriesout':ss,'jobsheetno':job,'customerid':raw(head,'CustomerID')};created=[]
    for definition in spec['inserts']:created.extend(insert(definition,p,actor))
    for row in matching(source('GrayOutRecord'),JobSheetNo=job).order_by('pk'):
        for table,barcode in [('JobGrayRecord','GrayBarCode'),('GrayInRecord','BarCode')]:
            values={'AssignedNo':raw(row,'AssignedNo')}
            if table=='GrayInRecord':values['JobSheetNo']=job
            change(matching(source(table),ReceSheetNo=raw(row,'ReceSheetNo'),**{barcode:raw(row,'BarCode')}),values,actor)
    post('GrayOut',ss,actor)
    details=list(matching(source('GrayOutDetail'),JobSheetNo=job));values={'CurrProcessID':'坯布出库'}
    for field in ['Rolls','WeightQty','LengthQty']:
        value=total(raw(r,field) or 0 for r in details)
        for prefix in ['SumAssigned','SumProcess']:values[prefix+field]=value
    change(matching(source('JobSheet'),SheetNo=job),values,actor)
    return result('Sp_AUTO_GrayOut',created,retained)


@transaction.atomic
def gray_all(actor):
    selected=[raw(r,'SheetNo') for r in source('JobSheet').order_by('pk') if raw(r,'AssignUnit') in [0,2]
        and raw(r,'SumProcessLengthQty') in [None,0] and raw(r,'PreRolls') is not None and raw(r,'PreRolls')>0 and raw(r,'SheetStatus') in [None,0]]
    output=[gray(job,actor) for job in selected]
    return {'report':'Sp_AUTO_GrayOut_all','rows':[r for result in output for r in result['rows']],
        'retained':[r for result in output for r in result['retained']]}


@transaction.atomic
def stuff(code,job,actor):
    spec=SPECS[code];created=[];price=None
    if code=='378':return planned(actor)
    values=query(spec['source'],{'jobsheetno':job})
    for value in values:
        p={'jobsheetno':job,**value};ss=new_code('StuffOut',4,actor);p.update(sheetseriesout=ss,sheetnoout=ss)
        if code=='243':
            masters=list(matching(source('p_Stuff'),StuffID=p['stuffid']).order_by('pk'))
            if masters:price=raw(masters[-1],'Price')
            p['price']=price
        for definition in spec['inserts']:
            definition={**definition,'sql':definition['sql'].replace('10 AS SheetStatus',"'1' AS SheetStatus")}
            items=insert(definition,p,actor);created.extend(items)
            for item in items:
                if item.SOURCE_TABLE=='StuffOut':record(item,'phase3_status_width',snapshot(item),actor,'原自动过程写SheetStatus=10，但最新列char(1)，采用1；原目标值10在此留档')
        post('StuffOut',ss,actor)
    return result('Sp_AUTO_StuffOut' if code=='243' else 'Sp_AUTO_StuffOut_small',created)


@transaction.atomic
def planned(actor):
    from sqlglot import exp
    specs=SPECS['378']['inserts'];fig=query(specs[0]['sql'],{})
    # @Fig在原过程先形成快照；随后新增出库单不能改变本次候选行。
    names=list(fig[0]) if fig else []
    if not fig:return result('Sp_StuffAutoOutPutFig',[])
    from .source_phase3_sql import bind
    fields=','.join('@'+f+' AS ['+f+']' for f in names)
    temp=' UNION ALL '.join(bind('SELECT '+fields,row) for row in fig)
    temps={'fig':temp};group=query(specs[1]['sql'],{},temps);created=[]
    for row in group:
        # 原MAX(RIGHT(...,9))+1在空表/混号下无法成号；采用已有原日编号规则，差异在异常清单明确列出。
        ss=new_code('StuffOut',4,actor)
        p={'sheetseriescode':ss,'sheetnocode':ss,'autosheetseries':row['figsheetseries'],'autosheetno':row['figsheetno'],
            'autotime':row['endtime'],'autocustomerid':row['customerid'],'autodeptid':row['deptid']}
        head=insert(specs[2],p,actor)[0];created.append(head)
        # WOF=0没有有效数量，保留明细并记录原除零事实，不能把系数改成1。
        detail={**specs[3],'sql':specs[3]['sql'].replace('ISNULL(WOF, 1)','NULLIF(ISNULL(WOF, 1),0)')}
        for item in insert(detail,p,actor,temps):
            created.append(item)
            if raw(item,'Qty') is None:record(item,'phase3_zero_wof',snapshot(item),actor,'计划领料原WOF为0，数量金额保留NULL；来源：'+str(fig))
        post('StuffOut',ss,actor)
    return result('Sp_StuffAutoOutPutFig',created)


@transaction.atomic
def balance(series,actor):
    specs=SPECS['433']['inserts'];ss,sn=numbers('GrayBalance','GrayBalance',actor)
    p={'sheetseries':ss,'sheetno':sn,'outsheetseries':series}
    sql=specs[0]['sql'];values=query(sql,p)
    selected=[v for v in values if v['piece'] is not None and v['piece']<=0 or v['weightqty'] is not None and v['weightqty']<=0]
    if not selected:return result('ToGrayBalance',[])
    first=values[0];head=create('GrayBalance',{'SheetSeries':ss,'SheetNo':sn,'SheetDate':timezone.now(),'WareHouseID':first['warehouseid'],
        'SheetKind':55,'SheetStatus':0,'RightStatus':0,'Remarks':'出库流水号'+series+'自动平账'},actor)
    fields={f.lower():f for f in model('GrayBalanceDetail').SOURCE_FIELDS}
    created=[head]+[create('GrayBalanceDetail',{fields[k]:v for k,v in value.items()},actor) for value in selected]
    post('GrayBalance',ss,actor)
    return result('ToGrayBalance',created)
