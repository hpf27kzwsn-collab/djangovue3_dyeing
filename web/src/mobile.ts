import {ref} from 'vue'
const viewport=window.matchMedia('(max-width: 768px)')
const mobile=ref(viewport.matches)
viewport.addEventListener('change',event=>mobile.value=event.matches)
export const useMobile=()=>mobile
