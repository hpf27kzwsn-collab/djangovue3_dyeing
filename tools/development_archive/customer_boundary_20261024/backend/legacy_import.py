"""仅采用已明确的主档字段；未确认关联和业务状态列入对照事项。"""
import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from django.db import models
from . import models as base
from plugins.erp_base.legacy_models import LegacyObjectMap
from .legacy_services import issue,source_path
from plugins.erp_base.business import persist

RULES={
    'p_FieldValid':(base.BusinessChoice,{'namespace':'FieldType','code':'Code','name':'Name','numeric_value':'NumValue','sort':'SortValue','is_active':'IsStop'}, {'is_active':'invert_bool'}),
    'p_Shift':(base.Shift,{'code':'ShiftID','name':'Name'},{}),
    'h_Employee':(base.Employee,{'code':'EmpID','name':'Name','english_name':'NameE','mobile':'Mobile','card_identifier':'RFID',
        'joined_on':'InDate','left_on':'OutDate','is_active':'IsOut'},{'is_active':'invert_bool'}),
    'p_Customer':(base.Party,{'code':'CustomerID','name':'NameC','english_name':'NameE','short_name':'ShortName','mnemonic':'Mnemonic',
        'phone':'Tel','fax':'Fax','email':'Email','website':'WebSite','automatic_packaging':'IsAbroad','orders_enabled':'EnableOrders',
        'is_active':'IsStop','stopped_at':'StopDate'},{'is_active':'invert_bool'}),
    'p_Machine':(base.Machine,{'code':'MachineID','number':'MachineNo','name':'Name','workshop_code':'WorkShopID',
        'capacity_description':'Capacity','load_capacity_kg':'MinVatQty','maximum_pieces':'MaxRolls','maximum_spindles':'MAxSpindles',
        'bath_ratio':'Rate','manufacturer':'Manufacturer','controller_number':'SequenceNo','is_scheduled':'IsProcess','is_active':'IsStop'},{'is_active':'invert_bool'}),
}

FINANCE_CHOICES={'APKind','ARKind','AccountAge','Bank','Currency','Insurance','MoneyInKind','MoneyOutKind','Payment','Settle','ExpressSettle','ReimBursement','PayGrade','OrderFree'}
RELATION_SOURCES={
    'p_FieldValid':{'parent':'ParentCode'},'p_Shift':{},
    'h_Employee':{'department':'DeptID','business_unit':'BusinessUnitID','shift':'ShiftID'},
    'p_Customer':{'parent':'ParentCustID','salesperson':'SalerID','category':'CustKindID','default_label':'LabelID'},
    'p_Machine':{'business_unit':'BusinessUnitID','work_center':'StationID','machine_kind':'MachineKindID'},
}


def comparison_value(field,value,conversion):
    if value is None:return None
    if conversion=='invert_bool':
        if not isinstance(value,bool):raise ValidationError('源停用标志不是已确认的 SQL bit。')
        return not value
    if isinstance(field,models.DateTimeField):
        fraction=value.partition('.')[2]
        if len(fraction)>6 and any(c!='0' for c in fraction[6:]):raise ValidationError('源日期精度高于新模型微秒，保留完整归档，暂不舍入。')
        result=datetime.fromisoformat(value)
        return timezone.make_aware(result,ZoneInfo('Asia/Shanghai')) if timezone.is_naive(result) else result
    return field.to_python(value)


