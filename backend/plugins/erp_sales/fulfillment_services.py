"""实际包装交付、客户退回及投诉，不处理财务。"""
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction
from plugins.erp_base.business import locked,persist,record,snapshot,require_state,require_rows
from plugins.erp_production.services import converted_sum
from plugins.erp_warehouse import models as wh
from . import models as m


def reopened_quantity(line):
    return converted_sum(m.SalesReturnLine.objects.filter(original_delivery_line__order_line=line,
        reopen_order_demand=True,receipt_line__receipt__status='posted',return_order__status__in=['received','closed']), 'quantity','unit',line.ordered_unit)


def delivered_quantity(line):
    return converted_sum(m.DeliveryLine.objects.filter(order_line=line,delivery__status='delivered',delivery__warehouse_issue__status='posted'),'quantity','unit',line.ordered_unit)


def validate_line(line):
    line.full_clean()
    if line.package_allocation_id is None:raise ValidationError({'package_allocation':'新交付须采用明确的包装订单分配。'})
    allocation=line.package_allocation
    require_state(allocation.package,['received','issued','returned'])
    if allocation.work_card_allocation.order_line_id!=line.order_line_id:raise ValidationError({'package_allocation':'包装分配与订单明细不一致。'})
    line.unit.convert_quantity(line.quantity,allocation.unit)


@transaction.atomic
def confirm_delivery(item,actor):
    item=locked(item);require_state(item,['draft'])
    rows=require_rows(m.DeliveryLine.objects.filter(delivery=item))
    list(m.SalesOrder.objects.select_for_update().filter(pk__in=[row.order_line.order_id for row in rows]).order_by('pk'))
    if item.warehouse_issue_id is None:raise ValidationError({'warehouse_issue':'送货须关联实际出库单及所选包装明细。'})
    issue=locked(item.warehouse_issue);require_state(issue,['draft','confirmed'])
    if issue.kind!='delivery' or issue.destination_party_id!=item.customer_id:raise ValidationError({'warehouse_issue':'关联出库必须是本客户的交付出库。'})
    list(wh.Package.objects.select_for_update().filter(pk__in=[row.package_allocation.package_id for row in rows if row.package_allocation_id is not None]).order_by('pk'))
    before=snapshot(item)
    for row in rows:
        validate_line(row)
        previous=converted_sum(m.DeliveryLine.objects.filter(package_allocation=row.package_allocation,delivery__status__in=['confirmed','issued','delivered']).exclude(delivery=item),'quantity','unit',row.package_allocation.unit)
        returned=converted_sum(m.SalesReturnLine.objects.filter(original_delivery_line__package_allocation=row.package_allocation,receipt_line__receipt__status='posted',return_order__status__in=['received','closed']),'quantity','unit',row.package_allocation.unit)
        current=converted_sum([r for r in rows if r.package_allocation_id==row.package_allocation_id],'quantity','unit',row.package_allocation.unit)
        if previous-returned+current>row.package_allocation.quantity:raise ValidationError({'quantity':'有效交付净采用不能超过对应包装订单分配。'})
        source=row.order_line
        reserved=converted_sum(m.DeliveryLine.objects.filter(order_line=source,delivery__status__in=['confirmed','issued','delivered']).exclude(delivery=item),'quantity','unit',source.ordered_unit)
        current_demand=converted_sum([r for r in rows if r.order_line_id==source.pk],'quantity','unit',source.ordered_unit)
        if reserved+current_demand>source.ordered_quantity+reopened_quantity(source):raise ValidationError({'quantity':'有效交付采用不能超过原需求及明确重新打开的需求量。'})
        require_state(source.order,['confirmed','running','completed'])
        if row.manual_price_reason.strip():
            if row.unit_price_snapshot is None or row.price_unit_id is None:raise ValidationError({'unit_price_snapshot':'人工价格须明确价格、计价单位及原因。'})
            row.price_adoption_snapshot={'kind':'manual','reason':row.manual_price_reason,'unit_price':str(row.unit_price_snapshot),'price_unit':row.price_unit_id}
        else:
            if source.unit_price is None or source.price_unit_id is None:raise ValidationError({'order_line':'来源订单尚未明确价格及计价单位。'})
            row.unit_price_snapshot=source.unit_price;row.price_unit=source.price_unit
            row.price_adoption_snapshot={'kind':'order','order_line':source.pk,'price_source':source.price_source_id,
                'unit_price':str(source.unit_price),'price_unit':source.price_unit_id,'manual_price_reason':source.manual_price_reason}
        persist(row,actor)
    check_issue(item,rows,issue)
    item.status='confirmed';persist(item,actor);record(item,'confirm',before,actor)
    return item


