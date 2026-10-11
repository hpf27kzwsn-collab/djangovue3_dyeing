"""旧来源资料只读；管理命令完成文件核对及明确映射。"""
from .business_resources import options
MODEL_FIELDS={
    'LegacyImportBatch':'number database_name started_at finished_at manifest_sha256 table_count row_count byte_count verified_at note',
    'LegacySourceTable':'batch schema_name table_name modules columns primary_key row_count byte_count sha256',
    'LegacyObjectMap':'source_table row_number source_key target_model target_id mapped_fields',
    'LegacyImportIssue':'batch source_table row_number source_key target_model field_name category source_value detail handling is_resolved',
}
RELATIONS={
    'LegacyImportBatch':{},'LegacySourceTable':{'batch':('erp_base_legacyimportbatch','number')},
    'LegacyObjectMap':{'source_table':('erp_base_legacysourcetable','table_name')},
    'LegacyImportIssue':{'batch':('erp_base_legacyimportbatch','number'),'source_table':('erp_base_legacysourcetable','table_name')},
}
VIEWSETS={name:'plugins.erp_base.legacy_views.LegacyReadViewSet' for name in MODEL_FIELDS}
VIEWSETS.update({'LegacySourceTable':'plugins.erp_base.legacy_views.LegacySourceViewSet','LegacyObjectMap':'plugins.erp_base.legacy_views.LegacyMapViewSet'})
RESOURCE_OPTIONS=options('erp_base',MODEL_FIELDS,RELATIONS,VIEWSETS)
for resource in RESOURCE_OPTIONS.values():
    resource['workflow']={'readonly':True}
    resource['serializer']='core.api.CoreSerializer'
RESOURCE_OPTIONS['LegacyImportBatch']['workflow']['children']=[
    {'entity':'erp_base_legacysourcetable','title':'完整旧来源表','key':'batch'},
    {'entity':'erp_base_legacyimportissue','title':'待核实及差异','key':'batch'}]
RESOURCE_OPTIONS['LegacySourceTable']['workflow']['children']=[{'entity':'erp_base_legacyobjectmap','title':'明确逐项对照','key':'source_table'}]
RESOURCE_OPTIONS['LegacyImportBatch']['serializer_exclude_fields']=['source_directory']
RESOURCE_OPTIONS['LegacySourceTable']['serializer_exclude_fields']=['file_path']
