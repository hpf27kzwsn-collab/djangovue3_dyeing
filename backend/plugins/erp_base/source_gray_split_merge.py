"""出库前坯料、出库后投坯细码拆合及原汇总回写；原参与行留档。"""
from plugins.erp_base.source_provenance import reference as source_reference
import re
from uuid import uuid4
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum
from .business import locked,persist,record,snapshot
from .source_stock_services import raw
from .source_business_updates import matching
from .source_context import SourceDocumentContext
from .source_continuation import save_effect,origin,copy_new
from .source_operation_effects import change,restore
from .source_calculations import store_value
from .source_numbers import reserve

MEASURES=['Rolls','WeightQty','LengthQty']


def rows(name,module='erp_warehouse'):
    return apps.get_model(module+'.SourceDye'+name).objects.all()


def active(query):
    from .source_execution_state import active as execution_active
    query=execution_active(query)
    consumed=SourceDocumentContext.objects.filter(entity=query.model._meta.label,effects__gray_consumed__active=True).values('object_id')
    return query.exclude(pk__in=consumed)


def require_active(item):
    if not active(type(item).objects.filter(pk=item.pk)).exists():
        raise ValidationError({'source':'此原行已参加合匹并留档，请使用合匹结果或先撤回原合匹。'})


def totals(query):
    result={key:query.aggregate(total=Sum(query.model.SOURCE_FIELDS[key]))['total'] for key in MEASURES}
    return {key:0 for key in MEASURES} if not query.exists() else result


def query_change(query,values,effects,actor,reason):
    for item in query.order_by('pk'):change(item,values,effects,actor,reason)


def refresh_receipts(receipts,split,effects,actor,reason):
    for receipt in dict.fromkeys(receipts):
        values=totals(active(matching(rows('GrayInRecord'),ReceSheetNo=receipt)))
        details=matching(rows('GrayInDetail'),ReceSheetNo=receipt)
        fields={'Rolls':values['Rolls']} if split else values
        query_change(details,fields,effects,actor,reason)
        for detail in details.order_by('pk'):
            books=matching(rows('GrayStockBook'),SheetSeries=raw(detail,'SheetSeries'),ReceSheetNo=receipt)
            if not split:books=matching(books,DetailNo=receipt)
            query_change(books,{'In'+key:value for key,value in fields.items()},effects,actor,reason)


def refresh_jobs(series_receipts,after,split,effects,actor,reason):
    for series,receipt in dict.fromkeys(series_receipts):
        source=active(matching(rows('JobGrayRecord','erp_production'),SheetSeries=series,ReceSheetNo=receipt))
        values=totals(source)
        if split and not after:
            values={'Rolls':active(matching(rows('GrayInRecord'),ReceSheetNo=receipt)).count()}
        query_change(matching(rows('JobAssign','erp_production'),SheetSeries=series,ReceSheetNo=receipt),values,effects,actor,reason)
    if after:
        for series in dict.fromkeys(pair[0] for pair in series_receipts):
            values=totals(active(matching(rows('JobGrayRecord','erp_production'),SheetSeries=series)))
            # 原过程先重量再长度，长度为正会覆盖PreVatQty；不擅自改为单位推测。
            for measure in ['WeightQty','LengthQty']:
                if values[measure] is not None and values[measure]>0:
                    fields={'PreRolls':values['Rolls'],'PreVatQty':values[measure],
                        'SumAssignedRolls':values['Rolls'],'SumAssigned'+measure:values[measure],
                        'SumProcessRolls':values['Rolls'],'SumProcess'+measure:values[measure]}
                    query_change(matching(rows('JobSheet','erp_production'),SheetSeries=series),fields,effects,actor,reason)


def new_identity(item,actor,after):
    roll,code=raw(item,'RollNo'),raw(item,'BarCode')
    base_roll=None if roll is None else roll[:3] if after else roll.split('-',1)[0]
    base_code=None if code is None else code[:16] if after else code.split('-',1)[0]
    query=matching(type(item).objects.all(),ReceSheetNo=raw(item,'ReceSheetNo'))
    def initial():
        if after:
            related=[row for row in query if (raw(row,'RollNo') or '')[:3]==(roll or '')[:3] and (raw(row,'BarCode') or '')[:16]==(code or '')[:16]]
            suffixes=[int(raw(row,'RollNo')[4:]) for row in related if raw(row,'RollNo') is not None and re.fullmatch('[0-9]+',raw(row,'RollNo')[4:])]
            return max([len(related)-1,*suffixes])
        suffixes=[]
        for value in query.values_list('old_roll_no',flat=True):
            if value is not None and base_roll is not None and value.startswith(base_roll+'-'):
                suffix=value[len(base_roll)+1:]
                if re.fullmatch('[0-9]+',suffix):suffixes.append(int(suffix))
        return max(suffixes,default=0)
    number=reserve(item,'gray_split',{'receipt':raw(item,'ReceSheetNo'),'roll':base_roll,'barcode':base_code,'after':after},initial,actor)
    suffix='-'+str(number)
    def generated(base,field):
        return None if base is None else base[:item._meta.get_field(field).max_length-len(suffix)]+suffix
    return generated(base_roll,'old_roll_no'),generated(base_code,'old_bar_code')