def check_issue(delivery,rows,issue):
    actual=list(wh.StockIssueLine.objects.filter(issue=issue))
    if not actual or {row.delivery_line_id for row in actual}!={row.pk for row in rows}:raise ValidationError({'delivery_line':'出库行须完整对应本送货全部明细，不混用其他送货。'})
    for row in rows:
        matches=[r for r in actual if r.delivery_line_id==row.pk]
        package=row.package_allocation.package
        if any(r.package_id!=package.pk or r.lot_id!=package.lot_id or r.work_card_id!=package.work_card_id for r in matches):raise ValidationError({'package':'出库的实际包装、批次及工卡须对应送货采用。'})
        if converted_sum(matches,'quantity','unit',row.unit)!=row.quantity:raise ValidationError({'quantity':'实际出库采用量须等于本送货行数量。'})


def refresh_delivery(item,actor):
    item=locked(item)
    if item.status in ['draft','cancelled']:return
    issue=item.warehouse_issue
    before=snapshot(item)
    item.status='delivered' if issue.status=='posted' and item.delivered_at is not None else 'issued' if issue.status=='posted' else 'confirmed'
    if before['status']!=item.status:persist(item,actor);record(item,'refresh_issue',before,actor)


@transaction.atomic
def deliver(item,actor,at):
    item=locked(item);require_state(item,['issued']);issue=locked(item.warehouse_issue);require_state(issue,['posted'])
    if at < issue.posted_at:raise ValidationError({'at':'实际客户交付不能早于实际出库。'})
    check_issue(item,require_rows(m.DeliveryLine.objects.filter(delivery=item)),issue)
    before=snapshot(item);item.status,item.delivered_at='delivered',at;persist(item,actor);record(item,'deliver',before,actor)
    return item


@transaction.atomic
def cancel_delivery(item,actor,reason):
    item=locked(item);require_state(item,['draft','confirmed'])
    if item.warehouse_issue_id is not None and item.warehouse_issue.status=='posted':raise ValidationError({'warehouse_issue':'请先冲销实际出库。'})
    before=snapshot(item);item.status='cancelled';persist(item,actor);record(item,'cancel',before,actor,reason)
    return item


@transaction.atomic
def undo_delivery(item,actor,reason):
    item=locked(item);require_state(item,['delivered'])
    if m.SalesReturnLine.objects.filter(original_delivery_line__delivery=item).exclude(return_order__status='cancelled').exists():raise ValidationError({'delivery':'此交付已有客户退回引用，先处理退回业务。'})
    before=snapshot(item);item.status,item.delivered_at='issued',None;persist(item,actor);record(item,'undo_delivery',before,actor,reason)
    return item


def return_scope(row):
    row.full_clean()
    if row.original_issue_line_id is None or row.receipt_line_id is None:raise ValidationError({'original_issue_line':'客户退回须关联原实际交付出库行及本次待检收回行。'})
    source=row.original_issue_line;delivery=row.original_delivery_line.delivery
    require_state(delivery,['delivered']);require_state(source.issue,['posted'])
    if source.delivery_line_id!=row.original_delivery_line_id or source.issue_id!=delivery.warehouse_issue_id:raise ValidationError({'original_issue_line':'原出库行必须对应原实际送货行。'})
    receipt=row.receipt_line
    if receipt.receipt.kind!='sales_return' or receipt.receipt.source_party_id!=row.return_order.customer_id or receipt.original_issue_line_id!=source.pk:
        raise ValidationError({'receipt_line':'退回收货须明确本客户、原实际出库及待检范围。'})
    if receipt.package_id!=source.package_id or receipt.lot_id!=source.lot_id or receipt.quality_state!='pending':raise ValidationError({'receipt_line':'退回包装、批次须对应原出库，并进入待检。'})
    if row.unit.convert_quantity(row.quantity,receipt.unit)!=receipt.quantity:raise ValidationError({'quantity':'退回量须等于本次实际收回行量。'})
    if row.reopen_order_demand and not row.reopen_reason.strip():raise ValidationError({'reopen_reason':'重新打开需求须填写明确处理意见。'})


