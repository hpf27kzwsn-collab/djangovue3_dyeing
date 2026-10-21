"""第二阶段明确批量办理：阶段补号、复版分配、材料调价及收费回写。"""
from decimal import Decimal
from django.db import transaction
from .business import snapshot
from .source_quality_reports import rows,total
from .source_stock_services import raw
from .source_business_updates import matching,update_rows
from .source_master_data import retain
from .source_continuation import save_effect
from .source_services import write
from .source_phase2_functions import previous_material_price
from .source_trial_steps import equal,sql_like
from .source_calculations import store_value


def change(query,values,actor):
    update_rows(query,values,actor,'phase2_operation','按第二阶段原过程办理')


@transaction.atomic
def auto_phase(actor):
    previous_series=0;previous_phase='N';phase=stuff=None;changed=[]
    source=list(rows('SmpPrescriptEntry','erp_sampling').filter(old_phase_no__isnull=True).order_by('old_finter_id','old_fentry_id','pk'))
    for item in source:
        series=raw(item,'FInterID');technology=None if raw(item,'FTechID') is None else str(raw(item,'FTechID'))
        if series==previous_series:
            if previous_phase is not None and technology is not None and not equal(previous_phase,technology):
                phase=None if phase is None else phase+1;stuff=1
            else:stuff=None if stuff is None else stuff+1
        else:phase=stuff=1
        targets=rows('SmpPrescriptEntry','erp_sampling').filter(old_finter_id=series,old_fentry_id=raw(item,'FEntryID'))
        changed.extend({'id':r.pk,'before':snapshot(r)} for r in targets)
        change(targets,{'PhaseNo':phase,'StuffNo':stuff},actor)
        previous_series,previous_phase=series,technology
    return {'report':'AutoCalcPhaseNo','rows':changed}


@transaction.atomic
def reprint(item,actor,retain_zero=False):
    members=list(matching(rows('DyeReprint','erp_sampling'),SheetSeries=raw(item,'SheetSeries')).order_by('pk'))
    before=[{'id':r.pk,'before':snapshot(r)} for r in members]
    for member in members:
        number=sum(1 for f in ['EmpID','EmpID1','EmpID2','EmpID3'] if not equal(raw(member,f) or '', ''))
        share=None if retain_zero and number==0 else 1.0/number
        if retain_zero and number==0:
            from .business import record
            record(member,'entry_reprint_zero_people',snapshot(member),actor,'原复版分摊分母为零；保存全部人员原字段，Num记NULL，不伪造份额')
        change(matching(rows('DyeReprint','erp_sampling'),SheetSeries=raw(member,'SheetSeries')),{'Num':share},actor)
    save_effect(item,'reprint_allocation',{'rows':before},actor,'Sp_DyeReprint按四工号原分母分配')
    item.refresh_from_db();return item


@transaction.atomic
def material_adjustment(item,actor):
    kind=0 if item.SOURCE_TABLE=='StuffIn' else 1
    table,field,prefix=('StuffIn','StuffID','SM') if kind==0 else ('ArticleIn','ArticleID','AM')
    series=raw(item,'SheetSeries');retired=[];created=[]
    for name in ['MaterialPriceAdjustDetail','MaterialPriceAdjust']:
        targets=matching(rows(name,'erp_base'),InSheetSeries=series)
        if name=='MaterialPriceAdjust':targets=targets.filter(old_sheet_kind=kind)
        for target in targets:
            retired.append({'entity':target._meta.label,'id':target.pk,'before':snapshot(target)})
            retain(target,actor,'MaterialPriceAdjustUpdate重新计算，原调整单留档')
    details=[]
    for line in matching(rows(table+'Detail','erp_warehouse'),SheetSeries=series).order_by('pk'):
        for head in matching(rows(table,'erp_warehouse'),SheetSeries=series).order_by('pk'):
            if kind==1 and raw(head,'WareHouseID') not in ['18','19']:continue
            old=previous_material_price(series,raw(head,'SheetDate'),raw(head,'SupplierID'),raw(line,field),kind)
            price=raw(line,'Price')
            if price is None or old in [None,0] or price<=old:continue
            new_series=prefix+series[-8:]
            details.append({'SheetSeries':new_series,'DetailNo':None if raw(line,'DetailNo') is None else new_series+raw(line,'DetailNo')[len(series.rstrip(' ')):],
                'SupplierID':raw(head,'SupplierID'),field:raw(line,field),'LastUnitPrice':old,'CurrentUnitPrice':price,
                'InDetailNo':raw(line,'DetailNo'),'InSheetSeries':series,'ExecutionDate':raw(head,'SheetDate')})
    if details:
        model=rows('MaterialPriceAdjust','erp_base').model
        for head in matching(rows(table,'erp_warehouse'),SheetSeries=series).order_by('pk'):
            values={f:raw(head,f) for f in ['SheetDate','WareHouseID','Creater','CreateDate','Modifyer','ModifyDate']}
            values.update(SheetSeries=prefix+series[-8:],SheetNo=None if raw(head,'SheetNo') is None else prefix+raw(head,'SheetNo')[-8:],
                SheetKind=kind,InSheetNo=raw(head,'SheetNo'),InSheetSeries=series)
            created.append(write(model,dict(store_value(model(),f,v) for f,v in values.items()),actor=actor))
        model=rows('MaterialPriceAdjustDetail','erp_base').model
        for values in details:created.append(write(model,dict(store_value(model(),f,v) for f,v in values.items()),actor=actor))
    save_effect(item,'material_price_adjustment',{'retained':retired,'created':[{'entity':r._meta.label,'id':r.pk} for r in created]},actor,'材料调价：只生成实际上涨且有前次价的明细，全部旧版本留档')
    return item


