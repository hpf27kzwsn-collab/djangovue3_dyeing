"""按具体旧入口翻译的公式；不动态解析、执行旧表达式或SQL。"""
from decimal import Decimal, localcontext
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db.models import Sum, Count
from .source_calculations import decimal, product, zero, store_value, packaging_values
from .source_calculation_entries import ENTRY_METHODS


def divide(numerator, denominator, name):
    if denominator == 0:
        raise ValidationError({name: '本入口公式的除数为零，不能计算；原值仍可保存。'})
    return None if numerator is None or denominator is None else decimal(numerator) / decimal(denominator)


def difference(left, right):
    return None if left is None or right is None else decimal(left) - decimal(right)


def source_parent(item):
    if item.source_parent_1_id is None:
        raise ValidationError({'source_parent_1': '本入口公式需要明确的原表头或阶段关联；原码仍可保存。'})
    return item.source_parent_1


def child_sum(item, label, field):
    child = apps.get_model(label)
    return child.objects.filter(source_parent_1=item).aggregate(value=Sum(child.SOURCE_FIELDS[field]))['value']


def nested_details(item, label):
    return apps.get_model(label).objects.filter(source_parent_1__source_parent_1=item)


def subtotal(queryset, field):
    return queryset.aggregate(value=Sum(queryset.model.SOURCE_FIELDS[field]))['value']


def recipe_values(item, entry):
    amount = product(item.old_price, item.old_dosage)
    if entry in ['BulkDyeRecipePhaseDetail', 'StandardDyeRecipePhaseDetail']:
        ratio = None if item.old_recipe_unit == 0 else source_parent(item).old_bath_ratio
        factor = Decimal('10') if ratio is None else decimal(ratio)
        amount = product(amount, factor)
    elif entry == 'FinishDyeRecipePhaseDetail':
        ratio = None if item.old_stuff_type == 'S' else source_parent(item).old_bath_ratio
        factor = Decimal('10') if ratio is None else decimal(ratio)
        amount = product(amount, factor)
    return {'Amount': amount}


def weight_phase_values(item, entry):
    head = source_parent(item)
    if entry == 'SelfStuffWeightPhaseDetail':
        return {'BathRatio': divide(item.old_water_qty, head.old_cloth_qty_kg, 'old_cloth_qty_kg')}
    if entry == 'NormalStuffWeightPhaseDetail_Wash':
        return {'WaterQty': head.old_rate,
                'StepIndex': (item.old_program_id or '') + '-3'}
    machine = '' if head.old_machine_id is None else str(head.old_machine_id)
    values = {'BathRatio': head.old_rate,
              'StepIndex': machine + '-' + (item.old_program_id or '')}
    if entry == 'AddStuffWeightPhaseDetail':
        values['WaterQty'] = head.old_rate
    return values


def weight_detail_values(item, entry):
    values = {}
    dosage = decimal(item.old_dosage)
    if entry in ['AfterNormalStuffWeightPhaseDetail', 'NormalStuffWeightPhaseDetail', 'ReworkStuffWeightPhaseDetail']:
        original = zero(item.old_oir_dosage)
        adjustment = zero(item.old_adjust_dosage)
        dosage = original + original * adjustment / Decimal('100') if adjustment != 0 else original
        values['Dosage'] = dosage
    if entry == 'AddStuffWeightPhaseDetail':
        values['NeedQty'] = Decimal('0')
    needed = values.get('NeedQty', item.old_need_qty)
    if entry in ['ProcessStuffWeightPhaseDetail', 'WashProcessStuffWeightPhaseDetail']:
        head = source_parent(source_parent(item))
        divisor = Decimal('1000') if entry == 'ProcessStuffWeightPhaseDetail' else Decimal('100')
        values['NeedQty'] = product(head.old_rate, dosage)
        if values['NeedQty'] is not None:
            values['NeedQty'] /= divisor
        amount = product(product(product(item.old_price, dosage), head.old_cloth_net_kg), Decimal('0.01'))
        values['Money'] = amount
        if entry == 'ProcessStuffWeightPhaseDetail':
            values['NeedMoney'] = unit_money(item.old_price, values['NeedQty'], item.old_weight_unit)
        else:
            values['NeedMoney'] = product(product(item.old_price, dosage), values['NeedQty'])
        return values
    if entry == 'SelfStuffWeightPhaseDetail':
        phase = source_parent(item)
        if item.old_recipe_unit == 1:
            amount = product(product(item.old_price, dosage), phase.old_water_qty)
            values['Money'] = None if amount is None else amount / Decimal('1000')
        else:
            head = source_parent(phase)
            values['Money'] = product(product(product(item.old_price, dosage), head.old_cloth_net_kg), Decimal('0.01'))
        values['NeedMoney'] = product(product(item.old_price, dosage), item.old_need_qty)
        values['RealMoney'] = product(product(item.old_price, dosage), item.old_real_qty)
        return values
    if entry == 'StuffWeightPhaseDetail':
        return {'NeedMoney': product(item.old_price, item.old_need_qty),
                'RealMoney': product(item.old_price, item.old_real_qty)}
    values['Money'] = unit_money(item.old_price, needed, item.old_weight_unit)
    if entry in ['NormalStuffWeightPhaseDetail', 'AfterNormalStuffWeightPhaseDetail']:
        # The saved old expressions explicitly use NeedQty for all three amounts.
        values['NeedMoney'] = values['RealMoney'] = values['Money']
    else:
        values['RealMoney'] = product(product(item.old_price, dosage), item.old_real_qty)
    return values


