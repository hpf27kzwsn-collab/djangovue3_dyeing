<script setup lang="ts">
import {computed} from 'vue'
const props=defineProps<{modelValue?:any[]}>()
const emit=defineEmits(['update:modelValue'])
const rows=computed(()=>props.modelValue??[])
function add(){emit('update:modelValue',[...rows.value,{detail_no:null,header_sheet_series:null,sheet_date:null,sheet_kind:null,job_number:null,quantity:null,metres:null,zero_amount:null}])}
function update(index:number,key:string,value:any){emit('update:modelValue',rows.value.map((row,i)=>i===index?{...row,[key]:value}:row))}
function remove(index:number){emit('update:modelValue',rows.value.filter((_,i)=>i!==index))}
const fields=[['detail_no','原明细号'],['header_sheet_series','原匹配表头流水'],['job_number','原工卡号'],['quantity','原重量Qty（公斤）'],['metres','有依据的原长度PreMeter（米）']]
</script>
<template>
  <div class="rework-sources">
    <p>每行对应原表头与明细的一次连接；重复来源按原行保留。未知长度留空，不能由重量推算。未提供数量来源时报告显示未知。</p>
    <div v-for="(row,index) in rows" :key="index" class="source-row">
      <el-form-item v-for="[key,title] in fields" :key="key" :label="title">
        <el-input :model-value="row[key]" clearable @update:model-value="(value:any)=>update(index,key,value===''?null:value)"/>
      </el-form-item>
      <el-form-item label="原表头日期"><el-date-picker :model-value="row.sheet_date" type="datetime" value-format="YYYY-MM-DDTHH:mm:ssZ" @update:model-value="(value:any)=>update(index,'sheet_date',value)"/></el-form-item>
      <el-form-item label="原单据类型"><el-input-number :model-value="row.sheet_kind" :precision="0" @update:model-value="(value:any)=>update(index,'sheet_kind',value??null)"/></el-form-item>
      <el-form-item label="原ARMoney是否等于零"><el-select :model-value="row.zero_amount" clearable @update:model-value="(value:any)=>update(index,'zero_amount',value===''?null:value)"><el-option label="等于零" :value="true"/><el-option label="不等于零" :value="false"/></el-select></el-form-item>
      <el-button @click="remove(index)">移除本次输入行</el-button>
    </div>
    <el-button @click="add">添加数量来源</el-button>
  </div>
</template>
<style scoped>.rework-sources{width:100%}.source-row{border:1px solid var(--el-border-color);padding:12px;margin:8px 0;display:grid;grid-template-columns:1fr 1fr;gap:8px}.source-row .el-form-item{margin:0}</style>
