"""将只读结构及关系核验结果整理为可追溯Markdown，不修改业务代码或数据。"""
import json,hashlib
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'.runtime-temp/model-compare-live-20261018';D=ROOT/'docs'
def read(name):return json.loads((P/name).read_text(encoding='utf8'))
def cell(v):return str(v if v is not None else 'NULL').replace('|','\\|').replace('\n',' ').replace('\r',' ')
def row(*v):return '| '+' | '.join(map(cell,v))+' |\n'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
a=read('comparison.json');s=read('structure-and-logic.json');counts=read('relation-counts.json');extra=read('extra-counts.json');plans=read('extra-select-plan.json');newdb=read('new-database.json')
byid={r['id']:r for r in counts};exid={r['id']:r for r in extra}
assert len(counts)==len(a['relations'])==165 and all(r['status']=='checked' for r in counts+extra)
for r in counts+extra:assert r['child_rows']==sum(r[k] for k in ['null_key_rows','missing_parent_rows','unique_parent_rows','multiple_parent_rows'])
assert len(a['fields'])==12606 and not any(r['differences'] for r in a['fields'])
assert len(a['tables'])==690 and sum(bool(t['models']) for t in a['tables'])==655
assert all(t['handling']=='finance_excluded' for t in a['tables'] if not t['models'])
assert all(t['key_metadata_equal'] and not t['extra_source_fields'] for t in a['tables'] if t['models'])
assert not a['extra_legacy_id_fields'] and not a['new_source_tables_missing_old']
legacy_fields={r['table']+'.'+r['field']:r for r in a['fields']}
legacy_model_tables={r['model']:r['table'] for r in a['fields']}
main='2026-10-18新旧ERP模型字段与关联核对报告.md'
tables='2026-10-18新旧ERP逐表与关联核对明细.md'
fielddoc='2026-10-18当前系统全部模型字段明细.md'
old=json.loads((ROOT/'tools/legacy_models/schema.json').read_text(encoding='utf8'))
summary={'captured_at':s['captured_at'],'old_tables':690,'old_fields':13268,'source_models':655,'source_fields':12606,
    'finance_tables_paused':35,'finance_fields_paused':662,'django_registered_models':len(a['models']),
    'erp_models':sum(m['erp'] for m in a['models']),'field_declaration_differences':0,
    'old_fk_groups':len(a['foreign_keys']),'fk_group_matching':sum(bool(r['matched_relation']) for r in a['foreign_keys']),
    'source_relations':165,'relations_with_data':sum(r['child_rows']>0 for r in counts),'empty_relations':sum(r['child_rows']==0 for r in counts),
    'relations_with_missing_parent':sum(r['missing_parent_rows']>0 for r in counts),'relations_with_null_key':sum(r['null_key_rows']>0 for r in counts),
    'relations_with_multiple_parent':sum(r['multiple_parent_rows']>0 for r in counts),
    'ui_relation_states':dict(Counter(r['status'] for r in a['ui_relations'])),
    'schema_fields_unchanged_since_saved_snapshot':old['fields']==s['fields'],
    'live_new_database':newdb,'historical_reconciliation':'未完成','field_acceptance':'未进行',
    'operation':'仅SQL Server SELECT、Django内存元数据读取、新库只读连接尝试；未修改业务代码、未生成迁移、未导入数据',
    'evidence':{str(p.relative_to(ROOT)):sha(p) for p in [P/'structure-and-logic.json',P/'comparison.json',P/'relation-counts.json',P/'extra-counts.json',P/'relation-select-plan.json',P/'extra-select-plan.json',P/'new-database.json',ROOT/'tools/legacy_models/source_catalog.json']}}
