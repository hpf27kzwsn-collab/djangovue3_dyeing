"""实际生产完成、暂停和结案分别记录。"""
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.dateparse import parse_datetime
from plugins.erp_base.business import locked,persist,record,snapshot,require_state,require_rows
from plugins.erp_warehouse import models as wh
from . import models as m,execution_services as execution
from decimal import Decimal
from django.db.models import Q


@transaction.atomic
def release_demand(item,actor,at,quantity,reason):
    card=locked(item.work_card);require_state(card,['completed','closed'])
    locked(item.order_line.order);item=locked(item)
    if item.original_allocation_id is not None:raise ValidationError({'allocation':'返修承接不另释放原订单需求，应处理原工卡分配。'})
    if at<card.completed_at:raise ValidationError({'at':'需求释放不能早于实际生产完成。'})
    related=m.WorkCardOrderAllocation.objects.filter(original_allocation=item).exclude(work_card__status='cancelled')
    if related.exclude(work_card__status__in=['completed','closed']).exists():raise ValidationError({'allocation':'还有未完成承接返修工卡，不能释放这部分需求。'})
    packages=wh.PackageOrderAllocation.objects.filter(Q(work_card_allocation=item)|Q(work_card_allocation__original_allocation=item)).exclude(package__status='void')
    used=sum((row.unit.convert_quantity(row.quantity,item.unit) for row in packages),Decimal('0'))
    if quantity<=0 or used+item.released_unfulfilled_quantity+quantity>item.allocated_quantity:raise ValidationError({'quantity':'明确释放量不能超过尚未形成包装分配的原需求量。'})
    before=snapshot(item);item.released_unfulfilled_quantity+=quantity;item.demand_release_at,item.demand_release_reason=at,reason
    persist(item,actor);record(item,'release_demand',before,actor,reason)
    return item


@transaction.atomic
def pause(item,actor,paused,reason):
    item=locked(item);require_state(item,['released','running'])
    if item.is_paused==paused:raise ValidationError({'is_paused':'工卡已经处于所选暂停状态。'})
    before=snapshot(item);item.is_paused=paused;persist(item,actor);record(item,'pause' if paused else 'resume',before,actor,reason)
    return item


@transaction.atomic
def complete_card(item,actor,at,reason):
    item=locked(item);require_state(item,['running'])
    if item.is_paused:raise ValidationError({'is_paused':'暂停工卡须先恢复。'})
    for operation in require_rows(m.WorkCardOperation.objects.filter(work_card=item)):
        if operation.is_skipped:continue
        latest=m.OperationExecution.objects.filter(operation=operation).exclude(status='cancelled').order_by('-execution_number').first()
        if latest is None or latest.status!='completed':raise ValidationError({'operation':'全部所选且未跳过的节点须实际完工。'})
        if at<parse_datetime(execution.effective(latest)['ended_at']):raise ValidationError({'at':'生产完成不能早于任何实际节点完工。'})
    if wh.Package.objects.filter(work_card=item,status='draft').exists():raise ValidationError({'package':'请先完成或作废尚未采用的包装草稿。'})
    before=snapshot(item);item.status,item.completed_at='completed',at;persist(item,actor);record(item,'complete',before,actor,reason)
    return item


@transaction.atomic
def reopen_card(item,actor,reason):
    batches=list(m.DyeBatch.objects.select_for_update().filter(pk__in=m.DyeBatchWorkCard.objects.filter(work_card=item).values('batch_id')).order_by('pk'))
    item=locked(item);require_state(item,['completed','closed'])
    if wh.StockReceiptLine.objects.filter(work_card=item,receipt__status='posted').exists():raise ValidationError({'receipt':'重新处理生产前须先处理原实际产出入库。'})
    before=snapshot(item);item.status,item.completed_at,item.closed_at='running',None,None;persist(item,actor);record(item,'reopen',before,actor,reason)
    for batch in batches:
        if batch.status in ['completed','closed']:
            previous=snapshot(batch);batch.status='running';persist(batch,actor);record(batch,'reopen_member',previous,actor,reason)
    return item


@transaction.atomic
def close_card(item,actor,at,reason):
    item=locked(item);require_state(item,['completed'])
    if at<item.completed_at:raise ValidationError({'at':'结案不能早于生产完成。'})
    if m.ReworkOrder.objects.filter(original_work_card=item).exclude(status__in=['closed','cancelled']).exists():raise ValidationError({'rework':'原工卡还有未结案返修任务。'})
    if m.WeighingOrder.objects.filter(batch__erp_production_dyebatchworkcard_batch_set__work_card=item).exclude(status__in=['closed','cancelled']).exists():raise ValidationError({'weighing':'关联料单须先结束。'})
    before=snapshot(item);item.status,item.closed_at='closed',at;persist(item,actor);record(item,'close',before,actor,reason)
    return item


@transaction.atomic
def finish_batch(item,actor,close,reason):
    item=locked(item);require_state(item,['completed'] if close else ['running'])
    cards=require_rows(m.DyeBatchWorkCard.objects.filter(batch=item))
    if any(row.work_card.status not in (['closed'] if close else ['completed','closed']) for row in cards):raise ValidationError({'work_cards':'全部缸批成员须先完成对应生产或结案。'})
    if m.PhysicalBatchExecution.objects.filter(batch=item,status='running').exists():raise ValidationError({'execution':'仍有未完工物理执行。'})
    before=snapshot(item);item.status='closed' if close else 'completed';persist(item,actor);record(item,'close' if close else 'complete',before,actor,reason)
    return item
