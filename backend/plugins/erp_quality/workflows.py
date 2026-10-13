from plugins.erp_production.workflows import field,related,action,at,reason

def child(name,title,key,atomic=False,**extra):
    return {'entity':'erp_quality_'+name.lower(),'title':title,'key':key,'atomic':atomic,**extra}

employee=related('employee','操作员工','erp_base_employee','name')
unit=lambda key,title:related(key,title,'erp_base_unit','name',False)
WORKFLOWS={
'QualityInspection': {'state_field':'result','editable_states':['pending'],'freeze_when':['is_void'],'children':[
        child('InspectionResultLine','实际检验项目','inspection',True),child('QualityDisposition','处置历史','inspection')],
        'actions':[dict(action('void','取消检验采用',['pending','pass','fail'],[at,reason]),hide_when=['is_void']),action('judge','检验判定',['pending'],[employee,field('result','实际判定','select',options=[
            {'value':'pass','label':'合格'},{'value':'fail','label':'不合格'}])]),action('dispose','明确数量处置',['pass','fail'],[
            at,employee,field('kind','实际处置','select',options=[{'value':key,'label':label} for key,label in [
                ('release','放行'),('concession','让步'),('rework','返修'),('downgrade','降级'),('scrap','报废'),('hold','隔离')]]),
            field('quantity','覆盖数量','decimal'),related('unit','覆盖单位','erp_base_unit','name'),reason,
            related('supersedes','被替换原处置','erp_quality_qualitydisposition','id',False)])]},
'InspectionResultLine': {},
'QualityDisposition': {'readonly':True},
'QualityDefect': {'editable_states':['open','handling'],'actions':[action('close','关闭异常',['open','handling'],[field('handling','处理说明','textarea')])]}
}
