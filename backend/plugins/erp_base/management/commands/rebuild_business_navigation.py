from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = '应用销售及工艺/排产/生产入口归属，不采用或导入业务数据'

    def handle(self, *args, **options):
        call_command('rebuild_management_menus')
        self.stdout.write('染整订单、报价与三类生产入口已整理；未导入业务数据。')
