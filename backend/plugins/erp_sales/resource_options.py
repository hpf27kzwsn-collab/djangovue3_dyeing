"""业务页面字段与分页关联选择；与模型实际字段对应。"""
from plugins.erp_base.business_resources import options

MODEL_FIELDS = {'CommercialPrice': 'kind number customer document_at status',
 'CommercialPriceLine': 'price_document line_number material color_standard version confirmed_base_price additional_price '
                        'additional_price_description customer_quote_price unit_price unit valid_from valid_to is_confirmed',
 'SalesOrder': 'number document_at business_unit customer detail_customer_name salesperson customer_order_number '
               'customer_job_number order_kind delivery_address delivery_address_snapshot brand_name contact_information '
               'first_due_at is_urgent primary_light secondary_light status confirmed_by confirmed_at closed_at',
 'SalesOrderLine': 'price_source manual_price_reason adopted_price_snapshot order line_number material customer_material '
                   'specification_snapshot customer_product_snapshot customer_line_number supplier_lot_number color_standard '
                   'color_number_snapshot customer_color_number color_depth ordered_quantity ordered_unit required_raw_quantity '
                   'required_raw_unit piece_quantity dyeing_due_at final_due_at intended_use special_requirements default_route '
                   'approved_recipe unit_price price_unit is_closed',
 'SalesLineRequirement': 'order_line namespace requirement_code name value_text',
 'SalesOrderChange': 'order change_number requested_at reason status confirmed_by confirmed_at',
 'SalesOrderChangeLine': 'before_values change order_line new_quantity new_due_at new_requirements'}

RELATIONS = {'CommercialPrice': {'customer': ('erp_base_party', 'name')},
 'CommercialPriceLine': {'price_document': ('erp_sales_commercialprice', 'number'),
                         'material': ('erp_base_material', 'name'),
                         'color_standard': ('erp_base_colorstandard', 'code'),
                         'unit': ('erp_base_unit', 'name')},
 'SalesOrder': {'business_unit': ('erp_base_businessunit', 'name'),
                'customer': ('erp_base_party', 'name'),
                'salesperson': ('erp_base_employee', 'name'),
                'order_kind': ('erp_base_businesschoice', 'name'),
                'delivery_address': ('erp_base_partyaddress', 'id'),
                'primary_light': ('erp_base_businesschoice', 'name'),
                'secondary_light': ('erp_base_businesschoice', 'name'),
                'confirmed_by': ('erp_base_employee', 'name')},
 'SalesOrderLine': {'price_source': ('erp_sales_commercialpriceline', 'version'),
                    'order': ('erp_sales_salesorder', 'number'),
                    'material': ('erp_base_material', 'name'),
                    'customer_material': ('erp_base_customermaterial', 'id'),
                    'color_standard': ('erp_base_colorstandard', 'code'),
                    'color_depth': ('erp_base_businesschoice', 'name'),
                    'ordered_unit': ('erp_base_unit', 'name'),
                    'required_raw_unit': ('erp_base_unit', 'name'),
                    'default_route': ('erp_base_routeversion', 'version'),
                    'approved_recipe': ('erp_sampling_recipeversion', 'version'),
                    'price_unit': ('erp_base_unit', 'name')},
 'SalesLineRequirement': {'order_line': ('erp_sales_salesorderline', 'line_number')},
 'SalesOrderChange': {'order': ('erp_sales_salesorder', 'number'), 'confirmed_by': ('erp_base_employee', 'name')},
 'SalesOrderChangeLine': {'change': ('erp_sales_salesorderchange', 'id'),
                          'order_line': ('erp_sales_salesorderline', 'line_number')}}

VIEWSETS = {'CommercialPrice': 'plugins.erp_sales.views.CommercialPriceViewSet',
 'CommercialPriceLine': 'plugins.erp_base.business_api.BusinessViewSet',
 'SalesOrder': 'plugins.erp_sales.views.SalesOrderViewSet',
 'SalesOrderLine': 'plugins.erp_base.business_api.BusinessViewSet',
 'SalesLineRequirement': 'plugins.erp_base.business_api.BusinessViewSet',
 'SalesOrderChange': 'plugins.erp_sales.views.SalesOrderChangeViewSet',
 'SalesOrderChangeLine': 'plugins.erp_base.business_api.BusinessViewSet'}

# Fulfillment resource fields
MODEL_FIELDS.update({'Delivery': 'number document_at customer address_snapshot status delivered_at warehouse_issue',
 'DeliveryLine': 'package_allocation price_unit adopted_price_snapshot price_adoption_snapshot manual_price_reason delivery line_number '
                 'order_line quantity unit unit_price_snapshot',
 'SalesReturn': 'number customer returned_at reason status',
 'SalesReturnLine': 'original_issue_line reopen_order_demand reopen_reason return_order original_delivery_line '
                    'quantity unit receipt_line',
 'CustomerComplaint': 'number customer complained_at content status',
 'CustomerComplaintLine': 'complaint line_number work_card package material order_line delivery_line quantity '
                          'unit content handling_text disposition'})
