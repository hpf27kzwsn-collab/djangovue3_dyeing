"""八个原库存结转变体；按原分组保存，反结转原行留档。"""
import json
from pathlib import Path
from decimal import Decimal,ROUND_HALF_UP
from django.db import transaction
from .source_phase3_sql import bind
from .source_static_lookup import execute
from .source_quality_reports import rows
from .source_business_updates import matching,update_rows
from .source_stock_services import raw
from .source_calculations import store_value
from .source_sequences import allocate
from .source_master_data import retain
from .business import persist,record,snapshot

SPECS=json.loads(Path(__file__).with_name('source_phase3_carry.json').read_text(encoding='utf8'))


def change(query,values,actor):
    from django.utils import timezone
    values={key:timezone.make_aware(value) if value is not None and query.model._meta.get_field(query.model.SOURCE_FIELDS[key]).get_internal_type()=='DateTimeField' and timezone.is_naive(value) else value for key,value in values.items()}
    update_rows(query,values,actor,'original_inventory_carry','原库存结转/反结转明确回写')


def create(table,values,actor):
    from .source_phase3_operations import create as original_create
    return original_create(table,values,actor)


def scope(query,name):
    if name=='Sp_UpdateBigStuffStock':return matching(query,WareHouseID='12')
    if name=='Sp_UpdateStuffStock':return query.filter(old_ware_house_id__in=['13','14'])
    return query


def weighted_price(stuff,warehouse,end):
    from .source_phase4_functions import weighted_price as original_weighted_price
    return original_weighted_price('Stuff',stuff,warehouse)['result']


