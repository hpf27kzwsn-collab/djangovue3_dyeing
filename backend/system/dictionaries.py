from .models import Dictionary, Users, Post


def dictionary_value(row):
    if row.value is None:
        return None
    if row.type == 1:
        return float(row.value)
    if row.type == 6:
        return row.value.lower() == 'true'
    return row.value


def dictionary_options(key):
    return [{'label':row.label, 'value':dictionary_value(row), 'color':row.color}
            for row in Dictionary.objects.filter(parent__value=key, parent__status=True,
                                                is_value=True, status=True)]


def dictionary_key(model, field):
    if model == Users and field in ['gender', 'user_type']:
        return field
    if model == Post and field == 'status':
        return 'post_status'
    if field in ['status', 'is_active', 'enable'] and model._meta.get_field(field).get_internal_type() == 'BooleanField':
        return 'button_status_bool'


def initialize_dictionaries():
    definitions = [('gender', '性别', Users._meta.get_field('gender').choices, 1),
                   ('user_type', '用户类型', Users._meta.get_field('user_type').choices, 1),
                   ('post_status', '岗位状态', Post._meta.get_field('status').choices, 1),
                   ('button_status_bool', '启用状态', [(True,'启用'),(False,'停用')], 6)]
    for key, title, values, kind in definitions:
        root, created = Dictionary.objects.get_or_create(value=key, parent=None,
                                                        defaults={'label':title})
        if created:
            Dictionary.objects.bulk_create([Dictionary(parent=root,label=label,
                value=str(value).lower() if kind == 6 else str(value), type=kind,is_value=True,sort=sort)
                for sort,(value,label) in enumerate(values)])
