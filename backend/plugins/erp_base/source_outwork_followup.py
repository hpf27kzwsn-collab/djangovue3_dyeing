"""结案后实际收退登记与重新核对；旧结案快照和损耗始终保留。"""
from django.apps import apps
from .business import locked,persist,record,snapshot
from .source_context import SourceDocumentContext
from .source_continuation import origin,save_effect
from .source_stock_services import raw
from .source_business_updates import matching
from .source_ownership import OWNERS
from .source_outwork_close import facts,closure
from .source_execution_state import active

ORIGINS=['outwork_dispatch_origin','outwork_receipt_origin','material_return_origin','product_dispatch_origin','outwork_return_origin']
APPLICATIONS=['OutWorkApply','SemiOutWorkApply']


def applications(source):
    pending=[source];seen=set();found={}
    while pending:
        row=pending.pop();identity=(row._meta.label,row.pk)
        if identity in seen:continue
        seen.add(identity)
        if row.SOURCE_TABLE in APPLICATIONS:found[identity]=row;continue
        for rule in OWNERS.get(row._meta.label,[]):
            model=apps.get_model(rule['target'])
            parent_id=getattr(row,rule['field']+'_id')
            if parent_id is not None:pending.extend(model.objects.filter(pk=parent_id))
            else:
                query=model.objects.all()
                for left,right in zip(rule['source_fields'],rule['target_fields']):query=matching(query,**{right:raw(row,left)})
                pending.extend(query)
        context=SourceDocumentContext.objects.filter(entity=row._meta.label,object_id=row.pk).first()
        if context is not None:
            for name in ORIGINS:
                if name in context.effects:
                    value=context.effects[name];pending.extend(apps.get_model(value['entity']).objects.filter(pk=value['source']['id']))
        # 原历史链缺少生成来源时，明确结案选择亦是可证明的关联。
        for context in SourceDocumentContext.objects.filter(effects__outwork_closure__reconciliation__sources__contains=[
                {'entity':row._meta.label,'source':{'id':row.pk}}]):
            model=apps.get_model(context.entity)
            if model.SOURCE_TABLE in APPLICATIONS:pending.extend(model.objects.filter(pk=context.object_id))
    return list(found.values())


def movement(source,target,actor,kind,at,reason):
    roots=applications(source)
    for application in roots:
        application=locked(application)
        context,_=SourceDocumentContext.objects.get_or_create(entity=application._meta.label,object_id=application.pk,
            defaults={'entry_name':'explicit_business_continuation'})
        before=snapshot(context)
        events=context.effects.setdefault('outwork_movements',[])
        event=facts({'number':len(events)+1,'kind':kind,'source':origin(source),'target':origin(target),'at':at,'reason':reason})
        events.append(event)
        value=context.effects.get('outwork_closure')
        if value is not None and value['state'] in ['closed','needs_review']:
            value['state']='needs_review'
        persist(context,actor);record(context,'outwork_followup',before,actor,reason or kind)
    if roots:save_effect(target,'outwork_applications',{'applications':[origin(row) for row in roots],'kind':kind,'at':at},actor,reason or kind)


def review(application,query):
    context=SourceDocumentContext.objects.filter(entity=application._meta.label,object_id=application.pk).first()
    effects={} if context is None else context.effects
    value=effects.get('outwork_closure');events=effects.get('outwork_movements',[])
    cursor=0 if value is None else value.get('movement_count',0)
    data=[];changes=[]
    for event in events:
        source=event['target'];model=apps.get_model(source['entity'])
        target=query(model.SOURCE_TABLE,model._meta.app_label).filter(pk=source['source']['id']).first()
        if target is None:continue
        data.append({'number':event['number'],'kind':event['kind'],'at':event['at'],'reason':event['reason'],
            'entity':model._meta.label,'record_id':target.pk,'legacy_id':target.legacy_id,
            'after_closure':value is not None and event['number']>cursor,'active':active(type(target).objects.filter(pk=target.pk)).exists(),
            **{name:raw(target,name) for name in ['SheetNo','SheetKind','WeightQty','Rolls'] if name in target.SOURCE_FIELDS}})
    if value is not None:
        selected=[]
        for source in value['reconciliation']['sources']:
            model=apps.get_model(source['entity'])
            selected.append((model,source['source']))
            if model.SOURCE_TABLE.endswith('Detail'):
                parent=apps.get_model(OWNERS[model._meta.label][0]['target'])
                selected.extend((parent,header) for header in source['headers'])
        checked=set()
        for model,saved in selected:
            identity=(model._meta.label,saved['id'])
            if identity in checked:continue
            checked.add(identity)
            row=query(model.SOURCE_TABLE,model._meta.app_label).filter(pk=saved['id']).first()
            if row is None:
                changes.append({'entity':model._meta.label,'record_id':saved['id'],'issue':'当前来源不可见或已删除，原结案快照仍保留。'});continue
            changed=[name for name in model.SOURCE_FIELDS.values() if getattr(row,name)!=model._meta.get_field(name).to_python(saved[name])]
            if changed or not active(type(row).objects.filter(pk=row.pk)).exists():
                changes.append({'entity':model._meta.label,'record_id':row.pk,'changed_fields':changed,'issue':'结案后原字段或活动状态已变化。'})
    return {'report':'外协结案后收退核对','rows':data,'supplemental_rows':changes,
        'closure_state':None if value is None else 'needs_review' if changes and value['state']=='closed' else value['state'],
        'closure_versions':len(effects.get('outwork_closure_history',[]))+(1 if value is not None else 0),
        'notes':['原结案保留当时收发和损耗快照；结案后新收退标为待复核，不阻止实际收退，也不自动认定新的损耗。',
            '重新结案应明确选择当前累计收发及实际退回；原历史版本保存在本单审计。']}
