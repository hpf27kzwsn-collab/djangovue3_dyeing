"""成品单位、疵点原式与打印复核；只将真实证据写入盘点。"""
import base64
import gzip
import hashlib
import importlib.util
import re
from collections import Counter
from datetime import datetime
from sync_phase6_local_chains import ROOT,DOCS,read,save,digest
from sync_phase6_continuation import replace_section

TITLE='2026-10-17第六阶段单位疵点与原打印复核续项.md'
EVIDENCE='erp-phase6-units-rules-verification-20261017.json'


def main():
    previous=read('docs/erp-phase6-conditions-dispatch-verification-20261017.json')
    runtime=read('docs/erp-phase6-runtime-review-20261017.json')
    support=read('backend/plugins/erp_base/source_phase6_query_support.json')
    live_dir='.runtime-temp/phase6/units-parameters-evidence/'
    live=read(live_dir+'query-metadata.json')
    profile=read(live_dir+'source-units-profile.json')
    structure_path='.runtime-temp/phase6-live-units-authorized-20261017/structure-and-logic.json'
    structure=read(structure_path);old=read('.runtime-temp/phase6-live-20261017-current/structure-and-logic.json')
    same={k:structure[k]==old[k] for k in ['fields','modules','ui_tables','ui_fields']}
    assert all(same.values()),same
    errors=[r for r in live['queries'] if r.get('error') or any(c.get('error_number') for c in r.get('columns',[]))]
    assert len(errors)==len(live['queries'])==36
    templates=__import__('json').loads(gzip.decompress((ROOT/'backend/plugins/erp_base/source_phase6_templates.json.gz').read_bytes()))
    stored=Counter((r['RptID'],hashlib.sha256(base64.b64decode(r['Template'])).hexdigest().upper() if r['Template'] is not None else None,
                    hashlib.sha256(base64.b64decode(r['TemplateXml'])).hexdigest().upper() if r['TemplateXml'] is not None else None) for r in templates)
    current=Counter((r['RptID'],r['template_sha256'],r['xml_sha256']) for r in live['print_hashes'])
    assert current==stored,'原打印摘要变化，需重新核对'
    log='.runtime-temp/phase6/units-rules-regression.log'
    match=re.search(r'Ran (\d+) tests in ([\d.]+)s\s+OK',(ROOT/log).read_text(encoding='utf8'))
    assert match,log
    targeted='.runtime-temp/phase6/units-rules-final-targeted.log'
    final=re.search(r'Ran (\d+) tests in ([\d.]+)s\s+OK',(ROOT/targeted).read_text(encoding='utf8'))
    assert final,targeted
    build='.runtime-temp/phase6/units-rules-frontend.log'
    assert 'built in' in (ROOT/build).read_text(encoding='utf8')
    spec=importlib.util.spec_from_file_location('automatic',ROOT/'backend/plugins/erp_base/source_phase6_auto_values.py')
    automatic=importlib.util.module_from_spec(spec);spec.loader.exec_module(automatic)
    auto_entries=len(automatic.AUTO_ENTRIES);auto_targets=sum(len(automatic.generated_fields(n)) for n in automatic.AUTO_ENTRIES)
    assert (auto_entries,auto_targets)==(48,70)
    assert runtime['counts']['fixed_proof_templates']==5
    unresolved=previous['unresolved_queries']
    assert {r['entry'] for r in unresolved}=={r['name'] for r in live['queries']}
    schema=read('.runtime-temp/phase6/final-schema-check.json')
    schema['fresh_readonly_snapshot_comparison']=same
    schema['snapshot_comparison_note']='本轮成功只读读取旧库，新快照与前轮fields/modules/ui_tables/ui_fields完全一致；旧结构与新模型检查是不同证据。'
    files=['backend/plugins/erp_base/'+n for n in ['source_phase6_auto_values.py','source_phase6_print_rules.py',
        'source_phase6_rendering.py','source_phase6_date_format.py','tests/test_source_phase6_units_rules.py']]
    evidence={
        'verified_at':datetime.now().astimezone().isoformat(),'development':'部分完成',
        'query_status_counts':dict(Counter(v['query_state'] for v in support.values())),
        'original_query_differences':55,'explicit_query_reconstructions':previous['explicit_query_reconstructions'],
        'new_query_reconstructions':[],'unresolved_queries':unresolved,'unresolved_nonfinancial':35,
        'unresolved_nonfinancial_categories':previous['unresolved_nonfinancial_categories'],
        'automatic_formula_entries':auto_entries,'automatic_formula_targets':auto_targets,
        'new_formula_entries':['ProdOutRecord','ProdOutRecordUpdate','QC_RecordDefect','QueryRecordDefect','QueryRecordDefect2'],
        'new_formula_targets':11,'new_transfer_variants':[],
        'runtime_counts':runtime['counts'],'field_copy_status_counts':runtime['field_copy_status_counts'],
        'tests':{'count':int(match[1]),'seconds':float(match[2]),'result':'passed','log':log,'sha256':digest(log),
            'scope':'20个模块扩大回归，含本轮12项；并非全项目测试或历史数据对账'},
        'final_targeted':{'count':int(final[1]),'seconds':float(final[2]),'result':'passed','log':targeted,'sha256':digest(targeted),
            'note':'最后日期格式及同名格式规则引用区分修正后的针对性复验，不累加到独立测试总数'},
        'frontend':{'result':'typecheck_and_build_passed','log':build,'sha256':digest(build),'note':'既有大分包提示保留'},
        'schema':schema,'old_sql_readonly_metadata':live,
        'old_sql_this_run':{'status':'readonly_connected','service_status':'Running','database':'Textile_GXHFRS',
            'note':'最初受限会话SSPI失败；Windows认证只读重试成功。36条原SELECT仅描述结果集，不执行原业务过程。',
            'fresh_structure_at':structure['captured_at'],'original_print_hashes_equal':True,'templates_compared':len(templates)},
        'source_profile':profile,'source_profile_reconciliation':'两个本次目标原表为0行，不构成公式历史样本对账通过',
        'fresh_structure_source':{'path':structure_path,'sha256':digest(structure_path)},
        'print_validation':'H023闲置规则保留，原高度不足仍报差异；400高度测试副本只验证填数/重复行，不是修改原纸张；R001占位库存继续未完成。',
        'whole_entry_development_completed':0,'whole_entry_historical_reconciled':0,'field_accepted':0,
        'historical_import_rows_this_run':0,'files_sha256':{p:digest(p) for p in files}}
    save('docs/'+EVIDENCE,evidence)
    text=f'''# 第六阶段单位、疵点与原打印复核续项

日期：2026-10-17。承接35处非财务查询余项。财务暂缓、不新增旧erpID、不跳过异常和重复数据。

## 当前结果与三类完成标准

**第六阶段仍为部分完成，35处非财务查询没有减少。** 本轮新增5个入口11条自动公式：成品出仓细码公斤/磅4字段×2入口，以及疵点积分1字段×3入口；累计48个入口70个自动目标字段。补原日期格式和闲置格式规则识别；H023纸张高度、R001库存占位的新发现单独列明。本轮没有新增转单动作，既有采购、报价转单随扩大回归验证。

|事项|开发与必要验证|历史数据对账|现场验收|
|---|---|---|---|
|成品出仓细码单位换算|原2入口8公式接入保存service，NULL、未知单位、负数、重复及原字段容量测试通过|本轮旧ProdOutRecord为0行，无历史公式样本可对账|单位使用习惯、自动时机未验收|
|疵点积分|原3入口3公式，正积/负积/NULL、显式值和接口重复记录测试通过|本轮旧RecordDefect为0行，无历史公式样本可对账|录入、审核、报表结果未现场验收|
|原打印日期格式|数字年月日、时分秒、引号及转义字面量和业务时区通过|未与旧客户端输出逐项核对|字体/纸张未验收|
|H023紧筒排产|闲置5条格式规则可识别并保留；原纸张高度不足，接口明确报告|原XML/模板摘要一致；不是历史输出对账|原纸张、裁切、缩放仍待核对|
|R001坯布进出存|检出原查询数量全为客户端待填0，继续阻止真实库存校样|缺原动态填数及期间来源，未完成|未完成|
|35处非财务查询|原库重新编译描述，35处仍报错，缺失来源逐项保留|结构/原式核查不是业务数据对账|未完成|

扩大回归{evidence['tests']['count']}项通过（{evidence['tests']['seconds']}秒，20个模块，含本轮12项）；最后日期格式及同名格式规则引用区分修正后针对性复验{evidence['final_targeted']['count']}项通过，不重复累计。前端类型检查/构建、Django检查、迁移检查通过，既有大分包提示保留。仍766个ERP模型、655个原表模型、12606个原字段，额外旧erpID为0。本轮新增迁移0、历史导入0。

完整旧入口级别的开发完成0、历史数据对账完成0、现场验收完成0；上述局部能力通过测试单列记录。290条原打印仍5份填数校样、256份XML运行差异、29份缺XML、0份完整原打印。

## 本轮旧库只读实查

用户启动SQL Server后已成功只读连接。最初受限会话Windows认证出现SSPI错误，换用可用Windows认证上下文后成功；没有执行旧业务过程或业务写入。

原库快照时间：{structure['captured_at']}。共有690个表、13268个物理列、732个过程/视图等模块、1682个界面入口及48962行界面字段配置。它们是旧库全结构统计，包含本期暂缓内容，不能与新项目655个原表模型直接等同。

本轮fields、modules、ui_tables、ui_fields与前轮快照完全一致；290份原模板/原XML的摘要也与项目留档一致。对当前36条未解决原SELECT进行结果集编译描述，36条仍有错误，其中35条非财务、1条FARSumMainMoney财务暂缓。

当前实例除系统库之外只有Textile_GXHFRS；sys.servers只有本机，无链接服务器。这证明当前实例未提供清单里的外部来源，不代表那些现场系统从来没有存在。

本轮仅对ProdOutRecord和RecordDefect补只读数据概况，两表均0行。重复组合统计为0组是空表结果，**不能推断旧业务从无重复或公式没有差异**。新实现用测试数据验证重复、负值、NULL和未知代码，历史对账状态仍为未完成。

## 成品细码原单位公式

入口ProdOutRecord、ProdOutRecordUpdate，共用原ProdOutRecord表；不增加字段，不改源单位。

|目标字段|原规则|
|---|---|
|GKg|ISNULL(GUnit,1)=1时取GrayQty，否则GrayQty÷2.2046|
|GPound|ISNULL(GUnit,3)=3时取GrayQty，否则GrayQty×2.2046|
|PKg|PUnit=1时取WeightQty，否则WeightQty÷2.2046|
|PPound|PUnit=3时取WeightQty，否则WeightQty×2.2046|

**同样是空单位，原式的处理并不一致。** GUnit=NULL、GrayQty=5时，GKg和GPound都为5；PUnit=NULL、WeightQty=5时，PKg=2.27、PPound=11.02。两者不能人为统一。未知代码99按原IIF的else分支处理，源代码99保留；负数量照原式计算，不取绝对值。数量NULL则对应结果保留NULL。

新增或修改对应数量/单位时计算，显式目标值（包括NULL）优先；无关字段修改不重算，历史来源行不重算。原目标为decimal(6,2)，按原字段两位精度及项目既有ROUND_HALF_UP保存。原公式没有提供强制计算/生成时机证据，因此不宣称新保存时机已等同旧客户端。

例如GrayQty=5000、GUnit=1，计算GPound=11023超过原字段最大9999.99：报告容量错误、整笔不半存，不截断成9999.99。明确将GPound设为NULL仍可保存GrayQty=5000、GKg=5000；来源原值不丢弃，不能把NULL当成已算好的重量。此处理为已验证的明确录入方式，见E211。

## 疵点积分原公式

QC_RecordDefect、QueryRecordDefect、QueryRecordDefect2都按原式：`IIF(IsNull([Dots]*[Times],0)>0,[Dots]*[Times],0)`写SumDots。它属于质量业务，不是财务。

Dots=2、Times=3得6；Dots=-2、Times=3得0；Dots=-2、Times=-3仍得6。负输入原值保留，不自动改成正数。任一输入NULL时结果为0，这是原式明确要求，不是对未知数据任意补0。

显式SumDots=NULL或手工分数优先；不重算历史行。同条码、同疵点序号的重复记录分别保存，接口验证两条记录都存在；不以条码自动去重。旧头汇总、其他质量链仍沿用现有逻辑，本轮不把一个明细公式当成整条质量链完成。

## 原打印规则、日期及尚未复刻部分

格式规则库里的定义只有被控件/区段引用才会生效，依据见[DevExpress FormattingRule说明](https://docs.devexpress.com/XtraReports/DevExpress.XtraReports.UI.FormattingRule)。H023存在5条定义，但没有引用，原定义与模板字节完整保留；不因这5条闲置定义阻止其余填数。真实规则引用、无法定位的规则引用继续列为待实现，不能静默忽略。打印结果附实际引用/未引用清单。

**H023不能因此升级为原版式可打印。** 其原PageHeight=350、上下边距10和5（单位为0.1毫米），明细高度超过335的可用高度。现在静态核查就明确发现此差异，实际接口仍报告纸张高度不足。测试仅把内存副本PageHeight改为400验证取数：保留原JR.SheetNo=JR.JobSheetNo连接条件，2条排产原行与2条工卡连接仍得到4条输出，不擅改原连接或去重。测试副本不写入原模板，不记新增原校样，不增加打印次数。原纸张裁切/缩放行为尚不能复刻，见E213。

日期格式支持原数字年月日/时分秒、单/双引号字面量、反斜线转义；例如`yyyy'年'M'月'd'日'`输出“2026年1月2日”。有时区的时间先转业务本地时间，单纯日期的时分秒为00:00:00。未实现的区域星期/月名、单字符标准格式和百分号标记明确列错，不输出看似正确的字母。语义依据见[Microsoft自定义日期格式说明](https://learn.microsoft.com/en-us/dotnet/standard/base-types/custom-date-and-time-format-strings)；旧客户端区域配置仍未核对。

**R001不只是缺STARTDATE。** GrayStockInAndOut的LastRemain、CurrentIn、CurrentOut、CurrentTOut、Remain数量全部是原SQL的0占位，旧客户端实际期间和退料分类填数来源未找回。本轮不把今日填到STARTDATE，也不把占位0当库存余额。原查询、版式及来源台账继续保留，需同时补真实数量和期间参数后才可运行原校样，见E214。此打印差异不从35查询数量中扣除。

## 35处查询逐项保留

全部1682入口仍为1519空夹具执行通过、108财务暂缓、36未解决、19明确替代。原55差异全保留；35处非财务未解决仍是11缺列、2缺本地对象、22缺外部来源。

|原入口|缺失来源/字段|本轮旧库编译|历史对账|现场验收|
|---|---|---|---|---|
'''
    dependencies={r['entry']:r for r in read('docs/erp-phase6-query-dependencies-20261017.json')['entries']}
    indexed={r['name']:r for r in live['queries']}
    for row in unresolved:
        if row['scope']!='本期保留':continue
        name=row['entry'];d=dependencies[name];q=indexed[name]
        missing='；'.join([*d['external_sources'],*d['missing_objects'],*d['missing_fields']]).replace('|','／')
        numbers=[q['error_number']] if q.get('error_number') else sorted({c['error_number'] for c in q['columns'] if c['error_number']})
        text+=f"|{name}|{missing}|仍报错：{','.join(map(str,numbers))}|未完成|未完成|\n"
    text+='''
## 后续顺序

1. 查询来源：补WPProcess、原能耗价格实体和能耗缺列；继续寻找两类库存账页及R001的客户端分类填数。所有原表达式和字段都保留，不以空表、未知单位或固定0伪造结果。
2. 外部链：按逐项清单恢复TFEMS、TF_METER、WeighingSystem、ReportServer、Link_Pclbase和CCS的真实定义与对应。当前实例没有这些来源，现有只读结构不能证明它们的字段、连接和历史数据。
3. 自动与转单：继续27条未绑定身份/续行、13组残缺过滤、40条原复制配置和216处事件；现有明确办理动作不等于原自动时机。成品细码、疵点新增公式也不抵消这些数量。
4. 打印：先补真实数据来源与已明确的固定版式，再逐模板处理脚本、动态高度、多层分组、子报表、条码、实际格式规则。H023原纸张差异与R001动态填数单列，不跳过。
5. 历史和现场：有真实原样本后按旧表原主键、明确时点逐行核对，包括NULL、负数、重复及逆向业务。开发夹具、空表统计和模板摘要相等都不能代替历史对账或现场验收。
'''
    text+='\n证据：['+EVIDENCE+']('+EVIDENCE+')；[异常E211～E215](旧ERP复刻异常与合理实现说明.md)。\n'
    (DOCS/TITLE).write_text(text,encoding='utf8')
    section=f'''## 第六阶段当前状态：单位、疵点与原打印复核（2026-10-17）

本节为最新口径，下方保留历史记录。见[{TITLE}]({TITLE})和[本轮验证证据]({EVIDENCE})。

本轮补成品细码公斤/磅和疵点积分5入口11自动公式，累计48入口70目标；补日期字面量、闲置格式规则识别及固定纸张高度核查。H023仍缺原裁切/缩放设置，R001缺库存动态填数和期间来源；没有新增完整原打印。本轮{evidence['tests']['count']}项扩大回归及最后{evidence['final_targeted']['count']}项针对性复验通过，后者不重复计数；前端、模型、迁移检查通过。未新增旧erpID，历史导入0。

**第六阶段仍部分完成，35处非财务查询未减少（11缺列、2缺本地对象、22缺外部来源）。** 旧SQL服务已启动，本轮只读成功；36条原查询含1财务暂缓仍全部编译报错。新结构与前轮一致，290份原模板摘要一致。两个本次公式目标原表为0行，不计历史对账通过。

完整入口开发完成、历史对账完成、现场验收完成仍分别0。290原打印仍5校样、256 XML运行差异、29缺XML、0完整复刻。27条未绑定身份/续行、13组残缺过滤、40条复制配置、216处事件继续保留。异常E211～E215已汇总。'''
    targets=[DOCS/'染色ERP后续开发方案.md',DOCS/'2026-10-16染色ERP剩余工作全量盘点清单.md',
        *DOCS.glob('2026-10-1*第六阶段*.md')]
    for path in dict.fromkeys(targets):
        if path.name!=TITLE:replace_section(path,'phase6-units-rules-current',section)
    inventory=read('docs/erp-remaining-inventory-20261016.json')
    current={k:evidence[k] for k in ['query_status_counts','runtime_counts','field_copy_status_counts','unresolved_nonfinancial',
        'unresolved_nonfinancial_categories','automatic_formula_entries','automatic_formula_targets']}
    current.update(evidence=EVIDENCE,document=TITLE,development='部分完成',historical_reconciliation='未完成',field_acceptance='未完成')
    inventory['phase6_units_rules_20261017']=current
    exceptions=[
        ('成品公斤磅原公式的不对称NULL与字段容量','两入口8原公式已接入。GUnit=NULL让GKg/GPound均保留GrayQty，PUnit=NULL分别走除/乘2.2046；未知码、负数原样保留。decimal(6,2)超范围明确报错，显式NULL可保留原输入，不截断或跳行。旧客户端时机未验收。'),
        ('疵点正积规则及空原表核验','三入口按正乘积取值否则0，负负得正、负输入及重复条码不删除，显式值和历史值保留。本次ProdOutRecord、RecordDefect均0行，没有历史样本，不把空表统计计作公式历史对账通过。'),
        ('H023闲置规则与原纸张高度不足','5条格式规则未引用仍保留；已引用或未知引用仍待实现。原纸张高度350减上下边距后容不下明细，继续报差异。400高度内存副本仅测试4条重复连接输出，不修改原模板、不增加校样/打印完成数。'),
        ('R001占位库存与原日期格式','R001缺STARTDATE并且全部数量是客户端待填0，不能打印成真实库存；缺期间、结存及退料分类来源。数字日期/引号/转义已支持，区域名字和未实现格式报差异，旧输出待核对。'),
        ('旧库已启动后的三十五处查询复核','只读成功，36条未解决原查询含1财务仍编译报错。旧结构和290份原模板摘要相同，当前实例没有外部数据库/链接。35处仍无可执行替代，外部、缺列、异常及不常用业务继续保留，不冒充历史或现场完成。')]
    axis=inventory['axes']['新旧系统差异及处理情况'];md='## E211～E215：单位、疵点及原打印复核\n\n见['+TITLE+']('+TITLE+')。\n\n'
    for number,(name,reason) in enumerate(exceptions,211):
        md+=f'### E{number} {name}\n\n{reason}\n\n'
        item={'id':'E'+str(number),'name':name,'status':'部分完成','reason':reason,'related_sql':[],
            'source':'docs/旧ERP复刻异常与合理实现说明.md'}
        found=next((n for n,r in enumerate(axis) if r['id']==item['id']),None)
        if found is None:axis.append(item)
        else:axis[found]=item
    inventory['counts']['新旧系统差异及处理情况']=dict(Counter(r['status'] for r in axis))
    replace_section(DOCS/'旧ERP复刻异常与合理实现说明.md','phase6-units-rules-exceptions',md)
    review=read('docs/erp-phase6-review-20261016.json');review['units_rules_20261017']=current
    review['current_review_at']=evidence['verified_at']
    inventory['phase6_review']['counts']=review['counts'];inventory['phase6_review']['current_evidence']='docs/'+EVIDENCE
    save('docs/erp-phase6-review-20261016.json',review);save('docs/erp-remaining-inventory-20261016.json',inventory)
    print({'tests':evidence['tests']['count'],'unresolved_nonfinancial':35,'automatic_entries':auto_entries,'automatic_targets':auto_targets,'document':TITLE})


if __name__=='__main__':main()
