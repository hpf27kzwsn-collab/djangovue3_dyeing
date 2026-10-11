export function resourceQuery(query:Record<string,any>){
  return Object.fromEntries(Object.entries(query).filter(([,value])=>!Array.isArray(value)||value.length>0)
    .map(([key,value])=>Array.isArray(value)?[key.endsWith('__in')?key:key+'__in',value.join(',')]:[key,value]))
}
