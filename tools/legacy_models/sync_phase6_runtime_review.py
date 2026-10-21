"""同步本次字段/版式核查，不改写前次原查询结论或虚增完成数量。"""
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DOCS=ROOT/'docs'


def write_json(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')


def sync():
    path=DOCS/'erp-phase6-runtime-review-20261017.json'
    result=json.loads(path.read_text(encoding='utf8'))
    section='''<!-- phase6-runtime-current -->
## 2026-10-17 字段与版式继续核查

本节记录先前字段联动工作；后续变化以[查询转单及分组打印续项](2026-10-17第六阶段查询转单及分组打印续项.md)为准。[字段联动与版式运行核查](2026-10-17第六阶段字段联动与版式运行核查.md)的附表及[逐项证据](erp-phase6-runtime-review-20261017.json)已更新。先前新增登录身份默认值116处模型字段绑定、原配置续行223处、资料选择及代码回填2860处（含允许手填的原变体），修正来样色号重建的重复连接与留档。**完整原打印运行版式仍为0，第六阶段尚未全部开发完成**。

55处原查询差异继续逐项保留（其中3处已有明确缺列替代、52处尚不能运行）；216处自动事件不因公共能力接入而整体升级。40条字段复制中17条独立财务暂缓、3条配置不完整、7条已接显式采购转单、11条缺原来源视图、2条目标字段已不存在。3组完整资料过滤配置已接等值替代，13组缺失对应继续列明。所有异常和重复配置保留，先前异常说明E164～E173继续有效。公式和当前单据打印不重复计入已撤回留档的明细；工卡保存改为原进度过程，试验配方两次版本更新逐次执行。历史新增导入0、完整入口历史对账0、现场验收0；不新增旧erpID。
<!-- /phase6-runtime-current -->
'''
    for name in ['染色ERP后续开发方案.md','2026-10-16染色ERP剩余工作全量盘点清单.md',
                 '2026-10-17第六阶段查询自动调用及原版式续项清单.md',
                 '2026-10-16第六阶段旧入口自动调用与打印核查清单.md',
                 '2026-10-16第六阶段未复刻入口与打印异常明细.md']:
        target=DOCS/name;text=target.read_text(encoding='utf8')
        if '<!-- phase6-runtime-current -->' in text:
            start=text.index('<!-- phase6-runtime-current -->');end=text.index('<!-- /phase6-runtime-current -->')+len('<!-- /phase6-runtime-current -->')
            text=text[:start]+section.rstrip()+text[end:]
        else:
            title,body=text.split('\n',1);text=title+'\n\n'+section+'\n'+body.lstrip('\n')
        target.write_text(text,encoding='utf8')
    inventory_path=DOCS/'erp-remaining-inventory-20261016.json'
    inventory=json.loads(inventory_path.read_text(encoding='utf8'))
    inventory['phase6_runtime_followup_20261017']={'counts':result['counts'],'field_copy_status_counts':result['field_copy_status_counts'],
        'evidence':path.name,'development':'部分完成，剩余代码/验证及外部来源分别保留'}
    titles=['登录员工默认值的明确来源','CopyPrevRow与CopyLastRow的行序','来样保存的重复连接及原行替换',
            'QC保存目标Dots已经不在最新工卡表','原打印运行与固定高度校样','资料选择与40条跨表复制配置',
            '活动公式与打印不重复计入撤回留档行','资料上下文过滤的等值替代及残缺配置',
            '工卡保存调用原进度过程及重复流水','试验配方两次版本更新不能合成一次']
    axis=inventory['axes']['新旧系统差异及处理情况']
    for number,title in enumerate(titles,164):
        if not any(row['id']=='E'+str(number) for row in axis):
            axis.append({'id':'E'+str(number),'name':title,'status':'部分完成',
                'reason':'代码接入、明确替代、剩余实现及历史/现场状态分开记录，见本次运行核查。',
                'related_sql':[],'source':'docs/旧ERP复刻异常与合理实现说明.md'})
    inventory['counts']['新旧系统差异及处理情况']=dict(Counter(row['status'] for row in axis))
    write_json(inventory_path,inventory)
    review_path=DOCS/'erp-phase6-review-20261016.json';review=json.loads(review_path.read_text(encoding='utf8'))
    review['runtime_followup_20261017']=inventory['phase6_runtime_followup_20261017'];write_json(review_path,review)
    target=DOCS/'2026-10-17第六阶段字段联动与版式运行核查.md'
    text=target.read_text(encoding='utf8').split('<!-- runtime-appendix -->')[0].rstrip()
    lines=['','<!-- runtime-appendix -->','## 仍未绑定写入模型的原生成字段','',
           '原入口TableName为空或字段属于联查投影时，不能以公共默认值/续行已接入宣称该字段已经办理。下列原配置完整保留，编辑目标与自动时点仍需补齐。',
           '','|原入口|字段|原生成方式|原TableName|','|---|---|---|---|']
    for row in [*result['unbound_identity_configurations'],*result['unbound_copy_configurations']]:
        lines.append('|'+row['entry']+'|'+row['field']+'|'+row['kind']+'|'+str(row['original_table_name'])+'|')
    lines+=['','## 16组原资料上下文过滤','','|Lookup|来源字段|筛选字段|开发状态|','|---|---|---|---|']
    for row in result['context_filters']:
        lines.append('|'+str(row['lookup'])+'|'+str(row['master'])+'|'+str(row['target'])+'|'+
                     ('等值替代已接入；当前表单没有来源值时明确提示' if row['state']=='explicit_equality' else '原配置缺少对应，未猜测补齐')+'|')
    lines+=['','## 40条原字段复制逐项清单','','|序号|来源入口/字段|原目标入口/字段|状态|','|---:|---|---|---|']
    for row in result['field_copy_rows']:
        lines.append('|'+str(row['index']+1)+'|'+str(row['DataTableName'])+'.'+str(row['FieldName'])+'|'+
                     str(row['DestDataTableName'])+'.'+str(row['DestFieldName'])+'|'+row['status']+'|')
    lines += ['','## 全部290条原打印运行待办','','下表是开发运行能力，不是打印成功或现场验收。各表脚本和全部字段绑定原文仍保存在项目中。',
              '','|序号|原编号|名称|本次运行核查|','|---:|---|---|---|']
    for row in result['templates']:
        reason='；'.join(row['runtime_issues']) or row['development']
        lines.append('|'+str(row['index']+1)+'|'+str(row['report_id'])+'|'+str(row['title']).replace('|','／')+'|'+reason.replace('|','／')+'|')
    target.write_text(text+'\n'+'\n'.join(lines)+'\n',encoding='utf8')


if __name__=='__main__':sync()
