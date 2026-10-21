import csv
import json
from collections import Counter
from datetime import date, datetime, time
from decimal import Decimal
from io import StringIO
from types import SimpleNamespace

from django.db import models
from django.utils import timezone
from rest_framework import serializers
from core.permissions import scoped_queryset
from core.resources import resource_options
from .catalog import ENTITIES
from .models import Users, OperationLog, LoginLog, DownloadCenter
from django_celery_results.models import TaskResult

UPDATE_KEY = '更新主键(勿改)'
SERIAL = '序号'
NULL = '#NULL'
EMPTY = '#EMPTY'
KEEP = '#KEEP'
TEXT = '#TEXT:'
READ_ONLY = {OperationLog, LoginLog, DownloadCenter, TaskResult}
USER_IMPORT = ['username', 'name', 'email', 'mobile', 'gender', 'is_active', 'dept', 'role']
USER_EXPORT = ['username', 'name', 'email', 'mobile', 'gender', 'is_active', 'last_login', 'dept', 'dept_owner']
USER_TITLES = {'username': '登录账号', 'name': '用户名称', 'email': '用户邮箱', 'mobile': '手机号码',
               'gender': '用户性别', 'is_active': '账号状态', 'dept': '部门', 'role': '角色',
               'last_login': '最后登录时间', 'dept_owner': '部门负责人'}


def supports_import(model):
    return model not in READ_ONLY


def relation_options(field, request, selected_queryset=None):
    related = field.related_model
    entity = next((key for key, model in ENTITIES.items() if model == related), None)
    choices = related.objects.all()
    if entity:
        query_request = SimpleNamespace(user=request.user, method='GET', path=f'/api/system/{entity}/')
        choices = scoped_queryset(choices, query_request)
    if selected_queryset is not None:
        choices = related.objects.filter(models.Q(pk__in=choices.values('pk')) |
                                         models.Q(pk__in=selected_queryset.values(field.name))).distinct()
    labels = [f.name for f in related._meta.fields if f.name in ['name', 'title', 'label', 'username']]
    label = labels[0] if labels else related._meta.pk.name
    return [{'value': obj.pk, 'label': f'{getattr(obj, label)} [{obj.pk}]'} for obj in choices]


def columns_for(view, mode, queryset=None):
    model = view.queryset.model
    serializer = view.get_serializer()
    model_fields = {f.name: f for f in list(model._meta.fields) + list(model._meta.many_to_many)}
    keys = USER_EXPORT if model is Users and mode == 'export' else (
        USER_IMPORT if model is Users else list(serializer.fields))
    custom = resource_options(model).get('fields', {})
    if model is Users and mode == 'export':
        keys = keys + [key for key in custom if key not in keys]
    columns = []
    for key in keys:
        serialized_key = 'dept' if model is Users and key == 'dept_owner' else key
        if serialized_key not in serializer.fields:
            continue
        sf = serializer.fields[serialized_key]
        source_path = (sf.source or serialized_key).split('.')
        source = source_path[0]
        grant = serializer.field_permissions.get(source, {'is_query': True, 'is_create': True, 'is_update': True})
        if mode == 'export' and (sf.write_only or not grant['is_query']):
            continue
        if mode != 'export' and (sf.read_only or sf.write_only or isinstance(sf, serializers.FileField) or not grant['is_create' if mode == 'create' else 'is_update']):
            continue
        if mode == 'update' and (not grant['is_query'] or source == model._meta.pk.name):
            continue
        mf = model_fields.get(source)
        for part in source_path[1:]:
            mf = {f.name: f for f in mf.related_model._meta.get_fields()}.get(part) if mf and mf.is_relation else None
        title = custom.get(key, {}).get('title', USER_TITLES[key] if model is Users and key in USER_TITLES else str(mf.verbose_name) if mf else key)
        column = {'key': key, 'title': title,
                  'kind': 'text', 'required': sf.required if mode == 'create' else False, 'options': []}
        if model is Users and key == 'dept_owner':
            column['source'] = 'dept.owner'
        elif mf is None:
            column['kind'] = custom.get(key, {}).get('excel_kind', 'text')
        elif mf.choices:
            column.update(kind='choice', options=[{'value': value, 'label': str(label)} for value, label in mf.flatchoices])
        elif isinstance(mf, models.BooleanField):
            column.update(kind='choice', options=[{'value': True, 'label': '启用' if key == 'is_active' else '是'},
                                                 {'value': False, 'label': '禁用' if key == 'is_active' else '否'}])
        elif mf.is_relation:
            column.update(kind='multi' if mf.many_to_many else 'relation',
                          options=relation_options(mf, view.request, queryset))
        elif isinstance(mf, models.DateTimeField):
            column['kind'] = 'datetime'
        elif isinstance(mf, models.DateField):
            column['kind'] = 'date'
        elif isinstance(mf, models.TimeField):
            column['kind'] = 'time'
        elif isinstance(mf, models.JSONField):
            column['kind'] = 'json'
        elif isinstance(mf, (models.IntegerField, models.FloatField, models.DecimalField)) and not mf.primary_key:
            column.update(kind='number', decimals=mf.decimal_places if isinstance(mf, models.DecimalField) else None)
        columns.append(column)
    titles=Counter(column['title'] for column in columns)
    original={field:name for name,field in getattr(model,'SOURCE_FIELDS',{}).items()}
    for column in columns:
        if titles[column['title']]>1 or column['title'] in [SERIAL,UPDATE_KEY]:
            column['title']+=' ['+original.get(column['key'],column['key'])+']'
    return columns


