// 每页仅列出原流程实际使用的独立查询项。权限由元数据和后端共同决定。
export const searches:Record<string,string[]>={
 user:['username','name','mobile','email','gender','dept','role','is_active','user_type'],
 operation_log:['request_modular','request_path','request_ip','request_method','creator','status','response_code'],
 login_log:['username','ip','browser','os','status'],
 download_center:['file_name','task_name','task_status'],task_result:['task_id','task_name','status','worker'],
 file:['name','file_type','upload_method'],message_center:['title','target_type','creator'],
 area:['code','name','level','enable'],dept:['name','status'],role:['name','key','status'],
 post:['name','code','status'],periodic_task:['name','task','enabled'],
 dictionary:['label','value','type','status'],
}
