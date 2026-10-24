from plugins.erp_quality import models as q
"""实际报工与更正；采用计划不产生实际时间、产量或领料。"""
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Max
from plugins.erp_base import models as base
from plugins.erp_sales import models as sales
from plugins.erp_warehouse import models as warehouse
from plugins.erp_base.business import locked, persist, record, snapshot, require_state
from . import models as m


def effective(execution):
    values = snapshot(execution)
    for correction in m.ExecutionCorrection.objects.filter(execution=execution).order_by('id'):
        for flag, field, value in [('changes_quantity','output_quantity',correction.new_output_quantity),
            ('changes_mass','output_mass_kg',correction.new_output_mass_kg),
            ('changes_start_time','started_at',correction.new_started_at),('changes_end_time','ended_at',correction.new_ended_at)]:
            if getattr(correction, flag):values[field] = value
    import json
    from plugins.erp_base.business import FactsEncoder
    return json.loads(json.dumps(values,cls=FactsEncoder))


def predecessor_complete(operation,at=None):
    if operation.predecessor_id is not None and not operation.predecessor.is_skipped:
        previous=m.OperationExecution.objects.filter(operation=operation.predecessor).exclude(status='cancelled').order_by('-execution_number').first()
        if previous is None or previous.status!='completed':raise ValidationError({'operation':'所选前置工序最新轮次尚未完工。'})
        if at is not None:
            from django.utils.dateparse import parse_datetime
            if at < parse_datetime(effective(previous)['ended_at']):raise ValidationError({'at':'当前开工时间不能早于前置实际完工。'})


def check_start(operation, machine, at):
    card=operation.work_card
    require_state(card,['released','running'])
    if card.is_paused or operation.is_skipped:
        raise ValidationError({'operation': '工卡已暂停或本节点已跳过。'})
    if at < card.released_at:
        raise ValidationError({'at': '实际开工不能早于工卡下达。'})
    predecessor_complete(operation,at)
    if m.OperationExecution.objects.filter(operation=operation,status='running').exists():
        raise ValidationError({'operation': '本节点已经开工，请采用现有执行。'})
    if operation.process.requires_recipe is True:
        member_batches = m.DyeBatchWorkCard.objects.filter(work_card=card).exclude(batch__status='cancelled').values_list('batch_id',flat=True)
        if not m.ProductionRecipe.objects.filter(batch_id__in=member_batches,status='active').exists():
            raise ValidationError({'recipe': '此工序需要已采用的生产配方。'})
    if machine is None:
        if operation.process.requires_machine is True:
            raise ValidationError({'machine': '此工序必须明确实际机台。'})
    else:
        if machine.is_active is not True or machine.factory_id != card.factory_id or not base.MachineProcess.objects.filter(machine=machine,process=operation.process,is_active=True).exists():
            raise ValidationError({'machine': '实际机台必须启用、属于本工厂并适用于此工序。'})
        if operation.work_center_id is not None and machine.work_center_id != operation.work_center_id:
            raise ValidationError({'machine': '实际机台不属于本节点工作中心。'})
        if m.OperationExecution.objects.filter(machine=machine,status='running').exists():
            raise ValidationError({'machine': '实际机台仍有未完工执行。'})
        machine_interval(machine,at,None)


def machine_interval(machine,started_at,ended_at,exclude=()):
    """机台的实际占用按有效报工时间核对；同缸成员共用一个区间。"""
    from django.utils.dateparse import parse_datetime
    rows=m.OperationExecution.objects.filter(machine=machine,started_at__isnull=False,status__in=['running','completed','cancelled']).exclude(pk__in=exclude)
    for row in rows:
        values=effective(row)
        other_start=parse_datetime(values['started_at'])
        other_end=None if values['ended_at'] is None else parse_datetime(values['ended_at'])
        if (ended_at is None or other_start<ended_at) and (other_end is None or started_at<other_end):
            raise ValidationError({'machine':'本次有效实际时间与该机台其他执行重叠。'})


def start_card(card, actor):
    if card.status == 'released':
        before=snapshot(card);card.status='running';persist(card,actor);record(card,'start',before,actor)
        for rework in m.ReworkOrder.objects.select_for_update().filter(rework_work_card=card,status='released'):
            previous=snapshot(rework);rework.status='running';persist(rework,actor);record(rework,'start',previous,actor)
        for order_id in sorted(set(m.WorkCardOrderAllocation.objects.filter(work_card=card).values_list('order_line__order_id',flat=True))):
            order=sales.SalesOrder.objects.select_for_update().get(pk=order_id)
            if order.status == 'confirmed':
                before=snapshot(order);order.status='running';persist(order,actor);record(order,'start_production',before,actor)


