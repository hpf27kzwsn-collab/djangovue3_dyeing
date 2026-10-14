from plugins.erp_quality import models as q
"""跨模块查询使用各来源的查询、字段和数据范围权限。"""
import csv,io
from decimal import Decimal
from types import SimpleNamespace
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from core.permissions import ApiPermission,scoped_queryset,field_access
from core.responses import success
from plugins.erp_sales import models as sales
from plugins.erp_production import models as production
from plugins.erp_warehouse import models as warehouse
from . import models as base


REPORTS={
    'orders':{'title':'订单需求与交付进度','columns':[('number','订单号'),('line_number','行号'),('material','物料ID'),('unit','数量单位'),
        ('ordered','原订货量'),('allocated','原需求有效分配'),('rework_allocated','返修承接计划'),('packed','包装实际量'),('delivered','实际交付量'),('returned','实际退回量'),('reopened','重新打开需求'),('remaining','未交付需求')]},
    'production':{'title':'工卡实际执行进度','columns':[('number','工卡号'),('status','工卡状态'),('process','工序ID'),('round','执行轮次'),
        ('machine','实际机台ID'),('execution_status','执行状态'),('started_at','实际开工'),('ended_at','实际完工'),('mass_kg','有效实绩kg'),('skipped','明确跳过')]},
    'materials':{'title':'计划、实称与净领用','columns':[('order','料单号'),('sequence','行号'),('material','染化料ID'),('unit','单位'),
        ('planned','计划量'),('measured','有效实称'),('issued','实际领出'),('returned','实际退料'),('net_issued','净领用'),('difference','净领用减计划')]},
    'quality':{'title':'检验范围与数量处置','columns':[('number','检验单'),('kind','检验类型'),('work_card','工卡ID'),('result','实际判定'),
        ('void','取消采用'),('inspected_at','检验时间'),('scope','检验覆盖量'),('scope_unit','覆盖单位'),('disposition','处置类型'),('quantity','处置数量'),('unit','处置单位'),('adoption','采用状态')]},
    'stock':{'title':'货权、批次、库位与质量库存','columns':[('lot','批次号'),('material','物料ID'),('owner','货权ID'),('location','库位ID'),
        ('quality','质量状态'),('package','包装ID'),('quantity','库存量'),('unit','库存单位')]},
    'packages':{'title':'包装细码与实际收发','columns':[('code','包装号'),('barcode','条码'),('work_card','工卡ID'),('source_execution','实际产出ID'),
        ('status','包装状态'),('packed_at','实际包装时间'),('net_mass_kg','包装净重kg'),('pieces','粒数'),('received','有效成品入库'),('issued','有效交付出库'),('returned','实际客户退回'),('unit','库存单位')]},
}


class ReportInput(serializers.Serializer):
    page=serializers.IntegerField(min_value=1,default=1)
    page_size=serializers.IntegerField(min_value=1,max_value=200,default=50)
    start=serializers.DateTimeField(required=False)
    end=serializers.DateTimeField(required=False)
    status=serializers.CharField(required=False)
    barcode=serializers.CharField(required=False,trim_whitespace=False)


class Reader:
    def __init__(self,request):self.request=request;self.units={}
    def source(self,model,columns):
        scope=SimpleNamespace(user=self.request.user,method='GET',path='/api/system/'+model._meta.app_label+'_'+model._meta.model_name+'/')
        if not ApiPermission().has_permission(scope,None):raise PermissionDenied('没有来源 '+str(model._meta.verbose_name)+' 的查询权限。')
        access=field_access(self.request.user,model)
        if not self.request.user.is_superuser and any(not access[key]['is_query'] for key in columns if key!='id'):
            raise PermissionDenied('来源 '+str(model._meta.verbose_name)+' 的报表所需字段未授权。')
        return scoped_queryset(model.objects.all(),scope)
    def labels(self,model,field,ids):
        ids={key for key in ids if key is not None}
        rows={row.pk:getattr(row,field) for row in self.source(model,[field]).filter(pk__in=ids)}
        if set(rows)!=ids:raise PermissionDenied('关联来源超出当前查询范围。')
        return rows
    def load_units(self):self.units={row.pk:row for row in self.source(base.Unit,['name','dimension','factor_to_base','base_unit'])}
    def unit(self,key):
        if key not in self.units:raise PermissionDenied('数量单位超出当前查询数据范围。')
        return self.units[key]
    def total(self,rows,quantity,unit,target):return sum((self.unit(getattr(row,unit+'_id')).convert_quantity(getattr(row,quantity),target) for row in rows),Decimal('0'))


