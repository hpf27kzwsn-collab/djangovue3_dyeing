"""旧业务码等值连接和有审计的明确字段回写。"""
from django.db.models.functions import Upper, RTrim
from django.db import transaction
from .business import locked, persist, record, snapshot
from .source_calculations import store_value


def matching(query, **values):
    for old, value in values.items():
        if value is None:  # SQL 等号不匹配 NULL，包括另一侧也是 NULL。
            return query.none()
        field = query.model.SOURCE_FIELDS[old]
        query = query.alias(**{f'match_{field}': Upper(RTrim(field))}).filter(
            **{f'match_{field}': value.rstrip(' ').upper()})
    return query


@transaction.atomic
def update_rows(query, values, actor, action, reason):
    for item in query.order_by('pk'):
        item = locked(item)
        converted = dict(store_value(item, old, value) for old, value in values.items())
        changed = {key: value for key, value in converted.items() if getattr(item, key) != value}
        if changed:
            before = snapshot(item)
            for key, value in changed.items():
                setattr(item, key, value)
            persist(item, actor)
            if item.SOURCE_TABLE=='QuoteDetail':
                from .source_quote_rules import saved
                saved(item,converted,False,actor)
            record(item, action, before, actor, reason)
        elif item.SOURCE_TABLE=='QuoteDetail':
            from .source_quote_rules import saved
            saved(item,converted,False,actor)
        from .source_master_data import saved as master_saved
        master_saved(item, converted, False, actor)
