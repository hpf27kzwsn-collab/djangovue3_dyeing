"""明确检验数量和处置；检验判定本身不改变库存。"""
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction
from plugins.erp_base.business import locked, persist, record, snapshot, require_state, require_rows
from plugins.erp_warehouse import models as warehouse
from plugins.erp_production import models as m
from . import models as q
from plugins.erp_production.execution_services import effective
from plugins.erp_production.services import converted_sum


def validate_scope(item):
    item.full_clean()
    if item.is_void:raise ValidationError({'inspection':'已取消采用的检验不能用于新判定、处置或放行。'})
    if item.inspected_quantity is None or item.inspected_quantity <= 0 or item.quantity_unit_id is None:
        raise ValidationError({'inspected_quantity':'新检验必须明确实际覆盖数量和单位。'})
    if item.kind=='incoming':
        source=warehouse.StockReceiptLine.objects.get(pk=item.receipt_line_id)
        receipt=warehouse.StockReceipt.objects.get(pk=source.receipt_id)
        require_state(receipt,['posted'])
        if item.inspected_at < receipt.posted_at:raise ValidationError({'inspected_at':'检验不能早于实际收货生效时间。'})
        maximum=source.unit.convert_quantity(source.quantity,item.quantity_unit)
    elif item.package_id is not None:
        package=warehouse.Package.objects.get(pk=item.package_id)
        require_state(package,['packed','received','issued','returned'])
        from plugins.erp_base.models import Unit
        maximum=Unit.objects.get(code='kg').convert_quantity(package.net_mass_kg,item.quantity_unit)
    elif item.execution_id is not None:
        item.execution=m.OperationExecution.objects.get(pk=item.execution_id)
        require_state(item.execution,['completed'])
        if item.kind in ['final','reinspection']:
            from plugins.erp_warehouse.packing_services import final_source
            if item.execution.operation_id!=final_source(item.work_card).pk:
                raise ValidationError({'execution':'终检或复检须对应当前路线包装前最后实际产出。'})
        actual=effective(item.execution)
        from django.utils.dateparse import parse_datetime
        if item.inspected_at < parse_datetime(actual['ended_at']):raise ValidationError({'inspected_at':'检验不能早于来源执行的实际完工。'})
        if item.quantity_unit.dimension=='mass' and actual['output_mass_kg'] is not None:
            from plugins.erp_base.models import Unit
            maximum=Unit.objects.get(code='kg').convert_quantity(Decimal(actual['output_mass_kg']),item.quantity_unit)
        elif actual['output_quantity'] is not None and item.execution.output_unit_id is not None:
            maximum=item.execution.output_unit.convert_quantity(Decimal(actual['output_quantity']),item.quantity_unit)
        else:raise ValidationError({'execution':'所选执行没有对应计量维度的实际产出。'})
    else:raise ValidationError({'execution':'新生产检验必须明确实际执行或包装范围，不能仅按工卡整体放行。'})
    if item.inspected_quantity > maximum:
        raise ValidationError({'inspected_quantity':'检验范围量超过所选来源实际数量。'})
    if item.previous_inspection_id is not None:
        source=item.previous_inspection
        allowed_cards=[item.work_card_id,item.work_card.original_work_card_id] if item.work_card_id is not None else [None]
        if source.work_card_id not in allowed_cards or source.lot_id!=item.lot_id:
            raise ValidationError({'previous_inspection':'复检必须对应原工卡或原批次。'})


@transaction.atomic
def judge(item,actor,result,employee):
    if item.kind=='incoming':
        locked(item.receipt_line.receipt)
    else:locked(item.work_card)
    item=locked(item);require_state(item,['pending'],'result')
    validate_scope(item)
    require_rows(q.InspectionResultLine.objects.filter(inspection=item))
    if q.InspectionResultLine.objects.filter(inspection=item,result='pending').exists():
        raise ValidationError({'lines':'请先完成全部实际检验项目判定。'})
    if result=='pass' and q.InspectionResultLine.objects.filter(inspection=item,result='fail').exists():
        raise ValidationError({'result':'有不合格项目不能判为全部合格；让步通过单独处置记录。'})
    before=snapshot(item);item.result,item.inspector=result,employee
    persist(item,actor);record(item,'judge',before,actor)
    if item.kind=='reinspection':
        for order in m.ReworkOrder.objects.select_for_update().filter(rework_work_card=item.work_card,status__in=['released','running']):
            previous=snapshot(order);order.status='reinspected';persist(order,actor);record(order,'reinspect',previous,actor)
    return item


