<script setup lang="ts">
import {computed,ref,watch} from 'vue'
import {useRoute} from 'vue-router'
import {useAccount} from '../../store'
import {api} from '../../api'
import ResourceTable from '../../components/ResourceTable.vue'
import BusinessPane from './BusinessPane.vue'
const route=useRoute(),account=useAccount(),ownPath=route.path
const entity=computed(()=>account.menus.find(menu=>menu.web_path===ownPath)?.resource)
const meta=ref<any>(),open=ref(false),current=ref<any>(),raw=ref<any>(),comparison=ref<any>(),page=ref(1)
const special=computed(()=>entity.value==='erp_base_legacysourcetable'||entity.value==='erp_base_legacyobjectmap')
async function loadRows(){raw.value=(await api(`/api/system/erp_base_legacysourcetable/${current.value.id}/rows/`,{params:{page:page.value,limit:50}})).data}
const actions=computed(()=>entity.value==='erp_base_legacysourcetable'?[{key:'rows',text:'完整原始业务数据',permission:entity.value+':rows-get',click:async(row:any)=>{current.value=row;page.value=1;comparison.value=null;await loadRows();open.value=true}}]:[
  {key:'compare',text:'逐字段旧新对照',permission:entity.value+':compare-get',click:async(row:any)=>{raw.value=null;comparison.value=(await api(`/api/system/erp_base_legacyobjectmap/${row.id}/compare/`)).data;open.value=true}}])
watch(entity,async value=>{if(value&&special.value)meta.value=(await api('/api/meta/'+value+'/')).data},{immediate:true})
</script>
<template>
  <el-alert title="完整历史来源单独保留。归档资料与已确认导入记录分别展示，原有空值、重复行及未核实关系保留在来源及核对事项中。" type="info" :closable="false"/>
  <ResourceTable v-if="special&&meta" :meta="meta" readonly :row-actions="actions"/>
  <BusinessPane v-else-if="entity" :entity="entity" readonly/>
  <el-dialog v-model="open" title="旧资料与字段对照" width="95%">
    <template v-if="raw">
      <el-alert :title="raw.table+'；原主键：'+(raw.primary_key.length?raw.primary_key.join('、'):'没有主键，保留提取行号及全部重复行')" type="info" :closable="false"/>
      <el-table :data="raw.rows" border max-height="620">
        <el-table-column prop="row" label="提取行号" width="110"/>
        <el-table-column v-for="column in raw.columns" :key="column.field_name" :label="column.field_name" min-width="170">
          <template #default="{row}">{{row.values[column.field_name]===null?'NULL':row.values[column.field_name]}}</template>
        </el-table-column>
      </el-table>
      <el-pagination v-model:current-page="page" :page-size="50" :total="raw.count" layout="prev,pager,next,total" @current-change="loadRows"/>
    </template>
    <template v-if="comparison">
      <el-alert :title="'原完整主键：'+JSON.stringify(comparison.old_key)" type="info" :closable="false"/>
      <el-table :data="comparison.rows" border>
        <el-table-column prop="title" label="新字段"/><el-table-column prop="old_field" label="原字段"/>
        <el-table-column prop="old_value" label="完整原值"/><el-table-column prop="new_value" label="当前新值"/>
        <el-table-column label="核对"><template #default="{row}">{{row.matches?'一致':'存在差异'}}</template></el-table-column>
      </el-table>
    </template>
  </el-dialog>
</template>
