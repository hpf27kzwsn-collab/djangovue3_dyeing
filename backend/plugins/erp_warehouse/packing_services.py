"""包装实物、数量放行和打印请求；库存仍由收发单据生效。"""
from decimal import Decimal, ROUND_HALF_UP
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.dateparse import parse_datetime
from plugins.erp_base import models as base
from plugins.erp_production import models as production, execution_services as execution
from plugins.erp_base.business import locked, persist, record, snapshot, require_state, require_rows
from plugins.erp_production.services import converted_sum
from . import models as m


def package_quantity(item,unit):
    if unit.dimension=='mass':return base.Unit.objects.get(code='kg').convert_quantity(item.net_mass_kg,unit)
    if unit.dimension=='length':
        if item.length_m is None:raise ValidationError({'length_m':'长度单位分配必须记录实际包装长度。'})
        return base.Unit.objects.get(code='m').convert_quantity(item.length_m,unit)
    if unit.dimension=='count':
        if item.piece_quantity is None:raise ValidationError({'piece_quantity':'计数单位分配必须记录实际粒数。'})
        if unit.base_unit_id is not None:raise ValidationError({'unit':'粒数分配须采用明确的一粒基准单位。'})
        return item.piece_quantity
    raise ValidationError({'unit':'包装实物仅有已记录的质量、长度及粒数计量。'})


def final_source(card):
    operations=list(production.WorkCardOperation.objects.filter(work_card=card,is_skipped=False).exclude(process__code='GX98').order_by('sequence'))
    if not operations:raise ValidationError({'work_card':'工卡没有包装前实际生产节点。'})
    for operation in operations:
        latest=production.OperationExecution.objects.filter(operation=operation).exclude(status='cancelled').order_by('-execution_number').first()
        if latest is None or latest.status!='completed':raise ValidationError({'work_card':'所有已选包装前节点必须实际完工。'})
    return operations[-1]


def validate_allocation(row):
    row.full_clean()
    source=row.work_card_allocation
    row.unit.convert_quantity(row.quantity,source.unit)
    used=converted_sum(m.PackageOrderAllocation.objects.filter(work_card_allocation=source).exclude(package__status='void').exclude(pk=row.pk),'quantity','unit',source.unit)
    if used+row.unit.convert_quantity(row.quantity,source.unit)>source.allocated_quantity:raise ValidationError({'quantity':'累计包装分配不能超过对应工卡订单分配。'})
    root=source if source.original_allocation_id is None else source.original_allocation
    from django.db.models import Q
    entries=m.PackageOrderAllocation.objects.filter(Q(work_card_allocation=root)|Q(work_card_allocation__original_allocation=root)).exclude(package__status='void').exclude(pk=row.pk)
    if converted_sum(entries,'quantity','unit',root.unit)+row.unit.convert_quantity(row.quantity,root.unit)>root.allocated_quantity-root.released_unfulfilled_quantity:raise ValidationError({'quantity':'原工卡及承接返修包装合计不能重复占用同一订单需求。'})


def validate_coverage(row):
    row.full_clean()
    disposition=row.disposition
    require_state(disposition,['active'])
    inspection=disposition.inspection
    if inspection.is_void or inspection.result not in ['pass','fail'] or disposition.kind not in ['release','concession','downgrade']:
        raise ValidationError({'disposition':'包装须采用有效的实际放行、让步或降级处置。'})
    if inspection.kind not in ['final','reinspection'] or inspection.work_card_id!=row.package.work_card_id or inspection.execution_id!=row.package.source_execution_id:
        raise ValidationError({'disposition':'放行须明确对应包装前本轮实际产出及终检或复检范围。'})
    row.unit.convert_quantity(row.quantity,base.Unit.objects.get(code='kg'))


