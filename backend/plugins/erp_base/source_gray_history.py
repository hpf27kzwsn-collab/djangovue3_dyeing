"""历史细码日志解析、缺失行留档及有明确结果来源的历史逆向。"""
from plugins.erp_base.source_provenance import reference as source_reference
import re
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction
from .business import locked,persist,record
from .source_stock_services import raw
from .source_continuation import origin,save_effect
from .source_gray_split_merge import rows,active,require_active,refresh_receipts,refresh_jobs
from .source_business_updates import matching
from .source_calculations import store_value
from .source_context import SourceDocumentContext
from .source_operation_effects import change,restore

QUANTITIES={'重量':'WeightQty','长度':'LengthQty','匹数':'Rolls','粒数':'Rolls'}


def parts(value):
    return [] if value is None else value.split(',')


def quantities(value,measure):
    values={};issues=[]
    if value is None:return values,issues
    labelled=any(label in value for label in QUANTITIES)
    sections=re.split('[；;]',value) if labelled else [value]
    for section in sections:
        if labelled:
            match=re.fullmatch(r'\s*(重量|长度|匹数|粒数)\s*[:：](.*)',section)
            if match is None:issues.append('无法识别数量段：'+section);continue
            field=QUANTITIES[match[1]];text=match[2]
        else:field='unclassified_quantity' if measure=='unknown' else measure;text=section
        parsed=[]
        for token in parts(text):
            token=token.strip()
            if token.upper() in ['NULL','[NULL]','']:parsed.append(None)
            elif re.fullmatch(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)',token):parsed.append(Decimal(token))
            else:parsed.append(None);issues.append('无法转换的原数量片段：'+token)
        values[field]=parsed
    if not labelled and measure=='unknown':issues.append('旧日志未标数量种类，原数量保留，需明确重量/长度/粒数后才能应用逆向')
    return values,issues


def parse_side(item,side,measure):
    receipt=parts(raw(item,side+'ReceSheetNoList'));roll=parts(raw(item,side+'RollNoList'));barcode=parts(raw(item,side+'BarCodeList'))
    amounts,issues=quantities(raw(item,side+'QtyList'),measure)
    count=max([len(receipt),len(roll),len(barcode),*[len(values) for values in amounts.values()]])
    if side=='New' and not receipt and raw(item,'Kind')==0:receipt=parts(raw(item,'OriReceSheetNoList'))
    if len(receipt)==1 and count>1:receipt=receipt*count
    for name,values in [('ReceSheetNo',receipt),('RollNo',roll),('BarCode',barcode),*amounts.items()]:
        if values and len(values)!=count:issues.append(f'{side}.{name}有{len(values)}项，记录数为{count}，按原位置保存缺项')
    result=[]
    for index in range(count):
        row={'position':index+1,'side':side}
        for field,values in [('ReceSheetNo',receipt),('RollNo',roll),('BarCode',barcode),*amounts.items()]:
            if index<len(values):row[field]=values[index]
        result.append(row)
    return result,issues


def preview(item,measure='unknown'):
    original,first=parse_side(item,'Ori',measure);after,second=parse_side(item,'New',measure)
    status=raw(item,'Status');table=raw(item,'DataTableName')
    notes=['日志原文、失败状态和缺项全部保留；未记录的物料、单位、领用及库位不按经验补造。']
    if status!=0:
        notes.append('此日志未记录成功状态，不能当作已发生的拆合冲销；可恢复已记录的来源资料留档。')
        after=[{'side':'failed','raw_payload':{name:raw(item,name) for name in ['NewReceSheetNoList','NewRollNoList','NewBarCodeList','NewQtyList','Remarks']}}]
    if table=='JobGrayRecord':notes.append('JobGrayRecord入口既可能用于出库前选坯，也可能出库后操作，办理时明确选择阶段与工卡。')
    return {'report':'历史细码拆合恢复依据','rows':original,'result_rows':after,
        'supplemental_rows':[{'issue':issue} for issue in first+second],
        'source': source_reference(item),'log_id':item.pk,'old_status':status,'old_table':table,'old_kind':raw(item,'Kind'),'notes':notes}


def current_values(item):
    return {key:raw(item,key) for key in ['ReceSheetNo','RollNo','BarCode','WeightQty','LengthQty','Rolls']}


def same_record(row,values):
    from .source_auto_combine import equal
    return equal(raw(row,'ReceSheetNo'),values.get('ReceSheetNo')) and equal(raw(row,'RollNo'),values.get('RollNo')) and (
        'BarCode' not in values or values['BarCode'] is None or equal(raw(row,'BarCode'),values['BarCode']))


