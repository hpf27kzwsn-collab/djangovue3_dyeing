"""简单编号业务服务。取号、保存及流水上限在同一事务中；历史原值不重写。"""
import hashlib
import json
import re
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import connection, transaction, models
from .numbering_registry import registry, scope_definition


class GeneratedCode(str):
    """仅服务间传递的取号结果；HTTP/Excel普通文本不能伪造此类型。"""
    def __new__(cls, value, rule_id):
        obj = super().__new__(cls, value)
        obj.rule_id = rule_id
        return obj


@transaction.atomic
def generate_for_entry(item, field, entry):
    selected = [r for r in lock_model(type(item)) if r.target_field == field and matches(item, r, entry)]
    if not selected:
        return None
    if len(selected) != 1:
        raise ValidationError({field: '同一编号命中多条规则。'})
    rule = selected[0]
    if not rule.auto_enabled:
        raise ValidationError({field: '此类别采用手工编号，请明确传入编号。'})
    code, number = next_code(rule)
    rule.last_number = number
    rule.save(update_fields=['last_number', 'update_datetime'])
    return GeneratedCode(code, rule.pk)


def rules(model):
    from .numbering_models import NumberingRule
    return NumberingRule.objects.filter(target_model=model._meta.label).order_by('id')


def lock_model(model):
    # 配置新增时还没有规则行；同一个模型使用固定事务锁，随后按id锁规则行。
    if connection.vendor == 'postgresql':
        key = int.from_bytes(hashlib.sha256(('erp.numbering:' + model._meta.label).encode()).digest()[:8], 'big', signed=True)
        with connection.cursor() as cursor:
            cursor.execute('SELECT pg_advisory_xact_lock(%s)', [key])
    return list(rules(model).select_for_update())


def equivalent(model, field, value):
    if isinstance(value, str) and field in getattr(model, 'SOURCE_COLLATIONS', {}):
        value = value.rstrip(' ')
        if '_CI_' in model.SOURCE_COLLATIONS[field]:
            value = value.upper()
    return value


def matches(item, rule, entry):
    if rule.entry_name and rule.entry_name != entry:
        return False
    return all(equivalent(type(item), field, getattr(item, field)) in
               [equivalent(type(item), field, v) for v in (value if isinstance(value, list) else [value])]
               for field, value in rule.scope_filters.items())


def pool(rule):
    model = apps.get_model(rule.target_model)
    query = model.objects.all()
    # 原复合主键的其他分量定义号码池；物料、客户和幅宽克重单位的原码是全表身份。
    old = next(old for old, key in model.SOURCE_FIELDS.items() if key == rule.target_field)
    for part in model.SOURCE_KEY:
        field = model.SOURCE_FIELDS[part]
        if part != old and field in rule.scope_filters:
            from .source_business_updates import matching
            value = rule.scope_filters[field]
            candidates = model.objects.none()
            for candidate in value if isinstance(value, list) else [value]:
                candidates = candidates | matching(query, **{part: candidate})
            query = candidates
    return query


def suffix(rule, value):
    model = apps.get_model(rule.target_model)
    value = equivalent(model, rule.target_field, value)
    prefix = equivalent(model, rule.target_field, rule.prefix + '#')[:-1]
    if not isinstance(value, str) or not value.startswith(prefix):
        return None
    tail = value[len(prefix):]
    return int(tail) if re.fullmatch('[0-9]+', tail) else None


