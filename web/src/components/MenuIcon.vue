<script setup lang="ts">
import {computed} from 'vue'
import {Icon} from '@iconify/vue'
const props=defineProps<{name:string}>()
const image=computed(()=>/^(https?:\/\/|\/|data:image\/|\.\.?\/)/i.test(props.name))
</script>
<template><img v-if="image" :src="name" alt="" class="menu-image-icon"/><Icon v-else-if="name.includes(':')" :icon="name"/><component v-else :is="name"/></template>
<style scoped>.menu-image-icon{width:1em;height:1em;object-fit:contain;vertical-align:middle}</style>
