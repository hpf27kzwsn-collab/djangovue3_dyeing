from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = '整理系统管理与业务选项菜单，保留原接口、模型和既有授权范围'

    @transaction.atomic
    def handle(self, *args, **options):
        from plugins.erp_base.foundation_initialize import load as foundation
        from system.management_layout import load
        foundation()
        result = load()
        self.stdout.write(f"系统管理已整理：{result['groups']}个分组、{result['reused_pages']}个复用入口；未导入业务资料。")
