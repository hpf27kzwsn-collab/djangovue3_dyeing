"""原仓储触发规则。异常检查留事实，原字段回写保留重复行和来源。"""
from django.utils import timezone
from django.core.exceptions import ValidationError
from .source_provenance import is_historical
from .source_quality_reports import rows
from .source_business_updates import matching,update_rows
from .source_stock_services import raw
from .source_master_data import retain
from .business import record,snapshot


def change(query,values,actor):
    update_rows(query,values,actor,'original_warehouse_trigger','采用原仓储触发器字段回写')


def anomaly(item,actor,name,values):
    record(item,'original_warehouse_anomaly',snapshot(item),actor,name+'：'+str(values)+'；原记录完整保留')


def latest_stuff_price(stuff,query=rows,positive=True):
    pairs=[(head,line) for line in matching(query('StuffInDetail','erp_warehouse'),StuffID=stuff).order_by('pk')
        if not positive or raw(line,'Price') is not None and raw(line,'Price')>0
        for head in matching(query('StuffIn','erp_warehouse'),SheetSeries=raw(line,'SheetSeries')).filter(old_sheet_kind=13).order_by('pk')]
    pairs.sort(key=lambda pair:(raw(pair[0],'SheetDate') is not None,raw(pair[0],'SheetDate'),pair[0].pk,pair[1].pk),reverse=True)
    return None if not pairs else raw(pairs[0][1],'Price')


def fill_stuff_price(stuff,price,actor,master):
    targets=matching(rows('StuffStockBook','erp_warehouse'),StuffID=stuff)
    for line in targets.order_by('pk'):
        if raw(line,'Price') in [None,0]:
            values={'Price':price}
            for qty,money in [('OutQty','OutMoney'),('InQty','InMoney')]:
                values[money]=None if price is None or raw(line,qty) is None else price*raw(line,qty)
            change(targets.filter(pk=line.pk),values,actor)
    if master:change(matching(rows('PStuff','erp_base'),StuffID=stuff),{'Price':price},actor)


