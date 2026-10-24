from .source_resources import RESOURCE_OPTIONS as SOURCE_RESOURCES
from .legacy_resources import RESOURCE_OPTIONS as IMPORT_RESOURCES
RESOURCE_OPTIONS=dict(SOURCE_RESOURCES)
RESOURCE_OPTIONS.update(IMPORT_RESOURCES)
RESOURCE_OPTIONS['BusinessAction']={'viewset':'plugins.erp_base.business_api.BusinessActionViewSet','serializer':'core.api.CoreSerializer','workflow':{'readonly':True}}
RESOURCE_OPTIONS['SourceIdentitySequence'] = {
    'viewset': 'plugins.erp_base.business_api.BusinessActionViewSet',
    'crud_fields': ['id','namespace','last_number','create_datetime','update_datetime'],
}
RESOURCE_OPTIONS['SourceDocumentContext'] = {
    'viewset': 'plugins.erp_base.business_api.BusinessActionViewSet',
    'crud_fields': ['id', 'entity', 'object_id', 'entry_name', 'create_datetime'],
}
RESOURCE_OPTIONS['SourceBusinessParameter'] = {
    'viewset': 'system.views.ResourceViewSet',
    'serializer': 'core.api.CoreSerializer',
    'crud_fields': ['id', 'name', 'value', 'remarks', 'create_datetime', 'update_datetime'],
    'label_field': 'name',
    'fields': {},
}


RESOURCE_OPTIONS['NumberingRule'] = {
    'viewset': 'plugins.erp_base.numbering_api.NumberingViewSet',
    'serializer': 'plugins.erp_base.numbering_api.NumberingSerializer',
    'label_field': 'name',
    'crud_fields': ['id', 'name', 'target_model', 'target_field', 'scope_key', 'scope_filters', 'entry_name',
                    'prefix', 'digits', 'start_number', 'last_number', 'auto_enabled',
                    'allow_manual_input', 'allow_code_change', 'notes', 'create_datetime', 'update_datetime'],
}

from plugins.erp_base.foundation_catalog import configure_resources
configure_resources(RESOURCE_OPTIONS, 'erp_base')

from plugins.erp_base.business_navigation import configure_resources as configure_business_navigation
configure_business_navigation(RESOURCE_OPTIONS, 'erp_base')
