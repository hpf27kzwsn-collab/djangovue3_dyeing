// 列表表单与整单编辑共用原入口规则；计算和保存仍由后端服务执行。
export function entryChoices(meta:any){return meta.workflow?.entries??[]}
export function formEntry(meta:any,selected?:string,parentEntry?:string){
  const choices=entryChoices(meta)
  if(selected)return selected
  if(parentEntry){
    const inherited=choices.filter((e:any)=>e.value===parentEntry||e.master_entry===parentEntry)
    if(inherited.length===1)return inherited[0].value
    return inherited.some((e:any)=>e.value===meta.workflow.default_entry)?meta.workflow.default_entry:undefined
  }
  return meta.workflow?.default_entry??(choices.length===1?choices[0].value:undefined)
}
export function originalValues(meta:any,row:any){
  return Object.fromEntries(entryChoices(meta).flatMap((e:any)=>Object.entries(e.field_rules??{}).filter(([key])=>row[key]!==undefined).map(([key,rule]:[string,any])=>[rule.old_name,row[key]])))
}
export function entryRule(meta:any,entry:string|undefined,key:string){return entryChoices(meta).find((e:any)=>e.value===entry)?.field_rules?.[key]}
export function formField(meta:any,field:any,entry:string|undefined,row:any,parentContext:Record<string,any>={}){
  const rule=entryRule(meta,entry,field.key)
  return {...field,...(rule?.title?{title:rule.title}:{}),...(rule&&['Lookup','Lookup_NoCheck','DBCombo','DBCombo_Edit'].includes(rule.editor_kind)&&rule.editor_id?{originalLookup:{entity:meta.entity,entry,field:rule.old_name,context:{...parentContext,...originalValues(meta,row)}}}:{})}
}
export function createValues(meta:any,row:any,entry:string|undefined,useDefaults:boolean){
  const data={...row}
  if(entry){
    data._entry=entry
    if(useDefaults)for(const key of entryChoices(meta).find((e:any)=>e.value===entry).generated_fields)if(data[key]===null||data[key]===''||data[key]===undefined)delete data[key]
  }
  return data
}
export function formRequired(meta:any,field:any,entry:string|undefined,useDefaults:boolean){
  const rule=entryRule(meta,entry,field.key),config=entryChoices(meta).find((e:any)=>e.value===entry)
  return (field.required||rule?.required===true)&&rule?.readonly!==true&&!(useDefaults&&config?.generated_fields.includes(field.key))
}
