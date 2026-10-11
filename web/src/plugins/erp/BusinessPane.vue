<script setup lang="ts">
import {computed,ref,watch} from 'vue'
import {compute} from '@fast-crud/fast-crud'
import {ElMessage} from 'element-plus'
import {api} from '../../api'
import {useAccount} from '../../store'
import ResourceTable from '../../components/ResourceTable.vue'
import FieldInput from '../../components/FieldInput.vue'
import DocumentEditor from './DocumentEditor.vue'
const props=defineProps<{entity:string;context?:Record<string,any>;contextLabel?:string;readonly?:boolean}>()
const account=useAccount(),meta=ref<any>(),table=ref(),selected=ref<any>(),open=ref(false),activeTab=ref(''),editor=ref(false)
const actionOpen=ref(false),currentAction=ref<any>(),actionRow=ref<any>(),actionData=ref<Record<string,any>>({}),actionForm=ref(),saving=ref(false)
const workflow=computed(()=>meta.value?.workflow??{})
const tabs=computed(()=>(workflow.value.children??[]).filter((child:any)=>account.can(child.entity+':list')))
const frozen=(row:any)=>props.readonly||workflow.value.readonly||Boolean(workflow.value.editable_states&&!workflow.value.editable_states.includes(row[workflow.value.state_field??'status']))
function childReadonly(child:any){return child.parent_states?!child.parent_states.includes(selected.value[workflow.value.state_field??'status']):frozen(selected.value)}
async function submitAction(){
  await actionForm.value.validate()
  saving.value=true
  try{await api(`/api/system/${props.entity}/${actionRow.value.id}/${currentAction.value.key}/`,{method:'POST',data:actionData.value});actionOpen.value=false;ElMessage.success('操作成功');await table.value.refresh()}finally{saving.value=false}
}
const actions=computed(()=>{
  const result:any[]=[]
  if(tabs.value.length)result.push({key:'children',text:'明细与关联',permission:props.entity+':detail',click:(row:any)=>{selected.value=row;activeTab.value=tabs.value[0].entity;open.value=true}})
  if((workflow.value.children??[]).some((child:any)=>child.atomic))result.push({key:'document',text:'整单编辑',permission:props.entity+':save-document-post',show:(row:any)=>!frozen(row),click:(row:any)=>{selected.value=row;editor.value=true}})
  for(const action of workflow.value.actions??[])result.push({key:action.key,text:action.title,permission:props.entity+':'+action.key+'-post',show:(row:any)=>action.states.includes(row[workflow.value.state_field??'status'])&&!(props.entity==='erp_sampling_sampleconfirmation'&&action.key==='send'&&row.sent_at!==null),click:async(row:any)=>{
    if(action.inputs.length){currentAction.value=action;actionRow.value=row;actionData.value=Object.fromEntries(action.inputs.filter((f:any)=>f.kind==='datetime').map((f:any)=>[f.key,new Date().toISOString()]));actionOpen.value=true}
    else{await api(`/api/system/${props.entity}/${row.id}/${action.key}/`,{method:'POST',data:{}});ElMessage.success('操作成功');await table.value.refresh()}
  }})
  return result
})
watch(()=>[props.entity,account.menus,account.buttons],async()=>{
  const data=(await api('/api/meta/'+props.entity+'/')).data
  for(const field of data.fields)if(props.context&&field.key in props.context)field.form={...field.form,component:{name:'FieldInput',vModel:'modelValue',field:{...field},disabled:true}}
  data.crud_options={...data.crud_options,rowHandle:{width:620,buttons:{edit:{show:compute(({row}:any)=>!frozen(row)&&!(props.entity==='erp_sampling_sampleconfirmation'&&row.sent_at!==null)&&account.can(props.entity+':patch'))},remove:{show:compute(({row}:any)=>!frozen(row)&&account.can(props.entity+':delete'))},copy:{show:false}}}}
  meta.value=data
},{immediate:true})
</script>
<template>
  <div class="business-pane"><el-alert v-if="contextLabel" :title="contextLabel" type="info" :closable="false"/>
    <el-alert v-if="readonly" title="本层资料已经冻结，业务进度通过对应操作维护。" type="info" :closable="false"/>
    <ResourceTable v-if="meta" ref="table" :key="entity" :meta="meta" :context="context" :context-label="contextLabel" :readonly="readonly||workflow.readonly" :row-actions="actions"/><el-skeleton v-else animated/>
    <el-drawer v-model="open" :title="meta?.title+' · 明细与关联'" size="min(1400px, 97vw)" destroy-on-close>
      <el-tabs v-if="open" v-model="activeTab"><el-tab-pane v-for="child in tabs" :key="child.entity" :name="child.entity" :label="child.title">
        <BusinessPane v-if="activeTab===child.entity" :key="child.entity+'-'+selected.id" :entity="child.entity" :context="{[child.key]:selected.id}" :context-label="String(selected.number??selected.code??selected.name??selected.id)" :readonly="childReadonly(child)"/>
      </el-tab-pane></el-tabs>
    </el-drawer>
    <el-drawer v-model="editor" :title="meta?.title+' · 整单编辑'" size="min(1500px, 98vw)" destroy-on-close><DocumentEditor v-if="editor" :meta="meta" :row="selected" @saved="editor=false;table.refresh()"/></el-drawer>
    <el-dialog v-model="actionOpen" :title="currentAction?.title" width="600px" destroy-on-close><el-form v-if="actionOpen" ref="actionForm" :model="actionData" label-width="120px">
      <el-form-item v-for="field in currentAction.inputs" :key="field.key" :prop="field.key" :label="field.title" :rules="[{required:field.required,message:'请填写'+field.title}]"><FieldInput v-model="actionData[field.key]" :field="field"/></el-form-item>
    </el-form><template #footer><el-button @click="actionOpen=false">取消</el-button><el-button type="primary" :loading="saving" @click="submitAction">确认操作</el-button></template></el-dialog>
  </div>
</template>
<style scoped>.business-pane{height:100%;display:flex;flex-direction:column;gap:12px}.business-pane>.page{flex:1;min-height:0}.el-tabs{height:100%}</style>
