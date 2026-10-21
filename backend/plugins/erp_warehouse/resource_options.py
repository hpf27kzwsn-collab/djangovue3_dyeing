"""业务页面实际字段、关联及操作。"""
from plugins.erp_base.business_resources import options

MODEL_FIELDS = {'InventoryLot': 'code material owner supplier supplier_lot_number production_batch received_at expiry_at',
 'StockReceipt': 'number document_at kind warehouse source_party status posted_at',
 'StockReceiptLine': 'quantity_source receipt line_number lot location quantity unit auxiliary_mass_kg auxiliary_pieces '
                     'quality_state purchase_order_line work_card package original_issue_line',
 'StockIssue': 'number document_at kind warehouse destination_party status posted_at',
 'StockIssueLine': 'quantity_source measurement_record issue line_number lot location quantity unit quality_state work_card '
                   'weighing_line delivery_line package original_receipt_line',
 'InventoryMovement': 'occurred_at lot location quality_state package quantity_delta unit receipt_line issue_line transfer_line '
                      'adjustment_line leg_number reverses',
 'StockBalance': 'lot location quality_state package quantity',
 'StockTransfer': 'number document_at from_warehouse to_warehouse status posted_at',
 'StockTransferLine': 'transfer line_number lot package from_location to_location quantity quality_state',
 'StockCount': 'number warehouse snapshot_at counted_at status',
 'StockCountLine': 'count lot location quality_state package book_quantity counted_quantity reason',
 'StockAdjustment': 'number document_at warehouse count reason status posted_at',
 'StockAdjustmentLine': 'adjustment line_number lot location quality_state package quantity_delta new_quality_state count_line '
                        'disposition'}

RELATIONS = {'InventoryLot': {'material': ('erp_base_material', 'name'),
                  'owner': ('erp_base_party', 'name'),
                  'supplier': ('erp_base_party', 'name'),
                  'production_batch': ('erp_production_dyebatch', 'number')},
 'StockReceipt': {'warehouse': ('erp_base_warehouse', 'name'), 'source_party': ('erp_base_party', 'name')},
 'StockReceiptLine': {'receipt': ('erp_warehouse_stockreceipt', 'number'),
                      'lot': ('erp_warehouse_inventorylot', 'code'),
                      'location': ('erp_base_storagelocation', 'name'),
                      'unit': ('erp_base_unit', 'name'),
                      'purchase_order_line': ('erp_purchase_purchaseorderline', 'line_number'),
                      'work_card': ('erp_production_workcard', 'number'),
                      'package': ('erp_warehouse_package', 'code'),
                      'original_issue_line': ('erp_warehouse_stockissueline', 'line_number')},
 'StockIssue': {'warehouse': ('erp_base_warehouse', 'name'), 'destination_party': ('erp_base_party', 'name')},
 'StockIssueLine': {'measurement_record': ('erp_production_weighingrecord', 'id'),
                    'issue': ('erp_warehouse_stockissue', 'number'),
                    'lot': ('erp_warehouse_inventorylot', 'code'),
                    'location': ('erp_base_storagelocation', 'name'),
                    'unit': ('erp_base_unit', 'name'),
                    'work_card': ('erp_production_workcard', 'number'),
                    'weighing_line': ('erp_production_weighingline', 'sequence'),
                    'delivery_line': ('erp_sales_deliveryline', 'line_number'),
                    'package': ('erp_warehouse_package', 'code'),
                    'original_receipt_line': ('erp_warehouse_stockreceiptline', 'line_number')},
 'InventoryMovement': {'lot': ('erp_warehouse_inventorylot', 'code'),
                       'location': ('erp_base_storagelocation', 'name'),
                       'package': ('erp_warehouse_package', 'code'),
                       'unit': ('erp_base_unit', 'name'),
                       'receipt_line': ('erp_warehouse_stockreceiptline', 'line_number'),
                       'issue_line': ('erp_warehouse_stockissueline', 'line_number'),
                       'transfer_line': ('erp_warehouse_stocktransferline', 'line_number'),
                       'adjustment_line': ('erp_warehouse_stockadjustmentline', 'line_number'),
                       'reverses': ('erp_warehouse_inventorymovement', 'id')},
 'StockBalance': {'lot': ('erp_warehouse_inventorylot', 'code'),
                  'location': ('erp_base_storagelocation', 'name'),
                  'package': ('erp_warehouse_package', 'code')},
 'StockTransfer': {'from_warehouse': ('erp_base_warehouse', 'name'), 'to_warehouse': ('erp_base_warehouse', 'name')},
 'StockTransferLine': {'transfer': ('erp_warehouse_stocktransfer', 'number'),
                       'lot': ('erp_warehouse_inventorylot', 'code'),
                       'package': ('erp_warehouse_package', 'code'),
                       'from_location': ('erp_base_storagelocation', 'name'),
                       'to_location': ('erp_base_storagelocation', 'name')},
 'StockCount': {'warehouse': ('erp_base_warehouse', 'name')},
 'StockCountLine': {'count': ('erp_warehouse_stockcount', 'number'),
                    'lot': ('erp_warehouse_inventorylot', 'code'),
                    'location': ('erp_base_storagelocation', 'name'),
                    'package': ('erp_warehouse_package', 'code')},
 'StockAdjustment': {'warehouse': ('erp_base_warehouse', 'name'), 'count': ('erp_warehouse_stockcount', 'number')},
 'StockAdjustmentLine': {'adjustment': ('erp_warehouse_stockadjustment', 'number'),
                         'lot': ('erp_warehouse_inventorylot', 'code'),
                         'location': ('erp_base_storagelocation', 'name'),
                         'package': ('erp_warehouse_package', 'code'),
                         'count_line': ('erp_warehouse_stockcountline', 'id'),
                         'disposition': ('erp_quality_qualitydisposition', 'id')}}

