"""登记当前数据库程序和入口覆盖；登记不能代替业务对照通过。"""
import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
import sqlparse

ROOT = Path(__file__).resolve().parents[2]
IMPLEMENTED_PARTS = {
    'Fn_Get_AZ': '原varchar输入/返回、字母提取及全角字符原样保留已接入；与六个同批函数合计175组SQL对照；完整排序规则仍待证明，见E102',
    'Fn_Get_NumNo': '原数字/点号提取及20字节返回已接入；全角原字不改写；175组同批函数对照，排序规则边界见E102',
    'GET_NUMBER': '原纯数字提取、100字节输入/返回已接入；175组同批函数对照，排序规则边界见E102',
    'GetNumberFromString3': '原首段、负号、小数点、50字符累加器、零返回与转换错误已接入；全角负号和全角数字分别保留；字符边界见E102',
    'SafeVarToFloat': '原varchar(1)逐字符检查、decimal(18,4)舍入、原零值/转换错误/溢出已接入；非新兜底规则；其他调用点接续见E102',
    'SafeVarToInt': '原先decimal(18,0)舍入再FLOOR/int转换已接入，12.5为13；原溢出及全角无效值保留；其他调用点接续见E102',
    'NormalizeTextFast': '原32种标点、换行替换、空格合并及XML控制字符错误已接入；特殊Unicode/XML全范围仍待证明，见E102',
    'fn_GetContinuousDate': '年/月/日/年中月/指定月五路、闰日及非正参数已接入；35组390行只读SQL一致；datetime极值及全部NULL组合仍待证明，见E102',
    'GetSysParamValue': '完整7字段参数来源及20字节名字/局部返回值已接入；348项旧函数值一致；无序多来源及全部业务调用点未标完成，见E104',
    'sp_App_sysGetSystemParams': '原8项现场参数按完整名字直接查询、10字节返回已接入；与20字节名字函数分开；其他APP调用协议见E104',
    'sp_App_S_GetDBComboListByID': '原组合编号/LIKE/NULL筛选、不排序不去重已接入；103组403行实际空筛选对照；全部排序规则及过滤边界见E104',
    'sp_App_S_GetLookUpListByID': '266项定义完整留存，其中101项资料选择按原过滤/连接/投影翻译并对照；165项复杂联查明确待办；动态附加列及NULL协议差异见E104',
    'sp_GetNewCode_HasOutput': 'yyMMdd按对象/日期计数、位数扩展、重复/负数/NULL计数及bigint表/int变量边界已接入；旧表0行，非空用隔离测试；所有单据调用点尚未替换，见E103',
    'sp_GetNewCode_HasOutputNew': 'yyyyMMdd与短日期独立计数已接入；历史计数复制采用及事务/无序差异见E103；空原表不声称非空历史编号已验收',
    'convertUnit': '原decimal(10,2)输入/返回、四种换算系数、其他组合原值及NULL已接入service与查询入口；320组实际SQL对照，见E100',
    'fn_GetDays': 'dbo/dye两版均按实库0～2047日序号、含首尾/闰日/NULL/倒序接入；日期上界溢出尚未证明等价，见E100',
    'fn_ConcatBusinessUnitID': '原员工主体及空值回退字典、100字节截断已接入；274名实际员工对照；重复员工无序差异见E101',
    'fn_ConcatBusinessUnitName': '原字典/CHARINDEX尾分隔符匹配、NULL拼接与返回长度已接入；274名实际员工对照；回退无序和字符排序差异见E101',
    'SalaryChanges_InUp': '新单Kind=3/4按原生产编号存在规则保存，其他Kind不附加检查；历史孤立行原样承接；批量无序标量按逐单办理，见E99/E101',
    'sp_App_SaveInspectionLog': '原巡检表头/方案三串左连接、重复倍增、项目替换留档与撤回已接入；修改不回写InspectDate，见E94',
    'sp_App_SaveMachineCareRecords': '原保养表头/项目生成与替换留档/撤回已接入；修改CareDate不变且ModifyDate=NULL，未臆造计划回写，见E94',
    'sp_App_GetMachineCaseProject': '直接方案/机台最新方案及原项目返回已接入；40条实际项目一致，ISNUMERIC有限模拟及无序差异见E95',
    'sp_App_GetInspectionLogBySheetSeries': '项目与IsUseMachineCase查询已接入；原表头由原模型展示，未声称旧双结果集逐列接口兼容；字面Y补项目见E94',
    'sp_App_GetMachineCareRecordsBySheetSeries': '项目与IsUseMachineCase查询已接入；原表头由原模型展示，未声称旧双结果集逐列接口兼容；字面Y补项目见E94',
    'f_splitWithRowNo': '巡检/保养反引号三串的行号、空段、去控制字符、末尾反斜线及100字节溢出已接入；其他分隔符不标全覆盖，见E95',
    'sp_App_SaveMachineFaultBill': '报修新增/修改、机台部门赋值、附件绑定及流转留档/撤回已接入；原通知保留待投递事实，未接旧APP发送，见E96/E98',
    'sp_App_CheckMachineFaultBill': '原描述/机台/可选分类分组检查及后项覆盖已接入；注释检查不新增，见E96',
    'sp_App_GetFaultActions': '原报修人/维修工/管理者/指派权限及标准精简流程已接入；与新版合计104组真实查询一致，见E96',
    'sp_App_GetFaultActions2': '原签到文字和取消签到标志差异已接入；与普通版合计104组真实查询一致，见E96',
    'sp_App_FalutAction_Check': '原动作检查和消息覆盖顺序已接入；已注释状态检查不新增，见E96',
    'sp_App_FalutAction_Accept': '受理/指派原人员回写、申请时间和流转记录已接入，空指定人员的表头/日志差异保留，见E96',
    'sp_App_FalutAction_Commit': '提交/退回、配件非负最大轮次加1及仅-1行回写已接入；退回不清时间，见E96',
    'sp_App_FalutAction_Confirm': '确认/拒绝及精简流程拒绝也已确认已接入，见E96',
    'sp_App_FalutAction_Evaluate': '评价状态及原整数评分留档已接入，不新增0～5限制，见E96',
    'sp_App_FalutAction_Remark': '评论日志与独立评论两行均已接入，撤回留档，见E96',
    'sp_App_FalutAction_SignIn': '签到/取消签到、SeverityID及FaultID覆盖默认人员的原变量行为已接入，见E96',
    'sp_App_FalutAction_Close': '关闭/恢复/重新提交字段及逐步撤回已接入；重新提交通知来源留存，实际发送待接，见E96/E98',
    'MachineFault_Update': 'ResultID=3或包含已修的结束时间触发接入保存/确认/审核/重新办理及维修动作；按行执行与旧无序批量差异见E97',
    'ChangeIDListToEmpName': '维修分号名单调用的LIKE匹配、空姓名重置和串联已接入；无序改来源ID顺序，其他分隔符不标全覆盖，见E97',
    'sp_Get_Machine_Parameters': '本批已核对原定义及当前无远程链接；未伪造外部机台参数和接收结果，待实际来源接入，见E98',
    'V_Machine_Parameters': '本批已核对远程定义；外库数据与现场协议未取得，保留待办，见E98',
    'V_Machine_ProcessID': '本批已核对远程定义；外库数据与现场协议未取得，保留待办，见E98',
    'vw_DyeMachine': '本批已核对机台来源定义；涉及外部链路仍列待办，未当成本地p_Machine等价结果，见E98',
    'Sp_CreateShiftAndClassDetail': '原最新配置/周期/种子/换版/跨日四段已接入预览、生成、替换留档和撤回；1460条15字段重建一致；无序末组与事务差异见E90',
    'Sp_GetShiftAndClass3': '原时分首含尾不含、后段覆盖、部门机台与PATINDEX、一次365天自动生成已接入；1440组查询117行与只读SQL一致；RIGHT尾字及ClassName原义见E91',
    'qry_ProcessMachine': '原机型来源、员工名单、06近30天及复版审核两路、其他工位AA/NULL规则已接入；全候选与排除原因保留，无序与NULL效应见E92',
    'Fn_Get_Machine': 'GX07非空机台TOP1及工卡前三字符备选已接入；全部候选列示，无序采用项目ID首条，见E92',
    'New_StringSplit': 'qry_ProcessMachine分号名单调用已按去空格/内部空段/末尾分号接入；其他分隔符调用不以本批标记全覆盖，见E92',
    'DPJobSheet': '主/副卡原LIKE、状态0称料主卡赋值、原七表左连接及候选完整展示已接入；五个真实扫码结果对照通过，无序选择差异见E85',
    'DPJobStep': '正式版状态0首轮与仅指定工序号排除已接入；与Test变体分开；五组实际0步骤及隔离非空分支通过，见E85',
    'v_StuffWeightStep': '原CarryIndex排除0、四列DISTINCT与PhaseNo/StepName序号已接入；空和非空分支验证，见E86',
    'v_StuffWeightStep_LX': '原称料/阶段/明细连接、包含0桶序及原字段DISTINCT已接入；三张实际称料9行逐字段对照通过，见E86',
    'v_StuffWeightStep_TO_LX': '原中控料单/缸号、第一同程序阶段及S/A默认槽号已接入；实际5行逐字段一致，不冒充中控写入，见E86',
    'fn_GetPhaseNo': '同流水/程序TOP1阶段字符串已接入TO_LX；无序按来源ID首条，全部候选留明，见E86',
    'GetPropOfJobShiftEmp': '工号/流水截断、两位变量后四位比例已接入；30组真实函数值一致；零分母及溢出NULL留明，见E87',
    'UpdateJobShiftEmp': '创建时间范围、含费率/备注/修改人隐藏分组、异班组重复插入、替换留档与逐步撤回已接入；审核后钩子接入，两个实际排班1404组对照通过，见E87',
    'ShiftArrange_Update': '原12小时边界审核、未来日期原行为、班组人员同步、较晚排班反审限制已接入；最新必填流水号及重复异常留档差异见E87',
    'V_Progs_Step': '外部中控七表连接原定义已核对；当前本地证据无七表完整数据，不伪造返回/回执，仍待实际中控接入，见E88',
    'QuoteDetailInsert': '客户/色号/物料原连接COUNT>1已接入保存检查；重复异常按要求照存并留检查事实，差异见E82',
    'QuoteDetailModify': '原COUNT>2及NOT UPDATE(RightStatus)审核限制已接入普通保存、计算及调价回写；同值UPDATE也检查，孤立明细原绑定保留；重复不拒存，见E82',
    'QuoteDetail_Del': '原RightStatus=10禁止删除已接入；批量逐条保护与原无序标量区别见E82',
    'DyeDipsRecordCheckerID': '2021-04-18起EmpID打样次数来源已接入，未替换为CheckerID，见E83',
    'DyeDipsRecordBulkCheckerID': 'Times>1及2021-04-18起CheckerID返打责任来源已接入，见E83',
    'Sp_DyeDipsRecord_CheckerID1': 'S按EmpID、R按CheckerID、首尾包含、三位比值乘100及零S原0率已接入；当前实际0组对照一致，非空经隔离测试，见E83',
    'vw_DyeDipsRecord_EmpID': '主EmpID/A版及复版1～6、7:30换日、原float舍入已接入；qry产量与EmpID1变体独立，原空结果和EmpID1非空结果已核对，见E83',
    'fn_GetDay_DyeDipsRecord_EmpID': '开始包含/结束不含、SDate分组COUNT及无行NULL已接入；原工作日统计和明确逐日展开分别保留，见E83',
    'DPJobStep_Test': '原2类选卡、LIKE、阶段/曲线、COUNT(RealValue)、班组比较与跨层子查询已接入；只读SQL证明跨曲线影响；当前阶段曲线连接0、实际工卡0行对照通过，未匹配来源保留，见E84',
    'fn_GetColorNumPrice': '数字色号原报价/最新调价已接入，不增加客户物料过滤；NULL及无序候选见E78',
    'fn_GetPriceListVat': '前两条调价日期分支、20公斤区间逐行累加已接入，NULL/负价/重复区间保留，见E78',
    'fn_GetPriceUnit': '坯布/成品80公斤区间、RC07及20位数字色号客户单位已接入，见E78',
    'fn_ColorNum_BasicsPrice': '用量/成本区间、最低价0或NULL时第二次取价、除1000已接入；48组真实SQL结果一致，见E78',
    'fn_GetPackPrice': '工序Price直接返回已接入；18组真实SQL结果一致，见E78',
    'fn_GetPackQtyPrice': '同源p_Process.Price已接入，非另算数量价，见E78',
    'fn_GetDyePrice': '原p_DyeCurve.MaxValue实际返回已接入；21组真实SQL结果一致，见E78',
    'fn_GetPriceRemark': '原数字色号等于原参数、NULL重置及varchar100拼接已接入，见E78',
    'fn_GetJObSheetNoAttePrice': '基础另收费、客户空物料/通用空物料优先顺序已接入；未赋值ProdID原分支保留，见E78',
    'fn_GetJObSheetNoAttePriceUnit': '另收费单位、NULL和空物料优先顺序已接入，见E78',
    'fn_NewGetDyePrice': '六项套价、工艺加扣、ZN免价及Kind0～8已接入；12张真实工卡总价一致，重复连接与TOP1见E78',
    'fn_GetTechPrice': '出库单位4/05附加工艺、客户优先和通用价格累计已接入，含NULL及重复，见E78',
    'Sp_DyeDipsRecord': '原所选流水色深、最大成本、全库高牢度及色号/客样回写、预览/撤回已接入；双染未赋值差异见E79',
    'Sp_DyeDipsRecord1': '0.2/1色深、本白/全漂/洗水及回写/撤回已接入；全库与明确所选范围分别提供，见E79',
    'Sp_DyeDipsRecord2': '旧阈值、原全库/明确所选范围及回写/撤回已接入，见E79',
    'Sp_DyeDipsRecord10': '旧色深、染程数及特殊色深双染0/1/2、前段客样更新及撤回已接入，NULL变量残值保留，见E79',
    'Sp_DyeDipsRecord22': '全库新版阈值、成本、高牢度及色号/客样回写、预览/撤回已接入，见E79',
    'Sp_DyeDipsRecord_EmpID': '2021-04-18起四人员槽位分摊及撤回已接入；零人员原除零改NULL并明列，见E79',
    'ProdTest_Add': '物料比较原结果展示；允许异常试验录入，七入口及加色保存钩子已接入，见E81',
    'sp_AuTo_Quote': '再次只读证实P_ColorNum3缺失；映射留档，未伪造替代表或自动报价，见E78',
    'sp_AuTo_RecordYield': '投坯条码资料回写、全包装条码DB2Code同步、预览及撤回已接入；整链撤销含跨卡标签恢复；无序选择按项目ID确定且保留候选，真实库当前无连接目标，动作经隔离数据验证，见E75',
    'RecordYield_EmpID': '全历史DetailNo最大PackTime、并列及员工左连接已接入；70751条真实结果与旧SQL一致，306464条未参与来源保留，见E76',
    'V_RecordYield': '原BarCode人数COUNT及12位小数截断分摊已接入；原视图和明确Guid录入口径分别保留；当前两者均0条并展示全部未匹配来源，非空/负数/重复分支经隔离数据验证，见E76',
    'Sp_WprocessBackUp': '六月前月初归档、既存备份扩大范围、触发回写和撤回已接入；ProcessNo漏写修复、原行留档及无序批量触发差异见E77；当前备份三表为空，未对开发历史库实际归档',
    'Sp_DyeRateNew': '班组直通/返修率原分组、总计及SQL比例精度已接入；含负数、NULL、零分母留档，真实SQL对照通过，见E69',
    'Sp_DyeRateNew_ColorMatching': '对色员直通/返修率及JTimes已接入；真实SQL对照通过，见E69',
    'Sp_DyeRate_ColorMatching_Query': '8点换日员工质量看板与原称料加色次数已接入，重复连接及原日期保留；取消100行截断，真实SQL对照通过，见E69',
    'Sp_DyeRate_dyeCheckout_Query': '原色级框架、班次倍增、10号汇总冲突及上月栏目错连均保留；明确修正版可选，原口径真实SQL对照通过，见E70',
    's_vwColorDepth': '原色级字典UNION ALL 10号汇总已接入，保留冲突和重复，见E70',
    'v_ColorMatching_DyeAdd': '2类RecipeType=1且对色员非空的称料单次数及8点换日已用于质量看板，见E69',
    'v_WProcess_WorkQty': '原人员/工卡/工序连接、DISTINCT及7点50分换日已接入；不匹配来源单列，1252条真实结果对照通过，见E71',
    'sp_SimpleRecordYieldQuery': '员工包装产量、品种字典连接及跨日期多值拼接已接入；字典403行已完整承接；200组真实SQL对照通过，见E72',
    'sp_RecordYieldByWinding': '络筒包装产量及单工号/多姓名原分支已接入；245组真实SQL对照通过；无序字符串和员工多行差异见E72',
    'Sp_CheckProcessRS': '重复排程核对及页面入口已接入，原重复行保留，不拼接执行SQL；未擅自统一拦截所有录入，见E73',
    'CheckProcessStatus': 'GX03装笼顺序、GX07间隔/顺序及其他工序原检查已接入；无序多候选逐项展示，调用范围待客户端补证，见E73',
    'vw_ProcessDyMachine': '排程检查使用原60天/2025-01-01范围及称料关联；最新时间并列保留全部候选，见E73',
    'T_PSD': '原未结工卡、染色状态、日期DENSE_RANK及IsNot优先逻辑已接入；81条真实序位与旧SQL一致，见E73',
    'Sp_ReworkCloth1': '布种/车间日及月累计返修已接入；05重量/06次数比例、原小计重复分母保留；零分母显示NULL并说明，见E64，待原客户端对照',
    'Sp_ReworkCloth4': '05/06综合返修计算已接入；FAR质量数量已自动映射；401条逐字段及五个月旧SQL汇总对照通过，批次来源及长度边界见E66',
    'Rework_Comparison1': '05同比计算与入口已接入；默认保留原上年连接本年来源错误，另提供明确同期修正版；FAR自动批次及边界见E65/E66，未全量原单验收',
    'Rework_Comparison2': '06同比计算与入口已接入；默认原过程口径，另提供同期修正版；FAR已按质量数量投影自动映射；原年份及明确修正版对照通过，见E65/E66，待全量原单对照',
    'Rework_Comparison3': '责任部门/班次数量长度分类已接入；原FARDetail.PreMeter在最新结构缺失，长度需明确来源；数量已自动映射，401条全部保留、无满足原责任分类记录，与旧SQL一致，见E66；未全量原单验收',
    'Sp_ReworkCloth2': '05站点月度总产量及内部/客退返修已接入；原WProcessNo重复连接、两阶段舍入、NULL和负值保留；月份边界合理差异见E61，待原客户端对照',
    'Sp_ReworkCloth3': '06站点月度总产量及内部/客退返修已接入；跨05/06同流水来源和重复字典连接完整保留；月份边界合理差异见E61，待原客户端对照',
    'RecordYield_Add': '同工卡同卷号全部活动包装替换新增及撤回已接入；原行留档、原参数复制、最新CheckNo沿用、实际入库独立及整链追溯见E56/E58；待原单对照',
    'RecordYield_INSERT': '空码新增按当前日期+五位序号补号；入口已生成或明确填写的原码保留；溢出扩位及异常尾号差异见E44，待原单对照',
    'RecordYield_': '本次包装的卷序号、JobDetailNo及GX98开工/当前工序回写已接入；保留负净重、超重和原品名，不执行全库改写，见E44',
    'RecordYieldDel': '原触发器仅查询入库计数，没有阻止/删除副作用；实称入口的实际删除限制另按WeighRecordYield钩子执行，见E44',
    'Sp_RecordYieldQuery': '包装RollNo与投坯ReceSheetNo/RollNo排序、按流水分组及重复条码全候选连接、回写与撤回已接入；无序并列/三位溢出/重复Guid按E57合理处理；明确单行采用亦可撤回，待原单对照',
    'Sp_DPSyncToCombineSheets': '称料/排程选路、0/1/2同步、全库空进度、Curr1、DPJobStep_UPDATE及GX06/GX07质量重建、JTimes/色深已接入；NULL删除不匹配、重复插入保留，差异及原单对照见E46/E50-E51',
    'Sp_JobProcessUpdate_Curr': '全库待维护工卡预览与回写、未开始/已完成/后续4与5状态已接入自动合卡；逐卡审计，无序选行确定化及变量残值差异见E51',
    'vwDyeWorkQty': '最小工序编码组、刷卡合计及最大结束时间并列、机台bit4、结束工序、加料与责任评审已接入质量重建；多行标量展开差异见E50',
    'vw_DyeWorkQtyQuer': '染色质量视图、早8点业务日及7:30至19:30班别、公斤两位与粒数截断、正染/加料/返染及缺陷统计已接入；见E50',
    'DPJobStep_UPDATE': '称料状态/类型/配方筛选、染程曲线步骤与实际WProcessStep排除已接入，剩余为0回写Status=1；不伪造实际设备步骤，见E46',
    'sp_CutGray': '明确原细码拆分、粒数汇总、选定工卡投坯同步与逐字段撤回已接入；异常量/编号/缺失列差异见E48-E49，待原单对照',
    'sp_CutGrayAfterGrayOut': '投坯细码拆分、Kg/GUnit、JobAssign与工卡重量后长度回写及撤回已接入；原多工卡标量归属改按实际来源，见E48-E49',
    'sp_CombineGray': '明确参与细码合并、收料/流水/选定工卡分配回写及撤回已接入；原DELETE改参与行留档，空组归零及重复连接差异见E48-E49',
    'sp_CombineGrayAfterGrayOut': '出库后细码合并、实际所涉工卡分配汇总及撤回已接入；原DELETE改留档，旧实际收发保留，见E48-E49',
    'WProcess_DELETE': '独立删除与工卡执行整链逐条撤销均调用人员/班组/末次流水及工序回写；整链原行留档、活动范围选择及组合差异见E37/E53-E55，待原单对照',
    'Sp_CheckWProcessIsDelete': '明确班次删除入口已接入03/04班窗口、06工位最新状态限制；边界保留，调用范围见E37；待原单对照',
    'Sp_MaintainForWProcessDel': 'GX07/GX16、人员/步骤、当前及下一工序、结束工序参数已接入独立及整链入口；整链可选触发后维护，历史原行保留，组合差异见E37/E54',
    'Sp_QualityIssues1': '日/月部门班次数量及卡数统计已接入，原01单引号07条件保持；原遗漏来源另展示，见E38；待原库逐项对照',
    'Sp_QualityIssues2': '旬/月二级分类及分母已自动采用质量数量批次；全类型Qty和去重工卡数按原规则核对通过，仍可明确手动输入，见E74',
    'Sp_QualityIssues3': '日/月一级质量分类统计已接入，包含负值、NULL及重复连接，另展示未归类来源；见E38；待原库逐项对照',
    'Sp_QualityIssues4': '染色班组质量责任奖扣已接入原2000/5/50/2.3公式及重复返修关联；不生成财务凭证，见E40；待原库逐项对照',
    'A_PurDetailNo': '按18类坯料/20类半成品实际收货的采购重量查询已接入；NULL/负数及原多表头连接保留；待原单对照',
    'vwQueryPurTOGrayIn': '采购明细原坯料待收选择可见性已接入；不把存在任意收货等同数量结清；待原单对照',
    'vw_SemiOutWorkApply': '订单颜色原外协待申请量及原选择条件已接入；全部分配/申请来源返回，负余量保留；待原单对照',
    'ColoringCheck_Insert': '对色累计曲线值与本单班组人员已接入；多步骤排序及旧人员保留差异见E33；待原单对照',
    'ColoringCheck_Delete': '删除新对色行撤销自身生成人员；不删除历史人员，差异见E33；待原单对照',
    'DefectiveInDetail_Insert': '新疵布入库明细正粒数回写工卡9及疵布入库处理已接入；不附加重量或审核限制；待原单对照',
    'DefectiveInDetail_Delete': '删除新明细按原范围恢复工卡并接续当前工序查询；待原单对照',
    'Sp_JobProcessUpdate_Curr1': '疵布删除与包装GX98开工调用范围及完成/处理中/下一工序分支已接入；无序选择与游标变量遗留差异见E34/E44；待原单对照',
    'vwDefectiveStock': '粒数/重量/长度实际收发差额已接入；负数及仅长度余额继续返回并标记原查询可见性；待原单对照',
    'WProcess_Insert': '新刷卡记录按实际染色起始状态继承机台、指定工序原零产量规则已接入；待原单对照',
    'WProcess_InsertNew': '新刷卡记录EndTime为NULL或1900零时按原规则写实际保存时刻；历史不重演；待原单对照',
    'OrderAtte_Insert': '订单另收费税价分支、同项回写及最后单位控制整单汇总已接入；多候选取价见E27；待真实单据对照',
    'QuoteItemPrice_Insert': '附加收费报价登记另收费字典已接入；非数字旧编码保留，编号差异见E27；待真实单据对照',
    'fn_GetPriceAtte': '工卡另收费查询已接入：基础价DISTINCT、确认存在条件及实际求和范围保留；待真实单据对照',
    'fn_GetPriceAtteWITHOUTSG': '工卡另收费不含手感并除1000查询已接入；NULL及单位4排除规则保留；待真实单据对照',
    'Sp_DyeDipsRecord_update': '所选打样结果色深/染程/备注回写及旧版本失效已接入；原全库游标范围差异见E28；待真实单据对照',
    'Fn_Get_No': '打样旧版本失效采用ASCII数字及20位截断；调价仍采用另一个10位函数；待真实单据对照',
    'Sp_UpdateSampleStockBook': '样品入出库原字段及1/2类流水、反审已接入；原变量误写和生效时点差异见E30；待真实单据对照',
    'OrderMainUpdate': '客户/客户自编号回写关联工卡分配已接入；180天结单改为所选订单明确动作，见E24；待真实单据对照',
    'OrderColorInsert': '订单量、备注、用途、品名、物料、色号及合同号回写已接入；多卡分别处理，见E24；待真实单据对照',
    'PriceAdjustDetail_Insert': '保存时按F_Get_No数字色号回写确价及调价来源已接入；不附加客户或审核条件；待真实单据对照',
    'PriceAdjustDetail_DELETE': '删除后按剩余最新生效日回退价格及来源，日期字段保留原行为；同日排序见E25；待真实单据对照',
    'SP_UpdateQuotePrice': '新调价单审核/反审核按QuoteDetailNo更新及清零已接入；与保存触发的范围分别保留；待真实单据对照',
    'F_Get_No': '调价链采用ASCII数字提取和10位返回截断，NULL不等值；Fn_Get_No的20位规则未替代；待真实单据对照',
    'DyeRecipePhase_Insert': '新配方同单染程重复规则及行尾单引号替换已接入；历史原行保留；待真实单据对照',
    'DyeDipsRecordPhase_Insert': '新打样配方同单染程重复规则已接入；缺父项/NULL保持原SQL比较语义；待真实单据对照',
    'DyeRecipeDetail_INSERT': '新配方用料按原Status=1停用规则办理；历史用料原行保留；待真实单据对照',
    'DyeDipsRecordDetail_INSERT': '新打样用料按原Status=1停用规则办理；历史用料原行保留；待真实单据对照',
    'Sp_DyeRecipe': '新配方各实际染程明细Amount合计到Cost；原染色限定已注释；按本单保存执行，见E26；待真实单据对照',
    'DyeRecipe_Delete': '删除新配方后回写剩余试样版本，最后版本置空/1900日期；多版本采用最新日期，见E26；待真实单据对照',
    'DyeRecipeInsert': '重复限制已注释；原全库孤立行删除不执行，全部旧行保留，差异见E26',
    'DyeRecipe_IU': '当前色号改写及重复限制均已注释，不重新激活；旧字段继续保存',
    'DyeLabColor_UPDATE': '当前禁止修改色号段已注释，不新增此限制；旧字段继续保存',
    'DyeLabColor_Delete': '按色号/来样颜色的实际打样引用限制删除；关联新色号随删、历史色号保留，见E26；待真实单据对照',
    'Sp_UpdateProdStockBook': '成品入/出库、盘点、30类修正流水及入库工卡回写；待真实单据对照',
    'Sp_UpdateJobSheetByProdIn': '按实际 JobReProdIn 参数回写新办理工卡；待真实单据对照',
    'Sp_JobProcessUpdate': '新办理工卡的实际工序进度；无序TOP1和子串范围采用明确排序及归属，见异常说明',
    'Sp_UpdateStuffStockBook': '染化料入/出库、调整、TO/SR调拨派生单及M计价主档价回写已接入；待真实单据对照',
    'Sp_UpdateArticleStockBook': '机物料入/出库及调整流水已接入；现行主档价回写段已注释，不新增生效动作；待真实单据对照',
    'Sp_UpdateGrayStockBook': '坯料入/出库、盘点、规格变更、调拨、收料细码单位、工卡细码领用及库位调整/反审已接入；对应差异见异常说明，待真实单据对照',
    'Sp_UpdateSemiStockBook': '半成品入/出库、盘点、规格变更、实际细码合理分配及工卡领用回写已接入；待实际单据对照',
    'sp_StuffWeightAutoStuffOut': '本库计划/实称采用、单位/WOF换算及一次领料已接入明确软件动作；外库与真实设备回传仍待接入',
    'Sp_InSertSemiOutRecord': '按收料单/条码/细码合理分配已接入，保留人工细码及历史；原重量符号/重复连接差异见异常文档',
    'Sp_UpdateJobOutAC': '各明确工卡分别回写当前出库单实配总量；多分组与名称冲突的合理处理见异常文档',
    'FD_GetFieldSeries': '日期、时间、表内/行内等编号已接入；原客户端模式和溢出采用说明见异常文档',
}


