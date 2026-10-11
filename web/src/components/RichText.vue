<script setup lang="ts">
import {ref,onMounted,onBeforeUnmount,watch} from 'vue'
import {createEditor,createToolbar,type IDomEditor,type IToolbarConfig} from '@wangeditor/editor'
import '@wangeditor/editor/dist/css/style.css'
import {api} from '../api'
import {toolbarKeys} from './editorToolbar'
const props=withDefaults(defineProps<{modelValue?:string;disabled?:boolean;mode?:'default'|'simple';placeholder?:string;height?:string|number;toolbarConfig?:Partial<IToolbarConfig>}>(),{modelValue:'',disabled:false,mode:'default',placeholder:'请输入内容',height:310});const emit=defineEmits(['update:modelValue','change'])
const editorElement=ref<HTMLDivElement>(),toolbarElement=ref<HTMLDivElement>()
let editor:IDomEditor
onMounted(()=>{
  editor=createEditor({selector:editorElement.value!,html:props.modelValue,mode:props.mode,config:{placeholder:props.placeholder,onChange:instance=>{emit('update:modelValue',instance.getHtml());emit('change',instance.getHtml(),instance.getText())},
    MENU_CONF:{uploadVideo:{customUpload:async(file:File,insert:(url:string)=>void)=>{const data=new FormData();data.append('url',file);insert((await api('/api/system/file/',{method:'POST',data})).data.url)}},uploadImage:{customUpload:async(file:File,insert:(url:string)=>void)=>{const data=new FormData();data.append('url',file);insert((await api('/api/system/file/',{method:'POST',data})).data.url)}}}}})
  createToolbar({editor,selector:toolbarElement.value!,mode:props.mode,config:{...(props.mode==='default'?{toolbarKeys}:{}),...props.toolbarConfig}})
  if(props.disabled)editor.disable()
})
watch(()=>props.modelValue,value=>{if(value!==editor.getHtml())editor.setHtml(value)})
watch(()=>props.disabled,value=>value?editor.disable():editor.enable())
onBeforeUnmount(()=>editor.destroy())
defineExpose({getHtml:()=>editor.getHtml(),getText:()=>editor.getText()})
</script>
<template><div class="rich-editor"><div ref="toolbarElement"/><div ref="editorElement" :style="{height:typeof height==='number'?height+'px':height}"/></div></template>

<style scoped>.rich-editor{width:100%;min-width:0;overflow:hidden}.rich-editor :deep(.w-e-bar){flex-wrap:wrap}.rich-editor :deep(.w-e-text-container){overflow:auto}</style>