VIEWSETS = {'InventoryLot': 'plugins.erp_base.business_api.BusinessViewSet',
 'StockReceipt': 'plugins.erp_warehouse.views.StockDocumentViewSet',
 'StockReceiptLine': 'plugins.erp_base.business_api.BusinessViewSet',
 'StockIssue': 'plugins.erp_warehouse.views.StockDocumentViewSet',
 'StockIssueLine': 'plugins.erp_base.business_api.BusinessViewSet',
 'InventoryMovement': 'plugins.erp_warehouse.views.InventoryReadViewSet',
 'StockBalance': 'plugins.erp_warehouse.views.InventoryReadViewSet',
 'StockTransfer': 'plugins.erp_warehouse.views.StockDocumentViewSet',
 'StockTransferLine': 'plugins.erp_base.business_api.BusinessViewSet',
 'StockCount': 'plugins.erp_warehouse.views.StockCountViewSet',
 'StockCountLine': 'plugins.erp_base.business_api.BusinessViewSet',
 'StockAdjustment': 'plugins.erp_warehouse.views.StockDocumentViewSet',
 'StockAdjustmentLine': 'plugins.erp_base.business_api.BusinessViewSet'}

WORKFLOWS = {'InventoryLot': {},
 'StockReceipt': {'editable_states': ['draft'],
                  'children': [{'entity': 'erp_warehouse_stockreceiptline', 'title': '业务明细', 'key': 'receipt', 'atomic': True}],
                  'actions': [{'key': 'confirm', 'title': '确认', 'states': ['draft'], 'inputs': []},
                              {'key': 'post',
                               'title': '库存过账',
                               'states': ['confirmed'],
                               'inputs': [{'key': 'at', 'title': '实际生效时间', 'kind': 'datetime', 'options': [], 'required': True}]},
                              {'key': 'reverse',
                               'title': '冲销',
                               'states': ['posted'],
                               'inputs': [{'key': 'at', 'title': '实际生效时间', 'kind': 'datetime', 'options': [], 'required': True},
                                          {'key': 'reason',
                                           'title': '原因',
                                           'kind': 'textarea',
                                           'options': [],
                                           'required': True}]}]},
 'StockReceiptLine': {},
 'StockIssue': {'editable_states': ['draft'],
                'children': [{'entity': 'erp_warehouse_stockissueline', 'title': '业务明细', 'key': 'issue', 'atomic': True}],
                'actions': [{'key': 'confirm', 'title': '确认', 'states': ['draft'], 'inputs': []},
                            {'key': 'post',
                             'title': '库存过账',
                             'states': ['confirmed'],
                             'inputs': [{'key': 'at', 'title': '实际生效时间', 'kind': 'datetime', 'options': [], 'required': True}]},
                            {'key': 'reverse',
                             'title': '冲销',
                             'states': ['posted'],
                             'inputs': [{'key': 'at', 'title': '实际生效时间', 'kind': 'datetime', 'options': [], 'required': True},
                                        {'key': 'reason', 'title': '原因', 'kind': 'textarea', 'options': [], 'required': True}]}]},
 'StockIssueLine': {},
 'InventoryMovement': {'readonly': True},
 'StockBalance': {'readonly': True},
 'StockTransfer': {'editable_states': ['draft'],
                   'children': [{'entity': 'erp_warehouse_stocktransferline',
                                 'title': '业务明细',
                                 'key': 'transfer',
                                 'atomic': True}],
                   'actions': [{'key': 'confirm', 'title': '确认', 'states': ['draft'], 'inputs': []},
                               {'key': 'post',
                                'title': '库存过账',
                                'states': ['confirmed'],
                                'inputs': [{'key': 'at',
                                            'title': '实际生效时间',
                                            'kind': 'datetime',
                                            'options': [],
                                            'required': True}]},
                               {'key': 'reverse',
                                'title': '冲销',
                                'states': ['posted'],
                                'inputs': [{'key': 'at', 'title': '实际生效时间', 'kind': 'datetime', 'options': [], 'required': True},
                                           {'key': 'reason',
                                            'title': '原因',
                                            'kind': 'textarea',
                                            'options': [],
                                            'required': True}]}]},
 'StockTransferLine': {},
 'StockCount': {'editable_states': ['draft'],
                'children': [{'entity': 'erp_warehouse_stockcountline',
                              'title': '实盘明细',
                              'key': 'count',
                              'atomic': False,
                              'parent_states': ['counting']}],
                'actions': [{'key': 'begin', 'title': '冻结账面开始盘点', 'states': ['draft'], 'inputs': []},
                            {'key': 'confirm',
                             'title': '确认实盘差异',
                             'states': ['counting'],
                             'inputs': [{'key': 'at', 'title': '实际生效时间', 'kind': 'datetime', 'options': [], 'required': True}]},
                            {'key': 'adjust',
                             'title': '应用盘点差异',
                             'states': ['confirmed'],
                             'inputs': [{'key': 'number', 'title': '调整单号', 'kind': 'text', 'options': [], 'required': True},
                                        {'key': 'at', 'title': '实际生效时间', 'kind': 'datetime', 'options': [], 'required': True},
                                        {'key': 'reason', 'title': '原因', 'kind': 'textarea', 'options': [], 'required': True}]}]},
 'StockCountLine': {'delete_disabled': True},
 'StockAdjustment': {'editable_states': ['draft'],
                     'children': [{'entity': 'erp_warehouse_stockadjustmentline',
                                   'title': '业务明细',
                                   'key': 'adjustment',
                                   'atomic': True}],
                     'actions': [{'key': 'confirm', 'title': '确认', 'states': ['draft'], 'inputs': []},
                                 {'key': 'post',
                                  'title': '库存过账',
                                  'states': ['confirmed'],
                                  'inputs': [{'key': 'at',
                                              'title': '实际生效时间',
                                              'kind': 'datetime',
                                              'options': [],
                                              'required': True}]},
                                 {'key': 'reverse',
                                  'title': '冲销',
                                  'states': ['posted'],
                                  'inputs': [{'key': 'at',
                                              'title': '实际生效时间',
                                              'kind': 'datetime',
                                              'options': [],
                                              'required': True},
                                             {'key': 'reason',
                                              'title': '原因',
                                              'kind': 'textarea',
                                              'options': [],
                                              'required': True}]}]},
 'StockAdjustmentLine': {}}

