<script setup lang="ts">
import {computed,ref} from 'vue'
import {actionTopics,type BusinessAction} from './action-presentation'
const props=defineProps<{actions:BusinessAction[];collection?:boolean}>()
const emit=defineEmits<{execute:[action:BusinessAction]}>()
const search=ref('')
const groups=computed(()=>actionTopics(props.actions.filter(action=>!search.value||action.display_title.includes(search.value)||action.title.includes(search.value))))
</script>
<template>
  <div class="business-actions">
    <el-input v-if="actions.length>8" v-model="search" clearable placeholder="查找业务操作" aria-label="查找业务操作"/>
    <el-empty v-if="!groups.length" description="当前没有可办理的操作" :image-size="60"/>
    <section v-for="group in groups" :key="group.title">
      <h3>{{group.title}}</h3>
      <div class="action-group"><el-button v-for="action in group.actions" :key="action.key" :data-action="action.key" @click="emit('execute',action)">{{action.display_title}}</el-button></div>
    </section>
  </div>
</template>
<style scoped>
.business-actions{display:flex;flex-direction:column;gap:18px}.action-group{display:flex;flex-wrap:wrap;gap:10px}.action-group .el-button{margin-left:0}h3{font-size:15px;margin:0 0 12px}
</style>