(D/'erp-model-relation-comparison-20261018.json').write_text(json.dumps({'summary':summary,'tables':a['tables'],'relations':a['relations'],'relation_counts':counts,'additional_counts':extra,'additional_plans':plans,'foreign_keys':a['foreign_keys'],'ui_relations':a['ui_relations']},ensure_ascii=False,indent=2),encoding='utf8')
text=f'''# 当前系统与旧ERP模型、字段及关联关系核对报告

核验日期：2026-10-18（北京时间）。旧库：localhost / Textile_GXHFRS；结构采集时间：{s['captured_at']}。

## 结论

**原表与原字段的声明覆盖已对齐，但两套系统的数据库约束、关联执行和部署状态不能判为完全一致。**

- 本次实际连接旧SQL Server核验了全部690张表、13,268个字段。当前655个原表模型对应12,606个原字段，逐字段比较未发现缺字段、额外原字段、类型映射、NULL、长度、小数精度、默认规则、自增规则或排序规则元数据差异。
- 剩余35张旧表、662个字段全部已在原目录登记为财务暂缓对象，没有本次才发现而未登记的旧表。**这35张财务表与此前暂缓的35项查询是两个不同集合，数量相同不代表同一件事。** 所有35张表逐项列在附件。
- 原主键字段保留，589张有原主键的表及66张无原主键的表，其 `SOURCE_KEY` 元数据与旧库一致；但Django实际主键为新系统 `id`，原主键列是普通原值字段。589张表没有照搬原数据库主键约束，因此“原键字段一致”不能说成“实际主键结构相同”。
- 旧库7组真实外键（10个字段配对）中，5组找到新模型显式关系，2组未找到；已匹配5组也使用可空的附加关联字段和PROTECT删除行为，与原CASCADE/NO_ACTION不等价。
- 新模型165条显式原关系字段与目标声明有效，全部完成旧数据基数核验；其中68条有数据、97条当前无子记录。14条出现非空关联码无父匹配，1条存在空关联码，均逐项保留。不能把这些统计直接当作14个模型错误，也不能忽略。
- 原界面547条主从配置逐条登记：309条字段配对匹配显式关系；33条未匹配显式关系；198条涉及非直接物理表、查询别名或暂缓对象；2条字段配置不完整；5条父入口缺失或重名。33条中已有服务按原码关联的情况另作说明，不能全部宣称“功能缺失”。

**当前可下的结论：字段复刻声明检查通过；关联与约束等价性仍部分完成。** 本轮没有修改业务模型或service，也没有导入任何旧数据。

## 1. 核验范围和准确分母

|范围|数量|说明|
|---|---:|---|
|旧库全部物理表|690|包括财务暂缓表，不含177个视图|
|旧库全部物理字段|13,268|非本次只取业务抽样|
|已建原表模型|655|纳入复刻的655张旧表各对应1个原表模型，没有重复映射|
|已建原字段|12,606|全部逐字段比较|
|财务暂缓表/字段|35 / 662|单列，不删除原目录登记|
|当前ERP模型|766|655原表模型＋111个新系统业务/辅助模型|
|当前全部注册模型|800|另外34个Django/系统/第三方支撑模型|
|全部模型字段声明|24,868|含继承字段和M2M，按模型计数；不是24,868个旧字段|
|全部模型关系字段声明|4,885|含继承审计用户/部门、导入批次等，不等于旧业务关联数|
|旧库SQL定义|732|358过程、177视图、112触发器、76标量函数、6表值函数、3内联表值函数；只读定义，没有执行|
|原界面配置|1,682条入口 / 48,962条字段配置|本轮读取当前配置，用于主从关系证据|

新系统800个注册模型的每个字段、目标模型、NULL、主键、唯一性和删除行为均列在[全部模型字段明细]({fielddoc})；111个新增ERP模型及34个系统模型不强行与旧表做一对一比较。自动生成的M2M中间表未另外算成注册模型。

## 2. 逐字段检查通过的内容及边界

|检查项|本次结果|判定范围|
|---|---|---|
|原字段覆盖与原名映射|12,606项通过，缺少0、额外原字段0|旧表列 → SOURCE_FIELDS → Django实际字段|
|类型、NULL、字符串声明长度、小数精度|12,606项通过|按SQL Server到Django的已声明类型映射比较|
|原默认值|508个定义均与SOURCE_DEFAULTS一致|默认值在service执行，不是数据库default完全相同|
|原自增|44个字段及seed/increment规则一致|原字段仍由服务分配；不是原IDENTITY直接搬迁|
|原主键元数据|655表一致，其中589有原键、66无原键|原有字段保存；新系统使用独立id定位|
|排序规则元数据|7,732个字符字段均保留Chinese_PRC_CI_AS|PostgreSQL列未直接设置同名SQL Server排序规则|
|旧计算列 / CHECK约束|均为0|不代表业务公式或校验为0；其余在触发器、入口、服务层|
|与项目保存的2026-10-14结构比较|13,268个字段定义、外键字段清单、CHECK清单相同|本轮确实重新读取了旧库，而非仅比较旧快照|
|额外旧erpID字段|0|本轮未新增字段|

仍需保留的语义差异：SQL Server varchar长度按字节限制，而PostgreSQL字符长度按字符计；tinyint/smallint统一使用IntegerField扩大允许范围；char/nchar固定长度与普通CharField的填充语义不同；datetime/smalldatetime/time的精度、时区解释需按样本复验。小数精度已核对，但上述跨数据库差异不能通过“字段类型映射正确”自动关闭。

原表有680个索引，其中606个唯一索引（包含589个主键索引）。原表模型声明1,133个索引，多数按来源批次和原码建立，并包括大小写/尾空格表达式索引；655个模型各有来源批次＋提取行号唯一约束。**这些不是原索引、原唯一约束的逐个等价复制。** 原字段自身未声明unique；这样能够保留跨批次和无唯一键来源数据，但新业务的重复约束需要由对应入口规则明确承担，不能据此宣称完全一致。

## 3. 真实外键的具体差异

|原外键|来源→目标|新显式关系|旧删除/更新行为|结论|
|---|---|---|---|---|
'''
for f in a['foreign_keys']:
    text+=row(f['name'],f['source']+'('+','.join(f['source_fields'])+') → '+f['target']+'('+','.join(f['target_fields'])+')',f['matched_relation'] or '无',f['delete']+'/'+f['update'],'配对存在，但可空附加FK/PROTECT不同' if f['matched_relation'] else '原模型未声明该显式关系')
