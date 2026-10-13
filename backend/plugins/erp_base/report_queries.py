from plugins.erp_quality import models as q
"""价格、打样、采购、排程、返修与批次谱系的只读查询。"""
from decimal import Decimal
from plugins.erp_sales import models as sales
from plugins.erp_sampling import models as sampling
from plugins.erp_purchase import models as purchase
from plugins.erp_production import models as production
from plugins.erp_warehouse import models as warehouse
from . import models as base


EXTRA_REPORTS={
 'prices':{'title':'价格版本与有效期','columns':[('number','价格资料号'),('customer','客户'),('material','物料'),('version','版本'),('price','合同单价'),('unit','计价单位'),('confirmed','已确认'),('start','生效时间'),('end','失效时间')]},
 'sampling':{'title':'打样轮次与最新确认','columns':[('number','打样任务'),('line','行号'),('customer','客户'),('material','物料'),('color','色号'),('status','明细状态'),('round','最新轮次'),('trial_status','试验状态'),('started','实际开工'),('ended','实际完成'),('sent','本轮送版时间'),('reply','本轮客户回复'),('confirmed','本轮回复时间')]},
 'purchases':{'title':'采购到货与净收货','columns':[('number','采购订单'),('supplier','供应商'),('status','订单状态'),('line','行号'),('material','物料'),('planned','采购数量'),('received','有效收货'),('returned','实际退货'),('net','净收货'),('remaining','剩余需求'),('unit','单位')]},
 'schedules':{'title':'排程版本与机台实际占用','columns':[('card','工卡号'),('process','工序'),('machine','机台'),('version','安排版本'),('status','安排状态'),('planned_start','计划开始'),('planned_end','计划结束'),('round','实际轮次'),('started','实际开工'),('ended','实际完工'),('mass','有效实际kg')]},
 'rework':{'title':'返修来源与复检进度','columns':[('number','返修号'),('original','原工卡'),('card','返修工卡'),('quantity','返修量'),('unit','单位'),('status','返修状态'),('reason','实际原因'),('inspection','复检单'),('result','复检结果')]},
 'lineage':{'title':'实际投入产出批次追溯','columns':[('number','转换号'),('card','工卡'),('occurred','转换时间'),('confirmed','已确认'),('void','取消采用'),('direction','投入或产出'),('lot','批次'),('material','物料'),('quantity','实际数量'),('unit','单位'),('document','实际收发单')]},
}


def choices(model,field,value):return None if value is None else dict(model._meta.get_field(field).choices)[value]


def prices(reader,filters):
    from .reports import page
    count,heads=page(reader.source(sales.CommercialPrice,['number','customer','document_at','status']),filters,'document_at','status')
    h={row.pk:row for row in heads};customers=reader.labels(base.Party,'name',[row.customer_id for row in heads])
    lines=list(reader.source(sales.CommercialPriceLine,['price_document','material','version','unit_price','unit','is_confirmed','valid_from','valid_to']).filter(price_document_id__in=h))
    materials=reader.labels(base.Material,'name',[row.material_id for row in lines])
    return count,[{'number':h[row.price_document_id].number,'customer':customers[h[row.price_document_id].customer_id],'material':materials[row.material_id],
        'version':row.version,'price':str(row.unit_price),'unit':reader.unit(row.unit_id).name,'confirmed':row.is_confirmed,'start':row.valid_from,'end':row.valid_to} for row in lines]


def samples(reader,filters):
    from .reports import page
    count,heads=page(reader.source(sampling.SampleRequest,['number','customer','document_at','status']),filters,'document_at','status')
    h={row.pk:row for row in heads};customers=reader.labels(base.Party,'name',[row.customer_id for row in heads])
    lines=list(reader.source(sampling.SampleLine,['request','line_number','material','color_number','status']).filter(request_id__in=h))
    materials=reader.labels(base.Material,'name',[row.material_id for row in lines])
    trials=list(reader.source(sampling.SampleTrial,['sample_line','trial_number','status','started_at','finished_at']).filter(sample_line_id__in=[row.pk for row in lines]).order_by('trial_number','pk'))
    latest={row.sample_line_id:row for row in trials}
    replies=list(reader.source(sampling.SampleConfirmation,['trial','sent_at','confirmed_at','result']).filter(trial_id__in=[row.pk for row in latest.values()]).order_by('pk'))
    latest_replies={row.trial_id:row for row in replies}
    result=[]
    for row in lines:
        trial=latest.get(row.pk)
        reply=None if trial is None else latest_replies.get(trial.pk)
        result.append({'number':h[row.request_id].number,'line':row.line_number,'customer':customers[h[row.request_id].customer_id],'material':materials[row.material_id],'color':row.color_number,
            'status':choices(sampling.SampleLine,'status',row.status),'round':None if trial is None else trial.trial_number,'trial_status':None if trial is None else choices(sampling.SampleTrial,'status',trial.status),
            'started':None if trial is None else trial.started_at,'ended':None if trial is None else trial.finished_at,
            'sent':None if reply is None else reply.sent_at,'reply':None if reply is None else choices(sampling.SampleConfirmation,'result',reply.result),'confirmed':None if reply is None else reply.confirmed_at})
    return count,result


