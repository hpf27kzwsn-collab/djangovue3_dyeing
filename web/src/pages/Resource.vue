<script setup lang="ts">
import {watch,ref} from 'vue'
import {useRoute} from 'vue-router'
import {api} from '../api'
import ResourceTable from '../components/ResourceTable.vue'
import {useAccount} from '../store'
const props=defineProps<{entity?:string;context?:Record<string,any>;contextLabel?:string;chartDemo?:boolean}>()
const route=useRoute(),account=useAccount(), meta=ref<any>()
const ownPath=route.path
watch(()=>[props.entity||(route.path===ownPath?route.params.entity:undefined),account.menus,account.buttons],async([entity],previous)=>{if(entity){if(entity!==previous?.[0])meta.value=undefined;meta.value=(await api('/api/meta/'+entity+'/')).data}},{immediate:true})
</script>
<template><ResourceTable v-if="meta" :meta="meta" :context="context" :context-label="contextLabel" :chart-demo="chartDemo"/><el-skeleton v-else animated/></template>
