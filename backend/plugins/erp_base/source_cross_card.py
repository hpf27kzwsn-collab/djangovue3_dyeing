"""跨卡再加工和实际退领；明确采用原单据，不把计划拆合变成虚构库存。"""
from django.apps import apps
from django.db import transaction
from .business import locked
from .source_calculations import store_value, product
from .source_continuation import copy_new, origin, save_effect
from .source_stock_services import raw
from .source_business_updates import matching, update_rows
from .source_execution_state import require_available, active


def rows(name, module='erp_warehouse'):
    return apps.get_model(module+'.SourceDye'+name).objects.all()


@transaction.atomic
def reprocess(job, actor, review, quantity, rolls, unit, sheet_kind, job_kind, processes, at, reason):
    from .source_job_flow import create_card
    from . import source_services as services
    job=locked(job);require_available(job)
    if review is not None:
        review=locked(review);require_available(review)
    target,adopted=create_card(job,actor,quantity,rolls,unit,at,reason,processes)
    # 原LossStr指向评审单SheetNo；空号/同号多单仍由完整原记录ID补充追溯。
    update_rows(type(target).objects.filter(pk=target.pk),{
        'LossStr':None if review is None else raw(review,'SheetNo'),
        'SheetKind':sheet_kind,'JobKindID':job_kind},actor,'reprocess_plan',reason)
    target.refresh_from_db()
    save_effect(target,'card_adoption',{'kind':'reprocess','source':origin(job),
        'review':None if review is None else origin(review),'processes':adopted,'unit':unit,
        'quantity_deducted':False,'at':at,'reason':reason},actor,reason)
    services.finish([target],actor)
    return target


@transaction.atomic
def issue_receipt(item, actor, target, weight, length, rolls, warehouse, unit, sheet_kind, at, reason, issue_number=None):
    from . import source_services as services
    from .source_card_reverse import require_current_plan
    item,target=locked(item),locked(target)
    require_available(item);require_current_plan(target)
    gray=item.SOURCE_TABLE=='GrayInDetail'
    table='GrayOut' if gray else 'SemiOut'
    head_model,line_model=rows(table).model,rows(table+'Detail').model
    header={'_entry':table+'Job','old_sheet_date':at,'old_sheet_kind':sheet_kind,
        'old_ware_house_id':warehouse,'old_stock_unit':unit,'old_remarks':reason}
    head=services.write(head_model,header,actor=actor,apply_effects=False)
    values=copy_new(item,line_model,['SheetSeries','AssignedNo','DetailNo','Rolls','LengthQty','WeightQty','Amount'])
    values.update(source_parent_1=head,old_job_sheet_no=raw(target,'SheetNo'))
    if issue_number is not None:values[line_model.SOURCE_FIELDS['AssignedNo' if gray else 'DetailNo']]=issue_number
    if gray:values['old_job_sheet_series']=raw(target,'SheetSeries')
    values.update(store_value(line_model(),key,value) for key,value in [('WeightQty',weight),('LengthQty',length),
        ('Rolls',rolls),('Amount',product(raw(item,'Price'),weight))])
    line=services.write(line_model,values,actor=actor,apply_effects=False)
    save_effect(head,'cross_card_issue',{'source':origin(item),'target':origin(target),
        'line_id':line.pk,'at':at,'reason':reason},actor,reason)
    # 显式工卡记录优先于同号其他工卡；原单据码完整保留。
    save_effect(line,'execution_source',{'job_id':target.pk,'job':origin(target),'source':origin(item),
        'at':at,'reason':reason},actor,reason)
    save_effect(head,'execution_source',{'job_id':target.pk,'job':origin(target),'source':origin(item),
        'at':at,'reason':reason},actor,reason)
    services.finish([head],actor)
    return head


