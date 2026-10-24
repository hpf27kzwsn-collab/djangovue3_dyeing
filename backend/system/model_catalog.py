from django.apps import apps
from application.plugins import MODEL_EXCLUDE_APPS


def project_models():
    from plugins.erp_base.customer_resources import exposed_model
    return [model for model in apps.get_models()
            if model._meta.app_label not in MODEL_EXCLUDE_APPS
            and model.__name__ not in getattr(model._meta.app_config, 'exclude_models', [])
            and exposed_model(model)]


def permission_models():
    from .catalog import ENTITIES
    return list(dict.fromkeys(ENTITIES.values()))
