"""销售/打样的原保存触发；重复检查留事实，原行不去重。"""
from django.core.exceptions import ValidationError
from .business import persist, record, snapshot
from .source_provenance import is_historical
from .source_quality_reports import rows
from .source_stock_services import raw
from .source_business_updates import matching, update_rows
from .source_execution_state import active
from .source_master_data import retain

HEADER_FIELDS='SheetSeries SheetNo SheetDate SheetKind SheetStatus SheetType RightStatus PrintTimes Modifyer ModifyDate CreateDate Creater Revisions BusinessUnitID StepNo ApproveDate Approver'.split()
COLOR_FIELDS='SheetSeries CheckNo ProdID LotNo FabricKindID ColorKind LOT ColorMatch ColorNum NeedleCountUp NeedleCountDn ColorID Twist Tenters WeightDn Plaiting WeightUp Edge CodeFront ProviderCode DlvAddress DlvDate PlanDate RequireWeight RequireKG MachinePin MachineDozen FabricID OutQty OutYard DryFub WetFub WashFastness SolarFastness ShrinV ShrinL CutYard Remarks01 Remarks02 Remarks03 Remarks04'.split()


def source(table,module):
    return active(rows(table,module))


def change(query,values,actor):
    update_rows(query,values,actor,'phase2_trigger','采用原销售/打样触发字段')


def color_registered(item,actor):
    color=raw(item,'ColorNum')
    targets=matching(source('PColorNum','erp_base'),SheetSeries=raw(item,'SheetSeries'),ColorNo=raw(item,'ColorNo'))
    # 原UPDATE JOIN未指定多来源优先级；按新库原行顺序逐次采用，全部候选留在来源模型。
    for sample in matching(source('DyeDipsRecord','erp_sampling'),ColorNum=color).order_by('pk'):
        change(matching(source('DyeLabColor','erp_sampling'),SheetSeries=raw(item,'SheetSeries'),ColorNo=raw(item,'ColorNo')),
               {'ColorDepthID':raw(sample,'ColorDepthID')},actor)
        notes=list(matching(source('DyeDipsRecordNote','erp_sampling'),SheetSeries=raw(sample,'SheetSeries')).order_by('pk'))
        for note in notes or [None]:
            change(targets,{'Note':None if note is None else raw(note,'Note'),'EmpID':raw(sample,'EmpID'),
                'EndTime':raw(sample,'SheetDate'),'IsToSampleDaTe':raw(sample,'SheetDate'),'IsToDoSample':True,
                **{f:raw(sample,f) for f in ['ColorDepthID','StuffDosage','DyePhaseName']}},actor)
    for recipe in matching(source('DyeRecipe','erp_sampling'),ColorNum=color).filter(old_sheet_kind=1).order_by('pk'):
        change(matching(source('PColorNum','erp_base'),ColorNum=color),
               {'ColorNumNO':raw(recipe,'ColorVersion'),'OKTime':raw(recipe,'SheetDate')},actor)


def order_info(item,created,actor):
    for table,fields in [('OrderMain',HEADER_FIELDS),('OrderColor',COLOR_FIELDS)]:
        query=source(table,'erp_sales')
        values={f:raw(item,f) for f in fields}
        if created:
            from .source_services import write
            write(query.model,{query.model.SOURCE_FIELDS[f]:v for f,v in values.items()},actor=actor)
        else:
            targets=matching(query,SheetSeries=raw(item,'SheetSeries'))
            if table=='OrderColor':targets=matching(targets,CheckNo=raw(item,'CheckNo'))
            change(targets,{f:v for f,v in values.items() if f not in ['SheetSeries','CheckNo']},actor)


def saved(item,data,created,actor):
    if is_historical(item):return
    table=item.SOURCE_TABLE
    if table=='p_Product':
        if matching(source('PProduct','erp_base'),NameC=raw(item,'NameC')).count()>1:
            record(item,'original_product_duplicate',snapshot(item),actor,'p_ProductUpdate：成品重名检查命中，原行照存')
        if (created or 'old_prod_id' in data) and matching(source('OrderColor','erp_sales'),CustFabricName=raw(item,'ProdID')).exists():
            raise ValidationError({'old_prod_id':'原p_ProductUpdate：此成品编号已被订单客户品名引用，不能修改。'})
    elif table=='CustomerNoLimit':
        if matching(source('CustomerNoLimit','erp_sales'),CustomerID=raw(item,'CustomerID')).count()>1:
            record(item,'original_customer_limit_duplicate',snapshot(item),actor,'CustomerNoLimitInsert：同客户重复权限原行照存')
    elif table=='P_ColorNum' and created:
        color_registered(item,actor)
    elif table=='OrderInfo':
        order_info(item,created,actor)
    elif table=='DyeRecipe' and created:
        from django.db.models import Exists,OuterRef
        from django.db.models.functions import Upper,RTrim
        heads=source('DyeRecipe','erp_sampling').alias(normal_series=Upper(RTrim('old_sheet_series'))).filter(normal_series=OuterRef('normal_series'))
        for child in ['DyeRecipePhase','DyeRecipeDetail']:
            orphans=source(child,'erp_sampling').alias(normal_series=Upper(RTrim('old_sheet_series'))).alias(has_head=Exists(heads)).filter(has_head=False)
            for orphan in orphans.order_by('pk'):
                retain(orphan,actor,'DyeRecipeInsert原全库孤立行清理；保留原阶段及用料供查阅')


def removing(item,actor):
    if item.SOURCE_TABLE=='OrderInfo':
        for table in ['OrderMain','OrderColor']:
            for target in matching(source(table,'erp_sales'),SheetSeries=raw(item,'SheetSeries')):
                retain(target,actor,'tgr_OrderInfo删除联动；原关联行留档')
