<script setup lang="ts">
const props=defineProps<{modelValue:any[]}>(),emit=defineEmits(['update:modelValue'])
function update(index:number,key:string,value:any){emit('update:modelValue',props.modelValue.map((row,i)=>i===index?{...row,[key]:value}:row))}
function add(){emit('update:modelValue',[...(props.modelValue||[]),{title:'',key:'',value:''}])}
function remove(index:number){emit('update:modelValue',props.modelValue.filter((_,i)=>i!==index))}
</script>
<template><div class="array-input"><el-form :model="modelValue||[]"><el-table :data="modelValue||[]"><el-table-column v-for="[key,title] in [['title','标题'],['key','键名'],['value','键值']]" :key="key" :label="title"><template #default="{row,$index}"><el-form-item :prop="$index+'.'+key" :rules="[{validator:(_rule:any,value:any)=>value==null||value===''?new Error('请填写'+title):true,trigger:['change','blur']}]"><el-input :model-value="row[key]" @update:model-value="update($index,key,$event)"/></el-form-item></template></el-table-column><el-table-column label="操作" width="80"><template #default="{$index}"><el-button text @click="remove($index)">移除</el-button></template></el-table-column></el-table></el-form><el-button @click="add">添加一行</el-button></div></template>
<style scoped>.array-input{width:100%}.array-input>.el-button{margin-top:8px}</style>
