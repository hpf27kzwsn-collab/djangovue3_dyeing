"""本轮补齐的原界面保存联动；由整单保存结束时统一调用。"""
from .source_entry_services import entry_for
from .source_provenance import is_historical
from .source_phase3_operations import source,change
from .source_business_updates import matching
from .source_stock_services import raw
from .business import locked,record,snapshot


def xml_text(value):
    return value.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')


def joined_names(item,entry,actor):
    if entry=='p_Production':
        targets=matching(source('p_FieldValid'),FieldType='Production',Code=raw(item,'Code'))
        for target in targets:
            names=[]
            lines=list(matching(source('p_FieldValidSub'),FieldType='Production',Code=raw(target,'Code')).order_by('old_sort_value','pk'))
            for line in lines:
                for process in matching(source('p_Process'),ProcessID=raw(line,'SubCode')).order_by('pk'):
                    value=raw(process,'Name')
                    if value is not None:names.append(xml_text(value))
            if names:
                change(type(target).objects.filter(pk=target.pk),{'Name':'→'.join(names)},actor)
            else:
                # 表头先保存、明细后录入；原空集STUFF为NULL，与原Name NOT NULL冲突。
                # 未匹配工序的原明细仍保留；不补空串、不删行，明确记录尚不能重建名称。
                record(target,'entry_route_name_pending',snapshot(target),actor,
                    '工艺路线尚无可连接的工序名称，保留当前名称；原明细ID：'+str([line.pk for line in lines]))
    else:
        for job in matching(source('JobSheet'),SheetSeries=raw(item,'SheetSeries')):
            names=[]
            for line in matching(source('JobAtte'),SheetSeries=raw(job,'SheetSeries')).exclude(old_atte_value='纸筒').order_by('old_atte_code','pk'):
                for valid in matching(source('p_FieldValidSub'),FieldType='AtteKind',Name=raw(line,'AtteValue')).filter(old_num_value3=1):
                    names.append(xml_text(raw(line,'AtteValue')))
            change(type(job).objects.filter(pk=job.pk),{'Jobattes1':','.join(names) if names else None},actor)

POSITION_ENTRIES={**{e:'98' for e in ['GrayIn','GrayInWork','JiaNianGrayIn','KeTuiGrayIn','PurGrayIn']},
    **{e:'99' for e in ['CusReturnSemiIn','GrayOutToSemiIn','MaterialSemiIn','PurSemiIn','SemiIn','SemiInBack']}}
OUT_ENTRIES={'GrayOut','GrayOutJob','GrayOutSale','GrayOutTurn','GrayOutWork','TSGrayOut',
    'SemiOut','SemiOutJob','SemiOutSale','SemiOutTurn','SemiOutWork'}


def rebuild_sensitive_dye(item,actor):
    from .source_phase3_operations import query,create,retire
    series=raw(item,'SheetSeries')
    rows=query("""SELECT SheetSeries,JobSheetNo,FabricKindID,PhaseID,PhaseNo,
        CAST(Dosage AS DECIMAL(10,6)) AS Dosage,CAST(MDosage AS DECIMAL(10,6)) AS MDosage,N'敏感色' AS ColorLevel
      FROM (SELECT c.SheetSeries,c.JobSheetNo,e.FabricKindID,b.PhaseID,b.PhaseNo,
        SUM(CASE WHEN ISNULL(a.StuffType,'')='S' THEN ISNULL(a.Dosage,0) ELSE 0 END) AS Dosage,
        SUM(CASE WHEN ISNULL(d.Kind,'')=2 AND ISNULL(a.StuffType,'')='S' THEN a.Dosage ELSE 0 END) AS MDosage
        FROM dye.StuffWeightDetail a JOIN dye.StuffWeightPhase b ON a.SheetSeries=b.SheetSeries AND a.PhaseNo=b.PhaseNo
        JOIN dye.StuffWeight c ON b.SheetSeries=c.SheetSeries JOIN dye.p_Stuff d ON a.StuffID=d.StuffID
        LEFT JOIN dye.p_Gray e ON c.ProdID=e.GrayID
        WHERE ISNULL(c.SheetKind,0)=2 AND ISNULL(c.RecipeType,0) IN (0,2) AND a.SheetSeries=@SheetSeries
          AND EXISTS(SELECT 1 FROM dye.p_DyeCurve f WHERE f.PhaseID=b.PhaseID)
        GROUP BY c.SheetSeries,c.JobSheetNo,e.FabricKindID,b.PhaseID,b.PhaseNo) a
      WHERE CAST(MDosage AS DECIMAL(10,6))>0""",{'SheetSeries':series})
    old=retire(matching(source('DyeProduceItem'),SheetSeries=series),actor,'返修料单原AfterSaveSQL重建敏感色明细；旧行保留')
    fields={name.lower():name for name in source('DyeProduceItem').model.SOURCE_FIELDS}
    created=[create('DyeProduceItem',{fields[k]:v for k,v in row.items()},actor) for row in rows]
    record(item,'entry_sensitive_dye_rebuild',snapshot(item),actor,
        '原敏感色投影重建；保留原行：'+str([v['id'] for v in old])+'；新增：'+str([v.pk for v in created]))


