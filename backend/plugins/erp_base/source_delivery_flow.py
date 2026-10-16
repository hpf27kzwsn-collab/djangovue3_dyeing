"""外协退回、加工厂质量处置、包装入库及实际交付的明确单据接续。"""
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import transaction
from .business import locked
from .source_calculations import store_value, field_values
from .source_stock_services import raw
from .source_continuation import save_effect, origin, copy_new as copy_values
from .source_business_updates import matching
from .source_execution_state import require_available


def rows(name):
    return apps.get_model('erp_warehouse.SourceDye' + name).objects.all()


def amounts(model, weight, length, rolls):
    return dict(store_value(model(), key, value) for key, value in [('WeightQty', weight), ('LengthQty', length), ('Rolls', rolls)])


@transaction.atomic
def return_material(item, actor, weight, length, rolls, warehouse, unit, sheet_kind, at, reason, customer):
    from . import source_services as services
    item = locked(item)
    require_available(item)
    gray = item.SOURCE_TABLE == 'GrayOutDetail'
    table, entry = ('GrayIn', 'GrayInWork') if gray else ('SemiIn', 'SemiInBack')
    head_model, detail_model = rows(table).model, rows(table+'Detail').model
    head = services.write(head_model, {'_entry': entry, 'old_sheet_date': at, 'old_sheet_kind': sheet_kind,
        'old_ware_house_id': warehouse, 'old_stock_unit': unit, 'old_remarks': reason,
        'old_customer_id': customer}, actor=actor, apply_effects=False)
    values = copy_values(item, detail_model, ['SheetSeries','ReceSheetNo','Rolls','WeightQty','LengthQty','Amount'])
    values.update(source_parent_1=head, **amounts(detail_model, weight, length, rolls))
    values.update(field_values(detail_model(**values)))
    detail = services.write(detail_model, values, actor=actor, apply_effects=False)
    save_effect(head, 'material_return_origin', {**origin(item), 'detail_id': detail.pk, 'at': at, 'reason': reason}, actor, reason)
    services.finish([head], actor)
    from .source_outwork_followup import movement
    movement(item,head,actor,'material_return',at,reason)
    return head


@transaction.atomic
def factory_quality(item, actor, factory, result, inspection, at, reason):
    item = locked(item)
    require_available(item)
    inspection = None if inspection is None else locked(inspection)
    value = {'factory': factory, 'result': result, 'at': at, 'reason': reason,
        'receipt': origin(item), 'inspection': None if inspection is None else origin(inspection)}
    save_effect(item, 'factory_quality', value, actor, reason)
    from .source_outwork_followup import movement
    movement(item,item,actor,'factory_quality',at,reason)
    return item


@transaction.atomic
def receive_package(item, actor, weight, length, rolls, warehouse, unit, sheet_kind, at, reason):
    from . import source_services as services
    item = locked(item)
    require_available(item)
    head_model, line_model = rows('ProdIn').model, rows('ProdInRecord').model
    values = copy_values(item, head_model, ['SheetSeries','SheetNo','SheetDate','SheetKind','StockUnit','Rolls','WeightQty','LengthQty','NetKg','Price','Amount','Total'])
    values.update(_entry='ProdIn', old_sheet_date=at, old_sheet_kind=sheet_kind, old_stock_unit=unit,
        old_ware_house_id=warehouse, old_remarks=reason, **amounts(head_model, weight, length, rolls))
    head = services.write(head_model, values, actor=actor, apply_effects=False)
    values = copy_values(item, line_model, ['SheetSeries','RollNo','BarCode','WeightQty','LengthQty','NetKg','InRolls'])
    values.update(source_parent_1=head, old_prod_bar_code=raw(item,'BarCode'))
    values.update(store_value(line_model(),key,value) for key,value in [
        ('WeightQty',weight),('LengthQty',length),('InRolls',rolls)])
    line = services.write(line_model, values, actor=actor, apply_effects=False)
    save_effect(head, 'package_receipt_origin', {**origin(item), 'record_id': line.pk, 'at': at, 'reason': reason,
        'requested_amounts':{'weight':weight,'length':length,'rolls':rolls}}, actor, reason)
    services.finish([head], actor)
    return head


