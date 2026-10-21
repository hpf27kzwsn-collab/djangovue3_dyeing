"""当前旧表已删除的纯展示列：保留原查询关系，明确返回未知值。"""
from sqlglot import exp, parse_one
from django.core.exceptions import ValidationError

QUANTITY_ENTRIES = {'vwGrayStockByCheck':'GrayStockBook', 'vwProdStockByCheck':'ProdStockBook',
                    'ProdStockToProdOut':'ProdStockBook', 'GrayCurrentStockQuery':'vwGrayStockBook',
                    'vwProdCurrentStockQuery':'ProdStockBook'}
QUANTITY_OPTIONS = [{'value':'weight','label':'重量原数值'}, {'value':'length','label':'长度原数值'}]


MISSING_PROJECTIONS = {
    'qry_CraftPreCheckJobSheet': {'a.IsNew': 'IsNew'},
    'vwGrayOutQueryBySaleBack': {
        'GrayOutDetail.Structure': 'Structure', 'GrayOutDetail.JobDetailNo': 'JobDetailNo'},
    'vwGrayInAndOutDetailQuery': {
        'GrayInDetail.FabricID': 'FabricID', 'GrayInDetail.Structure': 'Structure',
        'GrayInDetail.JobDetailNo': 'JobDetailNo', 'GrayInDetail.NoticeDetailNo': 'NoticeDetailNo'},
    'vwGrayStockByCheck': {'.JobDetailNo':'JobDetailNo', '.FabricID':'FabricID'},
    'vwProdStockByCheck': {'.ProdKindID':'ProdKindID'},
    'ProdStockToProdOut': {'ProdIn.ProdKindID':'ProdKindID'},
    'GrayCurrentStockQuery': {'GrayInDetail.FabricID':'FabricID','GrayInDetail.Structure':'Structure'},
}


def adapt(name, tree):
    from .source_phase6_reference_queries import NOTES as reference_notes, adapt as reference_adapt
    if name in reference_notes:return reference_adapt(name,tree)
    from .source_phase6_inventory_queries import NOTES, adapt as inventory_adapt
    if name in NOTES:return inventory_adapt(name,tree)
    from .source_phase6_local_queries import QUERIES
    if name in QUERIES:return parse_one(QUERIES[name],read='tsql')
    if name == 'ProdStockToProdOut':
        # 原 vwProdStockBook 缺失，按最新台账明确重建，原库存单位不用于猜测数量维度。
        tree = parse_one('''SELECT b.Rolls,b.Qty,b.SheetNo, p.ColorID,p.ColorNum,
            p.SheetSeries,p.ProdID,p.Spec,p.LotNo,p.StorageUnitID,p.JobSheetNo,p.Remarks,
            p.SheetDate,p.SheetNo,p.BusinessUnitID,p.IsInputRecord,p.SheetKind,
            NULL AS ProdKindID,p.StockUnit,p.SheetStatus,p.CreateDate,p.Creater,CAST(0 AS BIT) AS bIsselect
            FROM dye.ProdIn p JOIN
            (SELECT SheetNo,SUM(InRolls-OutRolls) AS Rolls,
                SUM(CASE @QuantityBasis WHEN 'weight' THEN InWeightQty-OutWeightQty
                    WHEN 'length' THEN InLengthQty-OutLengthQty END) AS Qty
             FROM dye.ProdStockBook GROUP BY SheetNo) b ON p.SheetNo=b.SheetNo
            WHERE b.Qty>0 AND 1=2''', read='tsql')
    elif name == 'GrayCurrentStockQuery':
        # 最新表仅有 GrayID；将其作为公开的新增分组维度，不冒充原 FabricID。
        tree.append('expressions',exp.alias_(exp.column('GrayID','GrayInDetail'),'GrayID'))
        groups=[]
        for column in tree.args['group'].expressions:
            if column.name=='Structure':continue
            if column.name=='FabricID':column.set('this',exp.to_identifier('GrayID'))
            groups.append(column)
        tree.args['group'].set('expressions',groups)
        for table in list(tree.find_all(exp.Table)):
            if table.name.lower()=='vwgraystockbook':
                derived=parse_one('''SELECT *,CASE @QuantityBasis WHEN 'weight' THEN WeightQty
                    WHEN 'length' THEN LengthQty END AS Qty FROM dye.vwGrayStockBook''',read='tsql')
                table.replace(exp.Subquery(this=derived,alias=exp.TableAlias(this=exp.to_identifier(table.alias_or_name))))
    elif name in QUANTITY_ENTRIES:
        physical = QUANTITY_ENTRIES[name]
        # 只替换物理台账来源；内部 UNION ALL、类别筛选、NULL 运算和外层重复连接仍是原式。
        for table in list(tree.find_all(exp.Table)):
            if table.name.lower() == physical.lower():
                derived = parse_one(f'''SELECT *,
                    CASE @QuantityBasis WHEN 'weight' THEN InWeightQty WHEN 'length' THEN InLengthQty END AS InQty,
                    CASE @QuantityBasis WHEN 'weight' THEN OutWeightQty WHEN 'length' THEN OutLengthQty END AS OutQty
                    FROM dye.{physical}''', read='tsql')
                table.replace(exp.Subquery(this=derived, alias=exp.TableAlias(this=exp.to_identifier(table.alias_or_name))))
    missing = MISSING_PROJECTIONS.get(name, {})
    for index, projection in enumerate(tree.expressions):
        if isinstance(projection, exp.Column):
            key = projection.table+'.'+projection.name
            if key in missing:
                tree.expressions[index] = exp.alias_(exp.Null(), missing[key], quoted=True)
    return tree


