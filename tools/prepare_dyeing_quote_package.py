"""读取只读快照并准备报价xlsx数据；不写入任何业务表。"""
import os
import sys
import json
import hashlib
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.runtime-temp/sales-production-20261022'
sys.path.insert(0, str(ROOT / 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
import django
django.setup()
from django.apps import apps
from system.views import view_for
import system.excel_fields as excel_metadata
from plugins.erp_base.source_excel_history import columns
from plugins.erp_base.foundation_catalog import DEFINITIONS
from plugins.erp_base.business_navigation import RESOURCES
from plugins.erp_base.source_entry_registry import ENTRY_RULES
from system.models import Menu

excel_metadata.relation_options = lambda *args, **kwargs: []
source = WORK / 'source'
manifest_path = source / 'manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
digest = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
tables = {x['table']: x for x in manifest['tables']}
catalog = json.loads((ROOT / 'tools/legacy_models/source_catalog.json').read_text(encoding='utf8'))['tables']
models = {x['table']: apps.get_model(x['module'] + '.' + x['model']) for x in catalog if x['schema'] == 'dye' and x['table'] in tables}
configs = [('FixedPrice','染整报价表头','Quote'),('FixedPriceDetail','染整报价明细','QuoteDetail'),
           ('FixedPriceAtte','染整报价要求','QuoteAtte'),('FixedPriceProcess','染整报价工序',None),
           ('QuoteItemPrice','报价加价项目',None),('QuotePriceAtte','报价要求价格',None),
           ('QuotePriceProcess','报价工序价格',None),('FixedCanRecord','克重报价规则',None),('FixedCanDetail','克重报价规则明细',None),
           ('s_DBComboValue','计价单位_C010','s_DBComboValue'),('s_DBComboValue','服务方式_Z010','s_DBComboValue')]
menus = {m.component_name: m for m in Menu.objects.select_related('parent')}


def menu_path(menu):
    return (menu_path(menu.parent) + ' / ' if menu.parent_id else '') + menu.name


files = []
for index, (table, title, preferred) in enumerate(configs, 1):
    model, meta = models[table], tables[table]
    rows = [json.loads(line) for line in (source / meta['file']).read_text(encoding='utf8').splitlines()]
    assert len(rows) == meta['rows']
    assert set(meta['columns'][i]['field_name'] for i in range(len(meta['columns']))) == set(model.SOURCE_FIELDS)
    entity = model._meta.label_lower.replace('.', '_')
    profile = 'foundation_combo_' + title.rsplit('_', 1)[1] if table == 's_DBComboValue' else ''
    if profile:
        definition = DEFINITIONS[profile]
        rows = [row for row in rows if row['values']['ComboID'] == definition['filters']['old_combo_id']]
    entries = ENTRY_RULES.get(model._meta.label, {})
    assert preferred is None or preferred in entries, (table, preferred)
    entry = preferred or (next(iter(entries)) if len(entries) == 1 else '')
    field_meta = {x['field_name']: x for x in meta['columns']}
    original = []
    for col in columns(model):
        old = next(o for o, n in model.SOURCE_FIELDS.items() if n == col['key'])
        original.append({**col, 'original': old, **field_meta[old]})
    params = {'_foundation': profile} if profile else {}
    view = view_for(entity, model)()
    view.request = SimpleNamespace(user=SimpleNamespace(is_superuser=True,is_authenticated=True,pk=1), method='GET',
                                   path='/api/system/' + entity + '/', query_params=params)
    view.kwargs = {};view.format_kwarg = None
    view.excel_context()
    new_columns = [c for c in view.excel_columns('create') if c['key'] in set(model.SOURCE_FIELDS.values()) or c['key'].startswith('source_parent_') or c['key'] == '_entry']
    menu = menus[profile or entity]
    section = '02配套选项' if profile else '01业务报价'
    base = f'{index:02d}_{title}'
    files.append({'id': index, 'title': title, 'table': 'dye.' + table, 'model': model._meta.label, 'entity': entity,
                  'profile': profile, 'entry': entry, 'rows': rows, 'history_columns': original, 'columns': new_columns,
                  'relations': model.SOURCE_RELATIONS, 'menu_path': menu_path(menu), 'page_path': menu.web_path,
                  'history_file': section + '/已有资料/' + base + '.xlsx', 'new_template': section + '/新增空白模板/' + base + '.xlsx'})
    for row in rows:
        assert all(not isinstance(v, str) or len(v) <= 30000 for v in row['values'].values()), (table, row['row'], '原值超出Excel单元格限制')
pack = {'date': '2026-10-22', 'source_manifest_sha256': digest, 'batch': '染整报价20261022-' + digest[:12],
        'source_tables': len(tables), 'files': files, 'total_rows': sum(len(f['rows']) for f in files)}
(WORK / 'quote-package.json').write_text(json.dumps(pack, ensure_ascii=False, indent=2), encoding='utf8')
print([(f['title'], len(f['rows'])) for f in files], 'total', pack['total_rows'])
