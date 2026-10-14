"""原称料自动领料算法的明确软件动作；实际事件证明由调用方提供。"""
from datetime import datetime
from decimal import Decimal, localcontext
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models.functions import Upper, RTrim
from django.utils import timezone
from .business import locked, persist, snapshot, record
from .source_context import SourceDocumentContext
from .source_calculations import decimal, store_value
from .source_stock_services import raw


@transaction.atomic
def issue(item, actor, finished_at, evidence_kind, evidence_reference):
    if item.SOURCE_TABLE != 'StuffWeight':
        raise ValidationError({'source': '本动作适用于原染化料称料单。'})
    item = locked(item)
    if item.source_batch_id is not None or item.legacy_id is not None:
        raise ValidationError({'source': '历史称料与原自动出库已承接；本动作在明确的新接续称料单上办理。'})
    context = SourceDocumentContext.objects.select_for_update().filter(entity=item._meta.label, object_id=item.pk).first()
    if context is None:
        raise ValidationError({'_entry': '请为这张新称料单明确业务类型，再采用对应领料动作。'})
    if 'material_issue' in context.effects:
        return item  # 同一称料单已生成实际领料；重复回传不再次出库。
    cutoff = timezone.make_aware(datetime(2025, 3, 1, 8))
    if finished_at <= cutoff:
        raise ValidationError({'finished_at': '原自动领料规则只处理2025-03-01 08:00之后的事件；早期原单仍完整保留。'})
    out_model = apps.get_model('erp_warehouse.SourceDyeStuffOut')
    if out_model.objects.filter(old_weight_sheet_no=raw(item, 'SheetNo')).exists():
        raise ValidationError({'source': '原称料单号已经有出库单，请采用已有实际出库，不能重复生成。'})
    material_model = apps.get_model('erp_base.SourceDyePStuff')
    detail_model = apps.get_model('erp_production.SourceDyeStuffWeightDetail')
    lines = detail_model.objects.filter(source_parent_1__source_parent_1=item).order_by('old_phase_no', 'old_stuff_no', 'pk')
    adopted = []; omitted = []
    with localcontext() as arithmetic:
        arithmetic.prec = 80
        for line in lines:
            code = raw(line, 'StuffID'); planned = raw(line, 'NeedQty'); measured = raw(line, 'RealQty')
            if code in [None, ''] or planned is None or planned <= 0:
                omitted.append({'source_id': line.pk, 'reason': '原自动规则要求物料原码非空且计划量大于0'})
                continue
            used_real = measured is not None and measured != 0
            quantity = decimal(measured if used_real else planned)
            weight_unit = raw(line, 'WeightUnit')
            kg = quantity if weight_unit is not None and weight_unit.rstrip(' ').upper() == 'K' else quantity / 1000
            if kg <= 0 or kg >= 1000000:
                omitted.append({'source_id': line.pk, 'reason': '原自动写出库明细要求采用公斤量大于0且小于1000000'})
                continue
            matches = list(material_model.objects.alias(code=Upper(RTrim('old_stuff_id'))).filter(code=code.rstrip(' ').upper()).order_by('pk'))
            if not matches:
                omitted.append({'source_id': line.pk, 'reason': '原自动写出库明细内连接物料，此原码尚无物料匹配'})
                continue
            for material in matches:
                factor = raw(material, 'WOF'); factor = Decimal(1) if factor is None else decimal(factor)
                if factor == 0:
                    raise ValidationError({'WOF': '物料 ' + code + ' 的原WOF为0，不能按原除法自动领料；原行可保存，实际收发可另行录入。'})
                price = decimal(raw(material, 'Price'))
                adopted.append({'line': line, 'material': material, 'basis': 'RealQty' if used_real else 'NeedQty',
                    'kg': kg, 'quantity': kg / factor, 'money': None if price is None else kg * price / factor, 'price': price})
    before = snapshot(context)
    from .source_services import write, finish
    out = write(out_model, {'_entry': 'StuffOut', 'old_sheet_date': finished_at,
        'old_sheet_kind': 21, 'old_remarks': '自动出库', 'old_creater': '自动出库',
        'old_create_date': timezone.now(), 'old_ware_house_id': '13', 'old_dept_id': '08',
        'old_keeper': '自动出库', 'old_weight_sheet_no': raw(item, 'SheetNo'),
        'old_shift_id': '白班' if 8 <= timezone.localtime(finished_at).hour <= 20 else '夜班',
        'old_out_date': finished_at, 'old_job_sheet_no': raw(item, 'JobSheetNo')}, actor=actor, apply_effects=False)
    outgoing_detail = apps.get_model('erp_warehouse.SourceDyeStuffOutDetail')
    sources = []
    for ordinal, value in enumerate(adopted, 1):
        line = value['line']
        values = {'DetailNo': raw(out, 'SheetSeries') + '-' + str(ordinal).zfill(2),
            'StuffID': raw(line, 'StuffID'), 'Price': value['price'], 'Qty': value['quantity'], 'Amount': value['money'],
            'APDetailNo': str(raw(line, 'PhaseNo')), 'InDetailNo': str(raw(line, 'StuffNo'))}
        data = dict(store_value(outgoing_detail(), old, original) for old, original in values.items())
        target = write(outgoing_detail, {'source_parent_1': out, **data}, actor=actor, apply_effects=False)
        sources.append({'source_id': line.pk, 'outgoing_detail_id': target.pk, 'basis': value['basis'],
            'planned': None if raw(line, 'NeedQty') is None else str(raw(line, 'NeedQty')),
            'measured': None if raw(line, 'RealQty') is None else str(raw(line, 'RealQty')), 'adopted_kg': str(value['kg'])})
    finish([out], actor)
    context.effects = {**context.effects, 'material_issue': {'outgoing_id': out.pk,
        'evidence_kind': evidence_kind, 'evidence_reference': evidence_reference, 'finished_at': finished_at.isoformat(),
        'rows': sources, 'not_generated': omitted}}
    persist(context, actor)
    record(context, 'issue_stuff_weight', before, actor, '按原自动规则采用实称非零值或计划量；保留实际事件证明')
    return item
