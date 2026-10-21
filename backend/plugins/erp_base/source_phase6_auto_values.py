"""明确原入口的保存联动；显式录入值和历史原值优先。"""

PRODUCT_ENTRIES = {'PurDetail','ArticlePurDetail','DStuffOutDetail','SmallStuffOutDetail',
                   'StuffOutDetail','SmallStuffInDetail','StuffInDetail','StuffAllotDetail'}
AUTO_PRODUCTS={name:[('Amount','Qty','Price')] for name in PRODUCT_ENTRIES}
for _entry in ['ArticleInDetail','FabricArticleInDetail']:
    AUTO_PRODUCTS[_entry]=[('Amount','InQty','Price'),('Total','InQty','Price')]
for _entry in ['ArticleOutDetail','FabricArticleOutDetail']:
    AUTO_PRODUCTS[_entry]=[('Total','OutQty','Price')]
for _entry in ['CusReturnSemiInDetail','GrayOutToSemiInDetail','MaterialSemiInDetail','PurSemiInDetail',
               'SemiInDetail','SemiInDetailBack','TurnSemiInDetail','GrayInDetail','JiaNianGrayInDetail',
               'KeTuiGrayInDetail','PurGrayInDetail','SemiToGrayInDetail','TuiHuoGrayInDetail',
               'GrayOutDetail','GrayOutDetailJob','GrayOutDetailTurn']:
    AUTO_PRODUCTS[_entry]=[('Amount','Price','WeightQty')]
for _entry in ['GrayInWorkDetail','GrayOutSaleDetail']:
    AUTO_PRODUCTS[_entry]=[('Amount','Price','WeightQty')]
AUTO_PRODUCTS['StuffPurDetail']=[('Amount','Price','Qty')]
AUTO_PRODUCTS['EnergyConsumptionDetail']=[('Amount','UseQty','Price')]
AUTO_NULL_DIFFERENCES={'EnergyConsumptionDetail':[('UseQty','ThisReadQty','LastReadQty')]}
AUTO_NULL_PRODUCTS={name:[('Amount','Price','Qty',('Price','Qty'))]
                    for name in ['ArticlePurApplyDetail','StuffPurApplyDetail','PurDetailList']}
for _entry in ['ArticleStockAdjustDetail','StuffStockAdjustDetail']:
    AUTO_NULL_PRODUCTS[_entry]=[('RealMoney','RealQty','Price',('RealQty',))]
    AUTO_NULL_DIFFERENCES[_entry]=[('AdjustMoney','RealMoney','PaperMoney'),('AdjustQty','RealQty','PaperQty')]
for _entry in ['GrayStockAdjustDetail','ProdStockAdjustDetail','SemiStockAdjustDetail']:
    AUTO_NULL_DIFFERENCES[_entry]=[('AdjustLengthQty','RealLengthQty','PaperLength'),
        ('AdjustRolls','RealRolls','PaperRolls'),('AdjustWeightQty','RealWeightQty','PaperWeight')]
AUTO_NULL_DIFFERENCES['GrayStockAdjustDetail'].append(('AdjustPacks','RealPacks','PaperPacks'))
AUTO_ZERO_PRODUCTS={name:[('Amount','Price','WeightQty')] for name in ['ProdOutDetail','ProdOutDetailUpdate']}
AUTO_NULL_COPIES={name:[('Total','Amount')] for name in ['ProdOutDetail','ProdOutDetailUpdate']}
for _entry in ['ProdInRecord','ProdInRecordWork','TwistingInRecord']:AUTO_NULL_COPIES[_entry]=[('RealQty','WeightQty')]
AUTO_UNITS={name:[('GKg','GrayQty','GUnit',1,1,'divide'),('GPound','GrayQty','GUnit',3,3,'multiply'),
    ('PKg','WeightQty','PUnit',1,None,'divide'),('PPound','WeightQty','PUnit',3,None,'multiply')]
    for name in ['ProdOutRecord','ProdOutRecordUpdate']}
AUTO_POSITIVE_PRODUCTS={name:[('SumDots','Dots','Times')]
    for name in ['QC_RecordDefect','QueryRecordDefect','QueryRecordDefect2']}
AUTO_ENTRIES=set(AUTO_PRODUCTS)|set(AUTO_NULL_PRODUCTS)|set(AUTO_NULL_DIFFERENCES)|set(AUTO_ZERO_PRODUCTS)|set(AUTO_NULL_COPIES)|set(AUTO_UNITS)|set(AUTO_POSITIVE_PRODUCTS)


