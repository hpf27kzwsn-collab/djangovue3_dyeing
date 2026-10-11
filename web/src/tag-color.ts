export const semanticColors=['primary','success','info','warning','danger'] as const
export function tagColor(color?:string){
  return semanticColors.includes(color as any)?{type:color}:{color:color||undefined,style:color?{color:'white',borderColor:color}:undefined}
}
export function fileSize(size:number){
  const units=['B','KB','MB','GB','TB'],index=size>0?Math.min(Math.floor(Math.log(size)/Math.log(1024)),units.length-1):0
  return (size/1024**index).toFixed(index===0?0:1)+' '+units[index]
}
