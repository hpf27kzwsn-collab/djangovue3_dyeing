"""客户本地原表业务的主从和字段归属。"""
def policy_for(model):
    from .source_services import managed_fields
    return {'owned': {model: managed_fields(model)}}


def document_children(model):
    from django.apps import apps
    from .source_ownership import OWNERS
    return {apps.get_model(label): rule['field'] for label,rules in OWNERS.items()
            for rule in rules if rule['target']==model._meta.label}
