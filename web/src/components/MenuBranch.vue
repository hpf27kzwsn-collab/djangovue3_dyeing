<script setup lang="ts">
import type { Menu } from '../store'
import MenuIcon from './MenuIcon.vue'
import {navigateMenu} from '../navigation'
import {useRouter} from 'vue-router'
const router=useRouter()
defineProps<{items: Menu[]; parent: number | null}>()

</script>
<template>
  <template v-for="item in items.filter(x => x.parent_id === parent && x.visible)" :key="item.id">
    <el-sub-menu v-if="item.is_catalog" :index="String(item.id)"><template #title><el-icon v-if="item.icon"><MenuIcon :name="item.icon"/></el-icon>{{ item.name }}</template><MenuBranch :items="items" :parent="item.id"/></el-sub-menu>
    <el-menu-item v-else :index="item.web_path" @click="navigateMenu(item,router)"><el-icon v-if="item.icon"><MenuIcon :name="item.icon"/></el-icon><span>{{ item.name }}</span></el-menu-item>
  </template>
</template>
