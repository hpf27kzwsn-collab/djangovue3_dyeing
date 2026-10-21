"""APP订单原保存/替换：使用原字段，旧版行留档，列表重复项逐行保留。"""
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from django.db import transaction
from django.utils import timezone
from .business import snapshot
from .source_quality_reports import rows
from .source_stock_services import raw
from .source_business_updates import matching
from .source_execution_state import active
from .source_services import write
from .source_master_data import retain
from .source_continuation import save_effect
from .source_entry_registry import ENTRY_RULES
from .source_numbers import generate
from .source_foundation_scalars import split_with_row_number

DETAIL_FIELDS='ColorID ColorNum CustColorNum CustFabricName CustSelfProduct LotNo DlvDate OrderQty OrderRolls'.split()
ATTE_FIELDS='AtteCode AtteValue Description FieldType'.split()


def check_save():
    """sp_App_CheckSaveOrder原过程没有检查条件。"""
    return {'Code':0,'Msg':''}


def original_lists(parameters,fields,anchor):
    columns={f:{r['RowNo']:r['Name'] for r in split_with_row_number(parameters[f+'List'],'|' if f=='Description' else ',')} for f in fields}
    result=[]
    for number in columns[anchor]:
        item={f:columns[f].get(number) for f in fields}
        for f in ['OrderQty','OrderRolls']:
            if f in item and item[f] is not None:item[f]=Decimal(item[f] or '0').quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
        if 'DlvDate' in item and item['DlvDate'] is not None:
            item['DlvDate']=timezone.make_aware(datetime.fromisoformat(item['DlvDate'] or '1900-01-01'))
        result.append(item)
    return result


def check_modify(series):
    blocked=matching(active(rows('OrderMain','erp_sales')),SheetSeries=series).filter(old_sheet_status=10).exists()
    return {'Code':1 if blocked else 0,'Msg':'当前单据已经审核，不能修改！' if blocked else ''}


@transaction.atomic
def save(parameters,actor,original=None,details=None,requirements=None):
    now=timezone.localtime()
    employee=parameters['EmpID'] or ''
    customers=list(matching(active(rows('HEmployee','erp_base')),EmpID=employee).filter(old_is_customer=True).order_by('pk'))
    customer=raw(customers[-1],'CustomerID') if customers else None
    names=list(matching(active(rows('HEmployee','erp_base')),EmpID=employee).order_by('pk'))
    name=raw(names[-1],'Name') if names else None
    source_customers=list(matching(active(rows('PCustomer','erp_base')),CustomerID=customer).order_by('pk'))
    master=source_customers[-1] if source_customers else None
    model=rows('OrderMain','erp_sales').model
    if original is None:
        series=generate(model(),'SheetSeries',ENTRY_RULES[model._meta.label]['OrderMain']['number_fields']['SheetSeries'],actor,now)
        creator,created=name,now
        retained=[]
    else:
        series=raw(original,'SheetSeries')
        mains=list(matching(active(rows('OrderMain','erp_sales')),SheetSeries=series).order_by('pk'))
        creator,created=(raw(mains[-1],'Creater'),raw(mains[-1],'CreateDate')) if mains else (None,None)
        retained=[]
        for table in ['OrderAtte','OrderColor','OrderMain']:
            for old in matching(active(rows(table,'erp_sales')),SheetSeries=series).select_for_update().order_by('pk'):
                retained.append({'entity':old._meta.label,'id':old.pk,'before':snapshot(old)})
                retain(old,actor,'sp_APP_ModifyOrder替换前原行留档')
    unit=parameters['AssignUnit']
    values={f:parameters[f] for f in ['DetailCustName','CustSelfNo','ContractNo']}
    values.update(SheetSeries=series,SheetNo=series,CustomerID=customer if customer is not None else parameters['CustomerIDMain'],
        AssignUnit=None if unit is not None and unit<0 else unit,SheetDate=now if original is None else created,
        SalerID=None if master is None else raw(master,'SalerID'),LabelID=None if master is None else raw(master,'LabelID'),
        ExchangeRate=None if master is None else raw(master,'Deposit'),OrderKindID='01',SheetKind=0,SheetType=10,Creater=creator,CreateDate=created)
    if original is not None:values.update(Modifyer=name,ModifyDate=now)
    head=write(model,{model.SOURCE_FIELDS[f]:v for f,v in values.items()},actor=actor)
    created_rows=[head]
    for index,detail in enumerate(original_lists(parameters,DETAIL_FIELDS,'ColorID') if details is None else details,1):
        detail=dict(detail)
        detail.update(SheetSeries=series,CheckNo=series+'-'+('00'+str(index))[-2:])
        target=rows('OrderColor','erp_sales').model
        created_rows.append(write(target,{target.SOURCE_FIELDS[f]:v for f,v in detail.items()},actor=actor))
    for detail in original_lists(parameters,ATTE_FIELDS,'AtteCode') if requirements is None else requirements:
        detail=dict(detail)
        detail['SheetSeries']=series
        target=rows('OrderAtte','erp_sales').model
        created_rows.append(write(target,{target.SOURCE_FIELDS[f]:v for f,v in detail.items()},actor=actor))
    save_effect(head,'app_order_save',{'retained':retained,'created':[{'entity':r._meta.label,'id':r.pk} for r in created_rows],
        'original_id':None if original is None else original.pk},actor,'APP订单保存/替换；保留全部列表项与旧行')
    return head
