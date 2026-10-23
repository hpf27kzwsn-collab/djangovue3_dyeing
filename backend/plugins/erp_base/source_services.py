"""原表单据的主从保存与办理；历史导入独立保存原事实。"""
from plugins.erp_base.source_provenance import is_historical
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models.deletion import ProtectedError
from django.utils import timezone
from uuid import uuid4
from datetime import datetime
from .business import locked, persist, record, snapshot
from .source_ownership import OWNERS
from .source_calculations import field_values,packaging_values,aggregate_values,price_from_amount,PRODUCTS,SPECIAL_TABLES,PACK_METHODS,AGGREGATES
from .source_sequences import allocate
from .source_calculation_entries import ENTRY_METHODS
from .source_entry_calculations import entry_values
from . import source_entry_services as entries
from . import source_stock_services as stock
from . import source_workflow_services as workflow
from . import source_sales_services as sales
from . import source_sampling_services as sampling
from . import source_charge_services as charges
from . import source_purchase_flow as purchase
from . import source_quality_flow as quality
from . import source_packaging_flow as packing

OWNED = {'source_batch', 'source_row', 'approval_stage', 'confirmed_at',
         'confirmed_by', 'approved_at', 'approved_by'}


def managed_fields(model):
    return OWNED | set(model.SOURCE_IDENTITIES) | {
        model.SOURCE_FIELDS[target] for target, child, old, coalesce in AGGREGATES.get(model.SOURCE_TABLE, [])}


def owner_relations(model):
    return OWNERS.get(model._meta.label, [])


def parents(item):
    if item.SOURCE_TABLE=='RecordDefect' and item.source_parent_1_id is not None and entries.entry_for(item.source_parent_1) in ['QueryRecordCheck','QC_Record','QueryRecord']:
        return [item.source_parent_1]
    return [getattr(item, rule['field']) for rule in owner_relations(type(item))
            if getattr(item, rule['field'] + '_id') is not None]


def chain(item):
    owners = parents(item)
    if len(owners) > 1:
        raise ValidationError({'parent': '本条明细请明确采用一个办理表头，原多来源码仍保留。'})
    return [item] if not owners else chain(owners[0]) + [item]


def lock_chain(item):
    return [locked(parent) for parent in chain(item)]


def require_origin_edit(item):
    from .source_execution_state import require_available
    require_available(item)
    from .source_context import SourceDocumentContext
    context = SourceDocumentContext.objects.filter(entity=item._meta.label, object_id=item.pk).first()
    if context is not None and 'derived_from' in context.effects:
        raise ValidationError({'parent': '此记录由来源单据办理生成，请修改实际来源单据。'})


def editable(items):
    for item in items:
        require_origin_edit(item)
        if item.pk is not None and item.SOURCE_TABLE in ['GrayInRecord','JobGrayRecord']:
            from .source_gray_split_merge import require_active
            require_active(item)
        if item.approval_stage in ['confirmed', 'approved']:
            raise ValidationError({'approval_stage': '所属单据已经确认或审核，请先重新办理。'})


def child_rows(item):
    for label, rules in OWNERS.items():
        model = apps.get_model(label)
        for rule in rules:
            if rule['target'] == item._meta.label:
                yield from model.objects.filter(**{rule['field']: item}).order_by('pk')


def validate_document(item):
    item.full_clean()
    for child in child_rows(item):
        child.full_clean()
        validate_document(child)


def assign_owner_values(item, data):
    selected = [rule for rule in owner_relations(type(item)) if getattr(item, rule['field'] + '_id') is not None]
    if len(selected) > 1:
        raise ValidationError({'parent': '采购明细只能选择一个实际办理表头。'})
    for rule in selected:
        parent = getattr(item, rule['field'])
        for old, parent_old in zip(rule['source_fields'], rule['target_fields']):
            key = item.SOURCE_FIELDS[old]
            value = getattr(parent, parent.SOURCE_FIELDS[parent_old])
            if key in data and data[key] != value:
                raise ValidationError({key: '原关联码必须与所选表头一致。'})
            setattr(item, key, value)


