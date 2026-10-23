<script setup lang="ts">
import {computed,ref,watch} from 'vue'
import {useRouter} from 'vue-router'
import {useAccount} from '../store'
import {managementMenus,descendants} from '../erp-workspace'
import type {Menu} from '../store'
import maintenanceResources from '../plugins/erp/maintenance-resources.json'
const account=useAccount(),router=useRouter(),search=ref('')
const advanced=ref<string[]>([])
const maintenance=computed(()=>account.superuser?account.menus.filter(menu=>!menu.is_catalog&&menu.component_name===menu.resource&&maintenanceResources.includes(menu.resource)&&menu.name.includes(search.value)):[])
watch(search,value=>advanced.value=value?['data']:[])
const sections=[['system_identity','账号与权限'],['numbering','编号管理'],['system_configuration','系统设置'],['system_records','操作与导入记录'],['system_devices','设备接入设置'],['system_runtime','运行维护'],['system_archives','配置档案']]
const groups=computed(()=>{
  const menus=managementMenus(account.menus).filter(menu=>menu.component_name!=='system_overview'&&menu.name.includes(search.value))
  return sections.map(([key,title])=>{
    const folder=account.menus.find(menu=>menu.component_name===key)
    const ids=new Set(folder?descendants(folder,account.menus).map(menu=>menu.id):[])
    return {key,title,items:menus.filter(menu=>key==='numbering'?menu.component_name==='erp_base_numberingrule':ids.has(menu.id))}
  })
})
function open(menu:Menu){router.push({path:menu.web_path,query:{workspace:'maintenance'}})}
</script>
<template><div class="page management-page"><h1>系统管理</h1><p>管理登录账号、权限、编号规则和系统运行。部门、人员、客户、供应商等业务资料请从对应业务模块维护。</p><el-input v-model="search" placeholder="查找管理功能" clearable/>
  <el-card v-for="group in groups.filter(group=>group.key!=='system_archives'&&group.items.length)" :key="group.key" :header="group.title"><p v-if="group.key==='system_identity'">登录账号与业务员工分别管理；账号归属部门用于权限范围，业务部门仍在基础信息。</p><p v-if="group.key==='system_devices'">维护通讯端口、机台通讯配置与采集点。配置保存后仍需在现场核验实际数据接收。</p><div class="shortcut-grid"><a v-for="menu in group.items" :key="menu.id" :href="menu.web_path+'?workspace=maintenance'" @click.prevent="open(menu)">{{menu.name}}<span>→</span></a></div></el-card>
  <el-collapse v-if="groups[6].items.length" v-model="advanced"><el-collapse-item title="配置档案" name="data"><p>用于查看配置来源与资料对应。业务主档及历史业务资料保留在对应业务模块。</p><div class="shortcut-grid"><a v-for="menu in groups[6].items" :key="menu.id" :href="menu.web_path+'?workspace=maintenance'" @click.prevent="open(menu)">{{menu.name}}<span>→</span></a></div></el-collapse-item></el-collapse>
  <el-collapse v-if="maintenance.length"><el-collapse-item title="业务数据维护" name="business-maintenance"><p>按业务专题进行历史核验、全库重算、来源修复及补同步。正常录入请使用对应业务入口。</p><div class="shortcut-grid"><a v-for="menu in maintenance" :key="menu.id" :href="menu.web_path+'?workspace=maintenance'" @click.prevent="open(menu)">{{menu.name}}<span>→</span></a></div></el-collapse-item></el-collapse>
  <el-empty v-if="!groups.some(group=>group.items.length)&&!maintenance.length" description="当前没有可查看的管理功能"/>
</div></template>
<style scoped>.management-page{gap:18px}.management-page h1{margin:0}.management-page>p{color:var(--el-text-color-secondary)}.management-page>.el-input{max-width:420px}</style>