def page(query,filters,time_field=None,status_field=None):
    if time_field is not None:
        if 'start' in filters:query=query.filter(**{time_field+'__gte':filters['start']})
        if 'end' in filters:query=query.filter(**{time_field+'__lt':filters['end']})
    if status_field is not None and 'status' in filters:query=query.filter(**{status_field:filters['status']})
    count=query.count();offset=(filters['page']-1)*filters['page_size']
    return count,list(query.order_by('-pk')[offset:offset+filters['page_size']])


def orders(reader,filters):
    headers=reader.source(sales.SalesOrder,['number','document_at','status'])
    count,heads=page(headers,filters,'document_at','status');ids=[row.pk for row in heads];headmap={row.pk:row for row in heads}
    lines=list(reader.source(sales.SalesOrderLine,['order','line_number','material','ordered_quantity','ordered_unit']).filter(order_id__in=ids))
    line_ids=[row.pk for row in lines]
    cards=reader.source(production.WorkCard,['status']).exclude(status='cancelled').values('pk')
    allocations=list(reader.source(production.WorkCardOrderAllocation,['order_line','work_card','allocated_quantity','released_unfulfilled_quantity','original_allocation','unit']).filter(order_line_id__in=line_ids,work_card_id__in=cards))
    packages=reader.source(warehouse.Package,['status']).exclude(status__in=['draft','void']).values('pk')
    packed=list(reader.source(warehouse.PackageOrderAllocation,['package','work_card_allocation','quantity','unit']).filter(work_card_allocation_id__in=[row.pk for row in allocations],package_id__in=packages))
    issues=reader.source(warehouse.StockIssue,['status']).filter(status='posted').values('pk')
    delivery_ids=reader.source(sales.Delivery,['status','warehouse_issue']).filter(status='delivered',warehouse_issue_id__in=issues).values('pk')
    delivered=list(reader.source(sales.DeliveryLine,['order_line','delivery','quantity','unit']).filter(order_line_id__in=line_ids,delivery_id__in=delivery_ids))
    receipts=reader.source(warehouse.StockReceipt,['status']).filter(status='posted').values('pk')
    receipt_rows=reader.source(warehouse.StockReceiptLine,['receipt']).filter(receipt_id__in=receipts).values('pk')
    return_heads=reader.source(sales.SalesReturn,['status']).filter(status__in=['received','closed']).values('pk')
    returns=list(reader.source(sales.SalesReturnLine,['original_delivery_line','quantity','unit','reopen_order_demand','receipt_line','return_order']).filter(original_delivery_line_id__in=[row.pk for row in delivered],return_order_id__in=return_heads,receipt_line_id__in=receipt_rows))
    delivery_map={row.pk:row.order_line_id for row in delivered};allocation_map={row.pk:row.order_line_id for row in allocations}
    result=[]
    for line in lines:
        unit=reader.unit(line.ordered_unit_id)
        actual=reader.total([row for row in delivered if row.order_line_id==line.pk],'quantity','unit',unit)
        returned=[row for row in returns if delivery_map[row.original_delivery_line_id]==line.pk]
        reopened=reader.total([row for row in returned if row.reopen_order_demand],'quantity','unit',unit)
        result.append({'number':headmap[line.order_id].number,'line_number':line.line_number,'material':line.material_id,'unit':unit.name,
            'ordered':str(line.ordered_quantity),'allocated':str(sum((row.unit.convert_quantity(row.allocated_quantity-row.released_unfulfilled_quantity,unit) for row in allocations if row.order_line_id==line.pk and row.original_allocation_id is None),Decimal('0'))),
            'rework_allocated':str(reader.total([row for row in allocations if row.order_line_id==line.pk and row.original_allocation_id is not None],'allocated_quantity','unit',unit)),
            'packed':str(reader.total([row for row in packed if allocation_map[row.work_card_allocation_id]==line.pk],'quantity','unit',unit)),
            'delivered':str(actual),'returned':str(reader.total(returned,'quantity','unit',unit)),'reopened':str(reopened),
            'remaining':str(line.ordered_quantity+reopened-actual)})
    return count,result