def differences(name):
    from .source_phase6_reference_queries import differences as reference_differences
    reference=reference_differences(name)
    if reference is not None:return reference
    from .source_phase6_inventory_queries import differences as inventory_differences
    inventory=inventory_differences(name)
    if inventory is not None:return inventory
    from .source_phase6_local_queries import differences as local_differences
    local=local_differences(name)
    if local is not None:return local
    rows = [{'source': key, 'column': value, 'value': None,
             'reason': ('当前旧表已无此字段，原值未知；原分组维度无法复原，现用另列GrayID明确分组。'
                        if name=='GrayCurrentStockQuery' else '当前旧表已无此字段，原值未知；本列只用于展示，未替代筛选或连接条件。')}
            for key, value in MISSING_PROJECTIONS.get(name, {}).items()]
    return {'mode': 'explicit_missing_projection', 'missing_columns': rows,
            'join_note': {
                'vwGrayOutQueryBySaleBack': '保留原 GrayOut.SheetSeries=GrayOut.SheetSeries 连接及其重复组合。',
                'vwGrayInAndOutDetailQuery': '保留原收发连接；末个 LEFT JOIN 的 1=2 仍在连接条件内，出库表头原投影为空；不将它当作外层加载开关。',
                'qry_CraftPreCheckJobSheet': '保留原连接、筛选和 DISTINCT。',
                'vwGrayStockByCheck': '按明确选择的重量或长度原数值重建InQty/OutQty；保留原UNION ALL、类别筛选及重复入库关联。不是单位换算。',
                'vwProdStockByCheck': '按明确选择的重量或长度原数值重建InQty/OutQty；保留原UNION ALL、类别筛选及重复入库关联。不是单位换算。',
                'ProdStockToProdOut': '缺原库存视图；按最新台账及所选数量维度汇总每个SheetNo，再保留原正库存条件和入库头重复连接；不声称等价于缺失视图。',
                'GrayCurrentStockQuery': '按最新vwGrayStockBook所选重量/长度列取Qty；缺失FabricID、Structure保持NULL，以另列GrayID分组。原外层与原视图重复关联仍保留，不去重，不换算单位。'}[name],
            'historical_reconciliation': '旧查询在当前旧库无法编译，尚不能取得同口径历史结果。',
            'field_acceptance': '未现场验收'} if rows else None


def validate_parameters(name, values):
    from .source_phase6_inventory_queries import validate
    validate(name,values)
    if name in QUANTITY_ENTRIES and values.get('quantitybasis') not in ['weight','length']:
        raise ValidationError({'QuantityBasis':'请选择重量原数值或长度原数值；缺失的旧Qty不自动猜测单位。'})
