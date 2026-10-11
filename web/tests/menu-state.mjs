// Execute the component source with real Vue reactivity; network and DOM dependencies are isolated.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire,stripTypeScriptTypes} from 'node:module';
import assert from 'node:assert/strict';
const web=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..'),require=createRequire(path.join(web,'package.json'));
const vue=require('vue'),{ref,reactive,computed,nextTick,effectScope}=vue;
const source=file=>stripTypeScriptTypes(fs.readFileSync(path.join(web,'src',file),'utf8').match(/<script[^>]*>([\s\S]*?)<\/script>/)[1],{mode:'strip'}).replace(/^import .*$/gm,'');
const evaluate=(file,globals,result)=>new Function(...Object.keys(globals),source(file)+';return '+result)(...Object.values(globals));
const hooks={onMounted:()=>{},onActivated:()=>{},onDeactivated:()=>{},onBeforeUnmount:()=>{}};
const checks={};
function tags({shared=true,fullPath='/system/user?dept=3',affix=false,cached=[],id=1}={}){
 const account=reactive({user:{id},menus:[{id:2,web_path:'/system/user',name:'用户',is_affix:affix,icon:'User'}]});
 const route=reactive({path:fullPath.split(/[?#]/)[0],fullPath,name:'menu-2'}),props=reactive({title:'用户',contentFullscreen:false});
 const theme=reactive({config:{cacheTags:true,shareTags:shared,sortableTags:false}}),events=[],navigations=[],resizes=[],storage=new Map([['tabs:1',JSON.stringify(cached)]]);
 const state=evaluate('components/TagsBar.vue',{...vue,...hooks,defineProps:()=>props,defineEmits:()=>((...args)=>events.push(args)),
 useAccount:()=>account,useAppearance:()=>theme,useRoute:()=>route,useRouter:()=>({push:value=>navigations.push(value)}),useI18n:()=>({t:x=>x}),useMobile:()=>ref(true),Sortable:{},
 localStorage:{getItem:key=>storage.get(key),setItem:(key,value)=>storage.set(key,value),removeItem:key=>storage.delete(key)},document:{addEventListener:()=>{},removeEventListener:()=>{}},ResizeObserver:class{constructor(callback){resizes.push(callback)}observe(){}disconnect(){}}},'{tabs,current,activeAction,close,element}');
 return {...state,account,route,props,theme,events,navigations,storage,resizes};
}
const scope=effectScope();
await scope.run(async()=>{
 const shared=tags();shared.route.fullPath='/system/user?dept=9';await nextTick();
 assert.equal(shared.tabs.value.filter(tab=>tab.menuId===2).length,1);assert.equal(shared.tabs.value.find(tab=>tab.menuId===2).fullPath,'/system/user?dept=9');
 checks.shared_query_update={latest_query:true};
 const a=tags();a.theme.config.shareTags=false;await nextTick();a.activeAction('refresh');
 assert.equal(a.tabs.value.filter(tab=>tab.path===a.current.value).length,1);
 assert.deepEqual(a.events.at(-1),['refresh','/system/user?dept=3']);
 a.route.fullPath='/system/user?dept=4#section';await nextTick();a.theme.config.shareTags=true;await nextTick();a.activeAction('refresh');
 assert.equal(a.tabs.value.filter(tab=>tab.menuId===2).length,1);assert.equal(a.current.value,'/system/user');
 assert.deepEqual(a.events.at(-1),['refresh','/system/user?dept=4#section']);
 a.theme.config.shareTags=false;await nextTick();a.close(a.tabs.value.find(tab=>tab.path===a.current.value));assert.equal(a.navigations.at(-1),'/');
 checks.F36={both_directions:true,latest_query_and_hash:true,close_to_home:true};
 const hydrated=tags({shared:false,cached:[{path:'/system/user',fullPath:'/system/user?dept=3',title:'缓存用户',menuId:2,icon:'User',affix:false}]});
 assert.equal(hydrated.tabs.value.filter(tab=>tab.menuId===2).length,1);assert.equal(hydrated.tabs.value.at(-1).path,'/system/user?dept=3');
 hydrated.account.user.id=2;await nextTick();assert.ok(!hydrated.tabs.value.some(tab=>tab.title==='缓存用户'));checks.cached_account_isolation=true;
 for(const affix of [false,true]){
  const b=tags({affix});b.account.menus=[{...b.account.menus[0],web_path:'/erp-users',name:'ERP用户'}];b.props.title='页面';await nextTick();
  b.route.path='/erp-users';b.route.fullPath='/erp-users?dept=3';b.props.title='ERP用户';await nextTick();
  assert.equal(b.tabs.value.filter(tab=>tab.menuId===2).length,1);assert.ok(!b.tabs.value.some(tab=>tab.path==='/system/user'));
  const tab=b.tabs.value.find(tab=>tab.menuId===2);assert.equal(tab.fullPath,'/erp-users?dept=3');assert.equal(tab.affix,affix);
  b.account.menus=[];b.props.title='页面';await nextTick();assert.ok(!b.tabs.value.some(tab=>tab.menuId===2||tab.path==='/erp-users'));
 }
 checks.F32_R2={ordinary_and_affix:true,path_query_title_migrated:true,deleted_menu_removed:true};
 const scroll=tags();let item={left:1100,right:1210};const viewport={left:0,right:300};
 scroll.element.value={scrollLeft:0,querySelector:()=>({getBoundingClientRect:()=>item}),getBoundingClientRect:()=>viewport};
 await nextTick();await nextTick();assert.equal(scroll.element.value.scrollLeft,910);
 item={left:-100,right:10};scroll.route.fullPath='/system/user?dept=8';await nextTick();await nextTick();assert.equal(scroll.element.value.scrollLeft,810);
 item={left:210,right:310};viewport.right=240;scroll.resizes[0]();assert.equal(scroll.element.value.scrollLeft,880);
 checks.F37={local_scroll_to_current:true,right_and_left:true,container_resize:true};
 // The entire ResourceTable script runs, including its actual metadata watcher/reset callback.
 const account=reactive({user:{id:1},menus:[{id:2,web_path:'/business',component:'system/Resource',component_name:'before'}],buttons:['before:add'],superuser:false,can(value){return this.buttons.includes(value)}});
 const route=reactive({path:'/business',query:{}}),props=reactive({meta:{entity:'post',pk:'id',fields:[]}});
 const binding=ref({pagination:{currentPage:3,pageSize:20}}),search=ref({name__icontains:'keep'}),resourceMobile=ref(false);let resets=0,refreshes=0;
 const crudExpose={getSearchFormData:()=>search.value,setSearchFormData:({form})=>search.value=form,doRefresh:async()=>refreshes++,getBaseTableRef:()=>({clearSelection:()=>{}})};
 const table=evaluate('components/ResourceTable.vue',{...vue,...hooks,defineProps:()=>props,useAccount:()=>account,useRoute:()=>route,useRouter:()=>({}),useMobile:()=>resourceMobile,
 api:async()=>({data:[]}),resourceQuery:x=>x,toTree:x=>x,dict:x=>x,compute:fn=>fn,searches:{post:['name']},componentNames:[],fileSize:x=>x,merge:(target,value)=>Object.assign(target,value),
 useFs:()=>({crudBinding:binding,crudRef:ref(),crudExpose,appendCrudBinding:options=>Object.assign(binding.value,options),resetCrudOptions:options=>{resets++;binding.value={pagination:{currentPage:1,pageSize:10},...options}}})},'{can,permissionPrefix,isOwnRoute,createCrudOptions,payload}');
 assert.equal(table.can('add'),true);account.menus=[{...account.menus[0],component_name:'after',web_path:'/renamed'}];account.buttons=['after:add'];route.path='/renamed';
 assert.equal(table.permissionPrefix.value,'after');assert.equal(table.can('add'),true);assert.equal(table.isOwnRoute(),true);
 route.path='/other-resource';assert.equal(table.permissionPrefix.value,'after');assert.equal(table.isOwnRoute(),false);
 props.meta={...props.meta,fields:[{key:'name',title:'名称',kind:'text',is_query:true,is_create:false,is_update:false,options:[],default:null}]};await nextTick();await nextTick();
 assert.equal(resets,1);assert.equal(refreshes,1);assert.equal(binding.value.pagination.currentPage,3);assert.deepEqual(search.value,{name__icontains:'keep'});
 assert.equal(binding.value.columns.name.addForm.show,false);assert.equal(binding.value.columns.name.editForm.show,false);
 assert.deepEqual(table.payload({name:'已撤销新增字段'}),{});
 assert.equal(binding.value.actionbar.buttons.add.show,true);
 account.buttons=[];props.meta={...props.meta,fields:[{...props.meta.fields[0],is_query:false}]};await nextTick();await nextTick();assert.equal(binding.value.actionbar.buttons.add.show,false);
 assert.equal(binding.value.columns.name.column.show,false);assert.deepEqual(search.value,{});
 checks.F38={prefix_follows_menu_identity:true,inactive_page_isolated:true,metadata_updates_field_and_button_grants:true,search_and_page_preserved:true,revoked_query_and_write_fields_removed:true};
 assert.equal(table.createCrudOptions().crudOptions.form.labelPosition,'right');resourceMobile.value=true;await nextTick();
 assert.equal(binding.value.addForm.labelPosition,'top');assert.equal(binding.value.editForm.labelWidth,'auto');
 assert.equal(table.createCrudOptions().crudOptions.form.labelPosition,'top');checks.mobile_form_layout={literal_top_and_right:true,viewport_updates_form_options:true};
 // Exercise the Resource page metadata watcher with unchanged entity, not just a text assertion.
 const pageProps=reactive({entity:'post'}),pageAccount=reactive({menus:[],buttons:[]}),calls=[];
 evaluate('pages/Resource.vue',{...vue,defineProps:()=>pageProps,useRoute:()=>({path:'/business'}),useAccount:()=>pageAccount,
 api:async url=>{calls.push(url);return {data:{entity:'post'}}}},'{meta}');await nextTick();
 pageAccount.menus=[{id:2}];pageAccount.buttons=['after:list'];await nextTick();await nextTick();assert.equal(calls.length,2);
 checks.resource_metadata_reload={same_entity_reload:true,calls};
 const frameProps=reactive({path:'/frame?dept=3#section',menu:{name:'内嵌',is_iframe:true,web_path:'/frame',link_url:'/terms/privacy',cache:true},menus:[],tabs:['/frame'],versions:{},shareTags:true,showTags:true});frameProps.menus=[frameProps.menu];
 const frames=evaluate('components/IframePages.vue',{...vue,defineProps:()=>frameProps,localStorage:{getItem:()=>''}},'{frames,current}');
 assert.equal(frames.current.value,'/frame');assert.equal(frames.frames.value.length,1);
 frameProps.shareTags=false;frameProps.tabs=[frameProps.path];await nextTick();assert.equal(frames.current.value,frameProps.path);assert.equal(frames.frames.value.length,1);
 frameProps.shareTags=true;frameProps.tabs=['/frame'];await nextTick();assert.equal(frames.frames.value.length,1);assert.equal(frames.frames.value[0].key,'/frame');
 checks.iframe_share_identity={query_hash_and_both_modes:true,no_duplicate_frames:true};
});scope.stop();
const result={date:new Date().toISOString().slice(0,10),method:'actual component scripts with real Vue watch/nextTick; dependency-isolated, browser evidence recorded separately',checks};
fs.writeFileSync(path.resolve(web,'..',process.argv[2]||'docs/menu-state-verification.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));
