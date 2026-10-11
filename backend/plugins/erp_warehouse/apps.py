from django.apps import AppConfig
from .resource_options import RESOURCE_OPTIONS


class ErpWarehouseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plugins.erp_warehouse'
    label = 'erp_warehouse'
    verbose_name = '仓储管理'
    resource_options = RESOURCE_OPTIONS
