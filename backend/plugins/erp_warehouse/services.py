"""库存只由实际收发、调拨、调整和等量反向冲销生效。"""
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from plugins.erp_base.business import locked, persist, record, snapshot, require_state, require_rows
from plugins.erp_base.models import Warehouse
from . import models as m

PARENTS = {m.StockReceiptLine: ('receipt', ''), m.StockIssueLine: ('issue', ''),
           m.StockTransferLine: ('transfer', ''), m.StockCountLine: ('count', ''),
           m.StockAdjustmentLine: ('adjustment', '')}
LINES = {m.StockReceipt: (m.StockReceiptLine, 'receipt'), m.StockIssue: (m.StockIssueLine, 'issue'),
         m.StockTransfer: (m.StockTransferLine, 'transfer'), m.StockAdjustment: (m.StockAdjustmentLine, 'adjustment')}
OWNED = {m.InventoryLot: {'production_batch'}, m.StockReceipt: {'status', 'posted_at'},
    m.StockIssue: {'status', 'posted_at'}, m.StockTransfer: {'status', 'posted_at'},
    m.StockAdjustment: {'status', 'posted_at', 'count'}, m.StockCount: {'status', 'snapshot_at', 'counted_at'},
    m.StockReceiptLine: {'work_card', 'package', 'quantity_source'},
    m.StockIssueLine: {'work_card', 'weighing_line', 'delivery_line', 'package', 'measurement_record', 'quantity_source'},
    m.StockTransferLine: {'package'}, m.StockCountLine: {'book_quantity', 'package'},
    m.StockAdjustmentLine: {'disposition', 'package'},
    m.InventoryMovement: {f.name for f in m.InventoryMovement._meta.fields},
    m.StockBalance: {f.name for f in m.StockBalance._meta.fields}}


def editable(item):
    if isinstance(item, (m.InventoryMovement, m.StockBalance)):
        raise ValidationError({'id': '库存余额和流水由过账维护。'})
    if isinstance(item, m.InventoryLot):
        if m.StockReceiptLine.objects.filter(lot=item).exists() or m.StockIssueLine.objects.filter(lot=item).exists():
            raise ValidationError({'lot': '批次已有业务来源，不能修改批次身份和货权。'})
        return
    if isinstance(item, m.StockCountLine):
        require_state(item.count, ['counting'])
        return
    if type(item) in PARENTS:
        item = getattr(item, PARENTS[type(item)][0])
    require_state(item, ['draft'])


def parent_editable(model, item):
    if model is m.StockCountLine:
        require_state(item, ['counting'])
    else:
        editable(item)


def validate(item):
    if isinstance(item, m.StockCountLine):
        balance = m.StockBalance.objects.filter(lot=item.lot, location=item.location,
                                               quality_state=item.quality_state, package=item.package).first()
        if item.pk is None:
            item.book_quantity = Decimal('0') if balance is None else balance.quantity
        elif row_dimensions(item) != row_dimensions(m.StockCountLine.objects.get(pk=item.pk)):
            raise ValidationError({'lot': '快照行的批次、库位、质量和包装不能改变。'})
    if isinstance(item, (m.StockReceiptLine, m.StockIssueLine)) and item.quantity_source == 'legacy_unverified':
        raise ValidationError({'quantity_source': '待核实旧事实由导入归档维护，不作为新单据的实际数量。'})


def deletable(item):
    if isinstance(item, m.StockCountLine):
        raise ValidationError({'count': '盘点快照行不能删除，请填写实盘数量。'})
    editable(item)


POLICY = {'parents': PARENTS, 'owned': OWNED, 'editable': editable, 'validate': validate,
          'parent_editable': parent_editable, 'lock_root': locked, 'deletable': deletable}


def warehouse_ids(item):
    return [item.from_warehouse_id, item.to_warehouse_id] if isinstance(item, m.StockTransfer) else [item.warehouse_id]


def lock_warehouses(ids, count=None):
    rows = list(Warehouse.objects.select_for_update().filter(pk__in=ids).order_by('pk'))
    if any(row.is_active is False for row in rows):
        raise ValidationError({'warehouse': '仓库已停用。'})
    counts = m.StockCount.objects.filter(warehouse_id__in=ids, status__in=['counting', 'confirmed'])
    if count is not None:
        counts = counts.exclude(pk=count.pk)
    if counts.exists():
        raise ValidationError({'warehouse': '仓库盘点中，请先完成盘点调整，再进行收发。'})


