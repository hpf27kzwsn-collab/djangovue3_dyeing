from django.apps import AppConfig


class ErpSamplingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plugins.erp_sampling'
    label = 'erp_sampling'
    verbose_name = '打样管理'
