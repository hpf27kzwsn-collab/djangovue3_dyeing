import type {Menu} from './store'
import type {Router} from 'vue-router'

export function menuLink(menu:Menu){return menu.link_url.replaceAll('{{token}}',localStorage.getItem('access')||'')}
export function navigateMenu(menu:Menu,router:Router){
  if(menu.is_link&&!menu.is_iframe){
    const target=new URL(menuLink(menu),window.location.origin)
    if(target.origin===window.location.origin)return router.push(target.pathname+target.search+target.hash)
    window.open(target.href,'_blank');return router.push(menu.web_path)
  }
  else return router.push(menu.web_path)
}

// 改为 frontend 时，菜单由此文件和账号角色决定；接口权限继续由后端判断。
export const navigation:{mode:'backend'|'frontend';menus:Array<Menu&{roles?:string[]}>}={mode:'backend',menus:[]}
export function accountMenus(data:{menus:Menu[];user:{role_info:Array<{key:string}>};superuser:boolean}):Menu[]{
  if(navigation.mode==='backend')return data.menus
  const keys=data.user.role_info.map(role=>role.key)
  const allowed=navigation.menus.filter(menu=>data.superuser||!menu.roles?.length||menu.roles.some(key=>keys.includes(key)))
  const ids=new Set(allowed.map(menu=>menu.id))
  return allowed.filter(menu=>{let parent=menu.parent_id;while(parent!==null){if(!ids.has(parent))return false;parent=navigation.menus.find(item=>item.id===parent)!.parent_id}return true})
}
