import type { App } from 'vue'
import type { Router } from 'vue-router'
const plugins = import.meta.glob<{install: (app: App, router: Router) => void}>('./*/index.ts', {eager: true})
export function installPlugins(app: App, router: Router) {
  for (const plugin of Object.values(plugins)) plugin.install(app, router)
}
