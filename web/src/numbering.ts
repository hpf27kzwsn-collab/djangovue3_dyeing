import {ref} from 'vue'
export const numberingUpdated=ref({entity:'',version:0})
export function notifyNumbering(model:string){numberingUpdated.value={entity:model.toLowerCase().replace('.','_'),version:numberingUpdated.value.version+1}}
