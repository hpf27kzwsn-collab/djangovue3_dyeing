<script setup lang="ts">
import {computed} from 'vue'
import FieldInput from '../../components/FieldInput.vue'
const props=defineProps<{modelValue:any[];field:any}>()
const emit=defineEmits(['update:modelValue'])
const rows=computed(()=>props.modelValue??[])
function add(){emit('update:modelValue',[...rows.value,Object.fromEntries(props.field.columns.map((c:any)=>[c.key,null]))])}
function remove(index:number){emit('update:modelValue',rows.value.filter((_,i)=>i!==index))}
function update(index:number,key:string,value:any){emit('update:modelValue',rows.value.map((row,i)=>i===index?{...row,[key]:value}:row))}
</script>
<template>
  <div class="editable-action-rows">
    <el-button @click="add">添加明细</el-button>
    <div v-for="(row,index) in rows" :key="index" class="action-row">
      <div class="row-title">第 {{index+1}} 行 <el-button text type="danger" @click="remove(index)">移除此行</el-button></div>
      <el-form-item v-for="column in field.columns" :key="column.key" :label="column.title" :prop="`${field.key}.${index}.${column.key}`">
        <FieldInput :model-value="row[column.key]" :field="column" @update:model-value="value=>update(index,column.key,value)"/>
      </el-form-item>
    </div>
  </div>
</template>
<style scoped>.editable-action-rows{width:100%}.action-row{border:1px solid var(--el-border-color);padding:12px;margin-top:12px}.row-title{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}</style>
