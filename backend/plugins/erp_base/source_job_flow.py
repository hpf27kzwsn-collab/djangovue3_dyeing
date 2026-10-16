"""工卡拆分、合卡关系及订单分配量转移；原实际报工和库存不随计划复制。"""
from plugins.erp_base.source_provenance import reference as source_reference
from django.apps import apps
from django.db import transaction
from .business import locked
from .source_stock_services import raw
from .source_calculations import store_value
from .source_business_updates import matching, update_rows
from .source_continuation import origin, save_effect, copy_new


def rows(name):
    return apps.get_model('erp_production.SourceDye'+name).objects.all()


def difference(before, adopted):
    return None if before is None or adopted is None else before-adopted


def create_card(item, actor, quantity, rolls, unit, at, reason, processes):
    from . import source_services as services
    from .source_card_reverse import require_current_plan
    require_current_plan(item)
    # 计划采用保留业务属性；既有执行量、设备执行、质量实绩保留在来源快照。
    excluded = ['NewSheetNo','PreVatQty','PreRolls','PrePacks','AssignUnit','VatNo','FinishDate','StartDate','PlanDate',
        'CurrProcessID','CurrProcessNo','CurrStationID','NextProcessID','NextStationID','MachineID',
        'IsSplited','SplitCardReason','IsProdInFinished','IsPause','IsOver','Finish','Loss','RealLoss',
        'Kg','WeightQty','Weight','Pound','ProdQty','Pkg','PRolls','PlengthQyt','PDots','CHECKDots',
        'Checker','Grade','YAvgdots','BarCode','DB2BarCode','ReleaseCardDate','ReleaseCardDateTwo',
        'Sender','Receiver','SetHurryTime','SetPauseBegTime','SetPauseEndTime','HurryInfo','PauseInfo']
    excluded += [key for key in item.SOURCE_FIELDS if key.startswith('SumAssigned') or key.startswith('SumProcess')]
    values = copy_new(item, type(item), excluded)
    values.update(_entry='JobSheet',old_sheet_date=at,old_remarks=reason,
        old_ori_source_job_no=raw(item,'SheetNo'),old_ori_jobsheet_no=raw(item,'SheetNo'),old_assign_unit=unit)
    values.update([store_value(item,'PreVatQty',quantity),store_value(item,'PreRolls',rolls)])
    target = services.write(type(item),values,actor=actor,apply_effects=False)
    # JobSheet原入口先生成NewSheetNo，再按原SheetNo表达式采用；不能复制来源空号抑制生成。
    number=raw(target,'NewSheetNo')
    sheet_no=number[4:10]+number[:3]+number[10:12] if raw(target,'OriSourceJobNo') in [None,''] else number
    update_rows(type(target).objects.filter(pk=target.pk),{'SheetNo':sheet_no},actor,'card_number',reason)
    target.refresh_from_db()
    adopted=[]
    model=rows('JobProcess').model
    for process in {p.pk:p for p in processes}.values():
        process=locked(process)
        # 工序、站别、参数名称/理论值均按所选原行采用，实测值和报工事实不继承。
        plan_fields=['ProcessNo','ProcessID','StationID','CraftParam']
        plan_fields += [key for key in model.SOURCE_FIELDS if key.startswith(('PPName','TheoryValue','PPPName','PValue'))]
        data=dict(store_value(model(),key,raw(process,key)) for key in plan_fields)
        data.update(source_parent_1=target,old_status='0')
        new=services.write(model,data,actor=actor,apply_effects=False)
        adopted.append({'source':origin(process),'target_id':new.pk})
    return target,adopted


@transaction.atomic
def split_card(item, actor, quantity, rolls, unit, at, reason, processes):
    from . import source_services as services
    item=locked(item)
    before=origin(item)
    target,adopted=create_card(item,actor,quantity,rolls,unit,at,reason,processes)
    values={'PreVatQty':difference(raw(item,'PreVatQty'),raw(target,'PreVatQty')),
        'PreRolls':difference(raw(item,'PreRolls'),raw(target,'PreRolls')),'IsSplited':True,'SplitCardReason':reason}
    if unit is None or raw(item,'AssignUnit') != unit:
        # 跨单位没有换算依据时保留来源计划；目标计划与未扣减原因明确留档。
        values.pop('PreVatQty');values.pop('PreRolls')
    update_rows(type(item).objects.filter(pk=item.pk),values,actor,'card_split','拆卡：'+reason)
    save_effect(target,'card_adoption',{'kind':'split','source':before,'processes':adopted,
        'source_changes':values,'unit':unit,'requested_quantity':quantity,'requested_rolls':rolls,'at':at,'reason':reason,
        'quantity_deducted': 'PreVatQty' in values},actor,reason)
    services.finish([target],actor)
    return target


