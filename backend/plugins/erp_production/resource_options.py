"""生产计划资源：按实际模型显式登记。"""
from plugins.erp_base.business_resources import options

MODEL_FIELDS = {'WorkCard': 'manual_creation_reason number document_at factory business_unit material specification_snapshot '
             'color_standard color_number_snapshot route_version planned_quantity quantity_unit planned_pieces '
             'planned_packages due_at is_urgent is_paused original_work_card status released_at completed_at '
             'closed_at',
 'WorkCardOrderAllocation': 'adopted_order_snapshot original_allocation released_unfulfilled_quantity '
                            'demand_release_at demand_release_reason work_card order_line allocated_quantity unit '
                            'is_primary',
 'DyeBatch': 'number factory original_batch planned_mass_kg planned_machine status',
 'DyeBatchWorkCard': 'batch work_card sequence quantity unit',
 'DyeBatchAllocation': 'batch_work_card work_card_allocation quantity unit',
 'WorkCardOperation': 'is_skipped skip_reason work_card sequence process route_step work_center is_required '
                      'planned_minutes predecessor',
 'OperationParameter': 'operation sequence name required_value_text unit_text',
 'WorkCardRequirement': 'work_card source_order_requirement namespace code name_snapshot value_text',
 'ScheduleAssignment': 'change_reason previous_assignment batch operation machine planned_start planned_end '
                       'version status',
 'ProductionRecipe': 'batch recipe_version adoption_number adopted_at dry_mass_kg status',
 'MaterialPlanStage': 'bath_density_kg_per_litre production_recipe sequence recipe_stage phase_name_snapshot '
                      'phase curve_version ph_text bath_ratio bath_ratio_basis water_amount water_unit '
                      'temperature_c minutes',
 'MaterialPlanLine': 'calculation_snapshot stage sequence recipe_ingredient material original_dosage '
                     'adjustment_percent adopted_dosage dosage_basis original_required_quantity required_quantity '
                     'quantity_unit',
 'OperationExecution': 'physical_execution operation batch execution_number machine shift started_at ended_at '
                       'input_quantity input_unit output_quantity output_unit output_mass_kg output_length_m '
                       'output_pieces defect_quantity status quality_note',
 'ExecutionWorker': 'execution employee role participation_minutes',
 'ExecutionMeasurement': 'execution planned_parameter name value_text measured_at',
 'ExecutionCorrection': 'before_values after_values execution reason corrected_at changes_quantity '
                        'new_output_quantity changes_mass new_output_mass_kg changes_start_time new_started_at '
                        'changes_end_time new_ended_at approved_by',
 'PhysicalBatchExecution': 'batch process machine execution_number operator shift started_at ended_at '
                           'output_mass_kg status',
 'PhysicalExecutionCorrection': 'physical_execution corrected_at approved_by reason before_values after_values '
                                'member_changes',
 'WeighingOrder': 'number document_at batch kind production_recipe reason status',
 'WeighingStage': 'order sequence plan_stage phase_name_snapshot phase curve_version ph_text bath_ratio '
                  'bath_ratio_basis water_amount water_unit temperature_c minutes',
 'WeighingLine': 'stage sequence plan_line material planned_quantity unit status',
 'WeighingRecord': 'void_reason voided_at line quantity unit source measured_at operator original_record is_void',
 'QualityInspection': 'is_void voided_at void_reason inspected_quantity quantity_unit lot receipt_line number '
                      'work_card execution package kind inspected_at inspector result grade previous_inspection',
 'InspectionResultLine': 'inspection item_code item_name_snapshot value_text numeric_value unit result',
 'QualityDisposition': 'status supersedes inspection kind quantity unit reason approved_by approved_at',
 'QualityDefect': 'number work_card execution inspection occurred_at defect_description source_defect_codes '
                  'quantity unit pieces responsible_process responsible_employee discovering_process '
                  'discovering_employee disposition status',
 'ReworkOrder': 'number original_work_card disposition rework_work_card quantity unit reason status'}

