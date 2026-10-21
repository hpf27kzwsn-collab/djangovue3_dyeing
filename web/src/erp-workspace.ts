import type {Menu} from './store'
import presentation from './erp-business-presentation.json'

export const moduleKeys=['erp_base','erp_sales','erp_purchase','erp_sampling','erp_production','erp_warehouse','erp_quality']
const systemKeys=new Set(['system'])
const demos=new Set(['component_demo','chart_demo'])
export const commonKeys=presentation.common_keys
export const preferredEntries=presentation.preferred as Record<string,string[]>
const fieldTitles:Record<string,string>={Code:'编码',NameC:'名称',Name:'名称',NumValue:'数值',Creater:'创建人',CreateDate:'创建时间',Modifyer:'修改人',ModifyDate:'修改时间',Kind:'类型',Description:'说明',SheetNo:'单据号',SheetDate:'单据日期',SheetSeries:'单据流水',DetailNo:'明细号',SortValue:'排序'}
export function businessFieldTitle(title:string){return fieldTitles[title]??title}
export function businessTitle(value:string){
  return value.replaceAll('完整旧业务资料','业务资料与单据').replaceAll('原表检索','资料汇总')
    .replaceAll('原分类待核','其他分类').replaceAll('历史基础来源','历史档案').replaceAll('历史基础资料','历史档案')
    .replaceAll('原表总览','资料汇总').replaceAll('原未编码资料','未编码资料').replaceAll('（原分类含义待核）','')
    .replaceAll('（用途待核）','').replaceAll('（独立旧表）','（独立资料）').replaceAll('（旧启停状态保留）','')
    .replaceAll('原字段','字段').replaceAll('原分类','分类').replaceAll('原表','资料表')
    .replaceAll('旧平台来源：','配置档案：')
}
export function presentMenus(menus:Menu[]){
  const names=presentation.names as Record<string,string>
  const byId=new Map(menus.map(menu=>[menu.id,menu]))
  return menus.map(menu=>({...menu,name:businessTitle(belongsTo(menu,systemKeys,byId)?menu.name:names[menu.component_name]??menu.name)}))
}
function belongsTo(menu:Menu,keys:Set<string>,byId:Map<number,Menu>){
  let node:Menu|undefined=menu
  while(node){if(keys.has(node.component_name))return true;node=node.parent_id===null?undefined:byId.get(node.parent_id)}
  return false
}
export function managementMenus(menus:Menu[]){
  const byId=new Map(menus.map(menu=>[menu.id,menu]))
  return menus.filter(menu=>!menu.is_catalog&&menu.visible&&!demos.has(menu.component_name)&&belongsTo(menu,systemKeys,byId))
}
export function workspaceMenus(menus:Menu[]){
  const byId=new Map(menus.map(menu=>[menu.id,menu])),erp=menus.find(menu=>menu.component_name==='erp')
  const result=menus.filter(menu=>menu.visible&&menu.component_name!=='erp'&&!belongsTo(menu,demos,byId))
    .map(menu=>({...menu,parent_id:menu.parent_id===erp?.id?null:menu.parent_id}))
  function hasPage(menu:Menu):boolean{return !menu.is_catalog||result.some(child=>child.parent_id===menu.id&&hasPage(child))}
  const pages=result.filter(hasPage)
  const roots=pages.filter(menu=>menu.parent_id===null).sort((a,b)=>{
    const first=moduleKeys.indexOf(a.component_name),second=moduleKeys.indexOf(b.component_name)
    return (a.component_name==='system'?moduleKeys.length+1:first<0?moduleKeys.length:first)-(b.component_name==='system'?moduleKeys.length+1:second<0?moduleKeys.length:second)
  })
  return [...roots,...pages.filter(menu=>menu.parent_id!==null)]
}
export function businessMenus(menus:Menu[]){
  const byId=new Map(menus.map(menu=>[menu.id,menu]))
  return workspaceMenus(menus).filter(menu=>!belongsTo(menu,systemKeys,byId))
}
export function descendants(menu:Menu,menus:Menu[]):Menu[]{
  const byId=new Map(menus.map(item=>[item.id,item]))
  return menus.filter(item=>!item.is_catalog&&belongsTo(item,new Set([menu.component_name]),byId))
}
export function businessBrand(title:string){return title==='ERP 管理平台'?'染色ERP':title}
export function businessSubtitle(subtitle:string){return subtitle==='组织、权限、系统数据与消息任务'?'销售、采购、打样、生产、仓储与质量业务管理':subtitle}