def purchases(reader,filters):
    from .reports import page
    count,heads=page(reader.source(purchase.PurchaseOrder,['number','supplier','status','document_at']),filters,'document_at','status')
    h={row.pk:row for row in heads};parties=reader.labels(base.Party,'name',[row.supplier_id for row in heads])
    lines=list(reader.source(purchase.PurchaseOrderLine,['order','line_number','material','quantity','unit']).filter(order_id__in=h));ids=[row.pk for row in lines]
    materials=reader.labels(base.Material,'name',[row.material_id for row in lines])
    receipt_ids=reader.source(warehouse.StockReceipt,['status']).filter(status='posted').values('pk')
    receipts=list(reader.source(warehouse.StockReceiptLine,['receipt','purchase_order_line','quantity','unit']).filter(receipt_id__in=receipt_ids,purchase_order_line_id__in=ids))
    issue_ids=reader.source(warehouse.StockIssue,['status','kind']).filter(status='posted',kind='purchase_return').values('pk')
    returns=list(reader.source(warehouse.StockIssueLine,['issue','original_receipt_line','quantity','unit']).filter(issue_id__in=issue_ids,original_receipt_line_id__in=[row.pk for row in receipts]))
    origins={row.pk:row.purchase_order_line_id for row in receipts};result=[]
    for row in lines:
        unit=reader.unit(row.unit_id);received=reader.total([x for x in receipts if x.purchase_order_line_id==row.pk],'quantity','unit',unit)
        returned=reader.total([x for x in returns if origins[x.original_receipt_line_id]==row.pk],'quantity','unit',unit)
        result.append({'number':h[row.order_id].number,'supplier':parties[h[row.order_id].supplier_id],'status':choices(purchase.PurchaseOrder,'status',h[row.order_id].status),'line':row.line_number,'material':materials[row.material_id],
            'planned':str(row.quantity),'received':str(received),'returned':str(returned),'net':str(received-returned),'remaining':str(row.quantity-received+returned),'unit':unit.name})
    return count,result


def schedules(reader,filters):
    from .reports import page
    count,slots=page(reader.source(production.ScheduleAssignment,['operation','machine','version','status','planned_start','planned_end']),filters,'planned_start','status')
    operations={row.pk:row for row in reader.source(production.WorkCardOperation,['work_card','process']).filter(pk__in=[row.operation_id for row in slots])}
    # 阅读每项关联同样必须有来源查询及数据范围。
    from rest_framework.exceptions import PermissionDenied
    if set(operations)!={row.operation_id for row in slots}:raise PermissionDenied('排程节点超出当前查询范围。')
    cards=reader.labels(production.WorkCard,'number',[row.work_card_id for row in operations.values()]);processes=reader.labels(base.Process,'name',[row.process_id for row in operations.values()]);machines=reader.labels(base.Machine,'number',[row.machine_id for row in slots])
    executions=list(reader.source(production.OperationExecution,['operation','machine','execution_number','started_at','ended_at','output_mass_kg','status']).filter(operation_id__in=operations).exclude(status='cancelled').order_by('execution_number','pk'))
    changes=list(reader.source(production.ExecutionCorrection,['execution','changes_mass','new_output_mass_kg','changes_start_time','new_started_at','changes_end_time','new_ended_at']).filter(execution_id__in=[row.pk for row in executions]).order_by('pk'))
    result=[]
    for row in slots:
        op=operations[row.operation_id];actuals=[x for x in executions if x.operation_id==op.pk and x.machine_id==row.machine_id]
        for execution in actuals or [None]:
            actual={'started':None,'ended':None,'mass':None,'round':None}
            if execution is not None:
                actual.update(started=execution.started_at,ended=execution.ended_at,mass=execution.output_mass_kg,round=execution.execution_number)
                for change in changes:
                    if change.execution_id!=execution.pk:continue
                    if change.changes_mass:actual['mass']=change.new_output_mass_kg
                    if change.changes_start_time:actual['started']=change.new_started_at
                    if change.changes_end_time:actual['ended']=change.new_ended_at
                if actual['mass'] is not None:actual['mass']=str(actual['mass'])
            result.append({'card':cards[op.work_card_id],'process':processes[op.process_id],'machine':machines[row.machine_id],'version':row.version,'status':choices(production.ScheduleAssignment,'status',row.status),'planned_start':row.planned_start,'planned_end':row.planned_end,**actual})
    return count,result


