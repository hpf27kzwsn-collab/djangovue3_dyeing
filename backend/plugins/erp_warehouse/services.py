from plugins.erp_quality import models as q
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
           m.StockAdjustmentLine: ('adjustment', ''),m.LotTransformationLine:('transformation','')}
PARENTS.update({m.PackageOrderAllocation:('package',''),m.PackageDispositionAllocation:('package','')})
LINES = {m.StockReceipt: (m.StockReceiptLine, 'receipt'), m.StockIssue: (m.StockIssueLine, 'issue'),
         m.StockTransfer: (m.StockTransferLine, 'transfer'), m.StockAdjustment: (m.StockAdjustmentLine, 'adjustment')}
OWNED = {m.InventoryLot: set(), m.StockReceipt: {'status', 'posted_at'},
    m.StockIssue: {'status', 'posted_at'}, m.StockTransfer: {'status', 'posted_at'},
    m.StockAdjustment: {'status', 'posted_at', 'count'}, m.StockCount: {'status', 'snapshot_at', 'counted_at'},
    m.StockReceiptLine: {'quantity_source'},
    m.StockIssueLine: {'quantity_source'},
    m.StockTransferLine: {'package'}, m.StockCountLine: {'book_quantity', 'package'},
    m.StockAdjustmentLine: {'package'},m.LotTransformation:{'is_confirmed','confirmed_at','is_void','voided_at','void_reason'},m.LotTransformationLine:set(),
    m.InventoryMovement: {f.name for f in m.InventoryMovement._meta.fields},
    m.StockBalance: {f.name for f in m.StockBalance._meta.fields}}
OWNED.update({m.Package:{'status','packed_at','packer','net_mass_kg','calculation_snapshot','packaging_execution'},
    m.PackageOrderAllocation:set(),m.PackageDispositionAllocation:set(),m.LabelPrint:{f.name for f in m.LabelPrint._meta.fields}})


def editable(item):
    if isinstance(item, (m.InventoryMovement, m.StockBalance,m.LabelPrint)):
        raise ValidationError({'id': '库存余额和流水由过账维护。'})
    if isinstance(item,(m.LotTransformation,m.LotTransformationLine)):
        root=item if isinstance(item,m.LotTransformation) else item.transformation
        if root.is_confirmed or root.is_void:raise ValidationError({'transformation':'已确认或已取消采用的批次谱系不能改写。'})
        return
    if isinstance(item, m.InventoryLot):
        if m.StockReceiptLine.objects.filter(lot=item).exists() or m.StockIssueLine.objects.filter(lot=item).exists() or m.Package.objects.filter(lot=item).exists():
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
    if isinstance(item,m.LabelPrint):raise ValidationError({'print':'打印记录通过明确请求和确认生成。'})
    if isinstance(item,m.PackageOrderAllocation):
        from .packing_services import validate_allocation
        validate_allocation(item)
    if isinstance(item,m.PackageDispositionAllocation):
        from .packing_services import validate_coverage
        validate_coverage(item)
    if isinstance(item,m.StockIssueLine) and item.measurement_record_id is not None:
        item.quantity_source=item.measurement_record.source
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
        if item.kind=='semi_output':
            from plugins.erp_production import execution_services as actual
            from plugins.erp_base.models import Unit
            if row.source_execution_id is None:raise ValidationError({'source_execution':'半成品实际产出须采用明确执行。'})
            require_state(row.source_execution,['completed'])
            if row.source_execution.operation.work_card_id!=row.work_card_id:raise ValidationError({'source_execution':'半成品执行来源与工卡不一致。'})
            if row.lot.material_id!=row.work_card.material_id:raise ValidationError({'lot':'半成品物料须对应实际生产工卡。'})
            fact=actual.effective(row.source_execution)
            from django.utils.dateparse import parse_datetime
            if item.document_at<parse_datetime(fact['ended_at']):raise ValidationError({'document_at':'半成品收货不能早于本轮实际完工。'})
            if row.unit.dimension=='mass':
                if fact['output_mass_kg'] is None:raise ValidationError({'source_execution':'本轮未记录实际产出kg。'})
                maximum=Unit.objects.get(code='kg').convert_quantity(Decimal(fact['output_mass_kg']),row.unit)
            else:
                if fact['output_quantity'] is None or row.source_execution.output_unit_id is None:raise ValidationError({'source_execution':'本轮未记录该维度的实际产出量。'})
                maximum=row.source_execution.output_unit.convert_quantity(Decimal(fact['output_quantity']),row.unit)
            previous=sum((r.quantity for r in m.StockReceiptLine.objects.filter(source_execution=row.source_execution,receipt__kind='semi_output',receipt__status='posted').exclude(receipt=item)),Decimal('0'))
            current=sum((r.quantity for r in rows if r.source_execution_id==row.source_execution_id),Decimal('0'))
            if previous+current>maximum:raise ValidationError({'quantity':'半成品有效收货累计不能超过本轮实际产出。'})
        if item.kind == 'finished_output':
            if row.package_id is None or row.work_card.status not in ['completed', 'closed']:
                raise ValidationError({'package': '成品入库必须关联完成包装的生产工卡和包装单元。'})
            from .packing_services import package_quantity
            require_state(row.package, ['packed','received'])
            if row.package.lot_id!=row.lot_id or row.package.work_card_id!=row.work_card_id or row.quality_state!='released':raise ValidationError({'package':'成品入库必须对应放行包装的批次和工卡。'})
            if item.document_at<row.package.packed_at or item.document_at<row.work_card.completed_at:raise ValidationError({'document_at':'成品收货不能早于实际包装及生产完成。'})
            prior=sum((r.quantity for r in m.StockReceiptLine.objects.filter(package=row.package,receipt__kind='finished_output',receipt__status='posted').exclude(receipt=item)),Decimal('0'))
            current=sum((r.quantity for r in rows if r.package_id==row.package_id),Decimal('0'))
            if prior+current>package_quantity(row.package,row.unit):raise ValidationError({'quantity':'分批成品入库累计不能超过实际包装量。'})
        if item.kind=='sales_return':
            from plugins.erp_sales.models import SalesReturnLine
            from plugins.erp_sales.fulfillment_services import return_scope
            source=SalesReturnLine.objects.get(receipt_line=row)
            require_state(source.return_order,['confirmed','received'])
            return_scope(source)
    for key in sorted(totals):
        source = locked(purchase.PurchaseOrderLine.objects.get(pk=key))
        if received_quantity(source) + totals[key] > source.quantity:
            raise ValidationError({'quantity': '累计实际收货不能超过采购订货数量。'})


