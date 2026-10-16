"""报价明细原触发检查；重复异常照存，审核限制按原语句列判断。"""
from plugins.erp_base.source_provenance import reference as source_reference
from django.core.exceptions import ValidationError
from .source_stock_services import raw
from .source_quality_reports import key
from .source_business_updates import matching
from .source_package_operations import reader,check_scope
from .source_package_labels import varchar
from .source_continuation import save_effect


def inspect(item,operation,right_status_in_statement=False,query=reader):
    heads=list(matching(reader('Quote','erp_sales'),SheetSeries=raw(item,'SheetSeries')).order_by('pk'))
    customer=varchar(raw(heads[-1],'CustomerID'),50) if heads else ''
    color=varchar(raw(item,'ColorNum'),20) if heads or operation=='delete' else ''
    product=varchar(raw(item,'ProdID'),20) if heads else ''
    status=raw(item,'RightStatus') if heads or operation=='delete' else None
    pairs=[];sources=[item,*heads]
    if key(customer or '')!='' and key(color or '')!='' and operation!='delete':
        for head in matching(reader('Quote','erp_sales'),CustomerID=customer).order_by('pk'):
            for line in matching(reader('QuoteDetail','erp_sales'),SheetSeries=raw(head,'SheetSeries'),ColorNum=color,ProdID=product).order_by('pk'):
                pairs.append((head,line));sources.extend([head,line])
    customers=list(matching(reader('PCustomer','erp_base'),CustomerID=customer).order_by('pk')) if customer else []
    sources.extend(customers);check_scope(sources,query)
    threshold=1 if operation=='insert' else 2
    duplicate=operation!='delete' and len(pairs)>threshold
    approved=status==10 and (operation=='delete' or operation=='update' and not right_status_in_statement)
    return {'report':'报价明细原触发检查','rows':[{'record_id':item.pk,'source': source_reference(item),'operation':operation,
        'CustomerID':customer,'ColorNum':color,'ProdID':product,'RightStatus':status,'join_count':len(pairs),
        'duplicate_threshold':None if operation=='delete' else threshold,'duplicate':duplicate,
        'right_status_in_statement':right_status_in_statement,'approved_block':approved,'original_rejected':duplicate or approved}],
        'candidate_rows':[{'header_id':head.pk,'record_id':line.pk,'source': source_reference(line)} for head,line in pairs],
        'supplemental_rows':[{'record_id':row.pk,'ShortName':raw(row,'ShortName')} for row in customers],
        'notes':['新增重复阈值>1，修改>2；按原表头连接倍数COUNT，不去重，也不提取数字色号。',
            'UPDATE(RightStatus)表示语句包含该列，即使值未改变也成立；缺表头时修改触发器读不到审核状态。',
            '重复异常按项目要求照存并留检查事实；审核修改/删除限制仍按原规则执行，见E82。']}


def saved(item,data,created,actor):
    report=inspect(item,'insert' if created else 'update','old_right_status' in data)
    if report['rows'][0]['approved_block']:
        raise ValidationError({'old_right_status':'原报价明细已审核；先办理RightStatus变更，再修改其他字段。'})
    save_effect(item,'quote_trigger_check',report,actor,'保留原报价触发检查及重复异常来源')


def removing(item):
    if raw(item,'RightStatus')==10:
        raise ValidationError({'old_right_status':'原报价明细已审核，按QuoteDetail_Del不能删除。'})
