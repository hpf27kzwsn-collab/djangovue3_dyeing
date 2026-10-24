"""计划料单、实际称量与净领用分别保存。"""
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction
from plugins.erp_base.business import locked, persist, record, snapshot, require_state, require_rows
from plugins.erp_warehouse import models as warehouse
from . import models as m
from .services import converted_sum


@transaction.atomic
def create_order(item,actor,number,at,kind,reason):
    batch=locked(item.batch);item=locked(item);require_state(item,['active'])
    require_state(batch,['planned','scheduled','running'])
    if kind=='normal' and m.WeighingOrder.objects.filter(production_recipe=item,kind='normal').exclude(status='cancelled').exists():
        raise ValidationError({'kind':'本采用已有正常料单，不能重复生成计划需求。'})
    if kind!='normal' and not reason.strip():raise ValidationError({'reason':'加料、后处理或洗缸须填写实际依据。'})
    if at < item.adopted_at:raise ValidationError({'at':'料单不能早于配方采用时间。'})
    order=persist(m.WeighingOrder(number=number,document_at=at,batch=batch,production_recipe=item,kind=kind,reason=reason,dept_belong_id=item.dept_belong_id),actor)
    for source in require_rows(m.MaterialPlanStage.objects.filter(production_recipe=item)):
        stage=persist(m.WeighingStage(order=order,sequence=source.sequence,plan_stage=source,
            phase_name_snapshot=source.phase_name_snapshot,phase=source.phase,curve_version=source.curve_version,
            ph_text=source.ph_text,bath_ratio=source.bath_ratio,bath_ratio_basis=source.bath_ratio_basis,
            water_amount=source.water_amount,water_unit=source.water_unit,temperature_c=source.temperature_c,
            minutes=source.minutes,dept_belong_id=item.dept_belong_id),actor)
        for plan in require_rows(m.MaterialPlanLine.objects.filter(stage=source)):
            persist(m.WeighingLine(stage=stage,sequence=plan.sequence,plan_line=plan,material=plan.material,
                planned_quantity=plan.required_quantity,unit=plan.quantity_unit,dept_belong_id=item.dept_belong_id),actor)
    record(order,'create_plan',{'exists':False},actor,reason)
    return item


@transaction.atomic
def confirm(item,actor):
    locked(item.batch);item=locked(item);require_state(item,['draft'])
    for stage in require_rows(m.WeighingStage.objects.filter(order=item)):
        for line in require_rows(m.WeighingLine.objects.filter(stage=stage)):
            if line.plan_line_id is not None and line.plan_line.stage.production_recipe_id!=item.production_recipe_id:
                raise ValidationError({'plan_line':'料单明细必须对应本次采用版本。'})
    before=snapshot(item);item.status='confirmed';persist(item,actor);record(item,'confirm',before,actor)
    return item


def measured_quantity(line):
    return converted_sum(m.WeighingRecord.objects.filter(line=line,is_void=False),'quantity','unit',line.unit)


def issued_quantity(line):
    issued=converted_sum(warehouse.StockIssueLine.objects.filter(weighing_line=line,issue__status='posted'),'quantity','unit',line.unit)
    returned=converted_sum(warehouse.StockReceiptLine.objects.filter(original_issue_line__weighing_line=line,receipt__status='posted'),'quantity','unit',line.unit)
    return issued-returned


@transaction.atomic
def weigh(item,actor,quantity,unit,source,at,employee):
    order=locked(item.stage.order);item=locked(item)
    require_state(order,['confirmed','partial_issued','issued'])
    if at < order.document_at:raise ValidationError({'at':'实称时间不能早于料单。'})
    unit.convert_quantity(quantity,item.unit)
    result=persist(m.WeighingRecord(line=item,quantity=quantity,unit=unit,source=source,measured_at=at,
        operator=employee,dept_belong_id=item.dept_belong_id),actor)
    before=snapshot(item);item.status='weighed';persist(item,actor)
    record(result,'weigh',{'exists':False},actor);record(item,'weigh',before,actor)
    return item


