<script setup lang="ts">import {useRoute} from 'vue-router';const route=useRoute()</script>
<template><article class="terms-page"><h1>{{ route.params.type==='privacy' ? '隐私政策' : '服务条款' }}</h1><p>此平台用于本地组织管理。账号资料、业务附件和操作记录保存在运行平台的设备中。</p><p>账号权限由平台管理员配置。请按组织规定使用平台和管理数据。</p><router-link to="/login">返回登录</router-link></article></template>
