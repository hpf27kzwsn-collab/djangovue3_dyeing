"""全量原入口逐公式核验；注册数量与自动/手动执行证据分开。"""
import os,sys,json,gzip,re
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','application.settings')
import django
django.setup()
from django.apps import apps
from plugins.erp_base.source_entry_registry import ENTRY_RULES
from plugins.erp_base.source_phase6_auto_values import generated_fields
from plugins.erp_base.source_phase6_local_values import RULES
from plugins.erp_base.source_phase6_service_values import RULES as SERVICE_RULES
from plugins.erp_base.source_calculations import AGGREGATES
from plugins.erp_base.source_calculation_entries import ENTRY_METHODS


def dedicated_save_path(label,entry,field):
    table=apps.get_model(label).SOURCE_TABLE
    if field in [r[0] for r in AGGREGATES.get(table,[])]:return 'source_services.refresh_totals → source_calculations.aggregate_values'
    if table=='DyeRecipe' and entry in ['BulkDyeRecipe','FinishDyeRecipe','TrialDyeRecipe'] and field=='Cost':
        return 'source_sampling_services.refresh_chain → recipe_cost（保存与两类试算共用）'
    if table=='ProdIn' and entry=='TwistingIn' and field in ['WeightQty','Rolls','LengthQty','NetKg']:
        return 'source_services.refresh_totals → source_entry_calculations.inventory_values'
    if table=='RecordYield' and entry=='QueryRecordCheck' and field=='Dots':return 'source_services.refresh_totals（疵点SumDots）'
    return None


def audit():
    catalog=json.loads(gzip.decompress((ROOT/'backend/plugins/erp_base/source_phase6_catalog.json.gz').read_bytes()))['entries']
    inventory=json.loads((ROOT/'docs/erp-remaining-inventory-20261016.json').read_text(encoding='utf8'))
    original={r['name']:r for r in inventory['axes']['旧界面配置入口']}
    result=[]
    for entry in catalog:
        name=entry['table']['DataTableName'];models=[label for label,rules in ENTRY_RULES.items() if name in rules]
        rows=[]
        for f in entry['fields']:
            if not f['Express']:continue
            rows.append({'field':f['FieldName'],'expression':f['Express'],'generate_time':f['GenerateTime'],
                'targets':[{'model':label,'physical_field':f['FieldName'] in apps.get_model(label).SOURCE_FIELDS,
                    'save_automatic_registered':f['FieldName'] in generated_fields(name,label.split('.')[1]),
                    'dedicated_save_path':dedicated_save_path(label,name,f['FieldName']),
                    'manual_service_entry_available':name in ENTRY_METHODS.get(apps.get_model(label).SOURCE_TABLE,{}),
                    'local_inputs_missing':[x for x in RULES.get(name,{}).get(f['FieldName'],[]) if x not in apps.get_model(label).SOURCE_FIELDS]}
                    for label in models],
                'requires_parent_or_child':bool(re.search(r'\bparent\.|\bchild\(',f['Express'] or '',re.I))})
        result.append({'entry':name,'title':entry['table'].get('Alias'), 'finance':entry['finance'],'models':models,
            'original_status':original.get(name,{}).get('status'),'formulas':rows,
            'development':'本轮列明保存公式已验证；完整入口仍按全量清单' if name in RULES else '完整入口仍按全量清单，不能因有查询/录入路径算完成',
            'historical_reconciliation':'未完成','field_acceptance':'未完成'})
    new=[{'entry':name,'field':field,'inputs':inputs,'models':[label for label,entries in ENTRY_RULES.items() if name in entries]}
        for name,fields in RULES.items() for field,inputs in fields.items()]
    for r in new:
        for label in r['models']:
            model=apps.get_model(label)
            assert r['field'] in model.SOURCE_FIELDS and all(f in model.SOURCE_FIELDS for f in r['inputs']),r
            assert r['field'] in ENTRY_RULES[label][r['entry']]['formula_fields'],r
    nonfinance=[r for r in result if not r['finance']]
    formulas=[f for r in nonfinance for f in r['formulas']]
    followup=[]
    for entry in nonfinance:
        for formula in entry['formulas']:
            targets=formula['targets']
            if any(t['save_automatic_registered'] for t in targets):continue
            category=('未绑定模型' if not targets else '非物理目标' if not any(t['physical_field'] for t in targets)
                      else '父子来源公式' if formula['requires_parent_or_child'] else '本行或SQL函数公式')
            followup.append({'entry':entry['entry'],'category':category,**formula})
    counts={'all_entries':len(result),'nonfinancial_entries':len(nonfinance),'finance_entries':len(result)-len(nonfinance),
        'nonfinancial_bound_entries':sum(bool(r['models']) for r in nonfinance),
        'nonfinancial_formula_entries':sum(bool(r['formulas']) for r in nonfinance),
        'nonfinancial_formulas':len(formulas),'save_registry_formulas':sum(any(t['save_automatic_registered'] for t in f['targets']) for f in formulas),
        'outside_save_registry_formulas':sum(not any(t['save_automatic_registered'] for t in f['targets']) for f in formulas),
        'new_local_formula_entries':len(RULES),'new_local_formulas':len(new)}
    service_formulas=[{'table':table,'entry':entry,'field':target,'inputs':inputs} for table,entries in SERVICE_RULES.items()
                      for entry,targets in entries.items() for target,inputs in targets.items()]
    paths=Counter('统一保存登记' if any(t['save_automatic_registered'] for t in f['targets'])
        else '另有明确自动汇总服务' if any(t['dedicated_save_path'] for t in f['targets'])
        else '本轮尚未定位自动路径' for f in formulas)
    data={'counts':counts,'new_local_formulas':new,'entries':result,
        'service_formula_registrations':service_formulas,'execution_path_counts':dict(paths),
        'outside_registry_categories':dict(Counter(f['category'] for f in followup)),
        'outside_registry_followup':followup,
        'note':'统一登记之外另追踪明确自动汇总路径；路径登记不是整入口或全部浏览器验收。manual_service_entry_available只说明入口有专用手动服务，不保证覆盖该字段。尚未定位不等于未实现。所有原入口保留，零公式亦登记。'}
    (ROOT/'docs/erp-phase6-entry-formula-audit-20261017.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(counts)


if __name__=='__main__':audit()
