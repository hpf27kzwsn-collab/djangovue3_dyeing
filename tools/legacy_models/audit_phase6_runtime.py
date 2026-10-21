"""按当前原配置列出第六阶段字段与版式实现边界，不把解析或空库查询当完成。"""
import os
import sys
import json
import gzip
import hashlib
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
import django
django.setup()
from django.apps import apps
from plugins.erp_base.source_phase6_api import templates
from plugins.erp_base.source_phase6_entries import catalog, entries
from plugins.erp_base.source_phase6_rendering import requirements, describe
from plugins.erp_base.source_entry_registry import ENTRY_RULES
from plugins.erp_base.source_entry_identity import LOGIN_KINDS
from plugins.erp_base.source_entry_copy import fields as copy_fields
from plugins.erp_base.source_phase6_editors import CONFIG, filter_mapping


def audit():
    base=ROOT/'backend/plugins/erp_base'
    identity=[];copy=[];editors=[];copy_aliases=[]
    for label,rules in ENTRY_RULES.items():
        model=apps.get_model(label)
        for entry,rule in rules.items():
            identity.extend({'model':label,'entry':entry,'field':field,'kind':spec['FieldKind']}
                            for field,spec in rule['default_fields'].items() if spec['FieldKind'] in LOGIN_KINDS)
            copy.extend({'model':label,'entry':entry,'field':field} for field in copy_fields(model,entry))
            copy_aliases.extend({'model':label,'entry':entry,'field':alias,'target':target}
                for alias,target in rule['field_aliases'].items() if target in copy_fields(model,entry))
            editors.extend({'model':label,'entry':entry,'field':field['FieldName'],'kind':field['EditorKind'],'editor_id':field['EditorID']}
                           for field in entries()[entry]['fields'] if field['EditorKind'] in ['Lookup','Lookup_NoCheck','DBCombo','DBCombo_Edit']
                           and field['FieldName'] in model.SOURCE_FIELDS and field['EditorID'])
    layouts=[]
    bound_identity={(r['entry'],r['field']) for r in identity}
    bound_copy={(r['entry'],r['field']) for r in copy}
    bound_copy.update((r['entry'],r['field']) for r in copy_aliases)
    unbound_identity=[];unbound_copy=[]
    for name,entry in entries().items():
        if entry['finance']:continue
        for field in entry['fields']:
            spec={'entry':name,'field':field['FieldName'],'kind':field['FieldKind'],
                  'original_table_name':entry['table']['TableName'],'update_sql':entry['table']['UpdateSQL']}
            if field['FieldKind'] in LOGIN_KINDS and (name,field['FieldName']) not in bound_identity:unbound_identity.append(spec)
            if field['FieldKind'] in ['CopyPrevRow','CopyLastRow'] and (name,field['FieldName']) not in bound_copy:unbound_copy.append(spec)
    for i,row in enumerate(templates()):
        issues=requirements(row)
        layouts.append({'index':i,'report_id':row['RptID'],'title':row['RptTitle'],'runtime_issues':issues,
                        'development':'固定高度填数校样，原显示枚举仍有差异' if not issues else '未完成原版式运行',
                        'historical_reconciliation':'未完成','field_acceptance':'未完成'})
    source_models=[m for m in apps.get_models() if hasattr(m,'SOURCE_FIELDS')]
    physical={m.SOURCE_TABLE:set(m.SOURCE_FIELDS) for m in source_models}
    links=[]
    for index,row in enumerate(CONFIG['field_copy']):
        target=row['DestDataTableName'];field=row['DestFieldName']
        status=('独立财务转单暂缓' if target in ['FAPDetail','FARDetail'] or row['DataTableName'] in ['FARMain','ProdInToAPList','ProdOutToARList'] else
                '原目标表或字段不完整' if not target or not field or target not in physical else
                '最新原表没有此目标字段' if field not in physical[target] else
                '原七列映射已接显式采购转单，旧按钮时机未证明' if row['DataTableName']=='PurNondeliveryList' else
                '原来源视图缺失，物料由明确参数选定或留NULL' if row['DataTableName']=='vwQuoteMDToOrderMD' and field=='FabricID' else
                '原来源视图缺失，已接明确报价头/行替代映射' if row['DataTableName']=='vwQuoteMDToOrderMD' else
                '原字段对应存在，自动转单时机未证明')
        links.append({'index':index,**row,'status':status})
    context_filters=[{'lookup':r['LookupID'],'master':m['MasterFilterField'],'target':m['LookupFilterField'],
                     'original':m['original'],'mapping_source':m['mapping_source'],
                     'active_editor_consumers':[{'entry':name,'field':f['FieldName']} for name,e in entries().items()
                        if not e['finance'] for f in e['fields'] if f['EditorID']==r['LookupID'] and f['EditorKind'] in ['Lookup','Lookup_NoCheck']],
                     'state':'explicit_equality' if m['MasterFilterField'] and m['LookupFilterField'] else 'incomplete_configuration'}
                    for r in CONFIG['lookups'] if r['MasterFilterField'] or r['LookupFilterField'] for m in [filter_mapping(r)]]
    result={'configuration_snapshot_sha256':hashlib.sha256((base/'source_phase6_field_links.json').read_bytes()).hexdigest(),
            'configuration_captured_at':CONFIG['captured_at'],'configuration_mode':CONFIG['mode'],
            'counts':{'identity_model_field_bindings':len(identity),'copy_model_field_bindings':len(copy),
                      'unbound_identity_configurations':len(unbound_identity),'unbound_copy_configurations':len(unbound_copy),
                      'copy_alias_configurations':len(copy_aliases),
                      'editor_model_field_bindings':len(editors),'original_field_copy_rows':len(links),
                      'lookup_definitions':len(CONFIG['lookups']),'lookup_column_rows':len(CONFIG['lookup_columns']),
                      'explicit_context_filters':sum(r['state']=='explicit_equality' for r in context_filters),
                      'incomplete_context_filters':sum(r['state']=='incomplete_configuration' for r in context_filters),
                      'reconstructed_context_filters':sum(r['mapping_source']=='explicit_reconstruction' for r in context_filters),
                      'reconstructed_filters_with_active_editors':sum(r['mapping_source']=='explicit_reconstruction' and bool(r['active_editor_consumers']) for r in context_filters),
                      'data_relation_rows':len(CONFIG['data_relations']),'table_relation_rows':len(CONFIG['table_relations']),
                      'templates':len(layouts),'fixed_proof_templates':sum(not r['runtime_issues'] for r in layouts),
                      'complete_original_templates':0,'whole_entries_completed':0,
                      'historical_import_rows_this_run':0,'whole_entry_historical_reconciled':0,'field_accepted':0},
            'identity_bindings':identity,'copy_bindings':copy,'copy_alias_bindings':copy_aliases,'editor_bindings':editors,
            'unbound_identity_configurations':unbound_identity,'unbound_copy_configurations':unbound_copy,
            'field_copy_status_counts':dict(Counter(r['status'] for r in links)),
            'context_filters':context_filters,'field_copy_rows':links,'templates':layouts}
    path=ROOT/'docs/erp-phase6-runtime-review-20261017.json'
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(result['counts'],ensure_ascii=False));print(result['field_copy_status_counts'])
    return result


if __name__=='__main__':audit()
