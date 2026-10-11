import {defineStore} from 'pinia'

export const appearanceDefaults = {
  layout:'defaults',primary:'#409eff',dark:false,topBar:'#ffffff',topBarColor:'#606266',topBarGradient:false,
  menuBar:'#ffffff',menuBarColor:'#303133',menuBarActiveColor:'#409eff',menuBarGradient:false,
  columnsMenuBar:'#334054',columnsMenuBarColor:'#e6e6e6',columnsMenuBarGradient:false,
  collapse:false,uniqueOpened:true,fixedHeader:true,classicSplitMenu:false,showLogo:true,
  showBreadcrumb:true,breadcrumbIcon:true,showTags:true,tagsIcon:true,cacheTags:true,sortableTags:true,shareTags:false,
  showFooter:true,grayscale:false,invert:false,watermark:false,watermarkText:'',tagsStyle:'tags-style-five',
  animation:'slide-right',columnsStyle:'round',columnsDirection:'vertical',componentSize:'default',
  autoLock:false,lockSeconds:30,columnsHover:false,
}
function initialAppearance(){
  const saved=JSON.parse(localStorage.getItem('appearance') || '{}')
  if(localStorage.getItem('appearance-layout-version')!=='1'){
    saved.layout=appearanceDefaults.layout
    saved.classicSplitMenu=false
    localStorage.setItem('appearance',JSON.stringify(saved))
    localStorage.setItem('appearance-layout-version','1')
  }
  return {...appearanceDefaults,...saved} as Record<string,any>
}
export const useAppearance=defineStore('appearance',{
  state:()=>({config:initialAppearance()}),
  actions:{reset(){this.config={...appearanceDefaults}}},
})
