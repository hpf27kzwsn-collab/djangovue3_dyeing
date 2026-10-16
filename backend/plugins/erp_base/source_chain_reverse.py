"""工卡执行链撤销：原单留档、实际库存反记、明确回写及撤销恢复。"""
from plugins.erp_base.source_provenance import reference as source_reference
from contextlib import contextmanager
from contextvars import ContextVar
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from .business import locked,persist,record,snapshot
from .source_stock_services import raw
from .source_business_updates import matching,update_rows
from .source_continuation import origin,save_effect
from .source_context import SourceDocumentContext
from .source_ownership import OWNERS
from .source_execution_state import active,require_available

_changes=ContextVar('chain_reverse_changes',default=None)
ORIGINS=['package_receipt_origin','product_dispatch_origin','material_return_origin',
    'outwork_dispatch_origin','outwork_receipt_origin','outwork_return_origin']
BOOKS={'StuffOut':'StuffStockBook','StuffIn':'StuffStockBook','GrayOut':'GrayStockBook','GrayIn':'GrayStockBook',
       'SemiOut':'SemiStockBook','SemiIn':'SemiStockBook','ProdOut':'ProdStockBook','ProdIn':'ProdStockBook'}
MEASURES={'Qty','Money','Rolls','Packs','WeightQty','LengthQty','GrayQty','NetKg'}
DIRECT={'WProcess','StuffWeight','RecordYield','ProdIn','GrayOutDetail','SemiOutDetail','StuffOut',
        'ProdOutDetail','JobGrayRecord','ColoringCheck','DyeCheckout','CarryMaterialDetail'}
LINKABLE=DIRECT|set(BOOKS)|set(BOOKS.values())|{'ProdInRecord','ProdOutRecord','GrayOutRecord','SemiOutRecord',
    'StuffWeightPhase','StuffWeightDetail','WProcessStep','JobShiftEmp','ColorShiftEmp'}


def capture_change(item,before,after):
    changes=_changes.get()
    if changes is None or before.get('exists') is False:return
    if isinstance(item,SourceDocumentContext):
        left,right=before['effects'],after['effects']
        changed={key:{'before_exists':key in left,'before':left.get(key),'after_exists':key in right,'after':right.get(key)}
            for key in left.keys()|right.keys() if left.get(key)!=right.get(key) or (key in left)!=(key in right)}
        if changed:changes.append({'entity':item._meta.label,'id':item.pk,'effect_changes':changed})
        return
    fields=list(item.SOURCE_FIELDS.values()) if hasattr(item,'SOURCE_FIELDS') else []
    changed=[key for key in fields if before[key]!=after[key]]
    if changed:changes.append({'entity':item._meta.label,'id':item.pk,
        'before':{key:before[key] for key in changed},'after':{key:after[key] for key in changed}})


@contextmanager
def capture():
    changes=[];token=_changes.set(changes)
    try:yield changes
    finally:_changes.reset(token)


def source_models():
    return {key:m for m in apps.get_models() if hasattr(m,'SOURCE_TABLE') for key in [m.SOURCE_TABLE,m.__name__.removeprefix('SourceDye')]}


def identity(item):return (item._meta.label,item.pk)


def sources(query,model):
    return query(model.SOURCE_TABLE,model._meta.app_label)


def reader(name,module):return apps.get_model(module+'.SourceDye'+name).objects.all()


@transaction.atomic
def link_source(job,actor,source_table,record_id,at,reason,query=reader):
    job=locked(job);require_available(job)
    model=source_models()[source_table]
    row=locked(get_object_or_404(sources(query,model),pk=record_id));require_available(row)
    save_effect(row,'execution_source',{'job_id':job.pk,'job':origin(job),'source':origin(row),'at':at,'reason':reason},actor,reason)
    return job


def related(query,rule,parent):
    selected=query.filter(**{rule['field']:parent})
    old=query
    for key,target in zip(rule['source_fields'],rule['target_fields']):
        value=raw(parent,target);field=query.model._meta.get_field(query.model.SOURCE_FIELDS[key])
        old=matching(old,**{key:value}) if field.get_internal_type() in ['CharField','TextField'] else old.filter(**{field.name:value}) if value is not None else old.none()
    # 明确附加外键优先；历史没有附加外键时按完整原归属键连接。
    return selected | old.filter(**{rule['field']+'__isnull':True})


