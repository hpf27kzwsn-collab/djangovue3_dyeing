"""来样色号同步、打样结果/回复及试产、生产配方采用。"""
import json
from decimal import Decimal
from django.db import transaction
from django.db.models import F
from .business import locked, persist, record, snapshot
from .source_stock_services import raw
from .source_business_updates import matching, update_rows
from .source_sampling_services import rows, change
from .source_entry_services import entry_for
from .source_context import SourceDocumentContext
from .source_calculations import store_value


COLOR_FIELDS = ['ColorNo', 'CheckNo', 'LabDipsSource', 'ProdID', 'LotNo', 'Spec', 'ColorDepthID',
    'ColorID', 'ColorNum', 'ColorE', 'CustColorNum', 'ColorRGB', 'Price', 'MainStuffKindID', 'IsToDoSample',
    'ColorCards', 'Status', 'StartTime', 'LimitHours', 'OverTimeReason', 'ShiftID', 'EmpID', 'WorkQty',
    'RedoTimes', 'OriColorNo', 'OriEmpID', 'OriShifID', 'JobSheetNo', 'Remarks', 'Width', 'Weight',
    'CustSelfProduct', 'ColorNumMark', 'R', 'G', 'B', 'RGB', 'GradeID']
LAB_FIELDS = ['CustomerID', 'CreateDate', 'Creater', 'VerLight1ID', 'VerLight2ID',
              'Duiseluogang', 'Daipaidaban', 'Dabanpise', 'KindType']


@transaction.atomic
def sync_lab(item, actor):
    if item.SOURCE_TABLE != 'DyeLabMain' or entry_for(item) != 'ShowDyeLabMain':
        return
    from .source_phase3_operations import retire
    from .source_phase2_triggers import color_registered
    series = raw(item, 'SheetSeries')
    heads = list(matching(rows('DyeLabMain'), SheetSeries=series).order_by('pk'))
    # 原游标来自主从连接；不能按色号或颜色编码去重。
    cursor = [(raw(color, 'ColorNum'), raw(color, 'ColorNo')) for head in heads
              for color in matching(rows('DyeLabColor'), SheetSeries=raw(head, 'SheetSeries')).order_by('pk')]
    for color_num, color_no in cursor:
        retire(matching(rows('PColorNum', 'erp_base'), SheetSeries=series, ColorNo=color_no), actor,
               '原来样保存删除后重建色号；被替换的完整原行留档')
        for color in matching(rows('DyeLabColor'), SheetSeries=series, ColorNum=color_num).order_by('pk'):
            for head in heads:
                values = {name: raw(color, name) for name in COLOR_FIELDS}
                values.update({name: raw(head, name) for name in LAB_FIELDS})
                values.update(SheetSeries=series, ColorMark=raw(color, 'ColorMarkt'),
                              CusRemark=raw(head, 'Remarks'), Modifyer=None, ModifyDate=None)
                model = rows('PColorNum', 'erp_base').model
                master = persist(model(**{model.SOURCE_FIELDS[key]: value for key, value in values.items()}), actor)
                color_registered(master, actor)
                record(master, 'lab_color_register', {'exists': False}, actor,
                       f'来样主行：{head.pk}；颜色原行：{color.pk}；游标：{color_num}/{color_no}')
        # 原UPDATE未排序；明确采用承接行顺序末项，保留全部来源及候选审计。
        for master in matching(rows('PColorNum', 'erp_base'), SheetSeries=series).order_by('pk'):
            candidates = list(matching(rows('DyeDipsRecord'), ColorNum=raw(master, 'ColorNum')).order_by('pk'))
            if candidates:
                change(type(master).objects.filter(pk=master.pk),
                       {key: raw(candidates[-1], key) for key in ['StuffDosage', 'CostQuote', 'ColorDepthID']}, actor)
                if len(candidates) > 1:
                    record(master, 'lab_trial_candidates', snapshot(master), actor,
                           '原无序UPDATE候选：'+str([row.pk for row in candidates]))


