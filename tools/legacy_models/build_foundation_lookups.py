"""从只读快照生成原Lookup证据及已逐项翻译的资料选择定义。"""
import argparse
import json
import re
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def build(evidence, live):
    datasets = {row['DataTableName']: row['SQL'] for row in evidence['ui_tables']}
    lookups = {}
    special = {'B001': 'PCustomer', 'A002': 'PCustomer', 'B006': 'HEmployee',
               'B154': 'HEmployee', 'B062': 'PDept', 'B405': 'PGray'}
    adapters=json.loads((ROOT/'backend/plugins/erp_base/source_foundation_lookup_adapters.json').read_text(encoding='utf8'))
    for original in live['lookups']:
        row = dict(original, query=datasets.get(original['DataTableName']), adapter=None)
        condition = re.fullmatch(r"\s*FieldType\s*=\s*'([^']*)'\s*", row['LookupDataFilter'] or '', re.I)
        if row['DataTableName'] == 'p_FieldValid' and condition:
            row['adapter'] = {'table': 'PFieldValid', 'field_type': condition[1]}
        elif row['LookupID'] == 'B005':
            row['adapter'] = {'table': 'PFieldValid', 'field_type': 'Production'}
        elif row['LookupID'] in special:
            row['adapter'] = {'table': special[row['LookupID']]}
        elif row['LookupID'] in adapters:
            adapter=adapters[row['LookupID']]
            original={k:row[k] for k in ['query','LookupDataFilter','KeyField','DisplayField']}
            digest=hashlib.sha256(json.dumps(original,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
            if digest!=adapter['source_sha256']:raise ValueError('原资料查询定义变更，需要重新核对：'+row['LookupID'])
            row.update({k:v for k,v in adapter.items() if k!='source_sha256'})
        lookups[row['LookupID']] = row
    return {'captured_at': evidence['captured_at'], 'lookups': lookups}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--live', type=Path, required=True)
    args = parser.parse_args()
    result = build(*[json.loads(path.read_text(encoding='utf-8-sig')) for path in [args.evidence, args.live]])
    target = ROOT / 'backend/plugins/erp_base/source_foundation_lookups.json'
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
    print(json.dumps({'definitions': len(result['lookups']), 'implemented': sum(r['adapter'] is not None for r in result['lookups'].values())}))
