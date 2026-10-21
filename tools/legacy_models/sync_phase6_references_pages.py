"""保养引用和分页续项：局部能力、完整入口、历史对账及现场验收分别计数。"""
import re
from collections import Counter
from datetime import datetime
from sync_phase6_local_chains import ROOT, DOCS, read, save, digest
from sync_phase6_continuation import replace_section

TITLE='2026-10-17第六阶段保养领料细码复核与分页打印续项.md'
EVIDENCE='erp-phase6-references-pages-verification-20261017.json'


def main():
    support=read('backend/plugins/erp_base/source_phase6_query_support.json')
    runtime=read('docs/erp-phase6-runtime-review-20261017.json')
    previous=read('docs/erp-phase6-period-stock-verification-20261017.json')
    dependencies=read('docs/erp-phase6-query-dependencies-20261017.json')
    live=read('.runtime-temp/phase6/references-evidence/query-metadata.json')
    assert live['print_hashes']==previous['old_sql_readonly_metadata']['print_hashes']
    assert len(live['queries'])==55
    assert all(r.get('error') or any(c.get('error_number') for c in r.get('columns',[])) for r in live['queries'])
    log='.runtime-temp/phase6/references-regression.log'
    match=re.search(r'Ran (\d+) tests in ([\d.]+)s\s+OK',(ROOT/log).read_text(encoding='utf8'))
    assert match,log
    build='.runtime-temp/phase6/references-frontend.log'
    assert 'built in' in (ROOT/build).read_text(encoding='utf8')
    unresolved=[{'entry':n,'category':v['live_original']['category'],'error':v['error'],
        'scope':'财务暂缓' if n=='FARSumMainMoney' else '本期保留'} for n,v in support.items() if v['query_state']=='unresolved']
    replacements=[n for n,v in support.items() if v['query_state']=='reconstructed_missing_projection']
    schema=read('.runtime-temp/phase6/final-schema-check.json')
    schema['snapshot_comparison_note']='全量结构相等引用本日较早保存快照；本轮重新只读核查55条原查询元数据和290份打印摘要。'
    files=['backend/plugins/erp_base/'+n for n in [
        'source_phase6_reference_queries.py','source_phase6_reconstructions.py','source_phase6_query_support.json',
        'source_phase6_transfers.py','source_api.py','source_phase6_auto_values.py','source_phase6_forms.py',
        'source_phase6_rendering.py','source_phase6_print_rules.py','source_phase6_page_info.py',
        'source_phase6_layouts.py','tests/test_source_phase6_references_pages.py']]
    evidence={'verified_at':datetime.now().astimezone().isoformat(),'development':'部分完成',
        'query_status_counts':dict(Counter(v['query_state'] for v in support.values())),
        'original_query_differences':len(unresolved)+len(replacements),'explicit_query_reconstructions':replacements,
        'new_query_reconstructions':['MachineCarePlanArticle','GrayInRecord_Test'],
        'extended_query_reconstructions':['qry_MachineArticle'],
        'unresolved_queries':unresolved,'unresolved_nonfinancial':sum(r['scope']=='本期保留' for r in unresolved),
        'unresolved_nonfinancial_categories':dict(Counter(r['category'] for r in unresolved if r['scope']=='本期保留')),
        'automatic_formula_entries':36,'automatic_formula_targets':43,
        'new_formula_entries':['ArticlePurApplyDetail','StuffPurApplyDetail','ArticleStockAdjustDetail','StuffStockAdjustDetail'],
        'runtime_counts':runtime['counts'],'field_copy_status_counts':runtime['field_copy_status_counts'],
        'tests':{'count':int(match[1]),'seconds':float(match[2]),'result':'passed','log':log,'sha256':digest(log),
            'scope':'17个模块扩大回归，含本轮12项；不是全项目重跑或历史导入数量'},
        'frontend':{'result':'typecheck_and_build_passed','log':build,'sha256':digest(build),'note':'保留既有分包体积大于500kB提示'},
        'schema':schema,'old_sql_readonly_metadata':live,'old_print_hashes_equal_previous':True,
        'print_validation':'页汇总、页码日期、组/页不同范围及纯尾页使用合成模板验证；原4份校样回归，无新增完整原模板、无像素外观或打印机验收。',
        'whole_entry_development_completed':0,'whole_entry_historical_reconciled':0,'field_accepted':0,
        'historical_import_rows_this_run':0,'files_sha256':{p:digest(p) for p in files}}
    assert evidence['unresolved_nonfinancial']==36 and len(replacements)==18
    assert runtime['counts']['fixed_proof_templates']==4
    save('docs/'+EVIDENCE,evidence)
    content=f'''# 第六阶段保养领料、细码复核与分页打印续项

日期：2026-10-17。承接上一轮38处非财务查询余项。财务暂缓，未新增旧erpID，未导入历史数据；重复、负数、孤立关联和明确NULL继续保留。

## 当前结论与计数口径

**第六阶段仍为部分完成。本轮没有把任何完整旧入口标记为开发完成。** 两处新增“现存记录明确关联查询”，一处已承接查询补保养分支。旧导入暂存表、保养耗用表仍缺失，所以不能说这两个业务已经完整恢复。

若只统计“尚无可执行替代查询”，非财务数量从38变为36：11处缺列、2处缺本地对象、23处缺外部来源。原55处差异一条未删除，累计18处明确替代、37处未解决（其中FARSumMainMoney为财务暂缓）。原始SQL与编译错误继续保留。**36不是剩余全部开发工作数量，也不表示原38处中已有两处等价完成。**

全部1682查询入口状态：1519处空夹具执行通过、108处财务暂缓、37处未解决、18处明确替代。空夹具通过、查询替代、局部能力测试通过，都不计完整入口复刻完成。

|本轮事项|开发与必要验证|历史数据对账|现场验收|
|---|---|---|---|
|保养计划配件引用|现存计划行及全部同代码资料关联已实现；重复和孤立行测试通过|缺原耗用明细；数量、行号不能恢复，未完成|未完成|
|设备配件综合查询|报修分支加保养引用分支，UNION ALL并标明来源；测试通过|不是原保养耗用统计，未完成|未完成|
|坯布细码导入入口的现存记录复核|17个原配置列映射及现存记录只读查询已实现|原外部待导入记录、导入过程仍缺失；未完成|未完成|
|保养计划明确领料|选择具体配件资料和出库表头，明确数量/单价，服务及接口测试通过|旧按钮、领料来源和耗用回写关系未证明|未完成|
|4入口8条自动公式|原NULL算式、连续计算、显式值优先及历史值保留测试通过|未对历史行重算/逐行对账|旧客户端生成时机未证明|
|页汇总、页码与日期|固定高度分页后填数；重复、负数、空值、纯尾页、跨页组汇总测试通过|未与原客户端逐页对照|纸张、字体、打印机未验收|

本轮扩大回归{evidence['tests']['count']}项通过（{evidence['tests']['seconds']}秒，17个模块），含新增12项。前端类型检查和构建通过，仍有既有大分包提示。Django检查及迁移检查通过：766个ERP模型、655个原表模型、12606个原字段、额外旧erpID为0，本轮新增迁移0、历史导入0。

## 保养配件与领料

MachineCarePlanArticle明确读取MachineCarePlanDetail，左连接p_Article。DetailNo为计划明细号，Qty和RowNo为未知NULL，Unit为所选资料对应的当前单位。没有配件代码、没有资料对应、重复代码对应不同单位的行均保留；不做合并、去重或按“异常”排除。

qry_MachineArticle保留现存MachineFaultArticleInfo报修明细分支，新增上述保养引用分支。SourceKind分别为fault_article_detail和care_plan_reference。报修Qty保留原值；保养Qty仍未知。计划同流水多表头、同代码多资料产生的所有连接行保留。保养日期取HandleDate，人员取HandlerIDs，机台取MachineID；不能据此声称原耗用量或原单位换算已恢复。

在保养计划明细上新增“保养配件领料（明确来源）”：选择目标配件出库单、具体配件资料原行，输入本次OutQty和Price；InDetailNo、StorageUnitIDs未知时可为空。资料代码须与计划引用一致，但重复代码可明确选择其中一个实际资料行，不擅自取第一条。复制ArticleID、ArticleKindID、Spec、SupplierID、MachineID、Remarks；Total采用现有原公式OutQty×Price。

动作在事务中写入ArticleOutDetail，使用现有主从保存、汇总与办理链。每次办理各生成一条明细，保留负数、NULL和重复办理。计划及资料完整快照、原单位与本次参数记录到已有业务上下文，未添加新来源ID字段。新增接口验证来源可读权限、目标新增及表头修改权限；已确认/审核的目标表头沿用现有重新办理要求。新动作是明确实现，不冒充失去来源的旧自动按钮。

## 坯布细码复核与导入边界

GrayInRecord_Test原暂存表已缺失。本轮只能展示已经存在的GrayInRecord，并按ReceSheetNo左连接全部GrayInDetail，再按SheetSeries左连接全部GrayIn；不创建虚构暂存行，也不把这份结果当成外部待导入名单。

|原配置字段|明确采用的现存来源|
|---|---|
|Area、CustJobNo、GrayID、MachineID、PreField1、PreField3、PreField5、SheetSeries|GrayInDetail对应原字段|
|CustomerID、SheetDate|GrayIn对应原字段|
|BarCode、GUnit、LengthQty、RollNo、Rolls、WeightQty|GrayInRecord对应原字段|
|StorageUnitIDs|GrayInRecord.StorageUnitID|

另列ReceSheetNo、OriReceSheetNo、OriBarCode、InputDetailCode和SourceKind，方便辨识来源。两条相同条码细码×两条同收料号明细×两个同流水表头，保留8条连接结果；另有孤立细码仍单独保留。查询连接行数不等于实际货物件数。原导入操作、暂存状态和外部数据格式仍是未完成事项。

## 自动公式与保存时机

新增四个入口、八条原公式，累计36个入口43条自动计算目标，计算继续放在service调用链。NULL变0只发生在原表达式明确写ISNULL的位置。

- ArticlePurApplyDetail、StuffPurApplyDetail：Amount = ISNULL(Price,0) × ISNULL(Qty,0)。
- ArticleStockAdjustDetail、StuffStockAdjustDetail：先算RealMoney = ISNULL(RealQty,0) × Price，再算AdjustMoney = ISNULL(RealMoney,0) − ISNULL(PaperMoney,0)，以及AdjustQty = ISNULL(RealQty,0) − ISNULL(PaperQty,0)。

例如RealQty=NULL、Price=NULL、PaperMoney=10时，RealMoney仍为NULL，AdjustMoney按原式为-10；不是把全部未知金额都强制写成0。显式传入的目标值（包括NULL）优先，修改无关字段不重算，来源历史行保留原值。原GenerateTime/强制计算时机缺少客户端证明，因此保存时计算是本项目明确实现，不表示216处事件全部验收。

## 分页汇总、页码和打印日期

固定高度分页先确定每页实际明细，再计算Page汇总、填充页码和总页数。页头/页尾使用同一页明细集合；组汇总仍用完整组，报表汇总用完整报表，不互相混用。重复行逐行参与；NULL遵守原IgnoreNullValues，负数保留。仅有组尾/报表尾的页面，Page Sum/Count为0，不重复计上一页明细。

XRPageInfo支持Number、NumberOfTotal、DateTime、None。日期只取一次校样生成时间；保留原Format文字、年月日/时分秒和占位编号。例如原模板写“当前{{0}}页/共{{0}}页”会照原式打印两个当前页码，不暗自改成总页数。原格式缺失时明确采用“当前页 / 总页数”和yyyy-MM-dd HH:mm:ss；原客户端区域默认外观仍待对照。

页信息类型及格式行为参考[DevExpress页信息定义](https://docs.devexpress.com/XtraReports/DevExpress.XtraReports.UI.XRPageInfo.PageInfo)和[格式字符串说明](https://docs.devexpress.com/XtraReports/DevExpress.XtraReports.UI.XRPageInfo.TextFormatString)。当前文档版本不能代替旧客户端实际输出核验。自定义起始页、组内重置、其他页码类型仍明确列差异。

290份原模板重新核查后仍为4份可填数校样、257份XML有运行差异、29份缺XML、0份完整复刻。本轮没有新增完整可用原模板。多层组、脚本、动态高度、子报表、条码及缺失数据绑定仍未被这次公共能力代替。只生成校样，不执行打印前业务动作、不增加打印次数、不表示设备打印成功。本轮没有浏览器像素或实机输出验收。

## 本轮38处查询逐项保留

下面按本轮起点列全38处；2处有明确现存记录查询，其原业务缺口仍保留。外部、缺表、缺列可能同时存在；分类依据原库首错，详细依赖见附表JSON。

|原入口|当前开发状态|依赖或差异|历史对账|现场验收|
|---|---|---|---|---|
'''
    deps={r['entry']:r for r in dependencies['entries']}
    for row in previous['unresolved_queries']:
        if row['scope']!='本期保留':continue
        n=row['entry'];d=deps[n]
        state='现存记录明确关联，原功能未完整恢复' if n in evidence['new_query_reconstructions'] else '尚无可执行替代'
        detail='；'.join([*d['external_sources'],*d['missing_objects'],*d['missing_fields']])
        content+=f'|{n}|{state}|{detail.replace("|","／")}|未完成|未完成|\n'
    content+='''
## 后续顺序与不能凭现有资料补全的内容

1. 本地缺失定义：DPWPProcess只剩WPProcess表名、WProcessNo主键及LabSheetNo关联配置，字段配置为空；不能把WProcess改名当成WPProcess。EnergyPrice残留Code、EndTime、EnergyKind、Flag、ID、Mnemonic、Name、Price、SequenceNo、StartTime配置，但EnergyPrice/p_EnergyPrice实体及历史价格来源均缺。待找回定义/实际输入依据后再接模型与查询。
2. 11处缺列查询：继续核对原ProcessSchedule能耗字段、机台/单位关系及vwGrayAccount、vwProdAccount客户端动态填数。完整日志是操作入口记录，未搜到对应动态SQL；当前模块快照亦未找回账页后续填数。保留全部原查询，不能把占位0作为真实收发统计。
3. 23处外部查询：当前SQL实例只有Textile_GXHFRS和系统库，没有所需外部库/链接。TFEMS、TF_METER、WeighingSystem、ReportServer、Link_Pclbase及192.168.23.254来源逐项留档。接入需要实际来源定义/连接或可验证数据；不返回空结果冒充成功。
4. 自动及转单：本轮新增明确领料，继续核对旧耗用表、导入暂存、采购选择条件、复制按钮及生成时机。27条未绑定身份/续行、13组残缺过滤、40条复制配置和216处事件继续保留，不因8条公式通过而整体升级。
5. 原打印：继续逐模板补缺失数据绑定、计算字段、多层组、事件脚本、动态高度和设备控件；4份校样仍需旧输出和真实纸张比较。不能按解析成功或公共分页用例通过计整张报表完成。
6. 历史对账与现场验收分别开展：采用一致抽取时点、明确单据范围和旧表原有主键逐行对比；异常、重复行必须包含。现场另记录真实办理、撤销、打印及设备回传。当前完整入口开发完成0、完整历史对账完成0、现场验收完成0。
'''
    content+='\n证据：['+EVIDENCE+']('+EVIDENCE+')；[逐项依赖](erp-phase6-query-dependencies-20261017.json)；[异常E195～E200](旧ERP复刻异常与合理实现说明.md)。\n'
    (DOCS/TITLE).write_text(content,encoding='utf8')
    section=f'''## 第六阶段当前状态：保养领料、细码复核与分页打印（2026-10-17）

本节为最新口径，下方前轮数字为历史记录。详见[{TITLE}]({TITLE})和[验证证据]({EVIDENCE})。

本轮增加2处现存原行明确关联查询、扩展1处保养分支、增加保养计划明确领料动作及4入口8条自动公式（累计36入口43条）；补Page汇总、页码及日期。{evidence['tests']['count']}项扩大回归、前端类型检查/构建和模型/迁移检查通过。无新增旧erpID，本轮历史导入0。

**第六阶段仍为部分完成。** 原55处查询差异全部保留：18处明确替代、37处未解决（含1处财务暂缓）；非财务“无可执行替代查询”由38变为36（11缺列、2缺本地对象、23缺外部来源）。36不是剩余全部工作数，新增2处查询也不表示原耗用及导入业务已完整复刻。完整入口开发完成、历史对账完成、现场验收完成仍分别为0。

原打印仍为4份可填数校样、257份XML运行差异、29份缺XML、0份完整复刻。27条未绑定身份/续行、13组残缺过滤、40条复制配置、216处事件仍逐项保留。异常新增E195～E200；本轮没有删除或去重异常业务数据。'''
    targets=['染色ERP后续开发方案.md','2026-10-16染色ERP剩余工作全量盘点清单.md',
        '2026-10-17第六阶段查询自动调用及原版式续项清单.md','2026-10-16第六阶段旧入口自动调用与打印核查清单.md',
        '2026-10-16第六阶段未复刻入口与打印异常明细.md','2026-10-17第六阶段字段联动与版式运行核查.md',
        '2026-10-17第六阶段查询转单及分组打印续项.md','2026-10-17第六阶段库存查询报价转单与汇总打印续项.md',
        '2026-10-17第六阶段本地收发查询与连续分组打印续项.md','2026-10-17第六阶段期间库存采购候选与组尾打印续项.md']
    for name in targets:replace_section(DOCS/name,'phase6-references-pages-current',section)
    inventory=read('docs/erp-remaining-inventory-20261016.json')
    current={k:evidence[k] for k in ['query_status_counts','runtime_counts','field_copy_status_counts','unresolved_nonfinancial','unresolved_nonfinancial_categories']}
    current.update(evidence=EVIDENCE,document=TITLE,development='部分完成',historical_reconciliation='未完成',field_acceptance='未完成')
    inventory['phase6_references_pages_20261017']=current
    for row in inventory['axes']['旧界面配置入口']:
        if row['name'] in replacements:
            row['phase6_query']={**support[row['name']],'state':support[row['name']]['query_state']}
            row['status']='部分完成';row['reason']='现存来源明确替代已验证，原耗用/导入/过滤、自动时机及真实对账未完整复刻。'
            row['development']={'status':'部分完成','reason':row['reason']};row['phase6_evidence']='docs/'+EVIDENCE
    inventory['counts']['旧界面配置入口']=dict(Counter(r['status'] for r in inventory['axes']['旧界面配置入口']))
    exceptions=[
        ('保养引用不等于保养耗用','MachineCarePlanArticle已缺失；现存计划引用可查，数量和行号保持未知。综合查询以UNION ALL保留报修及保养引用，全部重复/孤立来源保留，未恢复原耗用统计。'),
        ('细码复核不等于原暂存导入','GrayInRecord_Test缺原暂存表；以现存细码左连明细及头提供17配置列只读复核，全部同条码/同收料号连接保留。原待导入文件、暂存状态和导入过程仍未复刻。'),
        ('保养计划明确领料与旧自动按钮差异','选择具体配件资料及目标出库头，数量/单价明确提供，未知入库明细/库位可留空。事务保存、原Total公式及上下文来源快照已验证；不推断单位换算，不去重重复办理。原耗用回写与旧触发时机未证明。'),
        ('采购申请及库存调整NULL公式','新增4入口8公式，按原ISNULL位置计算，RealMoney先于AdjustMoney；Price未知时不擅自当0。显式目标含NULL优先，无关编辑不重算，历史原值保留。原客户端生成时机仍待核实。'),
        ('页汇总及页码日期的原打印边界','已补Page汇总和XRPageInfo四种类型；分页后取实际明细，尾页不重复计前页，保留原格式及错误占位。未给格式时采用明确默认文字，旧区域外观未知；多层组/脚本/动态高度等继续列差异，完整原打印仍0。'),
        ('三十八处余项与缺失来源续查','38处原入口逐项列入本轮MD；2处只有明确现存记录查询，其原功能缺口未关闭。36处仍无可执行替代，11缺列、2缺本地对象、23缺外部来源。本轮只读元数据再次确认55条原查询仍报错；完整日志未找回动态填数SQL，未伪造缺失表、价格或全零账页。')]
    axis=inventory['axes']['新旧系统差异及处理情况']
    exception_md='## E195～E200：保养领料、细码复核与分页打印差异\n\n详见['+TITLE+']('+TITLE+')。\n\n'
    for number,(title,body) in enumerate(exceptions,195):
        exception_md+=f'### E{number} {title}\n\n{body}\n\n'
        item={'id':'E'+str(number),'name':title,'status':'部分完成','reason':body,'related_sql':[],
            'source':'docs/旧ERP复刻异常与合理实现说明.md'}
        old=next((i for i,r in enumerate(axis) if r['id']==item['id']),None)
        if old is None:axis.append(item)
        else:axis[old]=item
    inventory['counts']['新旧系统差异及处理情况']=dict(Counter(r['status'] for r in axis))
    replace_section(DOCS/'旧ERP复刻异常与合理实现说明.md','phase6-references-pages-exceptions',exception_md)
    review=read('docs/erp-phase6-review-20261016.json');review['references_pages_20261017']=current
    indexed={r['name']:r for r in inventory['axes']['旧界面配置入口']}
    for row in review['entries']:
        if row['name'] in replacements:
            row['development']=indexed[row['name']]['development'];row['query']=indexed[row['name']]['phase6_query']
    review['counts']['query_execution']=evidence['query_status_counts']
    review['counts']['development']=dict(Counter(r['development']['status'] for r in review['entries']))
    review['counts']['development']['开发完成']=0
    review['current_review_at']=evidence['verified_at']
    inventory['phase6_review']['counts']=review['counts'];inventory['phase6_review']['current_evidence']='docs/'+EVIDENCE
    save('docs/erp-phase6-review-20261016.json',review);save('docs/erp-remaining-inventory-20261016.json',inventory)
    print({'tests':evidence['tests']['count'],'unresolved_nonfinancial':36,'document':TITLE})


if __name__=='__main__':main()
