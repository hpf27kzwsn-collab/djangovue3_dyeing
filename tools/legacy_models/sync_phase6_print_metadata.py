"""同步133份来源复查、文字事件及保存来源证据，不提升全量对账或现场状态。"""
from sync_phase6_six_groups_continued import read,save,digest,section,test_result,cell,ROOT,DOCS
from collections import Counter
from datetime import datetime
import re

TITLE='2026-10-17第六阶段六组续验与剩余清单.md'
EVIDENCE='erp-phase6-print-metadata-verification-20261018.json'


def main():
    baseline=read('docs/erp-phase6-six-groups-baseline-20261017.json')
    review=read('docs/erp-phase6-six-groups-review-20261017.json')
    previous=read('.runtime-temp/phase6/metadata-prior-review.json')
    assert review['paused_queries']==baseline['paused_queries']
    for group,rows in review['groups'].items():
        assert [r['id'] for r in rows]==[r['id'] for r in baseline['groups'][group]]
        old={r['id']:r for r in previous['groups'][group]}
        for row in rows:
            for key in ['verification','browser_verification']:
                if key in old[row['id']]:row[key]=old[row['id']][key]
    tests={'regression':test_result('metadata-regression.log'),'final_targeted':test_result('metadata-target-final.log'),
           'note':'464项相关回归通过；最终18项复验包含新增1项范围测试，其余17项与464项重叠，不能相加。'}
    assert tests['regression']['count']==464 and tests['final_targeted']['count']==18
    proofs=[]
    for item in read('docs/assets/phase6-metadata-browser-print-20261018.json'):
        code=item['report'];path=f'docs/assets/phase6-metadata-{code}-20261018.html';html=(ROOT/path).read_text(encoding='utf8')
        rows,pages=map(int,re.search(r'(\d+) 行，(\d+) 页',item['text']).groups())
        assert html.count('<section class="page">')==pages
        assert (rows,pages)==((8,1) if code=='R121' else (17,3))
        proofs.append({'report':code,'rows':rows,'pages':pages,'html':path,'sha256':digest(path),
            'scope':'META-IN' if code=='R121' else 'META-OUT','query_rows':11 if code=='R121' else 57,
            'development':'应用发起校样及独立HTML页面验证通过；内嵌纸张显示未通过',
            'historical_reconciliation':'未完成','field_acceptance':'未完成'})
    assert {p['report'] for p in proofs}=={'H008','H024','R121'}
    for row in review['groups']['5']:
        proof=next((p for p in proofs if p['report']==row['report']),None)
        if proof:row['browser_verification']=proof
        if row['report'] in ['R101','R101-1']:
            row['verification']='原单位文字事件已逐值验证；仍缺TrialDyeRecipe.ColorID_R父投影，整份打印未完成。'
    for row in review['groups']['4']:
        if row.get('entry')=='CookIn' and row.get('event')=='AfterSaveSQL':
            row['verification']='实际CookIn保存后按原SQL的ArticleIn/ArticleInDetail→p_Article回写；同号2头×3行的6个候选全部留痕。NULL/0/已有Price、负数及实际浏览器保存通过。无序UPDATE取末项是明确替代，不称原数据库逐值等价。'
    states=['464项相关回归及18项最终复验通过（17项重叠、1项新增）',
        '新增3份非空打印及CookIn保存浏览器验证；独立HTML排版通过，内嵌校样框纸张显示未通过，之前证据保留',
        '766模型/655原表/12606原字段；额外旧erpID为0；类型检查及构建通过',
        '全量历史对账未完成，现场验收未完成；本轮历史导入0']
    for row,state in zip(review['groups']['6'],states):row['state']=state
    review['updated_at']=datetime.now().astimezone().isoformat()
    review['state_counts']={g:dict(Counter(r['state'] for r in rows)) for g,rows in review['groups'].items()}
    eligible=[r for r in review['groups']['5'] if not r['issues']]
    differences=[r for r in review['groups']['5'] if r['scope']=='非财务入口' and r['issues']]
    gaps=[r for g in ['1','2'] for r in review['groups'][g] if any(v['state']=='explicit_difference' for v in r['results'])]
    assert len(eligible)==28 and len(differences)==130 and len(gaps)==5
    live=read('docs/erp-phase6-remaining-save-live-20261018.json');oldlive=read('docs/erp-phase6-remaining-save-live-20261017.json')
    assert all(live[k]==oldlive[k] for k in ['tables','entries','fields','references'])
    schema=read('.runtime-temp/phase6/continued-schema.json');assert not schema['extra_legacy_id_fields']
    source_audit=read('docs/erp-phase6-print-source-audit-20261018.json')
    assert (source_audit['reports_checked'],source_audit['remaining_report_count'])==(133,130)
    save('docs/erp-phase6-six-groups-review-20261017.json',review)
    files=['backend/plugins/erp_base/'+n for n in ['source_phase6_rendering.py','source_phase6_print_sources.py','source_phase6_text_scripts.py','source_phase6_hooks.py','tests/test_source_phase6_bookmark_events.py']]+['web/src/plugins/erp/OriginalEntryWorkbench.vue','tools/legacy_models/audit_phase6_print_sources.py']
    evidence={'verified_at':review['updated_at'],'baseline_sha256':digest('docs/erp-phase6-six-groups-baseline-20261017.json'),
        'fixed_ids_preserved':True,'fixed_counts':review['counts'],'paused_queries_unchanged':True,
        'save_differences':[r['id'] for r in gaps],'save_sources_live':'erp-phase6-remaining-save-live-20261018.json','save_sources_unchanged_since_20261017':True,
        'print_eligible':28,'nonfinance_print_differences':130,'source_audit':'erp-phase6-print-source-audit-20261018.json',
        'tests':tests,'schema':schema,'browser_prints':proofs,'browser_save':read('docs/assets/phase6-metadata-browser-cook-20261018.json'),
        'browser_save_database_result':'assets/phase6-metadata-cook-result-20261018.json','browser_visual':read('docs/assets/phase6-metadata-browser-visual-20261018.json'),
        'frontend':{'typecheck':'通过','build':'通过','build_log_sha256':digest('.runtime-temp/phase6/metadata-build.log')},
        'synthetic_browser_rows_added':36,'historical_import_rows_this_run':0,'historical_reconciliation':'未完成','field_acceptance':'未完成',
        'previous_evidence':'erp-phase6-delivery-quality-verification-20261018.json','code_sha256':{p:digest(p) for p in files},
        'screenshots':{f'docs/assets/phase6-metadata-{code}-20261018.png':digest(f'docs/assets/phase6-metadata-{code}-20261018.png') for code in ['H008','H024','R121']}}
    save('docs/'+EVIDENCE,evidence)
    old=(DOCS/TITLE).read_text(encoding='utf8')
    source_section=old.split('## 5条保存来源差异的最新核验')[1].split('## 本次完成的增量开发与验证')[0]
    source_section=source_section.replace('2026-10-17通过SELECT','2026-10-18再次通过SELECT').replace('erp-phase6-remaining-save-live-20261017.json','erp-phase6-remaining-save-live-20261018.json')
    text=f'''# 第六阶段六组续验与剩余清单

更新日期：2026-10-18（133份打印来源复查、书签/文字事件、实际采购保存来源续验）。933个固定编号全部保留，六组有交叉，不能相加为独立功能。**第六阶段整体仍为部分完成。** 原35项查询、财务继续暂缓，不新增额外旧erpID。

## 当前数量与完成标准

|组|固定数量|开发核验现状|历史全量对账|现场验收|
|---|---:|---|---|---|
|1 本行/保存字段|116|111条编译保存、3条人工原字段、2条来源差异|未完成|未完成|
|2 父子/专用来源|156|123条编译保存、29条已有专用服务、1条仅查询投影、3条来源差异|未完成|未完成|
|3 查询试算|95|85条非财务公式：84条样本通过，ReworkBathRatio仍含5行缺父来源；此前35入口浏览器证据保留；10条财务暂缓|未完成|未完成|
|4 自动事件/转单|272|235条接线或明确替代、9条明确缺口、28条财务配置暂缓；本轮补CookIn重复来源留痕及实际保存验证，不能将接线数称为全部验收完成|未完成|未完成|
|5 原打印|290|28份具备填数校样条件、233份运行/来源差异、29份缺XML；完整原样张验收0份|未完成|未完成|
|6 综合验证|4|464项回归、18项最终复验（17项重叠）；3份非空打印、1组采购保存浏览器验证；内嵌纸张显示仍待排查|未完成|未完成|

打印范围：158份非财务＝28份可校样＋130份差异；另35份财务、68份缺明确入口、29份缺XML。本轮开始133份全部逐份复查，新增H008/H024/R121三份可校样，余130份逐项保留；67份含缺定义事件是这133份中的交叉统计，不能再次相加。

## 5条保存来源差异的最新核验
{source_section}
2026-10-18只读结果：170条字段元数据、5条入口、7条字段配置、0条关联SQL模块；与2026-10-17相同，5条差异没有新依据可关闭。

## 本次完成的增量开发与验证

1. **133份原来源逐份复查**：同时读取XML与原C#模板，逐份保存哈希、事件绑定、前后问题。90份含事件名，49份有脚本文本；排除注释、字符串后，67份存在两种来源均无可执行方法声明的事件。缺声明可能来自未提供客户端程序集，不能当空事件跳过；有声明也不等于移植完成。详见[逐份来源清单](2026-10-18第六阶段133份非财务打印来源复查.md)。
2. **送货书签与标签绑定**：H008/H024的Text、Bookmark、Tag分别执行，附加信息不覆盖正文。按原日期格式生成每页独立书签，重复文本不合并，NULL与空串分别留痕；HTML转义测试通过。按SheetSeries选父单，原查询57行、所选17行，均3页；书签实际跳至第3页成功。合成样本总件数16，H008总重160.00，H024原模板无总重栏，保留Lb原文不擅自换算。
3. **原文字事件时机**：R121在数据绑定后、打印前执行原tableCell28_BeforePrint：OriJobsheetNo去空格后非空则显示，否则显示ReceSheetNo。按单头流水号限定日期页眉。4条原明细与2条同号客户形成8行全部进入原汇总；原ZRolls/ZWeightQty使用Abs，合计14条/14kg，负数原行仍保留。ReceSheetNo组头显示一次不是删除重复数据。R101/R101-1单位事件0→%、1→g/l、其余取原RecipeUnit_R，已验证；仍缺父投影TrialDyeRecipe.ColorID_R，两份整版继续列差异。只承接已核对的脚本正文与事件绑定，未绑定方法不执行。
4. **无字段分组头**：空GroupFields按整份本次数据分组；内层分组仍独立保留。R011因此去掉此项功能障碍，但剩余5处打印来源差异仍报出，包括CusProName、JobKind，未虚报整版完成。
5. **CookIn实际保存事件**：原AfterSaveSQL引用ArticleIn/ArticleInDetail（SheetKind=13）更新p_Article，不擅改为CookInDetail/p_Cook。保存联动仍由service层承担；同号2头×3行的6个候选逐个记录，3条同号材料全部保留。Price仅原NULL/0时回写，已有9保持，LastPrice均更新为-7。原SQL无ORDER BY，多来源取承接顺序末项是明确替代，完整候选、选择行及前后值留档；不能声称与旧SQL每次随机执行结果相同。

## 验证证据与界限

- [本轮验证汇总]({EVIDENCE})；[固定编号状态](erp-phase6-six-groups-review-20261017.json)；[前轮证据](erp-phase6-delivery-quality-verification-20261018.json)。464项回归通过；最终18项中17项重叠、1项新增。类型检查、构建、模型及迁移检查通过，766模型/655原表/12606原字段，额外旧erpID=0。
- [H008校样](assets/phase6-metadata-H008-20261018.html)、[H024校样](assets/phase6-metadata-H024-20261018.html)、[R121校样](assets/phase6-metadata-R121-20261018.html)；[采购浏览器保存](assets/phase6-metadata-browser-cook-20261018.json)及[数据库只读核验](assets/phase6-metadata-cook-result-20261018.json)。
- 应用内校样操作返回正确范围、行数、页数和HTML，但本次内嵌iframe纸张未绘制；同一HTML在本机独立浏览器页面已显示并核对书签和版式，三份截图存档。**内嵌显示不能判定通过**，未改变sandbox权限。窄列原代码/多个候选可能裁切，原12.2同值样张、区域字体及纸张仍待对照。
- 新增36行合成数据均在独立浏览器验证库；本轮历史业务导入0。单元测试在独立测试库事务回滚。旧SQL Server仅SELECT读取字段、配置、定义，没有调用业务过程。
- 开发验证、全量历史对账、现场验收分别登记；打印未向真实设备发送，也未登记成功回执。

## 剩余开发顺序

1. 继续现有235条事件接线逐绑定验证保存、审核、转单和逆向时机；9条缺口保留：3外部回执、2缺原表、2缺目标字段、2不完整过滤。
2. 处理130份非财务打印的未移植脚本、动态高度、多列、子报表及显示来源；以133份固定来源清单逐项推进。67份缺事件定义要补相应客户端来源；68份缺明确入口、29份缺XML继续登记。28份可校样仍需原样张对照，应用内嵌显示待排查。
3. 5条保存来源按明确公式、最新字段及主从关系补足；现有原值录入和待补来源留痕保持，不猜来源、不丢异常或重复行。
4. 统一抽取时点后逐单逐行历史对账，计划、实称、收发分别核对；全量对账不能用本轮合成样本代替。
5. 现场岗位流转、纸张裁切、字体、条码扫描及设备回执验收。原35查询、财务仍暂缓。

## 固定编号逐项结果

编号未删减或重排；历史全量对账与现场验收均未完成。
'''
    for group,rows in review['groups'].items():
        text+='\n### 第'+group+'组\n\n|编号|入口/报表|字段/事件|当前状态与差异|\n|---|---|---|---|\n'
        for row in rows:
            reasons=[r['reason'] for r in row.get('results',[]) if r['state'] in ['explicit_difference','explicit_manual_input','query_projection_only']]+row.get('issues',[])
            if group=='5':reasons.insert(0,row['scope'])
            text+='|'+'|'.join(cell(v) for v in [row['id'],row.get('entry',row.get('report',row.get('name',''))),row.get('field',row.get('event',row.get('title',''))),row['state']+('；'+'；'.join(reasons) if reasons else '')])+'|\n'
    (DOCS/TITLE).write_text(text,encoding='utf8')
    current=f'''## 当前有效第六阶段清单（133份来源复查及保存事件续验）

以[{TITLE}]({TITLE})和[{EVIDENCE}]({EVIDENCE})为准。933固定编号、原35查询及财务暂停范围不变；第六阶段整体部分完成。

本轮133份打印逐份复查；新增H008/H024/R121三份可校样，当前28份具备条件、130份非财务差异，另68缺入口/29缺XML。R101/R101-1单位事件已承接，缺父ColorID_R来源；67份原事件定义缺失逐份保留。采购CookIn实际保存及重复来源留痕通过。5条保存来源经2026-10-18只读复核仍无新依据；235事件接线需继续逐绑定验证，9缺口、28财务配置不变。

464项回归、18项最终复验（17重叠1新增），前端及模型检查通过。三份独立HTML浏览器版式已验证，应用内嵌纸张未绘制，明确保留显示差异。额外旧erpID=0，历史导入0；全量历史对账、现场验收均未完成。'''
    for name in ['2026-10-16染色ERP剩余工作全量盘点清单.md','染色ERP后续开发方案.md']:section(DOCS/name,'phase6-form-flows-current',current)
    reasons={
        'E248':('书签、标签及空分组原版式','部分完成','H008/H024三页校样和书签跳页通过；Tag只作附加数据，不覆盖正文。空字段组头覆盖整份所选数据，R011剩余5处来源差异不关闭。当前28可校样/130非财务差异，非完整纸张验收。'),
        'E249':('CookIn原跨表保存来源及无序多来源更新','部分完成','保留原ArticleIn/ArticleInDetail→p_Article规则；不以CookInDetail代替。2头×3行全部6候选及3材料更新验证。原UPDATE无序，承接末项选择明确留痕，NULL/负数/已有价格不清洗。全量历史取值未对账。'),
        'E250':('133份原脚本来源、文字事件及内嵌显示','部分完成','133份XML/C#均复查，90份有事件，67份存在缺定义事件（排除注释字符串），49份有脚本文本。R121文字事件已承接；R101/R101-1单位事件已实现但父ColorID_R未证明。内嵌校样纸张未绘制，独立同一HTML页面显示已验证，仍不将内嵌显示判定通过。')}
    exception='## 2026-10-18 133份打印来源与采购保存续验\n\n当前28份可校样、130份非财务差异；此前25/133属于历史状态。原35查询、财务继续暂停。\n\n'
    for key,(name,status,reason) in reasons.items():exception+=f'### {key} {name}\n\n{reason}\n\n'
    exception+=f'逐份未复刻内容见[133份来源复查](2026-10-18第六阶段133份非财务打印来源复查.md)，完整证据见[{TITLE}]({TITLE})。5条保存来源和9条事件缺口仍保留；历史对账、现场验收均未完成。'
    section(DOCS/'旧ERP复刻异常与合理实现说明.md','phase6-print-metadata-exceptions',exception)
    inventory=read('docs/erp-remaining-inventory-20261016.json');axis=inventory['axes']['新旧系统差异及处理情况']
    for key,(name,status,reason) in reasons.items():
        value={'id':key,'name':name,'status':status,'reason':reason,'related_sql':[],'source':'docs/旧ERP复刻异常与合理实现说明.md'}
        index=next((i for i,r in enumerate(axis) if r['id']==key),None)
        if index is None:axis.append(value)
        else:axis[index]=value
    inventory['counts']['新旧系统差异及处理情况']=dict(Counter(r['status'] for r in axis))
    summary={'document':TITLE,'evidence':EVIDENCE,'fixed_counts':review['counts'],'state_counts':review['state_counts'],'development':'本轮增量已验证；内嵌显示仍有差异，第六阶段整体部分完成','historical_reconciliation':'未完成','field_acceptance':'未完成','tests':tests}
    inventory['phase6_six_groups_20261017']=summary
    inventory['phase6_review'].update(current_evidence='docs/'+EVIDENCE,next='235事件逐绑定及9缺口；130非财务打印差异与内嵌显示；5保存来源；全量对账及现场。原35查询和财务继续暂缓。')
    for row in inventory['axes']['旧界面配置入口']:
        if row['name'] in ['CookIn','ProdOutDetailSum','GrayInWaste','TrialDyeRecipePhaseDetail']:
            row['phase6_print_metadata_20261018']={'evidence':EVIDENCE,'development':'所列增量验证，整入口不升级完成','historical_reconciliation':'未完成','field_acceptance':'未完成'}
    save('docs/erp-remaining-inventory-20261016.json',inventory)
    old_review=read('docs/erp-phase6-review-20261016.json');old_review.update(six_groups_20261017=summary,current_review_at=evidence['verified_at']);save('docs/erp-phase6-review-20261016.json',old_review)
    print({'print_eligible':28,'nonfinance_differences':130,'exceptions':len(axis),'tests':tests,'fixed_counts':review['counts']})


if __name__=='__main__':main()
