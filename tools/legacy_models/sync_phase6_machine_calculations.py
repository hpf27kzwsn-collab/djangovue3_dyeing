"""同步染机、盘点、申请转采购及计算字段续项；未取得的新旧库核验不计完成。"""
import re
from collections import Counter
from datetime import datetime
from sync_phase6_local_chains import ROOT,DOCS,read,save,digest
from sync_phase6_continuation import replace_section

TITLE='2026-10-17第六阶段染机盘点采购与计算字段打印续项.md'
EVIDENCE='erp-phase6-machine-calculations-verification-20261017.json'


def main():
    support=read('backend/plugins/erp_base/source_phase6_query_support.json')
    runtime=read('docs/erp-phase6-runtime-review-20261017.json')
    previous=read('docs/erp-phase6-references-pages-verification-20261017.json')
    deps=read('docs/erp-phase6-query-dependencies-20261017.json')
    log='.runtime-temp/phase6/machine-calculations-regression.log'
    match=re.search(r'Ran (\d+) tests in ([\d.]+)s\s+OK',(ROOT/log).read_text(encoding='utf8'))
    assert match,log
    build='.runtime-temp/phase6/machine-calculations-frontend.log'
    assert 'built in' in (ROOT/build).read_text(encoding='utf8')
    unresolved=[{'entry':n,'category':v['live_original']['category'],'error':v['error'],
        'scope':'财务暂缓' if n=='FARSumMainMoney' else '本期保留'} for n,v in support.items() if v['query_state']=='unresolved']
    replacements=[n for n,v in support.items() if v['query_state']=='reconstructed_missing_projection']
    schema=read('.runtime-temp/phase6/final-schema-check.json')
    schema['snapshot_comparison_note']='此处结构相等只引用本日已保存快照。本轮MSSQLSERVER已停止，未取得新的旧库结构/查询/打印核验。Django检查及迁移检查为本轮实际运行。'
    files=['backend/plugins/erp_base/'+n for n in ['source_phase6_reference_queries.py','source_phase6_query_support.json',
        'source_phase6_auto_values.py','source_phase6_transfers.py','source_phase6_forms.py','source_api.py',
        'source_phase6_calculated_print.py','source_phase6_print_rules.py','source_phase6_rendering.py',
        'tests/test_source_phase6_machine_calculations.py']]
    evidence={'verified_at':datetime.now().astimezone().isoformat(),'development':'部分完成',
        'query_status_counts':dict(Counter(v['query_state'] for v in support.values())),
        'original_query_differences':len(unresolved)+len(replacements),'explicit_query_reconstructions':replacements,
        'new_query_reconstructions':['vw_DyeMachine'],'unresolved_queries':unresolved,
        'unresolved_nonfinancial':sum(r['scope']=='本期保留' for r in unresolved),
        'unresolved_nonfinancial_categories':dict(Counter(r['category'] for r in unresolved if r['scope']=='本期保留')),
        'automatic_formula_entries':39,'automatic_formula_targets':53,
        'new_formula_entries':['GrayStockAdjustDetail','ProdStockAdjustDetail','SemiStockAdjustDetail'],
        'new_transfer_variants':['ArticleDeptApplyDetail -> ArticlePurDetail','StuffDeptApplyDetail -> StuffPurDetail'],
        'runtime_counts':runtime['counts'],'field_copy_status_counts':runtime['field_copy_status_counts'],
        'tests':{'count':int(match[1]),'seconds':float(match[2]),'result':'passed','log':log,'sha256':digest(log),
            'scope':'18个模块扩大回归，含本轮10项；不是全项目重跑或历史数据对账'},
        'frontend':{'result':'typecheck_and_build_passed','log':build,'sha256':digest(build),'note':'既有大分包提示保留'},
        'schema':schema,'old_sql_this_run':{'status':'connection_failed','service':'MSSQLSERVER','service_status':'Stopped',
            'error':'Named Pipes Provider error 40；本轮只读连接未成功，未获取查询元数据或打印摘要',
            'last_success_evidence':'erp-phase6-references-pages-verification-20261017.json',
            'last_success_at':previous['old_sql_readonly_metadata']['captured_at']},
        'cached_structure_source':{'path':'.runtime-temp/phase6-live-20261017-current/structure-and-logic.json',
            'sha256':digest('.runtime-temp/phase6-live-20261017-current/structure-and-logic.json')},
        'print_validation':'算术、Abs、双参数IsNull、依赖顺序、NULL、重复行、除零/缺来源以及R127原公式经过验证；未新增完整原模板，未做像素外观/现场打印验收。',
        'whole_entry_development_completed':0,'whole_entry_historical_reconciled':0,'field_accepted':0,
        'historical_import_rows_this_run':0,'files_sha256':{p:digest(p) for p in files}}
    assert evidence['unresolved_nonfinancial']==35 and len(replacements)==19
    assert runtime['counts']['fixed_proof_templates']==4
    save('docs/'+EVIDENCE,evidence)
    text=f'''# 第六阶段染机、盘点、申请转采购与计算字段打印续项

日期：2026-10-17。承接36处非财务查询余项；财务暂缓，不新增旧erpID，不跳过异常和重复数据。

## 当前结果与完成标准

**第六阶段仍为部分完成，未将任何完整旧入口升级为开发完成。** 本轮补1处染机本地查询、3入口10条自动公式、2种部门申请明确转采购，以及原打印逐行计算字段。

尚无可执行替代的非财务查询从36变为35：11处缺列、2处缺本地对象、22处缺外部来源。vw_DyeMachine仍缺外部中控编号及关联行数，只恢复本地资料，不是外部链已接通。原55处差异继续全部保留，累计19处明确替代、36处未解决（含FARSumMainMoney财务暂缓）。**35不是剩余全部开发工作数量，查询有替代不等于完整旧业务已复刻。**

全部1682查询入口：1519空夹具执行通过、108财务暂缓、36未解决、19明确替代。空夹具执行或局部能力通过不能当作完整入口完成。

|本轮事项|开发与必要验证|历史数据对账|现场验收|
|---|---|---|---|
|vw_DyeMachine|本地机台原筛选及重复行查询已验证，中控编号为未知|缺外部Machines，关联行数与编号未对账|未完成|
|坯布、成品、半成品盘点差额|3入口10原公式、显式NULL优先、历史值保留已验证|未重算/导入历史行，未逐行对账|原自动时机未确认|
|机物料、染化料部门申请转采购|明确原行/头、数量、单价、重复办理、来源留档及接口已验证|原候选筛选保留，旧按钮及合并转单时机仍缺证据|未完成|
|原打印计算字段|算术、Abs、双参数IsNull、依赖顺序及R127原公式已验证|原客户端NULL/类型/区域输出尚未逐项对比|未完成|

扩大回归{evidence['tests']['count']}项通过（{evidence['tests']['seconds']}秒，18个模块，含本轮10项），前端类型检查及构建通过；既有大分包提示保留。Django检查和迁移检查通过。仍为766个ERP模型、655个原表模型、12606个原字段、额外旧erpID为0；本轮新增迁移0、历史导入0。

完整入口开发完成0、完整入口历史对账完成0、现场验收完成0，局部开发测试结果单独记录。

## 本轮旧库核验限制

本轮只读连接失败，服务检查为MSSQLSERVER=Stopped。没有取得新的旧表结构、查询元数据或打印摘要。本轮实现依据为今天已保存的原配置、视图和字段快照；上次成功只读查询核验时间为{evidence['old_sql_this_run']['last_success_at']}。此前55条原SQL编译错误及290份打印摘要是此前证据，不能写成本轮重新核验通过。

当前模型检查和测试使用项目独立测试数据库，与旧ERP数据导入无关。测试库此前未运行，本轮启动已有测试实例后执行回归；没有执行业务历史导入。

## 染机本地查询

原vw_DyeMachine定义是p_Machine左连接外部CCS Machines，连接条件为本地MachineNo=外部MachineId，并筛选MachineType=50。本轮保留MachineNo、MachineID、Name、MaxWaitVats及原筛选；缺失的LX_MachineId明确返回NULL。不会将MachineNo直接认作已核准的中控编号。

同代码多条本地机台全部展示，缺MachineNo的原行保留，负MaxWaitVats原值不修正。外部存在多条匹配时的倍增行数无法从本地推断，所以查询仍是明确替代，不能用于宣称中控回传、程序选择或设备接入完成。

## 盘点自动差额

以下原表达式逐入口核对后接入保存service：

|入口|自动字段|原公式|
|---|---|---|
|GrayStockAdjustDetail、ProdStockAdjustDetail、SemiStockAdjustDetail|AdjustLengthQty|ISNULL(RealLengthQty,0) − ISNULL(PaperLength,0)|
|同上|AdjustRolls|ISNULL(RealRolls,0) − ISNULL(PaperRolls,0)|
|同上|AdjustWeightQty|ISNULL(RealWeightQty,0) − ISNULL(PaperWeight,0)|
|仅GrayStockAdjustDetail|AdjustPacks|ISNULL(RealPacks,0) − ISNULL(PaperPacks,0)|

长度、重量、粒数、包数分别计算，不互相换算。原式明确ISNULL才把该输入NULL按0参与运算；手工传入的目标值（包括NULL）优先，修改无关字段不重算，历史原行不改。比如实盘NULL、账面5，差额按原式为-5；这不代表系统自动确认真实实盘为0。

累计自动计算39个入口、53个目标字段。本轮不更改库存过账流程，不把保存时计算当成已验证旧GenerateTime和强制计算时机。

## 部门申请明确转采购

原ArticlePurApplyToPur及StuffPurApplyToPur查询仍保留RightStatus=10、NOT EXISTS及原GROUP BY。它们给出聚合候选，不直接当成某一条原明细。本轮在原部门申请明细上新增“部门申请转采购（明确原行）”，允许用户选择具体申请表头及采购表头，明确本次Qty和Price。

|来源|目标入口与表头|复制字段|
|---|---|---|
|ArticleDeptApplyDetail + 明确ArticleDeptApply头|ArticlePurDetail / ArticlePurMain|ArticleID、ArticleKindID；Name→ArticleName，Unit→ArticleUnit|
|StuffDeptApplyDetail + 明确StuffDeptApply头|StuffPurDetail / StuffPurMain|StuffID、StuffKindID；Name→StuffName，Unit→StuffUnit|

两种目标都使用原PurDetail模型。ApplySheetNo取选定申请头SheetNo；目标SheetSeries和明细编号走现有主从编号链。Qty/Price来自本次明确输入，Amount按Qty×Price生成，原申请Qty/Amount保存在已有上下文快照。单位原样复制，不作换算。

申请头必须与明细同流水；同流水多表头由用户明确选择，不自动取第一条。重复转入每次形成独立明细，完整保留原行和头的快照。原查询因已经转入而不再显示某候选，不影响通过原明细明确再次办理；未审核或不常用来源也不会因候选未显示而被删除。目标已确认/审核时沿用现有重新办理要求，整个动作事务提交。

**字段不能原样容纳的具体差异：** 申请Remarks允许NULL，目标PurDetail.Remarks原字段不允许NULL，所以目标写空字符串，来源快照保留原NULL。不是悄悄丢弃备注；普通字符串、空白和重复文本照原值复制。其他未知数量、单价、物料与单位按目标允许的NULL保留。原自动按钮、聚合行如何拆回原明细及合并转单规则仍未证明，因此这两种操作是明确实现。

## 原打印计算字段

在原XML计算字段中，补逐行加减乘除、正负号、Abs和双参数IsNull；按实际引用递归计算依赖，字段名称匹配不区分大小写。未引用的旧计算定义仍保留，不因其中存在未支持函数而删除模板内容。仅执行已支持的表达式，不执行模板中的任意程序代码。

计算列参与现有排序、分组、页/组/报表汇总。原查询行不修改，重复行各自计算。普通算术遇NULL明确传播NULL，IsNull只按原式指定的替代值计算；除零、缺来源、重复投影或类型冲突报告原行和字段，不能跳过行或填0生成假结果。计算列与原投影重名时明确报告，不能覆盖原数据。

R127的ZRolls=Abs(Rolls)、ZWeightQty=Abs(WeightQty)原XML算式已用负数、重复行和NULL验证，但R127仍有其他版式差异，不因此列为完整可打印。计算字段能力不包含Iif、Round、跨表聚合、脚本、动态高度或多层分组；未支持原式仍逐模板列出。

计算字段引用及类型依据见[DevExpress表达式说明](https://docs.devexpress.com/XtraReports/DevExpress.XtraReports.UI.CalculatedField.Expression)和[函数说明](https://docs.devexpress.com/XtraReports/403363/feature-guide-to-devexpress-reports/use-expressions/functions-in-expressions)。当前官方文档与旧版本不等同，NULL传播、类型转换和最终外观仍按“明确实现、待原客户端对账”记录。

原290份模板仍为4份可填数校样、257份XML运行差异、29份缺XML、0份完整原打印。未增加打印次数，没有浏览器像素、真实纸张或设备打印验收。

## 本轮36处查询逐项记录

本表保留本轮起点全部36处，已增加本地替代的vw_DyeMachine仍列原外部差异。

|原入口|当前开发状态|缺失来源/字段|历史对账|现场验收|
|---|---|---|---|---|
'''
    indexed_deps={r['entry']:r for r in deps['entries']}
    for row in previous['unresolved_queries']:
        if row['scope']!='本期保留':continue
        name=row['entry'];d=indexed_deps[name]
        state='本地资料明确替代；中控来源仍缺' if name=='vw_DyeMachine' else '尚无可执行替代'
        missing='；'.join([*d['external_sources'],*d['missing_objects'],*d['missing_fields']]).replace('|','／')
        text+=f'|{name}|{state}|{missing}|未完成|未完成|\n'
    text+='''
## 后续顺序

1. 继续补本地定义与客户端动态填数：DPWPProcess仍缺WPProcess实际结构；EnergyPrice仍缺原价格实体与历史记录；vwGrayAccount/vwProdAccount旧分类占位0没有找回填数来源，不能当真实账页。11处能耗/账页缺列继续逐条保留。
2. 22处尚无替代的外部查询及vw_DyeMachine外部部分，等待可验证的原库/链接定义与数据。TFEMS、TF_METER、WeighingSystem、ReportServer、Link_Pclbase、CCS都不是本地近似表可以等价替代的来源，不据此删除不常用链条。
3. 继续恢复自动及转单时机。保留27条未绑定身份/续行、13组残缺过滤、40条复制配置、216处事件；本轮两个明确办理动作不冒充这40条配置的自动映射数量。
4. 复杂原打印继续逐模板补Iif/日期/字符串/聚合算式、多层组、脚本、动态高度、子报表、条码及数据绑定。已支持算式不意味着整模板运行完成。
5. 旧库可读时再取得一致时点数据，按旧表原主键和明确范围逐行对账；真实办理、逆向、纸张、标签及设备回传独立现场验收。当前这两项均未完成，本轮开发测试不能替代。
'''
    text+='\n证据：['+EVIDENCE+']('+EVIDENCE+')；[异常E201～E205](旧ERP复刻异常与合理实现说明.md)。\n'
    (DOCS/TITLE).write_text(text,encoding='utf8')
    section=f'''## 第六阶段当前状态：染机、盘点、采购与计算字段打印（2026-10-17）

本节为最新口径，下方为前轮历史记录。见[{TITLE}]({TITLE})和[验证证据]({EVIDENCE})。

本轮补vw_DyeMachine本地资料查询、3入口10自动差额（累计39入口53条）、机物料/染化料部门申请明确转采购，以及逐行算术、Abs、IsNull打印计算字段。{evidence['tests']['count']}项扩大回归、前端类型检查/构建、模型及迁移检查通过；未新增旧erpID，本轮历史导入0。

**第六阶段仍为部分完成。** 原55差异全部保留：19明确替代、36未解决（含1财务暂缓）。非财务“无可执行替代查询”36→35（11缺列、2缺本地对象、22缺外部来源）；染机外部编号仍缺，35不是剩余全部工作数量。完整入口开发完成、历史对账完成、现场验收完成仍分别0。

原打印仍4份校样、257份XML运行差异、29份缺XML、0份完整复刻。27条未绑定身份/续行、13组残缺过滤、40条复制配置、216处事件仍保留。异常E201～E205已记录。**本轮旧SQL Server服务停止，只读连接失败；采用本日已有快照，没有新的旧库核验结果。**'''
    targets=['染色ERP后续开发方案.md','2026-10-16染色ERP剩余工作全量盘点清单.md',
        '2026-10-17第六阶段查询自动调用及原版式续项清单.md','2026-10-16第六阶段旧入口自动调用与打印核查清单.md',
        '2026-10-16第六阶段未复刻入口与打印异常明细.md','2026-10-17第六阶段字段联动与版式运行核查.md',
        '2026-10-17第六阶段查询转单及分组打印续项.md','2026-10-17第六阶段库存查询报价转单与汇总打印续项.md',
        '2026-10-17第六阶段本地收发查询与连续分组打印续项.md','2026-10-17第六阶段期间库存采购候选与组尾打印续项.md',
        '2026-10-17第六阶段保养领料细码复核与分页打印续项.md']
    for name in targets:replace_section(DOCS/name,'phase6-machine-calculations-current',section)
    inventory=read('docs/erp-remaining-inventory-20261016.json')
    current={k:evidence[k] for k in ['query_status_counts','runtime_counts','field_copy_status_counts','unresolved_nonfinancial','unresolved_nonfinancial_categories']}
    current.update(evidence=EVIDENCE,document=TITLE,development='部分完成',historical_reconciliation='未完成',field_acceptance='未完成')
    inventory['phase6_machine_calculations_20261017']=current
    for row in inventory['axes']['旧界面配置入口']:
        if row['name']=='vw_DyeMachine':
            row['phase6_query']={**support[row['name']],'state':support[row['name']]['query_state']}
            row['status']='部分完成';row['reason']='本地机台原行已验证；外部中控编号、重复匹配及历史对账尚未复刻。'
            row['development']={'status':'部分完成','reason':row['reason']};row['phase6_evidence']='docs/'+EVIDENCE
    inventory['counts']['旧界面配置入口']=dict(Counter(r['status'] for r in inventory['axes']['旧界面配置入口']))
    exceptions=[
        ('染机本地资料与中控编号','保留p_Machine原行及MachineType=50，LX_MachineId未知NULL。本地重复及缺MachineNo原行保留，外部重复匹配和中控编号不能从本地猜出，不计中控接入完成。'),
        ('三类库存盘点差额及原触发时机','3入口10原ISNULL差额已接service，重量、长度、粒数和包数分开，显式NULL优先，历史原值保留。新增/输入修改时计算是明确实现，旧自动时机及真实盘点尚未验收。'),
        ('部门申请明确转采购及备注NULL','机物料/染化料均选具体申请原行与头转入采购，原候选RightStatus/NOT EXISTS不变，重复办理独立留档。目标Remarks不允许NULL，申请NULL转空串并保留原快照；原聚合转单及按钮时机未证明。'),
        ('原打印计算字段部分运行','支持算术、Abs、双参数IsNull及依赖顺序；重复/NULL保留，缺来源、除零等按原行报告。R127原公式已验证，其他版式问题仍在；Iif、跨表聚合、脚本及复杂分页继续列差异，完整原打印0。'),
        ('本轮旧库未启动及三十五处来源缺口','本轮MSSQLSERVER停止，只读连接失败；使用本日已保存定义，未取得新核验结果。36起点查询逐项列明，仅染机增加本地替代；35仍无替代，所有缺来源、动态填数、异常及重复业务继续保留，历史对账和现场验收未完成。')]
    axis=inventory['axes']['新旧系统差异及处理情况'];exception_md='## E201～E205：染机、盘点、采购及计算字段打印\n\n见['+TITLE+']('+TITLE+')。\n\n'
    for number,(name,reason) in enumerate(exceptions,201):
        exception_md+=f'### E{number} {name}\n\n{reason}\n\n'
        item={'id':'E'+str(number),'name':name,'status':'部分完成','reason':reason,'related_sql':[],
            'source':'docs/旧ERP复刻异常与合理实现说明.md'}
        old=next((i for i,r in enumerate(axis) if r['id']==item['id']),None)
        if old is None:axis.append(item)
        else:axis[old]=item
    inventory['counts']['新旧系统差异及处理情况']=dict(Counter(r['status'] for r in axis))
    replace_section(DOCS/'旧ERP复刻异常与合理实现说明.md','phase6-machine-calculations-exceptions',exception_md)
    review=read('docs/erp-phase6-review-20261016.json');review['machine_calculations_20261017']=current
    indexed={r['name']:r for r in inventory['axes']['旧界面配置入口']}
    for row in review['entries']:
        if row['name']=='vw_DyeMachine':row['development']=indexed[row['name']]['development'];row['query']=indexed[row['name']]['phase6_query']
    review['counts']['query_execution']=evidence['query_status_counts']
    review['counts']['development']=dict(Counter(r['development']['status'] for r in review['entries']))
    review['counts']['development']['开发完成']=0;review['current_review_at']=evidence['verified_at']
    inventory['phase6_review']['counts']=review['counts'];inventory['phase6_review']['current_evidence']='docs/'+EVIDENCE
    save('docs/erp-phase6-review-20261016.json',review);save('docs/erp-remaining-inventory-20261016.json',inventory)
    print({'tests':evidence['tests']['count'],'unresolved_nonfinancial':35,'document':TITLE})


if __name__=='__main__':main()
