"""丢失旧视图的明确原表取数方案；原视图未知条件不冒充已恢复。"""

QUERIES = {
    'vwProdOutDataByCheckNo': '''SELECT d.ARDetailNo,d.CheckNo,d.ColorID,d.ColorNum,
        h.CustomerID,d.DetailNo,d.FabricID,NULL AS JobDetailNo,d.LengthQty,d.LotNo,
        d.OrderSheetNo AS OrderNo,d.OutRolls,d.InSheetNo AS ReceSheetNo,h.SalerID,
        h.SheetDate,h.SheetNo,d.Spec,d.Structure,d.WeightQty,
        d.SheetSeries,d.JobSheetNo,d.Rolls,d.InSheetNo,d.OrderSheetNo
        FROM dye.ProdOutDetail d LEFT JOIN dye.ProdOut h ON d.SheetSeries=h.SheetSeries
        WHERE 1=1 AND 1=2''',
    'vwProdCurrentStockQuery': '''SELECT CustomerID,NULL AS FabricID,Spec,LotNo,
        NULL AS StockUnit,ColorID,ColorNum,NULL AS SheetKind,NULL AS Structure,
        SUM(InRolls)-SUM(OutRolls) AS RemainsRolls,
        SUM(CASE @QuantityBasis WHEN 'weight' THEN InWeightQty WHEN 'length' THEN InLengthQty END)
        -SUM(CASE @QuantityBasis WHEN 'weight' THEN OutWeightQty WHEN 'length' THEN OutLengthQty END) AS RemainsQty,
        BusinessUnitID,WareHouseID,ProdID,StorageUnitIDs,JobSheetNo,CheckNo,FactID
        FROM dye.ProdStockBook WHERE 1=1 AND 1=2
        GROUP BY CustomerID,Spec,LotNo,ColorID,ColorNum,BusinessUnitID,WareHouseID,
                 ProdID,StorageUnitIDs,JobSheetNo,CheckNo,FactID''',
    'qry_MachineArticle': '''SELECT d.ArticleID,NULL AS DetailNo,h.ApplyTime AS HandleDate,
        h.HandlerIDs,h.MachineID,d.Qty,d.SerialNum AS RowNo,d.SheetSeries,h.SheetType,
        d.Unit AS unit,p.LastPrice,d.Rounds,d.Kind,d.ArticleName,d.Spec,
        h.SheetNo,h.StartTime,h.EndTime
        FROM dye.MachineFaultArticleInfo d
        LEFT JOIN dye.MachineFault h ON d.SheetSeries=h.SheetSeries
        LEFT JOIN dye.p_Article p ON d.ArticleID=p.ArticleID WHERE 1=1 AND 1=2''',
}

# 原入库明细表已失：以现在ProdIn整行作为入库来源，分别展示实际出库及累计剩余。
_IN_FIELDS=['Amount','BusinessUnitID','CheckNo','ColorID','ColorNum','CustomerID','FabricID',
    'LengthQty','LotNo','Price','Remarks','Rolls','SalerGroupID','SalerID','SheetDate',
    'SheetKind','SheetNo','Spec','StockUnit','Weight','WeightQty','Width']
_UNKNOWN=['APDetailNo','DlvRolls','FactID','JobDetailNo','NoticeDetailNo','ProdKindID','PurDetailNo','Structure']
_OUT_FIELDS={'DetailNo':'d.DetailNo','OutAmount':'d.Amount','OutCustomerID':'h.CustomerID',
    'OutFactID':'h.FactID','OutLengthQty':'d.LengthQty','OutPrice':'d.Price','OutRolls':'d.OutRolls',
    'OutSheetDate':'h.SheetDate','OutSheetKind':'h.SheetKind','OutWeightQty':'d.WeightQty'}
_PROJECTION=[*(f'p.{f}' for f in _IN_FIELDS),*(f'NULL AS {f}' for f in _UNKNOWN),
    *(f'{source} AS {name}' for name,source in _OUT_FIELDS.items()),
    'p.ProdInOriSheetNo AS OriReceSheetNo','p.SheetNo AS ReceSheetNo','p.StorageUnitID AS StorageUnitIDs',
    'p.SheetSeries AS InSheetSeries','d.SheetSeries AS OutSheetSeries','d.InSheetNo','d.Rolls AS ActualOutRolls']
for _name,_field in [('Rolls','Rolls'),('WeightQty','WeightQty'),('LengthQty','LengthQty')]:
    _PROJECTION.append(f'''p.{_field}-(CASE WHEN s.RowCount IS NULL THEN 0 ELSE s.{_field} END) AS Remain{_name}''')
QUERIES['vwProdInAndOutDetailQuery']='SELECT '+','.join(_PROJECTION)+'''
    FROM dye.ProdIn p FULL OUTER JOIN dye.ProdOutDetail d ON d.InSheetNo=p.SheetNo
    LEFT JOIN dye.ProdOut h ON h.SheetSeries=d.SheetSeries
    LEFT JOIN (SELECT InSheetNo,COUNT(*) AS RowCount,SUM(Rolls) AS Rolls,
        SUM(WeightQty) AS WeightQty,SUM(LengthQty) AS LengthQty
        FROM dye.ProdOutDetail GROUP BY InSheetNo) s ON s.InSheetNo=p.SheetNo
    WHERE 1=1 AND 1=2'''

NOTES = {
    'vwProdOutDataByCheckNo': '缺原视图；明确从出库明细左连全部同流水表头，孤立明细保留。OrderNo采用OrderSheetNo、ReceSheetNo采用InSheetNo；JobDetailNo未知为NULL。OutRolls和Rolls分列，不合并；未套用未知旧筛选。',
    'vwProdCurrentStockQuery': '缺原视图；按最新台账的货主、工厂、仓库、库位、物料、工卡、订单及批色规格等原字段汇总，明确选择重量或长度，不过滤零/负库存。FabricID、StockUnit、SheetKind、Structure未知为NULL；FactID单列，不当作FabricID。旧视图分组及期初范围未知，当前只累计台账。',
    'qry_MachineArticle': '缺原vwMachineArticle及MachineCarePlanArticle；当前仅从现存报修配件明细取数，保养配件分支仍缺来源。全部重复报修头/配件资料参与左连接，孤立明细保留；HandleDate明确取ApplyTime，RowNo取SerialNum，DetailNo未知。',
    'vwProdInAndOutDetailQuery': '缺原视图和ProdInDetail；以最新ProdIn整行与ProdOutDetail.InSheetNo全连接，孤立收发均保留。剩余量为每个入库原行减同入库号全部出库明细，Rolls采用实际Rolls，不取计划OutRolls；重复出库头影响展示行但不重复扣减明细。无出库才扣0，已有全NULL出库量保持NULL。缺失字段显示NULL，未知旧过滤不套用。',
}


def differences(name):
    if name not in QUERIES:return None
    return {'mode':'explicit_local_source_reconstruction','missing_columns':[],
            'join_note':NOTES[name], 'historical_reconciliation':'缺原视图，未完成同口径历史对账。',
            'field_acceptance':'未现场验收'}
