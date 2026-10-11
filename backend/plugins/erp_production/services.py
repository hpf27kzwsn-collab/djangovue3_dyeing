"""工卡、组缸、人工排程和配方采用；数量与时间均保存明确来源。"""
from decimal import Decimal, ROUND_HALF_UP
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Max
from plugins.erp_base import models as base
from plugins.erp_sales import models as sales
from plugins.erp_sampling import models as sampling
from plugins.erp_base.business import locked, persist, snapshot, record, require_state, require_rows, validate_effective
from .calculations import calculate_adopted_dosage, planned_chemical_mass_kg
from . import models as m

PARENTS = {m.WorkCardOrderAllocation: ('work_card', ''), m.WorkCardOperation: ('work_card', ''),
    m.OperationParameter: ('operation', 'work_card'), m.WorkCardRequirement: ('work_card', ''),
    m.DyeBatchWorkCard: ('batch', ''), m.DyeBatchAllocation: ('batch_work_card', 'batch')}
READONLY = {m.ScheduleAssignment, m.ProductionRecipe, m.MaterialPlanStage, m.MaterialPlanLine}
OWNED = {m.WorkCard: {'status', 'released_at', 'completed_at', 'closed_at'},
    m.WorkCardOrderAllocation: {'adopted_order_snapshot'}, m.DyeBatch: {'status'}, m.DyeBatchWorkCard: set(),
    m.DyeBatchAllocation: set(), m.WorkCardOperation: {'process', 'sequence', 'route_step', 'is_required', 'planned_minutes', 'predecessor'},
    m.OperationParameter: set(), m.WorkCardRequirement: {'source_order_requirement'}}
for model in READONLY:
    OWNED[model] = {f.name for f in model._meta.fields}


def editable(item):
    if type(item) in READONLY or isinstance(item, m.WorkCardOperation):
        raise ValidationError({'id': '此对象由生产业务操作维护。'})
    if type(item) in PARENTS:
        key, path = PARENTS[type(item)]
        item = getattr(item, key)
        for part in path.split('.') if path else []:
            item = getattr(item, part)
    if isinstance(item, m.WorkCard):
        require_state(item, ['draft'])
    else:
        require_state(item, ['planned'])
        if m.ProductionRecipe.objects.filter(batch=item, status='active').exists() or m.ScheduleAssignment.objects.filter(batch=item, status__in=['planned', 'released']).exists():
            raise ValidationError({'batch': '已采用配方或排程的缸批成员已冻结。'})


def parent_editable(model, item):
    if model is m.WorkCardOperation:
        raise ValidationError({'operation': '计划工序由展开路线维护。'})
    editable(item)


def converted_sum(rows, quantity, unit, target):
    return sum((getattr(row, unit).convert_quantity(getattr(row, quantity), target) for row in rows), Decimal('0'))


def validate(item):
    if type(item) in READONLY or isinstance(item, m.WorkCardOperation):
        raise ValidationError({'id': '此对象由生产业务操作创建。'})
    if isinstance(item, m.WorkCard):
        require_state(item.route_version, ['active'])
        validate_effective(item.route_version, item.document_at)
        if item.color_standard_id is not None and item.color_standard.material_id not in [None, item.material_id]:
            raise ValidationError({'color_standard': '色标准物料与工卡不一致。'})
        if item.pk is not None:
            for allocation in m.WorkCardOrderAllocation.objects.filter(work_card=item):
                check_order_allocation(allocation, work_card=item)
    if isinstance(item, m.DyeBatch) and item.planned_mass_kg is not None and item.planned_mass_kg <= 0:
        raise ValidationError({'planned_mass_kg': '已明确的计划kg必须为正数。'})
    if isinstance(item, m.WorkCardOrderAllocation):
        check_order_allocation(item)
    if isinstance(item, m.DyeBatchWorkCard):
        card = locked(item.work_card)
        require_state(card, ['released'])
        if card.factory_id != item.batch.factory_id:
            raise ValidationError({'work_card': '组缸工卡必须明确采用本缸批工厂。'})
        peers = m.DyeBatchWorkCard.objects.filter(batch=item.batch).exclude(pk=item.pk)
        for peer in peers:
            other = peer.work_card
            if (card.material_id, card.color_standard_id, card.route_version_id) != (other.material_id, other.color_standard_id, other.route_version_id):
                raise ValidationError({'work_card': '本版合缸采用相同物料、色标准和路线版本。'})
        used = converted_sum(m.DyeBatchWorkCard.objects.filter(work_card=card).exclude(batch__status='cancelled').exclude(pk=item.pk), 'quantity', 'unit', card.quantity_unit)
        if used + item.unit.convert_quantity(item.quantity, card.quantity_unit) > card.planned_quantity:
            raise ValidationError({'quantity': '各有效缸批分配合计不能超过工卡计划量。'})
    if isinstance(item, m.DyeBatchAllocation):
        source = locked(item.work_card_allocation)
        member = item.batch_work_card
        used = converted_sum(m.DyeBatchAllocation.objects.filter(work_card_allocation=source).exclude(batch_work_card__batch__status='cancelled').exclude(pk=item.pk), 'quantity', 'unit', source.unit)
        if used + item.unit.convert_quantity(item.quantity, source.unit) > source.allocated_quantity:
            raise ValidationError({'quantity': '有效缸批分配不能超过原工卡订单分配。'})
        member_used = converted_sum(m.DyeBatchAllocation.objects.filter(batch_work_card=member).exclude(pk=item.pk), 'quantity', 'unit', member.unit)
        if member_used + item.unit.convert_quantity(item.quantity, member.unit) > member.quantity:
            raise ValidationError({'quantity': '订单分配合计不能超过本缸工卡量。'})


