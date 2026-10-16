"""拆合计划、采用关系和订单分配逆向；实际执行单据保留各自来源。"""
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import transaction
from .business import locked,snapshot
from .source_stock_services import raw
from .source_calculations import store_value
from .source_context import SourceDocumentContext
from .source_continuation import save_effect,origin
from .source_business_updates import matching,update_rows
from .source_operation_effects import restore


def effect(item,key):
    context=SourceDocumentContext.objects.filter(entity=item._meta.label,object_id=item.pk).first()
    if context is None or key not in context.effects:
        raise ValidationError({'source':'本记录没有该接续动作的前值；请使用明确原关系/分配转移办理，不猜测原归属。'})
    value=context.effects[key]
    if value.get('state')=='reversed':raise ValidationError({'source':'此接续动作已经撤回。'})
    return value


def require_current_plan(item):
    from .source_execution_state import require_available
    require_available(item)
    context=SourceDocumentContext.objects.filter(entity=item._meta.label,object_id=item.pk).first()
    if context is not None and any(context.effects.get(key,{}).get('state')=='reversed'
        for key in ['card_adoption','order_transfer_origin','combine_link_origin']):
        raise ValidationError({'source':'此计划或采用结果已经撤回并留档，请选择当前有效计划办理。'})


def patch_from_snapshot(item,before,after):
    return {'entity':item._meta.label,'id':item.pk,
        'before':{item.SOURCE_FIELDS[key]:before[item.SOURCE_FIELDS[key]] for key in after},
        'after':dict(store_value(item,key,value) for key,value in after.items())}


@transaction.atomic
def reverse_allocation(item,actor,at,reason):
    item=locked(item);value=effect(item,'order_transfer_origin')
    source_data=value['source']['source'];source=locked(apps.get_model(value['source']['entity']).objects.get(pk=source_data['id']))
    field=type(item)._meta.get_field('old_combine_qty');quantity=field.to_python(value['quantity'])
    original=field.to_python(source_data['old_combine_qty'])
    if raw(item,'CombineQty')!=quantity:
        raise ValidationError({'source':'目标分配量已有后续变更，请先撤回后续分配。'})
    expected=None if original is None or quantity is None else original-quantity
    restore([patch_from_snapshot(source,source_data,{'CombineQty':expected})],actor,reason)
    update_rows(type(item).objects.filter(pk=item.pk),{'CombineQty':0},actor,'allocation_reversed',reason)
    save_effect(item,'order_transfer_origin',{**value,'state':'reversed','reversed_at':at,'reverse_reason':reason},actor,reason)
    item.refresh_from_db();return item


@transaction.atomic
def reverse_link(item,actor,at,reason):
    item=locked(item);value=effect(item,'combine_link_origin')
    for key in ['Qty','Rolls']:
        field=item._meta.get_field(item.SOURCE_FIELDS[key])
        if raw(item,key)!=field.to_python(value['source']['source'][field.name]):
            raise ValidationError({'source':'采用的合卡关系已有后续数量变更，请先撤回后续办理。'})
    update_rows(type(item).objects.filter(pk=item.pk),{'Qty':0,'Rolls':0},actor,'combine_link_reversed',reason)
    save_effect(item,'combine_link_origin',{**value,'state':'reversed','reversed_at':at,'reverse_reason':reason},actor,reason)
    item.refresh_from_db();return item


def actual_references(item):
    values=[]
    for module,name,key,number in [
        ('erp_production','WProcess','JobSheetNo',raw(item,'SheetNo')),
        ('erp_production','StuffWeight','JobSheetNo',raw(item,'SheetNo')),
        ('erp_production','JobGrayRecord','SheetSeries',raw(item,'SheetSeries')),
        ('erp_warehouse','RecordYield','JobSheetNo',raw(item,'SheetNo')),
        ('erp_warehouse','ProdIn','JobSheetNo',raw(item,'SheetNo')),
        ('erp_warehouse','GrayOutDetail','JobSheetNo',raw(item,'SheetNo')),
        ('erp_warehouse','SemiOutDetail','JobSheetNo',raw(item,'SheetNo'))]:
        model=apps.get_model(module+'.SourceDye'+name)
        from .source_execution_state import active
        ids=list(matching(active(model.objects.all()),**{key:number}).values_list('pk',flat=True))
        if ids:values.append({'entity':model._meta.label,'ids':ids})
    return values


@transaction.atomic
def reverse_card(item,actor,mode,at,reason):
    item=locked(item);value=effect(item,'card_adoption');references=actual_references(item)
    if references and mode=='unstarted':
        raise ValidationError({'source':'此工卡已有实际执行单据；请先按各单据撤回，或明确选择仅撤回计划并保留实际单据。'})
    allocation=apps.get_model('erp_production.SourceDyeJobCombineOrder')
    pending=[]
    for row in matching(allocation.objects.all(),SheetSeries=raw(item,'SheetSeries')).order_by('-pk'):
        context=SourceDocumentContext.objects.filter(entity=row._meta.label,object_id=row.pk).first()
        entry=None if context is None else context.effects.get('order_transfer_origin')
        if entry is not None and entry.get('state')!='reversed':reverse_allocation(row,actor,at,reason)
        elif entry is None and raw(row,'CombineQty') not in [None,0]:pending.append(origin(row))
    if pending and mode=='unstarted':raise ValidationError({'source':'含没有转移前值的分配，请先明确转移；也可选择仅撤回计划保留此分配。'})
    if value['kind']=='split':
        source_data=value['source']['source'];source=locked(type(item).objects.get(pk=source_data['id']))
        restore([patch_from_snapshot(source,source_data,value['source_changes'])],actor,reason)
    if value['kind']=='merge':
        model=apps.get_model('erp_production.SourceDyeJobCombine')
        for member in value['members']:
            link=locked(model.objects.get(pk=member['target_id']))
            save_effect(link,'combine_link_reversal',{'before':origin(link),'at':at,'reason':reason},actor,reason)
            update_rows(model.objects.filter(pk=link.pk),{'Qty':0,'Rolls':0},actor,'combine_link_reversed',reason)
    before=origin(item)
    update_rows(type(item).objects.filter(pk=item.pk),{'PreVatQty':0,'PreRolls':0},actor,'card_plan_reversed',reason)
    save_effect(item,'card_adoption',{**value,'state':'reversed','reversed_at':at,'reverse_reason':reason,
        'reverse_mode':mode,'card_before_reverse':before,'actual_records_retained':references,'manual_allocations_retained':pending},actor,reason)
    item.refresh_from_db();return item
