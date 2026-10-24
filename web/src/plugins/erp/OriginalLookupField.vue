<script setup lang="ts">
import {ref} from 'vue'
import {api} from '../../api'
const props=defineProps<{modelValue:any;entity:string;entry:string;field:string;context?:Record<string,any>;disabled?:boolean}>()
const emit=defineEmits(['update:modelValue'])
const visible=ref(false),filter=ref(''),result=ref<any>(),busy=ref(false)
async function load(){busy.value=true;try{result.value=(await api(`/api/system/${props.entity}/lookup_options/`,{method:'POST',data:{entry:props.entry,field:props.field,context:props.context,filter_text:filter.value}})).data}finally{busy.value=false}}
async function open(){visible.value=true;result.value=undefined;await load()}
function choose(row:any){emit('update:modelValue',row.id);visible.value=false}
</script>
<template>
  <div class="original-lookup">
    <el-input :model-value="modelValue" :disabled="disabled" @update:model-value="emit('update:modelValue',$event)"/>
    <el-button :disabled="disabled" @click="open">选资料</el-button>
    <el-button :disabled="disabled" @click="emit('update:modelValue',null)">空值</el-button>
    <el-dialog v-model="visible" title="选择资料" width="80%" append-to-body>
      <el-input v-model="filter" placeholder="代码或名称" @keyup.enter="load"><template #append><el-button :loading="busy" @click="load">查询</el-button></template></el-input>
      <template v-if="result">
        <p v-if="!result.implemented">此项资料选项尚未接通，可在表单中手工填写业务编码。</p>
        <el-table :data="result.rows" height="50vh" border>
          <el-table-column type="index" label="行" width="60"/>
          <el-table-column prop="id" label="代码"/><el-table-column prop="text" label="名称"/>
          <el-table-column v-for="key in Object.keys(result.rows[0]??{}).filter(k=>!['id','text'].includes(k))" :key="key" :prop="key" :label="result.columns.find((c:any)=>c.FieldName===key)?.Caption||key"/>
          <el-table-column label="选择"><template #default="scope"><el-button :disabled="disabled" @click="choose(scope.row)">采用此行</el-button></template></el-table-column>
        </el-table>
        <p>共 {{result.rows.length}} 行；重复代码和名称分别保留。</p>
      </template>
    </el-dialog>
  </div>
</template>
<style scoped>.original-lookup{display:flex;gap:4px;width:100%}</style>
