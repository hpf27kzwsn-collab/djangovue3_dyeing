"""保存逐入口联动的验证范围，完整入口、历史和现场状态不作越级升级。"""
import hashlib
import re
from collections import Counter
from datetime import datetime
from sync_phase6_continuation import ROOT,DOCS,read,save,replace_section

TITLE='2026-10-17第六阶段基础资料来样报价入口联动核验.md'
EVIDENCE='erp-phase6-entry-values-verification-20261017.json'


def main():
    audit=read('docs/erp-phase6-entry-formula-audit-20261017.json')
    browser=read('.runtime-temp/phase6/entry-browser-evidence.json')
    prior=read('docs/erp-phase6-cross-browser-verification-20261017.json')
    log='.runtime-temp/phase6/entry-regression.log'
    match=re.search(r'Ran (\d+) tests in ([\d.]+)s\s+OK',(ROOT/log).read_text(encoding='utf8'))
    assert match
    assert browser['entries_verified']==audit['counts']['new_local_formula_entries']==14
    assert all(r['result']=='passed' for r in browser['checks'])
    frontend='.runtime-temp/phase6/entry-frontend.log'
    assert 'built in' in (ROOT/frontend).read_text(encoding='utf8')
    evidence={'verified_at':datetime.now().astimezone().isoformat(),
        'scope':'14个原入口的24条本行公式保存联动及表单布局；不是14个完整入口全部复刻',
        'audit_counts':audit['counts'],'outside_registry_categories':audit['outside_registry_categories'],
        'browser':browser,'schema':read('.runtime-temp/phase6/final-schema-check.json'),
        'tests':{'count':int(match[1]),'seconds':float(match[2]),'modules':23,'result':'passed','log':log},
        'frontend':{'result':'typecheck_and_build_passed','log':frontend,
            'browser_layout':read('.runtime-temp/phase6/entry-layout-evidence.json')},
        'paused_query_count':35,'paused_nonfinancial_queries':prior['paused_nonfinancial_queries'],
        'manual_parent_formulas':prior['manual_parent_formulas'],
        'new_missing_formula_input':{'entry':'Quote','table':'FixedPrice','target':'IsConfirmed','missing':'Price','replacement':'手工录入原字段'},
        'whole_entry_development_completed':0,'historical_import_rows_this_run':0,
        'historical_reconciliation':'未完成','field_acceptance':'未完成',
        'original_print_complete':0,'original_print_proofs':5,
        'old_sql_this_run':'未连接旧SQL Server；依据已提取原结构和配置，本轮数据全为独立测试库合成数据。',
        'exception_ids':['E227','E228'],'screenshots':['docs/assets/phase6-entry-values-20261017.png']}
    paths=[log,frontend,'tools/legacy_models/audit_phase6_entry_formulas.py','web/src/responsive.css']+[
        'backend/plugins/erp_base/'+x for x in ['source_phase6_local_values.py','source_phase6_auto_values.py','source_services.py','tests/test_source_phase6_local_values.py']]
    evidence['files_sha256']={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
    save('docs/'+EVIDENCE,evidence)
    text=f'''# 第六阶段基础资料、来样及报价入口联动核验

日期：2026-10-17。继续逐入口核验；35项查询继续暂缓，财务暂时忽略。没有新增旧erpID，没有导入旧ERP数据。

## 本轮完成范围

修复了“已有公式试算，但日常保存没有自动联动”的缺口：**14个原入口、24条本行公式**接入service保存逻辑，并逐入口完成浏览器验证及落库结果核对。计算结果明确填写时（含NULL）保留输入；修改无关字段时不重算；历史来源原行不批量回填、不去重、不清洗。另修复长原公式说明撑出录入弹窗的布局问题。

|范围|开发与必要验证|历史对账|现场验收|
|---|---|---|---|
|本文14入口的24条保存公式|本轮范围完成；浏览器14/14、持久化核对通过|未完成|未完成|
|长公式表单布局|修复，重新构建并浏览器复查|不适用|未完成|
|14个完整业务入口|仍按全量盘点原状态，不因单项公式通过升级|未完成|未完成|
|第六阶段整体|部分完成|未完成|未完成|

扩大回归 **{evidence['tests']['count']}项通过，23个模块，{evidence['tests']['seconds']}秒**，包括本轮新增7项测试，不重复累计。前端类型检查、构建通过。Django检查和迁移检查通过：766个ERP模型、655个原表模型、12606个原字段、额外旧erpID为0，无新迁移。结构快照比较使用既有提取文件，本轮没有重新连接旧SQL Server。

## 逐入口结果

|入口|公式数|本轮规则及浏览器核验|
|---|---:|---|
|p_Customer|1|客户CustomerID生成Num；UI-CUST保存为KUI-CUST。|
|p_Supplier|1|新增时Num写CustomerID；手填UI-SUP可以直接保存，不先被既有异常自动编号阻断。|
|p_Stuff|3|RecipeUnit按StuffType；StockUnit/WeightUnit采用新增时默认。A新增得到1/K/K，修改B后0/K/K，单位不随修改重置。|
|DyeLabColor|4|ColorNum、KHSHORPTSH、Markt、OriColorNo按依赖顺序计算；AB987/N/Z得到N987Z、N、987、N987Z。|
|ShowDyeLabColor|4|同原公式变体；显式输入UI-MANUAL及客户色号UI-COLOR，结果与派生原色号一致。|
|p_ColorNum|1|R=-1/G=256/B=255照录，RGB=-16776961，不限定为0～255。|
|p_ColorNumSup|1|R/G/B=255，RGB=-1。|
|OrderColor|1|GrayQty=-7保存后OrderQty=-7。|
|OrderColorChange|1|订单变更入口独立验证，-7→-7。|
|OrderColorSup|1|补充入口独立验证，-7→-7。|
|PrintOrderColor|1|打印订单颜色入口独立验证，-7→-7；这不是原打印版式验收。|
|Quote|1|原映射为FixedPrice表，CustomerID改为UI-C2，CustomerCode同步；表头IsConfirmed暂手填，见E228。|
|FixedPrice|1|原映射为Quote表，客户UI-C2同步原CustomerCode；未按入口英文名擅自换表。|
|QuoteDetail|3|Price=-2、ProcessPrice=3：Pricesum=1、IsConfirmed=1；成本4和-6合计-2。|

客户、供应商、染化料由浏览器新增；另11个入口由服务夹具准备原行，再逐个在浏览器修改保存。数据库只读查询用于核对保存结果，不能称为浏览器操作。独立库erp_phase6_browser_20261017全部为合成数据。

修复前p_Stuff记录396仍保留三个空计算值；修复后同StuffID新增397，二者都在，未用同编码覆盖旧行。自动测试另覆盖重复客户/供应商编号、显式空值、负成本、依赖顺序和历史行不回填。显式空值等自动测试场景没有全部重复进行页面操作，不能扩大浏览器覆盖范围。

## 计算顺序与原配置差异

所有本轮计算在service保存前执行，页面继续提交原字段。供应商原CustomerID同时有自动编号和Num公式：明确填写Num时先采用它；未填时仍执行既有原编号规则，不自动跳过无法递增的旧号。

GenerateTime=1的供应商CustomerID、染化料StockUnit/WeightUnit采用仅新增时生成；其他本轮公式在新增或依赖输入发生修改时计算。原客户端GenerateTime完整事件语义尚未被运行证据证实，因此这里是明确实现约定，不宣称逐事件完全相同。ColorNumInput非空优先，计算得到ColorNum后再计算OriColorNo；显式ColorNum=NULL也传播为OriColorNo=NULL。

来样空/短OrderNum沿用既有Python截取规则，从第3字符取尾部，短串得到空串，NULL的Markt保持NULL。旧表达式SUBSTRING在极短输入下的报错时机未确认，本系统允许原值照录并计算，不跳过该行。差异见E227。

## 全量入口核验口径

本轮生成了包含全部1682个原入口（含零公式入口）的[逐公式清单](erp-phase6-entry-formula-audit-20261017.json)，不是只统计常用业务。

|口径|数量|含义|
|---|---:|---|
|全部原入口|1682|含108个财务入口，财务继续暂忽略|
|非财务原入口|1574|全部保留原盘点状态|
|已绑定原模型的非财务入口|818|原819总绑定入口含1个财务入口，统计口径不同|
|含公式的非财务入口|208|共497条非空原Express|
|列入统一保存生成登记的公式|105|包含本轮24条；登记数量不等于完整入口验收数量|
|未列入该登记的公式|392|待追踪专用服务、主从汇总、手动动作、查询显示或真实缺口，不能称392项未实现|

392条按互斥核验顺序分成：54条未绑定模型、41条目标非物理字段、158条父子来源公式、139条本行或SQL函数公式。逐条入口、字段、原表达式、目标模型和分类已保留在JSON。此分类只是定位执行路径，不代表缺资料或开发缺口；35项暂缓查询可能与其交叉，不能相加，也不恢复其调查。

## 尚未解决与后续顺序

1. 优先追踪上述139条已有物理目标的本行/SQL函数公式，核实专用服务或手动动作是否已承接，再对真实缺口接入保存和浏览器回归。例如FixedPriceDetail.Pricesum、染化料领料金额与用量、次品收发净重换算；采购/报价业务金额不等于恢复财务系统。
2. 继续158条父子来源公式的明确主从上下文、汇总与转单后刷新核验；保留每条重复来源，不用first或distinct代替关联证据。54条无模型和41条非物理目标按查询展示/投影/打印路径追踪，35项暂停范围继续跳过开发但保留待办记录。
3. 本轮新增明确缺口：Quote.IsConfirmed引用Price，而目标FixedPrice原表无Price字段。保留手工录入IsConfirmed，不猜用第一条明细价格或虚构字段，见E228。此前qry_QuoteRelaRecipe.Remarks、QueryRecordCheck.GradeID两项父行公式继续显式录入替代，仍未完成自动化。
4. 已通过的前轮6个明确转单及2种跨链组合不重新列为未实现；其他未覆盖组合仍按全量清单。原打印仍5份校样、0份完整原版式，不能用页面数据打印替代。
5. 历史对账及真实单据现场验收独立执行。历史导入量0；本轮不做历史全量对账，不用合成测试结果冒充现场签收。

完整结果见[验证证据]({EVIDENCE})。计算和生成时点差异、缺字段分别登记到异常文档E227、E228。
'''
    (DOCS/TITLE).write_text(text,encoding='utf8')
    reasons={
        'E227':('本行公式自动保存的生成时点与短串处理','14入口24条本行公式接入保存前service。GenerateTime=1的供应商CustomerID及染化料StockUnit/WeightUnit只在新增生成；其他公式按依赖改变计算。原客户端完整事件时机未证实。来样极短OrderNum采用从第3字符取尾部得到空串，允许原值照录；不冒充旧SUBSTRING报错行为。显式值/NULL、重复、负数和历史原行保留。'),
        'E228':('报价表头确价公式缺Price来源','原Quote入口映射FixedPrice表，IsConfirmed公式IIf([Price]>\'0\',2,1)引用的Price不在此原表。已有FixedPriceDetail.Price不能未经业务依据选择或汇总为表头Price。保留IsConfirmed原字段手工录入；未新增字段，未跳过报价记录。明细QuoteDetail的确价、总价和成本公式已自动保存，但不等于表头缺口解决。')}
    exception_text='\n\n'.join('## '+key+' '+name+'\n\n'+reason for key,(name,reason) in reasons.items())
    replace_section(DOCS/'旧ERP复刻异常与合理实现说明.md','phase6-entry-values-exceptions',exception_text+'\n\n见['+TITLE+']('+TITLE+')。开发范围、历史对账、现场验收分别登记。')
    current=f'''## 当前执行范围：逐入口本行公式与页面核验（2026-10-17）

本节及[当前核验清单]({TITLE})、[验证证据]({EVIDENCE})为最新口径；下方旧轮次保留。35项查询继续暂缓，财务暂时忽略。

本轮补齐14个入口的24条本行公式自动保存，14入口浏览器及落库核验通过；修复长原公式说明撑出弹窗的布局。{evidence['tests']['count']}项回归、前端类型检查和构建、Django与迁移检查通过。异常E227、E228已登记。无新增模型字段、无额外旧erpID、无历史数据导入。

**上述增量开发完成；完整入口及第六阶段整体仍部分完成；历史对账、现场验收未完成。** 全量1682入口中1574非财务；208非财务入口含497条公式，105条已列入统一保存登记，392条待追踪专用服务/手动/查询路径，不能直接算392项未实现。分类为139条本行或SQL函数、158条父子来源、41条非物理目标、54条未绑定模型，逐条见全量JSON。

下一步先逐条核验139条本行/函数执行路径及真实自动保存缺口，再核验158条父子上下文和其余投影；35项暂停范围不恢复调查。Quote表头确价缺Price来源保留手填，既有2项父行公式也保留显式替代。前轮6个转单分支、2种跨链组合已联调的事实保持；原打印仍5校样/0完整。全绑定385模型840条819入口（非财务818），21条身份/续行未绑定剩余0，口径不变。
'''
    for doc in ['2026-10-16染色ERP剩余工作全量盘点清单.md','染色ERP后续开发方案.md']:
        replace_section(DOCS/doc,'phase6-form-flows-current',current)
    replace_section(DOCS/'2026-10-17第六阶段其余转单与跨链逆向浏览器联调.md','phase6-entry-values-superseded',
        f'## 后续状态更新\n\n后续逐入口联动核验见[{TITLE}]({TITLE})；本文原转单/逆向证据继续有效，不代表全部入口完成。')
    inventory=read('docs/erp-remaining-inventory-20261016.json');axis=inventory['axes']['新旧系统差异及处理情况']
    for key,(name,reason) in reasons.items():
        row={'id':key,'name':name,'status':'部分完成','reason':reason,'related_sql':[],'source':'docs/旧ERP复刻异常与合理实现说明.md'}
        existing=next((i for i,r in enumerate(axis) if r['id']==key),None)
        if existing is None:axis.append(row)
        else:axis[existing]=row
    inventory['counts']['新旧系统差异及处理情况']=dict(Counter(r['status'] for r in axis))
    summary={'document':TITLE,'evidence':EVIDENCE,'entry_count':14,'formula_count':24,'browser_entry_count':14,
        'development':'本轮列明保存公式与布局通过；完整入口未升级','historical_reconciliation':'未完成','field_acceptance':'未完成',
        'tests':int(match[1]),'paused_query_count':35,'outside_registry_formula_count':392}
    inventory['phase6_entry_values_20261017']=summary
    entries={r['entry'] for r in audit['new_local_formulas']}
    for row in inventory['axes']['旧界面配置入口']:
        if row['name'] in entries:
            row['phase6_local_values_20261017']={**summary,
                'entry_formulas':[r['field'] for r in audit['new_local_formulas'] if r['entry']==row['name']]}
    inventory['phase6_review']['current_evidence']='docs/'+EVIDENCE
    inventory['phase6_review']['next']='先逐项追踪139条本行/函数公式与158条父子公式的现有执行路径，仅真实缺口继续开发浏览器联调；非物理目标及无模型公式按投影等追踪。392不等于未实现。35项查询及财务继续暂缓；历史/现场独立验收。'
    review=read('docs/erp-phase6-review-20261016.json');review['entry_values_20261017']=summary;review['current_review_at']=evidence['verified_at']
    save('docs/erp-remaining-inventory-20261016.json',inventory);save('docs/erp-phase6-review-20261016.json',review)
    print(summary)


if __name__=='__main__':main()
