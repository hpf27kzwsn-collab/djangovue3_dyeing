"""只读结构快照与当前Django声明逐项比较，生成关系数据核验SELECT计划。"""
import json,os,sys,re,hashlib
from pathlib import Path
from collections import defaultdict,Counter
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'backend'));os.environ.setdefault('DJANGO_SETTINGS_MODULE','application.settings')
import django
django.setup()
from django.apps import apps
from django.db.models import NOT_PROVIDED
from generate_models import original_default
OUT=ROOT/'.runtime-temp/model-compare-live-20261018'
def save(name,data): (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2,default=str),encoding='utf8')
def key(r):return (r['schema_name'],r['table_name'])
def q(v):return '['+v.replace(']',']]')+']'
def table(k):return '.'.join(map(q,k))
def signature(sk,tk,sf,tf):return (sk,tk,tuple(x.lower() for x in sf),tuple(x.lower() for x in tf))

live=json.loads((OUT/'structure-and-logic.json').read_text(encoding='utf8'))
catalog=json.loads((ROOT/'tools/legacy_models/source_catalog.json').read_text(encoding='utf8'))
specs={(r['schema'],r['table']):r for r in catalog['tables']}
allmodels=list(apps.get_models());models=[m for m in allmodels if hasattr(m,'SOURCE_FIELDS')]
bytable=defaultdict(list)
for m in models:bytable[m.SOURCE_SCHEMA,m.SOURCE_TABLE].append(m)
fields=defaultdict(dict);keys=defaultdict(list);indexes=defaultdict(list);ids={}
for r in live['fields']:fields[key(r)][r['field_name']]=r
for r in live['indexes']:
    indexes[key(r)].append(r)
    if r['is_primary_key']:keys[key(r)].append((r['key_ordinal'],r['field_name']))
for r in live['identities']:ids[key(r),r['field_name']]=(int(r['seed']),int(r['increment']))
types={'varchar':'CharField','nvarchar':'CharField','char':'CharField','nchar':'CharField','text':'TextField','ntext':'TextField','decimal':'DecimalField','numeric':'DecimalField','money':'DecimalField','float':'FloatField','real':'FloatField','tinyint':'IntegerField','smallint':'IntegerField','int':'IntegerField','bigint':'BigIntegerField','bit':'BooleanField','datetime':'DateTimeField','datetime2':'DateTimeField','smalldatetime':'DateTimeField','date':'DateField','time':'TimeField','image':'BinaryField','binary':'BinaryField','varbinary':'BinaryField','uniqueidentifier':'UUIDField'}
field_results=[];table_results=[];model_inventory=[];relations=[]
for m in allmodels:
    record={'model':m._meta.label,'table':m._meta.db_table,'erp':m._meta.app_label.startswith('erp_'),'source':hasattr(m,'SOURCE_FIELDS'),'fields':[],'indexes':[str(i) for i in m._meta.indexes],'index_specs':[{'fields':i.fields,'expressions':[str(e) for e in i.expressions]} for i in m._meta.indexes],'constraints':[str(c) for c in m._meta.constraints]}
    for f in [*m._meta.fields,*m._meta.many_to_many]:
        record['fields'].append({'name':f.name,'column':f.column,'type':f.get_internal_type(),'null':f.null,'primary_key':f.primary_key,'unique':f.unique,'max_length':f.max_length,'max_digits':getattr(f,'max_digits',None),'decimal_places':getattr(f,'decimal_places',None),'default':None if f.default is NOT_PROVIDED else str(f.default),'target':f.remote_field.model._meta.label if f.is_relation else None,'delete':getattr(getattr(f.remote_field,'on_delete',None),'__name__',None)})
    record['unique_together']=m._meta.unique_together
    model_inventory.append(record)
