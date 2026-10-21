"""送货单原版式与质量保存时机增量核验；固定编号、暂停范围与历史证据保持。"""
from sync_phase6_six_groups_continued import read,save,digest,section,test_result,cell,ROOT,DOCS
from collections import Counter
from datetime import datetime
import re

TITLE='2026-10-17第六阶段六组续验与剩余清单.md'
EVIDENCE='erp-phase6-delivery-quality-verification-20261018.json'

def main():
    baseline=read('docs/erp-phase6-six-groups-baseline-20261017.json')
    review=read('docs/erp-phase6-six-groups-review-20261017.json')
    previous=read('.runtime-temp/phase6/delivery-prior-review.json')
    assert review['paused_queries']==baseline['paused_queries']
    for group,rows in review['groups'].items():
        assert [r['id'] for r in rows]==[r['id'] for r in baseline['groups'][group]]
        old={r['id']:r for r in previous['groups'][group]}
        for row in rows:
            for key in ['verification','browser_verification']:
                if key in old[row['id']]:row[key]=old[row['id']][key]
    tests={'regression':test_result('delivery-regression.log'),'targeted':test_result('delivery-target-final.log'),
           'note':'454项相关回归通过；浏览器发现日期问题后修复，再通过29项针对性复验。29项包含在454项内，不相加。'}
    assert tests['regression']['count']==454 and tests['targeted']['count']==29
    browser=read('docs/assets/phase6-delivery-browser-print-20261018.json')
    proofs=[]
    for item in browser:
        code=item['report'];path=f'docs/assets/phase6-delivery-{code}-20261018.html';html=(ROOT/path).read_text(encoding='utf8')
        rows,pages=map(int,re.search(r'(\d+) 行，(\d+) 页',item['text']).groups())
        assert rows==37 and html.count('<section class="page">')==pages
        proofs.append({'report':code,'rows':rows,'pages':pages,'query_rows':40,'scope':'DELIVERY-S','html':path,'sha256':digest(path)})
    assert {p['report'] for p in proofs}=={'H015','H017','H018','H025','H029'}
    for row in review['groups']['5']:
        proof=next((p for p in proofs if p['report']==row['report']),None)
        if proof:row['browser_verification']=proof
    for row in review['groups']['4']:
        if row.get('entry') in ['QC_Record','QFQC_Record'] and row.get('event')=='AfterSaveSQL':
            row['verification']='2026-10-18：质量汇总后回写工卡；重复条码跨卡、子行修改和删除、NULL与负数回归通过。QC_Record浏览器保存后包装Dots=0、工卡PDots=0。dots→PDots字段差异仍保留，不能视为完整原脚本复刻。'
    states=['454项相关回归与29项最终针对性复验通过（重叠）','新增5份非空跨页送货单校样与质量保存回写浏览器验证；之前逐入口证据保留',
            '766模型/655原表/12606原字段；额外旧erpID为0；前端类型检查与构建通过','全量历史对账未完成，现场验收未完成；本轮历史导入0']
    for row,state in zip(review['groups']['6'],states):row['state']=state
    review['updated_at']=datetime.now().astimezone().isoformat()
    review['state_counts']={g:dict(Counter(r['state'] for r in rows)) for g,rows in review['groups'].items()}
    eligible=[r for r in review['groups']['5'] if not r['issues']]
    differences=[r for r in review['groups']['5'] if r['scope']=='非财务入口' and r['issues']]
    assert len(eligible)==25 and len(differences)==133
    gaps=[r for g in ['1','2'] for r in review['groups'][g] if any(v['state']=='explicit_difference' for v in r['results'])]
    assert len(gaps)==5
    save('docs/erp-phase6-six-groups-review-20261017.json',review)
    files=['backend/plugins/erp_base/'+name for name in ['source_phase6_print_groups.py','source_phase6_rendering.py','source_phase6_print_sources.py','source_phase6_entries.py','source_packaging_flow.py','source_services.py','source_phase6_hook_manifest.json','tests/test_source_phase6_delivery_print.py']]+['web/src/plugins/erp/OriginalEntryWorkbench.vue']
    schema=read('.runtime-temp/phase6/continued-schema.json');assert not schema['extra_legacy_id_fields']
    evidence={'verified_at':review['updated_at'],'baseline_sha256':digest('docs/erp-phase6-six-groups-baseline-20261017.json'),'fixed_ids_preserved':True,
        'fixed_counts':review['counts'],'paused_queries_unchanged':True,'save_differences':[r['id'] for r in gaps],
        'print_eligible':25,'nonfinance_print_differences':133,'tests':tests,'schema':schema,'browser_prints':proofs,
        'browser_quality':read('docs/assets/phase6-delivery-browser-quality-20261018.json'),
        'frontend':{'typecheck':'通过','build':'通过','build_log_sha256':digest('.runtime-temp/phase6/delivery-build.log')},
        'synthetic_browser_rows_added':47,'historical_import_rows_this_run':0,'historical_reconciliation':'未完成','field_acceptance':'未完成',
        'code_sha256':{p:digest(p) for p in files},'previous_evidence':'erp-phase6-parent-save-print-verification-20261017.json',
        'screenshot':{'file':'docs/assets/phase6-delivery-quality-20261018.png','sha256':digest('docs/assets/phase6-delivery-quality-20261018.png')},
        'print_rule_source':'https://docs.devexpress.com/XtraReports/2587/feature-guide-to-devexpress-reports/introduction-to-banded-reports'}
    save('docs/'+EVIDENCE,evidence)
    old_text=(DOCS/TITLE).read_text(encoding='utf8')
    source_section=old_text.split('## 5条保存来源差异的最新核验')[1].split('## 本次完成的增量开发与验证')[0].replace('本次补的是保存保留与审计','前轮已补保存保留与审计')
    text=f'''# 第六阶段六组续验与剩余清单

更新日期：2026-10-18（送货单无组头组尾、日期及质量保存事件时机续验）。固定933个编号全部保留；六组存在交叉，不能相加为独立功能数。**第六阶段整体仍为部分完成。** 原35项查询与财务继续暂缓，不新增额外旧erpID。

## 当前数量与完成标准

|组|固定数量|开发核验现状|历史全量对账|现场验收|
|---|---:|---|---|---|
|1 本行/保存字段|116|111条编译保存、3条人工原字段、2条来源差异|未完成|未完成|
|2 父子/专用来源|156|123条编译保存、29条已有专用服务、1条仅查询投影、3条来源差异|未完成|未完成|
|3 查询试算|95|85条非财务公式；35个入口原有非空浏览器证据保留，84条样本通过，ReworkBathRatio含5行缺父来源；10条财务暂缓|未完成|未完成|
|4 自动事件/转单|272|235条接线或明确替代、9条明确缺口、28条财务配置暂缓；本轮补QC/QFQC保存时机，不将接线数量称为逐绑定验证完成|未完成|未完成|
|5 原打印|290|25份具备静态填数条件，236份运行/来源差异，29份无XML；完整原样张验收为0|未完成|未完成|
|6 综合验证|4|454项相关回归、29项最终针对性复验（重叠）；5份跨页浏览器校样及1组质量保存回写验证；类型检查与构建通过|未完成|未完成|

打印范围：158份非财务＝25份具备校样条件＋133份仍有差异；另35份财务暂缓、68份缺明确入口、29份缺XML。前轮20/138更新为25/133，不能说25份已经完整复刻。

## 5条保存来源差异的最新核验
{source_section}
## 本次完成的增量开发与验证

1. **质量保存时机**：原QC_Record、QFQC_Record的AfterSaveSQL应在本次包装/疵点保存汇总后执行。之前在包装单行写入时先回写工卡，可能采用旧Dots；子疵点单独保存后也未同步工卡。现在由service层在来源公式、明细汇总完成后回写。验证重复条码涉及多张工卡、重复包装、负数、NULL、疵点修改和明确删除后的结果。没有给QFQC添加原本不存在的QC子表公式。
2. **质量浏览器**：合成包装DELIVERY-QC原扣分99，三条同疵点号明细5/-2/-3；在页面仅修改备注保存，包装Dots变0，工卡PDots变0、Pkg=10、PRolls=1、PlengthQyt=-2。原脚本写JobSheet.dots而最新原表没有该列，仍保留此前明确的PDots对应差异；未添加猜测字段。
3. **无组头组尾**：H015/H017/H018/H025/H029没有分组头，组尾按整份本次所选单据确定汇总范围，Level从内向外；原Level 0组尾标记RepeatEveryPage，逐页输出页小计及签收栏，Level 1总计仅在最后输出一次；原XML未改。依据[DevExpress带区说明](https://docs.devexpress.com/XtraReports/2587/feature-guide-to-devexpress-reports/introduction-to-banded-reports)中“无分组时组头/尾覆盖整份报表”的规则。混合有组头却缺同级组头的情况仍报明差异，不套入整单规则。旧12.2实际纸张行为还需原样张对照。
4. **五种送货单范围与分页**：按SheetSeries明确选择父单，NULL与空串可分别选用。两种原查询各40行，所选DELIVERY-S保留37个原查询分组，重复原明细按原GROUP BY进入合计，不删除或去重原行。H015为6页，其余4份均2页；总件数36、原本带总重量的模板为45.00。LB版原模板只有总件数，没有总重量，不补造公斤合计，也不把原标注Lb自行折算。
5. **原日期标签**：浏览器因已有非空日期暴露ProdOut.RQ把英文月份October转整数的错误。仅此入口明确改用DATEPART(MONTH,SheetDate)，输出原意的中文数字日期；原目录SQL保留。测试非空日期2026-10-18、原重复明细、空值与负数，通过后浏览器重试5份校样成功。原DATENAME的语言依赖记录为合理实现差异，不声称所有语言环境逐字等价。

## 验证证据与界限

- [本轮验证汇总]({EVIDENCE})；[固定933项状态](erp-phase6-six-groups-review-20261017.json)；[前轮父子保存与打印证据](erp-phase6-parent-save-print-verification-20261017.json)。
- 浏览器原HTML：[H015](assets/phase6-delivery-H015-20261018.html)、[H017](assets/phase6-delivery-H017-20261018.html)、[H018](assets/phase6-delivery-H018-20261018.html)、[H025](assets/phase6-delivery-H025-20261018.html)、[H029](assets/phase6-delivery-H029-20261018.html)；[打印范围/页数](assets/phase6-delivery-browser-print-20261018.json)；[质量保存后页面证据](assets/phase6-delivery-browser-quality-20261018.json)。
- 454项回归与29项最终复验有重叠，不相加。前端类型检查与构建通过。766个ERP模型、655个原表模型、12606个原字段；额外旧erpID为0，无迁移改动。
- 本轮在独立浏览器验证库新增47行合成数据；没有历史业务导入。单元测试在独立测试库事务回滚。打印首次截图失败，质量结果页面截图已成功存档；原HTML与可见页面读数也已保留，未完成原样张像素对比。
- 本轮未重新抽取旧数据库字段，5条来源沿用2026-10-17晚的只读证据。开发验证、全量历史对账、现场纸张及设备验收分开；没有向打印机发送或登记成功回执。

## 剩余开发顺序

1. 5条保存来源仍缺完整公式、表或主从对应；原值录入、异常和重复行保留及来源待补留痕保持。无法从现有资料确定时，按异常说明保留，不能虚报关闭。
2. 继续235条接线的逐绑定时机及转单/撤销核验；9条缺口仍为3条外部调用回执、2条缺原表、2条最新原表缺目标字段、2条不完整过滤。QC/QFQC本轮验证不代表235条全部完成。
3. 133份非财务复杂打印仍有脚本、动态高度、多列、子报表及显示来源差异；68份缺明确入口、29份缺XML继续登记。25份可校样版式仍需原12.2样张及实际纸张对照。
4. 全量历史对账：按统一抽取时点逐单逐行，保留异常、重复、撤回记录；计划、实称、收发分开比对。合成样本不能替代历史对账。
5. 现场验收：实际岗位流转、纸张裁切、字体、条码扫描及设备回执。原35查询与财务继续暂缓。

## 固定编号逐项结果

编号没有删除或重排；历史全量对账与现场验收均未完成。
'''
    for group,rows in review['groups'].items():
        text+='\n### 第'+group+'组\n\n|编号|入口/报表|字段/事件|当前状态与差异|\n|---|---|---|---|\n'
        for row in rows:
            reasons=[r['reason'] for r in row.get('results',[]) if r['state'] in ['explicit_difference','explicit_manual_input','query_projection_only']]+row.get('issues',[])
            if group=='5':reasons.insert(0,row['scope'])
            text+='|'+'|'.join(cell(v) for v in [row['id'],row.get('entry',row.get('report',row.get('name',''))),row.get('field',row.get('event',row.get('title',''))),row['state']+('；'+'；'.join(reasons) if reasons else '')])+'|\n'
    (DOCS/TITLE).write_text(text,encoding='utf8')
    current=f'''## 当前有效第六阶段清单（送货单与质量保存时机续验）

以[{TITLE}]({TITLE})和[{EVIDENCE}]({EVIDENCE})为准。933固定编号、原35查询暂停范围与财务暂停范围不变；第六阶段整体部分完成。

5条保存来源差异仍在，原值及异常重复行继续保留。QC/QFQC工卡汇总已移至明细保存汇总后，QC浏览器验证完成；旧dots→PDots对应差异仍保留。新增5种送货单非空跨页校样和数字月份修复；25份具备校样条件、236份运行/来源差异、29份缺XML；非财务打印差异133份，另68份缺入口。

454项相关回归、29项最终复验（重叠），类型检查和构建通过。事件235接线仍需逐绑定核验，9缺口、28财务配置不变。额外旧erpID=0，历史导入0。全量历史对账、现场验收均未完成。'''
    for name in ['2026-10-16染色ERP剩余工作全量盘点清单.md','染色ERP后续开发方案.md']:section(DOCS/name,'phase6-form-flows-current',current)
    reasons={'E246':('QC/QFQC保存后工卡汇总时机','部分完成','质量保存回写在本次来源与明细汇总之后；子行修改/删除、重复条码跨卡、NULL与负数已验证，QC浏览器保存已验证。旧JobSheet.dots不存在，沿用PDots明确对应，完整历史对账及现场未完成。'),
             'E247':('五种送货单无组头组尾及数字月份','部分完成','H015/H017/H018/H025/H029跨页校样通过；组尾按整份所选单据汇总；原Level 0按RepeatEveryPage逐页输出、Level 1总计末页输出，原XML保留。ProdOut.RQ数字月份改用DATEPART避免英文月份转整数失败；LB原Lb标注与缺重量总计保持。25份校样不代表完整原样张验收；当前133份非财务打印差异。')}
    exception='## 2026-10-18 质量保存时机与五种送货单续验\n\n当前有效打印数量为25份具备校样条件、133份非财务差异。此前20/138是历史记录。\n\n'
    for key,(name,status,reason) in reasons.items():exception+=f'### {key} {name}\n\n{reason}\n\n'
    exception+=f'具体原来源、合理实现、浏览器及测试证据见[{TITLE}]({TITLE})。5条保存来源及9条事件缺口均未删除。'
    section(DOCS/'旧ERP复刻异常与合理实现说明.md','phase6-delivery-quality-exceptions',exception)
    inventory=read('docs/erp-remaining-inventory-20261016.json');axis=inventory['axes']['新旧系统差异及处理情况']
    for key,(name,status,reason) in reasons.items():
        value={'id':key,'name':name,'status':status,'reason':reason,'related_sql':[],'source':'docs/旧ERP复刻异常与合理实现说明.md'}
        index=next((i for i,r in enumerate(axis) if r['id']==key),None)
        if index is None:axis.append(value)
        else:axis[index]=value
    inventory['counts']['新旧系统差异及处理情况']=dict(Counter(r['status'] for r in axis))
    summary={'document':TITLE,'evidence':EVIDENCE,'fixed_counts':review['counts'],'state_counts':review['state_counts'],'development':'本轮增量验证完成，第六阶段整体部分完成','historical_reconciliation':'未完成','field_acceptance':'未完成','tests':tests}
    inventory['phase6_six_groups_20261017']=summary
    inventory['phase6_review'].update(current_evidence='docs/'+EVIDENCE,next='5条保存来源；235接线逐绑定及9缺口；133份非财务打印差异、68缺入口/29缺XML；25份校样需原样张对照。原35查询和财务继续暂缓。')
    for row in inventory['axes']['旧界面配置入口']:
        if row['name'] in ['QC_Record','QFQC_Record','ProdOut','ProdOutDetailSum','ProdOutDetailXISHU']:
            row['phase6_delivery_quality_20261018']={'evidence':EVIDENCE,'development':'所列增量验证完成，整入口不升级完成','historical_reconciliation':'未完成','field_acceptance':'未完成'}
    save('docs/erp-remaining-inventory-20261016.json',inventory)
    old=read('docs/erp-phase6-review-20261016.json');old.update(six_groups_20261017=summary,current_review_at=evidence['verified_at']);save('docs/erp-phase6-review-20261016.json',old)
    print({'tests':tests,'print_eligible':25,'nonfinance_differences':133,'exceptions':len(axis),'fixed_counts':review['counts']})

if __name__=='__main__':main()