def assign_reference_values(item,data,entry=None):
    assigned={}
    for rule in item.SOURCE_RELATIONS:
        if getattr(item,rule['field']+'_id') is None:
            continue
        parent=getattr(item,rule['field'])
        targets=['BarCode'] if item.SOURCE_TABLE=='RecordDefect' and entry=='QueryRecordDefect2' and rule['field']=='source_parent_1' else rule['target_fields']
        for old,parent_old in zip(rule['source_fields'],targets):
            key=item.SOURCE_FIELDS[old]
            value=getattr(parent,parent.SOURCE_FIELDS[parent_old])
            if key in data and data[key]!=value:
                raise ValidationError({key:'原关联码必须与所选来源记录一致。'})
            if key in assigned and assigned[key]!=value:
                raise ValidationError({key:'所选来源记录的共同关联码不一致。'})
            assigned[key]=value
            setattr(item,key,value)


def literal_default(model,key,value):
    if model.SOURCE_TABLE == 'PurMain' and key == 'old_sheet_status' and value == '':
        value=0  # 原整数列DEFAULT('')在SQL Server中的实际转换结果。
    if model.SOURCE_TABLE == 'CHECKEXACT' and key == 'old_checktime' and value == 0:
        value=datetime(1900,1,1)  # 已核实原datetime DEFAULT((0))及CAST(0 AS datetime)的实际值。
    return model._meta.get_field(key).to_python(value)


def apply_defaults(item, data):
    if item.SOURCE_TABLE == 'RecordYield' and 'old_guid' not in data:
        item.old_guid = str(uuid4())
    for key, (kind, value) in item.SOURCE_DEFAULTS.items():
        if key in data:
            continue
        if kind == 'now':
            value = timezone.now()
        elif kind == 'uuid':
            value = uuid4()
        field = item._meta.get_field(key)
        value = literal_default(type(item),key,value) if kind == 'literal' else field.to_python(value)
        if field.get_internal_type() == 'DateTimeField' and value is not None and timezone.is_naive(value):
            value = timezone.make_aware(value)
        setattr(item, key, value)


def refresh_totals(items, actor):
    for item in reversed(items):
        twisting=item.SOURCE_TABLE=='ProdIn' and entries.entry_for(item)=='TwistingIn'
        check_dots=item.SOURCE_TABLE=='RecordYield' and entries.entry_for(item)=='QueryRecordCheck'
        if item.SOURCE_TABLE not in AGGREGATES and not twisting and not check_dots:
            continue
        original = item
        item = locked(item)
        if is_historical(item):
            continue
        values = entry_values(item,'TwistingIn') if twisting else aggregate_values(item)
        if check_dots:
            from django.db.models import Sum
            from .source_execution_state import active
            from .source_calculations import store_value
            defects=apps.get_model('erp_quality.SourceDyeRecordDefect')
            dots=active(defects.objects.filter(source_parent_1=item)).aggregate(value=Sum(defects.SOURCE_FIELDS['SumDots']))['value']
            values=dict([store_value(item,'Dots',dots)])
        changed = {key: value for key, value in values.items() if getattr(item, key) != value}
        if changed:
            before = snapshot(item)
            for key, value in changed.items():
                setattr(item, key, value)
            persist(item, actor)
            for key,value in changed.items():
                setattr(original,key,value)
            if actor is not None:
                record(item, 'refresh_totals', before, actor, '采用原子表汇总公式')


def finish(items, actor):
    from .source_phase6_save_timing import flush
    flush()
    from .source_phase6_formula_runtime import refresh_totals as remaining_totals
    remaining_totals(items,actor)
    refresh_totals(items, actor)
    for item in items:packing.after_saved(item,actor)
    stock.refresh_chain(items, actor)
    workflow.refresh_chain(items, actor)
    sampling.refresh_chain(items, actor)
    from .source_sample_flow import sync_lab
    for item in items:
        sync_lab(item, actor)
    from .source_phase6_hooks import saved as entry_saved
    for item in items:entry_saved(item,actor)
    from .source_phase6_guards import before as entry_before
    for item in items:entry_before(item,'AfterSaveSQL',actor)