def issue_rules(item, rows):
    for row in rows:
        if item.kind=='production':
            if row.work_card_id is None:raise ValidationError({'work_card':'生产领料必须明确实际工卡。'})
            require_state(row.work_card,['released','running'])
            if row.work_card.factory_id!=item.warehouse.factory_id:raise ValidationError({'work_card':'领料工卡和仓库工厂不一致。'})
        if item.kind=='chemical':
            if row.weighing_line_id is None:raise ValidationError({'weighing_line':'化工领料必须明确本次料单阶段及明细。'})
            from plugins.erp_production.weighing_services import validate_issue
            validate_issue(row)
        if item.kind=='delivery':
            from plugins.erp_sales.models import Delivery
            from plugins.erp_sales.fulfillment_services import check_issue
            delivery=Delivery.objects.get(warehouse_issue=item)
            require_state(delivery,['confirmed','issued'])
            check_issue(delivery,require_rows(delivery.erp_sales_deliveryline_delivery_set.all()),item)
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
    lock_source_documents(item)
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


def lock_source_documents(item):
    from plugins.erp_sales import models as sales
    if isinstance(item,m.StockIssue):
        list(sales.Delivery.objects.select_for_update().filter(warehouse_issue=item).order_by('pk'))
    if isinstance(item,m.StockReceipt):
        list(sales.SalesReturn.objects.select_for_update().filter(pk__in=sales.SalesReturnLine.objects.filter(receipt_line__receipt=item).values('return_order_id')).order_by('pk'))
    if isinstance(item,m.StockIssue):order_ids=m.StockIssueLine.objects.filter(issue=item,delivery_line__isnull=False).values('delivery_line__order_line__order_id')
    elif isinstance(item,m.StockReceipt):order_ids=m.StockReceiptLine.objects.filter(receipt=item,original_issue_line__delivery_line__isnull=False).values('original_issue_line__delivery_line__order_line__order_id')
    else:order_ids=[]
    list(sales.SalesOrder.objects.select_for_update().filter(pk__in=order_ids).order_by('pk'))


