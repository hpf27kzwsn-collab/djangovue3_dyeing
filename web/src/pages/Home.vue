<script setup lang="ts">
import {computed} from 'vue'
import {useAccount} from '../store'
import {useRouter} from 'vue-router'
import {navigateMenu} from '../navigation'
import {businessMenus,managementMenus,commonKeys,moduleKeys,descendants,preferredEntries} from '../erp-workspace'
import type {Menu} from '../store'
const router=useRouter(),account=useAccount()
const menus=computed(()=>businessMenus(account.menus))
const common=computed(()=>commonKeys.map(key=>menus.value.find(menu=>menu.component_name===key)).filter((menu):menu is Menu=>Boolean(menu)))
const modules=computed(()=>moduleKeys.map(key=>menus.value.find(menu=>menu.component_name===key)).filter((menu):menu is Menu=>Boolean(menu)))
const descriptions:Record<string,string>={erp_base:'维护组织、人员、往来单位、物料与业务分类',erp_sales:'办理销售订单、加工报价与客户交付',erp_purchase:'办理采购申请、订单、到货与退回',erp_sampling:'办理打样、对色、配方与色卡流转',erp_production:'办理工卡、排程、报工、称料与外协',erp_warehouse:'办理坯料、成品、染化料及机物料收发',erp_quality:'办理检验、异常、返修与质量放行'}
function links(module:Menu){
  const pages=descendants(module,menus.value),preferred=preferredEntries[module.component_name]??[]
  const selected=preferred.map(key=>pages.find(menu=>menu.component_name===key)).filter((menu):menu is Menu=>Boolean(menu))
  return selected.length?selected:pages.slice(0,3)
}
</script>
<template><div class="page business-home">
  <div class="welcome"><h1>染色业务工作台</h1><p>{{account.user.name||account.user.username}}，从基础资料维护开始，按业务模块办理单据。</p></div>
  <el-card v-if="common.length" header="常用基础资料"><div class="shortcut-grid"><a v-for="menu in common" :key="menu.id" :href="menu.web_path" @click.prevent="navigateMenu(menu,router)">{{menu.name}}<span>→</span></a></div></el-card>
  <div class="business-modules"><el-card v-for="module in modules" :key="module.id"><h2>{{module.name}}</h2><p>{{descriptions[module.component_name]}}</p><div class="module-links"><a v-for="menu in links(module)" :key="menu.id" :href="menu.web_path" @click.prevent="navigateMenu(menu,router)">{{menu.name}} →</a></div></el-card></div>
  <el-card v-if="managementMenus(account.menus).length" header="系统管理"><p>维护账号权限、编号规则、系统配置与运行记录。</p><a href="/management" @click.prevent="router.push('/management')">进入系统管理 →</a></el-card>
</div></template>
<style scoped>.business-home{gap:20px}.business-home h1{margin:0 0 12px}.business-home h2{font-size:19px;margin:0 0 12px}.business-home p{color:var(--el-text-color-secondary);line-height:1.6}.business-modules{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}.module-links{display:flex;flex-wrap:wrap;gap:12px}.module-links a{color:var(--el-color-primary);text-decoration:none}</style>
