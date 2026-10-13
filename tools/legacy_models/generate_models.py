"""从明确的结构快照和逐表去向生成静态Django字段，不读取或修改旧数据库。"""
import argparse,ast,json,re,hashlib
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
MODULES=['erp_base','erp_sales','erp_purchase','erp_sampling','erp_production','erp_warehouse','erp_quality']

def identifier(name):
    words=re.sub(r'([a-z0-9])([A-Z])',r'\1_\2',name)
    return 'old_'+re.sub(r'\W','_',words.lower()).strip('_')

def model_name(schema,table):return 'Source'+schema.title()+''.join(word[:1].upper()+word[1:] for word in re.split(r'[^\w]|_',table) if word)

def declaration(column,title):
    kind=column['data_type'];null=column['is_nullable']
    blank=null or kind in ['varchar','nvarchar','char','nchar','text','ntext','image','binary','varbinary']
    arguments=[repr(title),'null='+repr(null),'blank='+repr(blank)]
    if kind in ['varchar','nvarchar','char','nchar']:
        size=column['max_length']//2 if kind in ['nvarchar','nchar'] else column['max_length']
        if size==-1:field='TextField'
        else:field='CharField';arguments.append('max_length='+str(size))
    elif kind in ['text','ntext']:field='TextField'
    elif kind in ['decimal','numeric','money']:
        field='DecimalField';arguments.extend(['max_digits='+str(column['precision']),'decimal_places='+str(column['scale'])])
    elif kind in ['float','real']:field='FloatField'
    elif kind in ['tinyint','smallint','int']:field='IntegerField'
    elif kind=='bigint':field='BigIntegerField'
    elif kind=='bit':field='BooleanField'
    elif kind in ['datetime','datetime2','smalldatetime']:field='DateTimeField'
    elif kind=='date':field='DateField'
    elif kind=='time':field='TimeField'
    elif kind in ['image','binary','varbinary']:field='BinaryField';arguments.append('editable=True')
    elif kind=='uniqueidentifier':field='UUIDField'
    else:raise ValueError('未声明的源类型：'+kind)
    return 'models.'+field+'('+', '.join(arguments)+')'

def generate(schema_path,registry_path):
    source=json.loads(schema_path.read_text(encoding='utf-8-sig'));registry=json.loads(registry_path.read_text(encoding='utf-8'))
    columns=defaultdict(list)
    for column in source['fields']:columns[(column['schema_name'],column['table_name'])].append(column)
    grouping=defaultdict(list)
    for table in registry['tables']:
        if table['handling']=='business_model':grouping[table['module']].append(table)
    for module in MODULES:
        code=['"""静态旧业务字段；由tools/legacy_models生成，逐表来源见source_catalog.json。"""',
              'from django.db import models','from plugins.erp_base.source_documents import SourceRecord','']
        resources=['"""原业务模型的完整字段与主从入口。"""','RESOURCE_OPTIONS = {']
        for table in grouping[module]:
            name=table['model'];fields=columns[(table['schema'],table['table'])]
            raw={column['field_name']:identifier(column['field_name']) for column in fields}
            assert len(set(raw.values()))==len(raw),name
            code += ['', 'class '+name+'(SourceRecord):','    SOURCE_SCHEMA='+repr(table['schema']),
                     '    SOURCE_TABLE='+repr(table['table']),'    SOURCE_FIELDS='+repr(raw),'    SOURCE_KEY='+repr(tuple(table['primary_key'])),
                     '    SOURCE_DOCUMENT='+repr(table['document'])]
            for column in fields:
                title=table['captions'][column['field_name']]
                code.append('    '+raw[column['field_name']]+'='+declaration(column,title))
            for relation in table['relations']:
                code.append('    '+relation['field']+'=models.ForeignKey('+repr(relation['target'])+", verbose_name="+repr(relation['title'])+", null=True, blank=True, on_delete=models.PROTECT, related_name='+')")
            indexed={tuple(table['primary_key'])} if table['primary_key'] else set()
            indexed.update(tuple(r['target_fields']) for t in registry['tables'] for r in t['relations'] if r['target']==module+'.'+name)
            index_code=[]
            for key in sorted(indexed):
                fields=['source_batch',*[raw[column] for column in key]]
                index_name='src_'+hashlib.sha256((module+'.'+name+','.join(key)).encode()).hexdigest()[:16]
                index_code.append('models.Index(fields='+repr(fields)+',name='+repr(index_name)+')')
            code+=['','    class Meta(SourceRecord.Meta):','        db_table='+repr(table['db_table']),
                   '        indexes=['+','.join(index_code)+']',
                   '        verbose_name=verbose_name_plural='+repr(table['title']),'        ordering=["-id"]']
            options={'viewset':'plugins.erp_base.source_api.SourceRecordViewSet','serializer':'plugins.erp_base.source_api.SourceRecordSerializer',
                     'crud_fields':['id',*raw.values(),*[r['field'] for r in table['relations']],'approval_stage','confirmed_at','confirmed_by','approved_at','approved_by','legacy_id','source_batch','source_row','remarks'],
                     'fields':{'legacy_id':{'column':{'show':False}},'source_batch':{'column':{'show':False}},'source_row':{'column':{'show':False}}},
                     'workflow':{'source_model':True,'state_field':'approval_stage','actions':[]}}
            if table['document']:
                options['workflow'].update({'editable_states':['draft'],'actions':[
                    {'key':'confirm','title':'确认','states':['draft'],'inputs':[]},
                    {'key':'approve','title':'审核','states':['confirmed'],'inputs':[]},
                    {'key':'reopen','title':'重新办理','states':['confirmed','approved'],'inputs':[{'key':'reason','title':'原因','kind':'textarea','required':True,'options':[]}]}]})
            children=[{'entity':child['module']+'_'+child['model'].lower(),'title':child['title'],'key':relation['field']} for child in registry['tables'] if child['handling']=='business_model' for relation in child['relations'] if relation['target']==module+'.'+name]
            options['workflow']['children']=children
            resources.append('    '+repr(name)+': '+repr(options)+',')
        resources.append('}')
        code_text='\n'.join(code)+'\n';ast.parse(code_text)
        (ROOT/'backend/plugins'/module/'source_models.py').write_text(code_text,encoding='utf-8',newline='\n')
        (ROOT/'backend/plugins'/module/'source_resources.py').write_text('\n'.join(resources)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'business_models':sum(map(len,grouping.values())),'by_module':{key:len(value) for key,value in grouping.items()},'fields':sum(len(columns[(t['schema'],t['table'])]) for t in registry['tables'] if t['handling']=='business_model')},ensure_ascii=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--schema',type=Path,required=True);parser.add_argument('--catalog',type=Path,required=True)
    args=parser.parse_args();generate(args.schema,args.catalog)
