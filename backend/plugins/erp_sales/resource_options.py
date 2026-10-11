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