@transaction.atomic
def pack(item,actor,at,employee,machine=None):
    card=locked(item.work_card)
    sources=list(production.WorkCardOrderAllocation.objects.filter(work_card=card))
    roots={row.pk if row.original_allocation_id is None else row.original_allocation_id for row in sources}
    list(production.WorkCardOrderAllocation.objects.select_for_update().filter(pk__in=roots).order_by('pk'))
    item=locked(item);require_state(item,['draft'])
    require_state(card,['running'])
    last=final_source(card)
    if item.source_execution_id is None:raise ValidationError({'source_execution':'包装必须明确包装前本轮实际产出。'})
    source=locked(item.source_execution);require_state(source,['completed'])
    if source.operation_id!=last.pk:raise ValidationError({'source_execution':'包装只能采用当前路线包装前最后实际产出节点。'})
    if at < parse_datetime(execution.effective(source)['ended_at']):raise ValidationError({'at':'包装不能早于来源实际完工。'})
    item.full_clean()
    net=item.calculated_net_mass_kg
    if net is None:raise ValidationError({'net_mass_basis':'请按已选净重方法填写全部实际测量参数；明确零皮重须填零。'})
    net=net.quantize(Decimal('.000001'),rounding=ROUND_HALF_UP)
    if net<=0:raise ValidationError({'net_mass_kg':'实际包装净重必须大于零。'})
    actual=execution.effective(source)
    if actual['output_mass_kg'] is None:raise ValidationError({'source_execution':'来源本轮执行必须有实际产出kg。'})
    used=sum((row.net_mass_kg for row in m.Package.objects.filter(source_execution=source).exclude(status__in=['draft','void'])),Decimal('0'))
    if used+net>Decimal(actual['output_mass_kg']):raise ValidationError({'net_mass_kg':'同一实际产出轮次的累计包装净重不能超量。'})
    before=snapshot(item);item.net_mass_kg=net
    coverages=require_rows(m.PackageDispositionAllocation.objects.filter(package=item))
    ids=[row.disposition_id for row in coverages]
    list(production.QualityDisposition.objects.select_for_update().filter(pk__in=ids).order_by('pk'))
    kg=base.Unit.objects.get(code='kg')
    if converted_sum(coverages,'quantity','unit',kg)!=net:raise ValidationError({'quality_coverages':'放行覆盖kg合计必须等于本包装实际净重。'})
    for row in coverages:
        row.package=item;row.disposition=production.QualityDisposition.objects.get(pk=row.disposition_id)
        validate_coverage(row)
        prior=converted_sum(m.PackageDispositionAllocation.objects.filter(disposition=row.disposition).exclude(package__status__in=['draft','void']),'quantity','unit',row.disposition.unit)
        if prior+row.unit.convert_quantity(row.quantity,row.disposition.unit)>row.disposition.quantity:raise ValidationError({'quantity':'累计包装采用不能超过本笔实际放行数量。'})
    allocations=list(m.PackageOrderAllocation.objects.filter(package=item))
    if production.WorkCardOrderAllocation.objects.filter(work_card=card).exists() and not allocations:raise ValidationError({'allocations':'有订单工卡的包装须填写明确订单分配。'})
    dimensions={row.unit.dimension for row in allocations}
    if len(dimensions)>1:raise ValidationError({'unit':'同一包装的订单分配须采用同一计量维度。'})
    if allocations:
        target=allocations[0].unit
        if converted_sum(allocations,'quantity','unit',target)!=package_quantity(item,target):raise ValidationError({'quantity':'订单分配合计必须等于对应维度的包装实际量。'})
        for row in allocations:validate_allocation(row)
    item.calculation_snapshot={'method':item.net_mass_basis,'gross_mass_kg':None if item.gross_mass_kg is None else str(item.gross_mass_kg),
        'tube_unit_tare_kg':None if item.tube_unit_tare_kg is None else str(item.tube_unit_tare_kg),
        'outer_tare_kg':None if item.outer_tare_kg is None else str(item.outer_tare_kg),
        'piece_quantity':None if item.piece_quantity is None else str(item.piece_quantity),
        'fixed_piece_mass_kg':None if item.fixed_piece_mass_kg is None else str(item.fixed_piece_mass_kg),
        'net_mass_kg':str(net),'source_execution':source.pk,'source_effective':actual}
    item.status,item.packed_at,item.packer='packed',at,employee
    persist(item,actor)
    packaging=list(production.WorkCardOperation.objects.filter(work_card=card,process__code='GX98',is_skipped=False))
    if len(packaging)>1:raise ValidationError({'operation':'当前顺序路线包装节点应只有一个。'})
    if packaging:
        operation=packaging[0]
        if machine is not None:machine=locked(machine)
        execution.check_start(operation,machine,at)
        execution.make_execution(operation,actor,at,employee,machine,None)
        current=production.OperationExecution.objects.filter(operation=operation).latest('pk')
        execution.complete(current,actor,at=at,input_quantity=None,input_unit=None,output_quantity=net,output_unit=kg,
            output_mass_kg=net,output_length_m=item.length_m,output_pieces=item.piece_quantity,defect_quantity=None,quality_note=None)
        item.packaging_execution=current;persist(item,actor)
    record(item,'pack',before,actor)
    return item


