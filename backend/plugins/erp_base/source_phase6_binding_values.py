"""补绑查询入口的原行公式；未知查询父行不自动选择。"""
from decimal import Decimal
from .source_calculations import product, zero, store_value
from .source_entry_calculations import difference

RULES={
    'DStuffWeight': {'ClothNetKg':('ClothQtyKg','SubRate')},
    'qry_QuoteRelaStuff': {'ClothNetKg':('ClothQtyKg','SubRate')},
    'qry_Employee': {'LoginName':('EmpID',),'Password':('EmpID',)},
    'QueryRecordCheck': {'CustQty':('Kg','Addkg'),'NetKg':('Kg','TubeWeight'),
        'Pound':('Kg',),'RealQty':('Meter','AddQty','CutQty','Qty'),'Tubes':('Status','GradeID')},
}


def before_save(item,data,entry,creating):
    from .source_provenance import is_historical
    from .source_stock_services import raw
    if is_historical(item):return
    if entry=='qry_Employee' and not creating:
        from django.utils import timezone
        if 'old_modifyer' not in data:item.old_modifyer=item.modifier.username
        if 'old_modify_date' not in data:item.old_modify_date=timezone.localtime()
    for target,inputs in RULES.get(entry,{}).items():
        if item.SOURCE_FIELDS[target] in data:continue
        if not creating and not {item.SOURCE_FIELDS[name] for name in inputs}.intersection(data):continue
        if entry=='qry_Employee' and target=='Password' and not creating:continue
        values=[raw(item,name) for name in inputs]
        if target=='ClothNetKg':value=difference(values[0],product(*values))
        elif target in ['LoginName','Password']:value=values[0]
        elif target=='CustQty':value=sum(zero(v) for v in values)
        elif target=='NetKg':value=difference(values[0],zero(values[1]))
        elif target=='Pound':value=product(values[0],Decimal('2.2046'))
        elif target=='RealQty':value=difference(values[0],sum(zero(v) for v in values[1:]))
        elif target=='Tubes':
            status=1 if values[0] is None else values[0]
            grade='A' if values[1] is None else values[1]
            value=1 if status==1 and grade<='C' else 0
        key,value=store_value(item,target,value)
        setattr(item,key,value)
