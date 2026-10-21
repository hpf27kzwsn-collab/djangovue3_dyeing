"""21条配置补绑和浏览器实测的当前清单，三种完成状态分别记录。"""
import gzip
import hashlib
import json
import re
from collections import Counter
from datetime import datetime
from sync_phase6_continuation import ROOT,DOCS,read,save,replace_section

TITLE='2026-10-17第六阶段21条字段绑定与浏览器联调.md'
EVIDENCE='erp-phase6-field-bindings-verification-20261017.json'


def main():
    previous=read('docs/erp-phase6-form-flows-verification-20261017.json')
    runtime=read('docs/erp-phase6-runtime-review-20261017.json')
    rules=read('backend/plugins/erp_base/source_entry_rules.json')['models']
    overrides=read('tools/legacy_models/entry_binding_overrides.json')
    originals={e['table']['DataTableName']:e for e in json.loads(gzip.decompress((ROOT/'backend/plugins/erp_base/source_phase6_catalog.json.gz').read_bytes()))['entries']}
    closed=[]
    for group in ['identity','copy']:
        for row in previous['unbound_'+group+'_configurations']:
            name=row['entry'];field=row['field']
            targets=[{'model':label,'table':rule['write_binding']['table'],
                      'field':rule['field_aliases'].get(field,field),'binding':rule['write_binding']}
                     for label,entries in rules.items() for entry,rule in entries.items() if entry==name]
            closed.append({**row,'kind_group':group,'targets':targets,'development':'实现及保存测试通过',
                'historical_reconciliation':'未完成','field_acceptance':'未完成'})
    assert len(closed)==21 and all(r['targets'] for r in closed)
    assert runtime['counts']['unbound_identity_configurations']==runtime['counts']['unbound_copy_configurations']==0
    automatic=[]
    for label,entries in rules.items():
        for name,rule in entries.items():
            if rule['write_binding']['source'] not in ['explicit_UpdateSQL','explicit_projection_target']:continue
            events={k:v for k,v in originals[name]['table'].items() if k.endswith('SQL') and k not in ['SQL','UpdateSQL'] and v}
            automatic.append({'entry':name,'model':label,'formula_fields':rule['formula_fields'],
                'events':list(events),'event_sha256':{k:hashlib.sha256(v.encode()).hexdigest() for k,v in events.items()}})
    assert len(automatic)==45
    log='.runtime-temp/phase6/bindings-regression.log'
    match=re.search(r'Ran (\d+) tests in ([\d.]+)s\s+OK',(ROOT/log).read_text(encoding='utf8'))
    assert match,'扩大回归未完成或未通过'
    build='.runtime-temp/phase6/bindings-frontend.log'
    assert 'built in' in (ROOT/build).read_text(encoding='utf8')
    browser=read('.runtime-temp/phase6/browser-evidence.json')
    evidence={'verified_at':datetime.now().astimezone().isoformat(),'closed_configurations':closed,
        'closed_configuration_count':21,'remaining_unbound_identity_and_copy':0,
        'entry_models':len(rules),'entry_bindings':sum(len(r) for r in rules.values()),
        'distinct_bound_entries':len({name for rows in rules.values() for name in rows}),
        'runtime_counts':runtime['counts'],'original_automatic_inventory':automatic,
        'automatic_inventory_counts':{'entries':45,'formula_entries':sum(bool(r['formula_fields']) for r in automatic),
            'formula_fields':sum(len(r['formula_fields']) for r in automatic),'event_entries':sum(bool(r['events']) for r in automatic),
            'event_bindings':sum(len(r['events']) for r in automatic),
            'no_formula_or_event':sum(not r['formula_fields'] and not r['events'] for r in automatic)},
        'manual_parent_formulas':[{'entry':'qry_QuoteRelaRecipe','field':'Remarks','original':'Parent.[Remarks]',
            'handling':'选定配方表头允许显式录入备注；不按重复工卡原码选任意父行。'},
            {'entry':'QueryRecordCheck','field':'GradeID','original':"IIF([avgdots]>parent.[CHECKDots],'B','A')",
             'handling':'保留原GradeID默认配置和显式等级；未确认查询父行与avgdots口径前不自动覆盖等级。'}],
        'paused_nonfinancial_queries':previous['paused_nonfinancial_queries'],'paused_query_count':35,
        'tests':{'count':int(match[1]),'seconds':float(match[2]),'modules':21,'result':'passed','log':log,
                 'sha256':hashlib.sha256((ROOT/log).read_bytes()).hexdigest()},
        'frontend':{'result':'typecheck_and_build_passed','log':build,'warning':'既有大分包提示'},
        'browser':browser,'schema':read('.runtime-temp/phase6/final-schema-check.json'),
        'historical_import_rows_this_run':0,'historical_reconciliation':'未完成','field_acceptance':'未完成',
        'development':'21条字段配置、本地联动及已列自动事件完成必要验证；2条查询父行公式采用显式录入，整入口未全部完成',
        'whole_entry_development_completed':0,
        'old_sql_this_run':'沿用2026-10-17已核对快照；本轮未连接旧SQL，未导入历史数据'}
    files=['source_entry_copy.py','source_entry_rules.json','source_phase6_binding_values.py','source_phase6_auto_values.py',
        'source_phase6_editors.py','source_phase6_entries.py','source_phase6_forms.py','source_services.py','source_documents.py',
        'source_api.py','tests/test_source_phase6_field_bindings.py']
    paths=['backend/plugins/erp_base/'+f for f in files]+['tools/legacy_models/build_entry_rules.py',
        'tools/legacy_models/entry_binding_overrides.json','tools/legacy_models/audit_phase6_runtime.py',
        'web/src/components/ResourceTable.vue','web/src/plugins/erp/BusinessPane.vue','web/src/plugins/erp/OriginalEntryWorkbench.vue']
    evidence['files_sha256']={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
    save('docs/'+EVIDENCE,evidence)
    text=f'''# 第六阶段21条字段绑定与浏览器联调

日期：2026-10-17。本文件接续上一轮表单清单。35项非财务查询继续暂缓，财务暂缓，不新增旧erpID，不删异常或重复来源。

## 本轮结果与完成口径

|范围|开发及必要验证|历史对账|现场验收|
|---|---|---|---|
|原剩余21条身份/续行配置|21条全部有明确原表落点并通过实际保存测试；未绑定数21→0。并非21个完整业务入口全部复刻|未完成|未完成|
|本地过滤B145、B146|2组均按原查询列含义补齐；重复候选、其他工卡排除通过|未完成|未完成|
|前轮37入口自动配置|6项原公式、6条事件绑定逐项核查和验证；30入口原无公式/事件，不再笼统列为37项自动事件待办|未完成|未完成|
|新8入口自动配置|12项原公式中10项按原行/明确子表计算；2项查询父行公式保留显式录入替代，见E222|未完成|未完成|
|浏览器整链|采购录入计算、长度差异报错、来源选择、转入、撤回留档；加捻明细、表头和库存联调，详见后文|未完成；测试不是旧数据|未完成；无现场人员签收|

扩大回归 **{evidence['tests']['count']}项通过，{evidence['tests']['seconds']}秒，21个测试模块**。前端类型检查及构建通过。模型检查仍为766个ERP模型、655个原表模型、12606个原字段、额外旧erpID为0，无新增迁移。本轮没有历史数据导入。

## 21条逐项落点

|序号|原入口|原配置字段|写入原表/字段|处理依据|
|---|---|---|---|---|
'''
    for index,row in enumerate(closed,1):
        target=row['targets'][0]
        reason='原SELECT明确GrayID AS Code，两个名字只写同一个原字段一次' if row['field']=='Code' else target['binding'].get('reason','原单表字段')
        text+=f"|{index}|{row['entry']}|{row['field']}|{target['table']}.{target['field']}|{reason}|\n"
    text+='''
原查询JOIN产生的重复展示行继续保留。写入选择具体原表记录，不将联查倍增误当成多条待更新实体，不合并同码、同条码或同旧主键记录。显式NULL不改成默认零；只有原公式明确ISNULL的输入才按其语义处理。

## 联动与自动事件

- B145：当前工卡SheetNo对查询结果SheetNo；该查询列实际来自WDefect.JobSheetNo，评审单号输出为strSheetNo。
- B146：当前工卡SheetNo对查询结果JobSheetNo，不能拿评审单号SheetNo等值比较。
- 16组原非空过滤关系现有14组明确映射、2组不完整（B153/B197，外部来源随35项暂缓）。11组属于明确补全，其中9组有启用的编辑器；B128原编辑器停用、B210无调用，原配置保留。
- PurDetailList.Amount保存时执行ISNULL(Price,0)×ISNULL(Qty,0)。加捻原5项公式维持明细实际量→表头4项汇总→库存顺序。
- NewFuBan的删除限制和按登录员工、09工位、日夜班的审核检查；qry_Winding_ToCustomer和qry_Order_ToCustomer的原排单删除限制；RequestLimit指定人审核及反审核，共6条事件均有非空服务调用测试。
- DStuffWeight、qry_QuoteRelaStuff自动算ClothNetKg。qry_Employee新增时保留EmpID默认取PosID这一原配置，LoginName/原表Password公式仍使用EmpID；修改EmpID不重新生成仅新增时执行的Password；修改资料时按登录账号和当前业务时间维护Modifyer/ModifyDate，显式值含NULL优先。它是旧员工原表字段，不修改Django登录账号密码。
- QueryRecordCheck自动算CustQty、NetKg、Pound、RealQty、Tubes；QueryRecordDefect2按BarCode→BarCode关联，保存、修改、删除后按SumDots汇总Dots。另一QueryRecordDefect原BarCode→Guid规则保留，不能混用。负数原值和重复疵点均可保留。

45个补绑入口的全部原公式和事件清单在证据JSON的original_automatic_inventory中，共8个入口18项公式、4个入口6条事件绑定；其余33个入口没有这些原配置。不凭空新增未配置事件，也不把它们列成未实现。

## 无法逐字复刻的2项查询父行公式

1. qry_QuoteRelaRecipe.Remarks：原式Parent.[Remarks]依赖查询父行。原报价联查可多行对应一个配方表头，不能根据同工卡原码任取一行。当前提供原备注字段显式录入和保存，不自动覆盖。
2. QueryRecordCheck.GradeID：原式依赖查询列avgdots及父行CHECKDots，原写入表RecordYieldCheck已不在最新旧结构。当前明确采用RecordYield原行，保留原GradeID默认和手填值，其余已确认的原行公式正常执行；尚未证明该查询父行和阈值来源，不能把手填等级称为原自动判级已完成。

这两项与暂缓35个查询的计数分开；代码提供可录入路径，原表达式仍保存、可见，异常清单继续跟踪。

## 浏览器联调与修复

使用独立测试库erp_phase6_browser_20261017，测试单明确标为BROWSER或UI开头。表头/来源由测试夹具建立，采购修改、新增计算、转单、撤回和加捻明细由浏览器操作完成；不将夹具创建冒充浏览器录入。

1. 采购来源物料编码长度11、到货字段最大10时，页面显示原字段长度错误；整次未转入，来源仍在。随后在采购编辑页面把本次测试编码改为FAB-UI，再办理转单。
2. 在PurDetailList入口新增UI-CALC，价格2、数量-3，保存后金额显示-6。没有把负数过滤掉。
3. 采购原行328转入到货通知70，生成明细105，数量-3；浏览器撤回后原行仍显示，新增“已撤回留档”状态，编辑/删除/重复办理按钮退出。该状态读取现有办理记录，没有新增数据库字段。
4. 加捻表头UI-TWIST下新增卷记录：页面原本提交空流水号，修正为按已登记原主从关系显示表头原码，并由服务层绑定；仅处理关联码，不将父单所有字段写进子单。毛重-5、粒数3、净重-4，验证明细实际量、表头合计及库存。
5. 操作时间默认值按项目Asia/Shanghai生成，避免把UTC字符串直接交给无时区日期控件显示。

浏览器记录、测试库结果核对及截图见证据JSON和[撤回留档截图](assets/phase6-transfer-retained-20261017.png)。这些是开发联调证据，不是现场验收；没有声称819个已绑定入口全部经过浏览器逐一验收。

## 后续顺序

1. 当前21条字段配置及2组本地过滤不再作为待办重复计数。保留上述2项父行公式的显式录入替代与原行为差异，取得明确父行、阈值后再自动化。
2. 扩展其余已开发转单和跨后续单据的浏览器回归：部门申请采购、保养领料、报价调价/订单、采购成品入库。现有后端非空回归通过，不等于这些分支本轮全部在浏览器走过。
3. 各模块按原主键、批次、提取行号做历史全量/分批对账，逐条保留重复与异常；不得凭开发测试数量宣称旧数据已导入。
4. 使用真实单据和现场人员验收选路、单位、质量、包装、收发及逆向时点。35项查询和财务仍暂缓；原打印仍为5个固定校样、0个完整原版式，未因本轮补绑自动升级。
'''
    (DOCS/TITLE).write_text(text,encoding='utf8')
    exceptions=[
        ('21条残缺字段绑定的原SQL依据与别名','6条Code为GrayID别名；其余15条按原展示SQL和现有物理字段明确写入8个入口，原查询连接倍增保留，写入选择具体原行。21项保存验证通过不等于入口全部完成。'),
        ('QC缺失写入表及2项查询父行公式','RecordYieldCheck最新原库不存在，采用RecordYield原行，不新增虚构旧表。qry_QuoteRelaRecipe.Remarks与QueryRecordCheck.GradeID缺明确查询父行，已提供显式原字段录入，未自动覆盖，不标原公式已复刻。'),
        ('员工默认编号沿用原岗位代码配置','qry_Employee.EmpID原默认为LoginPeople_EmpPositionID，按原PosID保留；显式输入优先，同码员工不合并。修改时维护Modifyer/ModifyDate，显式NULL仍保留；LoginName与原Password公式仅落旧员工原字段，不改变Django登录凭据。'),
        ('QC疵点两种原主从关联不能混用','QueryRecordDefect2的原关系是BarCode→BarCode；QueryRecordDefect是BarCode→Guid。按入口分别赋原码，明确包装父行参与锁定、汇总及删除刷新。原长Guid与其他入口20字符字段差异仍保留，不能截断旧数据。'),
        ('浏览器发现的主从空码与转单留档可见性','从表头新增明细原来提交空关联码，已依据登记关系显示和绑定；仅派生关联字段。撤回行在列表显示已撤回留档并退出编辑及办理；原值/负数/重复记录仍在。浏览器开发联调不升级为历史对账或现场验收。')]
    inventory=read('docs/erp-remaining-inventory-20261016.json');axis=inventory['axes']['新旧系统差异及处理情况']
    section='## E221～E225：字段补绑及浏览器联调\n\n见['+TITLE+']('+TITLE+')。\n\n'
    for number,(name,reason) in enumerate(exceptions,221):
        section+=f'### E{number} {name}\n\n{reason}\n\n'
        row={'id':'E'+str(number),'name':name,'status':'部分完成','reason':reason,'related_sql':[],
             'source':'docs/旧ERP复刻异常与合理实现说明.md'}
        found=next((i for i,r in enumerate(axis) if r['id']==row['id']),None)
        if found is None:axis.append(row)
        else:axis[found]=row
    replace_section(DOCS/'旧ERP复刻异常与合理实现说明.md','phase6-field-bindings-exceptions',section)
    current=f'''## 当前执行范围：21条字段绑定与浏览器联调（2026-10-17）

35项非财务查询和财务继续暂缓。本节与[当前清单]({TITLE})、[验证证据]({EVIDENCE})为当前口径；下方旧轮次保留作历史记录。

21条身份/续行配置全部补绑，未绑定数21→0；新增8个入口绑定，累计385个模型、840条模型/入口绑定、819个不同入口。补B145/B146后，原16组过滤配置中14组明确映射、2组外部暂缓。45个补绑入口共18项公式、6条事件绑定：16项公式已接自动计算，2项查询父行公式采用显式录入并留异常，6条事件均有非空验证；33入口原无公式或事件。

{evidence['tests']['count']}项扩大回归通过；前端及模型检查通过。浏览器完成采购录入计算、转入撤回留档和加捻主从联调，修复空关联码提交及留档状态展示。**本轮列明增量开发完成；第六阶段整体仍部分完成；历史对账、现场验收均未完成。** 无旧数据导入，无新增旧erpID。后续优先扩展其余转单/跨链浏览器分支，再推进历史对账及现场验收。2项父行公式差异与35项暂缓查询分别计数；原打印5校样/0完整。异常E221～E225。
'''
    for doc in ['2026-10-16染色ERP剩余工作全量盘点清单.md','染色ERP后续开发方案.md']:
        replace_section(DOCS/doc,'phase6-form-flows-current',current)
    replace_section(DOCS/'2026-10-17第六阶段表单联动转单撤回与流程联调.md','phase6-field-bindings-superseded',
        f'## 当前状态更新\n\n本文是前轮记录。原剩余21条绑定和B145/B146已补齐，浏览器发现的问题已修复；最新数量、替代范围、测试及后续顺序以[{TITLE}]({TITLE})为准。')
    for row in inventory['axes']['旧界面配置入口']:
        if row['name'] in overrides['entries']:
            row['models']=list(dict.fromkeys([*row['models'],*[label for label,entries in rules.items() if row['name'] in entries]]))
            row['field_binding_increment']={'development':'本轮列明字段保存已验证，完整入口仍按原状态',
                'historical_reconciliation':'未完成','field_acceptance':'未完成','evidence':EVIDENCE}
    inventory['counts']['新旧系统差异及处理情况']=dict(Counter(r['status'] for r in axis))
    for key in ['entry_models','entry_bindings','distinct_bound_entries']:inventory[key]=evidence[key]
    summary={k:evidence[k] for k in ['runtime_counts','closed_configuration_count','remaining_unbound_identity_and_copy','automatic_inventory_counts','manual_parent_formulas','paused_query_count']}
    summary.update(document=TITLE,evidence=EVIDENCE,development=evidence['development'],historical_reconciliation='未完成',field_acceptance='未完成')
    inventory['phase6_field_bindings_20261017']=summary
    inventory['phase6_review']['current_evidence']='docs/'+EVIDENCE
    inventory['phase6_review']['next']='21条绑定与2组本地过滤已补；2项父行公式显式录入差异保留。继续其余转单/跨链浏览器分支、历史对账及现场验收；35项查询和财务暂缓。'
    review=read('docs/erp-phase6-review-20261016.json');review['field_bindings_20261017']=summary;review['current_review_at']=evidence['verified_at']
    save('docs/erp-remaining-inventory-20261016.json',inventory);save('docs/erp-phase6-review-20261016.json',review)
    print({'closed':len(closed),'unbound_remaining':0,'automatic':evidence['automatic_inventory_counts'],'tests':evidence['tests']['count']})


if __name__=='__main__':main()