RELATIONS = {'WorkCard': {'factory': ('erp_base_factory', 'name'),
              'business_unit': ('erp_base_businessunit', 'name'),
              'material': ('erp_base_material', 'name'),
              'color_standard': ('erp_base_colorstandard', 'code'),
              'route_version': ('erp_base_routeversion', 'version'),
              'quantity_unit': ('erp_base_unit', 'name'),
              'original_work_card': ('erp_production_workcard', 'number')},
 'WorkCardOrderAllocation': {'original_allocation': ('erp_production_workcardorderallocation', 'id'),
                             'work_card': ('erp_production_workcard', 'number'),
                             'order_line': ('erp_sales_salesorderline', 'line_number'),
                             'unit': ('erp_base_unit', 'name')},
 'DyeBatch': {'factory': ('erp_base_factory', 'name'),
              'original_batch': ('erp_production_dyebatch', 'number'),
              'planned_machine': ('erp_base_machine', 'name')},
 'DyeBatchWorkCard': {'batch': ('erp_production_dyebatch', 'number'),
                      'work_card': ('erp_production_workcard', 'number'),
                      'unit': ('erp_base_unit', 'name')},
 'DyeBatchAllocation': {'batch_work_card': ('erp_production_dyebatchworkcard', 'id'),
                        'work_card_allocation': ('erp_production_workcardorderallocation', 'id'),
                        'unit': ('erp_base_unit', 'name')},
 'WorkCardOperation': {'work_card': ('erp_production_workcard', 'number'),
                       'process': ('erp_base_process', 'name'),
                       'route_step': ('erp_base_routestep', 'sequence'),
                       'work_center': ('erp_base_workcenter', 'name'),
                       'predecessor': ('erp_production_workcardoperation', 'id')},
 'OperationParameter': {'operation': ('erp_production_workcardoperation', 'id')},
 'WorkCardRequirement': {'work_card': ('erp_production_workcard', 'number'),
                         'source_order_requirement': ('erp_sales_saleslinerequirement', 'name')},
 'ScheduleAssignment': {'previous_assignment': ('erp_production_scheduleassignment', 'id'),
                        'batch': ('erp_production_dyebatch', 'number'),
                        'operation': ('erp_production_workcardoperation', 'id'),
                        'machine': ('erp_base_machine', 'name')},
 'ProductionRecipe': {'batch': ('erp_production_dyebatch', 'number'),
                      'recipe_version': ('erp_sampling_recipeversion', 'version')},
 'MaterialPlanStage': {'production_recipe': ('erp_production_productionrecipe', 'id'),
                       'recipe_stage': ('erp_sampling_recipestage', 'sequence'),
                       'phase': ('erp_base_businesschoice', 'name'),
                       'curve_version': ('erp_sampling_processcurveversion', 'code'),
                       'water_unit': ('erp_base_unit', 'name')},
 'MaterialPlanLine': {'stage': ('erp_production_materialplanstage', 'id'),
                      'recipe_ingredient': ('erp_sampling_recipeingredient', 'sequence'),
                      'material': ('erp_base_material', 'name'),
                      'quantity_unit': ('erp_base_unit', 'name')},
 'OperationExecution': {'physical_execution': ('erp_production_physicalbatchexecution', 'id'),
                        'operation': ('erp_production_workcardoperation', 'id'),
                        'batch': ('erp_production_dyebatch', 'number'),
                        'machine': ('erp_base_machine', 'name'),
                        'shift': ('erp_base_shift', 'id'),
                        'input_unit': ('erp_base_unit', 'name'),
                        'output_unit': ('erp_base_unit', 'name')},
 'ExecutionWorker': {'execution': ('erp_production_operationexecution', 'execution_number'),
                     'employee': ('erp_base_employee', 'name')},
 'ExecutionMeasurement': {'execution': ('erp_production_operationexecution', 'execution_number'),
                          'planned_parameter': ('erp_production_operationparameter', 'id')},
 'ExecutionCorrection': {'execution': ('erp_production_operationexecution', 'execution_number'),
                         'approved_by': ('erp_base_employee', 'name')},
 'PhysicalBatchExecution': {'batch': ('erp_production_dyebatch', 'number'),
                            'process': ('erp_base_process', 'name'),
                            'machine': ('erp_base_machine', 'name'),
                            'operator': ('erp_base_employee', 'name'),
                            'shift': ('erp_base_shift', 'id')},
 'PhysicalExecutionCorrection': {'physical_execution': ('erp_production_physicalbatchexecution', 'id'),
                                 'approved_by': ('erp_base_employee', 'name')},
 'WeighingOrder': {'batch': ('erp_production_dyebatch', 'number'),
                   'production_recipe': ('erp_production_productionrecipe', 'id')},
 'WeighingStage': {'order': ('erp_production_weighingorder', 'number'),
                   'plan_stage': ('erp_production_materialplanstage', 'id'),
                   'phase': ('erp_base_businesschoice', 'name'),
                   'curve_version': ('erp_sampling_processcurveversion', 'code'),
                   'water_unit': ('erp_base_unit', 'name')},
 'WeighingLine': {'stage': ('erp_production_weighingstage', 'id'),
                  'plan_line': ('erp_production_materialplanline', 'id'),
                  'material': ('erp_base_material', 'name'),
                  'unit': ('erp_base_unit', 'name')},
 'WeighingRecord': {'line': ('erp_production_weighingline', 'sequence'),
                    'unit': ('erp_base_unit', 'name'),
                    'operator': ('erp_base_employee', 'name'),
                    'original_record': ('erp_production_weighingrecord', 'id')},
 'QualityInspection': {'quantity_unit': ('erp_base_unit', 'name'),
                       'lot': ('erp_warehouse_inventorylot', 'id'),
                       'receipt_line': ('erp_warehouse_stockreceiptline', 'id'),
                       'work_card': ('erp_production_workcard', 'number'),
                       'execution': ('erp_production_operationexecution', 'execution_number'),
                       'package': ('erp_warehouse_package', 'code'),
                       'inspector': ('erp_base_employee', 'name'),
                       'grade': ('erp_base_businesschoice', 'name'),
                       'previous_inspection': ('erp_production_qualityinspection', 'number')},
 'InspectionResultLine': {'inspection': ('erp_production_qualityinspection', 'number'),
                          'unit': ('erp_base_unit', 'name')},
 'QualityDisposition': {'supersedes': ('erp_production_qualitydisposition', 'id'),
                        'inspection': ('erp_production_qualityinspection', 'number'),
                        'unit': ('erp_base_unit', 'name'),
                        'approved_by': ('erp_base_employee', 'name')},
 'QualityDefect': {'work_card': ('erp_production_workcard', 'number'),
                   'execution': ('erp_production_operationexecution', 'execution_number'),
                   'inspection': ('erp_production_qualityinspection', 'number'),
                   'unit': ('erp_base_unit', 'name'),
                   'responsible_process': ('erp_base_process', 'name'),
                   'responsible_employee': ('erp_base_employee', 'name'),
                   'discovering_process': ('erp_base_process', 'name'),
                   'discovering_employee': ('erp_base_employee', 'name'),
                   'disposition': ('erp_production_qualitydisposition', 'id')},
 'ReworkOrder': {'original_work_card': ('erp_production_workcard', 'number'),
                 'disposition': ('erp_production_qualitydisposition', 'id'),
                 'rework_work_card': ('erp_production_workcard', 'number'),
                 'unit': ('erp_base_unit', 'name')}}

