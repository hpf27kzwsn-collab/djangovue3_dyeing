"""原形单据的库存生效；依据实际旧库存过程，历史承接不调用。"""
from plugins.erp_base.source_provenance import is_historical
from django.apps import apps
from django.utils import timezone
from .business import persist, locked, record, snapshot
from .source_context import SourceDocumentContext
from .source_entry_registry import ENTRY_RULES
from .source_calculations import store_value, decimal


STOCK_TABLES = {'StuffIn', 'StuffOut', 'StuffStockAdjust', 'StuffAllot', 'ProdIn', 'ProdOut', 'ProdStockAdjust',
                'ArticleIn', 'ArticleOut', 'ArticleStockAdjust', 'SampleIn', 'SampleOut', 'GrayIn', 'GrayOut', 'GrayStockAdjust',
                'GrayBalance', 'GrayStockSpecUp', 'GrayStockAllot', 'GrayStorageAdjust', 'SemiIn', 'SemiOut', 'SemiStockAdjust', 'SemiStockSpecUp'}


def raw(item, old):
    return getattr(item, item.SOURCE_FIELDS[old])


def copy_fields(item, names):
    return {name: raw(item, name) for name in names}


def detail_rows(item, name):
    from .source_execution_state import active
    return active(apps.get_model('erp_warehouse.SourceDye' + name).objects.filter(source_parent_1=item)).order_by('pk')


def signed_return(value, kind):
    return None if value is None else -abs(decimal(value)) if kind == 16 else value


def stuff_rows(item):
    base = {'BookDate': raw(item, 'SheetDate'), 'AccDate': raw(item, 'SheetDate'),
            'CurrDate': timezone.now(), 'BookKind': raw(item, 'SheetKind'),
            **copy_fields(item, ['SheetSeries', 'SheetNo', 'WareHouseID', 'Remarks']), 'StorageUnitIDs': ''}
    if item.SOURCE_TABLE == 'StuffIn':
        base.update(SupplierID=raw(item, 'SupplierID'), DeptID='', OutQty=0, OutMoney=0)
        for line in detail_rows(item, 'StuffInDetail'):
            yield 'StuffStockBook', {**base, **copy_fields(line, ['DetailNo', 'StuffID', 'LotNo', 'Price']),
                'InQty': signed_return(raw(line, 'Qty'), base['BookKind']),
                'InMoney': signed_return(raw(line, 'Amount'), base['BookKind']), 'InDetailNo': raw(line, 'OriInDetailNo')}
    elif item.SOURCE_TABLE == 'StuffOut':
        base.update(SupplierID='', DeptID=raw(item, 'DeptID'), InQty=0, InMoney=0)
        for line in detail_rows(item, 'StuffOutDetail'):
            yield 'StuffStockBook', {**base, **copy_fields(line, ['DetailNo', 'StuffID', 'LotNo', 'Price', 'InDetailNo']),
                'OutQty': raw(line, 'Qty'), 'OutMoney': raw(line, 'Amount')}
    else:
        base.update(SupplierID='', DeptID='', OutQty=0, OutMoney=0)
        for line in detail_rows(item, 'StuffStockAdjustDetail'):
            yield 'StuffStockBook', {**base, **copy_fields(line, ['DetailNo', 'StuffID', 'LotNo', 'Price', 'InDetailNo']),
                'InQty': raw(line, 'AdjustQty'), 'InMoney': raw(line, 'AdjustMoney')}