def production_progress(reader,filters):
    count,cards=page(reader.source(production.WorkCard,['number','document_at','status']),filters,'document_at','status')
    operations=list(reader.source(production.WorkCardOperation,['work_card','process','is_skipped']).filter(work_card_id__in=[row.pk for row in cards]))
    executions=list(reader.source(production.OperationExecution,['operation','execution_number','machine','status','started_at','ended_at','output_mass_kg']).filter(operation_id__in=[row.pk for row in operations]).exclude(status='cancelled').order_by('execution_number','pk'))
    corrections=list(reader.source(production.ExecutionCorrection,['execution','changes_mass','new_output_mass_kg','changes_start_time','new_started_at','changes_end_time','new_ended_at']).filter(execution_id__in=[row.pk for row in executions]).order_by('pk'))
    cardmap={row.pk:row for row in cards};latest={row.operation_id:row for row in executions};result=[]
    for operation in operations:
        card=cardmap[operation.work_card_id];actual=latest.get(operation.pk)
        values={'number':card.number,'status':card.status,'process':operation.process_id,'skipped':operation.is_skipped,
            'round':None,'machine':None,'execution_status':None,'started_at':None,'ended_at':None,'mass_kg':None}
        if actual is not None:
            values.update(round=actual.execution_number,machine=actual.machine_id,execution_status=actual.status,started_at=actual.started_at,ended_at=actual.ended_at,mass_kg=actual.output_mass_kg)
            for correction in corrections:
                if correction.execution_id!=actual.pk:continue
                if correction.changes_mass:values['mass_kg']=correction.new_output_mass_kg
                if correction.changes_start_time:values['started_at']=correction.new_started_at
                if correction.changes_end_time:values['ended_at']=correction.new_ended_at
            if values['mass_kg'] is not None:values['mass_kg']=str(values['mass_kg'])
        result.append(values)
    return count,result


def materials(reader,filters):
    count,orders=page(reader.source(production.WeighingOrder,['number','document_at','status']),filters,'document_at','status')
    ordermap={row.pk:row for row in orders}
    stages=list(reader.source(production.WeighingStage,['order']).filter(order_id__in=ordermap))
    stagemap={row.pk:row.order_id for row in stages}
    lines=list(reader.source(production.WeighingLine,['stage','sequence','material','planned_quantity','unit']).filter(stage_id__in=stagemap))
    measured=list(reader.source(production.WeighingRecord,['line','is_void','quantity','unit']).filter(line_id__in=[row.pk for row in lines],is_void=False))
    issue_ids=reader.source(warehouse.StockIssue,['status']).filter(status='posted').values('pk')
    issues=list(reader.source(warehouse.StockIssueLine,['issue','weighing_line','quantity','unit']).filter(weighing_line_id__in=[row.pk for row in lines],issue_id__in=issue_ids))
    receipt_ids=reader.source(warehouse.StockReceipt,['status']).filter(status='posted').values('pk')
    returns=list(reader.source(warehouse.StockReceiptLine,['receipt','original_issue_line','quantity','unit']).filter(original_issue_line_id__in=[row.pk for row in issues],receipt_id__in=receipt_ids))
    issue_map={row.pk:row.weighing_line_id for row in issues};result=[]
    for line in lines:
        unit=reader.unit(line.unit_id);issued=reader.total([row for row in issues if row.weighing_line_id==line.pk],'quantity','unit',unit)
        returned=reader.total([row for row in returns if issue_map[row.original_issue_line_id]==line.pk],'quantity','unit',unit)
        result.append({'order':ordermap[stagemap[line.stage_id]].number,'sequence':line.sequence,'material':line.material_id,'unit':unit.name,
            'planned':str(line.planned_quantity),'measured':str(reader.total([row for row in measured if row.line_id==line.pk],'quantity','unit',unit)),
            'issued':str(issued),'returned':str(returned),'net_issued':str(issued-returned),'difference':str(issued-returned-line.planned_quantity)})
    return count,result


