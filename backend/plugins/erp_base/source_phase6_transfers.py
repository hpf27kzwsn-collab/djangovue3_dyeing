"""按 s_FieldCopy 原七列将选定采购明细转到货通知；整批保存后执行联动。"""
import json
from pathlib import Path
from django.core.exceptions import ValidationError
from django.db import transaction
from .business import locked, record, snapshot, persist
from .source_phase3_operations import model
from .source_stock_services import raw
from .source_entry_services import save_context
from .source_trial_steps import equal
from .source_transfer_numbers import values as number_values


def purchase_fields():
    links = json.loads(Path(__file__).with_name('source_phase6_field_links.json').read_text(encoding='utf8'))
    return [r for r in links['field_copy'] if r['DataTableName'] == 'PurNondeliveryList'
            and r['DestDataTableName'] == 'ArrivalNoticeDetail']


@transaction.atomic
def purchase_to_arrival(head, selected, actor):
    from . import source_services as services
    head = locked(head)
    if head.SOURCE_TABLE != 'ArrivalNotice':
        raise ValidationError({'source': '此转单的目标为到货通知单。'})
    services.editable([head])
    before = snapshot(head)
    fields = purchase_fields(); target = model('ArrivalNoticeDetail'); created = []
    for original in selected:
        original = locked(original)
        if original.SOURCE_TABLE != 'PurDetail':
            raise ValidationError({'selected': '请选取采购明细原行。'})
        values = {target.SOURCE_FIELDS[r['DestFieldName']]: raw(original, r['FieldName']) for r in fields}
        for key, value in values.items():
            try:
                target._meta.get_field(key).clean(value, None)
            except ValidationError as error:
                raise ValidationError({'selected': '采购记录 '+str(original.pk)+' 的 '+key+
                    ' 不能按原到货字段保存：'+'；'.join(error.messages)+'。整批未转入，采购原值保留。'}) from error
        values.update(source_parent_1=head, _entry='ArivalNoticeDetail')
        line = services.write(target, values, actor=actor, apply_effects=False)
        context = save_context(line, actor, 'ArivalNoticeDetail')
        context.effects['field_copy_origin'] = {'entry': 'PurNondeliveryList',
            'source_entity': original._meta.label, 'source_id': original.pk,
            'source_snapshot': snapshot(original), 'mapping': fields,
            'mode': 'explicit_selected_purchase_row'}
        persist(context, actor)
        created.append(line)
    # 明细逐条完成后，才执行整单联动；不按相同原编号、相同值合并。
    services.finish([head, *created], actor)
    record(head, 'purchase_to_arrival', before, actor,
           '按原七列转入；采购来源行顺序：'+str([row.pk for row in selected])+
           '；到货明细：'+str([row.pk for row in created]))
    return {'report': '采购转到货通知', 'rows': [
        {'source_id': original.pk, 'target_id': line.pk, 'PurDetailNo': raw(line, 'PurDetailNo')}
        for original, line in zip(selected, created)],
        'notes': ['按明确选择的采购原行转入；重复来源及重复编号逐行保存。',
                  '原选择视图的主表连接可能重复；本操作选择具体采购明细，不猜测缺失的旧客户端转单按钮行为。']}


@transaction.atomic
def quote_to_order(line, quote, fabric_id, actor, sheet_no=None, sheet_series=None, check_no=None):
    """缺原报价联查视图时，使用明确选定的报价头、明细生成新的订单草稿。"""
    from . import source_services as services
    line=locked(line);quote=locked(quote)
    if line.SOURCE_TABLE!='QuoteDetail' or quote.SOURCE_TABLE!='Quote':
        raise ValidationError({'source':'请选取报价明细与报价表头。'})
    if not equal(raw(line,'SheetSeries'),raw(quote,'SheetSeries')):
        raise ValidationError({'quote':'所选报价表头流水与此明细不一致；重复流水的表头可以明确选择。'})
    head_model=model('OrderMain');detail_model=model('OrderColor')
    fields=['BusinessUnitID','CurrencyID','CustomerID','ExchangeRate','Linker','SalerID','SettleID']
    values={head_model.SOURCE_FIELDS[name]:raw(quote,name) for name in fields}
    values.update(_entry='OrderMain',old_price_unit=raw(line,'PriceUnit'),
        **number_values(sheet_no=sheet_no,sheet_series=sheet_series))
    head=services.write(head_model,values,actor=actor,apply_effects=False)
    detail=services.write(detail_model,{'_entry':'OrderColor','source_parent_1':head,
        'old_price':raw(line,'Price'),'old_spec':raw(line,'Spec'),'old_fabric_id':fabric_id,**number_values(check_no=check_no)},
        actor=actor,apply_effects=False)
    context=save_context(head,actor,'OrderMain')
    context.effects['quote_transfer_origin']={'source_entry':'vwQuoteMDToOrderMD',
        'mode':'explicit_quote_header_and_line','quote':snapshot(quote),'line':snapshot(line),
        'header_fields':fields,'PriceUnit_source':'QuoteDetail.PriceUnit','FabricID_explicit':fabric_id,
        'missing_target_fields':{'OrderMain.PreUnitProfit':None,'OrderColor.Structure':raw(line,'Structure')},
        'notes':['原联查视图缺失，当前按具体头和明细转单，未模拟未知视图筛选。',
                 'FabricID由操作参数明确指定或留NULL，不将QuoteDetail.ProdID当作FabricID。',
                 '原目标Structure已缺失，报价原值保留在来源快照；PreUnitProfit来源未知。']}
    persist(context,actor)
    services.finish([head,detail],actor)
    record(head,'quote_to_order',{'exists':False},actor,
        '报价头ID='+str(quote.pk)+'；报价明细ID='+str(line.pk)+'；明确替代旧视图转单')
    return head


