"""报价、订单及变更的明确业务规则。"""
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from plugins.erp_base.business import (locked, persist, record, snapshot, require_state,
                                      require_rows, validate_effective)
from . import models as m

PARENTS = {m.CommercialPriceLine: ('price_document', ''), m.SalesOrderLine: ('order', ''),
           m.SalesLineRequirement: ('order_line', 'order'), m.SalesOrderChangeLine: ('change', '')}
PARENTS.update({m.DeliveryLine:('delivery',''),m.SalesReturnLine:('return_order',''),m.CustomerComplaintLine:('complaint','')})
OWNED = {m.CommercialPrice: {'status'}, m.CommercialPriceLine: {'is_confirmed'},
         m.SalesOrder: {'status', 'confirmed_by', 'confirmed_at', 'closed_at'},
         m.SalesOrderLine: {'adopted_price_snapshot', 'is_closed'}, m.SalesLineRequirement: set(),
         m.SalesOrderChange: {'status', 'confirmed_by', 'confirmed_at'},
         m.SalesOrderChangeLine: {'before_values'}}
OWNED.update({m.Delivery:{'status','delivered_at'},m.DeliveryLine:{'price_adoption_snapshot'},
    m.SalesReturn:{'status'},m.SalesReturnLine:set(),m.CustomerComplaint:{'status'},m.CustomerComplaintLine:set()})


def editable(item):
    if type(item) in PARENTS:
        key, path = PARENTS[type(item)]
        item = getattr(item, key)
        for part in path.split('.') if path else []:
            item = getattr(item, part)
    require_state(item,['open','handling'] if isinstance(item,m.CustomerComplaint) else ['draft'])


def validate(item):
    if isinstance(item,m.DeliveryLine):
        from .fulfillment_services import validate_line
        validate_line(item)
    if isinstance(item, m.CommercialPriceLine):
        if item.valid_from is not None and item.valid_to is not None and item.valid_to <= item.valid_from:
            raise ValidationError({'valid_to': '失效时间必须晚于生效时间。'})
    if isinstance(item, m.SalesOrder):
        if item.delivery_address_id is not None and item.delivery_address.party_id != item.customer_id:
            raise ValidationError({'delivery_address': '送货地址必须属于订单客户。'})
    if isinstance(item, m.SalesOrderLine):
        if item.customer_material_id is not None and (item.customer_material.customer_id, item.customer_material.material_id) != (item.order.customer_id, item.material_id):
            raise ValidationError({'customer_material': '客户物料必须与订单客户和本厂物料一致。'})
        if item.price_source_id is not None:
            source = locked(item.price_source)
            if source.price_document.status != 'confirmed' or source.is_confirmed is not True:
                raise ValidationError({'price_source': '只能采用已确认的价格明细。'})
            if source.price_document.customer_id != item.order.customer_id or source.material_id != item.material_id:
                raise ValidationError({'price_source': '来源价格必须属于同一客户和物料。'})
            if source.color_standard_id is not None and source.color_standard_id != item.color_standard_id:
                raise ValidationError({'price_source': '来源价格的色标准不匹配。'})
            validate_effective(source, item.order.document_at)
            item.adopted_price_snapshot, item.price_unit = source.unit_price, source.unit
        else:
            item.adopted_price_snapshot = None
        if item.approved_recipe_id is not None:
            recipe = item.approved_recipe
            if recipe.status not in ['approved', 'active']:
                raise ValidationError({'approved_recipe': '只能选择已审核的配方版本。'})
            if recipe.recipe.customer_id is not None and recipe.recipe.customer_id != item.order.customer_id:
                raise ValidationError({'approved_recipe': '配方适用客户不匹配。'})
            if recipe.recipe.material_id is not None and recipe.recipe.material_id != item.material_id:
                raise ValidationError({'approved_recipe': '配方适用物料不匹配。'})


POLICY = {'parents': PARENTS, 'owned': OWNED, 'editable': editable, 'validate': validate,
          'parent_editable': lambda model, item: editable(item), 'lock_root': locked, 'deletable': editable}


@transaction.atomic
def confirm_price(item, actor):
    item = locked(item)
    require_state(item, ['draft'])
    before = snapshot(item)
    for line in require_rows(m.CommercialPriceLine.objects.filter(price_document=item)):
        validate(line)
        line.is_confirmed = True
        persist(line, actor)
    item.status = 'confirmed'
    persist(item, actor)
    record(item, 'confirm', before, actor)
    return item


