"""登记原配置证据与具体归属；只读取保存的快照，不执行旧SQL。"""
import argparse
import json
from pprint import pformat
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def build(snapshot, full_ui):
    catalog = json.loads((ROOT / 'tools/legacy_models/source_catalog.json').read_text(encoding='utf-8'))
    current = json.loads(snapshot.read_text(encoding='utf-8-sig'))
    all_ui = json.loads(full_ui.read_text(encoding='utf-8-sig'))
    specs = {(row['schema'], row['table']): row for row in catalog['tables'] if row['handling'] == 'business_model'}
    # 有效入口直接声明的两组主从；补入真实FK，不把同表查询父项当归属。
    for child_name, parent_name in [('CustomerTSDetail', 'CustomerTS'), ('GrayMaterialDetail', 'GrayMaterial')]:
        child, parent = specs[('dye', child_name)], specs[('dye', parent_name)]
        target = parent['module'] + '.' + parent['model']
        if not any(relation['target'] == target for relation in child['relations']):
            child['relations'].append({'field': 'source_parent_' + str(len(child['relations']) + 1),
                                      'title': '原关联：' + parent_name, 'target': target,
                                      'source_fields': ['Sheetseries'], 'target_fields': ['SheetSeries'],
                                      'evidence': ['2026-10-11有效入口' + child_name + '的MasterDataTableName及RelaFieldNames']})
        for relation in child['relations']:
            if relation['target'] == target:
                relation['source_fields'] = ['Sheetseries']
    (ROOT / 'tools/legacy_models/source_catalog.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    tables = {row['DataTableName']: row for row in current['ui_tables']}
    fields = defaultdict(list)
    for field in current['ui_fields']:
        fields[field['DataTableName']].append(field)
    full_tables = {row['DataTableName']: row for row in all_ui['tables']}
    evidence = []
    for name, table in tables.items():
        spec = specs.get(('dye', table['TableName']))
        if spec is None:
            continue
        hooks = {key: value for key, value in full_tables[name].items()
                 if key.startswith(('Before', 'After')) and value not in [None, '', r'\N']}
        expressions = [field for field in fields[name] if field['Express'] not in [None, '', r'\N']]
        evidence.append({'entry': name, 'table': table['TableName'], 'model': spec['module'] + '.' + spec['model'],
                         'master': table['MasterDataTableName'], 'source_sql': table['SQL'],
                         'hooks': hooks, 'formulas': expressions, 'implementation_status': '待逐项对照'})
    output = ROOT / 'tools/legacy_models/workflow_evidence.json'
    output.write_text(json.dumps({'captured_at': current['captured_at'], 'scope': '已保存有效入口配置中的业务原表；不是全部旧入口上限',
                                 'entries': evidence}, ensure_ascii=False, indent=2), encoding='utf-8')
    # 明确的原主从关系。跨单据引用、记录谱系和自关系不作为可编辑明细归属。
    references = {'OrderDlvApplySheet', 'RecordYield', 'RecordDefect', 'RecordEmp', 'h_EmployeeIORecord', 'z_RevisionDetail'}
    owners = {}
    for spec in specs.values():
        if spec['table'] in references:
            continue
        candidates = [relation for relation in spec['relations']
                      if relation['target'] != spec['module'] + '.' + spec['model']]
        if not candidates:
            continue
        if spec['table'] == 'PurDetail':
            selected = candidates
        else:
            selected = [candidates[0]]
        owners[spec['module'] + '.' + spec['model']] = [
            {'field': relation['field'], 'source_fields': relation['source_fields'], 'target_fields': relation['target_fields'],
             'target': relation['target']} for relation in selected]
    code = '"""已登记的原单据明细归属；原跨单据引用不参与表头编辑冻结。"""\nOWNERS = ' + pformat(owners, width=115, sort_dicts=False) + '\n'
    (ROOT / 'backend/plugins/erp_base/source_ownership.py').write_text(code, encoding='utf-8')
    lines = ['# 旧ERP业务动作与计算复刻台账', '', '生成依据：保存的有效入口配置及原完整配置快照。日期：2026-10-14。', '',
             '台账中的“待逐项对照”表示证据已登记，不表示代码已复刻。空值、注释SQL和原公式均保留证据；旧SQL不执行。', '',
             '| 原入口 | 原表/模型 | 主入口 | 公式数 | 钩子SQL数 | 状态 |', '|---|---|---|---:|---:|---|']
    for row in evidence:
        lines.append(f"| {row['entry']} | {row['table']} / {row['model']} | {row['master']} | {len(row['formulas'])} | {len(row['hooks'])} | 待逐项对照 |")
    lines += ['', '## 主从办理范围', '',
              '已登记主从关系集中到source_ownership.py。PurDetail明确允许三种采购表头之一；记录包装到工卡、质量/人员到包装、订单交付申请到订单等独立事实引用不作编辑归属。原外键与归属关系含义不同，不能只因有外键就冻结所有来源单据。', '',
              '## 仍需补查的入口', '', '未在有效入口快照中登记的业务原表继续在全源表目录中跟踪，不能因没有匹配当前配置而排除。', '']
    documented = {row['table'] for row in evidence}
    lines += [f"- {row['schema']}.{row['table']}：{row['title']}；已建模型，入口动作仍需查证。" for row in specs.values() if row['table'] not in documented]
    (ROOT / 'docs/旧ERP业务动作与计算复刻台账.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({'entries': len(evidence), 'formulas': sum(len(row['formulas']) for row in evidence),
                      'hooks': sum(len(row['hooks']) for row in evidence), 'owned_models': len(owners)}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--snapshot', type=Path, required=True)
    parser.add_argument('--full-ui', type=Path, required=True)
    args = parser.parse_args()
    build(args.snapshot, args.full_ui)