@transaction.atomic
def void(item,actor,at,reason):
    card=locked(item.work_card);item=locked(item);require_state(item,['draft','packed'])
    if item.status=='packed':require_state(card,['running'])
    if m.StockReceiptLine.objects.filter(package=item,receipt__status__in=['confirmed','posted']).exists():raise ValidationError({'package':'包装已被收货采用，请先处理对应收货。'})
    from plugins.erp_sales.models import DeliveryLine
    if DeliveryLine.objects.filter(package_allocation__package=item).exclude(delivery__status='cancelled').exists():raise ValidationError({'package':'包装已有有效交付采用。'})
    if item.packed_at is not None and at < item.packed_at:raise ValidationError({'at':'作废不能早于包装时间。'})
    before=snapshot(item);item.status='void';persist(item,actor);record(item,'void',before,actor,reason)
    if item.packaging_execution_id is not None:
        actual=locked(item.packaging_execution);previous=snapshot(actual);actual.status='cancelled';persist(actual,actor);record(actual,'void_package',previous,actor,reason)
    return item


@transaction.atomic
def request_print(item,actor,at,employee,copies,previous=None,reason=''):
    locked(item.work_card);item=locked(item);require_state(item,['packed','received','issued','returned'])
    if item.label_template_id is None:raise ValidationError({'label_template':'请明确采用的实际标签版本。'})
    template=locked(item.label_template)
    if template.is_active is not True:raise ValidationError({'label_template':'当前标签版本未启用。'})
    if at < item.packed_at:raise ValidationError({'at':'打印请求不能早于包装完成。'})
    if previous is None:
        if m.LabelPrint.objects.filter(package=item).exists():raise ValidationError({'previous':'已有打印请求，重打须引用原请求。'})
    else:
        previous=locked(previous)
        if previous.package_id!=item.pk or not reason.strip():raise ValidationError({'previous':'重打须引用本包装原请求并填写原因。'})
    customer_ids=set(m.PackageOrderAllocation.objects.filter(package=item).values_list('work_card_allocation__order_line__order__customer_id',flat=True))
    if template.customer_id is not None and customer_ids!={template.customer_id}:raise ValidationError({'label_template':'客户专用标签必须对应本包装全部订单客户。'})
    template_data={'template':snapshot(template),'package':snapshot(item),'order_allocations':[snapshot(row) for row in m.PackageOrderAllocation.objects.filter(package=item)]}
    if template.template_file_id is not None:
        import base64,hashlib
        template_data['file']=snapshot(template.template_file)
        with template.template_file.url.open('rb') as stream:content=stream.read()
        template_data['file_content_base64']=base64.b64encode(content).decode('ascii')
        template_data['file_sha256']=hashlib.sha256(content).hexdigest()
    result=persist(m.LabelPrint(package=item,template=template,requested_at=at,copies=copies,kind='first' if previous is None else 'reprint',
        reason=reason,operator=employee,previous_print=previous,template_snapshot=template_data,dept_belong_id=item.dept_belong_id),actor)
    record(result,'request_print',{'exists':False},actor,reason)
    return item


@transaction.atomic
def confirm_print(item,actor,at,succeeded,reason):
    item=locked(item);require_state(item,['requested'])
    if at < item.requested_at:raise ValidationError({'at':'打印确认不能早于请求。'})
    if not succeeded and not reason.strip():raise ValidationError({'reason':'打印失败须填写实际原因。'})
    before=snapshot(item);item.status='succeeded' if succeeded else 'failed';item.confirmed_at=at;item.confirmation_source='manual'
    item.printed_at=at if succeeded else None;persist(item,actor);record(item,'confirm_print',before,actor,reason)
    return item
