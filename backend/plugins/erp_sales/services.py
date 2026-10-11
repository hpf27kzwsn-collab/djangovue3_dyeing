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
OWNED = {m.CommercialPrice: {'status'}, m.CommercialPriceLine: {'is_confirmed'},
         m.SalesOrder: {'status', 'confirmed_by', 'confirmed_at', 'closed_at'},
         m.SalesOrderLine: {'adopted_price_snapshot', 'is_closed'}, m.SalesLineRequirement: set(),
         m.SalesOrderChange: {'status', 'confirmed_by', 'confirmed_at'},
         m.SalesOrderChangeLine: {'before_values'}}


def editable(item):
    if type(item) in PARENTS:
        key, path = PARENTS[type(item)]
        item = getattr(item, key)
        for part in path.split('.') if path else []:
            item = getattr(item, part)
    require_state(item, ['draft'])


def validate(item):
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
                for row in WorkCardOrderAllocation.objects.filter(order_line=source).exclude(work_card__status='cancelled')), Decimal('0'))
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
