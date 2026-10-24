from django.core.management.base import BaseCommand
from system.models import Users
from plugins.erp_base.legacy_models import LegacyImportBatch
from plugins.erp_base.source_import import import_table,link_relations


class Command(BaseCommand):
    help='将已登记完整旧来源逐表写入七模块原形业务模型；失败中断，不跳过原行。'
    def add_arguments(self,parser):
        parser.add_argument('batch');parser.add_argument('--actor',required=True);parser.add_argument('--table',action='append')
    def handle(self,*args,**options):
        batch=LegacyImportBatch.objects.get(number=options['batch']);actor=Users.objects.get(username=options['actor'])
        tables=batch.source_tables.order_by('schema_name','table_name')
        if options['table']:tables=tables.filter(table_name__in=options['table'])
        for table in tables:
            count=import_table(table,actor)
            self.stdout.write(f'{table.schema_name}.{table.table_name}: {count} 行完整承接。')
        links=link_relations(batch)
        self.stdout.write('明确主从匹配：'+str(sum(links.values()))+' 项；未匹配原码仍在业务模型，不丢原行。')
