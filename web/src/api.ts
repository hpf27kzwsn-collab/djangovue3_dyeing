import axios, { type AxiosRequestConfig } from 'axios'
import { ElMessage } from 'element-plus'
export interface Result<T = any> {code: number; msg: string; data: T; page: number; limit: number; total: number; is_next?:boolean; is_previous?:boolean}
const client = axios.create()
client.interceptors.request.use(config => {
  const token = localStorage.getItem('access')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})
client.interceptors.response.use(response => response, async error => {
  if (error.response?.status === 401 && localStorage.getItem('refresh') && !error.config.refreshed) {
    error.config.refreshed = true
    const refreshConfig:any={url:'/api/token/refresh/',method:'POST',data:{refresh:localStorage.getItem('refresh')},refreshed:true}
    const response = await client(refreshConfig)
    localStorage.setItem('access', response.data.access)
    localStorage.setItem('refresh', response.data.refresh)
    return client(error.config)
  }
  const detail=error.response?.data?.data
  ElMessage.error(detail?.sheet?`${detail.sheet}，第 ${detail.row} 行，${detail.field}：${typeof detail.detail==='string'?detail.detail:JSON.stringify(detail.detail)}`:error.response?.data?.msg || error.message)
  if (error.response?.status === 401) {
    localStorage.removeItem('access'); localStorage.removeItem('refresh')
    window.location.href = '/login'
  }
  if(error.response?.status===403)window.location.href='/401'
  return Promise.reject(error)
})
export async function api<T = any>(url: string, config: AxiosRequestConfig = {}): Promise<Result<T>> {
  return (await client({url, ...config})).data
}
export async function download(url: string, filename: string, params = {}) {
  const response = await client.get(url, {responseType: 'blob', params})
  const href = URL.createObjectURL(response.data)
  const link = document.createElement('a'); link.href = href; link.download = filename; link.click()
  URL.revokeObjectURL(href)
}