@transaction.atomic
def purchase_to_product(line, purchase, quantity_basis, sheet_kind, stock_unit,
                        warehouse_id, customer_id, prod_id, actor, sheet_no=None, sheet_series=None):
    """明确采购头/行及入库口径；不冒充已丢失ProdInDetail的旧转单关系。"""
    from . import source_services as services
    from .source_calculations import store_value
    line=locked(line);purchase=locked(purchase)
    if line.SOURCE_TABLE!='PurDetail' or purchase.SOURCE_TABLE!='PurMain':
        raise ValidationError({'source':'请选择采购明细和采购表头。'})
    if not equal(raw(line,'SheetSeries'),raw(purchase,'SheetSeries')):
        raise ValidationError({'purchase':'所选采购表头与明细流水不一致。'})
    if quantity_basis not in ['weight','length']:
        raise ValidationError({'quantity_basis':'须明确采购Qty采用重量还是长度原数值。'})
    target=model('ProdIn')
    names=['FabricID','Spec','LotNo','ColorID','ColorNum','Rolls','Price','Amount','CheckNo','Remarks']
    values=dict(store_value(target(),name,raw(line,name)) for name in names)
    values.update(_entry='ProdIn',**number_values(sheet_no=sheet_no,sheet_series=sheet_series),old_business_unit_id=raw(purchase,'BusinessUnitID'),
        old_sheet_kind=sheet_kind,old_stock_unit=stock_unit,old_ware_house_id=warehouse_id,
        old_customer_id=customer_id,old_prod_id=prod_id,
        old_weight_qty=raw(line,'Qty') if quantity_basis=='weight' else None,
        old_length_qty=raw(line,'Qty') if quantity_basis=='length' else None)
    head=services.write(target,values,actor=actor,apply_effects=False)
    context=save_context(head,actor,'ProdIn')
    context.effects['purchase_product_origin']={'purchase':snapshot(purchase),'line':snapshot(line),
        'mode':'explicit_purchase_to_current_product_header','mapping':names,
        'quantity_basis':quantity_basis,'sheet_kind':sheet_kind,'stock_unit':stock_unit,
        'warehouse_id':warehouse_id,'customer_id':customer_id,'prod_id':prod_id,
        'notes':['原ProdInDetail缺失，PurDetailNo及完整采购来源保留在已有上下文。',
                 '复制数值按最新目标字段小数精度四舍五入；更高精度采购原值完整保存在来源快照。',
                 'SupplierID不当作CustomerID，FabricID不当作ProdID，Qty不猜测维度。',
                 '重复转入分别建立新单，不执行无法证明的旧NOT IN排除条件；原选择查询仍列差异。']}
    persist(context,actor)
    services.finish([head],actor)
    record(head,'purchase_to_product',{'exists':False},actor,
        '明确采购头ID='+str(purchase.pk)+'，采购行ID='+str(line.pk)+'；数量维度='+quantity_basis)
    return head


