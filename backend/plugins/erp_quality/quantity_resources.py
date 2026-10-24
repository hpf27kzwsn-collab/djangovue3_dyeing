from plugins.erp_base.business_resources import options

FIELDS={'QualityQuantityBatch':'name',
    'QualityQuantitySource':'batch detail_no header_sheet_series sheet_date sheet_kind business_unit job_number out_detail_no quantity stock_unit zero_amount metres'}
RELATIONS={'QualityQuantityBatch':{},'QualityQuantitySource':{'batch':('erp_quality_qualityquantitybatch','name')}}
RESOURCE_OPTIONS=options('erp_quality',FIELDS,RELATIONS,{name:'system.views.ResourceViewSet' for name in FIELDS})
for resource in RESOURCE_OPTIONS.values():
    resource['serializer']='core.api.CoreSerializer'
RESOURCE_OPTIONS['QualityQuantityBatch']['workflow']={'children':[{'entity':'erp_quality_qualityquantitysource','title':'统计数量明细','key':'batch','atomic':False}]}
