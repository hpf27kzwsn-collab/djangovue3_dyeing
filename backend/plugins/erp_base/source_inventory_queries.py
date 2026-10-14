"""按原库存流水的实际维度查询；不重演历史出入库或叠加切换期初。"""
from django.apps import apps
from django.db.models import Sum, Count, Q


DIMENSIONS = [('BusinessUnitID', '经营单位原码'), ('WareHouseID', '仓库原码'), ('StorageUnitIDs', '库位原码'),
              ('SupplierID', '供应商原码'), ('CustomerID', '客户原码'), ('Spec', '规格'), ('LotNo', '批号'),
              ('ReceSheetNo', '收料单号'), ('ColorID', '色号原码'), ('CheckNo', '订单明细号'), ('StockFlag', '原库存标志')]
FAMILIES = {
    'stuff': ('StuffStockBook', '染化料', 'StuffID', [('Qty', '原库存数量'), ('Money', '原库存金额')]),
    'article': ('ArticleStockBook', '机物料', 'ArticleID', [('Qty', '原库存数量'), ('Money', '原库存金额')]),
    'gray': ('GrayStockBook', '坯料', 'GrayID', [('Rolls', '粒数'), ('Packs', '件数'), ('LengthQty', '长度量'), ('WeightQty', '重量量')]),
    'semi': ('SemiStockBook', '半成品', 'ProdID', [('Rolls', '粒数'), ('Packs', '件数'), ('LengthQty', '长度量'), ('WeightQty', '重量量')]),
    'product': ('ProdStockBook', '成品', 'ProdID', [('Rolls', '粒数'), ('LengthQty', '长度量'), ('WeightQty', '重量量'), ('NetKg', '净重kg'), ('GrayQty', '坯量')]),
}


def spec(family):
    table, title, material, quantities = FAMILIES[family]
    model = apps.get_model('erp_warehouse.SourceDye' + table)
    dimensions = [(old, label) for old, label in DIMENSIONS if old in model.SOURCE_FIELDS]
    columns = [(material, '物料原码'), *dimensions, ('row_count', '原流水条数')]
    for quantity, label in quantities:
        columns += [(quantity + '_in', label + '入'), (quantity + '_out', label + '出'),
                    (quantity + '_net', label + '收发净额'), (quantity + '_unknown', label + '双侧未填条数')]
    return model, material, dimensions, quantities, {'title': title + '原库存流水汇总', 'columns': columns, 'uses_units': False}


def balances(reader, filters, family):
    model, material, dimensions, quantities, report = spec(family)
    keys = [material, *[old for old, label in dimensions]]
    fields = [model.SOURCE_FIELDS[old] for old in keys]
    quantity_fields = [model.SOURCE_FIELDS[prefix + name] for name, label in quantities for prefix in ['In', 'Out']]
    query = reader.source(model, [*fields, *quantity_fields, model.SOURCE_FIELDS['BookDate']])
    if 'start' in filters:
        query = query.filter(old_book_date__gte=filters['start'])
    if 'end' in filters:
        query = query.filter(old_book_date__lt=filters['end'])
    totals = {'row_count': Count('pk')}
    for quantity, label in quantities:
        incoming = model.SOURCE_FIELDS['In' + quantity]; outgoing = model.SOURCE_FIELDS['Out' + quantity]
        totals[quantity + '_in'] = Sum(incoming)
        totals[quantity + '_out'] = Sum(outgoing)
        totals[quantity + '_unknown'] = Count('pk', filter=Q(**{incoming + '__isnull': True, outgoing + '__isnull': True}))
    groups = query.order_by().values(*fields).annotate(**totals)
    count = groups.count(); offset = (filters['page'] - 1) * filters['page_size']
    result = []
    for row in groups.order_by(*fields)[offset:offset + filters['page_size']]:
        current = {old: row[field] for old, field in zip(keys, fields)}
        current['row_count'] = row['row_count']
        for quantity, label in quantities:
            incoming = row[quantity + '_in']; outgoing = row[quantity + '_out']
            # 未填两侧不制造结存；已记录单侧收发时另一侧表示没有该方向流水。
            net = None if incoming is None and outgoing is None else (0 if incoming is None else incoming) - (0 if outgoing is None else outgoing)
            current.update({quantity + '_in': None if incoming is None else str(incoming),
                quantity + '_out': None if outgoing is None else str(outgoing),
                quantity + '_net': None if net is None else str(net), quantity + '_unknown': row[quantity + '_unknown']})
        result.append(current)
    return count, result


def definitions():
    from functools import partial
    reports = {}; functions = {}
    for family in FAMILIES:
        key = 'source_stock_' + family
        reports[key] = spec(family)[-1]
        functions[key] = partial(balances, family=family)
    return reports, functions
