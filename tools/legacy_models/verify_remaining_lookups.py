"""仅指定隔离库：COPY完整核验来源后比较原资料查询，绝不采用到开发业务库。"""
import os, sys, json, hashlib, argparse
import unicodedata
from pathlib import Path
from collections import Counter
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'backend'))
os.environ.update(DJANGO_SETTINGS_MODULE='application.settings',DJANGO_DB_ENGINE='postgresql',
    DJANGO_DB_HOST='127.0.0.1',DJANGO_DB_PORT='5440',DJANGO_DB_USER='erp_test',DJANGO_DB_PASSWORD='',
    DJANGO_DB_NAME='erp_p1_complete_compare_20261016')
import django
django.setup()
from django.db import connection
from django.utils import timezone
from psycopg import sql
from system.models import Users
from plugins.erp_base.legacy_services import register_snapshot
from plugins.erp_base.source_import import source_model, original_values, identity
from plugins.erp_base.source_foundation_queries import LOOKUPS
from plugins.erp_base.source_static_lookup import lookup
from plugins.erp_base.source_quality_reports import rows

BASE=ROOT/'.runtime-temp/erp-phase1-completion-20261016'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def load(manifest):
    actor=Users.objects.create_superuser(username='lookup-verify-'+manifest.parent.name,password=None)
    batch=register_snapshot(manifest,actor)
    evidence=read(manifest);output=[]
    for definition in evidence['tables']:
        table=batch.source_tables.get(table_name=definition['table']); model=source_model(table)
        assert not model.objects.exists(), '隔离表已有记录，不能重复试载入：'+definition['table']
        path=manifest.parent/definition['file']
        with path.open('rb') as stream:
            assert hashlib.file_digest(stream,'sha256').hexdigest()==definition['sha256']
        fields=list(model.SOURCE_FIELDS.values())
        extra=['description','remarks','create_datetime','update_datetime','source_row','source_batch_id']
        now=timezone.now();count=0
        with connection.cursor() as cursor:
            command=sql.SQL('COPY {} ({}) FROM STDIN').format(sql.Identifier(model._meta.db_table),
                sql.SQL(',').join(map(sql.Identifier,fields+extra)))
            with cursor.copy(command) as copier, path.open(encoding='utf8') as stream:
                for line in stream:
                    original=json.loads(line);values=original_values(model,original)
                    copier.write_row([values[f] for f in fields]+['','',now,now,identity(table,original,model),original['row'],batch.pk])
                    count+=1
        assert count==definition['rows']==model.objects.count()
        output.append({'table':definition['table'],'rows':count,'source_sha256':definition['sha256']})
        print('LOADED',definition['table'],count,flush=True)
    (BASE/(manifest.parent.name+'-copy-result.json')).write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf8')


def normalize(value):
    if isinstance(value,bool): return int(value)
    if isinstance(value,(Decimal,float,int)):return format(Decimal(str(value)).normalize(),'f')
    if isinstance(value,dict):return {k:normalize(v) for k,v in value.items()}
    return value


def bag(values):
    return Counter(json.dumps(normalize(v),ensure_ascii=False,sort_keys=True,default=str) for v in values)


def canonical_bag(values):
    return bag([{k:unicodedata.normalize('NFKC',v).rstrip(' ').upper() if isinstance(v,str) else v for k,v in row.items()} for row in values])


def compare():
    proof=read(BASE/'lookup-reference.json');result=[]
    for probe in proof['lookups']:
        spec=LOOKUPS[probe['id']]
        try:
            actual=lookup(spec,'',(),rows)
            status='matched' if probe['ok'] and bag(actual)==bag(probe['rows']) else 'original_error' if not probe['ok'] else 'different'
            if status=='different' and canonical_bag(actual)==canonical_bag(probe['rows']):status='collation_group_match_raw_representative_difference'
            detail={'id':probe['id'],'status':status,'new_rows':len(actual),'old_rows':len(probe.get('rows',[]))}
            if status=='different':
                detail['only_new']=list((bag(actual)-bag(probe['rows'])).items())[:3]
                detail['only_old']=list((bag(probe['rows'])-bag(actual)).items())[:3]
            if not probe['ok']:detail['original_error']={'number':probe['number'],'message':probe['message']}
        except Exception as error:
            detail={'id':probe['id'],'status':'new_error','error':str(error)}
        result.append(detail)
        print(detail['id'],detail['status'],detail.get('new_rows',''),flush=True)
    (BASE/'lookup-comparison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    print(Counter(r['status'] for r in result),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--load',action='store_true');parser.add_argument('--compare',action='store_true')
    parser.add_argument('--manifest',type=Path,default=BASE/'lookup-sources/manifest.json')
    args=parser.parse_args()
    if args.load:load(args.manifest)
    if args.compare:compare()
