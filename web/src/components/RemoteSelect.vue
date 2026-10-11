<script setup lang="ts">
import {computed,ref,watch} from 'vue'
import {api} from '../api'
const props=withDefaults(defineProps<{modelValue:any;entity:string;pk?:string;label?:string;multiple?:boolean;disabled?:boolean;initialData?:any[];params?:Record<string,any>}>(),{pk:'id',label:'name',multiple:false,disabled:false,initialData:()=>[],params:()=>({})}),emit=defineEmits(['update:modelValue'])
const rows=ref<any[]>([]),labels=ref<any[]>(props.initialData),page=ref(1),total=ref(0),search=ref('')
const values=computed(()=>props.multiple?props.modelValue||[]:props.modelValue===null||props.modelValue===undefined?[]:[props.modelValue])
const options=computed(()=>[...new Map([...labels.value,...rows.value].map(row=>[row[props.pk],row])).values()])
watch(values,async ids=>{labels.value=ids.length?(await api(`/api/system/${props.entity}/`,{params:{...props.params,[props.pk+'__in']:ids.join(','),limit:ids.length}})).data:[]},{immediate:true,deep:true})
async function load(value:string){search.value=value;page.value=1;const result=await api(`/api/system/${props.entity}/`,{params:{...props.params,search:value,page:1}});rows.value=result.data;total.value=result.total}
async function more(){page.value++;const result=await api(`/api/system/${props.entity}/`,{params:{...props.params,search:search.value,page:page.value}});rows.value.push(...result.data);total.value=result.total}
defineExpose({load,clear:()=>emit('update:modelValue',props.multiple?[]:null),data:options})
</script>
<template><el-select :model-value="modelValue" :multiple="multiple" :disabled="disabled" filterable remote clearable :remote-method="load" @visible-change="(value:boolean)=>value&&load('')" @clear="emit('update:modelValue',multiple?[]:null)" @update:model-value="emit('update:modelValue',$event)"><el-option v-for="row in options" :key="row[pk]" :value="row[pk]" :label="String(row[label])"/><template #footer><el-button v-if="rows.length<total" text @click="more">加载更多（{{rows.length}} / {{total}}）</el-button></template></el-select></template>
