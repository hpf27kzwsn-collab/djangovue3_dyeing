<script setup lang="ts">
import {computed,ref,watch} from 'vue'
import {compute} from '@fast-crud/fast-crud'
import {ElMessage} from 'element-plus'
import {useRoute,useRouter} from 'vue-router'
import {businessTitle,businessFieldTitle} from '../../erp-workspace'
import {api} from '../../api'
import {useAccount} from '../../store'
import ResourceTable from '../../components/ResourceTable.vue'
import FieldInput from '../../components/FieldInput.vue'
import DocumentEditor from './DocumentEditor.vue'
import ActionRows from './ActionRows.vue'
import EditableActionRows from './EditableActionRows.vue'
import ActionChanges from './ActionChanges.vue'
import LossRows from './LossRows.vue'
import ReworkSources from './ReworkSources.vue'
import {originalValues} from './source-form'
import OrderPricingWorkspace from './OrderPricingWorkspace.vue'
import BusinessActionPanel from './BusinessActionPanel.vue'
import {availableActions,type BusinessAction} from './action-presentation'
const props=defineProps<{entity:string;context?:Record<string,any>;lookupContext?:Record<string,any>;parentEntry?:string;contextLabel?:string;contextState?:string;readonly?:boolean;foundation?:any}>()
const route=useRoute(),router=useRouter(),maintenance=computed(()=>route.query.workspace==='maintenance')
const account=useAccount(),meta=ref<any>(),table=ref(),selected=ref<any>(),open=ref(false),activeTab=ref(''),editor=ref(false)
const actionOpen=ref(false),currentAction=ref<any>(),actionRow=ref<any>(),actionData=ref<Record<string,any>>({}),actionForm=ref(),saving=ref(false)
const actionResult=ref('')
const reportOpen=ref(false),report=ref<any>()
const pricingOrder=ref<any>()
const operationOpen=ref(false),operationRow=ref<any>(),collectionOpen=ref(false)
const generatedDocument=ref<any>()
const generatedMenu=computed(()=>account.menus.find(menu=>menu.resource===generatedDocument.value?.entity&&menu.component_name===menu.resource))
function openGenerated(){operationOpen.value=false;collectionOpen.value=false;router.push({path:generatedMenu.value!.web_path,query:{id:generatedDocument.value.id}})}
const childLookupContext=computed(()=>({...props.lookupContext,...(selected.value?originalValues(meta.value,selected.value):{})}))
const reportTables=computed(()=>report.value?[{title:'办理或查询结果',rows:report.value.rows},{title:'补充明细（含原筛选未展示记录）',rows:report.value.supplemental_rows??[]},{title:'未归类来源',rows:report.value.unclassified_rows??[]},...(report.value.quantity_sources?[{title:'本次报告数量来源',rows:report.value.quantity_sources}]:[]),...(report.value.candidate_rows?[{title:'原多候选及本次采用',rows:report.value.candidate_rows}]:[]),...(report.value.summary?[{title:'原变量与循环依据',rows:[report.value.summary]}]:[]),...(report.value.seed_rows?[{title:'上一循环班组种子来源',rows:report.value.seed_rows}]:[]),...(report.value.generation?[{title:'本次自动生成日历',rows:report.value.generation.rows}]:[]),...(report.value.result_rows?[{title:'结果与参与来源明细',rows:report.value.result_rows}]:[]),...(report.value.result_sets??[])]:[])
const columns=(rows:any[])=>Array.from(new Set(rows.flatMap(row=>Object.keys(row))))
const reportLabels:Record<string,string>={DefectDept:'责任部门编码',DefectDeptName:'责任部门',ClassName:'班次',UnitName:'计量口径',OneGrade:'一级分类',TowGrade:'二级分类',ClassID:'班次编码',AClassIDNum:'本班产量次数',BClassIDNum:'责任数量',ClassIDMoeny:'质量奖份额',KFMoeny:'质量扣罚',Rate:'责任比例（%）',Moeny:'质量奖结果',N1:'旬内审比例（%）',N2:'月内审比例（%）',K1:'旬客退比例（%）',K2:'月客退比例（%）',unit:'库存单位编码',measure:'数量种类',dispatched:'实际发出',received:'实际回货',difference:'收发差额',confirmed_loss:'确认损耗',unexplained_difference:'未解释差额',dispatch_nulls:'发出空值条数',receipt_nulls:'回货空值条数',unresolved_unit_source:'未确定单位的原记录',direction:'收发方向',entity:'来源表',source:'原字段来源',detail_no:'原明细号',header_count:'匹配表头数',reason:'说明'}
Object.assign(reportLabels,{FlowStatus:'维修流转状态',MFLevel:'原维修角色等级',isFixMan:'是否原维修工',isReportMan:'是否原报修人',CaseDetailNo:'原方案项目明细号',caseDetailNo:'原方案项目明细号',SerialNum:'项目序号原文',ProjectInfo:'项目内容',Value:'实际值',VALUE:'原待填结果值',DefaultValue:'原对照默认值',OriValue:'原带出值',Result:'原结果整数',IsInputText:'是否文本录入',IsUseMachineCase:'原已有项目标志',suffix:'原三位项目后缀',change_index:'变更原行序',HandlerIDs:'维修工原编码列表',Handlers:'维修工名称',Action:'原动作文字',ActionType:'流转记录类型',RecordDate:'记录时间',Operator:'操作员工',Score:'原评分或配件轮次',rounds:'配件轮次',notification_delivery:'原APP通知接入状态'})
Object.assign(reportLabels,{ID:'原ID',CurrDate:'排班日期',BeginDate:'配置生效日期',CycleDays:'原周期天数字符串',AllDays:'原总周期',LastCreateDate:'原末组排班日期',LastBeginDate:'原末组配置日期',LastMaxID:'本次ID计算起点',CreateDays:'生成天数',CycRemain:'原循环余数',config_id:'采用配置记录ID',slot:'时段序号',DateBetween:'原时段文字',DateStart:'原开始文字',DateEnd:'原结束文字',GatherHM:'查询时分',matched:'本段命中',LastShiftID:'最后命中班组',LastClassID:'最后命中班别',machine_id:'机台记录ID',department_id:'部门记录ID',shift_id:'班组记录ID',ShiftName:'班组名称',source_ids:'来源记录ID',generated_count:'本次生成条数'})
for(let n=1;n<=4;n++){const slot=String(n).padStart(2,'0');reportLabels['ShiftID'+slot]='第'+n+'段班组';reportLabels['ClassID'+slot]='第'+n+'段班别';reportLabels['DateBetween'+slot]='第'+n+'段时间'}
Object.assign(reportLabels,{Prop:'原人员分摊比例',EmpRate:'个人两位费率',SumRate:'班组两位总率',EffiRate:'原效率比例',SumCount:'原连接分组行数',work_ids:'参与报工ID',ShiftID:'原班组',ProcessNo:'工序序号',ProgramID:'中控工艺号',BathRatio:'浴比',WaterQty:'水量',CarryIndex:'备料桶序',StepName:'工步名称',StuffNo:'物料序号',uiTransIndex:'备料传输次序',StuffSheetNo:'原中控料单号',StuffJobSheetNo:'原中控缸号',StuffType:'染化料类别',TankNo:'料槽号',StuffRolls:'称料粒数',StuffLengthQty:'原称料长度投影',StuffWeightQty:'称料重量',CustomerID_R:'客户名称',ProdID_R:'物料名称',joined_ids:'全部连接来源ID',entry:'原现场入口'})
Object.assign(reportLabels,{CheckerID:'原责任对色员/工号',EmpID:'主工号',EmpID1:'原第二工号',S:'原打样次数',R:'原返打责任次数',SDate:'7:30归属工作日',WorkDays:'原工作日数',SumNum:'计件份额合计',DNum:'单染次数',WNum:'双染次数',TNum:'三染次数',MNum:'四染次数',FWNum:'复双染次数',FTNum:'复三染次数',FDNum:'复单染次数',DaBan:'打样次数',FuBan:'复版次数',Amount:'原计件计算值',join_count:'原连接计数',duplicate_threshold:'原重复比较阈值',duplicate:'达到原重复报错条件',approved_block:'原审核规则是否阻止',original_rejected:'原触发器是否拒绝',operation:'核对操作',right_status_in_statement:'语句包含审核状态列',RightStatus:'原审核状态',ProdID:'原物料编码',ShortName:'原客户简称',RowNum:'原步骤行序',DoneValue:'原已做非空次数',LimitValue:'原剩余值',CurveID:'曲线编码',StepNo:'步骤序号',DyeProcessID:'染程步骤编码',DefaultValue:'原默认值',blockers:'原排除条件命中的报工人员',weight_id:'称料来源ID',curve_id:'曲线来源ID',dictionary_id:'字典来源ID'})
Object.assign(reportLabels,{function:'原报价函数',component:'套价分量序号',stage:'取价步骤',before:'办理前原值',after:'本次回写值',white:'使用增白剂',dye:'使用染料',global_fast_count:'全库高牢度打样单数',note_candidates:'原备注候选ID',material_ids:'染化料记录ID',phase_ids:'染程记录ID',original_visible:'原未打样列表可见',original_comparison_passed:'原物料比较是否通过',trial_id:'试验记录ID',member_id:'班组人员记录ID',shift_id:'班组记录ID',ColorNo:'来样颜色号',ColorNum:'原色号',DyePhaseName:'原染程名称',Num:'原计件份额',StuffID:'试验物料',CompareStuffID:'比较物料',MachineID:'机台',PhaseID:'染程',ProcessID:'工序'})
Object.assign(reportLabels,{record_id:'记录ID',state:'办理状态',active:'已消耗留档',kind:'办理类型',after_dispatch:'出库后细码',source_count:'参与原记录数',created_count:'新建记录数',at:'办理时间',reversed_at:'撤回时间',reverse_reason:'撤回原因',reverse_mode:'撤回范围',operation_id:'拆合日志ID',operation_ids:'相关拆合日志ID',source_job:'来源工卡',source_job_id:'来源工卡记录ID',mode:'选路分支',token:'原成员片段',target_id:'目标工序记录ID',candidate_ids:'全部候选记录ID',selected_source_id:'采用的排程或称料记录ID',issue:'原差异或未匹配原因',role:'结果用途',assigned_ids:'原领用记录ID',assigned_quantities:'原领用数量',field:'原字段',value:'原值'})
Object.assign(reportLabels,{rank:'排序序号',candidate_count:'候选数量',source_id:'采用的投坯记录ID',candidates:'全部候选及来源',matched:'已找到对应',GrayWeight:'采用投坯重量',GrayBarCode:'投坯条码',rank_package_id:'排序位置的包装记录ID',Kg:'包装重量',SheetSeries:'原单据流水'})
Object.assign(reportLabels,{month:'月份',AllNum:'原连接口径产量次数',AllKg:'总重量（汇总吨/明细公斤）',N_Num:'内部返修次数',K_Num:'客退返修次数',N_RKg:'内部返修重量（汇总吨/明细公斤）',K_RKg:'客退返修重量（汇总吨/明细公斤）',repair_source:'返修来源及原计算明细',RKg:'原加权返修公斤',Kind:'原评审类别',StationID:'原站点编码',WProcessNo:'原刷卡流水',CurrDosage:'原投入比例',CurrKg:'原刷卡公斤',quantity:'本条原数量',stock_quantity_rule:'原库存符号规则结果',source_unit:'原申请单位',missing_header:'缺少表头',header_id:'表头记录ID',factory_quality:'加工厂质量处置',delivery_confirmation:'交付确认',SheetNo:'原单据号',SheetKind:'原单据类型',CheckNo:'原订单明细号',StockUnit:'原库存单位',Qty:'原数量'})
Object.assign(reportLabels,{outside_gray_scope:'不在首轮投坯匹配范围',gray_ids:'投坯来源记录ID',gray_id:'投坯来源ID',CustomerID:'原客户编码',ProdCode:'原标签品名代码',target_ids:'全部标签回写目标',eligible:'是否进入空客户标签分支',selected:'本次采用',NameC:'原品名',Packer:'包装人员',PackTime:'包装时间',employee_id:'员工记录ID',copy_count:'本次备份行数',retire_count:'退出现行范围行数',copy_ids:'备份来源ID',retire_ids:'归档原行ID',existing_backup_ids:'原有备份记录ID',source_ids:'全部来源ID',source_entity:'来源表',count:'行数',employee_record_id:'包装人员原行ID',people:'同条码人员原行数',label_sync_job_id:'标签同步发起工卡ID'})
function columnTitle(key:string){if(key==='Rate'&&report.value.report.startsWith('Sp_DyeRate'))return '直通率（%）';if(key==='active'&&['外协完整来源与质量处置追溯','外协结案后收退核对'].includes(report.value.report))return '当前参与活动业务';const match=key.match(/^(Day|Month)_([NKP])_(Qty|LengthQty)$/);return reportLabels[key]??(match?`${match[1]==='Month'?'月累计':report.value.report==='Sp_QualityIssues2'?'本旬':'当日'}${({N:'内审',K:'客退',P:'赔付'} as Record<string,string>)[match[2]]}${match[3]==='Qty'?'数量':'长度'}`:key)}
Object.assign(reportLabels,{job_id:'工卡记录ID',process_id:'工序记录ID',changes:'本次字段回写',process_count:'工序数',result:'处理结果',source_work_id:'原刷卡记录ID',work_id:'刷卡记录ID',position:'原列表位置',side:'日志阶段',unclassified_quantity:'未标明种类的旧数量',raw_payload:'原失败日志内容',log_id:'拆合日志记录ID',consumed_count:'退出活动汇总行数',ReceSheetNo:'收料号',RollNo:'卷号',BarCode:'条码',WeightQty:'重量',LengthQty:'长度',Rolls:'粒数',JobSheetNo:'工卡号',DAYS:'产量归属日',TMonth:'统计月份',Class:'白晚班',ClothQtyKg:'汇总重量',ZNum:'正常次数',ZKg:'正常重量',JNum:'加料次数口径',JKg:'加料重量',RNum:'返修次数口径',RTKg:'返修重量',TNum:'总次数',AddNumber1:'原加料单计数',AddNumber2:'原第二加料计数',WDNum:'责任计数',DefectClassID:'责任班次',DefectEmpID:'责任人员',ColorDepthID:'色深编码',JTimes:'有效加料单分组数',completion_status:'本次传入完成状态',created_ids:'新建统计记录ID',retired_ids:'替换留档记录ID'})
Object.assign(reportLabels,{StationID:'工段编码',StationIDName:'工段名称',FabricName:'布种',Workshop:'责任车间',Num:'明细/小计',N_NumDay:'当日内部返修次数',K_NumDay:'当日客退返修次数',N_RKgDay:'当日内部返修吨数',K_RKgDay:'当日客退返修吨数',N_NumMonth:'月内部返修次数',K_NumMonth:'月客退返修次数',N_RKgMonth:'月内部返修吨数',K_RKgMonth:'月客退返修吨数',AllMonthNum:'月返修总次数',ALLMonthKg:'月返修总吨数',FARNum:'原FAR连接行数',FARKg:'原FAR数量（吨）',YF:'月份显示',RQ1:'上年月份',RQ2:'本年月份',FARKg1:'上年FAR数量（吨）',FARKg2:'本年FAR数量（吨）',AllKg1:'上年总量（吨）',AllKg2:'本年总量（吨）',N_RKg1:'上年内部返修（吨）',N_RKg2:'本年内部返修（吨）',K_RKg1:'上年客退返修（吨）',K_RKg2:'本年客退返修（吨）',NRate1:'上年内部返修比例（%）',NRate2:'本年内部返修比例（%）',KRate1:'上年客退返修比例（%）',KRate2:'本年客退返修比例（%）',material_return:'原料实际退回',product_return:'成品实际退厂',net_dispatched:'发出扣除原料退回',net_received:'回货扣除成品退厂',number:'收退登记序号',after_closure:'发生于当前结案之后',changed_fields:'结案后变化字段',header_sheet_series:'原匹配表头流水',sheet_date:'原表头日期',sheet_kind:'原单据类型',job_number:'原工卡号',quantity:'原数量Qty',batch_id:'数量来源批次ID',source_row:'原连接行序号',out_detail_no:'原出库明细号',stock_unit:'原StockUnit',business_unit:'原经营单位编码',metres:'有依据的原长度PreMeter',zero_amount:'原ARMoney等于零',period:'同期来源'})
for(const [station,title] of [['05','定型'],['06','溢流']])for(const [key,label] of [['N_Num','内部返修次数'],['K_Num','客退返修次数'],['N_RKg','内部返修吨数'],['K_RKg','客退返修吨数']])reportLabels[key+station]=title+label
for(const [prefix,title] of [['JQty1','定型03/05班数量'],['YQty1','定型其他班数量'],['JQty2','溢流03/05班数量'],['YQty2','溢流其他班数量'],['Qty3','12部门数量'],['Qty4','14部门数量'],['Qty5','其他部门数量'],['AllQty','全部数量']]){reportLabels[prefix]=title+'（吨）';reportLabels[prefix.replace('Qty','Meter')]=title.replace('数量','长度')+'（万米）'}
Object.assign(reportLabels,{purchase_reference_fields:'匹配的采购引用列',PurDetailNo:'原采购明细引用',PurchaseOrders:'原采购单引用',SupplierID:'原供应商编码',destination:'收回仓类',receipt_kind:'收回原类型',dispatch_kind:'发出原类型',original_rolls_formula:'原粒数余额公式结果（含混量）',remaining_weight:'原剩余重量',remaining_packs:'原剩余件数',old_selection_available:'原选择列表可见'})
Object.assign(reportLabels,{ZuoRiJiaBan:'昨日甲班',ZuoRiYiBan:'昨日乙班',JinRiJiaBan:'今日甲班',JinRiYiBan:'今日乙班',BenYueJiaBan:'本月甲班',BenYueYiBan:'本月乙班',BenYueZongHeJi:'本月总合计',ShangYueZongHeJi:'上月总合计'})
Object.assign(reportLabels,{TotalKg:'原出缸总重量',ZKg:'原直通重量',JKg:'原加色重量',RTKg:'原返修重量',ZNum:'原直通次数',JNum:'原加色次数',RNum:'原返修次数',TNum:'原总次数',JTimes:'原加色次数字段',RTRate:'原返修率（%）',DyeAdd:'称料单加色次数',DayType:'统计期间',original_group:'原分组',ratio_issue:'比例说明',original_depth_code:'原色级码',ColorDepthName:'色级名称',pinzhong:'原品种',WindingID:'络筒原编码',CmOk:'原检查结果（1为提示）',rule:'原检查规则',Mesge:'原检查说明',Interval:'原分钟间隔',required_minutes:'原要求间隔分钟',MinNUM:'最早排程序位',NUM:'本卡排程序位',source_unit:'原数量单位',source_price_unit:'原价格单位',source_pack_unit:'原包装单位'})
const display=(value:any)=>value===null?'NULL':typeof value==='object'?JSON.stringify(value):String(value)
Object.assign(reportLabels,{retained_count:'本次原单留档数',compensation_count:'新增反向库存流水数',table:'原表',effect:'本次处理',source_entity:'来源表',source_id:'来源记录ID',target_entity:'下游表',relation:'关联依据',WareHouseID:'仓库',LotNo:'批号',StorageUnitIDs:'库位',InQty:'原入库量',OutQty:'原出库量',InWeightQty:'原入库重量',OutWeightQty:'原出库重量',InRolls:'原入库粒数',OutRolls:'原出库粒数',InLengthQty:'原入库长度',OutLengthQty:'原出库长度',InMoney:'原入库金额',OutMoney:'原出库金额'})
function showActionResult(result:{msg:string;data:any}){actionResult.value=result.msg==='success'?'':result.msg;ElMessage.success(actionResult.value||'操作成功');if(result.data?.entity&&result.data?.id)generatedDocument.value=result.data;if(result.data?.report){report.value=result.data;reportOpen.value=true}}
const workflow=computed(()=>meta.value?.workflow??{})
const collectionActions=computed(()=>availableActions((workflow.value.actions??[]).filter((action:any)=>action.detail===false),null,{},permission=>account.can(permission),maintenance.value))
const rowActions=computed(()=>operationRow.value?availableActions((workflow.value.actions??[]).filter((action:any)=>action.detail!==false),state(operationRow.value),operationRow.value,permission=>account.can(permission),maintenance.value):[])
const hasMaintenance=computed(()=>(workflow.value.actions??[]).some((action:any)=>['maintenance','automatic'].includes(action.placement)&&account.can(action.permission)))
function switchWorkspace(){const query={...route.query};if(maintenance.value)delete query.workspace;else query.workspace='maintenance';router.push({path:route.path,query})}
const tabs=computed(()=>(workflow.value.children??[]).filter((child:any)=>account.can(child.entity+':list')))
const frozen=(row:any)=>props.readonly||workflow.value.readonly||Boolean(workflow.value.freeze_when?.some((key:string)=>row[key]))||Boolean(workflow.value.editable_states&&!workflow.value.editable_states.includes(row[workflow.value.state_field??'status']))
function state(row:any){return workflow.value.state_from_parent?props.contextState:row[workflow.value.state_field??'status']}
function childReadonly(child:any){return child.parent_states?!child.parent_states.includes(state(selected.value)):frozen(selected.value)}
function childHasKey(child:any){return !child.parent_field||![null,undefined,''].includes(selected.value[child.parent_field])}
function actionField(field:any){return field.params_from_row?{...field,remote:{...field.remote,params:Object.fromEntries(Object.entries(field.params_from_row).map(([key,source])=>[key,actionRow.value[String(source)]]))}}:field}
async function submitAction(){
  await actionForm.value.validate()
  saving.value=true
  try{await performAction(currentAction.value,actionRow.value,actionData.value);actionOpen.value=false}finally{saving.value=false}
}
async function performAction(action:BusinessAction,row:any,data:any){
  const result=await api(`/api/system/${props.entity}/${action.detail===false?'':row.id+'/'}${action.key}/`,{method:'POST',data})
  if(result.data?.report){result.data.title=action.display_title;result.msg='操作完成'}
  showActionResult(result);await table.value.refresh()
  if(action.detail!==false&&operationRow.value?.id===row.id){
    if(action.key==='delete_shift_record'){operationOpen.value=false;operationRow.value=undefined}
    else operationRow.value=(await api(`/api/system/${props.entity}/${row.id}/`)).data
  }
}
async function executeAction(action:BusinessAction,row?:any){
  if(action.inputs.length)openAction(action,row)
  else await performAction(action,row,{})
}
function businessNow(){return new Intl.DateTimeFormat('sv-SE',{timeZone:'Asia/Shanghai',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit',hourCycle:'h23'}).format(new Date())}
function openAction(action:any,row?:any){currentAction.value=action;actionRow.value=row;actionData.value=Object.fromEntries(action.inputs.filter((f:any)=>f.source_field!==undefined||f.default!==undefined||f.kind==='multi'||f.kind==='datetime'&&f.default_now!==false).map((f:any)=>[f.key,f.source_field!==undefined?row[f.source_field]:f.default??(f.kind==='multi'?[]:businessNow())]));actionOpen.value=true}
const actions=computed(()=>{
  const result:any[]=[]
  if(workflow.value.order_pricing_head)result.push({key:'order_pricing',text:'订单选价',permission:props.entity+':detail',click:(row:any)=>{pricingOrder.value=row}})
  if(tabs.value.length)result.push({key:'children',text:'单据明细',permission:props.entity+':detail',click:(row:any)=>{selected.value=row;activeTab.value=tabs.value[0].entity;open.value=true}})
  if((workflow.value.actions??[]).some((action:any)=>action.detail!==false&&action.placement!=='deferred'&&(maintenance.value||action.placement==='business')&&account.can(action.permission)))result.push({key:'business',text:maintenance.value?'维护办理':'业务办理',permission:props.entity+':detail',show:(row:any)=>availableActions((workflow.value.actions??[]).filter((action:any)=>action.detail!==false),state(row),row,permission=>account.can(permission),maintenance.value).length>0,click:(row:any)=>{operationRow.value=row;operationOpen.value=true}})
  return result
})
watch(()=>[props.entity,props.foundation,account.menus,account.buttons,maintenance.value],async()=>{
  const data=(await api('/api/meta/'+props.entity+'/')).data
  data.title=account.menus.find(menu=>menu.component_name===props.entity)?.name??businessTitle(data.title)
  for(const field of data.fields)field.title=businessFieldTitle(field.title)
  if(data.workflow?.source_model&&!maintenance.value)for(const field of data.fields){
  }
  if(props.foundation){
    const entry=props.foundation
    data.title=account.menus.find(menu=>menu.component_name===entry.key)?.name??businessTitle(entry.title);data.foundation=entry
    data.workflow={...data.workflow,readonly:data.workflow.readonly||Boolean(entry.readonly)}
    if(entry.entry)data.workflow.entries=data.workflow.entries.filter((item:any)=>item.value===entry.entry)
    if(entry.children)data.workflow.children=entry.children
    if(entry.simple_master)data.workflow.actions=data.workflow.actions.filter((item:any)=>!['confirm','approve','reopen'].includes(item.key))
    const entryFields=data.workflow.entries.find((item:any)=>item.value===entry.entry)?.field_rules??{}
    for(const field of data.fields){
      if(entryFields[field.key]?.title)field.title=businessFieldTitle(entryFields[field.key].title)
      if(entry.field_titles?.[field.key])field.title=entry.field_titles[field.key]
      if(field.key in entry.filters)field.form={...field.form,value:entry.filters[field.key],component:{name:'FieldInput',vModel:'modelValue',field:{...field},disabled:true}}
    }
  }
  for(const field of data.fields)if(props.context&&field.key in props.context)field.form={...field.form,component:{name:'FieldInput',vModel:'modelValue',field:{...field},disabled:true}}
  const atomic=(data.workflow.children??[]).some((child:any)=>child.atomic)&&account.can(props.entity+':save-document-post')
  data.crud_options={...data.crud_options,rowHandle:{width:data.workflow.order_pricing_head?420:340,buttons:{edit:{show:compute(({row}:any)=>!frozen(row)&&!(props.entity==='erp_sampling_sampleconfirmation'&&row.sent_at!==null)&&account.can(props.entity+':patch')), ...(atomic?{click:({row}:any)=>{selected.value=row;editor.value=true}}:{})},remove:{show:compute(({row}:any)=>!frozen(row)&&!workflow.value.delete_disabled&&account.can(props.entity+':delete'))},copy:{show:false}}}}
  meta.value=data
},{immediate:true})
</script>
<template>
  <div class="business-pane"><el-alert v-if="contextLabel" :title="contextLabel" type="info" :closable="false"/>
    <el-dialog :model-value="!!pricingOrder" title="染整订单报价与金额" width="min(1350px,96vw)" destroy-on-close @close="pricingOrder=undefined"><OrderPricingWorkspace v-if="pricingOrder" :row="pricingOrder" @saved="table.refresh()"/></el-dialog>
    <el-alert v-if="actionResult" :title="actionResult" type="success" @close="actionResult=''"/>
    <div v-if="generatedDocument&&!operationOpen">已生成：{{generatedDocument.sheet_no??generatedDocument.id}} <el-button v-if="generatedMenu" text @click="openGenerated">打开新单</el-button></div>
    <el-drawer v-model="operationOpen" :title="meta?.title+' · '+(maintenance?'维护办理':'业务办理')" size="min(1000px,96vw)" destroy-on-close>
      <p v-if="operationRow" class="document-identity">{{operationRow.old_sheet_no??operationRow.number??operationRow.code??operationRow.id}}</p>
      <p v-if="generatedDocument">已生成：{{generatedDocument.sheet_no??generatedDocument.id}} <el-button v-if="generatedMenu" text @click="openGenerated">打开新单</el-button></p>
      <BusinessActionPanel :actions="rowActions" @execute="action=>executeAction(action,operationRow)"/>
    </el-drawer>
    <el-drawer v-model="collectionOpen" :title="meta?.title+' · '+(maintenance?'专题工具':'业务查询与办理')" size="min(1000px,96vw)" destroy-on-close><BusinessActionPanel :actions="collectionActions" collection @execute="action=>executeAction(action)"/></el-drawer>
    <div v-if="collectionActions.length||hasMaintenance" class="business-toolbar"><el-button v-if="collectionActions.length" @click="collectionOpen=true">{{maintenance?'专题工具':'业务查询与办理'}}</el-button><el-button v-if="hasMaintenance" text @click="switchWorkspace">{{maintenance?'返回业务':'数据维护'}}</el-button></div>
    <el-alert v-if="readonly" title="本层资料已经冻结，业务进度通过对应操作维护。" type="info" :closable="false"/>
    <ResourceTable v-if="meta" ref="table" :key="entity" :meta="meta" :context="context" :lookup-context="lookupContext" :parent-entry="parentEntry" :context-label="contextLabel" :readonly="readonly||workflow.readonly" :disable-delete="workflow.delete_disabled" :row-actions="actions"/><el-skeleton v-else animated/>
    <el-drawer v-model="open" :title="meta?.title+' · 明细与关联'" size="min(1400px, 97vw)" destroy-on-close>
      <el-tabs v-if="open" v-model="activeTab"><el-tab-pane v-for="child in tabs" :key="child.entity" :name="child.entity" :label="child.title">
        <el-alert v-if="activeTab===child.entity&&!childHasKey(child)" title="此表头的关联流水为空，无法按流水确定所属明细。原行仍保留，可从染程或材料明细入口核对。" type="info" :closable="false"/>
        <BusinessPane v-else-if="activeTab===child.entity" :key="child.entity+'-'+selected.id" :entity="child.entity" :context="{[child.key]:selected[child.parent_field??'id'],...(child.entry?{_entry:child.entry}:{})}" :lookup-context="childLookupContext" :parent-entry="selected.entry_name" :foundation="foundation?{title:child.title,entry:child.entry,filters:{},field_titles:child.field_titles,simple_master:foundation.simple_master}:undefined" :context-state="state(selected)" :context-label="String(selected.number??selected.code??selected.name??selected.id)" :readonly="childReadonly(child)"/>
      </el-tab-pane></el-tabs>
    </el-drawer>
    <el-drawer v-model="editor" :title="meta?.title+' · 整单编辑'" size="min(1500px, 98vw)" destroy-on-close><DocumentEditor v-if="editor" :meta="meta" :row="selected" :context="context" @saved="editor=false;table.refresh()"/></el-drawer>
    <el-dialog v-model="actionOpen" :title="currentAction?.display_title" width="min(900px,95vw)" destroy-on-close><el-form v-if="actionOpen" ref="actionForm" :model="actionData" label-width="150px">
      <el-form-item v-for="field in currentAction.inputs" :key="field.key" :prop="field.key" :label="field.title" :rules="[{required:field.required,message:'请填写'+field.title}]"><ReworkSources v-if="field.kind==='rework_sources'" v-model="actionData[field.key]"/><LossRows v-else-if="field.kind==='losses'" v-model="actionData[field.key]"/><EditableActionRows v-else-if="field.kind==='editable_rows'" v-model="actionData[field.key]" :field="field"/><ActionRows v-else-if="field.kind==='rows'" v-model="actionData[field.key]" :field="field" :form="actionData" :row="actionRow"/><ActionChanges v-else-if="field.kind==='changes'" v-model="actionData[field.key]" :field="field"/><FieldInput v-else v-model="actionData[field.key]" :field="actionField(field)"/></el-form-item>
    </el-form><template #footer><el-button @click="actionOpen=false">取消</el-button><el-button type="primary" :loading="saving" @click="submitAction">确认操作</el-button></template></el-dialog>
    <el-dialog v-model="reportOpen" :title="report?.title??report?.report" width="96vw" destroy-on-close>
      <template v-if="reportOpen">
        <el-alert v-for="note in report.notes" :key="note" :title="note" type="info" :closable="false"/>
        <p v-if="report.period">统计区间：{{report.period.start}} 至 {{report.period.end}}<span v-if="report.period.month_start">；月起点：{{report.period.month_start}}</span></p>
        <p v-if="report.denominator">原分母：{{report.denominator}}；来源：{{report.denominator_reference||'未提供'}}</p>
        <p v-if="report.quantity_sources">数量来源依据：{{report.quantity_reference||'未提供'}}；本次输入 {{report.quantity_sources.length}} 行</p>
        <p v-if="report.quantity_mapping">数量取数状态：{{({mapped:'已采用本地数量集',unavailable:'尚无本地数量集',manual:'本次手动输入'} as Record<string,string>)[report.quantity_mapping.state]}}<span v-if="report.quantity_mapping.batch_id">；数量集 {{report.quantity_mapping.batch_id}}</span></p>
        <p v-if="report.ambiguous">原检查存在多个候选，已逐项列出结果。</p>
        <p v-if="report.calculation_mode">上月栏目口径：{{report.calculation_mode==='legacy'?'原栏目连接':'明确修正上月栏目连接'}}</p>
        <p v-if="report.mode">同比口径：{{report.mode==='legacy'?'原过程':'同期修正'}}</p>
        <p v-if="report.closure_versions!==undefined">结案状态：{{({closed:'已结案',needs_review:'待复核',open:'已撤回'} as Record<string,string>)[report.closure_state]||'尚未结案'}}；历史版本：{{report.closure_versions}}</p>
        <el-tabs><el-tab-pane v-for="part in reportTables" :key="part.title" :label="part.title+'（'+part.rows.length+'行）'">
          <el-table :data="part.rows" height="55vh" border><el-table-column v-for="key in columns(part.rows)" :key="key" :label="columnTitle(key)" min-width="150"><template #default="scope">{{display(scope.row[key])}}</template></el-table-column></el-table>
        </el-tab-pane></el-tabs>
      </template>
    </el-dialog>
  </div>
</template>
<style scoped>.business-pane{height:100%;display:flex;flex-direction:column;gap:12px}.business-pane>.page{flex:1;min-height:0}.el-tabs{height:100%}</style>
