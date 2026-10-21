"""基础资料、来样颜色及报价订单的原行公式，按输入变更在保存前计算。"""
from .source_calculations import zero,store_value

RULES={
    'p_Customer': {'Num':('CustomerID',)},
    'p_Supplier': {'CustomerID':('Num',)},
    'p_Stuff': {'RecipeUnit':('StuffType',),'StockUnit':('StuffType',),'WeightUnit':('StuffType',)},
    'FixedPrice': {'CustomerCode':('CustomerID',)},
    'Quote': {'CustomerCode':('CustomerID',)},
    'QuoteDetail': {'IsConfirmed':('Price',),'Pricesum':('Price','ProcessPrice'),
                    'SumChengBen':tuple('ChengBen'+str(i) for i in range(6))},
}
for entry in ['DyeLabColor','ShowDyeLabColor']:
    RULES[entry]={'ColorNum':('ColorNumInput','ColorMarkt','OrderNum','ColorAfter'),
        'KHSHORPTSH':('CustColorNum','ColorMarkt'),'Markt':('OrderNum',),'OriColorNo':('ColorNum',)}
for entry in ['p_ColorNum','p_ColorNumSup']:RULES[entry]={'RGB':('R','G','B')}
for entry in ['OrderColor','OrderColorChange','OrderColorSup','PrintOrderColor']:
    RULES[entry]={'OrderQty':('GrayQty',)}

CREATE_ONLY={('p_Supplier','CustomerID'),('p_Stuff','StockUnit'),('p_Stuff','WeightUnit')}


def prepare_numbers(item,data,entry):
    from .source_provenance import is_historical
    if is_historical(item):return
    # 供应商同一原字段同时配置了编号和NUM公式；明确输入NUM时直接采用，不能先卡在自动编号。
    if entry=='p_Supplier' and 'old_num' in data and 'old_customer_id' not in data:
        data['old_customer_id']=data['old_num']
        item.old_customer_id=data['old_num']


def before_save(item,data,entry,creating):
    from .source_stock_services import raw
    from .source_provenance import is_historical
    if is_historical(item):return
    changed=set(data)
    for target,inputs in RULES.get(entry,{}).items():
        key=item.SOURCE_FIELDS[target]
        if key in data:continue
        if not creating and ((entry,target) in CREATE_ONLY or not {item.SOURCE_FIELDS[name] for name in inputs}.intersection(changed)):continue
        values=[raw(item,name) for name in inputs]
        if target=='Num':value=None if values[0] is None else 'K'+values[0]
        elif target in ['CustomerID','CustomerCode','OrderQty','OriColorNo']:value=values[0]
        elif target=='RecipeUnit':value=1 if values[0]=='A' else 0
        elif target=='StockUnit':value='K'
        elif target=='WeightUnit':value='K' if values[0]=='A' else 'G'
        elif target=='RGB':value=(zero(values[0])-255)*256*256+(zero(values[1])-255)*256+(zero(values[2])-255)-1
        elif target=='IsConfirmed':value=2 if values[0] is not None and values[0]>0 else 1
        elif target in ['Pricesum','SumChengBen']:value=sum(zero(v) for v in values)
        elif target=='Markt':value=None if values[0] is None else values[0][2:]
        elif target=='KHSHORPTSH':value=(values[1] or '') if values[0] in [None,''] else values[0]
        elif target=='ColorNum':
            entered,marker,order,suffix=values
            value=entered if entered not in [None,''] else (marker or '')+('' if order is None else order[2:])+(suffix or '')
        key,value=store_value(item,target,value)
        setattr(item,key,value);changed.add(key)