text+='''
两组没有显式关系的是 `s_DBComboValue.ComboID → s_DBCombo.ComboID` 和 `s_LookupColumn.LookUpID → s_Lookup.LookupID`，均属于旧平台配置表。它们的原字段已保留，不能把“没有附加FK”解释为原数据字段丢失，但配置父子维护、删除/改码连带处理还需验证。

原 `p_CustRelation → p_Customer` 外键处于启用但不受信任状态，其余6组启用且受信任。新模型附加关系指向新id，旧码另外保留。旧库自动级联与Django保护删除不是同一行为；即使专用service实现了某条撤销链，也要对具体链提供验证，不能在此整体判等价。

## 4. 165条显式关联的实际数据结果

每条关系按旧库自身比较规则，用原字段统计完整子表，不做去重、不用TOP抽样。四类互斥：关联键含NULL、非空键无父行、唯一父行、多个父行；程序验证四类之和等于该关系的子行数。165条查询均成功，未忽略空表或异常行。

- 68条存在子记录，97条为空表；空表只能证明查询和字段有效，不能证明实际流程已验收。
- 14条出现无父匹配，按关系累计579,744次；1条有571个空关联键。**这些是关系命中次数，同一条原记录可以参与多个关系，不能相加当作唯一异常记录数。**
- 在本次165条指定关联键下，多父匹配为0；这不代表全库不存在重复条码、重复业务编号或其他关联上的重复。

|关系|原字段配对|子表总行|非空键无父匹配|空关联键|解释|
|---|---|---:|---:|---:|---|
'''
for r in a['relations']:
    c=byid[r['id']]
    if not(c['missing_parent_rows'] or c['null_key_rows']):continue
    reason='原行保留；需结合历史生命周期、来源和删除记录解释，不能自动改码'
    if r['source_table']=='PurDetail':reason='同一明细支持三类表头，此两路无命中；PurMain一路580/580命中，不能报为580条丢父单'
    if r['source_table']=='RecordEmp':reason='另查BarCode→BarCode仍577705/577705无匹配；不能仅换关联字段解决'
    if r['source_table']=='WDefectPenalty':reason='SheetSeries一路571条无匹配，WDefectNo一路571条均NULL；不能凭另一空键补造父单'
    text+=row(r['id'],r['source']+'('+','.join(r['source_fields'])+') → '+r['target_table']+'('+','.join(r['target_fields'])+')',c['child_rows'],c['missing_parent_rows'],c['null_key_rows'],reason)
