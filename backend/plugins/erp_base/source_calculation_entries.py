"""有明确原表达式的入口；连接查询的阶段与物料明细分别计算。"""
RECIPE_DETAIL_ENTRIES = {
    'DyeRecipePhaseDetail': '一般配方',
    'OtherDyeRecipePhaseDetail': '其他配方',
    'PrepareDyeRecipePhaseDetail': '预处理配方',
    'ReworkDyeRecipePhaseDetail': '返修配方',
    'WashDyeRecipePhaseDetail': '洗缸配方',
    'BulkDyeRecipePhaseDetail': '大货配方',
    'StandardDyeRecipePhaseDetail': '标准配方',
    'FinishDyeRecipePhaseDetail': '后处理配方',
}
WEIGHT_PHASE_ENTRIES = {
    'AddStuffWeightPhaseDetail': '染色加料',
    'AfterNormalStuffWeightPhaseDetail': '后处理领料',
    'NormalStuffWeightPhaseDetail': '正常称料',
    'NormalStuffWeightPhaseDetail_Wash': '正常洗缸称料',
    'ReworkStuffWeightPhaseDetail': '返修称料',
    'SelfStuffWeightPhaseDetail': '自配称料浴比',
}
WEIGHT_DETAIL_ENTRIES = {
    **WEIGHT_PHASE_ENTRIES,
    'ProcessStuffWeightPhaseDetail': '工艺领料',
    'WashProcessStuffWeightPhaseDetail': '工艺洗缸领料',
    'SelfStuffWeightPhaseDetail': '自配称料',
    'StuffWeightPhaseDetail': '一般称料',
}
ENTRY_METHODS = {
    'WProcess': {'AddWProcessEdit': '刷卡补录结束时间取开始时间'},
    'JobShiftEmp': {'JobShiftEmpEdit': '普通登记人员原表头字段', 'DPJobShiftEmpEdit': '刷卡产量查询人员原表头字段'},
    'DyeRecipeDetail': RECIPE_DETAIL_ENTRIES,
    'StuffWeightPhase': WEIGHT_PHASE_ENTRIES,
    'StuffWeightDetail': WEIGHT_DETAIL_ENTRIES,
    'StuffWeight': {
        'SelfStuffWeight': '自配称料净量及金额',
        'StuffWeight': '一般称料净量',
        'NormalStuffWeight': '正常称料金额',
        'NormalStuffWeight_Wash': '洗缸称料金额',
        'AfterNormalStuffWeight': '后处理称料金额',
        'AddStuffWeight': '加料金额',
        'ReworkStuffWeight': '返修称料金额及浴比',
        'ProcessStuffWeight': '工艺领料金额',
        'WashProcessStuffWeight': '工艺洗缸领料金额',
    },
    'DyeRecipe': {
        'BulkDyeRecipe': '大货配方金额',
        'FinishDyeRecipe': '后处理配方金额',
        'TrialDyeRecipe': '试验配方金额',
    },
    'DyeLabColor': {'DyeLabColor': '来样色号', 'ShowDyeLabColor': '来样色号查询'},
    'OrderColor': {
        'OrderColor': '订单数量', 'OrderColorChange': '变更订单数量',
        'OrderColorSup': '补单数量', 'PrintOrderColor': '印花订单数量',
    },
    'p_Stuff': {'p_Stuff': '染化料单位'},
    'p_DyeCurveDetail': {'p_DyeCurveDetail': '曲线参数价格', 'p_DyeCurveDetailJJ': '曲线参数价格'},
    'JobSheet': {
        'JobSheet': '工卡计划汇总', 'PrintJobSheet': '印花工卡计划汇总',
        'SaleJobSheet': '销售工卡计划汇总', 'TwiJobSheet': '加捻工卡计划汇总',
    },
    'ProdIn': {
        'TwistingIn': '加捻入库细码汇总',
        'ProdIn': '成品入库汇总', 'ProdInWork': '车间成品入库汇总',
        'ProdIn_ht': '合同成品入库汇总及损耗', 'ProdInEdit': '成品入库修改汇总及损耗',
    },
    'ProdInRecord': {'ProdInRecord': '成品实际量', 'ProdInRecordWork': '车间成品实际量','TwistingInRecord':'加捻实际量'},
    'GrayInDetail': {'GrayAllotInDetail': '调拨坯料明细汇总'},
    'GrayOutDetail': {'TSGrayOutDetail': '坯料出库匹配汇总'},
    'SemiOutDetail': {
        'SemiOutDetailJob': '半成品领用包装汇总',
        'SemiOutSaleDetail': '半成品销售汇总',
        'SemiOutDetailTurn': '半成品调拨数量',
    },
    'RecordYield': {
        'QC_Record': '质检包装原入口', 'QFQC_Record': '固定粒重质检包装原入口',
        'QueryRecord': '称重细码原入口', 'WeighRecordYield': '标签卷号原入口',
    },
    'Quote': {'FixedPrice': '报价客户码'},
    'FixedPrice': {'Quote': '确价客户码（表头确认价来源待查）'},
    'FixedPriceDetail': {'QuoteDetail': '确价组成价及状态'},
}
