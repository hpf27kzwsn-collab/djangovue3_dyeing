<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { api } from '../api'
import { useAccount } from '../store'
const router = useRouter(), route=useRoute(), account = useAccount(), {t} = useI18n()
const formRef=ref()
const rules={username:[{required:true,message:'请填写账号'}],password:[{required:true,message:'请填写密码'}],captcha:[{required:true,message:'请填写验证码'}]}
const form = reactive({username:'',password:'',captcha:'',captcha_key:''})
const config = ref({title:'ERP 管理平台',captcha:false,first_password:false,logo:'',subtitle:'',copyright:'',keep_record:'',help_url:'',privacy_url:'/terms/privacy',clause_url:'/terms/service'}), image = ref(''), loading=ref(false)
async function captcha() {form.captcha='';const data=(await api('/api/captcha/')).data;form.captcha_key=data.key;image.value=data.image}
onMounted(async () => {config.value=(await api('/api/config/')).data;if(config.value.captcha) await captcha()})
async function login() {
  if(!await formRef.value.validate(()=>{}))return
  loading.value=true
  try {
    const response = await api('/api/login/', {method:'POST', data:form})
    localStorage.setItem('access',response.data.access);localStorage.setItem('refresh',response.data.refresh)
    await account.load()
    const redirect=String(route.query.redirect||'/')
    router.push(config.value.first_password && response.data.pwd_change_count === 0 ? {path:'/first-password',query:{redirect}} : redirect)
  } catch(error) {if(config.value.captcha)await captcha();throw error} finally {loading.value=false}
}
</script>
<template><div class="login-page"><div class="login-intro"><img v-if="config.logo" :src="config.logo" class="brand-logo"/><span v-else class="brand-symbol">D</span><h1>{{ config.title }}</h1><p>{{config.subtitle}}</p><div class="intro-grid"><span>{{t('organization')}}</span><span>{{t('permissions')}}</span><span>{{t('systemData')}}</span><span>{{t('messageTasks')}}</span></div></div><div class="login-card"><div class="mobile-login-brand"><img v-if="config.logo" :src="config.logo" class="brand-logo"/><strong>{{config.title}}</strong></div><h2>{{t('welcome')}}</h2><p class="muted">{{t('loginHint')}}</p><el-form ref="formRef" :model="form" :rules="rules" @submit.prevent="login"><el-form-item prop="username"><el-input v-model="form.username" size="large" :placeholder="t('username')" autocomplete="username"/></el-form-item><el-form-item prop="password"><el-input v-model="form.password" size="large" type="password" show-password :placeholder="t('password')" autocomplete="current-password"/></el-form-item><el-form-item v-if="config.captcha" prop="captcha"><el-input v-model="form.captcha" :placeholder="t('captcha')"/><img :src="image" @click="captcha"/></el-form-item><el-button type="primary" size="large" native-type="submit" :loading="loading" style="width:100%">{{ t('login') }}</el-button></el-form><p class="terms"><a v-if="config.help_url" :href="config.help_url" target="_blank">帮助</a> · <a :href="config.privacy_url">{{t('privacy')}}</a> · <a :href="config.clause_url">{{t('service')}}</a></p><footer class="login-footer"><span>Copyright © {{config.copyright}}</span><a v-if="config.keep_record" href="https://beian.miit.gov.cn" target="_blank">{{config.keep_record}}</a></footer></div></div></template>


<style scoped>.mobile-login-brand{display:none}@media(max-width:768px){.mobile-login-brand{display:flex;align-items:center;gap:10px;margin-bottom:20px}}</style>

<style scoped>.login-footer,.terms{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;overflow-wrap:anywhere}.login-footer{font-size:12px;color:var(--el-text-color-secondary);margin-top:22px}</style>
