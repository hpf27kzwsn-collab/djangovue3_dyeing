from django.core.management.base import BaseCommand
from system.models import Users
from plugins.erp_base.legacy_services import register_snapshot


class Command(BaseCommand):
    help='核对完整旧资料文件，并登记旧新对照资料批次；不产生业务库存。'
    def add_arguments(self,parser):parser.add_argument('manifest');parser.add_argument('--actor',required=True)
    def handle(self,*args,**options):
        batch=register_snapshot(options['manifest'],Users.objects.get(username=options['actor']))
        self.stdout.write(f'批次 {batch.number}：{batch.table_count} 张表，{batch.row_count} 行，{batch.byte_count} 字节。')
