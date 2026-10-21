"""逐项审计本轮43处原SQL及其可见视图依赖，不用首错代替完整清单。"""
import json
import gzip
from pathlib import Path
from collections import defaultdict
from sqlglot import parse_one, exp
from sqlglot.optimizer.scope import traverse_scope

ROOT = Path(__file__).resolve().parents[2]


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def main():
    snapshot = read('.runtime-temp/phase6-live-20261017-current/structure-and-logic.json')
    initial = read('docs/erp-phase6-local-chains-verification-20261017.json')
    support = read('backend/plugins/erp_base/source_phase6_query_support.json')
    catalog = json.loads(gzip.decompress((ROOT / 'backend/plugins/erp_base/source_phase6_catalog.json.gz').read_bytes()))
    entries = {r['table']['DataTableName']: r['table'] for r in catalog['entries']}
    fields = defaultdict(set)
    for row in snapshot['fields']:
        fields[row['table_name'].lower()].add(row['field_name'].lower())
    views = {r['object_name'].lower(): r['definition'] for r in snapshot['modules'] if r['type'].strip() == 'V'}
    results = []
    for item in initial['unresolved_queries']:
        if item['scope'] != '本期保留':
            continue
        name = item['entry']
        missing_objects = set(); missing_fields = set(); external = set(); examined = set()
        def visit(sql, context):
            tree = parse_one(sql, read='tsql')
            if isinstance(tree, exp.Create):
                tree = tree.expression
            for scope in traverse_scope(tree):
                physical = {alias.lower(): source for alias, source in scope.sources.items() if isinstance(source, exp.Table)}
                for table in physical.values():
                    key = table.name.lower()
                    if len(table.parts) > 2:
                        external.add(table.sql(dialect='tsql'))
                    elif key in views:
                        if key not in examined:
                            examined.add(key); visit(views[key], key)
                    elif key not in fields:
                        missing_objects.add(table.sql(dialect='tsql'))
                for column in scope.columns:
                    source = physical.get(column.table.lower()) if column.table else (
                        next(iter(physical.values())) if len(scope.sources) == 1 and len(physical) == 1 else None)
                    if source is not None and len(source.parts) <= 2 and source.name.lower() in fields:
                        if column.name != '*' and column.name.lower() not in fields[source.name.lower()]:
                            missing_fields.add(source.name + '.' + column.name)
        visit(entries[name]['SQL'], name)
        results.append({'entry': name, 'original_first_error_category': item['category'],
            'query_state': support[name]['query_state'], 'missing_objects': sorted(missing_objects),
            'missing_fields': sorted(missing_fields), 'external_sources': sorted(external),
            'examined_views': sorted(examined), 'historical_reconciliation': '未完成', 'field_acceptance': '未完成'})
    assert len(results) == 43
    result = {'source_snapshot_at': snapshot['captured_at'],
        'method': '原SQL直接表来源、限定字段及单源未限定字段，加递归可见视图；多源未限定列和动态客户端填数不推断。外部库存在性由本轮只读sys.databases/sys.servers另核。',
        'entries': results}
    (ROOT / 'docs/erp-phase6-query-dependencies-20261017.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    print(json.dumps({'entries': len(results), 'with_external': sum(bool(r['external_sources']) for r in results),
                      'with_missing_objects': sum(bool(r['missing_objects']) for r in results),
                      'with_missing_fields': sum(bool(r['missing_fields']) for r in results)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