def make_execution(operation, actor, at, employee, machine, shift, physical=None):
    maximum=m.OperationExecution.objects.filter(operation=operation).aggregate(value=Max('execution_number'))['value']
    execution=persist(m.OperationExecution(operation=operation,execution_number=1 if maximum is None else maximum+1,
        batch=physical.batch if physical is not None else None,physical_execution=physical,machine=machine,shift=shift,
        started_at=at,status='running',dept_belong_id=operation.work_card.dept_belong_id),actor)
    persist(m.ExecutionWorker(execution=execution,employee=employee,role='operator',dept_belong_id=execution.dept_belong_id),actor)
    start_card(operation.work_card,actor)
    record(execution,'start',{'exists':False},actor)
    return execution


@transaction.atomic
def start(item, actor, at, employee, machine=None, shift=None):
    card=locked(item.work_card);item=locked(item);item.work_card=card
    if machine is not None:machine=locked(machine)
    check_start(item,machine,at)
    if m.DyeBatchWorkCard.objects.filter(work_card=card).exclude(batch__status='cancelled').exists() and item.process.requires_recipe is True:
        raise ValidationError({'batch': '共用染色节点从缸批统一开工。'})
    make_execution(item,actor,at,employee,machine,shift)
    return item


def check_output(execution, values, at):
    if at < execution.started_at:
        raise ValidationError({'at': '实际完工不能早于开工，可跨日保存。'})
    for key in ['input_quantity','output_quantity','output_mass_kg','output_length_m','output_pieces','defect_quantity']:
        if values[key] is not None and values[key] < 0:
            raise ValidationError({key:'新实际报工数量不能为负数。'})
    for quantity,unit in [('input_quantity','input_unit'),('output_quantity','output_unit')]:
        if (values[quantity] is None)!=(values[unit] is None):
            raise ValidationError({unit: '实际数量和单位必须同时提供或同时留空。'})
    process=execution.operation.process
    if process.requires_quantity is True and values['output_quantity'] is None:
        raise ValidationError({'output_quantity': '此工序必须记录实际产出量。'})
    if process.requires_weight is True and values['output_mass_kg'] is None:
        raise ValidationError({'output_mass_kg': '此工序必须记录实际重量kg。'})


@transaction.atomic
def complete(item,actor,at,**values):
    if item.physical_execution_id is not None:
        raise ValidationError({'physical_execution': '同缸成员由物理执行统一完工并分配实绩。'})
    locked(item.operation.work_card);item=locked(item);require_state(item,['running'])
    if item.machine_id is not None:
        locked(item.machine);machine_interval(item.machine,item.started_at,at,[item.pk])
    check_output(item,values,at)
    before=snapshot(item)
    for field,value in values.items():setattr(item,field,value)
    item.ended_at,item.status=at,'completed'
    persist(item,actor);record(item,'complete',before,actor)
    return item


@transaction.atomic
def start_batch(item,actor,process,machine,at,employee,shift=None):
    item=locked(item);require_state(item,['scheduled','running'])
    if process.requires_recipe is True and not m.ProductionRecipe.objects.filter(batch=item,status='active').exists():
        raise ValidationError({'recipe':'当前染色缸批必须已采用明确配方。'})
    members=list(m.DyeBatchWorkCard.objects.filter(batch=item).order_by('work_card_id'))
    if not members:raise ValidationError({'batch':'请先明确同缸成员。'})
    cards={row.pk:row for row in m.WorkCard.objects.select_for_update().filter(pk__in=[row.work_card_id for row in members]).order_by('pk')}
    machine=locked(machine)
    operations=[]
    for member in members:
        matches=list(m.WorkCardOperation.objects.filter(work_card=member.work_card,process=process))
        if len(matches)!=1:raise ValidationError({'process':'当前缸批每张工卡必须明确且只有一个本工序节点。'})
        operation=locked(matches[0]);operation.work_card=cards[member.work_card_id]
        check_start(operation,machine,at)
        operations.append(operation)
    if not m.ScheduleAssignment.objects.filter(batch=item,operation__process=process,machine=machine,status='released').exists():
        raise ValidationError({'schedule':'同缸开工必须采用已发布的本工序机台安排。'})
    maximum=m.PhysicalBatchExecution.objects.filter(batch=item,process=process).aggregate(value=Max('execution_number'))['value']
    physical=persist(m.PhysicalBatchExecution(batch=item,process=process,machine=machine,operator=employee,shift=shift,
        started_at=at,execution_number=1 if maximum is None else maximum+1,dept_belong_id=item.dept_belong_id),actor)
    for operation in operations:make_execution(operation,actor,at,employee,machine,shift,physical)
    before=snapshot(item);item.status='running';persist(item,actor);record(item,'start',before,actor)
    record(physical,'start',{'exists':False},actor)
    return item


