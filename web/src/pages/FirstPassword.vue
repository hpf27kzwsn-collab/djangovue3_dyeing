<script setup lang="ts">
import {onMounted,reactive,ref} from 'vue'
import {useRouter,useRoute} from 'vue-router'
import {useAccount} from '../store'
import {useI18n} from 'vue-i18n'
import {api} from '../api'
const account=useAccount(),router=useRouter(),route=useRoute(),{t}=useI18n(),form=reactive({new_password:'',new_password_confirm:''})
const formRef=ref()
const rules={new_password:[{required:true,message:'请填写新密码'}],new_password_confirm:[{required:true,message:'请确认新密码'},{validator:(_rule:any,value:string)=>value===form.new_password||new Error('两次密码不匹配')}]}
onMounted(()=>account.load())
async function save(){if(!await formRef.value.validate(()=>{}))return;await api('/api/password/first/',{method:'POST',data:form});await account.load();router.push(String(route.query.redirect||'/'))}
function logout(){account.logout();router.push('/login')}
</script>
<template><div class="login-page"><div class="login-intro"><h1>{{t('firstPassword')}}</h1><p>{{t('firstPasswordHint')}}</p></div><div class="login-card"><h2>{{account.user.name||account.user.username}}</h2><el-form ref="formRef" :model="form" :rules="rules" @submit.prevent="save"><el-form-item prop="new_password" :label="t('newPassword')"><el-input v-model="form.new_password" type="password" show-password/></el-form-item><el-form-item prop="new_password_confirm" :label="t('confirmPassword')"><el-input v-model="form.new_password_confirm" type="password" show-password/></el-form-item><el-button type="primary" native-type="submit">{{t('save')}}</el-button><el-button @click="logout">{{t('logout')}}</el-button></el-form></div></div></template>