@transaction.atomic
def write(model, data, instance=None, actor=None, apply_effects=True, check_entry_update=True):
    from . import numbering
    from copy import copy
    numbering.lock_model(model)
    data = dict(data)
    pricing_choice=data.pop('_pricing',None)
    selected_entry = data.pop('_entry', None)
    copy_from = data.pop('_entry_copy_from', None)
    if instance is not None and copy_from is not None:
        raise ValidationError({'_entry_copy_from': '续行只在新增记录时使用。'})
    denied = managed_fields(model).intersection(data)
    if denied:
        raise ValidationError({key: '由来源导入或明确办理动作维护。' for key in denied})
    item = model() if instance is None else lock_chain(instance)[-1]
    previous_numbering = None if instance is None else copy(item)
    for parent in chain(item):
        if parent.pk is not None:
            purchase.require_change(parent, '修改')
    if instance is None:
        apply_defaults(item, data)
    editable(chain(item))
    if instance is not None and check_entry_update:
        from .source_phase6_guards import before as entry_before
        for parent in chain(item):entry_before(parent,'BeforeUpdateSQL',actor)
        status=model.SOURCE_FIELDS.get('SheetStatus')
        if status in data and getattr(item,status)==9 and data[status]!=9:
            entry_before(item,'BeforeUnAbortSQL',actor)
    if instance is not None and model.SOURCE_TABLE not in ['p_Customer', 'p_Gray', 'p_Dept', 'h_Employee', 'USERINFO']:
        for old in model.SOURCE_KEY:
            key = model.SOURCE_FIELDS[old]
            if key in data and data[key] != getattr(item, key) and not numbering.managed(item, key, selected_entry or entries.entry_for(item)):
                raise ValidationError({key: '原业务身份建立后保持不变，变更另建明确记录。'})
    for rule in owner_relations(model):
        field = rule['field']
        if instance is not None and field in data and getattr(item, field + '_id') is not None:
            previous = getattr(item, field + '_id')
            target = None if data[field] is None else data[field].pk
            if previous != target:
                raise ValidationError({field: '已有明细不能移到另一张表头。'})
    before = {'exists': False} if instance is None else snapshot(item)
    for key, value in data.items():
        setattr(item, key, value)
    from .source_execution_state import require_available
    for rule in item.SOURCE_RELATIONS:
        if getattr(item,rule['field']+'_id') is not None:require_available(getattr(item,rule['field']))
    if item.SOURCE_TABLE in ['WProcess','StuffWeight','RecordYield','ProdIn','StuffOut','ProdOutDetail','GrayOutDetail','SemiOutDetail']:
        from .source_business_updates import matching
        jobs=apps.get_model('erp_production.SourceDyeJobSheet')
        for job in matching(jobs.objects.all(),SheetNo=stock.raw(item,'JobSheetNo')):require_available(locked(job))
    if instance is None:
        for parent in chain(item)[:-1]:
            from .source_phase6_guards import before as entry_before
            if check_entry_update:entry_before(parent,'BeforeUpdateSQL',actor)
            purchase.require_change(parent, '修改')
    editable(lock_chain(item) if item.pk is not None else [locked(parent) for parent in chain(item)[:-1]])
    entry = entries.resolve_entry(item, selected_entry, chain(item)[:-1])
    if not is_historical(item):
        assign_owner_values(item, data)
        assign_reference_values(item,data,entry)
    if copy_from is not None:
        from .source_entry_copy import apply as copy_entry_fields
        copied_fields = copy_entry_fields(item, data, copy_from, entry)
    protected_numbers = numbering.prepare(item, data, entry, instance is None, previous_numbering)
    if instance is None:
        data.update(protected_numbers)
    if instance is None and entry is not None:
        from .source_phase6_local_values import prepare_numbers
        prepare_numbers(item,data,entry)
        entries.apply_new_rules(item, data, actor, entry)
        from .source_site_work import bind
        bind(item,data,entry)
    if instance is None:
        item.approval_stage = 'draft' if item.SOURCE_DOCUMENT and not parents(item) else None
        allocate(item, actor)
    if actor is not None:
        item.modifier = actor
        if instance is None:
            item.creator = actor
            owner_chain = chain(item)
            item.dept_belong_id = actor.dept_id if len(owner_chain) == 1 else owner_chain[0].dept_belong_id
    from .source_phase6_auto_values import before_save as entry_auto_values
    entry_auto_values(item, data, entry, instance is None)
    if model.SOURCE_TABLE=='OrderColor':
        from .source_order_pricing import prepare as prepare_pricing
        prepare_pricing(item,data,pricing_choice,actor)
    result = persist(item)
    from .source_master_data import saved as master_saved
    master_saved(item, data, instance is None, actor)
    from .source_phase2_triggers import saved as phase2_saved
    phase2_saved(item, data, instance is None, actor)
    from .source_phase3_triggers import saved as phase3_saved
    phase3_saved(item, data, instance is None, actor)
    from .source_phase4_triggers import saved as phase4_saved
    phase4_saved(item, data, instance is None, actor)
    from .source_phase5_triggers import saved as phase5_saved
    phase5_saved(item, data, instance is None, actor)
    if entry is not None:
        entries.save_context(item, actor, entry)
    if model.SOURCE_TABLE in ['OrderMain','OrderColor']:
        from .source_order_pricing import saved as pricing_saved
        pricing_saved(item,data,actor)
    from .source_phase6_service_values import saved as service_values_saved
    service_values_saved(item,data,entry,instance is None,actor)
    from .source_phase6_formula_runtime import saved as remaining_values_saved
    remaining_values_saved(item,data,entry,instance is None,actor)
    sales.saved(item, data, instance is None, actor)
    charges.saved(item, actor)
    sampling.saved(item, actor)
    quality.saved(item, instance is None, actor)
    from .source_work_progress import saved as work_progress_saved
    work_progress_saved(item,data,instance is None,actor,previous_numbering)
    packing.saved(item, instance is None, actor)
    if item.SOURCE_TABLE=='ShiftArrange':
        from .source_shift_work import trigger
        trigger(item,data,instance is None,actor)
    if item.SOURCE_TABLE=='MachineFault':
        from .source_equipment_faults import trigger
        trigger(item,actor)
    if item.SOURCE_TABLE == 'SalaryChanges':
        from .source_foundation import salary_changes_saved
        salary_changes_saved(item)
    if actor is not None:
        record(item, 'create' if instance is None else 'edit', before, actor)
        if copy_from is not None:
            record(item, 'entry_copy_fields', {'source': snapshot(copy_from), 'fields': copied_fields}, actor,
                   '按用户选定上一行应用原复制字段；手填值及显式NULL优先，来源原行不变')
    if apply_effects:
        finish(chain(item), actor)
    if instance is not None and model.SOURCE_FIELDS.get('SheetStatus') in data:
        status=model.SOURCE_FIELDS['SheetStatus']
        if data[status]==9 and before.get(status)!=9:
            from .source_phase6_hooks import aborted as entry_aborted
            entry_aborted(item,actor)
    if item.SOURCE_TABLE=='ProdTest':
        from .source_trial_variants import saved as trial_saved
        trial_saved(item,entry,actor)
    return result


