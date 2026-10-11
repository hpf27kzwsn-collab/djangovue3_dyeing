<script setup lang="ts">
import {ref,onMounted} from 'vue'
import {api} from '../api'
const props=defineProps<{modelValue:boolean;message:any}>(),emit=defineEmits(['update:modelValue'])
const rows=ref<any[]>([]),page=ref(1),total=ref(0)
async function load(){const result=await api(`/api/system/message_center/${props.message.id}/recipients/`,{params:{page:page.value}});rows.value=result.data;total.value=result.total}
onMounted(load)
</script>
<template><el-drawer :model-value="modelValue" :title="message.title+' · 实际接收者'" size="min(750px, 100vw)" @update:model-value="emit('update:modelValue',$event)"><el-table :data="rows"><el-table-column label="姓名" min-width="140"><template #default="{row}">{{row.user.name||row.user.username}}</template></el-table-column><el-table-column label="账号" min-width="140"><template #default="{row}">{{row.user.username}}</template></el-table-column><el-table-column label="部门路径" min-width="180"><template #default="{row}">{{row.user.dept_path}}</template></el-table-column><el-table-column label="状态" width="90"><template #default="{row}"><el-tag :type="row.is_read?'success':'info'">{{row.is_read?'已读':'未读'}}</el-tag></template></el-table-column></el-table><el-pagination v-model:current-page="page" :page-size="10" :total="total" layout="prev,pager,next,total" @current-change="load"/></el-drawer></template>
