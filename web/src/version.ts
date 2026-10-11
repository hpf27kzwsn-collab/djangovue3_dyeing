import {h} from 'vue'
import {ElNotification,ElButton} from 'element-plus'
import {api} from './api'
let notified=false
export async function checkVersion(){
 const config=(await api('/api/config/')).data
 if(config.version!==__BUILD_VERSION__&&!notified){notified=true;ElNotification({title:'平台已更新',duration:0,message:h(ElButton,{onClick:()=>window.location.reload()},()=> '刷新页面')})}
}
