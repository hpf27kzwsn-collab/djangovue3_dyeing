"""指定隔离新库：本批九张完整来源逐字段核对及原函数/101项资料查询对照。"""
import argparse
from collections import Counter
from datetime import date
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
import django
django.setup()
from django.db import connection
from system.models import Users
from plugins.erp_base import source_foundation_functions as functions
from plugins.erp_base import source_foundation_queries as queries
from plugins.erp_base.legacy_services import register_snapshot
from plugins.erp_base.source_import import import_table, compare_table, link_relations, source_model


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def normalize(value):
    if isinstance(value, (float, Decimal)):
        return format(Decimal(str(value)).normalize(), 'f')
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in value.items()}
    return value


def bag(rows):
    return Counter(json.dumps(normalize(row), ensure_ascii=False, sort_keys=True) for row in rows)


def verify(args):
    live, evidence = read(args.live), read(args.structure)
    assert evidence['fields'] == read(ROOT/'tools/legacy_models/schema.json')['fields']
    actor = Users.objects.create_superuser(username='foundation-functions-verification', password=None)
    result = {'scope': '本项目隔离核验库；完整试导入、未采用到开发历史库或正式切换库存',
              'database': connection.settings_dict['NAME'], 'captured_at': live['captured_at'],
              'sql_access': 'SELECT only', 'completed': False, 'tables': [],
              'all_latest_field_definitions_match': True, 'lookups': []}
    for manifest in [args.sources, args.masters]:
        batch = register_snapshot(manifest, actor)
        for table in batch.source_tables.order_by('table_name'):
            count = import_table(table, actor)
            compared = compare_table(table)
            assert count == compared['rows']
            compared['source_rows'] = source_model(table).objects.filter(source_batch=batch).count()
            result['tables'].append(compared)
        link_relations(batch)
        for table in batch.source_tables.all():
            compare_table(table)
    errors = 0
    for probe in live['probes']:
        try:
            actual = functions.FUNCTIONS[probe['name']](probe['input'])
        except (ValueError, OverflowError):
            assert not probe['ok'], probe['name']
            errors += 1
        else:
            assert probe['ok'], probe['name']
            expected = probe['value']
            if isinstance(actual, Decimal):
                expected = Decimal(str(expected))
            assert actual == expected, probe['name']
    for probe in live['dates']:
        actual = functions.continuous_dates(date(2024, 2, 29), probe['kind'], probe['prev'], probe['next'])
        for row in actual:
            row['DataDate'] = row['DataDate'].isoformat()
        assert actual == probe['rows'], probe['kind']
    for probe in live['parameters']:
        assert queries.parameter_value(probe['ParamName']) == probe['result'], probe['ParamName']
    for probe in live['lookup_results']:
        actual = queries.lookup(probe['lookup'], other_fields=probe['other_fields'])
        assert bag(actual['rows']) == bag(probe['rows']), ('lookup differs', probe['lookup'])
        result['lookups'].append({'lookup': probe['lookup'], 'rows': len(actual['rows']),
                                  'other_fields': probe['other_fields'], 'all_rows_equal': True})
    combo_groups = {}
    for row in live['combos']:
        combo_groups.setdefault(row['ComboID'], []).append({k: row[k] for k in ['index', 'id', 'text']})
    for name, original in combo_groups.items():
        assert bag(queries.combo(name, '')['rows']) == bag(original), ('combo differs', name)
    result.update(scalar_probes=len(live['probes']), expected_scalar_errors=errors,
                  date_groups=len(live['dates']), date_rows=sum(len(p['rows']) for p in live['dates']),
                  parameter_probes=len(live['parameters']), combo_groups=len(combo_groups), combo_rows=len(live['combos']),
                  lookup_definitions=len(queries.LOOKUPS), implemented_lookups=len(result['lookups']),
                  pending_lookups=[name for name, spec in queries.LOOKUPS.items() if spec['adapter'] is None],
                  live_sha256=hashlib.sha256(args.live.read_bytes()).hexdigest(), completed=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
    print(json.dumps({key: value for key, value in result.items() if key not in ['lookups', 'pending_lookups']}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['sources', 'masters', 'live', 'structure', 'output']:
        parser.add_argument('--'+name, type=Path, required=True)
    verify(parser.parse_args())
