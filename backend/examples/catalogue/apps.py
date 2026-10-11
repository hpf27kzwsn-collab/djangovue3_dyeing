from django.apps import AppConfig


class CatalogueConfig(AppConfig):
    name = 'examples.catalogue'
    label = 'example_catalogue'
    verbose_name = '扩展接入示例'
    exclude_models = ['Note', 'NoteLine']
    resource_options = {'Entry': {'fields': {'amount': {'title':'金额', 'column':{'minWidth':180}}}}}
