<script setup lang="ts">
import {computed,ref,onMounted} from 'vue'
import {useRoute} from 'vue-router'
import {api,download} from '../../api'
import {useAccount} from '../../store'
const route=useRoute(),account=useAccount(),report=String(route.path.split('/').at(-1))
const rows=ref<any[]>([]),columns=ref<any[]>([]),title=ref('业务查询'),count=ref(0),loading=ref(false),page=ref(1)
const dates=ref<string[]>([]),barcode=ref('')
const params=computed(()=>({page:page.value,page_size:50,...(dates.value.length?{start:dates.value[0],end:dates.value[1]}:{}),...(barcode.value?{barcode:barcode.value}:{})}))
async function load(){loading.value=true;try{const result=(await api(`/api/plugins/erp/reports/${report}/`,{params:params.value})).data;rows.value=result.rows;columns.value=result.columns;title.value=result.title;count.value=result.count}finally{loading.value=false}}
function query(){page.value=1;load()}
onMounted(load)
</script>
<template>
  <div class="erp-reports">
    <h2>{{title}}</h2>
    <el-alert title="按当前来源查询权限汇总。不同物料、货权及计量维度分别展示；计划、实测、出入库及交付量分别核对。" type="info" :closable="false"/>
    <div class="filters">
      <el-date-picker v-if="report!=='stock'" v-model="dates" type="datetimerange" start-placeholder="开始时间（含）" end-placeholder="截止时间（不含）" value-format="YYYY-MM-DDTHH:mm:ssZ"/>
      <el-input v-if="report==='packages'" v-model="barcode" placeholder="包装条码" clearable style="width:240px" @keyup.enter="query"/>
      <el-button type="primary" @click="query">查询</el-button>
      <el-button v-if="account.can('erp_report_'+report+':export-get')" @click="download(`/api/plugins/erp/reports/${report}/export/`,title+'.csv',params)">导出全部查询结果</el-button>
    </div>
    <el-table :data="rows" v-loading="loading" border>
      <el-table-column v-for="column in columns" :key="column.key" :prop="column.key" :label="column.title" min-width="140">
        <template #default="{row}">{{row[column.key]===null?'未记录':typeof row[column.key]==='boolean'?(row[column.key]?'是':'否'):row[column.key]}}</template>
      </el-table-column>
    </el-table>
    <el-pagination v-model:current-page="page" :page-size="50" :total="count" layout="prev,pager,next,total" @current-change="load"/>
  </div>
</template>
<style scoped>.erp-reports{padding:16px}.filters{display:flex;gap:12px;margin:16px 0;align-items:center;flex-wrap:wrap}.el-pagination{margin-top:16px}</style>
