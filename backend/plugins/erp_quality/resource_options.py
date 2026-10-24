from .source_resources import RESOURCE_OPTIONS as SOURCE_RESOURCES
RESOURCE_OPTIONS=dict(SOURCE_RESOURCES)
from .quantity_resources import RESOURCE_OPTIONS as QUANTITY_RESOURCES
RESOURCE_OPTIONS.update(QUANTITY_RESOURCES)

from plugins.erp_base.foundation_catalog import configure_resources
configure_resources(RESOURCE_OPTIONS, 'erp_quality')

from plugins.erp_base.business_navigation import configure_resources as configure_business_navigation
configure_business_navigation(RESOURCE_OPTIONS, 'erp_quality')