def saved(item,data,created,actor):
    if is_historical(item):return
    table=item.SOURCE_TABLE
    if table in ['p_Gray','p_Stuff'] and created:
        fields=['GrayID','NameC'] if table=='p_Gray' else ['Name']
        for field in fields:
            count=matching(type(item).objects.all(),**{field:raw(item,field)}).count()
            if count>1:anomaly(item,actor,table+'Insert',{field:raw(item,field),'count':count})
    elif table in ['GrayInDetail','SemiInDetail']:
        family=table.removesuffix('Detail');receipt=raw(item,'ReceSheetNo');lot=raw(item,'LotNo')
        lot=None if lot is None else lot.replace('\t','')
        if family=='GrayIn' and lot is not None:lot=lot.strip(' ')
        change(matching(rows(table,'erp_warehouse'),ReceSheetNo=receipt),{'LotNo':lot},actor)
        item.refresh_from_db()
        if family=='GrayIn' and created:
            heads=matching(rows('GrayIn','erp_warehouse'),SheetSeries=raw(item,'SheetSeries')).order_by('pk')
            head=heads.last();job=raw(item,'OriJobsheetNo')
            if head is not None and raw(head,'SheetKind')==14 and job is not None and job.rstrip(' '):
                change(matching(rows('JobSheet','erp_production'),SheetNo=job),{'CurrProcessID':'退仓待处理','SheetStatus':9},actor)
    elif table=='GrayInRecord' and raw(item,'BarCode') in [None,'']:
        receipt,roll=raw(item,'ReceSheetNo'),raw(item,'RollNo')
        value=None if receipt is None or roll is None else receipt.strip(' ')+roll
        change(matching(rows('GrayInRecord','erp_warehouse'),ReceSheetNo=receipt,RollNo=roll),{'BarCode':value},actor)
        item.refresh_from_db()
    elif table=='GrayOutDetail':
        heads=list(matching(rows('GrayOut','erp_warehouse'),SheetSeries=raw(item,'SheetSeries')).order_by('pk'))
        if heads and raw(heads[-1],'SheetKind')==29:
            change(matching(rows('JobSheet','erp_production'),SheetNo=raw(item,'JobSheetSeries'),CurrProcessID='退仓待处理').filter(old_sheet_status=9),
                {'CurrProcessID':'返车间生产','SheetStatus':0},actor)
    elif table=='ArticleOutDetail':
        sources=list(matching(rows('ArticleInDetail','erp_warehouse'),DetailNo=raw(item,'InDetailNo')).order_by('pk'))
        # 原子查询排除当前InDetailNo，实际比较的是入库量，不能擅自换成累计可用量。
        available=None if not sources else raw(sources[-1],'InQty')
        if available is not None and raw(item,'OutQty') is not None and raw(item,'OutQty')>available:
            anomaly(item,actor,'CheckCanOut_InDetailNo',{'OutQty':raw(item,'OutQty'),'SaveQty':available})
    elif table=='SemiOut':
        details=list(matching(rows('SemiOutDetail','erp_warehouse'),SheetSeries=raw(item,'SheetSeries')).order_by('pk'))
        target=rows('SemiOutWorkApplyDetail','erp_production').order_by('pk').first()
        if details and target is not None:
            from .source_trial_steps import equal
            compared=[(raw(details[-1],'JobSheetNo'),raw(target,'DetailNo')),(raw(item,'CustomerID'),raw(target,'CustomerID')),
                (raw(details[-1],'ProdID'),raw(target,'ProdID'))]
            if all(not equal(a or '',b or '') for a,b in compared):anomaly(item,actor,'SemiOutStockBookCheck',compared)
    elif table=='ProdIn' and created:
        number=raw(item,'JobSheetNo') or ''
        for schedule in matching(rows('ProcessSchedule','erp_production'),JobSheetNo=number):
            retain(schedule,actor,'ProdInInsert：入库后退出排程，原记录留档')
        incoming=list(matching(rows('ProdIn','erp_warehouse'),JobSheetNo=number).order_by('pk'))
        for job in matching(rows('JobSheet','erp_production'),SheetNo=number):
            change(matching(rows('JobProcess','erp_production'),SheetSeries=raw(job,'SheetSeries'),ProcessID='GX98'),
                {'EndTime':raw(incoming[-1],'SheetDate')},actor)
    elif table=='StuffOut':
        targets=matching(rows('StuffOut','erp_warehouse'),SheetSeries=raw(item,'SheetSeries'))
        kind=raw(item,'SheetKind');outdate=raw(item,'OutDate');now=timezone.now()
        if kind==21 and outdate is not None and outdate>now:
            anomaly(item,actor,'StuffOut_INSERT',{'OutDate':str(outdate),'now':str(now)})
        weight=raw(item,'WeightSheetNo');sources=list(matching(rows('StuffWeight','erp_production'),SheetNo=weight).order_by('pk'))
        if weight is not None and weight.rstrip(' '):
            change(targets,{'JobSheetNo':None if not sources else raw(sources[-1],'JobSheetNo')},actor)
        if outdate is None:
            values={'OutDate':now if kind==21 else raw(item,'SheetDate')}
            if kind==21:
                values['WareHouseID']=None if not sources else raw(sources[-1],'WareHouseID')
                if len(sources)>1:anomaly(item,actor,'StuffOut_INSERT原标量子查询多行',{'source_ids':[r.pk for r in sources]})
            change(targets,values,actor)
        item.refresh_from_db()
    elif table=='StuffStockBook' and (raw(item,'Price') or 0)>=0:
        stuff=raw(item,'StuffID');fill_stuff_price(stuff,latest_stuff_price(stuff),actor,True)
        item.refresh_from_db()


def removing(item,actor):
    if item.SOURCE_TABLE=='ArticleInDetail' and matching(rows('ArticleOutDetail','erp_warehouse'),InDetailNo=raw(item,'DetailNo')).exists():
        raise ValidationError({'source':'原CheckArticleOutInDetailNo：入库明细已有实际出库引用，不能删除。'})
    # GrayOut_Delete的@JobSheetNo和@WProcessNo均未赋值，原删除分支不匹配任何行。
    # 需要撤销关联报工时使用明确的整链逆向服务，不能在普通表头删除中推断扩展。
