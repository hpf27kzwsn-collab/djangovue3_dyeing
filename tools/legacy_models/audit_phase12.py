"""复核原字段、原键和实际页面动作；测试结论只从本次成功日志读取。"""
import argparse
from collections import defaultdict
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[2]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--snapshot',type=Path,required=True)
    parser.add_argument('--tests',type=Path,required=True)
    parser.add_argument('--build',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    sys.path.insert(0,str(ROOT/'backend'))
    os.environ['DJANGO_SETTINGS_MODULE']='application.settings'
    import django
    django.setup()
    from django.apps import apps
    from plugins.erp_base.source_documents import SourceRecord
    from core.resources import resource_options
    from system.actions import resource_actions,workflow_actions
    from system.catalog import ENTITIES
    from system.views import view_for

    snapshot=json.loads(args.snapshot.read_text(encoding='utf-8-sig'))
    fields=defaultdict(dict);keys=defaultdict(list)
    for row in snapshot['fields']:fields[row['schema_name'],row['table_name']][row['field_name']]=row
    for row in snapshot['indexes']:
        if row['is_primary_key']:keys[row['schema_name'],row['table_name']].append((row['key_ordinal'],row['field_name']))
    types={'varchar':'CharField','nvarchar':'CharField','char':'CharField','nchar':'CharField',
        'text':'TextField','ntext':'TextField','decimal':'DecimalField','numeric':'DecimalField','money':'DecimalField',
        'float':'FloatField','real':'FloatField','tinyint':'IntegerField','smallint':'IntegerField','int':'IntegerField',
        'bigint':'BigIntegerField','bit':'BooleanField','datetime':'DateTimeField','datetime2':'DateTimeField',
        'smalldatetime':'DateTimeField','date':'DateField','time':'TimeField','image':'BinaryField','binary':'BinaryField',
        'varbinary':'BinaryField','uniqueidentifier':'UUIDField'}
    models=[m for m in apps.get_models() if m._meta.app_label.startswith('erp_')]
    source=[m for m in models if issubclass(m,SourceRecord)]
    schema_checks=[]
    for model in models:
        assert not ({'legacy_id','header_legacy_id'} & {f.name for f in model._meta.fields}),model._meta.label
    for model in source:
        original=fields[model.SOURCE_SCHEMA,model.SOURCE_TABLE]
        assert set(model.SOURCE_FIELDS)==set(original),model._meta.label
        assert tuple(name for _,name in sorted(keys[model.SOURCE_SCHEMA,model.SOURCE_TABLE]))==model.SOURCE_KEY,model._meta.label
        for name,column in original.items():
            field=model._meta.get_field(model.SOURCE_FIELDS[name]);kind=column['data_type']
            expected='TextField' if kind in ['varchar','nvarchar','char','nchar'] and column['max_length']==-1 else types[kind]
            assert field.get_internal_type()==expected,(model._meta.label,name,expected)
            assert field.null==column['is_nullable'],(model._meta.label,name,'nullable')
            if expected=='CharField':
                assert field.max_length==column['max_length']//(2 if kind in ['nchar','nvarchar'] else 1),(model._meta.label,name,'length')
            if expected=='DecimalField':
                assert (field.max_digits,field.decimal_places)==(column['precision'],column['scale']),(model._meta.label,name,'decimal')
        schema_checks.append({'model':model._meta.label,'table':model.SOURCE_SCHEMA+'.'+model.SOURCE_TABLE,
            'fields':len(original),'original_key':list(model.SOURCE_KEY),'passed':True})
    actions=[]
    for entity,model in ENTITIES.items():
        options=resource_options(model)
        if 'workflow' not in options:continue
        view=view_for(entity,model)
        registered={entity+':'+key:(verb,url) for key,_,verb,url in resource_actions(entity,view)}
        for action in workflow_actions(entity,view,options['workflow'])['actions']:
            verb,url=registered[action['permission']]
            assert verb==1 and url.endswith('/'+action['key']+'/'),(entity,action['key'])
            actions.append({'entity':entity,'action':action['key'],'permission':action['permission'],'url':url})
    test_log=args.tests.read_text(encoding='utf-8-sig')
    assert re.search(r'^OK\s*$',test_log,re.M),args.tests
    test_count=int(re.search(r'Ran (\d+) tests',test_log)[1])
    build_log=args.build.read_text(encoding='utf-8-sig')
    assert 'vue-tsc --noEmit' in build_log and 'built in' in build_log,args.build
    result={'audit_at':datetime.now().astimezone().isoformat(),'schema_snapshot_at':snapshot['captured_at'],
        'schema_snapshot_sha256':hashlib.sha256(args.snapshot.read_bytes()).hexdigest(),
        'scope':'按已取得最新结构快照复核；旧SQL Server本轮停止，不冒充新实库抽取',
        'erp_models':len(models),'source_models':len(source),'original_fields':sum(len(m.SOURCE_FIELDS) for m in source),
        'extra_legacy_id_fields':0,'schema_checks':schema_checks,'registered_page_actions':len(actions),'actions':actions,
        'tests':{'passed':test_count,'failed':0,'log_sha256':hashlib.sha256(args.tests.read_bytes()).hexdigest()},
        'frontend':'vue-tsc + vite passed','build_log_sha256':hashlib.sha256(args.build.read_bytes()).hexdigest(),
        'historical_import_this_audit':0,'field_acceptance_this_audit':False}
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:v for k,v in result.items() if k not in ['actions','schema_checks']},ensure_ascii=False))


if __name__=='__main__':main()