def unit_money(price, quantity, unit):
    value = decimal(quantity)
    if unit == 'G' and value is not None:
        value /= Decimal('1000')
    return product(price, value)


def weight_header_values(item, entry):
    values = {}
    if entry in ['StuffWeight', 'SelfStuffWeight']:
        values['ClothNetKg'] = difference(item.old_cloth_qty_kg, product(item.old_cloth_qty_kg, item.old_sub_rate))
    if entry == 'StuffWeight':
        return values
    details = nested_details(item, 'erp_production.SourceDyeStuffWeightDetail')
    if entry == 'SelfStuffWeight':
        values['CostMoney'] = subtotal(details, 'Money')
    elif entry in ['ProcessStuffWeight', 'WashProcessStuffWeight']:
        values['Cost'] = subtotal(details, 'Money')
    else:
        values['Cost'] = subtotal(details, 'NeedMoney')
        values['CostMoney'] = subtotal(details, 'Money')
    if entry == 'ReworkStuffWeight':
        ratio = divide(item.old_votl, item.old_cloth_qty_kg, 'old_cloth_qty_kg')
        values['Rate'] = None if ratio is None else ratio + Decimal('2.5')
    return values


def lab_color_values(item):
    order = item.old_order_num
    tail = None if order is None else order[2:]
    marker = item.old_color_markt or ''
    color = item.old_color_num_input if (item.old_color_num_input or '') != '' else marker + (tail or '') + (item.old_color_after or '')
    return {'ColorNum': color, 'KHSHORPTSH': marker if (item.old_cust_color_num or '') == '' else item.old_cust_color_num,
            'Markt': tail, 'OriColorNo': color}


def job_values(item, entry):
    values = {'JobKindID': '02' if item.old_sheet_kind == 10 else '03' if item.old_sheet_kind == 40 else '01'}
    label = 'erp_production.SourceDyeJobAssign'
    values['PreRolls'] = child_sum(item, label, 'Rolls')
    values['PreVatQty'] = child_sum(item, label, 'WeightQty')
    if entry != 'JobSheet':
        values['PrePacks'] = child_sum(item, label, 'Packs')
    else:
        values['Stereotypes'] = child_sum(item, 'erp_production.SourceDyeJobProcess', 'Stereotypes')
        values['StockUnit'] = item.old_assign_unit
    return values


def inventory_values(item, entry):
    if item.SOURCE_TABLE == 'ProdIn':
        records = apps.get_model('erp_warehouse.SourceDyeProdInRecord').objects.filter(source_parent_1=item)
        values = {'WeightQty': subtotal(records, 'WeightQty')}
        if entry == 'ProdInEdit':
            count = records.aggregate(value=Count('old_roll_no'))['value']
            values['Rolls'] = -count if item.old_sheet_kind == 16 else count
            values['LengthQty'] = subtotal(records, 'Yard')
            values['GaryWeight'] = subtotal(records, 'GrayQty')
        else:
            values['Rolls'] = subtotal(records, 'InRolls')
            values['LengthQty'] = subtotal(records, 'Meter')
            if entry == 'ProdIn_ht':
                gray = subtotal(records, 'GrayQty')
                values['GaryWeight'] = None if gray is None else -gray if item.old_sheet_kind == 16 else gray
                if item.old_sheet_kind == 16 and values['Rolls'] is not None:
                    values['Rolls'] = -values['Rolls']
            else:
                values['NetKg'] = subtotal(records, 'NetKg')
        if entry in ['ProdIn_ht', 'ProdInEdit']:
            weight = decimal(values['WeightQty'])
            rolls = values['Rolls']
            gray = values['GaryWeight']
            shipment = None if item.old_ship_ment_type is None else decimal(item.old_ship_ment_type)
            if entry == 'ProdInEdit' or shipment == 1:
                fees = zero(item.old_atte_fee) + zero(item.old_vat_fee)
                if entry == 'ProdIn_ht':
                    fees += zero(item.old_plastic_bags)
                weight = difference(weight, product(fees, rolls))
            values['RealLoss'] = product(divide(difference(weight, gray), gray, 'old_gary_weight'), Decimal('100'))
        return values
    if item.SOURCE_TABLE == 'GrayInDetail':
        records = apps.get_model('erp_warehouse.SourceDyeGrayInRecord').objects.filter(source_parent_1=item)
        count = records.aggregate(value=Count('old_roll_no'))['value']
        head = source_parent(item)
        return {'LengthQty': subtotal(records, 'LengthQty'), 'WeightQty': subtotal(records, 'WeightQty'),
                'Rolls': -count if head.old_sheet_kind == 15 else count}
    if item.SOURCE_TABLE == 'GrayOutDetail':
        records = apps.get_model('erp_warehouse.SourceDyeGrayOutRecord').objects.filter(source_parent_1=item)
        return {'LengthQty': zero(subtotal(records, 'LengthQty')), 'WeightQty': zero(subtotal(records, 'WeightQty')),
                'Rolls': records.aggregate(value=Count('old_roll_no'))['value']}
    if entry == 'SemiOutDetailTurn':
        return {'OutQty': item.old_weight_qty, 'OutRolls': item.old_rolls}
    records = apps.get_model('erp_warehouse.SourceDyeSemiOutRecord').objects.filter(source_parent_1=item)
    values = {'Packs': subtotal(records, 'Packs')}
    if entry == 'SemiOutSaleDetail':
        values.update({'Rolls': subtotal(records, 'Rolls'), 'WeightQty': subtotal(records, 'WeightQty')})
    return values


