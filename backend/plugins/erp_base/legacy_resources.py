"""客户本地导入记录；开发原始文件浏览与旧新映射不注册。"""
from .business_resources import options
MODEL_FIELDS={
    'LegacyImportBatch':'number started_at finished_at row_count byte_count note',
    'LegacyImportIssue':'batch row_number target_model field_name category source_value detail handling is_resolved',
}
RELATIONS={'LegacyImportBatch':{},'LegacyImportIssue':{'batch':('erp_base_legacyimportbatch','number')}}
RESOURCE_OPTIONS=options('erp_base',MODEL_FIELDS,RELATIONS,
    {name:'plugins.erp_base.business_api.BusinessActionViewSet' for name in MODEL_FIELDS})
for resource in RESOURCE_OPTIONS.values():
    resource['workflow']={'readonly':True}
    resource['serializer']='core.api.CoreSerializer'
RESOURCE_OPTIONS['LegacyImportBatch']['serializer_exclude_fields']=['source_directory']
RESOURCE_OPTIONS['LegacyImportIssue']['serializer_exclude_fields']=['source_table','source_key']
