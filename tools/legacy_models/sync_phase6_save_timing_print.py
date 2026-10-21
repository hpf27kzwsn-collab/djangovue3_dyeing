"""保存时机与条码增量证据；固定编号、暂缓范围及历史/现场状态分别维护。"""
from sync_phase6_six_groups_continued import read,save,digest,section,test_result,cell,ROOT,DOCS
from collections import Counter
from datetime import datetime
import json

TITLE='2026-10-17第六阶段六组续验与剩余清单.md'
EVIDENCE='erp-phase6-save-timing-print-verification-20261017.json'


def main():
    baseline=read('docs/erp-phase6-six-groups-baseline-20261017.json')
    review=read('docs/erp-phase6-six-groups-review-20261017.json')
    prior=read('docs/erp-phase6-six-groups-continued-verification-20261017.json')
    assert review['paused_queries']==baseline['paused_queries']
    for group,rows in baseline['groups'].items():assert [r['id'] for r in rows]==[r['id'] for r in review['groups'][group]]
    tests={'regression':test_result('timing-regression.log'),'targeted':test_result('timing-final.log'),'note':'37项包含在413项内，不相加'}
    browser=read('docs/assets/phase6-timing-browser-save-20261017.json')
    assert browser['tests'][0]['values']==[{'label':'Rate','value':'9.00'},{'label':'浴比','value':'-3.00'}]
    assert browser['tests'][1]['values']==[{'label':'Rate','value':'12.00'},{'label':'浴比','value':''}]
    prints=[]
    for code,count,pages,bars in [('H005',2,2,4),('H006',2,2,4),('R154',4,1,4)]:
        path=f'docs/assets/phase6-timing-{code}-20261017.html';html=(ROOT/path).read_text(encoding='utf8')
        assert html.count('<section class="page">')==pages
        assert html.count('data-symbology="Code128"')==bars
        prints.append({'report':code,'rows':count,'pages':pages,'barcodes':bars,'html':path,'sha256':digest(path)})
    for row in review['groups']['5']:
        for proof in [*prior['browser_prints'],*prints]:
            if row['report']==proof['report']:row['browser_verification']=proof
    for row in review['groups']['3']:
        if row['entry'] in {v['entry'] for v in read('docs/assets/phase6-continued-browser-entries-20261017.json')}:
            row['browser_verification']='沿用此前非空浏览器查询证据；不是全部业务分支验收'
    for row in review['groups']['1']+review['groups']['2']:
        states={r['state'] for r in row['results']}
        if 'explicit_manual_input' in states:row['verification']='test_manual_placeholder_dates_and_anomalous_values_survive_save：原时间、负数及无关字段编辑保留'
        if 'query_projection_only' in states:row['verification']='原Kind=Query且无UpdateSQL/TableName；此前父工卡备注非空投影测试及浏览器证据，不把原查询映射成配方写回'
    event=next(r for r in review['groups']['4'] if r['id']=='H197')
    event['verification']='test_small_stuff_after_save_sees_all_new_lines_once：整单2/2/-3重复明细写完，先库存触发再AfterSave；本例LastPrice=NULL、Price=5。浏览器该入口时机仍未逐绑定验收。'
    statuses=['413项相关回归通过，37项最终针对性复验通过（重叠）',
              '新增2组父子同次保存及3份非空原条码校样浏览器验证；此前35入口证据保留',
              '模型及迁移检查通过，无新增字段；前端本轮未改，沿用上轮构建验证',
              '全量历史数据对账未完成；现场验收未完成']
    for row,state in zip(review['groups']['6'],statuses):row['state']=state
    review['updated_at']=datetime.now().astimezone().isoformat()
    review['state_counts']={g:dict(Counter(r.get('state','待验证') for r in rows)) for g,rows in review['groups'].items()}
    save('docs/erp-phase6-six-groups-review-20261017.json',review)
    eligible=[r for r in review['groups']['5'] if not r['issues']]
    nonfinance=[r for r in review['groups']['5'] if r['scope']=='非财务入口' and r['issues']]
    assert len(eligible)==16 and len(nonfinance)==142
    schema=read('.runtime-temp/phase6/continued-schema.json');assert not schema['extra_legacy_id_fields']
    files=['backend/plugins/erp_base/'+n for n in ['document_services.py','source_services.py','source_phase6_save_timing.py','source_phase6_formula_runtime.py','source_phase6_formula_registry.json','source_phase6_linear_print.py','source_phase6_qr_print.py','source_phase6_rendering.py','source_phase6_print_sources.py','tests/test_source_phase6_save_timing_print.py']]
    files+=['backend/requirements.txt','requirements.lock.txt','tools/legacy_models/build_phase6_formula_registry.py','tools/legacy_models/review_phase6_six_groups.py']
    evidence={'verified_at':review['updated_at'],'baseline_sha256':digest('docs/erp-phase6-six-groups-baseline-20261017.json'),
              'fixed_ids_preserved':True,'fixed_counts':review['counts'],'state_counts':review['state_counts'],
              'formula_registry_counts':review['formula_registry_counts'],'tests':tests,'schema':schema,
              'browser_save':browser,'browser_prints':prints,'previous_evidence':'docs/erp-phase6-six-groups-continued-verification-20261017.json',
              'paused_queries_unchanged':True,'historical_import_rows_this_run':0,'synthetic_browser_rows_added':8,
              'development':'本次保存时机修正和Code128开发验证完成；第六阶段整体部分完成',
              'historical_reconciliation':'未完成全量对账','field_acceptance':'未现场验收',
              'screenshot':'接口仍无法截图；已保存实际浏览器校样HTML和重新打开后的表单值',
              'code_sha256':{p:digest(p) for p in files}}
    save('docs/'+EVIDENCE,evidence)
    text=f'''# 第六阶段六组续验与剩余清单

更新日期：2026-10-17（保存时机与条码续验）。固定933个编号全部保留。六组有交叉，不相加为独立功能数；第六阶段整体仍为部分完成。原35项查询及财务继续暂缓，额外旧erpID字段为0。

## 当前数量与完成边界

|固定组|数量|当前开发与验证|剩余内容|
|---|---:|---|---|
|1 本行/函数公式|116|111条编译保存路径；3条人工字段的原值保存已验证|2条原表达式/来源差异；全部保存分支仍需逐项验证|
|2 父子来源公式|156|123条编译保存路径，29条已有自动服务；1条确认属于只读查询投影|3条保存来源差异；已接线不表示全部事件时机已验收|
|3 查询/非物理字段|95|85条非财务公式覆盖35入口，此前均非空运行并逐入口浏览器查询；84条样例行成功，1条保留5行父单缺失|10条财务赔款公式暂缓；异常行和整入口其他来源差异保留|
|4 事件、转单、过滤|272|235条有实现或明确替代接线；本次补充H197整单后事件时机测试|9条明确缺口、28条财务配置；235条仍有逐绑定原行为及浏览器核验工作|
|5 原打印|290|16份具备当前静态校样条件；本次H005/H006/R154三份完成非空浏览器校样|245份原运行/来源差异，29份无XML。16份不等于完整复刻；完整原版式验收仍为0|
|6 验证和资料|4|413项相关回归、37项最终针对性复验通过；2组同次父子保存、3份条码校样通过浏览器验证|37项包含在413项内。历史全量对账、现场验收分别未完成|

打印按范围分为158份明确非财务入口（16份具备静态条件、142份有差异）、35份财务打印暂缓、68份缺明确入口定义、29份缺XML。后两类没有从业务范围删除。第三组核验的35入口与继续暂缓的原35项查询不是同一批。

## 本次实改及核验

1. **整单保存顺序修正**：原代码写完父单便向旧子行传播公式，同次提交的子行输入尚未写完。现在先写本次全部主从输入，再传播和汇总，最后执行保存后事件。本次明确输入（包括NULL、负数）在整个事务内优先；下一次单独修改父来源时仍照原公式传播，不永久冻结子行。
2. 浏览器TIME-SAVE同次保存父Rate=9、子BathRatio=-3，重新打开分别为9/-3；再保存父Rate=12、子BathRatio明确清空，重新打开分别为12/空。必要测试另保留两条相同PhaseNo子行：只明确改一条时，另一条正常跟随父公式。
3. **H197染料入库价格事件**：通过真实整单服务写入2、2、-3三条重复明细，正价格3、5及负价格-2全部保留。旧库存触发器先重取13类采购价，本例没有13类采购，因此先写Price=NULL；随后AfterSave才将NULL移到LastPrice，并将Price置为最后正价5。多候选仍全部留档，按承接顺序末项回写属于已有明确替代，尚未证明旧无序UPDATE选行与之相同。
4. **保存来源清单更正**：AddStuffWeight.ClothQtyKg是自引用占位；MoveShiftBill.BeginTime/DayEnd是日期格式串。三项保留人工录入和完整时间，不执行伪公式，测试已通过。qry_QuoteRelaRecipe.Remarks的原Kind为Query，UpdateSQL和TableName均为空；它按父工卡备注做查询投影，不应写回某张配方表。这4项仍保留原固定编号，不再误称缺保存计算。
5. **Code128原打印**：补齐固定A/B/C与Auto编码、校验位、自动模块及可见文字。原XML省略CharacterSet时按A；中文、小写等超出固定字符集时明确指出原值异常，不删字符、截断、换码或跳过记录。三份新校样均保留重复数据。
6. H006日期误绑PrintJobSheet、R154员工号误绑h_Employee：按当前行同一原表字段明确替代，不跨行借值。松筒/加捻多选机台串分隔约定尚未证明，暂打印完整原代码（含重复、未知代码），不猜分隔后取名称。原XML没有改写。

## 验证证据

- [本轮验证汇总]({EVIDENCE})、[933项固定编号状态](erp-phase6-six-groups-review-20261017.json)、[固定基线](erp-phase6-six-groups-baseline-20261017.json)。
- [两组浏览器整单保存](assets/phase6-timing-browser-save-20261017.json)。H005为2行2页4个条码；H006为2行2页4个条码；R154为4行1页4个条码，含2行相同员工号。均为合成验证库，历史导入0行。
- [H005浏览器校样](assets/phase6-timing-H005-20261017.html)、[H006浏览器校样](assets/phase6-timing-H006-20261017.html)、[R154浏览器校样](assets/phase6-timing-R154-20261017.html)。截图接口仍不可用，没有用生成图片冒充截图；未向打印机发送、未增加打印成功次数。
- 此前35个查询入口、H007/H019/R014/R040/R036校样证据保留于[上轮汇总](erp-phase6-six-groups-continued-verification-20261017.json)。K035仍只有静态条件检查，不能计作非空浏览器验收。
- 当前766个ERP模型、655个原表模型、12606个原字段；额外旧erpID字段0，系统检查通过，无新迁移。本轮前端未改动，沿用上轮构建验证，没有声称再次构建。

## 剩余开发顺序

1. **5条真实保存来源差异**：AddStuffWeight.Moisture1原IIF畸形且来源不齐；Quote.IsConfirmed在实际FixedPrice表中找不到Price；QueryRecordCheck.GradeID依赖缺失的核对表/avgdots；WareHouseProdCount.Rolls/WeightQty引用另一个入口的子关系，原目录未定义对应子表。原值可明确录入的继续保留；不能改成无依据的合计或凭空补表。
2. **事件逐绑定**：9条明确缺口仍为3条外部调用及回执、2条缺原表、2条最新表已无目标字段、2条不完整过滤。235条接线中原行为差异、转单及撤销时机仍需逐绑定测试和浏览器核验，本次H197单项测试不能覆盖其他入口。
3. **复杂原打印**：继续142份非财务差异及68份缺明确入口/29份缺XML的来源核实。脚本、动态高度、多列、子报表、缺显示名/关系等仍是开发问题，不能统称设备接入。R122的JobKind中文标签来源仍未证明。
4. **历史对账**：同一抽取时点逐单逐行核对，包括异常、重复、撤回留档；计划、实称、实际收发各自对比。合成测试不替代此项。
5. **现场验收**：岗位实际顺序、原打印纸张/字体/裁切、条码可扫性与真实设备回执。本轮均未完成。

Code128属性依据：[字符集与默认A](https://docs.devexpress.com/CoreLibraries/DevExpress.XtraPrinting.BarCode.Code128Generator.CharacterSet)、[自动模块](https://docs.devexpress.com/XtraReports/DevExpress.XtraReports.UI.XRBarCode.AutoModule)、[文字对齐](https://docs.devexpress.com/XtraReports/DevExpress.XtraReports.UI.XRBarCode.TextAlignment)。当前文档用于解释属性，不等于证明旧12.2版本的每个像素；静区、字体尺寸和扫描设备效果继续列为对照事项。

## 固定编号逐项结果

下表“通过”限代码及所列合成验证；各项历史全量对账未完成、现场未验收。固定编号未删除、未重新分组。
'''
    for group,rows in review['groups'].items():
        text+='\n### 第'+group+'组\n\n|编号|入口/报表|字段/事件|当前状态与差异|\n|---|---|---|---|\n'
        for row in rows:
            reasons=[r['reason'] for r in row.get('results',[]) if r['state'] in ['explicit_difference','explicit_manual_input','query_projection_only']]
            reasons+=row.get('issues',[])
            if group=='5':reasons.insert(0,row['scope'])
            text+='|'+'|'.join(cell(v) for v in [row['id'],row.get('entry',row.get('report',row.get('name',''))),row.get('field',row.get('event',row.get('title',''))),row['state']+('；'+'；'.join(reasons) if reasons else '')])+'|\n'
    (DOCS/TITLE).write_text(text,encoding='utf8')
    current=f'''## 当前有效第六阶段清单（保存时机与原条码续验）

以[{TITLE}]({TITLE})和[{EVIDENCE}]({EVIDENCE})为准。933固定编号不变；第六阶段整体部分完成。已修正整单主从公式传播时机，2组浏览器保存通过，新增3份条码校样。413项相关回归、37项最终针对性复验通过（重叠）。

原9条保存差异重新核实为3条人工原字段、1条只读查询投影和5条真实来源差异；没有删除编号或伪称新增4条计算。原打印16份具备静态条件，245份运行/来源差异、29份缺XML；明确非财务打印剩余142份，另68份缺明确入口继续核实。事件235条接线仍需逐绑定验证，9条明确缺口与28条财务配置保持登记。

原35项查询、财务继续暂缓。额外旧erpID字段0，历史导入0；开发验证、全量历史对账、现场验收分列，后两项未完成。'''
    for name in ['2026-10-16染色ERP剩余工作全量盘点清单.md','染色ERP后续开发方案.md']:section(DOCS/name,'phase6-form-flows-current',current)
    reasons={
        'E240':('整单父子公式时机修正','已完成','本次全部输入写完后才传播公式；同次明确NULL/负数不被父来源覆盖，未改子行正常联动。已做服务与浏览器验证；历史对账和现场另列。'),
        'E241':('人工字段与只读投影的保存范围更正','已完成','F001胚重自引用、调班两项日期格式保留输入；qry_QuoteRelaRecipe.Remarks为无更新目标的原只读投影。原9项中仍5项缺来源/畸形配置，不猜公式、不删异常原值。'),
        'E242':('原Code128条码与误绑定的明确替代','部分完成','H005/H006/R154非空浏览器校样通过；两处前缀误绑采用当前原表行，机台多选串完整原代码展示。默认A字符集、校验位与自动模块已实现；静区、原字体、旧版排版及扫码设备尚未对照，不能计原打印完整复刻。')}
    exception='## 保存时机、字段范围及条码续验\n\n当前数量以六组续验清单为准；E233/E234/E237中的旧数量为此前记录。\n\n'
    for key,(name,status,reason) in reasons.items():exception+=f'### {key} {name}\n\n{reason}\n\n'
    exception+='明确未复刻的5条保存来源、142份非财务打印差异以及事件缺口逐项见['+TITLE+']('+TITLE+')。'
    section(DOCS/'旧ERP复刻异常与合理实现说明.md','phase6-save-timing-print-exceptions',exception)
    inventory=read('docs/erp-remaining-inventory-20261016.json');axis=inventory['axes']['新旧系统差异及处理情况']
    for key,(name,status,reason) in reasons.items():
        value={'id':key,'name':name,'status':status,'reason':reason,'related_sql':[],'source':'docs/旧ERP复刻异常与合理实现说明.md'}
        existing=next((i for i,r in enumerate(axis) if r['id']==key),None)
        if existing is None:axis.append(value)
        else:axis[existing]=value
    inventory['counts']['新旧系统差异及处理情况']=dict(Counter(r['status'] for r in axis))
    summary={'document':TITLE,'evidence':EVIDENCE,'fixed_counts':review['counts'],'state_counts':review['state_counts'],'development':'增量验证完成，阶段整体部分完成','historical_reconciliation':'未完成','field_acceptance':'未完成','tests':tests}
    inventory['phase6_six_groups_20261017']=summary
    inventory['phase6_review'].update(current_evidence='docs/'+EVIDENCE,next='5条保存来源差异、事件235接线逐绑定及9缺口、142份非财务打印差异和68缺入口/29缺XML；原35查询及财务继续暂缓。')
    for row in inventory['axes']['旧界面配置入口']:
        formulas=[r for g in ['1','2','3'] for r in review['groups'][g] if r['entry']==row['name']]
        if formulas:row['phase6_six_groups_20261017']={'document':TITLE,'fields':[{'id':r['id'],'field':r['field'],'state':r['state']} for r in formulas],'development':'整入口不升级完成','historical_reconciliation':'未完成','field_acceptance':'未完成'}
    save('docs/erp-remaining-inventory-20261016.json',inventory)
    old=read('docs/erp-phase6-review-20261016.json');old.update(six_groups_20261017=summary,current_review_at=evidence['verified_at']);save('docs/erp-phase6-review-20261016.json',old)
    print(json.dumps({'tests':tests,'print_eligible':len(eligible),'nonfinance_print_differences':len(nonfinance),'exceptions':len(axis),'fixed_counts':review['counts']},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
