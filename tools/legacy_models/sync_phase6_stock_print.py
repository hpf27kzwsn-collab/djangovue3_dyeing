"""记录库存查询、报价转单及汇总校样的实测范围，不把替代实现改记等价完成。"""
import hashlib
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from sync_phase6_continuation import replace_section

ROOT=Path(__file__).resolve().parents[2]
DOCS=ROOT/'docs'
TITLE='2026-10-17第六阶段库存查询报价转单与汇总打印续项.md'
EVIDENCE='erp-phase6-stock-print-verification-20261017.json'


def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))
def save(path,value):(ROOT/path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def digest(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def main():
    support=read('backend/plugins/erp_base/source_phase6_query_support.json')
    runtime=read('docs/erp-phase6-runtime-review-20261017.json')
    live=read('.runtime-temp/phase6/stock-print-evidence/query-metadata.json')
    previous=read('.runtime-temp/phase6/continuation-evidence/query-metadata.json')
    assert live['print_hashes']==previous['print_hashes']
    assert len(live['queries'])==55 and all(r.get('error') or any(c.get('error_number') for c in r.get('columns',[])) for r in live['queries'])
    log='.runtime-temp/phase6/stock-print-regression.log'
    match=re.search(r'Ran (\d+) tests in ([\d.]+)s\s+OK',(ROOT/log).read_text(encoding='utf8'))
    assert match,log
    schema=read('.runtime-temp/phase6/final-schema-check.json')
    schema['snapshot_comparison_note']='结构/程序/界面相等结论引用本日较早的已保存快照；本轮重新连接旧库的是55项查询元数据及290份打印摘要。'
    unresolved=[{'entry':n,'category':v['live_original']['category'],'error':v['error'],
                 'scope':'财务暂缓' if n=='FARSumMainMoney' else '本期保留',
                 'historical_reconciliation':'未完成','field_acceptance':'未完成'}
                for n,v in support.items() if v['query_state']=='unresolved']
    replacements=[n for n,v in support.items() if v['query_state']=='reconstructed_missing_projection']
    files=['backend/plugins/erp_base/'+n for n in ['source_phase6_reconstructions.py','source_phase6_transfers.py',
        'source_phase6_auto_values.py','source_phase6_print_rules.py','source_phase6_rendering.py','source_phase6_layouts.py',
        'source_phase6_entries.py','source_phase6_query_support.json','source_phase6_forms.py','source_api.py',
        'tests/test_source_phase6_stock_print.py']]+['web/src/plugins/erp/OriginalEntryWorkbench.vue']
    evidence={'verified_at':datetime.now().astimezone().isoformat(),'development':'部分完成',
        'query_status_counts':dict(Counter(v['query_state'] for v in support.values())),
        'original_query_differences':len(unresolved)+len(replacements),'explicit_query_reconstructions':replacements,
        'unresolved_queries':unresolved,'unresolved_categories':dict(Counter(v['category'] for v in unresolved)),
        'scope_note':'48处待办中FARSumMainMoney为销售收入汇总，按本期忽略财务要求暂缓；仍保留原清单行，不算开发完成。',
        'new_quantity_reconstructions':['vwGrayStockByCheck','vwProdStockByCheck','ProdStockToProdOut','GrayCurrentStockQuery'],
        'automatic_amount_entries':['PurDetail','ArticlePurDetail','DStuffOutDetail','SmallStuffOutDetail','StuffOutDetail','SmallStuffInDetail','StuffInDetail','StuffAllotDetail'],
        'runtime_counts':runtime['counts'],'field_copy_status_counts':runtime['field_copy_status_counts'],
        'tests':{'count':int(match[1]),'seconds':float(match[2]),'result':'passed','log':log,'sha256':digest(log),
                 'scope':'第六阶段六组旧测试、新增库存/转单/汇总用例及报价打样、采购质量、库存共10个模块；不是全项目重跑。'},
        'frontend':{'result':'typecheck_and_build_passed','log':'.runtime-temp/phase6/stock-print-frontend.log',
                    'note':'构建通过，保留既有部分分包体积大于500kB的提示。'},
        'schema':schema,'old_sql_readonly_metadata':live,'old_print_hashes_equal_previous':True,
        'browser_proof':{**read('.runtime-temp/phase6/stock-print-proof/proof.json'),
                         'result':'浏览器核对71条合成行、3页及末页491/3/-70/140汇总；不是现场验收。'},
        'whole_entry_historical_reconciled':0,'field_accepted':0,'historical_import_rows_this_run':0,
        'files_sha256':{p:digest(p) for p in files}}
    save('docs/'+EVIDENCE,evidence)
    content='''# 第六阶段库存查询、报价转单与汇总打印续项

日期：2026-10-17。本轮承接上一轮52处待办查询。财务暂缓，不新增旧erpID；原表原键、重复记录、负数、NULL及中间留档继续保留。

## 结果与统计口径

|事项|开发与必要验证|历史数据对账|现场验收|
|---|---|---|---|
|4处库存查询|明确数量维度和缺列替代已实现，非空/重复/NULL及接口CSV验证通过；不是原式等价完成|旧原式仍无法编译，未完成同口径对账|未完成|
|报价转订单|明确选定报价头和行的转单已实现，10列替代映射、1列手工指定；重复来源、事务及接口验证通过|缺原联查视图，未完成历史转单结果对账|未完成|
|8入口金额公式|原数量×单价公式自动保存已实现，本轮新增7入口；显式金额优先，测试通过|未完成全量历史对账|未完成|
|原R016打办月份统计表|报告级汇总、分页及非空查询到校样路径已验证；71条合成行分3页经浏览器核查|未完成原客户端打印结果对账|纸张、字体、打印机未验收|
|原R155订单交货情况|识别未引用计算声明，并新增原查询与打印绑定检查；缺失绑定逐项列明，尚不能生成完整原打印|未完成|未完成|

本轮187项扩大回归全部通过（56.822秒），前端类型检查与构建通过，Django检查及迁移检查通过。模型仍为766个ERP模型、655个原表模型、12606个原字段；本轮新增迁移0、额外旧erpID字段0。测试使用隔离测试库，本轮历史业务导入0，不能把测试记录数量当作历史导入数量。

55处旧查询差异没有从清单移除：其中7处已有公开替代（此前3处、本轮4处），48处仍不能运行。48处按旧库首个编译阻断分类为14处缺列、11处缺本地对象、23处缺外部库或链接；这是首错分类，单条可能同时缺多种依赖。其中FARSumMainMoney是销售收入汇总，本期按财务暂缓处理，不列入下一步非财务开发，也不算完成；其余47处继续保留。

原打印290条中可填数校样由2条增加为3条：H002打样任务明细A、H003打样任务明细B、R016打办月份统计表。完整原打印运行仍为0；其余258条有XML但存在运行差异，29条没有XML。290是原配置全量数，包含财务归档配置，财务不进入本期开发。

## 4处库存查询如何取数

界面新增“重量原数值/长度原数值”选择，服务端要求明确传入QuantityBasis。没有用StockUnit的未知枚举推断旧Qty，也没有将重量与长度相加或做隐含单位换算。历史台账字段保持原值。

|原入口|本轮明确实现|仍有差异|
|---|---|---|
|vwGrayStockByCheck|将GrayStockBook的InWeightQty/OutWeightQty或InLengthQty/OutLengthQty投影为原InQty/OutQty，保留原UNION ALL、类别筛选及入库重复关联|JobDetailNo、FabricID原列已缺失，显示NULL；原Qty口径不能证明|
|vwProdStockByCheck|按所选维度投影成品台账，保留原入出分类、汇总和同单号多入库头连接|ProdKindID已缺失，显示NULL；原Qty口径不能证明|
|ProdStockToProdOut|缺失vwProdStockBook时，明确按最新ProdStockBook的SheetNo汇总，再关联全部同号ProdIn；保留Qty>0筛选及两处同名SheetNo投影|缺原视图，无法证明原视图的全部筛选、分组和NULL规则；ProdKindID显示NULL|
|GrayCurrentStockQuery|使用现存vwGrayStockBook的WeightQty或LengthQty，保留其内部与原外层的重复连接|FabricID、Structure缺失，返回NULL；另列GrayID作为明确替代分组，不能冒充原FabricID|

NULL运算按各自原式保留。例如盘点中InQty=NULL、OutQty=3的原减法仍为NULL，不擅自当成-3。原现存坯料视图自身有ISNULL的地方则继续执行其原式。重复2个表头×2个明细的嵌套连接可能放大至16份，测试明确保留此结果，不自行去重或“纠正”旧连接。CSV保留重复行、重复列名，继续用\\N区别NULL和空字符串。

本轮Windows身份只读核查55处原查询的结果集元数据，55处仍报编译错误；核查原打印的290组字节摘要与上一轮一致。没有执行这55条业务查询、没有取得其历史结果，不能据此标记历史对账。结构/程序/界面相等结论引用本日较早的已保存快照，未冒充本轮重新全量抽取。

## 报价转新订单

报价明细提供“报价转新订单（明确来源）”动作，必须明确选定报价表头；同SheetSeries的多个原头可以分别选择，不取任意第一条。服务在事务内新建OrderMain和OrderColor，再一次执行整单联动；重复办理生成不同订单，不按来源ID、单号或内容去重。

从所选Quote复制BusinessUnitID、CurrencyID、CustomerID、ExchangeRate、Linker、SalerID、SettleID七列，从QuoteDetail取PriceUnit写订单头、Price和Spec写订单行，共10列明确替代映射。原vwQuoteMDToOrderMD不存在，所以不声称已还原其选择条件或旧按钮时机。

原FabricID由动作参数明确指定，也可保留NULL；不把QuoteDetail.ProdID当作FabricID。原目标OrderColor.Structure已不存在，原报价Structure存入已有来源上下文；OrderMain.PreUnitProfit字段已不存在且来源未知，记录为未知。头、行完整来源快照均保留，不新加业务模型字段。

40条原复制配置现在分别为：7条显式采购转到货；10条明确报价头/行替代；1条物料明确指定；2条目标字段已缺失；3条配置不完整；17条财务暂缓。各项均有逐行记录，见字段与版式运行核查附表。

## 金额自动触发

PurDetail、ArticlePurDetail、DStuffOutDetail、SmallStuffOutDetail、StuffOutDetail、SmallStuffInDetail、StuffInDetail、StuffAllotDetail八个入口的原公式均为Amount=[Qty]*[Price]。两个采购入口GenerateTime为0，其余六个为空。原客户端枚举/空值触发含义仍缺证据，当前明确采用新增行或修改数量/价格时计算，不擅自推广其它公式。

计算在service保存层完成。显式提交Amount包括NULL时优先保留；修改无关字段不重算；负数和数量/单价NULL按原数值传播。历史导入识别保持现有逻辑，历史原值不触发新计算。新表单使用自动默认值时将未填金额交给服务，选择保留手填值则不覆盖。216处原事件绑定仍按逐入口证据处理，不能因八条公式接入就整体升级完成。

## 原打印汇总与具体缺项

R016按原XML汇总DNum、WNum、TNum、MNum，Report范围跨页累计，重复行计入；原IgnoreNullValues=true继续生效。支持报告级Sum/Count/Avg/Min/Max；汇总默认Sum、IgnoreNullValues默认false（计入时按0）、TreatStringsAsNumerics默认true。数值字符串按数值处理；明确关闭字符串转换时的文本Min/Max使用Unicode比较，旧区域排序仍待核对。无法转换的文本明确指出原行问题，不能跳过或变成0。

这些默认语义参考[DevExpress Func](https://docs.devexpress.com/XtraReports/DevExpress.XtraReports.UI.XRSummary.Func)、[IgnoreNullValues](https://docs.devexpress.com/XtraReports/DevExpress.XtraReports.UI.XRSummary.IgnoreNullValues)及[TreatStringsAsNumerics](https://docs.devexpress.com/XtraReports/DevExpress.XtraReports.UI.XRSummary.TreatStringsAsNumerics)当前官方文档。旧模板所用组件版本的逐值对照尚未完成，因此仍计为校样，不计完整原打印。

R016名称是月份统计表，但保存的qryDyeDipsRecord原SQL本身没有月份参数；当前按该入口返回的全部行填数，不能宣称已经还原旧客户端月份过滤。本轮浏览器71行合成数据得到3页，末页合计491、3、-70、140；另有API测试使用真实模型夹具走查询、员工显示名和校样生成，二者不是历史生产数据。

计算字段按实际绑定和依赖链识别，未引用的原声明保留，不执行无关表达式。R155有PKG和calculatedField3两个未引用声明，但仍缺当前取数：

'''
    blocked=next(r for r in runtime['templates'] if r['index']==276)
    content+='\n'.join('- '+v for v in blocked['runtime_issues'])+'\n\n'
    content+='''不能把OrderQty当作OrderRolls，也不能用最新ProdOutQty冒充原ProdOutWeightQty，更不能给退货量或库存量填0。缺失映射进入异常E183，原模板保留。其余原脚本、多栏、组/页汇总、子报表、条码、动态高度和跨表参数仍有实现工作；没有统一归为“缺外部资料”。

## 后续实际顺序

1. 继续处理下表非财务查询。按依赖区分本地列变更、本地旧对象丢失和外部来源；能给出明确替代的写代码并做非空对照，其余逐项保留缺失定义和所需来源。7处替代的原口径差异继续待核对。
2. 自动触发继续按原入口与事件补齐，重点是主从整批保存、GenerateTime/IsEnForceExpress/RelyRule以及QueryWorkList2缺失RecordYieldCheck。27处未绑定身份/续行配置、13组残缺上下文过滤仍登记，不能归入已完成。
3. 转单继续补齐缺失报价视图的原来源条件、3条残缺复制目标及旧客户端按钮时机；本轮明确转单可用不代表旧操作完全等价。
4. 原打印优先补当前查询到R155所缺的收发/退货/库存字段链，再处理各模板的计算、组/页汇总、脚本、跨表绑定及条码。R016月份过滤也单独待补；按模板校验每一个绑定，不能仅统计XML可解析数量。
5. 对已通过代码和非空验证的功能，另行开展一致时点历史对账与现场验收。原数据异常、不常用流程和重复记录继续纳入验证范围。

## 48处查询待办逐项保留

下表为原清单余项，含1处财务暂缓；全部不是已完成。各行历史对账、现场验收均未完成。最新原库首错详见本轮验证JSON。

|原入口|原库首错类别|本期范围|新实现当前缺项|
|---|---|---|---|
'''
    for row in unresolved:
        content+='|'+row['entry']+'|'+row['category']+'|'+row['scope']+'|'+row['error'].replace('|','／').replace('\n',' ')+'|\n'
    content+='\n证据：['+EVIDENCE+']('+EVIDENCE+')。原配置全量字段、复制行及290条打印逐项差异见[字段联动与版式运行核查](2026-10-17第六阶段字段联动与版式运行核查.md)。\n'
    (DOCS/TITLE).write_text(content,encoding='utf8')
    section=f'''## 第六阶段当前状态：库存查询、报价转单和汇总校样（2026-10-17）

本节取代下方前轮数量作为当前口径。见[{TITLE}]({TITLE})及[本轮实测证据]({EVIDENCE})。

本轮新增4处库存查询明确替代、报价转订单（10列替代映射、1列明确指定）、7个入口金额自动计算及R016报告汇总校样。187项扩大回归、前端类型检查与构建、模型及迁移检查通过。不新增旧erpID，本轮历史导入0。

**第六阶段仍为部分完成。** 原55处查询差异中7处已有公开替代、48处仍不能运行（14缺列、11缺本地对象、23缺外部来源；其中销售收入汇总1处财务暂缓，其余47处继续开发）。这不是将7处计作等价完成。原打印290条中可填数校样3条，完整原打印运行0条；R155实际缺少取数列，不计可用校样。

40条复制配置：7采购显式转单、10报价替代映射、1物料明确指定、2缺目标字段、3配置残缺、17财务暂缓。216原事件仍逐入口验证，27处身份/续行未绑定、13组上下文过滤残缺继续保留。异常新增E179～E183；异常和重复记录不删除、不跳过。

开发验证、历史数据对账、现场验收分别记录。完整入口开发完成0、完整入口历史对账完成0、现场验收完成0的严口径不因局部功能完成上调。后续先处理非财务查询来源和自动时机，再补原转单条件与复杂打印取数；详见续项文档。'''
    targets=['染色ERP后续开发方案.md','2026-10-16染色ERP剩余工作全量盘点清单.md',
        '2026-10-17第六阶段查询自动调用及原版式续项清单.md','2026-10-16第六阶段旧入口自动调用与打印核查清单.md',
        '2026-10-16第六阶段未复刻入口与打印异常明细.md','2026-10-17第六阶段字段联动与版式运行核查.md',
        '2026-10-17第六阶段查询转单及分组打印续项.md']
    for name in targets:
        replace_section(DOCS/name,'phase6-stock-print-current',section)
    inventory=read('docs/erp-remaining-inventory-20261016.json')
    current={k:evidence[k] for k in ['query_status_counts','runtime_counts','field_copy_status_counts','unresolved_categories']}
    current.update(evidence=EVIDENCE,document=TITLE,development='部分完成',historical_reconciliation='未完成',field_acceptance='未完成')
    inventory['phase6_stock_print_20261017']=current
    for row in inventory['axes']['旧界面配置入口']:
        if row['name'] in replacements:
            row['phase6_query']={**support[row['name']],'state':support[row['name']]['query_state']}
            row['status']='部分完成'
            row['reason']='明确替代查询可运行；原口径、自动时机、打印或真实对账仍有差异，不能计作等价完成。'
            row['development']={'status':'部分完成','reason':row['reason']}
            row['phase6_evidence']='docs/'+EVIDENCE
    inventory['counts']['旧界面配置入口']=dict(Counter(r['status'] for r in inventory['axes']['旧界面配置入口']))
    titles=['库存Qty维度和原重复连接','报价转单的明确来源与缺失目标','八入口金额保存的替代时机','报告级汇总、原默认值与月份过滤','订单交货原打印缺失绑定']
    axis=inventory['axes']['新旧系统差异及处理情况']
    for number,title in enumerate(titles,179):
        row={'id':'E'+str(number),'name':title,'status':'部分完成','reason':'已开发的明确替代、未实现原口径、历史对账及现场验收分别列明。',
             'related_sql':[],'source':'docs/旧ERP复刻异常与合理实现说明.md'}
        prior=next((i for i,r in enumerate(axis) if r['id']==row['id']),None)
        if prior is None:axis.append(row)
        else:axis[prior]=row
    inventory['counts']['新旧系统差异及处理情况']=dict(Counter(r['status'] for r in axis))
    save('docs/erp-remaining-inventory-20261016.json',inventory)
    review=read('docs/erp-phase6-review-20261016.json');review['stock_print_20261017']=current
    review.setdefault('pre_stock_print_counts',review['counts'].copy())
    indexed={r['name']:r for r in inventory['axes']['旧界面配置入口']}
    for row in review['entries']:
        if row['name'] in replacements:
            source=indexed[row['name']]
            row['development']=source['development'];row['query']=source['phase6_query']
    review['counts']['query_execution']=evidence['query_status_counts']
    review['counts']['development']=dict(Counter(r['development']['status'] for r in review['entries']))
    review['counts']['development']['开发完成']=0
    review['current_review_at']=evidence['verified_at']
    save('docs/erp-phase6-review-20261016.json',review)
    inventory['phase6_review']['counts']=review['counts']
    inventory['phase6_review']['current_evidence']='docs/'+EVIDENCE
    save('docs/erp-remaining-inventory-20261016.json',inventory)
    exceptions='''## E179～E183：库存、报价和报告汇总本轮差异

本轮实现和完整余项见[库存查询报价转单与汇总打印续项](2026-10-17第六阶段库存查询报价转单与汇总打印续项.md)。开发、历史对账、现场验收分别记录，所有原配置与异常原行保留。

### E179 库存Qty维度和原重复连接

4处入口改为明确选择重量或长度原数值，不按StockUnit猜单位。缺少的展示列为NULL，原盘点UNION ALL、类别条件、NULL减法和重复连接保留；ProdStockToProdOut的缺失视图明确按最新台账SheetNo汇总替代。GrayCurrentStockQuery缺FabricID/Structure，另用GrayID分组并公开差异，不将其混作同一字段。原库查询无法编译，替代测试通过不能计作等价或历史对账完成。

### E180 报价转单的明确来源与缺失目标

原vwQuoteMDToOrderMD缺失，新动作选定具体报价头/行。10列按可证明原字段给出公开替代，FabricID由明确参数指定或留NULL，不能猜测ProdID关系。目标Structure已缺失，原值留上下文；PreUnitProfit来源和目标均无法恢复，记录未知。重复头、重复行和重复转单分别保留。7条采购映射、11条报价相关配置、2条缺目标、3条残缺、17条财务合计40条，未因替代开发从原差异清单删除。

### E181 八入口金额保存的替代时机

8条Amount原式均为Qty*Price；原GenerateTime两条为0、六条为空，当前采用新增/修改输入时计算的公开时点。显式Amount包括NULL优先、负数和原NULL继续传播；历史行不重算。不泛化原时机枚举，不加吞错、补0或跳过异常行。7条为本轮新增，PurDetail是上一轮已有。

### E182 报告级汇总、原默认值与月份过滤

R016恢复Report级汇总和固定高度分页，重复行计入、负数及原空值规则保留，71行3页校样核查通过。部分默认规则依据现行DevExpress文档实现，旧版本逐值结果尚未验证。原查询无月份条件，旧客户端月份过滤仍未还原；不能把标题为月表等同于已按月过滤。完整原打印运行仍为0，历史打印对账和设备验收未完成。

### E183 订单交货原打印缺失绑定

R155的PKG、calculatedField3虽未被引用，原声明仍完整保存。其打印绑定与最新qry_Order_ToCustomer已经不一致：AssignUnit_R、FabricKindID_R、OrderRolls、ReceSheetNo、各收发/退货数量、CurrRolls/CurrGrayQty/CurrWeightQty、出货率及完成情况等缺来源。运行前逐项列明，不能填0、拿近似列替代或把合成齐全列的渲染算作实际查询可打印。此项仍有代码和取数对应待补，不仅是现场验收。
'''
    replace_section(DOCS/'旧ERP复刻异常与合理实现说明.md','phase6-stock-print-exceptions',exceptions)
    print(json.dumps({'tests':evidence['tests']['count'],'query_states':evidence['query_status_counts'],
                      'proof_templates':runtime['counts']['fixed_proof_templates'],'document':TITLE},ensure_ascii=False))


if __name__=='__main__':main()