MODEL_FIELDS['LotTransformation']='number work_card execution occurred_at reason is_confirmed confirmed_at'
MODEL_FIELDS['LotTransformationLine']='transformation direction lot quantity unit receipt_line issue_line'
RELATIONS['LotTransformation']={'work_card':('erp_production_workcard','number'),'execution':('erp_production_operationexecution','execution_number')}
RELATIONS['LotTransformationLine']={'transformation':('erp_warehouse_lottransformation','number'),
    'lot':('erp_warehouse_inventorylot','code'),'unit':('erp_base_unit','name'),
    'receipt_line':('erp_warehouse_stockreceiptline','line_number'),'issue_line':('erp_warehouse_stockissueline','line_number')}
VIEWSETS['LotTransformation']='plugins.erp_warehouse.views.LotTransformationViewSet'
VIEWSETS['LotTransformationLine']='plugins.erp_base.business_api.BusinessViewSet'
# Fulfillment resource fields
MODEL_FIELDS.update({'Package': 'source_execution calculation_snapshot code barcode display_number lot work_card batch packed_at '
            'packer piece_quantity tube_specification tube_unit_tare_kg outer_packaging outer_tare_kg '
            'gross_mass_kg net_mass_kg net_mass_basis fixed_piece_mass_kg length_m label_template label_remarks '
            'status',
 'PackageOrderAllocation': 'package work_card_allocation quantity unit',
 'PackageDispositionAllocation': 'package disposition quantity unit',
 'LabelPrint': 'requested_at status confirmed_at confirmation_source previous_print template_snapshot package '
               'template printed_at copies kind reason operator'})