def salary_team_detail(item,actor):
    from .source_phase3_operations import query,create
    from datetime import timedelta
    series=raw(item,'SheetSeries')
    if matching(source('SalaryChangesDetail'),SheetSeries=series).exists():return
    heads=list(matching(source('SalaryChanges'),SheetSeries=series).order_by('pk'))
    head=heads[-1];day=raw(head,'RQ')
    values=query("""SELECT @SheetSeries AS SheetSeries,
        @SheetSeries+'-'+CAST(ROW_NUMBER() OVER(ORDER BY a.EmpID) AS VARCHAR(10)) AS DetailNo,
        a.EmpID,CAST(CAST(@OtherAmount AS DECIMAL(10,2))/SUM(a.Num) OVER(ORDER BY a.ShiftID) AS DECIMAL(8,2)) AS OtherAmount
        FROM (SELECT DISTINCT a.ShiftID,a.EmpID,1 AS Num FROM dye.JobShiftEmp a
          LEFT JOIN dye.WProcess b ON a.WProcessNo=b.WProcessNo
          WHERE a.ShiftID=@ShiftID AND b.CreateDate>@FromTime AND b.CreateDate<@ToTime
          UNION ALL SELECT DISTINCT b.ShiftID,a.EmpID,1 AS Num FROM dye.RecordEmp a
          LEFT JOIN dye.RecordYield b ON b.BarCode=a.BarCode
          WHERE b.ShiftID=@ShiftID AND b.PackTime>@FromTime AND b.PackTime<@ToTime) a""",
        {'SheetSeries':series,'OtherAmount':raw(head,'OtherAmount'),'ShiftID':raw(head,'ShiftID'),
         'FromTime':None if day is None else day+timedelta(hours=7.5),'ToTime':None if day is None else day+timedelta(hours=31.5)})
    fields={name.lower():name for name in source('SalaryChangesDetail').model.SOURCE_FIELDS}
    created=[create('SalaryChangesDetail',{fields[k]:v for k,v in row.items()},actor) for row in values]
    record(item,'entry_salary_team_detail',snapshot(item),actor,
        '原班组调整两来源各自DISTINCT再UNION ALL；不合并跨来源相同员工：'+str([v.pk for v in created]))


