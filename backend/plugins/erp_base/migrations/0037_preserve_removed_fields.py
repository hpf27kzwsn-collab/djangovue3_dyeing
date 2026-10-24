"""精简前保留有内容的附加字段，退役空的备用模型组件。"""
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db import migrations

REMOVED_SOURCE_FIELDS = ['description','remarks','approval_stage','confirmed_at','confirmed_by','approved_at','approved_by']
GEO = ['location','continent','country','province','city','district','isp','area_code','country_english','country_code','longitude','latitude']
OTHER_FIELDS = {
    'erp_base.SourceBusinessParameter':['captured_at'],
    'erp_base.LegacyImportBatch':['database_name','table_count','verified_at'],
    'erp_quality.QualityQuantityBatch':['sha256','database_name','captured_at','row_count','length_available','evidence'],
    'erp_quality.QualityQuantitySource':['source_row','detail_sheet_series'],
    'system.LoginLog':GEO,
}
MARKER = 'erp_base.0037_preserve_removed_fields'
RETIRED = ['erp_base.BusinessChoice', 'erp_base.BusinessUnit', 'erp_base.ChemicalSpecification', 'erp_base.ColorStandard', 'erp_base.CustomerMaterial', 'erp_base.Employee', 'erp_base.Factory', 'erp_base.LabelTemplate', 'erp_base.LegacyImportIssue', 'erp_base.LegacyObjectMap', 'erp_base.LegacySourceTable', 'erp_base.Machine', 'erp_base.MachineProcess', 'erp_base.Material', 'erp_base.PackagingSpecification', 'erp_base.Party', 'erp_base.PartyAddress', 'erp_base.PartyContact', 'erp_base.PartyRole', 'erp_base.Process', 'erp_base.Route', 'erp_base.RouteStep', 'erp_base.RouteVersion', 'erp_base.Shift', 'erp_base.StorageLocation', 'erp_base.Unit', 'erp_base.Warehouse', 'erp_base.WorkCenter', 'erp_base.YarnSpecification', 'erp_production.DyeBatch', 'erp_production.DyeBatchAllocation', 'erp_production.DyeBatchWorkCard', 'erp_production.ExecutionCorrection', 'erp_production.ExecutionMeasurement', 'erp_production.ExecutionWorker', 'erp_production.MaterialPlanLine', 'erp_production.MaterialPlanStage', 'erp_production.OperationExecution', 'erp_production.OperationParameter', 'erp_production.PhysicalBatchExecution', 'erp_production.PhysicalExecutionCorrection', 'erp_production.ProductionRecipe', 'erp_production.ReworkOrder', 'erp_production.ScheduleAssignment', 'erp_production.WeighingLine', 'erp_production.WeighingOrder', 'erp_production.WeighingRecord', 'erp_production.WeighingStage', 'erp_production.WorkCard', 'erp_production.WorkCardOperation', 'erp_production.WorkCardOrderAllocation', 'erp_production.WorkCardRequirement', 'erp_purchase.PurchaseOrder', 'erp_purchase.PurchaseOrderLine', 'erp_purchase.PurchaseRequest', 'erp_purchase.PurchaseRequestLine', 'erp_purchase.PurchaseReturn', 'erp_purchase.PurchaseReturnLine', 'erp_quality.InspectionResultLine', 'erp_quality.QualityDefect', 'erp_quality.QualityDisposition', 'erp_quality.QualityInspection', 'erp_sales.CommercialPrice', 'erp_sales.CommercialPriceLine', 'erp_sales.CustomerComplaint', 'erp_sales.CustomerComplaintLine', 'erp_sales.Delivery', 'erp_sales.DeliveryLine', 'erp_sales.SalesLineRequirement', 'erp_sales.SalesOrder', 'erp_sales.SalesOrderChange', 'erp_sales.SalesOrderChangeLine', 'erp_sales.SalesOrderLine', 'erp_sales.SalesReturn', 'erp_sales.SalesReturnLine', 'erp_sampling.ProcessCurveStep', 'erp_sampling.ProcessCurveVersion', 'erp_sampling.Recipe', 'erp_sampling.RecipeIngredient', 'erp_sampling.RecipeStage', 'erp_sampling.RecipeVersion', 'erp_sampling.SampleConfirmation', 'erp_sampling.SampleLine', 'erp_sampling.SampleRequest', 'erp_sampling.SampleTrial', 'erp_warehouse.InventoryLot', 'erp_warehouse.InventoryMovement', 'erp_warehouse.LabelPrint', 'erp_warehouse.LotTransformation', 'erp_warehouse.LotTransformationLine', 'erp_warehouse.Package', 'erp_warehouse.PackageDispositionAllocation', 'erp_warehouse.PackageOrderAllocation', 'erp_warehouse.StockAdjustment', 'erp_warehouse.StockAdjustmentLine', 'erp_warehouse.StockBalance', 'erp_warehouse.StockCount', 'erp_warehouse.StockCountLine', 'erp_warehouse.StockIssue', 'erp_warehouse.StockIssueLine', 'erp_warehouse.StockReceipt', 'erp_warehouse.StockReceiptLine', 'erp_warehouse.StockTransfer', 'erp_warehouse.StockTransferLine']


