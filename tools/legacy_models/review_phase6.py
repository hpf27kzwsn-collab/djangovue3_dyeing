"""由实际入口执行记录更新P6清单；查询执行与整项开发严格分列。"""
import argparse
from collections import Counter
from datetime import datetime
import gzip
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DOCS=ROOT/'docs'


def write(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--audit',type=Path,required=True);parser.add_argument('--hooks',type=Path,required=True)
    parser.add_argument('--snapshot',type=Path,required=True)
    args=parser.parse_args();audit=json.loads(args.audit.read_text(encoding='utf8'))
    catalog=json.loads(gzip.decompress((ROOT/'backend/plugins/erp_base/source_phase6_catalog.json.gz').read_bytes()))
    inventory_path=DOCS/'erp-remaining-inventory-20261016.json'
    inventory=json.loads(inventory_path.read_text(encoding='utf8'))
    source={row['table']['DataTableName']:row for row in catalog['entries']}
    finance_count=sum(row['finance'] for row in source.values())
    executed={row['name']:row for row in audit['entries']}
    assert len(executed)==len(source)==1682
    assert audit['snapshot_sha256']==catalog['snapshot_sha256']
    schema=json.loads(args.snapshot.read_text(encoding='utf-8-sig'))
    physical={r['table_name'].lower() for r in schema['fields']}
    modules={r['object_name'].lower() for r in schema['modules']}
    unresolved=[]
    for check in audit['entries']:
        if check['query_state']!='unresolved':continue
        kind=check['error_type'];missing=check['error'].strip("'").lower()
        if kind=='KeyError':
            category=('原表存在，当前模型尚未承接' if missing in physical else
                      '原视图/程序定义存在，当前查询尚未展开' if missing in modules else '最新快照没有该原对象')
        elif kind=='ValueError' and '外部数据库' in check['error']:category='缺外部查询来源'
        elif kind=='OptimizeError':category='字段/别名与当前投影尚不一致'
        elif kind=='ValidationError':category='原多语句与临时表尚未移植'
        else:category='本地查询转换尚未实现'
        unresolved.append({**check,'category':category})
    difference_counts=dict(Counter(r['category'] for r in unresolved))
    output=[]
    for row in inventory['axes']['旧界面配置入口']:
        name=row['name'];check=executed[name];spec=source[name]
        if spec['finance']:status='财务暂缓';reason='独立财务本期暂缓，原配置和字段保留。'
        elif check['query_state']=='executed_empty_fixture' or check['models']:
            status='部分完成';reason='具备原查询执行或原表录入路径；逐入口字段联动/调用时点及原打印版式尚不能整体判定开发完成。'
        elif row.get('external'):
            status='缺外部资料';reason='查询依赖旧外部来源；原配置保留，尚无可执行的本地原表办理路径。'
        else:
            status='未实现';reason='原配置可查，但原入口查询仍未执行成功，尚无绑定的原表办理路径。'
        row.setdefault('pre_phase6_status',row['status'])
        row.update(status=status,reason=reason,models=check['models'],development={'status':status,'reason':reason},
            historical_reconciliation={'status':'财务暂缓' if spec['finance'] else '待原业务结果全量对账','new_import_rows':0},
            field_acceptance={'status':'财务暂缓' if spec['finance'] else '待现场验收','confirmed':False},
            phase6_query={'state':check['query_state'],'error':check.get('error'),'parameters':check.get('parameters',[])},
            phase6_evidence='docs/erp-phase6-review-20261016.json')
        output.append({'id':row['id'],'name':name,'title':row['title'],'kind':row['kind'],'module':row['module'],
            'development':row['development'],'historical_reconciliation':row['historical_reconciliation'],
            'field_acceptance':row['field_acceptance'],'models':check['models'],'query':row['phase6_query'],
            'field_count':len(spec['fields']),'formula_count':len(check['formulas']),
            'raw_nonempty_hooks':list(check['hooks']),'remaining':[] if spec['finance'] else [
                *(['修复本条原查询执行错误：'+check['error']] if check['query_state']=='unresolved' else []),
                '验证原投影、分组、排序和实际入口过滤的非空结果',
                *(['核对编辑列、资料选择回填及写入目标；验证默认值和主从单据办理'] if check['models'] else []),
                *(['核对原公式来源、运算及客户端实际自动时点'] if check['formulas'] else []),
                *(['逐项区分有效钩子与注释，验证对应动作自动调用'] if check['hooks'] else []),
                '核实是否为旧客户端打印数据源；有对应版式时继续移植，不由名称猜测绑定']} )
    counts=dict(Counter(r['development']['status'] for r in output))
    inventory['counts']['旧界面配置入口']={'已完成':0,**counts}
    report={'review_at':datetime.now().astimezone().isoformat(),'scope':f'第六阶段旧界面1682项；财务{finance_count}项暂缓',
        'snapshot_sha256':catalog['snapshot_sha256'],'counts':{'development':{'开发完成':0,**counts},
        'query_execution':audit['counts'],'whole_entry_historical_reconciled':0,'field_accepted':0},
        'definition':'executed_empty_fixture只证明隔离库查询执行；不能据此认定整项入口、历史结果或现场已完成。',
        'fields':sum(len(e['fields']) for e in source.values()),'entries':output}
    write(DOCS/'erp-phase6-review-20261016.json',report)
    write(ROOT/'backend/plugins/erp_base/source_phase6_query_support.json',{
        name:{k:value for k,value in check.items() if k in ['query_state','parameters','error','error_type']} for name,check in executed.items()})
    reports={'templates':catalog['reports'],'report_menu_links':catalog['report_menus'],'functions':catalog['functions'],
        'count':len(catalog['reports']),'original_templates_are_executable_web_layouts':False,
        'reason':'原DevExpress/TF.ReportDesign客户端模板和脚本保留；本轮实现原字段数据版打印及打印前联动。'}
    write(DOCS/'erp-phase6-print-review-20261016.json',reports)
    differences=['# 第六阶段未复刻入口与打印异常明细','',
        '本清单只列当前仍有差异的内容，不取消其开发范围。原始数据、重复记录及配置全文继续保留。当前共有'+str(len(unresolved))+'项查询执行差异；分类依据是已保存最新结构快照，未连接旧库重新抽取。','',
        '|类别|入口数|','|---|---:|',*[f'|{k}|{v}|' for k,v in difference_counts.items()],'',
        '本轮已补齐最新快照中全部非财务原表模型。其余查询仍按缺失对象、字段/别名差异及外部来源分别处理；原查询投影和失败依据完整保留，不能用空结果替代。','',
        '下列错误是本次第一个实际失败点；解决后须重新执行整条查询，不能假定只剩一个问题。原始错误全文见逐项JSON。','',
        '|原入口|名称|差异类别|实际错误|','|---|---|---|---|']
    for check in unresolved:
        values=[check['name'],check['title'],check['category'],check['error']]
        differences.append('|'+ '|'.join(str(v).replace('|','／').replace('\r','').replace('\n','<br>') for v in values)+'|')
    differences+=['','## 原打印差异','',
        '290条原报表、289份模板内容、261份XML全部保留。149份XML包含客户端脚本，当前仅实现数据版打印，原版式、脚本、条码、套打和分页不能算已复刻。','',
        '|报表编号|原XML解析错误|','|---|---|']
    for row in catalog['reports']:
        if 'xml_error' in row:differences.append('|'+row['RptID']+'|'+row['xml_error'].replace('|','／')+'|')
    differences+=['','## 自动规则差异','',
        '有效钩子216处，逐项正文与接线状态见[钩子核查JSON](erp-phase6-hook-review-20261016.json)。需要继续补齐调用及验证；不能按标题猜测原业务。',
        'p_ShiftKF/p_ShiftPB仅有dechare残片，QCJobList引用trade架构，ReworkStuffWeight含缺失对象及外部中控。原字段可录入不意味着这些事件已经完整复刻。',
        '默认值/复制行/登录员工来源、GenerateTime自动时点、资料选择回填以及公式循环关系仍有代码和验证待办。完整处理与数据保留规则见[异常E146～E157](旧ERP复刻异常与合理实现说明.md)。']
    (DOCS/'2026-10-16第六阶段未复刻入口与打印异常明细.md').write_text('\n'.join(differences)+'\n',encoding='utf8')
    report['query_difference_counts']=difference_counts
    write(DOCS/'erp-phase6-review-20261016.json',report)
    hooks=json.loads(args.hooks.read_text(encoding='utf8'));hook_rows=[]
    # 这里只标记可定位的接线，不把“有函数”升级为逐入口行为验证完成。
    connected={2,4,12,16,17,18,19,20,21,22,24,25,26,29,30,50,54,55,69,74,80,91,96,102,103,111,112,116,123,125,126,135}
    for index,hook in enumerate(hooks):
        for name,event in hook['entries']:
            hook_rows.append({'entry':name,'event':event,'sql':hook['sql'],'definition_index':index,
                'connection':'已定位service接线，待逐入口验证' if index in connected else '尚未逐项核实实现与时机',
                'full_behavior_verified':False})
    hook_counts=dict(Counter(r['connection'] for r in hook_rows))
    write(DOCS/'erp-phase6-hook-review-20261016.json',{'unique_bodies':len(hooks),'binding_count':len(hook_rows),
        'counts':hook_counts,'bindings':hook_rows,'note':'不以注释正文计有效钩子；未复核并不表示既有service完全不存在。'})
    def cell(value):return str(value if value is not None else '').replace('|','／').replace('\r','').replace('\n','<br>')
    differences+=['','## 全部有效自动钩子的开发与验证待办','',
        '以下216处均为非财务有效正文绑定。已有service接线也须继续核验实际时点、完整检查及逆向；每条原SQL正文保存在对应JSON。','',
        '|原入口|原事件|正文索引|当前状态|','|---|---|---:|---|']
    for row in hook_rows:differences.append('|'+ '|'.join(cell(row[k]) for k in ['entry','event','definition_index','connection'])+'|')
    differences+=['','## 全部原报表版式保留清单','',
        '原报表配置290条逐条保留，包括财务配置；本期只推进非财务版式。原数据入口是模板声明，并不直接证明实际菜单绑定。下列原版式均未作为完整网页模板验收。','',
        '|原行索引|报表编号|原标题|模板数据入口|原模板|原XML|有效脚本属性|','|---:|---|---|---|---|---|---:|']
    for row in catalog['reports']:
        scripts=sum(v['attribute']!='Ref' and bool(v.get('value')) for v in row.get('script_attributes',[]))
        values=[row['index'],row['RptID'],row['RptTitle'],row.get('data_member'),row['has_template'],row['has_xml'],scripts]
        differences.append('|'+ '|'.join(cell(value) for value in values)+'|')
    (DOCS/'2026-10-16第六阶段未复刻入口与打印异常明细.md').write_text('\n'.join(differences)+'\n',encoding='utf8')
    inventory['phase6_review']={'file':'docs/erp-phase6-review-20261016.json','counts':report['counts'],
        'printing':'docs/erp-phase6-print-review-20261016.json','hooks':'docs/erp-phase6-hook-review-20261016.json',
        'next':'仍需补齐旧入口逐项联动验证与原模板移植；不能提前称为仅待现场或进入P7。'}
    write(inventory_path,inventory)
    rows=['# 第六阶段旧入口、自动调用与打印开发核查清单','',
        '依据2026-10-16 12:15结构和界面快照。财务暂缓，不新增额外旧erpID。原字段、重复行、异常和不常用入口均保留。','',
        '**本阶段尚未全部开发完成。** 本轮建成统一旧入口工作台、原查询执行/导出、字段规则展示、公式试算/采用、部分保存审核联动及数据版打印。目录可访问和查询能够执行，不等于整个旧入口已经复刻完成。','',
        '逐项异常另见[未复刻入口与打印异常明细](2026-10-16第六阶段未复刻入口与打印异常明细.md)；字段、原键和实际动作权限检查见[验证证据](erp-phase6-verification-20261016.json)。','',
        '## 数量与三项状态','',
        f'- 原入口1682项、原字段配置{report["fields"]}项；非财务{1682-finance_count}项，财务暂缓{finance_count}项。',
        '- 整入口开发状态：'+ '；'.join(f'{k} {v}' for k,v in report['counts']['development'].items())+'。',
        '- 隔离库查询执行：'+ '；'.join(f'{k} {v}' for k,v in audit['counts'].items())+'。',
        '- 本轮新增历史导入0；完整历史业务结果对账完成0；现场验收确认0。',
        '- 有效钩子'+str(len(hook_rows))+'处、不同正文'+str(len(hooks))+'种：'+'；'.join(f'{k} {v}' for k,v in hook_counts.items())+'。',
        '- SQL对象732项、原物理表690项、界面1682项是不同统计轴，不能相加。P1～P5单SQL对象结论不等于本阶段整界面结论。','',
        '## 本轮已经实现的路径','',
        '1. 原表页面的“旧业务入口”打开完整目录。原表办理页按入口显示原字段标题、只读规则、公式及格式依据；用户仍可录入原始异常值。',
        '2. 查询按原SQL投影执行，支持参数、原外层空表初始化条件的明确解除、旧标量服务调用、日期零值、文本算术、STUFF及XML串联。结果按位置保留重名列，权限过滤不会合并两条完全相同的原行。',
        '3. CSV导出完整本次结果；SQL NULL写成\\N，文字中的反斜杠双写，空字符串保持空白，二进制列用base64:前缀加Base64正文，读取时须按此规则及原字段类型还原；不会把NULL与空串混成同一种值。',
        '4. 原公式逐字段试算，子行按原键或明确主从连接取数，重复物理行参与计算。缺字段、父行歧义、错误表达式、除零逐项列出并保留原值。采用结果走业务service；历史原计算值仅试算不覆盖。',
        '5. 工卡状态/属性、工艺路线名称、库位合并、复版份额、采购材料调价、报价日期、出库日期共享来源等保存联动已补入service；审核与反审核同步原相关状态。具体仍须按入口验证自动时点。',
        '6. 数据版打印准备保存原字段快照，旧键匹配的全部重复子行包含在内。准备、取消、失败、人工确认分开留事实；重开页面可继续同一打印记录，不重复运行打印前联动。历史单据打印不重跑旧业务副作用。',
        '7. 新增63个原平台配置表的静态模型、533个原字段及0032～0034迁移；字段/原键逐一沿用快照，重复原键可以并存。原配置SQL和通知内容仅作为原数据保存，不等于启用原定时任务或通知投递。',
        '8. 机物料部门横向汇总、成品十卷细码横向打印、员工考勤临时表流程改为等价本地查询；验证负数、重复领料/刷卡、缺卡、迟到和假日，原始SQL继续保留。','',
        '到货通知、染色计件、包装质量及工艺审核的5项取数歧义另已明确修复，按明细产品、工卡客户、包装聚合及已关联工卡订单号分别取数，来源调整见E157。','',
        '## 原打印证据和不能冒充完成的部分','',
        '保留290条报表配置、289份原模板内容、261份XML、148条原打印菜单关联及1395条功能配置。原模板属于DevExpress/TF.ReportDesign客户端；网页数据版不是原版式。',
        '7份XML含非法字符引用，149份XML含客户端脚本；原文原样保留。模板下载、数据取数、脚本/条码/套打还原及真实打印机回执分别计数。',
        '旧入口只有2项填写ModuleNo，和打印菜单FuncNo没有明确对应；不依据相似名称自动绑定报表。仍须从旧客户端取得真实功能/数据集关系。','',
        '## 仍需继续开发及必要验证','',
        '1. 先补本表列出的未执行查询：区分最新库已经缺失的原表字段、旧SQL原式错误和真实外部库。每个错误均保留，不返回空结果掩盖。',
        '2. 对全部旧入口核对编辑目标、资料选择器/回填、父子行与完整非空单据，完成必要自动规则验证。仅在备注展示配置不能算该规则已实现。',
        '3. 原GenerateTime代码0～4的客户端含义尚无实现源证据；目前明确试算/采用，不擅自把全部公式改成每次保存自动运行。CopyPrevRow/CopyLastRow的行序和登录员工/部门/班组映射也不能从名字猜测。',
        '4. 补齐所有Before/After钩子的逐入口差异测试；已连接原服务仍要验证调用时点。原代码仅有dechare、引用缺失表/字段等异常分别留档；不把所有钩子算已完成。',
        '5. 移植有证据的旧打印版式与脚本；没有客户端功能绑定的报表单列。随后进行真实历史结果对账、现场操作及设备打印验收。',
        '以上第1～5项中仍含代码/必要验证工作，不能全部列作“等待现场”；没有因异常、重复、空表、停用或不常用而从范围删项。','',
        '## 逐入口状态','',
        '全字段及旧SQL原文保存在随代码提交的压缩目录；完整错误、参数和三项状态见同名JSON。下表保留全部1682项。','',
        '|编号|原入口|业务名称|整入口开发状态|查询执行|原字段配置|',
        '|---|---|---|---|---|---:|']
    for r in output:
        cells=[r['id'],r['name'],r['title'] or '',r['development']['status'],r['query']['state'],str(r['field_count'])]
        rows.append('|'+ '|'.join(str(c).replace('|','／').replace('\n',' ') for c in cells)+'|')
    (DOCS/'2026-10-16第六阶段旧入口自动调用与打印核查清单.md').write_text('\n'.join(rows)+'\n',encoding='utf8')
    print(json.dumps(report['counts'],ensure_ascii=False))


if __name__=='__main__':main()
