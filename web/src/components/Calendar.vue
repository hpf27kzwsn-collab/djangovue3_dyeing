<script setup lang="ts">
import {computed,ref,watch,nextTick} from 'vue'
import {useFormItem} from 'element-plus'
const {formItem}=useFormItem()
import Holidays from 'date-holidays'
import {Solar} from 'lunar-javascript'
const props=withDefaults(defineProps<{modelValue?:Date|Date[]|null;multiple?:boolean;range?:[Date,Date];pageTurn?:boolean;crossPage?:boolean;watermark?:boolean;watermarkPosition?:string;showPageTurn?:boolean;selectable?:boolean;validDate?:(date:Date)=>boolean}>(),{
 multiple:false,pageTurn:true,crossPage:false,watermark:true,watermarkPosition:'bottom-right',showPageTurn:true,selectable:true,validDate:()=>true,
})
const emit=defineEmits(['update:modelValue','change'])
const month=ref(new Date()),showHoliday=ref(true),showLunarHoliday=ref(true),showJieQi=ref(true),showDetailedHoliday=ref(false)
const holidays=new Holidays('CN'),key=(date:Date)=>`${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`
const selected=computed<Date[]>(()=>Array.isArray(props.modelValue)?props.modelValue:props.modelValue?[props.modelValue]:[])
const bounds=computed(()=>props.range||[new Date(month.value.getFullYear(),month.value.getMonth(),1),new Date(month.value.getFullYear(),month.value.getMonth()+1,0)])
const holidayMap=computed(()=>{
 const map:Record<string,string>={};for(let year=bounds.value[0].getFullYear();year<=bounds.value[1].getFullYear();year++)for(const holiday of holidays.getHolidays(year))map[holiday.date.split(' ')[0]]=holiday.name
 return map
})
const weeks=computed(()=>{
 const first=new Date(bounds.value[0]);first.setDate(first.getDate()-first.getDay());const last=new Date(bounds.value[1]);last.setDate(last.getDate()+6-last.getDay())
 const cells=[];for(let date=new Date(first);date<=last;date.setDate(date.getDate()+1)){
  const value=new Date(date),solar=Solar.fromDate(value),lunar=solar.getLunar()
  const holiday=showHoliday.value?((showLunarHoliday.value?lunar.getFestivals()[0]:'')||(showJieQi.value?lunar.getJieQi():'')||(showDetailedHoliday.value?solar.getFestivals()[0]:holidayMap.value[key(value)])):''
  cells.push({date:value,key:key(value),holiday,selected:selected.value.some(x=>key(x)===key(value)),disabled:!props.validDate(value)||!!props.range&&(key(value)<key(props.range[0])||key(value)>key(props.range[1])),currentMonth:value.getMonth()===month.value.getMonth(),today:key(value)===key(new Date())})
 }
 const result=[];for(let index=0;index<cells.length;index+=7)result.push(cells.slice(index,index+7));return result
})
function update(value:Date|Date[]|null){emit('update:modelValue',value);emit('change',value);nextTick(()=>formItem?.validate('change',()=>{}))}
function choose(date:Date){if(!props.selectable)return;if(props.multiple)update(selected.value.some(x=>key(x)===key(date))?selected.value.filter(x=>key(x)!==key(date)):[...selected.value,date]);else update(date)}
function clear(){update(props.multiple?[]:null)}
function remove(date:Date){update(props.multiple?selected.value.filter(x=>key(x)!==key(date)):null)}
function turn(year:number,months:number){month.value=new Date(month.value.getFullYear()+year,month.value.getMonth()+months,1)}
function reset(){month.value=new Date();clear()}
watch(month,(value,previous)=>{if(!props.crossPage&&(value.getFullYear()!==previous.getFullYear()||value.getMonth()!==previous.getMonth()))clear()})
defineExpose({data:computed(()=>props.modelValue),onDataChange:update,reset,clear,showHoliday,showDetailedHoliday,showJieQi,showLunarHoliday})
</script>
<template><div class="platform-calendar" @focusout="formItem?.validate('blur',()=>{})"><div v-if="selectable&&selected.length" class="calendar-selection"><span>已选择：</span><el-tag v-for="date in selected" :key="key(date)" closable @close="remove(date)">{{key(date)}}</el-tag><el-button text @click="clear">清空</el-button></div>
 <div class="calendar-controls"><span>今天：{{key(new Date())}}</span><strong>{{month.getFullYear()}} 年 {{month.getMonth()+1}} 月</strong><div v-if="showPageTurn&&!range"><el-popover trigger="click" width="220"><template #reference><el-button>节假日设置</el-button></template><el-switch v-model="showHoliday" active-text="显示节日"/><el-checkbox v-model="showLunarHoliday">农历节日</el-checkbox><el-checkbox v-model="showJieQi">节气</el-checkbox><el-checkbox v-model="showDetailedHoliday">更多节日</el-checkbox></el-popover><el-button-group v-if="pageTurn"><el-button @click="turn(-1,0)">上年</el-button><el-button @click="turn(0,-1)">上月</el-button><el-button @click="month=new Date()">今天</el-button><el-button @click="turn(0,1)">下月</el-button><el-button @click="turn(1,0)">下年</el-button></el-button-group></div></div>
 <div class="calendar-grid"><div v-if="watermark" class="calendar-watermark" :class="watermarkPosition">{{month.getFullYear()}}-{{String(month.getMonth()+1).padStart(2,'0')}}</div><table><thead><tr><th v-for="day in ['日','一','二','三','四','五','六']" :key="day">{{day}}</th></tr></thead><tbody><tr v-for="(week,index) in weeks" :key="index"><td v-for="cell in week" :key="cell.key"><button :disabled="cell.disabled" :class="{selected:cell.selected,today:cell.today,adjacent:!cell.currentMonth}" @click="choose(cell.date)"><div class="calendar-cell-title">{{cell.date.getDate()}}<span v-if="cell.selected">✓</span></div><slot name="cell-body" v-bind="cell"/><div class="calendar-cell-footer">{{cell.holiday}}<span v-if="cell.today">今天</span></div></button></td></tr></tbody></table></div>
