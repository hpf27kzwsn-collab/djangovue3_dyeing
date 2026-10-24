"""客户本地导入批次。"""
from .business_resources import options
MODEL_FIELDS={'LegacyImportBatch':'number started_at finished_at row_count byte_count note'}
RESOURCE_OPTIONS=options('erp_base',MODEL_FIELDS,{'LegacyImportBatch':{}},
    {'LegacyImportBatch':'plugins.erp_base.business_api.BusinessActionViewSet'})
RESOURCE_OPTIONS['LegacyImportBatch'].update(serializer='core.api.CoreSerializer',workflow={'readonly':True})