@transaction.atomic
def update_result(item, actor):
    """Sp_DyeDipsRecord_update 的所选单据动作，不循环改写全部历史。"""
    item = locked(item)
    series, color = raw(item, 'SheetSeries'), raw(item, 'ColorNum')
    phases = matching(rows('DyeDipsRecordPhase'), SheetSeries=series).order_by('old_phase_no', 'pk')
    details = matching(rows('DyeDipsRecordDetail'), SheetSeries=series)
    white = dye = fast = False
    names = []
    for detail in details:
        materials = matching(rows('PStuff', 'erp_base'), StuffID=raw(detail, 'StuffID'))
        if materials.filter(old_gao_laodu=True).exists():
            fast = True
        if color is None or not phases.filter(old_phase_no=raw(detail, 'PhaseNo')).exists():
            continue
        white |= matching(materials, StuffKindID='5').exists()
        dye |= matching(materials, StuffType='S').exclude(old_stuff_kind_id__isnull=True).exclude(old_stuff_kind_id='5').exists()
    for phase in phases:
        dictionary = matching(rows('PFieldValid', 'erp_base'), FieldType='DyePhase',
                              Code=raw(phase, 'PhaseID'), Description='染色')
        names.extend(name for name in dictionary.order_by('pk').values_list('old_name', flat=True) if name is not None)
    depth = raw(item, 'ColorDepthID')
    dosage = raw(item, 'StuffDosage')
    dosage = 0 if dosage is None else dosage
    color_name = raw(item, 'ColorID')
    if white and not dye:
        depth = '06'
    elif dye and dosage > 0:
        depth = '01' if dosage < Decimal('0.2') else '02' if dosage < 1 else '03'
    elif not white and dosage == 0 and color_name is not None:
        if '本白' in color_name:
            depth = '04'
        elif '洗水' not in color_name:
            depth = '05'
        elif '洗水' not in color_name or '本白' not in color_name:
            depth = '01'
    values = {'ColorDepthID': depth, 'DyePhaseName': ','.join(names) if names else None}
    if fast:
        values['GaoLaodu'] = '高牢度染料'
    change(type(item).objects.filter(pk=item.pk), values, actor)
    item.refresh_from_db()
    note = matching(rows('DyeDipsRecordNote'), SheetSeries=series).order_by('-pk').first()
    copied = {key: raw(item, key) for key in ['GaoLaodu', 'EmpID', 'ColorDepthID', 'StuffDosage', 'DyePhaseName']}
    copied.update(Note=None if note is None else raw(note, 'Note'), EndTime=raw(item, 'SheetDate'),
                  IsToSampleDaTe=raw(item, 'SheetDate'), IsToDoSample=True)
    for key in ['ColorNum', 'ColorNo']:
        change(matching(rows('PColorNum', 'erp_base'), **{key: raw(item, key)}), copied, actor)
        change(matching(rows('DyeLabColor'), **{key: raw(item, key)}), {'ColorDepthID': depth}, actor)
    # 此处调用的是20位Fn_Get_No，不能用调价的10位F_Get_No。
    from .source_foundation_functions import extract_number, number_matches
    number = extract_number(color,20)
    if number is not None and raw(item, 'SheetDate') is not None:
        older = number_matches(rows('DyeDipsRecord').filter(old_sheet_date__lt=raw(item,'SheetDate')).exclude(old_color_num__regex=r'^ *$'),color,20)
        change(older, {'Invalid': True}, actor)
    return item


@transaction.atomic
def reply(item, actor, note, status, confirm_version, reply_at):
    item = locked(item)
    notes = matching(rows('DyeDipsRecordNote'), SheetSeries=raw(item, 'SheetSeries'))
    if notes.exists():
        change(notes, {'Note': note, 'Status': status}, actor)
    else:
        model = notes.model
        value = persist(model(old_sheet_series=raw(item, 'SheetSeries'), old_note=note, old_status=status), actor)
        record(value, 'sample_reply_create', {'exists': False}, actor, '打样回复原表记录')
    before = snapshot(item)
    change(type(item).objects.filter(pk=item.pk), {'ConfirmVersion': confirm_version}, actor)
    item.refresh_from_db()
    record(item, 'sample_reply', before, actor, json.dumps({'reply_at': reply_at.isoformat(),
        'note': note, 'raw_status': status, 'confirm_version': confirm_version}, ensure_ascii=False))
    for key in ['ColorNum', 'ColorNo']:
        change(matching(rows('PColorNum', 'erp_base'), **{key: raw(item, key)}), {'Note': note}, actor)
    if confirm_version not in [None, '']:
        update_result(item, actor)
    return item


