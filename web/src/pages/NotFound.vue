<script setup lang="ts">import {useI18n} from 'vue-i18n';const {t}=useI18n()</script>
<template><el-result icon="warning" title="404" :sub-title="t('notFound')"><template #extra><router-link to="/"><el-button type="primary">{{t('backHome')}}</el-button></router-link></template></el-result></template>
