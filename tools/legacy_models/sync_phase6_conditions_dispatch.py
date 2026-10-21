"""同步成品收发、明确调价和条件打印的实际证据，不缩减未解决查询。"""
import importlib.util
import re
from collections import Counter
from datetime import datetime
from sync_phase6_local_chains import ROOT, DOCS, read, save, digest
from sync_phase6_continuation import replace_section

TITLE = '2026-10-17第六阶段成品收发调价与条件打印续项.md'
EVIDENCE = 'erp-phase6-conditions-dispatch-verification-20261017.json'


def main():
    previous = read('docs/erp-phase6-machine-calculations-verification-20261017.json')
    support = read('backend/plugins/erp_base/source_phase6_query_support.json')
    runtime = read('docs/erp-phase6-runtime-review-20261017.json')
    deps = {row['entry']: row for row in read('docs/erp-phase6-query-dependencies-20261017.json')['entries']}
    log = '.runtime-temp/phase6/conditions-dispatch-regression.log'
    match = re.search(r'Ran (\d+) tests in ([\d.]+)s\s+OK', (ROOT/log).read_text(encoding='utf8'))
    assert match, log
    build = '.runtime-temp/phase6/conditions-dispatch-frontend.log'
    assert 'built in' in (ROOT/build).read_text(encoding='utf8')
    spec = importlib.util.spec_from_file_location('automatic', ROOT/'backend/plugins/erp_base/source_phase6_auto_values.py')
    automatic = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(automatic)
    auto_entries = len(automatic.AUTO_ENTRIES)
    auto_targets = sum(len(automatic.generated_fields(n)) for n in automatic.AUTO_ENTRIES)
    unresolved = previous['unresolved_queries']
    assert len([r for r in unresolved if r['scope'] == '本期保留']) == 35
    assert {r['entry'] for r in unresolved} == {n for n,v in support.items() if v['query_state'] == 'unresolved'}
    assert (auto_entries, auto_targets, runtime['counts']['fixed_proof_templates']) == (43, 59, 5)
    schema = read('.runtime-temp/phase6/final-schema-check.json')
    schema['snapshot_comparison_note'] = '结构相等使用本日缓存快照；本轮只检查到MSSQLSERVER为Stopped，未取得新的旧库查询或数据核验。Django检查和迁移检查为本轮实际运行。'
    files = ['backend/plugins/erp_base/'+n for n in [
        'source_phase6_auto_values.py', 'source_phase6_transfers.py', 'source_phase6_forms.py', 'source_api.py',
        'source_phase6_calculated_print.py', 'source_phase6_print_rules.py', 'source_phase6_rendering.py',
        'tests/test_source_phase6_conditions_dispatch.py', 'tests/test_source_phase6_machine_calculations.py']]
    evidence = {
        'verified_at': datetime.now().astimezone().isoformat(), 'development': '部分完成',
        'query_status_counts': dict(Counter(v['query_state'] for v in support.values())),
        'original_query_differences': 55, 'explicit_query_reconstructions': previous['explicit_query_reconstructions'],
        'new_query_reconstructions': [], 'unresolved_queries': unresolved, 'unresolved_nonfinancial': 35,
        'unresolved_nonfinancial_categories': previous['unresolved_nonfinancial_categories'],
        'automatic_formula_entries': auto_entries, 'automatic_formula_targets': auto_targets,
        'new_formula_entries': ['ProdOutDetail', 'ProdOutDetailUpdate', 'ProdInRecord', 'ProdInRecordWork'],
        'new_formula_targets': 6, 'new_transfer_variants': ['QuoteDetail -> PriceAdjustDetail'],
        'runtime_counts': runtime['counts'], 'field_copy_status_counts': runtime['field_copy_status_counts'],
        'new_proof_templates': [{'index': 152, 'report_id': 'R013', 'validation': 'API查询取数和校样测试；重复出仓关联、退车间原行保留'}],
        'tests': {'count': int(match[1]), 'seconds': float(match[2]), 'result': 'passed', 'log': log, 'sha256': digest(log),
            'scope': '19个模块扩大回归，含本轮11项；不是全项目测试或历史数据对账'},
        'frontend': {'result': 'typecheck_and_build_passed', 'log': build, 'sha256': digest(build), 'note': '既有大分包提示保留'},
        'schema': schema,
        'old_sql_this_run': {'status': 'not_queried_service_stopped', 'service': 'MSSQLSERVER', 'service_status': 'Stopped',
            'note': '本轮检查服务状态；没有新的旧库连接或查询结果，不将前轮连接失败冒充本轮尝试。',
            'last_success_evidence': previous['old_sql_this_run']['last_success_evidence'],
            'last_success_at': previous['old_sql_this_run']['last_success_at']},
        'cached_structure_source': previous['cached_structure_source'],
        'print_validation': 'Iif、比较、布尔、IsNull、字符串、Round和日期的明确实现已验证；K010原公式与R013取数校样通过；R010仍缺KKind/grayQty。未做原客户端像素、纸张或设备验收。',
        'whole_entry_development_completed': 0, 'whole_entry_historical_reconciled': 0, 'field_accepted': 0,
        'historical_import_rows_this_run': 0, 'files_sha256': {p: digest(p) for p in files}}
    save('docs/'+EVIDENCE, evidence)
    text = f'''# 第六阶段成品收发、报价调价与条件打印续项

日期：2026-10-17。承接35处非财务查询余项；财务暂缓，不新增旧erpID，异常和重复业务继续保留。

## 当前结果和完成标准

**第六阶段仍为部分完成。35处非财务查询尚无可执行替代，数量没有减少。** 本轮补的是4个成品收发入口的6条自动公式、报价明细明确转调价，以及原打印的条件、字符串、舍入和日期表达式；新增R013填数校样。不能用这些局部能力抵消查询缺口，也不把校样当成完整原打印。

|事项|开发与必要验证|历史数据对账|现场验收|
|---|---|---|---|
|成品出仓金额、合计及入仓实数|4入口6原公式接入保存service；NULL、负数、显式值及无关修改已验证|未导入、重算或逐行对账|旧客户端触发时机未验收|
|报价明细转调价|指定报价原行、报价头及调价头；重复办理、原色号回写、接口及事务回滚已验证|来源快照保留；原按钮与批量选择规则未证明|未完成|
|条件、字符串、舍入及日期打印|解释执行原表达式；K010原计算字段依赖已验证|旧版本舍入、NULL和日期输出未逐项比对|未完成|
|R013成品出仓及退车间校样|实际接口查询取数和生成校样通过；重复连接行、退回原行保留|未与旧库一致时点数据核对|纸张、分页外观及真实打印未完成|
|R010成品入仓版式|展开星号投影后明确检出KKind、grayQty缺失；继续列差异|未完成|未完成|

扩大回归 **{evidence['tests']['count']}项通过**（{evidence['tests']['seconds']}秒，19个模块，含本轮11项）；前端类型检查及构建通过，既有大分包提示保留。Django检查、迁移检查通过。模型仍为766个ERP模型、655个原表模型、12606个原字段，额外旧erpID为0；本轮新增迁移0、历史导入0。

完整入口开发完成0、完整入口历史对账完成0、现场验收完成0。这里的0是完整入口级别的核查结果，不否定上述已经通过测试的局部开发。

1682个查询入口继续分为1519空夹具执行通过、108财务暂缓、36未解决、19明确替代。原55处差异全部保留，36未解决中有1处FARSumMainMoney属于财务暂缓。35处非财务余项为11处缺列、2处缺本地对象、22处缺外部来源。**35不是剩余全部开发工作的总数。**

## 旧库证据边界

本轮检查到MSSQLSERVER为Stopped，未取得新的旧库查询、结构或历史数据核验。实现依据是本日已有原配置、原SQL和字段快照；上次成功只读核验时间为{evidence['old_sql_this_run']['last_success_at']}，详见证据中的缓存来源及摘要。此前连接失败是前轮记录，本轮没有新连接结果。

测试在独立测试库进行，不代表旧ERP数据已导入新项目。历史数据对账和现场验收仍单列为未完成。

## 成品收发自动公式

|原入口|目标字段|原表达式|当前执行方式|
|---|---|---|---|
|ProdOutDetail、ProdOutDetailUpdate|Amount|IsNull([Price]*[WeightQty],0)|先算金额|
|ProdOutDetail、ProdOutDetailUpdate|Total|IsNull([Amount],0)|再使用本次金额算合计|
|ProdInRecord、ProdInRecordWork|RealQty|ISNULL([WeightQty],0)|按原配置从WeightQty取值|

累计已接入43个入口、59个自动目标字段。成品价格和重量任一为NULL时，只有原Amount公式明确要求把乘积NULL变为0；不能据此把其他未知字段改为0。比如重量-2、单价3，Amount和Total均为-6，负值不删除。

显式输入目标值（包括NULL）优先；只改备注不重算；历史来源行保留原值。显式Amount=NULL而未指定Total时，Total按其自身原式为0。这里的RealQty来自旧配置，不意味着系统已经确认实称、计划和收发相等，也不合并这些数据的业务含义。

当前在新增或修改输入字段时运行这些公式。原客户端GenerateTime及强制重算时机仍未复现验证，不能将保存service实现直接标成旧自动事件全部完成。

## 报价明细明确转调价

在报价明细提供“报价转调价（保存回写关联报价）”，选择具体报价头和调价头。报价头必须与原明细同SheetSeries；重复流水的头由操作人明确选择，不能自动取第一条。

|目标字段|来源或计算|
|---|---|
|ColorNum、ColorID、ColorDepthID、CustColorNum、CustSelfProduct、ProdID、ProcessMemo|所选报价原明细同名字段|
|QuoteDetailNo、OldPrice|报价原行DetailNo、Price|
|AdjustPrice|OldPrice + 所选调价头AdjustMoney；任一NULL则保留NULL|
|CustomerID、SheetNo、SheetDate|所选报价头|

按原目标字段精度保存，原行和报价头在保存副作用之前留快照。AdjustRatio不替代AdjustMoney；例如原价10、加价-3、比例999，本次调价为7。未知FlowMain、CustSelfProdCode、FabricKindID不从近似字段猜填。

**保存会执行已有旧色号回写规则**：同数值色号关联到的全部报价原行都可能更新，不只是此次选择行；不把重复色号过滤掉。新增界面明确标注这个行为，接口检查目标新增、头修改、报价修改及相关来源可见范围。原报价基础Price不因这次转单改写，原链维护AdjustPrice等调价字段。

重复办理生成独立调价明细，并分别记录来源。审核、反审核仍沿用QuoteDetailNo原规则。选定头决定本次加价金额，但已有色号回写中DateType/StartDate仍按同流水的头及原排序规则选取；重复调价头时不宣称选择头已决定所有副作用。原按钮、批量挑选及生成时机未证明，当前属于明确办理实现。业务报错时整笔转单回滚，不留下半张单。

## 条件和复杂原打印

在先前算术、Abs及双参数IsNull基础上，新增Iif多条件分支、单参数IsNull、比较、AND/OR/NOT、IN、Len、Substring、Round、Now、Today、GetDate及AddDays。依赖既支持[字段]也支持原模板裸字段名，字符串常量中的方括号不会误当字段。Iif只计算选中分支，重复行逐行保留，不因另一分支除零而丢行。

语法和函数依据见[DevExpress表达式语言](https://docs.devexpress.com/XtraReports/120104/feature-guide-to-devexpress-reports/use-expressions/expression-language)及[官方函数说明](https://docs.devexpress.com/XtraReports/403363/feature-guide-to-devexpress-reports/use-expressions/functions-in-expressions)。官方说明包含数值比较时0与NULL相等的规则；本实现采用该规则，但当前文档不能替代旧版本客户端实测。

Round当前明确采用十进制“中点取偶”：1.245保留两位为1.24，-1.255为-1.26。旧打印版本的类型转换和中点结果尚未取得原输出对账，继续列异常。Substring按从0开始的位置取子串，越界明确报告，不自动截短；字符串与数值混合、缺字段、除零或未实现函数均保留原表达式并报告，不填0或跳行。日期采用同一份校样生成时点的业务本地时间；Now/Today与页信息不各取不同时间。跨关系聚合、脚本、子报表等仍未宣称完成。

K010原配方版式的RecipeUnitNew、Num、PhaseID_Rnew、NeedQtyNew、WeightUnit_RNew等条件依赖已用原XML验证，包括助剂、低数量、单位和舍入分支；K010整模板仍有其他运行差异。

R013（模板索引152）现可通过实际接口查询并生成填数校样。验证包含同一工卡号多条关联产生的两条出仓记录，以及两条退车间记录；原负向收发逻辑不被合并或去重。累计290条模板为 **5份填数校样、256份XML运行差异、29份缺XML、0份完整原打印**。5份校样为H002、H003、R013、R016、R102。

R010（索引149）仍缺KKind及ProdInList.grayQty。此前原查询的a.*容易掩盖缺列，本轮按本地原模型展开星号，并检查计算、绑定、排序及分组所需字段；不能把GaryWeight直接改名成grayQty来消除差异。未知外部查询的星号仍无法仅凭本地结构证明字段齐全，仍须真正取数核验。

校样未增加原打印次数，没有进行原客户端像素比较、真实纸张或设备打印验收。

## 35处非财务查询逐项保留

|原入口|当前开发状态|缺失来源/字段|历史对账|现场验收|
|---|---|---|---|---|
'''
    for row in unresolved:
        if row['scope'] != '本期保留': continue
        name = row['entry']; dependency = deps[name]
        missing = '；'.join([*dependency['external_sources'], *dependency['missing_objects'], *dependency['missing_fields']]).replace('|', '／')
        text += f'|{name}|尚无可执行替代|{missing}|未完成|未完成|\n'
    text += '''
## 后续开发顺序及保留事项

1. 补本地定义和动态填数来源：DPWPProcess缺WPProcess真实结构，EnergyPrice缺原价格实体；9处能耗查询缺列，以及vwGrayAccount/vwProdAccount的分类占位字段仍缺原客户端填数来源。原占位0不能当成真实账页数量，不创建空表或编造余额来通过核查。
2. 恢复TFEMS、TF_METER、WeighingSystem、ReportServer、Link_Pclbase、CCS等真实外部来源和字段。22处未解决查询及已有替代的染机外部部分继续保留，不能因不常用删除。
3. 继续补自动触发和转单时机。27条未绑定身份/续行、13组残缺过滤、40条原复制配置、216处事件保留；本轮明确报价转调价不冒充原40条配置中的已证明自动复制。
4. 逐模板补跨表聚合、多层组、脚本、动态高度、子报表、条码及复杂绑定；R010缺列单独跟踪，R013校样仍待原输出和纸张验收。
5. 旧库可读后按明确时点、旧原主键和完整范围逐行对账；重复、负值、NULL及逆向单据均纳入。现场真实办理、逆向、标签和设备回传单独验收。不能用开发测试替代这两个阶段。
'''
    text += '\n证据：['+EVIDENCE+']('+EVIDENCE+')；[异常E206～E210](旧ERP复刻异常与合理实现说明.md)。\n'
    (DOCS/TITLE).write_text(text, encoding='utf8')
    section = f'''## 第六阶段当前状态：成品收发、调价与条件打印（2026-10-17）

本节为最新口径，下方保留前轮记录。见[{TITLE}]({TITLE})及[验证证据]({EVIDENCE})。

本轮增加4个收发入口6条自动公式（累计43入口59目标）、报价明细明确转调价及原色号回写、条件/字符串/舍入/日期打印表达式，新增R013填数校样；R010的KKind、grayQty缺列明确保留。{evidence['tests']['count']}项扩大回归、前端类型检查/构建、模型及迁移检查通过。未新增旧erpID，本轮历史导入0。

**第六阶段仍为部分完成，35处非财务查询没有减少：11缺列、2缺本地对象、22缺外部来源。** 原55差异全部保留（19明确替代、36未解决，含1财务暂缓），35不是所有剩余工作总数。完整入口开发完成、历史对账完成、现场验收完成仍分别0。

290条原打印现为5份校样、256份XML运行差异、29份缺XML、0份完整原打印。27条未绑定身份/续行、13组残缺过滤、40条原复制配置和216处事件继续保留。异常E206～E210已记录。本轮检查旧SQL服务为Stopped，采用本日已有快照，未取得新的旧库核验结果。'''
    targets = ['染色ERP后续开发方案.md', '2026-10-16染色ERP剩余工作全量盘点清单.md',
        '2026-10-17第六阶段查询自动调用及原版式续项清单.md', '2026-10-16第六阶段旧入口自动调用与打印核查清单.md',
        '2026-10-16第六阶段未复刻入口与打印异常明细.md', '2026-10-17第六阶段字段联动与版式运行核查.md',
        '2026-10-17第六阶段查询转单及分组打印续项.md', '2026-10-17第六阶段库存查询报价转单与汇总打印续项.md',
        '2026-10-17第六阶段本地收发查询与连续分组打印续项.md', '2026-10-17第六阶段期间库存采购候选与组尾打印续项.md',
        '2026-10-17第六阶段保养领料细码复核与分页打印续项.md', '2026-10-17第六阶段染机盘点采购与计算字段打印续项.md']
    for name in targets: replace_section(DOCS/name, 'phase6-conditions-dispatch-current', section)
    inventory = read('docs/erp-remaining-inventory-20261016.json')
    current = {k: evidence[k] for k in ['query_status_counts', 'runtime_counts', 'field_copy_status_counts',
        'unresolved_nonfinancial', 'unresolved_nonfinancial_categories', 'automatic_formula_entries', 'automatic_formula_targets']}
    current.update(evidence=EVIDENCE, document=TITLE, development='部分完成', historical_reconciliation='未完成', field_acceptance='未完成')
    inventory['phase6_conditions_dispatch_20261017'] = current
    exceptions = [
        ('成品收发原NULL公式及自动时机', '4入口6公式接保存service，Amount先算、Total后算、RealQty按原WeightQty公式；显式NULL优先，历史原值保留。原公式指定的NULL转0不推广到其他字段；旧客户端时机未证明。'),
        ('报价转调价与原色号回写', '明确指定报价原行、报价头及调价头；按OldPrice+AdjustMoney，重复办理独立留档。保存触发同数值色号全部报价回写，来源在副作用前快照。重复调价头的日期回写仍沿用旧排序，比例、未知代码不猜填；原自动选择时机未证明。'),
        ('条件打印与旧版本表达式差异', '支持Iif、比较、布尔、IsNull、字符串、Round及日期。Round中点取偶、数值NULL比较、Substring和日期为已记录实现，未取得旧客户端逐项输出对账；未支持表达式/混合类型报原字段及行，不跳行补0。'),
        ('R013校样与R010真实缺列', 'R013新增实际接口取数校样，重复出仓关联与退车间记录保留；累计5份校样，完整原打印仍0。星号展开查出R010缺KKind、grayQty，不能用近似字段强配；K010仅原计算依赖验证，未完成整模板。'),
        ('三十五处查询继续保留及旧库停止', '35处仍无可执行替代（11缺列、2缺本地对象、22缺外部来源），未因其他局部开发减少。MSSQLSERVER本轮检查为Stopped，使用本日缓存，无新旧库核验；异常、重复、动态填数及外部链保留，历史对账和现场验收未完成。')]
    axis = inventory['axes']['新旧系统差异及处理情况']
    exception_md = '## E206～E210：成品收发、调价与条件打印\n\n见['+TITLE+']('+TITLE+')。\n\n'
    for number, (name, reason) in enumerate(exceptions, 206):
        exception_md += f'### E{number} {name}\n\n{reason}\n\n'
        item = {'id': 'E'+str(number), 'name': name, 'status': '部分完成', 'reason': reason, 'related_sql': [],
            'source': 'docs/旧ERP复刻异常与合理实现说明.md'}
        old = next((i for i,r in enumerate(axis) if r['id'] == item['id']), None)
        if old is None: axis.append(item)
        else: axis[old] = item
    inventory['counts']['新旧系统差异及处理情况'] = dict(Counter(r['status'] for r in axis))
    replace_section(DOCS/'旧ERP复刻异常与合理实现说明.md', 'phase6-conditions-dispatch-exceptions', exception_md)
    review = read('docs/erp-phase6-review-20261016.json')
    review['conditions_dispatch_20261017'] = current
    review['current_review_at'] = evidence['verified_at']
    inventory['phase6_review']['counts'] = review['counts']
    inventory['phase6_review']['current_evidence'] = 'docs/'+EVIDENCE
    save('docs/erp-phase6-review-20261016.json', review)
    save('docs/erp-remaining-inventory-20261016.json', inventory)
    print({'tests': evidence['tests']['count'], 'unresolved_nonfinancial': 35, 'automatic_entries': auto_entries,
        'automatic_targets': auto_targets, 'proof_templates': 5, 'document': TITLE})


if __name__ == '__main__': main()