@transaction.atomic
def care_plan_to_article_out(line, head, article, quantity, price, in_detail_no, storage_unit_ids, actor, detail_no=None):
    """选定保养计划原行和具体配件资料办理领料；原计划没有数量，不自动补数量。"""
    from . import source_services as services
    line=locked(line);head=locked(head);article=locked(article)
    if line.SOURCE_TABLE!='MachineCarePlanDetail' or head.SOURCE_TABLE!='ArticleOut' or article.SOURCE_TABLE!='p_Article':
        raise ValidationError({'source':'请选择保养计划明细、配件出库单和配件资料原行。'})
    if not equal(raw(line,'ArticleID'),raw(article,'ArticleID')):
        raise ValidationError({'article':'所选资料代码须与此保养计划明细的配件引用一致；重复代码可明确选择具体资料行。'})
    services.editable([head])
    target=model('ArticleOutDetail')
    fields={'ArticleID':raw(article,'ArticleID'),'ArticleKindID':raw(article,'ArticleKindID'),
        'Spec':raw(article,'Spec'),'SupplierID':raw(article,'SupplierID'),
        'MachineID':raw(line,'MachineID'),'Remarks':raw(line,'Remarks'),
        'OutQty':quantity,'Price':price,'InDetailNo':in_detail_no,'StorageUnitIDs':storage_unit_ids}
    created=services.write(target,{'_entry':'ArticleOutDetail','source_parent_1':head,
        **{target.SOURCE_FIELDS[k]:v for k,v in fields.items()},**number_values(detail_no=detail_no)},actor=actor,apply_effects=False)
    context=save_context(created,actor,'ArticleOutDetail')
    context.effects['care_plan_article_origin']={'plan_detail':snapshot(line),'article':snapshot(article),
        'mode':'explicit_plan_reference_to_article_out','quantity':None if quantity is None else str(quantity),'price':None if price is None else str(price),
        'in_detail_no':in_detail_no,'storage_unit_ids':storage_unit_ids,
        'unit_source':raw(article,'Unit'),
        'notes':['原保养配件耗用表缺失；数量、单价、入库明细及库位由本次操作明确提供。',
                 '资料单位留在来源快照，未隐含换算；重复办理逐次生成出库明细。']}
    persist(context,actor)
    services.finish([head,created],actor)
    record(created,'care_plan_to_article_out',{'exists':False},actor,
        '保养计划明细ID='+str(line.pk)+'；采用配件资料ID='+str(article.pk)+'；明确领料')
    return created


DEPT_PURCHASE={'ArticleDeptApplyDetail':('ArticleDeptApply','ArticlePurMain','source_parent_1','ArticlePurDetail','Article'),
    'StuffDeptApplyDetail':('StuffDeptApply','StuffPurMain','source_parent_3','StuffPurDetail','Stuff')}


@transaction.atomic
def department_apply_to_purchase(line,application,head,quantity,price,actor,detail_no=None):
    """原采购候选之外，明确选择一个部门申请原行转入采购；重复办理分别留来源。"""
    from . import source_services as services
    line=locked(line);application=locked(application);head=locked(head)
    source_table,target_table,parent,entry,prefix=DEPT_PURCHASE[line.SOURCE_TABLE]
    if application.SOURCE_TABLE!=source_table or head.SOURCE_TABLE!=target_table:
        raise ValidationError({'head':'申请及采购表头须与申请明细种类一致。'})
    if not equal(raw(line,'SheetSeries'),raw(application,'SheetSeries')):
        raise ValidationError({'application':'申请表头与明细流水不一致。'})
    services.editable([head])
    target=model('PurDetail')
    fields={prefix+'ID':raw(line,prefix+'ID'),prefix+'KindID':raw(line,prefix+'KindID'),
        prefix+'Name':raw(line,'Name'),prefix+'Unit':raw(line,'Unit'),
        'ApplySheetNo':raw(application,'SheetNo'),'Qty':quantity,'Price':price,
        'Remarks':'' if raw(line,'Remarks') is None else raw(line,'Remarks')}
    created=services.write(target,{'_entry':entry,parent:head,
        **{target.SOURCE_FIELDS[k]:v for k,v in fields.items()},**number_values(detail_no=detail_no)},actor=actor,apply_effects=False)
    context=save_context(created,actor,entry)
    context.effects['department_purchase_origin']={'application':snapshot(application),'line':snapshot(line),
        'quantity':None if quantity is None else str(quantity),'price':None if price is None else str(price),
        'mode':'explicit_department_line_to_purchase',
        'notes':['采用指定原行及表头，不把原候选的聚合行当作单条明细。',
            '原RightStatus=10及NOT EXISTS候选筛选不改；本动作允许明确办理未展示或已办理来源，逐次留档。',
            '单位按申请原行复制，不换算；Amount由本次Qty×Price计算，原申请Amount留在来源快照。',
            '目标PurDetail.Remarks原列不允许NULL；申请NULL备注转为空串，原NULL完整保存在来源快照。']}
    persist(context,actor);services.finish([head,created],actor)
    record(created,'department_apply_to_purchase',{'exists':False},actor,
        '明确部门申请头ID='+str(application.pk)+'；原行ID='+str(line.pk))
    return created


