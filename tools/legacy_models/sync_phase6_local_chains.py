"""登记本地查询替代、保存公式、采购转入与连续分组校样的验证边界。"""
import hashlib
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from sync_phase6_continuation import replace_section

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / 'docs'
TITLE = '2026-10-17第六阶段本地收发查询与连续分组打印续项.md'
EVIDENCE = 'erp-phase6-local-chains-verification-20261017.json'


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def save(path, value):
    (ROOT / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8')


def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def main():
    support = read('backend/plugins/erp_base/source_phase6_query_support.json')
    runtime = read('docs/erp-phase6-runtime-review-20261017.json')
    live = read('.runtime-temp/phase6/local-chains-evidence/query-metadata.json')
    previous = read('.runtime-temp/phase6/stock-print-evidence/query-metadata.json')
    assert live['print_hashes'] == previous['print_hashes']
    assert len(live['queries']) == 55
    assert all(r.get('error') or any(c.get('error_number') for c in r.get('columns', [])) for r in live['queries'])
    log = '.runtime-temp/phase6/local-chains-regression.log'
    match = re.search(r'Ran (\d+) tests in ([\d.]+)s\s+OK', (ROOT / log).read_text(encoding='utf8'))
    assert match, log
    schema = read('.runtime-temp/phase6/final-schema-check.json')
    schema['snapshot_comparison_note'] = '结构/程序/界面比较引用本日较早的保存快照；本轮重新连接旧库的是55项查询元数据及290份打印摘要。'
    unresolved = [{'entry': n, 'category': v['live_original']['category'], 'error': v['error'],
                   'scope': '财务暂缓' if n == 'FARSumMainMoney' else '本期保留',
                   'historical_reconciliation': '未完成', 'field_acceptance': '未完成'}
                  for n, v in support.items() if v['query_state'] == 'unresolved']
    replacements = [n for n, v in support.items() if v['query_state'] == 'reconstructed_missing_projection']
    formulas = {}
    exec((ROOT / 'backend/plugins/erp_base/source_phase6_auto_values.py').read_text(encoding='utf8'), formulas)
    products = formulas['AUTO_PRODUCTS']
    new_products = {k: v for k, v in products.items() if k not in formulas['PRODUCT_ENTRIES']}
    files = ['backend/plugins/erp_base/' + n for n in [
        'source_phase6_local_queries.py', 'source_phase6_periods.py', 'source_phase6_reconstructions.py',
        'source_phase6_entries.py', 'source_phase6_transfers.py', 'source_phase6_auto_values.py',
        'source_phase6_rendering.py', 'source_phase6_forms.py', 'source_api.py',
        'source_phase6_query_support.json', 'tests/test_source_phase6_local_chains.py',
    ]] + ['web/src/plugins/erp/OriginalEntryWorkbench.vue']
    evidence = {
        'verified_at': datetime.now().astimezone().isoformat(), 'development': '部分完成',
        'query_status_counts': dict(Counter(v['query_state'] for v in support.values())),
        'original_query_differences': len(unresolved) + len(replacements),
        'explicit_query_reconstructions': replacements, 'unresolved_queries': unresolved,
        'unresolved_nonfinancial': sum(r['scope'] == '本期保留' for r in unresolved),
        'unresolved_categories': dict(Counter(r['category'] for r in unresolved)),
        'unresolved_nonfinancial_categories': dict(Counter(r['category'] for r in unresolved if r['scope'] == '本期保留')),
        'new_local_queries': ['vwProdOutDataByCheckNo', 'vwProdCurrentStockQuery', 'qry_MachineArticle', 'vwProdInAndOutDetailQuery'],
        'automatic_formulas': products, 'new_automatic_formulas': new_products,
        'purchase_to_product': {'copied_detail_fields': ['FabricID', 'Spec', 'LotNo', 'ColorID', 'ColorNum', 'Rolls', 'Price', 'Amount', 'CheckNo', 'Remarks'],
            'price_precision': 'PurDetail原价4位，ProdIn目标2位，按目标精度保存，完整原值保存在来源上下文',
            'old_query_closed': False},
        'runtime_counts': runtime['counts'], 'field_copy_status_counts': runtime['field_copy_status_counts'],
        'tests': {'count': int(match[1]), 'seconds': float(match[2]), 'result': 'passed', 'log': log, 'sha256': digest(log),
                  'scope': '15个模块，覆盖第六阶段、报价打样、采购质量、库存、坯料、领料、第三阶段及其余链条；不是全项目重跑。'},
        'frontend': {'result': 'typecheck_and_build_passed', 'log': '.runtime-temp/phase6/local-chains-frontend.log',
                     'note': '保留既有部分分包体积大于500kB的构建提示。'},
        'schema': schema, 'old_sql_readonly_metadata': live, 'old_print_hashes_equal_previous': True,
        'browser_proof': {**read('.runtime-temp/phase6/local-chains-proof/proof.json'),
            'result': '浏览器可访问性树核对两个部门、50条合成员工行、两个分页容器；截图接口失败，未完成像素级外观核验。API真实模型夹具另行通过；不是历史对账或现场验收。'},
        'whole_entry_development_completed': 0, 'whole_entry_historical_reconciled': 0, 'field_accepted': 0,
        'historical_import_rows_this_run': 0, 'files_sha256': {p: digest(p) for p in files},
    }
    assert evidence['unresolved_nonfinancial'] == 43
    assert len(replacements) == 11 and len(new_products) == 20
    assert sum(len(v) for v in products.values()) == 30
    assert runtime['counts']['fixed_proof_templates'] == 4
    save('docs/' + EVIDENCE, evidence)
    content = '''# 第六阶段本地收发查询、自动公式、采购转入与连续分组打印续项

日期：2026-10-17。本轮承接47处非财务查询余项。财务暂缓，原表原主键继续保留，不新增旧erpID。异常、重复、负数、NULL和孤立记录均按明确的取数和保存规则处理，不去重或静默跳过。

## 当前数量与完成口径

**第六阶段仍为部分完成。** 47处非财务查询中，本轮4处增加可执行的公开替代，尚无可执行替代的剩43处；4处中报修配件只补了现存报修分支，缺失的保养分支没有完成。不能把47减4解释成4处完整复刻或全部业务已覆盖。

原55处查询差异全部保留：11处公开替代（含此前7处），44处仍未实现可执行替代，其中1处销售收入汇总按财务暂缓，其余43处继续开发。43处按旧库首个错误分类：13处原字段已不存在、7处缺本地原对象、23处缺外部库或链接。每条可能同时存在多类依赖，首错分类不表示已查尽该条所有问题。

全1682个查询入口的执行标记为：1519处空夹具执行通过、108处财务暂缓、44处未解决、11处明确替代。空夹具通过不代表非空业务正确；明确替代不代表旧口径等价。

|事项|开发与必要验证|历史数据对账|现场验收|
|---|---|---|---|
|4处本地查询|替代实现及非空验证通过；报修配件缺保养分支，其余缺原视图条件/部分列|未完成同口径历史对账|未完成|
|新增20入口、22条金额公式|按原乘法表达式接入service保存层；累计28入口、30条公式；显式金额/NULL优先|未完成全量历史原值对账；历史行不重算|旧客户端生成时机未证明|
|采购转成品入库|显式指定来源头/行和目标参数；重复办理、事务、接口及精度验证通过|原转单查询、旧防重条件未还原|未完成|
|打办月份统计日期范围|按现存生产日表达式实现起止过滤，07:30跨日/月边界通过|旧客户端筛选方式未证明|未完成|
|R102员工资料原XML校样|单层连续分组、WholePage、重复组头、超长组分页及真实接口夹具通过|未与原客户端输出逐页对照|纸张、字体、打印机未验收|

扩大回归266项全部通过，耗时118.288秒；覆盖15个模块，不是全项目重跑。另有53项针对性验证通过。前端类型检查和构建通过，保留既有分包体积提示。Django检查、迁移检查通过；766个ERP模型、655个原表模型、12606个原字段，本轮迁移0、额外旧erpID字段0、历史导入0。

完整入口开发完成、完整入口历史对账完成、现场验收完成仍分别为0。局部功能的测试通过与整个入口完成分开记录。

## 4处本地查询的明确取数

|原入口|已实现|保留差异|
|---|---|---|
|vwProdOutDataByCheckNo|ProdOutDetail左连全部同流水ProdOut；孤立明细保留；OrderNo取OrderSheetNo、ReceSheetNo取InSheetNo|JobDetailNo未知为NULL；原视图条件缺失；OutRolls与实际Rolls分列|
|vwProdCurrentStockQuery|按最新ProdStockBook的货主、组织、仓库、库位、物料、工卡、检验号、工厂、批色规格等原字段汇总；显式选择重量或长度|只累计台账，原期初范围未知；FabricID、StockUnit、SheetKind、Structure未知为NULL；FactID独立展示，不冒充FabricID|
|qry_MachineArticle|报修配件明细左连全部报修头及全部同代码配件资料；孤立明细与重复资料保留|缺vwMachineArticle和MachineCarePlanArticle，保养配件分支未实现；HandleDate明确取ApplyTime、RowNo取SerialNum；DetailNo未知|
|vwProdInAndOutDetailQuery|最新ProdIn整行与ProdOutDetail按入库单号全连接，再关联全部出库头；累计出库由明细原行求和|原ProdInDetail和视图已失；原条件未知；8个缺失列为NULL，逐列见下文|

收发查询缺失列：APDetailNo、DlvRolls、FactID、JobDetailNo、NoticeDetailNo、ProdKindID、PurDetailNo、Structure。OriReceSheetNo明确取ProdInOriSheetNo，StorageUnitIDs明确取StorageUnitID；保留原名、替代来源和额外原流水列用于核对。

剩余量按每个入库原行减同入库号的全部实际出库明细；筒数使用Rolls，不使用计划OutRolls。同号多个入库行各自计算并全部展示，不擅自分摊。重复出库头继续放大展示行，但累计出库只统计明细原行一次，不再被头数量重复扣减。不存在出库才扣0；存在出库但该数量全NULL时结果保持NULL。测试覆盖重复入库头、出库头、孤立收发、全NULL、负数及零库存。

当前库存不过滤零或负结果。重量和长度由参数明确选择，不混合相加，不按未知单位枚举猜换算。原SQL留档不改写，界面同时展示替代说明；这些是可用的公开方案，不是假定已找回旧视图。

本轮只读核查旧库55处原查询的结果集元数据，仍全部编译失败；未执行这些原业务查询取得历史结果。290份打印字节摘要与上轮一致。全量结构/程序/界面比较引用本日较早保存快照，不能当成本轮重新全量抽取。

## 新增20个入口的保存计算

下表每个入口均按原字段配置核对表达式，并用service写入非空、负数、显式NULL夹具验证。累计28个入口、30条目标公式；表中为本轮新增20入口、22条公式。

|入口|目标公式|
|---|---|
'''
    for name, rules in new_products.items():
        content += '|' + name + '|' + '；'.join(f'{target}={left}×{right}' for target, left, right in rules) + '|\n'
    content += '''
目前明确在新增行或修改公式输入时计算；显式提交目标值（包括NULL）优先，不因修改无关字段重算。历史识别沿用现有来源记录，历史值不重新计算。缺少原客户端GenerateTime等枚举含义，保存时点属于公开实现，不宣称完整恢复旧客户端时机；父子汇总、条件公式和其它生成方式不能由这些乘法公式推定完成。

## 采购明细转成品入库

采购明细新增显式动作，选定具体PurMain和PurDetail，核对原SheetSeries，事务内创建ProdIn并执行一次现有整单联动。相同流水的多个采购头由操作者明确选定，不取任意第一条；相同来源重复转入生成不同目标记录，不按单号或来源去重。

复制明细FabricID、Spec、LotNo、ColorID、ColorNum、Rolls、Price、Amount、CheckNo、Remarks共10列，BusinessUnitID取选定采购头。Qty按明确选择写WeightQty或LengthQty，另一维度保持NULL。SheetKind、StockUnit、WareHouseID、CustomerID、ProdID均作为明确参数；不把SupplierID当客户，也不把FabricID当ProdID。

PurDetail.Price有4位小数，当前ProdIn.Price为2位。按目标原字段精度四舍五入，例如1.2354保存1.24；采购原价、原金额及完整头/行仍保存在已有来源上下文中，不新增模型字段，不把目标单价反算覆盖原金额。无法容纳的其它原值按已有字段校验明确报错，不截断或静默丢行。

原PurToProdIn依赖的ProdInDetail已失，其NOT IN历史转入过滤无法证明，原查询继续列在43项中。本动作是明确替代，不把它从查询余项删去。原40条s_FieldCopy配置仍是7条采购到货显式映射、10条报价替代映射、1条物料明确参数、2条缺目标字段、3条残缺、17条财务暂缓；新动作不虚增这40条原配置。

## 打办月份统计的生产日边界

qryDyeDipsRecord增加可选FromProductionDate、UntilProductionDate。两者同时提供时按起日包含、止日不包含过滤；两者都空时保留全期查询。输入按YYYY-MM-DD，必须起日小于止日。

使用现存vw_DyeDipsRecord_EmpID.SDate，即SheetDate减450分钟后的日期，再聚合；这对应07:30生产日界限。例如查2026年2月使用2026-02-01至2026-03-01，2月1日07:29不计入，07:30计入；3月1日07:29仍计入2月生产日，07:30不计入。界面及校样显示范围，避免仅凭月份标题误认过滤已生效。旧客户端如何传筛选条件缺证据，本轮功能不计旧按钮流程等价完成。

## 连续分组原打印

R102员工资料（h_Employeelit）使用原XML的DeptID_R分组、GroupUnion=WholePage及重复组头。小组能放下时同页接排；放不下时整组移到下一页；整组超过新页容量时跨页继续，保留每一行并重复组头。含同名、同编号的员工不去重。支持空且零高度的GroupFooter，非空组尾和组汇总仍列为未实现。

WholePage的实现参考[DevExpress GroupHeaderBand.GroupUnion](https://docs.devexpress.com/XtraReports/DevExpress.XtraReports.UI.GroupHeaderBand.GroupUnion)当前官方语义。原模板使用旧组件版本，仍待原客户端逐页核对；文本按Unicode排序，旧区域排序未证明。

测试验证两组各2行同页、两组各25行分2页、单组70行跨页，另有接口夹具验证员工与部门/岗位资料显示。浏览器可访问性树确认50条合成员工和2个分页容器；截图接口失败，未完成像素级外观核验，不写成外观验收通过。

290份原打印中，可填数校样现为4份：H002、H003、R016、R102；完整原打印运行仍为0。另257份XML存在运行差异，29份无XML。财务模板仅保留清单，不纳入本期开发。多层组、非空组尾、组/页汇总、排序规则、脚本、子报表、条码、动态高度和跨表取数等仍逐模板保留。

## 后续开发顺序

1. 先补下表13处缺列、7处缺本地对象的明确来源；11处已有替代的未知条件、未知列、期初范围和保养配件分支继续保留，不能因能运行删除。23处缺外部来源逐条列出依赖，能用现存原表恢复的继续写代码，无法恢复的单列所缺证据。
2. 逐入口补自动事件和父子保存顺序。216处原事件未整体完成；27处身份/续行未绑定、13组上下文过滤残缺继续登记。金额公式不能替代GenerateTime、IsEnForceExpress、RelyRule的原语义核查。
3. 转单补原选择条件和触发时机；继续处理3条残缺复制目标和2条缺失目标字段。采购转成品与报价转订单均需独立历史结果对照。
4. 原打印优先补R155等实际取数绑定，再按模板补组汇总、排序、脚本、跨表数据、条码和动态布局；R102仍需外观核查及原客户端结果对照。
5. 开发验证通过后单独推进一致时点历史对账和现场验收，三个状态独立，不将真实历史导入与测试夹具混为一谈。

## 43处非财务未有可执行替代的查询

以下不是全部开发余项：还须连同11处替代差异、事件、转单和全部打印差异一起执行。各行历史对账、现场验收均未完成。

|原入口|首错类别|当前错误/缺项|
|---|---|---|
'''
    for row in unresolved:
        if row['scope'] == '本期保留':
            content += '|' + row['entry'] + '|' + row['category'] + '|' + row['error'].replace('|', '／').replace('\n', ' ') + '|\n'
    content += '\nFARSumMainMoney仍保留在原44处未解决清单，按财务暂缓，不算完成。\n\n证据：[' + EVIDENCE + '](' + EVIDENCE + ')；逐模板与复制配置见[字段联动与版式运行核查](2026-10-17第六阶段字段联动与版式运行核查.md)。异常详见[异常说明E184～E188](旧ERP复刻异常与合理实现说明.md)。\n'
    (DOCS / TITLE).write_text(content, encoding='utf8')
    section = f'''## 第六阶段当前状态：本地收发查询、采购转入与连续分组打印（2026-10-17）

本节取代下方前轮数量作为当前口径。详见[{TITLE}]({TITLE})及[实测证据]({EVIDENCE})。

本轮4处本地查询增加明确替代（其中报修配件仍缺保养分支），新增20入口22条金额公式，累计28入口30条；增加明确采购转成品入库、按07:30生产日的日期范围过滤，以及R102员工资料连续分组校样。266项扩大回归、前端类型检查与构建、模型及迁移检查通过。不新增旧erpID，本轮历史导入0。

**第六阶段仍为部分完成。** 原55处查询差异中11处已有替代、44处未解决；其中1处财务暂缓，非财务余项由47处变为43处（13缺列、7缺本地对象、23缺外部来源）。4处能运行不代表4处已完整复刻；55处差异均保留。290份打印有4份可填数校样，完整原打印运行0；257份XML仍有运行差异，29份无XML。R102截图核查未成功，未计外观验收。

40条原复制配置数量和状态不变；216处事件继续逐入口核查，27处身份/续行未绑定、13组上下文过滤残缺继续保留。异常新增E184～E188。完整入口开发完成、完整入口历史对账完成、现场验收完成仍分别为0；局部代码通过不提升整入口状态。下一步依次处理本地来源、自动时机、原转单条件及复杂打印。'''
    targets = ['染色ERP后续开发方案.md', '2026-10-16染色ERP剩余工作全量盘点清单.md',
        '2026-10-17第六阶段查询自动调用及原版式续项清单.md', '2026-10-16第六阶段旧入口自动调用与打印核查清单.md',
        '2026-10-16第六阶段未复刻入口与打印异常明细.md', '2026-10-17第六阶段字段联动与版式运行核查.md',
        '2026-10-17第六阶段查询转单及分组打印续项.md', '2026-10-17第六阶段库存查询报价转单与汇总打印续项.md']
    for name in targets:
        replace_section(DOCS / name, 'phase6-local-chains-current', section)
    inventory = read('docs/erp-remaining-inventory-20261016.json')
    current = {k: evidence[k] for k in ['query_status_counts', 'runtime_counts', 'field_copy_status_counts', 'unresolved_categories', 'unresolved_nonfinancial']}
    current.update(evidence=EVIDENCE, document=TITLE, development='部分完成', historical_reconciliation='未完成', field_acceptance='未完成')
    inventory['phase6_local_chains_20261017'] = current
    for row in inventory['axes']['旧界面配置入口']:
        if row['name'] in replacements:
            row['phase6_query'] = {**support[row['name']], 'state': support[row['name']]['query_state']}
            row['status'] = '部分完成'
            row['reason'] = '明确替代查询可运行；缺失分支、原口径、自动时机、打印或真实对账仍有差异，不能计作等价完成。'
            row['development'] = {'status': '部分完成', 'reason': row['reason']}
            row['phase6_evidence'] = 'docs/' + EVIDENCE
    inventory['counts']['旧界面配置入口'] = dict(Counter(r['status'] for r in inventory['axes']['旧界面配置入口']))
    titles = ['缺本地视图的取数及保养配件分支', '采购转成品的明确参数与原价精度', '新增二十入口金额公式的保存时机', '打办月份统计的生产日范围', '员工资料连续分组及未验收版式']
    axis = inventory['axes']['新旧系统差异及处理情况']
    for number, title in enumerate(titles, 184):
        row = {'id': 'E' + str(number), 'name': title, 'status': '部分完成',
            'reason': '已开发替代与未恢复原口径分别列明；历史对账、现场验收未完成。',
            'related_sql': [], 'source': 'docs/旧ERP复刻异常与合理实现说明.md'}
        prior = next((i for i, r in enumerate(axis) if r['id'] == row['id']), None)
        if prior is None:
            axis.append(row)
        else:
            axis[prior] = row
    inventory['counts']['新旧系统差异及处理情况'] = dict(Counter(r['status'] for r in axis))
    review = read('docs/erp-phase6-review-20261016.json')
    review['local_chains_20261017'] = current
    review.setdefault('pre_local_chains_counts', review['counts'].copy())
    indexed = {r['name']: r for r in inventory['axes']['旧界面配置入口']}
    for row in review['entries']:
        if row['name'] in replacements:
            source = indexed[row['name']]
            row['development'] = source['development']
            row['query'] = source['phase6_query']
    review['counts']['query_execution'] = evidence['query_status_counts']
    review['counts']['development'] = dict(Counter(r['development']['status'] for r in review['entries']))
    review['counts']['development']['开发完成'] = 0
    review['current_review_at'] = evidence['verified_at']
    save('docs/erp-phase6-review-20261016.json', review)
    inventory['phase6_review']['counts'] = review['counts']
    inventory['phase6_review']['current_evidence'] = 'docs/' + EVIDENCE
    save('docs/erp-remaining-inventory-20261016.json', inventory)
    exceptions = '''## E184～E188：本地查询、采购转入及连续分组本轮差异

详细实现、测试与完整查询余项见[本地收发查询与连续分组打印续项](2026-10-17第六阶段本地收发查询与连续分组打印续项.md)。开发、历史对账、现场验收分别记录。

### E184 缺本地视图的取数及保养配件分支

4条查询使用明确原表替代，不宣称旧视图条件恢复。成品入出全连接保留孤立记录与重复头；累计实际出库按明细原行计算，Rolls与计划OutRolls分开。当前库存仅台账累计，原期初范围未知，不过滤零/负库存。缺失展示列为NULL并逐项说明；报修配件只恢复MachineFaultArticleInfo分支，MachineCarePlanArticle缺失的保养分支仍待实现，没有跳过或计作完整。原55处差异仍全部保留。

### E185 采购转成品的明确参数与原价精度

缺ProdInDetail导致PurToProdIn的原NOT IN条件不能执行，继续列为未解决。新动作明确选来源头/行，复制10列，另外指定组织来源、数量维度及目标字段参数；不猜供应商/客户和物料关系。重复来源可再次办理。源Price四位、目标两位，按目标字段四舍五入，完整原价、金额及头行保存在已有来源上下文，不新增字段。此精度处理和新动作时点均为公开方案，未作历史等价确认。

### E186 新增二十入口金额公式的保存时机

新增20入口22条Amount/Total乘法，累计28入口30条。原表达式已核对，service及接口验证通过；新增或改输入时计算，显式提交值含NULL优先，历史行不重算。原客户端GenerateTime等枚举尚不能证明；不得据此宣称所有自动事件、父子公式或旧客户端时机已恢复。

### E187 打办月份统计的生产日范围

使用现存SDate=SheetDate减450分钟后的日期，增加包含起日、不包含止日的明确参数。跨月07:29/07:30边界测试通过，界面及校样记录筛选范围；两日期都不填仍为全期。原客户端月份选择和传参尚缺证据，功能已实现不等于旧流程验收。

### E188 员工资料连续分组及未验收版式

R102按原XML单层DeptID_R、WholePage和重复组头生成校样，小组接排、整组换页、超长组跨页均有验证。空且零高度组尾可处理；非空组尾、组汇总、多层组、排序差异等仍未实现。浏览器可访问性树确认50条合成行与2页，截图接口失败，未完成外观核验；未作真实历史打印对账或纸张/打印机验收。可填数校样4份，完整原打印仍0份。
'''
    replace_section(DOCS / '旧ERP复刻异常与合理实现说明.md', 'phase6-local-chains-exceptions', exceptions)
    print(json.dumps({'tests': evidence['tests']['count'], 'query_states': evidence['query_status_counts'],
                      'nonfinancial_remaining': evidence['unresolved_nonfinancial'], 'proof_templates': 4, 'document': TITLE}, ensure_ascii=False))


if __name__ == '__main__':
    main()
