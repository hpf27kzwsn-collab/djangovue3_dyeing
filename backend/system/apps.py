from django.apps import AppConfig

class SystemConfig(AppConfig):
    name = 'system'
    verbose_name = '系统管理'

    def ready(self):
        from . import signals