def require_operation_retention(item):
    from .source_context import SourceDocumentContext
    if item.SOURCE_TABLE == 'RecordYield':
        contexts = SourceDocumentContext.objects.filter(effects__package_label_sync__state='applied')
        if any(any(row['entity'] == item._meta.label and row['id'] == item.pk for row in context.effects['package_label_sync']['changes']) for context in contexts):
            raise ValidationError({'source':'本包装参与已生效的标签同步，请先撤回对应同步，保留原字段恢复链。'})
    context=SourceDocumentContext.objects.filter(entity=item._meta.label,object_id=item.pk).first()
    if context is not None and any(key in context.effects for key in [
        'quote_adjustment_origin','quote_transfer_origin','purchase_product_origin','field_copy_origin','department_purchase_origin','care_plan_article_origin','transfer_retained',
        'card_adoption','order_transfer_origin','combine_link_origin','combine_link_reversal','gray_operation','gray_lineage','gray_consumed',
        'history_gray_recovery','history_gray_origin','quality_rebuild_origin','quality_replaced',
        'execution_chain','chain_cancelled','chain_container','chain_compensation',
        'package_replacement','package_retained','package_pairing','package_gray_origin','package_label_sync',
        'work_archive','work_archived','work_archive_copy',
        'sample_variant','trial_work','trial_retained','trial_origin',
        'shift_work','shift_retained','shift_origin','shift_master_sync',
        'calendar_generation','calendar_retained','calendar_origin',
        'equipment_operation','equipment_retained','equipment_origin','foundation_retained',
        'cross_card_issue','cross_card_transfer']):
        raise ValidationError({'source':'此记录是拆合/转移办理事实，使用对应撤回动作并保留记录，不能直接删除。'})