@transaction.atomic
def transfer_issue(item, actor, source_job, target, weight, length, rolls, warehouse, unit,
                   return_kind, issue_kind, customer, at, reason, issue_number=None):
    from .source_delivery_flow import return_material
    from .source_card_reverse import require_current_plan
    item,source_job,target=locked(item),locked(source_job),locked(target)
    for row in [item,source_job]:require_available(row)
    require_current_plan(target)
    returned=return_material(item,actor,weight=weight,length=length,rolls=rolls,warehouse=warehouse,
        unit=unit,sheet_kind=return_kind,customer=customer,at=at,reason=reason)
    incoming=rows(returned.SOURCE_TABLE+'Detail').get(source_parent_1=returned)
    issued=issue_receipt(incoming,actor,target,weight,length,rolls,warehouse,unit,issue_kind,at,reason,issue_number)
    save_effect(returned,'execution_source',{'job_id':source_job.pk,'job':origin(source_job),
        'source':origin(item),'at':at,'reason':reason},actor,reason)
    save_effect(incoming,'execution_source',{'job_id':source_job.pk,'job':origin(source_job),
        'source':origin(item),'at':at,'reason':reason},actor,reason)
    save_effect(issued,'cross_card_transfer',{'state':'applied','source':origin(item),
        'source_job':origin(source_job),'target':origin(target),'return':origin(returned),
        'return_line_id':incoming.pk,'at':at,'reason':reason},actor,reason)
    return issued


def dependents(job, query):
    """跨卡实物退领建立的后续卡依赖；下游已撤销后可继续上游。"""
    from .source_context import SourceDocumentContext
    found={}
    for context in SourceDocumentContext.objects.filter(effects__cross_card_transfer__source_job__source__id=job.pk):
        value=context.effects['cross_card_transfer']
        head_model=apps.get_model(context.entity)
        if not active(query(head_model.SOURCE_TABLE,head_model._meta.app_label)).filter(pk=context.object_id).exists():continue
        target_id=value['target']['source']['id']
        if target_id==job.pk:continue
        target=query('JobSheet','erp_production').filter(pk=target_id).first()
        if target is not None:found[target.pk]=target
    return list(found.values())


def reprocess_links(job, query):
    from .source_context import SourceDocumentContext
    result=[]
    for context in SourceDocumentContext.objects.filter(entity=job._meta.label,
            effects__card_adoption__source__source__id=job.pk):
        value=context.effects['card_adoption']
        if value['kind'] not in ['split','reprocess'] or value.get('state')=='reversed':continue
        result.extend(query('JobSheet','erp_production').filter(pk=context.object_id))
    # 合卡的非首张来源不一定出现在OriSourceJobNo，逐条成员原ID建立依赖。
    for context in SourceDocumentContext.objects.filter(entity=job._meta.label,
            effects__card_adoption__members__contains=[{'source':{'entity':job._meta.label,'source':{'id':job.pk}}}]):
        if context.effects['card_adoption'].get('state')!='reversed':
            result.extend(query('JobSheet','erp_production').filter(pk=context.object_id))
    return result


def require_upstream_available(job, query):
    """恢复下游前，上游计划和实际退料必须处于可用状态。"""
    from .source_context import SourceDocumentContext
    from .source_card_reverse import require_current_plan
    from django.shortcuts import get_object_or_404
    upstream=set()
    context=SourceDocumentContext.objects.filter(entity=job._meta.label,object_id=job.pk).first()
    adoption={} if context is None else context.effects.get('card_adoption',{})
    if adoption.get('kind') in ['split','reprocess']:upstream.add(adoption['source']['source']['id'])
    elif adoption.get('kind')=='merge':upstream.update(row['source']['source']['id'] for row in adoption['members'])
    for context in SourceDocumentContext.objects.filter(effects__cross_card_transfer__target__source__id=job.pk):
        upstream.add(context.effects['cross_card_transfer']['source_job']['source']['id'])
    for pk in upstream-{job.pk}:
        require_current_plan(get_object_or_404(query('JobSheet','erp_production'),pk=pk))
