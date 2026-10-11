import {watchEffect,type App,type DirectiveBinding} from 'vue'
import {useAccount} from './store'
type Rule=string|string[]|{all:string[]}
const rules=new WeakMap<HTMLElement,{value:Rule;stop:()=>void;display:string}>()
export function auth(value:string){return useAccount().can(value)}
export function auths(values:string[]){return useAccount().any(values)}
export function authAll(values:string[]){return useAccount().all(values)}
function allowed(value:Rule){return typeof value==='string'?auth(value):Array.isArray(value)?auths(value):authAll(value.all)}
export function installAuthorization(app:App){app.directive('auth',{
 mounted(el:HTMLElement,binding:DirectiveBinding<Rule>){const entry={value:binding.value,stop:()=>{},display:el.style.display};rules.set(el,entry);entry.stop=watchEffect(()=>{el.style.display=allowed(entry.value)?entry.display:'none'})},
 updated(el:HTMLElement,binding:DirectiveBinding<Rule>){const entry=rules.get(el)!;entry.value=binding.value;el.style.display=allowed(entry.value)?entry.display:'none'},
 unmounted(el:HTMLElement){rules.get(el)!.stop();rules.delete(el)},
})}
