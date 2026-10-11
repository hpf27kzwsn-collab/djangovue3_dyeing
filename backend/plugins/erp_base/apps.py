from django.apps import AppConfig
from .resource_options import RESOURCE_OPTIONS


class ErpBaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plugins.erp_base'
    label = 'erp_base'
    verbose_name = '基础信息'
    resource_options = RESOURCE_OPTIONS
