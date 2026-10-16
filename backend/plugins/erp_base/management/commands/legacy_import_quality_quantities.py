from pathlib import Path
from django.core.management.base import BaseCommand
from system.models import Users
from plugins.erp_quality.quantity_services import import_quantities


class Command(BaseCommand):
    help='完整映射只读抽取的质量报告数量；保留旧erpID、NULL及孤立行，不办理财务业务。'
    def add_arguments(self,parser):
        parser.add_argument('file',type=Path);parser.add_argument('--actor',required=True)
    def handle(self,*args,**options):
        batch=import_quantities(options['file'],Users.objects.get(username=options['actor']))
        self.stdout.write(f'质量数量批次 {batch.pk}，{batch.row_count} 行，SHA256 {batch.sha256}')
