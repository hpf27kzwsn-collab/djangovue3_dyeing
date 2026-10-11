<script setup lang="ts">
import {ref,watch} from 'vue'
import {api} from '../../api'
import FieldInput from '../../components/FieldInput.vue'
const props=defineProps<{modelValue:any;field:any;form:Record<string,any>}>()
const emit=defineEmits(['update:modelValue'])
const rows=ref<any[]>([]),loading=ref(false)
watch(()=>props.form[props.field.source_key],async value=>{
  rows.value=[];emit('update:modelValue',[])
  if(value===null||value===undefined)return
  loading.value=true
  try{
    let page=1,more=true
    while(more){
      const result=await api(`/api/system/${props.field.entity}/`,{params:{[props.field.parent_key]:value,page,limit:200}})
      rows.value.push(...result.data);more=Boolean(result.is_next);page++
    }
    emit('update:modelValue',rows.value.map(row=>({[props.field.identity_key]:row.id,...props.field.defaults})))
  }finally{loading.value=false}
},{immediate:true})
function update(index:number,key:string,value:any){emit('update:modelValue',props.modelValue.map((row:any,i:number)=>i===index?{...row,[key]:value}:row))}
</script>
<template>
  <div v-loading="loading" class="stage-input"><el-empty v-if="!rows.length" description="请先选择配方版本"/>
    <div v-for="(row,index) in rows" :key="row.id" class="stage-row"><strong>阶段 {{row[field.label_key]}}</strong>
      <el-form-item v-for="column in field.columns" :key="column.key" :label="column.title" :prop="`${field.key}.${index}.${column.key}`" :rules="[{required:column.required,message:'请填写'+column.title}]">
        <FieldInput :model-value="modelValue[index][column.key]" :field="column" @update:model-value="value=>update(index,column.key,value)"/>
      </el-form-item>
    </div>
  </div>
</template>
<style scoped>.stage-input{width:100%}.stage-row{border:1px solid var(--el-border-color);padding:12px;margin:8px 0}.stage-row>strong{display:block;margin-bottom:12px}</style>
