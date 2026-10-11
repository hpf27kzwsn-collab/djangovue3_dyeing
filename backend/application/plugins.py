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
# ERP 先接入模型和表结构；确认、采用、库存生效等业务接口在对应服务实现时登记。
MODEL_EXCLUDE_APPS = [
    'auth', 'contenttypes', 'sessions', 'captcha',
    'django_celery_beat', 'django_celery_results',
    'erp_base', 'erp_sales', 'erp_purchase',
    'erp_sampling', 'erp_production', 'erp_warehouse',
]
INITIALIZERS = []  # ['inventory.initialize.load']，重复运行的应用种子函数
