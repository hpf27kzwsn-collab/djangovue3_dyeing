from django.core.management.base import BaseCommand
from plugins.erp_base.legacy_models import LegacyImportBatch
from plugins.erp_base.source_import import link_relations


class Command(BaseCommand):
    help = '为已完整承接的原行补明确唯一匹配关系，不重新导入或计算原字段。'

    def add_arguments(self, parser):
        parser.add_argument('batch')
        parser.add_argument('--table', action='append')

    def handle(self, *args, **options):
        batch = LegacyImportBatch.objects.get(number=options['batch'])
        if options['table']:
            for name in options['table']:
                batch.source_tables.get(table_name=name)
        links = link_relations(batch, options['table'])
        for name, count in links.items():
            self.stdout.write(f'{name}: 新增{count}项明确关系。')
