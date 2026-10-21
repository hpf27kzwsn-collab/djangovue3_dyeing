"""原库位合并、染料单及材料价格回写。"""
from html import escape
from django.db import transaction
from django.utils import timezone
from django.db.models import Q
from .source_phase3_operations import SPECS,source,query,create,insert,change,retire,result
from .source_business_updates import matching
from .source_stock_services import raw
from .source_trial_steps import equal


@transaction.atomic
def positions(code,series,actor):
    table='GrayPostionUp' if code=='98' else 'SemiPostionUp'
    retained=retire(source(table).filter(Q(old_in_detail_no__iexact=series)|(Q(old_in_detail_no__isnull=True) if series=='A-1' else Q(pk__in=[]))),actor,'原入库库位重新合并，旧记录留档')
    values=query(SPECS[code]['source'],{'sheetseries':series});created=[]
    for value in values:
        tokens=[]
        for field in ['field1','field2']:
            text=value[field]
            if text is None:continue
            start=0
            for token in text.split(';'):
                if start<1000:tokens.append(token)
                start+=len(token)+1
        unique=[]
        for token in tokens:
            if not any(equal(token,seen) for seen in unique):unique.append(token)
        if not unique:continue # 原SplitValues空集不产生汇总行；输入来源仍在原表。
        area=';'.join(escape(v,quote=False) for v in sorted(unique,key=lambda v:v.upper().rstrip()))
        no=series+str(value['id']).zfill(2)[-2:]
        values={f:value[f.lower()] for f in ['CustomerID','InSheetKind','LotNo','ColorID','PreField1','FixedQty','PurchaseOrders','A_A','A_B']}
        values.update(SheetSeries=no,SheetNo=no,SheetDate=timezone.now(),SheetKind=1,ProdID=value['grayid' if code=='98' else 'prodid'],
            Area='',NewArea=area,Creater='入库时',CreateDate=timezone.now(),InDetailNo=series)
        created.append(create(table,values,actor))
    return result('InTo'+table,created,retained)


@transaction.atomic
def dye_order(series,actor,cleanup=False):
    heads=list(matching(source('StuffOut'),SheetSeries=series).order_by('pk'));retained=[];created=[]
    if not cleanup and (not heads or raw(heads[-1],'SheetKind')!=29):return result('Dyeingliaodan',[])
    if any(raw(h,'RightStatus') not in [10,'10'] for h in heads):
        for table in ['DyeStuffOut','DyeStuffOutDetail']:retained.extend(retire(matching(source(table),SheetSeries=series),actor,'Dyeingliaodaninto反审核原染料单留档'))
    if not cleanup:
        for spec in SPECS['92']['inserts']:created.extend(insert(spec,{'dyesheetseries':series},actor))
    return result('Dyeingliaodaninto' if cleanup else 'Dyeingliaodan',created,retained)


@transaction.atomic
def prices(series,actor,all_materials=False):
    from .source_phase3_triggers import latest_stuff_price,fill_stuff_price
    selected=source('p_Stuff').order_by('pk') if all_materials else matching(source('StuffStockBook'),SheetSeries=series).order_by('pk')
    price=None;changed=[]
    for item in selected:
        current=latest_stuff_price(raw(item,'StuffID'))
        if current is not None:price=current # 原游标本轮无SELECT命中时保留上一轮变量。
        if price is not None and price>0:
            if all_materials:change(matching(source('p_Stuff'),StuffID=raw(item,'StuffID')),{'Price':price},actor)
            else:fill_stuff_price(raw(item,'StuffID'),price,actor,False)
        changed.append(item)
    return result('Sp_Stuffin_Price' if all_materials else 'Sp_StuffPrice',changed)