def product_rows(item, entry):
    base = {'BookDate': raw(item, 'SheetDate'), **copy_fields(item, ['SheetSeries', 'SheetNo', 'BusinessUnitID', 'CustomerID', 'WareHouseID'])}
    if item.SOURCE_TABLE == 'ProdIn':
        yield 'ProdStockBook', {**base, 'BookKind': raw(item, 'SheetKind'),
            **copy_fields(item, ['SalerID', 'ProdID', 'Spec', 'LotNo', 'ColorID', 'ColorNum', 'SalerGroupID', 'JobSheetNo', 'CheckNo', 'Price']),
            'FactID': raw(item, 'FabricID'), 'StorageUnitIDs': raw(item, 'StorageUnitID'), 'DetailNo': raw(item, 'SheetSeries'),
            'InRolls': raw(item, 'Rolls'), 'InLengthQty': raw(item, 'LengthQty'), 'InWeightQty': raw(item, 'WeightQty'),
            'InGrayQty': raw(item, 'GaryWeight'), 'InNetKg': raw(item, 'NetKg'), 'OutRolls': 0,
            'OutLengthQty': 0, 'OutWeightQty': 0, 'OutGrayQty': 0}
    elif item.SOURCE_TABLE == 'ProdOut':
        base.update(BookKind=30 if entry == 'ProdOutUpdate' else 22, StorageUnitIDs='',
                    **copy_fields(item, ['SalerID', 'SalerGroupID', 'Remarks']),
                    InRolls=0, InLengthQty=0, InWeightQty=0, InGrayQty=0)
        for line in detail_rows(item, 'ProdOutDetail'):
            yield 'ProdStockBook', {**base,
                **copy_fields(line, ['ColorNum', 'ProdID', 'Spec', 'LotNo', 'CheckNo', 'JobSheetNo', 'DetailNo', 'Price', 'ColorID']),
                'FactID': raw(line, 'FabricID'), 'OutRolls': raw(line, 'Rolls'), 'OutLengthQty': raw(line, 'LengthQty'),
                'OutWeightQty': raw(line, 'WeightQty'), 'OutGrayQty': raw(line, 'GrayQty'), 'OutNetKg': raw(line, 'NetKg')}
    else:
        base.update(BookKind=raw(item, 'SheetKind'), SalerGroupID=raw(item, 'SalerGroupID'),
                    FactID=None, StorageUnitIDs=None, OutRolls=0, OutLengthQty=0, OutWeightQty=0)
        for line in detail_rows(item, 'ProdStockAdjustDetail'):
            if not any(raw(line, field) is not None and raw(line, field) != 0 for field in ['AdjustRolls', 'AdjustLengthQty', 'AdjustWeightQty']):
                continue  # 原过程仅对非零调整生成流水；原明细仍完整保存。
            yield 'ProdStockBook', {**base,
                **copy_fields(line, ['CustomerID', 'ProdID', 'Spec', 'LotNo', 'CheckNo', 'JobSheetNo', 'DetailNo', 'Price', 'ColorID', 'ColorNum']),
                'InRolls': raw(line, 'AdjustRolls'), 'InLengthQty': raw(line, 'AdjustLengthQty'), 'InWeightQty': raw(line, 'AdjustWeightQty')}


def article_rows(item):
    base = {'BookDate': raw(item, 'SheetDate'), 'AccDate': raw(item, 'SheetDate'),
            'BookKind': raw(item, 'SheetKind'), **copy_fields(item, ['SheetSeries', 'SheetNo', 'WareHouseID', 'Remarks'])}
    if item.SOURCE_TABLE == 'ArticleIn':
        base.update(SupplierID=raw(item, 'SupplierID'), DeptID='', OutQty=0, OutMoney=0)
        for line in detail_rows(item, 'ArticleInDetail'):
            quantity = raw(line, 'InQty'); money = raw(line, 'Total')
            if base['BookKind'] == 16:
                quantity = None if quantity is None else -decimal(quantity)
                money = None if money is None else -decimal(money)
            yield 'ArticleStockBook', {**base,
                **copy_fields(line, ['ArticleID', 'ArticleKindID', 'StorageUnitIDs', 'DetailNo', 'Price', 'OriDetailNo']),
                'InQty': quantity, 'InMoney': money}
    elif item.SOURCE_TABLE == 'ArticleOut':
        base.update(DeptID=raw(item, 'DeptID'), InQty=0, InMoney=0)
        for line in detail_rows(item, 'ArticleOutDetail'):
            yield 'ArticleStockBook', {**base,
                **copy_fields(line, ['SupplierID', 'ArticleID', 'ArticleKindID', 'StorageUnitIDs', 'DetailNo', 'Price', 'InDetailNo']),
                'OutQty': raw(line, 'OutQty'), 'OutMoney': raw(line, 'Total')}
    else:
        base.update(DeptID='', StorageUnitIDs='', OutQty=None, OutMoney=None)
        incoming = apps.get_model('erp_warehouse.SourceDyeArticleInDetail')
        for line in detail_rows(item, 'ArticleStockAdjustDetail'):
            matches = list(incoming.objects.filter(old_detail_no__iexact=raw(line, 'InDetailNo')).select_related('source_parent_1'))
            suppliers = [None] if not matches else [raw(source.source_parent_1, 'SupplierID') if source.source_parent_1_id is not None else None for source in matches]
            for supplier in suppliers:
                yield 'ArticleStockBook', {**base,
                    **copy_fields(line, ['ArticleID', 'ArticleKindID', 'DetailNo', 'Price', 'InDetailNo']),
                    'SupplierID': supplier, 'InQty': raw(line, 'AdjustQty'), 'InMoney': raw(line, 'AdjustMoney')}


