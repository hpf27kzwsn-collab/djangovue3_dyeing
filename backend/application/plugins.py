# 扩展应用在这里登记 Django AppConfig；插件路由挂在 api/plugins/<插件名>/ 下。
APPS = [
    'plugins.erp_base.apps.ErpBaseConfig',
    'plugins.erp_sales.apps.ErpSalesConfig',
    'plugins.erp_purchase.apps.ErpPurchaseConfig',
    'plugins.erp_sampling.apps.ErpSamplingConfig',
    'plugins.erp_production.apps.ErpProductionConfig',
    'plugins.erp_warehouse.apps.ErpWarehouseConfig',
    'plugins.erp_quality.apps.ErpQualityConfig',
]
URLS = [('erp','plugins.erp_base.urls')]
# 七模块基础资料、单据动作、查询和旧新对照统一登记。
MODEL_EXCLUDE_APPS = [
    'auth', 'contenttypes', 'sessions', 'captcha',
    'django_celery_beat', 'django_celery_results',
]
INITIALIZERS = ['plugins.erp_base.initialize.load', 'plugins.erp_base.business_initialize.load', 'plugins.erp_base.source_initialize.load', 'plugins.erp_base.foundation_initialize.load', 'system.management_layout.load']