def discover(job,query=reader):
    models=source_models();nodes={};containers={};edges=[];notes=[];issues=[]
    def add(item,parent=None,via='原工卡号'):
        key=identity(item)
        owner=SourceDocumentContext.objects.filter(entity=item._meta.label,object_id=item.pk).first()
        explicit=None if owner is None else owner.effects.get('execution_source')
        if explicit is not None and explicit['job_id']!=job.pk:return False
        if parent is not None:edges.append({'from':list(identity(parent)),'to':list(key),'via':via})
        if key not in nodes:nodes[key]=item;return True
        return False
    number=raw(job,'SheetNo');series=raw(job,'SheetSeries')
    for name in sorted(DIRECT):
        model=models[name];key='SheetSeries' if name=='JobGrayRecord' else 'JobSheetNo'
        other_owners=SourceDocumentContext.objects.filter(entity=model._meta.label,
            effects__execution_source__job_id__isnull=False).exclude(effects__execution_source__job_id=job.pk).values('object_id')
        for row in matching(active(sources(query,model)),**{key:series if key=='SheetSeries' else number}).exclude(pk__in=other_owners).order_by('pk'):add(row,job)
    adopted_books={}
    for context in SourceDocumentContext.objects.filter(effects__execution_source__job_id=job.pk):
        model=apps.get_model(context.entity)
        for row in active(sources(query,model)).filter(pk=context.object_id):
            if model.SOURCE_TABLE in BOOKS.values():adopted_books[identity(row)]=row
            else:add(row,job,'明确采用原记录；原业务码不改写')
    from .source_cross_card import dependents,reprocess_links
    adopted=SourceDocumentContext.objects.filter(entity=job._meta.label,effects__card_adoption__isnull=False).values('object_id')
    children=[*matching(sources(query,type(job)),OriSourceJobNo=number).exclude(pk=job.pk).exclude(pk__in=adopted),
        *dependents(job,query),*reprocess_links(job,query)]
    other_jobs={child.pk:child for child in children if child.pk!=job.pk}.values()
    for child in other_jobs:
        context=SourceDocumentContext.objects.filter(entity=child._meta.label,object_id=child.pk).first()
        if context is None or (context.effects.get('card_adoption',{}).get('state')!='reversed' and context.effects.get('execution_chain',{}).get('state')!='applied'):
            issues.append({'entity':child._meta.label,'record_id':child.pk,'issue':'另有拆卡/返修子卡，请先从该子卡撤销，保留独立来源和实际数量'})
    handled=set()
    while True:
        pending=[row for key,row in nodes.items() if key not in handled]
        if not pending:break
        for item in pending:
            handled.add(identity(item))
            for label,rules in OWNERS.items():
                for rule in rules:
                    if rule['target']==item._meta.label:
                        model=apps.get_model(label)
                        for child in related(active(sources(query,model)),rule,item).order_by('pk'):add(child,item,'明细归属')
            for rule in OWNERS.get(item._meta.label,[]):
                parent_model=apps.get_model(rule['target'])
                if parent_model.SOURCE_TABLE=='JobSheet':continue
                parents=sources(query,parent_model)
                parent_id=getattr(item,rule['field']+'_id')
                if parent_id is not None:parents=parents.filter(pk=parent_id)
                else:
                    for child_key,parent_key in zip(rule['source_fields'],rule['target_fields']):
                        value=raw(item,child_key);field=parent_model._meta.get_field(parent_model.SOURCE_FIELDS[parent_key])
                        parents=matching(parents,**{parent_key:value}) if field.get_internal_type() in ['CharField','TextField'] else parents.filter(**{field.name:value}) if value is not None else parents.none()
                for parent in parents:
                    containers[identity(parent)]=parent
                    children=list(related(active(sources(query,type(item))),rule,parent))
                    if children and all(identity(child) in nodes for child in children):add(parent,item,'全部该类明细已在范围')
            links=[]
            if item.SOURCE_TABLE=='StuffWeight':links=[('StuffOut',{'WeightSheetNo':raw(item,'SheetNo')})]
            elif item.SOURCE_TABLE=='ProdIn':
                links=[('ProdOutDetail',{'InSheetNo':raw(item,'SheetNo'),'JobSheetNo':raw(item,'JobSheetNo')}),
                    ('ProdIn',{'ProdInOriSheetNo':raw(item,'SheetNo'),'JobSheetNo':raw(item,'JobSheetNo')})]
            elif item.SOURCE_TABLE=='ProdOutDetail':links=[('ProdIn',{'ProdOutSheetSeries':raw(item,'SheetSeries'),'JobSheetNo':raw(item,'JobSheetNo')})]
            elif item.SOURCE_TABLE=='WProcess':links=[(name,{'WProcessNo':raw(item,'WProcessNo')}) for name in ['WProcessStep','JobShiftEmp']]
            elif item.SOURCE_TABLE=='ColoringCheck':links=[('ColorShiftEmp',{'WProcessNo':raw(item,'WProcessNo'),'JobSheetNo':raw(item,'JobSheetNo')})]
            for table,values in links:
                for linked in matching(active(sources(query,models[table])),**values).order_by('pk'):add(linked,item,'完整原业务码')
            anchors=[item]
            if item.SOURCE_TABLE=='RecordYield':
                from .source_package_operations import replaced_sources
                anchors+=replaced_sources(item,query)
            for anchor in anchors:
                for key in ORIGINS:
                    contexts=SourceDocumentContext.objects.filter(**{f'effects__{key}__entity':anchor._meta.label,f'effects__{key}__source__id':anchor.pk})
                    for context in contexts:
                        model=apps.get_model(context.entity)
                        for linked in active(sources(query,model)).filter(pk=context.object_id):
                            add(linked,item,key if anchor.pk==item.pk else f'包装替换前原记录#{anchor.pk}：{key}')
            context=SourceDocumentContext.objects.filter(entity=item._meta.label,object_id=item.pk).first()
            if context is not None:
                if item.SOURCE_TABLE=='ColoringCheck':
                    for linked in active(sources(query,models['ColorShiftEmp'])).filter(pk__in=context.effects.get('color_staff',[])):
                        add(linked,item,'本次对色人员来源')
                for key in ['semi_records','derived_records']:
                    for label,ids in context.effects.get(key,{}).items():
                        for linked in active(sources(query,apps.get_model(label))).filter(pk__in=ids):add(linked,item,key)
    for book in adopted_books.values():
        for head_name,book_name in BOOKS.items():
            if book.SOURCE_TABLE!=book_name:continue
            for head in active(matching(sources(query,models[head_name]),SheetSeries=raw(book,'SheetSeries'))):
                containers[identity(head)]=head
    # 共用表头不退出活动范围，只冻结本次原流水对应；其他工卡明细照常保留。
    shared={key:row for key,row in containers.items() if key not in nodes}
    ledgers=dict(adopted_books)
    explicitly_shared={}
    from .source_auto_combine import equal
    for key,item in {**containers,**nodes}.items():
        table=item.SOURCE_TABLE
        if table not in BOOKS:continue
        books=matching(sources(query,models[BOOKS[table]]),SheetSeries=raw(item,'SheetSeries'))
        if table+'Detail' in models:
            selected=[row for row in nodes.values() if row.SOURCE_TABLE==table+'Detail' and equal(raw(row,'SheetSeries'),raw(item,'SheetSeries'))]
            detail_key={'GrayOut':'AssignedNo','GrayIn':'ReceSheetNo','SemiIn':'ReceSheetNo'}.get(table,'DetailNo')
            detail_numbers=[raw(row,detail_key) for row in selected]
            all_numbers=list(matching(sources(query,models[table+'Detail']),SheetSeries=raw(item,'SheetSeries')).values_list(models[table+'Detail'].SOURCE_FIELDS[detail_key],flat=True))
        else:detail_numbers=all_numbers=None
        compensation=SourceDocumentContext.objects.filter(entity=books.model._meta.label,effects__chain_compensation__isnull=False).values('object_id')
        for book in books.exclude(pk__in=compensation).order_by('pk'):
            association=SourceDocumentContext.objects.filter(entity=book._meta.label,object_id=book.pk).first()
            adopted=None if association is None else association.effects.get('execution_source')
            if adopted is not None:
                if adopted['job_id']==job.pk:ledgers[identity(book)]=book
                else:explicitly_shared[key]=item
                continue
            if detail_numbers is not None and not any(equal(raw(book,'DetailNo'),value) for value in detail_numbers):
                if any(equal(raw(book,'DetailNo'),value) for value in all_numbers):continue
                if key in shared:
                    issues.append({'entity':book._meta.label,'record_id':book.pk,'issue':'共用表头有无法对应明细的实际库存流水，需先明确该流水归属；不按比例猜分'})
                    continue
                notes.append(f'{book._meta.label}#{book.pk}缺少对应明细，按完整原表头流水归属反记并保留异常来源')
            ledgers[identity(book)]=book
        if not books.exists():notes.append(f'{item._meta.label}#{item.pk}没有匹配原库存流水；保留单据，不从计划量补造库存')
    for key,head in explicitly_shared.items():
        nodes.pop(key,None);shared[key]=head;containers[key]=head
    for row in shared.values():notes.append(f'{row._meta.label}#{row.pk}含其他明细或明确采用的其他工卡流水，原表头保留，仅撤销本卡已列明来源')
    for line in nodes.values():
        head_name=line.SOURCE_TABLE.removesuffix('Detail')
        if not line.SOURCE_TABLE.endswith('Detail') or head_name not in BOOKS:continue
        if matching(sources(query,models[head_name]),SheetSeries=raw(line,'SheetSeries')).exists():continue
        detail_key={'GrayOut':'AssignedNo','GrayIn':'ReceSheetNo','SemiIn':'ReceSheetNo'}.get(head_name,'DetailNo')
        orphan_books=matching(sources(query,models[BOOKS[head_name]]),SheetSeries=raw(line,'SheetSeries'),DetailNo=raw(line,detail_key))
        compensation=SourceDocumentContext.objects.filter(entity=orphan_books.model._meta.label,effects__chain_compensation__isnull=False).values('object_id')
        for book in orphan_books.exclude(pk__in=compensation):
            association=SourceDocumentContext.objects.filter(entity=book._meta.label,object_id=book.pk).first()
            adopted=None if association is None else association.effects.get('execution_source')
            if adopted is None or adopted['job_id']==job.pk:ledgers[identity(book)]=book
        notes.append(f'{line._meta.label}#{line.pk}缺少表头；按流水及明细号匹配实际库存，原孤立明细完整保留')
    return {'nodes':nodes,'containers':shared,'heads':{key:row for key,row in {**containers,**nodes}.items() if row.SOURCE_TABLE in BOOKS},
        'ledgers':ledgers,'edges':edges,'issues':issues,'notes':notes}