@transaction.atomic
def dispose(item,actor,kind,quantity,unit,reason,employee,at,supersedes=None):
    if item.kind=='incoming':locked(item.receipt_line.receipt)
    elif item.execution_id is not None:locked(item.execution.operation.work_card)
    item=locked(item);require_state(item,['pass','fail'],'result');validate_scope(item)
    if at < item.inspected_at:raise ValidationError({'at':'处置时间不能早于检验。'})
    if kind=='release' and item.result!='pass':
        raise ValidationError({'kind':'不合格不能普通放行；按真实情况采用让步、降级或返修处置。'})
    if supersedes is not None:
        previous=locked(supersedes);require_state(previous,['active'])
        if previous.inspection_id!=item.pk:raise ValidationError({'supersedes':'被替换处置必须属于本检验。'})
        if warehouse.StockAdjustmentLine.objects.filter(disposition=previous,adjustment__status='posted').exists():
            raise ValidationError({'supersedes':'原处置已经调整库存，请先冲销。'})
        if m.ReworkOrder.objects.filter(disposition=previous).exclude(status='cancelled').exists():
            raise ValidationError({'supersedes':'原处置已有有效返修任务。'})
        if warehouse.PackageDispositionAllocation.objects.filter(disposition=previous).exclude(package__status__in=['draft','void']).exists():raise ValidationError({'supersedes':'原处置已经用于实际包装，请先处理原包装。'})
        before=snapshot(previous);previous.status='replaced';persist(previous,actor);record(previous,'replace',before,actor,reason)
    used=converted_sum(q.QualityDisposition.objects.filter(inspection=item,status='active'),'quantity','unit',item.quantity_unit)
    if used+unit.convert_quantity(quantity,item.quantity_unit)>item.inspected_quantity:
        raise ValidationError({'quantity':'有效处置合计不能超过本次明确检验量。'})
    disposition=persist(q.QualityDisposition(inspection=item,kind=kind,quantity=quantity,unit=unit,reason=reason,
        approved_by=employee,approved_at=at,supersedes=supersedes,dept_belong_id=item.dept_belong_id),actor)
    record(disposition,'dispose',{'exists':False},actor,reason)
    record(item,'dispose',snapshot(item),actor,reason)
    return item


@transaction.atomic
def void(item,actor,reason,at):
    if item.kind=='incoming':locked(item.receipt_line.receipt)
    else:locked(item.work_card)
    item=locked(item)
    if item.is_void:raise ValidationError({'inspection':'此检验已取消采用。'})
    if at < item.inspected_at:raise ValidationError({'at':'取消采用不能早于检验时间。'})
    dispositions=list(q.QualityDisposition.objects.select_for_update().filter(inspection=item,status='active').order_by('pk'))
    if warehouse.PackageDispositionAllocation.objects.filter(disposition__in=dispositions).exclude(package__status__in=['draft','void']).exists():raise ValidationError({'inspection':'检验放行仍被实际包装采用，请先处理原包装。'})
    if warehouse.StockAdjustmentLine.objects.filter(disposition__in=dispositions,adjustment__status__in=['confirmed','posted']).exists() or m.ReworkOrder.objects.filter(disposition__in=dispositions).exclude(status='cancelled').exists():
        raise ValidationError({'inspection':'有效库存处置或返修仍引用此检验，请先处理对应业务。'})
    for disposition in dispositions:
        before=snapshot(disposition);disposition.status='cancelled';persist(disposition,actor);record(disposition,'void',before,actor,reason)
    before=snapshot(item);item.is_void,item.voided_at,item.void_reason=True,at,reason;persist(item,actor);record(item,'void',before,actor,reason)
    return item


