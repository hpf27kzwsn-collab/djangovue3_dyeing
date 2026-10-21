"""从实际只读核验、条件登记及版式解析更新第六阶段续项证据。"""
import argparse
from collections import Counter
from datetime import datetime
import gzip
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DOCS=ROOT/'docs'
BASE=ROOT/'backend/plugins/erp_base'


def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def write(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')


def review(live_directory):
    live=read(live_directory/'query-metadata.json')
    support=read(BASE/'source_phase6_query_support.json')
    catalog=json.loads(gzip.decompress((BASE/'source_phase6_catalog.json.gz').read_bytes()))
    unresolved={r['table']['DataTableName']:{'title':r['table']['Alias'],**support[r['table']['DataTableName']]} for r in catalog['entries'] if support[r['table']['DataTableName']]['query_state']=='unresolved'}
    queries=[]
    for row in live['queries']:
        errors=[{'number':c['error_number'],'message':c['error_message']} for c in row.get('columns',[]) if c['error_number']]
        if row.get('error'):errors.append({'number':row['error_number'],'message':row['error']})
        assert errors,row['name']
        local=unresolved[row['name']]
        category='缺外部库或链接' if local['error_type']=='ValueError' and '外部数据库' in local['error'] else '原字段已不存在' if errors[0]['number']==207 else '缺本地原对象'
        evidence={'name':row['name'],'title':local['title'],'category':category,'errors':errors,
            'development':'未能等价复刻，缺失原数据定义/来源；原入口与配置保留',
            'historical_reconciliation':'原查询在当前旧库无法编译，未获得可对账结果','field_acceptance':'未验收'}
        queries.append(evidence)
        support[row['name']]['live_original']={'verified_at':live['captured_at'],'status':'metadata_compile_failed',**evidence}
    write(BASE/'source_phase6_query_support.json',support)
    query_report={'verified_at':live['captured_at'],'mode':live['statements'],
        'source_snapshot_sha256':hashlib.sha256((live_directory/'structure-and-logic.json').read_bytes()).hexdigest(),
        'source_metadata_sha256':hashlib.sha256((live_directory/'query-metadata.json').read_bytes()).hexdigest(),
        'databases':live['databases'],'servers':live['servers'],'counts':dict(Counter(r['category'] for r in queries)),
        'queries':queries,'historical_import_rows':0,'historical_query_results_reconciled':0,'onsite_accepted':0,
        'print_hashes':live['print_hashes']}
    write(DOCS/'erp-phase6-live-query-review-20261017.json',query_report)

    hook_report=read(DOCS/'erp-phase6-hook-review-20261016.json')
    guards=read(BASE/'source_phase6_guards.json')
    wired={45:'source_workflow_services.refresh_job',74:'source_workflow_services.refresh_job',
        92:'source_trial_variants.saved',96:'source_packaging_flow.saved',124:'source_services.advance/shift_work.apply',
        125:'source_sample_flow.sync_lab',135:'source_sampling_services.saved'}
    effects={27:'source_phase6_hooks.approved/post',28:'source_phase6_hooks.approved/post',
        29:'source_phase6_hooks.approved/transfer',30:'source_phase6_hooks.undo_stock_transfer',
        117:'source_phase6_hooks.approved/transfer',118:'source_phase6_hooks.undo_stock_transfer',
        72:'source_phase6_hooks.before_delete',101:'source_phase6_hooks.before_delete',109:'source_phase6_hooks.aborted',
        110:'source_phase6_hooks.rebuild_sensitive_dye',114:'source_phase6_hooks.salary_team_detail',
        136:'source_phase6_hooks.before_delete',97:'source_phase6_hooks.approved',98:'source_phase6_hooks.approved'}
    for row in hook_report['bindings']:
        index=row['definition_index'];spec=guards.get(str(index))
        if index in [36,37,38,39]:
            row.update(connection='独立财务分支暂缓',reason='减值核销、账期及财务审核，原正文保留')
        elif index in [79,107,108]:
            row.update(connection='缺外部调用及回执',reason='旧动作依赖真实KPS/立信调用；服务明确返回未接入，事务不提交成功审核')
        elif index in [102,103]:
            row.update(connection='缺本地原表定义',reason='最新旧库没有RecordYieldCheck；不能替换成RecordYield。明确报告未复刻并回滚审核/反审核。')
        elif spec:
            row.update(connection='已接入动作条件，必要用例仍逐规则记录',implementation='source_phase6_guards.before',
                mode=spec['mode'],cursor_order=spec['cursor_order'],deferred_finance=spec.get('deferred_finance'),
                reconstruction=spec.get('reconstruction'),advisory=spec.get('advisory',False))
        elif index in effects:
            row.update(connection='已接入保存或逆向副作用，待逐入口验收',implementation=effects[index])
        elif index in wired:
            row.update(connection='已定位既有服务及回归用例，仍有原行为差异需核对',implementation=wired[index])
        # 各项整链/现场尚未验收，不能因服务存在而修改这个结论。
        row['full_behavior_verified']=False
        row['historical_reconciliation']='未完成原业务结果全量对账';row['field_acceptance']='未现场验收'
    hook_report['counts']=dict(Counter(r['connection'] for r in hook_report['bindings']))
    hook_report['followup_at']=datetime.now().astimezone().isoformat()
    hook_report['registered_condition_bodies']=len(guards)
    hook_report['registered_condition_bindings']=sum(len(s['bindings']) for s in guards.values())
    write(DOCS/'erp-phase6-hook-review-20261016.json',hook_report)
    write(BASE/'source_phase6_hook_manifest.json',{
        name:[{k:v for k,v in row.items() if k!='sql'} for row in hook_report['bindings'] if row['entry']==name]
        for name in dict.fromkeys(r['entry'] for r in hook_report['bindings'])})

    layouts=read(DOCS/'erp-phase6-layout-review-20261017.json')
    report=read(DOCS/'erp-phase6-review-20261016.json')
    report['followup_20261017']={'live_query_counts':query_report['counts'],'hooks':hook_report['counts'],
        'layouts':layouts['counts'],'historical_import_rows':0,'whole_entry_historical_reconciled':0,'field_accepted':0}
    write(DOCS/'erp-phase6-review-20261016.json',report)
    inventory=read(DOCS/'erp-remaining-inventory-20261016.json')
    for row in inventory['axes']['旧界面配置入口']:
        name=row['name']
        if name in unresolved:row['phase6_query']['live_original']=support[name]['live_original']
        row['phase6_hooks']=[{'event':h['event'],'status':h['connection']} for h in hook_report['bindings'] if h['entry']==name]
    inventory['phase6_followup_20261017']=report['followup_20261017']
    exceptions=inventory['axes']['新旧系统差异及处理情况']
    for number,title in [(158,'第六阶段55项查询的实库缺失依据'),(159,'原动作条件的顺序、原错误和身份对应'),
            (160,'原保存副作用、质量审核及设备调用'),(161,'半成品转坯料与坯料审核自动过账'),
            (162,'原版式解析修复与尚未实现的打印运行部分'),(163,'QueryWorkList2原核对表缺失与审核事务')]:
        if not any(r['id']=='E'+str(number) for r in exceptions):
            exceptions.append({'id':'E'+str(number),'name':title,'status':'部分完成',
                'reason':'明确实现、缺失来源及三项状态分别见续项清单；未冒充整入口完成。',
                'related_sql':[],'source':'docs/旧ERP复刻异常与合理实现说明.md'})
    inventory['counts']['新旧系统差异及处理情况']=dict(Counter(r['status'] for r in exceptions))
    write(DOCS/'erp-remaining-inventory-20261016.json',inventory)
    # 替换旧异常表中的自动调用状态，保留所有原正文和索引。
    path=DOCS/'2026-10-16第六阶段未复刻入口与打印异常明细.md'
    lines=path.read_text(encoding='utf8').splitlines()
    for i,line in enumerate(lines):
        for row in hook_report['bindings']:
            if line.startswith('|'+row['entry']+'|'+row['event']+'|'):
                columns=line.split('|');columns[-2]=row['connection'];lines[i]='|'.join(columns);break
    path.write_text('\n'.join(lines)+'\n',encoding='utf8')
    summary=['# 第六阶段续项核验：查询、自动调用和原打印版式','',
        '核验日期：2026-10-17。旧SQL Server只读；本轮没有向旧库写入或向新项目导入历史业务数据。财务暂缓；不新增旧erpID。','',
        '## 当前结论','',
        '55项查询均已在已启动的旧库做只读元数据编译核验，55项仍在旧库报错。这不代表新系统已经修复，也不能算历史对账通过。最新结构、程序、界面及字段配置与前次快照逐项相同；290条原打印配置的模板及XML字节摘要全部与旧库一致。','',
        '|原库实际差异|数量|','|---|---:|',*[f'|{k}|{v}|' for k,v in query_report['counts'].items()],'',
        '本地旧审计的13项字段、19项对象、23项外部来源，是新查询引擎首次失败点分类；本次旧库的首次失败点不同，两个分类不能相加。','',
        '## 开发、历史对账、现场验收','',
        '|工作|开发证据|历史数据对账|现场验收|','|---|---|---|---|',
        f'|原动作条件|登记{len(guards)}种正文、{sum(len(s["bindings"]) for s in guards.values())}处入口绑定；非空测试和全部关系式验证另列|未完成|未完成|',
        '|保存与逆向|敏感色重建、班组调整、印花清理、报工回写及质量审核等接入service；非等价处理见异常|未完成|未完成|',
        '|原打印版式|261份XML均可解析并核对几何、绑定、字体和表格；不是完整旧打印运行器|未完成|未完成|',
        '|剩余55查询|已核实原库首错及缺失来源；尚不能宣称等价复刻|原查询无可对账结果|未完成|','',
        '## 55项逐条核验','',
        '|入口|业务名称|原库差异|首条真实错误|','|---|---|---|---|',
        *['|'+'|'.join(str(v).replace('|','／').replace('\n',' ') for v in [r['name'],r['title'],r['category'],r['errors'][0]['message']])+'|' for r in queries],
        '', '## 全部216处自动调用状态','',
        '|状态|入口绑定数|','|---|---:|',*[f'|{k}|{v}|' for k,v in hook_report['counts'].items()],
        '','|入口|事件|当前状态|','|---|---|---|',*['|'+r['entry']+'|'+r['event']+'|'+r['connection']+'|' for r in hook_report['bindings']],
        '','## 全部290条原打印配置','',
        '261份XML已解析，其中7份数字控制字符实体在解析副本中逐字符恢复，原字节未替换。含脚本模板由先前可解析149份补充到156份。29条没有XML（原客户端模板或空配置继续保留）。目前原运行版式完整复刻0；预览不执行脚本，不代表条码、分页、汇总、子报表或真实设备输出已完成。','',
        '|报表|标题|几何解析|原脚本|尚需处理控件/事件数|','|---|---|---|---|---:|',
        *['|'+'|'.join(str(v).replace('|','／').replace('\n',' ') for v in [r['RptID'],r['title'],r['geometry_state'],'有' if r.get('script_bindings') else '无可解析脚本',len(r.get('issues',[]))])+'|' for r in layouts['reports']],
        '','## 后续顺序','',
        '1. 按异常说明核对本轮采用的无序游标顺序、器具原键、缺损班组条件和trade→dye质量关联；这些都是明确列出的实现差异。',
        '2. 恢复缺失原对象/历史版本定义及外部库，核对55项完整原查询输出。库存长度、重量、净重不能混成一个Qty；不以零或空结果填平未知字段。',
        '3. 依据完整模板继续实现脚本、汇总分组、分页、条码和子报表，并取得原客户端功能与数据集绑定及必要运行组件。',
        '4. 独立安排真实历史结果对账与现场单据/设备打印验收。当前三项状态分别登记，不能合并为“已完成”。','']
    (DOCS/'2026-10-17第六阶段查询自动调用及原版式续项清单.md').write_text('\n'.join(summary),encoding='utf8')
    print({'live_queries':query_report['counts'],'hooks':hook_report['counts'],'layouts':layouts['counts']})


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--live-directory',type=Path,required=True)
    args=parser.parse_args();review(args.live_directory)