RELATIONS.update({'Package': {'source_execution': ('erp_production_operationexecution', 'execution_number'),
             'lot': ('erp_warehouse_inventorylot', 'code'),
             'work_card': ('erp_production_workcard', 'number'),
             'batch': ('erp_production_dyebatch', 'id'),
             'packer': ('erp_base_employee', 'name'),
             'tube_specification': ('erp_base_packagingspecification', 'id'),
             'outer_packaging': ('erp_base_packagingspecification', 'id'),
             'label_template': ('erp_base_labeltemplate', 'name')},
 'PackageOrderAllocation': {'package': ('erp_warehouse_package', 'code'),
                            'work_card_allocation': ('erp_production_workcardorderallocation', 'id'),
                            'unit': ('erp_base_unit', 'name')},
 'PackageDispositionAllocation': {'package': ('erp_warehouse_package', 'code'),
                                  'disposition': ('erp_quality_qualitydisposition', 'id'),
                                  'unit': ('erp_base_unit', 'name')},
 'LabelPrint': {'previous_print': ('erp_warehouse_labelprint', 'id'),
                'package': ('erp_warehouse_package', 'code'),
                'template': ('erp_base_labeltemplate', 'name'),
                'operator': ('erp_base_employee', 'name')}})
VIEWSETS.update({'Package': 'plugins.erp_warehouse.packing_views.PackageViewSet',
 'PackageOrderAllocation': 'plugins.erp_base.business_api.BusinessViewSet',
 'PackageDispositionAllocation': 'plugins.erp_base.business_api.BusinessViewSet',
 'LabelPrint': 'plugins.erp_warehouse.packing_views.LabelPrintViewSet'})
MODEL_FIELDS['Package']+=' packaging_execution'
MODEL_FIELDS['StockReceiptLine']+=' source_execution'
RELATIONS['StockReceiptLine']['source_execution']=('erp_production_operationexecution','execution_number')
MODEL_FIELDS['LotTransformation']+=' is_void voided_at void_reason'
RELATIONS['Package']['packaging_execution']=('erp_production_operationexecution','execution_number')
RESOURCE_OPTIONS = options('erp_warehouse', MODEL_FIELDS, RELATIONS, VIEWSETS)
RESOURCE_OPTIONS['LotTransformation']['workflow']={'state_field':'is_confirmed','editable_states':[False],
    'children':[{'entity':'erp_warehouse_lottransformationline','title':'实际投入产出','key':'transformation','atomic':True}],
    'actions':[{'key':'confirm','title':'确认批次谱系','states':[False],'inputs':[{'key':'at','title':'确认时间','kind':'datetime','options':[],'required':True}]}]}
RESOURCE_OPTIONS['LotTransformation']['workflow']['freeze_when']=['is_void']
RESOURCE_OPTIONS['LotTransformation']['workflow']['actions'][0]['hide_when']=['is_void']
RESOURCE_OPTIONS['LotTransformation']['workflow']['actions'].append({'key':'void','title':'取消谱系采用','states':[False,True],'hide_when':['is_void'],
    'inputs':[{'key':'at','title':'取消时间','kind':'datetime','options':[],'required':True},{'key':'reason','title':'实际依据','kind':'textarea','options':[],'required':True}]})
for name, workflow in WORKFLOWS.items():
    RESOURCE_OPTIONS[name]["workflow"] = workflow
RESOURCE_OPTIONS['InventoryLot']['label_field'] = 'code'
RESOURCE_OPTIONS['StockReceipt']['label_field'] = 'number'
RESOURCE_OPTIONS['StockReceiptLine']['label_field'] = 'line_number'
RESOURCE_OPTIONS['StockIssue']['label_field'] = 'number'
RESOURCE_OPTIONS['StockIssueLine']['label_field'] = 'line_number'
RESOURCE_OPTIONS['InventoryMovement']['label_field'] = 'id'
RESOURCE_OPTIONS['StockBalance']['label_field'] = 'id'
RESOURCE_OPTIONS['StockTransfer']['label_field'] = 'number'
RESOURCE_OPTIONS['StockTransferLine']['label_field'] = 'line_number'
RESOURCE_OPTIONS['StockCount']['label_field'] = 'number'
RESOURCE_OPTIONS['StockCountLine']['label_field'] = 'id'
RESOURCE_OPTIONS['StockAdjustment']['label_field'] = 'number'
RESOURCE_OPTIONS['StockAdjustmentLine']['label_field'] = 'line_number'

from .packing_workflows import WORKFLOWS as FULFILLMENT_WORKFLOWS
for name, workflow in FULFILLMENT_WORKFLOWS.items():
    RESOURCE_OPTIONS[name]["workflow"] = workflow

from .source_resources import RESOURCE_OPTIONS as SOURCE_RESOURCES
RESOURCE_OPTIONS.update(SOURCE_RESOURCES)

from plugins.erp_base.foundation_catalog import configure_resources
configure_resources(RESOURCE_OPTIONS, 'erp_warehouse')