@transaction.atomic
def void(item,actor,reason,at):
    order=locked(item.line.stage.order);locked(item.line);item=locked(item)
    if item.is_void:raise ValidationError({'record':'此实称已经作废。'})
    if at < item.measured_at:raise ValidationError({'at':'作废时间不能早于实称。'})
    if warehouse.StockIssueLine.objects.filter(measurement_record=item,issue__status__in=['confirmed','posted']).exists():
        raise ValidationError({'record':'该实称已采用到领料，请先冲销或取消领料单。'})
    before=snapshot(item);item.is_void,item.void_reason,item.voided_at=True,reason,at;persist(item,actor);record(item,'void',before,actor,reason)
    refresh(order,actor)
    return item


def validate_issue(line):
    source=locked(line.weighing_line.stage.order);weighing=locked(line.weighing_line)
    require_state(source,['confirmed','partial_issued','issued'])
    if line.issue.kind!='chemical' or line.lot.material_id!=weighing.material_id:
        raise ValidationError({'weighing_line':'实际化工领料必须采用相同染化料的料单行。'})
    if line.measurement_record_id is not None:
        actual=locked(line.measurement_record)
        if actual.line_id!=weighing.pk or actual.is_void or actual.measured_at > line.issue.document_at:
            raise ValidationError({'measurement_record':'采用实称必须属于本行、仍有效且已经发生。'})
        if line.quantity_source!=actual.source:raise ValidationError({'quantity_source':'出库采用来源必须与具体实称一致。'})
        used=converted_sum(warehouse.StockIssueLine.objects.filter(measurement_record=actual,issue__status='posted').exclude(issue=line.issue),'quantity','unit',actual.unit)
        returns=converted_sum(warehouse.StockReceiptLine.objects.filter(original_issue_line__measurement_record=actual,receipt__status='posted'),'quantity','unit',actual.unit)
        current=converted_sum(warehouse.StockIssueLine.objects.filter(issue=line.issue,measurement_record=actual),'quantity','unit',actual.unit)
        if used-returns+current>actual.quantity:
            raise ValidationError({'quantity':'实称采用净领量不能超过该笔有效实称。'})
    elif line.quantity_source!='manual':
        raise ValidationError({'quantity_source':'没有具体采集来源时仅可使用人工实际录入，不能采用计划量兜底。'})


def refresh(order,actor):
    order=locked(order)
    if order.status in ['draft','cancelled','closed']:return
    lines=list(m.WeighingLine.objects.filter(stage__order=order))
    totals=[issued_quantity(line) for line in lines]
    for line,total in zip(lines,totals):
        before=snapshot(line)
        line.status='issued' if total>=line.planned_quantity else 'weighed' if measured_quantity(line)>0 else 'planned'
        persist(line,actor)
        if before['status']!=line.status:record(line,'refresh_issued',before,actor)
    before=snapshot(order)
    order.status='issued' if lines and all(total>=line.planned_quantity for line,total in zip(lines,totals)) else 'partial_issued' if any(total>0 for total in totals) else 'confirmed'
    persist(order,actor)
    if before['status']!=order.status:record(order,'refresh_issued',before,actor)


@transaction.atomic
def close(item,actor,reason):
    locked(item.batch);item=locked(item);require_state(item,['confirmed','partial_issued','issued'])
    before=snapshot(item);item.status='closed';persist(item,actor);record(item,'close',before,actor,reason)
    return item


@transaction.atomic
def cancel(item,actor,reason):
    locked(item.batch);item=locked(item);require_state(item,['draft','confirmed'])
    if m.WeighingRecord.objects.filter(line__stage__order=item).exists() or warehouse.StockIssueLine.objects.filter(weighing_line__stage__order=item,issue__status__in=['confirmed','posted']).exists():
        raise ValidationError({'order':'已有称量或有效领料，不能取消料单。'})
    before=snapshot(item);item.status='cancelled';persist(item,actor);record(item,'cancel',before,actor,reason)
    return item
