"""登记本行公式、明确父行回写及配方成本服务的验证证据。"""
import hashlib
import re
from collections import Counter
from datetime import datetime
from sync_phase6_continuation import ROOT,DOCS,read,save,replace_section

TITLE='2026-10-17第六阶段配方父子来源与专用服务联调.md'
EVIDENCE='erp-phase6-service-values-verification-20261017.json'


def main():
    audit=read('docs/erp-phase6-entry-formula-audit-20261017.json')
    browser=read('.runtime-temp/phase6/service-values-browser-evidence.json')
    prior=read('docs/erp-phase6-entry-values-verification-20261017.json')
    tests=[]
    for name in ['service-values-regression.log','service-values-final-targeted.log']:
        path='.runtime-temp/phase6/'+name
        match=re.search(r'Ran (\d+) tests in ([\d.]+)s\s+OK',(ROOT/path).read_text(encoding='utf8'))
        assert match,name
        tests.append({'log':path,'count':int(match[1]),'seconds':float(match[2]),'result':'passed'})
    registered=audit['service_formula_registrations']
    assert len(registered)==25 and len({r['entry'] for r in registered})==17
    assert browser['save_formula_entries_verified']==17 and all(r['result']=='passed' for r in browser['checks'])
    assert len(browser['cost_browser_reports'])==3
    evidence={'verified_at':datetime.now().astimezone().isoformat(),
        'scope':'17入口25条保存公式；2类明确父行参数回写；3入口成本保存与两类试算口径统一。不是20个完整入口全部复刻。',
        'new_save_entries':17,'new_save_formulas':25,'cost_service_entries':3,'cost_service_formulas':3,
        'browser_formula_entries':20,'parent_refresh_kinds':2,'parent_rows_edited_in_browser':3,
        'formula_registrations':registered,'audit_counts':audit['counts'],
        'execution_path_counts':audit['execution_path_counts'],'outside_registry_categories':audit['outside_registry_categories'],
        'browser':browser,'tests':tests,'regression_modules':27,
        'test_scope':'376项扩大回归通过；随后仅收紧普通配方的依赖输入并补充对应断言，11项针对性复验通过，后者不重复累计。',
        'schema':read('.runtime-temp/phase6/final-schema-check.json'),
        'frontend':'未修改前端源码；使用既有构建读取本轮后端元数据并操作页面。不重复算作本轮前端构建。',
        'paused_query_count':35,'paused_nonfinancial_queries':prior['paused_nonfinancial_queries'],
        'manual_parent_formulas':prior['manual_parent_formulas'],'new_missing_formula_input':prior['new_missing_formula_input'],
        'whole_entry_development_completed':0,'historical_import_rows_this_run':0,
        'historical_reconciliation':'未完成','field_acceptance':'未完成',
        'original_print_complete':0,'original_print_proofs':5,'exception_ids':['E229','E230'],
        'screenshots':['docs/assets/phase6-service-values-20261017.png']}
    paths=['backend/plugins/erp_base/'+x for x in ['source_phase6_service_values.py','source_phase6_auto_values.py',
        'source_phase6_forms.py','source_services.py','source_sampling_services.py','source_entry_calculations.py',
        'source_phase6_expressions.py','tests/test_source_phase6_service_values.py']]
    paths+=['tools/legacy_models/audit_phase6_entry_formulas.py']+[r['log'] for r in tests]
    evidence['files_sha256']={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
    save('docs/'+EVIDENCE,evidence)
    text=f'''# 第六阶段配方父子来源与专用服务联调

日期：2026-10-17。承接上一轮本行公式、父子来源及专用服务核验。35项查询继续暂缓；财务暂时忽略。没有新增旧erpID或其他模型字段。

## 本轮结果及完成标准

新增**17入口25条保存联动**；补齐配方染程浴比、工艺曲线最大值这2类明确父行修改后的子行回写；统一**3个配方表头入口的成本保存、专用试算、通用试算**。合计涉及20个公式入口、28条公式，但不代表20个完整入口全部完成。

|范围|开发及必要验证|历史对账|现场验收|
|---|---|---|---|
|17入口25条保存公式|本轮增量完成；17/17浏览器编辑与落库核对通过|未完成|未完成|
|2类父行参数回写|本轮完成；浏览器修改1个染程、2个曲线父行，子行结果核对通过|未完成|未完成|
|3入口配方成本统一|本轮完成；通用试算3/3、专用大货计算及采用路径通过|未完成|未完成|
|缺明确父行的记录|照录原行，记录缺来源事件；未算作公式复刻成功|未完成|未完成|
|第六阶段整体|部分完成，其他入口仍逐项核验|未完成|未完成|

扩大回归**{tests[0]['count']}项通过，27个模块，{tests[0]['seconds']}秒**。随后收紧普通配方触发字段，11项针对性复验通过（{tests[1]['seconds']}秒），不重复累加。本轮新增11项测试。Django与迁移检查通过：766个ERP模型、655个原表模型、12606个原字段、额外旧erpID为0，无新迁移。

前端源码本轮未改，页面使用已有构建。历史导入0。测试全部在独立合成库erp_phase6_browser_20261017及独立回归测试库进行；原公式依据既有资料提取，结构比较使用已保存快照，本轮没有重新提取旧库。

## 逐入口公式与浏览器结果

|入口|公式数|结果|
|---|---:|---|
|DyeRecipePhaseDetail、OtherDyeRecipePhaseDetail、PrepareDyeRecipePhaseDetail、ReworkDyeRecipePhaseDetail、WashDyeRecipePhaseDetail|各1，共5|Price=-4、Dosage=2，Amount=-8。五个入口逐一页面编辑保存。|
|BulkDyeRecipePhaseDetail|1|浴比7时Amount=-56；父行浴比改5后Amount=-40，另一同物料序号原行金额5。两行都保留。|
|StandardDyeRecipePhaseDetail|1|比例2、单价-4、配方单位1、浴比7，Amount=-56。|
|FinishDyeRecipePhaseDetail|1|染料类别S采用原固定系数10，比例2、单价-4，Amount=-80。|
|p_DyeCurveDetail、p_DyeCurveDetailJJ|各1，共2|DefaultValue=-4、父MaxValue=3，Price=-12；父值改5后两入口各为-20。相同步号另一行DefaultValue=2得到10。|
|FixedPriceDetail（原QuoteDetail表）|1|Price=-4、ProcessPrice=3，Pricesum=-1。保持旧入口与原表映射。|
|JobGrayPreRecord、JobGrayRecord、PrintJobGrayRecord、SaleJobGrayRecord、TwiJobGrayRecord|各2，共10|WeightQty=-20、GUnit=3，Kg=-9.07、Pound=-20。五个入口逐一验证。|
|DefectiveOutRecord|4|GrayQty=-10、GUnit=3：GKg=-4.54、GPound=-10；WeightQty=-20、PUnit=1：PKg=-20、PPound=-44.09。|
|BulkDyeRecipe、FinishDyeRecipe、TrialDyeRecipe|各1，共3，属于成本服务统一|浏览器原公式报告分别为-70、-80、-11；不是新增3条保存公式。|

以上来源由服务夹具准备，页面修改、保存和计算动作确实由浏览器操作；数据库查询只用于验证结果。缺父行配方另经浏览器修改Price=-4、Dosage=2，Amount仍NULL，记录保留并登记两次缺来源事件（创建及编辑）。未用测试库行数冒充旧数据导入或历史对账数量。

## 父子来源、重复连接及服务一致性

本轮未证实的旧客户端行为单列为[异常说明](旧ERP复刻异常与合理实现说明.md)中的E229（缺父行及参数回写时机）、E230（重复染程连接及多候选回写）。以下说明已实现范围，不将这些差异标为完全复刻。

配方Amount复用source_entry_calculations.entry_values；曲线Price复用同一专用服务。仅对应依赖字段发生修改时重算：普通配方只依赖Price/Dosage，大货和标准另依赖RecipeUnit，后处理另依赖StuffType。明确提交Amount或Price（含NULL）时保留本次输入。父表参数改变时按明确关联逐行重算活动子行，历史来源子行不回填。缺少关联时记录entry_formula_source_pending，原行照录，待明确关联后再计算，不按同编号挑第一行。

父子回写与父表保存处于同一事务。新增测试证明：某子行计算值超过旧Price字段精度时，整个父子修改回滚，先前已计算的子行也不留下半次结果；原行原值仍在，不截断、不跳过该子行。这类结果不能标记成功，需按原字段精度明确业务值。

发现并修复的成本差异：原自动保存服务按SheetSeries+PhaseNo连接，重复阶段会保留连接重复度；原专用手动服务按明确外键求和，原通用试算按物理行合并，二者可能与保存结果不同。本轮将3入口Cost统一到source_sampling_services.recipe_cost，通用试算仍通过本次授权reader读取来源，不扩大查询权限。

浏览器合成例：大货配方2条物料行同StuffNo，金额-40和5。只有1条PhaseNo=1染程时成本-35。再由夹具保留第二条相同PhaseNo=1染程后，旧联查成本为(-40+5)×2=-70。浏览器专用计算及通用试算均为-70。全部染程、物料原行都保留；不是去重求和，也不是把2条物料合并成1条。第二染程的浴比99不会擅自替代物料已明确关联的第一染程浴比5；未知旧客户端多候选回写时点仍记E230，不声称完全复现该歧义。

成本汇总为原非财务业务成本，财务模块没有恢复。页面截图与完整原字段结果见[验证证据]({EVIDENCE})及[成本核对截图](assets/phase6-service-values-20261017.png)。

## 全量清单的新口径

全部1682入口保持登记，其中1574非财务、108财务。818个非财务入口已绑定模型；含公式入口208，原公式497条。绑定数与完整入口完成数是两件事。

|定位状态|数量|准确含义|
|---|---:|---|
|统一保存生成登记|130|前轮105，本轮增加25；不是130条全部现场验收|
|登记外另有明确自动汇总服务|29|本轮沿调用路径定位，含配方成本、原主从合计、加捻入库及质量疵点汇总；不能把它们继续算作未实现|
|本轮尚未定位自动路径|338|可能在专用手动服务、其他服务、查询投影或确有缺口；不等于338项未实现|
|合计|497|全部非财务原公式保留|

统一登记以外仍367条（前轮392减本轮25）。分类为116条本行/SQL函数、156条父子来源、54条未绑定模型、41条非物理目标；其中29条已定位其他自动服务。上述两张口径互相交叉，不能相加。原35项暂缓查询继续保留，不能与公式条数相加。

逐公式JSON现在记录具体自动服务路径，以及是否存在该入口的手动服务。手动服务登记只说明入口有该能力，不代表覆盖该入口每个字段。完整入口开发完成数仍不升级；本文只认定实际列明的增量验证范围。

## 后续顺序

1. 接着追踪剩余116条本行/函数公式：优先称料Dosage、NeedQty及Money/NeedMoney/RealMoney，明确不同入口计划量和实称量的区别；随后包装净量、次品实重/净重、业务税价及双向金额公式。先确认已有专用服务承接范围，不能重复实现相冲突的算法。
2. 继续156条父子公式的上下文核验：优先称料头/染程/物料、班组人员取表头值、工卡计划和质检疵点汇总。已定位自动服务的29条核验触发时机和未覆盖页面组合，不重新记作未实现。
3. 无模型和非物理字段继续按查询/投影/打印追踪，财务和35项暂停查询不恢复调查。此前两项父行公式、Quote表头IsConfirmed缺Price来源仍为显式录入替代，未被本轮解决。
4. 原打印仍5份校样、0份完整原版式。历史对账按原主键、批次、提取行分别核对，异常、重复、NULL和负数全部保留；现场验收使用真实单据，不能用本轮合成数据替代。
'''
    (DOCS/TITLE).write_text(text,encoding='utf8')
    reasons={
        'E229':('缺明确父行的自动公式保留与参数回写时机',
            '配方Amount及工艺曲线Price需要明确父行时，不按同编号任选来源。缺关联原行及原值照存并记录entry_formula_source_pending，关联明确后才计算；不能计作该原行计算已复刻。父浴比/MaxValue修改后逐活动子行回写，历史行不回填，超过原字段精度则整次回滚。此为明确保存时点实现，未知旧客户端GenerateTime完整行为仍未现场确认。'),
        'E230':('配方成本重复连接与两种试算口径统一',
            '修复自动保存保留重复染程连接、手动试算却按物理行合并导致成本不同的问题。BulkDyeRecipe/FinishDyeRecipe/TrialDyeRecipe共用原SheetSeries+PhaseNo连接成本服务，通用试算保留授权来源范围；重复原行全部保留。单行Amount按明确染程关联计算，不从重复染程序号中任选浴比；旧客户端多候选写回时机未证实，仍单列差异。浏览器合成成本(-40+5)×2=-70，保存和试算一致，不能冒充历史/现场验收。')}
    replace_section(DOCS/'旧ERP复刻异常与合理实现说明.md','phase6-service-values-exceptions',
        '\n\n'.join('## '+key+' '+name+'\n\n'+reason for key,(name,reason) in reasons.items())+f'\n\n详细范围见[{TITLE}]({TITLE})。')
    current=f'''## 当前执行范围：本行公式、父子来源与专用服务（2026-10-17）

最新核验见[{TITLE}]({TITLE})、[验证证据]({EVIDENCE})及[全量逐公式清单](erp-phase6-entry-formula-audit-20261017.json)。下方旧轮次为历史记录。35项查询继续暂缓，财务暂时忽略。

本轮新增17入口25条保存联动，补齐2类明确父行参数回写；统一3入口Cost保存及两类试算口径。17入口页面编辑、3父行修改及3成本入口报告已验证，缺父行记录也照录留档。扩大回归376项通过，收紧公式触发字段后11项针对性复验通过，不重复累计。模型及迁移检查通过；无新模型字段、无旧erpID、历史导入0。异常E229、E230已登记。

**本轮列明增量开发完成；完整入口及第六阶段整体仍部分完成；历史对账、现场验收未完成。** 非财务497条公式中，130条进入统一保存登记，另29条定位到自动汇总服务，338条尚未定位自动路径（不能算作338项未实现）。登记外367条分为116本行/函数、156父子来源、54未绑定模型、41非物理目标，29个已有服务公式包含在其中，不能相加。

后续先核验称料计划/实称金额和包装换算，再核验称料父子链、班组表头取值、工卡计划和质量汇总；先查现有服务再补真正缺口及浏览器覆盖。已完成的前轮转单/逆向和14入口24公式不重复列未实现。2项父行公式与报价表头确价缺来源仍采用明确录入替代，35项暂停查询不减少；原打印5校样/0完整。全绑定385模型840条819入口（非财务818）、身份/续行未绑定剩余0，口径保持。
'''
    for name in ['2026-10-16染色ERP剩余工作全量盘点清单.md','染色ERP后续开发方案.md']:
        replace_section(DOCS/name,'phase6-form-flows-current',current)
    replace_section(DOCS/'2026-10-17第六阶段基础资料来样报价入口联动核验.md','phase6-service-values-superseded',
        f'## 后续状态更新\n\n后续保存联动及服务路径核验见[{TITLE}]({TITLE})；本文前轮14入口24公式结果保留。392为前轮未列统一登记的数量，当前变为367，其中29条已定位其他自动汇总服务。')
    inventory=read('docs/erp-remaining-inventory-20261016.json');axis=inventory['axes']['新旧系统差异及处理情况']
    for key,(name,reason) in reasons.items():
        row={'id':key,'name':name,'status':'部分完成','reason':reason,'related_sql':[],'source':'docs/旧ERP复刻异常与合理实现说明.md'}
        index=next((i for i,r in enumerate(axis) if r['id']==key),None)
        if index is None:axis.append(row)
        else:axis[index]=row
    inventory['counts']['新旧系统差异及处理情况']=dict(Counter(r['status'] for r in axis))
    summary={'document':TITLE,'evidence':EVIDENCE,'save_entries':17,'save_formulas':25,'cost_entries':3,'browser_formula_entries':20,
        'development':'本轮列明增量通过；完整入口未升级','historical_reconciliation':'未完成','field_acceptance':'未完成',
        'paused_query_count':35,'tests':tests,'execution_path_counts':audit['execution_path_counts']}
    entries={r['entry'] for r in registered}|{'BulkDyeRecipe','FinishDyeRecipe','TrialDyeRecipe'}
    for row in inventory['axes']['旧界面配置入口']:
        if row['name'] in entries:row['phase6_service_values_20261017']={**summary,
            'entry_fields':[r['field'] for r in registered if r['entry']==row['name']] or ['Cost']}
    inventory['phase6_service_values_20261017']=summary
    inventory['phase6_review']['current_evidence']='docs/'+EVIDENCE
    inventory['phase6_review']['next']='按当前清单追踪称料计划/实称金额、包装单位、称料父子链及其他原公式；先查已有服务再补缺口。497条原公式中130统一登记、29其他自动服务、338尚未定位，不等同未实现数量；35查询及财务继续暂缓。历史/现场独立。'
    review=read('docs/erp-phase6-review-20261016.json');review['service_values_20261017']=summary;review['current_review_at']=evidence['verified_at']
    save('docs/erp-remaining-inventory-20261016.json',inventory);save('docs/erp-phase6-review-20261016.json',review)
    print(summary)


if __name__=='__main__':main()