def preview(job,query=reader):
    data=discover(job,query)
    from .source_package_labels import related_operations
    from .source_package_operations import check_scope,effect
    labels=[]
    for job_id in related_operations(data['nodes'].values()):
        owner=reader('JobSheet','erp_production').get(pk=job_id)
        targets=[apps.get_model(row['entity']).objects.get(pk=row['id']) for row in effect(owner,'package_label_sync')['changes']]
        check_scope([owner,*targets],query)
        labels.extend({'label_sync_job_id':job_id,'record_id':row.pk,'table':row.SOURCE_TABLE,'effect':'先恢复本次标签同步前字段，含跨卡同条码目标和工位回写'} for row in targets)
    return {'report':'工卡执行整链撤销预览','rows':[{'entity':row._meta.label,'record_id':row.pk,'source': source_reference(row),
        'table':row.SOURCE_TABLE,'effect':'原单留档，退出活动办理'} for row in data['nodes'].values()],
        'result_rows':[{'entity':row._meta.label,'record_id':row.pk,'source': source_reference(row),
            **{name:raw(row,name) for name in row.SOURCE_FIELDS if name in ['WareHouseID','LotNo','StorageUnitIDs','JobSheetNo'] or name[2:] in MEASURES and name.startswith('In') or name[3:] in MEASURES and name.startswith('Out')}} for row in data['ledgers'].values()],
        'supplemental_rows':labels+data['issues']+[{'source_entity':edge['from'][0],'source_id':edge['from'][1],
            'target_entity':edge['to'][0],'target_id':edge['to'][1],'relation':edge['via']} for edge in data['edges']],
        'links':data['edges'],'notes':data['notes']+[
            '撤销顺序：交付/退回及实际库存→包装/称料/报工→进度回写→所选拆合计划。全部原行和原键及来源信息保留。',
            '反向流水使用原流水数量与维度；NULL仍为NULL，负数反向为正数；无流水不按计划补造。']}


