<script setup lang="ts">
import {ref,computed,watch} from 'vue'
import * as icons from '@element-plus/icons-vue'
import {Icon} from '@iconify/vue'
import MenuIcon from './MenuIcon.vue'
const props=withDefaults(defineProps<{modelValue:string;disabled?:boolean;size?:number;title?:string;clearable?:boolean}>(),{disabled:false,size:20,title:'选择图标',clearable:true})
const emit=defineEmits(['update:modelValue','change']),source=ref('element'),collection=ref('mdi'),search=ref(''),page=ref(1),names=ref<string[]>([])
const filtered=computed(()=>names.value.filter(name=>name.includes(search.value.toLowerCase())))
const visible=computed(()=>filtered.value.slice((page.value-1)*60,page.value*60))
async function load(){const response=await fetch('https://api.iconify.design/collection?prefix='+collection.value);if(!response.ok)throw new Error('图标目录加载失败：'+response.status);const data=await response.json();names.value=[...new Set<string>([...(data.uncategorized||[]),...Object.values(data.categories||{}).flat() as string[]])].sort();page.value=1}
watch([source,collection],async()=>{if(source.value==='iconify')await load()})
watch(search,()=>page.value=1)
function update(value:string){emit('update:modelValue',value);emit('change',value)}
defineExpose({clear:()=>update('')})
</script>
<template><div class="icon-picker"><el-radio-group v-model="source" :disabled="disabled"><el-radio-button value="element">Element Plus</el-radio-button><el-radio-button value="iconify">Iconify</el-radio-button></el-radio-group><el-select :model-value="modelValue" :placeholder="title" :disabled="disabled" filterable allow-create :clearable="clearable" @update:model-value="update"><el-option v-if="source==='element'" v-for="(icon,name) in icons" :key="name" :value="name" :label="name"><el-icon :size="size"><component :is="icon"/></el-icon> {{name}}</el-option><el-option v-else-if="modelValue" :value="modelValue" :label="modelValue"><MenuIcon :name="modelValue"/></el-option></el-select><template v-if="source==='iconify'"><el-select v-model="collection" :disabled="disabled"><el-option label="Material Design Icons" value="mdi"/><el-option label="Tabler" value="tabler"/><el-option label="Font Awesome" value="fa6-solid"/></el-select><el-input v-model="search" placeholder="搜索整套图标" :disabled="disabled" clearable/><div class="icon-grid"><el-button v-for="name in visible" :key="name" :title="name" :disabled="disabled" @click="update(collection+':'+name)"><Icon :icon="collection+':'+name" :width="size"/></el-button></div><el-pagination v-model:current-page="page" :page-size="60" :total="filtered.length" layout="prev,pager,next,total"/></template><el-icon v-if="modelValue" :size="size"><MenuIcon :name="modelValue"/></el-icon><small>可输入图标名、图片 URL 或 data 图片，例如 mdi:warehouse。</small></div></template>
<style scoped>.icon-picker{display:grid;gap:8px;width:100%;min-width:0}.icon-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(42px,1fr));gap:4px}.icon-grid .el-button{margin:0;padding:8px}</style>
