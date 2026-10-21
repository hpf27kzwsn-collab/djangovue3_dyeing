"""在P6查询/字段/测试核验后同步当前清单；不改写P1～P5历史结论。"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DOCS=ROOT/'docs'


def read(name):return json.loads((DOCS/name).read_text(encoding='utf8'))
def write(name,value):(DOCS/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')


def main():
    inventory=read('erp-remaining-inventory-20261016.json')
    review=read('erp-phase6-review-20261016.json')
    verified=read('erp-phase6-verification-20261016.json')
    added=read('erp-phase6-added-source-models-20261016.json')
    assert (verified['erp_models'],verified['source_models'],verified['original_fields'])==(766,655,12606)
    assert verified['tests']['failed']==0 and verified['tests']['passed']>=960
    rules=json.loads((ROOT/'backend/plugins/erp_base/source_entry_rules.json').read_text(encoding='utf8'))['models']
    inventory.update(source_models=verified['source_models'],source_fields=verified['original_fields'],
        entry_models=len(rules),entry_bindings=sum(map(len,rules.values())),
        distinct_bound_entries=len({name for value in rules.values() for name in value}))
    sources={'dye.'+r['table']:r for r in added['tables']}
    for row in inventory['axes']['原物理表表示']:
        if row['name'] not in sources:continue
        row.update(status='已完成',original_handling='business_model',phase=6,
            reason=f"原字段表示已完成：{row['fields']}列、原键及重复物理行保留；已验证完整迁移。原平台行为、历史数据采用及现场另计。",
            code=['backend/plugins/erp_base/source_models.py','backend/plugins/erp_base/migrations/0032_phase6_original_platform_sources.py',
                  'backend/plugins/erp_base/migrations/0033_phase6_remaining_platform_sources.py','backend/plugins/erp_base/migrations/0034_phase6_distinct_original_table_name.py'])
    inventory['counts']['原物理表表示']=dict(Counter(r['status'] for r in inventory['axes']['原物理表表示']))
    exceptions=inventory['axes']['新旧系统差异及处理情况']
    for number,title in [(154,'原平台表的缺口及字段承接'),(155,'第六阶段独立财务查询分类修正'),(156,'横向打印和考勤临时表的明确移植'),(157,'同名字段的取数来源及工艺审核订单号')]:
        if not any(r['id']=='E'+str(number) for r in exceptions):
            exceptions.append({'id':'E'+str(number),'name':title,'status':'部分完成','reason':'明确实现与范围已列明，历史结果及现场仍分别跟踪。','related_sql':[],
                'source':'docs/旧ERP复刻异常与合理实现说明.md'})
    inventory['counts']['新旧系统差异及处理情况']=dict(Counter(r['status'] for r in exceptions))
    write('erp-remaining-inventory-20261016.json',inventory)
    counts=review['counts']['development'];queries=review['counts']['query_execution']
    executed=queries['executed_empty_fixture'];unresolved=queries['unresolved'];finance=queries['finance']
    partial=counts.get('部分完成',0);missing=counts.get('未实现',0);external=counts.get('缺外部资料',0)
    progress=f'1682个入口中{executed}个在隔离库可执行查询，{unresolved}个仍有错误，{finance}个财务暂缓。查询执行只验证这一层，不能代替整入口非空数据、自动调用和版式验证。'
    states=f'按整入口标准：开发完成0、部分完成{partial}、未实现{missing}、缺外部资料{external}、财务暂缓{finance}；总数1682。所有异常、重复及不常用入口仍列在清单，没有缩小分母。本轮新增历史导入0、整入口完整历史结果对账完成0、现场验收确认0。'
    models='当前766个ERP模型、655个原表模型、12606个原字段。63个新增原平台模型承接533个原字段；690张原表中655张非财务原表均有字段表示，35张独立财务暂缓。0032～0034迁移随完整迁移链在全新隔离库通过；未部署或导入到开发历史库，额外旧erpID为0。部署到实际开发库时先按项目数据库配置应用迁移，再执行init_data更新新菜单及操作权限；历史导入另行按批次实施。'
    validation=f"验证：{verified['tests']['passed']}项七模块回归及{verified['phase6_final_tests']['passed']}项最终专项通过（集合重叠），前端类型检查与构建通过，全部原字段/原键及动作权限审计通过。完整验证依据见[核验JSON](erp-phase6-verification-20261016.json)。"
    final_date=verified['finalized_at'].split('T')[0]
    scope='本轮实现完整旧入口工作台、原投影查询及CSV导出、字段规则展示、公式试算/采用、部分保存审核联动、数据版打印和全部非财务原表字段承接。'
    nxt=f'继续顺序：①逐项处理{unresolved}条查询差异；②补齐编辑目标、资料选择回填、默认/复制行/登录员工来源与公式自动时点；③完成216处有效钩子的逐入口行为和时点验证；④移植原模板版式、脚本及真实功能绑定。290条打印配置全部保留，数据版不冒充旧版式。详见E146～E157。'
    p=DOCS/'2026-10-16染色ERP剩余工作全量盘点清单.md';s=p.read_text(encoding='utf8')
    start=s.index('本轮实现完整旧入口工作台');end=s.index('更新日期：',start)
    s=s[:start]+'\n\n'.join([scope+progress,states,models+' 异常及合理处理新增E146～E157。P1～P5按单个SQL对象的结论与P6整入口结论分列。',validation])+'\n\n'+s[end:]
    s=re.sub(r'\| 旧界面入口（整入口标准） \|[^\n]+',f'| 旧界面入口（整入口标准） | 0 | {partial} | {missing} | {external} | {finance} | 1682 |',s)
    s=re.sub(r'\| 原物理表表示 \|[^\n]+','| 原物理表表示 | 655 | 0 | 0 | 0 | 35 | 690 |',s)
    s=s.replace('新旧差异153项','新旧差异157项').replace('附录E：153项','附录E：157项').replace('P6新增E146～E153','P6新增E146～E157')
    s=s.replace('当前703个ERP模型、592个原表模型、12,073个原字段','第五阶段核验时703个ERP模型、592个原表模型、12,073个原字段')
    s=re.sub(r'^更新日期：\d{4}-\d{2}-\d{2}。','更新日期：'+final_date+'。',s,flags=re.M)
    s=re.sub(r'\| P6继续 \|[^\n]+',f'| P6继续 | 处理{unresolved}项查询差异，补资料选择回填、默认/公式实际时机及有效钩子验证，移植原打印版式和脚本 | {executed}项可执行查询仍需必要非空验证；整入口状态未升级为全部开发完成 |',s)
    ui={r['id']:r for r in review['entries']};physical={r['id']:r for r in inventory['axes']['原物理表表示']}
    lines=[]
    for line in s.splitlines():
        cells=line.split('|');key=cells[1].strip() if len(cells)>2 else ''
        if key in ui:
            row=ui[key];cells[4]=' '+row['development']['status']+' '
            label={'executed_empty_fixture':'原查询隔离库可执行','unresolved':'原查询仍有差异','finance':'财务暂缓'}[row['query']['state']]
            cells[6]=' '+('、'.join(row['models']) or '尚无原入口绑定')+'；'+label+' ';line='|'.join(cells)
        elif key in physical:
            row=physical[key];cells[4]=' '+row['status']+' ';cells[6]=' '+row['reason']+' ';line='|'.join(cells)
        elif re.fullmatch(r'E\d+',key) and len(cells)==6:
            cells.insert(4,' — ');line='|'.join(cells)
        lines.append(line)
    s='\n'.join(lines)+'\n'
    for row in exceptions[-4:]:
        if '| '+row['id']+' |' not in s:s+=f"| {row['id']} | {row['name']} | 部分完成 | — | [异常说明](旧ERP复刻异常与合理实现说明.md)同编号 |\n"
    p.write_text(s,encoding='utf8')
    p=DOCS/'染色ERP后续开发方案.md';s=p.read_text(encoding='utf8');section=s.index('## 2026-10-16第六阶段本轮核查后的当前执行依据');start=s.index('\n\n',s.index('以[第六阶段逐入口清单]',section))+2;end=s.index('\n## ',start)
    s=s[:start]+'\n\n'.join([scope+progress,states,models,validation,nxt,'以下各批次的模型数量和测试数量保留当时记录；当前数量及下一步以本节和第六阶段清单为准。'])+'\n'+s[end:]
    s=re.sub(r'^修订日期：\d{4}-\d{2}-\d{2}。','修订日期：'+final_date+'。',s,flags=re.M);p.write_text(s,encoding='utf8')
    p=DOCS/'旧ERP复刻异常与合理实现说明.md';s=p.read_text(encoding='utf8')
    start=s.index('\n\n',s.index('## E147 '))+2;end=s.index('\n\n',start)
    breakdown='、'.join(f'{k}{v}项' for k,v in review['query_difference_counts'].items())
    s=s[:start]+f'{unresolved}项执行差异的入口名称、分类和原始错误见[第六阶段异常明细](2026-10-16第六阶段未复刻入口与打印异常明细.md)。其中{breakdown}；这是查询错误分类，与整入口开发状态的“缺外部资料”不是同一统计口径。'+s[end:]
    s=s.replace('多个SQL语句或临时表而未执行成功的入口','其他未执行成功的入口');p.write_text(s,encoding='utf8')
    p=DOCS/'2026-10-16第六阶段旧入口自动调用与打印核查清单.md';s=p.read_text(encoding='utf8');start=s.index('## 逐入口状态')
    # 逐入口清单由review_phase6生成；再次同步仅替换当前验证段。
    if '当前766个ERP模型' in s[:start]:s=s[:s.index('当前766个ERP模型')]+s[start:]
    s=s.replace('## 逐入口状态',models+'\n\n'+validation+' 本轮最终核验日期：'+final_date+'。\n\n## 逐入口状态');p.write_text(s,encoding='utf8')
    print(json.dumps({'physical':inventory['counts']['原物理表表示'],'queries':queries,'development':counts},ensure_ascii=False))


if __name__=='__main__':main()