@transaction.atomic
def delete_documents(queryset, actor):
    """删除明确选择的新主从单据；真实外部引用及历史原行继续由原规则保护。"""
    def owned(item):
        descendants = []
        for child in child_rows(item):
            editable(lock_chain(child))
            if is_historical(child):
                raise ValidationError({'source_batch': '所属明细含历史来源记录，不能删除该原行。'})
            descendants.extend(owned(child))
            descendants.append(child)
        return descendants
    for item in queryset.order_by('pk'):
        require_operation_retention(item)
        editable(lock_chain(item))
        from .source_phase6_guards import before as entry_before
        entry_before(item,'BeforeDeleteSQL',actor)
        sales.removing(item)
        purchase.require_change(item, '删除')
        if not item.SOURCE_DOCUMENT or item.SOURCE_TABLE == 'WProcess':
            delete(type(item).objects.filter(pk=item.pk), actor)
            continue
        if is_historical(item):
            raise ValidationError({'source_batch': '历史来源单据保留原行，不从普通删除入口删除。'})
        from .source_context import SourceDocumentContext
        context = SourceDocumentContext.objects.filter(entity=item._meta.label, object_id=item.pk).first()
        if context is not None:
            from .source_stock_job_services import removing
            removing(item, context, actor)
            stock.clear_effects(context, actor)
        descendants = owned(item)
        for child in descendants:
            delete(type(child).objects.filter(pk=child.pk), actor, apply_effects=False)
        delete(type(item).objects.filter(pk=item.pk), actor)


