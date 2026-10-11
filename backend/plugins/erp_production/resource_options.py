"""生产计划资源：按实际模型显式登记。"""
from plugins.erp_base.business_resources import options

MODEL_FIELDS = {'WorkCard': 'manual_creation_reason number document_at factory business_unit material specification_snapshot '
             'color_standard color_number_snapshot route_version planned_quantity quantity_unit planned_pieces '
             'planned_packages due_at is_urgent is_paused original_work_card status released_at completed_at '
             'closed_at',
 'WorkCardOrderAllocation': 'work_card order_line allocated_quantity unit is_primary adopted_order_snapshot',
 'DyeBatch': 'number factory original_batch planned_mass_kg planned_machine status',
 'DyeBatchWorkCard': 'batch work_card sequence quantity unit',
 'DyeBatchAllocation': 'batch_work_card work_card_allocation quantity unit',
 'WorkCardOperation': 'work_card sequence process route_step work_center is_required planned_minutes predecessor',
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
                     'quantity_unit'}

RELATIONS = {'WorkCard': {'factory': ('erp_base_factory', 'name'),
              'business_unit': ('erp_base_businessunit', 'name'),
              'material': ('erp_base_material', 'name'),
              'color_standard': ('erp_base_colorstandard', 'code'),
              'route_version': ('erp_base_routeversion', 'version'),
              'quantity_unit': ('erp_base_unit', 'name'),
              'original_work_card': ('erp_production_workcard', 'number')},
 'WorkCardOrderAllocation': {'work_card': ('erp_production_workcard', 'number'),
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
                      'quantity_unit': ('erp_base_unit', 'name')}}

VIEWSETS = {'WorkCard': 'plugins.erp_production.views.WorkCardViewSet',
 'WorkCardOrderAllocation': 'plugins.erp_base.business_api.BusinessViewSet',
 'DyeBatch': 'plugins.erp_production.views.DyeBatchViewSet',
 'DyeBatchWorkCard': 'plugins.erp_base.business_api.BusinessViewSet',
 'DyeBatchAllocation': 'plugins.erp_base.business_api.BusinessViewSet',
 'WorkCardOperation': 'plugins.erp_production.views.WorkCardOperationViewSet',
 'OperationParameter': 'plugins.erp_base.business_api.BusinessViewSet',
 'WorkCardRequirement': 'plugins.erp_base.business_api.BusinessViewSet',
 'ScheduleAssignment': 'plugins.erp_production.views.ScheduleAssignmentViewSet',
 'ProductionRecipe': 'plugins.erp_production.views.ProductionFactsViewSet',
 'MaterialPlanStage': 'plugins.erp_production.views.ProductionFactsViewSet',
 'MaterialPlanLine': 'plugins.erp_production.views.ProductionFactsViewSet'}

RESOURCE_OPTIONS = options('erp_production', MODEL_FIELDS, RELATIONS, VIEWSETS)
from .workflows import WORKFLOWS
for name, workflow in WORKFLOWS.items():
    RESOURCE_OPTIONS[name]['workflow'] = workflow
RESOURCE_OPTIONS['WorkCard']['label_field'] = 'number'
RESOURCE_OPTIONS['DyeBatch']['label_field'] = 'number'
