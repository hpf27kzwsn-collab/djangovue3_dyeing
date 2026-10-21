"""将续验事实同步到固定清单；不改固定编号，不提升历史/现场状态。"""
import json,re,hashlib
from pathlib import Path
from collections import Counter
from datetime import datetime
ROOT=Path(__file__).resolve().parents[2];DOCS=ROOT/'docs'
TITLE='2026-10-17第六阶段六组续验与剩余清单.md'
EVIDENCE='erp-phase6-six-groups-continued-verification-20261017.json'


def read(path):return json.loads((ROOT/path).read_text(encoding='utf8'))
def save(path,data):(ROOT/path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def digest(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def cell(value):return str(value).replace('|','\\|').replace('\r','').replace('\n','<br>')
def section(path,key,text):
    begin='<!-- '+key+' -->';end='<!-- /'+key+' -->';body=path.read_text(encoding='utf8');block=begin+'\n'+text+'\n'+end
    body=re.sub(re.escape(begin)+r'.*?'+re.escape(end),lambda _:block,body,flags=re.S) if begin in body else body+'\n'+block+'\n'
    path.write_text(body,encoding='utf8')
def test_result(name):
    text=(ROOT/'.runtime-temp/phase6'/name).read_text(encoding='utf8')
    match=re.search(r'Ran (\d+) tests in ([\d.]+)s\s+OK',text)
    if not match:raise ValueError('验证未通过：'+name)
    return {'count':int(match[1]),'seconds':match[2],'log':'.runtime-temp/phase6/'+name,'sha256':digest('.runtime-temp/phase6/'+name)}


def main():
    baseline=read('docs/erp-phase6-six-groups-baseline-20261017.json');review=read('docs/erp-phase6-six-groups-review-20261017.json')
    for group,rows in baseline['groups'].items():
        if [r['id'] for r in rows]!=[r['id'] for r in review['groups'][group]]:raise ValueError('固定编号改变：'+group)
    audit=read('docs/erp-phase6-projection-entry-verification-20261017.json')
    browser=read('docs/assets/phase6-continued-browser-entries-20261017.json')
    names={r['entry'] for r in audit['entries'] if r['state']!='财务暂缓'}
    if names!={r['entry'] for r in browser} or len(browser)!=len(names):raise ValueError('逐入口浏览器证据不完整/重复')
    if not all(r['countMatches'] and r['hasFormulaColumns'] for r in browser):raise ValueError('浏览器行数或试算列不符')
    schema=read('.runtime-temp/phase6/continued-schema.json')
    if schema['extra_legacy_id_fields']:raise ValueError('存在额外旧erpID字段')
    tests={'regression':test_result('continued-regression.log'),'final_targeted':test_result('continued-targeted.log'),'note':'两套用例重叠，不能相加为独立用例数'}
    prints=[{'report':code,'rows':count,'pages':1,'html':f'docs/assets/phase6-continued-{code}-20261017.html'} for code,count in [('H007',2),('H019',2),('R014',3),('R040',3),('R036',3)]]
    for row in prints:
        text=(ROOT/row['html']).read_text(encoding='utf8')
        if text.count('<section class="page">')!=row['pages']:raise ValueError('浏览器校样页数不符')
        row['sha256']=digest(row['html'])
    statuses=['相关回归和最终针对性验证通过','固定第三组35个非财务入口已逐一浏览器查询；5份新增原打印非空校样通过','前端、模型及迁移检查通过；固定编号未变','历史结果全量对账和现场验收独立保留，未完成']
    for row,state in zip(review['groups']['6'],statuses):row['state']=state
    for row in review['groups']['3']:
        if row['entry'] in names:row['browser_verification']='查询行数与后台一致，试算列与逐行差异显示已核验；不代表整入口保存/审核链全部验收'
    for row in review['groups']['5']:
        if row['report'] in {r['report'] for r in prints}:row['browser_verification']=next(r for r in prints if r['report']==row['report'])
    review['state_counts']={g:dict(Counter(r.get('state','待验证') for r in rows)) for g,rows in review['groups'].items()}
    review['updated_at']=datetime.now().astimezone().isoformat();save('docs/erp-phase6-six-groups-review-20261017.json',review)
    print_scopes=dict(Counter(r['scope'] for r in review['groups']['5']))
    checks=[c for row in audit['entries'] for c in row.get('expected_value_checks',[])]
    if not all(c['passed'] for c in checks):raise ValueError('独立预期值核对失败')
    files=['backend/plugins/erp_base/'+n for n in ['source_phase6_formula_runtime.py','source_phase6_projection_context.py','source_phase6_projection_formulas.py','source_phase6_projection_overrides.py','source_phase6_print_sources.py','source_phase6_print_groups.py','source_phase6_rendering.py','source_phase6_entries.py','source_phase6_api.py','tests/test_source_phase6_six_groups_continued.py']]
    files+=['web/src/plugins/erp/OriginalEntryWorkbench.vue','tools/legacy_models/verify_phase6_projection_entries.py','tools/legacy_models/review_phase6_six_groups.py']
    evidence={'verified_at':review['updated_at'],'baseline_sha256':digest('docs/erp-phase6-six-groups-baseline-20261017.json'),'fixed_ids_preserved':True,
        'fixed_counts':review['counts'],'state_counts':review['state_counts'],'print_scopes':print_scopes,'tests':tests,'schema':schema,
        'query_entry_states':dict(Counter(r['state'] for r in audit['entries'])),'expected_value_checks':len(checks),'expected_value_checks_passed':len(checks),
        'browser_entry_count':len(browser),'browser_entry_evidence':'docs/assets/phase6-continued-browser-entries-20261017.json','browser_prints':prints,
        'frontend':{'result':'类型检查与构建通过','log':'.runtime-temp/phase6/continued-frontend.log','sha256':digest('.runtime-temp/phase6/continued-frontend.log')},
        'paused_query_count':35,'paused_queries_changed':False,'historical_import_rows_this_run':0,'historical_reconciliation':'未完成全量旧业务结果对账','field_acceptance':'未现场验收',
        'browser_screenshot':'本轮截图接口仍返回 Unable to capture screenshot；保存实际浏览器校样HTML和页面文本，不以生成图片冒充截图。',
        'code_sha256':{p:digest(p) for p in files}}
    save('docs/'+EVIDENCE,evidence)
    text=f'''# 第六阶段六组续验与剩余清单

更新日期：2026-10-17。本文承接上一轮固定六组清单，933 个固定编号全部保留；六组有交叉，不能将数量相加当作独立业务功能数。

**本轮代码、逐入口查询和新增打印校样已完成下列验证，第六阶段整体仍为部分完成。** 历史数据全量对账和现场验收没有完成，不能与开发验证混算。财务继续暂缓；没有新增旧erpID字段；本轮历史数据导入为0。

## 当前数量

|固定组|数量|已实现及本次验证|仍需继续的内容|
|---|---:|---|---|
|1 本行/函数公式|116|111条编译保存路径；缺上游来源时不再使用旧结果串算下游金额|5条原表达式/来源差异；逐保存分支、原时序不能由查询试算替代|
|2 父子来源公式|156|123条编译保存路径，29条已有自动服务|4条保存来源差异；已有路径不表示所有主从保存/撤销场景均已浏览器验收|
|3 查询/非物理字段|95|85条非财务固定公式覆盖35个入口，全部完成非空运行及逐入口浏览器查询；84条在当前样例所有行成功，1条保留5行父单缺失差异|10条财务赔款公式暂缓；缺父行记录原样保留。全部业务分支、历史同值对账仍未完成|
|4 事件、转单、过滤|272|235条有实现或明确替代接线，相关回归继续通过|9条明确缺口、28条财务配置；235条仍需逐绑定核验原按钮/事件时机，不能用本轮35个查询页面代替|
|5 原打印|290|13份通过当前静态校样条件检查（上一轮7份）；本轮5份完成非空浏览器校样|248份仍有原运行/来源差异、29份无XML；13份也不等于13份完整原打印，完整原版式验收仍为0；总量含财务归档配置|
|6 验证和资料|4|相关回归{tests['regression']['count']}项通过，最后{tests['final_targeted']['count']}项针对性复验通过；前端、模型、迁移检查通过|历史对账、现场验收独立待完成；两套测试重叠，不相加|

**本轮核验的35个入口，不是继续暂缓的35项查询。** 暂缓查询没有重新开发或改为已完成；本轮入口来自固定第三组的非财务公式范围。

## 已补齐的明确实现

1. 加料、正常、返工称料打印的浴比，按原SheetSeries读取对应称料单头Rate。旧父关系缺失或误指向明细的原文仍保存，页面展示替代依据。返工单头入口保留原RecipeType条件，因此其他类型明细出现在旧打印查询时仍如实列出缺父来源，不能删行或借用其他父单。
2. 染化料大小仓盘点4处B093/B097原Express被明确作为选择器误配置处理：试算保留当前物料/仓库代码，原代码、未知代码、NULL、空字符串及重复行均保留，不将B093/B097作为数据写回。
3. 报价关联称料和配方查询保留所有原同名列；金额公式明确采用原JOIN中的d.Price明细价格，另附来源列及依据。单头价格999、明细价格3的必要用例证明不会取错列。原Qty、Dosage和NULL语义没有替换。
4. 提料H007、紧筒H019的跨表打印字段沿原目录的父单关系取数，多个候选或缺父单会说明具体行和匹配数，所有明细仍在原表中，不选择第一条。
5. 打印按原Level组织多层分组、同层组尾、零高度明细汇总、重复组头/组尾与分页；保留重复行和负数。补齐NO:{{0}}等复合格式。R014补取已连接客户表pc.NameC；R036按出库单头GrayKindID原代码分组，旧GrayKind显示名仍未证明，页面和异常文档明确说明替代。
6. 保存联动中，上游公式缺父来源时，下游不能沿用旧数量生成新的金额。原行及原值保留并记录缺来源；明确输入数量后仍正常计算，不增加额外字段。

## 可复核的验证证据

- [逐固定编号状态](erp-phase6-six-groups-review-20261017.json)、[固定基线](erp-phase6-six-groups-baseline-20261017.json)、[本轮验证汇总]({EVIDENCE})。
- [35个入口的非空运行](erp-phase6-projection-entry-verification-20261017.json)：34个入口固定公式无逐行差异，1个返工打印入口列出5行缺父单；{len(checks)}个独立预期值检查全部通过，涉及颜色RGB、打样5套剂量、重复细码、负数库存汇总、故障分类、配方金额等。
- [35个入口的实际浏览器结果](assets/phase6-continued-browser-entries-20261017.json)：全部行数与后台一致并显示试算列。整入口其他公式另外可见4类缺父来源：PrintOrderColor、qry_QuoteRelaRecipe、QueryRecordCheck、ReworkStuffWeightPhaseDetailPrint。它们不被固定字段通过状态掩盖。
- 5份浏览器原校样：H007/H019各2行1页；R014/R040/R036各3行1页。R014/R040中两条重复的2件均参与汇总为4件，另有-3件，客户小计1件。没有真实向打印机发送，也没有增加业务打印成功次数。
- 当前模型766个，原表模型655个、原字段12606个，额外旧erpID字段0；系统检查通过，无新迁移。
- 浏览器截图接口失败，保留实际浏览器取得的HTML和页面文本；纸张、字体、分页与旧打印成品对照仍需现场验收。

|原报表|浏览器校样|验证范围|
|---|---|---|
'''
    for r in prints:text+=f"|{r['report']}|[{r['rows']}行/{r['pages']}页]({r['html'].removeprefix('docs/')})|非空渲染及本轮来源/汇总；历史和现场均未验收|\n"
    text+='''
K035机物料入库汇总表随公共多层分组能力通过静态条件检查，本轮没有做该入口非空浏览器校样，不能按验证通过登记。

打印范围另按原DataMember分类：158份对应非财务入口（13份具备静态校样条件、145份仍有差异），35份对应财务入口继续暂缓，68份无明确入口/缺原入口定义，29份无XML。68份和29份不能据此从业务范围删除；248是全目录运行差异数，不能当成248份非财务待开发报表。

## 后续顺序与未完成边界

1. 先继续固定第一、二组9条保存差异：AddStuffWeight.ClothQtyKg/Moisture1、MoveShiftBill.BeginTime/DayEnd、Quote.IsConfirmed、qry_QuoteRelaRecipe.Remarks、QueryRecordCheck.GradeID、WareHouseProdCount.Rolls/WeightQty。自引用/日期格式已有明确录入处理，缺物理字段、畸形表达式及原更新表不一致的项目继续按原编号记录，不伪称算式等价。
2. 按第四组H/C/L原编号逐绑定补齐保存、审核、转单、撤销与时机验证。9条明确缺口为3条外部调用及回执、2条缺原表、2条最新表已无目标字段、2条不完整过滤。其余235条中的原行为差异也继续保留；回归通过不等于每一条旧按钮已复刻。
3. 继续145份明确非财务原打印差异，并核对68份无明确入口配置、29份无XML的原文件来源；35份财务打印暂缓。脚本、动态高度、多列、条码/子报表、缺失展示列和关系等仍是开发或来源核对工作，不能一律归类为现场设备。R122仍缺JobKind“客退回修卡”等显示名的明确来源，不能直接拿JobKindID代码比较中文名称。
4. 再做旧库同抽取时点逐单/逐行对账，包括异常、重复、已撤回记录，核对计划、实称和实际收发分别对应的原值；本轮合成测试不替代这一步。
5. 最后现场验收实际打印纸张/字体、设备回执和岗位办理顺序。继续暂缓35项查询和财务，不因为暂缓而删除模型、原配置或原数据。

多层分组与重复组尾的实现依据为原XML属性以及[DevExpress GroupBand.Level说明](https://docs.devexpress.com/XtraReports/DevExpress.XtraReports.UI.GroupBand.Level)、[RepeatEveryPage说明](https://docs.devexpress.com/XtraReports/DevExpress.XtraReports.UI.GroupBand.RepeatEveryPage)。当前官方说明用于确认属性含义；不能据此宣称与旧12.2版本逐像素一致。

## 固定编号逐项结果

下表保留全部933个编号。每条历史对账均未完成、现场均未验收；表内“通过”仅限相应代码/合成数据验证范围。
'''
    titles={'1':'本行公式','2':'父子公式','3':'查询试算','4':'事件、转单、过滤','5':'原打印','6':'验证与资料'}
    for group,rows in review['groups'].items():
        text+='\n### '+group+' '+titles[group]+'\n\n|编号|入口/报表|字段/事件|当前状态及来源差异|\n|---|---|---|---|\n'
        for r in rows:
            reasons=r.get('issues',[])+[v['reason'] for v in r.get('results',[]) if v['state']=='explicit_difference']
            if r.get('source_resolution'):reasons.append(r['source_resolution'])
            if r.get('runtime_issues'):reasons.append(str(len(r['runtime_issues']))+'行来源差异，见入口核验JSON')
            if group=='5':reasons.insert(0,r['scope'])
            text+='|'+'|'.join(cell(v) for v in [r['id'],r.get('entry',r.get('report',r.get('name',''))),r.get('field',r.get('event',r.get('title',''))),r['state']+('；'+'；'.join(reasons) if reasons else '')])+'|\n'
    (DOCS/TITLE).write_text(text,encoding='utf8')
    current=f'''## 当前有效的第六阶段清单（六组续验）

以[{TITLE}]({TITLE})及[{EVIDENCE}]({EVIDENCE})为准，早前剩余数量保留为历史记录。固定编号未改；第六阶段仍部分完成。

第三组85条非财务公式、35个入口已经逐一非空运行和浏览器查询，84条固定公式所有样例行通过，1条保留5行缺父单；10条财务公式暂缓。此35个入口与继续暂缓的35项查询不是同一批。

原打印13份具备静态校样条件，本轮新增5份非空浏览器校样；248份原运行差异、29份无XML仍在清单。相关回归{tests['regression']['count']}项、最终针对性{tests['final_targeted']['count']}项通过（重叠不相加）。保存9差异、事件9缺口与235条接线的逐绑定原行为验证仍要推进。财务继续暂缓；旧erpID额外字段0；历史数据导入0，历史对账和现场验收未完成。'''
    for name in ['2026-10-16染色ERP剩余工作全量盘点清单.md','染色ERP后续开发方案.md']:section(DOCS/name,'phase6-form-flows-current',current)
    old=DOCS/'2026-10-17第六阶段六组固定清单与集中验证.md'
    body=old.read_text(encoding='utf8');notice=f'> 本文为上一轮集中验证记录；当前状态和剩余数量以[{TITLE}]({TITLE})为准。固定基线不变。\n\n'
    if not body.startswith('> 本文为上一轮集中验证记录；'):old.write_text(notice+body,encoding='utf8')
    reasons={
      'E236':('查询父来源、选择器误配置和同名价格列的明确替代','7处原显示来源差异已按明确规则承接，另明确报价关联称料/配方的d.Price来源。原配置/同名列/重复记录不删；35个非财务入口非空浏览器已核验，返工入口5行缺父单及其他入口的父单异常逐行显示。历史原行为仍待同值对账。'),
      'E237':('多层原打印、跨父单取数和分页校样边界','支持原Level、零高明细、同层组尾、每页重复组尾、复合格式及原父单取数；新增5份非空浏览器校样。当前13份具备静态条件，248份原运行差异、29份无XML；K035本轮未非空浏览器验证，不能计完整复刻。截图工具失败，校样HTML已保存。'),
      'E238':('原打印缺失展示列的补取与未证明类别','R014原客户全称来自已连接的pc.NameC。R036原GrayKind缺失，当前明确按GrayOut.GrayKindID原代码分组；不声称还原原显示名。R122的JobKind中文标签来源仍未证明，不能把JobKindID直接当成“客退回修卡”比较。'),
      'E239':('缺上游公式来源时不以旧结果生成新金额','已修正保存联动：上游NeedQty等公式缺父来源时，依赖金额保留原值并记录原因；明确输入数量后仍按原公式计算。异常单据仍可录入，不增加字段。必要回归通过，历史和现场结论独立。')}
    exception_text='## 六组续验新增说明\n\n本节为本轮当前结论，更新E233、E234中的上一轮数量，不删除旧事实。\n\n'
    for key,(name,reason) in reasons.items():exception_text+='## '+key+' '+name+'\n\n'+reason+'\n\n'
    exception_text+='完整剩余范围见['+TITLE+']('+TITLE+')。'
    section(DOCS/'旧ERP复刻异常与合理实现说明.md','phase6-six-groups-continued-exceptions',exception_text)
    inventory=read('docs/erp-remaining-inventory-20261016.json');axis=inventory['axes']['新旧系统差异及处理情况']
    for key,(name,reason) in reasons.items():
        value={'id':key,'name':name,'status':'已完成' if key=='E239' else '部分完成','reason':reason,'related_sql':[],'source':'docs/旧ERP复刻异常与合理实现说明.md'}
        index=next((i for i,r in enumerate(axis) if r['id']==key),None)
        if index is None:axis.append(value)
        else:axis[index]=value
    for r in axis:
        if r['id'] in ['E233','E234']:r['current_followup']='当前续验数量及处理见E236～E239和'+TITLE
    inventory['counts']['新旧系统差异及处理情况']=dict(Counter(r['status'] for r in axis))
    summary={'document':TITLE,'evidence':EVIDENCE,'fixed_counts':review['counts'],'state_counts':review['state_counts'],'development':'本轮增量验证通过，第六阶段整体部分完成','historical_reconciliation':'未完成','field_acceptance':'未完成','tests':tests}
    inventory['phase6_six_groups_20261017']=summary;inventory['phase6_review']['current_evidence']='docs/'+EVIDENCE
    inventory['phase6_review']['next']='按六组续验固定清单：9条保存差异、235事件接线逐绑定与9缺口、145份非财务打印差异及68份缺明确入口/29缺XML；35份财务打印暂缓。第三组35入口非空浏览器已核验，历史和现场独立；原35查询和财务继续暂缓。'
    for row in inventory['axes']['旧界面配置入口']:
        formulas=[r for g in ['1','2','3'] for r in review['groups'][g] if r['entry']==row['name']]
        if formulas:row['phase6_six_groups_20261017']={'document':TITLE,'fields':[{'id':r['id'],'field':r['field'],'state':r['state']} for r in formulas],'development':'逐字段验证；整入口不升级完成','historical_reconciliation':'未完成','field_acceptance':'未完成'}
    save('docs/erp-remaining-inventory-20261016.json',inventory)
    old_review=read('docs/erp-phase6-review-20261016.json');old_review['six_groups_20261017']=summary;old_review['current_review_at']=evidence['verified_at'];save('docs/erp-phase6-review-20261016.json',old_review)
    print(json.dumps({'fixed_counts':review['counts'],'state_counts':review['state_counts'],'expected_checks':len(checks),'browser_entries':len(browser),'tests':tests,'exceptions':len(axis)},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
