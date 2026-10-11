<script setup lang="ts">
import {ref,onMounted,onBeforeUnmount,nextTick} from 'vue'
import {init,use,type EChartsType} from 'echarts/core'
import {LineChart} from 'echarts/charts'
import {GridComponent,TitleComponent,TooltipComponent} from 'echarts/components'
import {SVGRenderer} from 'echarts/renderers'
use([LineChart,GridComponent,TitleComponent,TooltipComponent,SVGRenderer])
const element=ref<HTMLElement>(),visible=ref(true)
let chart:EChartsType,observer:ResizeObserver
onMounted(()=>{
  chart=init(element.value!,undefined,{renderer:'svg'})
  chart.setOption({title:{text:'2021年各月份销售量（原项目示例数据）',left:'center',textStyle:{fontSize:14}},tooltip:{trigger:'axis'},grid:{left:45,right:20,top:55,bottom:35},xAxis:{type:'category',data:['一月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月']},yAxis:{type:'value'},series:[{type:'line',smooth:true,label:{show:true,position:'top'},data:[606,542,985,687,501,787,339,706,383,684,669,737]}]})
  observer=new ResizeObserver(()=>chart.resize());observer.observe(element.value!)
})
onBeforeUnmount(()=>{observer.disconnect();chart.dispose()})
async function toggle(){visible.value=!visible.value;await nextTick();if(visible.value)chart.resize()}
</script>
<template><div class="chart-panel"><el-button text @click="toggle">{{visible?'隐藏图表':'显示图表'}}</el-button><el-button text @click="chart.resize()">刷新图表尺寸</el-button><div v-show="visible" ref="element" class="chart"/></div></template>
<style scoped>.chart-panel{min-width:0;width:100%;margin-bottom:16px}.chart{width:100%;height:300px}@media(max-width:600px){.chart{height:260px}}</style>
