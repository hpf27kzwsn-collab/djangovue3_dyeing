from django.apps import AppConfig
from .resource_options import RESOURCE_OPTIONS


class ErpQualityConfig(AppConfig):
    default_auto_field='django.db.models.BigAutoField'
    name='plugins.erp_quality'
    label='erp_quality'
    verbose_name='质量管理'
    resource_options=RESOURCE_OPTIONS
