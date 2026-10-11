from django.apps import AppConfig
from .resource_options import RESOURCE_OPTIONS


class ErpSalesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plugins.erp_sales'
    label = 'erp_sales'
    verbose_name = '销售管理'
    resource_options = RESOURCE_OPTIONS
    exclude_models = ['Delivery', 'DeliveryLine', 'SalesReturn', 'SalesReturnLine',
                      'CustomerComplaint', 'CustomerComplaintLine']
