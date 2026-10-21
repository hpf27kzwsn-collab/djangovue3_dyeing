"""原配置缺字的明确实现；原目录和原表达式保留，替代依据随试算结果返回。"""

# 三个打印查询均从 StuffWeightPhase/Detail 取 SheetSeries；浴比的原公式
# parent.Rate 与对应非打印入口一致，Rate 在 StuffWeight 单头，不在明细。
PRINT_PARENTS = {
    'AddStuffWeightPhaseDetailPrint': 'AddStuffWeight',
    'NormalStuffWeightPhaseDetailPrint': 'NormalStuffWeight',
    'ReworkStuffWeightPhaseDetailPrint': 'ReworkStuffWeight',
}

SELECTOR_EXPRESSIONS = {
    (entry, field): code
    for entry in ('StuffStockToCheck', 'StuffStockToCheckBig')
    for field, code in (('StuffID', 'B093'), ('WareHouseID', 'B097'))
}

PROJECTIONS={'qry_QuoteRelaStuff':('d.Price AS _formula_DetailPrice',),
             'qry_QuoteRelaRecipe':('d.Price AS _formula_DetailPrice',)}


def projections(entry):return PROJECTIONS.get(entry,())


def expression(entry, field):
    original = field['Express']
    code = SELECTOR_EXPRESSIONS.get((entry, field['FieldName']))
    price_formulas={('qry_QuoteRelaStuff','NeedMoney'):'[Price]*[Dosage]*[NeedQty]',
                    ('qry_QuoteRelaStuff','RealMoney'):'[Price]*[Dosage]*[RealQty]',
                    ('qry_QuoteRelaRecipe','Amount'):'[Price]*[Dosage]'}
    if original==price_formulas.get((entry,field['FieldName'])):
        return original.replace('[Price]','[_formula_DetailPrice]'),'按原JOIN中d明细的Price计算染化料金额；原同名单头价格列全部保留，附加明确来源列'
    if code is not None and original == code:
        return '[' + field['FieldName'] + ']', '原Express为选择器编号' + code + '；保留原查询的代码值，不把编号当字段或常量写回'
    if entry in PRINT_PARENTS and field['FieldName'] == 'BathRatio' and original == 'parent.[Rate]':
        return original, '按原SheetSeries连接' + PRINT_PARENTS[entry] + '.Rate；替代原缺失/指向明细的父配置'
    return original, None
