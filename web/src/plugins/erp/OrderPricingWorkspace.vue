<script setup lang="ts">
import {ref,onMounted,computed} from 'vue'
import {ElMessage} from 'element-plus'
import {api} from '../../api'
import OrderPriceChooser from './OrderPriceChooser.vue'
import {useAccount} from '../../store'
const props=defineProps<{row:any}>(),emit=defineEmits(['saved'])
const data=ref<any>(),selected=ref<any>(),choice=ref<any>(),saving=ref(false)
const chooser=ref<InstanceType<typeof OrderPriceChooser>>()
const account=useAccount()
const frozen=computed(()=>data.value?.historical||['confirmed','approved'].includes(props.row.approval_stage)||!account.can('erp_sales_sourcedyeordercolor:patch'))
async function load(){data.value=(await api(`/api/system/erp_sales_sourcedyeordermain/${props.row.id}/pricing_lines/`)).data}
function edit(row:any){selected.value={...row,source_parent_1:props.row.id};choice.value=undefined}
async function save(){
  saving.value=true
  try{const value=await chooser.value!.prepare();if(value===null)return;await api(`/api/system/erp_sales_sourcedyeordercolor/${selected.value.id}/`,{method:'PATCH',data:{_pricing:value}});selected.value=undefined;await load();emit('saved');ElMessage.success('订单单价、金额及采用来源已保存')}finally{saving.value=false}
}
onMounted(load)
</script>
<template>
  <div v-if="data" class="pricing-workspace">
    <p>订单 {{data.sheet_no}} · 客户 {{data.customer_id}} · {{data.summary.line_count}} 行</p>
    <el-alert v-if="frozen" title="历史原值或已确认单据保留现有价格；此处可查询，采用价格请在可办理的新业务单据中操作。" type="info" :closable="false"/>
    <el-alert :title="data.summary.total===null?'已计价小计：'+data.summary.known_subtotal+' 元；尚有 '+data.summary.unpriced_count+' 行未完整计价':'订单金额合计：'+data.summary.total+' 元'" :type="data.summary.total===null?'warning':'success'" :closable="false"/>
    <el-table :data="data.rows" border max-height="430" aria-label="订单计价明细">
      <el-table-column prop="old_check_no" label="订单明细" min-width="130"/><el-table-column prop="old_prod_id" label="物料"/>
      <el-table-column prop="old_order_qty" label="订单数量"/><el-table-column prop="old_unit" label="数量单位"/>
      <el-table-column prop="old_price" label="染整单价"/><el-table-column prop="old_amount" label="行金额"/>
      <el-table-column label="采用来源" min-width="160"><template #default="s">{{s.row.pricing_info?.quote_sheet_no??(s.row.pricing_info?.mode==='manual'?'手工议价':'尚未采用报价')}}</template></el-table-column>
      <el-table-column label="操作" width="170" fixed="right"><template #default="s"><el-button @click="edit(s.row)">{{frozen?'查看采用记录':'选择或重取报价'}}</el-button></template></el-table-column>
    </el-table>
    <el-dialog :model-value="!!selected" title="订单明细选价" width="min(1200px, 94vw)" append-to-body @close="selected=undefined">
      <template v-if="selected"><p>物料 {{selected.old_prod_id}} · 数量 {{selected.old_order_qty}} {{selected.old_unit}}</p><OrderPriceChooser ref="chooser" :key="selected.id" v-model="choice" :row="selected" :order="{...row,old_customer_id:data.customer_id}" :readonly="frozen"/></template>
      <template #footer><el-button @click="selected=undefined">关闭</el-button><el-button v-if="!frozen" type="primary" :loading="saving" @click="save">保存本行计价</el-button></template>
    </el-dialog>
  </div><el-skeleton v-else animated/>
</template>
<style scoped>.pricing-workspace .el-alert{margin:12px 0}</style>
