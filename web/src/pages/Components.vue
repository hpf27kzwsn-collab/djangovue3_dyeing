<script setup lang="ts">
import {computed,ref} from 'vue'
import Calendar from '../components/Calendar.vue'
import NoticeBar from '../components/NoticeBar.vue'
import FilePicker from '../components/FilePicker.vue'
import RichText from '../components/RichText.vue'
import RemoteSelect from '../components/RemoteSelect.vue'
import {auth,auths,authAll} from '../authorization'
import AvatarCrop from '../components/AvatarCrop.vue'
const selectedUsers=ref<number[]>([]),fileEvent=ref('尚未操作'),noticeEvent=ref('')
const dates=ref<Date[]>([]),crossPage=ref(true),rangeEnabled=ref(false),range=computed<[Date,Date]|undefined>(()=>rangeEnabled.value?[new Date(new Date().getFullYear(),0,1),new Date(new Date().getFullYear(),1,10)]:undefined)
const images=ref<string[]>([]),file=ref(''),content=ref('<p>富文本编辑器</p>'),avatar=ref(''),disabled=ref(false),text=ref('')
</script>
<template><div class="page"><h2>组件示例</h2><el-tabs><el-tab-pane label="滚动公告"><NoticeBar text="此处复刻原项目的滚动公告，可配置速度、延迟、图标、颜色和关闭或跳转事件。" mode="closeable" left-icon="Bell" right-icon="Close" @close="noticeEvent='公告已关闭'"/><NoticeBar text="点击右侧箭头打开公告。" mode="link" right-icon="ArrowRight" @link="noticeEvent='已触发公告链接'"/><NoticeBar scrollable><el-carousel height="40px" direction="vertical" :autoplay="true" indicator-position="none"><el-carousel-item v-for="item in ['垂直公告一','垂直公告二']" :key="item">{{item}}</el-carousel-item></el-carousel></NoticeBar><p>{{noticeEvent}}</p></el-tab-pane><el-tab-pane label="日历"><div class="toolbar"><el-checkbox v-model="crossPage">跨月保留选择</el-checkbox><el-checkbox v-model="rangeEnabled">指定日期范围</el-checkbox></div><Calendar v-model="dates" multiple :cross-page="crossPage" :range="range"/></el-tab-pane><el-tab-pane label="文件选择器"><h3>多图片选择</h3><FilePicker v-model="images" images multiple/><h3>文件选择</h3><FilePicker v-model="file" @save="fileEvent='已确认选择'" @close="fileEvent+=' · 关闭'" @closed="fileEvent+=' · 关闭动画完成'"><template #actionbar-left="{selected}"><el-tag>已选 {{selected.length}}</el-tag></template><template #actionbar-right><span>本地文件库</span></template></FilePicker><p>{{fileEvent}}</p></el-tab-pane><el-tab-pane label="富文本"><el-checkbox v-model="disabled">禁用编辑器</el-checkbox><RichText v-model="content" :disabled="disabled" @change="(_html:string,value:string)=>text=value"/><h3>HTML 输出</h3><pre>{{content}}</pre><h3>纯文本输出</h3><pre>{{text}}</pre></el-tab-pane><el-tab-pane label="关联与授权"><h3>分页远程用户多选</h3><RemoteSelect v-model="selectedUsers" entity="user" label="username" multiple/><p>提交用户 ID：{{selectedUsers}}</p><p v-auth="'user:list'">拥有用户查询权限时可见</p><p>任一权限：{{auths(['user:list','dept:list'])}}；全部权限：{{authAll(['user:list','dept:list'])}}</p></el-tab-pane><el-tab-pane label="头像裁剪"><AvatarCrop v-model="avatar"/></el-tab-pane></el-tabs></div></template>
