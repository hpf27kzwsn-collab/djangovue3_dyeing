"""从当前有效旧入口配置生成新办理规则；不执行旧SQL或表达式。"""
import argparse
import json
import re
import gzip
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NUMBER_KINDS = {'DateCode', 'AutoAdd_Time', 'SeriesAndRowNo', 'SheetRowNo', 'RowNo', 'AutoAdd',
                'AutoAdd_Local', 'AutoAdd_LocalPlusPrev', 'AutoAdd_LocalPlusPrev_LEFT', 'Guid', 'FollowSeries'}
JOINED_DETAILS = {'DyeRecipePhase': 'DyeRecipeDetail', 'StuffWeightPhase': 'StuffWeightDetail',
                  'PStuffWeightPhase': 'PStuffWeightDetail'}
LOGIN_KINDS = {'LoginPeople_LoginName', 'LoginPeople_EmpName', 'LoginPeople_EmpID', 'LoginPeople.EmpID',
               'LoginPeople_EmpDeptID', 'LoginPeople_EmpBusinessUnitID', 'LoginPeople_EmpShiftID',
               'LoginPeople_EmpPositionID', 'LoginPeople_EmpShift', 'LoginPeople_EmpDept'}
CONFIG_KEYS = ['FieldKind', 'GenerateTime', 'Prefix', 'EndCode', 'YearCode', 'MonthCode', 'IsUseDayCode',
               'FixedLength', 'YearMonthSplit', 'MonthDaySplit', 'DayQueueSplit', 'DefaultValue',
               'CodeDependentField', 'DateDependentField', 'IsAlone', 'IsEnForceExpress', 'IsRequired', 'IsCopyField']


def build(path):
    data = json.loads(path.read_text(encoding='utf-8-sig'))
    catalog = json.loads((ROOT / 'tools/legacy_models/source_catalog.json').read_text(encoding='utf8'))
    tables = {row['table']: row for row in catalog['tables'] if row['handling'] == 'business_model'
              and row['schema'] == 'dye' and row.get('entry_scope') != 'business_source_only'}
    fields = defaultdict(list)
    for row in data['ui_fields']:
        fields[row['DataTableName']].append(row)
    rules = {}
    entry_catalog=json.loads(gzip.decompress((ROOT/'backend/plugins/erp_base/source_phase6_catalog.json.gz').read_bytes()))
    financial={e['table']['DataTableName'] for e in entry_catalog['entries'] if e['finance']}
    overrides=json.loads((ROOT/'tools/legacy_models/entry_binding_overrides.json').read_text(encoding='utf8'))
    for row in data['ui_tables']:
        name = (row['TableName'] or '').strip().removeprefix('dye.')
        binding='TableName'
        override=overrides['entries'].get(row['DataTableName'])
        if override:
            name=override['table'];binding='explicit_projection_target'
        if not name and row['DataTableName'] not in financial:
            update=re.fullmatch(r'\s*SELECT\s+\*\s+FROM\s+(?:dye\.)?(\w+)\s*',row['UpdateSQL'] or '',re.I)
            if update:
                name=update[1];binding='explicit_UpdateSQL'
        if name not in tables:
            continue
        models = [tables[name]]
        if name in JOINED_DETAILS and JOINED_DETAILS[name].lower() in (row['SQL'] or '').lower():
            models.append(tables[JOINED_DETAILS[name]])
        for spec in models:
            physical = set(spec['fields'])
            active = [field for field in fields[row['DataTableName']] if field['FieldName'] in physical]
            rules.setdefault(spec['module'] + '.' + spec['model'], {})[row['DataTableName']] = {
                'title': row['Alias'] or row['Description'] or spec['title'],
                'master_entry': row['MasterDataTableName'], 'save_updates_stock': row['IsSaveUpdateStock'],
                'write_binding': {'source':binding,'table':name,'original_table':row['TableName'],
                    **({'reason':override['reason']} if override else {})},
                'field_aliases':overrides['field_aliases'].get(row['DataTableName'],{}),
                'number_fields': {field['FieldName']: {key: field[key] for key in CONFIG_KEYS}
                                  for field in active if field['FieldKind'] in NUMBER_KINDS},
                'default_fields': {field['FieldName']: {key: field[key] for key in CONFIG_KEYS}
                                   for field in active if field['FieldKind'] in {'DefaultValue', 'DefaultDate', *LOGIN_KINDS}},
                'formula_fields': {field['FieldName']: {'generate_time': field['GenerateTime'],
                    'enforce': field['IsEnForceExpress'], 'expression': field['Express']}
                    for field in active if field['Express']},
            }
    target = ROOT / 'backend/plugins/erp_base/source_entry_rules.json'
    target.write_text(json.dumps({'captured_at': data['captured_at'], 'models': rules}, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    print(json.dumps({'models_with_entries': len(rules), 'model_entry_bindings': sum(len(entries) for entries in rules.values()),
                      'number_fields': sum(len(rule['number_fields']) for entries in rules.values() for rule in entries.values())}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--evidence', type=Path, required=True)
    build(parser.parse_args().evidence)
