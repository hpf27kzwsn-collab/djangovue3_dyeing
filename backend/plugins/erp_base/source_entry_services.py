from django.core.exceptions import ValidationError
from django.utils import timezone
from .business import persist
from .source_context import SourceDocumentContext
from .source_entry_registry import ENTRY_RULES
from .source_numbers import generate


def entry_for(item):
    if item.source_batch_id is not None or item.legacy_id is not None:
        return None
    name = SourceDocumentContext.objects.filter(entity=item._meta.label, object_id=item.pk).values_list('entry_name', flat=True).first()
    return None if name in ['explicit_outwork_closure', 'explicit_business_continuation', 'foundation_trigger'] else name


def resolve_entry(item, selected, owners):
    choices = ENTRY_RULES.get(item._meta.label, {})
    previous = None if item.pk is None else entry_for(item)
    if selected is not None:
        if selected not in choices:
            raise ValidationError({'_entry': '此业务模型没有所选旧入口。'})
        if item.source_batch_id is not None or item.legacy_id is not None:
            raise ValidationError({'_entry': '历史记录不补造使用入口；新接续业务另建单据。'})
        if previous is not None and previous != selected:
            raise ValidationError({'_entry': '已建立的单据保持原业务入口，其他类型另建单据。'})
        return selected
    if previous is not None:
        return previous
    owner_names = {name for owner in owners if (name := entry_for(owner)) is not None}
    inherited = [name for name, rule in choices.items() if name in owner_names or rule['master_entry'] in owner_names]
    return inherited[0] if len(inherited) == 1 else None


def apply_new_rules(item, data, actor, entry):
    rule = ENTRY_RULES[item._meta.label][entry]
    at = timezone.localtime()
    for old, definition in rule['default_fields'].items():
        key = item.SOURCE_FIELDS[old]
        if key in data:
            continue
        kind = definition['FieldKind']
        if kind == 'DefaultDate':
            value = at
        elif kind == 'DefaultValue':
            value = definition['DefaultValue']
        elif kind == 'LoginPeople_LoginName':
            value = actor.username
        else:
            value = actor.name
        if value is not None:
            setattr(item, key, item._meta.get_field(key).to_python(value))
    for old, definition in rule['number_fields'].items():
        key = item.SOURCE_FIELDS[old]
        if key not in data and key not in item.SOURCE_IDENTITIES:
            setattr(item, key, generate(item, old, definition, actor, at))


def save_context(item, actor, entry):
    context, created = SourceDocumentContext.objects.get_or_create(entity=item._meta.label, object_id=item.pk,
        defaults={'entry_name': entry, 'creator': actor, 'modifier': actor, 'dept_belong_id': item.dept_belong_id})
    if context.entry_name in ['explicit_outwork_closure', 'explicit_business_continuation', 'foundation_trigger']:
        context.entry_name = entry
        persist(context, actor)
    return context
