from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '补齐资源权限登记并应用基础资料分类菜单；不导入业务资料'

    def handle(self, *args, **options):
        call_command('init_data')
        from plugins.erp_base.foundation_catalog import DEFINITIONS
        self.stdout.write(self.style.SUCCESS(f'已应用{len(DEFINITIONS)}个基础资料及原配置入口；业务资料未导入。'))

