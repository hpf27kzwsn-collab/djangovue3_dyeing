from django.apps import AppConfig


class ErpProductionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plugins.erp_production'
    label = 'erp_production'
    verbose_name = '生产管理'
