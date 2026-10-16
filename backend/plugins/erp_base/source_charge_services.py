"""订单另收费采用和工卡另收费查询；各原程序的不同条件分别保留。"""
import json
from decimal import Decimal
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db.models import F, Q, Max
from .business import persist, record, snapshot
from .source_business_updates import matching, update_rows
from .source_stock_services import raw
from .source_numbers import reserve


def rows(table, module='erp_sales'):
    return apps.get_model(module + '.SourceDye' + table).objects.all()


def basic_prices(customer, item):
    result = []
    for head in matching(rows('CusBasicsPrice'), CustomerID=customer).order_by(F('old_sheet_date').desc(nulls_last=True), '-pk'):
        for line in matching(rows('CusExtraCharge'), SheetSeries=raw(head, 'SheetSeries'), PayService=item).order_by('-pk'):
            result.append((head, line))
    return result


def blank_product(query):
    return query.filter(Q(old_prod_id__isnull=True) | Q(old_prod_id__regex=r'^ *$'))


def public_prices(item):
    return blank_product(matching(rows('QuoteItemPrice'), Item=item)).filter(
        Q(old_customer_id__isnull=True) | Q(old_customer_id__regex=r'^ *$'))


def selected_item_price(customer, product, item):
    prices = matching(rows('QuoteItemPrice'), CustomerID=customer, Item=item)
    specific = matching(prices, ProdID=product)
    if product is not None and product.rstrip(' ') == '':
        specific = blank_product(prices)
    selected = specific.order_by(F('old_sheet_date').desc(nulls_last=True), '-pk').first()
    general = blank_product(prices).order_by(F('old_sheet_date').desc(nulls_last=True), '-pk').first()
    if general is not None:
        selected = general  # 原程序是第二个独立IF，通用品种价覆盖具体品种价。
    else:
        public = public_prices(item).order_by(F('old_sheet_date').desc(nulls_last=True), '-pk').first()
        if public is not None:
            selected = public
    return selected


def order_charge(item, actor):
    heads = matching(rows('OrderMain'), SheetSeries=raw(item, 'SheetSeries')).order_by('pk')
    colors = matching(rows('OrderColor'), SheetSeries=raw(item, 'SheetSeries'))
    head = heads.first()
    if head is None or not colors.exists():
        return  # 原触发器内连接没有结果时不产生回写；来源行照常保存。
    own = matching(colors, CheckNo=raw(item, 'CheckNo')).first()
    color = own if own is not None else colors.order_by('old_check_no', 'pk').first()
    candidates = basic_prices(raw(head, 'CustomerID'), raw(item, 'AtteValue'))
    if raw(item, 'FieldType').rstrip(' ').upper() == '05' and not candidates:
        raise ValidationError({'old_atte_value': '原另收费规则：该客户尚未登记此另收费项目，请先维护客户基础价。'})
    untaxed = [(h, line) for h, line in candidates if raw(h, 'IsTax') in [None, False, 0]]
    taxed = [(h, line) for h, line in candidates if raw(h, 'IsTax') in [True, 1]]
    price = unit = None
    chosen = None
    targets = matching(rows('OrderAtte'), SheetSeries=raw(item, 'SheetSeries'), AtteValue=raw(item, 'AtteValue'))
    if untaxed or taxed:
        chosen_head, chosen = (untaxed or taxed)[0]
        price = raw(chosen, 'Price' if untaxed else 'TaxPrice')
        unit = raw(chosen, 'PriceUnit')
    else:
        chosen = selected_item_price(raw(head, 'CustomerID'), raw(color, 'ProdID'), raw(item, 'AtteValue'))
        if chosen is not None:
            price, unit = raw(chosen, 'Price'), raw(chosen, 'Unit')
        targets = matching(targets, FieldType='05')
    before = snapshot(item)
    stored_unit = 0 if unit is not None and unit.strip() == '' else unit
    update_rows(targets, {'Price': price, 'PriceUnit': stored_unit}, actor, 'order_extra_charge', '按原另收费取价及回写范围办理')
    # 原WHERE比较的是本次变量@PriceUnit，不是逐行PriceUnit；保持这个计算范围。
    total = None
    if unit is not None and str(unit).rstrip(' ') != '4':
        charges = matching(rows('OrderAtte'), SheetSeries=raw(item, 'SheetSeries'), FieldType='05').exclude(
            old_atte_value__isnull=True).exclude(old_atte_value__contains='手感')
        values = list(charges.values_list('old_price', flat=True))
        total = sum(Decimal(0) if value is None else value for value in values) if values else None
    update_rows(colors, {'ProcessPrice': total}, actor, 'order_extra_charge_total', '原整单另收费合计，不含手感；采用本次取价单位条件')
    item.refresh_from_db()
    record(item, 'order_charge_source', before, actor, json.dumps({
        'basis': None if chosen is None else {'entity': chosen._meta.label, 'id': chosen.pk},
        'basic_candidates': [line.pk for _, line in candidates], 'order_color': color.pk,
        'unit_controls_whole_sum': unit}, ensure_ascii=False))


def register_charge_name(item, actor):
    dictionary = rows('PFieldValidSub', 'erp_base')
    scope = matching(dictionary, FieldType='AtteKind', Code='05')
    name = raw(item, 'Item')
    if matching(scope, Name=name).exists():
        return
    new = dictionary.model(old_field_type='AtteKind', old_code='05', old_name=name)
    def initial():
        numbers = [int(code) for code in scope.values_list('old_sub_code', flat=True) if code is not None and code.strip().isdigit()]
        return max(numbers, default=0)
    new.old_sub_code = str(reserve(new, 'old_sub_code', {'FieldType': 'AtteKind', 'Code': '05'}, initial, actor))
    maximum = scope.aggregate(value=Max('old_sort_value'))['value']
    new.old_sort_value = (0 if maximum is None else maximum) + 1
    persist(new, actor)
    record(new, 'register_charge_name', {'exists': False}, actor, '原报价项目注册到另收费字典；原非数字编码保留')


def saved(item, actor):
    if item.source_batch_id is not None or item.legacy_id is not None:
        return
    if item.SOURCE_TABLE == 'OrderAtte':
        order_charge(item, actor)
    elif item.SOURCE_TABLE == 'QuoteItemPrice':
        register_charge_name(item, actor)


def job_charge_total(job, without_feel=False):
    """fn_GetPriceAtte / fn_GetPriceAtteWITHOUTSG；不把查询结果伪装成已采用价。"""
    prices = []
    for line in matching(rows('JobAtte', 'erp_production'), SheetSeries=raw(job, 'SheetSeries'), FieldType='05').order_by('pk'):
        name = raw(line, 'AtteValue')
        if raw(line, 'PriceUnit') == 4 or (without_feel and (name is None or '手感' in name)):
            continue
        base = basic_prices(raw(job, 'CustomerID'), name)
        if base:
            prices.extend(set(raw(value, 'Price') for _, value in base))
            continue
        candidates = matching(rows('QuoteItemPrice'), CustomerID=raw(job, 'CustomerID'), Item=name)
        specific = matching(candidates, ProdID=raw(job, 'CustSelfProduct'))
        general = blank_product(candidates)
        if specific.filter(old_is_confirmed=True).exists():
            adopted = specific
        elif general.filter(old_is_confirmed=True).exists():
            adopted = general
        else:
            adopted = public_prices(name)
        prices.extend(adopted.values_list('old_price', flat=True))
    values = [value for value in prices if value is not None]
    total = sum(values) if values else None
    return total if total is None or not without_feel else total / 1000
