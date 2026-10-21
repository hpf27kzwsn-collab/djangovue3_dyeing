"""成品交付及删除联动；所有计算在服务层，历史承接不重算原值。"""
from .source_phase3_operations import source,change,retire
from .source_business_updates import matching
from .source_stock_services import raw
from .source_provenance import is_historical
from .business import record,snapshot
from .source_trial_steps import equal

DELETE_TABLES=['GetJobSheetReceive','GrayInRecord','GrayOut','GrayOutDetail','JobProcess',
 'p_Customer','p_Dept','p_Gray','p_Product','ProcessSchedule','ProdIn','StuffWeight',
 'ColoringCheck','DefectiveInDetail','DyeLabColor','DyeRecipe','RecordYield']


def saved(item,data,created,actor):
    if is_historical(item):return
    if item.SOURCE_TABLE=='ProdOutDetail':
        gray=raw(item,'GrayQty')
        if gray is not None and gray>0:
            weight=raw(item,'WeightQty');rolls=raw(item,'Rolls') or 0
            tube=float(raw(item,'Jobattes6') or 0);added=float(raw(item,'Jobattes8') or 0)
            value=None if weight is None else (float(weight)-float(gray)-float(rolls)*(tube+added))/float(gray)*100
            change(matching(source('ProdOutDetail'),JobSheetNo=raw(item,'JobSheetNo') or '',DetailNo=raw(item,'DetailNo')),{'GRealLoss':value},actor)
    elif item.SOURCE_TABLE=='ProdOutRecord' and raw(item,'SheetSeries') is not None:
        # 原UPDATE覆盖同流水全部细码，只对固定两个客户按工卡+匹号取包装码长。
        for row in matching(source('ProdOutRecord'),SheetSeries=raw(item,'SheetSeries')).order_by('pk'):
            candidates=[]
            for line in matching(source('ProdOutDetail'),SheetSeries=raw(row,'SheetSeries'),DetailNo=raw(row,'DetailNo')):
                values=matching(source('RecordYield'),JobSheetNo=raw(line,'JobSheetNo'),RollNo=raw(row,'RollNo'))
                candidates.extend((matching(values,CustomerID='064')|matching(values,CustomerID='067')).order_by('pk'))
            if candidates:
                change(source('ProdOutRecord').filter(pk=row.pk),{'Yard':raw(candidates[-1],'Yard')},actor)
                if len(candidates)>1:record(row,'phase5_ambiguous_yard',snapshot(row),actor,'原码长多行连接无排序；取承接顺序末行，完整候选：'+str([{'id':v.pk,'Yard':raw(v,'Yard')} for v in candidates]))
    item.refresh_from_db(fields=list(item.SOURCE_FIELDS.values()))


def removal_issues(item):
    table=item.SOURCE_TABLE;checks=[]
    if table=='GrayInRecord':checks=[('JobGrayRecord',{'ReceSheetNo':raw(item,'ReceSheetNo'),'GrayBarCode':raw(item,'BarCode')})]
    elif table=='JobProcess':
        jobs=list(matching(source('JobSheet'),SheetSeries=raw(item,'SheetSeries')).order_by('pk'))
        if jobs:checks=[('WProcess',{'JobSheetNo':raw(jobs[-1],'SheetNo'),'ProcessID':raw(item,'ProcessID')})]
    elif table=='p_Customer':checks=[('OrderMain',{'CustomerID':raw(item,'CustomerID')}),('StuffIn',{'SupplierID':raw(item,'CustomerID')}),('ArticleIn',{'SupplierID':raw(item,'CustomerID')})]
    elif table=='p_Gray':checks=[('GrayInDetail',{'GrayID':raw(item,'GrayID')}),('OrderColor',{'ProdID':raw(item,'GrayID')}),('SemiInDetail',{'ProdID':raw(item,'GrayID')})]
    elif table=='p_Product':checks=[('P_ColorNum',{'ProdID':raw(item,'ProdID')}),('OrderColor',{'CustFabricName':raw(item,'ProdID')}),('QuoteDetail',{'ProdID':raw(item,'ProdID')})]
    elif table=='DyeLabColor':checks=[('DyeDipsRecord',{'ColorNum':raw(item,'ColorNum')}),('DyeDipsRecord',{'ColorNo':raw(item,'ColorNo')})]
    return [{'table':t,'ids':list(q.values_list('pk',flat=True))} for t,p in checks if (q:=matching(source(t),**p)).exists()]


def removing(item,actor):
    from django.core.exceptions import ValidationError
    issues=removal_issues(item)
    if issues:raise ValidationError({'source':'原删除条件存在业务引用，请从原行留档逆向入口办理并保留引用：'+str(issues)})


def removed(item,actor):
    table=item.SOURCE_TABLE
    if table=='GetJobSheetReceive':
        from .source_quality_flow import refresh_current_process
        change(matching(source('JobSheet'),SheetNo=raw(item,'JobSheetNo')),{'CurrProcessID':''},actor)
        for job in matching(source('JobSheet'),SheetNo=raw(item,'JobSheetNo')):refresh_current_process(job,actor)
    elif table=='GrayOutDetail':
        jobs=list(matching(source('JobSheet'),SheetNo=raw(item,'JobSheetNo')).exclude(old_job_sheet_type=0).exclude(old_job_sheet_type__isnull=True).order_by('pk'))
        if jobs:
            series=raw(jobs[-1],'SheetSeries')
            if series is not None and not equal(series,''):
                change(matching(source('JobAssign'),SheetSeries=series,ReceSheetNo=raw(item,'ReceSheetNo')),{'Status':0},actor)
                change(matching(source('JobGrayRecord'),SheetSeries=series,ReceSheetNo=raw(item,'ReceSheetNo')),{'AssignedNo':''},actor)
                change(matching(source('JobSheet'),SheetSeries=series),{'SumProcessRolls':0,'SumProcessLengthQty':0,'SumProcessWeightQty':0},actor)
    elif table=='p_Dept':retire(matching(source('DEPARTMENTS'),Code=raw(item,'DeptID')),actor,'p_Dept_delete原考勤部门退出活动范围，原行留档')
    elif table=='ProdIn':
        for job in matching(source('JobSheet'),SheetNo=raw(item,'JobSheetNo')):
            change(matching(source('JobProcess'),SheetSeries=raw(job,'SheetSeries'),ProcessID='GX99'),{'StartTime':None,'WPWorker':None},actor)
    elif table=='StuffWeight':
        retire(matching(source('StuffWeightJobSheetNo'),SheetSeries=raw(item,'SheetSeries')),actor,'StuffWeightDelete主副卡来源留档')
        retire(matching(source('StuffCombineSheets'),StuffSheetNo=raw(item,'SheetNo')),actor,'StuffWeightDelete领料合卡来源留档')
    elif table=='DefectiveInDetail':
        from .source_quality_flow import removed as quality_removed
        quality_removed(item,actor)
    elif table=='DyeRecipe':
        from .source_sampling_services import removed as sample_removed
        sample_removed(item,actor)
    # GrayOut_Delete原@JobSheetNo/@WProcessNo均未赋值，不能据字段名擅自删除报工。
    # ProcessSchedule_Delete/ProdOutInsert/ProdOut_UPDATE只有局部变量赋值。
