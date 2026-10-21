"""记录表单和撤回的实际开发证据；查询暂缓与开发/对账/现场三轴分开。"""
import json
import re
import hashlib
from collections import Counter
from datetime import datetime
from sync_phase6_local_chains import ROOT,DOCS,read,save
from sync_phase6_continuation import replace_section

TITLE='2026-10-17第六阶段表单联动转单撤回与流程联调.md'
EVIDENCE='erp-phase6-form-flows-verification-20261017.json'


def main():
    runtime=read('docs/erp-phase6-runtime-review-20261017.json')
    rules=read('backend/plugins/erp_base/source_entry_rules.json')['models']
    previous=read('docs/erp-phase6-units-rules-verification-20261017.json')
    bound=[{'model':label,'entry':name,'table':r['write_binding']['table'],'title':r['title']}
        for label,entries in rules.items() for name,r in entries.items() if r['write_binding']['source']=='explicit_UpdateSQL']
    assert len(bound)==37
    paused=[{**r,'scope':'用户明确暂缓','development':'原差异未解决','historical_reconciliation':'未完成','field_acceptance':'未完成'}
        for r in previous['unresolved_queries'] if r['scope']=='本期保留']
    assert len(paused)==35
    log='.runtime-temp/phase6/form-flows-regression.log'
    match=re.search(r'Ran (\d+) tests in ([\d.]+)s\s+OK',(ROOT/log).read_text(encoding='utf8'))
    assert match,'扩大回归未全部通过'
    build='.runtime-temp/phase6/form-flows-frontend.log'
    assert 'built in' in (ROOT/build).read_text(encoding='utf8')
    schema=read('.runtime-temp/phase6/final-schema-check.json')
    evidence={'verified_at':datetime.now().astimezone().isoformat(),'development':'部分完成，按本轮增量分别验证',
        'paused_nonfinancial_queries':paused,'paused_query_count':35,'new_write_bindings':bound,
        'entry_models':len(rules),'entry_bindings':sum(len(r) for r in rules.values()),
        'distinct_bound_entries':len({n for r in rules.values() for n in r}),
        'runtime_counts':runtime['counts'],'field_copy_status_counts':runtime['field_copy_status_counts'],
        'context_filters':runtime['context_filters'],
        'unbound_identity_configurations':runtime['unbound_identity_configurations'],
        'unbound_copy_configurations':runtime['unbound_copy_configurations'],
        'new_reverse_types':['采购转到货明细','部门申请转采购明细（配件/染化料）','保养计划转配件领料','报价转调价','报价转订单整单','采购转成品入库整单'],
        'remaining_reverse_types':[],
        'reverse_scope':'source_phase6_transfers中的六种明确转单；不是全系统逆向清单',
        'automatic_formula_entries':49,'automatic_formula_targets':71,
        'additional_header_aggregate':{'entry':'TwistingIn','fields':['WeightQty','LengthQty','Rolls','NetKg']},
        'tests':{'count':int(match[1]),'seconds':float(match[2]),'modules':20,'result':'passed','log':log,
            'sha256':hashlib.sha256((ROOT/log).read_bytes()).hexdigest(),'scope':'第六阶段14个模块及库存、工卡、销售、入口公式、跨链逆向、基础6模块；不是全项目测试'},
        'frontend':{'result':'typecheck_and_build_passed','log':build,'warning':'既有大分包提示；未进行浏览器逐表单人工走查'},
        'schema':schema,'historical_reconciliation':'未完成','field_acceptance':'未完成',
        'historical_import_rows_this_run':0,'old_sql_this_run':'未连接；沿用前轮已核实的原字段及界面配置快照',
        'whole_entry_development_completed':0,'whole_entry_historical_reconciled':0,'field_accepted':0,
        'evidence_semantics':'本轮补齐的功能点与必要测试完成，不代表37个完整入口、七模块整链或第六阶段全部完成。'}
    paths=['backend/plugins/erp_base/'+name for name in ['source_phase6_transfers.py','source_phase6_editors.py',
        'source_phase6_forms.py','source_phase6_auto_values.py','source_entry_rules.json','source_services.py',
        'source_execution_state.py','source_api.py','tests/test_source_phase6_form_flows.py','tests/test_source_phase6_editor_context.py']]
    paths+=['tools/legacy_models/build_entry_rules.py','tools/legacy_models/audit_phase6_runtime.py',
        'web/src/components/ResourceTable.vue','web/src/plugins/erp/BusinessPane.vue']
    evidence['files_sha256']={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
    save('docs/'+EVIDENCE,evidence)
    text=f'''# 第六阶段表单联动、转单撤回与流程联调

日期：2026-10-17。按用户最新要求，35处非财务查询差异暂缓；财务暂缓；不新增旧erpID；所有原字段、异常和重复记录继续保留。

## 本轮开发结果与三类状态

**本轮完成下列增量开发和必要自动化验证；第六阶段整体仍为部分完成。** 原库存、报价、工卡等历史数据没有在本轮导入，测试在隔离开发测试库内完成，不能记为历史对账或现场验收。

|工作|开发与必要验证|历史数据对账|现场验收|
|---|---|---|---|
|表单写入绑定|依据原UpdateSQL补37个入口；37项均验证进入表单元数据，登录、续行、主从保存有代表性非空用例；不等于37个整入口全部验证|未完成|未完成|
|上下文联动|补9组明确映射，其中7组存在启用的选择器；父单原字段传给子单选择器，子单显式值优先|未完成|未完成；父子页面仅完成类型检查和构建，仍需浏览器走查|
|加捻入库自动触发|明细RealQty计算→表头4项汇总→库存自动更新；负数、NULL、复制续行和修改通过|未完成|未完成|
|采购转到货撤回|可撤回选定的一条转入明细，重复转入的另一条保留生效；原明细留档，接口验证通过|未完成|未完成|
|部门申请转采购撤回|配件、染化料两种申请均可撤回指定转入明细；NULL及重复转单逐条保留|未完成|未完成|
|保养计划领料撤回|审核→反审核→撤回指定明细→再次审核通过；库存只按有效明细生成|未完成|未完成|
|报价转调价撤回|按原删除回写上一条有效调价；同色号及重复报价均纳入，撤回原行及来源留档；异常整次回滚|未完成|未完成|
|报价转订单撤回|原开卡引用限制、重复转单独立撤回、头明细留档通过|未完成|未完成|
|采购转成品入库撤回|原单留档、当前库存撤销及库存快照、GX99删除回写、工卡入库状态重算、失败回滚通过|未完成|未完成|

扩大回归 **{evidence['tests']['count']}项通过，{evidence['tests']['seconds']}秒，20个测试模块**，包括本轮表单/编辑器20项，不重复累计。前端类型检查和构建通过，保留原有大分包提示。Django检查及迁移检查通过：766个ERP模型、655个原表模型、12606个原字段，额外旧erpID为0，无新增迁移。没有执行旧SQL修改或历史导入。

## 表单录入与字段绑定

原TableName为空，但UpdateSQL明确为单表`SELECT * FROM 表名`的37个非财务入口，按写入表绑定。没有根据展示用JOIN、相似字段名称猜写入目标；原界面快照不改。新生成规则记录write_binding依据。

累计{evidence['entry_models']}个模型有入口规则、{evidence['entry_bindings']}条模型/入口绑定，涉及{evidence['distinct_bound_entries']}个不同入口。登录身份字段绑定118条、续行绑定227条、编辑器字段绑定2929条。原27条未绑定配置中补6条，余21条逐项列在后文。

|旧入口|写入原表|用途|
|---|---|---|
'''
    for row in bound:text+=f"|{row['entry']}|{row['table']}|{row['title']}|\n"
    text+='''
## 字段联动的明确范围

16组原非空过滤配置原样保留：3组原配置完整、9组本轮明确补全、4组仍不完整。9组中的B128原编辑器种类均为`_`，B210没有字段调用，保留映射但不擅自开启编辑器，因此不能把12组映射全部说成已启用的现场联动。

|Lookup|本次映射|执行范围|
|---|---|---|
|A026|JobSheetNo→JobSheetNo|合染订单候选按工卡筛选|
|A031|JobSheetNo→JobSheetNo|复版候选；仍保留原最新记录与已领用排除条件|
|B080|StationID→StationID|按工位选机台，同代码重复机台逐行展示|
|B128|CustomerID→CustomerID|映射已登记，原编辑器未启用，未自行开放|
|B133|CustomerID→CustomerID|客户送货地址|
|B176|CurveID→CurveID|染色曲线步骤，重复曲线/步骤连接倍增保留|
|B186|JobSheetNo→JobSheetNo|料单染色工序|
|B210|ProdID→ProdID|映射已登记，原配置没有字段调用|
|B305|CustomerID→CustomerID|收坯地址|

父单上下文只用于选择器，不混入子单写入数据。子单当前字段（含显式NULL）覆盖同名父字段。没有上下文时仍列原候选并标注缺失；NULL按原等值不匹配，不能擅改为空串或当前用户部门。B145/B146的复检单号、工卡号关系仍待实现；B153/B197涉及暂缓外部来源，不纳入本轮继续追查范围。已保存原代码仍可直接录入。

## 自动触发与业务顺序

加捻入库TwistingInRecord使用原式`ISNULL(WeightQty,0)`计算RealQty，显式录入值（含NULL）优先。其表头TwistingIn按当前归属明细汇总WeightQty、Meter→LengthQty、InRolls→Rolls、NetKg。顺序为明细计算、持久化、表头汇总、库存重建、上游状态回写；不将空值、负数或重复细码删掉。

当前逐字段自动公式注册共49个入口71个目标，另有本轮加捻表头4个汇总目标。两种计数分别列示，不能把“元数据里存在公式”直接记成“已自动执行”。37个新增绑定入口的其余公式与事件仍须逐项核实调用时机。

## 转单撤回与留档

本轮新增3个操作接口，覆盖6类明确转单、7个业务变体（部门申请包含配件及染化料两种）。从转入明细或整单执行撤回；已审核/确认的父单先走原重新办理流程。仅撤回指定新办理行或指定整单，同编号、同来源重复转入的其他行保持各自状态。

撤回标记及来源快照放在既有办理上下文，不新增业务模型字段。普通列表和办理审计保留原行，活动数量、下一次库存生成及后续调价候选不计已撤回行。原查询工作台的“包含留档”仍由使用者选择；包含留档查询不能当作当前有效库存或候选口径。

报价转调价撤回沿用旧删除逻辑：回写上一条有效调价的AdjustPrice/JobSheetNo，没有上一条则置NULL；原删除不恢复DateType/StartDate，因此不包装成“恢复所有字段到转单前”。原报价、原转入明细及重复行都保留。没有新转单来源上下文的历史记录，不伪造来源后套用本动作。

报价转订单整单撤回沿用原开卡引用限制，保留表头及所属明细，重复转单分别处理。采购转成品入库整单撤回保存本次新生成库存流水的完整快照，清理本次现行库存效果，再按原删除规则清理GX99的StartTime/WPWorker并重算工卡入库完成状态。涉及的原行与回写对象均检查当前数据范围，失败时整次回滚。

原成品入库新增会使排程退出活动范围并更新GX98结束时间；旧删除并不反向恢复这些内容。因此本次沿用原删除规则，不虚构旧系统不存在的完全对称撤回。跨后续领用、包装、发货和异常引用的完整实单链还需扩展验证，不能把这6类起始转单测试等同于全系统逆向已验收。

## 尚未绑定的21条原字段配置

这些记录不属于“已解决”。原配置及对应物理字段保留；缺目标字段、缺明确写入表或原表不一致的情况单列。不能为了表面上降到0而将Code当作GrayID、将职位当员工编号、或将RecordYieldCheck静默替换为RecordYield。

|旧入口|原字段|原类型|原写入表/依据|
|---|---|---|---|
'''
    for row in [*runtime['unbound_identity_configurations'],*runtime['unbound_copy_configurations']]:
        text+=f"|{row['entry']}|{row['field']}|{row['kind']}|{row['original_table_name'] or '未配置'}；{row['update_sql'] or '无明确UpdateSQL'}|\n"
    text+='''
## 后续顺序及准确口径

1. 完成剩余21条身份/续行配置的逐项对应或明确替代，再补B145/B146两组本地关系。B128/B210是否启用单列；当前未擅自变更旧编辑器类型。
2. 对新增37个绑定入口的其余字段计算与自动事件逐项跑非空场景。总事件216处，其中8处财务暂缓、208处非财务；208不是“全部未开发”，沿用原事件逐项状态，缺代码与缺验证继续分开。
3. 在6类明确转单及撤回已实现的基础上，扩展跨后续领用、包装、发货及异常引用的完整实单链验证。40条原字段复制配置改正为20条财务暂缓、20条非财务：18条现存目标明确映射、2条已缺目标字段。原先3条“非财务坏目标”实际来自财务入口，此次更正归类，不删除配置。
4. 按基础信息→销售/打样→采购/仓储→生产→质量/包装/交付→逆向，执行浏览器逐表单联调与接口整链回归。测试样例、自动化通过和现场签字分别记录。
5. 选择明确抽取时点做历史数据对账，比较原主键/原业务键/来源行及数量、金额、状态、关联记录；重复和异常逐条保留。随后由现场验收，不能将本轮隔离测试库样例当旧ERP数据已导入。

35处查询仍逐项保留为用户暂缓（22缺外部来源、11缺列、2缺本地对象），并非都属于设备接入，不参与本轮“待补代码”计数。原打印仍290份：5份固定高度校样、256份XML运行差异、29份缺XML、0份完整原版式；打印问题独立保留，未因查询暂缓而消失。

## 暂缓查询逐项索引

|入口|原差异类别|当前处理|历史对账|现场验收|
|---|---|---|---|---|
'''
    for row in paused:text+=f"|{row['entry']}|{row['category']}|用户明确暂缓，保留原差异|未完成|未完成|\n"
    (DOCS/TITLE).write_text(text,encoding='utf8')
    section=f'''## 当前执行范围：表单、联动、转单撤回与流程联调（2026-10-17）

**用户明确暂缓35处非财务查询差异，财务继续暂缓。** 下方此前各轮状态均为历史记录；本节和[本轮清单]({TITLE})、[验证证据]({EVIDENCE})为当前口径。暂缓不等于完成，也不删除原差异；35处不是全部设备接口。

已补37个原UpdateSQL写入绑定，未绑定身份/续行27→21；补9组上下文映射（7组有启用的选择器），残缺关系13→4；加捻入库串起明细实际量、4项表头汇总和库存；新增6类转单7个业务变体的留档撤回，包含重复原行及审核/反审核联调。40条字段复制归类更正为20财务、20非财务（18明确映射、2缺目标字段）。

{evidence['tests']['count']}项扩大回归通过；前端类型检查/构建、模型与迁移检查通过，无新增旧erpID，无历史导入。本轮增量开发与必要自动化验证完成，**第六阶段整体仍部分完成，历史对账及现场验收未完成**。剩余21条绑定、2组本地过滤及2组暂缓外部过滤、37入口其余事件验证、跨后续单据的逆向扩展验证和浏览器整链联调在本轮清单逐项保留。原打印状态保持5校样/0完整。异常E216～E220。
'''
    targets=[DOCS/'染色ERP后续开发方案.md',DOCS/'2026-10-16染色ERP剩余工作全量盘点清单.md',*DOCS.glob('2026-10-1*第六阶段*.md')]
    for path in dict.fromkeys(targets):
        if path.name!=TITLE:replace_section(path,'phase6-form-flows-current',section)
    exceptions=[
        ('原TableName空值与37个明确写入绑定','仅按原UpdateSQL明确单表绑定，原展示SQL及原配置原样保留；6条身份/续行配置恢复，21条仍缺明确对应，逐字段列在本轮文档，不能当完成。'),
        ('九组上下文映射的替代范围与未启用编辑器','9组映射为依据当前原字段的明确实现，不冒充已证实旧客户端行为；7组有启用选择器，B128原编辑器为_、B210无调用，不擅启用；4组残缺关系保留，其中2组外部暂缓。'),
        ('转单撤回留档与旧删除不对称','6类转单7业务变体新增撤回；保留原行、重复行和来源，活动计算排除撤回行。调价按原删除恢复上一有效价格及引用，不恢复DateType/StartDate。成品入库撤回保存库存快照并按原删除清理GX99/重算工卡，不虚构恢复新增时退出的排程或GX98；跨后续单据仍需实单扩展验证。'),
        ('加捻入库计算与保存库存的时序','补TwistingInRecord.RealQty与TwistingIn重量/米数/粒数/净重汇总后再库存生效。负数/NULL/重复不删，显式实际值优先；这不等于37个补绑入口全部公式和事件完成，其他时点继续核验。'),
        ('字段复制财务归类更正及三十五项用户暂缓','原40条复制应为20财务、20非财务；FARMain、ProdInToAPList、ProdOutToARList三条坏目标属于财务。35处非财务查询按用户要求暂缓，保留22外部/11缺列/2缺对象原事实，不算已解决或现场完成。')]
    inventory=read('docs/erp-remaining-inventory-20261016.json')
    axis=inventory['axes']['新旧系统差异及处理情况'];md='## E216～E220：表单、联动与转单撤回\n\n见['+TITLE+']('+TITLE+')。\n\n'
    for number,(name,reason) in enumerate(exceptions,216):
        md+=f'### E{number} {name}\n\n{reason}\n\n'
        item={'id':'E'+str(number),'name':name,'status':'部分完成','reason':reason,'related_sql':[],
            'source':'docs/旧ERP复刻异常与合理实现说明.md'}
        found=next((n for n,r in enumerate(axis) if r['id']==item['id']),None)
        if found is None:axis.append(item)
        else:axis[found]=item
    replace_section(DOCS/'旧ERP复刻异常与合理实现说明.md','phase6-form-flows-exceptions',md)
    paused_names={r['entry'] for r in paused}
    for row in inventory['axes']['旧界面配置入口']:
        if row['name'] in paused_names:row['execution_priority']={'state':'用户明确暂缓','date':'2026-10-17','reason':'本轮先补表单、联动和业务流程；原差异状态保留'}
        added=[r for r in bound if r['entry']==row['name']]
        if added:
            row['models']=list(dict.fromkeys([*row['models'],*[r['model'] for r in added]]))
            row['form_flow_increment']={'write_binding':'原UpdateSQL明确单表','development':'已接表单绑定；其余逐入口联调继续保留','evidence':EVIDENCE}
    inventory['counts']['新旧系统差异及处理情况']=dict(Counter(r['status'] for r in axis))
    for key in ['entry_models','entry_bindings','distinct_bound_entries']:inventory[key]=evidence[key]
    current={k:evidence[k] for k in ['runtime_counts','field_copy_status_counts','paused_query_count','automatic_formula_entries','automatic_formula_targets','remaining_reverse_types']}
    current.update(document=TITLE,evidence=EVIDENCE,development='部分完成',historical_reconciliation='未完成',field_acceptance='未完成')
    inventory['phase6_form_flows_20261017']=current
    inventory['phase6_review']['current_evidence']='docs/'+EVIDENCE
    inventory['phase6_review']['next']='35处非财务查询用户暂缓；先补21条绑定、本地过滤、逐入口事件验证、跨后续单据逆向验证及浏览器整链联调。'
    review=read('docs/erp-phase6-review-20261016.json');review['form_flows_20261017']=current;review['current_review_at']=evidence['verified_at']
    save('docs/erp-phase6-review-20261016.json',review);save('docs/erp-remaining-inventory-20261016.json',inventory)
    print({'document':TITLE,'tests':evidence['tests']['count'],'bindings':len(bound),'paused':len(paused)})


if __name__=='__main__':main()
