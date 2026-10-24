"""已逐字段编译的原入口公式；保存按依赖计算，明确外键承接父子来源。"""
import json
from pathlib import Path
from functools import lru_cache
from decimal import Decimal,localcontext
from sqlglot import exp,parse_one
from django.core.exceptions import ValidationError
from .source_calculations import store_value


@lru_cache(maxsize=1)
def registry():
    return json.loads(Path(__file__).with_name('source_phase6_formula_registry.json').read_text(encoding='utf8'))['rules']


def rules_for(model,entry):return registry().get(model,{}).get(entry,{})


@lru_cache(maxsize=1)
def unresolved_fields():
    return json.loads(Path(__file__).with_name('source_phase6_formula_registry.json').read_text(encoding='utf8'))['unresolved_inputs']


def generated_fields(entry,model=None):
    return [field for label,entries in registry().items() if model is None or label.split('.')[1]==model
            for field in entries.get(entry,{})]


@lru_cache(maxsize=1024)
def tree(text):return parse_one(text,read='tsql')


def number(value):return Decimal(str(value))


def scalar(node,read):
    def val(n):return scalar(n,read)
    if isinstance(node,exp.Column):return read(node.table,node.name)
    if isinstance(node,exp.Literal):return node.this if node.is_string else number(node.this)
    if isinstance(node,exp.Null):return None
    if isinstance(node,exp.Boolean):return node.this
    if isinstance(node,exp.Paren):return val(node.this)
    if isinstance(node,exp.Neg):
        value=val(node.this);return None if value is None else -number(value)
    if isinstance(node,exp.If):return val(node.args['true']) if val(node.this) else val(node.args['false'])
    if isinstance(node,exp.Coalesce):
        for n in [node.this,*node.expressions]:
            value=val(n)
            if value is not None:return value
        return None
    if isinstance(node,exp.Substring):
        value=val(node.this);start=val(node.args['start']);length=val(node.args['length'])
        return None if value is None or start is None or length is None else str(value)[int(start)-1:int(start)-1+int(length)]
    if isinstance(node,exp.Not):
        value=val(node.this);return None if value is None else not value
    if isinstance(node,exp.In):
        value=val(node.this);options=[val(n) for n in node.expressions]
        return None if value is None else True if value in options else None if None in options else False
    if isinstance(node,(exp.And,exp.Or)):
        a,b=val(node.this),val(node.expression)
        if isinstance(node,exp.And):return False if a is not None and not a or b is not None and not b else None if a is None or b is None else True
        return True if a is not None and a or b is not None and b else None if a is None or b is None else False
    a,b=val(node.this),val(node.expression)
    if a is None or b is None:return None
    if isinstance(node,exp.Add) and (isinstance(a,str) or isinstance(b,str)):return str(a)+str(b)
    if isinstance(node,(exp.EQ,exp.NEQ,exp.GT,exp.GTE,exp.LT,exp.LTE)):
        if isinstance(a,str)!=isinstance(b,str):a,b=number(a),number(b)
        if isinstance(node,exp.EQ):return a==b
        if isinstance(node,exp.NEQ):return a!=b
        if isinstance(node,exp.GT):return a>b
        if isinstance(node,exp.GTE):return a>=b
        if isinstance(node,exp.LT):return a<b
        return a<=b
    a,b=number(a),number(b)
    if isinstance(node,exp.Add):return a+b
    if isinstance(node,exp.Sub):return a-b
    if isinstance(node,exp.Mul):return a*b
    if isinstance(node,exp.Div):return a/b
    raise ValueError('未登记公式节点：'+type(node).__name__)


class MissingSource(ValueError):pass


def follow(item,path):
    for key in path:
        if key=='raw_parent':
            from .source_phase6_formula_links import parent_rows
            parents=parent_rows(item)
            if len(parents)!=1:raise MissingSource('原主从码父行候选：'+str([v.pk for v in parents]))
            item=parents[0];continue
        if getattr(item,key+'_id') is None:raise MissingSource('缺明确父行：'+'.'.join(path))
        item=getattr(item,key)
    return item


