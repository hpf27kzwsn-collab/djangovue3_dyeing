<script setup lang="ts">
import {defineAsyncComponent,computed,ref,watch} from 'vue'
import {toTree} from '../tree'
import {semanticColors} from '../tag-color'
const RichText=defineAsyncComponent(()=>import('./RichText.vue'))
const AvatarCrop=defineAsyncComponent(()=>import('./AvatarCrop.vue'))
const FilePicker=defineAsyncComponent(()=>import('./FilePicker.vue'))
const AssociationSetting=defineAsyncComponent(()=>import('./AssociationSetting.vue'))
const IconPicker=defineAsyncComponent(()=>import('./IconPicker.vue'))
const ArrayInput=defineAsyncComponent(()=>import('./ArrayInput.vue'))
const TableSelect=defineAsyncComponent(()=>import('./TableSelect.vue'))
const ApiPathInput=defineAsyncComponent(()=>import('./ApiPathInput.vue'))
const OriginalLookupField=defineAsyncComponent(()=>import('../plugins/erp/OriginalLookupField.vue'))
const props = defineProps<{modelValue: any; field: {kind: string; options: any[]; key: string;nullable?:boolean;placeholder?:string;originalLookup?:{entity:string;entry:string;field:string;context:Record<string,any>};remote?:{entity:string;pk:string;label:string;columns?:any[];params?:Record<string,any>}}}>()
const departmentTree=computed(()=>toTree(props.field.options,'value','parent'))
const emit = defineEmits(['update:modelValue'])
const jsonText=ref('')
watch(()=>props.modelValue,value=>{if(props.field.kind==='json')jsonText.value=JSON.stringify(value,null,2)},{immediate:true})
async function upload(event: Event) {
  const file = (event.target as HTMLInputElement).files![0]
  if (props.field.kind === 'file') emit('update:modelValue', file)
}
function json(value: string) {emit('update:modelValue', JSON.parse(value))}
</script>
<template>
  <OriginalLookupField v-if="field.originalLookup" :model-value="modelValue" v-bind="field.originalLookup" @update:model-value="(value:any)=>emit('update:modelValue',value)"/>
  <input v-else-if="field.kind === 'file'" type="file" @change="upload">
  <AvatarCrop v-else-if="field.kind === 'avatar'" :model-value="modelValue" @update:model-value="(value:any)=>emit('update:modelValue',value)"/>
  <RichText v-else-if="field.kind === 'richtext'" :model-value="modelValue || ''" @update:model-value="(value:any)=>emit('update:modelValue',value)"/>
  <AssociationSetting v-else-if="field.kind==='association'" :model-value="modelValue" @update:model-value="(value:any)=>emit('update:modelValue',value)"/>
  <ApiPathInput v-else-if="field.kind==='api-path'" :model-value="modelValue" @update:model-value="(value:any)=>emit('update:modelValue',value)"/>
  <IconPicker v-else-if="field.kind==='icon'" :model-value="modelValue" @update:model-value="(value:any)=>emit('update:modelValue',value)"/>
  <div v-else-if="field.kind==='color'" class="color-input"><el-select :model-value="modelValue" filterable allow-create @update:model-value="emit('update:modelValue',$event)"><el-option v-for="color in semanticColors" :key="color" :value="color" :label="color"/></el-select><el-color-picker :model-value="modelValue" @update:model-value="emit('update:modelValue',$event)"/><el-input :model-value="modelValue" @update:model-value="emit('update:modelValue',$event)"/></div>
  <FilePicker v-else-if="['image','images','attachment'].includes(field.kind)" :model-value="modelValue" :multiple="field.kind==='images'" :images="field.kind!=='attachment'" @update:model-value="(value:any)=>emit('update:modelValue',value)"/>
  <FilePicker v-else-if="field.kind==='attachment-id'" :model-value="modelValue" value-key="id" :show-network="false" @update:model-value="(value:any)=>emit('update:modelValue',value===''?null:value)"/>
  <ArrayInput v-else-if="field.kind==='array'" :model-value="modelValue" @update:model-value="(value:any)=>emit('update:modelValue',value)"/>
  <el-checkbox-group v-else-if="field.kind==='checkbox'" :model-value="modelValue||[]" @update:model-value="(value:any)=>emit('update:modelValue',value)"><el-checkbox v-for="item in field.options" :key="item.value" :value="item.value">{{item.label}}</el-checkbox></el-checkbox-group>
  <el-radio-group v-else-if="field.kind==='radio'" :model-value="modelValue" @update:model-value="(value:any)=>emit('update:modelValue',value)"><el-radio v-for="item in field.options" :key="item.value" :value="item.value">{{item.label}}</el-radio></el-radio-group>
  <el-input v-else-if="field.kind === 'json'" v-model="jsonText" type="textarea" :rows="5" @change="json"/>
  <TableSelect v-else-if="field.remote&&['select','multi'].includes(field.kind)" :model-value="modelValue" v-bind="field.remote" :multiple="field.kind==='multi'" @update:model-value="(value:any)=>emit('update:modelValue',value)"/>
  <el-tree-select v-else-if="['select','multi'].includes(field.kind)&&['dept','parent','dept_belong','target_dept'].includes(field.key)&&field.options.some(x=>'parent' in x)" :data="departmentTree" node-key="value" :model-value="modelValue" :multiple="field.kind==='multi'" check-strictly filterable clearable @update:model-value="(value:any)=>emit('update:modelValue',value)"/>
  <el-select v-else-if="['multi', 'select'].includes(field.kind)" :model-value="modelValue" :multiple="field.kind === 'multi'" filterable clearable @clear="emit('update:modelValue',field.kind==='multi'?[]:null)" @update:model-value="(value: any) => emit('update:modelValue', value)">
    <el-option v-for="item in field.options" :key="item.value" :label="item.label" :value="item.value" :disabled="item.disabled"/>
  </el-select>
  <el-select v-else-if="field.kind==='autocomplete'" :model-value="modelValue" filterable allow-create @update:model-value="emit('update:modelValue',$event)"><el-option v-for="item in field.options" :key="item.value" :label="item.label" :value="item.value"/></el-select>
  <el-select v-else-if="field.kind==='boolean'&&field.nullable" :model-value="modelValue" clearable placeholder="未填写" @clear="emit('update:modelValue',null)" @update:model-value="(value:any)=>emit('update:modelValue',value)"><el-option label="是" :value="true"/><el-option label="否" :value="false"/></el-select>
  <el-switch v-else-if="field.kind === 'boolean'" :model-value="modelValue" @update:model-value="(value: any) => emit('update:modelValue', value)"/>
  <el-input-number v-else-if="field.kind === 'number'" :model-value="modelValue" @update:model-value="(value: any) => emit('update:modelValue', value)"/>
  <el-input v-else-if="field.kind === 'decimal'" :model-value="modelValue" inputmode="decimal" @update:model-value="(value:string)=>emit('update:modelValue',value===''&&field.nullable?null:value)"/>
  <el-date-picker v-else-if="field.kind === 'datetime'" :model-value="modelValue" type="datetime" value-format="YYYY-MM-DD HH:mm:ss" @update:model-value="(value: any) => emit('update:modelValue', value)"/>
  <el-date-picker v-else-if="field.kind === 'date'" :model-value="modelValue" type="date" value-format="YYYY-MM-DD" @update:model-value="(value: any) => emit('update:modelValue', value)"/>
  <el-time-picker v-else-if="field.kind === 'time'" :model-value="modelValue" value-format="HH:mm:ss" @update:model-value="(value: any) => emit('update:modelValue', value)"/>
  <el-input v-else :model-value="modelValue" :placeholder="field.placeholder" :type="field.kind === 'textarea' ? 'textarea' : field.kind === 'password' ? 'password' : 'text'" :rows="4" @update:model-value="(value: any) => emit('update:modelValue', value)"/>
</template>
