<script setup lang="ts">
import {tagColor} from '../tag-color'
defineProps<{color?:string;label?:string}>()
</script>
<template><el-tag v-bind="tagColor(color)"><slot>{{label}}</slot></el-tag></template>
