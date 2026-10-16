from plugins.erp_base.business_resources import options

FIELDS={'QualityQuantityBatch':'sha256 database_name captured_at row_count length_available evidence',
    'QualityQuantitySource':'batch source_row detail_no detail_sheet_series header_sheet_series sheet_date sheet_kind business_unit job_number out_detail_no quantity stock_unit zero_amount metres'}
RELATIONS={'QualityQuantityBatch':{},'QualityQuantitySource':{'batch':('erp_quality_qualityquantitybatch','captured_at')}}
RESOURCE_OPTIONS=options('erp_quality',FIELDS,RELATIONS,{name:'plugins.erp_base.legacy_views.LegacyReadViewSet' for name in FIELDS})
for resource in RESOURCE_OPTIONS.values():
    resource['workflow']={'readonly':True}
    resource['serializer']='core.api.CoreSerializer'
RESOURCE_OPTIONS['QualityQuantityBatch']['workflow']['children']=[{'entity':'erp_quality_qualityquantitysource','title':'质量原数量明细','key':'batch'}]
