from django.apps import AppConfig


class ErpSalesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plugins.erp_sales'
    label = 'erp_sales'
    verbose_name = '销售管理'
