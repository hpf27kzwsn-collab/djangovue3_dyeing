<script setup lang="ts">
import {computed,ref, onMounted,reactive,watch,defineAsyncComponent,onActivated,onDeactivated} from 'vue'
import {useFs, dict,compute} from '@fast-crud/fast-crud'
import {ElMessage} from 'element-plus'
import {api,download} from '../api'
import {useAccount} from '../store'
import {useRoute,useRouter} from 'vue-router'
import {toTree} from '../tree'
import RolePermissions from './RolePermissions.vue'
import SettingsForm from './SettingsForm.vue'
import MediaPreview from './MediaPreview.vue'
import ExcelImport from './ExcelImport.vue'
import {searches} from '../resource-config'
import MessageRecipients from './MessageRecipients.vue'
import RoleUsers from './RoleUsers.vue'
import {useMobile} from '../mobile'
import {resourceQuery} from '../resource-query'
import {fileSize} from '../tag-color'
import {componentNames} from '../page-catalog'
import {merge,isEqual} from 'lodash-es'
const Resource=defineAsyncComponent(()=>import('../pages/Resource.vue'))
const ChartPanel=defineAsyncComponent(()=>import('./ChartPanel.vue'))
const DepartmentCharts=defineAsyncComponent(()=>import('./DepartmentCharts.vue'))
const props=defineProps<{meta:any;context?:Record<string,any>;contextLabel?:string;chartDemo?:boolean;readonly?:boolean;disableDelete?:boolean;rowActions?:Array<{key:string;text:string;permission:string;show?:(row:any)=>boolean;click:(row:any)=>void}>}>(), account=useAccount()
const route=useRoute(),router=useRouter()
const ownPath=route.path,active=ref(true)
onActivated(async()=>{active.value=true;if(!props.context&&isOwnRoute()&&JSON.stringify(context.value)!==JSON.stringify(route.query)){context.value={...route.query};await updateContext()}})
onDeactivated(()=>active.value=false)
const mobile=useMobile(),treeOpen=ref(false),includeChildren=ref(false),showDepartmentSummary=ref(true),departmentInfo=ref<any>()
const entity=props.meta.entity, base=`/api/system/${entity}/`
const context=ref<Record<string,any>>({...props.context??route.query}),treeVersion=ref(0),workspaceRow=ref<any>(),workspaceTab=ref('main')
const editable=!props.readonly&&!['operation_log','login_log','download_center','task_result'].includes(entity)
const selection=ref<any[]>([]), role=ref<any>(), permissionOpen=ref(false), importOpen=ref(false)
const tree=ref<any[]>([]),contextTitle=ref(''),jsonDetail=ref<any>(),recipientMessage=ref<any>(),recipientsOpen=ref(false)
const settings=ref<any>(),settingsOpen=ref(false),userGrantOpen=ref(false),grantRole=ref<any>()
const passwordRef=ref(),passwordUser=ref<any>(),passwordForm=reactive({password:'',password_confirm:''}),passwordOpen=ref(false),preview=ref<any>(),models=ref<any[]>([]),model=ref(''),matchOpen=ref(false)
const buttonEntity=ref(''),buttonEditorOpen=ref(false)
const pageMenuId=account.menus.find(menu=>menu.web_path===ownPath)?.id
const pageMenu=computed(()=>account.menus.find(menu=>menu.id===pageMenuId))
const permissionPrefix=computed(()=>!props.context&&pageMenu.value?.component==='system/Resource'?pageMenu.value.component_name:entity)
const can=(action:string)=>account.can(`${permissionPrefix.value}:${action}`)
const isOwnRoute=()=>route.path===(pageMenu.value?.web_path||ownPath)
function payload(form:any,operation='is_create',original?:any) {
  const data:any={}
  for(const field of props.meta.fields) {
    if(field.readonly || !field[operation] || !(field.key in form)) continue
    if(operation==='is_update'&&props.meta.workflow?.source_model&&isEqual(form[field.key],original[field.key]))continue
    if((operation==='is_update' && entity==='user' && field.key==='password') || (field.kind==='file' && !(form[field.key] instanceof File))) continue
    data[field.key]=form[field.key]
  }
  if(operation==='is_create'&&form._entry){
    const entry=props.meta.workflow.entries.find((value:any)=>value.value===form._entry)
    data._entry=form._entry
    if(form._use_entry_defaults!==false)for(const key of entry.generated_fields)if(data[key]===null||data[key]==='')delete data[key]
  }
  if(Object.values(data).some(x=>x instanceof File)) {const upload=new FormData();for(const [key,value] of Object.entries(data)) if(value!==null) upload.append(key,value as any);return upload}
  return data
}
function createCrudOptions() {
  const columns:any={_selected:{column:{type:'selection',width:48,reserveSelection:true},form:{show:false},search:{show:false}},_index:{title:'序号',column:{width:70,formatter:({index}:any)=>(crudBinding.value.pagination!.currentPage-1)*crudBinding.value.pagination!.pageSize+index+1},form:{show:false},search:{show:false}}}
  if(props.meta.workflow?.entries?.length){
    const entries=props.meta.workflow.entries
    columns._entry={title:'业务类型',type:'dict-select',dict:dict({data:entries,value:'value',label:'label'}),
      column:{show:false},search:{show:false},form:{value:entries.length===1?entries[0].value:undefined},
      addForm:{show:true},editForm:{show:false},viewForm:{show:false}}
    columns._use_entry_defaults={title:'使用自动编号和默认值',column:{show:false},search:{show:false},
      form:{value:true,component:{name:'el-switch',vModel:'modelValue'}},
      addForm:{show:compute(({form}:any)=>Boolean(form._entry))},editForm:{show:false},viewForm:{show:false}}
  }
  for(const field of props.meta.fields) {
    const isOptions=['select','multi'].includes(field.kind)
    columns[field.key]={title:field.title,type:isOptions?'dict-select':field.kind==='number'?'number':'text',
      ...(isOptions?{dict:dict({data:field.options,value:'value',label:'label'})}:{}),
      column:{show:field.is_query && !(entity==='user' && field.key==='password') && !['description','creator','modifier','dept_belong','create_datetime','update_datetime'].includes(field.key),minWidth:140,sortable:'custom',
        ...(field.kind==='multi'?{component:{multiple:true}}:{}),
        ...(field.kind==='boolean'?{formatter:({value}:any)=>value==null?'未填写':field.title==='成功'?(value?'成功':'失败'):(value?'是':'否')}:{}),
        ...(field.kind==='json'?{formatter:({value}:any)=>JSON.stringify(value)}:{})},
      search:{show:field.is_query&&(searches[entity]?.includes(field.key)??(!field.readonly&&['select','boolean'].includes(field.kind))),component:{name:'FieldInput',vModel:'modelValue',field:field.kind==='boolean'?{...field,kind:'select',options:[{label:'是',value:true},{label:'否',value:false}]}:field}},
      form:{show:!field.readonly,value:field.key in context.value ? field.options.find((x:any)=>String(x.value)===context.value[field.key])?.value ?? context.value[field.key] : entity==='user'&&field.key==='gender'?1:field.default,component:{name:'FieldInput',vModel:'modelValue',field:entity==='system_config' && field.key==='setting'?{...field,kind:'association'}:{...field,...(entity==='user'&&field.key==='avatar'?{kind:'avatar'}:entity==='message_center'&&field.key==='content'?{kind:'richtext'}:entity==='menu'&&field.key==='icon'?{kind:'icon'}:entity==='dictionary'&&field.key==='color'?{kind:'color'}:entity==='api_white_list'&&field.key==='url'?{kind:'api-path'}:entity==='message_center'&&field.key==='target_dept'?{remote:{entity:'dept',pk:'id',label:'name'}}:{})}},
        rules:field.required?[{required:true,message:`请填写${field.title}`}]:[]},
      addForm:{show:!field.readonly && field.is_create},editForm:{show:!field.readonly && field.is_update && !(entity==='user' && field.key==='password')},viewForm:{show:field.is_query}
    }
    if(field.display_key)columns[field.key].column={...columns[field.key].column,component:undefined,formatter:({row}:any)=>row[field.display_key]}
    if(field.dictionary)columns[field.key].column.component={name:'DictionaryBadge',modelValue:compute(({row}:any)=>row[field.key]),options:field.options}
    if(entity==='dictionary'&&field.key==='color')columns[field.key].column.component={name:'ColoredTag',color:compute(({row}:any)=>row.color),label:compute(({row}:any)=>row.label)}
    if(entity==='dictionary'){
      if(['parent','is_value'].includes(field.key))for(const operation of ['column','form','addForm','editForm','search'])columns[field.key][operation].show=false
      if(['type','color'].includes(field.key))for(const operation of ['column','form','addForm','editForm'])columns[field.key][operation].show=compute(()=>!!context.value.parent&&(operation==='column'?field.is_query:!field.readonly&&(operation==='addForm'?field.is_create:operation==='editForm'?field.is_update:true)))
    }
    if((entity==='user'&&field.key==='is_active')||(entity==='area'&&field.key==='enable'))columns[field.key].column.component={name:'el-switch',modelValue:compute(({row}:any)=>row[field.key]),disabled:!can('patch')||!field.is_update,'onUpdate:modelValue':compute(({row}:any)=>async(value:boolean)=>{await api(`${base}${row[props.meta.pk]}/`,{method:'PATCH',data:{[field.key]:value}});row[field.key]=value})}
    if(entity==='user'&&field.key==='avatar')columns[field.key].column.component={name:'el-avatar',src:compute(({row}:any)=>row.avatar)}
    if(field.column)merge(columns[field.key].column,field.column)
    if(field.form)merge(columns[field.key].form,field.form)
    if(columns[field.key].search.show&&field.kind==='text'&&!field.source){columns[field.key].search.show=false;columns[field.key+'__icontains']={title:field.title,column:{show:false},form:{show:false},search:{show:true,component:{name:'FieldInput',vModel:'modelValue',field}}}}
    if(['dept','menu'].includes(entity)&&field.key==='sort')columns[field.key].form.value=undefined
    if(field.source){columns[field.key].column.sortable=false;columns[field.key].search.show=false}
    if(entity==='message_center'&&['target_user','target_role','target_dept'].includes(field.key)){
      const target=['target_user','target_role','target_dept'].indexOf(field.key)
      for(const operation of ['addForm','editForm'])columns[field.key][operation].show=compute(({form}:any)=>form.target_type===target&&field[operation==='addForm'?'is_create':'is_update'])
      columns[field.key].form.rules=compute(({form}:any)=>form.target_type===target?[{required:true,type:'array',min:1,message:`请选择${field.title}`}]:[])
    }
    if(entity==='user'&&['name','description','dept','role'].includes(field.key))columns[field.key].form.rules=[{required:true,message:`请填写${field.title}`}]
    if((entity==='user'&&field.key==='password')||(entity==='dept'&&field.key==='key')||(entity==='role'&&field.key==='sort')||(['menu_button','api_white_list'].includes(entity)&&field.key==='method')||(entity==='message_center'&&field.key==='target_type')||(entity==='dictionary'&&['label','value','type','status','sort'].includes(field.key)))columns[field.key].form.rules=[{required:true,message:`请填写${field.title}`}]
    if(entity==='user'&&field.key==='email')columns[field.key].form.rules=[{type:'email',message:'邮箱格式不正确',trigger:['blur','change']}]
    if(entity==='dept'&&field.key==='parent'&&!('parent' in context.value))columns[field.key].form.value=account.user.dept
    if(entity==='system_config'&&['parent','form_item_type'].includes(field.key))columns[field.key].form.rules=compute(({form}:any)=>form.parent!=null||context.value.parent?[{required:true,message:`请选择${field.title}`}]:[])
    if(entity==='menu'){
      if(field.key==='cache')columns[field.key].form.value=true
      if(field.key==='component')columns[field.key].form.component.field={...field,kind:'autocomplete',options:componentNames.map(value=>({value,label:value}))}
      const condition=(form:any)=>field.key==='visible'?form.status:['is_link','cache','is_affix'].includes(field.key)?!form.is_catalog:field.key==='is_iframe'||field.key==='link_url'?!form.is_catalog&&form.is_link:['component','component_name'].includes(field.key)?!form.is_catalog&&!form.is_link:field.key==='resource'?!form.is_catalog&&!form.is_link&&form.component==='system/Resource':true
      for(const operation of ['form','addForm','editForm'])columns[field.key][operation].show=compute(({form}:any)=>!field.readonly&&(operation==='form'||field[operation==='addForm'?'is_create':'is_update'])&&condition(form))
      if(['component','component_name','link_url','resource'].includes(field.key))columns[field.key].form.rules=compute(({form}:any)=>condition(form)?[{required:true,message:`请填写${field.title}`},...(field.key==='link_url'?[{validator:(_rule:any,value:string)=>value?.startsWith('/')||URL.canParse(value)&&['http:','https:'].includes(new URL(value).protocol)||new Error('请填写站内地址或 http/https 链接')}]:[])]:[])
      if(field.key==='web_path')columns[field.key].form.rules=[{required:true,message:'请填写路由地址'},{validator:(_rule:any,value:string)=>value?.startsWith('/')||new Error('路由地址应以 / 开始')}]
    }
  }
  for(const field of props.meta.fields.filter((f:any)=>f.is_query&&f.kind==='datetime'&&['create_datetime','update_datetime','date_done'].includes(f.key)))for(const [suffix,label] of [['gte','起'],['lte','止']]){columns[field.key+'__'+suffix]={title:field.title+'（'+label+'）',column:{show:false},form:{show:false},search:{show:true,component:{name:'FieldInput',vModel:'modelValue',field}}}}
  columns.search={title:'关键词',type:'text',column:{show:false},form:{show:false},search:{show:true}}
  const buttons:any={view:{show:can('detail')},edit:{show:editable&&can('patch')},remove:{show:!props.readonly&&!['operation_log','login_log'].includes(entity)&&can('delete')}}
  buttons.copy={text:'复制',show:editable&&can('copy'),click:({row}:any)=>crudExpose.openCopy({row})}
  if(entity==='role') buttons.permissions={text:'权限配置',show:can('permissions-get'),click:({row}:any)=>{role.value=row;permissionOpen.value=true}}
  if(entity==='role') buttons.users={text:'授权用户',show:can('users-get'),click:({row}:any)=>{grantRole.value=row;userGrantOpen.value=true}}
  if(entity==='dept') buttons.users={text:'部门用户',show:account.can('user:list'),click:({row}:any)=>{workspaceRow.value=row;workspaceTab.value='users'}}
  if(entity==='dictionary')buttons.items={text:'字典配置',show:compute(({row}:any)=>can('list')&&!row.is_value),click:({row}:any)=>router.push({path:'/system/dictionary',query:{parent:row.id,parent_title:row.label}})}
  if(entity==='menu') {
    buttons.buttons={text:'按钮',show:account.can('menu_button:list'),click:({row}:any)=>{workspaceRow.value=row;workspaceTab.value='buttons'}}
    buttons.fields={text:'字段',show:account.can('column:list'),click:({row}:any)=>{workspaceRow.value=row;workspaceTab.value='fields'}}
  }
  if(['dept','menu'].includes(entity))for(const direction of ['up','down'])buttons[direction]={text:direction==='up'?'上移':'下移',show:can('move-'+direction+'-post'),click:async({row}:any)=>{await api(base+'move_'+direction+'/',{method:'POST',data:{id:row.id}});await refreshTree()}}
  if(entity==='system_config') buttons.settings={text:'配置表单',show:can('content-put'),click:({row}:any)=>{settings.value=row;settingsOpen.value=true}}
  if(entity==='user'){
    buttons.reset={text:'重置密码',show:account.superuser&&can('reset-password-post'),click:({row}:any)=>{passwordUser.value=row;passwordForm.password='';passwordForm.password_confirm='';passwordOpen.value=true}}
    buttons.defaultPassword={text:'恢复默认密码',show:account.superuser&&can('reset-to-default-password-put'),click:async({row}:any)=>{await api(`${base}${row.id}/reset_to_default_password/`,{method:'PUT',data:{}});ElMessage.success('已恢复配置的默认密码')}}
  }
  if(['operation_log','task_result'].includes(entity))buttons.json={text:'JSON 明细',show:can('detail'),click:({row}:any)=>{jsonDetail.value=row}}
  if(entity==='message_center')buttons.recipients={text:'收件明细',show:can('recipients-get'),click:({row}:any)=>{recipientMessage.value=row;recipientsOpen.value=true}}
  if(entity==='message_center') buttons.publish={text:'发布',show:can('publish-post'),click:async({row}:any)=>{const result=await api(`${base}${row.id}/publish/`,{method:'POST',data:{}});ElMessage.success(`已发送给 ${result.data.count} 位用户`)}}
  if(entity==='periodic_task') buttons.run={text:'执行一次',show:can('run-post'),click:async({row}:any)=>{await api(`${base}${row.id}/run/`,{method:'POST',data:{}});ElMessage.success('任务已提交')}}
  if(entity==='file'||entity==='download_center') buttons.download={text:'下载',show:compute(({row}:any)=>entity==='file'||row.task_status===2),click:({row}:any)=>window.open(row.url)}
  if(entity==='file')buttons.preview={text:'预览',click:({row}:any)=>preview.value=row}
  if(entity==='file'){columns._preview={title:'预览',column:{width:100,component:{name:'FileThumbnail',file:compute(({row}:any)=>row),onPreview:(row:any)=>preview.value=row}},form:{show:false},search:{show:false}};columns.size.column.formatter=({value}:any)=>fileSize(value)}
  for(const action of props.rowActions??[])buttons[action.key]={text:action.text,show:compute(({row}:any)=>account.can(action.permission)&&(!action.show||action.show(row))),click:({row}:any)=>action.click(row)}
  return {crudOptions:merge({
    request:{pageRequest:(query:any)=>api(base,{params:resourceQuery({...query,...context.value,...(entity==='user'?{include_children:includeChildren.value}:{})})}),addRequest:({form}:any)=>api(base,{method:'POST',data:payload(form)}),
      editRequest:({form,row}:any)=>api(`${base}${row[props.meta.pk]}/`,{method:'PATCH',data:payload(form,'is_update',row)}),
      delRequest:async({row}:any)=>{const result=await api(`${base}${row[props.meta.pk]}/`,{method:'DELETE'});deselect(row);await loadTree();return result}},
    table:{rowKey:props.meta.pk,onSelectionChange:(rows:any[])=>selection.value=rows},toolbar:{buttons:{export:{show:false}}},
    actionbar:{buttons:{add:{show:editable&&can('add')}}},rowHandle:{width:entity==='role'||entity==='user'?340:240,buttons},
    form:{labelWidth:mobile.value?'auto':'140px',labelPosition:mobile.value?'top':'right',scrollToError:true,afterSubmit:async()=>{ElMessage.success('保存成功');await loadTree();if(entity==='menu')await account.load()}},columns
  },props.meta.crud_options)}
}
const {crudBinding,crudRef,crudExpose,appendCrudBinding,resetCrudOptions}=useFs({createCrudOptions})
watch(mobile,value=>{
  const form={labelWidth:value?'auto':'140px',labelPosition:value?'top':'right'}
  appendCrudBinding({form,addForm:form,editForm:form,viewForm:form})
})
watch(()=>props.meta,async()=>{
  const options=createCrudOptions().crudOptions,pagination={...crudBinding.value.pagination}
  const search=Object.fromEntries(Object.entries(crudExpose.getSearchFormData()).filter(([key])=>options.columns[key]&&options.columns[key].search?.show!==false))
  resetCrudOptions(options)
  crudExpose.setSearchFormData({form:search})
  appendCrudBinding({pagination})
  await updateContext()
})
async function refresh(){await crudExpose.doRefresh()}
defineExpose({refresh})
async function loadTree(){if(entity==='area'){tree.value=(await api(base+'children/')).data;treeVersion.value++}else if(['dept','dictionary','menu','system_config'].includes(entity))tree.value=toTree((await api(base+'tree/')).data,props.meta.pk)}
async function refreshTree(){await refresh();await loadTree()}
async function updateContext(){
  const parentKey=entity==='area'?'pcode':'parent',parent=context.value[parentKey]
  const initialParent=parent===undefined&&entity==='dept'?account.user.dept??null:parent??null
  appendCrudBinding({addForm:{initialForm:{[parentKey]:initialParent,...(entity==='dictionary'?{is_value:!!parent}:{})}}})
  contextTitle.value=props.contextLabel||context.value.parent_title||context.value.menu_title||String(context.value.menu||parent||'')
  clearSelected()
  await refresh()
}
onMounted(async()=>{
  await updateContext();await loadTree()
})
watch(()=>route.query,async query=>{if(!props.context&&active.value&&isOwnRoute()){context.value={...query};await updateContext()}})
watch(()=>props.context,async value=>{if(value){context.value={...value};await updateContext()}},{deep:true})
async function loadArea(node:any,resolve:any){const params=node.level===0?{}:{pcode:node.data.code};resolve((await api(base+'children/',{params})).data)}
function exportFilters(){return resourceQuery({...crudExpose.getSearchFormData(),...context.value,...(entity==='user'?{include_children:includeChildren.value}:{})})}
function clearSelected(){crudExpose.getBaseTableRef().clearSelection();selection.value=[]}
function deselect(row:any){crudExpose.getBaseTableRef().toggleRowSelection(row,false)}
async function removeSelected(){await api(base+'multiple_delete/',{method:'DELETE',data:{keys:selection.value.map(x=>x[props.meta.pk])}});clearSelected();await refreshTree()}
async function asynchronous(){await api(base+'async_export/',{method:'POST',data:{},params:exportFilters()});ElMessage.success('导出任务已提交，可在下载中心查看')}
async function filterTree(row:any){treeOpen.value=false;workspaceRow.value=row;contextTitle.value=row.name||row.title||row.label;if(entity==='dept'&&account.can('user:list'))workspaceTab.value='users';if(entity==='menu'&&account.can('menu_button:list'))workspaceTab.value='buttons';context.value={...context.value,parent_title:row.name||row.title||row.label,[entity==='area'?'pcode':'parent']:row[props.meta.pk]};crudExpose.setSearchFormData({form:{}});await updateContext()}
async function allRows(){workspaceRow.value=undefined;workspaceTab.value='main';context.value={...context.value};delete context.value[entity==='area'?'pcode':'parent'];delete context.value.parent_title;crudExpose.setSearchFormData({form:{}});await updateContext()}
async function departmentSummary(){await refresh();departmentInfo.value=(await api(`/api/system/dept/${context.value.dept}/info/`,{params:{include_children:includeChildren.value}})).data}
watch(()=>context.value.dept,async dept=>{if(entity==='user'&&dept)departmentInfo.value=(await api(`/api/system/dept/${dept}/info/`,{params:{include_children:includeChildren.value}})).data},{immediate:true})
async function sortTree(){const rows:any[]=[];function walk(nodes:any[],parent:number|null=null){nodes.forEach((node,sort)=>{rows.push({id:node.id,parent,sort});walk(node.children,node.id)})}walk(tree.value);await api(base+'batch_update/',{method:'PUT',data:rows});await refreshTree()}
async function resetPassword(){if(!await passwordRef.value.validate(()=>{}))return;await api(`${base}${passwordUser.value.id}/reset_password/`,{method:'POST',data:passwordForm});passwordOpen.value=false;ElMessage.success('密码已重置')}
async function matchFields(){await api(base+'auto_match_fields/',{method:'POST',data:{model:model.value,menu:context.value.menu}});matchOpen.value=false;await refresh()}
async function showMatch(){models.value=(await api(base+'get_models/')).data;matchOpen.value=true}
async function createButtons(){models.value=props.meta.resources;buttonEntity.value='';buttonEditorOpen.value=true}
async function saveButtons(){await api(base+'batch_create/',{method:'POST',data:{menu:context.value.menu,entity:buttonEntity.value}});buttonEditorOpen.value=false;await refresh();await account.load();ElMessage.success('按钮已生成')}
</script>
<template><div class="page"><div class="page-heading"><h2>{{meta.title}}</h2><div class="toolbar"><el-button v-if="entity==='message_center'" @click="router.push('/inbox')">我的接收</el-button><el-button v-if="mobile&&tree.length" @click="treeOpen=!treeOpen">{{treeOpen?'收起筛选':'树形筛选'}}</el-button>
  <el-button v-if="entity==='column'&&context.menu&&can('auto-match-fields-post')" @click="showMatch">自动匹配模型字段</el-button>
  <el-button v-if="entity==='menu_button'&&context.menu&&can('batch-create-post')" @click="createButtons">批量生成按钮</el-button>
  <el-button v-if="can('export-get')" @click="download(base+'export/',meta.title+'导出.xlsx',exportFilters())">导出</el-button>
  <el-button v-if="can('async-export-post')" @click="asynchronous">异步导出</el-button>
  <el-button v-if="meta.excel_import&&can('import-template-get')" @click="download(base+'import_template/',meta.title+'新增模板.xlsx')">新增模板</el-button>
  <el-button v-if="meta.excel_import&&can('update-template-get')&&can('patch')" @click="download(base+'update_template/',meta.title+'更新模板.xlsx',exportFilters())">更新模板</el-button>
  <el-button v-if="editable&&meta.excel_import&&can('import-data-post')&&(can('add')||can('patch'))" @click="importOpen=true">xlsx 导入</el-button>
  <el-button v-if="can('init-data-get')" @click="download(base+'init_data/',entity+'.json')">初始化数据</el-button>
  <el-popover trigger="click" width="min(500px, calc(100vw - 24px))"><template #reference><el-button>已选 {{selection.length}} 项</el-button></template><el-button @click="clearSelected">清空选择</el-button><el-table :data="selection"><el-table-column :prop="meta.pk" label="主键"/><el-table-column label="名称"><template #default="{row}">{{row.name||row.title||row.label||row.field_name}}</template></el-table-column><el-table-column label="操作"><template #default="{row}"><el-button text @click="deselect(row)">移除</el-button></template></el-table-column></el-table></el-popover><el-button v-if="!props.readonly&&!props.disableDelete&&!['operation_log','login_log'].includes(entity)&&can('multiple-delete-delete')" :disabled="selection.length===0" @click="removeSelected">批量删除</el-button>
  <template v-if="entity==='periodic_task'"><el-button @click="router.push('/system/interval_schedule')">间隔规则</el-button><el-button @click="router.push('/system/crontab_schedule')">Crontab 规则</el-button><el-button @click="router.push('/system/clocked_schedule')">指定时间</el-button><el-button @click="router.push('/system/solar_schedule')">太阳事件</el-button></template>