def row_dimensions(row):
    return {'lot': row.lot, 'location': row.location, 'quality_state': row.quality_state, 'package': row.package}


def movement(row, quantity, actor, *, source, leg=1, location=None, quality_state=None, reverses=None, at=None):
    dimensions = row_dimensions(row) if isinstance(row, m.InventoryMovement) else {
        'lot': row.lot, 'location': location, 'quality_state': quality_state, 'package': row.package}
    balance = m.StockBalance.objects.select_for_update().filter(**dimensions).first()
    if balance is None:
        balance = m.StockBalance(**dimensions, quantity=Decimal('0'))
    balance.quantity += quantity
    if balance.quantity < 0:
        raise ValidationError({'quantity': '对应货权、批次、库位、质量状态和包装的实际库存不足。'})
    persist(balance, actor)
    values = {source: row if reverses is None else getattr(row, source), 'leg_number': leg,
              'quantity_delta': quantity, 'unit': row.lot.material.stock_unit,
              'occurred_at': at, 'reverses': reverses}
    return persist(m.InventoryMovement(**dimensions, **values), actor)


def receipt_rules(item, rows):
    from plugins.erp_purchase import models as purchase
    from plugins.erp_purchase.services import received_quantity
    totals = {}
    for row in rows:
        if row.quantity_source == 'legacy_unverified':
            raise ValidationError({'quantity_source': '数量来源未核实，不能过账。'})
        if item.kind == 'purchase':
            if row.purchase_order_line_id is None:
                raise ValidationError({'purchase_order_line': '采购收货必须关联采购明细。'})
            source = row.purchase_order_line
            require_state(source.order, ['confirmed', 'partial_received', 'received'])
            if item.source_party_id != source.order.supplier_id or row.lot.material_id != source.material_id:
                raise ValidationError({'purchase_order_line': '收货供应商或物料与采购明细不一致。'})
            totals[source.pk] = totals.get(source.pk, Decimal('0')) + row.unit.convert_quantity(row.quantity, source.unit)
        if item.kind == 'customer_material' and row.lot.owner_id != item.source_party_id:
            raise ValidationError({'lot': '客供料货权必须属于提供来料的客户。'})
        if item.kind in ['purchase', 'customer_material'] and row.quality_state != 'pending':
            raise ValidationError({'quality_state': '新来料先入待检库存，由来料检验及质量处置放行。'})
        if item.kind == 'material_return':
            if row.original_issue_line_id is None:
                raise ValidationError({'original_issue_line': '生产退料必须指定实际领料来源。'})
            original = row.original_issue_line
            require_state(original.issue, ['posted'])
            if original.lot_id != row.lot_id or original.work_card_id != row.work_card_id:
                raise ValidationError({'original_issue_line': '退料批次或工卡与原实际领料不一致。'})
            returned = sum((r.quantity for r in m.StockReceiptLine.objects.filter(original_issue_line=original,
                           receipt__status='posted').exclude(receipt=item)), Decimal('0'))
            current = sum((r.quantity for r in rows if r.original_issue_line_id == original.pk), Decimal('0'))
            if returned + current > original.quantity:
                raise ValidationError({'quantity': '累计退料不能超过原实际出库数量。'})
        if item.kind in ['semi_output', 'finished_output'] and row.work_card_id is None:
            raise ValidationError({'work_card': '生产产出必须关联实际工卡。'})
        if item.kind == 'finished_output':
            if row.package_id is None or row.work_card.status not in ['completed', 'closed']:
                raise ValidationError({'package': '成品入库必须关联完成包装的生产工卡和包装单元。'})
            require_state(row.package, ['packed'])
    for key in sorted(totals):
        source = locked(purchase.PurchaseOrderLine.objects.get(pk=key))
        if received_quantity(source) + totals[key] > source.quantity:
            raise ValidationError({'quantity': '累计实际收货不能超过采购订货数量。'})