def generated_fields(entry,model=None):
    from .source_phase6_formula_runtime import generated_fields as remaining_fields
    from .source_phase6_binding_values import RULES
    from .source_phase6_local_values import RULES as LOCAL_RULES
    from .source_phase6_service_values import generated_fields as service_fields
    return remaining_fields(entry,model)+service_fields(entry,model)+list(LOCAL_RULES.get(entry,{}))+list(RULES.get(entry,{}))+[rule[0] for rules in [AUTO_NULL_PRODUCTS,AUTO_NULL_DIFFERENCES,AUTO_PRODUCTS,AUTO_ZERO_PRODUCTS,AUTO_NULL_COPIES,AUTO_UNITS,AUTO_POSITIVE_PRODUCTS]
            for rule in rules.get(entry,[])]

def before_save(item, data, entry, creating):
    from .source_phase6_formula_runtime import before_save as remaining_values
    remaining_values(item,data,entry,creating)
    from .source_phase6_service_values import before_save as service_values
    service_values(item,data,entry,creating)
    from .source_phase6_local_values import before_save as local_values
    local_values(item,data,entry,creating)
    from .source_phase6_binding_values import before_save as binding_values
    binding_values(item,data,entry,creating)
    from .source_stock_services import raw
    from .source_calculations import product, store_value
    from .source_provenance import is_historical
    # 只执行逐入口核对的原公式；客户端时机定义缺失，明确在新增/修改输入时计算。
    if entry not in AUTO_ENTRIES or is_historical(item):
        return
    changed=set(data)
    from decimal import Decimal
    for target,quantity,unit,identity,null_unit,operation in AUTO_UNITS.get(entry,[]):
        inputs={item.SOURCE_FIELDS[name] for name in [quantity,unit]}
        if item.SOURCE_FIELDS[target] not in data and (creating or inputs.intersection(changed)):
            value=raw(item,quantity);code=raw(item,unit)
            if code is None:code=null_unit
            if value is not None and code!=identity:
                value=Decimal(str(value))/Decimal('2.2046') if operation=='divide' else Decimal(str(value))*Decimal('2.2046')
            key,value=store_value(item,target,value)
            setattr(item,key,value);changed.add(key)
    for target,left,right in AUTO_POSITIVE_PRODUCTS.get(entry,[]):
        inputs={item.SOURCE_FIELDS[name] for name in [left,right]}
        if item.SOURCE_FIELDS[target] not in data and (creating or inputs.intersection(changed)):
            value=product(raw(item,left),raw(item,right))
            key,value=store_value(item,target,value if value is not None and value>0 else 0)
            setattr(item,key,value);changed.add(key)
    for target,left,right in AUTO_ZERO_PRODUCTS.get(entry,[]):
        inputs={item.SOURCE_FIELDS[name] for name in [left,right]}
        if item.SOURCE_FIELDS[target] not in data and (creating or inputs.intersection(changed)):
            value=product(raw(item,left),raw(item,right))
            key,value=store_value(item,target,0 if value is None else value)
            setattr(item,key,value);changed.add(key)
    for target,source in AUTO_NULL_COPIES.get(entry,[]):
        if item.SOURCE_FIELDS[target] not in data and (creating or item.SOURCE_FIELDS[source] in changed):
            value=raw(item,source)
            key,value=store_value(item,target,0 if value is None else value)
            setattr(item,key,value);changed.add(key)
    for target,left,right,null_fields in AUTO_NULL_PRODUCTS.get(entry,[]):
        inputs={item.SOURCE_FIELDS[name] for name in [left,right]}
        if item.SOURCE_FIELDS[target] not in data and (creating or inputs.intersection(changed)):
            values=[0 if raw(item,name) is None and name in null_fields else raw(item,name) for name in [left,right]]
            key,value=store_value(item,target,product(*values))
            setattr(item,key,value);changed.add(key)
    for target,left,right in AUTO_NULL_DIFFERENCES.get(entry,[]):
        inputs={item.SOURCE_FIELDS[name] for name in [left,right]}
        if item.SOURCE_FIELDS[target] not in data and (creating or inputs.intersection(changed)):
            # 此入口原式明确ISNULL(...,0)，不是对未知字段补0。
            first,last=raw(item,left),raw(item,right)
            key,value=store_value(item,target,(0 if first is None else first)-(0 if last is None else last))
            setattr(item,key,value);changed.add(key)
    for target,left,right in AUTO_PRODUCTS.get(entry,[]):
        inputs={item.SOURCE_FIELDS[name] for name in [left,right]}
        if item.SOURCE_FIELDS[target] not in data and (creating or inputs.intersection(changed)):
            key,value=store_value(item,target,product(raw(item,left),raw(item,right)))
            setattr(item,key,value)