def operation_log(items,kind,job,actor,at,reason):
    from .source_services import write
    model=rows('GrayRecordCutLogs').model
    values={'old_id':str(uuid4()),'old_kind':kind,'old_job_sheet_no':None if job is None else raw(job,'SheetNo'),
        'old_operator':actor.name or actor.username,'old_operate_date':at,'old_status':0,'old_remarks':reason,'old_data_table_name':items[0].SOURCE_TABLE}
    for key,old in [('old_ori_rece_sheet_no_list','ReceSheetNo'),('old_ori_roll_no_list','RollNo'),('old_ori_bar_code_list','BarCode')]:
        full=','.join('[null]' if raw(item,old) is None else str(raw(item,old)) for item in items)
        limit=model._meta.get_field(key).max_length
        values[key]=full if limit is None else full[:limit]
    return write(model,values,actor=actor,apply_effects=False)


def add_copy(item,values,actor,effects):
    from .source_services import write
    data=copy_new(item,type(item));data.update(values)
    # 出库后的原表没有GraySpec/Num列；仅按最新字段复制。
    if item.SOURCE_TABLE=='JobGrayRecord':data['old_sheet_series']=raw(item,'SheetSeries')
    data['source_parent_1']=item.source_parent_1
    from .source_chain_reverse import capture
    with capture() as linked_changes:
        result=write(type(item),data,actor=actor,apply_effects=False)
    effects.extend(change for change in linked_changes if (change['entity'],change['id'])!=(result._meta.label,result.pk))
    result.refresh_from_db()
    return result


def issues(items,after):
    result=[]
    for item in items:
        for key in MEASURES:
            if raw(item,key) is None or raw(item,key)<0:result.append({'record_id':item.pk,'field':key,'value':raw(item,key),'issue':'原程序负值/空值限制，按明确异常事实继续保存'})
        if after:
            if raw(item,'AssignedNo') in [None,'']:result.append({'record_id':item.pk,'issue':'原出库后分支要求有AssignedNo，本次原值留存'})
            if matching(rows('ProdInRecord'),GrayBarCode=raw(item,'GrayBarCode')).exists():result.append({'record_id':item.pk,'issue':'已有成品入库引用；本次细码调整留档，成品原引用不改写'})
        elif raw(item,'AssignedNo') not in [None,'']:result.append({'record_id':item.pk,'issue':'原记录已有领用流水，既有收发单据保留'})
        if not after:
            assigned=active(matching(rows('JobGrayRecord','erp_production'),ReceSheetNo=raw(item,'ReceSheetNo'),GrayBarCode=raw(item,'BarCode')))
            out=totals(assigned)
            partial=any(out[key] is not None and out[key]>0 and raw(item,key) is not None and
                (raw(item,key)>0 if key=='Rolls' else raw(item,key)-out[key]>0) for key in MEASURES)
            if partial:result.append({'record_id':item.pk,'assigned_ids':list(assigned.values_list('pk',flat=True)),
                'assigned_quantities':out,'issue':'原合匹部分领用限制；本次明确调整留档，既有领用事实保留'})
    return result


