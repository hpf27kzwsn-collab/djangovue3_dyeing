<script setup lang="ts">
import {computed,reactive,ref,watch} from 'vue'
import {ElMessage} from 'element-plus'
import {api} from '../../api'
const props=defineProps<{modelValue?:any;row:any;order?:any;readonly?:boolean}>()
const emit=defineEmits(['update:modelValue'])
const saved=computed(()=>props.row.pricing_info)
const previous=props.modelValue??saved.value??{}
const units=[{value:1,label:'元/kg'},{value:2,label:'元/吨'},{value:3,label:'元/米'},{value:4,label:'元/条'},{value:5,label:'元/缸'},{value:6,label:'元/码'}]
const choice=reactive<any>({mode:previous.mode??'quote',yarn_category:previous.yarn_category,
  price_basis:previous.price_basis==='Price'?'Price':'CusPrice',quote_id:previous.quote_id,quote_head_id:previous.quote_head_id,
  price_unit:previous.price_unit??((props.row.old_unit??'').toUpperCase()==='KG'?1:null),
  quantity_mode:previous.quantity_mode??'order',quantity:previous.quantity??null,amount_mode:previous.amount_mode??'calculated',
  manual_amount:previous.manual_amount??null,manual_price:'manual_price' in previous?previous.manual_price:previous.mode==='manual'?previous.price:props.row.old_price??null,reason:''})