def multiple_text(values):
    stream = StringIO()
    csv.writer(stream, delimiter=';', lineterminator='').writerow(values)
    return stream.getvalue()


def encode(value, column, for_import=False):
    if for_import:
        if value is None:return NULL
        if value == '':return EMPTY
        if isinstance(value,str) and (value in [NULL,EMPTY,KEEP] or value.startswith(TEXT)):
            return TEXT+value
    if value is None or value == '':
        return None
    kind = column['kind']
    if kind in ['choice', 'relation', 'multi']:
        labels = {str(option['value']): option['label'] for option in column['options']}
        if kind == 'multi':
            return multiple_text([labels[str(item)] for item in value])
        return labels[str(value)]
    if kind == 'json':
        return json.dumps(value, ensure_ascii=False)
    if kind == 'datetime':
        result = value if isinstance(value, datetime) else datetime.fromisoformat(value)
        return timezone.localtime(result).replace(tzinfo=None) if timezone.is_aware(result) else result
    if kind == 'date':
        return value if isinstance(value, date) else date.fromisoformat(value)
    if kind == 'time':
        return value if isinstance(value, time) else time.fromisoformat(value)
    if kind == 'number':
        return Decimal(str(value))
    return str(value)


def decode(value, column):
    kind = column['kind']
    if value == NULL:return None
    if value == EMPTY:return [] if kind=='multi' else ''
    if isinstance(value,str) and value.startswith(TEXT):value=value[len(TEXT):]
    if kind == 'choice':
        if not isinstance(value, str):
            return value
        labels={option['label']: option['value'] for option in column['options']}
        return labels[value] if value in labels else {option['value']:option['value'] for option in column['options']}[value]
    if kind in ['relation', 'multi']:
        values = {str(option['value']): option['value'] for option in column['options']}

        def relation(token):
            return values[token.rstrip().rsplit(' [', 1)[1].removesuffix(']')]

        return [relation(token) for token in next(csv.reader([value], delimiter=';', strict=True))] if kind == 'multi' else relation(value)
    if kind == 'json':
        return json.loads(value)
    if kind == 'date':
        return value.date() if isinstance(value, datetime) else value if isinstance(value, date) else date.fromisoformat(value)
    if kind == 'datetime':
        return value if isinstance(value, datetime) else datetime.fromisoformat(value)
    if kind == 'time':
        return value if isinstance(value, time) else time.fromisoformat(value)
    if kind == 'text':
        return str(value)
    return value