@transaction.atomic
def confirm_return(item,actor):
    item=locked(item);require_state(item,['draft']);before=snapshot(item)
    rows=require_rows(m.SalesReturnLine.objects.filter(return_order=item))
    list(wh.StockIssueLine.objects.select_for_update().filter(pk__in=[row.original_issue_line_id for row in rows]).order_by('pk'))
    for row in rows:
        return_scope(row)
        require_state(row.receipt_line.receipt,['draft','confirmed'])
        if item.returned_at < row.original_delivery_line.delivery.delivered_at:raise ValidationError({'returned_at':'退回不能早于原客户交付。'})
        previous=converted_sum(m.SalesReturnLine.objects.filter(original_issue_line=row.original_issue_line).exclude(return_order__status__in=['draft','cancelled']).exclude(return_order=item),'quantity','unit',row.original_issue_line.unit)
        current=converted_sum([r for r in rows if r.original_issue_line_id==row.original_issue_line_id],'quantity','unit',row.original_issue_line.unit)
        if previous+current>row.original_issue_line.quantity:raise ValidationError({'quantity':'累计有效退回不能超过原实际出库量。'})
    item.status='confirmed';persist(item,actor);record(item,'confirm',before,actor)
    return item


def refresh_return(item,actor):
    item=locked(item)
    if item.status in ['draft','cancelled','closed']:return
    rows=list(m.SalesReturnLine.objects.filter(return_order=item))
    state='received' if rows and all(row.receipt_line.receipt.status=='posted' for row in rows) else 'confirmed'
    before=snapshot(item);item.status=state
    if before['status']!=state:persist(item,actor);record(item,'refresh_received',before,actor)
    if state=='received':
        for row in rows:
            if row.reopen_order_demand:
                order=locked(row.original_delivery_line.order_line.order);line=locked(row.original_delivery_line.order_line)
                if line.is_closed:prior=snapshot(line);line.is_closed=False;persist(line,actor);record(line,'reopen_demand',prior,actor,row.reopen_reason)
                if order.status in ['completed','closed']:
                    prior=snapshot(order);order.status='running';order.closed_at=None;persist(order,actor);record(order,'reopen_demand',prior,actor,row.reopen_reason)


@transaction.atomic
def close_return(item,actor,reason):
    item=locked(item);require_state(item,['received']);before=snapshot(item);item.status='closed';persist(item,actor);record(item,'close',before,actor,reason)
    return item


@transaction.atomic
def reopen_return(item,actor,reason):
    item=locked(item);require_state(item,['closed'])
    rows=require_rows(m.SalesReturnLine.objects.filter(return_order=item))
    for row in rows:require_state(row.receipt_line.receipt,['posted'])
    before=snapshot(item);item.status='received';persist(item,actor);record(item,'reopen',before,actor,reason)
    return item


@transaction.atomic
def cancel_return(item,actor,reason):
    item=locked(item);require_state(item,['draft','confirmed'])
    if m.SalesReturnLine.objects.filter(return_order=item,receipt_line__receipt__status='posted').exists():raise ValidationError({'receipt_line':'请先冲销实际收回库存。'})
    before=snapshot(item);item.status='cancelled';persist(item,actor);record(item,'cancel',before,actor,reason)
    return item


@transaction.atomic
def handle_complaint(item,actor,close,reason):
    item=locked(item);require_state(item,['open','handling'])
    rows=require_rows(m.CustomerComplaintLine.objects.filter(complaint=item))
    for row in rows:
        if row.order_line_id is not None and row.order_line.order.customer_id!=item.customer_id:raise ValidationError({'order_line':'投诉订单必须属于本客户。'})
        if row.delivery_line_id is not None and row.delivery_line.delivery.customer_id!=item.customer_id:raise ValidationError({'delivery_line':'投诉交付必须属于本客户。'})
        if row.package_id is not None and row.work_card_id is not None and row.package.work_card_id!=row.work_card_id:raise ValidationError({'package':'投诉包装与工卡不一致。'})
        if close and not row.handling_text:raise ValidationError({'handling_text':'结案须记录各投诉问题的实际处理意见。'})
    before=snapshot(item);item.status='closed' if close else 'handling';persist(item,actor);record(item,'close' if close else 'handle',before,actor,reason)
    return item
