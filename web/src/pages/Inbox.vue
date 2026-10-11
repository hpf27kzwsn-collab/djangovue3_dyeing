<script setup lang="ts">
import {ref,onMounted,watch} from 'vue'
import {useRoute} from 'vue-router'
import {api} from '../api'
import {useAccount} from '../store'
const account=useAccount(),messages=ref<any[]>([]),unread=ref(0),page=ref(1),total=ref(0),search=ref(''),readState=ref('')
const route=useRoute(),detail=ref<any>()
async function load(){const data=(await api('/api/inbox/',{params:{page:page.value,search:search.value,read:readState.value}})).data;messages.value=data.messages;unread.value=data.unread;total.value=data.total}
async function read(ids:number[]){await api('/api/inbox/',{method:'POST',data:{ids}});await load()}
async function show(message:any){detail.value=message;if(!message.is_read){await read([message.id]);detail.value.is_read=true}}
async function routeDetail(){if(route.query.id){const data=(await api('/api/inbox/',{params:{id:route.query.id}})).data;await show(data.messages[0])}}
onMounted(async()=>{await load();await routeDetail()})
watch(()=>route.query.id,routeDetail)
</script>
<template><div class="page"><div class="page-heading"><h2>我的接收 <el-tag>{{unread}} 条未读</el-tag></h2><div class="toolbar"><el-button v-if="account.can('message_center:list')" @click="$router.push('/system/message_center?creator='+account.user.id)">我的发布</el-button><el-button @click="read(messages.map(x=>x.id))">本页标为已读</el-button></div></div><div class="toolbar"><el-input v-model="search" placeholder="消息标题" clearable @keyup.enter="page=1;load()"/><el-select v-model="readState" @change="page=1;load()"><el-option label="全部状态" value=""/><el-option label="已读" value="true"/><el-option label="未读" value="false"/></el-select><el-button @click="page=1;load()">查询</el-button></div><el-empty v-if="!messages.length" description="暂无消息"/><el-card v-for="message in messages" :key="message.id"><template #header><div class="page-heading"><el-link @click="show(message)">{{message.title}}</el-link><el-tag v-if="!message.is_read" size="small">未读</el-tag><el-button @click="show(message)">查看详情</el-button></div></template><small class="muted">发布人：{{message.sender}} · {{message.time}}</small></el-card><el-pagination v-model:current-page="page" :page-size="10" :total="total" layout="prev,pager,next,total" @current-change="load"/><el-drawer :model-value="!!detail" :title="detail?.title" size="min(800px, 100vw)" @close="detail=undefined"><template v-if="detail"><p>{{detail.sender}} · {{detail.time}}</p><div class="message-content" v-html="detail.content"/></template></el-drawer></div></template>
<style scoped>.message-content{overflow-wrap:anywhere;overflow:auto}.message-content :deep(img){max-width:100%;height:auto}.el-card{margin-top:12px}</style>
