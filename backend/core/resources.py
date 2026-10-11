def resource_options(model):
    return getattr(model._meta.app_config, 'resource_options', {}).get(model.__name__, {})


def relation_label(instance):
    fields = {field.name for field in instance._meta.fields}
    config = resource_options(type(instance))
    key = config['label_field'] if 'label_field' in config else next((key for key in ['name','title','label','username'] if key in fields), instance._meta.pk.name)
    return str(getattr(instance, key))