def check_order_allocation(item, work_card=None):
    card = item.work_card if work_card is None else work_card
    source_order = locked(item.order_line.order)
    source = locked(item.order_line)
    require_state(source_order, ['confirmed', 'running'])
    if source.is_closed is True:
        raise ValidationError({'order_line': '订单行已经结束。'})
    if source.material_id != card.material_id or source.color_standard_id != card.color_standard_id:
        raise ValidationError({'order_line': '订单行物料与色标准必须和工卡一致。'})
    used = converted_sum(m.WorkCardOrderAllocation.objects.filter(order_line=source).exclude(work_card__status='cancelled').exclude(pk=item.pk), 'allocated_quantity', 'unit', source.ordered_unit)
    if used + item.unit.convert_quantity(item.allocated_quantity, source.ordered_unit) > source.ordered_quantity:
        raise ValidationError({'allocated_quantity': '各有效工卡分配不能超过订单需求。'})
    total = converted_sum(m.WorkCardOrderAllocation.objects.filter(work_card=card).exclude(pk=item.pk), 'allocated_quantity', 'unit', card.quantity_unit)
    if total + item.unit.convert_quantity(item.allocated_quantity, card.quantity_unit) > card.planned_quantity:
        raise ValidationError({'allocated_quantity': '订单分配不能超过工卡计划量。'})


POLICY = {'parents': PARENTS, 'owned': OWNED, 'editable': editable, 'parent_editable': parent_editable,
          'lock_root': locked, 'deletable': editable, 'validate': validate}


@transaction.atomic
def prepare(item, actor, steps):
    item = locked(item)
    require_state(item, ['draft'])
    route = locked(item.route_version)
    require_state(route, ['active'])
    validate_effective(route, item.document_at)
    selected = {step.pk for step in steps}
    all_steps = list(base.RouteStep.objects.filter(route_version=route).order_by('sequence'))
    if len(selected) != len(steps) or selected - {step.pk for step in all_steps}:
        raise ValidationError({'steps': '所选节点必须唯一且属于本路线版本。'})
    if not selected or any(step.is_required and step.pk not in selected for step in all_steps):
        raise ValidationError({'steps': '必须包含本路线的所有必经节点。'})
    if m.OperationExecution.objects.filter(operation__work_card=item).exists():
        raise ValidationError({'steps': '已有执行事实，不能重新展开计划。'})
    before = snapshot(item)
    before['operations'] = [snapshot(row) for row in m.WorkCardOperation.objects.filter(work_card=item)]
    m.WorkCardOperation.objects.filter(work_card=item).delete()
    operations = {}
    by_id = {step.pk: step for step in all_steps}
    for step in all_steps:
        if step.pk not in selected:
            continue
        predecessor = step.predecessor_id
        while predecessor is not None and predecessor not in selected:
            predecessor = by_id[predecessor].predecessor_id
        operations[step.pk] = persist(m.WorkCardOperation(work_card=item, route_step=step,
            sequence=step.sequence, process=step.process, work_center=step.process.work_center,
            is_required=step.is_required, planned_minutes=step.standard_minutes,
            predecessor=operations[predecessor] if predecessor is not None else None,
            dept_belong_id=item.dept_belong_id), actor)
    requirements = {}
    for allocation in m.WorkCardOrderAllocation.objects.filter(work_card=item).order_by('pk'):
        check_order_allocation(allocation)
        for requirement in sales.SalesLineRequirement.objects.filter(order_line=allocation.order_line):
            key = (requirement.namespace, requirement.requirement_code)
            if key in requirements and requirements[key].value_text != requirement.value_text:
                raise ValidationError({'requirements': '合卡订单存在冲突要求，请先更正订单要求或分别建卡。'})
            requirements[key] = requirement
    m.WorkCardRequirement.objects.filter(work_card=item, source_order_requirement__isnull=False).delete()
    for key, source in requirements.items():
        existing = m.WorkCardRequirement.objects.filter(work_card=item, namespace=key[0], code=key[1]).first()
        if existing is not None:
            if existing.value_text != source.value_text:
                raise ValidationError({'requirements': '人工工卡要求与订单快照冲突。'})
            continue
        persist(m.WorkCardRequirement(work_card=item, source_order_requirement=source, namespace=key[0], code=key[1],
            name_snapshot=source.name, value_text=source.value_text, dept_belong_id=item.dept_belong_id), actor)
    record(item, 'prepare', before, actor)
    return item


