"""原表单据的主从保存与办理；历史导入独立保存原事实。"""
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models.deletion import ProtectedError
from django.utils import timezone
from uuid import uuid4
from .business import locked, persist, record, snapshot
from .source_ownership import OWNERS
from .source_calculations import field_values,packaging_values,aggregate_values,price_from_amount,PRODUCTS,SPECIAL_TABLES,PACK_METHODS,AGGREGATES
from .source_sequences import allocate

OWNED = {'legacy_id', 'source_batch', 'source_row', 'approval_stage', 'confirmed_at',
         'confirmed_by', 'approved_at', 'approved_by'}


def managed_fields(model):
    return OWNED | set(model.SOURCE_IDENTITIES) | {
        model.SOURCE_FIELDS[target] for target, child, old, coalesce in AGGREGATES.get(model.SOURCE_TABLE, [])}


def owner_relations(model):
    return OWNERS.get(model._meta.label, [])


def parents(item):
    return [getattr(item, rule['field']) for rule in owner_relations(type(item))
            if getattr(item, rule['field'] + '_id') is not None]


def chain(item):
    owners = parents(item)
    if len(owners) > 1:
        raise ValidationError({'parent': '本条明细请明确采用一个办理表头，原多来源码仍保留。'})
    return [item] if not owners else chain(owners[0]) + [item]


def lock_chain(item):
    return [locked(parent) for parent in chain(item)]


def editable(items):
    for item in items:
        if item.approval_stage in ['confirmed', 'approved']:
            raise ValidationError({'approval_stage': '所属单据已经确认或审核，请先重新办理。'})


def child_rows(item):
    for label, rules in OWNERS.items():
        model = apps.get_model(label)
        for rule in rules:
            if rule['target'] == item._meta.label:
                yield from model.objects.filter(**{rule['field']: item}).order_by('pk')


def validate_document(item):
    item.full_clean()
    for child in child_rows(item):
        child.full_clean()
        validate_document(child)


def assign_owner_values(item, data):
    selected = [rule for rule in owner_relations(type(item)) if getattr(item, rule['field'] + '_id') is not None]
    if len(selected) > 1:
        raise ValidationError({'parent': '采购明细只能选择一个实际办理表头。'})
    for rule in selected:
        parent = getattr(item, rule['field'])
        for old, parent_old in zip(rule['source_fields'], rule['target_fields']):
            key = item.SOURCE_FIELDS[old]
            value = getattr(parent, parent.SOURCE_FIELDS[parent_old])
            if key in data and data[key] != value:
                raise ValidationError({key: '原关联码必须与所选表头一致。'})
            setattr(item, key, value)


def assign_reference_values(item,data):
    assigned={}
    for rule in item.SOURCE_RELATIONS:
        if getattr(item,rule['field']+'_id') is None:
            continue
        parent=getattr(item,rule['field'])
        for old,parent_old in zip(rule['source_fields'],rule['target_fields']):
            key=item.SOURCE_FIELDS[old]
            value=getattr(parent,parent.SOURCE_FIELDS[parent_old])
            if key in data and data[key]!=value:
                raise ValidationError({key:'原关联码必须与所选来源记录一致。'})
            if key in assigned and assigned[key]!=value:
                raise ValidationError({key:'所选来源记录的共同关联码不一致。'})
            assigned[key]=value
            setattr(item,key,value)


def apply_defaults(item, data):
    if item.SOURCE_TABLE == 'RecordYield' and 'old_guid' not in data:
        item.old_guid = str(uuid4())
    for key, (kind, value) in item.SOURCE_DEFAULTS.items():
        if key in data:
            continue
        if kind == 'now':
            value = timezone.now()
        elif kind == 'uuid':
            value = uuid4()
        field = item._meta.get_field(key)
        value = field.to_python(value)
        if field.get_internal_type() == 'DateTimeField' and value is not None and timezone.is_naive(value):
            value = timezone.make_aware(value)
        setattr(item, key, value)


def refresh_totals(items, actor):
    for item in reversed(items):
        if item.SOURCE_TABLE not in AGGREGATES:
            continue
        original = item
        item = locked(item)
        if item.source_batch_id is not None or item.legacy_id is not None:
            continue
        values = aggregate_values(item)
        changed = {key: value for key, value in values.items() if getattr(item, key) != value}
        if changed:
            before = snapshot(item)
            for key, value in changed.items():
                setattr(item, key, value)
            persist(item, actor)
            for key,value in changed.items():
                setattr(original,key,value)
            if actor is not None:
                record(item, 'refresh_totals', before, actor, '采用原子表汇总公式')


