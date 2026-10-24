from plugins.erp_production.workflows import action,at,reason


def child(name,title,key):return {'entity':'erp_sales_'+name.lower(),'title':title,'key':key,'atomic':True}


WORKFLOWS={
    'Delivery':{'editable_states':['draft'],'children':[child('DeliveryLine','实际包装交付明细','delivery')],
        'actions':[action('confirm','确认交付及价格来源',['draft'],[]),action('deliver','记录客户实际交付',['issued'],[at]),
            action('cancel','取消未出库交付',['draft','confirmed'],[reason]),action('undo_delivery','更正客户交付采用',['delivered'],[reason])]},
    'DeliveryLine':{},
    'SalesReturn':{'editable_states':['draft'],'children':[child('SalesReturnLine','原交付实物退回','return_order')],
        'actions':[action('confirm','确认退回及待检收回关联',['draft'],[]),action('close','退回业务结案',['received'],[reason]),action('cancel','取消未生效退回',['draft','confirmed'],[reason])]},
    'SalesReturnLine':{},
    'CustomerComplaint':{'editable_states':['open','handling'],'children':[child('CustomerComplaintLine','投诉问题及处理','complaint')],
        'actions':[action('handle','开始处理',['open'],[reason]),action('close','记录处理后结案',['open','handling'],[reason])]},
    'CustomerComplaintLine':{},
}
WORKFLOWS['SalesReturn']['actions'].append(action('reopen','重新处理原退回',['closed'],[reason]))