VIEWSETS = {'WorkCard': 'plugins.erp_production.views.WorkCardViewSet',
 'WorkCardOrderAllocation': 'plugins.erp_base.business_api.BusinessViewSet',
 'DyeBatch': 'plugins.erp_production.execution_views.ActualBatchViewSet',
 'DyeBatchWorkCard': 'plugins.erp_base.business_api.BusinessViewSet',
 'DyeBatchAllocation': 'plugins.erp_base.business_api.BusinessViewSet',
 'WorkCardOperation': 'plugins.erp_production.execution_views.ActualOperationViewSet',
 'OperationParameter': 'plugins.erp_base.business_api.BusinessViewSet',
 'WorkCardRequirement': 'plugins.erp_base.business_api.BusinessViewSet',
 'ScheduleAssignment': 'plugins.erp_production.views.ScheduleAssignmentViewSet',
 'ProductionRecipe': 'plugins.erp_production.execution_views.ProductionRecipeViewSet',
 'MaterialPlanStage': 'plugins.erp_production.views.ProductionFactsViewSet',
 'MaterialPlanLine': 'plugins.erp_production.views.ProductionFactsViewSet',
 'OperationExecution': 'plugins.erp_production.execution_views.ExecutionViewSet',
 'ExecutionWorker': 'plugins.erp_base.business_api.BusinessViewSet',
 'ExecutionMeasurement': 'plugins.erp_base.business_api.BusinessViewSet',
 'ExecutionCorrection': 'plugins.erp_production.views.ProductionFactsViewSet',
 'PhysicalBatchExecution': 'plugins.erp_production.execution_views.PhysicalExecutionViewSet',
 'PhysicalExecutionCorrection': 'plugins.erp_production.views.ProductionFactsViewSet',
 'WeighingOrder': 'plugins.erp_production.execution_views.WeighingOrderViewSet',
 'WeighingStage': 'plugins.erp_base.business_api.BusinessViewSet',
 'WeighingLine': 'plugins.erp_production.execution_views.WeighingLineViewSet',
 'WeighingRecord': 'plugins.erp_production.execution_views.WeighingRecordViewSet',
 'QualityInspection': 'plugins.erp_production.execution_views.QualityInspectionViewSet',
 'InspectionResultLine': 'plugins.erp_base.business_api.BusinessViewSet',
 'QualityDisposition': 'plugins.erp_production.views.ProductionFactsViewSet',
 'QualityDefect': 'plugins.erp_production.execution_views.QualityDefectViewSet',
 'ReworkOrder': 'plugins.erp_production.execution_views.ReworkOrderViewSet'}

