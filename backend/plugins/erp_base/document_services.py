"""整单主从事务；参数类型和页面权限由接口明确处理。"""
from django.core.exceptions import ValidationError
from django.db import transaction
from .business import locked, write, delete
from .business_policies import policy_for, document_children
from .source_documents import SourceRecord
from . import source_services


def write_row(model, data, item, actor, department):
    values = dict(data, modifier=actor)
    if item is None:
        values.update(creator=actor, dept_belong_id=department)
    if issubclass(model, SourceRecord):
        values.pop('modifier')
        return source_services.write(model, values, item, actor)
    return write(model, values, item, policy_for(model))


@transaction.atomic
def save_document(item, actor, head, children):
    model = type(item)
    original = issubclass(model, SourceRecord)
    if original:
        item = source_services.lock_chain(item)[-1]
        source_services.editable(source_services.chain(item))
    else:
        item = locked(item)
        policy_for(model)['editable'](item)
    allowed = document_children(model)
    if set(children) - set(allowed):
        raise ValidationError({'children': '明细类型不属于本表头。'})
    item = write_row(model, head, item, actor, item.dept_belong_id)
    for child, changes in children.items():
        parent_key = allowed[child]
        for change in changes['upsert']:
            previous, data = change['instance'], dict(change['data'])
            if parent_key in data:
                raise ValidationError({parent_key: '所属表头由整单保存确定。'})
            if previous is not None:
                previous = child.objects.get(pk=previous.pk, **{parent_key: item})
            else:
                data[parent_key] = item
            write_row(child, data, previous, actor, item.dept_belong_id)
        keys = changes['delete']
        if keys:
            rows = child.objects.filter(pk__in=keys, **{parent_key: item})
            if rows.count() != len(set(keys)):
                raise ValidationError({'children': '待删除明细不属于本表头。'})
            if original:
                source_services.delete(rows,actor)
            else:
                delete(rows, policy_for(child))
    return item
