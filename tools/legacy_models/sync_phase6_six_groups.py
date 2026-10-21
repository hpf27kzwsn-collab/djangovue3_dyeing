"""写入六组固定清单、实际验证范围和独立未完成轴。"""
import json,re,hashlib
from pathlib import Path
from collections import Counter
from datetime import datetime
ROOT=Path(__file__).resolve().parents[2];DOCS=ROOT/'docs'
TITLE='2026-10-17第六阶段六组固定清单与集中验证.md'
EVIDENCE='erp-phase6-six-groups-verification-20261017.json'
def read(path):return json.loads((ROOT/path).read_text(encoding='utf8'))
def save(path,value):(ROOT/path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def digest(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def section(path,marker,content):
    text=path.read_text(encoding='utf8');block='<!-- '+marker+' -->\n'+content.strip()+'\n<!-- /'+marker+' -->'
    pattern=r'<!-- '+re.escape(marker)+r' -->.*?<!-- /'+re.escape(marker)+r' -->'
    if re.search(pattern,text,re.S):text=re.sub(pattern,lambda _:block,text,flags=re.S)
    else:text+='\n\n'+block+'\n'
    path.write_text(text,encoding='utf8')
def escaped(value):return str(value).replace('|','\\|').replace('\r','').replace('\n','<br>')

def main():
    review=read('docs/erp-phase6-six-groups-review-20261017.json')
    for row,state in zip(review['groups']['6'],['扩大回归及最终针对性复验通过','重点浏览器验证通过；全部绑定尚未逐项浏览器验收','前端/模型/迁移及清单检查通过','独立登记，未完成历史对账和现场验收']):row['state']=state
    review['state_counts']['6']=dict(Counter(r['state'] for r in review['groups']['6']))
    log='.runtime-temp/phase6/six-groups-regression.log';text=(ROOT/log).read_text(encoding='utf8')
    match=re.search(r'Ran (\d+) tests in ([\d.]+)s',text);assert match and re.search(r'^OK$',text,re.M),text[-2000:]
    targeted='.runtime-temp/phase6/six-groups-targeted.log';tail=(ROOT/targeted).read_text(encoding='utf8')
    tm=re.search(r'Ran (\d+) tests in ([\d.]+)s',tail);assert tm and re.search(r'^OK$',tail,re.M),tail[-2000:]
    tests={'count':int(match[1]),'seconds':float(match[2]),'result':'passed','log':log,'sha256':digest(log),
        'final_targeted':{'count':int(tm[1]),'seconds':float(tm[2]),'log':targeted,'sha256':digest(targeted)},
        'note':'最终针对性复验与扩大回归重叠，不相加；234公式各有非空/NULL类型向量，不等于234个入口浏览器验收。'}
    values=read('.runtime-temp/phase6/six-groups-browser-values.json');schema=read('.runtime-temp/phase6/final-schema-check.json')
    files=['backend/plugins/erp_base/'+name for name in ['source_phase6_formula_runtime.py','source_phase6_formula_registry.json',
        'source_phase6_formula_links.py','source_phase6_auto_values.py','source_services.py','source_phase6_projection_formulas.py',
        'source_phase6_projection_context.py','source_phase6_api.py','source_phase6_entries.py','source_phase6_print_rules.py',
        'source_phase6_rendering.py','source_phase6_layouts.py','source_phase6_qr_print.py','tests/test_source_phase6_six_groups.py']]
    files+=['web/src/plugins/erp/OriginalEntryWorkbench.vue','requirements.lock.txt','backend/requirements.txt']
    evidence={'verified_at':datetime.now().astimezone().isoformat(),'baseline_sha256':review['baseline_sha256'],
        'fixed_counts':review['counts'],'state_counts':review['state_counts'],'formula_registry_counts':review['formula_registry_counts'],
        'tests':tests,'browser_saved_records':values,'schema':schema,
        'frontend':{'result':'vue-tsc_and_build_passed','log':'.runtime-temp/phase6/six-groups-frontend.log','sha256':digest('.runtime-temp/phase6/six-groups-frontend.log')},
        'browser_query':{'entry':'OrderColor','fixture':'SIXQ/UI-SIX-OC','source_duplicate_lines':2,'rolls':'6.00','weight':'-6.00','original_and_trial_columns':'均保留','whole_query_rows':6},
        'browser_prints':[{'report':'R153','rows':2,'pages':2,'html':'docs/assets/phase6-six-groups-qr-20261017.html','svg_count':2},
            {'report':'R013','rows':4,'pages':1,'html':'docs/assets/phase6-six-groups-outbound-20261017.html','note':'含此前合成出仓行及本轮两条重复明细、一条退回'}],
        'browser_screenshot':'浏览器截图工具多次返回 Unable to capture screenshot；保留实际浏览器取得的校样HTML及页面数值，不用生成图片冒充截图。',
        'paused_query_count':35,'historical_import_rows_this_run':0,'historical_reconciliation':'未完成全量旧业务结果对账','field_acceptance':'未完成',
        'files_sha256':{p:digest(p) for p in files},'legacy_schema_basis':'沿用已保存结构快照核对；本轮未重新提取旧 SQL Server'}
    transfer=ROOT/'.runtime-temp/phase6/six-groups-browser-transfer.json'
    if transfer.exists():evidence['browser_transfer']=json.loads(transfer.read_text(encoding='utf8'))
    save('docs/'+EVIDENCE,evidence)
    text=f'''# 第六阶段六组固定清单与集中验证

日期：2026-10-17。承接本次“六组一次性连续推进”要求。固定基线见[逐项原清单](erp-phase6-six-groups-baseline-20261017.json)，结果见[逐项状态及差异](erp-phase6-six-groups-review-20261017.json)，验证见[{EVIDENCE}]({EVIDENCE})。不改动基线编号，不删除异常、重复、停用或缺来源项。

## 当前结论与数量

本轮新增的明确公式执行、父子联动、查询试算及打印校样已实现并完成下表列明的验证。**第六阶段整体仍是部分完成**：逐入口非空对照、部分原事件行为、复杂原打印仍有未完成工作；不能把它们统称“只缺现场设备”。本文件后部逐编号保留全部项目，代码验证、历史对账、现场验收分别计。

|固定组|固定数量|本轮结果|尚未达到完整开发完成标准的部分|
|---|---:|---|---|
|1 本行/函数公式|116|111条编译接入保存，全部执行非空及NULL类型向量|5条原表达式/来源差异；类型向量不代替每种业务分支的真实单据对照|
|2 父子来源公式|156|123条编译接入保存，29条已有自动服务沿用|4条来源差异；已承接路径仍需逐入口非空结果对照|
|3 未绑定/非物理显示字段|95|78条具备查询试算及父子上下文执行路径；原列另存，试算另列|7条明确来源差异；10条赔款结算公式按财务暂缓；78条未全部逐入口非空核对|
|4 事件、转单、过滤|272|235条有实现或明确替代接线，扩大回归验证公共路径|9条明确缺口；28条财务配置暂缓；235条不能统称逐入口全验证通过|
|5 原打印配置|290|7份具备填数校样条件，新增R013与R153路径验证|254份有原运行差异，29份缺XML；完整原版式验收0；总数包含财务归档配置|
|6 验证与资料|4|相关回归{tests['count']}项通过；最后{tests['final_targeted']['count']}项针对性复验通过；前端、模型及迁移检查通过|历史业务结果全量对账与现场验收未完成|

各组存在交叉，不能把数量相加说成“剩余功能数”。原497条公式按本轮定位：此前130统一登记＋本轮234编译保存＋29已有自动服务＋9保存差异＋95显示/查询配置＝497。其中本次识别95条内有10条财务赔款/核销公式，保留原清单编号并暂缓；当前工作范围应称原清单497条、其中本期非财务487条，而不能继续把全部497都叫非财务。

35项查询继续暂缓，数量没有减少。本轮没有扩展财务系统，没有新模型字段、没有额外旧erpID字段、没有新迁移，也没有历史数据导入。

## 计算和保存如何落地

计算集中在service层。生成器按现存原字段、已证实外键和原表达式编译234条；保留原式、实际执行式、依赖字段和原GenerateTime值。用户明确提交目标值（含NULL）优先；修改依赖字段才重算；原键及编号只在创建时生成，不在普通修改中改号。双向单价按本次明确录入的含税价/单价或金额确定方向，不同时反复循环。

父字段向下传递，子行保存/撤回后向上汇总，处于同一事务。沿明确外键取来源；PStuffWeightDetail、DefectiveInRecord、ProdOutPriceProcess、ShiftArrangeDetail按已有原码对应，不新增关系字段。缺父行或多父候选保留原行原值并记录差异，不挑第一行。重复子行逐条参与；撤回行保留原始记录但退出新业务活动合计，历史来源行不自动回填。

普通表头无子行时，编辑表头保留原先明确录入数量；删除/撤回最后一条子行仍按空集合回算。采购直接转成品入库的数量来自所选采购行，不用不存在的细码覆盖。NULL、负数、重复都保留；公式除零明确报错并回滚，可明确录入原目标值（含NULL）保存异常单据，不把除零改成0。

## 浏览器实际操作与结果

|页面操作|已观察结果|
|---|---|
|正常称料明细修改单价-4、原用量8、计划量2000|用量6；Money/NeedMoney/RealMoney均-8；实称RealQty仍-7，原公式没有擅自改用实称量|
|工艺领料明细改单价-4、用量6，再改头Rate40、净重200|该行NeedQty0.24、Money-48；另一同物料序号原行NeedQty0.2、Money20；头Cost-28，两行均保留|
|正常称料主单Rate改9|所属染程BathRatio变9|
|自配称料明细单价-4、用量6|Money=-24、RealMoney=168；NeedQty和NeedMoney保持NULL|
|厨房入库改含税价226|单价200、数量-2、未税金额-400、合计-452、税金-52|
|其他入库改单价-50|含税价-56.5、数量-2、未税金额100、合计113、税金13|
|三种包装入口毛重均改20|QC_Record净重7；QFQC_Record指定纱类按固定锭重得到8；QueryRecord净重18|
|原码印花称料父Qty改-10，再改子Rate4|子Dosage先-30后-40，没有增加模型字段|
|无细码次品表头4粒、重量-10|数量保留4，实重-18，净重-22；修正了初次页面验证发现的空汇总覆盖问题|
|订单颜色查询打开“附加原公式试算列”|同编号两条预配行汇总粒数6、重量-6；原列和试算列均保留，NULL不变成0|
|采购转成品入库→修改备注→撤回整单|2粒、重量-4在转单及编辑后保留；撤回后原单仍在、原数量不变，活动台账由1条归0，撤回事实保存该台账快照；采购来源未改|
|R153机台二维码校样|两条重复机台原行输出2页，保留原100×100mm纸张、UTF-8字节编码、Version2；HTML中2个实际SVG|
|R013成品出仓明细校样|浏览器取得4行1页，含重复出仓与负数退回；独立测试3行场景核对粒数5、胚重-8及“退车间”计算文字|

浏览器修改后的14个主单/子行结果另由数据库独立读取验证。数据均为隔离开发库的合成单据，不是旧业务全量对账。两份实际浏览器校样可直接打开：[机台二维码](assets/phase6-six-groups-qr-20261017.html)、[成品出仓明细](assets/phase6-six-groups-outbound-20261017.html)。截图工具未能截取页面，未把文本核验冒充纸张/字体视觉验收。

## 原打印的实现与限制

补齐Running=None不启用汇总、RecordNumber按行位置保留重复行序号、不启用的单列MultiColumn配置、嵌套表格自身边框。R153仅对应已核对脚本摘要的UTF-8字节处理，不执行任意C#脚本。QRCode固定版本容量不足会报告原数据与版本冲突，不截短内容；当前纸张与SVG校样仍需与旧12.2客户端、实际标签机核对静区、字号和溢出方式。

采用的默认规则参考[DevExpress单列默认值](https://docs.devexpress.com/XtraReports/DevExpress.XtraReports.UI.MultiColumn.ColumnCount)、[二维码纠错默认L](https://docs.devexpress.com/CoreLibraries/DevExpress.XtraPrinting.BarCode.QRCodeGenerator.ErrorCorrectionLevel)及[qrcode 8.2官方包](https://pypi.org/project/qrcode/8.2/)。现代文档不能证明旧12.2的全部边界行为，相关差异列入E234。校样不执行打印前业务副作用、不增加打印次数，也不冒充打印机成功回执。

7份具备校样条件为H002、H003、H011、R013、R016、R102、R153。其余每份的脚本/控件/动态高度/子报表/缺列等具体差异见后部清单。254份中的代码未实现与资料缺失不能混为一类；取得XML不等于运行行为已经复刻。

## 验证标准和后续准确顺序

1. 保存公式优先处理9条明确差异；其中自引用占位与两个日期格式项按原值/格式保留，不虚构算式。其余缺物理来源或畸形表达式继续保留手填目标，并逐项核实旧业务含义。
2. 查询显示优先处理7条来源问题，再对78条已具备执行路径的查询逐入口非空核对（不重新开发已接入的通用执行器）。4条B093/B097是选择器代码，不能当数字或字段强算；3条BathRatio缺可靠父来源。
3. 对第4组235条已有接线逐原绑定核实必要分支及浏览器调用；9条明确缺口为3外部调用/回执、2缺原表定义、2旧目标字段不存在、2残缺过滤。原按钮隐式时点、原无序游标及多候选仍有已公开差异，不以“存在service”判定完成。28财务配置暂缓。
4. 原打印按逐模板差异实现后，必须跑真实取数、分页、重复/NULL/负数及浏览器校样，随后和旧客户端成品对照。当前7份可校样不能算7份完整复刻。29份无XML需要原客户端模板运行资料；其余254份保留可继续开发的代码事项，不能全部推给现场。
5. 历史对账按原表原键、提取批次与逐原行定位执行，重复原键逐条核对；这与上述代码完成分开。现场用真实单据及设备确认另列，不用本轮合成库记录数抵扣。

本次完成范围以代码和验证证据为准，不宣称剩余工作清零。此前轮次的“后续”数量均由本文件固定基线及结果接替，旧结果保留作历史记录。

## 逐编号结果

以下每行均对应固定基线原行；历史数据对账与现场验收均未完成。完整原因、原公式、目标模型和原配置见JSON，不省略重复配置。
'''
    names={'1':'本行/函数公式','2':'父子来源公式','3':'显示/查询公式','4':'事件、转单和过滤','5':'原打印配置'}
    for group,name in names.items():
        text+='\n### '+group+' '+name+'\n\n|固定编号|原入口/报表|字段/事件|当前状态与差异|\n|---|---|---|---|\n'
        for r in review['groups'][group]:
            reasons=r.get('issues',[])+[v['reason'] for v in r.get('results',[]) if v['state']=='explicit_difference']
            text+='|'+ '|'.join(escaped(v) for v in [r['id'],r.get('entry',r.get('report','')),r.get('field',r.get('event',r.get('title',''))),r['state']+('；'+'；'.join(reasons) if reasons else '')])+'|\n'
    (DOCS/TITLE).write_text(text,encoding='utf8')
    reasons={
        'E231':('九条保存公式差异与实际触发时点','9条原公式的自引用、日期格式、畸形IIF及缺物理来源逐项保留；234条已编译公式按明确输入/依赖变化执行，原GenerateTime值保留但旧客户端全部时序未证实。类型向量和重点浏览器通过不等于全部入口业务验收。'),
        'E232':('原码父子关系与重复候选','4类原码关系沿现存字段连接，无新增关系/旧erpID字段。多个父候选保留全部并记录差异，单父来源明确才回填；子汇总保留每个重复活动行。历史来源不回算，旧客户端歧义候选选择尚未证实。'),
        'E233':('查询虚拟字段、选择器误填表达式与财务重分类','95条配置中78条具备试算路径但逐入口非空对照未全完成；7条缺来源（3个BathRatio父来源、4个B093/B097选择器代码）；10条赔款核销归财务暂缓。试算追加列，原投影与原行不改；依赖计算失败不能用旧列值冒充本次结果，逐行报差异。'),
        'E234':('原二维码、单列与序号校样仍有旧运行差异','新增R153 UTF-8字节二维码及R013出仓打印路径，7份具备校样条件、254份有运行差异、29份无XML，完整原版式0。二维码固定版本溢出、静区、旧12.2字体分页仍待原成品对照；截图工具失败已记录，保留实际浏览器校样HTML。其余代码缺口不能统一列缺外部资料。'),
        'E235':('采购来源和无子行表头不被空汇总清掉','扩大回归修复采购直接转成品入库来源数量被空细码汇总覆盖；浏览器又发现无子行次品表头人工粒数被清0，已修正。编辑表头保留人工数量；子行变动/撤回仍按实际活动子集汇总，重复和负数不丢弃。')}
    section(DOCS/'旧ERP复刻异常与合理实现说明.md','phase6-six-groups-exceptions','\n\n'.join('## '+key+' '+name+'\n\n'+reason for key,(name,reason) in reasons.items())+f'\n\n逐项及验证见[{TITLE}]({TITLE})。')
    current=f'''## 当前执行范围：第六阶段六组固定清单（2026-10-17）

最新依据：[{TITLE}]({TITLE})、[固定基线](erp-phase6-six-groups-baseline-20261017.json)、[逐编号结果](erp-phase6-six-groups-review-20261017.json)、[验证证据]({EVIDENCE})。下方各轮“最新/后续”表述均为历史记录，以本节为当前口径。

固定六组为116、156、95、272、290、4个核验单元，组间有交叉不能相加。前两组272条中234条新增编译保存、29条已有自动服务、9条明确差异。显示/查询95条中78条具备执行路径但未逐入口全量非空核对、7条来源差异、10条财务赔款核销暂缓。原497条配置保留，本期非财务487条，不删原编号。

事件/转单/过滤272条中235条已有接线或替代，9条明确缺口，28条财务暂缓；已有接线不等于全部原行为及浏览器验证完成。原打印7份可校样、254运行差异、29缺XML、0完整原版式验收。35项查询继续暂缓。

扩大回归{tests['count']}项通过，最后{tests['final_targeted']['count']}项针对性复验通过（重叠不累计）；前端、模型及迁移检查通过，766 ERP模型/655原表模型/12606原字段不变。页面修改后的14个主子记录独立核验通过，查询重复预配、两种原打印及采购转单另列证据。无额外旧erpID、无新迁移、历史导入0。

**本轮列明增量开发及必要验证完成；第六阶段整体仍部分完成；历史业务结果全量对账、现场验收均未完成。** 后续按9保存差异→7查询来源及78逐入口非空核对→235接线逐绑定验证及9缺口→逐模板运行差异→历史对账/现场验收推进。已实现执行器及既有通过用例不重新算未实现，异常E231～E235独立保留。'''
    for name in ['2026-10-16染色ERP剩余工作全量盘点清单.md','染色ERP后续开发方案.md']:section(DOCS/name,'phase6-form-flows-current',current)
    section(DOCS/'2026-10-17第六阶段配方父子来源与专用服务联调.md','phase6-six-groups-superseded',f'## 后续清单已固定\n\n本文的116/156/95后续事项已统一纳入[{TITLE}]({TITLE})，本文件保留前轮验证事实，不再作为当前剩余数量。')
    inventory=read('docs/erp-remaining-inventory-20261016.json');axis=inventory['axes']['新旧系统差异及处理情况']
    for key,(name,reason) in reasons.items():
        row={'id':key,'name':name,'status':'已完成' if key=='E235' else '部分完成','reason':reason,'related_sql':[],'source':'docs/旧ERP复刻异常与合理实现说明.md'}
        index=next((i for i,r in enumerate(axis) if r['id']==key),None)
        if index is None:axis.append(row)
        else:axis[index]=row
    inventory['counts']['新旧系统差异及处理情况']=dict(Counter(r['status'] for r in axis))
    summary={'document':TITLE,'evidence':EVIDENCE,'fixed_counts':review['counts'],'state_counts':review['state_counts'],
        'development':'列明增量及必要验证通过；第六阶段部分完成','historical_reconciliation':'未完成','field_acceptance':'未完成','tests':tests}
    inventory['phase6_six_groups_20261017']=summary;inventory['phase6_review']['current_evidence']='docs/'+EVIDENCE
    inventory['phase6_review']['next']='以六组固定编号结果为准；9保存差异、7显示来源及78逐入口非空核对、235接线逐绑定及9缺口、原打印254运行差异/29缺XML；35查询与财务暂缓，历史和现场独立。'
    for row in inventory['axes']['旧界面配置入口']:
        formulas=[f for g in ['1','2','3'] for f in review['groups'][g] if f['entry']==row['name']]
        if formulas:row['phase6_six_groups_20261017']={'document':TITLE,'fields':[{'id':r['id'],'field':r['field'],'state':r['state']} for r in formulas],
            'development':'按逐字段证据，不升级整入口完成','historical_reconciliation':'未完成','field_acceptance':'未完成'}
    save('docs/erp-remaining-inventory-20261016.json',inventory)
    old=read('docs/erp-phase6-review-20261016.json');old['six_groups_20261017']=summary;old['current_review_at']=evidence['verified_at'];save('docs/erp-phase6-review-20261016.json',old)
    for row,state in zip(review['groups']['6'],['扩大回归及最终针对性复验通过','重点浏览器验证通过；全部绑定尚未逐项浏览器验收','前端/模型/迁移及清单检查通过','独立登记，未完成历史对账和现场验收']):row['state']=state
    review['state_counts']['6']=dict(Counter(r['state'] for r in review['groups']['6']));save('docs/erp-phase6-six-groups-review-20261017.json',review)
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
