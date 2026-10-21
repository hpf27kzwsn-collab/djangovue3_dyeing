<script setup lang="ts">
import {watch,ref} from 'vue'
import {useRoute} from 'vue-router'
import {api} from '../api'
import ResourceTable from '../components/ResourceTable.vue'
import {useAccount} from '../store'
import BusinessPane from '../plugins/erp/BusinessPane.vue'
const props=defineProps<{entity?:string;context?:Record<string,any>;contextLabel?:string;chartDemo?:boolean}>()
const route=useRoute(),account=useAccount(), meta=ref<any>()
const ownPath=route.path
watch(()=>[props.entity||(route.path===ownPath?route.params.entity:undefined),account.menus,account.buttons],async([entity],previous)=>{if(entity){if(entity!==previous?.[0])meta.value=undefined;const data=(await api('/api/meta/'+entity+'/')).data;if(!data.workflow?.source_model)data.title=account.menus.find(menu=>menu.web_path===ownPath&&menu.resource===data.entity)?.name??data.title;meta.value=data}},{immediate:true})
</script>
<template><BusinessPane v-if="meta?.workflow?.source_model" :entity="meta.entity" :context="context" :context-label="contextLabel"/><ResourceTable v-else-if="meta" :meta="meta" :context="context" :context-label="contextLabel" :chart-demo="chartDemo"/><el-skeleton v-else animated/></template>
