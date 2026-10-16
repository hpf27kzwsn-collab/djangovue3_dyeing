<script setup lang="ts">
import FieldInput from '../../components/FieldInput.vue'
const props=defineProps<{modelValue:any[]}>()
const emit=defineEmits(['update:modelValue'])
const columns=[{key:'measure',title:'数量种类',kind:'select',options:[{value:'Rolls',label:'粒数'},{value:'WeightQty',label:'重量'},{value:'LengthQty',label:'长度'}]},
  {key:'unit',title:'库存单位原编码',kind:'number',options:[]},{key:'quantity',title:'确认损耗（允许负数/空值）',kind:'decimal',nullable:true,options:[]},
  {key:'reason',title:'确认依据',kind:'text',options:[]}]
function add(){emit('update:modelValue',[...props.modelValue,{measure:'WeightQty',unit:null,quantity:null,reason:''}])}
function update(index:number,key:string,value:any){emit('update:modelValue',props.modelValue.map((row,i)=>i===index?{...row,[key]:key==='unit'&&value===undefined?null:value}:row))}
function remove(index:number){emit('update:modelValue',props.modelValue.filter((_,i)=>i!==index))}
</script>
<template><div style="width:100%"><el-button @click="add">添加损耗确认</el-button>
  <div v-for="(row,index) in modelValue" :key="index" style="border-bottom:1px solid var(--el-border-color);padding:12px 0">
    <el-form-item v-for="field in columns" :key="field.key" :label="field.title"><FieldInput :field="field" :model-value="row[field.key]" @update:model-value="value=>update(index,field.key,value)"/></el-form-item>
    <el-button @click="remove(index)">移除此项</el-button>
  </div>
</div></template>
