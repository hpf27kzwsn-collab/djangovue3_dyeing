<script setup lang="ts">
import {computed,nextTick,onBeforeUnmount,ref,watch} from 'vue'
import {useRoute,useRouter} from 'vue-router'
import Sortable from 'sortablejs'
import MenuIcon from './MenuIcon.vue'
import {useI18n} from 'vue-i18n'
import {useAccount} from '../store'
import {useAppearance} from '../appearance'
import {useMobile} from '../mobile'
const props=defineProps<{title:string;contentFullscreen:boolean}>(),emit=defineEmits(['refresh','fullscreen','tabs'])
const account=useAccount(),theme=useAppearance(),route=useRoute(),router=useRouter()
const {t}=useI18n()
const mobile=useMobile()
type Tab={path:string;fullPath?:string;title:string;affix:boolean;icon:string;menuId?:number;visited?:number}
const tabs=ref<Tab[]>([]),element=ref<HTMLElement>(),context=ref<{tab:Tab;x:number;y:number}>()
const routePath=(path:string)=>path.split(/[?#]/)[0]
const tabKey=(path:string)=>theme.config.shareTags?routePath(path):path
const current=computed(()=>tabKey(route.fullPath))
const storageKey=()=>`tabs:${account.user.id}`
function normalizeTabs(){
  const rows=new Map<string,Tab>()
  for(const tab of tabs.value){
    const fullPath=tab.fullPath||tab.path,path=tabKey(fullPath),previous=rows.get(path)
    if(!previous||fullPath===route.fullPath||previous.fullPath!==route.fullPath&&(tab.visited||0)>=(previous.visited||0))rows.set(path,{...tab,path,fullPath})
  }
  tabs.value=[...rows.values()]
}
watch(()=>account.user.id,id=>{
  tabs.value=id&&theme.config.cacheTags?JSON.parse(localStorage.getItem(storageKey()) || '[]'):[]
  if(!tabs.value.some(tab=>routePath(tab.path)==='/'))tabs.value.unshift({path:'/',fullPath:'/',title:t('home'),affix:true,icon:'House'})
  normalizeTabs()
},{immediate:true})
watch(()=>[account.menus,account.user.id],()=>{
  const menus=account.menus
  tabs.value=tabs.value.filter(tab=>!tab.menuId||menus.some(menu=>menu.id===tab.menuId))
  for(const tab of tabs.value){
    const menu=tab.menuId?menus.find(menu=>menu.id===tab.menuId):menus.find(menu=>menu.web_path===routePath(tab.path))
    if(menu){const address=tab.fullPath||tab.path,fullPath=menu.web_path+address.slice(routePath(address).length);Object.assign(tab,{path:tabKey(fullPath),fullPath,title:menu.name,affix:menu.is_affix,icon:menu.icon,menuId:menu.id})}
  }
  for(const menu of menus.filter(menu=>menu.is_affix))if(!tabs.value.some(tab=>tab.menuId===menu.id))tabs.value.push({path:menu.web_path,fullPath:menu.web_path,title:menu.name,affix:true,icon:menu.icon,menuId:menu.id})
  normalizeTabs()
},{immediate:true})
watch(()=>[route.fullPath,props.title,account.user.id,theme.config.shareTags],()=>{
  if(!account.user.id || route.path==='/login' || route.path.startsWith('/terms/'))return
  normalizeTabs()
  const menu=account.menus.find(x=>x.web_path===route.path||route.name===`menu-${x.id}`)
  if(String(route.name).startsWith('menu-')&&!menu)return
  const fullPath=menu?menu.web_path+route.fullPath.slice(route.path.length):route.fullPath,key=tabKey(fullPath)
  const tab=tabs.value.find(x=>x.path===key)
  const values={title:menu?.name||props.title,fullPath,affix:routePath(key)==='/'||!!menu?.is_affix,icon:menu?.icon||tab?.icon||'',menuId:menu?.id,visited:Date.now()}
  if(tab)Object.assign(tab,values)
  else tabs.value.push({path:key,...values})
},{immediate:true})
watch(tabs,()=>{emit('tabs',tabs.value.map(x=>x.path));if(account.user.id&&theme.config.cacheTags)localStorage.setItem(storageKey(),JSON.stringify(tabs.value))},{deep:true,immediate:true})
watch(()=>theme.config.cacheTags,value=>{if(!value)localStorage.removeItem(storageKey());else localStorage.setItem(storageKey(),JSON.stringify(tabs.value))})
function scrollToCurrent(){
  const selected=element.value?.querySelector<HTMLElement>('.active')
  if(selected){const item=selected.getBoundingClientRect(),view=element.value!.getBoundingClientRect();element.value!.scrollLeft+=item.left<view.left?item.left-view.left:item.right>view.right?item.right-view.right:0}
}
watch(()=>[current.value,element.value,tabs.value.map(tab=>tab.path).join('\0')],async()=>{
  await nextTick();scrollToCurrent()
},{flush:'post'})
watch(element,(value,_,onCleanup)=>{
  if(value){const observer=new ResizeObserver(scrollToCurrent);observer.observe(value);onCleanup(()=>observer.disconnect())}
})
watch(()=>[element.value,theme.config.sortableTags,mobile.value],(_,__,onCleanup)=>{
  if(element.value&&theme.config.sortableTags&&!mobile.value){const sortable=Sortable.create(element.value,{animation:150,onEnd:event=>{const [tab]=tabs.value.splice(event.oldIndex!,1);tabs.value.splice(event.newIndex!,0,tab)}});onCleanup(()=>sortable.destroy())}
})
function close(tab:Tab){const index=tabs.value.indexOf(tab);tabs.value.splice(index,1);if(current.value===tab.path){const next=tabs.value[index]||tabs.value[tabs.value.length-1];router.push(next.fullPath||next.path)}}
function action(name:string){const tab=context.value!.tab;context.value=undefined
  if(name==='refresh')emit('refresh',tab.fullPath||tab.path)
  if(name==='close')close(tab)
  if(name==='other'||name==='all'){tabs.value=tabs.value.filter(x=>x.affix || name==='other'&&x===tab);router.push(name==='other'?tab.fullPath||tab.path:tabs.value[0].fullPath||tabs.value[0].path)}
  if(name==='fullscreen'){router.push(tab.fullPath||tab.path);emit('fullscreen')}
}
function hide(){context.value=undefined}
function wheel(event:WheelEvent){if(!mobile.value&&event.deltaY){event.preventDefault();element.value!.scrollLeft+=event.deltaY}}
function activeAction(name:string){context.value={tab:tabs.value.find(x=>x.path===current.value)!,x:0,y:0};action(name)}
function showContext(event:MouseEvent,tab:Tab){context.value={tab,x:Math.min(event.clientX,window.innerWidth-180),y:Math.min(event.clientY,window.innerHeight-190)}}
document.addEventListener('click',hide);onBeforeUnmount(()=>document.removeEventListener('click',hide))
</script>
<template><div class="tags-bar"><nav ref="element" class="tabs" :class="theme.config.tagsStyle" @wheel="wheel"><button v-for="tab in tabs" :key="tab.path" :class="{active:current===tab.path}" @click="router.push(tab.fullPath||tab.path)" @auxclick.middle.prevent="!tab.affix&&close(tab)" @contextmenu.prevent="showContext($event,tab)">
 <el-icon v-if="theme.config.tagsIcon&&tab.icon"><MenuIcon :name="tab.icon"/></el-icon>{{tab.path==='/'?t('home'):tab.title}}<span v-if="current===tab.path" @click.stop="emit('refresh',tab.fullPath||tab.path)">↻</span><span v-if="!tab.affix" @click.stop="close(tab)">×</span>
</button></nav><el-dropdown v-if="mobile" class="tags-actions" @command="activeAction"><el-button text aria-label="标签操作">更多</el-button><template #dropdown><el-dropdown-menu><el-dropdown-item command="refresh">{{t('refreshCurrent')}}</el-dropdown-item><el-dropdown-item command="other">{{t('closeOther')}}</el-dropdown-item><el-dropdown-item command="all">{{t('closeAll')}}</el-dropdown-item><el-dropdown-item command="fullscreen">{{t(contentFullscreen?'exitFullscreen':'contentFullscreen')}}</el-dropdown-item></el-dropdown-menu></template></el-dropdown></div><Teleport to="body"><div v-if="context" class="tags-context" :style="{left:context.x+'px',top:context.y+'px'}"><button @click="action('refresh')">{{t('refreshCurrent')}}</button><button v-if="!context.tab.affix" @click="action('close')">{{t('closeCurrent')}}</button><button @click="action('other')">{{t('closeOther')}}</button><button @click="action('all')">{{t('closeAll')}}</button><button @click="action('fullscreen')">{{t(contentFullscreen?'exitFullscreen':'contentFullscreen')}}</button></div></Teleport></template>
<style scoped>.tags-bar{display:flex;min-width:0;background:var(--el-bg-color)}.tabs{flex:1;min-width:0}.tags-actions{flex-shrink:0;align-items:center;padding:0 4px;border-bottom:1px solid var(--el-border-color-light)}</style>