def aggregate_rows(item,definition):
    from django.apps import apps
    from .source_stock_services import raw
    from .source_execution_state import active
    child=apps.get_model(definition['model'])
    if definition['path']:return active(child.objects.filter(**{'__'.join(definition['path']):item})).order_by('pk')
    from .source_phase6_formula_links import match
    return match(active(child.objects.all()),{field:raw(item,parent) for field,parent in definition['keys'].items()}).order_by('pk')


def calculated(item,spec,unresolved=()):
    from .source_stock_services import raw
    aggregate_values={}
    for name,definition in spec['aggregates'].items():
        rows=aggregate_rows(item,definition)
        values=[1 for row in rows] if definition['field'] is None else [raw(row,definition['field']) for row in rows if raw(row,definition['field']) is not None]
        aggregate_values[name]=len(values) if definition['operation']=='count' else sum(values) if values else None
    def read(table,name):
        key=(table+'.' if table else '')+name
        if key in aggregate_values:return aggregate_values[key]
        definition=spec['inputs'][key]
        if not definition['path'] and definition['field'] in unresolved:
            raise MissingSource('依赖公式'+definition['field']+'缺本次来源；保留原值，不采用上次计算值冒充本次结果')
        return raw(follow(item,definition['path']),definition['field'])
    with localcontext() as context:
        context.prec=80
        return scalar(tree(spec['compiled_expression']),read)


def apply(item,data,entry,creating=False,upstream=None,aggregate=False,own_save=False):
    from .source_provenance import is_historical
    if is_historical(item):return {},[]
    rules=rules_for(item._meta.label,entry);changed=set(data);changes={};pending=[];unresolved=set()
    # 双向公式以本次明确输入为方向；单价只在明确金额/含税价输入时反推。
    omitted=set()
    if item.SOURCE_TABLE=='JobSheet' and item.pk is not None:
        from .source_context import SourceDocumentContext
        if SourceDocumentContext.objects.filter(entity=item._meta.label,object_id=item.pk,
            effects__first_card_origin__number_policy__in=['legacy_prefix','complete_generated_number']).exists():
            # 首次开卡服务已采用完整编号；保留旧表达式供其他原入口及历史核对。
            omitted.add('SheetNo')
    if entry in ['CookInDetail','OtherInDetail']:
        omitted.add('Price' if item.SOURCE_FIELDS['TaxPrice'] not in data or item.SOURCE_FIELDS['Price'] in data else 'TaxPrice')
    if entry=='SmallStuffInDetail' and item.SOURCE_FIELDS['Amount'] not in data:omitted.add('Price')
    if aggregate and item.SOURCE_TABLE=='ProdIn':
        from .source_context import SourceDocumentContext
        context=SourceDocumentContext.objects.filter(entity=item._meta.label,object_id=item.pk).first()
        if context is not None and 'purchase_product_origin' in context.effects:
            # 明确采购转单直接承接表头数量，没有伪造细码；不能用空细码覆盖真实采购数。
            omitted.update(field for field,spec in rules.items() if spec['aggregates'])
    remaining={field:spec for field,spec in rules.items() if field not in omitted and item.SOURCE_FIELDS[field] not in data
        and (not spec['create_only'] or creating) and (not spec['aggregates'] or aggregate)}
    while remaining:
        ready=[field for field,spec in remaining.items() if not {v['field'] for v in spec['inputs'].values() if not v['path'] and v['field']!=field}.intersection(remaining)]
        if not ready:raise ValueError('公式相互依赖尚未确定输入方向：'+entry+'/'+','.join(remaining))
        for field in ready:
            spec=remaining.pop(field)
            # 仅录表头、没有子行时，修改表头不清空已有人工数量；子行撤回仍按空集合回算。
            if own_save and spec['aggregates'] and not any(aggregate_rows(item,v).exists() for v in spec['aggregates'].values()):continue
            local={item.SOURCE_FIELDS[v['field']] for v in spec['inputs'].values() if not v['path']}
            parent=any(v['path'] for v in spec['inputs'].values())
            parent_changed=any(v['path'] and v['field'] in (upstream or {}).get(v['model'],set()) for v in spec['inputs'].values())
            if not (creating or changed.intersection(local) or parent and (parent_changed or any(k.startswith('source_parent_') for k in data)) or aggregate and spec['aggregates']):continue
            try:value=calculated(item,spec,unresolved)
            except MissingSource as error:
                unresolved.add(field);pending.append({'field':field,'reason':str(error)});continue
            except ArithmeticError as error:
                raise ValidationError({item.SOURCE_FIELDS[field]:'原公式无法计算：'+str(error)+'；可明确录入该原字段（含NULL）保留异常单据。'}) from error
            key,value=store_value(item,field,value)
            if getattr(item,key)!=value:changes[key]=value
            setattr(item,key,value);changed.add(key)
    return changes,pending


