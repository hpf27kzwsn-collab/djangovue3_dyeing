"""采购实际引用、分批收货及原采购进度查询。"""
from plugins.erp_base.source_provenance import reference as source_reference
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import transaction
from .business import locked, persist, record, snapshot
from .source_stock_services import raw
from .source_business_updates import matching
from .source_entry_services import entry_for
from .source_context import SourceDocumentContext
from .source_sample_flow import copy_values
from .source_calculations import store_value, product


def rows(table, module='erp_purchase'):
    from .source_execution_state import active
    return active(apps.get_model(module + '.SourceDye' + table).objects.all())


def require_change(item, operation):
    entry = entry_for(item)
    if item.SOURCE_TABLE == 'PurMain' and entry == 'PurMain' and operation != 'reopen':
        detail, incoming, key = 'PurDetail', 'GrayInDetail', 'PurchaseOrders'
    elif item.SOURCE_TABLE == 'PurApplyMain' and entry in ['ArticlePurApplyMain', 'StuffPurApplyMain']:
        detail = 'PurApplyDetail'
        incoming = 'ArticleInDetail' if entry == 'ArticlePurApplyMain' else 'StuffInDetail'
        key = 'PurDetailNo'
    else:
        return
    for line in matching(rows(detail), SheetSeries=raw(item, 'SheetSeries')):
        if matching(rows(incoming, 'erp_warehouse'), **{key: raw(line, 'DetailNo')}).exists():
            raise ValidationError({'source': f'原采购规则：明细{raw(line, "DetailNo")}已有{incoming}引用，不能{operation}。'})


def receipt_progress(item, query=rows):
    """A_PurDetailNo的18/20类收货与原待收选择分别返回，不臆造完成状态。"""
    number = raw(item, 'DetailNo')
    sources = []
    for table, kind in [('GrayIn', 18), ('SemiIn', 20)]:
        for line in matching(query(table + 'Detail', 'erp_warehouse'), PurDetailNo=number).order_by('pk'):
            for head in matching(query(table, 'erp_warehouse'), SheetSeries=raw(line, 'SheetSeries')).filter(old_sheet_kind=kind):
                sources.append({'entity': line._meta.label, 'id': line.pk, 'header_id': head.pk,
                    'source': source_reference(line), 'weight': raw(line, 'WeightQty')})
    values = [line['weight'] for line in sources if line['weight'] is not None]
    # 原视图排除空采购号；NULL不作为另一NULL的实际采购关系。
    total = sum(values) if values and number is not None and number.rstrip(' ') else None
    candidates = query('GrayInDetail', 'erp_warehouse')
    used = matching(candidates, PurDetailNo=number).exists()
    if number is None or number.rstrip(' ') == '':
        from django.db.models import Q
        used = candidates.filter(Q(old_pur_detail_no__isnull=True) | Q(old_pur_detail_no__regex=r'^ *$')).exists()
    return {'received_weight_18_20': total, 'source_rows': sources, 'old_gray_selection_available': not used}


@transaction.atomic
def receive(item, actor, entry, received_at, quantity, rolls, warehouse, unit, length=None, supplier=None, receipt_number=None):
    """明确分批量生成收货草稿；实际库存继续由原入口生效规则处理。"""
    from . import source_services as services
    item = locked(item)
    from .source_execution_state import require_available
    require_available(item)
    table, kind = {'PurGrayIn': ('GrayIn', 18), 'PurSemiIn': ('SemiIn', 20)}[entry]
    head_model = rows(table, 'erp_warehouse').model
    line_model = rows(table + 'Detail', 'erp_warehouse').model
    heads = list(matching(rows('PurMain'), SheetSeries=raw(item, 'SheetSeries')).order_by('pk'))
    # 多个原表头不任选：公用头字段只有明确一张原表头时采用，全部候选留档。
    head_values = {} if len(heads) != 1 else copy_values(heads[0], head_model,
        ['SheetSeries', 'SheetNo', 'SheetDate', 'SheetKind', 'SheetStatus', 'RightStatus', 'StepNo',
         'PrintTimes', 'Revisions', 'CreateDate', 'Creater', 'ModifyDate', 'Modifyer', 'ApproveDate', 'Approver'])
    head_values.update(_entry=entry, old_sheet_date=received_at, old_sheet_kind=kind,
                       old_ware_house_id=warehouse, old_stock_unit=unit)
    if supplier is not None:head_values['old_supplier_id']=supplier
    head = services.write(head_model, head_values, actor=actor, apply_effects=False)
    values = copy_values(item, line_model, ['SheetSeries', 'DetailNo', 'ReceSheetNo', 'Rolls', 'WeightQty', 'Amount'])
    values.update(source_parent_1=head, old_pur_detail_no=raw(item, 'DetailNo'),
                  old_purchase_orders=raw(item, 'DetailNo'), old_weight_qty=quantity, old_rolls=rolls)
    values.update([store_value(line_model(),'LengthQty',length)])
    if receipt_number is not None:values['old_rece_sheet_no']=receipt_number
    values.update(dict(store_value(line_model(), key, value) for key, value in [
        ('WeightQty', quantity), ('Rolls', rolls), ('Amount', product(raw(item, 'Price'), quantity))]))
    line = services.write(line_model, values, actor=actor, apply_effects=False)
    context = SourceDocumentContext.objects.get(entity=head._meta.label, object_id=head.pk)
    context.effects['purchase_origin'] = {'entity': item._meta.label, 'source': snapshot(item),
        'headers': [snapshot(value) for value in heads], 'line_id': line.pk}
    persist(context, actor)
    services.finish([head], actor)
    record(head, 'purchase_receipt_adopted', {'exists': False}, actor, f'分批收货来源：{item._meta.label}/{item.pk}')
    return head


