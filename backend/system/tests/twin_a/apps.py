from django.apps import AppConfig

class TwinAConfig(AppConfig):
    name='system.tests.twin_a'
    label='identity_a'
    resource_options = {'ExcludedFileEntry': {'serializer_exclude_fields': ['attachment']}}
