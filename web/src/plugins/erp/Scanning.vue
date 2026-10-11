<script setup lang="ts">
import {ref} from 'vue'
import {api} from '../../api'
import BusinessPane from './BusinessPane.vue'
const kind=ref('workcard'),employeeKey=ref('card_identifier'),value=ref(''),matches=ref<any[]>([]),entity=ref(''),selected=ref<any>(),loading=ref(false)
async function identify(){loading.value=true;selected.value=null;try{const result=(await api('/api/plugins/erp/identify/'+kind.value+'/',{params:{key:kind.value==='employee'?employeeKey.value:kind.value==='package'?'barcode':'number',value:value.value}})).data;matches.value=result.matches;entity.value=result.entity}finally{loading.value=false}}
</script>
<template>
  <el-alert title="扫描或录入现有员工卡、工卡号及包装条码，识别后继续对应业务。识别本身不会产生报工、称量、库存或打印成功记录。" type="info" :closable="false"/>
  <div class="scan-input">
    <el-select v-model="kind" style="width:180px" @change="matches=[];selected=null"><el-option label="工卡识别" value="workcard"/><el-option label="包装识别" value="package"/><el-option label="员工识别" value="employee"/></el-select>
    <el-select v-if="kind==='employee'" v-model="employeeKey" style="width:140px"><el-option label="员工卡号" value="card_identifier"/><el-option label="员工代码" value="code"/></el-select>
    <el-input v-model="value" placeholder="扫描或录入完整标识" style="width:330px" @keyup.enter="identify"/><el-button type="primary" :loading="loading" @click="identify">识别</el-button>
  </div>
  <el-table :data="matches" border>
    <el-table-column label="代码或单号"><template #default="{row}">{{row.number??row.code}}</template></el-table-column>
    <el-table-column label="名称或条码"><template #default="{row}">{{row.name??row.barcode}}</template></el-table-column>
    <el-table-column v-if="kind!=='employee'" label="继续办理"><template #default="{row}"><el-button @click="selected=row">查看业务操作</el-button></template></el-table-column>
  </el-table>
  <el-empty v-if="!matches.length&&!loading" description="当前没有匹配资料"/>
  <BusinessPane v-if="selected" :key="entity+selected.id" :entity="entity" :context="{id:selected.id}"/>
</template>
<style scoped>.scan-input{display:flex;gap:12px;margin:16px 0;flex-wrap:wrap}</style>
