"""订单首次开卡、明确采用路线；不从已有工卡冒充首次开卡。"""
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction
from .business import locked
from .source_phase3_operations import model,source
from .source_business_updates import matching,update_rows
from .source_stock_services import raw
from .source_continuation import origin,save_effect
from .source_calculations import store_value
from .source_execution_state import require_available


def route_rows(route):
    kind=raw(route,'FieldType')
    if kind is None or kind.rstrip(' ').upper()!='PRODUCTION':
        raise ValidationError({'route':'请选择工艺路线资料。'})
    return matching(source('p_FieldValidSub'),FieldType='Production',Code=raw(route,'Code')).order_by('old_sort_value','pk')


@transaction.atomic
def adopt_route(job,route,actor,at,reason):
    from . import source_services as services
    from .source_card_reverse import require_current_plan
    job=locked(job);route=locked(route);require_current_plan(job)
    services.editable([job])
    existing=matching(source('JobProcess'),SheetSeries=raw(job,'SheetSeries'))
    if existing.exists():raise ValidationError({'route':'已有计划工序，请在明细中保留/调整原行；采用路线只初始化空计划，不覆盖实绩。'})
    details=list(route_rows(route));ids=[]
    for detail in details:
        detail=locked(detail)
        data={'source_parent_1':job,'_entry':{'TwiJobSheet':'TwiJobProcess','SaleJobSheet':'SaleJobProcess','PrintJobSheet':'PrintJobProcess'}.get(job.entry_name,'JobProcess'),
            'old_process_no':raw(detail,'SortValue'),'old_process_id':raw(detail,'SubCode'),'old_status':'0'}
        definitions=list(matching(source('p_Process'),ProcessID=raw(detail,'SubCode')).order_by('pk'))
        stations={raw(row,'StationID') for row in definitions}
        if len(stations)==1:data['old_station_id']=stations.pop()
        line=services.write(model('JobProcess'),data,actor=actor,apply_effects=False)
        save_effect(line,'route_origin',{'route':origin(route),'detail':origin(detail),'process_candidates':[row.pk for row in definitions],
            'at':at,'reason':reason},actor,reason);ids.append(line.pk)
    update_rows(type(job).objects.filter(pk=job.pk),{'ProductionID':raw(route,'Code')},actor,'adopt_order_route',reason)
    save_effect(job,'route_adoption',{'route':origin(route),'detail_ids':[row.pk for row in details],'process_ids':ids,'at':at,'reason':reason},actor,reason)
    services.finish([job],actor);job.refresh_from_db();return job


