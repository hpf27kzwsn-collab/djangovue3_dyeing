export function selectButton(grants:Record<number,any>,id:number,checked:boolean,preset:{data_range:number;dept:number[]}){
  if(checked)grants[id] ||= {id,data_range:preset.data_range,dept:[...preset.dept]}
  else delete grants[id]
}
