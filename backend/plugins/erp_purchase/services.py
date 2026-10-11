from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from plugins.erp_base.business import locked, persist, record, snapshot, require_state, require_rows
from . import models as m

PARENTS = {m.PurchaseRequestLine: ('request', ''), m.PurchaseOrderLine: ('order', ''),
           m.PurchaseReturnLine: ('return_order', '')}
OWNED = {m.PurchaseRequest: {'status', 'confirmed_by', 'confirmed_at'},
         m.PurchaseRequestLine: {'work_card'}, m.PurchaseOrder: {'status'},
         m.PurchaseOrderLine: set(), m.PurchaseReturn: {'status'}, m.PurchaseReturnLine: set()}


def editable(item):
    if type(item) in PARENTS:
        item = getattr(item, PARENTS[type(item)][0])
    require_state(item, ['draft'])


def validate(item):
    if isinstance(item, m.PurchaseOrderLine) and item.request_line_id is not None:
        source = item.request_line
        require_state(source.request, ['confirmed'])
        if source.material_id != item.material_id:
            raise ValidationError({'request_line': '申请物料与采购物料不一致。'})
        source.unit.convert_quantity(source.quantity, item.unit)
    if isinstance(item, m.PurchaseReturnLine):
        original = item.original_receipt_line
        if original.receipt.kind != 'purchase' or original.receipt.source_party_id != item.return_order.supplier_id:
            raise ValidationError({'original_receipt_line': '退货必须来自本供应商的采购收货。'})
        require_state(original.receipt, ['posted'])
        item.unit.convert_quantity(item.quantity, original.unit)


POLICY = {'parents': PARENTS, 'owned': OWNED, 'editable': editable, 'validate': validate,
          'parent_editable': lambda model, item: editable(item), 'lock_root': locked, 'deletable': editable}


@transaction.atomic
def confirm(item, actor, employee=None):
    item = locked(item)
    require_state(item, ['draft'])
    before = snapshot(item)
    model, field = {m.PurchaseRequest: (m.PurchaseRequestLine, 'request'),
                    m.PurchaseOrder: (m.PurchaseOrderLine, 'order'),
                    m.PurchaseReturn: (m.PurchaseReturnLine, 'return_order')}[type(item)]
    for line in require_rows(model.objects.filter(**{field: item})):
        validate(line)
    if isinstance(item, m.PurchaseRequest):
        item.confirmed_by, item.confirmed_at = employee, timezone.now()
    if isinstance(item, m.PurchaseReturn):
        from plugins.erp_warehouse.models import StockIssue, StockIssueLine
        if item.warehouse_issue_id is None:
            raise ValidationError({'warehouse_issue': '请关联本次采购退货的实际出库单。'})
        issue = locked(item.warehouse_issue)
        require_state(issue, ['draft', 'confirmed'])
        if issue.kind != 'purchase_return' or issue.destination_party_id != item.supplier_id:
            raise ValidationError({'warehouse_issue': '出库单类型或供应商不匹配。'})
        expected = {}
        for line in model.objects.filter(return_order=item):
            key = line.original_receipt_line_id
            expected[key] = expected.get(key, Decimal('0')) + line.unit.convert_quantity(line.quantity, line.original_receipt_line.unit)
        actual = {}
        for line in StockIssueLine.objects.filter(issue=issue):
            if line.original_receipt_line_id is None:
                raise ValidationError({'warehouse_issue': '退货出库必须逐行指定原收货行。'})
            key = line.original_receipt_line_id
            actual[key] = actual.get(key, Decimal('0')) + line.quantity
        if expected != actual:
            raise ValidationError({'warehouse_issue': '实际退货出库的原收货行及数量必须与申请一致。'})
    item.status = 'confirmed'
    persist(item, actor)
    record(item, 'confirm', before, actor)
    return item


def received_quantity(line):
    from plugins.erp_warehouse.models import StockReceiptLine, StockIssueLine
    received = sum((row.unit.convert_quantity(row.quantity, line.unit)
        for row in StockReceiptLine.objects.filter(purchase_order_line=line, receipt__status='posted')), Decimal('0'))
    returned = sum((row.unit.convert_quantity(row.quantity, line.unit)
        for row in StockIssueLine.objects.filter(original_receipt_line__purchase_order_line=line,
                    issue__kind='purchase_return', issue__status='posted')), Decimal('0'))
    return received - returned


def refresh_order(order, actor):
    order = locked(order)
    if order.status in ['closed', 'cancelled', 'draft']:
        return order
    totals = [(received_quantity(line), line.quantity) for line in m.PurchaseOrderLine.objects.filter(order=order)]
    order.status = 'received' if all(actual >= planned for actual, planned in totals) else 'partial_received' if any(actual > 0 for actual, planned in totals) else 'confirmed'
    return persist(order, actor)
