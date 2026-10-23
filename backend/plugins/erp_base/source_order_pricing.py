"""染整订单明确采用报价；原报价、历史单据及原取价函数不被重写。"""
from copy import deepcopy
from decimal import Decimal
from types import SimpleNamespace
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils import timezone
from .business import persist, record, snapshot, locked
from .source_business_updates import matching
from .source_calculations import store_value
from .source_context import SourceDocumentContext
from .source_provenance import is_historical, reference

KEY='order_pricing'
UNITS={1:'元/kg',2:'元/吨',3:'元/米',4:'元/条',5:'元/缸',6:'元/码'}
YARNS={'本厂采购':'包工包料','客户来纱':'来料加工'}
QUOTE_COLUMNS=['old_sheet_series','old_detail_no','old_prod_id','old_yarn_category','old_price_unit','old_cus_price','old_price','old_pricesum']
HEAD_COLUMNS=['old_sheet_series','old_sheet_no','old_sheet_date','old_customer_id']
LINE_COLUMNS=['old_sheet_series','old_check_no','old_prod_id','old_order_qty','old_unit','old_card_qty','old_price','old_amount']


def model(table):
    return apps.get_model('erp_sales.SourceDye'+table)


def reader(actor):
    from .reports import Reader
    return Reader(SimpleNamespace(user=actor))


def context(item):
    return SourceDocumentContext.objects.filter(entity=item._meta.label,object_id=item.pk).first() if item.pk else None


def current(item):
    ctx=context(item)
    return deepcopy(ctx.effects.get(KEY)) if ctx else None


def head_for(item,actor=None):
    if item.source_parent_1_id is not None:
        heads=model('OrderMain').objects.filter(pk=item.source_parent_1_id)
    else:
        heads=matching(model('OrderMain').objects.all(),SheetSeries=item.old_sheet_series)
    if actor is not None:heads=heads.filter(pk__in=reader(actor).source(model('OrderMain'),HEAD_COLUMNS))
    values=list(heads[:2])
    if len(values)!=1:raise ValidationError({'_pricing':'请明确选择本行所属订单表头，再采用报价。'})
    return values[0]


def lines_for(head,actor=None):
    rows=model('OrderColor').objects.all()
    if actor is not None:rows=reader(actor).source(model('OrderColor'),LINE_COLUMNS)
    return rows.filter(Q(source_parent_1=head)|Q(source_parent_1__isnull=True,pk__in=matching(rows,SheetSeries=head.old_sheet_series))).order_by('pk')


def quote_rows(actor,customer,product,yarn):
    read=reader(actor)
    heads=matching(read.source(model('FixedPrice'),HEAD_COLUMNS),CustomerID=customer)
    details=matching(read.source(model('FixedPriceDetail'),QUOTE_COLUMNS),ProdID=product,YarnCategory=yarn)
    result=[]
    for detail in details.order_by('pk'):
        parents=heads.filter(pk=detail.source_parent_1_id) if detail.source_parent_1_id else matching(heads,SheetSeries=detail.old_sheet_series)
        for head in parents.order_by('pk'):
            result.append((head,detail))
    return result


def candidate_data(head,detail):
    return {'quote_id':detail.pk,'quote_head_id':head.pk,'sheet_no':head.old_sheet_no,
        'sheet_series':head.old_sheet_series,'sheet_date':head.old_sheet_date,'detail_no':detail.old_detail_no,
        'customer_id':head.old_customer_id,'prod_id':detail.old_prod_id,'yarn_category':detail.old_yarn_category,
        'price_unit':detail.old_price_unit,'cus_price':detail.old_cus_price,'confirmed_price':detail.old_price,
        'total_price':detail.old_pricesum}


def candidates(actor,customer,product,yarn):
    return [candidate_data(h,d) for h,d in quote_rows(actor,customer,product,yarn)]


