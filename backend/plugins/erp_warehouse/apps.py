from django.apps import AppConfig


class ErpWarehouseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plugins.erp_warehouse'
    label = 'erp_warehouse'
    verbose_name = '仓储管理'
