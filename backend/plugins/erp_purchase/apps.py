from django.apps import AppConfig
from .resource_options import RESOURCE_OPTIONS


class ErpPurchaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plugins.erp_purchase'
    label = 'erp_purchase'
    verbose_name = '采购管理'
    resource_options = RESOURCE_OPTIONS
