"""拆合办理的逐字段前后事实；逆向只撤销仍属于本次办理的改变。"""
from django.apps import apps
from django.core.exceptions import ValidationError
from .business import locked,persist,record,snapshot
from .source_calculations import store_value


def change(item,values,effects,actor,reason):
    item=locked(item);before=snapshot(item)
    fields=dict(store_value(item,key,value) for key,value in values.items())
    for key,value in fields.items():setattr(item,key,value)
    persist(item,actor);after=snapshot(item)
    effects.append({'entity':item._meta.label,'id':item.pk,'before':{key:before[key] for key in fields},
        'after':{key:after[key] for key in fields}})
    record(item,'split_merge_change',before,actor,reason)
    return item


def restore(effects,actor,reason):
    for effect in reversed(effects):
        item=locked(apps.get_model(effect['entity']).objects.get(pk=effect['id']))
        for key,value in effect['after'].items():
            expected=item._meta.get_field(key).to_python(value)
            if getattr(item,key)!=expected:
                raise ValidationError({'source':f'{item._meta.label}#{item.pk}的{key}已有后续变更，请先撤回对应后续办理。'})
        before=snapshot(item)
        for key,value in effect['before'].items():setattr(item,key,item._meta.get_field(key).to_python(value))
        persist(item,actor);record(item,'split_merge_restore',before,actor,reason)