def before_delete(item,actor):
    if is_historical(item):return
    from .source_phase3_operations import retire
    entry=entry_for(item)
    if entry=='PrintingTestList':
        for table in ['PrintingTestStuff','PrintingTestColor','PrintingTestDetail']:
            retire(matching(source(table),SheetSeries=raw(item,'SheetSeries')),actor,'原印花试验删除前明细清理；旧行留档')
    elif entry in ['qry_WorkQty','qry_WorkQtyAll']:
        numbers=matching(source('WProcess'),WProcessNo=raw(item,'WProcessNo')).values_list('old_wprocess_no',flat=True)
        for number in numbers:change(matching(source('JobProcess'),WProcessNo=number),{'VehicleNo':'','WPWorker':''},actor)
    elif entry=='TSGrayOut':
        for line in matching(source('GrayOutDetail'),SheetSeries=raw(item,'SheetSeries')).order_by('pk'):
            number=raw(line,'JobSheetNo')
            if matching(source('ProdIn'),JobSheetNo=number).exists() or matching(source('JobSheet'),OriSourceJobNo=number).exists():continue
            for original in matching(source('JobGrayRecord'),AssignedNo=raw(line,'AssignedNo')):
                change(matching(source('GrayInRecord'),ReceSheetNo=raw(line,'ReceSheetNo'),BarCode=raw(original,'BarCode')),{'AssignedNo':None},actor)


def aborted(item,actor):
    if entry_for(item)=='ReworkStuffWeight':
        from .source_phase3_operations import retire
        retire(matching(source('DyeProduceItem'),SheetSeries=raw(item,'SheetSeries')),actor,'返修料单原中止后清理；敏感色原行留档')


