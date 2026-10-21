"""最新库存原字段的明确期间取数；已丢失的旧维度不以相近代码顶替。"""
from datetime import date
from django.core.exceptions import ValidationError
from sqlglot import parse_one, exp

PERIOD_ENTRIES = {'vwProdStock', 'vwProdStockTotal'}
QUANTITY_ENTRIES = PERIOD_ENTRIES | {'ProdStockToOutPlanList'}
NOTES = {
    'ProdStockToOutPlanList': '缺ProdInDetail和vwProdStockBook；明确用最新ProdIn整行与台账SheetNo汇总连接。仅保留正库存，重复入库头全部参与；Qty选择重量或长度。ProdKindID、Structure未知为NULL，原入库明细分摊未知。',
    'PurToProdIn': '保留原采购头行内连接及全部投影，增加SheetSeries；缺ProdInDetail，原NOT IN防重条件不能恢复。当前列出全部采购候选，重复记录和重复办理保留；不得理解为全部尚未入库。',
    'qry_OrderDlvApply': '缺p_DlvAbility，以实际申请分类/交期汇总为主体，保留Status IN(0,2)、未批数及全部重复锁定行。MaxWorkQty未知为NULL；Status=1时MaxPlanLength明确取锁定LengthQty，其它情况未知。',
    'vwProdStock': '明确选StockDate期初及[StockDate,UntilDate)台账；重量/长度分别选择。保留UNION ALL、负数、零和同号全部工卡连接。期初无库位/检验号，单列NULL分组，不分摊；旧StockUnit未知。期初日期是期初开始还是期末结转尚待原口径核对。',
    'vwProdStockTotal': '明确选StockDate期初、[StockDate,FromDate)前期台账及[FromDate,UntilDate)本期台账，互不重复。重量/长度分别选择；期初缺检验号/库位单列NULL，不分摊；FabricID、ProdKindID未知。成品包数已无原字段，返回NULL；零/负余额保留，不套未知旧筛选。',
}


