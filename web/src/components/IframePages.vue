<script setup lang="ts">
import {computed,ref,watch} from 'vue'
import type {Menu} from '../store'
const props=defineProps<{menu?:Menu;menus:Menu[];path:string;tabs:string[];versions:Record<string,number>;shareTags:boolean;showTags:boolean}>()
type Frame={key:string;title:string;url:string;cache:boolean;loading:boolean}
const frames=ref<Frame[]>([]),current=computed(()=>props.shareTags?props.path.split(/[?#]/)[0]:props.path)
watch(()=>[props.path,props.menu,props.menus,props.versions[current.value]],()=>{
  frames.value=frames.value.filter(frame=>props.menus.some(menu=>menu.web_path===frame.key.split(/[?#]/)[0]&&menu.is_iframe))
  for(const frame of frames.value){const menu=props.menus.find(menu=>menu.web_path===frame.key.split(/[?#]/)[0])!;const url=menu.link_url.replaceAll('{{token}}',localStorage.getItem('access')!);if(frame.url!==url)frame.loading=true;Object.assign(frame,{title:menu.name,url,cache:menu.cache})}
  frames.value=frames.value.filter(frame=>frame.key===current.value||frame.cache&&(!props.showTags||props.tabs.includes(frame.key)))
  if(props.menu?.is_iframe&&!frames.value.some(frame=>frame.key===current.value)){
    frames.value.push({key:current.value,title:props.menu.name,url:props.menu.link_url.replaceAll('{{token}}',localStorage.getItem('access')!),cache:props.menu.cache,loading:true})
  }
},{immediate:true})
watch(()=>props.tabs,tabs=>{if(props.showTags)frames.value=frames.value.filter(frame=>frame.key===current.value||tabs.includes(frame.key))},{deep:true})
watch(()=>props.versions[current.value],()=>{
  if(props.menu?.is_iframe){const frame=frames.value.find(item=>item.key===current.value)!;frame.loading=true;frame.url=props.menu.link_url.replaceAll('{{token}}',localStorage.getItem('access')!)}
})
</script>
<template><div v-show="menu?.is_iframe" class="iframe-pages"><section v-for="frame in frames" v-show="menu?.is_iframe&&frame.key===current" :key="frame.key" v-loading="frame.loading"><iframe :key="frame.key+':'+(versions[frame.key]||0)" :src="frame.url" class="embedded-page" :title="frame.title" @load="frame.loading=false"/></section></div></template>
<style scoped>.iframe-pages,.iframe-pages section{width:100%;min-width:0}.embedded-page{width:100%;height:calc(100dvh - 150px);border:0;display:block}</style>