def compensate(book,job,actor,at,reason):
    from .source_services import write,managed_fields
    data={field:getattr(book,field) for field in book.SOURCE_FIELDS.values() if field not in managed_fields(type(book))}
    for name,field in book.SOURCE_FIELDS.items():
        if (name.startswith('In') and name[2:] in MEASURES) or (name.startswith('Out') and name[3:] in MEASURES):
            value=raw(book,name);data[field]=None if value is None else -value
    data[book.SOURCE_FIELDS['BookDate']]=at
    for name in ['CurrDate','AccDate']:
        if name in book.SOURCE_FIELDS:data[book.SOURCE_FIELDS[name]]=at
    entry=write(type(book),data,actor=actor,apply_effects=False)
    save_effect(entry,'chain_compensation',{'job_id':job.pk,'source':origin(book),'at':at,'reason':reason},actor,reason)
    return entry


def projections(job,nodes,actor,work_mode):
    from .source_work_delete import trigger_removed,maintain_removed
    from .source_workflow_services import refresh_product_inbound
    for row in nodes:
        context=SourceDocumentContext.objects.filter(entity=row._meta.label,object_id=row.pk).first()
        if context is None:continue
        for key in ['delivery_confirmation','factory_quality','material_issue']:
            if key not in context.effects:continue
            value=context.effects[key]
            state={'state':'reversed'} if key=='material_issue' else {'result':'withdrawn'}
            save_effect(row,key,{**value,**state,'reversed_by_job_id':job.pk,'reverse_reason':'工卡执行整链撤销'},actor,'撤回对应办理事实，原快照保留')
    work=[row for row in nodes if row.SOURCE_TABLE=='WProcess']
    for row in sorted(work,key=lambda row:row.pk,reverse=True):
        context=SourceDocumentContext.objects.get(entity=row._meta.label,object_id=row.pk)
        save_effect(row,'chain_cancelled',{**context.effects['chain_cancelled'],'active':True},actor,'逐条撤销刷卡后执行原回写')
        trigger_removed(row,actor,retain_children=True)
        if work_mode=='trigger_then_maintenance':maintain_removed(row,actor,retain_children=True)
    for row in nodes:
        if row.SOURCE_TABLE=='ProdIn':refresh_product_inbound(row,actor)
    # QC原聚合字段按仍活动包装重算；无包装时原COUNT=0，SUM=NULL。
    packages=matching(active(reader('RecordYield','erp_warehouse')),JobSheetNo=raw(job,'SheetNo'))
    from django.db.models import Count
    if any(row.SOURCE_TABLE=='RecordYield' for row in nodes):
        values=packages.aggregate(PDots=Sum('old_dots'),Pkg=Sum('old_kg'),PRolls=Count('old_bar_code'),PlengthQyt=Sum('old_yard'))
        update_rows(type(job).objects.filter(pk=job.pk),values,actor,'chain_package_totals','按剩余活动包装汇总')
        if not packages.exists():
            processes=matching(reader('JobProcess','erp_production'),SheetSeries=raw(job,'SheetSeries'),ProcessID='GX98')
            reported=matching(active(reader('WProcess','erp_production')),JobSheetNo=raw(job,'SheetNo'),ProcessID='GX98')
            if not reported.exists():update_rows(processes,{'Status':'0','StartTime':None,'EndTime':None,'WPWorker':None},actor,
                'chain_package_progress','包装和GX98实际报工均已撤销，清理包装开工投影；原前值保留')
    issue_lines=[row for row in nodes if row.SOURCE_TABLE in ['GrayOutDetail','SemiOutDetail']]
    if issue_lines:
        models=source_models();heads=[]
        for table in ['GrayOutDetail','SemiOutDetail']:
            remaining=matching(active(sources(reader,models[table])),JobSheetNo=raw(job,'SheetNo'))
            for line in remaining:
                for head in matching(active(sources(reader,models[table[:-6]])),SheetSeries=raw(line,'SheetSeries')):
                    heads.append(head)
        if heads:
            # 原保存钩子按一张单据回写，不跨StockUnit汇总不同单据。
            head=max(heads,key=lambda row:(raw(row,'SheetDate') is not None,raw(row,'SheetDate'),row.pk))
            remaining=matching(active(sources(reader,models[head.SOURCE_TABLE+'Detail'])),SheetSeries=raw(head,'SheetSeries'),JobSheetNo=raw(job,'SheetNo'))
            values=remaining.aggregate(SumAssignedWeightQty=Sum('old_weight_qty'),SumAssignedRolls=Sum('old_rolls'),SumAssignedPacks=Sum('old_packs'))
        else:values=dict.fromkeys(['SumAssignedWeightQty','SumAssignedRolls','SumAssignedPacks'])
        update_rows(type(job).objects.filter(pk=job.pk),values,actor,'chain_issue_totals','按最后一张剩余实际领用单回写；无单据时保留SQL空汇总')
        for line in issue_lines:
            if line.SOURCE_TABLE!='GrayOutDetail':continue
            assignments=matching(reader('JobAssign','erp_production'),SheetSeries=raw(job,'SheetSeries'),ReceSheetNo=raw(line,'ReceSheetNo'))
            remaining=matching(active(reader('GrayOutDetail','erp_warehouse')),JobSheetNo=raw(job,'SheetNo'),ReceSheetNo=raw(line,'ReceSheetNo'))
            approved=any(matching(active(reader('GrayOut','erp_warehouse')),SheetSeries=raw(row,'SheetSeries')).filter(old_right_status=10).exists() for row in remaining)
            update_rows(assignments,{'Status':1 if approved else 0},actor,'chain_assignment_status','按剩余审核领用单回写')
            outputs=[row for row in nodes if row.SOURCE_TABLE=='GrayOutRecord' and raw(row,'AssignedNo')==raw(line,'AssignedNo')]
            for output in outputs:
                tags=matching(reader('GrayInRecord','erp_warehouse'),ReceSheetNo=raw(line,'ReceSheetNo'),BarCode=raw(output,'BarCode'),AssignedNo=raw(line,'AssignedNo'))
                if raw(output,'RollNo') not in [None,'']:tags=matching(tags,RollNo=raw(output,'RollNo'))
                survivors=matching(active(reader('GrayOutRecord','erp_warehouse')),ReceSheetNo=raw(line,'ReceSheetNo'),BarCode=raw(output,'BarCode'))
                if raw(output,'RollNo') not in [None,'']:survivors=matching(survivors,RollNo=raw(output,'RollNo'))
                if not survivors.exists():update_rows(tags,{'AssignedNo':None,'JobSheetNo':None},actor,'chain_gray_release','无剩余对应出库细码，解除本次实际领用')


