<script setup lang="ts">
import {ref,onMounted,onBeforeUnmount,watch,nextTick,computed} from 'vue'
import MenuIcon from './MenuIcon.vue'
const props=withDefaults(defineProps<{mode?:''|'closeable'|'link';text?:string;color?:string;background?:string;size?:number|string;height?:number;delay?:number;speed?:number;scrollable?:boolean;leftIcon?:string;rightIcon?:string}>(),{mode:'',text:'',color:'var(--el-color-warning)',background:'var(--el-color-warning-light-9)',size:14,height:40,delay:1,speed:100,scrollable:false,leftIcon:'',rightIcon:''})
const emit=defineEmits(['close','link']),closed=ref(false),repeat=ref(false),box=ref<HTMLElement>(),textElement=ref<HTMLElement>(),width=ref(0),textWidth=ref(0)
let observer:ResizeObserver
function measure(){width.value=box.value!.clientWidth;if(!props.scrollable)textWidth.value=textElement.value!.offsetWidth}
onMounted(()=>{observer=new ResizeObserver(measure);observer.observe(box.value!);measure()})
onBeforeUnmount(()=>observer.disconnect())
watch(()=>[props.text,props.scrollable],async()=>{repeat.value=false;await nextTick();measure()})
const animation=computed(()=>({'--start':(repeat.value?width.value:0)+'px','--end':-textWidth.value+'px',animationDuration:(textWidth.value+(repeat.value?width.value:0))/props.speed+'s',animationDelay:(repeat.value?0:props.delay)+'s',animationIterationCount:repeat.value?'infinite':'1'}))
function action(){if(props.mode==='closeable'){closed.value=true;emit('close')}else if(props.mode==='link')emit('link')}
</script>
<template><div v-show="!closed" class="notice-bar" :style="{height:height+'px',background,color,fontSize:size+'px'}"><el-icon v-if="leftIcon"><MenuIcon :name="leftIcon"/></el-icon><div ref="box" class="notice-box"><div v-if="!scrollable" ref="textElement" :key="String(repeat)+text" class="notice-text" :style="animation" @animationend="repeat=true">{{text}}</div><slot v-else/></div><button v-if="rightIcon" :aria-label="mode==='closeable'?'关闭公告':'打开公告'" @click="action"><el-icon><MenuIcon :name="rightIcon"/></el-icon></button></div></template>
<style scoped>.notice-bar{display:flex;align-items:center;gap:10px;padding:0 15px;border-radius:4px;width:100%;box-sizing:border-box}.notice-box{flex:1;min-width:0;overflow:hidden;height:100%;display:flex;align-items:center}.notice-text{white-space:nowrap;flex:none;animation-name:notice-scroll;animation-timing-function:linear;animation-fill-mode:backwards}.notice-bar button{border:0;background:none;color:inherit;cursor:pointer;display:flex;align-items:center}@keyframes notice-scroll{from{transform:translateX(var(--start))}to{transform:translateX(var(--end))}}</style>
