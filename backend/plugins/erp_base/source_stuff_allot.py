"""染化料调拨的TO/SR派生单据及双侧流水，按原实际WOF换算。"""
from datetime import datetime
from django.apps import apps
from django.db.models.functions import Upper, RTrim
from django.utils import timezone
from .business import persist, record, snapshot, locked
from .source_context import SourceDocumentContext, SourceBusinessParameter
from .source_calculations import decimal, store_value
from .source_stock_services import raw, detail_rows


def create(table, values, actor, origin, parent=None):
    model = apps.get_model('erp_warehouse.SourceDye' + table)
    data = dict(store_value(model(), old, value) for old, value in values.items())
    item = model(**data, source_parent_1=parent) if parent is not None else model(**data)
    persist(item, actor)
    SourceDocumentContext.objects.create(entity=item._meta.label, object_id=item.pk,
        entry_name=table, creator=actor, modifier=actor, dept_belong_id=origin.dept_belong_id,
        effects={'derived_from': {'entity': origin._meta.label, 'id': origin.pk}})
    record(item, 'derive_stuff_allot', {'exists': False}, actor, '由染化料调拨生成')
    return item


def derive(item, context, actor, details=None):
    suffix = raw(item, 'SheetSeries')[-8:]
    at = timezone.now(); empty_date = timezone.make_aware(datetime(1900, 1, 1))
    original_empty = lambda name: '' if raw(item, name) is None else raw(item, name)
    common = {'SheetDate': raw(item, 'SheetDate'), 'BusinessUnitID': '', 'RightStatus': 10,
        'SheetStatus': 0, 'StepNo': 0, 'PrintTimes': 0, 'Revisions': 0,
        'Keeper': original_empty('Keeper'), 'Remarks': original_empty('Remarks'),
        'Creater': original_empty('Creater'), 'CreateDate': at, 'Modifyer': '', 'ModifyDate': empty_date}
    out = create('StuffOut', {**common, 'SheetSeries': 'TO' + suffix, 'SheetNo': 'TO' + suffix,
        'SheetKind': 24, 'WareHouseID': original_empty('WareHouseID'), 'DeptID': original_empty('DeptID'),
        'CustomerID': original_empty('CustomerID'), 'EmpID': '', 'WeightSheetNo': original_empty('SheetNo'),
        'ApproveDate': empty_date, 'Approver': ''}, actor, item)
    incoming = create('StuffIn', {**common, 'SheetSeries': 'SR' + suffix, 'SheetNo': 'SR' + suffix,
        'SheetKind': 15, 'WareHouseID': original_empty('ToWareHouseID'), 'SupplierID': original_empty('CustomerID'),
        'Reason': original_empty('SheetNo'), 'ApproveDate': at, 'Approver': original_empty('Creater')}, actor, item)
    effects = {out._meta.label + 'Detail': [], incoming._meta.label + 'Detail': [],
               out._meta.label: [out.pk], incoming._meta.label: [incoming.pk]}
    material = apps.get_model('erp_base.SourceDyePStuff')
    joined = []
    for line in detail_rows(item, 'StuffAllotDetail') if details is None else details:
        code = raw(line, 'StuffID')
        matches = [] if code is None else list(material.objects.alias(code=Upper(RTrim('old_stuff_id'))).filter(code=code.rstrip(' ').upper()).order_by('pk'))
        joined.extend((line, source) for source in matches or [None])  # 原LEFT JOIN缺失时仍生成对应行，WOF按明确ISNULL取1。
    books = []
    parameter = SourceBusinessParameter.objects.filter(name='CostMethodOfStuff').first()
    update_price = parameter is not None and parameter.value is not None and parameter.value.rstrip(' ').upper() == 'M' and raw(incoming, 'WareHouseID') in ['13', '14']
    if details is not None:
        from .source_business_updates import matching
        from .source_quality_reports import rows
        setting=matching(rows('SSysParams','erp_base'),ParamName='CostMethodOfStuff').order_by('pk').last()
        update_price=setting is not None and raw(setting,'ParamValue')=='M' and raw(incoming,'WareHouseID') in ['13','14']
    for ordinal, (line, source) in enumerate(joined, 1):
        quantity = 0 if raw(line, 'Qty') is None else raw(line, 'Qty')
        price = 0 if raw(line, 'Price') is None else raw(line, 'Price')
        factor = None if source is None else raw(source, 'WOF')
        factor = 1 if factor is None else factor
        detail = {'StuffID': raw(line, 'StuffID'), 'LotNo': '', 'Price': price,
            'TaxPrice': 0, 'TaxRate': 0, 'TaxMoney': 0, 'Amount': raw(line, 'Amount'),
            'APDetailNo': '', 'Remarks': raw(line, 'Remarks')}
        out_line = create('StuffOutDetail', {**detail, 'SheetSeries': raw(out, 'SheetSeries'),
            'DetailNo': raw(out, 'SheetSeries') + '-' + str(ordinal), 'InDetailNo': raw(line, 'InDetailNo'),
            'PurDetailNo': '', 'Qty': quantity, 'DlvQty': 0}, actor, item, out)
        in_line = create('StuffInDetail', {**detail, 'SheetSeries': raw(incoming, 'SheetSeries'),
            'DetailNo': raw(incoming, 'SheetSeries') + '-' + str(ordinal), 'Qty': decimal(quantity) * decimal(factor)}, actor, item, incoming)
        effects[out_line._meta.label].append(out_line.pk); effects[in_line._meta.label].append(in_line.pk)
        if update_price and source is not None:
            current = locked(source)
            adopted_price = raw(in_line, 'Price')
            if raw(current, 'Price') != adopted_price:
                before = snapshot(current)
                current.old_price = adopted_price
                persist(current, actor)
                record(current, 'allot_material_price', before, actor, '按原M计价参数和13/14仓调拨入价更新当前物料价；原提取值仍在来源文件中')
        base = {'BookDate': raw(item, 'SheetDate'), 'AccDate': raw(item, 'SheetDate'), 'CurrDate': at,
            'SupplierID': '', 'StuffID': raw(line, 'StuffID'), 'LotNo': '', 'Price': price}
        books.append(('StuffStockBook', {**base, 'BookKind': 24, 'WareHouseID': raw(out, 'WareHouseID'),
            'DeptID': raw(out, 'DeptID'), 'SheetNo': raw(out, 'SheetNo'), 'SheetSeries': raw(out, 'SheetSeries'),
            'DetailNo': raw(out_line, 'DetailNo'), 'InDetailNo': raw(line, 'InDetailNo'), 'InQty': 0,
            'OutQty': raw(out_line, 'Qty'), 'InMoney': 0, 'OutMoney': raw(line, 'Amount'), 'Remarks': raw(out, 'Remarks')}))
        books.append(('StuffStockBook', {**base, 'BookKind': 15, 'WareHouseID': raw(incoming, 'WareHouseID'),
            'DeptID': '', 'SheetNo': raw(incoming, 'SheetNo'), 'SheetSeries': raw(incoming, 'SheetSeries'),
            'DetailNo': raw(in_line, 'DetailNo'), 'InQty': raw(in_line, 'Qty'), 'OutQty': 0,
            'InMoney': raw(line, 'Amount'), 'OutMoney': 0}))
    context.effects = {**context.effects, 'derived_records': effects}
    persist(context, actor)
    return books
