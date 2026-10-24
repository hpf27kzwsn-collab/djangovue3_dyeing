"""把完整来源原行写入各模块的静态业务模型；失败中断批次，不跳原行。"""
import base64,json
from contextlib import closing
from datetime import datetime
from itertools import islice,zip_longest
from pathlib import Path
from django.apps import apps
from django.conf import settings
from django.db import models,transaction,connection
from django.utils import timezone
from .legacy_services import source_path,rows


CATALOG=Path(__file__).resolve().parents[4]/'tools/legacy_models/source_catalog.json'


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
            elif isinstance(field,models.DateField) and not isinstance(field,models.DateTimeField):
                value=datetime.fromisoformat(value).date()
            else:value=field.to_python(value)
            if isinstance(field,models.DateTimeField) and timezone.is_naive(value):value=timezone.make_aware(value)
        values[new]=value
    return values


def make_record(model,table,original,actor):
    return model(**original_values(model,original),source_batch=table.batch,
        source_row=original['row'],creator=actor,modifier=actor,dept_belong_id=actor.dept_id,approval_stage=None)


def import_table(table,actor,sample_rows=None):
    model=source_model(table)
    if model.objects.filter(source_batch=table.batch).exists():raise ValueError('该表已经承接本批原行，请先对照，不覆盖已有数据：'+table.table_name)
    count=0
    with transaction.atomic():
        from plugins.erp_base.numbering import lock_model, sync_model
        lock_model(model)
        if sample_rows is not None:
            originals=[rows(table,ordinal,1)[0] for ordinal in sample_rows]
            model.objects.bulk_create([make_record(model,table,row,actor) for row in originals],batch_size=500)
            sync_model(model)
            return len(originals)
        if connection.vendor == 'postgresql':
            count = copy_original_table(model, table, actor)
            sync_model(model)
            return count
        with source_path(table).open(encoding='utf-8') as stream:
            while chunk:=list(islice(stream,500)):
                originals=[json.loads(line) for line in chunk]
                objects=[make_record(model,table,row,actor) for row in originals]
                model.objects.bulk_create(objects,batch_size=500);count+=len(objects)
        if count!=table.row_count:raise ValueError('来源行数与已承接数不一致：'+table.table_name)
        sync_model(model)
    return count


def copy_original_table(model, table, actor):
    """PostgreSQL完整原行承接；COPY保留类型，不构造数千万个ORM对象。"""
    fields = [field for field in model._meta.local_fields if not field.primary_key]
    defaults = {field.attname: field.get_default() for field in fields}
    now = timezone.now()
    defaults.update(source_batch_id=table.batch_id, source_row=None,
                    creator_id=actor.pk, modifier_id=actor.pk, dept_belong_id=actor.dept_id,
                    create_datetime=now, update_datetime=now, approval_stage=None)
    quote = connection.ops.quote_name
    sql = 'COPY ' + quote(model._meta.db_table) + ' (' + ','.join(quote(field.column) for field in fields) + ') FROM STDIN'
    count = 0
    with source_path(table).open(encoding='utf-8') as stream, connection.cursor() as cursor:
        with cursor.copy(sql) as copy:
            for line in stream:
                original = json.loads(line)
                values = {**defaults, **original_values(model, original),
                          'source_row': original['row']}
                copy.write_row([values[field.attname] for field in fields])
                count += 1
    if count != table.row_count:
        raise ValueError('来源行数与COPY已承接数不一致：' + table.table_name)
    return count


@transaction.atomic
def compare_table(table):
    """流式逐行逐字段核对，不用抽样或合计代替原值对照。"""
    model=source_model(table)
    count=0;comparisons=0
    names=['source_row','approval_stage',*model.SOURCE_FIELDS.values()]
    records=model.objects.filter(source_batch=table.batch).order_by('source_row').values_list(*names).iterator(chunk_size=5000)
    with closing(records), source_path(table).open(encoding='utf-8') as stream:
        for line,current in zip_longest(stream,records):
            if line is None or current is None:raise ValueError('原行身份集合不一致：'+table.table_name)
            original=json.loads(line)
            if current[0]!=original['row']:raise ValueError('原行身份集合不一致：'+table.table_name)
            if current[1] is not None:raise ValueError(f"历史行出现新办理阶段：{table.table_name} 第{original['row']}行")
            for (name,expected),actual in zip(original_values(model,original).items(),current[2:]):
                if isinstance(actual,memoryview):actual=bytes(actual)
                if actual!=expected:raise ValueError(f"原字段不一致：{table.table_name} 第{original['row']}行 {name}")
                comparisons+=1
            count+=1
    stored=model.objects.filter(source_batch=table.batch).count()
    if count!=table.row_count or stored!=count:raise ValueError('来源总行数与已承接原行数不一致：'+table.table_name)
    return {'table':table.schema_name+'.'+table.table_name,'rows':count,'field_comparisons':comparisons}


def link_relations(batch, table_names=None):
    """原配置/数据库声明的关系，只有确切唯一匹配才建立FK；原码一直保留。"""
    totals={};quote=connection.ops.quote_name
    for spec in entries():
        if spec['handling']!='business_model':continue
        if table_names is not None and spec['table'] not in table_names:continue
        child=apps.get_model(spec['module'],spec['model'])
        for relation in spec['relations']:
            parent=apps.get_model(relation['target']);column=child._meta.get_field(relation['field']).column
            def comparable(model, alias, old):
                key=model.SOURCE_FIELDS[old]
                value=alias+'.'+quote(model._meta.get_field(key).column)
                if key in model.SOURCE_COLLATIONS:
                    value='RTRIM('+value+')'
                    if '_CI_' in model.SOURCE_COLLATIONS[key]:value='UPPER('+value+')'
                return value
            join=' AND '.join(comparable(parent,'p',right)+'='+comparable(child,'c',left)
                              for left,right in zip(relation['source_fields'],relation['target_fields']))
            condition='p.source_batch_id=c.source_batch_id AND '+join
            sql='UPDATE '+quote(child._meta.db_table)+' AS c SET '+quote(column)+'=(SELECT p.id FROM '+quote(parent._meta.db_table)+' AS p WHERE '+condition+') WHERE c.source_batch_id=%s AND c.'+quote(column)+' IS NULL AND (SELECT COUNT(*) FROM '+quote(parent._meta.db_table)+' AS p WHERE '+condition+')=1'
            with transaction.atomic(),connection.cursor() as cursor:cursor.execute(sql,[batch.pk]);totals[spec['model']+'.'+relation['field']]=cursor.rowcount
    return totals
