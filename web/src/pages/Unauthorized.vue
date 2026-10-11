<script setup lang="ts">
import {useRouter} from 'vue-router'
import {useAccount} from '../store'
import {useI18n} from 'vue-i18n'
const router=useRouter(),account=useAccount(),{t}=useI18n()
function login(){account.logout();router.push('/login')}
</script>
<template><el-result icon="warning" title="401" :sub-title="t('noAccess')"><template #extra><el-button type="primary" @click="router.push('/')">{{t('backHome')}}</el-button><el-button @click="login">{{t('switchAccount')}}</el-button></template></el-result></template>