@transaction.atomic
def cancel(job,actor,mode,work_mode,at,reason,query=reader):
    job=locked(job);require_available(job)
    previous=SourceDocumentContext.objects.filter(entity=job._meta.label,object_id=job.pk).first()
    if previous is not None and previous.effects.get('execution_chain',{}).get('state')=='applied':
        raise ValidationError({'source':'本工卡整链撤销已生效，不能重复反记库存。'})
    data=discover(job,query)
    if query is not reader:
        complete=discover(job,reader)
        if any(set(data[key])!=set(complete[key]) for key in ['nodes','containers','ledgers']) or data['issues']!=complete['issues']:
            raise ValidationError({'scope':'当前权限没有覆盖整条关联链，不能只撤销其中可见部分。'})
    if data['issues']:raise ValidationError({'source':[row['issue']+f"：{row['entity']}#{row['record_id']}" for row in data['issues']]})
    from .source_package_labels import related_operations,undo as undo_labels
    with capture() as label_changes:
        for job_id in related_operations(data['nodes'].values()):
            undo_labels(reader('JobSheet','erp_production').get(pk=job_id),actor,at,reason,query)
    nodes=[locked(row) for key,row in sorted(data['nodes'].items())]
    containers=[locked(row) for key,row in sorted(data['heads'].items())]
    books=[locked(row) for key,row in sorted(data['ledgers'].items())]
    before=[origin(row) for row in nodes];states=[]
    for flag,items in [('chain_cancelled',nodes),('chain_container',[job,*containers,*books])]:
        for row in items:
            context=SourceDocumentContext.objects.filter(entity=row._meta.label,object_id=row.pk).first()
            cancelled=None if context is None else context.effects.get('chain_cancelled')
            if cancelled and cancelled['active'] and cancelled['job_id']!=job.pk:
                raise ValidationError({'source':'关联记录已经由另一条链撤销，请先撤回该次办理。'})
            states.append({'entity':row._meta.label,'id':row.pk,'flag':flag,'previous':None if context is None else context.effects.get(flag)})
            previous=states[-1]['previous'];owners=[] if previous is None or not previous.get('active') else previous['job_ids']
            save_effect(row,flag,{'active':not (flag=='chain_cancelled' and row.SOURCE_TABLE=='WProcess'),
                'job_id':job.pk,'job_ids':[*owners,job.pk],'at':at,'reason':reason},actor,reason)
    reversals=[origin(compensate(book,job,actor,at,reason)) for book in books]
    with capture() as changes:
        projections(job,nodes,actor,work_mode)
        if mode=='execution_and_plan':
            from .source_card_reverse import reverse_card
            reverse_card(job,actor,'plan_only',at,reason)
        for change in changes:
            model=apps.get_model(change['entity'])
            if hasattr(model,'SOURCE_TABLE') and not sources(query,model).filter(pk=change['id']).exists():
                raise ValidationError({'scope':'进度或数量回写涉及当前权限外来源，本次整链撤销全部回滚。'})
    save_effect(job,'execution_chain',{'state':'applied','mode':mode,'work_mode':work_mode,'at':at,'reason':reason,
        'sources':before,'source_books':[origin(row) for row in books],'states':states,'compensations':reversals,
        'after_sources':[origin(type(row).objects.get(pk=row.pk)) for row in nodes],
        'changes':[*label_changes,*changes],'notes':data['notes'],'links':data['edges']},actor,reason)
    return {'report':'工卡执行整链撤销结果','rows':[{'job_id':job.pk,'retained_count':len(nodes),'compensation_count':len(reversals),'mode':mode}],
        'supplemental_rows':data['issues'],'notes':data['notes']}


