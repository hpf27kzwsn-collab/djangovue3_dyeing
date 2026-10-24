from plugins.erp_production.workflows import field,related,action,at,reason


def child(name,title,key,atomic=False):return {'entity':'erp_warehouse_'+name.lower(),'title':title,'key':key,'atomic':atomic}


WORKFLOWS={
    'Package':{'editable_states':['draft'],'children':[child('PackageOrderAllocation','包装订单分配','package',True),
        child('PackageDispositionAllocation','实际放行覆盖','package',True),child('LabelPrint','打印与重打','package')],
        'actions':[action('pack','确认实际包装',['draft'],[at,related('employee','包装员工','erp_base_employee','name'),
            related('machine','包装实际机台','erp_base_machine','name',False)]),
            action('void','作废包装',['draft','packed'],[at,reason]),
            action('request_print','标签打印或重打',['packed','received','issued','returned'],[at,
                related('employee','操作员工','erp_base_employee','name'),field('copies','份数','integer'),
                related('previous','原打印请求','erp_warehouse_labelprint','id',False),field('reason','重打依据','textarea',False)])]},
    'PackageOrderAllocation':{},'PackageDispositionAllocation':{},
    'LabelPrint':{'readonly':True,'actions':[action('confirm','人工确认打印结果',['requested'],[at,
        field('succeeded','实际打印成功','boolean'),field('reason','失败说明','textarea',False)])]},
}