@transaction.atomic
def import_row(batch,table,row,actor):
    model,fields,conversions=RULES[table.table_name]
    label=model._meta.label
    if table.table_name=='p_FieldValid' and row['values']['FieldType'] in FINANCE_CHOICES:return None
    # 原形模型逐行承接，转换到通用主档失败也不丢原行或合并重复记录。
    from .source_import import source_model
    original_model=source_model(table)
    from .source_import import original_values
    raw=original_values(original_model,row)
    original,created=original_model.objects.get_or_create(source_batch=batch,source_row=row['row'],defaults={
        **raw,
        'approval_stage':None,'creator':actor,'modifier':actor,'dept_belong_id':actor.dept_id})
    persist(LegacyObjectMap.objects.get_or_create(source_table=table,row_number=row['row'],target_model=original_model._meta.label,
        defaults={'source_key':row['key'],'target_id':original.pk,'mapped_fields':{
            original_model.SOURCE_FIELDS[k]:{'source':k,'conversion':'identity'} for k in row['values']}})[0],actor)
    if row['key'] is None:
        issue(batch,table,actor,'no_primary_key','没有原主键，已逐行承接原形模型；不按业务码合并到通用主档。',row,label);return original
    previous=LegacyObjectMap.objects.filter(source_table=table,row_number=row['row'],target_model=label).first()
    if previous is not None:return model.objects.get(pk=previous.target_id)
    values={};mapping={}
    for field,source in fields.items():
        mapping[field]={'source':source,'conversion':conversions.get(field,'identity')}
        try:values[field]=comparison_value(model._meta.get_field(field),row['values'][source],mapping[field]['conversion'])
        except ValidationError as error:
            issue(batch,table,actor,'source_value',str(error),row,label,field,row['values'][source]);return original
    mappings=LegacyObjectMap.objects.filter(source_table__batch__database_name=batch.database_name,
        source_table__schema_name=table.schema_name,source_table__table_name=table.table_name,
        source_key=row['key'],target_model=label)
    if mappings.filter(source_table=table).exists():
        issue(batch,table,actor,'duplicate_source_key','同批次重复原键已分别承接原形模型，不合并原行。',row,label);return original
    targets=list(mappings.order_by().values_list('target_id',flat=True).distinct())
    if len(targets)>1:
        issue(batch,table,actor,'ambiguous_source_key','原键对应多个已采用主档；原行已承接，不猜测覆盖。',row,label);return original
    existing=model.objects.get(pk=targets[0]) if targets else None
    if existing is not None:
        changed=[key for key,value in values.items() if getattr(existing,key)!=value]
        if changed:
            issue(batch,table,actor,'changed_source','来源与已经导入或人工维护的新值不一致；原形模型保存本次原值，不覆盖主档。',row,label,value=changed);return original
        item=existing
    else:
        item=model(**values)
        try:item.full_clean()
        except ValidationError as error:
            issue(batch,table,actor,'model_validation',str(error),row,label,value=row['values']);return original
        persist(item,actor)
    persist(LegacyObjectMap(source_table=table,row_number=row['row'],source_key=row['key'],target_model=label,target_id=item.pk,mapped_fields=mapping),actor)
    batch.import_issues.filter(source_table=table,row_number=row['row'],target_model=label,category__in=['model_validation','source_value']).update(is_resolved=True,handling='字段复刻修订后已原值导入。')
    for field,source in RELATION_SOURCES[table.table_name].items():
        value=row['values'][source]
        if value not in [None,'']:
            issue(batch,table,actor,'unmapped_relation','原关联完整保留在来源；新旧组织、代码或模板对应尚未采用，不猜测外键。',row,label,field,value)
    return item


def import_masters(batch,actor):
    counts={}
    for name in RULES:
        table=batch.source_tables.get(table_name=name)
        count={'original_rows':0,'adopted_rows':0,'original_only_rows':0,'excluded_finance':0}
        expected=set(RULES[name][1].values());actual={column['field_name'] for column in table.columns}
        missing=expected-actual
        if missing:raise ValueError('当前来源已变更，先修订明确字段映射：'+name+' '+','.join(sorted(missing)))
        with source_path(table).open(encoding='utf-8') as source:
            for line in source:
                item=import_row(batch,table,json.loads(line),actor)
                if item is None:
                    count['excluded_finance']+=1
                else:
                    count['original_rows']+=1
                    count['adopted_rows' if isinstance(item,RULES[name][0]) else 'original_only_rows']+=1
        counts[name]=count
    link_relations(batch,actor)
    return counts


@transaction.atomic
def link_relations(batch,actor):
    """第二遍采用已确认的代码关联，目标必须是同批次导入的唯一原记录。"""
    relations={
        'p_FieldValid':{'parent':('ParentCode',base.BusinessChoice,'p_FieldValid','code')},
        'h_Employee':{'shift':('ShiftID',base.Shift,'p_Shift','code')},
        'p_Customer':{'parent':('ParentCustID',base.Party,'p_Customer','code'),
            'salesperson':('SalerID',base.Employee,'h_Employee','code'),
            'category':('CustKindID',base.BusinessChoice,'p_FieldValid','code')},
    }
    from .legacy_services import rows
    for mapping in LegacyObjectMap.objects.filter(source_table__batch=batch,source_table__table_name__in=relations,
        target_model__in=[RULES[name][0]._meta.label for name in relations]).select_related('source_table'):
        model,_,_=RULES[mapping.source_table.table_name]
        target=model.objects.get(pk=mapping.target_id)
        original=rows(mapping.source_table,mapping.row_number,1)[0]
        for field,(column,related,table,key) in relations[mapping.source_table.table_name].items():
            value=original['values'][column]
            if value in [None,'']:continue
            ids=LegacyObjectMap.objects.filter(source_table__batch=batch,source_table__table_name=table,target_model=related._meta.label).values('target_id')
            query=related.objects.filter(pk__in=ids,**{key:value})
            if related is base.BusinessChoice:
                query=query.filter(namespace=target.namespace if isinstance(target,base.BusinessChoice) else 'CustKind')
            matches=list(query)
            if len(matches)!=1:continue  # 对应事项已经随原记录保存，保持未采用。
            match=matches[0]
            current=getattr(target,field+'_id')
            if current is not None and current!=match.pk:
                issue(batch,mapping.source_table,actor,'changed_relation','人工关联与旧代码对应不同，不覆盖。',original,model._meta.label,field,value)
                continue
            setattr(target,field,match);persist(target,actor)
            mapping.mapped_fields={**mapping.mapped_fields,field:{'source':column,'conversion':'foreign_code','target_attribute':key}}
            persist(mapping,actor)
            batch.import_issues.filter(source_table=mapping.source_table,row_number=mapping.row_number,field_name=field,category='unmapped_relation').update(is_resolved=True,handling='已采用同批次来源的唯一代码对应。')
