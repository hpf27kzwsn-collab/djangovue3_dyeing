"""在调用者指定的新项目验证库完整试导入P1来源，再逐原行/字段及函数核对。"""
import argparse
import hashlib
import json
import os
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
import django
django.setup()

from django.apps import apps
from django.db import connection
from system.models import Users
from plugins.erp_base import source_foundation as service
from plugins.erp_base.legacy_services import register_snapshot
from plugins.erp_base.source_import import import_table, compare_table, link_relations, source_model


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def verify(args):
    structure = read(args.structure)
    schema = read(ROOT / 'tools/legacy_models/schema.json')
    assert structure['fields'] == schema['fields']
    actor = Users.objects.create_superuser(username='foundation-verification', password=None)
    result = {'scope': '隔离验证库；全部来源逐行逐字段试导入，不是开发历史库采用或切换',
              'database': connection.settings_dict['NAME'], 'completed': False, 'batches': [],
              'schema_verification': {'captured_at': structure['captured_at'], 'tables': len(structure['tables']),
                                      'fields': len(structure['fields']), 'all_field_definitions_match_generator_schema': True}}
    for manifest in [args.shared, args.masters]:
        batch = register_snapshot(manifest, actor)
        tables = list(batch.source_tables.order_by('table_name'))
        item = {'manifest_sha256': hashlib.sha256(manifest.read_bytes()).hexdigest(),
                'tables': [], 'relations': {}}
        for table in tables:
            imported = import_table(table, actor)
            compared = compare_table(table)
            assert imported == compared['rows']
            model = source_model(table)
            compared.update(fields=len(model.SOURCE_FIELDS),
                            legacy_id_rows=model.objects.filter(source_batch=batch, legacy_id__isnull=False).count())
            item['tables'].append(compared)
        item['relations'] = link_relations(batch, [table.table_name for table in tables])
        # 建立FK后再次比较，关联过程不能改原字段。
        for table in tables:
            compare_table(table)
        result['batches'].append(item)

    live = read(args.live)
    for probe in live['units']:
        expected = None if probe['result'] is None else Decimal(str(probe['result']))
        actual = service.convert_unit(probe['source_unit'], probe['destination_unit'], probe['quantity'])
        assert actual == expected, (probe, actual)
    result['unit_probes'] = len(live['units'])
    for probe in live['business_units']:
        actual = service.business_units(probe['EmpID'])
        assert (actual['unit_ids'], actual['unit_names']) == (probe['unit_ids'], probe['unit_names']), probe
    result['employee_probes'] = len(live['business_units'])
    expected_days = service.get_days(date(2024, 2, 28), date(2024, 3, 1))
    for schema in ['dbo', 'dye']:
        actual = [{'days': date.fromisoformat(row['days'][:10])} for row in live['days'] if row['source_schema'] == schema]
        assert actual == expected_days
    assert live['day_numbers'] == [{'first_number': 0, 'last_number': 2047, 'count': 2048}]
    result['date_rows'] = len(live['days'])
    result['date_source_numbers'] = 2048
    result['lookups'] = []
    for probe in live['lookups']:
        table, code, name, kind = service.LOOKUPS[probe['LookupID']]
        assert code == probe['KeyField'] and name == probe['DisplayField']
        model = apps.get_model('erp_base', 'SourceDye'+table)
        assert model.SOURCE_TABLE == probe['DataTableName']
        result['lookups'].append({'lookup': probe['LookupID'], 'key': code, 'display': name,
                                 'rows': len(service.lookup(probe['LookupID'])['rows'])})
    result.update(completed=True, live_sha256=hashlib.sha256(args.live.read_bytes()).hexdigest())
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['shared', 'masters', 'live', 'structure', 'output']:
        parser.add_argument('--'+name, type=Path, required=True)
    verify(parser.parse_args())
