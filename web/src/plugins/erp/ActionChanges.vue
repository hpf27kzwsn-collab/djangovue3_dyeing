<script setup lang="ts">
import {ref,watch} from 'vue'
import FieldInput from '../../components/FieldInput.vue'
const props=defineProps<{modelValue:any;field:any}>()
const emit=defineEmits(['update:modelValue'])
const enabled=ref<string[]>([]),values=ref<Record<string,any>>({})
watch(()=>props.field,()=>{enabled.value=[];values.value={};emit('update:modelValue',{})},{immediate:true})
function publish(){emit('update:modelValue',Object.fromEntries(enabled.value.map(key=>[key,values.value[key]??null])))}
function update(key:string,value:any){values.value[key]=value;publish()}
</script>
<template><div class="correction-input"><p>勾选本次更正项；已勾选项留空表示明确清空原值。</p>
  <div v-for="column in field.columns" :key="column.key"><el-checkbox-group v-model="enabled" @change="publish"><el-checkbox :value="column.key">更正{{column.title}}</el-checkbox></el-checkbox-group>
    <FieldInput v-if="enabled.includes(column.key)" :model-value="values[column.key]" :field="column" @update:model-value="value=>update(column.key,value)"/>
  </div>
</div></template>
<style scoped>.correction-input{width:100%}.correction-input>div{margin-bottom:12px}.correction-input>p{color:var(--el-text-color-secondary)}</style>