@transaction.atomic
def quote_to_price_adjustment(line,quote,head,actor,detail_no=None):
    """指定报价原行到调价明细；保存后沿用原色号回写及既有审核/反审核链。"""
    from . import source_services as services
    from .source_calculations import store_value
    line=locked(line);quote=locked(quote);head=locked(head)
    if line.SOURCE_TABLE!='QuoteDetail' or quote.SOURCE_TABLE!='Quote' or head.SOURCE_TABLE!='PriceAdjust':
        raise ValidationError({'source':'请选择报价明细、报价头和调价单。'})
    if not equal(raw(line,'SheetSeries'),raw(quote,'SheetSeries')):
        raise ValidationError({'quote':'所选报价头与明细流水不一致。'})
    services.editable([head])
    target=model('PriceAdjustDetail');line_before=snapshot(line);quote_before=snapshot(quote)
    fields={name:raw(line,name) for name in ['ColorNum','ColorID','ColorDepthID','CustColorNum',
        'CustSelfProduct','ProdID','ProcessMemo']}
    old_price,delta=raw(line,'Price'),raw(head,'AdjustMoney')
    fields.update(QuoteDetailNo=raw(line,'DetailNo'),OldPrice=old_price,
        AdjustPrice=None if old_price is None or delta is None else old_price+delta,
        CustomerID=raw(quote,'CustomerID'),SheetNo=raw(quote,'SheetNo'),SheetDate=raw(quote,'SheetDate'))
    created=services.write(target,{'_entry':'PriceAdjustDetail','source_parent_1':head,
        **dict(store_value(target(),name,value) for name,value in fields.items()),**number_values(detail_no=detail_no)},actor=actor,apply_effects=False)
    context=save_context(created,actor,'PriceAdjustDetail')
    context.effects['quote_adjustment_origin']={'quote':quote_before,'line':line_before,
        'head':snapshot(head),'mapping':list(fields),'mode':'explicit_quote_to_price_adjustment',
        'notes':['调价按OldPrice+所选头AdjustMoney，不擅自改为AdjustRatio百分比。',
            '目标精度按原字段舍入，报价原精度保留在快照；未知FlowMain/CustSelfProdCode/FabricKindID不推断。',
            '保存仍执行已有原色号回写；同数值色号的全部报价可能被回写。审核/反审核沿用QuoteDetailNo原规则。',
            '重复转单各自留档；旧选择按钮及生成时机未证明。']}
    persist(context,actor);services.finish([head,created],actor)
    record(created,'quote_to_price_adjustment',{'exists':False},actor,
        '报价头ID='+str(quote.pk)+'；明细ID='+str(line.pk)+'；目标调价头ID='+str(head.pk))
    return created


@transaction.atomic
def reverse_quote_adjustment(item, actor, at, reason, query):
    """转调价撤回沿用原删除回写：恢复上一条调价，原明细与来源继续留档。"""
    from . import source_services as services, source_sales_services as sales
    from .source_context import SourceDocumentContext
    from .source_continuation import save_effect
    from .source_package_operations import check_scope
    item=locked(item)
    context=SourceDocumentContext.objects.filter(entity=item._meta.label,object_id=item.pk).first()
    if item.SOURCE_TABLE!='PriceAdjustDetail' or context is None or 'quote_adjustment_origin' not in context.effects:
        raise ValidationError({'source':'此记录不是明确报价转调价生成的明细，请使用对应原单据操作。'})
    chain=services.lock_chain(item);services.editable(chain)
    affected=list(sales.same_numeric_color(sales.rows('QuoteDetail'),raw(item,'ColorNum')).order_by('pk'))
    candidates=list(sales.same_numeric_color(sales.rows('PriceAdjustDetail'),raw(item,'ColorNum')).order_by('pk'))
    check_scope([*chain,*affected,*candidates],query)
    for row in affected:locked(row)
    before=snapshot(item)
    save_effect(item,'transfer_retained',{'active':True,'operation':'reverse_quote_adjustment',
        'at':at,'reason':reason,'before':before,
        'quote_ids':[row.pk for row in affected],
        'rule':'原删除回写上一条有效调价；DateType/StartDate保持原删除行为，不恢复创建前快照'},actor,reason)
    sales.removed(item,actor)
    record(item,'reverse_quote_adjustment',before,actor,reason)
    return item


LINE_TRANSFER_ORIGINS={'ArrivalNoticeDetail':'field_copy_origin','PurDetail':'department_purchase_origin',
    'ArticleOutDetail':'care_plan_article_origin'}