def rework(reader,filters):
    from .reports import page
    count,items=page(reader.source(production.ReworkOrder,['number','original_work_card','rework_work_card','quantity','unit','status','reason','create_datetime']),filters,'create_datetime','status')
    cards=reader.labels(production.WorkCard,'number',[key for row in items for key in [row.original_work_card_id,row.rework_work_card_id]])
    inspections=list(reader.source(q.QualityInspection,['number','work_card','kind','result','is_void','inspected_at']).filter(work_card_id__in=[row.rework_work_card_id for row in items],kind='reinspection',is_void=False).order_by('inspected_at','pk'))
    latest={row.work_card_id:row for row in inspections};result=[]
    for row in items:
        inspection=latest.get(row.rework_work_card_id)
        result.append({'number':row.number,'original':cards[row.original_work_card_id],'card':None if row.rework_work_card_id is None else cards[row.rework_work_card_id],'quantity':str(row.quantity),'unit':reader.unit(row.unit_id).name,'status':choices(production.ReworkOrder,'status',row.status),'reason':row.reason,
            'inspection':None if inspection is None else inspection.number,'result':None if inspection is None else choices(q.QualityInspection,'result',inspection.result)})
    return count,result


def lineage(reader,filters):
    from .reports import page
    count,items=page(reader.source(warehouse.LotTransformation,['number','work_card','occurred_at','is_confirmed','is_void']),filters,'occurred_at')
    h={row.pk:row for row in items};cards=reader.labels(production.WorkCard,'number',[row.work_card_id for row in items])
    lines=list(reader.source(warehouse.LotTransformationLine,['transformation','direction','lot','quantity','unit','receipt_line','issue_line']).filter(transformation_id__in=h))
    lots={row.pk:row for row in reader.source(warehouse.InventoryLot,['code','material']).filter(pk__in=[row.lot_id for row in lines])}
    from rest_framework.exceptions import PermissionDenied
    if set(lots)!={row.lot_id for row in lines}:raise PermissionDenied('谱系批次超出当前查询范围。')
    materials=reader.labels(base.Material,'name',[row.material_id for row in lots.values()])
    receipts={row.pk:row.receipt_id for row in reader.source(warehouse.StockReceiptLine,['receipt']).filter(pk__in=[row.receipt_line_id for row in lines])};issues={row.pk:row.issue_id for row in reader.source(warehouse.StockIssueLine,['issue']).filter(pk__in=[row.issue_line_id for row in lines])}
    if set(receipts)!={row.receipt_line_id for row in lines if row.receipt_line_id is not None} or set(issues)!={row.issue_line_id for row in lines if row.issue_line_id is not None}:raise PermissionDenied('谱系收发来源超出当前查询范围。')
    receipt_numbers=reader.labels(warehouse.StockReceipt,'number',receipts.values());issue_numbers=reader.labels(warehouse.StockIssue,'number',issues.values())
    return count,[{'number':h[row.transformation_id].number,'card':None if h[row.transformation_id].work_card_id is None else cards[h[row.transformation_id].work_card_id],'occurred':h[row.transformation_id].occurred_at,'confirmed':h[row.transformation_id].is_confirmed,'void':h[row.transformation_id].is_void,
        'direction':choices(warehouse.LotTransformationLine,'direction',row.direction),'lot':lots[row.lot_id].code,'material':materials[lots[row.lot_id].material_id],'quantity':str(row.quantity),'unit':reader.unit(row.unit_id).name,
        'document':receipt_numbers[receipts[row.receipt_line_id]] if row.direction=='output' else issue_numbers[issues[row.issue_line_id]]} for row in lines]


EXTRA_FUNCTIONS={'prices':prices,'sampling':samples,'purchases':purchases,'schedules':schedules,'rework':rework,'lineage':lineage}
