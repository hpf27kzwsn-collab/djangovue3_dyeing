"""各批业务资源的公共元数据；字段清单在各应用显式登记。"""


def options(app, fields, relations, viewsets):
    result = {}
    for name, keys in fields.items():
        result[name] = {
            'serializer': 'plugins.erp_base.business_api.BusinessSerializer',
            'viewset': viewsets[name],
            'crud_fields': ['id', *keys.split(), 'remarks', 'legacy_id', 'create_datetime', 'update_datetime'],
            'fields': {key: {'column': {'show': False}} for key in ('id', 'legacy_id', 'remarks')},
        }
        for key, target in relations[name].items():
            entity, label = target
            result[name]['fields'][key] = {'remote': {'entity': entity, 'pk': 'id', 'label': label}}
    return result