from foundation_completion_coverage import registrations
IMPLEMENTED_PARTS.update(registrations())
IMPLEMENTED_PARTS['UINav_Insert']='当前原定义EXEC已注释，保存导航不自动生成角色权限；显式生成动作另行提供，见E108'


def build(path):
    evidence = json.loads(path.read_text(encoding='utf-8-sig'))
    catalog = json.loads((ROOT / 'tools/legacy_models/source_catalog.json').read_text(encoding='utf8'))
    tables = {(row['schema'], row['table']): row for row in catalog['tables'] if row['handling'] == 'business_model'}
    dependencies = defaultdict(list)
    for row in evidence['dependencies']:
        dependencies[(row['source_schema'], row['source_name'])].append(row)
    objects = {(row['schema_name'].lower(), row['table_name'].lower()) for row in evidence['tables']}
    objects |= {(row['schema_name'].lower(), row['object_name'].lower()) for row in evidence['modules']}
    modules = []
    for row in evidence['modules']:
        definition = row['definition']
        active = '' if definition is None else sqlparse.format(definition, strip_comments=True)
        refs = sorted(set(re.findall(r'\b(dye|dbo)\.\[?([A-Za-z_][A-Za-z_0-9]*)\]?', active, re.I)))
        missing = ['.'.join(ref) for ref in refs if tuple(part.lower() for part in ref) not in objects]
        source_refs = [dependency for dependency in dependencies[(row['schema_name'], row['object_name'])]
            if (dependency['referenced_schema_name'] or 'dye', dependency['referenced_entity_name']) in tables
            and dependency['referenced_database_name'] in [None, evidence['database']]]
        modules.append({'schema': row['schema_name'], 'name': row['object_name'], 'type': row['type'],
            'encrypted': bool(row['is_encrypted']), 'definition_available': definition is not None,
            'definition_sha256': None if definition is None else hashlib.sha256(definition.encode('utf8')).hexdigest(),
            'business_dependencies': source_refs, 'declared_dependencies': dependencies[(row['schema_name'], row['object_name'])],
            'qualified_references_missing_in_current_objects': missing,
            'status': IMPLEMENTED_PARTS.get(row['object_name'], '已取得原定义，待逐项翻译/对照' if definition is not None else '定义不可读取，需合理替代并登记'),
        })
    registry = json.loads((ROOT / 'backend/plugins/erp_base/source_entry_rules.json').read_text(encoding='utf8'))
    output = {'captured_at': evidence['captured_at'], 'database': evidence['database'],
        'scope': '全部现存程序、视图、触发器、函数；基础/业务依赖与外库依赖分别登记，财务独立范围仍忽略',
        'modules': modules, 'entry_binding_count': sum(map(len, registry['models'].values()))}
    (ROOT / 'tools/legacy_models/logic_coverage.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    lines = ['# 旧ERP当前程序与入口覆盖核对', '', '核对时间：' + evidence['captured_at'], '',
        '本表登记所有现存程序，保留空表、少用及停用业务的证据。状态写“已接入”的具体分支才有对应代码；源码可读取、存在模型或历史字段一致均不等于整个业务链对照通过。', '',
        f"当前732个数据库模块，731个定义可读取；新办理规则覆盖{output['entry_binding_count']}组模型/入口对应。", '',
        '数据库已声明依赖保存在 logic_coverage.json。动态SQL依赖不一定登记完整；以下“缺失引用”是去除注释后发现的限定名称，需结合语句上下文核实，不据此停用整项业务。', '',
        '| 原对象 | 类型 | 当前代码覆盖/待办 | 当前对象集缺失的限定引用 |', '|---|---|---|---|']
    for row in modules:
        missing = '、'.join(row['qualified_references_missing_in_current_objects']) or '—'
        lines.append(f"| {row['schema']}.{row['name']} | {row['type']} | {row['status']} | {missing} |")
    lines += ['', '## 当前可证明的特殊项', '',
        '- dye.f_num_chn 为加密函数，无法读取其实现；不能宣称已按原代码复刻。',
        '- GrayStockAllot 的原库存过程引用 GrayStockAllotDetail；当前物理表及现存视图中没有该对象。新代码使用当前调拨表头实际持有的转出/转入字段，原表头及原流水仍完整保留。',
        '- 染化料自动出库含 WeighingSystem、Textile_GXHFZD 及旧计量链路依赖；仅凭当前 Textile_GXHFRS 不能证明外部实际回传。历史出库与称料数据仍完整承接。',
        '- 当前库存流水服务的生成结果按新单据办理对应保存；历史加载不调用这些服务，不重演原出库或覆盖原库存流水。', '']
    (ROOT / 'docs/旧ERP当前程序与入口覆盖核对.md').write_text('\n'.join(lines), encoding='utf8')
    print(json.dumps({'modules': len(modules), 'definitions': sum(row['definition_available'] for row in modules), 'entry_bindings': output['entry_binding_count']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--evidence', type=Path, required=True)
    build(parser.parse_args().evidence)
