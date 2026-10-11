<script setup lang="ts">
import {ref,watch} from 'vue'
import {api} from '../../api'
import FieldInput from '../../components/FieldInput.vue'
const props=defineProps<{modelValue:any;field:any;form:Record<string,any>;row:Record<string,any>}>()
const emit=defineEmits(['update:modelValue'])
const rows=ref<any[]>([]),loading=ref(false)
const values=ref<any[]>([]),selected=ref<boolean[]>([])
function emitValues(){emit('update:modelValue',values.value.filter((row,index)=>!props.field.selectable||selected.value[index]))}
watch(()=>props.field.source_from_row?props.row[props.field.source_key]:props.form[props.field.source_key],async value=>{
  rows.value=[];emit('update:modelValue',[])
  if(value===null||value===undefined)return
  loading.value=true
  try{
    let page=1,more=true
    while(more){
      const result=await api(`/api/system/${props.field.entity}/`,{params:{[props.field.parent_key]:value,page,limit:200}})
      rows.value.push(...result.data);more=Boolean(result.is_next);page++
    }
    values.value=rows.value.map(row=>({[props.field.identity_key]:row.id,...props.field.defaults}));selected.value=rows.value.map(()=>!props.field.selectable);emitValues()
  }finally{loading.value=false}
},{immediate:true})
function update(index:number,key:string,value:any){values.value[index][key]=value;emitValues()}
function payloadIndex(index:number){return props.field.selectable?selected.value.slice(0,index).filter(Boolean).length:index}
</script>
<template>
  <div v-loading="loading" class="stage-input"><el-empty v-if="!rows.length" :description="field.empty_text??'当前来源没有可采用明细'"/>
    <div v-for="(row,index) in rows" :key="row.id" class="stage-row"><strong>{{row[field.label_key]}}</strong>
      <el-checkbox v-if="field.selectable" v-model="selected[index]" @change="emitValues">采用本行</el-checkbox>
      <template v-if="!field.selectable||selected[index]">
        <el-form-item v-for="column in field.columns" :key="column.key" :label="column.title" :prop="`${field.key}.${payloadIndex(index)}.${column.key}`" :rules="[{required:column.required,message:'请填写'+column.title}]">
          <FieldInput :model-value="values[index][column.key]" :field="column" @update:model-value="value=>update(index,column.key,value)"/>
        </el-form-item>
      </template>
    </div>
  </div>
</template>
<style scoped>.stage-input{width:100%}.stage-row{border:1px solid var(--el-border-color);padding:12px;margin:8px 0}.stage-row>strong{display:block;margin-bottom:12px}</style>
