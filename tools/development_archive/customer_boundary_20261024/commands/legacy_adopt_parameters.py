"""采用只读取得的明确业务参数；不连接旧库。"""
import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.dateparse import parse_datetime
from system.models import Users
from plugins.erp_base.business import persist, snapshot, record
from plugins.erp_base.source_context import SourceBusinessParameter, SourceDocumentContext


class Command(BaseCommand):
    help = '按原ParamName采用已保存的旧业务参数值'

    def add_arguments(self, parser):
        parser.add_argument('--evidence', type=Path, required=True)
        parser.add_argument('--actor', required=True)

    @transaction.atomic
    def handle(self, *args, **options):
        evidence = json.loads(options['evidence'].read_text(encoding='utf-8-sig'))
        actor = Users.objects.get(username=options['actor'])
        for original in evidence['parameters']:
            item, created = SourceBusinessParameter.objects.get_or_create(name=original['name'])
            before = {'exists': False} if created else snapshot(item)
            item.value = original['value']
            item.captured_at = parse_datetime(evidence['captured_at'])
            persist(item, actor)
            context,_=SourceDocumentContext.objects.get_or_create(entity=item._meta.label,object_id=item.pk,
                defaults={'entry_name':'parameter_adoption','effects':{}})
            context.effects['parameter_source']={'schema':evidence['schema'],'table':evidence['table'],'field':'ParamName'}
            persist(context,actor)
            record(item, 'adopt_parameter', before, actor, '采用只读核实的旧业务参数')
        self.stdout.write('已采用业务参数：' + str(len(evidence['parameters'])))