@transaction.atomic
def split_record(item,actor,weight,length,rolls,job,at,reason):
    item=locked(item);require_active(item);after=item.SOURCE_TABLE=='JobGrayRecord'
    log=operation_log([item],0,job,actor,at,reason);before=origin(item);original_issues=issues([item],after);changes=[];created=[];job_pairs=[]
    new_roll,new_code=new_identity(item,actor,after)
    quantities=dict(store_value(item,key,value) for key,value in [('WeightQty',weight),('LengthQty',length),('Rolls',rolls)])
    data={**quantities,'old_roll_no':new_roll,'old_bar_code':new_code}
    if after:data.update(old_gray_bar_code=new_code,old_gunit=1,**dict([store_value(item,'Kg',quantities['old_weight_qty'])]))
    else:data.update(old_roll_no2=new_roll,old_cbz='剪')
    new=add_copy(item,data,actor,changes);created.append(origin(new))
    moved={key:raw(new,key) for key in MEASURES}
    remaining={key:None if raw(item,key) is None or moved[key] is None else raw(item,key)-moved[key] for key in MEASURES}
    if not after:remaining['CBz']='余'
    change(item,remaining,changes,actor,reason)
    if after:job_pairs.append((raw(item,'SheetSeries'),raw(item,'ReceSheetNo')))
    elif job is not None:
        selected=active(matching(rows('JobGrayRecord','erp_production'),SheetSeries=raw(job,'SheetSeries'),ReceSheetNo=raw(item,'ReceSheetNo'),RollNo=raw(item,'RollNo')))
        for assigned in selected.order_by('pk'):
            values=dict(store_value(assigned,key,moved[key]) for key in MEASURES)
            values.update(old_roll_no=new_roll,old_bar_code=new_code,old_gray_bar_code=new_code)
            child=add_copy(assigned,values,actor,changes);created.append(origin(child))
            change(assigned,{key:None if raw(assigned,key) is None or raw(child,key) is None else raw(assigned,key)-raw(child,key) for key in MEASURES},changes,actor,reason)
            job_pairs.append((raw(assigned,'SheetSeries'),raw(assigned,'ReceSheetNo')))
    if not after:refresh_receipts([raw(item,'ReceSheetNo')],True,changes,actor,reason)
    refresh_jobs(job_pairs,after,True,changes,actor,reason)
    value={'state':'applied','kind':'split','after_dispatch':after,'sources':[before],'changes':changes,'created':created,
        'issues':original_issues+issues([type(item).objects.get(pk=item.pk),new],after),'at':at,'reason':reason}
    save_effect(log,'gray_operation',value,actor,reason)
    retain_participants(log,value,actor,reason)
    complete_log(log,[before],[origin(type(item).objects.get(pk=item.pk)),*created],actor,reason)
    return log


@transaction.atomic
def merge_records(item,actor,members,job,at,reason):
    items=[locked(row) for row in {row.pk:row for row in [item,*members]}.values()]
    for row in items:require_active(row)
    after=item.SOURCE_TABLE=='JobGrayRecord';log=operation_log(items,1,job,actor,at,reason)
    sources=[origin(row) for row in items];changes=[];consumed=[];job_pairs=[]
    survivor=min(items,key=lambda row:('' if raw(row,'RollNo') is None else raw(row,'RollNo'),row.pk))
    combined={key:sum(values) if (values:=[raw(row,key) for row in items if raw(row,key) is not None]) else None for key in MEASURES}
    change(survivor,{**combined,**({} if after else {'CBz':None})},changes,actor,reason)
    for row in items:
        if row.pk!=survivor.pk:
            save_effect(row,'gray_consumed',{'active':True,'operation_id':log.pk,'survivor_id':survivor.pk,'before':origin(row)},actor,reason)
            consumed.append({'entity':row._meta.label,'id':row.pk})
        if after:job_pairs.append((raw(row,'SheetSeries'),raw(row,'ReceSheetNo')))
    if not after:
        refresh_receipts([raw(row,'ReceSheetNo') for row in items],False,changes,actor,reason)
        if job is not None:
            counterparts=[]
            for row in items:
                counterparts.extend(active(matching(rows('JobGrayRecord','erp_production'),SheetSeries=raw(job,'SheetSeries'),ReceSheetNo=raw(row,'ReceSheetNo'),RollNo=raw(row,'RollNo'))).order_by('pk'))
            counterparts=list({row.pk:row for row in counterparts}.values())
            for row in counterparts:
                if equal_identity(row,survivor):change(row,combined,changes,actor,reason)
                else:
                    save_effect(row,'gray_consumed',{'active':True,'operation_id':log.pk,'survivor_id':survivor.pk,'before':origin(row)},actor,reason)
                    consumed.append({'entity':row._meta.label,'id':row.pk})
                job_pairs.append((raw(row,'SheetSeries'),raw(row,'ReceSheetNo')))
    refresh_jobs(job_pairs,after,False,changes,actor,reason)
    value={'state':'applied','kind':'merge','after_dispatch':after,'sources':sources,'survivor_id':survivor.pk,
        'changes':changes,'created':[],'consumed':consumed,'issues':issues(items,after),'at':at,'reason':reason}
    save_effect(log,'gray_operation',value,actor,reason)
    retain_participants(log,value,actor,reason)
    complete_log(log,sources,[origin(type(survivor).objects.get(pk=survivor.pk))],actor,reason)
    return log


def equal_identity(left,right):
    return all(raw(left,key) is not None and raw(right,key) is not None and raw(left,key).rstrip(' ').upper()==raw(right,key).rstrip(' ').upper() for key in ['ReceSheetNo','RollNo'])