@transaction.atomic
def carry(name,kind,maxstockdate,startdate,enddate,actor):
    spec=SPECS[name];table=spec['table'];family=table.removesuffix('Stock')
    stocks=scope(rows(table,'erp_warehouse'),name);book=scope(rows(table+'Book','erp_warehouse'),name)
    result=[]
    if kind==1:
        removed=stocks.filter(old_carry_date__gte=enddate) if family in ['Gray','Semi'] else stocks.filter(old_stock_date=maxstockdate)
        for item in removed.order_by('pk'):
            result.append({'entity':item._meta.label,'id':item.pk,'operation':'反结转留档'})
            retain(item,actor,name+'反结转，原结存保留')
        change(book.filter(old_book_date__gt=startdate,old_book_date__lte=maxstockdate),{'StockFlag':'N'},actor)
        return {'report':name,'rows':result}
    if kind!=0:return {'report':name,'rows':[]} # 原过程只定义0/1两种办理。
    parameters={'maxstockdate':maxstockdate,'startdate':startdate,'enddate':enddate,'fnewprice':None}
    source=execute(bind(spec['source'],parameters),rows)
    setting='CostMethodOfArticle' if family=='Article' else 'CostMethodOfStuff'
    settings=list(matching(rows('SSysParams','erp_base'),ParamName=setting).order_by('pk'))
    mode=None if not settings else raw(settings[-1],'ParamValue')
    for row in source:
        parameters.update(row)
        projections=', '.join(sql+' AS ['+field+']' for field,sql in spec['values'].items())
        value=execute(bind('SELECT '+projections,parameters),rows)[0]
        values={field:value[field.lower()] for field in spec['values']}
        missing_detail=family in ['Stuff','Article'] and values.get('InDetailNo') is None
        if missing_detail:values['InDetailNo']=''
        existing=stocks.none()
        if family in ['Stuff','Article']:
            criteria={family+'ID':values[family+'ID'],'WareHouseID':values['WareHouseID']}
            if name in ['Sp_UpdateArticleStock','Sp_UpdateBigStuffStock']:criteria['InDetailNo']=values['InDetailNo']
            if name=='Sp_UpdateBigStuffStock':criteria['LotNo']=values['LotNo']
            existing=matching(stocks,**criteria).filter(old_stock_date=enddate)
            if missing_detail and name in ['Sp_UpdateArticleStock','Sp_UpdateBigStuffStock']:existing=stocks.none()
        targets=list(existing.order_by('pk'))
        if targets:
            fields=['PreMonthQty','Price','PreMonthMoney','CarryDate','Remarks']
            if family=='Stuff':fields.append('LotNo')
            updates={f:values[f] for f in fields}
            if family=='Article':updates['PreMonthMoney']=row['papermoney']
            if name in ['Sp_UpdateStuffStock_2208','Sp_UpdateStuffStock_Old']:updates.update(Price=row['price'],PreMonthMoney=row['total'])
            change(existing,updates,actor)
            result.extend({'entity':r._meta.label,'id':r.pk,'operation':'更新结存'} for r in targets)
            continue
        old_weighted=name in ['Sp_UpdateStuffStock_2208','Sp_UpdateStuffStock_Old'] and mode=='W'
        if old_weighted:
            price=weighted_price(row['stuffid'],row['warehouseid'],enddate)
            values.update(Price=price,PreMonthMoney=None if row['qty'] is None else price*Decimal(str(row['qty'])))
        item=create(table,values,actor);result.append({'entity':item._meta.label,'id':item.pk,'operation':'新增结存'})
        if missing_detail:record(item,'phase3_carry_missing_detail',snapshot(item),actor,
            name+'没有可写入最新非空InDetailNo的原值；本次写空串，完整原分组值留档：'+str(row))
        recalc=(family=='Article' and mode=='W') or (name in ['Sp_UpdateStuffStock','Sp_UpdateBigStuffStock'] and mode=='N') or old_weighted
        if recalc:
            price=None if family=='Article' else weighted_price(row['stuffid'],row['warehouseid'],enddate)
            if old_weighted and price<=0:continue
            code=row[family.lower()+'id'];warehouse=row['warehouseid'];lower=startdate if family=='Article' else maxstockdate
            heads=matching(rows(family+'Out','erp_warehouse'),WareHouseID=warehouse).filter(old_sheet_date__gt=lower,old_sheet_date__lte=enddate)
            for head in heads:
                for line in matching(rows(family+'OutDetail','erp_warehouse'),SheetSeries=raw(head,'SheetSeries'),**{family+'ID':code}):
                    qty=raw(line,'OutQty' if family=='Article' else 'Qty')
                    change(type(line).objects.filter(pk=line.pk),{'Price':price,'Total' if family=='Article' else 'Amount':None if price is None or qty is None else float(price)*float(qty)},actor)
            if old_weighted:
                for head in matching(rows('StuffIn','erp_warehouse'),WareHouseID=warehouse).filter(old_sheet_kind=15,old_sheet_date__gt=lower,old_sheet_date__lte=enddate):
                    for line in matching(rows('StuffInDetail','erp_warehouse'),SheetSeries=raw(head,'SheetSeries'),StuffID=code):
                        qty=raw(line,'Qty')
                        change(type(line).objects.filter(pk=line.pk),{'Price':price,'Amount':None if qty is None else float(price)*float(qty)},actor)
            selected=matching(book,**{family+'ID':code,'WareHouseID':warehouse}).filter(old_book_date__gt=lower,old_book_date__lte=enddate)
            for target in selected:
                kinds=[21,23,24,25,29] if family=='Article' else [15,21,22,24,29] if old_weighted else [21,22,29]
                field='OutMoney' if raw(target,'BookKind') in kinds else 'InMoney' if raw(target,'BookKind')==33 else None
                if field is not None:
                    qty=raw(target,'OutQty' if field=='OutMoney' else 'InQty')
                    change(type(target).objects.filter(pk=target.pk),{'Price':price,field:None if price is None or qty is None else float(price)*float(qty)},actor)
            reprice_stocks=stocks.none() if old_weighted else matching(stocks,**{family+'ID':code,'WareHouseID':warehouse}).filter(old_carry_date__gt=maxstockdate,old_carry_date__lte=enddate)
            for target in reprice_stocks:
                qty=raw(target,'PreMonthQty')
                change(type(target).objects.filter(pk=target.pk),{'Price':price,'PreMonthMoney':None if price is None or qty is None else float(price)*float(qty)},actor)
            if family=='Article':change(matching(rows('PArticle','erp_base'),ArticleID=code).exclude(old_price=0).exclude(old_price__isnull=True),{'Price':None},actor)
    change(book.filter(old_book_date__gt=maxstockdate,old_book_date__lte=enddate),{'StockFlag':'Y'},actor)
    return {'report':name,'rows':result}