@transaction.atomic
def merge_cards(item, actor, members, quantity, rolls, unit, at, reason, processes):
    from . import source_services as services
    item=locked(item)
    selected=[locked(value) for value in {row.pk:row for row in [item,*members]}.values()]
    from .source_card_reverse import require_current_plan
    for member in selected:require_current_plan(member)
    target,adopted=create_card(item,actor,quantity,rolls,unit,at,reason,processes)
    links=[]
    for member in selected:
        model=rows('JobCombine').model
        data=dict(store_value(model(),key,value) for key,value in [
            ('JobSheetNo',raw(member,'SheetNo')),('Qty',raw(member,'PreVatQty')),
            ('Rolls',raw(member,'PreRolls')),('CheckNo',raw(member,'CheckNo'))])
        data.update(source_parent_1=target,old_remarks=reason)
        link=services.write(model,data,actor=actor,apply_effects=False)
        links.append({'source':origin(member),'target_id':link.pk})
    save_effect(target,'card_adoption',{'kind':'merge','members':links,'processes':adopted,
        'unit':unit,'at':at,'reason':reason},actor,reason)
    services.finish([target],actor)
    return target


@transaction.atomic
def transfer_allocation(item, actor, target, quantity, at, reason):
    from . import source_services as services
    item,target=locked(item),locked(target)
    from .source_card_reverse import require_current_plan
    require_current_plan(item);require_current_plan(target)
    before=origin(item)
    values=copy_new(item,type(item),['SheetSeries','CombineQty'])
    values.update(source_parent_1=target,**dict([store_value(item,'CombineQty',quantity)]))
    adopted=services.write(type(item),values,actor=actor,apply_effects=False)
    update_rows(type(item).objects.filter(pk=item.pk),{'CombineQty':difference(raw(item,'CombineQty'),raw(adopted,'CombineQty'))},
        actor,'order_allocation_transfer',reason)
    save_effect(adopted,'order_transfer_origin',{'source':before,'target':origin(target),
        'quantity':raw(adopted,'CombineQty'),'requested_quantity':quantity,'at':at,'reason':reason},actor,reason)
    return adopted


def combine_members(item, query=None):
    members=rows('JobCombine') if query is None else query('JobCombine','erp_production')
    members=matching(members,SheetSeries=raw(item,'SheetSeries')).order_by('pk')
    data=[{'id':row.pk,'source': source_reference(row),'JobSheetNo':raw(row,'JobSheetNo'),
        'Qty':raw(row,'Qty'),'Rolls':raw(row,'Rolls'),'CombineKind':raw(row,'CombineKind')} for row in members]
    return {'report':'工卡合并原关系','rows':data,
        'notes':['按关系原行逐条列出，同名工卡和重复关系均保留；合卡计划不代替原卡实际收发。']}


@transaction.atomic
def adopt_combine_link(item, actor, target, at, reason):
    """原合卡表头缺失时，也能明确采用所选原关系，原孤立行继续留档。"""
    from . import source_services as services
    item,target=locked(item),locked(target)
    from .source_card_reverse import require_current_plan
    require_current_plan(item);require_current_plan(target)
    values=copy_new(item,type(item))
    values['source_parent_1']=target
    result=services.write(type(item),values,actor=actor,apply_effects=False)
    save_effect(result,'combine_link_origin',{'source':origin(item),'target':origin(target),'at':at,'reason':reason},actor,reason)
    return result


@transaction.atomic
def sync_combined_process(item, actor, targets, machine, time_way, at, reason):
    """明确采用Sp_DPSyncToCombineSheets的工序回写分支；目标原行由本次选择。"""
    item=locked(item)
    adopted=[]
    for target in {row.pk:row for row in targets}.values():
        target=locked(target)
        from .source_card_reverse import require_current_plan
        for job in matching(rows('JobSheet'),SheetSeries=raw(target,'SheetSeries')):require_current_plan(job)
        before=origin(target)
        values={'MachineID':machine,'Status':raw(item,'Status')}
        if time_way in [0,1]:values['StartTime']=at
        if time_way in [0,2]:values['EndTime']=at
        update_rows(type(target).objects.filter(pk=target.pk),values,actor,'combined_process_sync',reason)
        # 原INNER JOIN要求下一序号恰好+1；断档保留工卡当前字段。
        number=raw(target,'ProcessNo')
        next_process=None if number is None else matching(rows('JobProcess'),SheetSeries=raw(target,'SheetSeries')).filter(
            old_process_no=number+1).order_by('pk').first()
        if next_process is not None:
            update_rows(matching(rows('JobSheet'),SheetSeries=raw(target,'SheetSeries')),
                {'CurrProcessNo':number,'CurrProcessID':raw(target,'ProcessID'),'CurrStationID':raw(target,'StationID'),
                 'NextProcessID':raw(next_process,'ProcessID'),'NextStationID':raw(next_process,'StationID')},
                actor,'combined_job_progress',reason)
        adopted.append({'source':before,'changes':values})
    save_effect(item,'combined_process_sync',{'source':origin(item),'targets':adopted,'time_way':time_way,
        'machine':machine,'at':at,'reason':reason},actor,reason)
    return item