def issue_rules(item, rows):
    for row in rows:
        if row.quantity_source == 'legacy_unverified':
            raise ValidationError({'quantity_source': '数量来源未核实，不能过账。'})
        if item.kind in ['production', 'chemical', 'delivery', 'subcontract'] and row.quality_state != 'released':
            raise ValidationError({'quality_state': '此出库业务只能使用已放行库存。'})
        if item.kind == 'purchase_return':
            if row.original_receipt_line_id is None:
                raise ValidationError({'original_receipt_line': '采购退货必须明确原实际收货行。'})
            original = row.original_receipt_line
            require_state(original.receipt, ['posted'])
            if original.receipt.kind != 'purchase' or original.receipt.source_party_id != item.destination_party_id or row.lot_id != original.lot_id:
                raise ValidationError({'original_receipt_line': '采购退货来源、货权批次或供应商不一致。'})
            returned = sum((r.quantity for r in m.StockIssueLine.objects.filter(original_receipt_line=original,
                           issue__kind='purchase_return', issue__status='posted').exclude(issue=item)), Decimal('0'))
            current = sum((r.quantity for r in rows if r.original_receipt_line_id == original.pk), Decimal('0'))
            if returned + current > original.quantity:
                raise ValidationError({'quantity': '退货不能超过原实际收货数量。'})
        if item.kind == 'customer_material_return' and row.lot.owner_id != item.destination_party_id:
            raise ValidationError({'destination_party': '客料只能退回其货权客户。'})
        if item.kind == 'scrap' and row.quality_state != 'scrap':
            raise ValidationError({'quality_state': '报废出库只允许已处置为待报废的库存。'})


@transaction.atomic
def confirm(item, actor):
    item = locked(item)
    require_state(item, ['draft'])
    before = snapshot(item)
    model, key = LINES[type(item)]
    rows = require_rows(model.objects.filter(**{key: item}))
    if isinstance(item, m.StockReceipt):
        receipt_rules(item, rows)
    elif isinstance(item, m.StockIssue):
        issue_rules(item, rows)
    item.status = 'confirmed'
    persist(item, actor)
    record(item, 'confirm', before, actor)
    return item


def refresh_sources(item, actor):
    from plugins.erp_purchase import models as purchase
    from plugins.erp_purchase.services import refresh_order
    if isinstance(item, m.StockReceipt):
        ids = m.StockReceiptLine.objects.filter(receipt=item, purchase_order_line__isnull=False).values_list('purchase_order_line__order_id', flat=True)
    elif isinstance(item, m.StockIssue):
        ids = m.StockIssueLine.objects.filter(issue=item, original_receipt_line__purchase_order_line__isnull=False).values_list('original_receipt_line__purchase_order_line__order_id', flat=True)
        for returned in purchase.PurchaseReturn.objects.select_for_update().filter(warehouse_issue=item):
            returned.status = 'issued' if item.status == 'posted' else 'confirmed'
            persist(returned, actor)
    else:
        ids = []
    for source in purchase.PurchaseOrder.objects.filter(pk__in=ids).order_by('pk'):
        refresh_order(source, actor)


