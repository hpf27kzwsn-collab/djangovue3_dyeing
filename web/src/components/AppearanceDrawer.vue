<script setup lang="ts">
import {ref} from 'vue'
import {useAppearance} from '../appearance'
import {ElMessage} from 'element-plus'
import {useI18n} from 'vue-i18n'
defineProps<{modelValue:boolean}>();const emit=defineEmits(['update:modelValue'])
const appearance=useAppearance(),configuration=ref('')
const {t}=useI18n()
const colors=[['primary','主题颜色'],['topBar','顶栏背景'],['topBarColor','顶栏文字'],['menuBar','侧栏背景'],['menuBarColor','侧栏文字'],['menuBarActiveColor','选中菜单'],['columnsMenuBar','分栏背景'],['columnsMenuBarColor','分栏文字']]
const switches=[['topBarGradient','顶栏渐变'],['menuBarGradient','侧栏渐变'],['columnsMenuBarGradient','分栏渐变'],['collapse','折叠菜单'],['uniqueOpened','只展开一个目录'],['fixedHeader','固定顶栏'],['classicSplitMenu','经典布局拆分菜单'],['columnsHover','悬停切换分栏'],['showLogo','显示 Logo'],['showBreadcrumb','显示面包屑'],['breadcrumbIcon','面包屑图标'],['showTags','显示标签页'],['tagsIcon','标签图标'],['cacheTags','记住已打开标签'],['sortableTags','标签拖动排序'],['shareTags','同一路径共用标签'],['showFooter','显示页脚'],['grayscale','灰度模式'],['invert','色弱模式'],['watermark','显示水印'],['autoLock','启用定时锁屏']]
const selects=[{key:'layout',label:'布局',options:[['defaults','默认'],['classic','经典'],['transverse','横向'],['columns','分栏']]},
 {key:'tagsStyle',label:'标签样式',options:[['tags-style-one','简洁'],['tags-style-two','卡片'],['tags-style-three','圆角'],['tags-style-four','下划线'],['tags-style-five','按钮']]},
 {key:'animation',label:'页面动画',options:[['none','无'],['slide-right','滑动'],['fade','淡入'],['scale','缩放']]},
 {key:'columnsStyle',label:'分栏按钮',options:[['round','圆角'],['square','方形']]},
 {key:'columnsDirection',label:'分栏文字',options:[['vertical','上下排列'],['horizontal','左右排列']]},
 {key:'componentSize',label:'组件尺寸',options:[['large','大'],['default','默认'],['small','小']]}]
async function copy(){configuration.value=JSON.stringify(appearance.config,null,2);await navigator.clipboard.writeText(configuration.value);ElMessage.success(t('appearance.copied'))}
function apply(){appearance.config={...appearance.config,...JSON.parse(configuration.value)};ElMessage.success(t('appearance.applied'))}
</script>
<template><el-drawer :model-value="modelValue" :title="t('appearance.title')" size="min(390px, 100vw)" @update:model-value="emit('update:modelValue',$event)"><el-form label-width="160px">
 <el-form-item v-for="item in selects" :key="item.key" :label="t('appearance.'+item.key)"><el-select v-model="appearance.config[item.key]"><el-option v-for="option in item.options" :key="option[0]" :value="option[0]" :label="t('appearance.options.'+option[0])"/></el-select></el-form-item>
 <el-form-item :label="t('appearance.dark')"><el-switch v-model="appearance.config.dark"/></el-form-item>
 <el-form-item v-for="[key] in colors" :key="key" :label="t('appearance.'+key)"><el-color-picker v-model="appearance.config[key]"/></el-form-item>
 <el-form-item v-for="[key] in switches" :key="key" :label="t('appearance.'+key)"><el-switch v-model="appearance.config[key]"/></el-form-item>
 <el-form-item :label="t('appearance.watermarkText')"><el-input v-model="appearance.config.watermarkText" :placeholder="t('appearance.watermarkHint')"/></el-form-item>
 <el-form-item :label="t('appearance.lockSeconds')"><el-input-number v-model="appearance.config.lockSeconds"/></el-form-item>
 <el-divider>{{t('appearance.configuration')}}</el-divider><el-input v-model="configuration" type="textarea" :rows="5" :placeholder="t('appearance.configurationHint')"/>
 <div class="appearance-actions"><el-button @click="copy">{{t('appearance.copy')}}</el-button><el-button @click="apply">{{t('appearance.apply')}}</el-button><el-button @click="appearance.reset">{{t('appearance.reset')}}</el-button></div>
</el-form></el-drawer></template>
