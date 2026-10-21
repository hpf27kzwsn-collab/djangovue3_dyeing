"""记录本轮实际验证结果，并同步开发、历史对账、现场验收三个维度。"""
import hashlib
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT/'docs'
TITLE = '2026-10-17第六阶段查询转单及分组打印续项.md'


def read(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))


def save(path, value):
    (ROOT/path).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf8')


def digest(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def replace_section(path, marker, section):
    text=path.read_text(encoding='utf8');start='<!-- '+marker+' -->';end='<!-- /'+marker+' -->'
    content=start+'\n'+section.strip()+'\n'+end
    if start in text:
        a=text.index(start);b=text.index(end)+len(end);text=text[:a]+content+text[b:]
    else:
        title,body=text.split('\n',1);text=title+'\n\n'+content+'\n\n'+body.lstrip('\n')
    path.write_text(text,encoding='utf8')


def main():
    support=read('backend/plugins/erp_base/source_phase6_query_support.json')
    runtime=read('docs/erp-phase6-runtime-review-20261017.json')
    live=read('.runtime-temp/phase6/continuation-evidence/query-metadata.json')
    schema=read('.runtime-temp/phase6/final-schema-check.json')
    tests=[]
    for name in ['continuation-regression.log','continuation-final-targeted.log']:
        path='.runtime-temp/phase6/'+name;text=(ROOT/path).read_text(encoding='utf8')
        match=re.search(r'Ran (\d+) tests in ([\d.]+)s\s+OK',text)
        assert match, name
        tests.append({'log':path,'tests':int(match[1]),'seconds':float(match[2]),'result':'passed',
                      'sha256':digest(path)})
    files=['backend/plugins/erp_base/'+name for name in [
        'source_phase6_reconstructions.py','source_phase6_transfers.py','source_phase6_auto_values.py',
        'source_phase6_entries.py','source_phase6_query_support.json','source_phase6_rendering.py',
        'source_phase6_forms.py','source_api.py','source_services.py','source_trial_variants.py',
        'tests/test_source_phase6_continuation.py']]+['web/src/plugins/erp/OriginalEntryWorkbench.vue']
    unresolved=[{'entry':name,'category':row['live_original']['category'],'error':row['error']}
                for name,row in support.items() if row['query_state']=='unresolved']
    reconstructed=[name for name,row in support.items() if row['query_state']=='reconstructed_missing_projection']
    evidence={'verified_at':datetime.now().astimezone().isoformat(),'development':'部分完成',
        'query_status_counts':dict(Counter(r['query_state'] for r in support.values())),
        'original_query_differences':len(unresolved)+len(reconstructed),
        'explicit_query_reconstructions':reconstructed,'unresolved_queries':unresolved,
        'runtime_counts':runtime['counts'],'field_copy_status_counts':runtime['field_copy_status_counts'],
        'tests':tests,'test_scope':'168项扩大回归通过；随后仅表单金额默认值元数据调整，13项针对性回归通过。不是全项目重新跑测。',
        'frontend':{'log':'.runtime-temp/phase6/continuation-frontend.log','result':'typecheck_and_build_passed'},
        'schema':schema,'old_sql_readonly_metadata':live,
        'browser_proof':{'template_index':3,'synthetic_records':41,'pages':3,
            'result':'浏览器核对分组表头、表格、重复行及分页；不是纸张和打印机验收'},
        'historical_import_rows_this_run':0,'historical_reconciliation':'未完成真实历史全量对账',
        'field_acceptance':'未现场验收','code_sha256':{p:digest(p) for p in files}}
    save('docs/erp-phase6-continuation-verification-20261017.json',evidence)
    section=f'''## 第六阶段最新续项（2026-10-17）

见[查询转单及分组打印续项]({TITLE})和[本轮验证记录](erp-phase6-continuation-verification-20261017.json)。

本轮补齐3处查询的明确缺列替代、采购转到货通知的7列复制、采购行金额保存计算、加色报工逐候选执行及撤销、打样任务明细A的单层分组分页。168项扩大回归及随后13项针对性回归通过；前端类型检查与构建通过；模型检查无新增迁移，不新增旧erpID。

**第六阶段仍为部分完成。** 55处原查询差异中3处可按注明方案运行、52处尚未实现运行；不将缺列替代计作等价完成。原打印290项中可填数校样2项、完整原打印运行0项。40条跨表复制：7条已接显式采购转单、11条缺原报价来源视图、2条最新目标字段缺失、3条原配置不完整、17条独立财务暂缓。完整入口完成数不因局部功能完成上调。

开发验证、历史数据对账、现场验收分开记录。本轮新增历史导入0；真实历史全量对账未完成、现场验收未完成。异常新增E174～E178，异常、重复原行及中间替换记录保留。
'''
    for name in ['染色ERP后续开发方案.md','2026-10-16染色ERP剩余工作全量盘点清单.md',
                 '2026-10-17第六阶段查询自动调用及原版式续项清单.md',
                 '2026-10-16第六阶段旧入口自动调用与打印核查清单.md',
                 '2026-10-16第六阶段未复刻入口与打印异常明细.md',
                 '2026-10-17第六阶段字段联动与版式运行核查.md']:
        replace_section(DOCS/name,'phase6-continuation-current',section)
    titles=['缺列查询明确替代与原异常连接','采购转到货通知及目标字段限制','加色报工逐游标候选替换留档',
            '打样任务明细A分组分页及排序差异','采购金额保存计算与原GenerateTime枚举缺失']
    inventory=read('docs/erp-remaining-inventory-20261016.json')
    inventory['phase6_continuation_20261017']={k:evidence[k] for k in ['verified_at','development',
        'query_status_counts','original_query_differences','explicit_query_reconstructions','field_copy_status_counts',
        'historical_reconciliation','field_acceptance']}
    axis=inventory['axes']['新旧系统差异及处理情况']
    for number,title in enumerate(titles,174):
        row={'id':'E'+str(number),'name':title,'status':'部分完成','reason':'明确替代或局部开发已验证，原行为差异与对账/验收见续项文档。',
             'related_sql':[],'source':'docs/旧ERP复刻异常与合理实现说明.md'}
        existing=next((i for i,r in enumerate(axis) if r['id']==row['id']),None)
        if existing is None:axis.append(row)
        else:axis[existing]=row
    inventory['counts']['新旧系统差异及处理情况']=dict(Counter(r['status'] for r in axis))
    save('docs/erp-remaining-inventory-20261016.json',inventory)
    review=read('docs/erp-phase6-review-20261016.json')
    review['continuation_20261017']=inventory['phase6_continuation_20261017']
    save('docs/erp-phase6-review-20261016.json',review)
    document='''# 第六阶段查询、自动触发、转单与原打印续项

日期：2026-10-17。本轮承接最新盘点。财务系统暂缓，不新增旧erpID，不按异常、重复或不常用删除业务范围。

## 本轮结果及三个完成维度

|范围|开发与验证|历史数据对账|现场验收|
|---|---|---|---|
|3处缺列查询、7个原投影字段|明确缺列替代已开发并通过非空用例，仍非等价完成|旧查询当前无法编译；未完成同口径全量对账|未验收|
|采购转到货通知|原7列映射、批次事务、来源快照、界面动作与接口已开发；旧客户端按钮行为仍缺证据|未试导入真实历史单据并逐单对账|未验收|
|采购行金额|保存时数量×价格计算已开发；明确采用新触发时点，手工金额优先|未完成真实历史对账|未验收|
|加色报工|所有候选逐次生成、替换留档、整链撤销已开发；原无序游标顺序和编号差异仍保留|未完成真实历史对账|未验收|
|打样任务明细A|原XML单层分组、组前分页、跨页和重复行填数已开发；41条测试记录分3页经浏览器核查|未完成真实历史打印结果对账|纸张、字体、打印机未验收|

168项扩大回归全部通过；随后补充采购表单空金额自动计算元数据，13项针对性回归通过。前端类型检查与构建通过。766个ERP模型、655个原表模型、12606个原字段，新增迁移0，额外旧erpID字段0。上述数字是代码结构与测试结果，不是新导入数据数量。本轮没有导入旧业务数据。

## 查询的明确处理

原查询原文完整保留，改写仅针对以下顶层展示列，值为NULL并在界面说明缺失原因。不是用0补齐原数据，不修改连接、筛选或数量公式。

|旧入口|当前旧库缺少的列|保留行为|
|---|---|---|
|qry_CraftPreCheckJobSheet|JobSheet.IsNew|原未完成工序筛选及DISTINCT；相同投影的原DISTINCT仍生效，原表重复记录不删除|
|vwGrayOutQueryBySaleBack|GrayOutDetail.Structure、JobDetailNo|原头表自身等值连接继续保留：2个头×2个明细仍返回4行，不自行修成按流水关联|
|vwGrayInAndOutDetailQuery|GrayInDetail.FabricID、Structure、JobDetailNo、NoticeDetailNo|原收发明细关联保留；末个LEFT JOIN中的1=2保留，不能当成外层空表初始化条件删除；原剩余数量公式保留|

已用Windows身份只读核对旧SQL Server的查询元数据，三处仍报以上缺列。没有得到旧查询成功执行结果，不能把替代查询计作历史对账完成。新接口及CSV保留重复行，CSV继续用\\N区分NULL与空字符串。

## 转单及自动保存

到货通知单行新增“采购转到货通知”动作，选择明确的采购明细原行。复制ColorID、ColorNum、FabricID、Qty、Rolls、Spec；DetailNo写入目标PurDetailNo。目标自身DetailNo按原编号规则生成，SheetSeries取明确目标表头。相同原采购号、相同值和重复选择分别生成明细，不去重。来源完整快照与7列映射写入已有单据上下文，不新增业务模型字段。

整批明细保存后一次执行整单联动；任一行不能保存则整批回滚并指明来源，不把失败行静默丢弃。例如原采购FabricID为NULL，而ArrivalNoticeDetail.FabricID为非空字段，必须明确处理该目标限制；不替换成假物料。原字段长度和数值精度约束也继续有效。历史来源原行保留。

该转单按具体采购明细选择，而旧PurNondeliveryList查询的主表连接可能产生重复组合；没有据此猜测旧客户端一次点击究竟选了哪些组合。原查询仍可独立查看。报价转订单11个现存目标字段仍缺vwQuoteMDToOrderMD定义，另外PreUnitProfit、Structure两个目标字段已不在最新表中，继续作为未完成事项。

PurDetail.Amount的原公式是[Qty]*[Price]。新增采购行、修改Qty或Price时自动计算，NULL继续传播，负数保留，按目标原金额精度保存；显式提交Amount（包括NULL）优先，修改无关字段不重算。表单新增使用自动默认值时，空金额交由服务计算；关闭默认值则可以明确保留空金额。原GenerateTime=0的客户端枚举定义缺失，当前保存时计算是公开的替代时机，不推广猜测其它枚举值。

ProdTest_AddColorProduct保存后不再只生成最后一个候选：按试验原行、班组成员、班次的ID顺序逐个执行。每个有效候选生成WProcess、JobShiftEmp、WProcessStep；下一候选替换上一候选，全部中间记录留档，最终仅末轮活动。撤销恢复原先报工及回写效果，中间历史记录继续保留。旧游标无ORDER BY，真实原执行顺序不能证明；新编号仍采用既有明确序列，而非伪造过去GETDATE的毫秒值。

## 原打印

新增支持原打样任务明细A（模板索引3）：CustomerID单层分组、BeforeBand组前分页、固定明细行高度、同组跨页及RepeatEveryPage属性。组内重复行保留，空值和空字符串分别分组。文本采用Unicode原值排序，旧客户端区域排序比较尚待核对。原H003打样任务明细B继续可用。

290份原打印配置中，可填数校样从1份增加到2份；完整原模板运行仍为0。其余288份中259份有XML但还有运行差异、29份缺XML。计数包含归档的财务相关配置，财务不进入本期实现范围。复杂脚本、汇总、条码、多栏、嵌套报表及跨表参数仍逐项列明，不能以几何预览或本轮分组能力代替完成。校样不增加打印次数，不伪造设备成功。

## 后续顺序与剩余数

1. 55处原查询差异仍全部登记：3处已有明确替代、52处待实现。其中17处缺列、12处缺本地对象、23处依赖外部来源。继续逐查询确定原单位及来源，不能用未知数量填零或删掉原筛选。
2. 40条跨表复制：本轮7条已有显式采购转单；11条缺报价来源视图、2条缺目标字段、3条配置不完整、17条财务暂缓。继续处理报价来源的可证明投影、旧按钮时机及主从保存。
3. 自动时机仍需逐入口处理GenerateTime、IsEnForceExpress、RelyRule、EditSQL/UpdateSQL及主从批次保存；不因为采购一条公式或加色一条自动链补齐就整体标完成。13组残缺上下文过滤和27处未绑定身份/续行配置继续保留。
4. 继续实现原打印的计算字段、汇总、脚本、条码、多栏及跨表绑定，逐模板进行非空验证。原纸张和真实打印机验收单独进行。
5. 开发项满足对应非空验证后再做一致时点的历史对账与现场验收。完整入口开发完成0、完整入口历史对账完成0、现场验收完成0的现有统计不因本轮局部功能完成上调。

## 52处尚不能运行的查询

|入口|旧库核验分类|当前代码差异|
|---|---|---|
'''
    for row in unresolved:
        document+='|'+row['entry']+'|'+row['category']+'|'+row['error'].replace('|','／').replace('\n',' ')+'|\n'
    document+='\n完整日志、代码哈希及只读元数据见[本轮验证记录](erp-phase6-continuation-verification-20261017.json)。\n'
    (DOCS/TITLE).write_text(document,encoding='utf8')
    exceptions='''## E174～E178：第六阶段查询、转单、自动保存与分组打印续项

详细代码范围、验证和剩余清单见[续项记录](2026-10-17第六阶段查询转单及分组打印续项.md)。以下均未宣称历史全量对账或现场验收完成。

### E174 缺列查询明确替代与原异常连接

三处入口的7个展示字段在当前旧库已不存在，现明确返回NULL并显示来源缺失。保留qry_CraftPreCheckJobSheet的DISTINCT、坯布销售退回原头表自身连接产生的重复组合，以及收发查询最后LEFT JOIN中的1=2。没有把未知列改成0，没有悄悄修正连接。剩余52处查询仍未实现运行。

### E175 采购转到货通知及目标字段限制

原7列复制已接到显式选择采购明细的转单动作；不去重，逐行记录来源快照，整批事务保存。旧客户端按钮选择顺序未证明。采购物料为空但目标不允许NULL、字段超长或超精度等不能原样转入的行，明确报来源及原因，整批不采用，原行保留；不补假代码、不跳过异常行。报价来源视图缺失及两个目标字段缺失仍待复刻。

### E176 加色报工逐游标候选替换留档

原先仅取最后候选生成报工改为全部候选逐次执行，中间被替换的WProcess、JobShiftEmp、WProcessStep均留档。撤销恢复本次之前的活动业务。原游标无ORDER BY，采用原行ID顺序属于明确顺序替代；编号继续采用项目序列，不能宣称还原过去毫秒时间戳。

### E177 打样任务明细A分组分页及排序差异

新增CustomerID单层分组、组前分页及同组跨页填数校样；重复行、NULL、空字符串保留。文本比较采用Unicode原值，旧客户端区域排序待核对。校样模板2份、完整原打印0份；真实纸张、字体及打印机尚未验收，复杂打印项未跳过。

### E178 采购金额保存计算与原GenerateTime枚举缺失

PurDetail.Amount=[Qty]*[Price]的表达式已核对，但GenerateTime=0的客户端枚举定义未取得。当前在新增或数量/价格修改时计算，显式Amount（含NULL）优先，历史原值不自动覆盖。该保存时机作为合理实现公开记录，不据此推断其余GenerateTime枚举，不把异常手工金额清洗成计算值。
'''
    replace_section(DOCS/'旧ERP复刻异常与合理实现说明.md','phase6-continuation-exceptions',exceptions)
    print(json.dumps({'tests':tests,'query_counts':evidence['query_status_counts'],
        'proof_templates':runtime['counts']['fixed_proof_templates']},ensure_ascii=False))


if __name__ == '__main__':main()
