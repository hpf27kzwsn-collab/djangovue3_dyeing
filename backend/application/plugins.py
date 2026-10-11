# 扩展应用在这里登记 Django AppConfig；插件路由挂在 api/plugins/<插件名>/ 下。
APPS = [
    'plugins.erp_base.apps.ErpBaseConfig',
    'plugins.erp_sales.apps.ErpSalesConfig',
    'plugins.erp_purchase.apps.ErpPurchaseConfig',
    'plugins.erp_sampling.apps.ErpSamplingConfig',
    'plugins.erp_production.apps.ErpProductionConfig',
    'plugins.erp_warehouse.apps.ErpWarehouseConfig',
]
URLS = []  # [('inventory', 'plugins.inventory.urls')]
# 基础信息已接入页面和业务保存；其余应用在对应批次实现业务动作时登记。
MODEL_EXCLUDE_APPS = [
    'auth', 'contenttypes', 'sessions', 'captcha',
    'django_celery_beat', 'django_celery_results',
    'erp_sales', 'erp_purchase',
    'erp_sampling', 'erp_production', 'erp_warehouse',
]
INITIALIZERS = ['plugins.erp_base.initialize.load']
