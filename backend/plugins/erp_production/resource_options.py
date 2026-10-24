from .source_resources import RESOURCE_OPTIONS as SOURCE_RESOURCES
RESOURCE_OPTIONS=dict(SOURCE_RESOURCES)

from plugins.erp_base.foundation_catalog import configure_resources
configure_resources(RESOURCE_OPTIONS, 'erp_production')

from plugins.erp_base.business_navigation import configure_resources as configure_business_navigation
configure_business_navigation(RESOURCE_OPTIONS, 'erp_production')
