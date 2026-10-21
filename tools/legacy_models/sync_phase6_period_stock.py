"""同步期间库存与组尾打印续项；明确替代、整入口完成、真实对账分别计数。"""
import re
from collections import Counter
from datetime import datetime
from sync_phase6_local_chains import ROOT, DOCS, read, save, digest
from sync_phase6_continuation import replace_section

TITLE = '2026-10-17第六阶段期间库存采购候选与组尾打印续项.md'
EVIDENCE = 'erp-phase6-period-stock-verification-20261017.json'


def main():
    support = read('backend/plugins/erp_base/source_phase6_query_support.json')
    runtime = read('docs/erp-phase6-runtime-review-20261017.json')
    dependencies = read('docs/erp-phase6-query-dependencies-20261017.json')
    live = read('.runtime-temp/phase6/period-stock-evidence/query-metadata.json')
    previous = read('.runtime-temp/phase6/local-chains-evidence/query-metadata.json')
    assert live['print_hashes'] == previous['print_hashes']
    assert len(live['queries']) == 55
    assert all(r.get('error') or any(c.get('error_number') for c in r.get('columns', [])) for r in live['queries'])
    log = '.runtime-temp/phase6/period-stock-regression.log'
    match = re.search(r'Ran (\d+) tests in ([\d.]+)s\s+OK', (ROOT / log).read_text(encoding='utf8'))
    assert match, log
    assert 'built in' in (ROOT / '.runtime-temp/phase6/period-stock-frontend.log').read_text(encoding='utf8')
    unresolved = [{'entry': n, 'category': v['live_original']['category'], 'error': v['error'],
                   'scope': '财务暂缓' if n == 'FARSumMainMoney' else '本期保留'}
                  for n, v in support.items() if v['query_state'] == 'unresolved']
    replacements = [n for n, v in support.items() if v['query_state'] == 'reconstructed_missing_projection']
    added = ['ProdStockToOutPlanList', 'PurToProdIn', 'qry_OrderDlvApply', 'vwProdStock', 'vwProdStockTotal']
    new_formulas = ['GrayInWorkDetail', 'GrayOutSaleDetail', 'StuffPurDetail', 'EnergyConsumptionDetail']
    files = ['backend/plugins/erp_base/' + n for n in [
        'source_phase6_inventory_queries.py', 'source_phase6_reconstructions.py', 'source_phase6_periods.py',
        'source_phase6_query_support.json', 'source_phase6_auto_values.py', 'source_phase6_forms.py',
        'source_phase6_rendering.py', 'source_phase6_print_rules.py', 'tests/test_source_phase6_period_stock.py',
    ]] + ['web/src/plugins/erp/OriginalEntryWorkbench.vue', 'tools/legacy_models/audit_phase6_query_dependencies.py']
    schema = read('.runtime-temp/phase6/final-schema-check.json')
    schema['snapshot_comparison_note'] = '全量结构相等引用本日较早保存快照；本轮重新连接旧库核查55条查询元数据和290份打印摘要。'
    evidence = {'verified_at': datetime.now().astimezone().isoformat(), 'development': '部分完成',
        'query_status_counts': dict(Counter(v['query_state'] for v in support.values())),
        'original_query_differences': len(unresolved) + len(replacements),
        'explicit_query_reconstructions': replacements, 'new_query_reconstructions': added,
        'unresolved_queries': unresolved, 'unresolved_nonfinancial': sum(r['scope'] == '本期保留' for r in unresolved),
        'unresolved_nonfinancial_categories': dict(Counter(r['category'] for r in unresolved if r['scope'] == '本期保留')),
        'automatic_formula_entries': 32, 'automatic_formula_targets': 35, 'new_formula_entries': new_formulas,
        'runtime_counts': runtime['counts'], 'field_copy_status_counts': runtime['field_copy_status_counts'],
        'query_dependencies': {'document': 'erp-phase6-query-dependencies-20261017.json',
            'entries': len(dependencies['entries']), 'snapshot_at': dependencies['source_snapshot_at'],
            'sha256': digest('docs/erp-phase6-query-dependencies-20261017.json')},
        'tests': {'count': int(match[1]), 'seconds': float(match[2]), 'result': 'passed', 'log': log,
                  'sha256': digest(log), 'scope': '16个模块的扩大回归，不是全项目重跑。'},
        'frontend': {'result': 'typecheck_and_build_passed', 'log': '.runtime-temp/phase6/period-stock-frontend.log',
                     'note': '构建通过，保留既有分包体积大于500kB提示。'},
        'schema': schema, 'old_sql_readonly_metadata': live, 'old_print_hashes_equal_previous': True,
        'print_validation': '单层组尾、Group汇总、WithLastDetail、PrintAtBottom及明细排序使用合成模板/数据断言；R132缺GrayID已检出，未新增完整可用原模板；本轮未做浏览器像素核验。',
        'whole_entry_development_completed': 0, 'whole_entry_historical_reconciled': 0,
        'field_accepted': 0, 'historical_import_rows_this_run': 0, 'files_sha256': {p: digest(p) for p in files}}
    assert evidence['unresolved_nonfinancial'] == 38 and len(replacements) == 16
    assert len(dependencies['entries']) == 43 and runtime['counts']['fixed_proof_templates'] == 4
    save('docs/' + EVIDENCE, evidence)
    content = f'''# 第六阶段期间库存、采购候选、自动计算与组尾打印续项

日期：2026-10-17。本轮承接43处非财务查询余项，财务暂缓，不新增旧erpID。全部原SQL、缺失依赖、重复记录及异常原值继续保留。

## 当前结果

**第六阶段仍为部分完成，不能标记全部开发完成。** 本轮5处查询有明确替代取数，剩38处非财务查询尚无可执行替代。原55处差异全部保留：累计16处明确替代、39处未解决，其中1处FARSumMainMoney财务暂缓。非财务38处按原库首错分为11处缺列、4处缺本地对象、23处缺外部库/链接；这三类是首错分组，不表示每条只有一个缺项。

全1682入口仍是1519处空夹具执行通过、108处财务暂缓、39处未解决、16处明确替代。空夹具执行和替代取数均不等于整入口复刻完成。

|本轮事项|开发与必要验证|历史数据对账|现场验收|
|---|---|---|---|
|vwProdStock、vwProdStockTotal|明确期初及期间取数已实现；日期边界、重复、负/零、缺维度及接口CSV通过|旧结转时点、原维度和原筛选未证明|未完成|
|ProdStockToOutPlanList|按现存入库整行与台账正库存取候选，重复头保留|缺原入库明细与视图；分摊关系未证明|未完成|
|PurToProdIn|保留采购原投影和连接，展示全部候选；原NOT IN不能恢复，差异公开|不是旧“未入库”名单，历史转入状态未核对|未完成|
|qry_OrderDlvApply|原申请/锁定数据汇总已实现；缺产能上限为未知|原p_DlvAbility缺失，原产能口径未对账|未完成|
|新增4入口5条自动计算|抄表用量先算、金额后算；显式值/NULL优先，非空验证通过|历史行不重算，未全量对账|旧生成时机未确认|
|组尾、组内汇总、明细排序|合成模板边界验证通过；R132新增检出缺GrayID，仍不可计可用|未作旧客户端逐页对照|未完成|

本轮扩大回归{evidence['tests']['count']}项全部通过（{evidence['tests']['seconds']}秒，16个模块）；前端类型检查和构建通过。Django检查、迁移检查通过。仍为766个ERP模型、655个原表模型、12606个原字段，额外旧erpID字段0，本轮迁移0、历史导入0。

完整入口开发完成、完整入口历史对账完成、现场验收完成仍分别为0；局部能力的验证不替代整入口完成。

## 库存期间的明确实现

两条库存报表都要求选择QuantityBasis：重量原数值或长度原数值。StockDate选择具体期初快照，UntilDate为不包含的止日。vwProdStockTotal另要求FromDate作为本期起日，满足StockDate ≤ FromDate < UntilDate；vwProdStock要求StockDate < UntilDate。

vwProdStock：选中期初 + [StockDate,UntilDate)全部台账，计算PaperRolls/PaperQty。保留原UNION ALL和全部同号工卡连接，重复工卡会产生多个展示行。台账客户/物料/色号作为明确分组；工卡侧对应值另名JobCustomerID、JobProdID、JobColorID、JobColorNum，不覆盖台账值。

vwProdStockTotal：选中期初 + [StockDate,FromDate)前期收发得到PreMonth，再分别汇总[FromDate,UntilDate)本期入/出，最后计算Residual。两个期间不交叉。例：两个重复期初各10，前期入2，本期入3及-7，则前期22、本期入-4、期末18；止日发生的99不进入本次统计。重量/长度分别断言，不混加。

共同分组为BusinessUnitID、CustomerID、FactID、WareHouseID、ProdID、Spec、LotNo、ColorID、ColorNum、JobSheetNo、SalerID、StorageUnitIDs、CheckNo。期初原表没有库位、检验号，保持NULL组，不猜分摊到后续明细；空字符串和NULL不合并。零、负余额保留。当前已无成品包数、FabricID、ProdKindID的相应原汇总来源，明确返回NULL，不用FactID/ProdID顶替。

原期初StockDate代表日初还是日末结转尚未证明，当前明确按日初快照使用；旧原查询中日期条件被注释或留给客户端，本轮不冒充已找回原客户端期间过滤。原vwProdStockTotal的HAVING、重复资料连接和缺失维度没有宣称等价恢复。本轮查询结果中的period同时记录选定期初日、起日、止日和公开口径。

## 采购及出库计划候选

ProdStockToOutPlanList用最新ProdIn整行与ProdStockBook按SheetNo汇总连接，保留原Qty>0筛选；同号两条入库头仍输出两行。Qty明确选择重量/长度，原StockUnit仅展示，未用于隐含换算。原ProdInDetail不存在，不能恢复明细级分摊，也没有虚造一个同名原模型。

PurToProdIn继续使用原PurDetail INNER JOIN PurMain和原所有投影，并额外展示SheetSeries。原NOT IN依赖ProdInDetail.PurDetailNo，现已缺失；本轮公开取消这一条件、展示全部采购候选，界面标明这些不是已证实的“尚未入库”记录。重复头、明细和重复转入仍保留；不能依据缺失关系过滤掉异常或已转来源。

实际转成品入库沿用上轮的具体采购头/行选择、明确数量维度与目标参数、来源快照及事务保存。没有新增出库计划模型或假定旧按钮已恢复。40条原复制配置维持原逐项状态，新候选查询不虚增复制配置数量。

## 交期申请与锁定

qry_OrderDlvApply保留Status IN (0,2)的申请数、Status=0的未批数及原NULL减法；只存在Status=2时，SumLengthUnApprove和SumLengApprove仍为NULL，不自行补0。重复申请全部计入；同分类/同日期存在多个锁定行时全部连接展示。

缺p_DlvAbility后，以实际申请分类/交期为主体。MaxWorkQty未知；锁定Status=1时MaxPlanLength取明确的锁定LengthQty，其它情况NULL。不用最大历史申请数或p_Process近似字段猜原产能，原资料缺项仍列为差异。

## 自动保存公式

新增GrayInWorkDetail.Amount=Price×WeightQty、GrayOutSaleDetail.Amount=Price×WeightQty、StuffPurDetail.Amount=Price×Qty，以及EnergyConsumptionDetail两条公式：UseQty=ISNULL(ThisReadQty,0)-ISNULL(LastReadQty,0)，Amount=UseQty×Price。抄表公式中的补0来自原表达式，不推广至其它字段。

计算均在service保存层。新增或修改读数时，先更新未显式提交的UseQty，再更新未显式提交的Amount；显式UseQty包括NULL优先，显式金额优先。原读数减少得到负用量，继续计算并保存，不改成0；不改变历史原值。累计32个入口35条目标公式，其中34条乘法、1条读数差。原GenerateTime枚举/客户端时机仍缺证据，公开采用保存时机，不宣称216处事件全部完成。

## 组尾、组内汇总及排序

单层固定高度组尾支持None及WithLastDetail：前者允许组尾移至新页，后者保留最后一条明细和组尾同页。支持PrintAtBottom、跨页重复组头、Group范围Sum/Count/Avg/Min/Max。汇总按完整组计算，跨页不丢前页数据，重复行计入。组汇总放在非组头/组尾/明细区域时按组件规则显示问号，不擅自按全报告累计。

明细SortFields按声明顺序稳定排序，随后按组字段稳定分组；同键重复记录保留，NULL与空字符串分开。文字当前按Unicode排序，旧区域排序未证明。字段绑定检查现同时检查排序/分组字段，并补齐其_R资料显示列来源。

语义依据当前[DevExpress组尾规则](https://docs.devexpress.com/XtraReports/DevExpress.XtraReports.UI.GroupFooterBand.GroupUnion)和[汇总范围规则](https://docs.devexpress.com/XtraReports/DevExpress.XtraReports.UI.SummaryRunning)，旧组件版本和现场纸张仍待对照。测试使用合成模板核对组尾单独分页、末行同页、底部打印、负值、NULL和重复行；未做本轮浏览器像素核验，不算原打印外观验收。

R132“出入布汇总”的原GPInOutTotal SQL仅投影空客户/日期及零数量，且没有模板SortFields要求的GrayID。排序功能可用后仍不能宣称R132原取数已完成；原客户端动态填数缺失另列E193。290份模板仍仅4份可填数校样，257份XML有运行差异、29份无XML，完整原打印运行0份。

## 43处原查询依赖复查

本轮重新以Windows身份只读查询旧库55条SQL的结果集元数据，55条仍有编译错误；290份原打印摘要与前轮一致。现有数据库清单没有TFEMS、TF_METER、WeighingSystem、ReportServer等业务外库，也没有已配置链接服务器。本轮未执行这些失败的原业务查询取得历史结果。

下表结合本日较早结构快照审计直接表、限定字段、单源未限定字段，并递归现存视图，覆盖本轮起点全部43处。23处存在外部来源、14处存在缺本地对象、14处存在缺原列，类别可重叠。多源未限定字段、动态SQL和客户端动态填数未做猜测，所以不能称已穷尽所有运行依赖。完整原SQL仍保留，原错误不被替代状态抹除。

|原入口|本轮状态|外部来源|缺本地对象|缺列数|
|---|---|---|---|---:|
'''
    for row in dependencies['entries']:
        state = '明确替代，原差异保留' if row['entry'] in added else '未有可执行替代'
        content += '|' + row['entry'] + '|' + state + '|' + '；'.join(row['external_sources']).replace('|', '／') + '|' + '；'.join(row['missing_objects']).replace('|', '／') + '|' + str(len(row['missing_fields'])) + '|\n'
    content += '\n### 缺列逐项原名\n\n'
    for row in dependencies['entries']:
        if row['missing_fields']:
            content += '- **' + row['entry'] + '**：' + '、'.join(row['missing_fields']) + '。\n'
    content += '''
### 无法在现有资料中完整恢复的具体范围

- TFEMS的班次/每日/分时能耗、TF_METER的称料输出、WeighingSystem称重联查、ReportServer远程报表目录，以及192.168.23.254的机器/程序/工艺配料和Link_Pclbase文件信息：现存定义指向外部来源，但本实例无这些来源。未用空结果或本地近似数据冒充恢复。
- WPProcess、EnergyPrice、GrayInRecord_Test、MachineCarePlanArticle缺原对象；只有界面残留配置不足以证明完整表结构、历史原行及所有计算关系。本轮保留入口及原字段配置，没有伪造空同名原表使查询“通过”。
- ProcessSchedule当前字段已变更，旧能耗查询用到的ActStartTime/ActFinishTime、InLengthQty、Energy_*、Energy2_*、EPrice_*及部分资料关联缺失。现存StartTime/FinishTime不能直接证明为同一口径，普通抄表EnergyConsumptionDetail也不能冒充逐工序机台能耗。按上表逐字段保留。
- vwGrayAccount、vwProdAccount原SQL以0作多项账页占位，且缺StockUnit/FabricID。原客户端期间、入出类别填数关系未找回；仅补NULL使SQL编译会留下全零假账，因此仍登记未完成，需要继续定位客户端代码、日志中的后续填数语句或可对照输出。

## 后续顺序与三个状态

1. 继续定位38条未实现查询的原来源；先补本地缺失定义及客户端动态填数，再接有证据的外部来源。16条替代的分摊、结转时点、未知字段和原过滤仍待核对，不能删掉。
2. 自动触发继续逐入口处理主从顺序、GenerateTime/IsEnForceExpress/RelyRule。27条身份/续行未绑定、13组上下文过滤残缺、216处事件不因本轮4个入口扩展而整体完成。
3. 转单继续恢复旧选择条件和按钮时机；3条残缺复制目标、2条已缺目标字段仍保留。采购全部候选可查不等于原未交/未入库筛选完成。
4. 打印继续补R132动态取数、R155缺失绑定、多层组、页汇总、脚本、子报表、条码和动态高度，逐模板验证，不能只按XML可解析或分页引擎用例计完成。
5. 历史对账使用一致时点、明确范围和原主键逐行比较；现场验收另行记录真实操作、纸张、设备和标签确认。当前二者均未完成，不用合成测试数量充当导入数量。
'''
    content += '\n验证证据：[' + EVIDENCE + '](' + EVIDENCE + ')；[43条完整依赖JSON](erp-phase6-query-dependencies-20261017.json)；[异常E189～E194](旧ERP复刻异常与合理实现说明.md)。\n'
    (DOCS / TITLE).write_text(content, encoding='utf8')
    section = f'''## 第六阶段当前状态：期间库存、采购候选与组尾打印（2026-10-17）

本节取代下方前轮数量作为当前口径。详见[{TITLE}]({TITLE})和[验证证据]({EVIDENCE})。

本轮5处查询增加明确替代取数，新增4入口5条自动公式（累计32入口35条），补固定组尾、组汇总和明细排序。{evidence['tests']['count']}项扩大回归、前端类型检查与构建、模型和迁移检查通过。未新增旧erpID，本轮历史导入0。

**第六阶段仍为部分完成。** 原55处查询差异全部保留：16处明确替代、39处未解决（含1处财务暂缓），非财务余项由43变为38，分为11缺列、4缺本地对象、23缺外部来源。替代取数不计完整复刻。43处起点查询已逐条审计缺表、缺列和递归视图外部依赖，见续项附表。

原打印仍为4份可填数校样、0份完整原打印；257份XML有运行差异、29份缺XML。R132缺GrayID及客户端动态填数，排序能力实现未将它升级为可用模板。40条复制配置、216处事件、27条未绑定身份/续行、13组残缺过滤继续逐项保留。异常新增E189～E194。

完整入口开发完成、完整入口历史对账完成、现场验收完成仍分别为0，局部测试通过单独记录。下一步继续缺失来源/动态填数、自动时机、转单条件和复杂打印，不跳过异常及重复数据。'''
    targets = ['染色ERP后续开发方案.md', '2026-10-16染色ERP剩余工作全量盘点清单.md',
        '2026-10-17第六阶段查询自动调用及原版式续项清单.md', '2026-10-16第六阶段旧入口自动调用与打印核查清单.md',
        '2026-10-16第六阶段未复刻入口与打印异常明细.md', '2026-10-17第六阶段字段联动与版式运行核查.md',
        '2026-10-17第六阶段查询转单及分组打印续项.md', '2026-10-17第六阶段库存查询报价转单与汇总打印续项.md',
        '2026-10-17第六阶段本地收发查询与连续分组打印续项.md']
    for name in targets:
        replace_section(DOCS / name, 'phase6-period-stock-current', section)
    inventory = read('docs/erp-remaining-inventory-20261016.json')
    current = {k: evidence[k] for k in ['query_status_counts', 'runtime_counts', 'field_copy_status_counts', 'unresolved_nonfinancial', 'unresolved_nonfinancial_categories']}
    current.update(evidence=EVIDENCE, document=TITLE, development='部分完成', historical_reconciliation='未完成', field_acceptance='未完成')
    inventory['phase6_period_stock_20261017'] = current
    for row in inventory['axes']['旧界面配置入口']:
        if row['name'] in replacements:
            row['phase6_query'] = {**support[row['name']], 'state': support[row['name']]['query_state']}
            row['status'] = '部分完成'
            row['reason'] = '明确替代已验证，原来源/条件、自动时机、原打印或真实对账未完成；不计等价复刻。'
            row['development'] = {'status': '部分完成', 'reason': row['reason']}
            row['phase6_evidence'] = 'docs/' + EVIDENCE
    inventory['counts']['旧界面配置入口'] = dict(Counter(r['status'] for r in inventory['axes']['旧界面配置入口']))
    exceptions = [
        ('期间库存与原结转时点', '明确选择期初和互不交叉的期间，重量/长度分开；原缺维度、结转日初/日末语义及旧HAVING/重复资料连接仍未知。零和负余额保留，期初缺库位/检验号不猜分摊；替代取数不计等价。'),
        ('采购候选与缺失防重关系', 'PurToProdIn缺ProdInDetail.PurDetailNo，公开展示全部采购候选，保留原内连接与重复行；不是尚未入库名单。ProdStockToOutPlanList使用最新入库整行与台账正库存，缺原明细分摊。动作仍明确选择来源并记录快照，旧按钮时机未证明。'),
        ('交期申请缺产能资料', 'p_DlvAbility缺失；实际申请/锁定汇总可运行，产能上限未知，锁定Status=1才取明确LengthQty。重复锁定全部展示，原未批缺行导致NULL减法继续保留。'),
        ('抄表差值与金额的连续计算', '新增4入口5公式，抄表按原ISNULL差值先算UseQty再算Amount；显式值含NULL优先，负用量保留，历史行不重算。原客户端生成时机未证明，不将这批公式算作全部自动事件完成。'),
        ('固定组尾、组汇总与R132缺排序来源', '已补None/WithLastDetail、PrintAtBottom、单层Group汇总及稳定明细排序。跨页保留完整组，重复行不删除。旧区域排序、多层组等仍待实现/核对；R132的GPInOutTotal仅有空/零占位且没有GrayID，仍不能作为完整原打印；本轮无像素外观验收。'),
        ('四十三处查询完整依赖续查', '对本轮起点43处逐项记录递归视图外部来源、缺表和已能确定的缺列，23处外部来源在当前实例/链接中不可用；能耗原字段、WPProcess等对象及账页动态填数仍缺证据，不能补0、造空表或静默跳过。明细见本轮文档及依赖JSON，历史对账和现场验收均未完成。'),
    ]
    axis = inventory['axes']['新旧系统差异及处理情况']
    exception_md = '## E189～E194：期间库存、采购候选与组尾打印差异\n\n详细方案见[' + TITLE + '](' + TITLE + ')。开发、历史对账、现场验收分开记录。\n\n'
    for number, (title, body) in enumerate(exceptions, 189):
        exception_md += f'### E{number} {title}\n\n{body}\n\n'
        item = {'id': 'E' + str(number), 'name': title, 'status': '部分完成', 'reason': body,
                'related_sql': [], 'source': 'docs/旧ERP复刻异常与合理实现说明.md'}
        old = next((i for i, r in enumerate(axis) if r['id'] == item['id']), None)
        if old is None: axis.append(item)
        else: axis[old] = item
    inventory['counts']['新旧系统差异及处理情况'] = dict(Counter(r['status'] for r in axis))
    replace_section(DOCS / '旧ERP复刻异常与合理实现说明.md', 'phase6-period-stock-exceptions', exception_md)
    review = read('docs/erp-phase6-review-20261016.json')
    review['period_stock_20261017'] = current
    review.setdefault('pre_period_stock_counts', review['counts'].copy())
    indexed = {r['name']: r for r in inventory['axes']['旧界面配置入口']}
    for row in review['entries']:
        if row['name'] in replacements:
            row['development'] = indexed[row['name']]['development']
            row['query'] = indexed[row['name']]['phase6_query']
    review['counts']['query_execution'] = evidence['query_status_counts']
    review['counts']['development'] = dict(Counter(r['development']['status'] for r in review['entries']))
    review['counts']['development']['开发完成'] = 0
    review['current_review_at'] = evidence['verified_at']
    inventory['phase6_review']['counts'] = review['counts']
    inventory['phase6_review']['current_evidence'] = 'docs/' + EVIDENCE
    save('docs/erp-phase6-review-20261016.json', review)
    save('docs/erp-remaining-inventory-20261016.json', inventory)
    print({'tests': evidence['tests']['count'], 'remaining_nonfinancial': evidence['unresolved_nonfinancial'], 'document': TITLE})


if __name__ == '__main__':
    main()
