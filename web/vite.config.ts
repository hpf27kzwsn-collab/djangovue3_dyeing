import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import {writeFileSync,readFileSync} from 'node:fs'
const version=JSON.parse(readFileSync(new URL('./package.json',import.meta.url),'utf8')).version+'.'+Date.now()
writeFileSync(new URL('../backend/application/build_version.py',import.meta.url),`BUILD_VERSION = '${version}'\n`)
export default defineConfig({
  define:{__BUILD_VERSION__:JSON.stringify(version)},
  plugins: [vue()],
  build: {assetsDir: 'static/assets'},
  server: {proxy: {'/api': 'http://127.0.0.1:8000', '/media': 'http://127.0.0.1:8000', '/captcha': 'http://127.0.0.1:8000'}}
})