@transaction.atomic
def complete_batch(item,actor,at,output_mass_kg,members):
    batch=locked(item.batch)
    cards=list(m.WorkCard.objects.select_for_update().filter(pk__in=m.DyeBatchWorkCard.objects.filter(batch=batch).values('work_card_id')).order_by('pk'))
    item=locked(item);require_state(item,['running'])
    executions=list(m.OperationExecution.objects.select_for_update().filter(physical_execution=item).order_by('pk'))
    locked(item.machine);machine_interval(item.machine,item.started_at,at,[row.pk for row in executions])
    data={row['execution'].pk:row for row in members}
    if len(data)!=len(members) or set(data)!={row.pk for row in executions}:
        raise ValidationError({'members':'请逐项且仅一次提供本物理执行所有成员的实际量。'})
    if sum((row['output_mass_kg'] for row in members),Decimal('0')) != output_mass_kg:
        raise ValidationError({'output_mass_kg':'成员实绩kg合计必须等于本次同缸实际kg。'})
    before=snapshot(item)
    for execution in executions:
        values={key:value for key,value in data[execution.pk].items() if key!='execution'}
        check_output(execution,values,at)
        previous=snapshot(execution)
        for key,value in values.items():setattr(execution,key,value)
        execution.ended_at,execution.status=at,'completed';persist(execution,actor);record(execution,'complete',previous,actor)
    item.ended_at,item.output_mass_kg,item.status=at,output_mass_kg,'completed'
    persist(item,actor);record(item,'complete',before,actor)
    return item


@transaction.atomic
def skip(item,actor,reason):
    card=locked(item.work_card);require_state(card,['released','running']);item=locked(item)
    if item.is_required or item.process.may_skip is not True:
        raise ValidationError({'operation':'当前节点不是明确允许跳过的可选工序。'})
    if m.OperationExecution.objects.filter(operation=item).exists():
        raise ValidationError({'execution':'已有执行不能改为跳过。'})
    predecessor_complete(item)
    before=snapshot(item);item.is_skipped,item.skip_reason=True,reason;persist(item,actor);record(item,'skip',before,actor,reason)
    return item


@transaction.atomic
def correct(item,actor,reason,at,employee,changes):
    batch=locked(item.batch) if item.batch_id is not None else None
    locked(item.operation.work_card);item=locked(item);require_state(item,['completed'])
    if item.physical_execution_id is not None:
        raise ValidationError({'physical_execution':'同缸分配更正必须按整缸处理，不能单独改变一成员合计。'})
    save_correction(item,actor,reason,at,employee,changes)
    return item


def save_correction(item,actor,reason,at,employee,changes):
    require_state(item.operation.work_card,['running'])
    if q.QualityInspection.objects.filter(execution=item,is_void=False).exclude(result='pending').exists():
        raise ValidationError({'inspection':'此实绩已形成有效检验判定，请先取消对应检验采用并保留历史。'})
    if warehouse.LotTransformation.objects.filter(execution=item,is_confirmed=True,is_void=False).exists() or warehouse.Package.objects.filter(work_card=item.operation.work_card).exclude(status__in=['draft','void']).exists() or warehouse.StockReceiptLine.objects.filter(work_card=item.operation.work_card,receipt__status='posted').exists():
        raise ValidationError({'execution':'实绩已被产出或包装采用，请先冲销对应下游业务。'})
    allowed={'output_quantity','output_mass_kg','started_at','ended_at'}
    if not changes or set(changes)-allowed:
        raise ValidationError({'changes':'明确选择实际产量、重量、开工或完工时间更正项。'})
    for key in ['output_quantity','output_mass_kg']:
        if key in changes and changes[key] is not None and changes[key]<0:raise ValidationError({'changes':'新确认实绩不能为负数。'})
    before=effective(item);after={**before,**changes}
    started=after['started_at'];ended=after['ended_at']
    from django.utils.dateparse import parse_datetime
    started=parse_datetime(started) if isinstance(started,str) else started
    ended=parse_datetime(ended) if isinstance(ended,str) else ended
    if started is None or ended is None or ended < started:
        raise ValidationError({'changes':'已完成执行必须保留有效的实际开工与完工时间。'})
    if at < ended:raise ValidationError({'at':'更正时间不能早于更正后的实际完工。'})
    if started < item.operation.work_card.released_at:raise ValidationError({'changes':'更正后开工不能早于工卡下达。'})
    if item.machine_id is not None:
        locked(item.machine)
        excluded=[item.pk] if item.physical_execution_id is None else list(m.OperationExecution.objects.filter(physical_execution_id=item.physical_execution_id).values_list('pk',flat=True))
        machine_interval(item.machine,started,ended,excluded)
    predecessor_complete(item.operation,started)
    for successor in m.OperationExecution.objects.filter(operation__predecessor=item.operation,status__in=['running','completed']):
        if ended > parse_datetime(effective(successor)['started_at']):raise ValidationError({'changes':'更正后完工不能晚于后置实际开工。'})
    if item.operation.process.requires_quantity is True and after['output_quantity'] is None:
        raise ValidationError({'changes':'本工序实际产量不能清空。'})
    if item.operation.process.requires_weight is True and after['output_mass_kg'] is None:
        raise ValidationError({'changes':'本工序实际kg不能清空。'})
    from plugins.erp_base.business import FactsEncoder
    import json
    correction=persist(m.ExecutionCorrection(execution=item,reason=reason,corrected_at=at,approved_by=employee,
        changes_quantity='output_quantity' in changes,new_output_quantity=changes.get('output_quantity'),
        changes_mass='output_mass_kg' in changes,new_output_mass_kg=changes.get('output_mass_kg'),
        changes_start_time='started_at' in changes,new_started_at=changes.get('started_at'),
        changes_end_time='ended_at' in changes,new_ended_at=changes.get('ended_at'),
        before_values=json.loads(json.dumps(before,cls=FactsEncoder)),after_values=json.loads(json.dumps(after,cls=FactsEncoder)),
        dept_belong_id=item.dept_belong_id),actor)
    record(correction,'correct',{'exists':False},actor,reason)
    return item


