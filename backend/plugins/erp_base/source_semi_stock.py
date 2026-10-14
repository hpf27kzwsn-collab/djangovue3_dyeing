"""Sp_UpdateSemiStockBook的明确入出库、盘点及规格变更事实。"""
from django.db.models import Sum
from django.utils import timezone
from .source_stock_services import raw, copy_fields, detail_rows


def rows(item, entry):
    table = item.SOURCE_TABLE
    base = {'BookDate': raw(item, 'SheetDate'), 'CurrDate': timezone.now(),
            **copy_fields(item, ['SheetSeries', 'SheetNo', 'BusinessUnitID', 'WareHouseID'])}
    if table == 'SemiIn':
        base.update(BookKind=0, SheetKind=raw(item, 'SheetKind'),
                    **copy_fields(item, ['SemiKindID', 'CustomerID', 'SupplierID']))
        for line in detail_rows(item, 'SemiInDetail'):
            yield 'SemiStockBook', {**base,
                **copy_fields(line, ['ProdID', 'LotNo', 'Price', 'Remarks', 'ColorID', 'InSheetKind', 'PurchaseOrders', 'FixedQty', 'A_A', 'A_B', 'PreField1']),
                'StorageUnitIDs': raw(line, 'StorageUnitID'),
                'ReceSheetNo': raw(line, 'OriReceSheetNo') if base['SheetKind'] == 16 else raw(line, 'ReceSheetNo'),
                'DetailNo': raw(line, 'ReceSheetNo'), 'InRolls': raw(line, 'Rolls'), 'InPacks': raw(line, 'Packs'),
                'InLengthQty': raw(line, 'LengthQty'), 'InWeightQty': raw(line, 'WeightQty'), 'InMoney': raw(line, 'Amount')}
    elif table == 'SemiOut':
        base.update(BookKind=1, SheetKind=raw(item, 'SheetKind'), **copy_fields(item, ['CustomerID', 'SemiKindID']))
        for line in detail_rows(item, 'SemiOutDetail'):
            packs = detail_rows(line, 'SemiOutRecord').aggregate(value=Sum('old_packs'))['value']
            yield 'SemiStockBook', {**base,
                **copy_fields(line, ['DetailNo', 'ReceSheetNo', 'JobSheetNo', 'ProdID', 'LotNo', 'Price', 'Remarks', 'SupplierID',
                                     'ColorID', 'InSheetKind', 'PurchaseOrders', 'FixedQty', 'A_A', 'A_B', 'PreField1']),
                'StorageUnitIDs': raw(line, 'StorageUnitID'), 'OutRolls': raw(line, 'Rolls'), 'OutPacks': packs,
                'OutLengthQty': raw(line, 'LengthQty'), 'OutWeightQty': raw(line, 'WeightQty'), 'OutMoney': raw(line, 'Amount')}
    elif table == 'SemiStockAdjust':
        base.update(BookKind=raw(item, 'SheetKind'), SupplierID='', SalerGroupID=raw(item, 'SalerGroupID'))
        for line in detail_rows(item, 'SemiStockAdjustDetail'):
            if not any(raw(line, key) is not None and raw(line, key) != 0 for key in ['AdjustRolls', 'AdjustWeightQty']):
                continue
            yield 'SemiStockBook', {**base,
                **copy_fields(line, ['CustomerID', 'ProdID', 'Spec', 'LotNo', 'ReceSheetNo', 'DetailNo', 'Price', 'Remarks',
                                     'ColorID', 'InSheetKind', 'PurchaseOrders', 'FixedQty', 'A_A', 'A_B', 'PreField1']),
                'StorageUnitIDs': raw(line, 'StorageUnitIDs') or '', 'InRolls': raw(line, 'AdjustRolls'), 'InPacks': 0,
                'InLengthQty': raw(line, 'AdjustLengthQty'), 'InWeightQty': raw(line, 'AdjustWeightQty')}
    else:
        base.update(BookKind=raw(item, 'SheetKind'), SupplierID='', SalerGroupID=raw(item, 'SalerGroupID'))
        for line in detail_rows(item, 'SemiStockSpecUpDetail'):
            common = {**base, **copy_fields(line, ['ReceSheetNo', 'Price', 'Remarks', 'WareHouseID']),
                      'StorageUnitIDs': raw(line, 'StorageUnitIDs') or '', 'DetailNo': raw(line, 'AssignedNo')}
            dimensions = ['CustomerID', 'ProdID', 'LotNo', 'InSheetKind', 'PreField1', 'ColorID', 'PurchaseOrders', 'FixedQty', 'A_A', 'A_B']
            yield 'SemiStockBook', {**common, **copy_fields(line, dimensions),
                'OutRolls': raw(line, 'Rolls'), 'OutPacks': raw(line, 'Packs'),
                'OutLengthQty': raw(line, 'LengthQty'), 'OutWeightQty': raw(line, 'WeightQty')}
            yield 'SemiStockBook', {**common, **{key: raw(line, 'UP' + key) for key in dimensions},
                'InRolls': raw(line, 'Rolls'), 'InPacks': raw(line, 'Packs'),
                'InLengthQty': raw(line, 'LengthQty'), 'InWeightQty': raw(line, 'WeightQty')}