text+='''
包装人员的两种关联有旧配置/旧SQL依据：`QueryRecordEmp`用BarCode→Guid；`QueryRecordEmp2`及原V_RecordYield等视图使用BarCode→BarCode。项目 `source_package_people.py` 已分别保留legacy_barcode/entry_guid两种服务逻辑，本轮两种关系都核对了旧库全量人员记录，均无匹配。这只能证明当前库中这些原值无法相连，不能推断这些人员数据无效、应该删除，或凭空决定应连哪条包装记录。

历史导入的 `source_import.link_relations` 仅在同来源批次内唯一匹配时建立附加FK；原码一直保存。旧码找不到或存在多候选时，关系可能保持空，并不代表该行被跳过。实际导入后是否完整保留以及对账结果，本轮没有执行，因此不标为已对账。

## 5. 原界面关系与服务层关系

547条主从配置不是547条独立外键：多个入口可能共用同一物理表，也可能是查询筛选、同表选择或父查询投影。分类结果如下，全部逐入口留在附件，没有去掉财务、停用或不常用配置。

|类别|入口配置条数|结论|
|---|---:|---|
|字段配对匹配显式原关系|309|静态配对匹配，不等于保存和撤销全部验证|
|未匹配显式关系|33|见下表，需区分已有原码服务、查询选择及待补父子入口|
|非直接物理表/查询别名/暂缓对象|198|需解析查询来源或保持原暂缓范围，不能直接算模型缺失|
|关联字段配置不完整|2|原配置本身未提供完整字段配对|
|父入口缺失或重名|5|不能唯一确定父入口|

33条中24条属于s_平台配置入口，9条为其他入口。后者包括：6条入口对应5组具体业务主从；DefectiveInRecord已有RAW_LINKS原码服务；h_EmpRole有部分按RoleNo使用的服务；qry_GetOrderColorToJob属于OrderColor同表查询选择。**已有专用服务的不能因为缺FK就标为完全未实现；其保存、删除和主从入口是否完整，仍需对应验证。**

|原入口|子表→父表|字段配对|本轮判断|
|---|---|---|---|
'''
for r in a['ui_relations']:
    if not r['status'].startswith('未匹配'):continue
    note='未找到模型显式关系；需逐入口核对维护行为'
    if r['entry']=='DefectiveInRecord':note='source_phase6_formula_links.RAW_LINKS已有原码关系；3行均唯一匹配，不能报为关系完全缺失'
    elif r['entry']=='h_EmpRole':note='source_phase5_operations中存在RoleNo用法；53行唯一匹配，父子维护未验收'
    elif r['entry']=='qry_GetOrderColorToJob':note='同表查询选择，不应直接添加自外键；80053行按配对唯一匹配'
    elif not r['table'].startswith('s_'):note='业务主从显式关系未登记；原数据可唯一关联，需补核具体入口/服务'
    text+=row(r['entry'],r['table']+' → '+r['parent_table'],','.join(r['source_fields'])+' → '+','.join(r['target_fields']),note)