def packing_entry_values(item, entry):
    if entry == 'WeighRecordYield':
        return {'RollNo': None if item.old_q8 is None else '0' + item.old_q8[6:9]}
    values = {'NetKg': packaging_values(item, entry)['old_net_kg']}
    if entry == 'QueryRecord':
        values['CustQty'] = zero(item.old_kg) + zero(item.old_addkg)
        values['Pound'] = product(item.old_kg, Decimal('2.2046'))
        values['RealQty'] = None if item.old_meter is None else decimal(item.old_meter) - zero(item.old_add_qty) - zero(item.old_cut_qty) - zero(item.old_qty)
        status = 1 if item.old_status is None else item.old_status
        grade = 'A' if item.old_grade_id is None else item.old_grade_id
        values['Tubes'] = 1 if status == 1 and grade <= 'C' else 0
        values['Dots'] = child_sum(item, 'erp_quality.SourceDyeRecordDefect', 'SumDots')
    else:
        values['CustQty'] = item.old_kg
        values['DetailNo'] = item.old_job_sheet_no
        thickness = [decimal(getattr(item, 'old_t' + str(number))) for number in range(1, 6)]
        values['Thick'] = None if None in thickness else sum(thickness) / Decimal('5')
        if entry == 'QC_Record':
            values['Dots'] = child_sum(item, 'erp_quality.SourceDyeRecordDefect', 'Dots')
    return values


def entry_values(item, entry):
    if entry not in ENTRY_METHODS.get(item.SOURCE_TABLE, {}):
        raise ValidationError({'method': '本原表未登记所选入口公式。'})
    with localcontext() as context:
        context.prec = 80
        table = item.SOURCE_TABLE
        if table == 'DyeRecipeDetail':
            values = recipe_values(item, entry)
        elif table == 'StuffWeightPhase':
            values = weight_phase_values(item, entry)
        elif table == 'StuffWeightDetail':
            values = weight_detail_values(item, entry)
        elif table == 'StuffWeight':
            values = weight_header_values(item, entry)
        elif table == 'DyeRecipe':
            values = {'Cost': subtotal(nested_details(item, 'erp_sampling.SourceDyeDyeRecipeDetail'), 'Amount')}
        elif table == 'DyeLabColor':
            values = lab_color_values(item)
        elif table == 'OrderColor':
            values = {'OrderQty': item.old_gray_qty}
        elif table == 'p_Stuff':
            values = {'RecipeUnit': 1 if item.old_stuff_type == 'A' else 0,
                      'StockUnit': 'K', 'WeightUnit': 'K' if item.old_stuff_type == 'A' else 'G'}
        elif table == 'p_DyeCurveDetail':
            values = {'Price': product(item.old_default_value, source_parent(item).old_max_value)}
        elif table == 'JobSheet':
            values = job_values(item, entry)
        elif table in ['ProdIn', 'GrayInDetail', 'GrayOutDetail', 'SemiOutDetail']:
            values = inventory_values(item, entry)
        elif table == 'ProdInRecord':
            values = {'RealQty': zero(item.old_weight_qty)}
        elif table == 'RecordYield':
            values = packing_entry_values(item, entry)
        elif table == 'FixedPriceDetail':
            values = {'Pricesum': zero(item.old_price) + zero(item.old_process_price),
                      'IsConfirmed': 2 if item.old_price is not None and item.old_price > 0 else 1,
                      'SumChengBen': sum(zero(getattr(item, 'old_cheng_ben' + str(number))) for number in range(6))}
        elif table in ['Quote', 'FixedPrice']:
            values = {'CustomerCode': item.old_customer_id}
        return dict(store_value(item, old, value) for old, value in values.items())