def adapt(name, tree):
    if name == 'PurToProdIn':
        # 仅删除无法恢复的旧NOT IN，其它原投影和内连接保持原样。
        tree.set('where', parse_one('SELECT 1 WHERE 1=1 AND 1=2', read='tsql').args['where'])
        tree.append('expressions', exp.column('SheetSeries', 'PurDetail'))
        return tree
    if name == 'ProdStockToOutPlanList':
        return parse_one('''SELECT p.CustomerID,p.SheetDate,p.SheetNo,p.SheetKind,
            NULL AS ProdKindID,p.CheckNo,p.FabricID,p.Spec,b.SheetNo AS ReceSheetNo,
            b.Rolls,b.Qty,p.StockUnit,p.ColorID,p.ColorNum,p.SheetSeries,NULL AS Structure,
            p.LotNo,p.Remarks,p.SheetStatus,CAST(0 AS BIT) AS bIsselect
            FROM dye.ProdIn p JOIN (SELECT SheetNo,SUM(InRolls)-SUM(OutRolls) AS Rolls,
                SUM(CASE @QuantityBasis WHEN 'weight' THEN InWeightQty WHEN 'length' THEN InLengthQty END)
                -SUM(CASE @QuantityBasis WHEN 'weight' THEN OutWeightQty WHEN 'length' THEN OutLengthQty END) AS Qty
                FROM dye.ProdStockBook GROUP BY SheetNo) b ON b.SheetNo=p.SheetNo
            WHERE b.Qty>0 AND 1=2''', read='tsql')
    if name == 'qry_OrderDlvApply':
        return parse_one('''SELECT c.ApplyKindID,NULL AS MaxWorkQty,c.ApplyDlvDate,c.SumLength,c.SumRolls,
            d.LengthQty AS LockLength,ISNULL(d.Status,0) AS LockStatus,e.SumLengthUnApprove,
            c.SumLength-e.SumLengthUnApprove AS SumLengApprove,
            CASE WHEN d.Status=1 THEN d.LengthQty ELSE NULL END AS MaxPlanLength
            FROM (SELECT ApplyKindID,ApplyDlvDate,SUM(LengthQty) AS SumLength,SUM(Rolls) AS SumRolls
                FROM dye.OrderDlvApply WHERE Status IN (0,2) GROUP BY ApplyKindID,ApplyDlvDate) c
            LEFT JOIN (SELECT ApplyKindID,ApplyDlvDate,SUM(LengthQty) AS SumLengthUnApprove
                FROM dye.OrderDlvApply WHERE Status=0 GROUP BY ApplyKindID,ApplyDlvDate) e
                ON c.ApplyDlvDate=e.ApplyDlvDate AND c.ApplyKindID=e.ApplyKindID
            LEFT JOIN dye.OrderDlvApplyLock d ON c.ApplyDlvDate=d.ApplyDlvDate AND c.ApplyKindID=d.ApplyKindID
            WHERE 1=1 AND 1=2''', read='tsql')
    if name not in PERIOD_ENTRIES:
        return tree
    dimensions = ['BusinessUnitID', 'CustomerID', 'FactID', 'WareHouseID', 'ProdID', 'Spec',
                  'LotNo', 'ColorID', 'ColorNum', 'JobSheetNo', 'SalerID', 'StorageUnitIDs', 'CheckNo']
    initial = ','.join('NULL AS '+v if v in ['StorageUnitIDs', 'CheckNo'] else v for v in dimensions)
    keys = ','.join(dimensions)
    qty = "CASE @QuantityBasis WHEN 'weight' THEN PreMonthWeightQty WHEN 'length' THEN PreMonthLengthQty END"
    in_qty = "CASE @QuantityBasis WHEN 'weight' THEN InWeightQty WHEN 'length' THEN InLengthQty END"
    out_qty = "CASE @QuantityBasis WHEN 'weight' THEN OutWeightQty WHEN 'length' THEN OutLengthQty END"
    if name == 'vwProdStock':
        sql = f'''SELECT a.*,NULL AS StockUnit,0 AS ProdKind,
            b.CustomerID AS JobCustomerID,b.ProdID AS JobProdID,b.ColorID AS JobColorID,b.ColorNum AS JobColorNum
            FROM (SELECT {keys},SUM(Rolls) AS PaperRolls,SUM(Qty) AS PaperQty FROM (
                SELECT {initial},PreMonthRolls AS Rolls,{qty} AS Qty FROM dye.ProdStock WHERE StockDate=@StockDate
                UNION ALL SELECT {keys},SUM(InRolls)-SUM(OutRolls),SUM({in_qty})-SUM({out_qty})
                FROM dye.ProdStockBook WHERE BookDate>=@StockDate AND BookDate<@UntilDate GROUP BY {keys}
            ) u GROUP BY {keys}) a LEFT JOIN dye.JobSheet b ON a.JobSheetNo=b.SheetNo WHERE 1=1 AND 1=2'''
    else:
        sql = f'''SELECT {keys},NULL AS FabricID,NULL AS ProdKindID,NULL AS PreMonthPacks,
            SUM(PreRolls) AS PreMonthRolls,SUM(PreQty) AS PreMonthQty,NULL AS ThisMonthInPacks,
            SUM(InRolls) AS ThisMonthInRolls,SUM(InQty) AS ThisMonthInQty,NULL AS ThisMonthOutPacks,
            SUM(OutRolls) AS ThisMonthOutRolls,SUM(OutQty) AS ThisMonthOutQty,NULL AS ResidualPacks,
            SUM(PreRolls)+SUM(InRolls)-SUM(OutRolls) AS ResidualRolls,
            SUM(PreQty)+SUM(InQty)-SUM(OutQty) AS ResidualQty
            FROM (
                SELECT {initial},PreMonthRolls AS PreRolls,{qty} AS PreQty,
                    0 AS InRolls,0 AS InQty,0 AS OutRolls,0 AS OutQty
                FROM dye.ProdStock WHERE StockDate=@StockDate
                UNION ALL SELECT {keys},SUM(InRolls)-SUM(OutRolls),SUM({in_qty})-SUM({out_qty}),0,0,0,0
                FROM dye.ProdStockBook WHERE BookDate>=@StockDate AND BookDate<@FromDate GROUP BY {keys}
                UNION ALL SELECT {keys},0,0,SUM(InRolls),SUM({in_qty}),SUM(OutRolls),SUM({out_qty})
                FROM dye.ProdStockBook WHERE BookDate>=@FromDate AND BookDate<@UntilDate GROUP BY {keys}
            ) u WHERE 1=1 AND 1=2 GROUP BY {keys}'''
    return parse_one(sql, read='tsql')


def validate(name, values):
    if name in QUANTITY_ENTRIES and values.get('quantitybasis') not in ['weight', 'length']:
        raise ValidationError({'QuantityBasis': '须明确选择重量或长度原数值。'})
    if name not in PERIOD_ENTRIES:
        return
    keys = ['stockdate', 'untildate'] if name == 'vwProdStock' else ['stockdate', 'fromdate', 'untildate']
    try:
        dates = [date.fromisoformat(values[key]) for key in keys]
    except (KeyError, TypeError, ValueError) as error:
        raise ValidationError({'parameters': '库存期初日及查询起止日须明确填写YYYY-MM-DD。'}) from error
    if dates[0] >= dates[-1] or (name == 'vwProdStockTotal' and not dates[0] <= dates[1] < dates[2]):
        raise ValidationError({'parameters': '期初日不能晚于本期起日，止日不包含且须晚于起日。'})


def differences(name):
    if name not in NOTES:
        return None
    return {'mode': 'explicit_inventory_source', 'missing_columns': [], 'join_note': NOTES[name],
            'historical_reconciliation': '缺原对象/字段及旧客户端期间条件，未完成同口径历史对账。',
            'field_acceptance': '未现场验收'}
