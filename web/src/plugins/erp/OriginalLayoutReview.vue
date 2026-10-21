<script setup lang="ts">
import {computed} from 'vue'
const props=defineProps<{layout:any}>()
const dpi=computed(()=>Number(props.layout.page.Dpi??100))
const width=computed(()=>Number(props.layout.page.PageWidth))
const scale=computed(()=>25.4/dpi.value)
function leaves(nodes:any[]):any[]{return nodes.flatMap(n=>[n,...leaves(n.children)])}
function font(control:any){
  const value=control.style.Font??'宋体, 9pt',size=Number(value.match(/([\d.]+)pt/)?.[1]??9)
  return {family:value.split(',')[0],size:size*dpi.value/72,weight:value.includes('Bold')?'bold':'normal'}
}
function label(c:any){return c.bindings.length?c.bindings.map((b:any)=>'['+b.DataMember+']').join(' · '):c.text}
function x(c:any){const align=c.style.TextAlignment??'';return c.x+(align.endsWith('Right')?c.width-2:align.endsWith('Center')?c.width/2:2)}
function anchor(c:any){const align=c.style.TextAlignment??'';return align.endsWith('Right')?'end':align.endsWith('Center')?'middle':'start'}
function y(c:any){const align=c.style.TextAlignment??'';return c.y+(align.startsWith('Bottom')?c.height-2:align.startsWith('Middle')?c.height/2:font(c).size)}
const supported=new Set(['XRTable','XRTableCell','XRLabel','XRLine'])
</script>
<template>
  <section class="layout-review">
    <p>{{layout.report_id}} · {{layout.title}} · 原纸张 {{(width*scale).toFixed(2)}} × {{(Number(layout.page.PageHeight)*scale).toFixed(2)}} 毫米</p>
    <el-alert title="原版式核对预览：显示原位置、字体、表格及字段绑定；方括号是待取数的字段，不是业务数据。" type="info" :closable="false"/>
    <p>各打印区域分开展示。脚本、汇总、分页、子报表和特殊控件仍须逐项核实；此预览不代表原单据已能完整打印。</p>
    <div v-for="(band,i) in layout.bands" :key="i" class="band">
      <div>{{band.path.join(' / ')}} · {{band.kind}} · 原高度 {{(band.height*scale).toFixed(2)}} 毫米</div>
      <svg v-if="band.height>0" :viewBox="`0 0 ${width} ${band.height}`" :style="{width:width*scale+'mm',height:band.height*scale+'mm'}" xmlns="http://www.w3.org/2000/svg" role="img" :aria-label="band.name">
        <g v-for="(c,j) in leaves(band.controls)" :key="j">
          <title>{{c.name}} · {{c.kind}} · {{label(c)}}</title>
          <rect v-if="c.kind!=='XRLine'" :x="c.x" :y="c.y" :width="c.width" :height="c.height" :fill="supported.has(c.kind)?'white':'#fff3d6'" stroke="#d4d4d4" :stroke-width="0.4"/>
          <line v-for="edge in ['Top','Bottom','Left','Right']" v-show="c.style.Borders==='All'||String(c.style.Borders).includes(edge)" :key="edge" :x1="c.x+(edge==='Right'?c.width:0)" :y1="c.y+(edge==='Bottom'?c.height:0)" :x2="c.x+(edge==='Left'?0:c.width)" :y2="c.y+(edge==='Top'?0:c.height)" stroke="black" :stroke-width="c.style.BorderWidth??1"/>
          <line v-if="c.kind==='XRLine'" :x1="c.x" :y1="c.y" :x2="c.x+c.width" :y2="c.y" stroke="black"/>
          <text v-else-if="c.kind!=='XRTable'" :x="x(c)" :y="y(c)" :text-anchor="anchor(c)" :dominant-baseline="String(c.style.TextAlignment).startsWith('Middle')?'middle':'auto'" :font-family="font(c).family" :font-size="font(c).size" :font-weight="font(c).weight">{{supported.has(c.kind)?label(c):c.kind+' · '+label(c)}}</text>
        </g>
      </svg>
    </div>
    <el-collapse><el-collapse-item :title="'尚需处理的控件及脚本（'+layout.issues.length+'）'"><el-table :data="layout.issues"><el-table-column prop="control" label="原控件"/><el-table-column prop="kind" label="类型"/><el-table-column prop="reason" label="差异"/></el-table></el-collapse-item></el-collapse>
    <p v-if="layout.control_references.length">原文件含 {{layout.control_references.length}} 处控制字符数字实体，解析副本已恢复属性值，下载文件仍保留原始字节。</p>
  </section>
</template>
<style scoped>.layout-review{overflow:auto}.band{margin-top:18px}.band>div{padding:6px;background:#eef2f6}svg{display:block;background:white;border:1px solid #bbb}</style>