def copy_values(source, target, excluded):
    return dict(store_value(target(), old, raw(source, old))
                for old in (target.SOURCE_FIELDS.keys() & source.SOURCE_FIELDS.keys()) - set(excluded))


@transaction.atomic
def adopt_recipe(item, actor, entry, version, adopted_at, slot=None):
    from . import source_services as services
    item = locked(item)
    target_model = rows('DyeRecipe').model
    excluded = ['SheetSeries', 'SheetNo', 'SheetKind', 'SheetDate', 'ColorVersion', 'Cost',
                'SheetStatus', 'RightStatus', 'StepNo', 'PrintTimes', 'Revisions', 'Creater', 'CreateDate',
                'Modifyer', 'ModifyDate', 'Approver', 'ApproveDate']
    data = copy_values(item, target_model, excluded)
    data.update(_entry=entry, old_sheet_kind=1 if entry == 'TrialDyeRecipe' else 2,
                old_sheet_date=adopted_at, old_color_version=version, old_ori_recipe_sheet_no=raw(item, 'SheetNo'))
    target = services.write(target_model, data, actor=actor, apply_effects=False)
    is_dips = item.SOURCE_TABLE == 'DyeDipsRecord'
    phase_table = 'DyeDipsRecordPhase' if is_dips else 'DyeRecipePhase'
    detail_table = 'DyeDipsRecordDetail' if is_dips else 'DyeRecipeDetail'
    sources = list(matching(rows(phase_table), SheetSeries=raw(item, 'SheetSeries')).order_by('old_phase_no', 'pk'))
    details = list(matching(rows(detail_table), SheetSeries=raw(item, 'SheetSeries')).order_by('old_phase_no', 'old_stuff_no', 'pk'))
    target_phase = rows('DyeRecipePhase').model
    target_detail = rows('DyeRecipeDetail').model
    adopted_phases = {}
    for source in sources:
        values = copy_values(source, target_phase, ['SheetSeries'])
        phase = persist(target_phase(**values, old_sheet_series=target.old_sheet_series, source_parent_1=target), actor)
        adopted_phases.setdefault(raw(source, 'PhaseNo'), []).append(phase)
        record(phase, 'recipe_phase_copy', {'exists': False}, actor, f'原染程：{source._meta.label}/{source.pk}')
    for source in details:
        number = raw(source, 'PhaseNo')
        if number not in adopted_phases:
            # 旧孤立用料仍进入新配方；仅补实际PhaseNo，未知染程字段保持NULL。
            phase = persist(target_phase(old_sheet_series=target.old_sheet_series, old_phase_no=number, source_parent_1=target), actor)
            adopted_phases[number] = [phase]
            record(phase, 'recipe_orphan_phase', {'exists': False}, actor, f'承接孤立用料原行：{source.pk}')
        values = copy_values(source, target_detail, ['SheetSeries', 'Dosage', 'Amount'])
        values.update(old_dosage=raw(source, 'Dosage' + slot) if is_dips else raw(source, 'Dosage'),
                      old_amount=raw(source, 'Amount' + slot) if is_dips else raw(source, 'Amount'))
        # 一条原用料只复制一次；多张同序号阶段都保存，不制造重复剂量。
        line = persist(target_detail(**values, old_sheet_series=target.old_sheet_series,
                       source_parent_1=adopted_phases[number][0]), actor)
        record(line, 'recipe_material_copy', {'exists': False}, actor, f'原用料：{source._meta.label}/{source.pk}；采用列：{slot}')
    context = SourceDocumentContext.objects.get(entity=target._meta.label, object_id=target.pk)
    context.effects['recipe_origin'] = {'source': snapshot(item), 'entity': item._meta.label, 'slot': slot,
        'phases': [snapshot(value) for value in sources], 'materials': [snapshot(value) for value in details]}
    persist(context, actor)
    services.finish([target], actor)
    record(target, 'recipe_adopted', {'exists': False}, actor, f'采用来源：{item._meta.label}/{item.pk}；新配方可独立办理')
    return target