def saved(item,actor):
    if is_historical(item):return
    entry=entry_for(item)
    if entry=='SalaryChangesD':
        salary_team_detail(item,actor)
    elif entry=='ReworkStuffWeight':
        rebuild_sensitive_dye(item,actor)
    elif entry in ['p_Production','JobSheetQuery']:
        joined_names(item,entry,actor)
    elif entry=='ProdOutEdit':
        candidates={}
        for head in matching(source('ProdOut'),SheetSeries=raw(item,'SheetSeries')).order_by('pk'):
            for line in matching(source('ProdOutDetail'),SheetSeries=raw(head,'SheetSeries')).order_by('pk'):
                for target in matching(source('FARDetail'),OutDetailNo=raw(line,'DetailNo'),JobSheetNo=raw(line,'JobSheetNo')):
                    candidates.setdefault(target.pk,[]).append(head)
        for key,heads in candidates.items():
            target=source('FARDetail').get(pk=key)
            change(type(target).objects.filter(pk=key),{'OutDate':raw(heads[-1],'SheetDate')},actor)
            if len(heads)>1:record(target,'entry_out_date_candidates',snapshot(target),actor,'出库日期原多来源按承接顺序末项回写，候选：'+str([h.pk for h in heads]))
    elif entry in ['AfterNormalStuffWeight','NormalStuffWeight']:
        for head in matching(source('StuffWeight'),SheetSeries=raw(item,'SheetSeries')):
            change(matching(source('JobSheet'),SheetNo=raw(head,'JobSheetNo')),{'CurrProcessID':'已开料单'},actor)
    elif entry in ['FeelOfferMain','FixedPrice']:
        table='FeelOfferMain' if entry=='FeelOfferMain' else 'Quote'
        for row in matching(source(table),SheetSeries=raw(item,'SheetSeries')):
            changed=raw(row,'ModifyDate');change(type(row).objects.filter(pk=row.pk),{'LastTime':changed if changed is not None else raw(row,'SheetDate')},actor)
    elif entry in POSITION_ENTRIES:
        from .source_phase3_misc import positions
        positions(POSITION_ENTRIES[entry],raw(item,'SheetSeries'),actor)
    elif entry=='DyeReprint':
        from .source_phase2_operations import reprint
        reprint(item,actor,retain_zero=True)
    elif entry=='FabricArticleIn':
        from .source_phase2_operations import material_adjustment
        heads=list(matching(source('ArticleIn'),SheetSeries=raw(item,'SheetSeries')).order_by('pk'))
        if heads and raw(heads[0],'SheetKind')==13:
            material_adjustment(item,actor)
    elif entry=='s_Roles':
        from .source_foundation_platform import allocate_print_rights,field_rights
        allocate_print_rights(raw(item,'RoleNo'),actor);field_rights(raw(item,'RoleNo'),actor)
    elif entry in ['ODMIn','ODMOut']:
        for head in matching(source(entry),SheetSeries=raw(item,'SheetSeries')):
            for line in matching(source(entry+'Detail'),SheetSeries=raw(head,'SheetSeries')):
                change(matching(source('JobSheet'),SheetNo=raw(line,'JobSheetNo')),{'CurrProcessID':'发外加工'},actor)
    elif entry in OUT_ENTRIES:
        table=item.SOURCE_TABLE
        numbers=[]
        for head in matching(source(table),SheetSeries=raw(item,'SheetSeries')).filter(old_sheet_kind=21):
            numbers.extend(raw(line,'JobSheetNo') for line in matching(source(table+'Detail'),SheetSeries=raw(head,'SheetSeries')))
        # 原UPDATE的取单位子查询未限制当前流水；记录全部候选，按承接顺序末项取值。
        for number in dict.fromkeys(numbers):
            candidates=[]
            for line in matching(source(table+'Detail'),JobSheetNo=number).order_by('pk'):
                candidates.extend(matching(source(table),SheetSeries=raw(line,'SheetSeries')).order_by('pk'))
            if candidates:
                for job in matching(source('JobSheet'),SheetNo=number):
                    change(type(job).objects.filter(pk=job.pk),{'CurrProcessID':'胚纱出库' if table=='GrayOut' else '发纱出库','StockUnit':raw(candidates[-1],'StockUnit')},actor)
                    if len(candidates)>1:record(job,'entry_out_unit_candidates',snapshot(job),actor,'原界面多单位候选：'+str([{'id':r.pk,'StockUnit':raw(r,'StockUnit')} for r in candidates]))
    elif entry=='SemiToGrayIn':
        for head in matching(source('GrayIn'),SheetSeries=raw(item,'SheetSeries')).filter(old_sheet_kind=11):
            for line in matching(source('GrayInDetail'),SheetSeries=raw(head,'SheetSeries')):
                if raw(line,'CustJobNo') is None or raw(line,'CustJobNo').rstrip(' ')== '':
                    change(type(line).objects.filter(pk=line.pk),{'CustJobNo':raw(head,'FactDlvNo')},actor)
    elif entry=='SmallStuffIn':
        for head in matching(source('StuffIn'),SheetSeries=raw(item,'SheetSeries')).filter(old_sheet_kind__in=[11,13]):
            # SQL UPDATE多来源只更新目标一次；不把重复收货误作多次LastPrice滚动。
            by_stuff={}
            for line in matching(source('StuffInDetail'),SheetSeries=raw(head,'SheetSeries')).filter(old_price__gt=0).order_by('pk'):
                for material in matching(source('p_Stuff'),StuffID=raw(line,'StuffID')):by_stuff.setdefault(material.pk,[]).append(line)
            for key,lines in by_stuff.items():
                material=locked(source('p_Stuff').get(pk=key));old=raw(material,'Price')
                change(type(material).objects.filter(pk=key),{'LastPrice':old,'Price':raw(lines[-1],'Price')},actor)
                if len(lines)>1:record(material,'entry_price_candidates',snapshot(material),actor,'原无序UPDATE采用末项，完整收货候选：'+str([r.pk for r in lines]))
    elif entry=='CookIn':
        candidates={}
        for head in matching(source('ArticleIn'),SheetSeries=raw(item,'SheetSeries')).filter(old_sheet_kind=13):
            for line in matching(source('ArticleInDetail'),SheetSeries=raw(head,'SheetSeries')).order_by('pk'):
                for material in matching(source('p_Article'),ArticleID=raw(line,'ArticleID')):
                    candidates.setdefault(material.pk,[]).append((head,line))
        for key,sources in candidates.items():
            lines=[line for head,line in sources]
            material=locked(source('p_Article').get(pk=key));values={'LastPrice':raw(lines[-1],'TaxPrice')}
            if raw(material,'Price') in [None,0]:values['Price']=raw(lines[-1],'TaxPrice')
            before=snapshot(material)
            change(type(material).objects.filter(pk=key),values,actor)
            if len(sources)>1:
                import json
                material.refresh_from_db()
                record(material,'entry_cook_price_candidates',before,actor,json.dumps({
                    'entry':'CookIn','source_entry_id':item.pk,'source_sheet_series':raw(item,'SheetSeries'),
                    'rule':'原UPDATE未排序；采用承接顺序末项，全部连接候选留档，不以CookInDetail代替ArticleInDetail',
                    'candidates':[{'article_in_id':head.pk,'detail_id':line.pk,'TaxPrice':raw(line,'TaxPrice')} for head,line in sources],
                    'chosen_detail_id':lines[-1].pk,'updated_values':values},ensure_ascii=False,default=str))
    else:
        return
    item.refresh_from_db()


