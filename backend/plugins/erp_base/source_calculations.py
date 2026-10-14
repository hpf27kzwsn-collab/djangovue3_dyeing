"""已证实的原字段公式；不解析或执行旧表达式语言。"""
from decimal import Decimal, ROUND_HALF_UP, localcontext
from django.db import models
from django.apps import apps
from django.core.exceptions import ValidationError

# 每项都对应workflow_evidence.json中的物理表、实际字段和Express。
PRODUCTS = {
    'ArticleInDetail': [('Amount', 'InQty', 'Price'), ('Total', 'InQty', 'Price')],
    'ArticleOutDetail': [('Total', 'OutQty', 'Price')],
    'PurDetail': [('Amount', 'Qty', 'Price')],
    'GrayInDetail': [('Amount', 'Price', 'WeightQty')],
    'GrayOutDetail': [('Amount', 'Price', 'WeightQty')],
    'SemiInDetail': [('Amount', 'Price', 'WeightQty')],
    'StuffInDetail': [('Amount', 'Qty', 'Price')],
    'StuffOutDetail': [('Amount', 'Qty', 'Price')],
    'StuffAllotDetail': [('Amount', 'Qty', 'Price')],
}
SPECIAL_TABLES = {'PurApplyDetail', 'QuoteDetail', 'FixedPriceDetail', 'ProdOutDetail',
                  'SemiStockAdjustDetail', 'StuffStockAdjustDetail'}
PACK_METHODS = {
    'QC_Record': '实称毛重扣单筒皮重和外包装',
    'QueryRecord': '实称毛重扣原总皮重',
    'QFQC_Record': '按原物料类别采用固定粒重或实称扣皮',
}
AGGREGATES = {
    'GrayIn': [('DlvRolls', 'erp_warehouse.SourceDyeGrayInDetail', 'Rolls', False),
               ('DlvWeightQty', 'erp_warehouse.SourceDyeGrayInDetail', 'WeightQty', False)],
    'GrayOut': [('Rolls', 'erp_warehouse.SourceDyeGrayOutDetail', 'Rolls', False)],
    'ProdOut': [('DlvRolls', 'erp_warehouse.SourceDyeProdOutDetail', 'Rolls', False),
                ('DlvWeightQty', 'erp_warehouse.SourceDyeProdOutDetail', 'WeightQty', False)],
    'StuffIn': [('Total', 'erp_warehouse.SourceDyeStuffInDetail', 'Amount', True)],
}


def decimal(value):
    return None if value is None else Decimal(str(value))


def product(left, right):
    return None if left is None or right is None else decimal(left) * decimal(right)


def zero(value):
    """只用于原公式明确ISNULL(...,0)的字段。"""
    return Decimal('0') if value is None else decimal(value)


def store_value(item, old, value):
    field = item._meta.get_field(item.SOURCE_FIELDS[old])
    if value is not None and isinstance(field, models.DecimalField):
        value = decimal(value).quantize(Decimal('1').scaleb(-field.decimal_places), rounding=ROUND_HALF_UP)
    return field.name, field.to_python(value)


def field_values(item):
    values = {}
    table = item.SOURCE_TABLE
    with localcontext() as context:
        context.prec = 80
        for target, left, right in PRODUCTS.get(table, []):
            values[target] = product(getattr(item, item.SOURCE_FIELDS[left]), getattr(item, item.SOURCE_FIELDS[right]))
        if table == 'PurApplyDetail':
            values['Amount'] = zero(item.old_price) * zero(item.old_qty)
        elif table in ['QuoteDetail', 'FixedPriceDetail']:
            values['Pricesum'] = zero(item.old_price) + zero(item.old_process_price)
        elif table == 'ProdOutDetail':
            values['Amount'] = zero(product(item.old_price, item.old_weight_qty))
            values['Total'] = values['Amount']
        elif table == 'SemiStockAdjustDetail':
            values['AdjustLengthQty'] = zero(item.old_real_length_qty) - zero(item.old_paper_length)
            values['AdjustRolls'] = zero(item.old_real_rolls) - zero(item.old_paper_rolls)
            values['AdjustWeightQty'] = zero(item.old_real_weight_qty) - zero(item.old_paper_weight)
        elif table == 'StuffStockAdjustDetail':
            values['RealMoney'] = product(zero(item.old_real_qty), item.old_price)
            values['AdjustMoney'] = zero(values['RealMoney']) - zero(item.old_paper_money)
            values['AdjustQty'] = zero(item.old_real_qty) - zero(item.old_paper_qty)
        return dict(store_value(item, old, value) for old, value in values.items())


def packaging_values(item, method):
    with localcontext() as context:
        context.prec = 80
        gross = decimal(item.old_kg)
        if method == 'QueryRecord':
            net = None if gross is None else gross - zero(item.old_tube_weight)
        elif method == 'QC_Record':
            net = None if gross is None else gross - zero(item.old_tube_weight) * zero(item.old_rolls) - zero(item.old_pack_bag)
        elif method == 'QFQC_Record':
            if item.old_fabric_kind_id is not None and item.old_fabric_kind_id[2:3] == 'M':
                net = zero(item.old_fixed_qty) * zero(item.old_rolls)
            else:
                net = None if gross is None else gross - zero(item.old_tube_weight) * zero(item.old_rolls) - zero(item.old_pack_bag)
        else:
            raise ValueError('未登记的包装入口公式：' + method)
        return dict([store_value(item, 'NetKg', net)])


def aggregate_values(item):
    values = {}
    with localcontext() as context:
        context.prec = 80
        for target, label, old, coalesce in AGGREGATES.get(item.SOURCE_TABLE, []):
            child = apps.get_model(label)
            value = child.objects.filter(source_parent_1=item).aggregate(value=models.Sum(child.SOURCE_FIELDS[old]))['value']
            values[target] = zero(value) if coalesce else value
        return dict(store_value(item, old, value) for old, value in values.items())


def price_from_amount(item):
    """SmallStuffInDetail原表达式Amount/Qty，与Qty*Price的采用方向分开。"""
    with localcontext() as context:
        context.prec = 80
        quantity = decimal(item.old_qty)
        if quantity == 0:
            raise ValidationError({'old_qty': '数量为零不能通过金额计算单价；原记录可保存，单价另行明确。'})
        value = None if quantity is None or item.old_amount is None else decimal(item.old_amount) / quantity
        return dict([store_value(item, 'Price', value)])