@transaction.atomic
def undo(job,actor,at,reason,query=reader):
    from .source_card_reverse import effect
    from .source_operation_effects import restore
    job=locked(job);value=effect(job,'execution_chain')
    from .source_cross_card import require_upstream_available
    require_upstream_available(job,query)
    for entry in value['states']:
        current=SourceDocumentContext.objects.get(entity=entry['entity'],object_id=entry['id']).effects[entry['flag']]
        if current['active'] and current['job_ids'][-1]!=job.pk:
            raise ValidationError({'source':'共用单据已有另一工卡的后续撤销，请按实际办理先后倒序撤回。'})
    for entry in [*value['states'],*value['changes']]:
        model=apps.get_model(entry['entity'])
        if hasattr(model,'SOURCE_TABLE') and not sources(query,model).filter(pk=entry['id']).exists():
            raise ValidationError({'scope':'当前权限没有覆盖本次撤销涉及的完整来源，不能只恢复部分链条。'})
    # 原库存反记保留，撤回再生成反向记录，使原数量恢复且完整轨迹可核对。
    for source in [*value['after_sources'],*value['source_books'],*value['compensations']]:
        row=locked(apps.get_model(source['entity']).objects.get(pk=source['source']['id']))
        if any(getattr(row,field)!=row._meta.get_field(field).to_python(source['source'][field]) for field in row.SOURCE_FIELDS.values()):
            raise ValidationError({'source':f'{row._meta.label}#{row.pk}的原字段已有后续修改，请先处理该变更。'})
    for change in reversed(value['changes']):
        if 'effect_changes' not in change:
            restore([change],actor,reason);continue
        context=locked(SourceDocumentContext.objects.get(pk=change['id']));before=snapshot(context)
        for key,values in change['effect_changes'].items():
            if (key in context.effects)!=values['after_exists'] or context.effects.get(key)!=values['after']:
                raise ValidationError({'source':'对应拆合办理事实已有后续变化，请先撤回后续操作。'})
            if values['before_exists']:context.effects[key]=values['before']
            else:context.effects.pop(key)
        persist(context,actor);record(context,'chain_restore_fact',before,actor,reason)
    recovered=[]
    for entry in value['compensations']:
        row=locked(apps.get_model(entry['entity']).objects.get(pk=entry['source']['id']))
        recovered.append(origin(compensate(row,job,actor,at,reason)))
    for entry in value['states']:
        row=apps.get_model(entry['entity']).objects.get(pk=entry['id'])
        save_effect(row,entry['flag'],entry['previous'] or {'active':False,'reversed_at':at},actor,reason)
    save_effect(job,'execution_chain',{**value,'state':'reversed','reversed_at':at,'reverse_reason':reason,'recovery_books':recovered},actor,reason)
    return job