@transaction.atomic
def reverse_line_transfer(item,actor,at,reason,query):
    """明确转入明细的撤回：来源与原行留存，父单汇总和现行库存重新计算。"""
    from . import source_services as services
    from .source_context import SourceDocumentContext
    from .source_continuation import save_effect
    from .source_package_operations import check_scope
    from .source_phase6_guards import before as entry_before
    from .source_provenance import is_historical
    item=locked(item)
    context=SourceDocumentContext.objects.filter(entity=item._meta.label,object_id=item.pk).first()
    if item.SOURCE_TABLE not in LINE_TRANSFER_ORIGINS or context is None or LINE_TRANSFER_ORIGINS[item.SOURCE_TABLE] not in context.effects:
        raise ValidationError({'source':'此明细不是采购转到货、部门申请转采购或保养计划领料生成的记录。'})
    if is_historical(item):raise ValidationError({'source':'历史来源原行不能作为本次新转单撤回。'})
    chain=services.lock_chain(item);services.editable(chain);check_scope(chain,query)
    for parent in chain:services.purchase.require_change(parent,'撤回转单')
    entry_before(item,'BeforeDeleteSQL',actor)
    before=snapshot(item)
    save_effect(item,'transfer_retained',{'active':True,'operation':'reverse_line_transfer',
        'at':at,'reason':reason,'before':before,'origin_key':LINE_TRANSFER_ORIGINS[item.SOURCE_TABLE]},actor,reason)
    services.finish(chain[:-1],actor)
    record(item,'reverse_line_transfer',before,actor,reason)
    return item


HEAD_TRANSFER_ORIGINS={'OrderMain':'quote_transfer_origin','ProdIn':'purchase_product_origin'}


@transaction.atomic
def reverse_head_transfer(item,actor,at,reason,query):
    """整单撤回采用原删除业务规则；保存头、明细和本次库存来源快照。"""
    from . import source_services as services
    from .source_context import SourceDocumentContext
    from .source_continuation import save_effect
    from .source_package_operations import check_scope
    from .source_phase6_guards import before as entry_before
    from .source_phase5_triggers import removing,removed
    from .source_business_updates import matching
    from .source_phase3_operations import source
    from .source_provenance import is_historical
    from .source_execution_state import active
    item=locked(item)
    context=SourceDocumentContext.objects.filter(entity=item._meta.label,object_id=item.pk).first()
    if item.SOURCE_TABLE not in HEAD_TRANSFER_ORIGINS or context is None or HEAD_TRANSFER_ORIGINS[item.SOURCE_TABLE] not in context.effects:
        raise ValidationError({'source':'此单不是明确报价转订单或采购转成品入库生成的单据。'})
    def descendants(parent):
        for child in services.child_rows(parent):
            if active(type(child).objects.filter(pk=child.pk)).exists():
                yield locked(child)
                yield from descendants(child)
    selected=[item,*descendants(item)]
    affected=[]
    if item.SOURCE_TABLE=='ProdIn':
        jobs=list(matching(source('JobSheet'),SheetNo=raw(item,'JobSheetNo')).order_by('pk'))
        affected.extend(jobs)
        for job in jobs:affected.extend(matching(source('JobProcess'),SheetSeries=raw(job,'SheetSeries'),ProcessID='GX99'))
    check_scope([*selected,*affected],query)
    for row in affected:locked(row)
    for row in selected:
        if is_historical(row):raise ValidationError({'source':'转入单据含历史来源原行，不能作为新办理整单撤回；原行保留。'})
        services.editable(services.lock_chain(row))
        services.purchase.require_change(row,'撤回转单')
        services.sales.removing(row);removing(row,actor)
        entry_before(row,'BeforeDeleteSQL',actor)
    stocks=[]
    from django.apps import apps
    for label,ids in context.effects.get('stock_rows',{}).items():
        stocks.extend({'entity':label,'source':snapshot(row)} for row in apps.get_model(label).objects.filter(pk__in=ids).order_by('pk'))
    services.stock.clear_effects(context,actor)
    for row in reversed(selected):
        before=snapshot(row)
        save_effect(row,'transfer_retained',{'active':True,'operation':'reverse_head_transfer',
            'at':at,'reason':reason,'before':before,'head_id':item.pk,'head_entity':item._meta.label,
            'stock_before':stocks if row.pk==item.pk and type(row) is type(item) else []},actor,reason)
        record(row,'reverse_head_transfer',before,actor,reason)
    for row in selected:removed(row,actor)
    services.workflow.refresh_removed(item,actor)
    return item