def quality(reader,filters):
    count,inspections=page(reader.source(q.QualityInspection,['number','kind','work_card','result','is_void','inspected_at','inspected_quantity','quantity_unit']),filters,'inspected_at','result')
    dispositions=list(reader.source(q.QualityDisposition,['inspection','kind','quantity','unit','status']).filter(inspection_id__in=[row.pk for row in inspections]))
    result=[]
    for inspection in inspections:
        entries=[row for row in dispositions if row.inspection_id==inspection.pk]
        for entry in entries or [None]:
            result.append({'number':inspection.number,'kind':inspection.kind,'work_card':inspection.work_card_id,'result':inspection.result,
                'void':inspection.is_void,'inspected_at':inspection.inspected_at,'scope':None if inspection.inspected_quantity is None else str(inspection.inspected_quantity),
                'scope_unit':None if inspection.quantity_unit_id is None else reader.unit(inspection.quantity_unit_id).name,
                'disposition':None if entry is None else entry.kind,'quantity':None if entry is None else str(entry.quantity),
                'unit':None if entry is None else reader.unit(entry.unit_id).name,'adoption':None if entry is None else entry.status})
    return count,result


def stock(reader,filters):
    count,balances=page(reader.source(warehouse.StockBalance,['lot','location','quality_state','package','quantity']),filters)
    lots={row.pk:row for row in reader.source(warehouse.InventoryLot,['code','material','owner']).filter(pk__in=[row.lot_id for row in balances])}
    materials={row.pk:row for row in reader.source(base.Material,['stock_unit']).filter(pk__in=[row.material_id for row in lots.values()])}
    if set(lots)!={row.lot_id for row in balances} or set(materials)!={row.material_id for row in lots.values()}:raise PermissionDenied('库存批次或物料来源超出当前查询范围。')
    return count,[{'lot':lots[row.lot_id].code,'material':lots[row.lot_id].material_id,'owner':lots[row.lot_id].owner_id,
        'location':row.location_id,'quality':row.quality_state,'package':row.package_id,'quantity':str(row.quantity),
        'unit':reader.unit(materials[lots[row.lot_id].material_id].stock_unit_id).name} for row in balances]


def packages(reader,filters):
    query=reader.source(warehouse.Package,['code','barcode','work_card','source_execution','status','packed_at','net_mass_kg','piece_quantity','lot'])
    if 'barcode' in filters:query=query.filter(barcode=filters['barcode'])
    count,items=page(query,filters,'packed_at','status');ids=[row.pk for row in items]
    lots={row.pk:row for row in reader.source(warehouse.InventoryLot,['material']).filter(pk__in=[row.lot_id for row in items])}
    materials={row.pk:row for row in reader.source(base.Material,['stock_unit']).filter(pk__in=[row.material_id for row in lots.values()])}
    if set(lots)!={row.lot_id for row in items} or set(materials)!={row.material_id for row in lots.values()}:raise PermissionDenied('包装物料来源超出当前查询范围。')
    receipt_ids=reader.source(warehouse.StockReceipt,['status','kind']).filter(status='posted')
    receipts=list(reader.source(warehouse.StockReceiptLine,['receipt','package','quantity','unit']).filter(package_id__in=ids,receipt_id__in=receipt_ids.filter(kind='finished_output').values('pk')))
    returns=list(reader.source(warehouse.StockReceiptLine,['receipt','package','quantity','unit']).filter(package_id__in=ids,receipt_id__in=receipt_ids.filter(kind='sales_return').values('pk')))
    issue_ids=reader.source(warehouse.StockIssue,['status','kind']).filter(status='posted',kind='delivery').values('pk')
    issues=list(reader.source(warehouse.StockIssueLine,['issue','package','quantity','unit']).filter(package_id__in=ids,issue_id__in=issue_ids))
    result=[]
    for item in items:
        unit=reader.unit(materials[lots[item.lot_id].material_id].stock_unit_id)
        result.append({'code':item.code,'barcode':item.barcode,'work_card':item.work_card_id,'source_execution':item.source_execution_id,
            'status':item.status,'packed_at':item.packed_at,'net_mass_kg':None if item.net_mass_kg is None else str(item.net_mass_kg),
            'pieces':None if item.piece_quantity is None else str(item.piece_quantity),'unit':unit.name,
            'received':str(reader.total([row for row in receipts if row.package_id==item.pk],'quantity','unit',unit)),
            'issued':str(reader.total([row for row in issues if row.package_id==item.pk],'quantity','unit',unit)),
            'returned':str(reader.total([row for row in returns if row.package_id==item.pk],'quantity','unit',unit))})
    return count,result