@transaction.atomic
def release(item, actor, at):
    item = locked(item)
    require_state(item, ['draft'])
    validate(item)
    operations = require_rows(m.WorkCardOperation.objects.filter(work_card=item))
    required = set(base.RouteStep.objects.filter(route_version=item.route_version, is_required=True).values_list('pk', flat=True))
    if required - {row.route_step_id for row in operations}:
        raise ValidationError({'operations': '请先展开当前路线的必经节点。'})
    allocations = list(m.WorkCardOrderAllocation.objects.filter(work_card=item))
    if not allocations and not item.manual_creation_reason.strip():
        raise ValidationError({'manual_creation_reason': '无订单工卡必须明确填写建卡依据。'})
    total = converted_sum(allocations, 'allocated_quantity', 'unit', item.quantity_unit)
    if allocations and total != item.planned_quantity:
        raise ValidationError({'planned_quantity': '下达时订单分配合计必须等于本工卡计划量。'})
    if at < item.document_at:
        raise ValidationError({'at': '下达时间不能早于工卡日期。'})
    before = snapshot(item)
    for allocation in allocations:
        previous = snapshot(allocation)
        allocation.adopted_order_snapshot = snapshot(allocation.order_line)
        allocation.adopted_order_snapshot['requirements'] = [snapshot(row) for row in sales.SalesLineRequirement.objects.filter(order_line=allocation.order_line)]
        persist(allocation, actor)
        record(allocation, 'adopt_order', previous, actor)
    item.status, item.released_at = 'released', at
    persist(item, actor)
    record(item, 'release', before, actor)
    return item


def batch_members(batch):
    members = require_rows(m.DyeBatchWorkCard.objects.filter(batch=batch))
    for member in members:
        card = member.work_card
        require_state(card, ['released', 'running'])
        allocations = list(m.DyeBatchAllocation.objects.filter(batch_work_card=member))
        if m.WorkCardOrderAllocation.objects.filter(work_card=card).exists() and converted_sum(allocations, 'quantity', 'unit', member.unit) != member.quantity:
            raise ValidationError({'batch': '本缸成员的订单分配合计必须等于本缸工卡量。'})
    return members