def effective_physical(item):
    latest=m.PhysicalExecutionCorrection.objects.filter(physical_execution=item).order_by('-pk').first()
    return snapshot(item) if latest is None else latest.after_values


@transaction.atomic
def abort(item,actor,at,reason):
    if isinstance(item,m.PhysicalBatchExecution):
        locked(item.batch)
        list(m.WorkCard.objects.select_for_update().filter(pk__in=m.OperationExecution.objects.filter(physical_execution=item).values('operation__work_card_id')).order_by('pk'))
        item=locked(item);require_state(item,['running'])
        members=list(m.OperationExecution.objects.select_for_update().filter(physical_execution=item).order_by('pk'))
    else:
        if item.physical_execution_id is not None:raise ValidationError({'physical_execution':'同缸执行须整缸中止。'})
        locked(item.operation.work_card);item=locked(item);require_state(item,['running']);members=[item]
    if at<item.started_at:raise ValidationError({'at':'中止不能早于实际开工。'})
    if item.machine_id is not None:locked(item.machine)
    for member in members:
        require_state(member,['running']);before=snapshot(member)
        member.status,member.ended_at='cancelled',at;persist(member,actor);record(member,'abort',before,actor,reason)
    if isinstance(item,m.PhysicalBatchExecution):
        before=snapshot(item);item.status,item.ended_at='cancelled',at;persist(item,actor);record(item,'abort',before,actor,reason)
    return item


@transaction.atomic
def correct_batch(item,actor,at,employee,reason,output_mass_kg,started_at,ended_at,members):
    locked(item.batch)
    list(m.WorkCard.objects.select_for_update().filter(pk__in=m.OperationExecution.objects.filter(physical_execution=item).values('operation__work_card_id')).order_by('pk'))
    item=locked(item);require_state(item,['completed'])
    executions=list(m.OperationExecution.objects.select_for_update().filter(physical_execution=item).order_by('pk'))
    data={row['execution'].pk:row for row in members}
    if len(data)!=len(members) or set(data)!={row.pk for row in executions}:raise ValidationError({'members':'整缸更正必须逐项提供全部工卡成员。'})
    if sum((row['output_mass_kg'] for row in members),Decimal('0'))!=output_mass_kg:raise ValidationError({'output_mass_kg':'更正后的成员实绩合计必须等于整缸实绩。'})
    before=effective_physical(item);member_changes=[]
    for execution in executions:
        previous=effective(execution)
        changes={'output_mass_kg':data[execution.pk]['output_mass_kg'],'started_at':started_at,'ended_at':ended_at}
        if 'output_quantity' in data[execution.pk]:changes['output_quantity']=data[execution.pk]['output_quantity']
        save_correction(execution,actor,reason,at,employee,changes)
        member_changes.append({'execution':execution.pk,'before':previous,'after':effective(execution)})
    from plugins.erp_base.business import FactsEncoder
    import json
    after=json.loads(json.dumps({**before,'output_mass_kg':output_mass_kg,'started_at':started_at,'ended_at':ended_at},cls=FactsEncoder))
    correction=persist(m.PhysicalExecutionCorrection(physical_execution=item,corrected_at=at,approved_by=employee,
        reason=reason,before_values=before,after_values=after,member_changes=member_changes,dept_belong_id=item.dept_belong_id),actor)
    record(correction,'correct',{'exists':False},actor,reason)
    return item
