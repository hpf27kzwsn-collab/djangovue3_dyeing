<script setup lang="ts">
import {computed,ref,watch} from 'vue'
import {compute} from '@fast-crud/fast-crud'
import {ElMessage} from 'element-plus'
import {api} from '../../api'
import {useAccount} from '../../store'
import ResourceTable from '../../components/ResourceTable.vue'
const props=defineProps<{entity:string;context?:Record<string,any>;contextLabel?:string;readonly?:boolean}>()
const account=useAccount(),meta=ref<any>(),table=ref(),selected=ref<any>(),open=ref(false),activeTab=ref('')
type Child={entity:string;title:string;key:string;kinds?:string[]}
const children:Record<string,Child[]>={
  erp_base_party:[{entity:'erp_base_partyrole',title:'业务角色',key:'party'},{entity:'erp_base_partycontact',title:'联系人',key:'party'},{entity:'erp_base_partyaddress',title:'地址',key:'party'}],
  erp_base_material:[{entity:'erp_base_yarnspecification',title:'纱线/织物规格',key:'material',kinds:['yarn','fabric']},{entity:'erp_base_chemicalspecification',title:'染化料资料',key:'material',kinds:['chemical']},{entity:'erp_base_customermaterial',title:'客户物料对照',key:'material'}],
  erp_base_warehouse:[{entity:'erp_base_storagelocation',title:'库区与库位',key:'warehouse'}],
  erp_base_machine:[{entity:'erp_base_machineprocess',title:'适用工序',key:'machine'}],
  erp_base_route:[{entity:'erp_base_routeversion',title:'路线版本',key:'route'}],
  erp_base_routeversion:[{entity:'erp_base_routestep',title:'路线节点',key:'route_version'}],
}
const tabs=computed(()=>(children[props.entity]??[]).filter(item=>account.can(item.entity+':list')&&(!item.kinds||item.kinds.includes(selected.value?.kind))))
const selectedTitle=computed(()=>selected.value?.name??(props.entity==='erp_base_routeversion'?`${selected.value?.route_label} · 版本 ${selected.value?.version}`:selected.value?.code))
const actions=computed(()=>{
  const result=[]
  if(children[props.entity])result.push({key:'children',text:props.entity==='erp_base_routeversion'?'节点':'关联资料',permission:props.entity+':detail',show:(row:any)=>(children[props.entity]).some(child=>account.can(child.entity+':list')&&(!child.kinds||child.kinds.includes(row.kind))),click:(row:any)=>{selected.value=row;activeTab.value=tabs.value[0].entity;open.value=true}})
  if(props.entity==='erp_base_routeversion')for(const [key,text,states] of [['approve','审核',['draft']],['activate','启用',['approved']],['retire','停用',['approved','active']],['clone','复制新版本',['draft','approved','active','retired']]] as const)result.push({key,text,permission:props.entity+':'+key+'-post',show:(row:any)=>(states as readonly string[]).includes(row.status),click:async(row:any)=>{await api(`/api/system/${props.entity}/${row.id}/${key}/`,{method:'POST',data:{}});ElMessage.success(key==='clone'?'已复制为新草稿版本':'版本状态已更新');await table.value.refresh()}})
  return result
})
watch(()=>[props.entity,account.menus,account.buttons],async()=>{
  const data=(await api('/api/meta/'+props.entity+'/')).data
  for(const field of data.fields){
    if(props.context&&field.key in props.context)field.form={...field.form,component:{name:'FieldInput',vModel:'modelValue',field:{...field},disabled:true}}
    if(['pattern_file','template_file'].includes(field.key))field.kind='attachment-id'
    if(props.context?.party&&field.key==='contact')field.remote.params={party:props.context.party}
    if(props.context?.warehouse&&field.key==='parent')field.remote.params={warehouse:props.context.warehouse,kind:'zone'}
    if(props.context?.route_version&&field.key==='predecessor')field.remote.params={route_version:props.context.route_version}
  }
  if(props.entity==='erp_base_routeversion')data.crud_options={rowHandle:{width:560,buttons:{edit:{show:compute(({row}:any)=>row.status==='draft'&&account.can(props.entity+':patch'))},remove:{show:compute(({row}:any)=>row.status==='draft'&&account.can(props.entity+':delete'))},copy:{show:false}}}}
  meta.value=data
},{immediate:true})
</script>
<template>
  <div class="foundation-pane"><el-alert v-if="contextLabel" :title="contextLabel" type="info" :closable="false"/>
    <el-alert v-if="readonly" title="此路线版本已冻结。查看节点后，可回到版本列表复制为新草稿。" type="info" :closable="false"/>
    <ResourceTable v-if="meta" ref="table" :key="entity" :meta="meta" :context="context" :context-label="contextLabel" :readonly="readonly" :row-actions="actions"/><el-skeleton v-else animated/>
    <el-drawer v-model="open" :title="selectedTitle+' · 关联资料'" size="min(1300px, 96vw)" destroy-on-close>
      <el-tabs v-if="open" v-model="activeTab"><el-tab-pane v-for="child in tabs" :key="child.entity" :name="child.entity" :label="child.title">
        <FoundationPane v-if="activeTab===child.entity" :key="child.entity+'-'+selected.id" :entity="child.entity" :context="{[child.key]:selected.id}" :context-label="selectedTitle" :readonly="entity==='erp_base_routeversion'&&selected.status!=='draft'"/>
      </el-tab-pane></el-tabs>
    </el-drawer>
  </div>
</template>
<style scoped>.foundation-pane{height:100%;display:flex;flex-direction:column;gap:12px}.foundation-pane>.page{flex:1;min-height:0}.el-tabs{height:100%}</style>