@transaction.atomic
def post(item, actor, at):
    if isinstance(item, m.StockIssue) and item.kind == 'purchase_return':
        from plugins.erp_purchase.models import PurchaseReturn
        list(PurchaseReturn.objects.select_for_update().filter(warehouse_issue=item).order_by('pk'))
    if isinstance(item, m.StockAdjustment) and item.count_id is not None:
        locked(item.count)
    item = locked(item)
    if item.status == 'posted':
        return item
    require_state(item, ['confirmed'])
    before = snapshot(item)
    if at < item.document_at:
        raise ValidationError({'at': '库存生效时间不得早于单据日期。'})
    count = item.count if isinstance(item, m.StockAdjustment) else None
    lock_warehouses(warehouse_ids(item), count)
    model, key = LINES[type(item)]
    rows = require_rows(model.objects.filter(**{key: item}))
    list(m.InventoryLot.objects.select_for_update().filter(pk__in=[r.lot_id for r in rows]).order_by('pk'))
    if isinstance(item, m.StockReceipt):
        receipt_rules(item, rows)
        for row in rows:
            movement(row, row.quantity, actor, source='receipt_line', location=row.location, quality_state=row.quality_state, at=at)
    elif isinstance(item, m.StockIssue):
        issue_rules(item, rows)
        for row in rows:
            movement(row, -row.quantity, actor, source='issue_line', location=row.location, quality_state=row.quality_state, at=at)
    elif isinstance(item, m.StockTransfer):
        for row in rows:
            if row.from_location_id == row.to_location_id:
                raise ValidationError({'to_location': '调拨必须明确不同的发出和接收库位。'})
            for location in [row.from_location, row.to_location]:
                if location.kind != 'bin':
                    raise ValidationError({'location': '调拨只使用实际库位。'})
            movement(row, -row.quantity, actor, source='transfer_line', leg=1, location=row.from_location, quality_state=row.quality_state, at=at)
            movement(row, row.quantity, actor, source='transfer_line', leg=2, location=row.to_location, quality_state=row.quality_state, at=at)
    else:
        if count is not None:
            require_state(count, ['confirmed'])
            expected = set(m.StockCountLine.objects.filter(count=count).exclude(counted_quantity=F('book_quantity')).values_list('pk', flat=True))
            if {row.count_line_id for row in rows} != expected or at < count.counted_at:
                raise ValidationError({'count': '盘点调整必须完整对应本次已确认差异及实盘完成时间。'})
        for row in rows:
            if row.count_line_id is not None:
                source = row.count_line
                if source.count_id != item.count_id or source.difference != row.quantity_delta or row_dimensions(source) != row_dimensions(row):
                    raise ValidationError({'count_line': '调整维度和差异必须与盘点来源一致。'})
            if row.new_quality_state is None:
                movement(row, row.quantity_delta, actor, source='adjustment_line', location=row.location, quality_state=row.quality_state, at=at)
            else:
                quality_rules(row)
                movement(row, -row.quantity_delta, actor, source='adjustment_line', leg=1, location=row.location, quality_state=row.quality_state, at=at)
                movement(row, row.quantity_delta, actor, source='adjustment_line', leg=2, location=row.location, quality_state=row.new_quality_state, at=at)
    item.status, item.posted_at = 'posted', at
    persist(item, actor)
    if count is not None:
        count = locked(count)
        require_state(count, ['confirmed'])
        count.status = 'adjusted'
        persist(count, actor)
    refresh_sources(item, actor)
    record(item, 'post', before, actor)
    return item


def quality_rules(row):
    disposition = locked(row.disposition)
    target = {'release': 'released', 'concession': 'released', 'rework': 'held',
              'downgrade': 'released', 'scrap': 'scrap', 'hold': 'held'}[disposition.kind]
    if row.new_quality_state != target:
        raise ValidationError({'new_quality_state': '目标库存质量状态与处置结论不一致。'})
    inspection = disposition.inspection
    if inspection.kind == 'incoming' and inspection.lot_id != row.lot_id:
        raise ValidationError({'disposition': '来料处置只能处理所检批次。'})
    if inspection.kind != 'incoming' and (row.package_id is None or row.package.work_card_id != inspection.work_card_id):
        raise ValidationError({'disposition': '生产质量处置必须明确所检工卡的具体包装。'})
    used = sum((r.lot.material.stock_unit.convert_quantity(r.quantity_delta, disposition.unit)
                for r in m.StockAdjustmentLine.objects.filter(disposition=disposition, adjustment__status='posted')), Decimal('0'))
    amount = sum((r.lot.material.stock_unit.convert_quantity(r.quantity_delta, disposition.unit)
                  for r in m.StockAdjustmentLine.objects.filter(adjustment=row.adjustment,
                  disposition=disposition, new_quality_state__isnull=False)), Decimal('0'))
    if used + amount > disposition.quantity:
        raise ValidationError({'quantity_delta': '库存处置数量不能超过批准处置数量。'})


