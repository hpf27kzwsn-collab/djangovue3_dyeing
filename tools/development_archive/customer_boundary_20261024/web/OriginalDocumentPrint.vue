<script setup lang="ts">
import {ref,onMounted} from 'vue'
import {ElMessage} from 'element-plus'
import {api} from '../../api'
const props=defineProps<{entity:string;row:any;entries:any[]}>(),emit=defineEmits(['saved'])
const entry=ref(props.row.entry_name??''),job=ref<any>(),reason=ref(''),busy=ref(false),history=ref<any[]>([])
const base=`/api/system/${props.entity}/${props.row.id}/`
const text=(v:any)=>v===null?'〈NULL〉':typeof v==='object'?JSON.stringify(v):String(v)
async function loadHistory(){history.value=(await api(base+'phase6_print_history/')).data}
onMounted(loadHistory)
async function prepare(){busy.value=true;try{job.value=(await api(base+'phase6_prepare_print/',{method:'POST',data:{entry:entry.value}})).data;await loadHistory();emit('saved')}finally{busy.value=false}}
function print(){
  const target=window.open('','_blank')
  if(!target){ElMessage.error('浏览器未打开打印窗口，请允许本网站弹出窗口后重试。');return}
  const doc=target.document;doc.title=job.value.title+' · 数据版'
  const style=doc.createElement('style');style.textContent='body{font:12px sans-serif}table{border-collapse:collapse;width:100%;margin:12px 0;break-inside:auto}td,th{border:1px solid #999;padding:5px;white-space:pre-wrap;overflow-wrap:anywhere}tr{break-inside:avoid}h2{break-after:avoid}@page{margin:12mm}';doc.head.appendChild(style)
  const title=doc.createElement('h1');title.textContent=doc.title;doc.body.appendChild(title)
  for(const part of job.value.parts){
    const h=doc.createElement('h2');h.textContent=part.title+' · '+part.rows.length+' 行';doc.body.appendChild(h)
    for(const [index,row] of part.rows.entries()){
      const label=doc.createElement('p');label.textContent='原表 '+part.table+' · 第 '+(index+1)+' 行';doc.body.appendChild(label)
      const table=doc.createElement('table');for(const [n,col] of part.columns.entries()){const tr=table.insertRow();tr.insertCell().textContent=col;tr.insertCell().textContent=text(row[n])}doc.body.appendChild(table)
    }
  }
  target.focus();target.print()
}
async function finish(state:string){busy.value=true;try{job.value=(await api(base+'phase6_finish_print/',{method:'POST',data:{job_id:job.value.id,state,reason:reason.value}})).data;await loadHistory();emit('saved')}finally{busy.value=false}}
</script>
<template>
  <el-table :data="history" max-height="220"><el-table-column prop="prepared_at" label="准备时间"/><el-table-column prop="entry" label="入口"/><el-table-column prop="state" label="状态"/><el-table-column label="操作"><template #default="{row}"><el-button text @click="job=row;entry=row.entry;reason=''">{{row.state==='prepared'?'继续本次打印':'查看记录'}}</el-button></template></el-table-column></el-table>
  <el-form label-width="130px"><el-form-item label="本次打印入口"><el-select v-model="entry" filterable :disabled="!!job"><el-option v-for="e in entries" :key="e.value" :label="e.label+' · '+e.value" :value="e.value"/></el-select></el-form-item></el-form>
  <p>数据版按原字段逐行打印，包含关联明细和重复记录。原客户端版式另在“旧业务入口”保留。</p>
  <el-button v-if="!job" type="primary" :disabled="!entry" :loading="busy" @click="prepare">准备本次打印</el-button>
  <template v-if="job">
    <p>本次状态：{{job.state}}。准备时按原入口执行打印前联动；取消不会擅自撤回旧规则已经增加的打印次数。</p>
    <el-button v-if="job.state==='prepared'" @click="print">打开数据版打印窗口</el-button>
    <el-button @click="job=undefined;reason=''">另开一次打印</el-button>
    <el-input v-if="job.state==='prepared'" v-model="reason" placeholder="填写本次打印结果说明"/>
    <div v-if="job.state==='prepared'" class="result"><el-button :disabled="!reason" :loading="busy" @click="finish('operator_confirmed')">人工确认已打印</el-button><el-button :disabled="!reason" :loading="busy" @click="finish('cancelled')">记录取消</el-button><el-button :disabled="!reason" :loading="busy" @click="finish('failed')">记录失败</el-button></div>
    <p>人工确认单独留档，不表示已收到打印机回执。</p>
  </template>
</template>
<style scoped>.result{margin-top:12px}</style>