def quantity(item,unit,choice):
    if choice['quantity_mode']=='explicit':
        value=choice.get('quantity')
        return None if value is None else Decimal(value),'明确输入的本单计价数量'
    qty=item.old_order_qty
    code=(item.old_unit or '').rstrip(' ').upper()
    if unit==1 and code in ['KG','公斤','千克']:return qty,'OrderQty（KG）'
    if unit==2 and code in ['KG','公斤','千克']:return None if qty is None else qty/Decimal('1000'),'OrderQty（KG）÷1000'
    identities={2:['T','TON','吨'],3:['M','米'],4:['条'],5:['缸'],6:['Y','YD','YARD','码']}
    if unit in identities and code in identities[unit]:return qty,'OrderQty（'+code+'）'
    if unit==5:return None if item.old_card_qty is None else Decimal(item.old_card_qty),'CardQty（订单缸数）'
    return None,'本行单位与报价计价口径未明确对应，请指定计价数量'


def calculate(item,state):
    qty,basis=quantity(item,state.get('price_unit'),state)
    state['quantity']=None if qty is None else str(qty)
    state['quantity_basis']=basis
    _,price=store_value(item,'Price',None if state.get('price') is None else Decimal(state['price']))
    state['status']='priced' if price is not None and qty is not None and state.get('price_unit') is not None else 'unpriced'
    if state['amount_mode']=='manual':
        amount=None if state.get('manual_amount') is None else Decimal(state['manual_amount'])
        state['status']='manual_amount' if amount is not None else 'unpriced'
    else:amount=None if state['status']=='unpriced' else Decimal(price)*qty
    _,amount=store_value(item,'Amount',amount)
    state['price']=None if price is None else str(price)
    state['amount']=None if amount is None else str(amount)
    return {'old_price':price,'old_amount':amount},state


def selection(item,choice,actor,head=None,lock=False):
    head=head or head_for(item,actor)
    state={'mode':choice['mode'],'customer_id':head.old_customer_id,'prod_id':item.old_prod_id,
        'line_unit':item.old_unit,'yarn_category':choice.get('yarn_category'),
        'price_unit':choice.get('price_unit'),'quantity_mode':choice['quantity_mode'],
        'quantity':None if choice.get('quantity') is None else str(choice['quantity']),
        'amount_mode':choice['amount_mode'],'manual_amount':None if choice.get('manual_amount') is None else str(choice['manual_amount']),
        'reason':choice.get('reason',''),'adopted_at':timezone.now().isoformat()}
    if choice['mode']=='quote':
        if choice.get('quote_id') is None or choice.get('yarn_category') not in YARNS:
            raise ValidationError({'_pricing':'请选择明确的供纱方式及报价原行。'})
        matches=[(h,d) for h,d in quote_rows(actor,head.old_customer_id,item.old_prod_id,choice['yarn_category'])
                 if d.pk==choice['quote_id'] and (choice.get('quote_head_id') is None or h.pk==choice['quote_head_id'])]
        if len(matches)!=1:raise ValidationError({'_pricing':'所选报价不在本客户、物料、供纱方式的唯一明确来源中，请重新选择报价表头及明细。'})
        quote_head,detail=matches[0]
        if lock:
            quote_head,detail=locked(quote_head),locked(detail)
            if not any(h.pk==quote_head.pk and d.pk==detail.pk for h,d in quote_rows(actor,head.old_customer_id,item.old_prod_id,choice['yarn_category'])):
                raise ValidationError({'_pricing':'报价来源已变更，请按当前客户、物料和供纱方式重新选择。'})
        basis=choice['price_basis']
        price=getattr(detail,detail.SOURCE_FIELDS[basis])
        state.update(price=None if price is None else str(price),price_basis=basis,
            quote_id=detail.pk,quote_head_id=quote_head.pk,quote_sheet_no=quote_head.old_sheet_no,
            quote_detail_no=detail.old_detail_no,quote_head_source=reference(quote_head),quote_source=reference(detail),
            quote_prices={key:None if getattr(detail,detail.SOURCE_FIELDS[key]) is None else str(getattr(detail,detail.SOURCE_FIELDS[key]))
                          for key in ['CusPrice','Price','Pricesum','ProcessPrice','FenTouPrice','MinAmount']},
            original_price_unit=detail.old_price_unit)
        if state['price_unit'] is None:state['price_unit']=detail.old_price_unit
    else:
        price=choice.get('manual_price')
        state.update(price=None if price is None else str(price),price_basis='manual')
    return calculate(item,state)