</div></div><el-alert v-if="context.parent||context.menu" :title="'当前父项：'+contextTitle" type="info" :closable="false"/><el-button v-if="entity==='user'&&context.dept" class="department-toggle" text @click="showDepartmentSummary=!showDepartmentSummary">{{showDepartmentSummary?'隐藏部门概况':'显示部门概况'}}</el-button><div v-if="entity==='user'&&context.dept&&showDepartmentSummary" class="department-summary"><el-switch v-model="includeChildren" active-text="含下级部门" @change="departmentSummary"/><el-button @click="departmentSummary">部门统计</el-button><span v-if="departmentInfo">{{departmentInfo.name}} · {{departmentInfo.count}} 人 · 负责人：{{departmentInfo.owner||'未设置'}} · 男 {{departmentInfo.gender[1]}} / 女 {{departmentInfo.gender[2]}} / 未知 {{departmentInfo.gender[0]}}</span><el-tag v-for="item in departmentInfo?.children" :key="item.id">{{item.name}}：{{item.count}} 人</el-tag><p v-if="departmentInfo?.description">{{departmentInfo.description}}</p><DepartmentCharts v-if="departmentInfo" :info="departmentInfo"/></div><div class="resource-body"><aside v-if="tree.length&&(!mobile||treeOpen)" class="tree-panel"><el-button text @click="allRows">全部</el-button><el-tree v-if="entity!=='area'" :data="tree" :props="{label:entity==='dictionary'?'label':entity==='system_config'?'title':'name'}" :node-key="meta.pk" :draggable="['dept','menu'].includes(entity) && can('batch-update-put')" @node-drop="sortTree" @node-click="filterTree"/><el-tree v-else :key="treeVersion" lazy :load="loadArea" node-key="code" :props="{label:'name',isLeaf:(data:any)=>!data.has_children}" @node-click="filterTree"/></aside><div class="resource-crud" :class="{'with-chart':chartDemo}"><el-tabs v-if="workspaceRow&&['dept','menu'].includes(entity)" v-model="workspaceTab"><el-tab-pane label="基础管理" name="main"/><el-tab-pane v-if="entity==='dept'&&account.can('user:list')" :label="workspaceRow.name+' · 部门用户'" name="users"/><el-tab-pane v-if="entity==='menu'&&account.can('menu_button:list')" label="权限按钮" name="buttons"/><el-tab-pane v-if="entity==='menu'&&account.can('column:list')" label="字段权限" name="fields"/></el-tabs><fs-crud v-show="workspaceTab==='main'" ref="crudRef" v-bind="crudBinding"><template v-if="chartDemo" #header-top><ChartPanel/></template></fs-crud><Resource v-if="workspaceRow&&workspaceTab==='users'" :key="'users-'+workspaceRow.id" entity="user" :context="{dept:workspaceRow.id}" :context-label="workspaceRow.name"/><Resource v-if="workspaceRow&&workspaceTab==='buttons'" :key="'buttons-'+workspaceRow.id" entity="menu_button" :context="{menu:workspaceRow.id}" :context-label="workspaceRow.name"/><Resource v-if="workspaceRow&&workspaceTab==='fields'" :key="'fields-'+workspaceRow.id" entity="column" :context="{menu:workspaceRow.id}" :context-label="workspaceRow.name"/></div></div>
<MessageRecipients v-if="recipientsOpen" v-model="recipientsOpen" :message="recipientMessage"/><el-drawer :model-value="!!jsonDetail" title="JSON 明细" size="min(850px, 100vw)" @close="jsonDetail=undefined"><pre class="json-detail">{{JSON.stringify(jsonDetail,null,2)}}</pre></el-drawer>
<RolePermissions v-if="permissionOpen" v-model="permissionOpen" :role="role" :editable="can('permissions-put')"/>
<el-dialog v-model="buttonEditorOpen" title="生成资源权限按钮" width="min(550px, calc(100vw - 24px))"><el-select v-model="buttonEntity" filterable placeholder="选择实际接口资源"><el-option v-for="item in models" :key="item.entity" :value="item.entity" :label="item.title+' ('+item.entity+')'"/></el-select><template #footer><el-button @click="buttonEditorOpen=false">取消</el-button><el-button type="primary" @click="saveButtons">生成</el-button></template></el-dialog><ExcelImport v-if="importOpen" v-model="importOpen" :base="base" :title="meta.title" :filters="exportFilters()" :create-template="can('import-template-get')&&can('add')" :update-template="can('update-template-get')&&can('patch')" @imported="refresh"/>
<el-drawer v-model="settingsOpen" :title="settings?.title+' · 配置表单'" size="min(700px, 100vw)"><SettingsForm v-if="settingsOpen" :group="settings"/></el-drawer>
<RoleUsers v-if="userGrantOpen" v-model="userGrantOpen" :role="grantRole" :editable="can('users-put')"/>
<el-dialog v-model="passwordOpen" :title="'重置密码 · '+passwordUser?.username" width="min(450px, calc(100vw - 24px))"><el-form ref="passwordRef" :model="passwordForm" label-width="100px"><el-form-item label="新密码" prop="password" :rules="[{required:true,message:'请填写新密码'}]"><el-input v-model="passwordForm.password" type="password" show-password/></el-form-item><el-form-item label="确认密码" prop="password_confirm" :rules="[{required:true,message:'请确认新密码'},{validator:(_rule:any,value:string)=>value===passwordForm.password||new Error('两次密码不匹配')}]"><el-input v-model="passwordForm.password_confirm" type="password" show-password/></el-form-item></el-form><template #footer><el-button type="primary" @click="resetPassword">重置密码</el-button></template></el-dialog>
<el-dialog v-model="matchOpen" title="自动匹配模型字段" width="min(500px, calc(100vw - 24px))"><el-select v-model="model" filterable style="width:100%"><el-option v-for="item in models" :key="item.key" :value="item.key" :label="item.app+' · '+item.title+' ('+item.key+')'"/></el-select><template #footer><el-button type="primary" @click="matchFields">匹配字段</el-button></template></el-dialog><MediaPreview v-model="preview"/>
</div></template>