RELATIONS.update({'Delivery': {'customer': ('erp_base_party', 'name'), 'warehouse_issue': ('erp_warehouse_stockissue', 'number')},
 'DeliveryLine': {'package_allocation': ('erp_warehouse_packageorderallocation', 'id'),
                  'price_unit': ('erp_base_unit', 'name'),
                  'delivery': ('erp_sales_delivery', 'number'),
                  'order_line': ('erp_sales_salesorderline', 'line_number'),
                  'unit': ('erp_base_unit', 'name')},
 'SalesReturn': {'customer': ('erp_base_party', 'name')},
 'SalesReturnLine': {'original_issue_line': ('erp_warehouse_stockissueline', 'line_number'),
                     'return_order': ('erp_sales_salesreturn', 'number'),
                     'original_delivery_line': ('erp_sales_deliveryline', 'line_number'),
                     'unit': ('erp_base_unit', 'name'),
                     'receipt_line': ('erp_warehouse_stockreceiptline', 'line_number')},
 'CustomerComplaint': {'customer': ('erp_base_party', 'name')},
 'CustomerComplaintLine': {'complaint': ('erp_sales_customercomplaint', 'number'),
                           'work_card': ('erp_production_workcard', 'number'),
                           'package': ('erp_warehouse_package', 'code'),
                           'material': ('erp_base_material', 'id'),
                           'order_line': ('erp_sales_salesorderline', 'line_number'),
                           'delivery_line': ('erp_sales_deliveryline', 'line_number'),
                           'unit': ('erp_base_unit', 'name'),
                           'disposition': ('erp_quality_qualitydisposition', 'id')}})
VIEWSETS.update({'Delivery': 'plugins.erp_sales.fulfillment_views.DeliveryViewSet',
 'DeliveryLine': 'plugins.erp_base.business_api.BusinessViewSet',
 'SalesReturn': 'plugins.erp_sales.fulfillment_views.SalesReturnViewSet',
 'SalesReturnLine': 'plugins.erp_base.business_api.BusinessViewSet',
 'CustomerComplaint': 'plugins.erp_sales.fulfillment_views.CustomerComplaintViewSet',
 'CustomerComplaintLine': 'plugins.erp_base.business_api.BusinessViewSet'})
RESOURCE_OPTIONS = options('erp_sales', MODEL_FIELDS, RELATIONS, VIEWSETS)
RESOURCE_OPTIONS['CommercialPrice']['label_field'] = 'number'
RESOURCE_OPTIONS['CommercialPriceLine']['label_field'] = 'version'
RESOURCE_OPTIONS['SalesOrder']['label_field'] = 'number'
RESOURCE_OPTIONS['SalesOrderLine']['label_field'] = 'line_number'
RESOURCE_OPTIONS['SalesLineRequirement']['label_field'] = 'name'
RESOURCE_OPTIONS['SalesOrderChange']['label_field'] = 'id'
RESOURCE_OPTIONS['SalesOrderChangeLine']['label_field'] = 'id'

WORKFLOWS = {'CommercialPrice': {'editable_states': ['draft'],
                     'children': [{'entity': 'erp_sales_commercialpriceline',
                                   'title': '价格明细',
                                   'key': 'price_document',
                                   'atomic': True}],
                     'actions': [{'key': 'confirm', 'title': '确认价格', 'states': ['draft'], 'inputs': []}]},
 'CommercialPriceLine': {},
 'SalesOrder': {'editable_states': ['draft'],
                'children': [{'entity': 'erp_sales_salesorderline', 'title': '颜色规格', 'key': 'order', 'atomic': True},
                             {'entity': 'erp_sales_salesorderchange',
                              'title': '订单变更',
                              'key': 'order',
                              'atomic': False,
                              'parent_states': ['confirmed', 'running']}],
                'actions': [{'key': 'confirm',
                             'title': '确认订单',
                             'states': ['draft'],
                             'inputs': [{'key': 'employee',
                                         'title': '操作员工',
                                         'kind': 'select',
                                         'options': [],
                                         'required': True,
                                         'remote': {'entity': 'erp_base_employee', 'pk': 'id', 'label': 'name'}}]}]},
 'SalesOrderLine': {'children': [{'entity': 'erp_sales_saleslinerequirement',
                                  'title': '技术要求',
                                  'key': 'order_line',
                                  'atomic': True}]},
 'SalesLineRequirement': {},
 'SalesOrderChange': {'editable_states': ['draft'],
                      'children': [{'entity': 'erp_sales_salesorderchangeline',
                                    'title': '变更明细',
                                    'key': 'change',
                                    'atomic': True}],
                      'actions': [{'key': 'confirm',
                                   'title': '确认变更',
                                   'states': ['draft'],
                                   'inputs': [{'key': 'employee',
                                               'title': '操作员工',
                                               'kind': 'select',
                                               'options': [],
                                               'required': True,
                                               'remote': {'entity': 'erp_base_employee', 'pk': 'id', 'label': 'name'}}]}]},
 'SalesOrderChangeLine': {}}
for name, workflow in WORKFLOWS.items():
    RESOURCE_OPTIONS[name]["workflow"] = workflow

from .fulfillment_workflows import WORKFLOWS as FULFILLMENT_WORKFLOWS
for name, workflow in FULFILLMENT_WORKFLOWS.items():
    RESOURCE_OPTIONS[name]["workflow"] = workflow

from plugins.erp_production.workflows import action,at,reason
WORKFLOWS['SalesOrder']['actions'] += [action('complete','确认实际交付完成',['confirmed','running'],[at,reason]),action('close','订单结案',['confirmed','running','completed'],[at,reason]),action('reopen','重新打开订单',['completed','closed'],[reason])]

from .source_resources import RESOURCE_OPTIONS as SOURCE_RESOURCES
RESOURCE_OPTIONS.update(SOURCE_RESOURCES)

from plugins.erp_base.foundation_catalog import configure_resources
configure_resources(RESOURCE_OPTIONS, 'erp_sales')
