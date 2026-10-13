"""把完整来源原行写入各模块的静态业务模型；失败中断批次，不跳原行。"""
import base64,json
from itertools import islice
from pathlib import Path
from django.apps import apps
from django.conf import settings
from django.db import models,transaction,connection
from django.utils import timezone
from .legacy_services import source_path,rows


CATALOG=Path(__file__).resolve().parents[3]/'tools/legacy_models/source_catalog.json'


def entries():return json.loads(CATALOG.read_text(encoding='utf-8'))['tables']


def source_model(table):
    spec=next(row for row in entries() if row['schema']==table.schema_name and row['table']==table.table_name)
    if spec['handling']!='business_model':raise ValueError('该表未登记为基础或业务模型：'+table.table_name)
    return apps.get_model(spec['module'],spec['model'])


def original_values(model,original):
    values={}
    for old,new in model.SOURCE_FIELDS.items():
        value=original['values'][old];field=model._meta.get_field(new)
        if value is not None:
            if isinstance(field,models.BinaryField):value=base64.b64decode(value)
            else:value=field.to_python(value)
            if isinstance(field,models.DateTimeField) and timezone.is_naive(value):value=timezone.make_aware(value)
        values[new]=value
    return values


def identity(table,original):
    if original['key'] is None:return None
    return json.dumps({'schema':table.schema_name,'table':table.table_name,'key':original['key']},ensure_ascii=False,sort_keys=True,separators=(',',':'))


def make_record(model,table,original,actor):
    return model(**original_values(model,original),legacy_id=identity(table,original),source_batch=table.batch,
        source_row=original['row'],creator=actor,modifier=actor,dept_belong_id=actor.dept_id,approval_stage=None)


def import_table(table,actor,sample_rows=None):
    model=source_model(table)
    if model.objects.filter(source_batch=table.batch).exists():raise ValueError('该表已经承接本批原行，请先对照，不覆盖已有数据：'+table.table_name)
    count=0
    with transaction.atomic():
        if sample_rows is not None:
            originals=[rows(table,ordinal,1)[0] for ordinal in sample_rows]
            model.objects.bulk_create([make_record(model,table,row,actor) for row in originals],batch_size=500)
            return len(originals)
        with source_path(table).open(encoding='utf-8') as stream:
            while chunk:=list(islice(stream,500)):
                originals=[json.loads(line) for line in chunk]
                objects=[make_record(model,table,row,actor) for row in originals]
                model.objects.bulk_create(objects,batch_size=500);count+=len(objects)
        if count!=table.row_count:raise ValueError('来源行数与已承接数不一致：'+table.table_name)
    return count


def link_relations(batch):
    """原配置/数据库声明的关系，只有确切唯一匹配才建立FK；原码一直保留。"""
    totals={};quote=connection.ops.quote_name
    for spec in entries():
        if spec['handling']!='business_model':continue
        child=apps.get_model(spec['module'],spec['model'])
        for relation in spec['relations']:
            parent=apps.get_model(relation['target']);column=child._meta.get_field(relation['field']).column
            join=' AND '.join('p.'+quote(parent._meta.get_field(parent.SOURCE_FIELDS[right]).column)+'=c.'+quote(child._meta.get_field(child.SOURCE_FIELDS[left]).column) for left,right in zip(relation['source_fields'],relation['target_fields']))
            condition='p.source_batch_id=c.source_batch_id AND '+join
            sql='UPDATE '+quote(child._meta.db_table)+' AS c SET '+quote(column)+'=(SELECT p.id FROM '+quote(parent._meta.db_table)+' AS p WHERE '+condition+') WHERE c.source_batch_id=%s AND c.'+quote(column)+' IS NULL AND (SELECT COUNT(*) FROM '+quote(parent._meta.db_table)+' AS p WHERE '+condition+')=1'
            with transaction.atomic(),connection.cursor() as cursor:cursor.execute(sql,[batch.pk]);totals[spec['model']+'.'+relation['field']]=cursor.rowcount
    return totals
