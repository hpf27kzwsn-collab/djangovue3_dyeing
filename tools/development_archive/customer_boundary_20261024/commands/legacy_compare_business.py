import json
from pathlib import Path
from django.core.management.base import BaseCommand
from plugins.erp_base.legacy_models import LegacyImportBatch
from plugins.erp_base.source_import import compare_table


class Command(BaseCommand):
    help='逐表、逐原行身份、逐字段核对完整已承接历史，差异立即定位，不跳过。'

    def add_arguments(self,parser):
        parser.add_argument('batch')
        parser.add_argument('--table',action='append')
        parser.add_argument('--output',required=True)

    def handle(self,*args,**options):
        batch=LegacyImportBatch.objects.get(number=options['batch'])
        tables=batch.source_tables.order_by('schema_name','table_name')
        if options['table']:tables=tables.filter(table_name__in=options['table'])
        report={'batch':batch.number,'completed':False,'tables':[]}
        output=Path(options['output'])
        output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        for table in tables:
            result=compare_table(table)
            report['tables'].append(result)
            output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
            self.stdout.write(f"{result['table']}：{result['rows']}行、{result['field_comparisons']}次字段比较一致。")
        report['completed']=True
        output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