for t in live['tables']:
    k=key(t);ms=bytable[k];spec=specs.get(k,{})
    tr={'table':'.'.join(k),'models':[m._meta.label for m in ms],'fields':len(fields[k]),'handling':spec.get('handling','未登记'),'reason':spec.get('reason',''),'issues':[],'primary_key':[n for _,n in sorted(keys[k])],'indexes':len({r['index_name'] for r in indexes[k]}),'unique_indexes':len({r['index_name'] for r in indexes[k] if r['is_unique']})}
    table_results.append(tr)
    if not ms:continue
    if len(ms)!=1:tr['issues'].append('多模型对应同一旧表')
    for m in ms:
        tr['extra_source_fields']=sorted(set(m.SOURCE_FIELDS)-set(fields[k]))
        tr['key_metadata_equal']=list(m.SOURCE_KEY)==tr['primary_key']
        tr['new_pk']=m._meta.pk.name
        if not tr['key_metadata_equal']:tr['issues'].append('原键元数据不同')
        for name,col in fields[k].items():
            r={'table':'.'.join(k),'original':name,'model':m._meta.label,'old':col,'differences':[]}
            field_results.append(r)
            if name not in m.SOURCE_FIELDS:r['differences'].append('缺少原字段');continue
            f=m._meta.get_field(m.SOURCE_FIELDS[name]);typ=col['data_type'];expected=types.get(typ)
            if typ in ['varchar','nvarchar','char','nchar'] and col['max_length']==-1:expected='TextField'
            r['field']=f.name;r['new']={'type':f.get_internal_type(),'null':f.null,'max_length':f.max_length,'precision':getattr(f,'max_digits',None),'scale':getattr(f,'decimal_places',None),'primary_key':f.primary_key,'unique':f.unique,'default':str(f.default) if f.default is not NOT_PROVIDED else None,'db_collation':getattr(f,'db_collation',None)}
            if f.get_internal_type()!=expected:r['differences'].append('类型映射不同')
            if f.null!=col['is_nullable']:r['differences'].append('NULL定义不同')
            if expected=='CharField' and f.max_length!=col['max_length']//(2 if typ in ['nvarchar','nchar'] else 1):r['differences'].append('长度不同')
            if expected=='DecimalField' and (f.max_digits,f.decimal_places)!=(col['precision'],col['scale']):r['differences'].append('精度不同')
            wanted=original_default(col['default_definition']) if col['default_definition'] is not None else None
            r['default_service_equal']=m.SOURCE_DEFAULTS.get(f.name)==wanted
            if not r['default_service_equal']:r['differences'].append('默认值服务元数据不同')
            r['identity_service_equal']=((f.name in m.SOURCE_IDENTITIES)==col['is_identity'] and (not col['is_identity'] or m.SOURCE_IDENTITY_RULES[f.name]==ids[k,name]))
            if not r['identity_service_equal']:r['differences'].append('自增服务元数据不同')
            r['collation_metadata_equal']=m.SOURCE_COLLATIONS.get(f.name)==col['collation_name']
            if not r['collation_metadata_equal']:r['differences'].append('排序规则元数据不同')
            if col['is_computed']:r['differences'].append('旧计算列需另核执行语义')
        for rel in m.SOURCE_RELATIONS:
            p=apps.get_model(rel['target']);f=m._meta.get_field(rel['field']);tk=p.SOURCE_SCHEMA,p.SOURCE_TABLE
            validity=[]
            for n in rel['source_fields']:
                if n not in fields[k]:validity.append('源字段不存在:'+n)
            for n in rel['target_fields']:
                if n not in fields[tk]:validity.append('目标字段不存在:'+n)
            if f.remote_field.model!=p:validity.append('Django目标不同')
            relations.append({'id':'REL%03d'%(len(relations)+1),'source':'.'.join(k),'target':'.'.join(tk),'model':m._meta.label,**rel,'target_model':p._meta.label,'target_table':'.'.join(tk),'declared_target':rel['target'],'source_schema':k[0],'source_table':k[1],'target_schema':tk[0],'target_name':tk[1],'issues':validity,'delete':f.remote_field.on_delete.__name__,'nullable_fk':f.null})
relmap={signature((r['source_schema'],r['source_table']),(r['target_schema'],r['target_name']),r['source_fields'],r['target_fields']):r for r in relations}
fkgroups=defaultdict(list)
for r in live['foreign_keys']:fkgroups[r['source_schema'],r['source_table'],r['name']].append(r)
fks=[]
for (ss,st,n),rows in fkgroups.items():
    first=rows[0];sk=ss,st;tk=first['target_schema'],first['target_table'];sf=[r['source_field'] for r in rows];tf=[r['target_field'] for r in rows]
    match=relmap.get(signature(sk,tk,sf,tf))
    fks.append({'name':n,'source':'.'.join(sk),'target':'.'.join(tk),'source_fields':sf,'target_fields':tf,'matched_relation':match['id'] if match else None,'delete':first['delete_referential_action_desc'],'update':first['update_referential_action_desc'],'disabled':first['is_disabled'],'untrusted':first['is_not_trusted']})
