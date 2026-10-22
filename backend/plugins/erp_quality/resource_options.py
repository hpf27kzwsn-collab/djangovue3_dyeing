from plugins.erp_base.business_resources import options
from .workflows import WORKFLOWS

MODEL_FIELDS = {'QualityInspection': 'is_void voided_at void_reason inspected_quantity quantity_unit lot receipt_line number work_card execution package kind inspected_at inspector result grade previous_inspection', 'InspectionResultLine': 'inspection item_code item_name_snapshot value_text numeric_value unit result', 'QualityDisposition': 'status supersedes inspection kind quantity unit reason approved_by approved_at', 'QualityDefect': 'number work_card execution inspection occurred_at defect_description source_defect_codes quantity unit pieces responsible_process responsible_employee discovering_process discovering_employee disposition status'}
RELATIONS = {'QualityInspection': {'quantity_unit': ('erp_base_unit', 'name'), 'lot': ('erp_warehouse_inventorylot', 'id'), 'receipt_line': ('erp_warehouse_stockreceiptline', 'id'), 'work_card': ('erp_production_workcard', 'number'), 'execution': ('erp_production_operationexecution', 'execution_number'), 'package': ('erp_warehouse_package', 'code'), 'inspector': ('erp_base_employee', 'name'), 'grade': ('erp_base_businesschoice', 'name'), 'previous_inspection': ('erp_quality_qualityinspection', 'number')}, 'InspectionResultLine': {'inspection': ('erp_quality_qualityinspection', 'number'), 'unit': ('erp_base_unit', 'name')}, 'QualityDisposition': {'supersedes': ('erp_quality_qualitydisposition', 'id'), 'inspection': ('erp_quality_qualityinspection', 'number'), 'unit': ('erp_base_unit', 'name'), 'approved_by': ('erp_base_employee', 'name')}, 'QualityDefect': {'work_card': ('erp_production_workcard', 'number'), 'execution': ('erp_production_operationexecution', 'execution_number'), 'inspection': ('erp_quality_qualityinspection', 'number'), 'unit': ('erp_base_unit', 'name'), 'responsible_process': ('erp_base_process', 'name'), 'responsible_employee': ('erp_base_employee', 'name'), 'discovering_process': ('erp_base_process', 'name'), 'discovering_employee': ('erp_base_employee', 'name'), 'disposition': ('erp_quality_qualitydisposition', 'id')}}
VIEWSETS = {'QualityInspection': 'plugins.erp_quality.views.QualityInspectionViewSet', 'InspectionResultLine': 'plugins.erp_base.business_api.BusinessViewSet', 'QualityDisposition': 'plugins.erp_production.views.ProductionFactsViewSet', 'QualityDefect': 'plugins.erp_quality.views.QualityDefectViewSet'}
RESOURCE_OPTIONS=options('erp_quality',MODEL_FIELDS,RELATIONS,VIEWSETS)
for name,workflow in WORKFLOWS.items():RESOURCE_OPTIONS[name]['workflow']=workflow

from .source_resources import RESOURCE_OPTIONS as SOURCE_RESOURCES
RESOURCE_OPTIONS.update(SOURCE_RESOURCES)
from .quantity_resources import RESOURCE_OPTIONS as QUANTITY_RESOURCES
RESOURCE_OPTIONS.update(QUANTITY_RESOURCES)

from plugins.erp_base.foundation_catalog import configure_resources
configure_resources(RESOURCE_OPTIONS, 'erp_quality')

from plugins.erp_base.business_navigation import configure_resources as configure_business_navigation
configure_business_navigation(RESOURCE_OPTIONS, 'erp_quality')
