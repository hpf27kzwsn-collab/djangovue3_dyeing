from django.apps import AppConfig
from .resource_options import RESOURCE_OPTIONS


class ErpProductionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plugins.erp_production'
    label = 'erp_production'
    verbose_name = '生产管理'

    resource_options = RESOURCE_OPTIONS
