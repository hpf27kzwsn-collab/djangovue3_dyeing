"""业务页面实际字段、关联及操作。"""
from plugins.erp_base.business_resources import options

MODEL_FIELDS = {'PurchaseRequest': 'number document_at applicant department factory purchase_kind status confirmed_by confirmed_at',
 'PurchaseRequestLine': 'request line_number material quantity unit required_at order_line work_card',
 'PurchaseOrder': 'number document_at supplier buyer business_unit purchase_kind supplier_contract_number due_at status',
 'PurchaseOrderLine': 'order line_number request_line material supplier_specification specification_snapshot supplier_lot_number '
                      'quantity unit piece_quantity unit_price price_unit due_at order_line',
 'PurchaseReturn': 'number supplier returned_at reason status warehouse_issue',
 'PurchaseReturnLine': 'return_order original_receipt_line quantity unit'}

RELATIONS = {'PurchaseRequest': {'applicant': ('erp_base_employee', 'name'),
                     'department': ('dept', 'name'),
                     'factory': ('erp_base_factory', 'name'),
                     'purchase_kind': ('erp_base_businesschoice', 'name'),
                     'confirmed_by': ('erp_base_employee', 'name')},
 'PurchaseRequestLine': {'request': ('erp_purchase_purchaserequest', 'number'),
                         'material': ('erp_base_material', 'name'),
                         'unit': ('erp_base_unit', 'name'),
                         'order_line': ('erp_sales_salesorderline', 'line_number'),
                         'work_card': ('erp_production_workcard', 'number')},
 'PurchaseOrder': {'supplier': ('erp_base_party', 'name'),
                   'buyer': ('erp_base_employee', 'name'),
                   'business_unit': ('erp_base_businessunit', 'name'),
                   'purchase_kind': ('erp_base_businesschoice', 'name')},
 'PurchaseOrderLine': {'order': ('erp_purchase_purchaseorder', 'number'),
                       'request_line': ('erp_purchase_purchaserequestline', 'line_number'),
                       'material': ('erp_base_material', 'name'),
                       'unit': ('erp_base_unit', 'name'),
                       'price_unit': ('erp_base_unit', 'name'),
                       'order_line': ('erp_sales_salesorderline', 'line_number')},
 'PurchaseReturn': {'supplier': ('erp_base_party', 'name'), 'warehouse_issue': ('erp_warehouse_stockissue', 'number')},
 'PurchaseReturnLine': {'return_order': ('erp_purchase_purchasereturn', 'number'),
                        'original_receipt_line': ('erp_warehouse_stockreceiptline', 'line_number'),
                        'unit': ('erp_base_unit', 'name')}}

VIEWSETS = {'PurchaseRequest': 'plugins.erp_purchase.views.PurchaseViewSet',
 'PurchaseRequestLine': 'plugins.erp_base.business_api.BusinessViewSet',
 'PurchaseOrder': 'plugins.erp_purchase.views.PurchaseViewSet',
 'PurchaseOrderLine': 'plugins.erp_base.business_api.BusinessViewSet',
 'PurchaseReturn': 'plugins.erp_purchase.views.PurchaseViewSet',
 'PurchaseReturnLine': 'plugins.erp_base.business_api.BusinessViewSet'}

WORKFLOWS = {'PurchaseRequest': {'editable_states': ['draft'],
                     'children': [{'entity': 'erp_purchase_purchaserequestline',
                                   'title': '业务明细',
                                   'key': 'request',
                                   'atomic': True}],
                     'actions': [{'key': 'confirm',
                                  'title': '确认',
                                  'states': ['draft'],
                                  'inputs': [{'key': 'employee',
                                              'title': '确认员工',
                                              'kind': 'select',
                                              'options': [],
                                              'required': True,
                                              'remote': {'entity': 'erp_base_employee', 'pk': 'id', 'label': 'name'}}]}]},
 'PurchaseRequestLine': {},
 'PurchaseOrder': {'editable_states': ['draft'],
                   'children': [{'entity': 'erp_purchase_purchaseorderline', 'title': '业务明细', 'key': 'order', 'atomic': True}],
                   'actions': [{'key': 'confirm', 'title': '确认', 'states': ['draft'], 'inputs': []}]},
 'PurchaseOrderLine': {},
 'PurchaseReturn': {'editable_states': ['draft'],
                    'children': [{'entity': 'erp_purchase_purchasereturnline',
                                  'title': '业务明细',
                                  'key': 'return_order',
                                  'atomic': True}],
                    'actions': [{'key': 'confirm', 'title': '确认', 'states': ['draft'], 'inputs': []}]},
 'PurchaseReturnLine': {}}

RESOURCE_OPTIONS = options('erp_purchase', MODEL_FIELDS, RELATIONS, VIEWSETS)
for name, workflow in WORKFLOWS.items():
    RESOURCE_OPTIONS[name]["workflow"] = workflow
RESOURCE_OPTIONS['PurchaseRequest']['label_field'] = 'number'
RESOURCE_OPTIONS['PurchaseRequestLine']['label_field'] = 'line_number'
RESOURCE_OPTIONS['PurchaseOrder']['label_field'] = 'number'
RESOURCE_OPTIONS['PurchaseOrderLine']['label_field'] = 'line_number'
RESOURCE_OPTIONS['PurchaseReturn']['label_field'] = 'number'
RESOURCE_OPTIONS['PurchaseReturnLine']['label_field'] = 'id'

from plugins.erp_production.workflows import action,reason
for name,states in {'PurchaseRequest':['confirmed'],'PurchaseOrder':['confirmed','partial_received','received'],'PurchaseReturn':['confirmed','received']}.items():
    WORKFLOWS[name]['actions'] += [action('close','按实际情况结案',states,[reason]),action('reopen','重新办理',['closed'],[reason])]
