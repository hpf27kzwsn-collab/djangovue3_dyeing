from django.core.management.base import BaseCommand
from system.models import Users
from plugins.erp_base.legacy_models import LegacyImportBatch
from plugins.erp_base.legacy_import import import_masters


class Command(BaseCommand):
    help='逐行承接原表，再按明确字段采用通用主档；异常和重复原行不合并。'
    def add_arguments(self,parser):parser.add_argument('batch');parser.add_argument('--actor',required=True)
    def handle(self,*args,**options):
        batch=LegacyImportBatch.objects.get(number=options['batch'])
        counts=import_masters(batch,Users.objects.get(username=options['actor']))
        for source,count in counts.items():
            self.stdout.write(f"{source}: 原行承接 {count['original_rows']} 条；通用主档采用 {count['adopted_rows']} 条；"
                f"仅原形承接 {count['original_only_rows']} 条；本期排除财务字典 {count['excluded_finance']} 条。")