@transaction.atomic
def delete(queryset,actor=None,apply_effects=True):
    affected = {}
    removed = []
    work_progress = set()
    for item in queryset.order_by('pk'):
        require_operation_retention(item)
        editable(lock_chain(item))
        if is_historical(item):
            raise ValidationError({'source_batch': '历史来源记录保留原行，不从普通删除入口删除。'})
        from .source_phase6_guards import before as entry_before
        entry_before(item,'BeforeDeleteSQL',actor)
        sales.removing(item)
        sampling.removing(item, actor)
        from .source_phase6_hooks import before_delete as entry_before_delete
        entry_before_delete(item,actor)
        from .source_master_data import removing as master_removing
        master_removing(item, actor)
        from .source_phase2_triggers import removing as phase2_removing
        phase2_removing(item, actor)
        from .source_phase3_triggers import removing as phase3_removing
        phase3_removing(item, actor)
        from .source_phase5_triggers import removing as phase5_removing
        phase5_removing(item, actor)
        for parent in chain(item):
            purchase.require_change(parent, '删除')
        quality.removing(item,actor)
        packing.removing(item)
        if item.SOURCE_TABLE == 'WProcess':
            from .source_work_delete import prepare_delete
            prepare_delete(item, actor)
            record(item, 'work_deleted', snapshot(item), actor, '删除刷卡原行，随后执行WProcess_DELETE回写')
        if item.SOURCE_TABLE == 'StuffWeight':
            outgoing = apps.get_model('erp_warehouse.SourceDyeStuffOut')
            if outgoing.objects.filter(old_weight_sheet_no__iexact=item.old_sheet_no).exists():
                raise ValidationError({'source': '此称料单已有实际出库，按原规则保留来源称料单。'})
        removed.append(item)
        from .source_phase6_formula_links import parent_rows as raw_formula_parents
        for parent in [*chain(item)[:-1],*raw_formula_parents(item)]:
            affected[(parent._meta.label, parent.pk)] = parent
        from .source_context import SourceDocumentContext
        context = SourceDocumentContext.objects.filter(entity=item._meta.label, object_id=item.pk).first()
        if context is not None:
            if item.SOURCE_TABLE=='WProcess' and 'work_plan_progress' in context.effects:work_progress.add(item.pk)
            from .source_stock_job_services import removing
            removing(item, context, actor)
            stock.clear_effects(context, actor)
            context.delete()
    # 自动分配的细码由来源出库单维护，先撤回本次生成行，再删除实际明细并统一重建。
    for parent in affected.values():
        if parent.SOURCE_TABLE in stock.STOCK_TABLES:
            context = SourceDocumentContext.objects.filter(entity=parent._meta.label, object_id=parent.pk).first()
            if context is not None:
                stock.clear_effects(context, actor)
    try:
        queryset.delete()
    except ProtectedError as error:
        raise ValidationError({'parent': '此记录仍被明细或其他业务引用，请先处理相应业务。'}) from error
    for item in removed:
        sales.removed(item, actor)
        sampling.removed(item, actor)
        quality.removed(item, actor)
        from .source_work_delete import trigger_removed
        trigger_removed(item, actor)
        from .source_phase5_triggers import removed as phase5_removed
        if item.SOURCE_TABLE not in ['DyeRecipe','DefectiveInDetail']:phase5_removed(item, actor)
    if apply_effects:
        finish(list(affected.values()), actor)
        for item in removed:
            workflow.refresh_removed(item, actor,refresh_work_progress=item.SOURCE_TABLE=='WProcess' and item.pk in work_progress)


@transaction.atomic
def advance(item, actor, expected, target):
    objects = lock_chain(item)
    item = objects[-1]
    require_origin_edit(item)
    if not item.SOURCE_DOCUMENT or len(objects) > 1:
        raise ValidationError({'approval_stage': '关联明细由所属表头办理，请从表头确认或审核。'})
    if item.approval_stage != expected:
        raise ValidationError({'approval_stage': '当前办理阶段不允许此动作。'})
    validate_document(item)
    if target=='approved':
        from .source_phase6_guards import before as entry_before
        entry_before(item,'BeforeApproveSQL',actor)
    before = snapshot(item)
    item.approval_stage = target
    at = timezone.now()
    if target == 'confirmed':
        item.confirmed_at, item.confirmed_by = at, actor
    elif target == 'approved':
        item.approved_at, item.approved_by = at, actor
        if entries.entry_for(item) is not None and 'RightStatus' in item.SOURCE_FIELDS:
            setattr(item, item.SOURCE_FIELDS['RightStatus'], 10)
    persist(item, actor)
    if target == 'approved':
        sales.adjustment_audit(item, actor, True)
        if item.SOURCE_TABLE=='ShiftArrange' and entries.entry_for(item)=='ShiftArrange':
            from .source_shift_work import trigger,apply
            trigger(item,{'old_right_status':10},False,actor,at)
            apply(item,actor,at,'原排班AfterApproveSQL调整报工人员')
    if item.SOURCE_TABLE=='MachineFault':
        from .source_equipment_faults import trigger
        trigger(item,actor,at)
    stock.refresh(item, actor)
    workflow.refresh_chain([item], actor)
    if target=='approved':
        from .source_phase6_hooks import approved as entry_approved
        entry_before(item,'AfterApproveSQL',actor)
        entry_approved(item,actor,True)
    record(item, target, before, actor)
    return item


