"""登记明确转单及跨链逆向的浏览器证据，不升级历史或现场验收状态。"""
import hashlib
import re
from collections import Counter
from datetime import datetime
from sync_phase6_continuation import ROOT,DOCS,read,save,replace_section

TITLE='2026-10-17第六阶段其余转单与跨链逆向浏览器联调.md'
EVIDENCE='erp-phase6-cross-browser-verification-20261017.json'


def main():
    browser=read('.runtime-temp/phase6/cross-browser-evidence.json')
    prior=read('docs/erp-phase6-field-bindings-verification-20261017.json')
    log='.runtime-temp/phase6/cross-regression.log'
    match=re.search(r'Ran (\d+) tests in ([\d.]+)s\s+OK',(ROOT/log).read_text(encoding='utf8'))
    assert match,'扩大回归没有完成或未通过'
    branches=[
        ('配件部门申请→采购→撤回一行','同一申请、同一明细号转入2行：-2×3=-6、5×4=20；只撤回负数行，另一行仍有效。'),
        ('染化料部门申请→采购→撤回','数量-3、单价2、金额-6；撤回后采购原行与申请来源都保留。'),
        ('保养计划→配件领料→审核→重办→撤回→再审核','2次转单，初次库存为-2和5；重新办理并撤回负数行后，再审核库存仅为5，2条原明细仍在。'),
        ('报价→调价→重复转入→逐次撤回','报价原行2条同明细号、同数值色号；2次调价均留档。撤回第二条恢复UI-AD1/12；再撤回第一条，AdjustPrice与关联号为NULL，原DateType/StartDate保持原删除行为。'),
        ('报价→订单→整单撤回','生成UI-ORDER和UI-OC；整单撤回后表头与子行都留档，报价来源未删除。'),
        ('采购→成品入库→整单撤回','显式重量口径-4、粒数2；当前入库库存退出，1条撤回前库存快照保留，采购和入库原行仍在。'),
    ]
    modes=[
        ('撤销执行、原计划保留；原删除触发及独立进度维护','11条执行原行、4条原库存流水；撤销后净库存为0，恢复后成品净量20、染化料出库-3。原行、负数和反记均保留，另一工卡同条码包装不受影响。'),
        ('撤销执行及本次拆卡计划；仅原删除触发回写','浏览器新拆卡26101701，计划-4/1；包装与入库2条执行来源、1条库存。联合撤销后新卡计划0/0、净库存0；撤回后计划-4/1、库存-4。原卡单位空，原计划20/2保持，不臆测换算。'),
    ]
    evidence={'verified_at':datetime.now().astimezone().isoformat(),
        'scope':'既有明确转单的剩余6个业务分支及2种跨链逆向组合；不是所有原入口全部验收',
        'transfer_branch_count':len(branches),'cross_chain_mode_count':len(modes),
        'browser_scenarios':[{'name':name,'result':result,'development':'浏览器及结果核对通过',
            'historical_reconciliation':'未完成','field_acceptance':'未完成'} for name,result in branches+modes],
        'browser':browser,'schema':read('.runtime-temp/phase6/final-schema-check.json'),
        'tests':{'count':int(match[1]),'seconds':float(match[2]),'modules':22,'result':'passed','log':log,
            'sha256':hashlib.sha256((ROOT/log).read_bytes()).hexdigest()},
        'frontend':'本轮未修改前端源码；使用既有构建通过浏览器调用新增动作参数。前轮构建结果不重复算成本轮构建。',
        'paused_query_count':35,'paused_nonfinancial_queries':prior['paused_nonfinancial_queries'],
        'manual_parent_formulas':prior['manual_parent_formulas'],
        'historical_import_rows_this_run':0,'historical_reconciliation':'未完成','field_acceptance':'未完成',
        'whole_entry_development_completed':0,'original_print_complete':0,'original_print_proofs':5,
        'old_sql_this_run':'未连接旧SQL Server；本轮验证在独立合成测试库进行。',
        'exception_ids':['E226'],
        'screenshots':['docs/assets/phase6-cross-chain-cancelled-20261017.png']}
    paths=['backend/plugins/erp_base/'+name for name in ['source_transfer_numbers.py','source_phase6_transfers.py',
        'source_phase6_forms.py','source_api.py','tests/test_source_phase6_transfer_numbers.py']]
    evidence['files_sha256']={path:hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in paths}
    save('docs/'+EVIDENCE,evidence)
    text=f'''# 第六阶段其余转单与跨链逆向浏览器联调

日期：2026-10-17。承接上一轮清单第2项“其余转单和跨后续单据浏览器回归”。35项非财务查询、财务继续暂缓；没有新增旧erpID，没有导入旧数据。

## 本轮结论与范围

**清单列明的6个剩余明确转单分支及2种跨链逆向组合，已完成本轮开发联调。** 发现并修复1类实际代码缺口：异常原号导致自动编号不能递增时，转单窗口缺少手填目标原编号的路径。5个转单动作现提供8个可选原编号输入。

这不是“全部原ERP已复刻”的结论。此前缺原视图、原客户端生成时点的明确替代仍按原异常记录保留；35项查询不因浏览器联调升级为已完成。

|范围|开发及必要验证|历史数据对账|现场验收|
|---|---|---|---|
|本轮6个明确转单分支|通过，逐项见下表|未完成|未完成|
|2种跨链撤销/恢复组合|通过，原单、原库存及反记逐项核对|未完成|未完成|
|5个动作的8项目标原编号输入|通过；原规则与手填分别验证，重复编号不合并|未完成|未完成|
|第六阶段整体|仍部分完成|未完成|未完成|

扩大回归 **{evidence['tests']['count']}项通过，{evidence['tests']['seconds']}秒，22个模块**。其中本轮新增3项测试已包含在总数内，不重复累计。Django检查及迁移检查通过；766个ERP模型、655个原表模型、12606个原字段、额外旧erpID为0，没有新迁移。前端源码本轮未改，浏览器使用既有构建读取新增动作参数。

## 逐分支浏览器结果

|序号|业务链|已核实结果|
|---|---|---|
'''
    for number,(name,result) in enumerate(branches+modes,1):text+=f'|{number}|{name}|{result}|\n'
    text+='''
采购转到货通知和加捻主从录入为前轮已验证范围，本轮没有将其重新计入6个“剩余转单分支”。采购成品入库本轮浏览器采用重量分支；长度口径已有服务测试，本轮不声称两种口径都通过了页面操作。订单已开卡时的撤回限制、失败回滚、权限范围、重复撤销限制继续由已有非空自动测试覆盖，不冒充全部已在本轮浏览器逐项操作。

## 原编号缺口及修复

实际复现：浏览器测试库已有非数字明细号，部门申请转采购沿用原自动编号时报“现有原号的数值部分不能按本编号规则递增”，窗口却只能填写数量、单价，无法按错误提示继续办理。

|动作|可显式填写的旧表原字段|
|---|---|
|部门申请转采购（配件/染化料共用）|PurDetail.DetailNo|
|保养计划领料|ArticleOutDetail.DetailNo|
|报价转调价|PriceAdjustDetail.DetailNo|
|报价转订单|OrderMain.SheetNo、OrderMain.SheetSeries、OrderColor.CheckNo|
|采购转成品入库|ProdIn.SheetNo、ProdIn.SheetSeries|

这些是操作窗口参数，直接写入已有原字段，没有新增模型字段。留空仍执行原自动编号；填写时采用明确原值，不截断、不清理异常旧号、不挑选“看起来正常”的号码重试，也不合并相同编号的转入记录。字段长度按目标原字段验证，失败整次回滚。现有来源快照和操作记录继续记录原行、目标编号与办理者。

新增测试覆盖：非数字既有原号触发原错误后，同一个手填号可在两类部门申请各转2次；领料与调价的手填号实际落库；订单头、子行及入库原号实际落库；超长订单明细号不留下半张订单。全部保存及逆向逻辑仍在service层，页面只提供操作输入。

## 跨链数量核对

第一组工卡为UI-CHAIN。测试准备了报工、报工步骤、称料头/阶段/明细、实际领料、包装、入库、发货头/明细及退货，共11条执行来源。4条原库存流水的原值一直保留：成品20、-20、20；染化料出库-3。

|时点|成品库存行数/净量|染化料库存行数/净出库|执行原行|
|---|---|---|---|
|撤销前|3行/20|1行/-3|11条有效|
|撤销后|6行/0|2行/0|11条留档，退出活动办理|
|撤回撤销后|9行/20|3行/-3|11条恢复；反记及恢复流水均留档|

其中染化料原库存缺具体明细对应，页面明确列出异常，按完整原表头流水归属反记；没有跳过该来源。另一工卡同条码包装数量100保持有效。负数报工-2、实际称料-3保持原值。

第二组在浏览器从UI-CHAIN拆出新卡26101701。原卡AssignUnit为空，新卡明确采用1；按已有拆卡规则原计划不擅自扣减，新卡负数计划完整保存。随后测试准备新卡包装和入库。联合撤销使新卡计划归零并反记库存；撤回后新卡计划-4/1、库存-4完整恢复，原卡20/2始终保持。

## 证据来源与限制

使用独立库erp_phase6_browser_20261017。申请、采购、报价、保养来源及关联测试原行由夹具准备；六分支的转单、审核、重办、撤回，以及拆卡、两组整链撤销和恢复均由浏览器办理。拆卡后包装、入库和库存是补充夹具，不称为浏览器创建。全部为合成数据，不是历史导入或现场真实单据。

每次办理后用数据库只读查询核对目标行、活动范围和库存，并在撤销与恢复两个时点保存证据。完整字段、记录ID和结果见[验证JSON](erp-phase6-cross-browser-verification-20261017.json)；页面结果见[整链撤销截图](assets/phase6-cross-chain-cancelled-20261017.png)。本轮没有连接旧SQL Server。

## 当前后续顺序

1. 本文6个转单分支及2种跨链组合退出“尚未做浏览器联调”待办；不再重复列为未实现代码。其余完整入口、其他组合及原界面的逐入口核验仍按全量盘点原状态进行，不能用8个场景代表819个入口。
2. 历史数据按原表主键、来源批次和提取行号开展分批对账，数量、单位、重复键、NULL、负数及原异常全部逐行保留。导入量为0，不把测试原行数当作历史核验数量。
3. 现场使用真实单据确认单位、责任工序、实际选路、质量与库存时点及逆向业务。开发联调通过不能代替现场签收。
4. 2项查询父行公式仍采用显式录入替代，等待明确父行/阈值后继续自动化；原打印仍5份校样、0份完整原版式。35项查询和财务按要求暂缓，其既有差异不删除。
'''
    (DOCS/TITLE).write_text(text,encoding='utf8')
    reason='自动编号遇非数字原号时，原转单窗口没有可输入目标编号的路径；本轮为5个动作补8项原编号参数，空白按原自动规则，显式原号照录。异常原号不删除或略过，重复转入和重复编号逐行保留，超长值整次回滚。此为明确办理路径，不冒充未知旧客户端编号行为；历史和现场未验收。'
    replace_section(DOCS/'旧ERP复刻异常与合理实现说明.md','phase6-cross-browser-exceptions',
        '## E226 转单遇异常原号时的显式编号路径\n\n'+reason+'\n\n见['+TITLE+']('+TITLE+')，六分支和两种跨链组合已完成本轮浏览器验证。既有缺原视图/生成时机差异仍保留。')
    current=f'''## 当前执行范围：其余转单与跨链逆向浏览器联调（2026-10-17）

本节及[当前清单]({TITLE})、[验证证据]({EVIDENCE})为最新口径，下方旧轮次为历史记录。35项查询、财务继续暂缓。

清单所列6个剩余明确转单分支、2种跨链逆向组合通过浏览器及结果核对。修复自动编号遇异常旧号时无手填路径的问题：5个转单动作增加8项已有原编号输入。重复编号、负数、异常库存来源与全部撤回原行继续保留。扩大回归{evidence['tests']['count']}项通过，模型/迁移检查通过；无新字段，无额外旧erpID，无历史数据导入。异常E226。

**本轮列明增量开发完成；第六阶段整体仍部分完成；历史对账、现场验收均未完成。** 21条身份/续行未绑定数仍为0；385个模型、840条绑定、819个不同入口的数量不变。2项查询父行公式仍为显式录入替代，原打印5校样/0完整，35项暂缓查询不减少。下一步按原键/批次/行号开展历史对账，并按真实单据组织现场验收；其他原入口仍按全量清单原状态核验，不能把本轮8个场景当作所有入口完成。
'''
    for doc in ['2026-10-16染色ERP剩余工作全量盘点清单.md','染色ERP后续开发方案.md']:
        replace_section(DOCS/doc,'phase6-form-flows-current',current)
    replace_section(DOCS/'2026-10-17第六阶段21条字段绑定与浏览器联调.md','phase6-cross-browser-superseded',
        f'## 后续状态更新\n\n本文件原第2项后续任务所列6个转单分支及2种跨链逆向组合已完成本轮浏览器验证；编号缺口已修复。最新状态见[{TITLE}]({TITLE})，本文其余原证据保留。历史对账、现场验收仍未完成。')
    inventory=read('docs/erp-remaining-inventory-20261016.json');axis=inventory['axes']['新旧系统差异及处理情况']
    row={'id':'E226','name':'转单遇异常原号时的显式编号路径','status':'部分完成','reason':reason,
        'related_sql':[],'source':'docs/旧ERP复刻异常与合理实现说明.md'}
    found=next((i for i,r in enumerate(axis) if r['id']=='E226'),None)
    if found is None:axis.append(row)
    else:axis[found]=row
    inventory['counts']['新旧系统差异及处理情况']=dict(Counter(r['status'] for r in axis))
    summary={'document':TITLE,'evidence':EVIDENCE,'transfer_branch_count':6,'cross_chain_mode_count':2,
        'development':'本轮列明场景通过浏览器及结果验证','historical_reconciliation':'未完成','field_acceptance':'未完成',
        'paused_query_count':35,'tests':int(match[1])}
    inventory['phase6_cross_browser_20261017']=summary
    inventory['phase6_review']['current_evidence']='docs/'+EVIDENCE
    inventory['phase6_review']['next']='本轮六个明确转单分支及两种跨链组合浏览器联调已完成。后续历史分批对账、现场真实单据验收及其他原入口按清单核验；2项父行公式和原打印差异保留，35项查询及财务继续暂缓。'
    review=read('docs/erp-phase6-review-20261016.json');review['cross_browser_20261017']=summary;review['current_review_at']=evidence['verified_at']
    save('docs/erp-remaining-inventory-20261016.json',inventory);save('docs/erp-phase6-review-20261016.json',review)
    print(summary)


if __name__=='__main__':main()
