<script setup lang="ts">
import {computed} from 'vue'
import {useRoute} from 'vue-router'
import {useAccount} from '../store'
import {menuLink} from '../navigation'
const route=useRoute(),account=useAccount(),menu=computed(()=>account.menus.find(row=>row.web_path===route.path)!)
</script>
<template><div class="page"><h2>{{menu.name}}</h2><p>在新窗口打开此页面。</p><a :href="menuLink(menu)" target="_blank"><el-button type="primary">打开页面</el-button></a></div></template>
