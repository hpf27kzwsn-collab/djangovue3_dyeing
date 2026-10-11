# 扩展应用在这里登记 Django AppConfig；插件路由挂在 api/plugins/<插件名>/ 下。
APPS = []
URLS = []  # [('inventory', 'plugins.inventory.urls')]
MODEL_EXCLUDE_APPS = ['auth', 'contenttypes', 'sessions', 'captcha', 'django_celery_beat', 'django_celery_results']
INITIALIZERS = []  # ['inventory.initialize.load']，重复运行的应用种子函数