def lock_business_sources(item,rows):
    from plugins.erp_production import models as production
    if isinstance(item,m.StockIssue):
        order_ids=[row.weighing_line.stage.order_id for row in rows if row.weighing_line_id is not None]
    elif isinstance(item,m.StockReceipt):
        order_ids=[row.original_issue_line.weighing_line.stage.order_id for row in rows if row.original_issue_line_id is not None and row.original_issue_line.weighing_line_id is not None]
    else:order_ids=[]
    list(production.WeighingOrder.objects.select_for_update().filter(pk__in=order_ids).order_by('pk'))
    if isinstance(item,m.StockAdjustment):
        dispositions=[row.disposition_id for row in rows if row.disposition_id is not None]
        list(q.QualityInspection.objects.select_for_update().filter(pk__in=q.QualityDisposition.objects.filter(pk__in=dispositions).values('inspection_id')).order_by('pk'))
        list(q.QualityDisposition.objects.select_for_update().filter(pk__in=dispositions).order_by('pk'))
    list(m.Package.objects.select_for_update().filter(pk__in=[row.package_id for row in rows if row.package_id is not None]).order_by('pk'))


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
    if isinstance(item,m.StockIssue):
        weighing_ids=m.StockIssueLine.objects.filter(issue=item,weighing_line__isnull=False).values_list('weighing_line__stage__order_id',flat=True)
    elif isinstance(item,m.StockReceipt):
        weighing_ids=m.StockReceiptLine.objects.filter(receipt=item,original_issue_line__weighing_line__isnull=False).values_list('original_issue_line__weighing_line__stage__order_id',flat=True)
    else:weighing_ids=[]
    from plugins.erp_production.models import WeighingOrder
    from plugins.erp_production.weighing_services import refresh
    for order in WeighingOrder.objects.filter(pk__in=weighing_ids).order_by('pk'):refresh(order,actor)
    from plugins.erp_sales import models as sales,fulfillment_services as fulfillment
    if isinstance(item,m.StockIssue):
        for delivery in sales.Delivery.objects.filter(warehouse_issue=item):fulfillment.refresh_delivery(delivery,actor)
    if isinstance(item,m.StockReceipt):
        for returned in sales.SalesReturn.objects.filter(pk__in=sales.SalesReturnLine.objects.filter(receipt_line__receipt=item).values('return_order_id')):fulfillment.refresh_return(returned,actor)
    model,key=LINES[type(item)]
    for package in m.Package.objects.filter(pk__in=model.objects.filter(**{key:item}).values('package_id')).order_by('pk'):
        before=snapshot(package)
        returned=m.StockReceiptLine.objects.filter(package=package,receipt__kind='sales_return',receipt__status='posted').exists()
        issued=m.StockIssueLine.objects.filter(package=package,issue__kind='delivery',issue__status='posted').exists()
        received=m.StockReceiptLine.objects.filter(package=package,receipt__kind='finished_output',receipt__status='posted').exists()
        package.status='returned' if returned else 'issued' if issued else 'received' if received else 'packed'
        if before['status']!=package.status:persist(package,actor);record(package,'refresh_stock',before,actor)