def prepare(item,data,choice,actor):
    if item.SOURCE_TABLE!='OrderColor':return
    old=current(item)
    if choice is not None:
        from core.permissions import field_access
        access=field_access(actor,type(item))
        operation='is_create' if item.pk is None else 'is_update'
        if any(k in access and not access[k][operation] for k in ['old_price','old_amount']):
            raise ValidationError({'_pricing':'没有订单单价或金额的字段修改权限。'})
        if is_historical(item):raise ValidationError({'_pricing':'历史承接记录保留原价格；请在新业务单据中明确采用报价。'})
        values,state=selection(item,choice,actor,lock=True)
    elif old and not is_historical(item):
        state=old
        dependencies={'old_prod_id':state['prod_id'],'old_unit':state['line_unit']}
        if any(key in data and data[key]!=value for key,value in dependencies.items()):
            invalidate(item,state,data,'物料或数量单位已改变，需重新选择报价或明确手工价格。')
            return
        if state['status']=='invalid':return
        changed=False
        if 'old_price' in data and item.old_price!=(None if state['price'] is None else Decimal(state['price'])):
            for key in list(state):
                if key.startswith('quote_') or key=='original_price_unit':state.pop(key)
            state.update(mode='manual',price_basis='manual',price=None if item.old_price is None else str(item.old_price))
            changed=True
        if 'old_amount' in data and item.old_amount!=(None if state['amount'] is None else Decimal(state['amount'])):
            state.update(amount_mode='manual',manual_amount=None if item.old_amount is None else str(item.old_amount))
            changed=True
        if not changed and not {'old_order_qty','old_gray_qty','old_card_qty'}.intersection(data):return
        values,state=calculate(item,state)
    else:return
    for key,value in values.items():setattr(item,key,value)
    item._order_pricing_state=state


def invalidate(item,state,data,reason):
    state=deepcopy(state)
    state.update(status='invalid',invalid_reason=reason,invalidated_at=timezone.now().isoformat())
    for key in ['old_price','old_amount']:
        if key not in data:setattr(item,key,None)
    if 'old_price' in data or 'old_amount' in data:
        for key in list(state):
            if key.startswith('quote_') or key=='original_price_unit':state.pop(key)
        state.update(mode='manual',price_basis='manual',status='manual_input',price=None if item.old_price is None else str(item.old_price),
                     amount=None if item.old_amount is None else str(item.old_amount))
    item._order_pricing_state=state


def saved(item,data,actor):
    if item.SOURCE_TABLE=='OrderColor' and hasattr(item,'_order_pricing_state'):
        state=item._order_pricing_state
        from .source_entry_services import entry_for
        ctx,_=SourceDocumentContext.objects.get_or_create(entity=item._meta.label,object_id=item.pk,
            defaults={'entry_name':entry_for(item) or 'OrderColor'})
        before=snapshot(ctx)
        ctx.effects={**ctx.effects,KEY:state}
        persist(ctx,actor)
        record(ctx,'order_price_adoption',before,actor,'订单价格采用/重新计算；原报价及原行保留')
    if item.SOURCE_TABLE=='OrderMain' and 'old_customer_id' in data:
        for line in lines_for(item):
            state=current(line)
            if state and state['customer_id']!=item.old_customer_id and not is_historical(line):
                line=locked(line);before=snapshot(line)
                invalidate(line,state,{},'订单客户已改变，需重新选择报价或明确手工价格。')
                persist(line,actor);saved(line,{},actor)
                record(line,'order_price_invalidated',before,actor,'订单客户变更，不沿用旧报价')


def info(item):
    state=current(item)
    if state and state.get('quote_id'):
        state['source_exists']=(model('FixedPriceDetail').objects.filter(pk=state['quote_id']).exists()
                                and model('FixedPrice').objects.filter(pk=state['quote_head_id']).exists())
    return state


def summary(head,actor=None):
    rows=list(lines_for(head,actor));known=[r.old_amount for r in rows if r.old_amount is not None]
    unknown=sum(r.old_amount is None for r in rows)
    return {'line_count':len(rows),'unpriced_count':unknown,'known_subtotal':str(sum(known,Decimal('0'))),
        'total':None if unknown else str(sum(known,Decimal('0')))}
