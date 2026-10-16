"""明确接续业务的来源和办理事实，与旧字段分开存储。"""
from .business import locked, persist, record, snapshot
from .source_context import SourceDocumentContext
from .source_outwork_close import facts

CONTEXT_ENTRY = 'explicit_business_continuation'

# 新单据的创建/审批事实由本次办理产生，不能从历史单据复制。
NEW_DOCUMENT_FIELDS = ['SheetSeries', 'SheetNo', 'SheetDate', 'SheetStatus', 'RightStatus',
    'StepNo', 'PrintTimes', 'Revisions', 'Creater', 'CreateDate', 'Modifyer', 'ModifyDate',
    'Approver', 'ApproveDate']


def copy_new(source, model, excluded=()):
    from .source_sample_flow import copy_values
    from .source_services import managed_fields
    values = copy_values(source, model, [*NEW_DOCUMENT_FIELDS, *excluded])
    return {key: value for key, value in values.items() if key not in managed_fields(model)}


def save_effect(item, key, value, actor, reason):
    context, _ = SourceDocumentContext.objects.get_or_create(entity=item._meta.label, object_id=item.pk,
        defaults={'entry_name': CONTEXT_ENTRY, 'dept_belong_id': item.dept_belong_id})
    context = locked(context)
    before = snapshot(context)
    context.effects[key] = facts(value)
    persist(context, actor)
    record(context, key, before, actor, reason)
    return context


def origin(item):
    return {'entity': item._meta.label, 'source': snapshot(item)}


def view_effects(item):
    context = SourceDocumentContext.objects.filter(entity=item._meta.label, object_id=item.pk).first()
    return {} if context is None else {key: value for key, value in context.effects.items()
        if key in ['factory_quality', 'delivery_confirmation', 'card_adoption', 'material_return_origin',
                   'product_dispatch_origin', 'package_receipt_origin', 'order_transfer_origin', 'combined_process_sync', 'package_gray_origin', 'combine_link_origin',
                   'automatic_combine','gray_consumed','gray_operation','gray_lineage','combine_link_reversal',
                   'quality_rebuild','quality_rebuild_origin','quality_replaced','history_gray_recovery','history_gray_origin','progress_maintenance',
                   'execution_chain','chain_cancelled','chain_container','chain_compensation','execution_source',
                   'package_replacement','package_retained','package_pairing','package_label_sync',
                   'work_archive','work_archived','work_archive_copy',
                   'sample_variant','sample_schedule_origin','trial_work','trial_retained','trial_origin',
                   'shift_work','shift_retained','shift_origin','shift_master_sync','shift_trigger_check',
                   'calendar_generation','calendar_retained','calendar_origin',
                   'equipment_operation','equipment_retained','equipment_origin',
                   'cross_card_issue','cross_card_transfer','purchase_origin','purchase_return_origin',
                   'outwork_origin','outwork_dispatch_origin','outwork_receipt_origin','outwork_return_origin','outwork_closure']}
