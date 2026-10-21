"""试样/配方的染程、用料、成本和确板版本联动。"""
from plugins.erp_base.source_provenance import is_historical
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
    from .source_execution_state import active
    return active(apps.get_model(module + '.SourceDye' + table).objects.all())


def change(query, values, actor):
    update_rows(query, values, actor, 'sampling_source_update', '采用旧打样/配方的染程、成本及确板版本规则')


def saved(item, actor):
    if is_historical(item):
        return
    table = item.SOURCE_TABLE
    if table in ['DyeRecipeDetail', 'DyeDipsRecordDetail']:
        if matching(rows('PStuff', 'erp_base'), StuffID=raw(item, 'StuffID')).filter(old_status=1).exists():
            raise ValidationError({'old_stuff_id': '原用料规则：该染化料已停用，不能用于新办理配方；历史原用料仍保留。'})
    elif table in ['DyeRecipePhase', 'DyeDipsRecordPhase']:
        phases = matching(rows(table), SheetSeries=raw(item, 'SheetSeries'), PhaseID=raw(item, 'PhaseID'))
        has_parent = table == 'DyeRecipePhase' or matching(rows('DyeDipsRecord'), SheetSeries=raw(item, 'SheetSeries')).exists()
        if has_parent and phases.count() > 1:
            record(item,'original_recipe_phase_duplicate',snapshot(item),actor,
                '原同配方染程重复检查命中；按项目要求原行照存，不合并剂量和阶段')
        if table == 'DyeRecipePhase':
            for phase in matching(rows(table), SheetSeries=raw(item, 'SheetSeries')).filter(old_remarks__endswith="'"):
                change(type(phase).objects.filter(pk=phase.pk), {'Remarks': phase.old_remarks.replace("'", '’')}, actor)
            item.refresh_from_db()


def recipe_cost(item,reader=rows):
    """原染程/物料联查按原码连接；相同染程号的多行保留连接重复度。"""
    amounts=[]
    for phase in matching(reader('DyeRecipePhase','erp_sampling'),SheetSeries=raw(item,'SheetSeries')):
        amount=matching(reader('DyeRecipeDetail','erp_sampling'),SheetSeries=raw(item,'SheetSeries')).filter(
            old_phase_no=raw(phase,'PhaseNo')).aggregate(total=Sum('old_amount'))['total']
        if amount is not None:amounts.append(amount)
    return sum(amounts) if amounts else None


def refresh_chain(items, actor):
    for item in items:
        if item.SOURCE_TABLE != 'DyeRecipe' or is_historical(item):
            continue
        change(type(item).objects.filter(pk=item.pk), {'Cost': recipe_cost(item)}, actor)
        item.refresh_from_db()
        if entry_for(item) == 'TrialDyeRecipe':
            refresh_trial_versions(item,actor)


def refresh_trial_versions(item,actor):
    """原两条UPDATE依次执行；第二条更窄的ColorNo连接可能采用不同来源。"""
    heads=list(matching(rows('DyeRecipe'),SheetSeries=raw(item,'SheetSeries')).filter(old_sheet_kind=1).order_by('pk'))
    for fields in [('ColorNum',),('ColorNum','ColorNo')]:
        candidates={};targets={}
        for head in heads:
            for target in matching(rows('PColorNum','erp_base'),**{key:raw(head,key) for key in fields}).order_by('pk'):
                targets[target.pk]=target;candidates.setdefault(target.pk,[]).append(head)
        for pk,choices in candidates.items():
            target=targets[pk];selected=choices[-1]
            change(type(target).objects.filter(pk=pk),{'ColorNumNO':raw(selected,'ColorVersion'),
                                                     'OKTime':raw(selected,'SheetDate')},actor)
            if len(choices)>1:
                record(target,'trial_version_candidates',snapshot(target),actor,
                    '原UPDATE JOIN多来源，按承接顺序末项采用；连接字段：'+','.join(fields)+'；全部来源：'+
                    str([{'id':head.pk,'version':raw(head,'ColorVersion'),'date':raw(head,'SheetDate')} for head in choices]))


def removing(item, actor):
    if item.SOURCE_TABLE != 'DyeLabColor':
        return
    if matching(rows('DyeDipsRecord'), ColorNum=raw(item, 'ColorNum')).exists() or matching(
            rows('DyeDipsRecord'), ColorNo=raw(item, 'ColorNo')).exists():
        raise ValidationError({'source': '此来样颜色已有打样配方，按原规则不能删除。'})
    masters = matching(rows('PColorNum', 'erp_base'), SheetSeries=raw(item, 'SheetSeries'), ColorNo=raw(item, 'ColorNo'))
    from .source_master_data import retain
    for master in masters.order_by('pk'):
        retain(master,actor,'DyeLabColor_Delete：全部同流水及颜色序号原色号主档留档，不丢历史来源')


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
