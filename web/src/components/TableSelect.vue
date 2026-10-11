<script setup lang="ts">
import {ref,computed,watch,nextTick} from 'vue'
import {useFormItem} from 'element-plus'
import {api} from '../api'
const props=withDefaults(defineProps<{modelValue:any;config?:any;entity?:string;pk?:string;label?:string;multiple?:boolean;disabled?:boolean;columns?:any[];params?:Record<string,any>}>(),{pk:'id',label:'name',multiple:false,disabled:false,params:()=>({})}),emit=defineEmits(['update:modelValue'])
const {formItem}=useFormItem()
const standardColumns:Record<string,any[]>={user:[{field:'username',title:'登录账号'},{field:'name',title:'姓名'},{field:'dept_path',title:'部门'}],role:[{field:'name',title:'角色名称'},{field:'key',title:'权限字符'}],dept:[{field:'name',title:'部门名称'},{field:'key',title:'部门编码'},{field:'owner',title:'负责人'}],post:[{field:'name',title:'岗位名称'},{field:'code',title:'岗位编码'}],area:[{field:'name',title:'区域名称'},{field:'code',title:'区域编码'}]}
const setting=computed(()=>props.config?.setting||{primarykey:props.pk,field:props.label,searchField:props.columns||standardColumns[props.entity!]||[{field:props.label,title:'名称'}]})
const endpoint=computed(()=>props.config?`/api/system/system_config/${props.config.id}/table_data/`:`/api/system/${props.entity}/`)
const limit=ref(10),records=ref<Record<string,any>>({})
function remember(items:any[]){for(const row of items)records.value[String(row[setting.value.primarykey])]=row}
const open=ref(false),rows=ref<any[]>([]),page=ref(1),total=ref(0),search=ref(''),selected=ref<any[]>([])
const labels=ref<any[]>([]),values=computed(()=>props.multiple?(props.modelValue || []):props.modelValue==null||props.modelValue===''?[]:[props.modelValue])
watch([values,endpoint],async()=>{labels.value=values.value.length?(await api(endpoint.value,{params:{...props.params,[setting.value.primarykey+'__in']:values.value.join(','),limit:values.value.length}})).data:[];remember(labels.value)},{immediate:true,deep:true})
const query=()=>({...props.params,...(setting.value.treeField&&!search.value?{[setting.value.treeField]:'null'}:{}),page:page.value,limit:limit.value,search:search.value})
async function load(){const result=await api(endpoint.value,{params:query()});rows.value=result.data;total.value=result.total;remember(rows.value)}
async function show(){selected.value=[...values.value];open.value=true;await load()}
function choose(value:any,checked:any){selected.value=checked?[...selected.value,value]:selected.value.filter(x=>x!==value)}
function update(value:any){emit('update:modelValue',value);nextTick(()=>formItem?.validate('change',()=>{}))}
function save(){update(props.multiple?selected.value:selected.value[0]??null);open.value=false}
function clear(){update(props.multiple?[]:null);selected.value=[]}
function remove(value:any){update(props.multiple?values.value.filter((x:any)=>x!==value):null)}
async function loadChildren(row:any,node:any,resolve:any){const children:any[]=[];let next=1,total=0;do{const result=await api(endpoint.value,{params:{...props.params,[setting.value.treeField]:row._tree_id,page:next,limit:limit.value}});children.push(...result.data);total=result.total;next++}while(children.length<total);remember(children);resolve(children)}
defineExpose({open:show,load,clear,data:rows})
</script>
<template><div><el-tag v-for="row in labels" :key="row[setting.primarykey]" :closable="!disabled" @close="remove(row[setting.primarykey])">{{row[setting.field]}}</el-tag><el-button :disabled="disabled" @click="show">选择关联记录</el-button><el-button v-if="values.length&&!disabled" text @click="clear">清空</el-button></div><el-dialog v-model="open" title="选择关联记录" width="min(850px, calc(100vw - 24px))"><el-input v-model="search" placeholder="搜索记录" @keyup.enter="page=1;load()"/><div class="selected-records"><span>已选 {{selected.length}} 项</span><el-tag v-for="value in selected" :key="value" closable @close="choose(value,false)">{{records[String(value)]?.[setting.field]??value}}</el-tag></div><el-table :data="rows" :row-key="setting.primarykey" :lazy="!!setting.treeField" :load="loadChildren" :tree-props="{hasChildren:'has_children'}"><el-table-column width="70"><template #default="{row}"><el-checkbox v-if="multiple" :model-value="selected.includes(row[setting.primarykey])" @update:model-value="(value:any)=>choose(row[setting.primarykey],value)"/><el-radio v-else v-model="selected[0]" :value="row[setting.primarykey]">选择</el-radio></template></el-table-column><el-table-column v-for="field in setting.searchField.filter((x:any)=>x.visible!==false)" :key="field.field" :prop="field.field" :label="field.title" :min-width="field.width||160"/></el-table><el-pagination v-model:current-page="page" v-model:page-size="limit" :total="total" layout="prev,pager,next,total,sizes" @change="load"/><template #footer><el-button @click="selected=[]">清空选择</el-button><el-button @click="open=false">取消</el-button><el-button type="primary" @click="save">确认选择</el-button></template></el-dialog></template>


<style scoped>.selected-records{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:12px 0}.el-pagination{flex-wrap:wrap;margin-top:16px}.el-tag{max-width:100%;overflow:hidden}</style>
