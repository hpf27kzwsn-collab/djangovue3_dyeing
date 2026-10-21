"""父子保存与父单打印的增量核验；保留固定编号、旧证据和三个验收维度。"""
from sync_phase6_six_groups_continued import read,save,digest,section,test_result,cell,ROOT,DOCS
from collections import Counter
from datetime import datetime
import json

TITLE='2026-10-17第六阶段六组续验与剩余清单.md'
EVIDENCE='erp-phase6-parent-save-print-verification-20261017.json'


def main():
    baseline=read('docs/erp-phase6-six-groups-baseline-20261017.json')
    review=read('docs/erp-phase6-six-groups-review-20261017.json')
    previous=read('.runtime-temp/phase6/parent-prior-review.json')
    assert review['paused_queries']==baseline['paused_queries']
    for group,rows in baseline['groups'].items():
        assert [r['id'] for r in rows]==[r['id'] for r in review['groups'][group]]
        old={r['id']:r for r in previous['groups'][group]}
        for row in review['groups'][group]:
            for key in ['browser_verification','verification']:
                if key in old[row['id']]:row[key]=old[row['id']][key]
    tests={'regression':test_result('parent-regression-complete.log'),'targeted':test_result('parent-final.log'),
           'note':'44项针对性用例包含在425项相关回归内，不相加'}
    assert tests['regression']['count']==425 and tests['targeted']['count']==44
    live=json.loads((ROOT/'.runtime-temp/phase6/remaining-save-live.json').read_text(encoding='utf-8-sig'))
    save('docs/erp-phase6-remaining-save-live-20261017.json',live)
    save_evidence=read('docs/assets/phase6-parent-browser-save-20261017.json')
    assert [x['value'] for x in save_evidence['tests'][0]['values']]==['2.00','','3.00','6.00','3.00','2.00','1.00']
    assert [x['value'] for x in save_evidence['tests'][1]['values']]==['3.00','9.00','3.00','9.00','3.00','-7.00','1.00']
    prints=[]
    for code,count,total,scope in [('H004',3,6,'父单P-S'),('K008',3,3,'父单P-L'),('R66-2',3,3,'SheetSeries参数P-L'),('R015',6,9,'客户P-C')]:
        path=f'docs/assets/phase6-parent-{code}-20261017.html';html=(ROOT/path).read_text(encoding='utf8')
        assert html.count('<section class="page">')==1
        prints.append({'report':code,'rows':count,'query_rows_before_print_selection':total,'scope':scope,'pages':1,'html':path,'sha256':digest(path)})
    for row in review['groups']['5']:
        proof=next((p for p in prints if p['report']==row['report']),None)
        if proof:row['browser_verification']=proof
    gaps=[]
    for row in review['groups']['1']+review['groups']['2']:
        if any(r['state']=='explicit_difference' for r in row['results']):
            row['verification']='2026-10-17最新旧库SELECT元数据核验：差异仍存在；NULL、负数/异常等级、重复行保存及entry_formula_source_pending留痕测试通过；未执行猜测公式。'
            gaps.append({'id':row['id'],'entry':row['entry'],'field':row['field'],'results':row['results']})
    assert len(gaps)==5
    states=['425项相关回归通过，44项针对性复验通过（重叠）',
            '新增2组染程整单保存及4份非空浏览器校样；此前逐入口证据保留',
            '766模型/655原表/12606原字段检查通过；额外旧erpID为0；前端类型检查及构建通过',
            '全量历史对账未完成，现场验收未完成；本轮没有历史导入']
    for row,state in zip(review['groups']['6'],states):row['state']=state
    review['updated_at']=datetime.now().astimezone().isoformat()
    review['state_counts']={g:dict(Counter(r['state'] for r in rows)) for g,rows in review['groups'].items()}
    save('docs/erp-phase6-six-groups-review-20261017.json',review)
    eligible=[r for r in review['groups']['5'] if not r['issues']]
    nonfinance=[r for r in review['groups']['5'] if r['scope']=='非财务入口' and r['issues']]
    assert len(eligible)==20 and len(nonfinance)==138
    schema=read('.runtime-temp/phase6/continued-schema.json');assert not schema['extra_legacy_id_fields']
    files=['backend/plugins/erp_base/'+name for name in ['source_phase6_save_timing.py','source_phase6_service_values.py',
        'source_phase6_formula_runtime.py','source_phase6_rendering.py','source_phase6_print_sources.py','source_phase6_entries.py',
        'source_phase6_query_support.json','source_phase6_api.py','tests/test_source_phase6_parent_save_print.py']]
    files+=['web/src/plugins/erp/OriginalEntryWorkbench.vue','tools/legacy_snapshot/read_phase6_remaining_save_sources.ps1']
    evidence={'verified_at':review['updated_at'],'baseline_sha256':digest('docs/erp-phase6-six-groups-baseline-20261017.json'),
        'fixed_ids_preserved':True,'fixed_counts':review['counts'],'state_counts':review['state_counts'],
        'paused_queries_unchanged':True,'save_source_differences':gaps,'tests':tests,'schema':schema,
        'frontend':{'typecheck':'通过','build':'通过','build_log_sha256':digest('.runtime-temp/phase6/parent-build.log')},
        'browser_save':save_evidence,'browser_prints':prints,
        'screenshot':{'file':'docs/assets/phase6-parent-H004-20261017.png','sha256':digest('docs/assets/phase6-parent-H004-20261017.png')},
        'live_source_evidence':'docs/erp-phase6-remaining-save-live-20261017.json',
        'previous_evidence':'docs/erp-phase6-save-timing-print-verification-20261017.json',
        'synthetic_browser_rows_added':len(read('.runtime-temp/phase6/parent-fixtures.json')),
        'historical_import_rows_this_run':0,'development':'增量代码及所列验证完成；第六阶段整体部分完成',
        'historical_reconciliation':'未完成全量历史对账','field_acceptance':'未现场验收',
        'code_sha256':{p:digest(p) for p in files}}
    save('docs/'+EVIDENCE,evidence)
    text=f'''# 第六阶段六组续验与剩余清单

更新日期：{review['updated_at'][:10]}（最新旧库来源、专用保存时机、父单/客户打印范围续验）。固定933个编号全部保留；六组存在交叉，不能相加为独立功能数。**第六阶段整体仍为部分完成。** 原35项查询、财务继续暂缓；没有新增额外旧erpID字段。

## 当前数量与完成标准

|组|固定数量|开发核验现状|历史全量对账|现场验收|
|---|---:|---|---|---|
|1 本行/保存字段|116|111条编译保存、3条人工原字段、2条来源差异|未完成|未完成|
|2 父子/专用来源|156|123条编译保存、29条已有专用服务、1条仅查询投影、3条来源差异|未完成|未完成|
|3 查询试算|95|85条非财务公式；此前35个入口非空浏览器证据保留，84条样本通过，ReworkBathRatio含5行缺父来源；10条财务暂缓|未完成|未完成|
|4 自动事件/转单|272|235条接线或明确替代；9条明确缺口；28条财务配置暂缓。接线不代表全部逐绑定验证完成|未完成|未完成|
|5 原打印|290|20份具备静态填数条件，241份运行/来源差异，29份无XML；完整原样张验收仍为0|未完成|未完成|
|6 综合验证|4|425项相关回归、44项针对性复验通过（重叠）；新增2组浏览器保存、4份非空校样；前端类型检查及构建通过|未完成|未完成|

打印范围进一步拆分：158份明确非财务＝20份具备校样条件＋138份仍有差异；35份财务暂缓；68份无明确入口；29份无XML。缺入口、缺XML没有被排除。此前16/142已更新为20/138，不能说20份已完整复刻。

## 5条保存来源差异的最新核验

2026-10-17通过SELECT读取旧库Textile_GXHFRS的当前字段和入口配置。以下5条仍缺可执行的完整依据，**数量没有减少**。本次补的是保存保留与审计：逐条测试NULL、负数/异常等级和重复记录；保存后明确登记 `entry_formula_source_pending`，没有用0、第一条候选或猜测合计替换原值。

|编号|原入口.字段|最新证据|当前实现与尚缺内容|
|---|---|---|---|
|F004|AddStuffWeight.Moisture1|原IIF有4个参数，且GaryPrice/PreMeter等来源不齐|保留人工原值并留痕；需要完整公式与字段对应，不能随意移动括号|
|F281|Quote.IsConfirmed|原表达式引用Price，实际写入FixedPrice表没有Price|保留原IsConfirmed；不能借另一报价表Price代算|
|F273|QueryRecordCheck.GradeID|查询来自RecordYield，UpdateSQL指向缺失RecordYieldCheck；avgdots依赖另一个缺失明细关系|保留现有原字段录入和明确映射，核对表与评分来源仍未复刻|
|F361|WareHouseProdCount.Rolls|原式引用ProdIn_ProdInRecord；当前入口没有该子关系|保留原Rolls，不把其他入库细码当成本单所属细码|
|F362|WareHouseProdCount.WeightQty|同一未声明的子关系；没有新SQL模块定义补足关系|保留原WeightQty，完整子行归属仍待来源证据|

证据：[本轮只读元数据](erp-phase6-remaining-save-live-20261017.json)。3条人工占位字段、1条只读Remarks投影仍按前轮分类保留，不重新列为待开发公式，也不把这5条变成“已完成”。

## 本次完成的增量开发与验证

1. **专用服务保存时机**：染程上限和配方浴比的父子传播加入整单批次；先写本次主从输入，再传播，再执行保存后汇总/事件。父参数改变时，未修改子行正常计算；同次明确填写的NULL或负数保留。本次全部计算字段都已明确输入时，不先计算无须采用的溢出结果。真正超容量仍回滚整单，没有截断。
2. **浏览器两次保存**：P-SAVE父MaxValue由1改2，同时DefaultValue由999999改1，另一重复步号行Price明确清空，重开后三行价格为空/6/2；下次父改3且第三行明确Price=-7，重开后为9/9/-7。三个相同步号原行全部保留。
3. **原打印父单显示列**：沿原Master/RelaFieldNames取父单，使用原选择器解析本厂规格、客户、车牌；重复代码不同名称全部显示候选，枚举缺定义显示原代码。多父行歧义明确报出，不任选父行。H004、K008校样各3行1页。
4. **打印范围与页眉一致**：H004试样留底和K008装车单明确输入父单流水号；R015出库对账明确输入客户编码。查询结果保持完整，只对本次打印范围取全部明细；显示查询总行数与本范围行数；NULL与空字符串编码分别明确选用，未填写客户也可进入打印范围。若父单关联本身缺失仍明确列差异，不编造父单。不能用混合父单/客户的第一页单头代表所有明细。
5. **R66-2装箱表**：原内层SheetSeries空串按原父子键改为明确参数，原窗口、分组、重复计数和负数保持。P-L校样3行1页。原地址选择器A009指向付款类型，尚无正确地址来源依据；原配置保留，未匹配地址明确显示原代码。没有扩展财务流程。
6. **R015客户误绑定**：GrayInWaste.NameC明确采用当前GrayOutWaste查询已有pc.NameC；没有跨入库借值。浏览器原查询9行，客户P-C范围6行1页：3条出库明细连接2条同码客户，连接倍增与合计保留。其原页眉按该页首行显示客户名，本例客户甲；不同名称的同码原查询行仍全部保留，旧客户端在此异常下的显示顺序待样张对账。
7. **原字符串格式**：K008地址文本误带日期格式，按.NET字符串不实现IFormattable的行为保留原文字；不把地址解析成日期，也不把数字字符串自动转数值。已以本机.NET格式化结果和回归用例核实；原XML不改写。[格式化方法依据](https://learn.microsoft.com/en-us/dotnet/api/system.iformattable.tostring?view=netframework-4.8)。

## 验证证据与界限

- [本轮验证汇总]({EVIDENCE})、[固定933项状态](erp-phase6-six-groups-review-20261017.json)、[不可变基线](erp-phase6-six-groups-baseline-20261017.json)。
- [两次浏览器保存重开值](assets/phase6-parent-browser-save-20261017.json)。
- 浏览器校样：[H004](assets/phase6-parent-H004-20261017.html)、[K008](assets/phase6-parent-K008-20261017.html)、[R66-2](assets/phase6-parent-R66-2-20261017.html)、[R015](assets/phase6-parent-R015-20261017.html)；本次截图接口已可用，[H004实际截图](assets/phase6-parent-H004-20261017.png)。未向打印机发送，没有登记设备打印成功。
- 浏览器数据均为合成验证数据，本次增加22行，其中1行补齐上轮CONT-DIP明细试算样本的测试父单。首次缺父单时校样明确失败，未跳过3条旧测试明细；补齐测试父单后验证。没有导入旧ERP历史业务数据。
- 当前766个ERP模型、655个原表模型、12606个原字段；额外旧erpID字段0。系统检查及迁移检查通过。本轮前端有打印范围选择改动，类型检查与构建均通过。
- 开发完成只限上述代码和已列用例。全量历史结果对账、原12.2客户端显示细节、原纸张字体与条码设备验收仍未完成。

## 剩余开发顺序

1. 保留这5条来源差异及现有输入入口，按异常说明逐项补完整原公式、表或主从来源。最新旧库仍无定义的不能虚报完成；本轮已经完成可推进的保存保留和留痕验证。
2. 继续235条接线中的逐绑定事件时机、转单/撤销验证；9条明确缺口仍为3条外部调用与回执、2条缺原表、2条最新表缺目标字段、2条不完整过滤。原35查询继续暂缓，不能因此跳过其他异常入口。
3. 继续138份非财务复杂原打印：脚本、动态高度、多列、子报表及显示来源；68份缺明确入口、29份缺XML继续登记。20份校样还需逐原样张核对，不计完整原打印完成。
4. 历史对账：一致抽取时点下逐单逐行比较，保留异常、重复、撤回记录；计划、实称、收发分别比对。合成测试不能替代历史对账。
5. 现场验收：岗位实际流转、纸张字体裁切、扫描效果及真实设备回执。开发完成与这两项分开登记。

## 固定编号逐项结果

以下编号未删除、未重排；历史全量对账和现场验收均未完成，具体代码/样本证据见JSON。
'''
    for group,rows in review['groups'].items():
        text+='\n### 第'+group+'组\n\n|编号|入口/报表|字段/事件|当前状态与差异|\n|---|---|---|---|\n'
        for row in rows:
            reasons=[r['reason'] for r in row.get('results',[]) if r['state'] in ['explicit_difference','explicit_manual_input','query_projection_only']]+row.get('issues',[])
            if group=='5':reasons.insert(0,row['scope'])
            text+='|'+'|'.join(cell(v) for v in [row['id'],row.get('entry',row.get('report',row.get('name',''))),row.get('field',row.get('event',row.get('title',''))),row['state']+('；'+'；'.join(reasons) if reasons else '')])+'|\n'
    (DOCS/TITLE).write_text(text,encoding='utf8')
    current=f'''## 当前有效第六阶段清单（父子保存与原打印范围续验）

以[{TITLE}]({TITLE})、[{EVIDENCE}]({EVIDENCE})为准。933固定编号和原35项暂停范围不变；第六阶段整体部分完成。

5条真实保存来源差异经最新旧库只读核验仍存在；已补原值保留、NULL/负数/重复行保存和明确留痕，未伪造公式。专用配方/染程服务整单时机已补；2组浏览器保存通过。新增H004/K008/R66-2/R015四份非空校样及父单/客户打印范围，20份具备校样条件，241份运行/来源差异、29份缺XML；明确非财务打印仍138份差异，另68份缺入口。

425项相关回归、44项针对性复验通过（重叠），前端类型检查/构建通过。事件235接线仍需逐绑定核验，9缺口、28财务配置不变。模型无新增字段，额外旧erpID为0，历史导入0。全量历史对账与现场验收均未完成。'''
    for name in ['2026-10-16染色ERP剩余工作全量盘点清单.md','染色ERP后续开发方案.md']:section(DOCS/name,'phase6-form-flows-current',current)
    reasons={
        'E243':('5条保存来源的最新核验与保留审计','部分完成','最新旧库元数据仍不能还原5条公式；NULL、负数/异常等级、重复行保存及明确来源待补留痕验证完成。缺公式、缺核对表和子关系不以猜测结果替代。'),
        'E244':('专用配方及染程父子整单保存时机','已完成','本次全部输入写完后再传播，明确子值保留，真正超容量整单回滚；相关回归及两次浏览器保存重开验证通过。仅开发验证完成，历史对账和现场未完成。'),
        'E245':('父单显示来源及复杂原打印范围','部分完成','4份新增非空浏览器校样；原选择器、重复候选及单父单/单客户范围实现。R66-2空串改明确父单参数，A009地址误绑来源未证实；R015同码客户重复连接及原页眉首行显示保留；K008文本日期格式按.NET字符串规则输出。20份校样不等于完整原打印验收。')}
    exception='## 父子保存、5条来源及原打印范围续验\n\n本节为最新增量结论；此前16/142等数量为历史记录，当前为20份具备校样条件、138份非财务打印差异。\n\n'
    for key,(name,status,reason) in reasons.items():exception+=f'### {key} {name}\n\n{reason}\n\n'
    exception+='5条来源逐字段、装箱地址A009、R015同码多名、打印范围及全部剩余步骤见['+TITLE+']('+TITLE+')；最新只读证据见[旧库元数据](erp-phase6-remaining-save-live-20261017.json)。历史全量对账、现场验收未完成。'
    section(DOCS/'旧ERP复刻异常与合理实现说明.md','phase6-parent-save-print-exceptions',exception)
    inventory=read('docs/erp-remaining-inventory-20261016.json');axis=inventory['axes']['新旧系统差异及处理情况']
    for key,(name,status,reason) in reasons.items():
        value={'id':key,'name':name,'status':status,'reason':reason,'related_sql':[],'source':'docs/旧ERP复刻异常与合理实现说明.md'}
        existing=next((i for i,r in enumerate(axis) if r['id']==key),None)
        if existing is None:axis.append(value)
        else:axis[existing]=value
    inventory['counts']['新旧系统差异及处理情况']=dict(Counter(r['status'] for r in axis))
    summary={'document':TITLE,'evidence':EVIDENCE,'fixed_counts':review['counts'],'state_counts':review['state_counts'],
        'development':'增量代码及验证完成，阶段整体部分完成','historical_reconciliation':'未完成','field_acceptance':'未完成','tests':tests}
    inventory['phase6_six_groups_20261017']=summary
    inventory['phase6_review'].update(current_evidence='docs/'+EVIDENCE,next='5条来源差异保持；事件235接线逐绑定及9缺口；138份非财务打印差异及68缺入口/29缺XML。原35查询及财务继续暂缓。')
    for row in inventory['axes']['旧界面配置入口']:
        if row['name'] in {g['entry'] for g in gaps}|{'p_DyeCurve','p_DyeCurveDetail','ProdLoadingDetail','ProdLoadingDetail2','DyeDipsRecordPhaseDetail','GrayOutWaste'}:
            row['phase6_parent_save_print_20261017']={'evidence':EVIDENCE,'development':'所列增量已验证，整入口不升级完成','historical_reconciliation':'未完成','field_acceptance':'未完成'}
    save('docs/erp-remaining-inventory-20261016.json',inventory)
    old=read('docs/erp-phase6-review-20261016.json');old.update(six_groups_20261017=summary,current_review_at=evidence['verified_at']);save('docs/erp-phase6-review-20261016.json',old)
    print(json.dumps({'tests':tests,'print_eligible':len(eligible),'nonfinance_print_differences':len(nonfinance),'save_differences':len(gaps),'exceptions':len(axis),'fixed_counts':review['counts']},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
