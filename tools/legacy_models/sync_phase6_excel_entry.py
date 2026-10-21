"""登记Excel业务录入验证，保留固定清单和历史/现场验收边界。"""
from collections import Counter
from datetime import datetime
from sync_phase6_six_groups_continued import ROOT,DOCS,read,save,digest,section,test_result,cell

TITLE='2026-10-18Excel导入与手工录入验证清单.md'
EVIDENCE='erp-excel-entry-verification-20261018.json'


def main():
    baseline=read('docs/erp-phase6-six-groups-baseline-20261017.json')
    review=read('docs/erp-phase6-six-groups-review-20261017.json')
    assert review['paused_queries']==baseline['paused_queries']
    for group,rows in baseline['groups'].items():
        assert [r['id'] for r in rows]==[r['id'] for r in review['groups'][group]]
    tests={'regression':test_result('excel-regression-final.log'),'final_targeted':test_result('excel-target-final.log'),
           'note':'90项相关回归；最终17项专项中16项重叠、1项新增，共91项不同用例，不能相加为107项。'}
    assert tests['regression']['count']==90 and tests['final_targeted']['count']==17
    schema=read('.runtime-temp/phase6/continued-schema.json')
    assert not schema['extra_legacy_id_fields']
    browser=read('docs/assets/phase6-excel-browser-20261018.json')
    assert len(browser)==5
    db=read('docs/assets/phase6-excel-database-20261018.json')
    files=['backend/system/excel.py','backend/system/excel_fields.py','backend/system/tests/test_excel.py',
        'backend/plugins/erp_base/source_excel.py','backend/plugins/erp_base/source_api.py',
        'backend/plugins/erp_base/tests/test_source_excel_entry.py',
        'web/src/components/ExcelImport.vue','web/src/components/ResourceTable.vue']
    now=datetime.now().astimezone().isoformat()
    evidence={'verified_at':now,'document':TITLE,'development':'本次Excel录入通路及所列样本验证通过；非全业务完成',
        'historical_reconciliation':'未完成','field_acceptance':'未完成','historical_import_rows_this_run':0,
        'sql_server_access_this_run':'未连接或查询；验证使用独立PostgreSQL测试库和浏览器验证库',
        'synthetic_source_rows_added':14,'tests':tests,'schema':schema,'browser_cases':browser,'database_result':db,
        'baseline_sha256':digest('docs/erp-phase6-six-groups-baseline-20261017.json'),
        'fixed_ids_preserved':True,'paused_queries_unchanged':True,'printing_paused':True,'finance_paused':True,
        'frontend':{'typecheck':'通过','build':'通过','build_warning':'既有分包体积提示',
            'typecheck_log_sha256':digest('.runtime-temp/phase6/excel-typecheck.log'),
            'build_log_sha256':digest('.runtime-temp/phase6/excel-build.log')},
        'code_sha256':{p:digest(p) for p in files},
        'previous_evidence':'erp-phase6-print-metadata-verification-20261018.json'}
    save('docs/'+EVIDENCE,evidence)
    review['updated_at']=now
    review['excel_import_20261018']={'evidence':EVIDENCE,'document':TITLE,'development':evidence['development'],
        'historical_reconciliation':'未完成','field_acceptance':'未完成'}
    review['printing_paused']={'since':'2026-10-18','reason':'用户要求优先基础资料导入、业务录入和实际流程',
        'scope':'全部打印开发和验收；保留28份可校样、130份非财务差异及其余缺入口/缺XML记录'}
    states=['Excel相关90项回归、17项最终专项通过（16重叠1新增）；此前验证证据保留',
        'Excel浏览器新增3资料/3单据、3次更新及2类整批回滚通过；打印暂缓',
        '766模型/655原表/12606原字段，额外旧erpID=0；类型检查、构建、模型及迁移检查通过',
        '本轮历史导入0；全量历史对账与现场验收未完成']
    for row,state in zip(review['groups']['6'],states):row['state']=state
    review['state_counts']={g:dict(Counter(r['state'] for r in rows)) for g,rows in review['groups'].items()}
    save('docs/erp-phase6-six-groups-review-20261017.json',review)
    current=f'''## 当前执行范围：基础资料导入、业务录入与流程验证（2026-10-18）

**全部打印、原35项查询和财务继续暂缓。** 本轮优先项见[{TITLE}]({TITLE})，证据见[{EVIDENCE}]({EVIDENCE})。本节覆盖下方历史记录中的开发优先级；原打印数量和证据保留，不视作完成。

Excel导入已接入原业务入口、自动编号及现有保存service；新增模板携带入口，同表不同业务可逐行指定。空白/#KEEP与#NULL/#EMPTY分开，重复行逐行处理，同一更新主键可连续更新；无缓存公式和业务错误明确报行、整批回滚。通过90项回归和17项最终专项（16项重叠、1项新增），浏览器验证3条基础资料、3条业务单据、3次更新及2类整批回滚。766模型/655原表/12606原字段不变，额外旧erpID为0。

后续顺序：先录入组织、单位、仓库、客户/供应商、物料、工序和机台等基础资料并核对关联；再按实际业务先主单后明细录入，逐单验证保存、审核、转单、收发及撤销；发现原来源缺口继续登记并补齐。现有5条保存来源差异、9条事件缺口和235条事件接线的逐绑定验证继续保留，未因Excel通路通过而关闭。933个固定编号不变，不把跨组统计相加。

本轮使用独立库合成数据，历史导入0；全量历史对账和现场验收均未完成。旧业务的客户编码禁止修改等规则仍执行，错误不吞掉、异常和重复行不跳过。'''
    for name in ['2026-10-16染色ERP剩余工作全量盘点清单.md','染色ERP后续开发方案.md']:
        section(DOCS/name,'phase6-form-flows-current',current)
    six=DOCS/'2026-10-17第六阶段六组续验与剩余清单.md'
    text=six.read_text(encoding='utf8')
    lines=text.splitlines()
    for index,line in enumerate(lines):
        if line.startswith('|6 综合验证|'):
            lines[index]='|6 综合验证|4|Excel相关90项回归、17项最终专项（16重叠1新增）；3资料/3单据/3次更新及两类失败回滚浏览器验证；前轮证据保留|未完成|未完成|'
        for row in review['groups']['6']:
            if line.startswith('|'+row['id']+'|'):
                lines[index]='|'+'|'.join(cell(v) for v in [row['id'],row.get('name',''),row.get('title',''),row['state']])+'|'
    text='\n'.join(lines)+'\n'
    six.write_text(text,encoding='utf8')
    start='<!-- phase6-excel-priority -->';end='<!-- /phase6-excel-priority -->'
    if start not in text:
        title,body=text.split('\n',1)
        six.write_text(title+'\n\n'+start+'\n'+current+'\n'+end+'\n'+body,encoding='utf8')
    else:section(six,'phase6-excel-priority',current)
    # 原打印轮次的开发事实保留，只替换目前已失效的优先级段落。
    text=six.read_text(encoding='utf8')
    begin=text.index('## 剩余开发顺序');finish=text.index('## 固定编号逐项结果',begin)
    text=text[:begin]+'''## 剩余开发顺序

1. 基础资料按关联顺序录入；本轮Excel入口、编号、保存事件和空值处理已验证，使用上方操作清单。
2. 业务主单→明细→审核→转单→收发→撤销逐单联调，继续235条事件的逐绑定验证；9条缺口仍单列。
3. 5条保存来源差异保留原值录入和来源记录，取得对应依据后补齐；不删除异常和重复数据。
4. 统一时点开展历史逐单逐行对账，再进行岗位现场验收，两个状态分别登记。
5. 全部打印、原35项查询、财务按用户要求暂缓；原28可校样/130非财务差异及缺入口/缺XML清单保留。

'''+text[finish:]
    six.write_text(text,encoding='utf8')
    reasons={
        'E251':('Excel业务入口与新业务/历史承接边界','本轮开发验证通过','Excel新增接入既有入口、编号和保存service；更新保留已有入口。带历史来源的记录不因导入窗口补造新入口。此功能用于业务录入/修改，不能将旧历史原样导入误当作重新发生一次业务。历史批量承接及全量对账状态不变。'),
        'E252':('Excel空值、重复行和公式结果','本轮开发验证通过','空白/#KEEP为未提交；#NULL为空值，#EMPTY为空文本/空多选，#TEXT:转义保留字。0、负数、前导零和空格文本保留；整行物理空白单独计数，同主键更新逐行执行。不允许NULL的字段报错，缺缓存公式报错，有内容无标题列报错，均整批回滚，不静默补0或跳行。'),
        'E253':('Excel保存事件及旧客户编码修改规则','本轮开发验证通过','浏览器实测CustKindID=0的客户修改CustomerID被原p_Customer_UPDATE拒绝，整批回滚；保留该原规则，允许的名称/备注/空值更新通过。CookIn保存沿用ArticleIn来源，2头×3明细的6候选完整留痕，3条同码材料全部处理。原无序取值替代仍见E249，不宣称全量历史等价。')}
    exception='## 2026-10-18 Excel录入、空值与保存规则\n\n打印、原35项查询和财务暂缓；下列为本轮明确处理规则，并非新增旧系统字段。\n\n'
    for key,(name,status,reason) in reasons.items():exception+=f'### {key} {name}\n\n{reason}\n\n'
    exception+=f'操作和证据见[{TITLE}]({TITLE})。5条保存来源、9条事件缺口及历史异常清单完整保留；全量历史对账、现场验收未完成。'
    section(DOCS/'旧ERP复刻异常与合理实现说明.md','phase6-excel-entry-exceptions',exception)
    inventory=read('docs/erp-remaining-inventory-20261016.json');axis=inventory['axes']['新旧系统差异及处理情况']
    for key,(name,status,reason) in reasons.items():
        item={'id':key,'name':name,'status':'已完成','reason':reason,'related_sql':[],
            'source':'docs/旧ERP复刻异常与合理实现说明.md','development':status,'historical_reconciliation':'未完成','field_acceptance':'未完成'}
        index=next((i for i,r in enumerate(axis) if r['id']==key),None)
        if index is None:axis.append(item)
        else:axis[index]=item
    inventory['counts']['新旧系统差异及处理情况']=dict(Counter(r['status'] for r in axis))
    summary={'document':TITLE,'evidence':EVIDENCE,'fixed_counts':review['counts'],'state_counts':review['state_counts'],
        'development':evidence['development'],'historical_reconciliation':'未完成','field_acceptance':'未完成','tests':tests,'printing_paused':True}
    inventory['phase6_six_groups_20261017']=summary
    inventory['phase6_review'].update(current_evidence='docs/'+EVIDENCE,next='基础资料录入及关联→业务单据主从录入→保存审核转单收发撤销逐单验证→历史对账→现场验收。5来源/9事件缺口保留；全部打印、原35查询、财务暂缓。')
    inventory['excel_import_20261018']=review['excel_import_20261018']
    save('docs/erp-remaining-inventory-20261016.json',inventory)
    old=read('docs/erp-phase6-review-20261016.json');old.update(six_groups_20261017=summary,current_review_at=now,printing_paused=True)
    save('docs/erp-phase6-review-20261016.json',old)
    print({'fixed_counts':review['counts'],'tests':tests,'exceptions_added':list(reasons),'historical_import_rows':0})


if __name__=='__main__':main()
