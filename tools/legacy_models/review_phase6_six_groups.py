"""逐固定编号更新六组结果；不移动基线、不把代码登记当作整入口完成。"""
import os,sys,json,re,hashlib,base64
from pathlib import Path
from collections import Counter
from datetime import datetime
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'backend'));os.environ.setdefault('DJANGO_SETTINGS_MODULE','application.settings')
import django
django.setup()
from plugins.erp_base import source_phase6_entries as entries
from plugins.erp_base.source_phase6_api import templates
from plugins.erp_base.source_phase6_rendering import requirements,projection_names
from plugins.erp_base.source_phase6_layouts import parse_xml
from plugins.erp_base.source_phase6_formula_runtime import tree
from plugins.erp_base.source_phase6_projection_context import CHILD,ProjectionContext
from plugins.erp_base.source_phase6_projection_overrides import expression,PRINT_PARENTS,projections
from sqlglot import exp
from sqlglot.errors import ParseError

def read(name):return json.loads((ROOT/name).read_text(encoding='utf8'))
def digest(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()

def projection(row):
    entry=row['entry'];formula,resolution=expression(entry,{'FieldName':row['field'],'Express':row['expression']});support=entries.query_support()[entry];issues=[]
    if entry.startswith('ImpairmentPayouts'):
        return {'state':'财务赔款结算暂缓','issues':['旧目录归为非财务，但此字段为赔款/核销金额链；按本期范围暂缓，原编号保留']}
    if support['query_state']=='unresolved':return {'state':'原查询暂缓或有差异','issues':[str(support.get('error'))]}
    aggregates=[]
    def replace(m):aggregates.append(m.groups());return '[_projection_child_'+str(len(aggregates)-1)+']'
    try:
        parsed=tree(CHILD.sub(replace,formula));available=projection_names(entries.tree_for(entry))
        available.update(tree(value).alias_or_name.lower() for value in projections(entry))
        available.update(f['FieldName'].lower() for f in entries.definition(entry)['fields'] if f['Express'])
        context=ProjectionContext({'entry':entry},None,{},True)
        for node in parsed.find_all(exp.Column):
            if node.name.startswith('_projection_child_'):continue
            if node.table.lower()=='parent':
                parent=PRINT_PARENTS.get(entry,entries.definition(entry)['table']['MasterDataTableName'])
                if not parent:issues.append('缺原父入口')
                else:
                    context.relation(entry,parent)
                    if node.name.lower() not in projection_names(entries.tree_for(parent)):issues.append('父投影缺字段：'+node.name)
            elif node.table:issues.append('跨入口前缀未对应：'+node.table)
            elif node.name.lower() not in available:issues.append('当前投影缺字段：'+node.name)
        for operation,relation,name in aggregates:
            prefix=entry+'_'
            if not relation.startswith(prefix):issues.append('原子关系前缀未对应：'+relation);continue
            child=relation[len(prefix):]
            context.relation(child,entry)
            if entries.query_support()[child]['query_state']=='unresolved':issues.append('子查询有差异：'+child)
            elif name.lower() not in projection_names(entries.tree_for(child)):issues.append('子投影缺字段：'+child+'.'+name)
        if any(isinstance(n,exp.Anonymous) for n in parsed.walk()):issues.append('尚未对应查询函数')
    except (ValueError,KeyError,ParseError) as error:issues.append(str(error))
    return {'state':'试算有明确来源差异' if issues else '试算执行器已承接，逐入口非空对照未完成','issues':issues,'source_resolution':resolution,
            'verification':'静态来源及表达式核查；不是全部入口数据运行通过'}

def main():
    baseline=read('docs/erp-phase6-six-groups-baseline-20261017.json');registry=read('backend/plugins/erp_base/source_phase6_formula_registry.json')
    formulas={v['id']:v for v in registry['outcomes']};groups={str(i):[] for i in range(1,7)}
    for group in ['1','2']:
        for row in baseline['groups'][group]:
            result=formulas[row['id']];states=[v['state'] for v in result['results']]
            state='保存计算已实现并通过类型向量验证' if 'compiled_save_formula' in states else '沿用已有自动服务' if 'existing_auto_service' in states else '原来源或表达式差异，保留明确录入'
            if 'explicit_manual_input' in states:state='人工原字段保存已验证；原占位/格式不执行为算式'
            if 'query_projection_only' in states:state='原只读查询投影已验证；无原更新目标，不列为缺保存计算'
            groups[group].append({**row,**result,'state':state})
    groups['3']=[{**row,**projection(row)} for row in baseline['groups']['3']]
    verification=ROOT/'docs/erp-phase6-projection-entry-verification-20261017.json'
    if verification.exists():
        audit=json.loads(verification.read_text(encoding='utf8'))
        if audit['baseline_sha256']!=digest('docs/erp-phase6-six-groups-baseline-20261017.json'):raise ValueError('入口核验证据不属于当前固定基线')
        by_entry={r['entry']:r for r in audit['entries']}
        for row in groups['3']:
            result=by_entry[row['entry']]
            row['entry_verification']=result['state']
            calculation=result.get('calculations',{}).get(row['field'])
            if calculation and result.get('query_count',0)>0:
                row['state']='非空固定字段试算通过（合成测试库）' if calculation['unresolved_rows']==0 else '非空来源差异已逐行留存'
                row['verification']=calculation
                row['runtime_issues']=[v for v in result['issues'] if v['field']==row['field']]
                row['whole_entry_trial_issue_count']=len(result.get('full_entry_trial_issues',[]))
    for row in baseline['groups']['4']:
        c=row['configuration'];state=c.get('connection',c.get('status',c.get('state')))
        groups['4'].append({'id':row['id'],'entry':c.get('entry',c.get('DataTableName',c.get('lookup'))),
            'event':c.get('event',c.get('FieldName',c.get('master'))),'state':state,
            'implementation':c.get('implementation'),'baseline_configuration':row['id'],
            'verification':'扩大回归覆盖公共路径；本轮未把全部旧绑定逐入口验证标为完成'})
    reports=templates()
    for row in baseline['groups']['5']:
        c=row['configuration'];report=reports[c['index']];issues=requirements(report)
        name=parse_xml(base64.b64decode(report['TemplateXml']))[0].get('DataMember') if report['TemplateXml'] else None
        definition=entries.entries().get(name)
        scope='缺XML，未据此排除业务' if not report['TemplateXml'] else '缺明确入口定义，原配置保留' if definition is None else '财务打印暂缓' if definition['finance'] or name.startswith('ImpairmentPayouts') else '非财务入口'
        groups['5'].append({'id':row['id'],'index':c['index'],'report':report['RptID'],'title':report['RptTitle'],
            'state':'缺原XML' if report['TemplateXml'] is None else '有原运行差异' if issues else '具备填数校样条件，非完整原版式验收',
            'issues':issues,'original_complete':False,'scope':scope,'data_member':name})
    groups['6']=baseline['groups']['6']
    for rows in groups.values():
        for row in rows:row.update(historical_reconciliation='未完成全量旧业务结果对账',field_acceptance='未现场验收')
    result={'updated_at':datetime.now().astimezone().isoformat(),'baseline_sha256':digest('docs/erp-phase6-six-groups-baseline-20261017.json'),
        'groups':groups,'counts':{g:len(rows) for g,rows in groups.items()},'state_counts':{g:dict(Counter(v.get('state','待统一验证') for v in rows)) for g,rows in groups.items()},
        'formula_registry_counts':registry['counts'],'paused_queries':baseline['paused_queries'],'historical_import_rows_this_run':0,
        'note':'固定编号逐项登记；已实现部分与剩余代码、原来源差异分别列出。交叉组不相加，类型向量不是每入口浏览器或历史对账。'}
    (ROOT/'docs/erp-phase6-six-groups-review-20261017.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(result['state_counts'],ensure_ascii=False,indent=2))

if __name__=='__main__':main()