def before_save(item,data,entry,creating):
    changes,pending=apply(item,data,entry,creating)
    pending.extend({'field':field,'reason':reason,'handling':'保留本行原值；未执行来源不完整的原公式',
                    'explicitly_supplied':item.SOURCE_FIELDS[field] in data}
                   for name,field,model,reason in unresolved_fields() if name==entry and model==item._meta.label)
    item._entry_formula_pending=pending
    item._entry_formula_changed=set(data)|set(changes)
    item._entry_formula_explicit={k:getattr(item,k) for k in data if k in item.SOURCE_FIELDS.values()}


def refresh(item,actor,upstream=None,aggregate=False,trail=()):
    from .source_entry_services import entry_for
    from .source_services import child_rows
    from .source_phase6_formula_links import child_rows as raw_children
    from .business import locked,persist,record,snapshot
    if item._meta.label in trail:return
    original=item;explicit=getattr(item,'_entry_formula_explicit',{})
    own_save=hasattr(item,'_entry_formula_explicit')
    from .source_phase6_save_timing import explicit_for
    document_input=explicit_for(item)
    if document_input is not None:explicit=document_input;own_save=True
    item=locked(item);before=snapshot(item)
    changes,pending=apply(item,explicit,entry_for(item),upstream=upstream,aggregate=aggregate,own_save=own_save)
    if changes:
        persist(item,actor);record(item,'entry_formula_refresh',before,actor,'明确父子来源公式：'+','.join(changes))
        for key,value in changes.items():setattr(original,key,value)
    if upstream or changes:
        context={**(upstream or {}),item._meta.label:{name for name,key in item.SOURCE_FIELDS.items() if key in changes}}
        for child in child_rows(item):refresh(child,actor,upstream=context,trail=(*trail,item._meta.label))
        for child in raw_children(item):refresh(child,actor,upstream=context,trail=(*trail,item._meta.label))


def saved(item,data,entry,creating,actor):
    from .source_provenance import is_historical
    if is_historical(item):return
    from .source_phase6_save_timing import enqueue
    if enqueue(item,data,entry,creating,actor):return
    from .business import record,snapshot
    from .source_services import child_rows
    from .source_phase6_formula_links import child_rows as raw_children,parent_rows
    pending=getattr(item,'_entry_formula_pending',[])
    # 保存本行后只沿明确主从关系向下传播；汇总由finish在子行写完后向上执行。
    fields={name for name,key in item.SOURCE_FIELDS.items() if key in getattr(item,'_entry_formula_changed',set(data))}
    if fields:
        for child in child_rows(item):refresh(child,actor,upstream={item._meta.label:fields},trail=(item._meta.label,))
        for child in raw_children(item):refresh(child,actor,upstream={item._meta.label:fields},trail=(item._meta.label,))
    for parent in parent_rows(item):refresh(parent,actor,aggregate=True)


def refresh_totals(items,actor):
    for item in reversed(items):refresh(item,actor,aggregate=True)