@transaction.atomic
def recover(item,actor,stage,mode,measure,job,current,at,reason):
    item=locked(item);data=preview(item,measure)
    context=SourceDocumentContext.objects.filter(entity=item._meta.label,object_id=item.pk).first()
    if context is not None and 'gray_operation' in context.effects:
        raise ValidationError({'source':'本日志已有新系统完整前值，使用本次细码拆合撤回动作。'})
    if context is not None and context.effects.get('history_gray_recovery',{}).get('state')=='applied':
        raise ValidationError({'source':'本日志已办理恢复；先撤回该恢复记录再重新办理。'})
    after=stage=='after';model=rows('JobGrayRecord','erp_production').model if after else rows('GrayInRecord').model
    if after and job is None:raise ValidationError({'job':'历史日志没有工卡流水，请明确恢复所用工卡。'})
    current=[locked(row) for row in current]
    if any(type(row) is not model for row in current):raise ValidationError({'current':'选择的当前细码必须属于本次恢复阶段。'})
    for row in current:require_active(row)
    if mode=='reverse':
        if data['old_status']!=0:raise ValidationError({'source':'原记录不是成功操作，不能冲销未发生的业务。'})
        if data['old_kind'] not in [0,1]:raise ValidationError({'source':'原日志不是已证实的拆分或合并类型；先恢复资料留档。'})
        if data['supplemental_rows']:raise ValidationError({'source':'原日志数量/位置存在未确定项，先核对恢复依据或只恢复留档。'})
        if len(current)!=len(data['result_rows']):raise ValidationError({'current':'必须逐条选定日志对应的全部当前结果细码；缺失结果不能冲销当前库存。'})
        unused=list(current)
        for expected in data['result_rows']:
            matches=[row for row in unused if same_record(row,expected)]
            if len(matches)!=1:raise ValidationError({'current':'日志结果存在重复或未匹配身份，请先明确当前来源。'})
            row=matches[0];unused.remove(row)
            if after and raw(row,'SheetSeries')!=raw(job,'SheetSeries'):raise ValidationError({'job':'选定结果不属于本次明确工卡。'})
            for key in ['WeightQty','LengthQty','Rolls']:
                if key in expected and raw(row,key)!=store_value(row,key,expected[key])[1]:
                    raise ValidationError({'current':f'细码{row.pk}的{key}已不同于日志结果，请先撤回后续办理。'})
    originals=data['rows'];missing=[row for row in originals if row.get('ReceSheetNo') in [None,''] or row.get('RollNo') in [None,'']]
    if missing or not originals:raise ValidationError({'source':'原日志没有完整收料号/卷号身份，不能生成对应原表行；原文仍可查询。'})
    created=[];changes=[];consumed=[]
    for original in originals:
        values=dict(store_value(model(),key,original[key]) for key in ['ReceSheetNo','RollNo','BarCode','WeightQty','LengthQty','Rolls'] if key in original)
        if after:values.update(old_sheet_series=raw(job,'SheetSeries'),old_gray_bar_code=original.get('BarCode'),source_parent_1=job)
        row=persist(model(**values),actor)
        record(row,'restore_history_gray',{'exists':False},actor,reason)
        save_effect(row,'history_gray_origin',{'log':origin(item),'logged_values':original,'missing_fields':[key for key in model.SOURCE_FIELDS if model.SOURCE_FIELDS[key] not in values],
            'mode':mode,'at':at,'reason':reason},actor,reason)
        if mode=='archive':save_effect(row,'gray_consumed',{'active':True,'operation_id':item.pk,'reason':'历史恢复留档，未应用当前库存'},actor,reason)
        created.append(origin(row))
    if mode=='reverse':
        for row in current:
            state=SourceDocumentContext.objects.filter(entity=row._meta.label,object_id=row.pk).first()
            previous=None if state is None else state.effects.get('gray_consumed')
            save_effect(row,'gray_consumed',{'active':True,'operation_id':item.pk,'reason':'历史逆向，原结果留档'},actor,reason)
            consumed.append({'entity':row._meta.label,'id':row.pk,'previous':previous,'source':origin(row)})
        receipts=list(dict.fromkeys([row['ReceSheetNo'] for row in originals]+[raw(row,'ReceSheetNo') for row in current]))
        if after:refresh_jobs([(raw(job,'SheetSeries'),receipt) for receipt in receipts],True,False,changes,actor,reason)
        else:refresh_receipts(receipts,False,changes,actor,reason)
    value={'state':'applied','stage':stage,'mode':mode,'measure':measure,'log':origin(item),'created':created,'consumed':consumed,
        'changes':changes,'issues':data['supplemental_rows'],'at':at,'reason':reason}
    save_effect(item,'history_gray_recovery',value,actor,reason)
    return {'report':'历史细码恢复办理结果','rows':[{'log_id':item.pk,'mode':mode,'created_count':len(created),'consumed_count':len(consumed)}],
        'result_rows':[{'entity':row['entity'],'record_id':row['source']['id']} for row in created],
        'supplemental_rows':data['supplemental_rows'],'notes':['恢复行只采用已知原字段，旧细码ID未记录时不伪造；旧日志ID保留在来源事实中。',
            '留档模式不参与库存；逆向模式仅按所选当前结果和已知字段恢复，不补造旧库缺失的其他字段。']}


@transaction.atomic
def undo_recovery(item,actor,at,reason):
    from django.apps import apps
    from .source_card_reverse import effect
    from .business import snapshot
    item=locked(item);value=effect(item,'history_gray_recovery')
    for entry in value['created']:
        row=locked(apps.get_model(entry['entity']).objects.get(pk=entry['source']['id']))
        if any(snapshot(row)[field]!=entry['source'][field] for field in row.SOURCE_FIELDS.values()):
            raise ValidationError({'source':'恢复细码已有后续字段改变，请先撤回后续办理。'})
        if value['mode']=='reverse':require_active(row)
    restore(value['changes'],actor,reason)
    for entry in value['consumed']:
        row=locked(apps.get_model(entry['entity']).objects.get(pk=entry['id']))
        save_effect(row,'gray_consumed',entry['previous'] or {'active':False,'reversed_at':at},actor,reason)
    for entry in value['created']:
        row=apps.get_model(entry['entity']).objects.get(pk=entry['source']['id'])
        save_effect(row,'gray_consumed',{'active':True,'operation_id':item.pk,'reason':'历史恢复已撤回'},actor,reason)
    save_effect(item,'history_gray_recovery',{**value,'state':'reversed','reversed_at':at,'reverse_reason':reason},actor,reason)
    return item