const rows=ref<any[]>([]),preview=ref<any>(),busy=ref(false),applied=ref(!!props.modelValue)
const cancelled=ref(false)
const statusLabels:Record<string,string>={priced:'已采用并计价',unpriced:'未完整计价',invalid:'需重新选价',manual_input:'手工价格',manual_amount:'手工金额'}
function query(){
  const data:any={order_id:props.order?.id??props.row.source_parent_1,line_id:props.row.id,
    sheet_series:props.row.old_sheet_series??props.order?.old_sheet_series??props.order?.SheetSeries,
    line:Object.fromEntries(['old_prod_id','old_unit','old_order_qty','old_card_qty'].filter(k=>props.row[k]!==undefined).map(k=>[k,props.row[k]===''?null:props.row[k]]))}
  if(props.order&&('old_customer_id' in props.order||'CustomerID' in props.order))data.customer_id=props.order.old_customer_id??props.order.CustomerID
  return data
}
function payload(){
  const value:any={mode:choice.mode,price_unit:choice.price_unit||null,quantity_mode:choice.quantity_mode,
    amount_mode:choice.amount_mode,reason:choice.reason}
  if(choice.mode==='quote')Object.assign(value,{quote_id:choice.quote_id,quote_head_id:choice.quote_head_id,yarn_category:choice.yarn_category,price_basis:choice.price_basis})
  else value.manual_price=choice.manual_price===''?null:choice.manual_price
  if(choice.quantity_mode==='explicit')value.quantity=choice.quantity===''?null:choice.quantity
  if(choice.amount_mode==='manual')value.manual_amount=choice.manual_amount===''?null:choice.manual_amount
  return value
}
async function find(){
  if(!choice.yarn_category){ElMessage.info('请先选择供纱方式');return}
  busy.value=true
  try{rows.value=(await api('/api/system/erp_sales_sourcedyeordercolor/pricing_candidates/',{method:'POST',data:{...query(),yarn_category:choice.yarn_category}})).data.rows}finally{busy.value=false}
}
function choose(row:any){choice.quote_id=row.quote_id;choice.quote_head_id=row.quote_head_id;choice.yarn_category=row.yarn_category;if(row.price_unit!==null)choice.price_unit=row.price_unit;preview.value=undefined;applied.value=false}
async function prepare(){
  if(cancelled.value){ElMessage.info('本次选价已取消，请重新选择报价或录入议价');return null}
  if(choice.mode==='quote'&&!choice.quote_id){ElMessage.info('请先选择一条报价');return null}
  busy.value=true
  try{preview.value=(await api('/api/system/erp_sales_sourcedyeordercolor/pricing_preview/',{method:'POST',data:{...query(),pricing:payload()}})).data;
    const value=payload();emit('update:modelValue',value);applied.value=true;return value}finally{busy.value=false}
}
function unchanged(){emit('update:modelValue',null);applied.value=false;preview.value=undefined;cancelled.value=true}
watch([()=>props.row.old_prod_id,()=>props.row.old_unit,()=>props.order?.old_customer_id],()=>{
  rows.value=[];choice.quote_id=undefined;choice.quote_head_id=undefined;unchanged()
})
watch([()=>props.row.old_order_qty,()=>props.row.old_card_qty],()=>{preview.value=undefined})
watch(()=>choice.yarn_category,()=>{rows.value=[];choice.quote_id=undefined;choice.quote_head_id=undefined;unchanged()})
watch(()=>[choice.mode,choice.quote_id,choice.quote_head_id,choice.price_basis,choice.price_unit,choice.quantity_mode,choice.quantity,choice.amount_mode,choice.manual_price,choice.manual_amount,choice.reason],()=>{
  preview.value=undefined
  if(choice.mode==='manual'||choice.quote_id){cancelled.value=false;emit('update:modelValue',payload());applied.value=true}
  else unchanged()
})
defineExpose({query,payload,prepare})
</script>
<template>
  <div class="order-price-chooser">
    <el-descriptions v-if="saved" :column="2" border size="small">
      <el-descriptions-item label="当前计价">{{statusLabels[saved.status]??saved.status}}</el-descriptions-item>
      <el-descriptions-item label="采用报价">{{saved.quote_sheet_no||'手工价格'}} · {{saved.quote_detail_no||''}}<span v-if="saved.source_exists===false">（来源已删除，保留采用记录）</span></el-descriptions-item>
      <el-descriptions-item label="采用单价">{{saved.price??'未填写'}} {{units.find(u=>u.value===saved.price_unit)?.label??'单位未明确'}}</el-descriptions-item>
      <el-descriptions-item label="计价数量">{{saved.quantity??'未明确'}} · {{saved.quantity_basis}}</el-descriptions-item>
    </el-descriptions>
    <el-alert v-if="saved?.status==='invalid'" :title="saved.invalid_reason" type="warning" :closable="false"/>
    <template v-if="!readonly">
      <div class="price-controls">
        <el-radio-group v-model="choice.mode"><el-radio-button value="quote">采用染整报价</el-radio-button><el-radio-button value="manual">手工议价</el-radio-button></el-radio-group>
        <template v-if="choice.mode==='quote'">
          <label>供纱方式</label><el-select v-model="choice.yarn_category" placeholder="请选择供纱方式" aria-label="供纱方式"><el-option label="包工包料（本厂采购）" value="本厂采购"/><el-option label="来料加工（客户来纱）" value="客户来纱"/></el-select>
          <el-button :loading="busy" @click="find">查找报价</el-button>
          <label>采用价格</label><el-select v-model="choice.price_basis" aria-label="采用价格"><el-option label="对客报价" value="CusPrice"/><el-option label="客确价格" value="Price"/></el-select>
        </template>
        <template v-else><label>手工单价</label><el-input v-model="choice.manual_price" inputmode="decimal" aria-label="手工单价"/></template>
      </div>
      <el-table v-if="choice.mode==='quote'&&rows.length" :data="rows" border max-height="260" size="small" aria-label="匹配报价">
        <el-table-column type="index" label="行" width="48"/><el-table-column prop="quote_id" label="报价记录" width="85"/><el-table-column prop="sheet_no" label="报价单" min-width="125"/>
        <el-table-column prop="sheet_date" label="日期" min-width="110"/><el-table-column prop="detail_no" label="报价明细" min-width="120"/>
        <el-table-column prop="prod_id" label="物料"/><el-table-column prop="yarn_category" label="供纱方式" min-width="95"/>
        <el-table-column label="对客报价"><template #default="s">{{s.row.cus_price??'未填写'}}</template></el-table-column><el-table-column label="客确价"><template #default="s">{{s.row.confirmed_price??'未填写'}}</template></el-table-column><el-table-column label="总单价"><template #default="s">{{s.row.total_price??'未填写'}}</template></el-table-column>
        <el-table-column label="原单位" min-width="95"><template #default="s">{{units.find(u=>u.value===s.row.price_unit)?.label??'未填写'}}</template></el-table-column>
        <el-table-column label="选择" width="100" fixed="right"><template #default="s"><el-button size="small" :type="choice.quote_id===s.row.quote_id&&choice.quote_head_id===s.row.quote_head_id?'primary':'default'" @click="choose(s.row)">采用此条</el-button></template></el-table-column>
      </el-table>
      <p v-if="choice.mode==='quote'">共 {{rows.length}} 条候选；同价、重复明细分别保留。没有匹配报价时可继续保留未计价，或明确手工录价。</p>
      <div class="price-controls">
        <label>本单计价单位</label><el-select v-model="choice.price_unit" clearable aria-label="本单计价单位"><el-option v-for="u in units" :key="u.value" :value="u.value" :label="u.label"/></el-select>
        <label>计价数量</label><el-select v-model="choice.quantity_mode" aria-label="计价数量方式"><el-option label="按订单数量与单位" value="order"/><el-option label="明确指定本单数量" value="explicit"/></el-select>
        <el-input v-if="choice.quantity_mode==='explicit'" v-model="choice.quantity" inputmode="decimal" aria-label="指定计价数量"/>
        <label>金额方式</label><el-select v-model="choice.amount_mode" aria-label="金额方式"><el-option label="按数量乘单价" value="calculated"/><el-option label="明确手工金额" value="manual"/></el-select>
        <el-input v-if="choice.amount_mode==='manual'" v-model="choice.manual_amount" inputmode="decimal" aria-label="手工金额"/>
        <label>采用说明</label><el-input v-model="choice.reason" aria-label="采用说明"/>
      </div>
      <p>报价原单位为空时，本单所选单位只记录在订单中。已有订单不随报价修改自动改价。</p>
      <div class="price-controls"><el-button :loading="busy" @click="prepare">预览计价</el-button><el-button @click="unchanged">取消本次选价</el-button><el-tag v-if="applied" type="success">选价待保存</el-tag></div>
      <el-alert v-if="preview" :title="'本次单价：'+(preview.price??'未计价')+'；金额：'+(preview.amount??'未完整计价')+'；数量依据：'+preview.adoption.quantity_basis" :type="preview.amount===null?'warning':'success'" :closable="false"/>
    </template>
  </div>
</template>
<style scoped>.order-price-chooser{width:100%;text-align:left}.price-controls{display:flex;align-items:center;flex-wrap:wrap;gap:10px;margin:12px 0}.price-controls .el-select,.price-controls .el-input{width:190px}.order-price-chooser p{color:var(--el-text-color-secondary);font-size:13px;line-height:1.5}</style>
