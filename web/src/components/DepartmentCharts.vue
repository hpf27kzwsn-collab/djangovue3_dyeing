<script setup lang="ts">
import {ref,onMounted,onBeforeUnmount,watch} from 'vue'
import {init,use,type EChartsType} from 'echarts/core'
import {BarChart,PieChart} from 'echarts/charts'
import {GridComponent,TitleComponent,TooltipComponent,LegendComponent} from 'echarts/components'
import {SVGRenderer} from 'echarts/renderers'
use([BarChart,PieChart,GridComponent,TitleComponent,TooltipComponent,LegendComponent,SVGRenderer])
const props=defineProps<{info:any}>(),counts=ref<HTMLElement>(),gender=ref<HTMLElement>()
let bars:EChartsType,pie:EChartsType,observer:ResizeObserver
function draw(){
 bars.setOption({title:{text:'部门人数',textStyle:{fontSize:14}},tooltip:{trigger:'axis'},grid:{left:40,right:15,bottom:65},xAxis:{type:'category',axisLabel:{rotate:25},data:props.info.children.map((row:any)=>row.name)},yAxis:{type:'value',minInterval:1},series:[{type:'bar',label:{show:true,position:'top'},data:props.info.children.map((row:any)=>row.count)}]})
 pie.setOption({title:{text:'用户性别',textStyle:{fontSize:14}},tooltip:{trigger:'item'},legend:{bottom:0},series:[{type:'pie',radius:['30%','65%'],data:[{name:'男',value:props.info.gender['1']},{name:'女',value:props.info.gender['2']},{name:'未知',value:props.info.gender['0']}]}]})
}
onMounted(()=>{bars=init(counts.value!,undefined,{renderer:'svg'});pie=init(gender.value!,undefined,{renderer:'svg'});draw();observer=new ResizeObserver(()=>{bars.resize();pie.resize()});observer.observe(counts.value!);observer.observe(gender.value!)})
watch(()=>props.info,()=>{if(bars)draw()},{deep:true})
onBeforeUnmount(()=>{observer.disconnect();bars.dispose();pie.dispose()})
</script>
<template><div class="department-charts"><div class="charts"><div ref="counts"/><div ref="gender"/></div></div></template>
<style scoped>.department-charts{width:100%;min-width:0}.charts{display:grid;grid-template-columns:1fr 1fr;gap:16px}.charts>div{height:270px;min-width:0}@media(max-width:768px){.charts{grid-template-columns:1fr}}</style>