@transaction.atomic
def dispatch_product(item, actor, weight, length, rolls, warehouse, sheet_kind, at, purpose, receiver, price, records, reason):
    from . import source_services as services
    item = locked(item)
    require_available(item)
    head_model, line_model = rows('ProdOut').model, rows('ProdOutDetail').model
    # 已选入库细码的原归属是实际交付关系；同码其他记录不自动带入。
    for selected in records:
        if selected.source_parent_1_id not in [None,item.pk] or not matching(
                rows('ProdInRecord').filter(pk=selected.pk), SheetSeries=item.old_sheet_series).exists():
            raise ValidationError({'records': '选择的入库细码须属于本次来源入库单；异来源请分别办理。'})
    values = copy_values(item, head_model, ['SheetSeries','SheetNo','SheetDate','SheetKind','WareHouseID','FactID'])
    values.update(_entry='ProdOut',old_sheet_date=at,old_sheet_kind=sheet_kind,old_ware_house_id=warehouse,old_remarks=reason)
    values['old_fact_id' if purpose=='factory_return' else 'old_customer_id'] = receiver
    head = services.write(head_model, values, actor=actor, apply_effects=False)
    values = copy_values(item, line_model, ['SheetSeries','DetailNo','Rolls','WeightQty','LengthQty','Price','Amount','Total'])
    values.update(source_parent_1=head, old_in_sheet_no=raw(item,'SheetNo'),
        **amounts(line_model,weight,length,rolls))
    values.update([store_value(line_model(),'Price',price)])
    values.update(field_values(line_model(**values)))
    line = services.write(line_model, values, actor=actor, apply_effects=False)
    adopted = []
    model = rows('ProdOutRecord').model
    for selected in {r.pk:r for r in records}.values():
        selected = locked(selected)
        data = copy_values(selected, model, ['SheetSeries','DetailNo','OutDetailNo'])
        data.update(source_parent_1=line, old_rolls=raw(selected,'InRolls'))
        target = services.write(model, data, actor=actor, apply_effects=False)
        adopted.append({'source': origin(selected), 'target_id': target.pk})
    save_effect(head,'product_dispatch_origin',{**origin(item),'purpose':purpose,'receiver':receiver,
        'at':at,'reason':reason,'line_id':line.pk,'records':adopted,'adopted_price':raw(line,'Price'),
        'requested_price':price,'original_price':raw(item,'Price')},actor,reason)
    services.finish([head],actor)
    from .source_outwork_followup import movement
    movement(item,head,actor,purpose,at,reason)
    return head


@transaction.atomic
def confirm_delivery(item, actor, result, receiver, at, reason):
    item = locked(item)
    require_available(item)
    save_effect(item,'delivery_confirmation',{'result':result,'receiver':receiver,'at':at,'reason':reason,
        'document':origin(item)},actor,reason)
    return item


@transaction.atomic
def receive_delivery_return(item, actor, weight, length, rolls, warehouse, unit, sheet_kind, at, reason, customer):
    from . import source_services as services
    item = locked(item)
    require_available(item)
    model = rows('ProdIn').model
    values = copy_values(item,model,['SheetSeries','SheetNo','SheetDate','SheetKind','Rolls','WeightQty','LengthQty','Amount','Total'])
    values.update(_entry='ProdIn',old_sheet_date=at,old_sheet_kind=sheet_kind,old_stock_unit=unit,
        old_ware_house_id=warehouse,old_remarks=reason,old_prod_out_sheet_series=raw(item,'SheetSeries'),old_customer_id=customer,
        **amounts(model,weight,length,rolls))
    target=services.write(model,values,actor=actor,apply_effects=False)
    save_effect(target,'product_dispatch_origin',{**origin(item),'purpose':'delivery_return','at':at,'reason':reason},actor,reason)
    services.finish([target],actor)
    from .source_outwork_followup import movement
    movement(item,target,actor,'delivery_return',at,reason)
    return target
