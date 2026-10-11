import { defineStore } from 'pinia'
import { api } from './api'
import {registerMenus,clearMenus,router} from './router'
import {accountMenus} from './navigation'
export interface Menu {id:number;name:string;icon:string;parent_id:number|null;component_name:string;component:string;resource:string;web_path:string;is_catalog:boolean;visible:boolean;is_link:boolean;link_url:string;is_iframe:boolean;is_affix:boolean;cache:boolean}
export const useAccount = defineStore('account', {
  state: () => ({user: {} as Record<string, any>, menus: [] as Menu[], buttons: [] as string[], superuser: false, first_password:false}),
  actions: {
    async load() {const route=router.currentRoute.value,current=this.menus.find(menu=>menu.web_path===route.path);const data=(await api('/api/account/')).data;data.menus=accountMenus(data);const updated=data.menus.find((menu:Menu)=>menu.id===current?.id);registerMenus(data.menus);Object.assign(this,data);await router.replace(current?updated?{path:updated.web_path,query:route.query,hash:route.hash}:'/':route.fullPath)},
    can(value: string) {return this.superuser || this.buttons.includes(value)},
    any(values:string[]){return values.some(value=>this.can(value))},
    all(values:string[]){return values.every(value=>this.can(value))},
    logout() {localStorage.removeItem('access'); localStorage.removeItem('refresh');clearMenus();sessionStorage.removeItem('locked'); this.$reset()}
  }
})
