"""固定第三组逐入口运行证据。空结果、参数缺口和错误分别登记，不计作通过。"""
import os,sys,json,hashlib
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'backend'));os.environ.setdefault('DJANGO_SETTINGS_MODULE','application.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory,force_authenticate
from rest_framework.request import Request
from plugins.erp_base import source_phase6_entries as entries
from plugins.erp_base.source_phase6_projection_context import ProjectionContext
from plugins.erp_base.source_phase6_projection_formulas import calculate
from plugins.erp_base.source_phase6_projection_overrides import projections
from collections import Counter


EXPECTED={
    'ColorNumToQuotePrice':('CONT-COLOR',{'RGB__formula':[-65536]}),
    'qry_DyeColorNum':('CONT-COLOR',{'RGB__formula':[-65536]}),
    'DyeDipsRecordPhaseDetail':('CONT-DIP',{'AmountA__formula':[60,60,-90],'AmountB__formula':[None]*3,'AmountC__formula':[0]*3,'AmountD__formula':[-60,-60,90],'AmountE__formula':[60,60,-90]}),
    'p_MachineFaultClass':('CONT',{'value__formula':['机械/泵/漏液']}),
    'ProdOutRecord':('CONT-PROD',{'RollNo2__formula':['CONT-DUP']*3}),
    'ProdOutRecordUpdate':('CONT-PROD',{'RollNo2__formula':['CONT-DUP']*3}),
    'GrayStockToCheck':('CONT-G',{'AdjustRolls__formula':[0],'AdjustPacks__formula':[0],'AdjustWeightQty__formula':[0],'AdjustLengthQty__formula':[0],'realweightqty':[30],'realrolls':[3]}),
    'ProdStocktoCheck':('CONT-G',{'AdjustRolls__formula':[0],'AdjustWeightQty__formula':[0],'AdjustLengthQty__formula':[0],'realweightqty':[30],'realrolls':[3]}),
    'SemiStockToCheck':('CONT-G',{'AdjustRolls__formula':[0],'AdjustWeightQty__formula':[0],'AdjustLengthQty__formula':[0],'realweightqty':[30],'realrolls':[3]}),
    'qry_SemiStockToCarryMaterial':('CONT-G',{'UpWeightQty__formula':[0]}),
    'qry_QuoteRelaRecipe':('CONT-RECIPE',{'Amount__formula':[6,6,-9]}),
    'StuffInDetail':('CONT-STUFFIN',{'StuffCode__formula':['CONTB-S']}),
}


def check_expected(name,result):
    if name not in EXPECTED:return []
    marker,fields=EXPECTED[name]
    rows=[r for r in result['rows'] if marker in r]
    names=[c['name'].lower() for c in result['columns']];checks=[]
    for field,expected in fields.items():
        positions=[i for i,n in enumerate(names) if n==field.lower()]
        actual=[r[positions[0]] for r in rows] if len(positions)==1 else []
        checks.append({'field':field,'fixture':marker,'expected':expected,'actual':actual,'passed':len(positions)==1 and Counter(actual)==Counter(expected)})
    return checks


def main():
    from django.conf import settings
    if settings.DATABASES['default']['NAME']!='erp_phase6_browser_20261017':raise RuntimeError('本核验只对隔离浏览器测试库运行')
    baseline=json.loads((ROOT/'docs/erp-phase6-six-groups-baseline-20261017.json').read_text(encoding='utf8'))
    request=APIRequestFactory().get('/');force_authenticate(request,user=get_user_model().objects.get(username='phase6-browser'))
    reader=entries.reader(Request(request));groups={}
    for item in baseline['groups']['3']:groups.setdefault(item['entry'],[]).append(item)
    results=[]
    for name,items in groups.items():
        row={'entry':name,'ids':[i['id'] for i in items],'fields':[i['field'] for i in items]}
        if name.startswith('ImpairmentPayouts'):
            row['state']='财务暂缓';results.append(row);continue
        try:
            params=entries.query_parameters(name)
            if params:
                row.update(state='缺本入口参数样例',required_parameters=params)
            else:
                result=entries.run(name,{},reader,load_records=True,additional_projection=projections(name))
                fields=[f for f in entries.definition(name)['fields'] if f['FieldName'] in row['fields']]
                calculated=calculate(result,fields,ProjectionContext(result,reader,{},True))
                row.update(state='空结果，未验证数据分支' if not result['rows'] else '非空有逐行差异' if calculated['formula_issues'] else '非空固定公式运行通过',
                    query_count=len(result['rows']),calculations=calculated['formula_calculations'],issues=calculated['formula_issues'],
                    source_resolutions=calculated['formula_source_resolutions'])
                row['expected_value_checks']=check_expected(name,calculated)
                full=calculate(result,entries.definition(name)['fields'],ProjectionContext(result,reader,{},True))
                row['full_entry_trial_issues']=full['formula_issues']
                row['full_entry_trial_field_count']=len(full['formula_calculations'])
                if any(not check['passed'] for check in row['expected_value_checks']):row['state']='非空预期值不符'
        except Exception as error:
            row.update(state='运行失败，原入口保留',error_type=type(error).__name__,error=str(error))
        results.append(row)
    output={'captured_at':datetime.now().astimezone().isoformat(),'database':'erp_phase6_browser_20261017',
        'baseline_sha256':hashlib.sha256((ROOT/'docs/erp-phase6-six-groups-baseline-20261017.json').read_bytes()).hexdigest(),
        'entries':results,'historical_reconciliation':'未完成；本文件是合成测试库入口运行结果','field_acceptance':'未现场验收'}
    (ROOT/'docs/erp-phase6-projection-entry-verification-20261017.json').write_text(json.dumps(output,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf8')
    print(dict(Counter(r['state'] for r in results)))
    for r in results:
        if r['state'] in ['非空有逐行差异','运行失败，原入口保留','非空预期值不符']:print(r['entry'],str(r.get('issues',r.get('error')))[:500],str([c for c in r.get('expected_value_checks',[]) if not c['passed']]))

if __name__=='__main__':main()
