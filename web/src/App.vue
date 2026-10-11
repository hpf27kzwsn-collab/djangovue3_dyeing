<script setup lang="ts">
import {computed,defineComponent,h,onMounted,ref,watch,shallowRef} from 'vue'
import {useRoute,useRouter} from 'vue-router'
import {useI18n} from 'vue-i18n'
import {ElMessage,ElNotification,ElButton} from 'element-plus'
import MenuIcon from './components/MenuIcon.vue'
import IframePages from './components/IframePages.vue'
import {navigateMenu} from './navigation'
import {fetchEventSource} from '@microsoft/fetch-event-source'
import {version} from '../package.json'
import {useAccount} from './store'
import {useAppearance} from './appearance'
import {api} from './api'
import {routeLoading} from './route-loading'
import MenuBranch from './components/MenuBranch.vue'
import AppearanceDrawer from './components/AppearanceDrawer.vue'
import TagsBar from './components/TagsBar.vue'
import {useMobile} from './mobile'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import zhTw from 'element-plus/es/locale/lang/zh-tw'
import en from 'element-plus/es/locale/lang/en'
const route=useRoute(),router=useRouter(),account=useAccount(),appearance=useAppearance()
const {t,locale}=useI18n(),theme=computed(()=>appearance.config)
const publicPage=computed(()=>['/login','/first-password'].includes(route.path)||route.path.startsWith('/terms/'))
const title=ref('ERP 管理平台'),logo=ref(''),search=ref(''),themeDrawer=ref(false),contentFullscreen=ref(localStorage.getItem('contentFullscreen')==='true'),pageKeys=ref<Record<string,number>>({})
const mobile=useMobile(),mobileMenu=ref(false)
watch(contentFullscreen,value=>localStorage.setItem('contentFullscreen',String(value)))
const openTabs=ref<string[]>([]),cachedPages=new Map<string,any>(),cacheNames=new Map<string,string>();let cacheSerial=0
const nameFor=(key:string)=>{if(!cacheNames.has(key))cacheNames.set(key,'CachedPage'+(++cacheSerial));return cacheNames.get(key)!}
const cacheInclude=computed(()=>openTabs.value.map(path=>nameFor(path+':'+(pageKeys.value[path]||0))))
function cachedPage(component:any){const key=pageKey();if(!cachedPages.has(key)){const vnode=shallowRef(component);cachedPages.set(key,{vnode,wrapper:defineComponent({name:nameFor(key),setup:()=>()=>h(vnode.value)})})}const entry=cachedPages.get(key);entry.vnode.value=component;return entry.wrapper}
function updateTabs(paths:string[]){openTabs.value=paths;for(const key of cachedPages.keys())if(!paths.some(path=>key.startsWith(path+':'))){cachedPages.delete(key);cacheNames.delete(key)}}
const locked=ref(sessionStorage.getItem('locked')==='true'),unlockPassword=ref(''),unread=ref(0),activeCatalog=ref<number|null>(null)
const messageConnection=ref('')
const roots=computed(()=>account.menus.filter(x=>x.parent_id===null&&x.visible))
const split=computed(()=>theme.value.layout==='columns'||theme.value.layout==='classic'&&theme.value.classicSplitMenu)
const currentMenu=computed(()=>account.menus.find(x=>x.web_path===route.path))
const currentTitle=computed(()=>currentMenu.value?.name||route.meta.title||t('page'))
const ancestors=computed(()=>{const result=[];let menu=currentMenu.value;while(menu){result.unshift(menu);menu=account.menus.find(x=>x.id===menu!.parent_id)}return result})
const results=computed(()=>account.menus.filter(x=>!x.is_catalog&&x.visible&&(x.name.includes(search.value)||x.web_path.includes(search.value))))
watch(roots,items=>{if(activeCatalog.value===null&&items.length)activeCatalog.value=items[0].id})
watch(ancestors,items=>{if(items.length)activeCatalog.value=items[0].id})
watch(theme,value=>{
 localStorage.setItem('appearance',JSON.stringify(value));document.documentElement.classList.toggle('dark',value.dark)
 document.documentElement.classList.toggle('grayscale',value.grayscale);document.documentElement.classList.toggle('color-weak',value.invert)
 const style=document.documentElement.style;style.setProperty('--el-color-primary',value.primary)
 for(let n=1;n<10;n++)style.setProperty('--el-color-primary-light-'+n,`color-mix(in srgb, ${value.primary} ${100-n*10}%, ${value.dark?'#141414':'white'})`)
 for(const key of ['topBar','menuBar','columnsMenuBar'])style.setProperty('--'+key,value.dark?'#1d1e1f':value[key])
 for(const key of ['topBarColor','menuBarColor','menuBarActiveColor','columnsMenuBarColor'])style.setProperty('--'+key,value.dark&&key!=='menuBarActiveColor'?'#ddd':value[key])
},{deep:true,immediate:true})
watch(locale,value=>localStorage.setItem('language',value))
watch(()=>route.fullPath,async()=>{mobileMenu.value=false;if(!publicPage.value&&!account.user.id)await account.load()},{immediate:true})
watch(()=>[account.user.id,account.user.pwd_change_count,account.first_password],()=>{if(account.user.id&&account.first_password&&account.user.pwd_change_count===0&&!['/login','/first-password'].includes(route.path))router.replace({path:'/first-password',query:{redirect:route.fullPath}})})
watch(()=>[theme.value.autoLock,theme.value.lockSeconds,account.user.id],(_,__,onCleanup)=>{if(theme.value.autoLock&&account.user.id){const timer=setTimeout(lock,theme.value.lockSeconds*1000);onCleanup(()=>clearTimeout(timer))}})
watch(()=>account.user.id,async(id,previous,onCleanup)=>{
 if(!id){unread.value=0;return}
 const controller=new AbortController();onCleanup(()=>controller.abort())
 await fetchEventSource('/api/events/',{signal:controller.signal,openWhenHidden:true,
  fetch:(input,init)=>fetch(input,{...init,headers:{...init?.headers,Authorization:'Bearer '+localStorage.getItem('access')}}),
  async onopen(response){if(response.status===401){await api('/api/account/');throw new Error('重新连接消息服务')};if(!response.ok)throw new Error('消息连接失败：'+response.status);messageConnection.value=''},
  async onmessage(event){if(event.data==='')return;const count=JSON.parse(event.data).unread,increased=count>unread.value;unread.value=count;if(increased){const latest=(await api('/api/system/message_center/get_newest_msg/')).data;if(latest)ElNotification({title:latest.title,message:h(ElButton,{onClick:()=>router.push('/inbox')},()=>t('inbox'))})}},
  onclose(){throw new Error('消息连接已断开')},onerror(error){messageConnection.value=String(error)}
 })
})
onMounted(async()=>{const config=(await api('/api/config/')).data;title.value=config.title;logo.value=config.logo;document.title=config.title})
function logout(){locked.value=false;contentFullscreen.value=false;cachedPages.clear();cacheNames.clear();account.logout();router.push('/login')}
function mobileCommand(command:string){if(command==='theme')themeDrawer.value=true;else if(command==='fullscreen')fullscreen();else if(['zh','zh-tw','en'].includes(command))locale.value=command}
function selectCatalog(item:any){activeCatalog.value=item.id;if(!item.is_catalog)navigateMenu(item,router)}
function searchMenu(value:number){navigateMenu(account.menus.find(item=>item.id===value)!,router);search.value='';mobileMenu.value=false}
function lock(){locked.value=true;sessionStorage.setItem('locked','true')}
async function unlock(){await api('/api/account/',{method:'POST',data:{password:unlockPassword.value}});locked.value=false;sessionStorage.removeItem('locked');unlockPassword.value='';theme.value.autoLock=false}
async function fullscreen(){document.fullscreenElement?await document.exitFullscreen():await document.documentElement.requestFullscreen()}
async function refreshPage(path:string){await router.push(path);cachedPages.delete(pageKey());cacheNames.delete(pageKey());const key=theme.value.shareTags?route.path:route.fullPath;pageKeys.value[key]=(pageKeys.value[key]||0)+1}
function pageKey(){const key=theme.value.shareTags?route.path:route.fullPath;return key+':'+(pageKeys.value[key]||0)}
</script>
<template>
<el-config-provider :locale="locale==='en'?en:locale==='zh-tw'?zhTw:zhCn" :size="theme.componentSize">
 <div v-if="routeLoading" class="route-progress" aria-label="页面加载中"/>
 <router-view v-if="publicPage"/>
 <div v-else class="app-shell" :class="[theme.layout,{collapsed:theme.collapse,'content-fullscreen':contentFullscreen}]">
  <aside v-if="!mobile&&theme.layout==='columns'" class="catalog-rail" :class="[theme.columnsStyle,theme.columnsDirection,{gradient:theme.columnsMenuBarGradient}]"><button v-for="item in roots" :key="item.id" :class="{active:activeCatalog===item.id}" @click="selectCatalog(item)" @mouseenter="theme.columnsHover&&(activeCatalog=item.id)"><el-icon><MenuIcon :name="item.icon||'Folder'"/></el-icon><span>{{item.name}}</span></button></aside>
  <aside v-if="!mobile&&theme.layout!=='transverse'" class="sidebar" :class="{gradient:theme.menuBarGradient}">
   <div v-if="theme.showLogo&&theme.layout!=='classic'" class="brand" @click="router.push('/')"><img v-if="logo" :src="logo" class="brand-logo"/><span v-else class="brand-symbol">D</span><span v-if="!theme.collapse">{{title}}</span></div>
   <el-menu :default-active="route.path" :collapse="theme.collapse" :unique-opened="theme.uniqueOpened" background-color="transparent" :text-color="theme.dark?'#ddd':theme.menuBarColor" :active-text-color="theme.menuBarActiveColor"><el-menu-item index="/" @click="router.push('/')"><el-icon><House/></el-icon><span>{{t('home')}}</span></el-menu-item><MenuBranch :items="account.menus" :parent="split?activeCatalog:null"/></el-menu>
  </aside>
  <section class="workspace"><div class="workspace-heading" :class="{fixed:theme.fixedHeader}"><header class="topbar" :class="{gradient:theme.topBarGradient}">
   <div v-if="!mobile&&theme.showLogo&&['classic','transverse'].includes(theme.layout)" class="brand" @click="router.push('/')"><img v-if="logo" :src="logo" class="brand-logo"/><span v-else class="brand-symbol">D</span><span>{{title}}</span></div>
   <el-button v-if="!mobile&&theme.layout!=='transverse'" text :aria-label="t('collapse')" @click="theme.collapse=!theme.collapse"><el-icon><Fold/></el-icon></el-button>
   <el-button v-if="mobile" text aria-label="打开导航" @click="mobileMenu=true"><el-icon><Menu/></el-icon></el-button><strong v-if="mobile" class="mobile-title">{{currentTitle}}</strong><el-breadcrumb v-if="!mobile&&theme.showBreadcrumb"><el-breadcrumb-item to="/"><el-icon v-if="theme.breadcrumbIcon"><House/></el-icon>{{t('home')}}</el-breadcrumb-item><el-breadcrumb-item v-for="item in ancestors" :key="item.id" @click="!item.is_catalog&&navigateMenu(item,router)"><el-icon v-if="theme.breadcrumbIcon&&item.icon"><MenuIcon :name="item.icon"/></el-icon>{{item.name}}</el-breadcrumb-item><el-breadcrumb-item v-if="!ancestors.length&&route.path!=='/'">{{currentTitle}}</el-breadcrumb-item></el-breadcrumb>
   <div v-if="!mobile&&theme.layout==='classic'&&theme.classicSplitMenu" class="header-catalogs"><el-button v-for="item in roots" :key="item.id" :type="activeCatalog===item.id?'primary':undefined" text @click="selectCatalog(item)">{{item.name}}</el-button></div>
   <div class="top-actions"><el-select v-if="!mobile" v-model="search" filterable remote :remote-method="(value:string)=>search=value" :placeholder="t('search')" @change="searchMenu"><el-option v-for="item in results" :key="item.id" :value="item.id" :label="item.name"/></el-select>
    <el-button v-if="!mobile" text :aria-label="t('fullscreen')" @click="fullscreen"><el-icon><FullScreen/></el-icon></el-button>
    <el-badge :value="unread" :hidden="unread===0"><el-button text :aria-label="t('inbox')" :title="messageConnection||t('inbox')" @click="router.push('/inbox')"><el-icon><Bell/></el-icon></el-button></el-badge>
    <el-dropdown v-if="!mobile" @command="(value:string)=>locale=value"><el-button text>{{locale==='en'?'EN':locale==='zh-tw'?'繁':'简'}}</el-button><template #dropdown><el-dropdown-menu><el-dropdown-item command="zh">简体中文</el-dropdown-item><el-dropdown-item command="zh-tw">繁體中文</el-dropdown-item><el-dropdown-item command="en">English</el-dropdown-item></el-dropdown-menu></template></el-dropdown>
    <el-button v-if="!mobile" text :aria-label="t('settings')" @click="themeDrawer=true"><el-icon><Setting/></el-icon></el-button>
    <el-dropdown @command="(command:string)=>command==='logout'?logout():command==='lock'?lock():router.push('/profile')"><span class="account" role="button" :aria-label="t('account')" tabindex="0"><el-avatar :size="30" :src="account.user.avatar"/><span v-if="!mobile">{{account.user.name||account.user.username}}</span></span><template #dropdown><el-dropdown-menu><el-dropdown-item command="profile">{{t('account')}}</el-dropdown-item><el-dropdown-item command="lock">{{t('lock')}}</el-dropdown-item><el-dropdown-item command="logout">{{t('logout')}}</el-dropdown-item></el-dropdown-menu></template></el-dropdown>
   <el-dropdown v-if="mobile" @command="mobileCommand"><el-button text aria-label="更多功能"><el-icon><MoreFilled/></el-icon></el-button><template #dropdown><el-dropdown-menu><el-dropdown-item command="theme">{{t('settings')}}</el-dropdown-item><el-dropdown-item command="fullscreen">{{t('fullscreen')}}</el-dropdown-item><el-dropdown-item command="zh">简体中文</el-dropdown-item><el-dropdown-item command="zh-tw">繁體中文</el-dropdown-item><el-dropdown-item command="en">English</el-dropdown-item></el-dropdown-menu></template></el-dropdown></div></header>
   <el-menu v-if="!mobile&&theme.layout==='transverse'" class="horizontal-menu" mode="horizontal" :default-active="route.path"><el-menu-item index="/" @click="router.push('/')">{{t('home')}}</el-menu-item><MenuBranch :items="account.menus" :parent="null"/></el-menu>
   <TagsBar v-if="theme.showTags" :title="String(currentTitle)" :content-fullscreen="contentFullscreen" @tabs="updateTabs" @refresh="refreshPage" @fullscreen="contentFullscreen=!contentFullscreen"/>
  </div>
  <el-button v-if="contentFullscreen" class="exit-content-fullscreen" @click="contentFullscreen=false">{{t('exitFullscreen')}}</el-button>
  <main v-if="account.user.id" class="main"><el-watermark :content="theme.watermark?theme.watermarkText||account.user.name||account.user.username:''"><IframePages :key="account.user.id" :menu="currentMenu" :menus="account.menus" :path="route.fullPath" :tabs="openTabs" :versions="pageKeys" :share-tags="theme.shareTags" :show-tags="theme.showTags"/><router-view v-show="!currentMenu?.is_iframe" v-slot="{Component}"><Transition :name="theme.animation==='none'?'':theme.animation" mode="out-in"><KeepAlive :key="account.user.id" :include="theme.showTags?cacheInclude:undefined"><component :is="cachedPage(Component)" v-if="currentMenu?.cache&&!currentMenu?.is_iframe" :key="pageKey()"/></KeepAlive></Transition><Transition :name="theme.animation==='none'?'':theme.animation" mode="out-in"><component :is="Component" v-if="!currentMenu?.cache&&!currentMenu?.is_iframe" :key="pageKey()"/></Transition></router-view></el-watermark></main>
  <footer v-if="theme.showFooter" class="platform-footer">{{title}} · {{version}}</footer>
  </section>
  <el-drawer v-model="mobileMenu" title="导航" direction="ltr" size="min(320px, 90vw)" class="mobile-navigation"><el-select v-model="search" filterable remote :remote-method="(value:string)=>search=value" placeholder="搜索菜单" @change="searchMenu"><el-option v-for="item in results" :key="item.id" :value="item.id" :label="item.name"/></el-select><el-menu :default-active="route.path"><el-menu-item index="/" @click="router.push('/');mobileMenu=false">{{t('home')}}</el-menu-item><MenuBranch :items="account.menus" :parent="null"/></el-menu></el-drawer><AppearanceDrawer v-model="themeDrawer"/>
  <div v-if="locked" class="lock-screen"><div class="login-card"><el-avatar :size="64" :src="account.user.avatar"/><h2>{{account.user.name||account.user.username}}</h2><el-input v-model="unlockPassword" type="password" :placeholder="t('password')" @keyup.enter="unlock"/><el-button type="primary" @click="unlock">{{t('unlock')}}</el-button><el-button text @click="logout">{{t('logout')}}</el-button></div></div>
 </div>
</el-config-provider>
</template>

<style scoped>.route-progress{position:fixed;z-index:9999;top:0;left:0;height:3px;background:var(--el-color-primary);width:35%;animation:route-progress 1s ease-in-out infinite}@keyframes route-progress{from{transform:translateX(-100%)}to{transform:translateX(300%)}}</style>
