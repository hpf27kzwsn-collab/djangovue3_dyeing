from django.core.management.base import BaseCommand
from system.models import Users
from plugins.erp_base.legacy_models import LegacyImportBatch
from plugins.erp_base.legacy_import import import_masters


class Command(BaseCommand):
    help='按明确旧字段导入主档标量；其余字段与业务事实保持完整归档。'
    def add_arguments(self,parser):parser.add_argument('batch');parser.add_argument('--actor',required=True)
    def handle(self,*args,**options):
        batch=LegacyImportBatch.objects.get(number=options['batch'])
        counts=import_masters(batch,Users.objects.get(username=options['actor']))
        for source,count in counts.items():self.stdout.write(f'{source}: {count} 条明确主档记录。')
