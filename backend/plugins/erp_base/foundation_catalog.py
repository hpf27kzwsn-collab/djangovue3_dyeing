"""基础资料业务入口；共表分类和原表总览使用同一份原数据。"""
import json
from pathlib import Path
from django.db.models.functions import RTrim, Upper
from rest_framework.exceptions import ValidationError, PermissionDenied

CATALOG = json.loads(Path(__file__).with_suffix('.json').read_text(encoding='utf-8'))
DEFINITIONS = CATALOG['definitions']
MODEL_TITLES = CATALOG['model_titles']


def definition(key, model):
    if key not in DEFINITIONS:
        raise ValidationError({'_foundation': '未登记的基础资料入口。'})
    item = DEFINITIONS[key]
    if item['model'] != model._meta.label:
        raise ValidationError({'_foundation': '此入口不属于当前资料表。'})
    return item


def request_definition(request, model):
    key = request.query_params.get('_foundation')
    if not key:
        return None
    item = definition(key, model)
    if item.get('readonly') and request.method not in ['GET', 'HEAD', 'OPTIONS']:
        raise PermissionDenied('此类财务来源目前只提供原资料查询，财务办理继续暂缓。')
    return item


def scope(queryset, item):
    if item is None:
        return queryset
    for number, (field, value) in enumerate(item['filters'].items()):
        if isinstance(value, str):
            alias = 'foundation_filter_' + str(number)
            queryset = queryset.annotate(**{alias: Upper(RTrim(field))}).filter(**{alias: value.rstrip(' ').upper()})
        else:
            queryset = queryset.filter(**{field: value})
    return queryset


def bind(values, item, *, create, historical=False):
    if item is None:
        return values
    values = dict(values)
    for field, expected in item['filters'].items():
        if field not in values:
            if create and not historical:
                values[field] = expected
            continue
        actual = values[field]
        equal = actual.rstrip(' ').upper() == expected.rstrip(' ').upper() if isinstance(actual, str) and isinstance(expected, str) else actual == expected
        if not equal:
            raise ValidationError({field: '与当前业务分类不一致；原异常值可从原表总览完整承接，不覆盖或跳过本行。'})
    if create and not historical and item['entry'] is not None:
        if '_entry' in values and values['_entry'] != item['entry']:
            raise ValidationError({'_entry': '请使用当前业务入口，其他业务从对应菜单或原表总览办理。'})
        values['_entry'] = item['entry']
    return values


def configure_resources(options, app_label):
    for name, config in options.items():
        label = app_label + '.' + name
        if label in MODEL_TITLES:
            config['title'] = MODEL_TITLES[label]

