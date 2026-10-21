<script setup lang="ts">
import {ref} from 'vue'
import type {UploadFile,UploadUserFile} from 'element-plus'
import {api,download} from '../api'
const props=defineProps<{modelValue:boolean;base:string;title:string;filters:any;createTemplate:boolean;updateTemplate:boolean;entries?:Array<{value:string;label:string}>;entry?:string}>()
const emit=defineEmits(['update:modelValue','imported'])
const files=ref<UploadUserFile[]>([]),busy=ref(false),result=ref<any>(),problem=ref('')
const selectedEntry=ref(props.entry??(props.entries?.length===1?props.entries[0].value:''))
const entryParams=()=>({...selectedEntry.value?{_entry:selectedEntry.value}:{},_foundation:props.filters?._foundation})
function choose(file:UploadFile){files.value=[file];result.value=undefined;problem.value=''}
async function submit(){
  busy.value=true;problem.value='';result.value=undefined
  try{
    const data=new FormData();data.append('file',files.value[0].raw!)
    if(selectedEntry.value)data.append('_entry',selectedEntry.value)
    result.value=(await api(props.base+'import/',{method:'POST',params:{_foundation:props.filters?._foundation},data})).data
    files.value=[];emit('imported')
  }catch(error:any){
    const detail=error.response?.data?.data
    problem.value=detail?.sheet?`${detail.sheet}，第 ${detail.row} 行，${detail.field}：${typeof detail.detail==='string'?detail.detail:JSON.stringify(detail.detail)}`:error.response?.data?.msg||error.message
  }finally{busy.value=false}
}
</script>
<template>
<el-dialog :model-value="modelValue" :title="title+' · xlsx 导入'" width="min(640px, calc(100vw - 24px))" @update:model-value="(value:boolean)=>emit('update:modelValue',value)">
  <el-form v-if="entries?.length" label-width="100px"><el-form-item label="业务入口"><el-select v-model="selectedEntry" clearable filterable placeholder="选择本批业务类型，也可在表格中逐行填写"><el-option v-for="item in entries" :key="item.value" :value="item.value" :label="item.label"/></el-select></el-form-item></el-form>
  <div class="template-actions">
    <el-button v-if="createTemplate" @click="download(base+'import_template/',title+'新增模板.xlsx',entryParams())">下载新增模板</el-button>
    <el-button v-if="updateTemplate" @click="download(base+'update_template/',title+'更新模板.xlsx',{...filters,...entryParams()})">下载批量更新模板</el-button>
  </div>
  <p>空白或 #KEEP：新增采用默认值，更新保留原值。#NULL：设为空值；#EMPTY：清空文本或多选。0、负数和空格文本照常提交。</p>
  <p v-if="entries?.length">新增单据按业务入口生成编号并执行保存联动。表格逐行入口优先，其次模板保存的入口，最后使用这里的选择；已有单据保留原入口。</p>
  <p>资料包中的历史文件按“导入设置”承接原值和原主键；日常新增使用空白模板。历史文件的 #UTF8: 特殊文本会在导入时还原。</p>
  <p>已设置编号规则的资料：编号空白时按规则生成；填写编号须符合手工录入权限。历史原值承接保留原编号，不消耗新号，导入成功后同步流水上限。</p>
  <p>含“更新主键”的模板用于更新。标记本身作为文本时加 #TEXT: 前缀，例如 #TEXT:#NULL。重复数据逐行处理，一行失败则整批不保存。</p>
  <el-upload v-model:file-list="files" drag accept=".xlsx" :auto-upload="false" :disabled="busy" :on-change="choose">
    <div>点击选择 xlsx 文件，或将文件拖到这里</div>
    <template #tip><div class="el-upload__tip">手机可使用系统文件选择器。字段说明、关系选项和日期格式见模板中的“填写说明”。</div></template>
  </el-upload>
  <el-alert v-if="problem" type="error" :title="problem" :closable="false" show-icon/>
  <el-alert v-if="result" type="success" :title="`导入完成：新增 ${result.created} 条，更新 ${result.updated} 条，跳过空白 ${result.skipped} 行`" :closable="false" show-icon/>
  <el-table v-if="result" :data="result.rows" max-height="240"><el-table-column prop="row" label="Excel行"/><el-table-column label="结果"><template #default="{row}">{{row.status==='created'?'已新增':row.status==='updated'?'已更新':'空白行'}}</template></el-table-column><el-table-column prop="id" label="记录ID"/></el-table>
  <template #footer><div class="import-footer"><el-button :disabled="busy" @click="emit('update:modelValue',false)">关闭</el-button><el-button type="primary" :loading="busy" :disabled="!files.length" @click="submit">提交导入</el-button></div></template>
</el-dialog>
</template>
<style scoped>
.template-actions{display:flex;gap:12px;flex-wrap:wrap}.template-actions .el-button+.el-button{margin-left:0}.el-alert{margin-top:16px;overflow-wrap:anywhere}.import-footer{display:flex;justify-content:flex-end;gap:12px}.import-footer .el-button+.el-button{margin-left:0}
@media(max-width:600px){.template-actions{display:grid;grid-template-columns:1fr}.import-footer{display:grid;grid-template-columns:1fr 1fr}.import-footer .el-button{width:100%}}
</style>
