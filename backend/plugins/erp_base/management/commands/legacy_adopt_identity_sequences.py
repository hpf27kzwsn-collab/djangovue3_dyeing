"""采用实际SQL身份列高水位，空表和删除后的号码同样保留。"""
import json
from pathlib import Path
from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import transaction
from system.models import Users
from plugins.erp_base.business import locked, persist, record, snapshot
from plugins.erp_base.legacy_models import LegacyImportBatch
from plugins.erp_base.legacy_services import digest
from plugins.erp_base.source_import import entries
from plugins.erp_base.source_sequences import SourceIdentitySequence


class Command(BaseCommand):
    help = '从已登记来源清单采用真实SQL自增高水位；不降号，不改原业务字段。'

    def add_arguments(self, parser):
        parser.add_argument('batch')
        parser.add_argument('--manifest', required=True)
        parser.add_argument('--actor', required=True)

    @transaction.atomic
    def handle(self, *args, **options):
        batch = LegacyImportBatch.objects.get(number=options['batch'])
        path = Path(options['manifest'])
        if digest(path) != batch.manifest_sha256:
            raise ValueError('身份列清单必须来自本批已登记的完整来源。')
        manifest = json.loads(path.read_text(encoding='utf-8-sig'))
        actor = Users.objects.get(username=options['actor'])
        tables = {(row['schema'], row['table']): row for row in entries() if row['handling'] == 'business_model'}
        adopted = 0
        for identity in manifest['identities']:
            key = (identity['schema_name'], identity['table_name'])
            if key not in tables or identity['last_value'] is None:
                continue
            spec = tables[key]
            model = apps.get_model(spec['module'], spec['model'])
            field = model.SOURCE_FIELDS[identity['field_name']]
            if field not in model.SOURCE_IDENTITIES:
                raise ValueError('该原字段未声明为实际SQL自增列：' + model._meta.label + '.' + field)
            value = int(identity['last_value'])
            sequence, created = SourceIdentitySequence.objects.get_or_create(namespace=model._meta.label + '.' + field,
                defaults={'last_number': value, 'creator': actor, 'modifier': actor})
            sequence = locked(sequence)
            before = {'exists': False} if created else snapshot(sequence)
            if created or sequence.last_number < value:
                sequence.last_number = value
                persist(sequence, actor)
                record(sequence, 'adopt_sql_identity', before, actor, '采用原SQL身份列真实高水位，保留已删除号码')
            adopted += 1
        self.stdout.write(f'已核对采用{adopted}个实际自增字段高水位；已有更高号码保持不变。')
