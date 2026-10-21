"""旧DataColumn公式的明确求值：只读取登记表达式，逐字段报告缺失来源。"""
import re
from sqlglot import exp,parse_one
from sqlglot.errors import ParseError
from django.core.exceptions import ValidationError
from django.db import transaction,DatabaseError
from .source_entry_registry import ENTRY_RULES
from .source_phase6_entries import bindings
from .source_ownership import OWNERS
from .source_business_updates import matching
from .source_stock_services import raw
from .source_static_lookup import execute_table


def linked(query,child_fields,parent,parent_fields):
    for child,field in zip(child_fields,parent_fields):
        value=raw(parent,field)
        if value is None:return query.none()
        if isinstance(value,str):query=matching(query,**{child:value})
        else:query=query.filter(**{query.model.SOURCE_FIELDS[child]:value})
    return query


def parent_for(item,reader):
    from django.apps import apps
    candidates=[]
    for rule in OWNERS.get(item._meta.label,[]):
        model=apps.get_model(rule['target']);query=reader(model.__name__.removeprefix('SourceDye'),model._meta.app_label)
        key=getattr(item,rule['field']+'_id')
        if key is not None:candidates.extend(query.filter(pk=key))
        else:candidates.extend(linked(query,rule['target_fields'],item,rule['source_fields']))
    if len(candidates)!=1:raise ValueError('父行不是唯一来源，候选：'+str([{'model':v._meta.label,'id':v.pk} for v in candidates]))
    return candidates[0]


def child_rows(item,target,reader,trail=()):
    from django.apps import apps
    if target==item._meta.label:return [item]
    if target in trail:return []
    model=apps.get_model(target);result={}
    for rule in OWNERS.get(target,[]):
        for parent in child_rows(item,rule['target'],reader,(*trail,target)):
            query=reader(model.__name__.removeprefix('SourceDye'),model._meta.app_label)
            rows=query.filter(**{rule['field']:parent})|linked(query,rule['source_fields'],parent,rule['target_fields'])
            for row in rows.order_by('pk'):result[row.pk]=row
    return list(result.values())


def expression(item,entry,text,reader):
    from django.apps import apps
    values={};counter=0
    def aggregate(match):
        nonlocal counter
        operation,relation,field=match.groups()
        child=relation.removeprefix(entry+'_')
        candidates=[label for name,labels in bindings().items() if name.lower()==child.lower() for label in labels if field in apps.get_model(label).SOURCE_FIELDS]
        if len(candidates)!=1:raise ValueError('子关系无法唯一对应：'+relation+'.'+field+'；候选：'+str(candidates))
        rows=child_rows(item,candidates[0],reader);present=[raw(row,field) for row in rows if raw(row,field) is not None]
        value=len(present) if operation.lower()=='count' else sum(present) if present else None
        key='_aggregate'+str(counter);counter+=1;values[key]=value
        return '['+key+']'
    text=re.sub(r'(sum|count)\s*\(\s*Child\(([^)]+)\)\.\[([^]]+)\]\s*\)',aggregate,text,flags=re.I)
    tree=parse_one(text,read='tsql')
    for node in list(tree.find_all(exp.Column)):
        if node.table.lower()=='parent':value=raw(parent_for(item,reader),node.name)
        elif node.table:raise ValueError('未确定的连接投影字段：'+node.sql())
        elif node.name in values:value=values[node.name]
        else:
            fields={name.lower():name for name in item.SOURCE_FIELDS}
            if node.name.lower() not in fields:raise ValueError('原表没有公式来源字段：'+node.name)
            value=raw(item,fields[node.name.lower()])
        replacement=exp.convert(value)
        if node is tree:tree=replacement
        else:node.replace(replacement)
    return execute_table('SELECT '+tree.sql(dialect='tsql')+' AS result',reader,include_retained=True)['rows'][0][0]


def evaluate(item,entry,reader):
    if entry not in ENTRY_RULES.get(item._meta.label,{}):raise ValidationError({'entry':'此记录没有所选入口公式。'})
    rows=[];changes={}
    for field,spec in ENTRY_RULES[item._meta.label][entry]['formula_fields'].items():
        row={'field':field,'expression':spec['expression'],'before':raw(item,field),'generate_time':spec['generate_time']}
        try:
            with transaction.atomic():
                if item.SOURCE_TABLE=='DyeRecipe' and entry in ['BulkDyeRecipe','FinishDyeRecipe','TrialDyeRecipe'] and field=='Cost':
                    from .source_sampling_services import recipe_cost
                    value=recipe_cost(item,reader)
                else:value=expression(item,entry,spec['expression'],reader)
        except (ValueError,KeyError,ParseError,DatabaseError,ArithmeticError) as error:
            row.update(state='unresolved',issue=str(error))
        else:
            row.update(state='calculated',value=value);changes[item.SOURCE_FIELDS[field]]=value
        rows.append(row)
    return {'report':'旧入口公式逐字段核对','entry':entry,'rows':rows,'changes':changes,
        'notes':['各公式读取同一份保存前原值；互相引用的公式不自动迭代。缺来源或原式无法计算的字段列出原因，保持原值。']}


@transaction.atomic
def calculate(item,entry,reader,actor,apply=False):
    from .business import locked,record,snapshot
    from .source_services import write,managed_fields
    from .source_provenance import is_historical
    item=locked(item)
    reader(type(item).__name__.removeprefix('SourceDye'),item._meta.app_label).get(pk=item.pk)
    from .source_execution_state import active
    result=evaluate(item,entry,lambda name,module:active(reader(name,module)))
    result['notes'].append('本次公式使用活动父子行；已撤回留档的原行仍可查询，但不重复计入本次办理数量。')
    if apply:
        if is_historical(item):raise ValidationError({'source':'历史原计算结果保留，公式试算不覆盖历史字段。'})
        owned=managed_fields(type(item))|{item.SOURCE_FIELDS[key] for key in item.SOURCE_KEY};changes={key:value for key,value in result['changes'].items() if key not in owned}
        for row in result['rows']:
            if item.SOURCE_FIELDS[row['field']] in owned and row['state']=='calculated':row['state']='managed_field_preview'
        before=snapshot(item)
        item=write(type(item),changes,item,actor)
        record(item,'entry_formula_apply',before,actor,'按'+entry+'试算结果采用；失败和受管字段保留原值')
    result['applied']=apply
    return result
