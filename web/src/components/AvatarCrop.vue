<script setup lang="ts">
import {ref,nextTick} from 'vue'
import Cropper from 'cropperjs'
import {api} from '../api'
const props=withDefaults(defineProps<{modelValue:string;width?:number;height?:number;aspectRatio?:number;title?:string}>(),{width:256,height:256,aspectRatio:1,title:'裁剪头像'});const emit=defineEmits(['update:modelValue'])
const visible=ref(false),container=ref<HTMLDivElement>(),source=ref('')
let cropper:Cropper
async function load(url:string){source.value=url;visible.value=true;await nextTick();container.value!.innerHTML='';const image=new Image();image.src=source.value;cropper=new Cropper(image,{container:container.value!});cropper.getCropperImage()!.rotatable=true;cropper.getCropperSelection()!.aspectRatio=props.aspectRatio}
async function choose(event:Event){await load(URL.createObjectURL((event.target as HTMLInputElement).files![0]))}
function rotate(angle:string){cropper.getCropperImage()!.$rotate(angle)}
async function save(){
 const cropped=await cropper.getCropperSelection()!.$toCanvas({width:props.width,height:props.height})
 const canvas=document.createElement('canvas');canvas.width=props.width;canvas.height=props.height
 canvas.getContext('2d')!.drawImage(cropped,0,0,props.width,props.height)
 const blob=await new Promise<Blob>(resolve=>canvas.toBlob((value:any)=>resolve(value!),'image/png'))
 const data=new FormData();data.append('url',new File([blob],'avatar.png',{type:'image/png'}))
 emit('update:modelValue',(await api('/api/system/file/',{method:'POST',data})).data.url);visible.value=false
}
function close(){container.value!.innerHTML='';URL.revokeObjectURL(source.value)}
defineExpose({open:load,rotate,save})
</script>
<template><div class="avatar-input"><el-avatar :src="modelValue" @click="modelValue&&load(modelValue)"/><input type="file" accept="image/*" @change="choose"/></div><el-dialog v-model="visible" :title="title" width="min(600px, calc(100vw - 24px))" @closed="close"><div ref="container" class="crop-container"/><template #footer><el-button @click="rotate('-90deg')">向左旋转</el-button><el-button @click="rotate('90deg')">向右旋转</el-button><el-button @click="visible=false">取消</el-button><el-button type="primary" @click="save">使用头像</el-button></template></el-dialog></template>