def approved(item,actor,enabled):
    entry=entry_for(item)
    if entry=='SemiOutTurn':
        from .source_phase3_operations import transfer
        if enabled:transfer('372',raw(item,'SheetSeries'),actor)
        else:undo_stock_transfer(item,actor,'SemiOut','GrayIn',30,'SemiOutSheetNo','GrayStockBook')
    elif entry=='QCJobList':
        # 原配置引用本备份不存在的trade架构；本入口实际查询dye.JobSheet。
        # 按同名DetailNo关联本库原表实现，差异单独登记，不更换为工卡号或条码。
        for job in matching(source('JobSheet'),DetailNo=raw(item,'DetailNo')):
            change(matching(source('RecordYield'),DetailNo=raw(job,'DetailNo')),{'RightStatus':10 if enabled else 0},actor)
    elif entry in ['GrayOut','GrayOutJob','GrayOutSale','GrayOutWork','GrayOutTurn','GrayOutShenHe']:
        if entry=='GrayOutShenHe':
            from .source_phase3_posting import post
            post('GrayOut',raw(item,'SheetSeries'),actor)
        for line in matching(source('GrayOutDetail'),SheetSeries=raw(item,'SheetSeries')):
            for job in matching(source('JobSheet'),SheetNo=raw(line,'JobSheetNo')):
                change(matching(source('JobAssign'),SheetSeries=raw(job,'SheetSeries'),ReceSheetNo=raw(line,'ReceSheetNo')),{'Status':1 if enabled else 0},actor)
        if entry=='GrayOutTurn':
            from .source_phase3_operations import transfer
            if enabled:transfer('299',raw(item,'SheetSeries'),actor)
            else:undo_stock_transfer(item,actor,'GrayOut','SemiIn',26,'GrayOutSheetNo','SemiStockBook')
    elif entry=='QueryWorkList2':
        from django.core.exceptions import ValidationError
        raise ValidationError({'original_table':'QueryWorkList2原审核/反审核需要RecordYieldCheck；最新旧库没有该表定义，不能把RecordYield包装表当作该核对表。此动作尚未复刻，本次审核事务不提交，工卡及原数据保留。'})


def undo_stock_transfer(item,actor,origin,target,kind,link,book):
    """两个原转仓Delete过程的关联范围；删除变为留档，不丢弃重复入库。"""
    from .source_phase3_operations import retire
    series=raw(item,'SheetSeries')
    if not matching(source(origin),SheetSeries=series).filter(old_sheet_kind=kind).exists():return
    heads=matching(source(target),**{link:series})
    numbers=list(heads.values_list(heads.model.SOURCE_FIELDS['SheetSeries'],flat=True))
    for table in [target+'Detail',book]:
        retire(source(table).filter(**{source(table).model.SOURCE_FIELDS['SheetSeries']+'__in':numbers}),actor,
            '原Sp_'+origin+'Turn_Delete撤销转仓入库；全部匹配原行留档')
    retire(heads,actor,'原Sp_'+origin+'Turn_Delete撤销转仓入库表头；重复表头留档')