@transaction.atomic
def receive_material(item, actor, entry, quantity, warehouse, supplier, sheet_kind, at, reason):
    """采购申请及采购明细到染化料/机物料入库；实际数量独立保留。"""
    from . import source_services as services
    from .source_execution_state import require_available
    from .source_continuation import copy_new, origin, save_effect
    from .source_calculations import field_values
    item=locked(item);require_available(item)
    table={'StuffIn':'StuffIn','SmallStuffIn':'StuffIn','ArticleIn':'ArticleIn','FabricArticleIn':'ArticleIn'}[entry]
    expected={'StuffPurDetail':'StuffIn','ArticlePurDetail':'ArticleIn'}
    if item.SOURCE_TABLE in expected and table != expected[item.SOURCE_TABLE]:
        raise ValidationError({'entry':'收货家族必须与原采购物料家族一致。'})
    head_model,line_model=rows(table,'erp_warehouse').model,rows(table+'Detail','erp_warehouse').model
    head=services.write(head_model,{'_entry':entry,'old_sheet_date':at,'old_sheet_kind':sheet_kind,
        'old_ware_house_id':warehouse,'old_supplier_id':supplier,'old_remarks':reason},actor=actor,apply_effects=False)
    values=copy_new(item,line_model,['SheetSeries','DetailNo','Qty','InQty','Amount','Total'])
    values.update(source_parent_1=head,old_pur_detail_no=raw(item,'DetailNo'))
    values.update([store_value(line_model(),'Qty' if table=='StuffIn' else 'InQty',quantity)])
    values.update(field_values(line_model(**values)))
    line=services.write(line_model,values,actor=actor,apply_effects=False)
    parent_tables={'PurApplyDetail':['PurApplyMain'],'PurDetail':['PurMain','ArticlePurMain','StuffPurMain'],
        'ArticlePurDetail':['ArticlePurMain'],'StuffPurDetail':['StuffPurMain']}
    heads=[head for parent in parent_tables[item.SOURCE_TABLE]
        for head in matching(rows(parent),SheetSeries=raw(item,'SheetSeries')).order_by('pk')]
    save_effect(head,'purchase_origin',{'entity':item._meta.label,'source':snapshot(item),
        'headers':[{'entity':row._meta.label,'source':snapshot(row)} for row in heads],'line_id':line.pk,'at':at,'reason':reason},actor,reason)
    services.finish([head],actor)
    return head


@transaction.atomic
def return_purchase(item, actor, quantity, warehouse, supplier, at, reason):
    from . import source_services as services
    from .source_execution_state import require_available
    from .source_continuation import copy_new, origin, save_effect
    from .source_calculations import field_values
    item=locked(item);require_available(item)
    table=item.SOURCE_TABLE.removesuffix('Detail')
    head_model=rows(table,'erp_warehouse').model
    head=services.write(head_model,{'_entry':table,'old_sheet_date':at,'old_sheet_kind':16,
        'old_ware_house_id':warehouse,'old_supplier_id':supplier,'old_remarks':reason},actor=actor,apply_effects=False)
    values=copy_new(item,type(item),['SheetSeries','DetailNo','Qty','InQty','Amount','Total'])
    quantity_key='Qty' if table=='StuffIn' else 'InQty'
    original_key='OriInDetailNo' if table=='StuffIn' else 'OriDetailNo'
    values.update(source_parent_1=head,**dict([store_value(item,quantity_key,quantity),
        store_value(item,original_key,raw(item,'DetailNo'))]))
    values.update(field_values(type(item)(**values)))
    line=services.write(type(item),values,actor=actor,apply_effects=False)
    save_effect(head,'purchase_return_origin',{**origin(item),'line_id':line.pk,'at':at,'reason':reason},actor,reason)
    services.finish([head],actor)
    return head


def material_source_unit(item,table):
    if item.SOURCE_TABLE=='ArticlePurDetail':
        return raw(item,'Unit') if table=='ArticleIn' else None
    if item.SOURCE_TABLE=='StuffPurDetail':
        return None  # 原PriceUnit是价格单位；不能当作数量单位。
    return raw(item,'StuffUnit' if table=='StuffIn' else 'ArticleUnit')


