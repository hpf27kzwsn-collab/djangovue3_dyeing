"""Sp_WprocessBackUp的半年归档、备份表历史范围及可撤回的原行留档。"""
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models.functions import Upper, RTrim
from django.utils import timezone
from .business import locked, persist, record, snapshot
from .source_stock_services import raw
from .source_quality_reports import key
from .source_package_operations import reader, rows, scoped, check_scope, effect
from .source_continuation import origin, save_effect
from .source_chain_reverse import capture
from .source_operation_effects import restore


TABLES = ['WProcess', 'WProcessStep', 'JobShiftEmp']


def cutoff(as_of):
    local = timezone.localtime(as_of)
    year, month = divmod(local.year * 12 + local.month - 1 - 6, 12)
    return local.replace(year=year, month=month + 1, day=1, hour=0, minute=0, second=0, microsecond=0)


def plan(as_of, query=reader, lock=False):
    def materialize(queryset):
        queryset = queryset.order_by('pk')
        return list(queryset.select_for_update() if lock else queryset)
    aged = materialize(rows('WProcess', reader, 'erp_production').filter(old_end_time__lt=cutoff(as_of)))
    existing = materialize(rows('WProcessBak', reader, 'erp_production'))
    numbers = {key(raw(item, 'WProcessNo')) for item in [*aged, *existing] if raw(item, 'WProcessNo') is not None}
    selected = {name: materialize(rows(name, reader, 'erp_production').alias(work_code=Upper(RTrim('old_wprocess_no'))).filter(work_code__in=numbers)) for name in TABLES}
    check_scope([*aged, *existing, *[item for items in selected.values() for item in items]], query)
    report = {'report': '半年工位归档范围', 'rows': [
        {'source_table': name, 'copy_count': len(aged if name == 'WProcess' else items), 'retire_count': len(items),
         'copy_ids': [item.pk for item in (aged if name == 'WProcess' else items)], 'retire_ids': [item.pk for item in items]}
        for name, items in selected.items()], 'cutoff': cutoff(as_of),
        'supplemental_rows': [{'existing_backup_ids': [item.pk for item in existing]}],
        'notes': ['截止点为实际办理时间前六个月的月初，严格小于；NULL结束时间不进入首轮备份。',
            '后续范围包含备份表现有WProcessNo，所以同号较新工位及其明细也会退出现行范围；所有原行留档。',
            '原JobShiftEmpBak漏写必填ProcessNo，本服务照来源复制；原批量删除触发器无序选一行，采用ID最大行回写，差异见E77。']}
    return report, aged, selected


def preview(as_of, query=reader):
    return plan(as_of, query)[0]


@transaction.atomic
def archive(anchor, actor, at, reason, query=reader):
    anchor = scoped(anchor, query)
    previous = effect(anchor, 'work_archive')
    if previous is not None and previous['state'] == 'applied':
        raise ValidationError({'source': '请先撤回本记录发起的归档，再重新办理。'})
    report, aged, selected = plan(at, query, lock=True)
    created = []; states = []
    for name, items in selected.items():
        model = apps.get_model('erp_production.SourceDye' + name + 'Bak')
        for source in aged if name == 'WProcess' else items:
            values = {field: raw(source, old) for old, field in model.SOURCE_FIELDS.items()}
            target = persist(model(**values, dept_belong_id=source.dept_belong_id), actor)
            record(target, 'work_archive_copy', {'exists': False}, actor, reason)
            save_effect(target, 'work_archive_copy', {'anchor_id': anchor.pk, 'source': origin(source), 'at': at}, actor, reason)
            created.append(origin(target))
        for source in items:
            states.append({'source': origin(source), 'previous': effect(source, 'work_archived')})
            save_effect(source, 'work_archived', {'active': True, 'anchor_id': anchor.pk, 'at': at, 'reason': reason}, actor, reason)
    with capture() as changes:
        if selected['WProcess']:
            from .source_work_delete import trigger_removed
            trigger_removed(selected['WProcess'][-1], actor, retain_children=True)
    check_scope([apps.get_model(row['entity']).objects.get(pk=row['id']) for row in changes], query)
    save_effect(anchor, 'work_archive', {'state': 'applied', 'at': at, 'reason': reason, 'report': report,
        'created': created, 'states': states, 'changes': changes}, actor, reason)
    return report


@transaction.atomic
def undo(anchor, actor, at, reason, query=reader):
    anchor = scoped(anchor, query)
    value = effect(anchor, 'work_archive')
    if value is None or value['state'] != 'applied':
        raise ValidationError({'source': '本记录没有可撤回的工位归档。'})
    originals = value['created'] + [entry['source'] for entry in value['states']]
    targets = []
    for entry in originals:
        item = locked(apps.get_model(entry['entity']).objects.get(pk=entry['source']['id']))
        for field in item.SOURCE_FIELDS.values():
            if getattr(item, field) != item._meta.get_field(field).to_python(entry['source'][field]):
                raise ValidationError({'source': f'{item._meta.label}#{item.pk}归档后已有字段变化，请先处理后续变更。'})
        targets.append(item)
    targets.extend(apps.get_model(entry['entity']).objects.get(pk=entry['id']) for entry in value['changes'])
    check_scope(targets, query)
    for entry in value['states']:
        item = apps.get_model(entry['source']['entity']).objects.get(pk=entry['source']['source']['id'])
        current = effect(item, 'work_archived')
        if current is None or not current['active'] or current['anchor_id'] != anchor.pk:
            raise ValidationError({'source': '工位归档事实已有后续变更，请先撤回该办理。'})
    restore(value['changes'], actor, reason)
    for entry in value['created']:
        item = apps.get_model(entry['entity']).objects.get(pk=entry['source']['id'])
        save_effect(item, 'work_archived', {'active': True, 'anchor_id': anchor.pk, 'reversed_at': at}, actor, reason)
    for entry in value['states']:
        item = apps.get_model(entry['source']['entity']).objects.get(pk=entry['source']['source']['id'])
        save_effect(item, 'work_archived', entry['previous'] or {'active': False, 'reversed_at': at}, actor, reason)
    save_effect(anchor, 'work_archive', {**value, 'state': 'reversed', 'reversed_at': at, 'reverse_reason': reason}, actor, reason)
    return anchor
