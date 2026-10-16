"""试样/配方的染程、用料、成本和确板版本联动。"""
from datetime import datetime
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db.models import F, Sum
from django.utils import timezone
from .business import record, snapshot
from .source_business_updates import matching, update_rows
from .source_entry_services import entry_for
from .source_stock_services import raw


def rows(table, module='erp_sampling'):
    return apps.get_model(module + '.SourceDye' + table).objects.all()


def change(query, values, actor):
    update_rows(query, values, actor, 'sampling_source_update', '采用旧打样/配方的染程、成本及确板版本规则')


def saved(item, actor):
    if item.source_batch_id is not None or item.legacy_id is not None:
        return
    table = item.SOURCE_TABLE
    if table in ['DyeRecipeDetail', 'DyeDipsRecordDetail']:
        if matching(rows('PStuff', 'erp_base'), StuffID=raw(item, 'StuffID')).filter(old_status=1).exists():
            raise ValidationError({'old_stuff_id': '原用料规则：该染化料已停用，不能用于新办理配方；历史原用料仍保留。'})
    elif table in ['DyeRecipePhase', 'DyeDipsRecordPhase']:
        phases = matching(rows(table), SheetSeries=raw(item, 'SheetSeries'), PhaseID=raw(item, 'PhaseID'))
        has_parent = table == 'DyeRecipePhase' or matching(rows('DyeDipsRecord'), SheetSeries=raw(item, 'SheetSeries')).exists()
        if has_parent and phases.count() > 1:
            raise ValidationError({'old_phase_id': '原配方规则：同一配方的染程不能重复。'})
        if table == 'DyeRecipePhase':
            for phase in matching(rows(table), SheetSeries=raw(item, 'SheetSeries')).filter(old_remarks__endswith="'"):
                change(type(phase).objects.filter(pk=phase.pk), {'Remarks': phase.old_remarks.replace("'", '’')}, actor)
            item.refresh_from_db()


def refresh_chain(items, actor):
    for item in items:
        if item.SOURCE_TABLE != 'DyeRecipe' or item.source_batch_id is not None or item.legacy_id is not None:
            continue
        amounts = []
        for phase in matching(rows('DyeRecipePhase'), SheetSeries=raw(item, 'SheetSeries')):
            amount = matching(rows('DyeRecipeDetail'), SheetSeries=raw(item, 'SheetSeries')).filter(
                old_phase_no=raw(phase, 'PhaseNo')).aggregate(total=Sum('old_amount'))['total']
            if amount is not None:
                amounts.append(amount)
        change(type(item).objects.filter(pk=item.pk), {'Cost': sum(amounts) if amounts else None}, actor)
        item.refresh_from_db()
        if entry_for(item) == 'TrialDyeRecipe' and raw(item, 'SheetKind') == 1:
            # 旧 AfterSaveSQL 第一条已按 ColorNum 回写全部同色号，第二条是它的子集。
            change(matching(rows('PColorNum', 'erp_base'), ColorNum=raw(item, 'ColorNum')),
                   {'ColorNumNO': raw(item, 'ColorVersion'), 'OKTime': raw(item, 'SheetDate')}, actor)


def removing(item, actor):
    if item.SOURCE_TABLE != 'DyeLabColor':
        return
    if matching(rows('DyeDipsRecord'), ColorNum=raw(item, 'ColorNum')).exists() or matching(
            rows('DyeDipsRecord'), ColorNo=raw(item, 'ColorNo')).exists():
        raise ValidationError({'source': '此来样颜色已有打样配方，按原规则不能删除。'})
    masters = matching(rows('PColorNum', 'erp_base'), SheetSeries=raw(item, 'SheetSeries'), ColorNo=raw(item, 'ColorNo'))
    for master in masters.filter(source_batch__isnull=True, legacy_id__isnull=True).order_by('pk'):
        record(master, 'sampling_color_delete', snapshot(master), actor, '随所属新来样颜色删除；历史色号主档保留')
        master.delete()


def removed(item, actor):
    if item.SOURCE_TABLE != 'DyeRecipe':
        return
    recipes = matching(rows('DyeRecipe'), ColorNum=raw(item, 'ColorNum')).filter(old_sheet_kind=1)
    # 原 UPDATE JOIN 多版本时没有确定采用项；按最新配方日期、主键确定当前版本。
    previous = recipes.order_by(F('old_sheet_date').desc(nulls_last=True), '-pk').first()
    if previous is not None:
        values = {'ColorNumNO': raw(previous, 'ColorVersion'), 'OKTime': raw(previous, 'SheetDate')}
    elif raw(item, 'SheetKind') == 1:
        values = {'ColorNumNO': '', 'OKTime': timezone.make_aware(datetime(1900, 1, 1))}
    else:
        return
    change(matching(rows('PColorNum', 'erp_base'), ColorNum=raw(item, 'ColorNum')), values, actor)
