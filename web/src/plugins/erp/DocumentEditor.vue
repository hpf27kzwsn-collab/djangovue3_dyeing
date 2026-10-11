<script setup lang="ts">
import {computed,ref,onMounted} from 'vue'
import {ElMessage} from 'element-plus'
import {api} from '../../api'
import {useAccount} from '../../store'
import FieldInput from '../../components/FieldInput.vue'
const props=defineProps<{meta:any;row:any}>(),emit=defineEmits(['saved'])
const account=useAccount(),head=ref<Record<string,any>>({}),children=ref<any[]>([]),saving=ref(false),ready=ref(false)
const headFields=computed(()=>props.meta.fields.filter((f:any)=>!f.readonly&&f.is_update&&f.key!=='id'))
function values(row:any,fields:any[]){return Object.fromEntries(fields.filter(f=>f.key in row).map(f=>[f.key,row[f.key]]))}
function add(child:any){child.rows.push({data:Object.fromEntries(child.fields.map((f:any)=>[f.key,f.default])),id:null})}
function remove(child:any,index:string|number){const [row]=child.rows.splice(Number(index),1);if(row.id!==null)child.deleted.push(row.id)}
async function save(){
  saving.value=true
  try{
    const changes=Object.fromEntries(children.value.map(child=>[child.entity,{upsert:child.rows.map((row:any)=>({...values(row.data,child.fields),...(row.id!==null?{id:row.id}:{})})),delete:child.deleted}]))
    await api(`/api/system/${props.meta.entity}/${props.row.id}/save_document/`,{method:'POST',data:{head:values(head.value,headFields.value),children:changes}})
    ElMessage.success('表头与全部明细已保存');emit('saved')
  }finally{saving.value=false}
}
onMounted(async()=>{
  head.value=values(props.row,headFields.value)
  for(const config of props.meta.workflow.children.filter((child:any)=>child.atomic&&account.can(child.entity+':list'))){
    const meta=(await api('/api/meta/'+config.entity+'/')).data
    const child={...config,fields:meta.fields.filter((f:any)=>!f.readonly&&(f.is_create||f.is_update)&&!['id',config.key].includes(f.key)),rows:[] as any[],deleted:[] as number[]}
    let page=1,more=true
    while(more){const response=await api(`/api/system/${config.entity}/`,{params:{[config.key]:props.row.id,limit:200,page}});child.rows.push(...response.data.map((row:any)=>({id:row.id,data:values(row,child.fields)})));more=response.is_next===true;page++}
    children.value.push(child)
  }
  ready.value=true
})
</script>
<template>
  <el-skeleton v-if="!ready" animated/>
  <div v-else class="document-editor"><el-alert title="本页修改在点击保存后一次生效。确认前，请先保存明细。" type="info" :closable="false"/>
    <el-form label-width="150px"><el-form-item v-for="field in headFields" :key="field.key" :label="field.title"><FieldInput v-model="head[field.key]" :field="field"/></el-form-item></el-form>
    <section v-for="child in children" :key="child.entity"><h3>{{child.title}}</h3><el-button v-if="account.can(child.entity+':add')" @click="add(child)">添加明细</el-button>
      <div class="detail-row" v-for="(row,index) in child.rows" :key="row.id??'new-'+index"><el-form label-width="140px"><el-form-item v-for="field in child.fields" :key="field.key" :label="field.title"><FieldInput v-model="row.data[field.key]" :field="field" :disabled="row.id!==null?!field.is_update:!field.is_create"/></el-form-item></el-form><el-button type="danger" v-if="row.id===null||account.can(child.entity+':delete')" @click="remove(child,index)">移除此行</el-button></div>
    </section>
    <el-button type="primary" :loading="saving" @click="save">保存表头与明细</el-button>
  </div>
</template>
<style scoped>.document-editor{display:flex;flex-direction:column;gap:20px}.detail-row{border:1px solid var(--el-border-color);padding:16px;margin-top:12px}.el-form{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 20px}@media(max-width:800px){.el-form{grid-template-columns:1fr}}</style>
