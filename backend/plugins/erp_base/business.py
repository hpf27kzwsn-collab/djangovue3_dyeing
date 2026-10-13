"""业务服务共用的事务、事实快照和校验；状态规则由各模块明确实现。"""
import copy
import base64
import json
from datetime import datetime,time
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.db.models.deletion import RestrictedError
from .models import BusinessAction


class FactsEncoder(DjangoJSONEncoder):
    def default(self,value):
        if isinstance(value,(datetime,time)):return value.isoformat()
        if isinstance(value,(bytes,bytearray,memoryview)):return {'encoding':'base64','data':base64.b64encode(value).decode('ascii')}
        return super().default(value)


def snapshot(item):
    return json.loads(json.dumps({f.name: f.value_from_object(item) for f in item._meta.fields}, cls=FactsEncoder))


def persist(item, actor=None):
    if actor is not None:
        if item.pk is None:
            item.creator = actor
            item.dept_belong_id = actor.dept_id
        item.modifier = actor
    item.full_clean()
    item.save()
    return item


def record(item, action, before, actor, reason=''):
    return persist(BusinessAction(entity=item._meta.label, object_id=item.pk, action=action,
                                 reason=reason, before=before, after=snapshot(item)), actor)


def require_state(item, states, field='status'):
    if getattr(item, field) not in states:
        raise ValidationError({field: '当前状态不允许此业务操作。'})


def locked(item):
    return type(item).objects.select_for_update().get(pk=item.pk)


def write(model, data, instance, policy):
    """父对象先锁定；同一单据的明细编辑和确认使用同一把父锁。"""
    with transaction.atomic():
        parent_key, root_path = policy['parents'].get(model, (None, None))
        if parent_key is not None:
            parent = data[parent_key] if instance is None else getattr(instance, parent_key)
            root = parent
            for part in root_path.split('.') if root_path else []:
                root = getattr(root, part)
            root = policy['lock_root'](root)
            policy['parent_editable'](model, root)
        else:
            root = None
        if instance is not None:
            original = locked(instance)
            policy['editable'](original)
            item = copy.copy(original)
            if parent_key in data and data[parent_key].pk != getattr(original, parent_key + '_id'):
                raise ValidationError({parent_key: '不能变更明细所属单据。'})
        else:
            item = model()
        for key, value in data.items():
            setattr(item, key, value)
        if root is not None:
            item.dept_belong_id = root.dept_belong_id
        policy['validate'](item)
        return persist(item)


@transaction.atomic
def delete(queryset, policy):
    model = queryset.model
    parent_key, root_path = policy['parents'].get(model, (None, None))
    items = list(queryset.select_related(None).order_by('pk'))
    if parent_key is not None:
        roots = {}
        for item in items:
            root = getattr(item, parent_key)
            for part in root_path.split('.') if root_path else []:
                root = getattr(root, part)
            roots[root.pk] = root
        for key in sorted(roots):
            policy['parent_editable'](model, policy['lock_root'](roots[key]))
    items = list(queryset.select_related(None).select_for_update().order_by('pk'))
    for item in items:
        policy['deletable'](item)
    try:
        queryset.delete()
    except RestrictedError as error:
        raise ValidationError({'id': '该对象已被业务引用，不能删除。'}) from error


def require_rows(queryset):
    rows = list(queryset.select_related(None).order_by('pk'))
    if not rows:
        raise ValidationError({'lines': '请先填写业务明细。'})
    for item in rows:
        item.full_clean()
    return rows


def validate_effective(item, at):
    if item.valid_from is not None and at < item.valid_from:
        raise ValidationError({'valid_from': '来源版本在业务日期尚未生效。'})
    if item.valid_to is not None and at >= item.valid_to:
        raise ValidationError({'valid_to': '来源版本在业务日期已失效。'})
