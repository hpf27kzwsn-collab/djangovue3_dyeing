"""旧21/25/26类外协回料；原选择余额与本次实际收回独立。"""
from plugins.erp_base.source_provenance import reference as source_reference
from django.db import transaction
from django.db.models import Value
from django.db.models.functions import Coalesce,Upper,RTrim
from .business import locked
from .source_stock_services import raw
from .source_quality_reports import rows,key,total
from .source_business_updates import matching
from .source_continuation import copy_new,origin,save_effect
from .source_calculations import field_values,store_value
from .source_execution_state import require_available


def joined_receipts(table,kind,column,value,query):
    source=query(table+'Detail','erp_warehouse')
    if value is None:return []  # 原ISNULL(入库引用,'')=出库NULL不匹配。
    source=source.alias(link=Upper(RTrim(Coalesce(source.model.SOURCE_FIELDS[column],Value(''))))).filter(link=key(value))
    result=[]
    for row in source.order_by('pk'):
        for head in matching(query(table,'erp_warehouse'),SheetSeries=raw(row,'SheetSeries')).filter(old_sheet_kind=kind).order_by('pk'):
            result.append({'entity':row._meta.label,'record_id':row.pk,'source': source_reference(row),'header_id':head.pk,
                'SheetKind':kind,**{name:raw(row,name) for name in ['Rolls','WeightQty','Packs']}})
    return result


def receipt_options(item,query=rows):
    gray=item.SOURCE_TABLE=='GrayOutDetail'
    if gray:
        semi=joined_receipts('SemiIn',25,'JobSheetNo',raw(item,'JobSheetNo'),query)
        returned=joined_receipts('GrayIn',21,'CustJobNo',raw(item,'JobSheetNo'),query)
    else:
        semi=joined_receipts('SemiIn',26,'GrayOutDetailNo',raw(item,'DetailNo'),query);returned=[]
    zero=lambda value:0 if value is None else value
    summed=lambda data,name:zero(total([row[name] for row in data]))
    weight=zero(raw(item,'WeightQty'))-summed(semi,'WeightQty')-summed(returned,'WeightQty')
    parents=list(matching(query('GrayOut' if gray else 'SemiOut','erp_warehouse'),SheetSeries=raw(item,'SheetSeries')).order_by('pk'))
    result=[]
    for parent in parents or [None]:
        variants=[('gray',21),('semi',25)] if gray else [('semi',26)]
        for destination,kind in variants:
            original_rolls=zero(raw(item,'WeightQty'))-summed(semi,'Rolls')-summed(returned,'WeightQty' if destination=='gray' else 'Rolls') if gray else weight
            result.append({'destination':destination,'receipt_kind':kind,'header_id':None if parent is None else parent.pk,
                'dispatch_kind':None if parent is None else raw(parent,'SheetKind'),
                'original_rolls_formula':original_rolls,'remaining_weight':weight,
                'remaining_packs':zero(raw(item,'Packs'))-summed(semi,'Packs')-summed(returned,'Packs') if gray else None,
                'old_selection_available':parent is not None and raw(parent,'SheetKind')==(30 if gray else 32) and weight>0})
    return {'report':'外协21/25/26类收回原余额','rows':result,'result_rows':semi+returned,
        'notes':['原查询只显示正余额及30/32类发出；本报告保留全部原结果，明确列出原选择可见性，不删除负量或零量。',
            '原Rolls/LastRolls公式含重量，照原式展示；实际回料填写真实重量、长度、粒数，不以此混量公式代填。',
            '相同原引用及重复表头按原SQL全部展开；源NULL不匹配，源空串按原ISNULL连接。']}


@transaction.atomic
def receive_material(item,actor,destination,weight,length,rolls,packs,warehouse,unit,customer,supplier,at,reason,receipt_number=None):
    from . import source_services as services
    item=locked(item);require_available(item)
    gray=item.SOURCE_TABLE=='GrayOutDetail'
    table,entry,kind=('GrayIn','GrayInWork',21) if destination=='gray' else ('SemiIn','GrayOutToSemiIn',25) if gray else ('SemiIn','SemiInBack',26)
    head_model,line_model=rows(table,'erp_warehouse').model,rows(table+'Detail','erp_warehouse').model
    head=services.write(head_model,{'_entry':entry,'old_sheet_kind':kind,'old_sheet_date':at,'old_ware_house_id':warehouse,
        'old_stock_unit':unit,'old_customer_id':customer,'old_supplier_id':supplier,'old_remarks':reason},actor=actor,apply_effects=False)
    values=copy_new(item,line_model,['SheetSeries','ReceSheetNo','Rolls','WeightQty','LengthQty','Packs','Amount'])
    values['source_parent_1']=head
    if receipt_number is not None:values['old_rece_sheet_no']=receipt_number
    if destination=='gray':values['old_cust_job_no']=raw(item,'JobSheetNo')
    elif gray:values['old_prod_id']=raw(item,'GrayID')
    else:values['old_gray_out_detail_no']=raw(item,'DetailNo')
    values.update(store_value(line_model(),name,value) for name,value in [('WeightQty',weight),('LengthQty',length),('Rolls',rolls),('Packs',packs)])
    values.update(field_values(line_model(**values)))
    line=services.write(line_model,values,actor=actor,apply_effects=False)
    save_effect(head,'outwork_receipt_origin',{**origin(item),'line_id':line.pk,'at':at,'reason':reason,'receipt_kind':kind},actor,reason)
    services.finish([head],actor)
    from .source_outwork_followup import movement
    movement(item,head,actor,'material_receipt',at,reason)
    return head


@transaction.atomic
def return_to_factory(item,actor,weight,length,rolls,packs,warehouse,unit,customer,factory,sheet_kind,at,reason,issue_number=None):
    from . import source_services as services
    item=locked(item);require_available(item)
    gray=item.SOURCE_TABLE=='GrayInDetail'
    table='GrayOut' if gray else 'SemiOut'
    head_model,line_model=rows(table,'erp_warehouse').model,rows(table+'Detail','erp_warehouse').model
    fields={'_entry':table+'Work','old_sheet_kind':sheet_kind,'old_sheet_date':at,'old_ware_house_id':warehouse,
        'old_stock_unit':unit,'old_customer_id':customer,'old_remarks':reason}
    if gray:fields['old_fact_id']=factory
    head=services.write(head_model,fields,actor=actor,apply_effects=False)
    values=copy_new(item,line_model,['SheetSeries','AssignedNo','DetailNo','Rolls','WeightQty','LengthQty','Packs','Amount'])
    values['source_parent_1']=head
    if issue_number is not None:values['old_assigned_no' if gray else 'old_detail_no']=issue_number
    values.update(store_value(line_model(),name,value) for name,value in [('WeightQty',weight),('LengthQty',length),('Rolls',rolls),('Packs',packs)])
    values.update(field_values(line_model(**values)))
    line=services.write(line_model,values,actor=actor,apply_effects=False)
    save_effect(head,'outwork_return_origin',{**origin(item),'line_id':line.pk,'factory':factory,'at':at,'reason':reason},actor,reason)
    services.finish([head],actor)
    from .source_outwork_followup import movement
    movement(item,head,actor,'material_factory_return',at,reason)
    return head