@transaction.atomic
def post(item, actor, at):
    lock_source_documents(item)
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
    model, key = LINES[type(item)]
    rows = require_rows(model.objects.filter(**{key: item}))
    lock_business_sources(item,rows)
    count = item.count if isinstance(item, m.StockAdjustment) else None
    lock_warehouses(warehouse_ids(item), count)
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
    require_state(disposition,['active'])
    target = {'release': 'released', 'concession': 'released', 'rework': 'held',
              'downgrade': 'released', 'scrap': 'scrap', 'hold': 'held'}[disposition.kind]
    if row.new_quality_state != target:
        raise ValidationError({'new_quality_state': '目标库存质量状态与处置结论不一致。'})
    inspection = disposition.inspection
    if inspection.is_void:raise ValidationError({'disposition':'该检验已取消采用。'})
    if row.adjustment.document_at<disposition.approved_at:raise ValidationError({'document_at':'质量调整不能早于实际数量处置。'})
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
def confirm_transformation(item,actor,at):
    item=locked(item)
    if item.is_confirmed or item.is_void:raise ValidationError({'transformation':'此谱系不能再次确认。'})
    if item.work_card_id is None or item.execution_id is None:raise ValidationError({'execution':'新转化须明确真实工卡及实际执行。'})
    item.execution=locked(item.execution)
    require_state(item.execution,['completed'])
    if item.execution.operation.work_card_id!=item.work_card_id:raise ValidationError({'execution':'执行与工卡不一致。'})
    rows=require_rows(m.LotTransformationLine.objects.filter(transformation=item))
    if {row.direction for row in rows}!={'input','output'}:raise ValidationError({'lines':'转化必须明确实际投入及产出批次。'})
    for row in rows:
        if row.direction=='input':
            if row.issue_line_id is None or row.receipt_line_id is not None:raise ValidationError({'issue_line':'投入只关联实际领用行。'})
            source=row.issue_line;require_state(source.issue,['posted'])
        else:
            if row.receipt_line_id is None or row.issue_line_id is not None:raise ValidationError({'receipt_line':'产出只关联实际产出收货行。'})
            source=row.receipt_line;require_state(source.receipt,['posted'])
            if source.source_execution_id!=item.execution_id:
                raise ValidationError({'execution':'谱系产出须对应本次真实执行的产出收货。'})
        if source.lot_id!=row.lot_id or source.work_card_id!=item.work_card_id or row.unit.convert_quantity(row.quantity,source.unit)!=source.quantity:
            raise ValidationError({'quantity':'谱系批次、工卡、数量单位必须完整对应实际收发行。'})
        document=source.issue if row.direction=='input' else source.receipt
        if at<document.posted_at:raise ValidationError({'at':'谱系确认不能早于所引用实际收发过账。'})
    if at < item.occurred_at:raise ValidationError({'at':'确认时间不能早于转化发生。'})
    before=snapshot(item);item.is_confirmed,item.confirmed_at=True,at;persist(item,actor);record(item,'confirm_lineage',before,actor)
    return item


@transaction.atomic
def void_transformation(item,actor,at,reason):
    item=locked(item)
    if item.is_void:raise ValidationError({'transformation':'此谱系已取消采用。'})
    if at<item.occurred_at or item.confirmed_at is not None and at<item.confirmed_at:raise ValidationError({'at':'取消不能早于谱系发生及确认时间。'})
    before=snapshot(item);item.is_void,item.voided_at,item.void_reason=True,at,reason;persist(item,actor);record(item,'void_lineage',before,actor,reason)
    return item


@transaction.atomic
def reverse(item, actor, at, reason):
    lock_source_documents(item)
    from plugins.erp_sales import models as sales
    from plugins.erp_quality.models import QualityInspection
    if isinstance(item,m.StockReceipt) and sales.SalesReturnLine.objects.filter(receipt_line__receipt=item,return_order__status='closed').exists():raise ValidationError({'return_order':'先重新办理已结案的客户退回，再更正实际收回。'})
    if isinstance(item,m.StockIssue) and sales.Delivery.objects.filter(warehouse_issue=item,status='delivered').exists():raise ValidationError({'delivery':'请先更正原客户交付事实，再冲销其出库。'})
    if isinstance(item,m.StockReceipt) and QualityInspection.objects.filter(receipt_line__receipt=item,is_void=False).exclude(result='pending').exists():raise ValidationError({'inspection':'请先取消对应来料或退回检验的采用。'})
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
    model, key = LINES[type(item)]
    lock_business_sources(item,list(model.objects.filter(**{key:item})))
    lock_warehouses(warehouse_ids(item))
    source = {m.StockReceipt: 'receipt_line', m.StockIssue: 'issue_line',
              m.StockTransfer: 'transfer_line', m.StockAdjustment: 'adjustment_line'}[type(item)]
    rows = list(m.InventoryMovement.objects.filter(**{source+'__'+key: item}, reverses__isnull=True).order_by('-pk'))
    if isinstance(item,(m.StockReceipt,m.StockIssue)):
        reference='receipt_line__receipt' if isinstance(item,m.StockReceipt) else 'issue_line__issue'
        if m.LotTransformationLine.objects.filter(**{reference:item},transformation__is_confirmed=True,transformation__is_void=False).exists():raise ValidationError({'transformation':'请先取消引用本实际收发的谱系采用，保留原谱系历史。'})
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
