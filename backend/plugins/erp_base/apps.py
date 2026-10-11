from django.apps import AppConfig


class ErpBaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plugins.erp_base'
    label = 'erp_base'
    verbose_name = '基础信息'
