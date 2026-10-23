<script setup lang="ts">
import {computed,ref,onMounted} from 'vue'
import {ElMessage} from 'element-plus'
import {api} from '../../api'
import {useAccount} from '../../store'
import FieldInput from '../../components/FieldInput.vue'
import {cloneDeep,isEqual} from 'lodash-es'
import {entryChoices,formEntry,entryRule,originalValues,formField,createValues,formRequired} from './source-form'
import OrderPriceChooser from './OrderPriceChooser.vue'
const props=defineProps<{meta:any;row:any;context?:Record<string,any>}>(),emit=defineEmits(['saved'])
const account=useAccount(),head=ref<Record<string,any>>({}),children=ref<any[]>([]),saving=ref(false),ready=ref(false)
const headForm=ref(),detailForms=ref<any[]>([]),useLayout=ref(true)
const headFields=computed(()=>props.meta.fields.filter((f:any)=>!f.readonly&&f.is_update&&f.key!=='id'))
const parentContext=computed(()=>originalValues(props.meta,head.value))
function values(row:any,fields:any[]){return Object.fromEntries(fields.filter(f=>f.key in row).map(f=>[f.key,row[f.key]]))}
function changed(row:any,original:any,fields:any[]){return Object.fromEntries(Object.entries(values(row,fields)).filter(([key,value])=>!isEqual(value,original[key])))}
function codeLocked(field:any){return props.meta.numbering?.some((rule:any)=>rule.field===field.key&&(!rule.entry||rule.entry===props.row.entry_name)&&!rule.allow_code_change)}
function input(meta:any,field:any,entry:string|undefined,row:any,context:Record<string,any>={}){return formField(meta,field,entry,row,context)}
function disabled(meta:any,field:any,entry:string|undefined){return useLayout.value&&entryRule(meta,entry,field.key)?.readonly===true}
function rules(meta:any,field:any,entry:string|undefined,row:any,original:any,useDefaults:boolean){
  if(original&&isEqual(row[field.key],original[field.key]))return []
  return formRequired(meta,field,entry,useDefaults)?[{required:true,message:'请填写'+input(meta,field,entry,row).title}]:[]
}
function add(child:any){child.rows.push({data:Object.fromEntries(child.fields.map((f:any)=>[f.key,f.default])),id:null,entry:formEntry(child.meta,child.entry,props.row.entry_name),useDefaults:true})}
function remove(child:any,index:string|number){const [row]=child.rows.splice(Number(index),1);if(row.id!==null)child.deleted.push(row.id)}
async function save(){
  await headForm.value.validate()
  for(const form of detailForms.value)await form.validate()
  saving.value=true
  try{
    const changes=Object.fromEntries(children.value.map(child=>[child.entity,{upsert:child.rows.map((row:any)=>{
      const data=row.id!==null&&props.meta.workflow.source_model?changed(row.data,row.original,child.fields.filter((field:any)=>field.is_update)):values(row.data,child.fields.filter((field:any)=>row.id===null?field.is_create:field.is_update))
      if(child.meta.workflow.order_pricing&&row.data._pricing)data._pricing=row.data._pricing
      return row.id===null?createValues(child.meta,data,row.entry,row.useDefaults):{...data,id:row.id}
    }).filter((row:any)=>!props.meta.workflow.source_model||!('id' in row)||Object.keys(row).length>1),delete:child.deleted}]))
    await api(`/api/system/${props.meta.entity}/${props.row.id}/save_document/`,{method:'POST',params:{_foundation:props.context?._foundation},data:{head:props.meta.workflow.source_model?changed(head.value,props.row,headFields.value):values(head.value,headFields.value),children:changes}})
    ElMessage.success('表头与全部明细已保存');emit('saved')
  }finally{saving.value=false}
}
onMounted(async()=>{
  head.value=values(props.row,headFields.value)
  for(const config of props.meta.workflow.children.filter((child:any)=>child.atomic&&account.can(child.entity+':list'))){
    const meta=(await api('/api/meta/'+config.entity+'/')).data
    const parentFields=new Set((meta.workflow?.parent_bindings??[]).filter((binding:any)=>binding.relation===config.key).flatMap((binding:any)=>binding.fields.map((field:any)=>field.field)))
    const child={...config,meta,fields:meta.fields.filter((f:any)=>!f.readonly&&(f.is_create||f.is_update)&&!['id',config.key].includes(f.key)&&!parentFields.has(f.key)),rows:[] as any[],deleted:[] as number[]}
    let page=1,more=true
    while(more){const response=await api(`/api/system/${config.entity}/`,{params:{[config.key]:props.row.id,limit:200,page}});child.rows.push(...response.data.map((row:any)=>({id:row.id,entry:row.entry_name,data:{...values(row,child.fields),pricing_info:row.pricing_info},original:cloneDeep(values(row,child.fields))})));more=response.is_next===true;page++}
    children.value.push(child)
  }
  ready.value=true
})
</script>
<template>
  <el-skeleton v-if="!ready" animated/>
  <div v-else class="document-editor"><el-alert title="本页修改在点击保存后一次生效。审核或其他业务操作前，请先保存明细。" type="info" :closable="false"/>
    <el-checkbox v-if="meta.workflow.source_model" v-model="useLayout">按业务类型的字段规则编辑</el-checkbox>
    <el-form ref="headForm" :model="head" label-width="150px"><el-form-item v-for="field in headFields" :key="field.key" :prop="field.key" :label="input(meta,field,row.entry_name,head).title" :rules="rules(meta,field,row.entry_name,head,row,false)"><FieldInput v-model="head[field.key]" :field="input(meta,field,row.entry_name,head)" :disabled="field.key in (meta.foundation?.filters??{})||codeLocked(field)||disabled(meta,field,row.entry_name)"/></el-form-item></el-form>
    <section v-for="child in children" :key="child.entity"><h3>{{child.title}}</h3><el-button v-if="account.can(child.entity+':add')" @click="add(child)">添加明细</el-button>
      <div class="detail-row" v-for="(detail,index) in child.rows" :key="detail.id??'new-'+index"><el-form ref="detailForms" :model="detail" label-width="140px">
        <el-form-item v-if="child.meta.workflow.order_pricing" label="染整报价" class="pricing-form-item"><OrderPriceChooser v-model="detail.data._pricing" :row="{...detail.data,id:detail.id,source_parent_1:row.id}" :order="{id:row.id,...head}"/></el-form-item>
        <el-form-item v-if="detail.id===null&&entryChoices(child.meta).length" label="明细业务类型" prop="entry" :rules="[{required:true,message:'请选择本行业务类型'}]"><el-select v-model="detail.entry" filterable><el-option v-for="entry in entryChoices(child.meta)" :key="entry.value" :label="entry.label+' · '+entry.value" :value="entry.value"/></el-select></el-form-item>
        <el-form-item v-if="detail.id===null&&entryChoices(child.meta).length" label="使用表单默认值"><el-switch v-model="detail.useDefaults"/></el-form-item>
        <el-form-item v-for="field in child.fields" :key="field.key" :prop="'data.'+field.key" :label="input(child.meta,field,detail.entry,detail.data,parentContext).title" :rules="rules(child.meta,field,detail.entry,detail.data,detail.original,detail.useDefaults)"><FieldInput v-model="detail.data[field.key]" :field="input(child.meta,field,detail.entry,detail.data,parentContext)" :disabled="(detail.id!==null?!field.is_update:!field.is_create)||disabled(child.meta,field,detail.entry)"/></el-form-item>
      </el-form><el-button type="danger" v-if="detail.id===null||account.can(child.entity+':delete')" @click="remove(child,index)">移除此行</el-button></div>
    </section>
    <el-button type="primary" :loading="saving" @click="save">保存表头与明细</el-button>
  </div>
</template>
<style scoped>.document-editor{display:flex;flex-direction:column;gap:20px}.detail-row{border:1px solid var(--el-border-color);padding:16px;margin-top:12px}.el-form{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 20px}.pricing-form-item{grid-column:1/-1}@media(max-width:800px){.el-form{grid-template-columns:1fr}}</style>
