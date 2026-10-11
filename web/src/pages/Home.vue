<script setup lang="ts">
import { useAccount } from '../store'
import {useRouter} from 'vue-router'
import {navigateMenu,menuLink} from '../navigation'
const router=useRouter()
const account=useAccount()
</script>
<template><div class="page"><div class="welcome"><p class="eyebrow">WORKSPACE</p><h1>你好，{{ account.user.name || account.user.username }}</h1><p>从这里开始管理组织和系统。</p></div><div class="home-cards"><el-card><div class="metric">{{ account.menus.filter(x=>!x.is_catalog && x.visible).length }}</div><span>可访问功能</span></el-card><el-card><div class="metric">{{ account.buttons.length }}</div><span>授权操作</span></el-card><el-card><div class="metric">{{ account.user.role.length }}</div><span>所属角色</span></el-card></div><el-card header="常用入口"><div class="shortcut-grid"><a v-for="menu in account.menus.filter(x=>!x.is_catalog && x.visible)" :key="menu.id" :href="menu.is_link&&!menu.is_iframe?menuLink(menu):menu.web_path" @click.prevent="navigateMenu(menu,router)">{{ menu.name }}<span>→</span></a></div></el-card></div></template>