@transaction.atomic
def schedule(item, actor, machine, planned_start, planned_end, batch=None):
    if batch is not None:
        batch = locked(batch)
    card = locked(item.work_card)
    require_state(card, ['released', 'running'])
    if card.is_paused:
        raise ValidationError({'work_card': '工卡已暂停。'})
    item = locked(item)
    if batch is not None:
        require_state(batch, ['planned', 'scheduled'])
        members = batch_members(batch)
        if card.pk not in [member.work_card_id for member in members]:
            raise ValidationError({'batch': '缸批不包含当前工卡。'})
        for member in members:
            if not m.WorkCardOperation.objects.filter(work_card=member.work_card, process=item.process).exists():
                raise ValidationError({'batch': '同缸成员必须包含本次排程工序。'})
        if m.ScheduleAssignment.objects.filter(batch=batch, operation__process=item.process, status__in=['planned', 'released']).exists():
            raise ValidationError({'batch': '此缸批工序已有统一物理安排，请从原安排改排。'})
    machine = locked(machine)
    check_slot(item, machine, planned_start, planned_end, batch)
    if m.ScheduleAssignment.objects.filter(operation=item, status__in=['planned', 'released']).exists():
        raise ValidationError({'operation': '该工卡节点已有有效安排。'})
    maximum = m.ScheduleAssignment.objects.filter(operation=item).aggregate(value=Max('version'))['value']
    slot = persist(m.ScheduleAssignment(operation=item, batch=batch, machine=machine,
        planned_start=planned_start, planned_end=planned_end, version=1 if maximum is None else maximum + 1,
        dept_belong_id=card.dept_belong_id), actor)
    if batch is not None:
        before = snapshot(batch)
        batch.status = 'scheduled'
        persist(batch, actor)
        record(batch, 'schedule', before, actor)
    record(slot, 'schedule', {'exists': False}, actor)
    return item


def check_slot(operation, machine, start, end, batch, exclude=None):
    card = operation.work_card
    if end <= start:
        raise ValidationError({'planned_end': '结束时间必须晚于开始时间。'})
    if start < card.released_at:
        raise ValidationError({'planned_start': '排程不能早于工卡下达。'})
    if machine.is_active is not True or machine.factory_id != card.factory_id:
        raise ValidationError({'machine': '采用机台必须明确启用且属于工卡工厂。'})
    if not base.MachineProcess.objects.filter(machine=machine, process=operation.process, is_active=True).exists():
        raise ValidationError({'machine': '机台未登记此工序适用关系。'})
    if operation.work_center_id is not None and machine.work_center_id != operation.work_center_id:
        raise ValidationError({'machine': '机台不属于本计划工作中心。'})
    if batch is not None:
        mass = batch.planned_mass_kg
        if mass is not None and machine.load_capacity_kg is not None and mass > machine.load_capacity_kg:
            raise ValidationError({'batch': '计划染色重量超过已明确的机台kg承载量。'})
    if m.ScheduleAssignment.objects.filter(machine=machine, status__in=['planned', 'released'],
        planned_start__lt=end, planned_end__gt=start).exclude(pk=exclude).exists():
        raise ValidationError({'planned_start': '此机台时段已被有效安排占用。'})
    if m.OperationExecution.objects.filter(operation=operation, status__in=['running', 'completed']).exists():
        raise ValidationError({'operation': '此节点已有实际执行，不能新增或改排。'})


@transaction.atomic
def reschedule(item, actor, machine, planned_start, planned_end, reason):
    batch = locked(item.batch) if item.batch_id is not None else None
    locked(item.operation.work_card)
    machines = {row.pk: row for row in base.Machine.objects.select_for_update().filter(pk__in=[item.machine_id, machine.pk]).order_by('pk')}
    item = locked(item)
    require_state(item, ['planned', 'released'])
    check_slot(item.operation, machines[machine.pk], planned_start, planned_end, batch, exclude=item.pk)
    before = snapshot(item)
    old_status = item.status
    item.status, item.change_reason = 'replaced', reason
    persist(item, actor)
    maximum = m.ScheduleAssignment.objects.filter(operation=item.operation).aggregate(value=Max('version'))['value']
    result = persist(m.ScheduleAssignment(operation=item.operation, batch=batch, machine=machines[machine.pk],
        planned_start=planned_start, planned_end=planned_end, version=maximum + 1, status=old_status,
        previous_assignment=item, change_reason=reason, dept_belong_id=item.dept_belong_id), actor)
    record(item, 'replace', before, actor, reason)
    record(result, 'schedule', {'exists': False}, actor, reason)
    return result


@transaction.atomic
def publish(item, actor):
    locked(item.operation.work_card)
    item = locked(item)
    require_state(item, ['planned'])
    before = snapshot(item)
    item.status = 'released'
    persist(item, actor)
    record(item, 'publish', before, actor)
    return item


