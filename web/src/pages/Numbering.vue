<script setup lang="ts">
import {computed,onMounted,reactive,ref} from 'vue'
import {ElMessage} from 'element-plus'
import {api} from '../api'
import {useAccount} from '../store'
import {businessTitle} from '../erp-workspace'
import {notifyNumbering} from '../numbering'
const base='/api/system/erp_base_numberingrule/',account=useAccount()
const can=(action:string)=>account.can('erp_base_numberingrule:'+action)
const rows=ref<any[]>([]),catalog=ref<any[]>([]),open=ref(false),editing=ref<number>(),sample=ref<any>(),saving=ref(false)
const form=reactive<any>({})
const selectedModel=computed(()=>catalog.value.find(x=>x.value===form.target_model))
const selectedField=computed(()=>selectedModel.value?.fields.find((x:any)=>x.value===form.target_field))
const selectedScope=computed(()=>selectedField.value?.scopes.find((x:any)=>x.key===form.scope_key))
const modelTitle=(label:string)=>businessTitle(catalog.value.find(x=>x.value===label)?.title??label)
const fieldTitle=(row:any)=>row.name==='供应商'?'供应商编码':row.name==='客户'?'客户编码':catalog.value.find(x=>x.value===row.target_model)?.fields.find((x:any)=>x.value===row.target_field)?.title??row.target_field
const scopeTitle=(row:any)=>catalog.value.find(x=>x.value===row.target_model)?.fields.find((x:any)=>x.value===row.target_field)?.scopes.find((x:any)=>x.key===row.scope_key)?.title??row.scope_key
async function load(){rows.value=(await api(base,{params:{limit:1000}})).data}
onMounted(async()=>{catalog.value=(await api(base+'catalog/')).data;await load()})
function edit(row?:any){
  editing.value=row?.id
  Object.keys(form).forEach(key=>delete form[key])
  Object.assign(form,row?Object.fromEntries(['name','target_model','target_field','scope_key','prefix','digits','start_number','auto_enabled','allow_manual_input','allow_code_change','notes'].map(key=>[key,row[key]])):
    {name:'',target_model:'',target_field:'',scope_key:'',prefix:'',digits:3,start_number:'1',auto_enabled:true,allow_manual_input:true,allow_code_change:false,notes:''})
  sample.value=undefined;open.value=true
}
function chooseModel(){form.target_field='';form.scope_key='';sample.value=undefined}
function chooseField(){form.scope_key='';sample.value=undefined}
function chooseScope(){if(!editing.value)form.name=selectedScope.value?.title??'';sample.value=undefined}
async function preview(){sample.value=(await api(base+'preview/',{method:'POST',data:{...form,...(editing.value?{_id:editing.value}:{})}})).data}
async function save(){saving.value=true;try{await api(base+(editing.value?editing.value+'/':''),{method:editing.value?'PATCH':'POST',data:{...form}});notifyNumbering(form.target_model);open.value=false;await load();ElMessage.success('编号规则已保存')}finally{saving.value=false}}
async function synchronize(row:any){await api(base+row.id+'/synchronize/',{method:'POST'});await load();ElMessage.success('已按实际资料同步流水上限')}
</script>
<template><div class="page numbering-page"><div class="heading"><div><h1>编号管理</h1><p>设置资料编码与单据编号。规则只作用于后续保存，已有编号保持原值。</p></div><el-button v-if="can('add')" type="primary" @click="edit()">新增规则</el-button></div>
  <el-table :data="rows" border><el-table-column prop="name" label="规则名称" min-width="180"/><el-table-column label="业务资料" min-width="170"><template #default="{row}">{{modelTitle(row.target_model)}}</template></el-table-column><el-table-column label="编号字段" min-width="130"><template #default="{row}">{{fieldTitle(row)}}</template></el-table-column><el-table-column label="适用类别" min-width="150"><template #default="{row}">{{scopeTitle(row)}}</template></el-table-column><el-table-column label="编号格式" min-width="130"><template #default="{row}">{{row.prefix+'0'.repeat(row.digits)}}</template></el-table-column><el-table-column prop="last_number" label="已用流水上限" min-width="130"/><el-table-column label="录入方式" min-width="150"><template #default="{row}">{{row.auto_enabled?'自动编号':'手工编号'}}{{row.allow_manual_input&&row.auto_enabled?' / 允许手工':''}}</template></el-table-column><el-table-column label="更改编号" width="110"><template #default="{row}">{{row.allow_code_change?'未引用可更改':'不允许'}}</template></el-table-column><el-table-column label="操作" width="185" fixed="right"><template #default="{row}"><el-button v-if="can('patch')" link type="primary" @click="edit(row)">设置</el-button><el-button v-if="can('synchronize-post')" link type="primary" @click="synchronize(row)">同步上限</el-button></template></el-table-column></el-table>
  <el-dialog v-model="open" :title="editing?'设置编号规则':'新增编号规则'" width="660px" destroy-on-close><el-form label-width="130px" @input="sample=undefined">
    <el-form-item label="规则名称"><el-input v-model="form.name"/></el-form-item>
    <el-form-item label="业务模型"><el-select v-model="form.target_model" filterable :disabled="!!editing" @change="chooseModel"><el-option v-for="m in catalog" :key="m.value" :value="m.value" :label="businessTitle(m.title)"/></el-select></el-form-item>
    <el-form-item label="编号字段"><el-select v-model="form.target_field" :disabled="!!editing" @change="chooseField"><el-option v-for="f in selectedModel?.fields??[]" :key="f.value" :value="f.value" :label="f.title"/></el-select></el-form-item>
    <el-form-item label="适用类别"><el-select v-model="form.scope_key" :disabled="!!editing" @change="chooseScope"><el-option v-for="s in selectedField?.scopes??[]" :key="s.key" :value="s.key" :label="s.title"/></el-select></el-form-item>
    <el-form-item label="固定前缀"><el-input v-model="form.prefix" placeholder="留空表示纯数字"/></el-form-item>
    <el-form-item label="流水位数"><el-input-number v-model="form.digits" :min="1" :max="18" :precision="0"/></el-form-item>
    <el-form-item label="起始流水"><el-input v-model="form.start_number" inputmode="numeric" placeholder="例如 1；允许 0"/></el-form-item>
    <el-form-item label="自动编号"><el-switch v-model="form.auto_enabled"/></el-form-item>
    <el-form-item label="允许手工录入"><el-switch v-model="form.allow_manual_input"/></el-form-item>
    <el-form-item label="允许更改编号"><div><el-switch v-model="form.allow_code_change" :disabled="!selectedField?.can_change"/><p class="hint">{{selectedField?.change_capability}}</p></div></el-form-item>
    <el-form-item label="规则说明"><el-input v-model="form.notes" type="textarea"/></el-form-item>
    <el-form-item v-if="sample" label="下一个编号"><div><strong>{{sample.code}}</strong><p class="hint">已用流水上限：{{sample.baseline??'尚未使用'}}。预览不占号，保存资料时确定实际编号。</p></div></el-form-item>
  </el-form><template #footer><el-button @click="open=false">取消</el-button><el-button v-if="can('preview-post')" @click="preview">预览编号</el-button><el-button type="primary" :loading="saving" @click="save">保存规则</el-button></template></el-dialog>
</div></template>
<style scoped>.heading{display:flex;align-items:center;justify-content:space-between}.heading h1{margin:0}.heading p,.hint{color:var(--el-text-color-secondary)}.hint{font-size:13px;margin:8px 0 0}.el-select{width:100%}.numbering-page{gap:20px}</style>