</div></template>
<style scoped>
.calendar-selection,.calendar-controls{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:14px}.calendar-controls{justify-content:space-between}.calendar-grid{position:relative}.calendar-grid table{width:100%;border-collapse:collapse;position:relative}.calendar-grid th{height:38px}.calendar-grid td{border:1px solid var(--el-border-color-light);width:14.28%;padding:0}.calendar-grid td button{position:relative;width:100%;height:100px;border:0;background:transparent;color:inherit;text-align:left;cursor:pointer;display:flex;flex-direction:column;justify-content:space-between;padding:12px}.calendar-grid td button:hover{background:var(--el-color-primary-light-9)}.calendar-grid button.selected{background:var(--el-color-primary-light-8);color:var(--el-color-primary)}.calendar-grid button.today{box-shadow:inset 0 0 0 1px var(--el-color-primary)}.calendar-grid button.adjacent{color:var(--el-text-color-placeholder)}.calendar-grid button:disabled{opacity:.4;cursor:default}.calendar-cell-title,.calendar-cell-footer{display:flex;justify-content:space-between;gap:5px}.calendar-cell-footer{font-size:12px;color:var(--el-color-danger)}.calendar-watermark{position:absolute;pointer-events:none;opacity:.08;font-size:85px;bottom:8%;right:8%}.calendar-watermark.top-left{top:8%;left:8%;bottom:auto;right:auto}.calendar-watermark.top-right{top:8%;bottom:auto}.calendar-watermark.bottom-left{left:8%;right:auto}.calendar-watermark.center{top:45%;left:25%;bottom:auto;right:auto}.calendar-watermark.center-left{top:45%;left:5%;bottom:auto;right:auto}.calendar-watermark.center-right{top:45%;bottom:auto}.calendar-watermark.center-top{top:8%;left:25%;bottom:auto;right:auto}.calendar-watermark.center-bottom{left:25%;right:auto}
</style>

<style scoped>@media(max-width:768px){.calendar-grid td button{height:86px;padding:4px}.calendar-cell-footer{font-size:10px;display:block;overflow-wrap:anywhere}.calendar-watermark{font-size:42px}.calendar-controls .el-button{padding:8px}.calendar-controls>div{max-width:100%;overflow:auto}}</style>