@transaction.atomic
def open_card(line,actor,head,members,assignments,quantity,rolls,unit,yarn,route,at,reason,number_prefix=None):
    from . import source_services as services
    line=locked(line);head=locked(head)
    require_available(line);require_available(head)
    if line.source_parent_1_id is not None and line.source_parent_1_id!=head.pk:
        raise ValidationError({'order':'订单颜色行不属于所选订单。'})
    if not matching(type(head).objects.filter(pk=head.pk),SheetSeries=raw(line,'SheetSeries')).exists():
        raise ValidationError({'order':'订单原流水与颜色行不一致。'})
    selected=[(line,quantity)]
    for row in members:
        other=locked(row['line'])
        require_available(other)
        if other.pk==line.pk or any(item.pk==other.pk for item,_ in selected):
            raise ValidationError({'members':'每条实际订单行只选一次；同原号的不同记录可分别选择。'})
        selected.append((other,row['quantity']))
    from .source_order_pricing import head_for
    heads=[head]+[head_for(item,actor) for item,_ in selected[1:]]
    for parent in heads:require_available(parent)
    if any(raw(h,'CustomerID')!=raw(head,'CustomerID') or raw(item,'ProdID')!=raw(line,'ProdID') or raw(item,'Unit')!=raw(line,'Unit')
           for h,(item,qty) in zip(heads,selected)):
        raise ValidationError({'members':'首次共卡按同客户、物料和数量单位办理；跨客户/物料保留各自工卡再走明确合卡。'})
    common=['CustomerID','DetailCustName','CustSelfNo','ContractNo','BusinessUnitID','SalerID','SalerGroupID','LabelID']
    item_fields=['CheckNo','ProdID','LotNo','Spec','ColorID','ColorNum','ColorE','ColorRGB','CustColorNum','ProductionID','StandCraftNo',
        'WidthDn','WidthUp','WeightDn','WeightUp','WidthKindID','WeightUnit','CustFabricName','CustSelfNoDetail','ColorRemarks','OrderQty','CustGrayID']
    job=model('JobSheet')();data={}
    for parent,names in [(head,common),(line,item_fields)]:
        for name in names:
            if name in parent.SOURCE_FIELDS and name in job.SOURCE_FIELDS:data.update([store_value(job,name,raw(parent,name))])
    total=None if any(qty is None for _,qty in selected) else sum((qty for _,qty in selected),Decimal('0'))
    data.update(_entry='JobSheet',old_sheet_date=at,old_create_date=at,old_ori_order_series=raw(head,'SheetSeries'),
        old_order_sheet_no=raw(head,'SheetNo'),old_order_sheet_date=raw(head,'SheetDate'),old_pre_vat_qty=total,
        old_pre_rolls=rolls,old_assign_unit=unit,old_yarn_category=yarn,old_remarks=reason)
    job=services.write(type(job),data,actor=actor,apply_effects=False)
    number=raw(job,'NewSheetNo');sheet_number=number
    if number_prefix:
        from .numbering import rules,matches
        if any(matches(job,r,'JobSheet') for r in rules(type(job)).filter(target_field='old_new_sheet_no',auto_enabled=True)):
            raise ValidationError({'number_prefix':'已启用此模型的数字编号规则，请在编号管理中维护前缀，本次前缀留空。'})
        from .source_numbers import reserve,integer
        from django.utils import timezone
        day=timezone.localtime(at).strftime('%y%m%d');prefix=number_prefix+'-'+day
        def initial():
            return max((integer(value[len(prefix):],'old_new_sheet_no') for value in type(job).objects.filter(
                old_new_sheet_no__startswith=prefix).values_list('old_new_sheet_no',flat=True)),default=0)
        seq=reserve(job,'old_new_sheet_no',{'kind':'first_card_prefix','prefix':prefix},initial,actor)
        suffix=str(seq).zfill(2);number=prefix+suffix;sheet_number=day+number_prefix+suffix
    # 旧12位带前缀编号与简单流水分开；不能把8位数字按12位格式截断。
    update_rows(type(job).objects.filter(pk=job.pk),{'NewSheetNo':number,'SheetNo':sheet_number},actor,'first_card_number',reason)
    job.refresh_from_db();created=[]
    for index,((item,qty),parent) in enumerate(zip(selected,heads)):
        member=services.write(model('JobCombineOrder'),{'_entry':'JobCombineOrder','source_parent_1':job,
            'old_check_no':raw(item,'CheckNo'),'old_order_sheet_no':raw(parent,'SheetNo'),'old_customer_id':raw(parent,'CustomerID'),
            'old_prod_id':raw(item,'ProdID'),'old_color_num':raw(item,'ColorNum'),'old_order_qty':raw(item,'OrderQty'),
            'old_combine_qty':qty,'old_is_master_order':index==0},actor=actor,apply_effects=False)
        save_effect(member,'first_card_order',{'order':origin(parent),'line':origin(item),'quantity':qty,'at':at,'reason':reason},actor,reason)
        created.append(member.pk)
    assigned=[]
    allowed={'AssignNo','ReceSheetNo','GrayID','LotNo','Spec','Rolls','Packs','WeightQty','LengthQty','WareHouseID','SupplierID','StorageUnitID','Remarks'}
    for values in assignments:
        if set(values)-allowed:raise ValidationError({'assignments':'预配含未登记字段：'+','.join(set(values)-allowed)})
        assign=services.write(model('JobAssign'),{'_entry':'JobAssign','source_parent_1':job,
            **{model('JobAssign').SOURCE_FIELDS[k]:v for k,v in values.items()}},actor=actor,apply_effects=False)
        assigned.append(assign.pk)
    save_effect(job,'first_card_origin',{'order':origin(head),'line':origin(line),'members':created,'assignments':assigned,
        'order_allocated_quantity':total,'requested_rolls':rolls,'unit':unit,'yarn':yarn,
        'number_policy':'legacy_prefix' if number_prefix else 'complete_generated_number','number_prefix':number_prefix,'at':at,'reason':reason},actor,reason)
    # 预配只采用用户明确输入的实料来源及计划数量，不产生实际领用或库存。
    if route is not None:adopt_route(job,route,actor,at,reason)
    services.finish([job],actor);job.refresh_from_db();return job
