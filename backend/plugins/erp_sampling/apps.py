from django.apps import AppConfig
from .resource_options import RESOURCE_OPTIONS


class ErpSamplingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plugins.erp_sampling'
    label = 'erp_sampling'
    verbose_name = '打样管理'
    resource_options = RESOURCE_OPTIONS
