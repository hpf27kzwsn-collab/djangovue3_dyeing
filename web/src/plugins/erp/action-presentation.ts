export type BusinessAction={key:string;title:string;display_title:string;placement:string;topic:string;permission:string;detail?:boolean;states?:any[];hide_when?:string[];effect_required?:string;inputs:any[];audit:string}

export function availableActions(actions:BusinessAction[],state:any,row:any,can:(permission:string)=>boolean,maintenance=false){
  return actions.filter(action=>action.placement!=='deferred'&&can(action.permission)
    &&(maintenance||action.placement==='business')
    &&(!action.effect_required||row.action_effects?.[action.effect_required]==='applied')
    &&(action.detail===false||!row.transfer_retained&&action.states!.includes(state)&&!(action.hide_when??[]).some(key=>row[key])))
}

export function actionTopics(actions:BusinessAction[]){
  return [...new Set(actions.map(action=>action.topic))].map(title=>({title,actions:actions.filter(action=>action.topic===title)}))
}
