<script setup lang="ts">
import {defineAsyncComponent} from 'vue'
const Resource=defineAsyncComponent(()=>import('./Resource.vue'))
</script>
<template><Resource entity="login_log" chart-demo/></template>