text+='''
5组业务主从的只读结果：TightTubeDetail→TightTube 1,197行；CarryMaterialDetail→CarryMaterial 74,959行；JingShaRegisterDetail→JingShaRegister 6行；SwipeEmpEditDetail→SwipeEmpEdit 1行；TightTubePlanDetail→TightTubePlan 146行，全部唯一匹配。TightTubeDetail有取消/结案两个入口，因此是6条入口、5组配对。表有数据且原关系明确，后续不能因不常用而跳过。

还存在原SQL中的跨表JOIN、动态SQL、取TOP、按条件选择不同父表等关系。此次读取了732个SQL定义并针对上述关键差异追查；**没有完成全部SQL语句与所有service的逐分支语义等价证明**。因此不能把309条静态匹配或165条数据统计当作“所有业务关联已复刻”。现有service会使用原码查询，显式FK只是关系的一部分。

## 6. 当前新库部署状态

当前项目配置指向 `127.0.0.1:5439 / erp_full_trial_20261014`。本次连接超时，系统监听检查未发现5439服务，未擅自启动或切换数据库。因此：

- 本报告的“新模型”指当前工作目录经Django加载的真实模型声明。
- 尚未核对该新库实际建表、迁移应用、实际数据库索引/约束及已导入记录。
- 没有将之前5440测试库的测试结果当作5439当前新库部署结果。
- 业务代码开发状态、历史数据逐行对账、现场验收仍分开登记；后两项本轮未完成。

## 7. 后续处理顺序

1. 在当前新库可连接时补做部署结构核验：字段、实际约束、迁移状态；与本报告代码声明分开记录。
2. 优先补核上述5组业务主从的页面入口、父子来源、保存、删除与撤销链；保留原码及全部原行，不随意新增唯一约束。
3. 核对2组平台真实FK及其他平台配置父子维护，明确旧级联行为在新服务中的对应；查询型同表关系不机械改成FK。
4. 对RecordEmp、WDefectPenalty、JobCombine及其余未命中关系按历史来源逐项解释。采购多表头分别检查，不把未选表头当成异常。
5. 对字符串排序、尾空格、大小写、字符长度、日期精度及服务默认值绕行风险做针对性实际数据库验证，再开展历史逐行对账和现场验收。

原35项查询、打印和财务继续按要求暂缓；本次只读取结构和定义，未执行打印、财务或旧业务存储过程。所有异常、重复及空关系都保留证据，未进行清洗或删除。

## 8. 证据、附件与一致性说明

'''
text+=f'''- [逐表、全部显式关联、全部界面主从配置明细]({tables})。
- [全部800个模型的24,868个字段声明及12,606个原字段比较]({fielddoc})。
- [可复核JSON统计与关系结果](erp-model-relation-comparison-20261018.json)。
- 当前完整结构/定义快照：`.runtime-temp/model-compare-live-20261018/structure-and-logic.json`，SHA256：`{sha(P/'structure-and-logic.json')}`。
- 可重复执行的只读核验工具：`tools/legacy_models/compare_live_structure.py`、`tools/legacy_snapshot/verify_relation_cardinality.ps1`、`tools/legacy_models/report_live_structure.py`。SELECT计划及逐条时间在同一核验目录保留。

旧库快照隔离未开启，本次结构及计数为顺序SELECT，不是统一业务时点的事务快照；若现场期间继续录入，跨查询计数可能变化。本轮用于结构与关联问题盘点，不作为切换库存或财务结算基准。未使用NOLOCK，也没有为核验改变隔离设置。
'''
(D/main).write_text(text,encoding='utf8')

detail=f'# 新旧ERP逐表与关联核对明细\n\n核验时间：{s["captured_at"]}。结论与限制见[{main}]({main})。数量按原表、配置行和关系分别计数，不混加。\n\n## 全部690张旧表\n\n|旧表|新模型|原字段数|原主键|原索引/唯一索引|处理状态|说明|\n|---|---|---:|---|---|---|---|\n'
for t in a['tables']:detail+=row(t['table'],'、'.join(t['models']) or '未建立原表模型',t['fields'],','.join(t['primary_key']) or '无',str(t['indexes'])+'/'+str(t['unique_indexes']),'原字段声明通过' if t['models'] else '财务暂缓',t['reason'])
detail+='\n## 全部165条显式原关系及完整计数\n\n目标为原码配对；新附加FK均可空、PROTECT，结构检查与流程验收含义不同。\n\n|编号|子表字段|父表字段|新关联字段|子行数|空键|无父匹配|唯一匹配|多父匹配|证据|\n|---|---|---|---|---:|---:|---:|---:|---:|---|\n'
for r in a['relations']:
    c=byid[r['id']];detail+=row(r['id'],r['source']+'.'+','.join(r['source_fields']),r['target_table']+'.'+','.join(r['target_fields']),r['field'],*[c[k] for k in ['child_rows','null_key_rows','missing_parent_rows','unique_parent_rows','multiple_parent_rows']],'；'.join(r['evidence']))