@transaction.atomic
def confirm_order(item, actor, employee):
    item = locked(item)
    require_state(item, ['draft'])
    before = snapshot(item)
    validate(item)
    for line in require_rows(m.SalesOrderLine.objects.filter(order=item)):
        validate(line)
        if line.price_source_id is None and (line.unit_price is None or line.price_unit_id is None or not line.manual_price_reason.strip()):
            raise ValidationError({'price_source': '未采用价格资料时，请填写单价、计价单位和手工定价原因。'})
        if line.default_route_id is not None:
            require_state(line.default_route, ['active'])
            validate_effective(line.default_route, item.document_at)
        persist(line, actor)
        require_rows(m.SalesLineRequirement.objects.filter(order_line=line)) if m.SalesLineRequirement.objects.filter(order_line=line).exists() else None
    item.status, item.confirmed_by, item.confirmed_at = 'confirmed', employee, timezone.now()
    persist(item, actor)
    record(item, 'confirm', before, actor)
    return item


@transaction.atomic
def confirm_change(item, actor, employee):
    item = locked(item)
    require_state(item, ['draft'])
    order = locked(item.order)
    require_state(order, ['confirmed', 'running'])
    before = snapshot(item)
    from plugins.erp_production.models import WorkCardOrderAllocation
    for line in require_rows(m.SalesOrderChangeLine.objects.filter(change=item)):
        source = locked(line.order_line)
        line.before_values = snapshot(source)
        if line.new_quantity is not None:
            allocated = sum((row.unit.convert_quantity(row.allocated_quantity, source.ordered_unit)
                for row in WorkCardOrderAllocation.objects.filter(order_line=source,original_allocation__isnull=True).exclude(work_card__status='cancelled')), Decimal('0'))
            if line.new_quantity <= 0 or line.new_quantity < allocated:
                raise ValidationError({'new_quantity': '新订货数量必须大于零且不小于现有有效工卡分配量。'})
            source.ordered_quantity = line.new_quantity
        if line.new_due_at is not None:
            source.final_due_at = line.new_due_at
        if line.new_requirements != '':
            source.special_requirements = line.new_requirements
        persist(source, actor)
        persist(line, actor)
        record(source, 'order_change', line.before_values, actor, item.reason)
    item.status, item.confirmed_by, item.confirmed_at = 'confirmed', employee, timezone.now()
    persist(item, actor)
    record(item, 'confirm', before, actor, item.reason)
    return item


@transaction.atomic
def finish_order(item,actor,at,reason,close=False):
    item=locked(item);require_state(item,['confirmed','running','completed'] if close else ['confirmed','running'])
    if at<item.confirmed_at:raise ValidationError({'at':'完成或结案不能早于订单确认。'})
    lines=require_rows(m.SalesOrderLine.objects.filter(order=item))
    if m.DeliveryLine.objects.filter(order_line__order=item,delivery__status__in=['draft','confirmed','issued']).exists():
        raise ValidationError({'delivery':'还有未完成或未取消的交付单。'})
    if m.SalesReturnLine.objects.filter(original_delivery_line__order_line__order=item,return_order__status__in=['draft','confirmed','received']).exists():
        raise ValidationError({'return_order':'还有未结束的客户退货。'})
    from .fulfillment_services import reopened_quantity
    for line in lines:
        deliveries=m.DeliveryLine.objects.filter(order_line=line,delivery__status='delivered',delivery__warehouse_issue__status='posted')
        actual=sum((row.unit.convert_quantity(row.quantity,line.ordered_unit) for row in deliveries),Decimal('0'))
        if not close and actual<line.ordered_quantity+reopened_quantity(line):raise ValidationError({'quantity':'订单完成须有足量的客户实际交付；提前终止采用有原因的结案。'})
        if any(at<row.delivery.delivered_at for row in deliveries):raise ValidationError({'at':'完成或结案不能早于客户实际交付。'})
        if close:line.is_closed=True;persist(line,actor)
    from plugins.erp_production.models import WorkCardOrderAllocation
    if WorkCardOrderAllocation.objects.filter(order_line__order=item).exclude(work_card__status__in=['completed','closed','cancelled']).exists():
        raise ValidationError({'work_card':'还有有效的未完成工卡需求。'})
    before=snapshot(item);item.status='closed' if close else 'completed'
    if close:item.closed_at=at
    persist(item,actor);record(item,'close' if close else 'complete',before,actor,reason)
    return item


@transaction.atomic
def reopen_order(item,actor,reason):
    item=locked(item);require_state(item,['completed','closed'])
    before=snapshot(item);item.status,item.closed_at='running',None
    for line in m.SalesOrderLine.objects.filter(order=item):line.is_closed=False;persist(line,actor)
    persist(item,actor);record(item,'reopen',before,actor,reason)
    return item