def retain_participants(log,value,actor,reason):
    participants={(entry['entity'],entry['source']['id']) for entry in [*value['sources'],*value['created']]}
    participants.update((entry['entity'],entry['id']) for entry in value['changes'] if entry['entity'].lower().endswith(('grayinrecord','jobgrayrecord')))
    participants.update((entry['entity'],entry['id']) for entry in value.get('consumed',[]))
    for entity,pk in sorted(participants):
        row=apps.get_model(entity).objects.get(pk=pk)
        context=SourceDocumentContext.objects.filter(entity=entity,object_id=pk).first()
        previous=[] if context is None else context.effects.get('gray_lineage',{}).get('operation_ids',[])
        save_effect(row,'gray_lineage',{'operation_ids':[*previous,log.pk],'at':value['at'],'reason':reason},actor,reason)


def complete_log(log,sources,results,actor,reason):
    def joined(entries,key):
        return ','.join('NULL' if entry['source'][key] is None else str(entry['source'][key]) for entry in entries)
    quantities=lambda entries:'；'.join(label+':'+joined(entries,key) for label,key in [('重量','old_weight_qty'),('长度','old_length_qty'),('粒数','old_rolls')])
    values={'NewReceSheetNoList':joined(results,'old_rece_sheet_no'),'NewRollNoList':joined(results,'old_roll_no'),
        'NewBarCodeList':joined(results,'old_bar_code'),'OriQtyList':quantities(sources),'NewQtyList':quantities(results)}
    values={old:value[:log._meta.get_field(log.SOURCE_FIELDS[old]).max_length] for old,value in values.items()}
    change(log,values,[],actor,reason)


@transaction.atomic
def undo_operation(item,actor,at,reason):
    item=locked(item)
    from .source_card_reverse import effect
    value=effect(item,'gray_operation')
    if value['state']!='applied':raise ValidationError({'source':'此细码拆合已经撤回。'})
    for created in value['created']:
        row=locked(apps.get_model(created['entity']).objects.get(pk=created['source']['id']))
        require_active(row)
        if any(snapshot(row)[key]!=created['source'][key] for key in row.SOURCE_FIELDS.values()):
            raise ValidationError({'source':'拆分生成行已有后续变更，请先撤回后续办理。'})
        code=raw(row,'GrayBarCode') if row.SOURCE_TABLE=='JobGrayRecord' else raw(row,'BarCode')
        if matching(rows('ProdInRecord'),GrayBarCode=code).exists():raise ValidationError({'source':'拆分结果已有成品入库引用，请先办理对应退回。'})
    restore(value['changes'],actor,reason)
    for entry in value.get('consumed',[]):
        row=locked(apps.get_model(entry['entity']).objects.get(pk=entry['id']))
        state=SourceDocumentContext.objects.get(entity=row._meta.label,object_id=row.pk).effects['gray_consumed']
        save_effect(row,'gray_consumed',{**state,'active':False,'reversed_at':at},actor,reason)
    for created in value['created']:
        row=apps.get_model(created['entity']).objects.get(pk=created['source']['id'])
        save_effect(row,'gray_consumed',{'active':True,'operation_id':item.pk,'reason':'拆分已撤回','before':origin(row)},actor,reason)
    save_effect(item,'gray_operation',{**value,'state':'reversed','reversed_at':at,'reverse_reason':reason},actor,reason)
    return item


def operation_report(item):
    context=SourceDocumentContext.objects.filter(entity=item._meta.label,object_id=item.pk).first()
    if context is None or 'gray_operation' not in context.effects:
        return {'report':'原细码拆合日志','rows':[{'record_id':item.pk,'source': source_reference(item),**{old:raw(item,old) for old in item.SOURCE_FIELDS}}],
            'notes':['原日志原样展示；缺少逐行前值时不能猜测恢复，由明确的细码调整继续办理。']}
    value=context.effects['gray_operation']
    results=[{'entity':entry['entity'],'record_id':entry['source']['id'],'role':'拆分生成'} for entry in value['created']]
    if value['kind']=='merge':results.append({'entity':value['sources'][0]['entity'],'record_id':value['survivor_id'],'role':'合并结果'})
    return {'report':'细码拆合办理结果','rows':[{'record_id':item.pk,'state':value['state'],'kind':value['kind'],'after_dispatch':value['after_dispatch'],
        'source_count':len(value['sources']),'created_count':len(value['created']),'at':value['at'],'reason':value['reason']}],
        'result_rows':results,'supplemental_rows':value['issues'],'notes':['原参与行全部留档；合匹消耗行及已撤回的拆分结果保留原字段，活动细码汇总排除这些行。','按此办理记录ID可在坯料细码拆合日志中查看或撤回。']}