detail+='\n## 追加32条关系统计\n\n包括可直接按原字段核验的31组未匹配关系和1种RecordEmp条码变体；配置入口可能共用一组配对，原配置行仍全部保留。\n\n|编号|入口|子表→父表|字段配对|子行数|空键|无父|唯一|多父|\n|---|---|---|---|---:|---:|---:|---:|---:|\n'
for p in plans:
    c=exid[p['id']];detail+=row(p['id'],p['entry'],p['source']+' → '+p['target'],','.join(p['source_fields'])+' → '+','.join(p['target_fields']),*[c[k] for k in ['child_rows','null_key_rows','missing_parent_rows','unique_parent_rows','multiple_parent_rows']])
detail+='\n## 全部547条旧界面主从配置\n\n原行号为本轮按DataTableName排序的配置行号；不去重，不把查询别名直接当物理表。\n\n|配置行|入口|原TableName|父入口|父TableName|源→目标字段|静态分类|显式关系|\n|---:|---|---|---|---|---|---|---|\n'
for r in a['ui_relations']:detail+=row(r['row'],r['entry'],r['table'],r['parent_entry'],r.get('parent_table'),','.join(r['source_fields'])+' → '+','.join(r['target_fields']),r['status'],','.join(r['matches']))
detail+='\n## 732个旧SQL定义的读取登记\n\n本表证明定义已获取或原定义为空，不证明每个SQL业务分支已与服务层等价。未执行这些过程、触发器、函数或视图查询。\n\n|对象|类型|定义字符数|定义SHA256|\n|---|---|---:|---|\n'
for r in s['modules']:detail+=row(r['schema_name']+'.'+r['object_name'],r['type_desc'],len(r['definition'] or ''),hashlib.sha256((r['definition'] or '').encode()).hexdigest())
(D/tables).write_text(detail,encoding='utf8')

full=f'# 当前系统全部模型字段明细\n\n结论见[{main}]({main})。Django注册模型800个，字段声明24,868项（包括继承字段和M2M）。原字段12,606项逐一比较；支撑字段和新增业务模型字段标“新系统字段”，不伪装成旧字段。这里的声明不是当前5439数据库部署结构。\n'
for m in a['models']:
    full+='\n## '+m['model']+'\n\n数据库表：`'+m['table']+'`；类别：'+('旧原表模型' if m['source'] else '新增ERP业务/辅助模型' if m['erp'] else 'Django/系统/第三方支撑模型')+'。\n\n|字段|类型|NULL|主键/唯一|长度/精度|关联目标/删除|旧来源及核对|\n|---|---|---|---|---|---|---|\n'
    for f in m['fields']:
        origin=legacy_fields.get(legacy_model_tables[m['model']]+'.'+f['name']) if m['source'] else None
        source='新系统字段'
        if origin:
            o=origin['old'];source=origin['table']+'.'+origin['original']+'；'+o['data_type']+'；声明通过'
            if o['default_definition'] is not None:source+='；原默认'+o['default_definition']+'（服务规则）'
            if o['is_identity']:source+='；原IDENTITY（服务规则）'
        full+=row(f['name'],f['type'],f['null'],str(f['primary_key'])+'/'+str(f['unique']),f['max_length'] if f['max_length'] is not None else (str(f['max_digits'])+','+str(f['decimal_places']) if f['max_digits'] is not None else ''),(f['target'] or '')+('/'+str(f['delete']) if f['target'] else ''),source)
    full+='\n声明索引：'+cell('；'.join(m['indexes']) or '无显式Meta索引')+'\n\n声明约束：'+cell('；'.join(m['constraints']) or '无显式Meta约束')+'\n'
    if m['unique_together']:full+='\n联合唯一声明（unique_together）：'+cell(m['unique_together'])+'\n'
(D/fielddoc).write_text(full,encoding='utf8')
print(json.dumps(summary,ensure_ascii=False,default=str))

