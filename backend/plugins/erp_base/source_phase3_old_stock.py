"""保留旧版本库存入口；缺失旧列按最新原列明确对应，差异记录在办理日志。"""
from django.db import transaction
from .source_phase3_operations import SPECS,source,model,query,create,change,retire,result
from .source_stock_services import raw
from .source_business_updates import matching
from .business import record,snapshot

GRAY_KINDS={'GrayIn':[11,12,13,14,15,16,19],'GrayOut':[21,22,23,24,25,29],
    'GrayStockAdjust':[33,34],'GrayStockAllot':[31,32]}


@transaction.atomic
def gray(table,series,action,actor):
    heads=list(matching(source(table),SheetSeries=series).order_by('pk'))
    number=None if not heads else raw(heads[-1],'SheetNo')
    targets=matching(source('GrayStockBook'),SheetNo=number).filter(old_book_kind__in=GRAY_KINDS[table]);retained=[];changed=[]
    if action==2:
        if table=='GrayStockAdjust':targets=targets.filter(old_book_kind=33)
        if number not in [None,'']:retained=retire(targets,actor,'Sp_UpdateGrayStockBook_old反审核，原流水留档')
        return result('Sp_UpdateGrayStockBook_old',[],retained)
    approved=[h for h in heads if raw(h,'RightStatus')==10]
    if action==1 and approved and (raw(approved[-1],'SheetNo') or '')=='':
        return result('Sp_UpdateGrayStockBook_old',[],retire(targets,actor,'旧审核入口空单号分支移除原流水'))
    if table=='GrayStockAllot':return result('Sp_UpdateGrayStockBook_old',[])
    values=query(SPECS['405']['queries'][table],{'sheetseries':series})
    fields={k.lower():k for k in model('GrayStockBook').SOURCE_FIELDS}
    for value in values:
        payload={fields[k]:v for k,v in value.items()}
        if table in ['GrayIn','GrayStockAdjust']:
            payload.update(OutRolls=0,OutPacks=0,OutLengthQty=0,OutWeightQty=0)
        else:payload.update(InRolls=0,InPacks=0,InLengthQty=0,InWeightQty=0)
        selected=matching(source('GrayStockBook'),SheetNo=value['sheetno'],DetailNo=value['detailno']).filter(old_book_kind__in=GRAY_KINDS[table])
        exists=matching(source('GrayStockBook'),SheetNo=value['sheetno'],ReceSheetNo=value['recesheetno']).filter(old_book_kind__in=GRAY_KINDS[table]).exists() if table=='GrayOut' else selected.exists()
        if exists:change(selected,payload,actor);changed.extend(selected)
        else:changed.append(create('GrayStockBook',payload,actor))
        if table=='GrayOut':
            total=query('SELECT SUM(WeightQty) AS weight FROM dye.GrayOutDetail WHERE JobSheetNo=@j',{'j':value['jobsheetno']})[0]['weight']
            change(matching(source('JobSheet'),SheetNo=value['jobsheetno']),{'PreVatQty':total,'SumProcessWeightQty':total},actor)
    selected=query(SPECS['405']['cleanup'][table],{'sheetseries':series}) if action==0 else []
    retained.extend(retire(source('GrayStockBook').filter(old_book_no__in=[r['bookno'] for r in selected]),actor,'旧库存原清理条件命中，流水留档'))
    if not values:
        kinds=list(range(21,30)) if table=='GrayOut' and action==0 else GRAY_KINDS[table]
        retained.extend(retire(matching(source('GrayStockBook'),SheetNo=series).filter(old_book_kind__in=kinds),actor,'旧过程空来源流水留档'))
    return result('Sp_UpdateGrayStockBook_old',changed,retained)


@transaction.atomic
def semi(number,kind,actor):
    table,field=('SemiIn','ReceSheetNo') if kind==1 else ('SemiOut','AssignedNo')
    lines=list(matching(source(table+'Detail'),**{field:number}).order_by('pk'))
    target=matching(source('SemiStockBook'),SheetNo=number).filter(old_book_kind=kind)
    if not lines:return result('UpdateSemiStock',[],retire(target,actor,'旧版半成品来源删除，原流水留档'))
    joined=[(line,head) for line in lines for head in list(matching(source(table),SheetSeries=raw(line,'SheetSeries')).order_by('pk')) or [None]]
    line,head=joined[-1]
    names=['CustomerID','SalerGroupID','SalerID','SemiKindID'];values={f:None if head is None else raw(head,f) for f in names}
    values.update(SheetNo=number,BookKind=kind,WareHouseID='A',StorageUnitIDs=raw(line,'StorageUnitID'),Spec=raw(line,'Spec'),
        LotNo=raw(line,'NewLotNo' if kind==1 else 'LotNo'),CheckNo=raw(line,'CheckNo' if kind==1 else 'ReceSheetNo'),
        JobSheetNo=raw(line,'JobSheetNo'),BookDate=None if head is None else raw(head,'CreateDate'),
        ProdID=raw(line,'FabricID'),Remarks=raw(line,'Remarks'))
    # 最新SemiStockBook已没有InQty/OutQty、StockUnit和FabricID；原数量按单据单位映射，原值写入审计。
    unit=None if head is None else raw(head,'StockUnit');quantity=raw(line,'InQty' if kind==1 else 'OutQty')
    prefix='In' if kind==1 else 'Out';values[prefix+'Rolls']=raw(line,prefix+'Rolls')
    values[prefix+('LengthQty' if str(unit)=='2' else 'WeightQty')]=quantity
    if kind==2 and values['SemiKindID'] is None:values['SemiKindID']=''
    if target.exists():change(target,values,actor);changed=list(target)
    else:
        if values['Remarks'] is not None:values['Remarks']+='入库' if kind==1 else '出库'
        changed=[create('SemiStockBook',values,actor)]
    for item in changed:record(item,'phase3_old_semi_mapping',snapshot(item),actor,
        'UpdateSemiStock旧列映射：StockUnit='+str(unit)+'；原数量='+str(quantity)+'；FabricID='+str(raw(line,'FabricID'))+
        '；原无序标量连接候选='+str([(l.pk,None if h is None else h.pk) for l,h in joined]))
    return result('UpdateSemiStock',changed)
