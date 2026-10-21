import { createRouter, createWebHistory } from 'vue-router'
import {useAccount} from './store'
import {routeLoading} from './route-loading'
import {checkVersion} from './version'
import {pages} from './page-catalog'
import {managementMenus} from './erp-workspace'
export const router = createRouter({history: createWebHistory(), routes: [
  {path: '/login', component: () => import('./pages/Login.vue')},
  {path:'/first-password',component:()=>import('./pages/FirstPassword.vue'),meta:{title:'首次修改密码'}},
  {path:'/401',component:()=>import('./pages/Unauthorized.vue'),meta:{title:'无访问权限'}},
  {path: '/terms/:type', component: () => import('./pages/Terms.vue')},
  {path: '/', component: () => import('./pages/Home.vue'), meta:{title:'首页'}},
  {path: '/system/:entity', component: () => import('./pages/Resource.vue')},
  {path: '/profile', component: () => import('./pages/Profile.vue'), meta:{title:'个人中心'}},
  {path: '/management', component: () => import('./pages/Management.vue'), meta:{title:'系统管理'}},
  {path: '/inbox', component: () => import('./pages/Inbox.vue'), meta:{title:'我的消息'}},
  {path: '/:pathMatch(.*)*', component: () => import('./pages/NotFound.vue')}
]})
const menuRoutes:Array<()=>void>=[]
export function clearMenus(){for(const remove of menuRoutes)remove();menuRoutes.length=0}
export function registerMenus(menus:any[]) {
  clearMenus()
  for(const menu of menus.filter(x=>!x.is_catalog)) {
    menuRoutes.push(router.addRoute({name:'menu-'+menu.id,path:menu.web_path,
      component:menu.is_link&&!menu.is_iframe?()=>import('./pages/LinkLanding.vue'):menu.component==='system/Resource'?()=>import('./pages/Resource.vue'):menu.is_iframe?()=>import('./pages/Home.vue'):pages['./'+menu.component+'.vue'],
      props:menu.component==='system/Resource'?{entity:menu.resource}:undefined}))
  }
}
router.beforeEach(to => {
  routeLoading.value=true
  if (to.path !== '/login' && !to.path.startsWith('/terms/') && !localStorage.getItem('access')) return {path:'/login',query:{redirect:to.fullPath}}
  const account=useAccount()
  if(account.user.id){
    if(to.path==='/management'&&!managementMenus(account.menus).length)return '/401'
    if(to.path.startsWith('/management/')&&!account.menus.some(menu=>!menu.is_catalog&&menu.web_path===to.path))return '/401'
    if(to.path.startsWith('/system/')&&to.params.entity&&!account.menus.some(menu=>!menu.is_catalog&&(menu.resource===to.params.entity||menu.component_name===to.params.entity)))return '/401'
  }
  if(account.user.id&&account.first_password&&account.user.pwd_change_count===0&&!['/login','/first-password'].includes(to.path)&&!to.path.startsWith('/terms/'))return {path:'/first-password',query:{redirect:to.fullPath}}
})
router.afterEach(()=>{routeLoading.value=false;checkVersion()})
router.onError(()=>{routeLoading.value=false})
