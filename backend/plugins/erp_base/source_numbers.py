"""明确翻译旧编号模式；原号及完整原键由历史导入保持。"""
import hashlib
import json
from uuid import uuid4
from django.core.exceptions import ValidationError
from django.db.models import Max
from django.utils import timezone
from .business import persist, locked
from .source_sequences import SourceIdentitySequence


def reserve(item, key, scope, initial, actor):
    code = json.dumps(scope, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    namespace = item._meta.label + '.' + key + ':' + hashlib.sha256(code.encode()).hexdigest()[:32]
    sequence, created = SourceIdentitySequence.objects.get_or_create(namespace=namespace,
        defaults={'last_number': 0, 'creator': actor, 'modifier': actor})
    sequence = locked(sequence)
    if created:
        sequence.last_number = initial()
    sequence.last_number += 1
    persist(sequence, actor)
    return sequence.last_number


def integer(value, field):
    try:
        return int(str(value))
    except ValueError as error:
        raise ValidationError({field: '现有原号的数值部分不能按本编号规则递增，请明确录入新号。'}) from error


def owner_scope(item, key):
    return {item.SOURCE_FIELDS[old]: getattr(item, item.SOURCE_FIELDS[old]) for old in item.SOURCE_KEY
            if item.SOURCE_FIELDS[old] != key}


def generate(item, old, rule, actor, at):
    key = item.SOURCE_FIELDS[old]
    from .source_entry_registry import ENTRY_RULES
    from .numbering import generate_for_entry
    entry = next((name for name, definition in ENTRY_RULES.get(item._meta.label, {}).items()
                  if definition['number_fields'].get(old) is rule), None)
    number = generate_for_entry(item, key, entry)
    if number is not None:
        return number
    kind = rule['FieldKind']
    if kind == 'Guid':
        value = str(uuid4())
    elif kind == 'FollowSeries':
        value = item.old_sheet_series
    elif kind == 'AutoAdd_Time':
        clock = int(at.strftime('%Y%m%d%H%M%S') + f'{at.microsecond // 1000:03d}')
        value = reserve(item, key, {'kind': kind}, lambda: clock - 1, actor)
        namespace_scope = json.dumps({'kind': kind}, sort_keys=True, separators=(',', ':'))
        namespace = item._meta.label + '.' + key + ':' + hashlib.sha256(namespace_scope.encode()).hexdigest()[:32]
        sequence = locked(SourceIdentitySequence.objects.get(namespace=namespace))
        if value < clock:
            sequence.last_number = clock
            persist(sequence, actor)
            value = clock
        value = str(value)
    elif kind == 'DateCode':
        year_width = max(2, min(4, 4 if rule['YearCode'] is None else rule['YearCode']))
        prefix = '' if rule['Prefix'] is None else rule['Prefix']
        date_prefix = prefix + at.strftime('%Y')[-year_width:] + (rule['YearMonthSplit'] or '') + at.strftime('%m') + (rule['MonthDaySplit'] or '') + at.strftime('%d') + (rule['DayQueueSplit'] or '')
        width = 3 if rule['EndCode'] is None else 2 if rule['EndCode'] == '' else int(rule['EndCode'])
        def initial():
            suffixes = type(item).objects.filter(**{key + '__startswith': date_prefix}).values_list(key, flat=True)
            return max((integer(value[len(date_prefix):], key) for value in suffixes), default=0)
        number = reserve(item, key, {'kind': kind, 'prefix': date_prefix}, initial, actor)
        # 保留完整新序号，避免旧RIGHT截断后重复；该差异单独登记。
        value = date_prefix + str(number).zfill(width)
    elif kind in ['SeriesAndRowNo', 'SheetRowNo', 'RowNo', 'AutoAdd_Local', 'AutoAdd_LocalPlusPrev', 'AutoAdd_LocalPlusPrev_LEFT']:
        scope = owner_scope(item, key)
        width = 2 if not rule['FixedLength'] or rule['FixedLength'] <= 0 else rule['FixedLength']
        series = str(item.old_sheet_series) if kind == 'SeriesAndRowNo' else ''
        prefix = (rule['Prefix'] or '') if kind in ['AutoAdd_LocalPlusPrev', 'AutoAdd_LocalPlusPrev_LEFT'] else ''
        def initial():
            query = type(item).objects.filter(**scope)
            if prefix:
                query = query.filter(**{key + '__startswith': prefix})
            values = query.values_list(key, flat=True)
            return max((integer(str(value).split('-', 1)[-1] if kind == 'SeriesAndRowNo' else str(value)[len(prefix):], key)
                        for value in values if value not in [None, '']), default=0)
        number = reserve(item, key, {'kind': kind, 'scope': scope, 'series': series, 'prefix': prefix}, initial, actor)
        value = (series + '-' if kind == 'SeriesAndRowNo' else prefix) + str(number).zfill(width)
    elif kind == 'AutoAdd':
        prefix = rule['Prefix'] or ''
        width = max(6, rule['FixedLength'] or 2)
        def initial():
            maximum = type(item).objects.filter(**{key + '__startswith': prefix}).aggregate(value=Max(key))['value']
            return 0 if maximum in [None, ''] else integer(str(maximum)[len(prefix):], key)
        number = reserve(item, key, {'kind': kind, 'prefix': prefix}, initial, actor)
        value = prefix + str(number).zfill(width)
    else:
        raise ValidationError({key: '本字段的原编号模式尚未明确实现：' + str(kind)})
    return item._meta.get_field(key).to_python(value)
