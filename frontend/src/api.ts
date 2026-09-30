export type Row = Record<string, any>;
let token = sessionStorage.getItem('steel-token') || '';
export function setToken(value: string) { token = value; value ? sessionStorage.setItem('steel-token', value) : sessionStorage.removeItem('steel-token'); }
export async function api(path: string, method = 'GET', data?: unknown, key?: string): Promise<any> {
  const response = await fetch('/api/v1/' + path, {method, headers:{'Content-Type':'application/json',Authorization:`Bearer ${token}`,...(method !== 'GET' ? {'Idempotency-Key':key || crypto.randomUUID()} : {})},body:data === undefined ? undefined : JSON.stringify(data)});
  if (!response.ok) {const error = await response.json(); throw new Error(error.error?.code || '请求失败');}
  return response.json();
}
export async function downloadPdf(id: string) {
  const response = await fetch(`/api/v1/contracts/${id}/pdf`, {headers:{Authorization:`Bearer ${token}`}});
  if(!response.ok) throw new Error('PDF 导出失败');
  const url=URL.createObjectURL(await response.blob());const a=document.createElement('a');a.href=url;a.download='合同草稿.pdf';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