def baseline(rule):
    maximum = rule.last_number
    for value in pool(rule).values_list(rule.target_field, flat=True).iterator():
        number = suffix(rule, value)
        if number is not None and (maximum is None or number > maximum):
            maximum = number
    from .source_entry_registry import ENTRY_RULES
    from .source_sequences import SourceIdentitySequence
    model = apps.get_model(rule.target_model)
    old = next(old for old, field in model.SOURCE_FIELDS.items() if field == rule.target_field)
    namespaces = set()
    for definition in ENTRY_RULES.get(rule.target_model, {}).values():
        original = definition['number_fields'].get(old)
        if original is None or (original['Prefix'] or '') != rule.prefix:
            continue
        kind = original['FieldKind']
        if kind == 'AutoAdd':
            scope = {'kind': kind, 'prefix': rule.prefix}
        elif kind in ['AutoAdd_Local', 'AutoAdd_LocalPlusPrev', 'AutoAdd_LocalPlusPrev_LEFT']:
            owners = [model.SOURCE_FIELDS[part] for part in model.SOURCE_KEY if part != old]
            if any(key not in rule.scope_filters or isinstance(rule.scope_filters[key], list) for key in owners):
                continue
            scope = {'kind': kind, 'scope': {key: rule.scope_filters[key] for key in owners}, 'series': '', 'prefix': rule.prefix}
        else:
            continue
        encoded = json.dumps(scope, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
        namespaces.add(rule.target_model + '.' + rule.target_field + ':' + hashlib.sha256(encoded.encode()).hexdigest()[:32])
    for number in SourceIdentitySequence.objects.filter(namespace__in=namespaces).values_list('last_number', flat=True):
        if maximum is None or number > maximum:
            maximum = number
    return maximum


def next_code(rule):
    maximum = baseline(rule)
    number = rule.start_number if maximum is None else max(rule.start_number, maximum + 1)
    if len(str(number)) > rule.digits:
        raise ValidationError({rule.target_field: '流水已超过设定位数，请调整编号规则；不截断、不回绕。'})
    return rule.prefix + str(number).zfill(rule.digits), number


def preview(rule):
    code, number = next_code(rule)
    return {'code': code, 'next_number': str(number), 'baseline': None if (value := baseline(rule)) is None else str(value)}


def has_references(item, field):
    if any(rel.related_model._base_manager.filter(**{rel.field.name: item}).exists() for rel in item._meta.related_objects):
        return True
    old = next(old for old, key in item.SOURCE_FIELDS.items() if key == field)
    names = {
        'p_Customer': ['CustomerID', 'SupplierID'], 'p_Dept': ['DeptID'],
        'h_Employee': ['EmpID'], 'p_Gray': ['GrayID'], 'p_Shift': ['ShiftID'],
        'p_DyeCurve': ['CurveID'], 'p_Stuff': ['StuffID'], 'p_Article': ['ArticleID'],
        'p_Product': ['ProdID'], 'p_TestItem': ['ItemID'], 'p_DyeProgram': ['ProgramID'], 'p_Machine': ['MachineID'],
        'WidthGramWeight': ['WidthUnit', 'WeightUnit'],
    }.get(item.SOURCE_TABLE, [])
    if item.SOURCE_TABLE in ['p_FieldValid', 'p_StorageUnitID']:
        names = [item.old_field_type]
    # 即使FK尚未对应，原关联码仍是引用事实；重复父码不能按字符串批量改写。
    for model in apps.get_models():
        from .source_business_updates import matching
        for name in names:
            if model is not type(item) and name in getattr(model, 'SOURCE_FIELDS', {}):
                raw_field = model._meta.get_field(model.SOURCE_FIELDS[name])
                value = getattr(item, field)
                if isinstance(raw_field, models.IntegerField):
                    # 原单位选择列有整数存储；按列类型比对，不对整数列执行RTRIM。
                    if value is None or not re.fullmatch('[0-9]+', value.rstrip(' ')):
                        continue
                    referenced = model.objects.filter(**{raw_field.name: int(value)})
                elif isinstance(raw_field, (models.CharField, models.TextField)):
                    referenced = matching(model.objects.all(), **{name: value})
                else:
                    continue
                if referenced.exists():
                    return True
        for table, raw in {'p_Dept': [('DEPARTMENTS', 'Code')], 'h_Employee': [('USERINFO', 'SSN')]}.get(item.SOURCE_TABLE, []):
            if getattr(model, 'SOURCE_TABLE', None) == table and matching(model.objects.all(), **{raw: getattr(item, field)}).exists():
                return True
        for relation in getattr(model, 'SOURCE_RELATIONS', []):
            if relation['target'] != item._meta.label or old not in relation['target_fields']:
                continue
            values = {model.SOURCE_FIELDS[left]: getattr(item, item.SOURCE_FIELDS[right])
                      for left, right in zip(relation['source_fields'], relation['target_fields'])}
            originals = {left: values[model.SOURCE_FIELDS[left]] for left in relation['source_fields']}
            if matching(model.objects.all(), **originals).exists():
                return True
    return False


def prepare(item, data, entry=None, creating=True, previous=None):
    if item.source_batch_id is not None and creating:
        return {}
    locked_rules = lock_model(type(item))
    selected = {}
    for rule in locked_rules:
        if matches(item, rule, entry):
            if rule.target_field in selected:
                raise ValidationError({'scope_key': '同一编号字段命中多条规则，请更正适用类别。'})
            selected[rule.target_field] = rule
    if previous is not None:
        from .source_entry_services import entry_for
        for rule in locked_rules:
            field = rule.target_field
            if matches(previous, rule, entry_for(previous)) and getattr(previous, field) != getattr(item, field):
                if not rule.allow_code_change or has_references(previous, field):
                    raise ValidationError({field: '原类别的编号已受管理，不能通过更换类别绕过编号更改规则。'})
    # 供应商Num是CustomerID的旧输入别名；不能绕过手工编号限制。
    if entry == 'p_Supplier' and 'old_customer_id' in selected and creating and 'old_num' in data:
        if 'old_customer_id' in data and data['old_customer_id'] != data['old_num']:
            raise ValidationError({'old_num': '供应商编码与输入编号不一致，请明确采用同一个编号。'})
        data['old_customer_id'] = data['old_num']
        item.old_customer_id = data['old_num']
    protected = {}
    for field, rule in selected.items():
        if creating:
            if field in data:
                generated = isinstance(data[field], GeneratedCode) and data[field].rule_id == rule.pk
                if not rule.allow_manual_input and not generated:
                    raise ValidationError({field: '此规则不允许手工录入编号，请留空由系统生成。'})
            elif rule.auto_enabled:
                code, number = next_code(rule)
                setattr(item, field, code)
                rule.last_number = number
                rule.save(update_fields=['last_number', 'update_datetime'])
            else:
                raise ValidationError({field: '该类别采用手工编号，请填写编号。'})
        elif previous is not None and getattr(previous, field) != getattr(item, field):
            if not rule.allow_code_change:
                raise ValidationError({field: '该编号不允许更改。'})
            if has_references(previous, field):
                raise ValidationError({field: '该记录已有业务引用，尚无完整专用编号变更服务，请保留原编号。'})
        protected[field] = getattr(item, field)
    if entry == 'p_Supplier' and 'old_customer_id' in selected and creating:
        item.old_num = item.old_customer_id
        protected['old_num'] = item.old_num
    item._numbering_protected = protected
    return protected


def restore(item):
    for field, value in getattr(item, '_numbering_protected', {}).items():
        setattr(item, field, value)


def sync_model(model):
    for rule in lock_model(model):
        maximum = baseline(rule)
        if maximum != rule.last_number:
            rule.last_number = maximum
            rule.save(update_fields=['last_number', 'update_datetime'])


def managed(item, field, entry):
    return any(rule.target_field == field and matches(item, rule, entry) for rule in rules(type(item)))


def policies(model):
    return [{'field': r.target_field, 'scope': r.scope_filters, 'entry': r.entry_name, 'name': r.name,
             'auto_enabled': r.auto_enabled, 'allow_manual_input': r.allow_manual_input,
             'allow_code_change': r.allow_code_change, 'pattern': r.prefix + '0' * r.digits}
            for r in rules(model)]


@transaction.atomic
def save_rule(data, actor=None, instance=None, commit=True):
    from .numbering_models import NumberingRule
    from .business import persist, record, snapshot
    rule = NumberingRule() if instance is None else NumberingRule.objects.get(pk=instance.pk)
    label = data.get('target_model', rule.target_model)
    if instance is not None and label != instance.target_model:
        raise ValidationError({'target_model': '已有规则保持原业务模型。'})
    model = apps.get_model(label)
    others = lock_model(model)
    before = {'exists': False} if instance is None else snapshot(rule)
    if instance is not None:
        rule = next(r for r in others if r.pk == instance.pk)
        if any(key in data and data[key] != getattr(rule, key) for key in ['target_model', 'target_field', 'scope_key']):
            raise ValidationError({'target_model': '已有规则的模型、字段和类别保持不变；其他类别请新增规则。'})
    for key, value in data.items():
        setattr(rule, key, value)
    spec = scope_definition(rule.target_model, rule.target_field, rule.scope_key)
    rule.scope_filters, rule.entry_name = spec['filters'], spec['entry_name']
    if rule.allow_code_change and rule.entry_name:
        raise ValidationError({'allow_code_change': '此单据的专用编号变更服务尚未完整对应；可配置新增编号，暂不能开放更改已有单号。'})
    if not rule.auto_enabled and not rule.allow_manual_input:
        raise ValidationError({'allow_manual_input': '关闭自动编号时必须允许手工录入。'})
    if not 1 <= rule.digits <= 18 or len(rule.prefix) + rule.digits > model._meta.get_field(rule.target_field).max_length:
        raise ValidationError({'digits': '流水位数须为1～18，且完整编号不能超过字段长度。'})
    if rule.start_number < 0 or len(str(rule.start_number)) > rule.digits:
        raise ValidationError({'start_number': '起始流水须为非负整数，且不能超过设定位数。'})
    for other in others:
        if other.pk == rule.pk or other.target_field != rule.target_field:
            continue
        if other.scope_key == rule.scope_key:
            raise ValidationError({'scope_key': '该类别已存在编号规则。'})
        old = next(old for old, field in model.SOURCE_FIELDS.items() if field == rule.target_field)
        separate = any(model.SOURCE_FIELDS[p] in rule.scope_filters and model.SOURCE_FIELDS[p] in other.scope_filters
                       and rule.scope_filters[model.SOURCE_FIELDS[p]] != other.scope_filters[model.SOURCE_FIELDS[p]]
                       for p in model.SOURCE_KEY if p != old)
        a, b = equivalent(model, rule.target_field, rule.prefix + '#')[:-1], equivalent(model, rule.target_field, other.prefix + '#')[:-1]
        if not separate and rule.auto_enabled and other.auto_enabled and a == b:
            raise ValidationError({'prefix': '同一号码池的同前缀必须共用规则，不能按类别或位数另建计数器。'})
        if not separate and rule.auto_enabled and other.auto_enabled and len(a) + rule.digits == len(b) + other.digits:
            short, long = sorted([a, b], key=len)
            if long.startswith(short) and (long == short or long[len(short):].isascii() and long[len(short):].isdigit()):
                raise ValidationError({'prefix': '此编号格式与同一号码池的其他规则重叠，请使用不同前缀或共用一条规则。'})
    rule.last_number = baseline(rule)
    if not commit:
        return rule
    persist(rule, actor)
    if actor is not None:
        record(rule, 'numbering_configure', before, actor, '编号管理配置，仅作用于后续保存')
    return rule
