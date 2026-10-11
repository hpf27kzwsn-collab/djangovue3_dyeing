from django.apps import AppConfig


class ErpPurchaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plugins.erp_purchase'
    label = 'erp_purchase'
    verbose_name = '采购管理'