@transaction.atomic
def close_rework(item,actor,inspection,reason):
    card=locked(item.rework_work_card);require_state(card,['completed','closed'])
    item=locked(item);require_state(item,['reinspected'])
    inspection=locked(inspection)
    if inspection.work_card_id!=item.rework_work_card_id or inspection.kind!='reinspection' or inspection.result!='pass' or inspection.is_void:
        raise ValidationError({'inspection':'返修结案必须对应本返修工卡的有效合格复检。'})
    if not q.QualityDisposition.objects.filter(inspection=inspection,status='active',kind__in=['release','concession','downgrade']).exists():
        raise ValidationError({'inspection':'合格复检还需明确实际放行处置。'})
    before=snapshot(item);item.status='closed';persist(item,actor);record(item,'close',before,actor,reason)
    return item


@transaction.atomic
def release_rework(item,actor,number,route_version,at,allocations=None):
    original=locked(item.original_work_card);item=locked(item);require_state(item,['draft'])
    source=locked(item.disposition);require_state(source,['active'])
    if at<source.approved_at:raise ValidationError({'at':'返修下达不能早于实际返修处置。'})
    if source.kind!='rework' or source.inspection.work_card_id!=original.pk:
        raise ValidationError({'disposition':'返修任务必须来自原工卡的实际返修处置。'})
    prior=converted_sum(m.ReworkOrder.objects.filter(disposition=source).exclude(status__in=['draft','cancelled']), 'quantity','unit',source.unit)
    if prior+item.unit.convert_quantity(item.quantity,source.unit)>source.quantity:
        raise ValidationError({'quantity':'下达返修合计不能超过处置量。'})
    require_state(route_version,['active'])
    card=persist(m.WorkCard(number=number,document_at=at,factory=original.factory,business_unit=original.business_unit,
        material=original.material,specification_snapshot=original.specification_snapshot,color_standard=original.color_standard,
        color_number_snapshot=original.color_number_snapshot,route_version=route_version,planned_quantity=item.quantity,
        quantity_unit=item.unit,original_work_card=original,manual_creation_reason=item.reason,dept_belong_id=original.dept_belong_id),actor)
    from plugins.erp_base.models import RouteStep
    from plugins.erp_production.services import prepare, release
    old_allocations=list(m.WorkCardOrderAllocation.objects.filter(work_card=original))
    if old_allocations:
        if not allocations:raise ValidationError({'allocations':'订单返修须明确承接原工卡各订单的实际数量。'})
        if len({row['original'].pk for row in allocations})!=len(allocations):raise ValidationError({'allocations':'同一原需求只填写一次。'})
        if sum((row['unit'].convert_quantity(row['quantity'],item.unit) for row in allocations),Decimal('0'))!=item.quantity:raise ValidationError({'allocations':'承接订单分配合计必须等于本次返修量。'})
        from plugins.erp_production.services import check_order_allocation
        for row in allocations:
            if row['original'].work_card_id!=original.pk:raise ValidationError({'allocations':'承接来源必须属于原工卡。'})
            root=row['original'] if row['original'].original_allocation_id is None else row['original'].original_allocation
            allocation=m.WorkCardOrderAllocation(work_card=card,order_line=root.order_line,original_allocation=root,
                allocated_quantity=row['quantity'],unit=row['unit'],dept_belong_id=card.dept_belong_id)
            check_order_allocation(allocation);persist(allocation,actor)
    elif allocations:raise ValidationError({'allocations':'无订单原工卡不建立虚构订单承接。'})
    prepare(card,actor,list(RouteStep.objects.filter(route_version=route_version,is_required=True)))
    release(card,actor,at=at)
    before=snapshot(item);item.rework_work_card,item.status=card,'released';persist(item,actor);record(item,'release',before,actor,item.reason)
    return item


@transaction.atomic
def close_defect(item,actor,handling):
    locked(item.work_card);item=locked(item);require_state(item,['open','handling'])
    if item.disposition_id is None:raise ValidationError({'disposition':'关闭质量异常必须引用实际处置。'})
    if item.disposition.inspection.work_card_id!=item.work_card_id:raise ValidationError({'disposition':'处置来源工卡不一致。'})
    before=snapshot(item);item.status='closed';persist(item,actor);record(item,'close',before,actor,handling)
    return item