def confirm(item, actor):
    return advance(item, actor, 'draft', 'confirmed')


def approve(item, actor):
    return advance(item, actor, 'confirmed', 'approved')


@transaction.atomic
def reopen(item, actor, reason):
    objects = lock_chain(item)
    item = objects[-1]
    from .source_context import SourceDocumentContext
    context = SourceDocumentContext.objects.filter(entity=item._meta.label, object_id=item.pk).first()
    if context is not None and 'derived_from' in context.effects:
        raise ValidationError({'parent': '此记录由来源单据办理生成，请从实际来源单据重新办理。'})
    if len(objects) > 1:
        raise ValidationError({'approval_stage': '请从所属表头重新办理。'})
    if item.approval_stage not in ['confirmed', 'approved']:
        raise ValidationError({'approval_stage': '此单据当前不在确认或审核阶段。'})
    if not reason.strip():
        raise ValidationError({'reason': '重新办理须说明原因。'})
    before = snapshot(item)
    was_approved = item.approval_stage == 'approved'
    if was_approved:
        from .source_phase6_guards import before as entry_before
        entry_before(item,'BeforeUnApproveSQL',actor)
        purchase.require_change(item, 'reopen')
    item.approval_stage = 'draft'
    item.confirmed_at = item.approved_at = None
    item.confirmed_by = item.approved_by = None
    if entries.entry_for(item) is not None and 'RightStatus' in item.SOURCE_FIELDS:
        setattr(item, item.SOURCE_FIELDS['RightStatus'], 0)
    persist(item, actor)
    if was_approved:
        sales.adjustment_audit(item, actor, False)
        if item.SOURCE_TABLE=='ShiftArrange' and entries.entry_for(item)=='ShiftArrange':
            from .source_shift_work import trigger
            trigger(item,{'old_right_status':0},False,actor)
    if item.SOURCE_TABLE=='MachineFault':
        from .source_equipment_faults import trigger
        trigger(item,actor)
    stock.refresh(item, actor)
    workflow.refresh_chain([item], actor)
    if was_approved:
        from .source_phase6_hooks import approved as entry_approved
        entry_approved(item,actor,False)
    record(item, 'reopen', before, actor, reason)
    return item


@transaction.atomic
def calculate(item, actor, method):
    item = lock_chain(item)[-1]
    editable(chain(item))
    if is_historical(item):
        raise ValidationError({'source_batch': '历史原计算值保留；重新计算在新办理单据上采用。'})
    if method == 'fields':
        if item.SOURCE_TABLE not in PRODUCTS and item.SOURCE_TABLE not in SPECIAL_TABLES:
            raise ValidationError({'method': '本表尚未登记本行字段公式。'})
        values = field_values(item)
    elif method == 'amount_to_price':
        if item.SOURCE_TABLE != 'StuffInDetail':
            raise ValidationError({'method': '金额反算单价仅适用于原染化料入库明细。'})
        values = price_from_amount(item)
    elif method.startswith('entry:'):
        values = entry_values(item, method[len('entry:'):])
    else:
        if item.SOURCE_TABLE != 'RecordYield' or method not in PACK_METHODS:
            raise ValidationError({'method': '所选原入口公式不适用于本条记录。'})
        values = packaging_values(item, method)
    before = snapshot(item)
    for key, value in values.items():
        setattr(item, key, value)
    persist(item, actor)
    sales.saved(item, values, False, actor)
    charges.saved(item, actor)
    sampling.saved(item, actor)
    record(item, 'calculate', before, actor, '采用原入口公式：' + method)
    finish(chain(item), actor)
    return item