@transaction.atomic
def reverse(item, actor, at, reason):
    if isinstance(item, m.StockIssue) and item.kind == 'purchase_return':
        from plugins.erp_purchase.models import PurchaseReturn
        list(PurchaseReturn.objects.select_for_update().filter(warehouse_issue=item).order_by('pk'))
    if isinstance(item, m.StockAdjustment) and item.count_id is not None:
        locked(item.count)
    item = locked(item)
    if item.status == 'reversed':
        return item
    require_state(item, ['posted'])
    before = snapshot(item)
    lock_warehouses(warehouse_ids(item))
    model, key = LINES[type(item)]
    source = {m.StockReceipt: 'receipt_line', m.StockIssue: 'issue_line',
              m.StockTransfer: 'transfer_line', m.StockAdjustment: 'adjustment_line'}[type(item)]
    rows = list(m.InventoryMovement.objects.filter(**{source+'__'+key: item}, reverses__isnull=True).order_by('-pk'))
    list(m.InventoryLot.objects.select_for_update().filter(pk__in=[r.lot_id for r in rows]).order_by('pk'))
    original_ids = [r.pk for r in rows]
    reversed_ids = m.InventoryMovement.objects.filter(reverses__isnull=False).values_list('reverses_id', flat=True)
    for row in rows:
        if at < row.occurred_at:
            raise ValidationError({'at': '冲销时间不得早于原库存生效时间。'})
        later = m.InventoryMovement.objects.filter(**row_dimensions(row), pk__gt=row.pk, reverses__isnull=True).exclude(pk__in=original_ids).exclude(pk__in=reversed_ids)
        if later.exists():
            raise ValidationError({'source': '同维度已有后续有效库存业务，请先按逆序处理后续单据。'})
        movement(row, -row.quantity_delta, actor, source=source, leg=row.leg_number, reverses=row, at=at)
    item.status = 'reversed'
    persist(item, actor)
    if isinstance(item, m.StockAdjustment) and item.count_id is not None:
        count = locked(item.count)
        count_before = snapshot(count)
        count.status = 'cancelled'
        persist(count, actor)
        record(count, 'reverse_adjustment', count_before, actor, reason)
    refresh_sources(item, actor)
    record(item, 'reverse', before, actor, reason)
    return item


@transaction.atomic
def begin_count(item, actor):
    item = locked(item)
    require_state(item, ['draft'])
    lock_warehouses([item.warehouse_id])
    before = snapshot(item)
    item.snapshot_at, item.status = timezone.now(), 'counting'
    persist(item, actor)
    for balance in m.StockBalance.objects.filter(location__warehouse=item.warehouse).order_by('pk'):
        persist(m.StockCountLine(count=item, **row_dimensions(balance), book_quantity=balance.quantity), actor)
    record(item, 'begin', before, actor)
    return item


@transaction.atomic
def confirm_count(item, actor, at):
    item = locked(item)
    require_state(item, ['counting'])
    lock_warehouses([item.warehouse_id], item)
    before = snapshot(item)
    rows = list(m.StockCountLine.objects.filter(count=item).order_by('pk'))
    if at < item.snapshot_at:
        raise ValidationError({'at': '实盘完成时间不得早于账面快照时间。'})
    for row in rows:
        row.full_clean()
        if row.counted_quantity is None:
            raise ValidationError({'counted_quantity': '未盘数量不能作为零。请完成每一行实盘。'})
        if row.difference != 0 and not row.reason.strip():
            raise ValidationError({'reason': '实盘存在差异，请填写原因。'})
    item.status, item.counted_at = 'confirmed', at
    persist(item, actor)
    record(item, 'confirm', before, actor)
    return item


@transaction.atomic
def adjust_count(item, actor, number, at, reason):
    item = locked(item)
    require_state(item, ['confirmed'])
    lock_warehouses([item.warehouse_id], item)
    before = snapshot(item)
    rows = list(m.StockCountLine.objects.filter(count=item).exclude(counted_quantity=F('book_quantity')).order_by('pk'))
    if not rows:
        item.status = 'adjusted'
        persist(item, actor)
        record(item, 'adjust', before, actor, reason)
        return item
    adjustment = persist(m.StockAdjustment(number=number, document_at=at, warehouse=item.warehouse,
                                          count=item, reason=reason), actor)
    for index, row in enumerate(rows, 1):
        persist(m.StockAdjustmentLine(adjustment=adjustment, line_number=index, **row_dimensions(row),
                                      quantity_delta=row.difference, count_line=row), actor)
    confirm(adjustment, actor)
    post(adjustment, actor, at)
    item.refresh_from_db()
    record(item, 'adjust', before, actor, reason)
    return item
