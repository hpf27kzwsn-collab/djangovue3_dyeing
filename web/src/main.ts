import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import { FastCrud } from '@fast-crud/fast-crud'
import ui from '@fast-crud/ui-element'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'
import '@fast-crud/fast-crud/dist/style.css'
import './style.css'
import './appearance.css'
import './components/widgets.css'
import { router } from './router'
import { i18n } from './i18n'
import FieldInput from './components/FieldInput.vue'
import DictionaryBadge from './components/DictionaryBadge.vue'
import ColoredTag from './components/ColoredTag.vue'
import FileThumbnail from './components/FileThumbnail.vue'
import {installAuthorization} from './authorization'
import App from './App.vue'
import { installPlugins } from './plugins'

const app = createApp(App)
app.use(createPinia()).use(router).use(ElementPlus).use(i18n).use(ui)
app.use(FastCrud, {commonOptions: () => ({request: {
  transformQuery: ({page, form, sort}: any) => ({page: page.currentPage, limit: page.pageSize, ...form,
    ...(sort.asc !== undefined ? {ordering:(sort.asc ? '' : '-') + sort.prop} : {})}),
  transformRes: ({res}: any) => ({records:res.data, currentPage:res.page, pageSize:res.limit, total:res.total})
}})})
app.component('FieldInput', FieldInput)
app.component('DictionaryBadge',DictionaryBadge)
app.component('ColoredTag',ColoredTag)
app.component('FileThumbnail',FileThumbnail)
installAuthorization(app)
installPlugins(app, router)
router.isReady().then(()=>app.mount('#app'))

import './responsive.css'
