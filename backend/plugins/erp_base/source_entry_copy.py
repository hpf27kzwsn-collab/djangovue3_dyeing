"""按用户选中的上一行应用原CopyPrevRow/CopyLastRow，不猜数据库行序。"""
from django.core.exceptions import ValidationError
from .source_phase6_entries import definition
from .source_entry_registry import ENTRY_RULES


def fields(model, entry):
    aliases=ENTRY_RULES[model._meta.label][entry]['field_aliases']
    return list(dict.fromkeys(aliases.get(field['FieldName'],field['FieldName']) for field in definition(entry)['fields']
            if field['FieldKind'] in ['CopyPrevRow', 'CopyLastRow']
            and aliases.get(field['FieldName'],field['FieldName']) in model.SOURCE_FIELDS))


def apply(item, data, source, entry):
    if type(source) is not type(item) or entry is None:
        raise ValidationError({'_entry_copy_from': '续行需要同一原表的来源行和明确业务类型。'})
    names = fields(type(item), entry)
    for name in names:
        key = item.SOURCE_FIELDS[name]
        if key not in data:
            data[key] = getattr(source, key)
            setattr(item, key, data[key])
    return names
