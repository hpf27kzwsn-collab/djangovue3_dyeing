"""业务服务共用的事务、事实快照和校验；状态规则由各模块明确实现。"""
import base64
import json
from datetime import datetime,time
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from .models import BusinessAction


class FactsEncoder(DjangoJSONEncoder):
    def default(self,value):
        if isinstance(value,(datetime,time)):return value.isoformat()
        if isinstance(value,(bytes,bytearray,memoryview)):return {'encoding':'base64','data':base64.b64encode(value).decode('ascii')}
        return super().default(value)


def snapshot(item):
    return json.loads(json.dumps({f.name: f.value_from_object(item) for f in item._meta.fields}, cls=FactsEncoder))


@transaction.atomic
def persist(item, actor=None):
    from . import numbering
    from .numbering_registry import registry
    numbered = any(label == item._meta.label for label, field in registry())
    if numbered and not hasattr(item, '_numbering_protected'):
        from .source_entry_services import entry_for
        entry = None if item.pk is None else entry_for(item)
        previous = None if item.pk is None else type(item).objects.get(pk=item.pk)
        data = {field: getattr(item, field) for label, field in registry()
                if label == item._meta.label and getattr(item, field) not in [None, '']}
        numbering.prepare(item, data, entry, item._state.adding, previous)
    if numbered:
        numbering.restore(item)
    if actor is not None:
        if item.pk is None:
            item.creator = actor
            item.dept_belong_id = actor.dept_id
        item.modifier = actor
    item.full_clean()
    item.save()
    if numbered:
        numbering.sync_model(type(item))
    return item


def record(item, action, before, actor, reason=''):
    from .source_chain_reverse import capture_change
    capture_change(item,before,snapshot(item))
    return persist(BusinessAction(entity=item._meta.label, object_id=item.pk, action=action,
                                 reason=reason, before=before, after=snapshot(item)), actor)


def locked(item):
    return type(item).objects.select_for_update().get(pk=item.pk)