FUNCTIONS={'orders':orders,'production':production_progress,'materials':materials,'quality':quality,'stock':stock,'packages':packages}


from .report_queries import EXTRA_REPORTS,EXTRA_FUNCTIONS
REPORTS.update(EXTRA_REPORTS);FUNCTIONS.update(EXTRA_FUNCTIONS)
from .source_inventory_queries import definitions
SOURCE_REPORTS,SOURCE_FUNCTIONS=definitions()
REPORTS.update(SOURCE_REPORTS);FUNCTIONS.update(SOURCE_FUNCTIONS)

LABELS={
 'orders':{'material':(base.Material,'name')},
 'production':{'process':(base.Process,'name'),'machine':(base.Machine,'number')},
 'materials':{'material':(base.Material,'name')},
 'quality':{'work_card':(production.WorkCard,'number')},
 'stock':{'material':(base.Material,'name'),'owner':(base.Party,'name'),'location':(base.StorageLocation,'name'),'package':(warehouse.Package,'code')},
 'packages':{'work_card':(production.WorkCard,'number')},
}
ENUMS={
 'orders':{},'production':{'status':(production.WorkCard,'status'),'execution_status':(production.OperationExecution,'status')},
 'materials':{},'quality':{'kind':(q.QualityInspection,'kind'),'result':(q.QualityInspection,'result'),'disposition':(q.QualityDisposition,'kind'),'adoption':(q.QualityDisposition,'status')},
 'stock':{'quality':(warehouse.StockBalance,'quality_state')},'packages':{'status':(warehouse.Package,'status')},
}
for spec in REPORTS.values():
    spec['columns']=[(key,title.removesuffix('ID')) for key,title in spec['columns']]

def display_rows(reader,report,rows):
    if report not in LABELS:return rows
    for key,(model,field) in LABELS[report].items():
        labels=reader.labels(model,field,[row[key] for row in rows])
        for row in rows:
            if row[key] is not None:row[key]=labels[row[key]]
    for key,(model,field) in ENUMS[report].items():
        labels=dict(model._meta.get_field(field).choices)
        for row in rows:
            if row[key] is not None:row[key]=labels[row[key]]
    return rows


class BusinessReport(APIView):
    permission_classes=[ApiPermission]
    def get(self,request,report):
        spec=REPORTS[report]
        parameters=ReportInput(data=request.query_params);parameters.is_valid(raise_exception=True)
        reader=Reader(request)
        if spec.get('uses_units',True):reader.load_units()
        count,rows=FUNCTIONS[report](reader,parameters.validated_data);rows=display_rows(reader,report,rows)
        return success({'title':spec['title'],'columns':[{'key':key,'title':title} for key,title in spec['columns']],'count':count,'rows':rows})


class BusinessReportExport(BusinessReport):
    def get(self,request,report):
        spec=REPORTS[report];parameters=ReportInput(data=request.query_params);parameters.is_valid(raise_exception=True)
        reader=Reader(request)
        if spec.get('uses_units',True):reader.load_units()
        data=parameters.validated_data;data['page_size']=200;data['page']=1
        output=io.StringIO(newline='');writer=csv.writer(output);writer.writerow([title for key,title in spec['columns']])
        while True:
            count,rows=FUNCTIONS[report](reader,data);rows=display_rows(reader,report,rows)
            for row in rows:writer.writerow([row[key] for key,title in spec['columns']])
            if data['page']*data['page_size']>=count:break
            data['page']+=1
        response=HttpResponse('\ufeff'+output.getvalue(),content_type='text/csv; charset=utf-8')
        response['Content-Disposition']='attachment; filename="erp_'+report+'.csv"'
        return response