@transaction.atomic
def cancel_schedule(item, actor, reason):
    batch = locked(item.batch) if item.batch_id is not None else None
    locked(item.operation.work_card)
    item = locked(item)
    require_state(item, ['planned', 'released'])
    if m.OperationExecution.objects.filter(operation=item.operation, status__in=['running', 'completed']).exists():
        raise ValidationError({'operation': '已有执行不能取消安排。'})
    before = snapshot(item)
    item.status, item.change_reason = 'cancelled', reason
    persist(item, actor)
    record(item, 'cancel', before, actor, reason)
    if batch is not None and not m.ScheduleAssignment.objects.filter(batch=batch, status__in=['planned', 'released']).exists():
        previous = snapshot(batch)
        batch.status = 'planned'
        persist(batch, actor)
        record(batch, 'unschedule', previous, actor, reason)
    return item


@transaction.atomic
def cancel(item, actor, reason):
    item = locked(item)
    require_state(item, ['draft', 'released'] if isinstance(item, m.WorkCard) else ['planned', 'scheduled'])
    if isinstance(item, m.WorkCard):
        if m.DyeBatchWorkCard.objects.filter(work_card=item).exclude(batch__status='cancelled').exists():
            raise ValidationError({'batch': '请先取消所属有效缸批，再取消工卡。'})
        if m.OperationExecution.objects.filter(operation__work_card=item).exists():
            raise ValidationError({'execution': '已有执行事实不能取消工卡。'})
        slots = m.ScheduleAssignment.objects.filter(operation__work_card=item, status__in=['planned', 'released'])
    else:
        if m.OperationExecution.objects.filter(batch=item).exists():
            raise ValidationError({'execution': '已有执行事实不能取消缸批。'})
        slots = m.ScheduleAssignment.objects.filter(batch=item, status__in=['planned', 'released'])
        for adoption in m.ProductionRecipe.objects.select_for_update().filter(batch=item, status='active'):
            before = snapshot(adoption)
            adoption.status = 'cancelled'
            persist(adoption, actor)
            record(adoption, 'cancel', before, actor, reason)
    for slot in slots.select_for_update().order_by('pk'):
        before = snapshot(slot)
        slot.status, slot.change_reason = 'cancelled', reason
        persist(slot, actor)
        record(slot, 'cancel', before, actor, reason)
    before = snapshot(item)
    item.status = 'cancelled'
    persist(item, actor)
    record(item, 'cancel', before, actor, reason)
    return item


