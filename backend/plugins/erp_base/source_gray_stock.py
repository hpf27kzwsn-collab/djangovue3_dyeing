"""Sp_UpdateGrayStockBook的明确数量、规格及货权投影。"""
from django.utils import timezone
from .source_stock_services import raw, copy_fields, detail_rows


TABLES = {'GrayIn', 'GrayOut', 'GrayStockAdjust', 'GrayBalance', 'GrayStockSpecUp', 'GrayStockAllot'}


def rows(item, entry):
    table = item.SOURCE_TABLE
    base = {'BookDate': raw(item, 'SheetDate'), 'CurrDate': timezone.now(),
            **copy_fields(item, ['SheetSeries', 'SheetNo'])}
    if table == 'GrayIn':
        base.update(BookKind=raw(item, 'SheetKind'),
                    **copy_fields(item, ['GrayKindID', 'BusinessUnitID', 'SupplierID', 'CustomerID', 'FactID', 'WareHouseID', 'SalerGroupID']))
        for line in detail_rows(item, 'GrayInDetail'):
            yield 'GrayStockBook', {**base,
                **copy_fields(line, ['StorageUnitIDs', 'GrayID', 'LotNo', 'Price', 'Remarks', 'InSheetKind', 'PreField1', 'ColorID', 'PurchaseOrders', 'FixedQty', 'A_A', 'A_B']),
                'ReceSheetNo': raw(line, 'OriReceSheetNo') if base['BookKind'] == 16 else raw(line, 'ReceSheetNo'),
                'DetailNo': raw(line, 'ReceSheetNo'), 'InRolls': raw(line, 'Rolls'), 'InPacks': raw(line, 'Packs'),
                'InLengthQty': raw(line, 'LengthQty'), 'InWeightQty': raw(line, 'WeightQty')}
    elif table == 'GrayOut':
        base.update(BookKind=raw(item, 'SheetKind'),
                    **copy_fields(item, ['CustomerID', 'FactID', 'GrayKindID', 'BusinessUnitID', 'WareHouseID', 'SalerGroupID']))
        for line in detail_rows(item, 'GrayOutDetail'):
            values = {**base,
                **copy_fields(line, ['StorageUnitIDs', 'GrayID', 'LotNo', 'Price', 'Remarks', 'SupplierID', 'InSheetKind', 'PreField1', 'ColorID', 'PurchaseOrders', 'FixedQty', 'A_A', 'A_B', 'ReceSheetNo']),
                'DetailNo': raw(line, 'AssignedNo'),
                'JobSheetNo': raw(line, 'JobSheetNo') if base['BookKind'] == 21 else raw(line, 'JobSheetSeries'),
                'OutRolls': raw(line, 'Rolls'), 'OutPacks': raw(line, 'Packs'),
                'OutLengthQty': raw(line, 'LengthQty'), 'OutWeightQty': raw(line, 'WeightQty')}
            if entry == 'DiscardGrayOut':
                values['Spec'] = raw(line, 'Spec'); values['JobSheetNo'] = raw(line, 'JobSheetNo')
            yield 'GrayStockBook', values
    elif table == 'GrayBalance':
        base.update(BookKind=raw(item, 'SheetKind'), SheetKind=raw(item, 'SheetKind'),
                    GrayKindID='', SupplierID='', BusinessUnitID=raw(item, 'BusinessUnitID'))
        for line in detail_rows(item, 'GrayBalanceDetail'):
            yield 'GrayStockBook', {**base,
                **copy_fields(line, ['CustomerID', 'WareHouseID', 'StorageUnitIDs', 'GrayID', 'LotNo', 'ReceSheetNo', 'DetailNo', 'Price', 'Remarks']),
                'OutRolls': raw(line, 'Piece'), 'OutPacks': raw(line, 'Piece'),
                'OutLengthQty': raw(line, 'GrainQty'), 'OutWeightQty': raw(line, 'WeightQty'), 'InMoney': raw(line, 'Amount')}
    elif table == 'GrayStockAdjust':
        base.update(BookKind=raw(item, 'SheetKind'),
                    **copy_fields(item, ['GrayKindID', 'BusinessUnitID', 'WareHouseID', 'SalerGroupID']), SupplierID='', FactID='')
        for line in detail_rows(item, 'GrayStockAdjustDetail'):
            quantities = ['AdjustRolls', 'AdjustPacks', 'AdjustLengthQty', 'AdjustWeightQty']
            if not any(raw(line, key) is not None and raw(line, key) != 0 for key in quantities):
                continue
            yield 'GrayStockBook', {**base,
                **copy_fields(line, ['CustomerID', 'GrayID', 'Spec', 'LotNo', 'ReceSheetNo', 'DetailNo', 'Price', 'Remarks',
                                     'InSheetKind', 'PreField1', 'ColorID', 'PurchaseOrders', 'FixedQty', 'A_A', 'A_B']),
                'StorageUnitIDs': raw(line, 'StorageUnitIDs') or '',
                'InRolls': raw(line, 'AdjustRolls'), 'InPacks': raw(line, 'AdjustPacks'),
                'InLengthQty': raw(line, 'AdjustLengthQty'), 'InWeightQty': raw(line, 'AdjustWeightQty')}
    elif table == 'GrayStockSpecUp':
        base.update(BookKind=raw(item, 'SheetKind'),
                    **copy_fields(item, ['GrayKindID', 'BusinessUnitID', 'SalerGroupID']), SupplierID='', FactID='')
        for line in detail_rows(item, 'GrayStockSpecUpDetail'):
            common = {**base, **copy_fields(line, ['ReceSheetNo', 'Price', 'Remarks', 'WareHouseID']),
                      'StorageUnitIDs': raw(line, 'StorageUnitIDs') or '', 'DetailNo': raw(line, 'AssignedNo')}
            dimensions = ['CustomerID', 'GrayID', 'LotNo', 'InSheetKind', 'PreField1', 'ColorID', 'PurchaseOrders', 'FixedQty', 'A_A', 'A_B']
            yield 'GrayStockBook', {**common, **copy_fields(line, dimensions),
                'OutRolls': raw(line, 'Rolls'), 'OutPacks': raw(line, 'Packs'),
                'OutLengthQty': raw(line, 'LengthQty'), 'OutWeightQty': raw(line, 'WeightQty')}
            yield 'GrayStockBook', {**common, **{key: raw(line, 'UP' + key) for key in dimensions},
                'InRolls': raw(line, 'Rolls'), 'InPacks': raw(line, 'Packs'),
                'InLengthQty': raw(line, 'LengthQty'), 'InWeightQty': raw(line, 'WeightQty')}
    else:
        # 最新结构只有含完整转出/转入事实的表头，旧过程引用的明细表已不存在。
        common = {**base, 'FactID': None, 'StorageUnitIDs': None, 'JobSheetNo': raw(item, 'FromReceSheetNo'),
                  'DetailNo': raw(item, 'AssignedNo')}
        yield 'GrayStockBook', {**common, 'BookKind': 41, 'BusinessUnitID': raw(item, 'FromBusinessUnitID'),
            'SalerGroupID': raw(item, 'FromSaleGroupID'), 'CustomerID': raw(item, 'FromCustomerID'),
            'WareHouseID': raw(item, 'FromWareHouseID'), 'GrayID': raw(item, 'FromGrayID'),
            'Spec': raw(item, 'FromSpec'), 'LotNo': raw(item, 'FromLotNo'), 'Price': raw(item, 'FromPrice'),
            'ReceSheetNo': raw(item, 'FromReceSheetNo'), 'InRolls': 0, 'InLengthQty': 0, 'InWeightQty': 0,
            'OutRolls': raw(item, 'Rolls'), 'OutPacks': raw(item, 'Packs'),
            'OutLengthQty': raw(item, 'LengthQty'), 'OutWeightQty': raw(item, 'WeightQty')}
        yield 'GrayStockBook', {**common, 'BookKind': 42, 'BusinessUnitID': raw(item, 'ToBusinessUnitID'),
            'SalerGroupID': raw(item, 'ToSalerGroupID'), 'CustomerID': raw(item, 'ToCustomerID'),
            'WareHouseID': raw(item, 'ToWareHouseID'), 'GrayID': raw(item, 'ToGrayID'),
            'Spec': raw(item, 'ToSpec'), 'LotNo': raw(item, 'ToLotNo'), 'Price': raw(item, 'ToPrice'),
            'ReceSheetNo': raw(item, 'ToReceSheetNo'), 'OutRolls': 0, 'OutLengthQty': 0, 'OutWeightQty': 0,
            'InRolls': raw(item, 'Rolls'), 'InPacks': raw(item, 'Packs'),
            'InLengthQty': raw(item, 'LengthQty'), 'InWeightQty': raw(item, 'WeightQty')}
