<script setup lang="ts">
defineProps<{file:any}>()
const emit=defineEmits(['preview'])
</script>
<template><button class="file-thumbnail" :aria-label="'预览 '+file.name" @click="emit('preview',file)"><img v-if="file.file_type===0" :src="file.url" :alt="file.name"/><span v-else>{{['图片','视频','音频','文件'][file.file_type]}}</span></button></template>
<style scoped>.file-thumbnail{width:72px;height:56px;border:0;border-radius:4px;background:var(--el-fill-color-light);color:var(--el-color-primary);cursor:pointer}.file-thumbnail img{width:100%;height:100%;object-fit:contain}</style>