uie=defaultdict(list)
for r in live['ui_tables']:uie[r['DataTableName']].append(r)
uis=[]
for n,r in enumerate(live['ui_tables']):
    if not r['MasterDataTableName']:continue
    parents=uie[r['MasterDataTableName']];sf=[v.strip() for v in re.split('[,;]',r['RelaFieldNames'] or '') if v.strip()];tf=[v.strip() for v in re.split('[,;]',r['MasterRelaFieldNames'] or '') if v.strip()]
    item={'row':n+1,'entry':r['DataTableName'],'table':r['TableName'],'parent_entry':r['MasterDataTableName'],'source_fields':sf,'target_fields':tf,'matches':[]}
    if len(parents)!=1:item['status']='父入口缺失或重名'
    elif not sf or len(sf)!=len(tf):item['status']='配置关联字段未完整明确'
    else:
        parent=parents[0];item['parent_table']=parent['TableName']
        sk=('dye',r['TableName']);tk=('dye',parent['TableName'])
        match=relmap.get(signature(sk,tk,sf,tf))
        if match:item['status']='字段配对匹配';item['matches']=[match['id']]
        elif not bytable.get(sk) or not bytable.get(tk):item['status']='原表未直映射/查询别名/暂缓对象'
        else:item['status']='未匹配模型显式关系（需查服务/查询语义）'
    uis.append(item)
save('comparison.json',{'captured_at':live['captured_at'],'tables':table_results,'fields':field_results,'models':model_inventory,'relations':relations,'foreign_keys':fks,'ui_relations':uis,'new_source_tables_missing_old':['.'.join(k) for k in bytable if k not in fields],'extra_legacy_id_fields':[(m._meta.label,f.name) for m in allmodels for f in m._meta.fields if f.name in ['legacy_id','old_erp_id'] or '旧erpid' in str(f.verbose_name).lower()]})
plans=[]
for r in relations:
    if r['issues']:continue
    sk=r['source_schema'],r['source_table'];tk=r['target_schema'],r['target_name'];sf=r['source_fields'];tf=r['target_fields']
    join=' AND '.join('c.'+q(a)+'=p.'+q(b) for a,b in zip(sf,tf));null=' OR '.join('c.'+q(a)+' IS NULL' for a in sf);group=','.join(q(x) for x in tf)
    sql=f'''SELECT COUNT_BIG(*) AS child_rows,COALESCE(SUM(CASE WHEN {null} THEN CONVERT(bigint,1) ELSE 0 END),0) AS null_key_rows,COALESCE(SUM(CASE WHEN NOT ({null}) AND p.n IS NULL THEN CONVERT(bigint,1) ELSE 0 END),0) AS missing_parent_rows,COALESCE(SUM(CASE WHEN p.n=1 THEN CONVERT(bigint,1) ELSE 0 END),0) AS unique_parent_rows,COALESCE(SUM(CASE WHEN p.n>1 THEN CONVERT(bigint,1) ELSE 0 END),0) AS multiple_parent_rows FROM {table(sk)} c LEFT JOIN (SELECT {group},COUNT_BIG(*) n FROM {table(tk)} GROUP BY {group}) p ON {join}'''
    plans.append({'id':r['id'],'source':r['source'],'target':r['target_table'],'sql':sql})
save('relation-select-plan.json',plans)
print(json.dumps({'all_models':len(allmodels),'erp_models':sum(m._meta.app_label.startswith('erp_') for m in allmodels),'source_models':len(models),'field_checks':len(field_results),'field_differences':sum(bool(r['differences']) for r in field_results),'relations':len(relations),'fk_counts':dict(Counter(bool(f['matched_relation']) for f in fks)),'ui_counts':dict(Counter(r['status'] for r in uis))},ensure_ascii=False))