@transaction.atomic
def adopt_recipe(item, actor, recipe_version, at, dry_mass_kg, stages):
    item = locked(item)
    require_state(item, ['planned', 'scheduled'])
    members = batch_members(item)
    version = locked(recipe_version)
    require_state(version, ['approved', 'active'])
    if not version.recipe.is_active or (version.valid_from is not None and at < version.valid_from):
        raise ValidationError({'recipe_version': '配方尚未生效或已停用。'})
    if dry_mass_kg <= 0:
        raise ValidationError({'dry_mass_kg': '采用计算必须明确正数干料kg。'})
    for member in members:
        card = member.work_card
        if version.recipe.material_id not in [None, card.material_id] or version.recipe.color_standard_id not in [None, card.color_standard_id]:
            raise ValidationError({'recipe_version': '配方物料或色标准与缸批工卡不一致。'})
        if version.recipe.customer_id is not None and (not m.WorkCardOrderAllocation.objects.filter(work_card=card).exists() or m.WorkCardOrderAllocation.objects.filter(work_card=card).exclude(order_line__order__customer_id=version.recipe.customer_id).exists()):
            raise ValidationError({'recipe_version': '客户专用配方必须适用于所有合缸订单。'})
    source_stages = require_rows(sampling.RecipeStage.objects.filter(version=version))
    inputs = {row['stage'].pk: row for row in stages}
    if len(inputs) != len(stages) or set(inputs) != {row.pk for row in source_stages}:
        raise ValidationError({'stages': '每个配方阶段必须且只能提供一次采用数据。'})
    kg = base.Unit.objects.get(code='kg')
    litre = base.Unit.objects.get(code='L')
    if kg.dimension != 'mass' or kg.factor_to_base != 1 or kg.base_unit_id is not None or litre.dimension != 'volume' or litre.factor_to_base != 1 or litre.base_unit_id is not None:
        raise ValidationError({'unit': '计算基准kg、L必须配置为对应物理基准单位。'})
    for previous in m.ProductionRecipe.objects.select_for_update().filter(batch=item, status='active'):
        if m.WeighingOrder.objects.filter(production_recipe=previous).exists():
            raise ValidationError({'recipe_version': '旧采用已生成料单，不能覆盖；加料或后处理使用独立料单。'})
        before = snapshot(previous)
        previous.status = 'replaced'
        persist(previous, actor)
        record(previous, 'replace', before, actor)
    maximum = m.ProductionRecipe.objects.filter(batch=item).aggregate(value=Max('adoption_number'))['value']
    adoption = persist(m.ProductionRecipe(batch=item, recipe_version=version, adopted_at=at, dry_mass_kg=dry_mass_kg,
        adoption_number=1 if maximum is None else maximum + 1, dept_belong_id=item.dept_belong_id), actor)
    for source in source_stages:
        data = inputs[source.pk]
        amount, unit = data['water_amount'], data['water_unit']
        density = data['density']
        if amount is None and source.bath_ratio is not None and source.bath_ratio_basis in ['mass_per_mass', 'volume_per_mass']:
            amount = dry_mass_kg * source.bath_ratio
            unit = kg if source.bath_ratio_basis == 'mass_per_mass' else litre
        if (amount is None) != (unit is None):
            raise ValidationError({'water_amount': '浴液数量与单位必须同时明确或同时留空。'})
        if amount is not None and amount <= 0:
            raise ValidationError({'water_amount': '采用浴液量必须为正数。'})
        if density is not None and density <= 0:
            raise ValidationError({'density': '密度必须为正数kg/L。'})
        volume = None
        if amount is not None:
            if unit.dimension == 'volume':
                volume = unit.convert_quantity(amount, litre)
            elif unit.dimension == 'mass':
                if density is not None:
                    volume = unit.convert_quantity(amount, kg) / density
            else:
                raise ValidationError({'water_unit': '浴液单位只能使用质量或体积。'})
        stage = persist(m.MaterialPlanStage(production_recipe=adoption, sequence=source.sequence, recipe_stage=source,
            phase=source.phase, phase_name_snapshot=source.phase.name if source.phase_id is not None else '',
            curve_version=source.curve_version, ph_text=source.ph_text, bath_ratio=source.bath_ratio,
            bath_ratio_basis=source.bath_ratio_basis, water_amount=None if amount is None else amount.quantize(Decimal('.000001'), rounding=ROUND_HALF_UP), water_unit=unit,
            bath_density_kg_per_litre=density, temperature_c=source.temperature_c, minutes=source.hold_minutes,
            dept_belong_id=item.dept_belong_id), actor)
        for ingredient in require_rows(sampling.RecipeIngredient.objects.filter(stage=source)):
            dosage = calculate_adopted_dosage(ingredient.dosage, data['adjustment_percent'])
            original_kg = planned_chemical_mass_kg(ingredient.dosage, ingredient.dosage_basis, dry_mass_kg=dry_mass_kg, bath_volume_l=volume)
            needed_kg = planned_chemical_mass_kg(dosage, ingredient.dosage_basis, dry_mass_kg=dry_mass_kg, bath_volume_l=volume)
            if needed_kg is None:
                raise ValidationError({'stages': 'g/L计划缺少浴液体积；质量浴液还需实际密度依据。'})
            target = ingredient.material.stock_unit
            exact = kg.convert_quantity(needed_kg, target)
            rounded = exact.quantize(Decimal('1').scaleb(-min(target.decimal_places, 6)), rounding=ROUND_HALF_UP)
            persist(m.MaterialPlanLine(stage=stage, sequence=ingredient.sequence, recipe_ingredient=ingredient,
                material=ingredient.material, original_dosage=ingredient.dosage, adjustment_percent=data['adjustment_percent'],
                adopted_dosage=dosage.quantize(Decimal('.000001'), rounding=ROUND_HALF_UP), dosage_basis=ingredient.dosage_basis,
                original_required_quantity=kg.convert_quantity(original_kg, target).quantize(Decimal('.000001'), rounding=ROUND_HALF_UP),
                required_quantity=rounded, quantity_unit=target, dept_belong_id=item.dept_belong_id,
                calculation_snapshot={'dry_mass_kg': str(dry_mass_kg), 'bath_volume_l': None if volume is None else str(volume), 'exact_adopted_dosage': str(dosage),
                    'chemical_mass_kg': str(needed_kg), 'exact_stock_quantity': str(exact), 'unit': target.pk,
                    'factor_to_base': str(target.factor_to_base), 'rounding': 'ROUND_HALF_UP', 'decimal_places': min(target.decimal_places, 6)}), actor)
    record(adoption, 'adopt', {'exists': False}, actor)
    record(item, 'adopt_recipe', snapshot(item), actor)
    return item
