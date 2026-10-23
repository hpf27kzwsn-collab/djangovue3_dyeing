"""装车及工卡出仓登记采用明确原行；登记不重复产生库存收发。"""
from django.db import transaction
from .business import locked
from .source_phase3_operations import model
from .source_stock_services import raw
from .source_continuation import copy_new,origin,save_effect
from .source_execution_state import require_available


@transaction.atomic
def recipe_references(item,actor,at,reason,**selected):
    from . import source_services as services
    from .source_continuation import view_effects
    item=locked(item);require_available(item);values={}
    origins=dict(view_effects(item).get('recipe_reference_origin',{}).get('selected',{}))
    for key,(target,source) in {'color':('ColorNo','ColorNo'),'original':('OriRecipeSheetNo','SheetNo'),'standard':('StandRecipeNo','SheetNo')}.items():
        if key not in selected:continue
        row=selected[key]
        if row is not None:row=locked(row);require_available(row)
        values[item.SOURCE_FIELDS[target]]=None if row is None else raw(row,source)
        origins[key]=None if row is None else origin(row)
    item=services.write(type(item),values,item,actor)
    save_effect(item,'recipe_reference_origin',{'selected':origins,'at':at,'reason':reason},actor,reason)
    return item


@transaction.atomic
def load_lines(head,lines,actor,at,reason):
    from . import source_services as services
    head=locked(head);require_available(head);created=[]
    for original in lines:
        original=locked(original);require_available(original)
        values=copy_new(original,model('ProdLoadingDetail'),['SheetSeries','DetailNo','LineNumber'])
        values.update(_entry='ProdLoadingDetail',source_parent_1=head,old_out_detail_no=raw(original,'DetailNo'))
        line=services.write(model('ProdLoadingDetail'),values,actor=actor,apply_effects=False)
        save_effect(line,'loading_source',{'source':origin(original),'loading':origin(head),'at':at,'reason':reason},actor,reason)
        created.append(line.pk)
    services.finish([head],actor)
    return {'loading_id':head.pk,'created_line_ids':created}


@transaction.atomic
def out_of_job_warehouse(incoming,actor,rolls,weight,at,reason):
    from . import source_services as services
    from .source_calculations import store_value
    incoming=locked(incoming);require_available(incoming)
    values=copy_new(incoming,model('JobOutWareEdit'),['SheetSeries','SheetNo','SheetDate','SheetStatus','RightStatus','Approver','ApproveDate'])
    values.update(_entry='JobOutWareEdit',old_in_ware_sheet_no=raw(incoming,'SheetNo'),old_sheet_date=at,old_remarks=reason)
    values.update([store_value(model('JobOutWareEdit')(),'Rolls',rolls),store_value(model('JobOutWareEdit')(),'WeightQty',weight)])
    outgoing=services.write(model('JobOutWareEdit'),values,actor=actor)
    save_effect(outgoing,'job_warehouse_source',{'source':origin(incoming),'at':at,'reason':reason},actor,reason)
    return outgoing