@transaction.atomic
def order_prices(item,actor,feel_only=False,all_orders=False):
    series=raw(item,'SheetSeries');price=unit=customer=product=None
    sources=[];before=[]
    charges=rows('OrderAtte','erp_sales') if all_orders else matching(rows('OrderAtte','erp_sales'),SheetSeries=series)
    charges=charges.order_by('pk')
    if feel_only:charges=charges.filter(old_atte_value__contains='手感')
    else:charges=matching(charges,FieldType='05')
    loops=[]
    for charge in charges:
        series=raw(charge,'SheetSeries')
        pairs=[(h,c) for h in matching(rows('OrderMain','erp_sales'),SheetSeries=series).order_by('pk')
               for c in matching(rows('OrderColor','erp_sales'),SheetSeries=series).order_by('pk')]
        loops.extend((charge,h,c) for h,c in ((pairs[-1:] or [(None,None)]) if feel_only else pairs))
    for charge,head,color in loops:
        series=raw(charge,'SheetSeries');value=raw(charge,'AtteValue')
        if head is not None:customer=raw(head,'CustomerID');product=raw(color,'ProdID')
        basics=[c for h in matching(rows('CusBasicsPrice','erp_sales'),CustomerID=customer).order_by('pk')
                for c in matching(rows('CusExtraCharge','erp_sales'),SheetSeries=raw(h,'SheetSeries'),PayService=value).order_by('pk')]
        updates=[]
        if basics:
            candidate=basics[-1] if feel_only else basics[0]
            price,unit=raw(candidate,'Price'),raw(candidate,'PriceUnit');sources.extend(r.pk for r in basics)
            updates.append((matching(rows('OrderAtte','erp_sales'),SheetSeries=series,AtteValue=value),price,unit))
        else:
            offers=list(matching(rows('QuoteItemPrice','erp_sales'),Item=value).order_by('pk'))
            specific=[r for r in offers if equal(raw(r,'CustomerID'),customer) and equal(raw(r,'ProdID') or '',product)]
            generic=[r for r in offers if equal(raw(r,'CustomerID'),customer) and equal(raw(r,'ProdID') or '','')]
            public=[r for r in offers if equal(raw(r,'CustomerID') or '','') and equal(raw(r,'ProdID') or '','')]
            targets=matching(rows('OrderAtte','erp_sales'),SheetSeries=series,AtteValue=value,FieldType='05')
            if specific:
                price,unit=raw(specific[-1],'Price'),raw(specific[-1],'Unit');sources.extend(r.pk for r in specific)
                updates.append((targets,price,unit))
            selected=generic or public
            if selected:price,unit=raw(selected[-1],'Price'),raw(selected[-1],'Unit');sources.extend(r.pk for r in selected)
            # 原无匹配SELECT保留上一次循环变量，仍UPDATE；不擅自补0。
            updates.append((targets,price,unit))
        for targets,p,u in updates:
            before.extend({'entity':r._meta.label,'id':r.pk,'before':snapshot(r)} for r in targets)
            change(targets,{'Price':p,'PriceUnit':0 if u=='' else u},actor)
        values=[raw(r,'Price') or Decimal(0) for r in matching(rows('OrderAtte','erp_sales'),SheetSeries=series,FieldType='05')
                if raw(r,'AtteValue') is not None and not sql_like(raw(r,'AtteValue'),'%手感%')]
        result=total(values) if unit is not None and str(unit).rstrip(' ')!='4' else None
        targets=matching(rows('OrderColor','erp_sales'),SheetSeries=series)
        before.extend({'entity':r._meta.label,'id':r.pk,'before':snapshot(r)} for r in targets)
        change(targets,{'ProcessPrice':result},actor)
    save_effect(item,'order_price_refresh',{'before':before,'candidate_ids':sources,'feel_only':feel_only},actor,'原收费价格回写，保留独立IF覆盖和循环变量语义')
    item.refresh_from_db();return item