RESOURCE_OPTIONS = options('erp_production', MODEL_FIELDS, RELATIONS, VIEWSETS)
from .workflows import WORKFLOWS
for name, workflow in WORKFLOWS.items():
    RESOURCE_OPTIONS[name]['workflow'] = workflow
RESOURCE_OPTIONS['WorkCard']['label_field'] = 'number'
RESOURCE_OPTIONS['DyeBatch']['label_field'] = 'number'
from .execution_workflows import WORKFLOWS as ACTUAL_WORKFLOWS
for name, workflow in ACTUAL_WORKFLOWS.items():
    RESOURCE_OPTIONS[name]['workflow'] = workflow
RESOURCE_OPTIONS['OperationExecution']['serializer'] = 'plugins.erp_production.execution_views.ExecutionSerializer'
RESOURCE_OPTIONS['OperationExecution']['crud_fields'] += ['work_card_number','effective_facts']
RESOURCE_OPTIONS['OperationExecution']['fields'].update({'work_card_number': {'title':'工卡号','source':'operation'}, 'effective_facts': {'title':'更正后有效事实','kind':'json','source':'operation'}})
RESOURCE_OPTIONS['WorkCardOrderAllocation']['viewset']='plugins.erp_production.execution_views.WorkCardAllocationViewSet'
RESOURCE_OPTIONS['WorkCardOrderAllocation']['serializer']='plugins.erp_production.execution_views.WorkCardAllocationSerializer'
RESOURCE_OPTIONS['WorkCardOrderAllocation']['crud_fields'].append('order_number')
RESOURCE_OPTIONS['WorkCardOrderAllocation']['fields']['order_number']={'title':'原订单号','source':'order_line'}

RESOURCE_OPTIONS['PhysicalBatchExecution']['serializer']='plugins.erp_production.execution_views.PhysicalExecutionSerializer'
RESOURCE_OPTIONS['PhysicalBatchExecution']['crud_fields'].append('effective_facts')
RESOURCE_OPTIONS['PhysicalBatchExecution']['fields']['effective_facts']={'title':'更正后有效整缸事实','kind':'json','source':'batch'}
