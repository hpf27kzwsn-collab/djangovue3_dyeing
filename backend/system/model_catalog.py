from django.apps import apps
from application.plugins import MODEL_EXCLUDE_APPS


def project_models():
    return [model for model in apps.get_models()
            if model._meta.app_label not in MODEL_EXCLUDE_APPS
            and model.__name__ not in getattr(model._meta.app_config, 'exclude_models', [])]


def permission_models():
    from .catalog import ENTITIES
    return list(dict.fromkeys([*project_models(), *ENTITIES.values()]))