@transaction.atomic
def recipe_costs(actor):
    from .source_static_lookup import execute
    from .source_phase2_reports import bind
    result=[]
    for head in rows('DyeRecipe','erp_sampling').order_by('pk'):
        series=raw(head,'SheetSeries')
        values=execute(bind('''SELECT SUM(c.Amount) AS Amount FROM dye.DyeRecipe a
            JOIN dye.DyeRecipePhase b ON b.SheetSeries=a.SheetSeries
            JOIN dye.DyeRecipeDetail c ON c.SheetSeries=b.SheetSeries AND c.PhaseNo=b.PhaseNo
            WHERE a.SheetSeries=@series''',{'series':series}),rows)
        targets=matching(rows('DyeRecipe','erp_sampling'),SheetSeries=series)
        before=[{'entity':r._meta.label,'id':r.pk,'before':snapshot(r)} for r in targets]
        change(targets,{'Cost':values[0]['amount']},actor)
        save_effect(head,'recipe_cost_refresh',{'before':before},actor,'Sp_DyeRecipe全部配方成本重算，重复连接照计')
        result.append({'id':head.pk,'SheetSeries':series,'Cost':values[0]['amount']})
    return {'report':'Sp_DyeRecipe','rows':result}


@transaction.atomic
def quote_adjustment(item,actor,audited):
    from datetime import datetime
    from django.utils import timezone
    before=[]
    for detail in matching(rows('PriceAdjustDetail','erp_sales'),SheetSeries=raw(item,'SheetSeries')).order_by('pk'):
        heads=list(matching(rows('PriceAdjust','erp_sales'),SheetSeries=raw(detail,'SheetSeries')).order_by('pk'))
        for head in heads or [None]:
            values={'AdjustPrice':raw(detail,'AdjustPrice'),'StartDate':None if head is None else raw(head,'StartDate'),
                'DateType':None if head is None else raw(head,'DateType')} if audited else {
                'AdjustPrice':0,'StartDate':timezone.make_aware(datetime(1900,1,1)),'DateType':0}
            targets=matching(rows('QuoteDetail','erp_sales'),DetailNo=raw(detail,'QuoteDetailNo'))
            before.extend({'entity':r._meta.label,'id':r.pk,'before':snapshot(r)} for r in targets)
            change(targets,values,actor)
    save_effect(item,'quote_adjustment',{'before':before,'audited':audited},actor,'SP_UpdateQuotePrice原报价调价/反调价')
    return item


@transaction.atomic
def sample_book(item,actor,sheet_no,detail_no,kind):
    from django.utils import timezone
    from .business import persist,record
    table={1:'SampleIn',2:'SampleOut'}[kind]
    ledger=matching(rows('SampleStockBook','erp_sampling'),SheetNo=sheet_no,DetailNo=detail_no)
    if kind==1:ledger=ledger.filter(old_book_kind=1)
    existed=ledger.exists();before=[];created=[];retained=[]
    source=list(matching(rows(table+'Detail','erp_sampling'),DetailNo=detail_no).order_by('pk'))
    if not source:
        for target in ledger:
            retained.append({'entity':target._meta.label,'id':target.pk,'before':snapshot(target)})
            retain(target,actor,'Sp_UpdateSampleStockBook原删除流水，原行留档')
    else:
        for line in source:
            heads=list(matching(rows(table,'erp_sampling'),SheetSeries=raw(line,'SheetSeries')).order_by('pk'))
            for head in heads or [None]:
                values={f:None if head is None else raw(head,f) for f in ['BusinessUnitID','SalerID','SheetNo','Remarks']}
                values.update(BookDate=timezone.localtime(),BookKind=kind,DetailNo=detail_no,
                    CustomerID=None if head is None else raw(head,'FactID' if kind==1 else 'CustomerID'),
                    SampleInOutKindID=None if head is None else raw(head,table+'KindID'),
                    SampleKindID=raw(line,'SampleKindID'),StorageUnitIDs=raw(line,'StorageUnitID'),FabricID=raw(line,'FabricID'),
                    InQty=raw(line,'Qty') if kind==1 else 0,OutQty=raw(line,'Qty') if kind==2 else 0,Price=raw(line,'Price'))
        if existed:
            targets=matching(rows('SampleStockBook','erp_sampling'),SheetNo=values['SheetNo'],DetailNo=detail_no).filter(old_book_kind=kind)
            before=[{'entity':r._meta.label,'id':r.pk,'before':snapshot(r)} for r in targets]
            change(targets,values,actor)
        else:
            model=ledger.model
            target=write(model,dict(store_value(model(),f,v) for f,v in values.items()),actor=actor,apply_effects=False)
            created.append({'entity':target._meta.label,'id':target.pk})
    save_effect(item,'sample_book_refresh',{'before':before,'retained':retained,'created':created,
        'source_ids':[r.pk for r in source],'kind':kind},actor,'小样收发原流水同步；负数及重复原行保留')
    return item
