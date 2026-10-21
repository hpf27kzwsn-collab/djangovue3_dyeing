"""在指定隔离测试库核验全部旧入口。失败逐条列出，不改为成功或空结果。"""
import argparse
import json
import os
import sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]


def audit(output):
    from django.db import connection,transaction
    from django.apps import apps
    from plugins.erp_base.source_phase6_entries import entries,query_parameters,run,catalog
    from plugins.erp_base.source_entry_registry import ENTRY_RULES
    from plugins.erp_base.source_calculation_entries import ENTRY_METHODS
    if not connection.settings_dict['NAME'].startswith('test_'):
        raise ValueError('此执行核验只允许指定的test_隔离测试库。')
    def reader(name,module):return apps.get_model(module+'.SourceDye'+name).objects.all()
    result=[]
    for name,spec in entries().items():
        row={'name':name,'title':spec['table']['Alias'],'kind':spec['table']['Kind'],
            'field_count':len(spec['fields']),'models':[model for model,rules in ENTRY_RULES.items() if name in rules],
            'hooks':{k:v for k,v in spec['table'].items() if k.endswith('SQL') and k.startswith(('Before','After')) and v},
            'formulas':[f for f in spec['fields'] if f['Express']]}
        if spec['finance']:row['query_state']='finance'
        else:
            try:
                params=query_parameters(name);row['parameters']=params
                with transaction.atomic():
                    with connection.cursor() as cursor:
                        cursor.execute('SET LOCAL transaction_read_only=on')
                        cursor.execute('SET LOCAL statement_timeout=10000')
                    table=run(name,{p:None for p in params},reader,True,True)
                    row.update(query_state='executed_empty_fixture',columns=table['columns'],row_count=table['count'])
                    transaction.set_rollback(True)
            except Exception as error:
                row.update(query_state='unresolved',error_type=type(error).__name__,error=str(error)[:3000])
        result.append(row)
        if len(result)%100==0:print(len(result),dict(Counter(r['query_state'] for r in result)),flush=True)
    report={'snapshot_sha256':catalog()['snapshot_sha256'],'database':connection.settings_dict['NAME'],
        'verification':'隔离库空业务夹具执行；不代表真实历史对账或现场验收',
        'counts':dict(Counter(r['query_state'] for r in result)),'entries':result}
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(report['counts'])


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--database',required=True)
    args=parser.parse_args();sys.path.insert(0,str(ROOT/'backend'));os.environ['DJANGO_SETTINGS_MODULE']='application.settings'
    os.environ.update(DJANGO_DB_ENGINE='postgresql',DJANGO_DB_HOST='127.0.0.1',DJANGO_DB_PORT='5440',DJANGO_DB_USER='erp_test',DJANGO_DB_PASSWORD='',DJANGO_DB_NAME=args.database)
    import django;django.setup();audit(args.output)
