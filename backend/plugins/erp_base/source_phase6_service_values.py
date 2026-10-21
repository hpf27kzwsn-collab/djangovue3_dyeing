"""配方、染程参数及数量换算：复用原公式服务，明确父行改变后回写。"""
from decimal import Decimal, localcontext
from .source_calculation_entries import RECIPE_DETAIL_ENTRIES
from .source_calculations import product, zero, store_value

RULES={
    'DyeRecipeDetail':{entry:{'Amount':('Price','Dosage')} for entry in RECIPE_DETAIL_ENTRIES},
    'p_DyeCurveDetail':{entry:{'Price':('DefaultValue',)} for entry in ['p_DyeCurveDetail','p_DyeCurveDetailJJ']},
    'QuoteDetail':{'FixedPriceDetail':{'Pricesum':('Price','ProcessPrice')}},
    'JobGrayRecord':{entry:{'Kg':('WeightQty','GUnit'),'Pound':('WeightQty','GUnit')}
        for entry in ['JobGrayPreRecord','JobGrayRecord','PrintJobGrayRecord','SaleJobGrayRecord','TwiJobGrayRecord']},
    'DefectiveOutRecord':{'DefectiveOutRecord':{
        'GKg':('GrayQty','GUnit'),'GPound':('GrayQty','GUnit'),
        'PKg':('WeightQty','PUnit'),'PPound':('WeightQty','PUnit')}},
}
for entry in ['BulkDyeRecipePhaseDetail','StandardDyeRecipePhaseDetail']:
    RULES['DyeRecipeDetail'][entry]['Amount']=('Price','Dosage','RecipeUnit')
RULES['DyeRecipeDetail']['FinishDyeRecipePhaseDetail']['Amount']=('Price','Dosage','StuffType')
PARENTS={'DyeRecipePhase':('BathRatio','DyeRecipeDetail'), 'p_DyeCurve':('MaxValue','p_DyeCurveDetail')}


def generated_fields(entry,model=None):
    return [target for table,entries in RULES.items() if model is None or model=='SourceDye'+''.join(part[:1].upper()+part[1:] for part in table.split('_'))
            for target in entries.get(entry,{})]


def needs_parent(item,entry):
    if item.SOURCE_TABLE=='p_DyeCurveDetail':return True
    if entry in ['BulkDyeRecipePhaseDetail','StandardDyeRecipePhaseDetail']:return item.old_recipe_unit!=0
    if entry=='FinishDyeRecipePhaseDetail':return item.old_stuff_type!='S'
    return False


def missing_parent(item,entry):
    return needs_parent(item,entry) and item.source_parent_1_id is None


def selected_targets(item,data,entry,creating):
    rules=RULES.get(item.SOURCE_TABLE,{}).get(entry,{})
    return [target for target,inputs in rules.items() if item.SOURCE_FIELDS[target] not in data and
            (creating or 'source_parent_1' in data or any(item.SOURCE_FIELDS[x] in data for x in inputs))]


def values(item,entry):
    from .source_entry_calculations import entry_values
    from .source_stock_services import raw
    with localcontext() as context:
        context.prec=80
        if item.SOURCE_TABLE in ['DyeRecipeDetail','p_DyeCurveDetail']:
            return entry_values(item,entry)
        if entry=='FixedPriceDetail':result={'Pricesum':zero(item.old_price)+zero(item.old_process_price)}
        else:
            result={}
            for target,(quantity,unit) in RULES[item.SOURCE_TABLE][entry].items():
                qty=raw(item,quantity);code=raw(item,unit)
                is_pound=target in ['Pound','GPound','PPound'];identity=3 if is_pound else 1
                if code is None and target in ['GKg','GPound']:code=identity
                value=qty if code==identity else product(qty,Decimal('2.2046')) if is_pound else None if qty is None else Decimal(str(qty))/Decimal('2.2046')
                result[target]=value
        return dict(store_value(item,target,value) for target,value in result.items())


def before_save(item,data,entry,creating):
    from .source_provenance import is_historical
    targets=selected_targets(item,data,entry,creating)
    if not targets or is_historical(item) or missing_parent(item,entry):return
    calculated=values(item,entry)
    for target in targets:
        key=item.SOURCE_FIELDS[target];setattr(item,key,calculated[key])


def saved(item,data,entry,creating,actor):
    from .source_provenance import is_historical
    from .source_entry_services import entry_for
    from .source_phase3_operations import model
    from .source_execution_state import active
    from .business import locked,persist,record,snapshot
    if is_historical(item):return
    from .source_phase6_save_timing import enqueue,explicit_for
    if enqueue(item,data,entry,creating,actor,service='dedicated'):return
    targets=selected_targets(item,data,entry,creating)
    if targets and missing_parent(item,entry):
        record(item,'entry_formula_source_pending',snapshot(item),actor,
            entry+'：'+','.join(targets)+'缺明确父行关联，原行及原值照存；不按同编号任选父行。')
    if item.SOURCE_TABLE not in PARENTS:return
    parent_field,table=PARENTS[item.SOURCE_TABLE]
    if item.SOURCE_FIELDS[parent_field] not in data:return
    for child in active(model(table).objects.filter(source_parent_1=item)).order_by('pk'):
        child=locked(child);child_entry=entry_for(child)
        if is_historical(child) or child_entry not in RULES[table] or not needs_parent(child,child_entry):continue
        explicit=explicit_for(child) or {}
        targets=[child.SOURCE_FIELDS[name] for name in RULES[table][child_entry]]
        if all(name in explicit for name in targets):continue
        calculated=values(child,child_entry)
        changes={k:v for k,v in calculated.items() if k not in explicit and getattr(child,k)!=v}
        if changes:
            before=snapshot(child)
            for key,value in changes.items():setattr(child,key,value)
            persist(child,actor)
            record(child,'entry_parent_formula_refresh',before,actor,
                child_entry+'：明确父行'+parent_field+'修改后重算；父记录ID='+str(item.pk))
