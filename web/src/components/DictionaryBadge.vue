<script setup lang="ts">
import {computed} from 'vue'
import ColoredTag from './ColoredTag.vue'
const props=defineProps<{modelValue:any;options:any[]}>()
const option=computed(()=>props.options.find(item=>item.value===props.modelValue))
</script>
<template><ColoredTag v-if="option" :color="option.color" :label="option.label"/><span v-else>{{modelValue}}</span></template>