@transaction.atomic
def write(model, data, instance=None, actor=None):
    denied = managed_fields(model).intersection(data)
    if denied:
        raise ValidationError({key: '由来源导入或明确办理动作维护。' for key in denied})
    item = model() if instance is None else lock_chain(instance)[-1]
    if instance is None:
        apply_defaults(item, data)
    editable(chain(item))
    if instance is not None:
        for old in model.SOURCE_KEY:
            key = model.SOURCE_FIELDS[old]
            if key in data and data[key] != getattr(item, key):
                raise ValidationError({key: '原业务身份建立后保持不变，变更另建明确记录。'})
    for rule in owner_relations(model):
        field = rule['field']
        if instance is not None and field in data and getattr(item, field + '_id') is not None:
            previous = getattr(item, field + '_id')
            target = None if data[field] is None else data[field].pk
            if previous != target:
                raise ValidationError({field: '已有明细不能移到另一张表头。'})
    before = {'exists': False} if instance is None else snapshot(item)
    for key, value in data.items():
        setattr(item, key, value)
    editable(lock_chain(item) if item.pk is not None else [locked(parent) for parent in chain(item)[:-1]])
    if item.source_batch_id is None and item.legacy_id is None:
        assign_owner_values(item, data)
        assign_reference_values(item,data)
    if instance is None:
        item.approval_stage = 'draft' if item.SOURCE_DOCUMENT and not parents(item) else None
        allocate(item, actor)
    if actor is not None:
        item.modifier = actor
        if instance is None:
            item.creator = actor
            owner_chain = chain(item)
            item.dept_belong_id = actor.dept_id if len(owner_chain) == 1 else owner_chain[0].dept_belong_id
    result = persist(item)
    if actor is not None:
        record(item, 'create' if instance is None else 'edit', before, actor)
    refresh_totals(chain(item), actor)
    return result


@transaction.atomic
def delete(queryset,actor=None):
    affected = {}
    for item in queryset.order_by('pk'):
        editable(lock_chain(item))
        if item.source_batch_id is not None or item.legacy_id is not None:
            raise ValidationError({'legacy_id': '历史来源记录保留原行，不从普通删除入口删除。'})
        for parent in chain(item)[:-1]:
            affected[(parent._meta.label, parent.pk)] = parent
    try:
        queryset.delete()
    except ProtectedError as error:
        raise ValidationError({'parent': '此记录仍被明细或其他业务引用，请先处理相应业务。'}) from error
    refresh_totals(list(affected.values()), actor)


@transaction.atomic
def advance(item, actor, expected, target):
    objects = lock_chain(item)
    item = objects[-1]
    if not item.SOURCE_DOCUMENT or len(objects) > 1:
        raise ValidationError({'approval_stage': '关联明细由所属表头办理，请从表头确认或审核。'})
    if item.approval_stage != expected:
        raise ValidationError({'approval_stage': '当前办理阶段不允许此动作。'})
    validate_document(item)
    before = snapshot(item)
    item.approval_stage = target
    at = timezone.now()
    if target == 'confirmed':
        item.confirmed_at, item.confirmed_by = at, actor
    elif target == 'approved':
        item.approved_at, item.approved_by = at, actor
    persist(item, actor)
    record(item, target, before, actor)
    return item


def confirm(item, actor):
    return advance(item, actor, 'draft', 'confirmed')


def approve(item, actor):
    return advance(item, actor, 'confirmed', 'approved')


@transaction.atomic
def reopen(item, actor, reason):
    objects = lock_chain(item)
    item = objects[-1]
    if len(objects) > 1:
        raise ValidationError({'approval_stage': '请从所属表头重新办理。'})
    if item.approval_stage not in ['confirmed', 'approved']:
        raise ValidationError({'approval_stage': '此单据当前不在确认或审核阶段。'})
    if not reason.strip():
        raise ValidationError({'reason': '重新办理须说明原因。'})
    before = snapshot(item)
    item.approval_stage = 'draft'
    item.confirmed_at = item.approved_at = None
    item.confirmed_by = item.approved_by = None
    persist(item, actor)
    record(item, 'reopen', before, actor, reason)
    return item


@transaction.atomic
def calculate(item, actor, method):
    item = lock_chain(item)[-1]
    editable(chain(item))
    if item.source_batch_id is not None or item.legacy_id is not None:
        raise ValidationError({'legacy_id': '历史原计算值保留；重新计算在新办理单据上采用。'})
    if method == 'fields':
        if item.SOURCE_TABLE not in PRODUCTS and item.SOURCE_TABLE not in SPECIAL_TABLES:
            raise ValidationError({'method': '本表尚未登记本行字段公式。'})
        values = field_values(item)
    elif method == 'amount_to_price':
        if item.SOURCE_TABLE != 'StuffInDetail':
            raise ValidationError({'method': '金额反算单价仅适用于原染化料入库明细。'})
        values = price_from_amount(item)
    else:
        if item.SOURCE_TABLE != 'RecordYield' or method not in PACK_METHODS:
            raise ValidationError({'method': '所选原入口公式不适用于本条记录。'})
        values = packaging_values(item, method)
    before = snapshot(item)
    for key, value in values.items():
        setattr(item, key, value)
    persist(item, actor)
    record(item, 'calculate', before, actor, '采用原入口公式：' + method)
    refresh_totals(chain(item), actor)
    return item
