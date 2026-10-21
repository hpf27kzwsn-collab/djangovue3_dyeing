<script setup lang="ts">
import {computed,ref,watch} from 'vue'
import {useRoute,useRouter} from 'vue-router'
import {api} from '../../api'
import {useAccount} from '../../store'
import BusinessPane from './BusinessPane.vue'
const route=useRoute(),router=useRouter(),account=useAccount(),ownPath=route.path
const menu=computed(()=>account.menus.find(item=>item.web_path===ownPath)),definition=ref<any>()
watch(menu,async(item)=>{if(item)definition.value=(await api(`/api/system/${item.resource}/foundation_entry/`,{params:{key:item.component_name}})).data},{immediate:true})
const context=computed(()=>({_foundation:definition.value.key,...(definition.value.entry?{_entry:definition.value.entry}:{})}))
</script>
<template>
  <div v-if="definition" class="foundation-entry">
    <div v-if="!definition.canonical" class="entry-heading"><el-button link type="primary" @click="router.push(definition.raw_path)">资料汇总</el-button></div>
    <BusinessPane :key="definition.key" :entity="definition.entity" :context="context" :foundation="definition"/>
  </div><el-skeleton v-else animated/>
</template>
<style scoped>.foundation-entry{height:100%;display:flex;flex-direction:column;gap:10px}.entry-heading{display:flex;align-items:center;gap:16px}.entry-heading h2{margin:0;font-size:18px}.foundation-entry>.business-pane{flex:1;min-height:0}</style>
