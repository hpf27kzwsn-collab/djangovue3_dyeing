<script setup lang="ts">
import {onMounted,reactive,ref,toRaw} from 'vue'
import {api} from '../api'
import {ElMessage} from 'element-plus'
import FieldInput from './FieldInput.vue'
import TableSelect from './TableSelect.vue'
const props=defineProps<{group:any}>(),rows=ref<any[]>([]),form=reactive<Record<string,any>>({}),deleted=ref<number[]>([]),edit=ref<any>(),editorOpen=ref(false)
const options=reactive<Record<string,any[]>>({}),ruleTypes=ref<string[]>([])
let serial=0
const kinds=['text','datetime','date','textarea','select','checkbox','radio','image','attachment','boolean','number','array','images','select','multi','time']
const formRef=ref()
function rules(row:any){return row.form_item_type===11?[...row.rule,{type:'array',defaultField:{type:'object',fields:Object.fromEntries(['title','key','value'].map(key=>[key,{validator:(_rule:any,value:any)=>value==null||value===''?new Error('数组每行的标题、键名、键值均为必填'):true}]))}}]:row.rule}
async function loadOptions(row:any){options[row.localKey||row.id]=row.setting.dictionary?(await api('/api/dictionary/',{params:{key:row.setting.dictionary}})).data:row.data_options}
async function load(){deleted.value=[];rows.value=(await api('/api/system/system_config/tree/',{params:{parent:props.group.id}})).data;for(const row of rows.value){form[row.id]=row.value;await loadOptions(row)}}
onMounted(load)
async function save(){const valid=await formRef.value.validate((valid:boolean)=>valid);if(!valid)return;await api(`/api/system/system_config/${props.group.id}/content/`,{method:'PUT',data:{rows:rows.value.map(({localKey,...row})=>({id:row.id,title:row.title,key:row.key,status:row.status,form_item_type:row.form_item_type,data_options:row.data_options,rule:row.rule,placeholder:row.placeholder,setting:row.setting,sort:row.sort,value:form[localKey||row.id]})),deleted:deleted.value}});await load();ElMessage.success('配置已保存')}
function add(){const localKey='new-'+(++serial);edit.value={localKey,title:'',key:'',value:'',status:true,form_item_type:0,data_options:[],rule:[],placeholder:'',setting:{},sort:rows.value.length+1};ruleTypes.value=[];editorOpen.value=true}
function remove(row:any){if(row.id)deleted.value.push(row.id);rows.value=rows.value.filter(x=>x!==row)}
function editRow(row:any){edit.value=structuredClone(toRaw(row));ruleTypes.value=row.rule.filter((rule:any)=>rule.required||['email','url'].includes(rule.type)).map((rule:any)=>rule.required?'required':rule.type);editorOpen.value=true}
function setRules(values:string[]){edit.value.rule=edit.value.rule.filter((rule:any)=>!rule.required&&!['email','url'].includes(rule.type)).concat(values.map(type=>type==='required'?{required:true,message:'请填写'+edit.value.title}:{type,message:type==='email'?'邮箱格式不正确':'网址格式不正确'}))}
function changeKind(kind:number){edit.value.value=[5,11,12,14].includes(kind)?[]:kind===9?false:[1,2,4,6,13,15].includes(kind)?null:kind===10?0:''}
async function commit(){
  const row=edit.value,index=rows.value.findIndex(x=>row.id?x.id===row.id:x.localKey===row.localKey)
  const kindChanged=index!==-1&&rows.value[index].form_item_type!==row.form_item_type
  if([13,14].includes(row.form_item_type)){
    const {localKey,...data}=row
    data.value=kindChanged?row.value:form[row.localKey||row.id]??row.value
    const saved=(await api(`/api/system/system_config/${props.group.id}/content/`,{method:'PUT',data:{rows:[data],deleted:[]}})).data.find((item:any)=>item.key===row.key)
    Object.assign(row,saved);delete row.localKey;form[row.id]=row.value
  }
  if(index===-1){rows.value.push(row);form[row.localKey||row.id]=row.value}else{rows.value[index]=row;if(kindChanged)form[row.localKey||row.id]=row.value}
  await loadOptions(row);editorOpen.value=false
}
</script>
<template><el-form ref="formRef" :model="form" label-width="150px" scroll-to-error><el-form-item v-for="row in rows" :key="row.localKey||row.id" :label="row.title" :prop="String(row.localKey||row.id)" :rules="rules(row)"><div class="setting-value"><div class="setting-description"><small>{{group.key}}.{{row.key}}</small><el-switch v-model="row.status" active-text="前端公开"/><el-button text @click="editRow(row)">编辑字段</el-button><el-button text type="danger" @click="remove(row)">删除</el-button><el-popover trigger="click" width="350"><template #reference><el-button text>编辑名称 / 键</el-button></template><el-input v-model="row.title" placeholder="变量标题"/><el-input v-model="row.key" placeholder="变量名"/></el-popover></div><TableSelect v-if="[13,14].includes(row.form_item_type)" v-model="form[row.localKey||row.id]" :config="row" :multiple="row.form_item_type===14"/><FieldInput v-else v-model="form[row.localKey||row.id]" :field="{key:row.key,kind:kinds[row.form_item_type],options:options[row.localKey||row.id]||row.data_options,placeholder:row.placeholder}"/></div></el-form-item><el-form-item><el-button @click="add">新增配置项</el-button><el-button type="primary" @click="save">保存配置</el-button></el-form-item></el-form><el-dialog v-model="editorOpen" title="配置项" width="min(650px, calc(100vw - 24px))" append-to-body><el-form v-if="edit" label-width="100px"><el-form-item label="标题"><el-input v-model="edit.title"/></el-form-item><el-form-item label="配置键"><el-input v-model="edit.key"/></el-form-item><el-form-item label="类型"><el-select v-model="edit.form_item_type" @change="changeKind"><el-option v-for="(kind,index) in ['文本','日期时间','日期','多行文本','下拉','复选','单选','图片','文件','开关','数字','数组','多图片','关联对象','关联多对象','时间']" :key="index" :value="index" :label="kind"/></el-select></el-form-item><el-form-item label="排序"><el-input-number v-model="edit.sort"/></el-form-item><el-form-item label="提示"><el-input v-model="edit.placeholder"/></el-form-item><el-form-item v-if="[13,14].includes(edit.form_item_type)" label="关联设置"><FieldInput v-model="edit.setting" :field="{key:'setting',kind:'association',options:[]}"/></el-form-item><el-form-item v-if="[4,5,6].includes(edit.form_item_type)" label="字典键"><el-input v-model="edit.setting.dictionary" placeholder="字典编号；留空使用固定选项"/></el-form-item><el-form-item label="选项"><FieldInput v-model="edit.data_options" :field="{key:'data_options',kind:'json',options:[]}"/></el-form-item><el-form-item label="常用校验"><el-select v-model="ruleTypes" multiple @change="setRules"><el-option label="必填" value="required"/><el-option label="邮箱" value="email"/><el-option label="网址" value="url"/></el-select></el-form-item><el-form-item label="校验规则"><FieldInput v-model="edit.rule" :field="{key:'rule',kind:'json',options:[]}"/></el-form-item></el-form><template #footer><el-button @click="editorOpen=false">取消</el-button><el-button type="primary" @click="commit">{{[13,14].includes(edit?.form_item_type)?'保存字段并选择关联':'应用到表单'}}</el-button></template></el-dialog></template>
<style scoped>.setting-value{width:100%}.setting-description{display:flex;align-items:center;gap:12px;margin-bottom:8px}.setting-description small{flex:1;color:var(--el-text-color-secondary)}</style>