def clear_effects(context, actor):
    if context.effects.get('gray_storage_changes'):
        from .source_gray_storage import undo
        undo(context, actor)
    for label, keys in context.effects.get('stock_rows', {}).items():
        model = apps.get_model(label)
        model.objects.filter(pk__in=keys).delete()
    derived = context.effects.get('derived_records', {})
    # JSONB不保留字典插入顺序；TO/SR明细必须先于对应表头删除。
    for label in sorted(derived, key=lambda label: not label.endswith('Detail')):
        keys = derived[label]
        apps.get_model(label).objects.filter(pk__in=keys).delete()
        SourceDocumentContext.objects.filter(entity=label, object_id__in=keys).delete()
    for label, keys in context.effects.get('semi_records', {}).items():
        apps.get_model(label).objects.filter(pk__in=keys).delete()
        SourceDocumentContext.objects.filter(entity=label, object_id__in=keys).delete()
    context.effects = {**context.effects, 'stock_rows': {}, 'derived_records': {}, 'semi_records': {}}
    persist(context, actor)


def refresh(item, actor):
    if item.SOURCE_TABLE not in STOCK_TABLES or is_historical(item):
        return
    item = locked(item)
    from .source_execution_state import require_available
    require_available(item)
    context = SourceDocumentContext.objects.filter(entity=item._meta.label, object_id=item.pk).first()
    if context is None or context.entry_name in ['explicit_outwork_closure','explicit_business_continuation']:
        return
    if 'derived_from' in context.effects:
        return
    context = locked(context)
    rule = ENTRY_RULES[item._meta.label][context.entry_name]
    save_updates = rule['save_updates_stock'] is True
    if context.entry_name == 'ProdOutUpdate' and save_updates and raw(item, 'RightStatus') == 10:
        return  # 原修改入口审核后保留已有30类流水。
    ready = save_updates or raw(item, 'RightStatus') == 10
    before = snapshot(context)
    clear_effects(context, actor)
    if ready:
        if item.SOURCE_TABLE in ['SampleIn', 'SampleOut']:
            from .source_sample_stock import rows as sample_rows
            rows = sample_rows(item)
        elif item.SOURCE_TABLE == 'StuffAllot':
            from .source_stuff_allot import derive
            rows = derive(item, context, actor)
        elif item.SOURCE_TABLE.startswith('Stuff'):
            rows = stuff_rows(item)
        elif item.SOURCE_TABLE.startswith('Article'):
            rows = article_rows(item)
        elif item.SOURCE_TABLE == 'GrayStorageAdjust':
            from .source_gray_storage import derive
            rows = derive(item, context, actor)
        elif item.SOURCE_TABLE.startswith('Gray'):
            if item.SOURCE_TABLE in ['GrayIn', 'GrayOut']:
                from .source_gray_records import refresh as refresh_gray_records
                refresh_gray_records(item, context, actor)
            from .source_gray_stock import rows as gray_rows
            rows = gray_rows(item, context.entry_name)
        elif item.SOURCE_TABLE.startswith('Semi'):
            if item.SOURCE_TABLE == 'SemiOut':
                from .source_semi_allocation import allocate
                allocate(item, context, actor)
            from .source_semi_stock import rows as semi_rows
            rows = semi_rows(item, context.entry_name)
        else:
            rows = product_rows(item, context.entry_name)
        effects = {}
        from .source_services import write
        for table, values in rows:
            module = 'erp_sampling' if table == 'SampleStockBook' else 'erp_warehouse'
            model = apps.get_model(module + '.SourceDye' + table)
            prototype = model()
            data = dict(store_value(prototype, old, value) for old, value in values.items())
            entry = write(model, data, actor=actor)
            effects.setdefault(model._meta.label, []).append(entry.pk)
        context.effects = {**context.effects, 'stock_rows': effects}
        persist(context, actor)
    record(context, 'refresh_stock', before, actor, '按原库存生效规则重建本次新办理流水')


def refresh_chain(items, actor):
    for item in items:
        refresh(item, actor)
