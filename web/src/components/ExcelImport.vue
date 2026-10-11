<script setup lang="ts">
import {ref} from 'vue'
import type {UploadFile,UploadUserFile} from 'element-plus'
import {api,download} from '../api'
const props=defineProps<{modelValue:boolean;base:string;title:string;filters:any;createTemplate:boolean;updateTemplate:boolean}>()
const emit=defineEmits(['update:modelValue','imported'])
const files=ref<UploadUserFile[]>([]),busy=ref(false),result=ref<any>(),problem=ref('')
function choose(file:UploadFile){files.value=[file];result.value=undefined;problem.value=''}
async function submit(){
  busy.value=true;problem.value='';result.value=undefined
  try{
    const data=new FormData();data.append('file',files.value[0].raw!)
    result.value=(await api(props.base+'import/',{method:'POST',data})).data
    files.value=[];emit('imported')
  }catch(error:any){
    const detail=error.response?.data?.data
    problem.value=detail?.sheet?`${detail.sheet}，第 ${detail.row} 行，${detail.field}：${typeof detail.detail==='string'?detail.detail:JSON.stringify(detail.detail)}`:error.response?.data?.msg||error.message
  }finally{busy.value=false}
}
</script>
<template>
<el-dialog :model-value="modelValue" :title="title+' · xlsx 导入'" width="min(640px, calc(100vw - 24px))" @update:model-value="(value:boolean)=>emit('update:modelValue',value)">
  <div class="template-actions">
    <el-button v-if="createTemplate" @click="download(base+'import_template/',title+'新增模板.xlsx')">下载新增模板</el-button>
    <el-button v-if="updateTemplate" @click="download(base+'update_template/',title+'更新模板.xlsx',filters)">下载批量更新模板</el-button>
  </div>
  <p>仅使用 xlsx。填写中文列后上传；含更新主键的模板用于更新，空单元格保持原值。</p>
  <el-upload v-model:file-list="files" drag accept=".xlsx" :auto-upload="false" :disabled="busy" :on-change="choose">
    <div>点击选择 xlsx 文件，或将文件拖到这里</div>
    <template #tip><div class="el-upload__tip">手机可使用系统文件选择器。字段说明、关系选项和日期格式见模板中的“填写说明”。</div></template>
  </el-upload>
  <el-alert v-if="problem" type="error" :title="problem" :closable="false" show-icon/>
  <el-alert v-if="result" type="success" :title="`导入完成：新增 ${result.created} 条，更新 ${result.updated} 条，跳过空白 ${result.skipped} 行`" :closable="false" show-icon/>
  <template #footer><div class="import-footer"><el-button :disabled="busy" @click="emit('update:modelValue',false)">关闭</el-button><el-button type="primary" :loading="busy" :disabled="!files.length" @click="submit">提交导入</el-button></div></template>
</el-dialog>
</template>
<style scoped>
.template-actions{display:flex;gap:12px;flex-wrap:wrap}.template-actions .el-button+.el-button{margin-left:0}.el-alert{margin-top:16px;overflow-wrap:anywhere}.import-footer{display:flex;justify-content:flex-end;gap:12px}.import-footer .el-button+.el-button{margin-left:0}
@media(max-width:600px){.template-actions{display:grid;grid-template-columns:1fr}.import-footer{display:grid;grid-template-columns:1fr 1fr}.import-footer .el-button{width:100%}}
</style>