def material_receipts(item, query):
    result=[]
    for table,measure in [('StuffIn','Qty'),('ArticleIn','InQty')]:
        for line in matching(query(table+'Detail','erp_warehouse'),PurDetailNo=raw(item,'DetailNo')).order_by('pk'):
            heads=list(matching(query(table,'erp_warehouse'),SheetSeries=raw(line,'SheetSeries')).order_by('pk'))
            for head in heads or [None]:
                qty=raw(line,measure);kind=None if head is None else raw(head,'SheetKind')
                signed=qty if kind!=16 or qty is None else -abs(qty) if table=='StuffIn' else -qty
                result.append({'entity':line._meta.label,'record_id':line.pk,'source': source_reference(line),
                    'header_id':None if head is None else head.pk,'SheetKind':kind,'measure':measure,
                    'quantity':qty,'stock_quantity_rule':signed,'missing_header':head is None,
                    'source_unit':material_source_unit(item,table),
                    'source_price_unit':raw(item,'PriceUnit') if item.SOURCE_TABLE=='StuffPurDetail' else None,
                    'source_pack_unit':raw(item,'PackUnit') if item.SOURCE_TABLE in ['StuffPurDetail','ArticlePurDetail'] else None})
    return {'report':'采购申请及采购明细实际收货与退货来源','rows':result,
        'notes':['分别列出染化料Qty与机物料InQty，未知单位不相加；数量规则不等于原单已经审核或实际产生库存流水。',
            '染化料16类按-ABS，机物料16类按取负；负数、空值、重复表头及缺表头记录均保留。']}


@transaction.atomic
def return_raw_purchase(item,actor,weight,length,rolls,warehouse,unit,supplier,at,reason,receipt_number=None):
    from . import source_services as services
    from .source_execution_state import require_available
    from .source_continuation import copy_new,origin,save_effect
    from .source_calculations import field_values
    item=locked(item);require_available(item)
    table=item.SOURCE_TABLE.removesuffix('Detail');model=rows(table,'erp_warehouse').model
    head=services.write(model,{'_entry':'Pur'+table,'old_sheet_date':at,'old_sheet_kind':16,
        'old_ware_house_id':warehouse,'old_stock_unit':unit,'old_supplier_id':supplier,'old_remarks':reason},actor=actor,apply_effects=False)
    values=copy_new(item,type(item),['SheetSeries','ReceSheetNo','WeightQty','LengthQty','Rolls','Amount'])
    values.update(source_parent_1=head,old_ori_rece_sheet_no=raw(item,'ReceSheetNo'))
    if receipt_number is not None:values['old_rece_sheet_no']=receipt_number
    values.update(store_value(item,key,value) for key,value in [('WeightQty',weight),('LengthQty',length),('Rolls',rolls)])
    values.update(field_values(type(item)(**values)))
    line=services.write(type(item),values,actor=actor,apply_effects=False)
    save_effect(head,'purchase_return_origin',{**origin(item),'line_id':line.pk,'at':at,'reason':reason},actor,reason)
    services.finish([head],actor)
    return head


def raw_receipts(item,query):
    from django.db.models import Q
    from .source_quality_reports import key
    result=[]
    for table in ['GrayIn','SemiIn']:
        candidates=query(table+'Detail','erp_warehouse')
        number=raw(item,'DetailNo')
        selected=candidates.filter(Q(pk__in=matching(candidates,PurDetailNo=number).values('pk'))|
            Q(pk__in=matching(candidates,PurchaseOrders=number).values('pk')))
        for line in selected.order_by('pk'):
            heads=query(table,'erp_warehouse')
            heads=list(heads.filter(pk=line.source_parent_1_id) if line.source_parent_1_id is not None else matching(heads,SheetSeries=raw(line,'SheetSeries')))
            for head in heads or [None]:
                result.append({'entity':line._meta.label,'record_id':line.pk,'source': source_reference(line),
                    'purchase_reference_fields':[name for name in ['PurDetailNo','PurchaseOrders'] if key(raw(line,name))==key(number)],
                    'PurDetailNo':raw(line,'PurDetailNo'),'PurchaseOrders':raw(line,'PurchaseOrders'),
                    'header_id':None if head is None else head.pk,'SheetKind':None if head is None else raw(head,'SheetKind'),
                    'SupplierID':None if head is None else raw(head,'SupplierID'),
                    'unit':None if head is None else raw(head,'StockUnit'),'missing_header':head is None,
                    **{name:raw(line,name) for name in ['ReceSheetNo','OriReceSheetNo','WeightQty','LengthQty','Rolls']}})
    return {'report':'坯料半成品采购收退明细','rows':result,
        'notes':['按PurDetailNo或PurchaseOrders分别列出匹配依据；同一原行同时命中只显示一次，原18/20类统计仍按PurDetailNo，不混改旧公式。',
            '包括原18/20类收货、16类退货及其他原类型；仅逐条显示，不跨单位合计。',
            '原Gray/Semi入库过程直接记入库侧原数量，16类不自动取负；实际退货数量按原凭据填写，原正负值均保留。']}
