<script setup lang="ts">
import {ref,onMounted} from 'vue'
import {api} from '../api'
defineProps<{modelValue:string}>()
const emit=defineEmits(['update:modelValue']),paths=ref<string[]>([])
onMounted(async()=>{const schema:any=await api('/api/schema/',{headers:{Accept:'application/json'}});paths.value=Object.keys(schema.paths)})
</script>
<template><el-select :model-value="modelValue" filterable allow-create default-first-option @update:model-value="emit('update:modelValue',$event)"><el-option v-for="path in paths" :key="path" :value="path" :label="path"/></el-select></template>
