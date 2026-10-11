<script setup lang="ts">
import {computed} from 'vue'
import {useRoute} from 'vue-router'
import {useAccount} from '../../store'
import FoundationPane from './FoundationPane.vue'
const route=useRoute(),account=useAccount(),ownPath=route.path
const entity=computed(()=>account.menus.find(menu=>menu.web_path===ownPath)?.resource)
</script>
<template><FoundationPane v-if="entity" :key="entity" :entity="entity"/><el-skeleton v-else animated/></template>