def preserve(apps,schema_editor):
    Action=apps.get_model('erp_base','BusinessAction')
    alias=schema_editor.connection.alias
    selected=[(m,REMOVED_SOURCE_FIELDS) for m in apps.get_models() if m._meta.app_label.startswith('erp_') and m._meta.db_table.startswith('src_')]
    selected += [(apps.get_model(label),names) for label,names in OTHER_FIELDS.items()]
    for model,names in selected:
        fields=[model._meta.get_field(name) for name in names]
        logs=[]
        for row in model.objects.using(alias).values('pk','dept_belong_id',*[f.attname for f in fields]).iterator(chunk_size=500):
            values={f.name:row[f.attname] for f in fields}
            if any(value is not None and value!='' for value in values.values()):
                values=json.loads(json.dumps(values,cls=DjangoJSONEncoder))
                logs.append(Action(entity=model._meta.label,object_id=row['pk'],action='field_cleanup',
                    reason='模型精简：保留已有附加说明和办理事实',before=values,after={'migration':MARKER},dept_belong_id=row['dept_belong_id']))
            if len(logs)==500:
                Action.objects.using(alias).bulk_create(logs);logs=[]
        Action.objects.using(alias).bulk_create(logs)
    component=[apps.get_model(label) for label in RETIRED]
    if not any(model.objects.using(alias).exists() for model in component):
        for model in reversed(component):schema_editor.delete_model(model)


def restore(apps,schema_editor):
    alias=schema_editor.connection.alias
    tables=set(schema_editor.connection.introspection.table_names())
    for label in RETIRED:
        model=apps.get_model(label)
        if model._meta.db_table not in tables:schema_editor.create_model(model)
    Action=apps.get_model('erp_base','BusinessAction')
    for log in Action.objects.using(alias).filter(action='field_cleanup',after__migration=MARKER).order_by('pk').iterator():
        model=apps.get_model(log.entity)
        values={}
        for name,value in log.before.items():
            field=model._meta.get_field(name)
            values[field.attname]=field.to_python(value)
        model.objects.using(alias).filter(pk=log.object_id).update(**values)


class Migration(migrations.Migration):
    dependencies = [('erp_base', '0036_customer_import_records'), ('erp_production', '0023_explicit_material_tighttube_parents'), ('erp_purchase', '0011_remove_purchaseorder_legacy_id_and_more'), ('erp_quality', '0014_remove_extra_source_ids'), ('erp_sales', '0018_remove_commercialprice_legacy_id_and_more'), ('erp_sampling', '0011_remove_processcurvestep_legacy_id_and_more'), ('erp_warehouse', '0017_explicit_material_tighttube_parents'), ('system', '0020_fieldpermission_sys_fieldpermission_role_field_and_more')]
    operations = [migrations.RunPython(preserve,restore)]
