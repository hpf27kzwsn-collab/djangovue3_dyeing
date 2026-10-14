"""静态旧业务字段；由tools/legacy_models生成，逐表来源见source_catalog.json。"""
from django.db import models
from plugins.erp_base.source_documents import SourceRecord


class SourceDboBackDyeRecipePhase(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='BackDyeRecipePhase'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'PhaseNo': 'old_phase_no', 'PhaseID': 'old_phase_id', 'ProgramID': 'old_program_id', 'Remarks': 'old_remarks'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=True, blank=True, max_length=50)
    old_phase_no=models.CharField('PhaseNo', null=True, blank=True, max_length=50)
    old_phase_id=models.CharField('PhaseID', null=True, blank=True, max_length=50)
    old_program_id=models.CharField('ProgramID', null=True, blank=True, max_length=50)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_backdyerecipephase'
        indexes=[]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（BackDyeRecipePhase，待确认）'
        ordering=["-id"]

class SourceDyeAddDyeWProcessStep(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='AddDyeWProcessStep'
    SOURCE_FIELDS={'WPStepNo': 'old_wpstep_no', 'WProcessNo': 'old_wprocess_no', 'JobSheetNo': 'old_job_sheet_no', 'ProcessNo': 'old_process_no', 'ProcessID': 'old_process_id', 'DyeProcessID': 'old_dye_process_id', 'RealValue': 'old_real_value', 'RecordID': 'old_record_id', 'CurrTime': 'old_curr_time', 'Remarks': 'old_remarks', 'ProgramID': 'old_program_id', 'Rolls': 'old_rolls', 'WeightQty': 'old_weight_qty', 'MachineNo': 'old_machine_no', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id'}
    SOURCE_KEY=('WPStepNo',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_wpstep_no=models.CharField('WPStepNo', null=False, blank=True, max_length=20)
    old_wprocess_no=models.CharField('WProcessNo', null=True, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_process_no=models.IntegerField('ProcessNo', null=True, blank=True)
    old_process_id=models.CharField('工序', null=True, blank=True, max_length=10)
    old_dye_process_id=models.CharField('DyeProcessID', null=True, blank=True, max_length=50)
    old_real_value=models.DecimalField('比例', null=True, blank=True, max_digits=10, decimal_places=2)
    old_record_id=models.CharField('染色工', null=True, blank=True, max_length=38)
    old_curr_time=models.DateTimeField('日期', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=100)
    old_program_id=models.CharField('计件项目', null=True, blank=True, max_length=50)
    old_rolls=models.IntegerField('粒数', null=True, blank=True)
    old_weight_qty=models.FloatField('重量', null=True, blank=True)
    old_machine_no=models.CharField('机台', null=True, blank=True, max_length=10)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=100)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=100)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=100)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_adddyewprocessstep'
        indexes=[models.Index(fields=['source_batch', 'old_wpstep_no'],name='src_281a8b1075881f6b')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（AddDyeWProcessStep，待确认）'
        ordering=["-id"]

class SourceDyeColorCard(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ColorCard'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetKind': 'old_sheet_kind', 'SheetDate': 'old_sheet_date', 'BusinessUnitID': 'old_business_unit_id', 'CustomerID': 'old_customer_id', 'SalerGroupID': 'old_saler_group_id', 'SalerID': 'old_saler_id', 'Linker': 'old_linker', 'DeptID': 'old_dept_id', 'ColorNo': 'old_color_no', 'ProdID': 'old_prod_id', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'ColorID': 'old_color_id', 'ColorE': 'old_color_e', 'ColorNum': 'old_color_num', 'CustColorNum': 'old_cust_color_num', 'ColorDepthID': 'old_color_depth_id', 'ColorRGB': 'old_color_rgb', 'ColorVersion': 'old_color_version', 'ColorCards': 'old_color_cards', 'CheckNo': 'old_check_no', 'JobSheetNo': 'old_job_sheet_no', 'LimitDays': 'old_limit_days', 'Maker': 'old_maker', 'WareHouseID': 'old_ware_house_id', 'StorageUnitID': 'old_storage_unit_id', 'Place': 'old_place', 'MainStuffKindID': 'old_main_stuff_kind_id', 'RFID': 'old_rfid', 'SheetStatus': 'old_sheet_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=20)
    old_sheet_kind=models.IntegerField('SheetKind', null=True, blank=True)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('SalerGroupID', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('SalerID', null=True, blank=True, max_length=10)
    old_linker=models.CharField('Linker', null=True, blank=True, max_length=10)
    old_dept_id=models.CharField('DeptID', null=True, blank=True, max_length=10)
    old_color_no=models.CharField('ColorNo', null=True, blank=True, max_length=20)
    old_prod_id=models.CharField('ProdID', null=True, blank=True, max_length=20)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=128)
    old_lot_no=models.CharField('LotNo', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=20)
    old_color_e=models.CharField('ColorE', null=True, blank=True, max_length=20)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=20)
    old_cust_color_num=models.CharField('CustColorNum', null=True, blank=True, max_length=20)
    old_color_depth_id=models.CharField('ColorDepthID', null=True, blank=True, max_length=10)
    old_color_rgb=models.IntegerField('ColorRGB', null=True, blank=True)
    old_color_version=models.CharField('ColorVersion', null=True, blank=True, max_length=20)
    old_color_cards=models.IntegerField('ColorCards', null=True, blank=True)
    old_check_no=models.CharField('CheckNo', null=True, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)
    old_limit_days=models.IntegerField('LimitDays', null=True, blank=True)
    old_maker=models.CharField('Maker', null=True, blank=True, max_length=10)
    old_ware_house_id=models.CharField('WareHouseID', null=True, blank=True, max_length=10)
    old_storage_unit_id=models.CharField('StorageUnitID', null=True, blank=True, max_length=10)
    old_place=models.CharField('Place', null=True, blank=True, max_length=100)
    old_main_stuff_kind_id=models.CharField('MainStuffKindID', null=True, blank=True, max_length=10)
    old_rfid=models.CharField('RFID', null=True, blank=True, max_length=20)
    old_sheet_status=models.IntegerField('SheetStatus', null=True, blank=True)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_print_times=models.IntegerField('PrintTimes', null=True, blank=True)
    old_revisions=models.IntegerField('Revisions', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_colorcard'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_ae6bc79cae81a5f0')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（ColorCard，待确认）'
        ordering=["-id"]

class SourceDyeColorCardDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ColorCardDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'WorkSheetKind': 'old_work_sheet_kind', 'DataTableName': 'old_data_table_name', 'ProcessID': 'old_process_id', 'SheetDate': 'old_sheet_date', 'JobSheetNo': 'old_job_sheet_no', 'SheetNo': 'old_sheet_no', 'Photo': 'old_photo', 'Signer': 'old_signer', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('SheetSeries', 'WorkSheetKind', 'DataTableName', 'ProcessID')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_work_sheet_kind=models.IntegerField('WorkSheetKind', null=False, blank=False)
    old_data_table_name=models.CharField('DataTableName', null=False, blank=True, max_length=50)
    old_process_id=models.CharField('ProcessID', null=False, blank=True, max_length=10)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=20)
    old_photo=models.BinaryField('Photo', null=True, blank=True, editable=True)
    old_signer=models.CharField('Signer', null=True, blank=True, max_length=10)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=300)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_colorcarddetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_work_sheet_kind', 'old_data_table_name', 'old_process_id'],name='src_bdee20c1b756e9e4')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（ColorCardDetail，待确认）'
        ordering=["-id"]

class SourceDyeColorCardFlow(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ColorCardFlow'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SignedDate': 'old_signed_date', 'Flag': 'old_flag', 'Signer': 'old_signer'}
    SOURCE_KEY=('SheetSeries', 'SignedDate')
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_signed_date=models.DateTimeField('SignedDate', null=False, blank=False)
    old_flag=models.IntegerField('Flag', null=True, blank=True)
    old_signer=models.CharField('Signer', null=True, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_colorcardflow'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_signed_date'],name='src_6cbcbbe5a85f38b4')]
        verbose_name=verbose_name_plural='系统平台与配置相关表（ColorCardFlow，待确认）'
        ordering=["-id"]

class SourceDyeColorChangeRisk(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ColorChangeRisk'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'JobSheetNo': 'old_job_sheet_no', 'GrayID': 'old_gray_id', 'GrayName': 'old_gray_name', 'ProdID': 'old_prod_id', 'ProdName': 'old_prod_name', 'ColorNum': 'old_color_num', 'Color': 'old_color', 'CustColorNum': 'old_cust_color_num', 'ROLLS': 'old_rolls', 'Weight': 'old_weight', 'SheetDate': 'old_sheet_date', 'Remarks': 'old_remarks', 'CustomerID': 'old_customer_id', 'CustomerShortName': 'old_customer_short_name', 'CustomerName': 'old_customer_name', 'ChangeColorID': 'old_change_color_id', 'ChangeColor': 'old_change_color', 'ChangeCustColorNum': 'old_change_cust_color_num', 'CustomerOrderCode': 'old_customer_order_code'}
    SOURCE_KEY=('SheetSeries', 'JobSheetNo', 'ColorNum')
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=50)
    old_job_sheet_no=models.CharField('缸号', null=False, blank=True, max_length=50)
    old_gray_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_gray_name=models.CharField('GrayName', null=True, blank=True, max_length=150)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_prod_name=models.CharField('ProdName', null=True, blank=True, max_length=150)
    old_color_num=models.CharField('ColorNum', null=False, blank=True, max_length=50)
    old_color=models.CharField('Color', null=True, blank=True, max_length=50)
    old_cust_color_num=models.CharField('CustColorNum', null=True, blank=True, max_length=50)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_weight=models.DecimalField('Weight', null=True, blank=True, max_digits=7, decimal_places=2)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=500)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=10)
    old_customer_short_name=models.CharField('CustomerShortName', null=True, blank=True, max_length=50)
    old_customer_name=models.CharField('CustomerName', null=True, blank=True, max_length=250)
    old_change_color_id=models.CharField('ChangeColorID', null=True, blank=True, max_length=250)
    old_change_color=models.CharField('ChangeColor', null=True, blank=True, max_length=250)
    old_change_cust_color_num=models.CharField('ChangeCustColorNum', null=True, blank=True, max_length=250)
    old_customer_order_code=models.CharField('CustomerOrderCode', null=True, blank=True, max_length=250)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_colorchangerisk'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_job_sheet_no', 'old_color_num'],name='src_6beb43a8a1821866')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（ColorChangeRisk，待确认）'
        ordering=["-id"]

class SourceDyeCptLabRecipe(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='CptLabRecipe'
    SOURCE_FIELDS={'ID': 'old_id', 'strCode': 'old_str_code', 'lVersion': 'old_l_version', 'strName': 'old_str_name', 'strSubstateCode': 'old_str_substate_code', 'strOperator': 'old_str_operator', 'strCustomer': 'old_str_customer', 'dwSampleWt': 'old_dw_sample_wt', 'dwLiquidRatio': 'old_dw_liquid_ratio', 'dwTotalWt': 'old_dw_total_wt', 'dtModifyDate': 'old_dt_modify_date', 'dwCostPerKg': 'old_dw_cost_per_kg', 'strUser1': 'old_str_user1', 'strUser2': 'old_str_user2', 'strUser3': 'old_str_user3', 'bAddWater': 'old_b_add_water', 'strPotCode': 'old_str_pot_code', 'dwStdDispWt': 'old_dw_std_disp_wt', 'lDispFlag': 'old_l_disp_flag', 'IP': 'old_ip', 'CreateDate': 'old_create_date'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_create_date': ('now', None)}
    SOURCE_IDENTITIES=('old_id',)
    old_id=models.BigIntegerField('ID', null=False, blank=False)
    old_str_code=models.CharField('strCode', null=True, blank=True, max_length=30)
    old_l_version=models.IntegerField('lVersion', null=True, blank=True)
    old_str_name=models.CharField('strName', null=True, blank=True, max_length=50)
    old_str_substate_code=models.CharField('strSubstateCode', null=True, blank=True, max_length=30)
    old_str_operator=models.CharField('strOperator', null=True, blank=True, max_length=20)
    old_str_customer=models.CharField('strCustomer', null=True, blank=True, max_length=50)
    old_dw_sample_wt=models.FloatField('dwSampleWt', null=True, blank=True)
    old_dw_liquid_ratio=models.FloatField('dwLiquidRatio', null=True, blank=True)
    old_dw_total_wt=models.FloatField('dwTotalWt', null=True, blank=True)
    old_dt_modify_date=models.DateTimeField('dtModifyDate', null=True, blank=True)
    old_dw_cost_per_kg=models.FloatField('dwCostPerKg', null=True, blank=True)
    old_str_user1=models.CharField('strUser1', null=True, blank=True, max_length=40)
    old_str_user2=models.CharField('strUser2', null=True, blank=True, max_length=40)
    old_str_user3=models.CharField('strUser3', null=True, blank=True, max_length=40)
    old_b_add_water=models.BooleanField('bAddWater', null=False, blank=False)
    old_str_pot_code=models.CharField('strPotCode', null=True, blank=True, max_length=20)
    old_dw_std_disp_wt=models.FloatField('dwStdDispWt', null=True, blank=True)
    old_l_disp_flag=models.IntegerField('lDispFlag', null=True, blank=True)
    old_ip=models.CharField('IP', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_cptlabrecipe'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_62e9324d6398b1e8')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（CptLabRecipe，待确认）'
        ordering=["-id"]

class SourceDyeCptLabRecipeDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='CptLabRecipeDetail'
    SOURCE_FIELDS={'ID': 'old_id', 'nSide': 'old_n_side', 'dwRate': 'old_dw_rate', 'bManualSel': 'old_b_manual_sel', 'dwStrength': 'old_dw_strength', 'dwCalWt': 'old_dw_cal_wt', 'strCode': 'old_str_code', 'lVersion': 'old_l_version', 'lDetSeq': 'old_l_det_seq', 'lBottNo': 'old_l_bott_no', 'strProdCode': 'old_str_prod_code', 'strUnit': 'old_str_unit', 'dwDispWt': 'old_dw_disp_wt', 'IP': 'old_ip', 'CreateDate': 'old_create_date', 'dtModifyDate': 'old_dt_modify_date'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_create_date': ('now', None)}
    SOURCE_IDENTITIES=('old_id',)
    old_id=models.BigIntegerField('ID', null=False, blank=False)
    old_n_side=models.IntegerField('nSide', null=True, blank=True)
    old_dw_rate=models.FloatField('dwRate', null=True, blank=True)
    old_b_manual_sel=models.BooleanField('bManualSel', null=False, blank=False)
    old_dw_strength=models.FloatField('dwStrength', null=True, blank=True)
    old_dw_cal_wt=models.FloatField('dwCalWt', null=True, blank=True)
    old_str_code=models.CharField('strCode', null=True, blank=True, max_length=30)
    old_l_version=models.IntegerField('lVersion', null=True, blank=True)
    old_l_det_seq=models.IntegerField('lDetSeq', null=True, blank=True)
    old_l_bott_no=models.IntegerField('lBottNo', null=True, blank=True)
    old_str_prod_code=models.CharField('strProdCode', null=True, blank=True, max_length=30)
    old_str_unit=models.CharField('strUnit', null=True, blank=True, max_length=1)
    old_dw_disp_wt=models.FloatField('dwDispWt', null=True, blank=True)
    old_ip=models.CharField('IP', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_dt_modify_date=models.DateTimeField('dtModifyDate', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_cptlabrecipedetail'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_f0e16b982f73b514')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（CptLabRecipeDetail，待确认）'
        ordering=["-id"]

class SourceDyeCurSmpPrescriptEntry(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='Cur_Smp_PrescriptEntry'
    SOURCE_FIELDS={'FInterID': 'old_finter_id', 'FEntryID': 'old_fentry_id', 'FParentID': 'old_fparent_id', 'PhaseNo': 'old_phase_no', 'StuffNo': 'old_stuff_no', 'FItemID': 'old_fitem_id', 'FTechID': 'old_ftech_id', 'FTechUnit': 'old_ftech_unit', 'FRatioQty': 'old_fratio_qty', 'FRealRatioQty': 'old_freal_ratio_qty', 'FPrice': 'old_fprice', 'FAmount': 'old_famount', 'FCost': 'old_fcost', 'FNote': 'old_fnote', 'FBomEntryID': 'old_fbom_entry_id', 'FCalculateID': 'old_fcalculate_id', 'FRoutingRequest': 'old_frouting_request', 'FC_SW': 'old_fc_sw', 'FC_PZYL': 'old_fc_pzyl', 'FC_SWater': 'old_fc_swater', 'FC_PZYLI': 'old_fc_pzyli', 'FC_PHZ': 'old_fc_phz', 'FC_DDL': 'old_fc_ddl', 'FC_TIME': 'old_fc_time', 'FC_WD': 'old_fc_wd', 'FC_SB': 'old_fc_sb'}
    SOURCE_KEY=('FInterID', 'FEntryID', 'FParentID')
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_finter_id=models.IntegerField('FInterID', null=False, blank=False)
    old_fentry_id=models.IntegerField('FEntryID', null=False, blank=False)
    old_fparent_id=models.IntegerField('FParentID', null=False, blank=False)
    old_phase_no=models.IntegerField('PhaseNo', null=True, blank=True)
    old_stuff_no=models.IntegerField('StuffNo', null=True, blank=True)
    old_fitem_id=models.IntegerField('FItemID', null=True, blank=True)
    old_ftech_id=models.IntegerField('FTechID', null=True, blank=True)
    old_ftech_unit=models.CharField('FTechUnit', null=True, blank=True, max_length=30)
    old_fratio_qty=models.DecimalField('FRatioQty', null=True, blank=True, max_digits=28, decimal_places=10)
    old_freal_ratio_qty=models.DecimalField('FRealRatioQty', null=True, blank=True, max_digits=28, decimal_places=10)
    old_fprice=models.DecimalField('FPrice', null=True, blank=True, max_digits=28, decimal_places=10)
    old_famount=models.DecimalField('FAmount', null=True, blank=True, max_digits=28, decimal_places=10)
    old_fcost=models.DecimalField('FCost', null=True, blank=True, max_digits=28, decimal_places=10)
    old_fnote=models.CharField('FNote', null=True, blank=True, max_length=255)
    old_fbom_entry_id=models.IntegerField('FBomEntryID', null=True, blank=True)
    old_fcalculate_id=models.IntegerField('FCalculateID', null=True, blank=True)
    old_frouting_request=models.CharField('FRoutingRequest', null=True, blank=True, max_length=200)
    old_fc_sw=models.CharField('FC_SW', null=True, blank=True, max_length=50)
    old_fc_pzyl=models.CharField('FC_PZYL', null=True, blank=True, max_length=50)
    old_fc_swater=models.CharField('FC_SWater', null=True, blank=True, max_length=50)
    old_fc_pzyli=models.CharField('FC_PZYLI', null=True, blank=True, max_length=50)
    old_fc_phz=models.CharField('FC_PHZ', null=True, blank=True, max_length=50)
    old_fc_ddl=models.CharField('FC_DDL', null=True, blank=True, max_length=50)
    old_fc_time=models.CharField('FC_TIME', null=True, blank=True, max_length=50)
    old_fc_wd=models.CharField('FC_WD', null=True, blank=True, max_length=50)
    old_fc_sb=models.CharField('FC_SB', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_cur_smp_prescriptentry'
        indexes=[models.Index(fields=['source_batch', 'old_finter_id', 'old_fentry_id', 'old_fparent_id'],name='src_96984b66167c32f3')]
        verbose_name=verbose_name_plural='其他或待确认相关表（Cur_Smp_PrescriptEntry，待确认）'
        ordering=["-id"]

class SourceDyeDyeColor(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DyeColor'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'ColorNo': 'old_color_no', 'CheckNo': 'old_check_no', 'LabDipsSource': 'old_lab_dips_source', 'ProdID': 'old_prod_id', 'LotNo': 'old_lot_no', 'Spec': 'old_spec', 'ColorDepthID': 'old_color_depth_id', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'ColorE': 'old_color_e', 'CustColorNum': 'old_cust_color_num', 'ColorRGB': 'old_color_rgb', 'Price': 'old_price', 'MainStuffKindID': 'old_main_stuff_kind_id', 'IsToDoSample': 'old_is_to_do_sample', 'ColorCards': 'old_color_cards', 'Status': 'old_status', 'StartTime': 'old_start_time', 'LimitHours': 'old_limit_hours', 'OverTimeReason': 'old_over_time_reason', 'ShiftID': 'old_shift_id', 'EmpID': 'old_emp_id', 'WorkQty': 'old_work_qty', 'RedoTimes': 'old_redo_times', 'OriColorNo': 'old_ori_color_no', 'OriEmpID': 'old_ori_emp_id', 'OriShifID': 'old_ori_shif_id', 'JobSheetNo': 'old_job_sheet_no', 'Remarks': 'old_remarks', 'Width': 'old_width', 'Weight': 'old_weight', 'CustomerID': 'old_customer_id', 'GetSampleDate': 'old_get_sample_date', 'DlvSampleDate': 'old_dlv_sample_date', 'DyeRemarks': 'old_dye_remarks', 'fSampleDate': 'old_f_sample_date', 'PhaseID': 'old_phase_id', 'Dos': 'old_dos', 'fDos': 'old_f_dos', 'DosAll': 'old_dos_all', 'WSampleDate': 'old_wsample_date', 'SSampleDate': 'old_ssample_date', 'DyeColorID': 'old_dye_color_id', 'CreateDate': 'old_create_date', 'ModifyDate': 'old_modify_date', 'Creater': 'old_creater', 'Modifyer': 'old_modifyer', 'SheetDate': 'old_sheet_date'}
    SOURCE_KEY=('ColorNo',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单号', null=True, blank=True, max_length=20)
    old_color_no=models.CharField('来样明细号', null=False, blank=True, max_length=20)
    old_check_no=models.CharField('CheckNo', null=True, blank=True, max_length=20)
    old_lab_dips_source=models.IntegerField('LabDipsSource', null=True, blank=True)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=20)
    old_lot_no=models.CharField('LotNo', null=True, blank=True, max_length=50)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=128)
    old_color_depth_id=models.CharField('颜色深浅', null=True, blank=True, max_length=10)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=20)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=20)
    old_color_e=models.CharField('ColorE', null=True, blank=True, max_length=20)
    old_cust_color_num=models.CharField('客色号', null=True, blank=True, max_length=20)
    old_color_rgb=models.IntegerField('ColorRGB', null=True, blank=True)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=8, decimal_places=2)
    old_main_stuff_kind_id=models.CharField('MainStuffKindID', null=True, blank=True, max_length=10)
    old_is_to_do_sample=models.CharField('IsToDoSample', null=True, blank=True, max_length=10)
    old_color_cards=models.IntegerField('ColorCards', null=True, blank=True)
    old_status=models.CharField('Status', null=True, blank=True, max_length=2)
    old_start_time=models.CharField('StartTime', null=True, blank=True, max_length=14)
    old_limit_hours=models.DecimalField('LimitHours', null=True, blank=True, max_digits=5, decimal_places=2)
    old_over_time_reason=models.CharField('OverTimeReason', null=True, blank=True, max_length=20)
    old_shift_id=models.CharField('ShiftID', null=True, blank=True, max_length=10)
    old_emp_id=models.CharField('打样人', null=True, blank=True, max_length=10)
    old_work_qty=models.DecimalField('WorkQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_redo_times=models.IntegerField('RedoTimes', null=True, blank=True)
    old_ori_color_no=models.CharField('原色号明细', null=True, blank=True, max_length=20)
    old_ori_emp_id=models.CharField('OriEmpID', null=True, blank=True, max_length=10)
    old_ori_shif_id=models.CharField('OriShifID', null=True, blank=True, max_length=10)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_remarks=models.CharField('返打版原因', null=True, blank=True, max_length=100)
    old_width=models.DecimalField('Width', null=True, blank=True, max_digits=6, decimal_places=2)
    old_weight=models.DecimalField('Weight', null=True, blank=True, max_digits=6, decimal_places=2)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=100)
    old_get_sample_date=models.DateTimeField('GetSampleDate', null=True, blank=True)
    old_dlv_sample_date=models.DateTimeField('要求交样日期', null=True, blank=True)
    old_dye_remarks=models.CharField('打样要求描述', null=True, blank=True, max_length=1000)
    old_f_sample_date=models.DateTimeField('任务分配日期', null=True, blank=True)
    old_phase_id=models.CharField('染色流程', null=True, blank=True, max_length=100)
    old_dos=models.DecimalField('打样计分', null=True, blank=True, max_digits=10, decimal_places=2)
    old_f_dos=models.DecimalField('扣分', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dos_all=models.DecimalField('总分', null=True, blank=True, max_digits=10, decimal_places=2)
    old_wsample_date=models.DateTimeField('打样完成日期', null=True, blank=True)
    old_ssample_date=models.DateTimeField('送样日期', null=True, blank=True)
    old_dye_color_id=models.CharField('是否返打', null=True, blank=True, max_length=50)
    old_create_date=models.DateTimeField('制单日期', null=True, blank=True)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_creater=models.CharField('制单人', null=True, blank=True, max_length=50)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=50)
    old_sheet_date=models.DateTimeField('来样日期', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_dyecolor'
        indexes=[models.Index(fields=['source_batch', 'old_color_no'],name='src_997c9a69a1c288d5')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（DyeColor，待确认）'
        ordering=["-id"]

class SourceDyeDyeDipsRecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DyeDipsRecord'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetKind': 'old_sheet_kind', 'SheetDate': 'old_sheet_date', 'SheetStatus': 'old_sheet_status', 'BusinessUnitID': 'old_business_unit_id', 'CustomerID': 'old_customer_id', 'SalerGroupID': 'old_saler_group_id', 'SalerID': 'old_saler_id', 'ColorNo': 'old_color_no', 'ColorVersion': 'old_color_version', 'DeptID': 'old_dept_id', 'CheckNo': 'old_check_no', 'MainStuffKindID': 'old_main_stuff_kind_id', 'ProdID': 'old_prod_id', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'Structure': 'old_structure', 'ColorID': 'old_color_id', 'ColorDepthID': 'old_color_depth_id', 'ColorNum': 'old_color_num', 'CustColorNum': 'old_cust_color_num', 'ColorE': 'old_color_e', 'ColorRGB': 'old_color_rgb', 'RecipePriceSource': 'old_recipe_price_source', 'FabricSource': 'old_fabric_source', 'Weight': 'old_weight', 'CostEffirate': 'old_cost_effirate', 'Cost': 'old_cost', 'CostUnit': 'old_cost_unit', 'VerLight1ID': 'old_ver_light1_id', 'VerLight2ID': 'old_ver_light2_id', 'ConfirmSideID': 'old_confirm_side_id', 'EmpID': 'old_emp_id', 'ShiftID': 'old_shift_id', 'CheckerID': 'old_checker_id', 'ApproveDate': 'old_approve_date', 'DlvSampleDate': 'old_dlv_sample_date', 'RightStatus': 'old_right_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ConfirmVersion': 'old_confirm_version', 'Approver': 'old_approver', 'Times': 'old_times', 'StuffDosage': 'old_stuff_dosage', 'LabSheetNo': 'old_lab_sheet_no', 'PreFinalized': 'old_pre_finalized', 'CustSelfProduct': 'old_cust_self_product', 'DetailCustName': 'old_detail_cust_name', 'CostQuote': 'old_cost_quote', 'DyePhaseName': 'old_dye_phase_name', 'GaoLaodu': 'old_gao_laodu', 'EmpID1': 'old_emp_id1', 'ShiftCheckerID': 'old_shift_checker_id', 'EmpID2': 'old_emp_id2', 'EmpID3': 'old_emp_id3', 'Num': 'old_num', 'IsDoubleDye': 'old_is_double_dye', 'Invalid': 'old_invalid', 'GradeID': 'old_grade_id', 'ColorNumMark': 'old_color_num_mark', 'DepthE': 'old_depth_e', 'Revise': 'old_revise', 'Fluorescence': 'old_fluorescence', 'OriColorNo': 'old_ori_color_no'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('记录单号', null=True, blank=True, max_length=20)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户名称', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('业务组别', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('业务员', null=True, blank=True, max_length=10)
    old_color_no=models.CharField('颜色明细ID', null=True, blank=True, max_length=20)
    old_color_version=models.CharField('色板号', null=True, blank=True, max_length=20)
    old_dept_id=models.CharField('部门', null=True, blank=True, max_length=10)
    old_check_no=models.CharField('订单明细ID', null=True, blank=True, max_length=20)
    old_main_stuff_kind_id=models.CharField('主料类别', null=True, blank=True, max_length=10)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=20)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=128)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=50)
    old_structure=models.CharField('组织', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=50)
    old_color_depth_id=models.CharField('颜色深浅', null=True, blank=True, max_length=30)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=50)
    old_cust_color_num=models.CharField('客户色号', null=True, blank=True, max_length=100)
    old_color_e=models.CharField('英文名', null=True, blank=True, max_length=20)
    old_color_rgb=models.IntegerField('颜色RGB', null=True, blank=True)
    old_recipe_price_source=models.IntegerField('单价来源', null=True, blank=True)
    old_fabric_source=models.CharField('纱来源', null=True, blank=True, max_length=1)
    old_weight=models.DecimalField('克重', null=True, blank=True, max_digits=6, decimal_places=2)
    old_cost_effirate=models.DecimalField('成本系数', null=True, blank=True, max_digits=6, decimal_places=2)
    old_cost=models.DecimalField('成本', null=True, blank=True, max_digits=10, decimal_places=2)
    old_cost_unit=models.CharField('成本单位', null=True, blank=True, max_length=1)
    old_ver_light1_id=models.CharField('主光源', null=True, blank=True, max_length=10)
    old_ver_light2_id=models.CharField('副光源', null=True, blank=True, max_length=10)
    old_confirm_side_id=models.CharField('对色面', null=True, blank=True, max_length=10)
    old_emp_id=models.CharField('员工名称', null=True, blank=True, max_length=10)
    old_shift_id=models.CharField('班别', null=True, blank=True, max_length=10)
    old_checker_id=models.CharField('检验人', null=True, blank=True, max_length=10)
    old_approve_date=models.DateTimeField('确版时间', null=True, blank=True)
    old_dlv_sample_date=models.DateTimeField('交样日期', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_step_no=models.IntegerField('节点号', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_confirm_version=models.CharField('确版号', null=True, blank=True, max_length=20)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_times=models.IntegerField('试样次数', null=True, blank=True)
    old_stuff_dosage=models.DecimalField('染料分量', null=True, blank=True, max_digits=15, decimal_places=6)
    old_lab_sheet_no=models.CharField('LabSheetNo', null=True, blank=True, max_length=20)
    old_pre_finalized=models.CharField('预定', null=True, blank=True, max_length=50)
    old_cust_self_product=models.CharField('客户规格', null=True, blank=True, max_length=200)
    old_detail_cust_name=models.CharField('明细客户', null=True, blank=True, max_length=50)
    old_cost_quote=models.DecimalField('CostQuote', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dye_phase_name=models.CharField('DyePhaseName', null=True, blank=True, max_length=100)
    old_gao_laodu=models.CharField('高牢度', null=True, blank=True, max_length=100)
    old_emp_id1=models.CharField('打样员1', null=True, blank=True, max_length=50)
    old_shift_checker_id=models.CharField('领班', null=True, blank=True, max_length=50)
    old_emp_id2=models.CharField('打样员2', null=True, blank=True, max_length=50)
    old_emp_id3=models.CharField('打样员3', null=True, blank=True, max_length=50)
    old_num=models.FloatField('计件数', null=True, blank=True)
    old_is_double_dye=models.IntegerField('单双染', null=True, blank=True)
    old_invalid=models.BooleanField('Invalid', null=True, blank=True)
    old_grade_id=models.CharField('色号等级', null=True, blank=True, max_length=30)
    old_color_num_mark=models.CharField('色号类型', null=True, blank=True, max_length=30)
    old_depth_e=models.CharField('深浅E', null=True, blank=True, max_length=30)
    old_revise=models.BooleanField('是否修改', null=True, blank=True)
    old_fluorescence=models.CharField('荧光类别', null=True, blank=True, max_length=30)
    old_ori_color_no=models.CharField('原色号明细', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_dyedipsrecord'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_ce0a187e87c16394')]
        verbose_name=verbose_name_plural='小样/打样记录'
        ordering=["-id"]

class SourceDyeDyeDipsRecordDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DyeDipsRecordDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'PhaseNo': 'old_phase_no', 'StuffNo': 'old_stuff_no', 'StuffType': 'old_stuff_type', 'StuffID': 'old_stuff_id', 'Price': 'old_price', 'DosageA': 'old_dosage_a', 'AmountA': 'old_amount_a', 'DosageB': 'old_dosage_b', 'AmountB': 'old_amount_b', 'DosageC': 'old_dosage_c', 'AmountC': 'old_amount_c', 'DosageD': 'old_dosage_d', 'AmountD': 'old_amount_d', 'DosageE': 'old_dosage_e', 'AmountE': 'old_amount_e', 'DosageF': 'old_dosage_f', 'AmountF': 'old_amount_f', 'RecipeUnit': 'old_recipe_unit', 'DetailNote': 'old_detail_note', 'NewStuffID': 'old_new_stuff_id'}
    SOURCE_KEY=('SheetSeries', 'PhaseNo', 'StuffNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_phase_no=models.IntegerField('染程序号', null=False, blank=False)
    old_stuff_no=models.IntegerField('染料序号', null=False, blank=False)
    old_stuff_type=models.CharField('染料类别', null=True, blank=True, max_length=1)
    old_stuff_id=models.CharField('染料编码', null=True, blank=True, max_length=10)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=8, decimal_places=2)
    old_dosage_a=models.DecimalField('用量比例（A）', null=True, blank=True, max_digits=15, decimal_places=6)
    old_amount_a=models.DecimalField('金额A', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dosage_b=models.DecimalField('用量比例（B）', null=True, blank=True, max_digits=15, decimal_places=6)
    old_amount_b=models.DecimalField('金额B', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dosage_c=models.DecimalField('用量比例（C）', null=True, blank=True, max_digits=15, decimal_places=6)
    old_amount_c=models.DecimalField('金额C', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dosage_d=models.DecimalField('用量比例（D）', null=True, blank=True, max_digits=15, decimal_places=6)
    old_amount_d=models.DecimalField('金额D', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dosage_e=models.DecimalField('用量比例（E）', null=True, blank=True, max_digits=15, decimal_places=6)
    old_amount_e=models.DecimalField('金额E', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dosage_f=models.DecimalField('DosageF', null=True, blank=True, max_digits=15, decimal_places=6)
    old_amount_f=models.DecimalField('AmountF', null=True, blank=True, max_digits=10, decimal_places=2)
    old_recipe_unit=models.IntegerField('RecipeUnit', null=True, blank=True)
    old_detail_note=models.CharField('备注', null=True, blank=True, max_length=256)
    old_new_stuff_id=models.CharField('NewStuffID', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_dyedipsrecorddetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_phase_no'],name='src_e3c3ddb59b76a7d9'),models.Index(fields=['source_batch', 'old_sheet_series', 'old_phase_no', 'old_stuff_no'],name='src_39fc40d6878110e3')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（DyeDipsRecordDetail，待确认）'
        ordering=["-id"]

class SourceDyeDyeDipsRecordEmp(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DyeDipsRecordEmp'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'EmpID': 'old_emp_id', 'ColorVersion': 'old_color_version', 'CurrTime': 'old_curr_time', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('SheetSeries', 'EmpID')
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：DyeDipsRecord', 'target': 'erp_sampling.SourceDyeDyeDipsRecord', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 DyeDipsRecordEmp → DyeDipsRecord']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_emp_id=models.CharField('员工名称', null=False, blank=True, max_length=10)
    old_color_version=models.CharField('色板号', null=True, blank=True, max_length=20)
    old_curr_time=models.DateTimeField('当前时间', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    source_parent_1=models.ForeignKey('erp_sampling.SourceDyeDyeDipsRecord', verbose_name='原关系：DyeDipsRecord', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_dyedipsrecordemp'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_emp_id'],name='src_14545523a4c693f1')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（DyeDipsRecordEmp，待确认）'
        ordering=["-id"]

class SourceDyeDyeDipsRecordNote(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DyeDipsRecordNote'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'Note': 'old_note', 'Status': 'old_status'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_note=models.CharField('Note', null=True, blank=True, max_length=1000)
    old_status=models.BooleanField('Status', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_dyedipsrecordnote'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_6c9aa4e6e863349e')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（DyeDipsRecordNote，待确认）'
        ordering=["-id"]

class SourceDyeDyeDipsRecordPhase(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DyeDipsRecordPhase'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'PhaseNo': 'old_phase_no', 'PhaseID': 'old_phase_id', 'BathRatio': 'old_bath_ratio', 'PH': 'old_ph', 'ProgramID': 'old_program_id', 'WaterQty': 'old_water_qty', 'Remarks': 'old_remarks', 'Temperature': 'old_temperature', 'Minutes': 'old_minutes'}
    SOURCE_KEY=('SheetSeries', 'PhaseNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：DyeDipsRecord', 'target': 'erp_sampling.SourceDyeDyeDipsRecord', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 DyeDipsRecordPhaseDetail → DyeDipsRecord', '原界面主从 DyeDipsRecordPhase → DyeDipsRecord']}, {'field': 'source_parent_2', 'title': '原关系：DyeDipsRecordDetail', 'target': 'erp_sampling.SourceDyeDyeDipsRecordDetail', 'source_fields': ['SheetSeries', 'PhaseNo'], 'target_fields': ['SheetSeries', 'PhaseNo'], 'evidence': ['原界面主从 DyeDipsRecordPhaseBulk → DyeDipsRecordDetailBulk']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_phase_no=models.IntegerField('染程序号', null=False, blank=False)
    old_phase_id=models.CharField('染程编码', null=True, blank=True, max_length=10)
    old_bath_ratio=models.DecimalField('浴比', null=True, blank=True, max_digits=6, decimal_places=2)
    old_ph=models.CharField('PH值', null=True, blank=True, max_length=10)
    old_program_id=models.CharField('工艺编码', null=True, blank=True, max_length=10)
    old_water_qty=models.DecimalField('水重', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_temperature=models.DecimalField('Temperature', null=True, blank=True, max_digits=5, decimal_places=1)
    old_minutes=models.DecimalField('Minutes', null=True, blank=True, max_digits=10, decimal_places=2)
    source_parent_1=models.ForeignKey('erp_sampling.SourceDyeDyeDipsRecord', verbose_name='原关系：DyeDipsRecord', null=True, blank=True, on_delete=models.PROTECT, related_name='+')
    source_parent_2=models.ForeignKey('erp_sampling.SourceDyeDyeDipsRecordDetail', verbose_name='原关系：DyeDipsRecordDetail', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_dyedipsrecordphase'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_phase_no'],name='src_63441dec6b8a9d84')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（DyeDipsRecordPhase，待确认）'
        ordering=["-id"]

class SourceDyeDyeLabAtte(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DyeLabAtte'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'FieldType': 'old_field_type', 'AtteCode': 'old_atte_code', 'AtteValue': 'old_atte_value', 'Description': 'old_description'}
    SOURCE_KEY=('SheetSeries', 'FieldType', 'AtteCode')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：DyeLabMain', 'target': 'erp_sampling.SourceDyeDyeLabMain', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 DyeLabAtteBulk → DyeLabMainBulk', '原界面主从 DyeLabAtte → DyeLabMain']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_field_type=models.CharField('数据类别', null=False, blank=True, max_length=20)
    old_atte_code=models.CharField('事项', null=False, blank=True, max_length=10)
    old_atte_value=models.CharField('内容', null=True, blank=True, max_length=500)
    old_description=models.CharField('描述', null=True, blank=True, max_length=500)
    source_parent_1=models.ForeignKey('erp_sampling.SourceDyeDyeLabMain', verbose_name='原关系：DyeLabMain', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_dyelabatte'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_field_type', 'old_atte_code'],name='src_03867000420b7541')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（DyeLabAtte，待确认）'
        ordering=["-id"]

class SourceDyeDyeLabColor(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DyeLabColor'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'ColorNo': 'old_color_no', 'CheckNo': 'old_check_no', 'LabDipsSource': 'old_lab_dips_source', 'ProdID': 'old_prod_id', 'CustSelfProduct': 'old_cust_self_product', 'LotNo': 'old_lot_no', 'Spec': 'old_spec', 'ColorDepthID': 'old_color_depth_id', 'ColorID': 'old_color_id', 'OrderNum': 'old_order_num', 'ColorNum': 'old_color_num', 'ColorE': 'old_color_e', 'CustColorNum': 'old_cust_color_num', 'ColorRGB': 'old_color_rgb', 'ColorAfter': 'old_color_after', 'ColorNumInput': 'old_color_num_input', 'ColorNumMark': 'old_color_num_mark', 'ColorMark': 'old_color_mark', 'ColorMarkt': 'old_color_markt', 'Price': 'old_price', 'MainStuffKindID': 'old_main_stuff_kind_id', 'IsToDoSample': 'old_is_to_do_sample', 'ColorCards': 'old_color_cards', 'Status': 'old_status', 'StartTime': 'old_start_time', 'LimitHours': 'old_limit_hours', 'OverTimeReason': 'old_over_time_reason', 'ShiftID': 'old_shift_id', 'EmpID': 'old_emp_id', 'WorkQty': 'old_work_qty', 'RedoTimes': 'old_redo_times', 'OriColorNo': 'old_ori_color_no', 'OriEmpID': 'old_ori_emp_id', 'OriShifID': 'old_ori_shif_id', 'JobSheetNo': 'old_job_sheet_no', 'Remarks': 'old_remarks', 'Width': 'old_width', 'Weight': 'old_weight', 'Markt': 'old_markt', 'R': 'old_r', 'G': 'old_g', 'B': 'old_b', 'RGB': 'old_rgb', 'GradeID': 'old_grade_id', 'KHSHORPTSH': 'old_khshorptsh', 'DetailCustName': 'old_detail_cust_name'}
    SOURCE_KEY=('ColorNo',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：DyeLabMain', 'target': 'erp_sampling.SourceDyeDyeLabMain', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 DyeLabColor → DyeLabMain', '原界面主从 DyeLabColorBulk → DyeLabMainBulk', '原界面主从 ShowDyeLabColor → ShowDyeLabMain']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=True, blank=True, max_length=20)
    old_color_no=models.CharField('颜色明细号', null=False, blank=True, max_length=20)
    old_check_no=models.CharField('订单明细号', null=True, blank=True, max_length=20)
    old_lab_dips_source=models.IntegerField('打样任务来源', null=True, blank=True)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=20)
    old_cust_self_product=models.CharField('客户规格', null=True, blank=True, max_length=200)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=50)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=128)
    old_color_depth_id=models.CharField('颜色深浅', null=True, blank=True, max_length=10)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=50)
    old_order_num=models.CharField('顺序编号', null=True, blank=True, max_length=10)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=20)
    old_color_e=models.CharField('原色号', null=True, blank=True, max_length=20)
    old_cust_color_num=models.CharField('客户色号', null=True, blank=True, max_length=100)
    old_color_rgb=models.IntegerField('颜色RGB', null=True, blank=True)
    old_color_after=models.CharField('色号后缀', null=True, blank=True, max_length=10)
    old_color_num_input=models.CharField('输入色号', null=True, blank=True, max_length=20)
    old_color_num_mark=models.CharField('色号类型', null=True, blank=True, max_length=10)
    old_color_mark=models.CharField('颜色代号', null=True, blank=True, max_length=10)
    old_color_markt=models.CharField('色号前缀', null=True, blank=True, max_length=10)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=8, decimal_places=2)
    old_main_stuff_kind_id=models.CharField('主料类别', null=True, blank=True, max_length=10)
    old_is_to_do_sample=models.CharField('打样安排', null=True, blank=True, max_length=10)
    old_color_cards=models.IntegerField('色卡份数', null=True, blank=True)
    old_status=models.CharField('状态', null=True, blank=True, max_length=2)
    old_start_time=models.CharField('开始时间', null=True, blank=True, max_length=14)
    old_limit_hours=models.DecimalField('限制时间', null=True, blank=True, max_digits=5, decimal_places=2)
    old_over_time_reason=models.CharField('超时原因', null=True, blank=True, max_length=20)
    old_shift_id=models.CharField('班别', null=True, blank=True, max_length=10)
    old_emp_id=models.CharField('员工', null=True, blank=True, max_length=10)
    old_work_qty=models.DecimalField('产量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_redo_times=models.IntegerField('返打次数', null=True, blank=True)
    old_ori_color_no=models.CharField('原色号明细', null=True, blank=True, max_length=20)
    old_ori_emp_id=models.CharField('原工号', null=True, blank=True, max_length=10)
    old_ori_shif_id=models.CharField('原班别', null=True, blank=True, max_length=10)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=1000)
    old_width=models.DecimalField('门幅', null=True, blank=True, max_digits=6, decimal_places=2)
    old_weight=models.DecimalField('重量', null=True, blank=True, max_digits=6, decimal_places=2)
    old_markt=models.CharField('Markt', null=True, blank=True, max_length=10)
    old_r=models.IntegerField('R', null=True, blank=True)
    old_g=models.IntegerField('G', null=True, blank=True)
    old_b=models.IntegerField('B', null=True, blank=True)
    old_rgb=models.IntegerField('RGB', null=True, blank=True)
    old_grade_id=models.CharField('色号等级', null=True, blank=True, max_length=50)
    old_khshorptsh=models.CharField('KHSHORPTSH', null=True, blank=True, max_length=255)
    old_detail_cust_name=models.CharField('明细客户', null=True, blank=True, max_length=512)
    source_parent_1=models.ForeignKey('erp_sampling.SourceDyeDyeLabMain', verbose_name='原关系：DyeLabMain', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_dyelabcolor'
        indexes=[models.Index(fields=['source_batch', 'old_color_no'],name='src_732b11e8a63606cd'),models.Index(fields=['source_batch', 'old_sheet_series', 'old_color_no'],name='src_6047d0144d733d66')]
        verbose_name=verbose_name_plural='化验室颜色与打样'
        ordering=["-id"]

class SourceDyeDyeLabColorRecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DyeLabColorRecord'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'ColorNo': 'old_color_no', 'RecordID': 'old_record_id', 'EmpID': 'old_emp_id', 'StartTime': 'old_start_time', 'EndTime': 'old_end_time', 'Status': 'old_status', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('SheetSeries', 'ColorNo', 'RecordID')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：DyeLabColor', 'target': 'erp_sampling.SourceDyeDyeLabColor', 'source_fields': ['SheetSeries', 'ColorNo'], 'target_fields': ['SheetSeries', 'ColorNo'], 'evidence': ['原界面主从 DyeLabColorRecord → DyeLabColor']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('流水', null=False, blank=True, max_length=20)
    old_color_no=models.CharField('颜色明细号', null=False, blank=True, max_length=20)
    old_record_id=models.CharField('记录编号', null=False, blank=True, max_length=50)
    old_emp_id=models.CharField('员工', null=True, blank=True, max_length=50)
    old_start_time=models.DateTimeField('开始时间', null=True, blank=True)
    old_end_time=models.DateTimeField('结束时间', null=True, blank=True)
    old_status=models.CharField('状态', null=True, blank=True, max_length=10)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    source_parent_1=models.ForeignKey('erp_sampling.SourceDyeDyeLabColor', verbose_name='原关系：DyeLabColor', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_dyelabcolorrecord'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_color_no', 'old_record_id'],name='src_5afddd002e2634a7')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（DyeLabColorRecord，待确认）'
        ordering=["-id"]

class SourceDyeDyeLabMain(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DyeLabMain'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetKind': 'old_sheet_kind', 'SheetDate': 'old_sheet_date', 'SheetStatus': 'old_sheet_status', 'DeptID': 'old_dept_id', 'BusinessUnitID': 'old_business_unit_id', 'SalerID': 'old_saler_id', 'SalerGroupID': 'old_saler_group_id', 'CustomerID': 'old_customer_id', 'OrderSheetNo': 'old_order_sheet_no', 'GetSampleDate': 'old_get_sample_date', 'ToBackSample': 'old_to_back_sample', 'DlvSampleDate': 'old_dlv_sample_date', 'TakeFabStatus': 'old_take_fab_status', 'IsSampleCharge': 'old_is_sample_charge', 'Linker': 'old_linker', 'LinkerInfo': 'old_linker_info', 'VerLight1ID': 'old_ver_light1_id', 'VerLight2ID': 'old_ver_light2_id', 'RightStatus': 'old_right_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'NumInfo': 'old_num_info', 'DetailCustName': 'old_detail_cust_name', 'NumNO': 'old_num_no', 'KindType': 'old_kind_type', 'Duiseluogang': 'old_duiseluogang', 'Daipaidaban': 'old_daipaidaban', 'Dabanpise': 'old_dabanpise', 'CustomerCode': 'old_customer_code'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('任务单号', null=True, blank=True, max_length=20)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_status=models.IntegerField('单据日期', null=True, blank=True)
    old_dept_id=models.CharField('部门', null=True, blank=True, max_length=10)
    old_business_unit_id=models.CharField('经营单位', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('业务员', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('业务组别', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户名称', null=True, blank=True, max_length=10)
    old_order_sheet_no=models.CharField('订单号', null=True, blank=True, max_length=20)
    old_get_sample_date=models.DateTimeField('收样时间', null=True, blank=True)
    old_to_back_sample=models.BooleanField('客样退回', null=True, blank=True)
    old_dlv_sample_date=models.DateTimeField('交样日期', null=True, blank=True)
    old_take_fab_status=models.CharField('带纱状态', null=True, blank=True, max_length=1)
    old_is_sample_charge=models.BooleanField('是否收费', null=True, blank=True)
    old_linker=models.CharField('联系人', null=True, blank=True, max_length=10)
    old_linker_info=models.CharField('联系信息', null=True, blank=True, max_length=100)
    old_ver_light1_id=models.CharField('主光源', null=True, blank=True, max_length=10)
    old_ver_light2_id=models.CharField('副光源', null=True, blank=True, max_length=10)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_step_no=models.IntegerField('节点号', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_num_info=models.CharField('送版份数', null=True, blank=True, max_length=50)
    old_detail_cust_name=models.CharField('明细客户', null=True, blank=True, max_length=50)
    old_num_no=models.IntegerField('色版数', null=True, blank=True)
    old_kind_type=models.CharField('打板需求', null=True, blank=True, max_length=10)
    old_duiseluogang=models.CharField('原办选项', null=True, blank=True, max_length=10)
    old_daipaidaban=models.CharField('待排打板', null=True, blank=True, max_length=10)
    old_dabanpise=models.CharField('打板批色', null=True, blank=True, max_length=10)
    old_customer_code=models.CharField('CustomerCode', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_dyelabmain'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_00eaf39a257a8850')]
        verbose_name=verbose_name_plural='化验室打样主表'
        ordering=["-id"]

class SourceDyeDyeProduceItem(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DyeProduceItem'
    SOURCE_FIELDS={'ID': 'old_id', 'SheetSeries': 'old_sheet_series', 'JobSheetNo': 'old_job_sheet_no', 'FabricKindID': 'old_fabric_kind_id', 'PhaseID': 'old_phase_id', 'PhaseNo': 'old_phase_no', 'Dosage': 'old_dosage', 'MDosage': 'old_mdosage', 'ColorLevel': 'old_color_level'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=('old_id',)
    old_id=models.IntegerField('ID', null=False, blank=False)
    old_sheet_series=models.CharField('SheetSeries', null=True, blank=True, max_length=50)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)
    old_fabric_kind_id=models.CharField('FabricKindID', null=True, blank=True, max_length=50)
    old_phase_id=models.CharField('PhaseID', null=True, blank=True, max_length=50)
    old_phase_no=models.CharField('PhaseNo', null=True, blank=True, max_length=50)
    old_dosage=models.DecimalField('Dosage', null=True, blank=True, max_digits=10, decimal_places=6)
    old_mdosage=models.DecimalField('MDosage', null=True, blank=True, max_digits=10, decimal_places=6)
    old_color_level=models.CharField('ColorLevel', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_dyeproduceitem'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_e5368aa89774d366')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（DyeProduceItem，待确认）'
        ordering=["-id"]

class SourceDyeDyeRecipe(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DyeRecipe'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetKind': 'old_sheet_kind', 'SheetType': 'old_sheet_type', 'SheetDate': 'old_sheet_date', 'BusinessUnitID': 'old_business_unit_id', 'DeptID': 'old_dept_id', 'CustomerID': 'old_customer_id', 'SalerID': 'old_saler_id', 'CheckNo': 'old_check_no', 'ProcessID': 'old_process_id', 'MainStuffKindID': 'old_main_stuff_kind_id', 'ColorNo': 'old_color_no', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'ColorE': 'old_color_e', 'ColorRGB': 'old_color_rgb', 'ColorDepthID': 'old_color_depth_id', 'CustColorNum': 'old_cust_color_num', 'L': 'old_l', 'A': 'old_a', 'B': 'old_b', 'OriRecipeSheetNo': 'old_ori_recipe_sheet_no', 'ProdID': 'old_prod_id', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'Structure': 'old_structure', 'ToPlace': 'old_to_place', 'RecipePriceSource': 'old_recipe_price_source', 'Cost': 'old_cost', 'CostUnit': 'old_cost_unit', 'IsHaveFirstVat': 'old_is_have_first_vat', 'CheckerID': 'old_checker_id', 'MakerID': 'old_maker_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'ProdKindID': 'old_prod_kind_id', 'StandRecipeNo': 'old_stand_recipe_no', 'ColorVersion': 'old_color_version', 'VerLight1ID': 'old_ver_light1_id', 'CustSelfProduct': 'old_cust_self_product', 'GradeID': 'old_grade_id', 'ColorNumMark': 'old_color_num_mark', 'DepthE': 'old_depth_e', 'Revise': 'old_revise', 'Fluorescence': 'old_fluorescence', 'OriColorNo': 'old_ori_color_no', 'Whether': 'old_whether', 'staff': 'old_staff'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('配方编号', null=True, blank=True, max_length=20)
    old_sheet_kind=models.IntegerField('配方类型', null=True, blank=True)
    old_sheet_type=models.IntegerField('配方料单类别', null=True, blank=True)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位', null=True, blank=True, max_length=10)
    old_dept_id=models.CharField('部门', null=True, blank=True, max_length=32)
    old_customer_id=models.CharField('客户名称', null=True, blank=True, max_length=32)
    old_saler_id=models.CharField('业务员', null=True, blank=True, max_length=32)
    old_check_no=models.CharField('订单明细号', null=True, blank=True, max_length=56)
    old_process_id=models.CharField('工序名称', null=True, blank=True, max_length=250)
    old_main_stuff_kind_id=models.CharField('染化料主料类别', null=True, blank=True, max_length=56)
    old_color_no=models.CharField('任务颜色明细号', null=True, blank=True, max_length=56)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=50)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=20)
    old_color_e=models.CharField('英文名称', null=True, blank=True, max_length=50)
    old_color_rgb=models.IntegerField('颜色RGB', null=True, blank=True)
    old_color_depth_id=models.CharField('颜色深浅', null=True, blank=True, max_length=32)
    old_cust_color_num=models.CharField('客户色号', null=True, blank=True, max_length=100)
    old_l=models.DecimalField('CIE色度L值', null=True, blank=True, max_digits=7, decimal_places=3)
    old_a=models.DecimalField('CIE色度A值', null=True, blank=True, max_digits=7, decimal_places=3)
    old_b=models.DecimalField('CIE色度B值', null=True, blank=True, max_digits=7, decimal_places=3)
    old_ori_recipe_sheet_no=models.CharField('原配方编号', null=True, blank=True, max_length=56)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=128)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=128)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=50)
    old_structure=models.CharField('组织', null=True, blank=True, max_length=50)
    old_to_place=models.CharField('交货地址', null=True, blank=True, max_length=500)
    old_recipe_price_source=models.IntegerField('单价源', null=True, blank=True)
    old_cost=models.DecimalField('成本', null=True, blank=True, max_digits=10, decimal_places=2)
    old_cost_unit=models.CharField('成本单位', null=True, blank=True, max_length=1)
    old_is_have_first_vat=models.BooleanField('是否头缸', null=True, blank=True)
    old_checker_id=models.CharField('检验员', null=True, blank=True, max_length=10)
    old_maker_id=models.CharField('复样员', null=True, blank=True, max_length=10)
    old_sheet_status=models.CharField('单据状态', null=True, blank=True, max_length=1)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_step_no=models.IntegerField('节点号', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=1000)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_prod_kind_id=models.CharField('成品类别', null=True, blank=True, max_length=10)
    old_stand_recipe_no=models.CharField('标准配方号', null=True, blank=True, max_length=128)
    old_color_version=models.CharField('确板号', null=True, blank=True, max_length=20)
    old_ver_light1_id=models.CharField('VerLight1ID', null=True, blank=True, max_length=20)
    old_cust_self_product=models.CharField('客户规格', null=True, blank=True, max_length=200)
    old_grade_id=models.CharField('色号等级', null=True, blank=True, max_length=30)
    old_color_num_mark=models.CharField('色号类型', null=True, blank=True, max_length=30)
    old_depth_e=models.CharField('DepthE', null=True, blank=True, max_length=30)
    old_revise=models.BooleanField('是否修改', null=True, blank=True)
    old_fluorescence=models.CharField('荧光类别', null=True, blank=True, max_length=30)
    old_ori_color_no=models.CharField('原色号明细', null=True, blank=True, max_length=50)
    old_whether=models.BooleanField('是否', null=True, blank=True)
    old_staff=models.CharField('打办人员', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_dyerecipe'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_0febd1c6c101864b')]
        verbose_name=verbose_name_plural='染色配方'
        ordering=["-id"]

class SourceDyeDyeRecipeDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DyeRecipeDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'PhaseNo': 'old_phase_no', 'StuffNo': 'old_stuff_no', 'StuffType': 'old_stuff_type', 'StuffID': 'old_stuff_id', 'Dosage': 'old_dosage', 'Price': 'old_price', 'Amount': 'old_amount', 'RecipeUnit': 'old_recipe_unit', 'DetailNote': 'old_detail_note', 'CarryIndex': 'old_carry_index', 'StepName': 'old_step_name', 'NewStuffID': 'old_new_stuff_id', 'Describe': 'old_describe'}
    SOURCE_KEY=('SheetSeries', 'PhaseNo', 'StuffNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：DyeRecipePhase', 'target': 'erp_sampling.SourceDyeDyeRecipePhase', 'source_fields': ['SheetSeries', 'PhaseNo'], 'target_fields': ['SheetSeries', 'PhaseNo'], 'evidence': ['原界面主从 DyeRecipeDetail → DyeRecipePhase']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_phase_no=models.IntegerField('染程序号', null=False, blank=False)
    old_stuff_no=models.IntegerField('染程明细序号', null=False, blank=False)
    old_stuff_type=models.CharField('染料类别', null=True, blank=True, max_length=1)
    old_stuff_id=models.CharField('染料名称', null=True, blank=True, max_length=10)
    old_dosage=models.DecimalField('比例', null=True, blank=True, max_digits=15, decimal_places=6)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=16, decimal_places=6)
    old_amount=models.DecimalField('金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_recipe_unit=models.IntegerField('单位', null=True, blank=True)
    old_detail_note=models.CharField('DetailNote', null=True, blank=True, max_length=256)
    old_carry_index=models.CharField('CarryIndex', null=True, blank=True, max_length=20)
    old_step_name=models.CharField('StepName', null=True, blank=True, max_length=50)
    old_new_stuff_id=models.CharField('NewStuffID', null=True, blank=True, max_length=20)
    old_describe=models.CharField('Describe', null=True, blank=True, max_length=25)
    source_parent_1=models.ForeignKey('erp_sampling.SourceDyeDyeRecipePhase', verbose_name='原关系：DyeRecipePhase', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_dyerecipedetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_phase_no', 'old_stuff_no'],name='src_c667fe7abeddc3af')]
        verbose_name=verbose_name_plural='染色配方明细'
        ordering=["-id"]

class SourceDyeDyeRecipeJob(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DyeRecipeJob'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'JobSheetNo': 'old_job_sheet_no', 'Status': 'old_status', 'CurrTime': 'old_curr_time'}
    SOURCE_KEY=('SheetSeries', 'JobSheetNo')
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：DyeRecipe', 'target': 'erp_sampling.SourceDyeDyeRecipe', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 FinishDyeRecipeJob → FinishDyeRecipe', '原界面主从 DyeRecipeJob → DyeRecipe', '原界面主从 PrepareDyeRecipeJob → PrepareDyeRecipe']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('缸号', null=False, blank=True, max_length=50)
    old_status=models.CharField('状态', null=True, blank=True, max_length=1)
    old_curr_time=models.DateTimeField('当前时间', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_sampling.SourceDyeDyeRecipe', verbose_name='原关系：DyeRecipe', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_dyerecipejob'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_job_sheet_no'],name='src_8436eb921600e4ff')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（DyeRecipeJob，待确认）'
        ordering=["-id"]

class SourceDyeDyeRecipePhase(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DyeRecipePhase'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'PhaseNo': 'old_phase_no', 'PhaseID': 'old_phase_id', 'BathRatio': 'old_bath_ratio', 'PH': 'old_ph', 'ProgramID': 'old_program_id', 'WaterQty': 'old_water_qty', 'Remarks': 'old_remarks', 'Minutes': 'old_minutes', 'Temperature': 'old_temperature'}
    SOURCE_KEY=('SheetSeries', 'PhaseNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：DyeRecipe', 'target': 'erp_sampling.SourceDyeDyeRecipe', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 DyeRecipePhase → DyeRecipe', '原界面主从 WashDyeRecipePhaseDetail → WashDyeRecipe', '原界面主从 PrepareDyeRecipePhaseDetail → PrepareDyeRecipe', '原界面主从 ReworkDyeRecipePhaseDetail → ReworkDyeRecipe', '原界面主从 OtherDyeRecipePhaseDetail → OtherDyeRecipe', '原界面主从 StandardDyeRecipePhaseDetail → StandardDyeRecipe', '原界面主从 BulkDyeRecipePhaseDetail → BulkDyeRecipe', '原界面主从 FinishDyeRecipePhaseDetail → FinishDyeRecipe', '原界面主从 TrialDyeRecipePhaseDetail → TrialDyeRecipe', '原界面主从 DyeRecipePhaseDetail → DyeRecipe']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('明细流水号', null=False, blank=True, max_length=20)
    old_phase_no=models.IntegerField('染程序号', null=False, blank=False)
    old_phase_id=models.CharField('染程名称', null=True, blank=True, max_length=10)
    old_bath_ratio=models.DecimalField('浴比', null=True, blank=True, max_digits=6, decimal_places=2)
    old_ph=models.CharField('PH值', null=True, blank=True, max_length=10)
    old_program_id=models.CharField('工艺编码', null=True, blank=True, max_length=10)
    old_water_qty=models.DecimalField('水量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_minutes=models.DecimalField('分钟', null=True, blank=True, max_digits=10, decimal_places=2)
    old_temperature=models.DecimalField('温度', null=True, blank=True, max_digits=5, decimal_places=1)
    source_parent_1=models.ForeignKey('erp_sampling.SourceDyeDyeRecipe', verbose_name='原关系：DyeRecipe', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_dyerecipephase'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_phase_no'],name='src_031ed90a706fbd41')]
        verbose_name=verbose_name_plural='染色配方阶段'
        ordering=["-id"]

class SourceDyeDyeReprint(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DyeReprint'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetKind': 'old_sheet_kind', 'JobSheetNo': 'old_job_sheet_no', 'CustomerID': 'old_customer_id', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'ProdID': 'old_prod_id', 'ShiftID': 'old_shift_id', 'ShiftCheckerID': 'old_shift_checker_id', 'EmpID': 'old_emp_id', 'EmpID1': 'old_emp_id1', 'EmpID2': 'old_emp_id2', 'EmpID3': 'old_emp_id3', 'Num': 'old_num', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'SheetDate': 'old_sheet_date', 'Kind': 'old_kind'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('单号', null=True, blank=True, max_length=50)
    old_sheet_kind=models.IntegerField('类型', null=True, blank=True)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=50)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=50)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_shift_id=models.CharField('班别', null=True, blank=True, max_length=50)
    old_shift_checker_id=models.CharField('领班', null=True, blank=True, max_length=50)
    old_emp_id=models.CharField('员工名称', null=True, blank=True, max_length=10)
    old_emp_id1=models.CharField('打样员1', null=True, blank=True, max_length=50)
    old_emp_id2=models.CharField('打样员2', null=True, blank=True, max_length=50)
    old_emp_id3=models.CharField('打样员3', null=True, blank=True, max_length=50)
    old_num=models.FloatField('Num', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=1000)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=50)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_kind=models.IntegerField('类型', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_dyereprint'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_20b8c06d5252b7e9')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（DyeReprint，待确认）'
        ordering=["-id"]

class SourceDyeDyeStartDateTime(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DyeStartDateTime'
    SOURCE_FIELDS={'AutoID': 'old_auto_id', 'JobSheetNo': 'old_job_sheet_no', 'ProcessNo': 'old_process_no', 'ProcessID': 'old_process_id', 'MachineID': 'old_machine_id', 'PlanDate': 'old_plan_date', 'JobSheetSeries': 'old_job_sheet_series', 'CombineSheetNos': 'old_combine_sheet_nos'}
    SOURCE_KEY=('AutoID',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=('old_auto_id',)
    old_auto_id=models.IntegerField('AutoID', null=False, blank=False)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)
    old_process_no=models.CharField('ProcessNo', null=True, blank=True, max_length=10)
    old_process_id=models.CharField('ProcessID', null=True, blank=True, max_length=32)
    old_machine_id=models.CharField('MachineID', null=True, blank=True, max_length=50)
    old_plan_date=models.DateTimeField('PlanDate', null=True, blank=True)
    old_job_sheet_series=models.CharField('JobSheetSeries', null=True, blank=True, max_length=50)
    old_combine_sheet_nos=models.CharField('CombineSheetNos', null=True, blank=True, max_length=200)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_dyestartdatetime'
        indexes=[models.Index(fields=['source_batch', 'old_auto_id'],name='src_f9b6756ec4be0806')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（DyeStartDateTime，待确认）'
        ordering=["-id"]

class SourceDyeLabDips(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='LabDips'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetKind': 'old_sheet_kind', 'SheetType': 'old_sheet_type', 'SheetDate': 'old_sheet_date', 'DeptID': 'old_dept_id', 'CustomerID': 'old_customer_id', 'SalerID': 'old_saler_id', 'DetailCustName': 'old_detail_cust_name', 'OrderSheetNo': 'old_order_sheet_no', 'IsHurry': 'old_is_hurry', 'IsHaveFirstVat': 'old_is_have_first_vat', 'GetSampleDate': 'old_get_sample_date', 'ToBackSample': 'old_to_back_sample', 'DlvSampleDate': 'old_dlv_sample_date', 'TakeFabStatus': 'old_take_fab_status', 'Linker': 'old_linker', 'LinkerInfo': 'old_linker_info', 'VerLight1ID': 'old_ver_light1_id', 'VerLight2ID': 'old_ver_light2_id', 'Width': 'old_width', 'Weight': 'old_weight', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'TotalColors': 'old_total_colors'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=20)
    old_sheet_kind=models.IntegerField('SheetKind', null=True, blank=True)
    old_sheet_type=models.IntegerField('SheetType', null=True, blank=True)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_dept_id=models.CharField('DeptID', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('SalerID', null=True, blank=True, max_length=10)
    old_detail_cust_name=models.CharField('DetailCustName', null=True, blank=True, max_length=50)
    old_order_sheet_no=models.CharField('OrderSheetNo', null=True, blank=True, max_length=20)
    old_is_hurry=models.BooleanField('IsHurry', null=True, blank=True)
    old_is_have_first_vat=models.BooleanField('IsHaveFirstVat', null=True, blank=True)
    old_get_sample_date=models.DateTimeField('GetSampleDate', null=True, blank=True)
    old_to_back_sample=models.BooleanField('ToBackSample', null=True, blank=True)
    old_dlv_sample_date=models.DateTimeField('DlvSampleDate', null=True, blank=True)
    old_take_fab_status=models.CharField('TakeFabStatus', null=True, blank=True, max_length=10)
    old_linker=models.CharField('Linker', null=True, blank=True, max_length=10)
    old_linker_info=models.CharField('LinkerInfo', null=True, blank=True, max_length=100)
    old_ver_light1_id=models.CharField('VerLight1ID', null=True, blank=True, max_length=10)
    old_ver_light2_id=models.CharField('VerLight2ID', null=True, blank=True, max_length=10)
    old_width=models.DecimalField('Width', null=True, blank=True, max_digits=6, decimal_places=2)
    old_weight=models.DecimalField('Weight', null=True, blank=True, max_digits=6, decimal_places=2)
    old_sheet_status=models.CharField('SheetStatus', null=True, blank=True, max_length=1)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_print_times=models.IntegerField('PrintTimes', null=True, blank=True)
    old_revisions=models.IntegerField('Revisions', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_total_colors=models.IntegerField('TotalColors', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_labdips'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_de21aad3a84abf3e')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（LabDips，待确认）'
        ordering=["-id"]

class SourceDyePrintColorSeparate(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PrintColorSeparate'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetKind': 'old_sheet_kind', 'SheetDate': 'old_sheet_date', 'SheetStatus': 'old_sheet_status', 'LYSheetNo': 'old_lysheet_no', 'LYDetailNo': 'old_lydetail_no', 'CustomerID': 'old_customer_id', 'DetailCustomer': 'old_detail_customer', 'GrayID': 'old_gray_id', 'ScreenType': 'old_screen_type', 'OriginalNO': 'old_original_no', 'PrintCode': 'old_print_code', 'PrintName': 'old_print_name', 'ColorPlateCount': 'old_color_plate_count', 'FilmPiece': 'old_film_piece', 'FilmSize': 'old_film_size', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'RightStatus': 'old_right_status', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'PrintSheetNo': 'old_print_sheet_no'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('分色单号', null=True, blank=True, max_length=20)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_lysheet_no=models.CharField('来样单号', null=True, blank=True, max_length=50)
    old_lydetail_no=models.CharField('来样明细单号', null=True, blank=True, max_length=50)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=10)
    old_detail_customer=models.CharField('明细客户', null=True, blank=True, max_length=100)
    old_gray_id=models.CharField('本厂规格', null=True, blank=True, max_length=20)
    old_screen_type=models.CharField('网版类型', null=True, blank=True, max_length=20)
    old_original_no=models.CharField('原稿编号', null=True, blank=True, max_length=50)
    old_print_code=models.CharField('花号', null=True, blank=True, max_length=50)
    old_print_name=models.CharField('花名', null=True, blank=True, max_length=50)
    old_color_plate_count=models.IntegerField('色位个数', null=True, blank=True)
    old_film_piece=models.IntegerField('菲林张数', null=True, blank=True)
    old_film_size=models.CharField('菲林尺寸', null=True, blank=True, max_length=100)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('Revisions', null=True, blank=True)
    old_print_sheet_no=models.CharField('PrintSheetNo', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_printcolorseparate'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_ee33b46f6773b7c6')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（PrintColorSeparate，待确认）'
        ordering=["-id"]

class SourceDyePrintColorSeparateDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PrintColorSeparateDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'ColorPlateID': 'old_color_plate_id', 'ColorPlateName': 'old_color_plate_name', 'Note': 'old_note', 'ColorCount': 'old_color_count', 'DetailNo': 'old_detail_no'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_color_plate_id=models.CharField('色位组号', null=False, blank=True, max_length=10)
    old_color_plate_name=models.CharField('色位名称', null=True, blank=True, max_length=20)
    old_note=models.CharField('备注', null=True, blank=True, max_length=512)
    old_color_count=models.IntegerField('分色个数', null=True, blank=True)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_printcolorseparatedetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_81a8af898dee2e48'),models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no', 'old_color_plate_id'],name='src_70be4df516e7ed40')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（PrintColorSeparateDetail，待确认）'
        ordering=["-id"]

class SourceDyePrintColorSeparateRecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PrintColorSeparateRecord'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'ColorPlateID': 'old_color_plate_id', 'RowNo': 'old_row_no', 'ColorIndex': 'old_color_index', 'NetNo': 'old_net_no', 'NetKind': 'old_net_kind', 'ColorName': 'old_color_name', 'Rate': 'old_rate', 'Density': 'old_density', 'DetailNo': 'old_detail_no'}
    SOURCE_KEY=('SheetSeries', 'RowNo', 'DetailNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：PrintColorSeparateDetail', 'target': 'erp_sampling.SourceDyePrintColorSeparateDetail', 'source_fields': ['SheetSeries', 'DetailNo', 'ColorPlateID'], 'target_fields': ['SheetSeries', 'DetailNo', 'ColorPlateID'], 'evidence': ['原界面主从 PrintColorSeparateRecord → PrintColorSeparateDetail']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_color_plate_id=models.CharField('色位组号', null=False, blank=True, max_length=10)
    old_row_no=models.CharField('行号', null=False, blank=True, max_length=10)
    old_color_index=models.IntegerField('分色序号', null=True, blank=True)
    old_net_no=models.CharField('网号', null=True, blank=True, max_length=10)
    old_net_kind=models.CharField('网别', null=True, blank=True, max_length=10)
    old_color_name=models.CharField('颜色名', null=True, blank=True, max_length=100)
    old_rate=models.DecimalField('比例', null=True, blank=True, max_digits=8, decimal_places=4)
    old_density=models.CharField('密度', null=True, blank=True, max_length=100)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=50)
    source_parent_1=models.ForeignKey('erp_sampling.SourceDyePrintColorSeparateDetail', verbose_name='原关系：PrintColorSeparateDetail', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_printcolorseparaterecord'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_row_no', 'old_detail_no'],name='src_c0e61a719b2031ee')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（PrintColorSeparateRecord，待确认）'
        ordering=["-id"]

class SourceDyePrintingTest(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PrintingTest'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'PrintCode': 'old_print_code', 'ColorPlateCount': 'old_color_plate_count', 'ProdID': 'old_prod_id', 'CustomerID': 'old_customer_id', 'DetailCustomer': 'old_detail_customer', 'BeginDate': 'old_begin_date', 'EndDate': 'old_end_date', 'Sampler': 'old_sampler', 'SkillGrade': 'old_skill_grade', 'Remarks': 'old_remarks', 'DeptID': 'old_dept_id', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'RightStatus': 'old_right_status'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=50)
    old_sheet_no=models.CharField('配方单号', null=False, blank=True, max_length=50)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_print_code=models.CharField('花号', null=True, blank=True, max_length=50)
    old_color_plate_count=models.IntegerField('色位个数', null=True, blank=True)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=20)
    old_detail_customer=models.CharField('明细客户', null=True, blank=True, max_length=100)
    old_begin_date=models.DateTimeField('试样开始日期', null=True, blank=True)
    old_end_date=models.DateTimeField('试样结束日期', null=True, blank=True)
    old_sampler=models.CharField('试样员', null=True, blank=True, max_length=20)
    old_skill_grade=models.CharField('难易程度', null=True, blank=True, max_length=50)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=256)
    old_dept_id=models.CharField('部门', null=True, blank=True, max_length=10)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_printingtest'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_b81e3e3f6bd37f63')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（PrintingTest，待确认）'
        ordering=["-id"]

class SourceDyePrintingTestColor(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PrintingTestColor'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'WPSerialNumber': 'old_wpserial_number', 'SerialNumber': 'old_serial_number', 'ColorID': 'old_color_id', 'ColorName': 'old_color_name', 'Factor': 'old_factor', 'WaterValue': 'old_water_value', 'Note': 'old_note', 'IsSamePulp': 'old_is_same_pulp', 'PrintCode': 'old_print_code'}
    SOURCE_KEY=('SheetSeries', 'WPSerialNumber', 'SerialNumber')
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：PrintingTestDetail', 'target': 'erp_sampling.SourceDyePrintingTestDetail', 'source_fields': ['SheetSeries', 'WPSerialNumber'], 'target_fields': ['SheetSeries', 'WPSerialNumber'], 'evidence': ['原界面主从 PrintingTestColor → PrintingTestDetail']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=50)
    old_wpserial_number=models.IntegerField('色位序号', null=False, blank=False)
    old_serial_number=models.IntegerField('颜色序号', null=False, blank=False)
    old_color_id=models.CharField('颜色编号', null=True, blank=True, max_length=50)
    old_color_name=models.CharField('颜色名称', null=True, blank=True, max_length=50)
    old_factor=models.FloatField('Factor', null=True, blank=True)
    old_water_value=models.FloatField('WaterValue', null=True, blank=True)
    old_note=models.CharField('Note', null=True, blank=True, max_length=256)
    old_is_same_pulp=models.BooleanField('是否同浆', null=True, blank=True)
    old_print_code=models.CharField('PrintCode', null=True, blank=True, max_length=50)
    source_parent_1=models.ForeignKey('erp_sampling.SourceDyePrintingTestDetail', verbose_name='原关系：PrintingTestDetail', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_printingtestcolor'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_wpserial_number', 'old_serial_number'],name='src_cb8fe1b2a50f966a')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（PrintingTestColor，待确认）'
        ordering=["-id"]

class SourceDyePrintingTestDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PrintingTestDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'WPSerialNumber': 'old_wpserial_number', 'SampleSign': 'old_sample_sign', 'MaterialType': 'old_material_type', 'MachineCode': 'old_machine_code', 'Note': 'old_note', 'MaterialName': 'old_material_name', 'PrintCode': 'old_print_code', 'GroundColor': 'old_ground_color', 'ColorPlateID': 'old_color_plate_id', 'ColorPlateName': 'old_color_plate_name'}
    SOURCE_KEY=('SheetSeries', 'WPSerialNumber')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：PrintingTest', 'target': 'erp_sampling.SourceDyePrintingTest', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 PrintingTestDetail → PrintingTest']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=50)
    old_wpserial_number=models.IntegerField('色位序号', null=False, blank=False)
    old_sample_sign=models.CharField('色位标记', null=True, blank=True, max_length=32)
    old_material_type=models.CharField('材料类型', null=True, blank=True, max_length=32)
    old_machine_code=models.CharField('机台号', null=True, blank=True, max_length=32)
    old_note=models.CharField('备注', null=True, blank=True, max_length=256)
    old_material_name=models.CharField('糊料', null=True, blank=True, max_length=64)
    old_print_code=models.CharField('印花花号', null=True, blank=True, max_length=50)
    old_ground_color=models.CharField('底色', null=True, blank=True, max_length=64)
    old_color_plate_id=models.CharField('色位ID', null=True, blank=True, max_length=20)
    old_color_plate_name=models.CharField('色位名称', null=True, blank=True, max_length=20)
    source_parent_1=models.ForeignKey('erp_sampling.SourceDyePrintingTest', verbose_name='原关系：PrintingTest', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_printingtestdetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_wpserial_number'],name='src_0b44f34063b6a38f')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（PrintingTestDetail，待确认）'
        ordering=["-id"]

class SourceDyePrintingTestStuff(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PrintingTestStuff'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'WPSerialNumber': 'old_wpserial_number', 'SerialNumber': 'old_serial_number', 'ColorID': 'old_color_id', 'ColorName': 'old_color_name', 'DyeStuffSerialNumber': 'old_dye_stuff_serial_number', 'DyeStuffCode': 'old_dye_stuff_code', 'DyeStuffName': 'old_dye_stuff_name', 'Class': 'old_class', 'Ratio': 'old_ratio', 'RatioUnit': 'old_ratio_unit', 'Dosage': 'old_dosage', 'Unit': 'old_unit', 'IsSend': 'old_is_send', 'Send': 'old_send', 'DpCode': 'old_dp_code', 'OrderColorNumber': 'old_order_color_number', 'Note': 'old_note', 'detail_id': 'old_detail_id', 'PrintCode': 'old_print_code'}
    SOURCE_KEY=('SheetSeries', 'WPSerialNumber', 'SerialNumber', 'DyeStuffSerialNumber')
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：PrintingTestColor', 'target': 'erp_sampling.SourceDyePrintingTestColor', 'source_fields': ['SheetSeries', 'WPSerialNumber', 'SerialNumber'], 'target_fields': ['SheetSeries', 'WPSerialNumber', 'SerialNumber'], 'evidence': ['原界面主从 PrintingTestStuff → PrintingTestColor']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=50)
    old_wpserial_number=models.IntegerField('色位序号', null=False, blank=False)
    old_serial_number=models.IntegerField('颜色序号', null=False, blank=False)
    old_color_id=models.CharField('颜色编号', null=True, blank=True, max_length=50)
    old_color_name=models.CharField('颜色名称', null=True, blank=True, max_length=50)
    old_dye_stuff_serial_number=models.IntegerField('染化料序号', null=False, blank=False)
    old_dye_stuff_code=models.CharField('染化料编号', null=True, blank=True, max_length=50)
    old_dye_stuff_name=models.CharField('染化料名称', null=True, blank=True, max_length=100)
    old_class=models.CharField('类型', null=True, blank=True, max_length=64)
    old_ratio=models.FloatField('比例', null=True, blank=True)
    old_ratio_unit=models.CharField('比例单位', null=True, blank=True, max_length=8)
    old_dosage=models.FloatField('领用量', null=True, blank=True)
    old_unit=models.CharField('领用量单位', null=True, blank=True, max_length=50)
    old_is_send=models.BooleanField('IsSend', null=True, blank=True)
    old_send=models.CharField('Send', null=True, blank=True, max_length=8)
    old_dp_code=models.CharField('DpCode', null=True, blank=True, max_length=16)
    old_order_color_number=models.CharField('OrderColorNumber', null=True, blank=True, max_length=50)
    old_note=models.CharField('备注', null=True, blank=True, max_length=256)
    old_detail_id=models.CharField('detail_id', null=True, blank=True, max_length=20)
    old_print_code=models.CharField('花号', null=True, blank=True, max_length=50)
    source_parent_1=models.ForeignKey('erp_sampling.SourceDyePrintingTestColor', verbose_name='原关系：PrintingTestColor', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_printingteststuff'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_wpserial_number', 'old_serial_number', 'old_dye_stuff_serial_number'],name='src_994f2c729d90de07')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（PrintingTestStuff，待确认）'
        ordering=["-id"]

class SourceDyePrintLabAttach(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PrintLabAttach'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'RowNo': 'old_row_no', 'FileName': 'old_file_name', 'Description': 'old_description'}
    SOURCE_KEY=('SheetSeries', 'RowNo')
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_row_no=models.IntegerField('RowNo', null=False, blank=False)
    old_file_name=models.CharField('FileName', null=True, blank=True, max_length=100)
    old_description=models.CharField('Description', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_printlabattach'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_row_no'],name='src_d31aa10f5346fe61')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（PrintLabAttach，待确认）'
        ordering=["-id"]

class SourceDyePrintLabAtte(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PrintLabAtte'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'FieldType': 'old_field_type', 'AtteCode': 'old_atte_code', 'AtteValue': 'old_atte_value', 'Description': 'old_description'}
    SOURCE_KEY=('SheetSeries', 'FieldType', 'AtteCode')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_field_type=models.CharField('FieldType', null=False, blank=True, max_length=20)
    old_atte_code=models.CharField('AtteCode', null=False, blank=True, max_length=10)
    old_atte_value=models.CharField('AtteValue', null=True, blank=True, max_length=50)
    old_description=models.CharField('Description', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_printlabatte'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_field_type', 'old_atte_code'],name='src_c3604475e254b818')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（PrintLabAtte，待确认）'
        ordering=["-id"]

class SourceDyePrintLabMain(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PrintLabMain'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetKind': 'old_sheet_kind', 'SheetDate': 'old_sheet_date', 'SheetStatus': 'old_sheet_status', 'BusinessUnitID': 'old_business_unit_id', 'SalerID': 'old_saler_id', 'SalerGroupID': 'old_saler_group_id', 'CustomerID': 'old_customer_id', 'GetSampleDate': 'old_get_sample_date', 'ToBackSample': 'old_to_back_sample', 'DlvSampleDate': 'old_dlv_sample_date', 'IsSampleCharge': 'old_is_sample_charge', 'Linker': 'old_linker', 'LinkerInfo': 'old_linker_info', 'VerLight1ID': 'old_ver_light1_id', 'VerLight2ID': 'old_ver_light2_id', 'RightStatus': 'old_right_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'ProdID': 'old_prod_id', 'Spec': 'old_spec', 'DesignNo': 'old_design_no', 'Sets': 'old_sets', 'Price': 'old_price', 'StrikeOffFee': 'old_strike_off_fee', 'ShapeSource': 'old_shape_source', 'Film': 'old_film', 'PrintKind': 'old_print_kind', 'PrintSampleKind': 'old_print_sample_kind', 'Width': 'old_width', 'Weight': 'old_weight', 'DifficultyID': 'old_difficulty_id', 'ColorCards': 'old_color_cards', 'RedoReasonID': 'old_redo_reason_id', 'IsNeedDraw': 'old_is_need_draw', 'IsNeedStrike': 'old_is_need_strike', 'AlloterID': 'old_alloter_id', 'AllotTime': 'old_allot_time', 'Idea': 'old_idea', 'DrawerID': 'old_drawer_id', 'DrawedTime': 'old_drawed_time', 'CheckerID': 'old_checker_id', 'CheckedTime': 'old_checked_time', 'CheckResult': 'old_check_result', 'ShiftID': 'old_shift_id', 'StrikedTime': 'old_striked_time', 'SamplerID': 'old_sampler_id', 'SampleTime': 'old_sample_time', 'SampledTime': 'old_sampled_time', 'SampleAlloterID': 'old_sample_alloter_id', 'SampleAllotTime': 'old_sample_allot_time'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=20)
    old_sheet_kind=models.IntegerField('SheetKind', null=True, blank=True)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_sheet_status=models.IntegerField('SheetStatus', null=True, blank=True)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('SalerID', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('SalerGroupID', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=10)
    old_get_sample_date=models.DateTimeField('GetSampleDate', null=True, blank=True)
    old_to_back_sample=models.BooleanField('ToBackSample', null=True, blank=True)
    old_dlv_sample_date=models.DateTimeField('DlvSampleDate', null=True, blank=True)
    old_is_sample_charge=models.BooleanField('IsSampleCharge', null=True, blank=True)
    old_linker=models.CharField('Linker', null=True, blank=True, max_length=10)
    old_linker_info=models.CharField('LinkerInfo', null=True, blank=True, max_length=100)
    old_ver_light1_id=models.CharField('VerLight1ID', null=True, blank=True, max_length=10)
    old_ver_light2_id=models.CharField('VerLight2ID', null=True, blank=True, max_length=10)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_print_times=models.IntegerField('PrintTimes', null=True, blank=True)
    old_revisions=models.IntegerField('Revisions', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_prod_id=models.CharField('ProdID', null=True, blank=True, max_length=20)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=128)
    old_design_no=models.CharField('DesignNo', null=True, blank=True, max_length=50)
    old_sets=models.IntegerField('Sets', null=True, blank=True)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=8, decimal_places=2)
    old_strike_off_fee=models.DecimalField('StrikeOffFee', null=True, blank=True, max_digits=10, decimal_places=2)
    old_shape_source=models.CharField('ShapeSource', null=True, blank=True, max_length=2)
    old_film=models.CharField('Film', null=True, blank=True, max_length=2)
    old_print_kind=models.CharField('PrintKind', null=True, blank=True, max_length=2)
    old_print_sample_kind=models.CharField('PrintSampleKind', null=True, blank=True, max_length=2)
    old_width=models.DecimalField('Width', null=True, blank=True, max_digits=6, decimal_places=2)
    old_weight=models.DecimalField('Weight', null=True, blank=True, max_digits=6, decimal_places=2)
    old_difficulty_id=models.CharField('DifficultyID', null=True, blank=True, max_length=10)
    old_color_cards=models.IntegerField('ColorCards', null=True, blank=True)
    old_redo_reason_id=models.CharField('RedoReasonID', null=True, blank=True, max_length=10)
    old_is_need_draw=models.BooleanField('IsNeedDraw', null=True, blank=True)
    old_is_need_strike=models.BooleanField('IsNeedStrike', null=True, blank=True)
    old_alloter_id=models.CharField('AlloterID', null=True, blank=True, max_length=10)
    old_allot_time=models.DateTimeField('AllotTime', null=True, blank=True)
    old_idea=models.TextField('Idea', null=True, blank=True)
    old_drawer_id=models.CharField('DrawerID', null=True, blank=True, max_length=10)
    old_drawed_time=models.DateTimeField('DrawedTime', null=True, blank=True)
    old_checker_id=models.CharField('CheckerID', null=True, blank=True, max_length=10)
    old_checked_time=models.DateTimeField('CheckedTime', null=True, blank=True)
    old_check_result=models.CharField('CheckResult', null=True, blank=True, max_length=100)
    old_shift_id=models.CharField('ShiftID', null=True, blank=True, max_length=10)
    old_striked_time=models.DateTimeField('StrikedTime', null=True, blank=True)
    old_sampler_id=models.CharField('SamplerID', null=True, blank=True, max_length=10)
    old_sample_time=models.DateTimeField('SampleTime', null=True, blank=True)
    old_sampled_time=models.DateTimeField('SampledTime', null=True, blank=True)
    old_sample_alloter_id=models.CharField('SampleAlloterID', null=True, blank=True, max_length=10)
    old_sample_allot_time=models.DateTimeField('SampleAllotTime', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_printlabmain'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_fa50c0f3e9881184')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（PrintLabMain，待确认）'
        ordering=["-id"]

class SourceDyePrintRecipe(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PrintRecipe'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetKind': 'old_sheet_kind', 'SheetType': 'old_sheet_type', 'SheetDate': 'old_sheet_date', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'DeptID': 'old_dept_id', 'ProdID': 'old_prod_id', 'Spec': 'old_spec', 'Cost': 'old_cost', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'BusinessUnitID': 'old_business_unit_id', 'CustomerID': 'old_customer_id', 'SalerID': 'old_saler_id', 'DesignNo': 'old_design_no', 'LabSheetNo': 'old_lab_sheet_no', 'ColorSeries': 'old_color_series', 'ColorID': 'old_color_id', 'ColorE': 'old_color_e', 'OriRecipeSheetNo': 'old_ori_recipe_sheet_no', 'Weight': 'old_weight', 'Width': 'old_width', 'RecipePriceSource': 'old_recipe_price_source', 'CostUnit': 'old_cost_unit', 'CheckerID': 'old_checker_id', 'MakerID': 'old_maker_id', 'DifficultyID': 'old_difficulty_id', 'Colors': 'old_colors', 'ColorCards': 'old_color_cards'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=20)
    old_sheet_kind=models.IntegerField('SheetKind', null=True, blank=True)
    old_sheet_type=models.IntegerField('SheetType', null=True, blank=True)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_sheet_status=models.CharField('SheetStatus', null=True, blank=True, max_length=1)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_print_times=models.IntegerField('PrintTimes', null=True, blank=True)
    old_revisions=models.IntegerField('Revisions', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_dept_id=models.CharField('DeptID', null=True, blank=True, max_length=10)
    old_prod_id=models.CharField('ProdID', null=True, blank=True, max_length=20)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=128)
    old_cost=models.DecimalField('Cost', null=True, blank=True, max_digits=10, decimal_places=2)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('SalerID', null=True, blank=True, max_length=10)
    old_design_no=models.CharField('DesignNo', null=True, blank=True, max_length=50)
    old_lab_sheet_no=models.CharField('LabSheetNo', null=True, blank=True, max_length=20)
    old_color_series=models.CharField('ColorSeries', null=True, blank=True, max_length=20)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=20)
    old_color_e=models.CharField('ColorE', null=True, blank=True, max_length=20)
    old_ori_recipe_sheet_no=models.CharField('OriRecipeSheetNo', null=True, blank=True, max_length=20)
    old_weight=models.DecimalField('Weight', null=True, blank=True, max_digits=6, decimal_places=2)
    old_width=models.DecimalField('Width', null=True, blank=True, max_digits=6, decimal_places=2)
    old_recipe_price_source=models.IntegerField('RecipePriceSource', null=True, blank=True)
    old_cost_unit=models.CharField('CostUnit', null=True, blank=True, max_length=1)
    old_checker_id=models.CharField('CheckerID', null=True, blank=True, max_length=10)
    old_maker_id=models.CharField('MakerID', null=True, blank=True, max_length=10)
    old_difficulty_id=models.CharField('DifficultyID', null=True, blank=True, max_length=10)
    old_colors=models.IntegerField('Colors', null=True, blank=True)
    old_color_cards=models.IntegerField('ColorCards', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_printrecipe'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_fc9ff80947523c9a')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（PrintRecipe，待确认）'
        ordering=["-id"]

class SourceDyePrintRecipeColor(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PrintRecipeColor'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SequenceNo': 'old_sequence_no', 'ColorNo': 'old_color_no', 'PasteID': 'old_paste_id', 'Dosage': 'old_dosage', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('SheetSeries', 'SequenceNo')
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_sequence_no=models.BigIntegerField('SequenceNo', null=False, blank=False)
    old_color_no=models.CharField('ColorNo', null=True, blank=True, max_length=20)
    old_paste_id=models.CharField('PasteID', null=True, blank=True, max_length=10)
    old_dosage=models.DecimalField('Dosage', null=True, blank=True, max_digits=15, decimal_places=6)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_printrecipecolor'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_sequence_no'],name='src_6a48d9f5253dbddc')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（PrintRecipeColor，待确认）'
        ordering=["-id"]

class SourceDyePrintRecipeDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PrintRecipeDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SequenceNo': 'old_sequence_no', 'StuffNo': 'old_stuff_no', 'StuffID': 'old_stuff_id', 'Dosage': 'old_dosage', 'Price': 'old_price', 'Amount': 'old_amount', 'Unit': 'old_unit', 'DetailNote': 'old_detail_note'}
    SOURCE_KEY=('SheetSeries', 'SequenceNo', 'StuffNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_sequence_no=models.BigIntegerField('SequenceNo', null=False, blank=False)
    old_stuff_no=models.IntegerField('StuffNo', null=False, blank=False)
    old_stuff_id=models.CharField('StuffID', null=True, blank=True, max_length=10)
    old_dosage=models.DecimalField('Dosage', null=True, blank=True, max_digits=15, decimal_places=6)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=16, decimal_places=6)
    old_amount=models.DecimalField('Amount', null=True, blank=True, max_digits=10, decimal_places=2)
    old_unit=models.IntegerField('Unit', null=True, blank=True)
    old_detail_note=models.CharField('DetailNote', null=True, blank=True, max_length=256)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_printrecipedetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_sequence_no', 'old_stuff_no'],name='src_9c5b2e9fc2138e67')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（PrintRecipeDetail，待确认）'
        ordering=["-id"]

class SourceDyePTSampleRegist(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PTSampleRegist'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetKind': 'old_sheet_kind', 'SheetDate': 'old_sheet_date', 'SheetStatus': 'old_sheet_status', 'CustomerID': 'old_customer_id', 'DetailCustomer': 'old_detail_customer', 'PTCount': 'old_ptcount', 'TempletType': 'old_templet_type', 'MainLight': 'old_main_light', 'SecondaryLight': 'old_secondary_light', 'ColorMatchMethod': 'old_color_match_method', 'QualityStandard': 'old_quality_standard', 'TrackerID': 'old_tracker_id', 'GetSampleDate': 'old_get_sample_date', 'DlvSampleDate': 'old_dlv_sample_date', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'RightStatus': 'old_right_status', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('来样单号', null=True, blank=True, max_length=20)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=10)
    old_detail_customer=models.CharField('明细客户', null=True, blank=True, max_length=100)
    old_ptcount=models.IntegerField('花型个数', null=True, blank=True)
    old_templet_type=models.CharField('确版方式', null=True, blank=True, max_length=20)
    old_main_light=models.CharField('对色主光源', null=True, blank=True, max_length=100)
    old_secondary_light=models.CharField('对色副光源', null=True, blank=True, max_length=100)
    old_color_match_method=models.CharField('对色方法', null=True, blank=True, max_length=50)
    old_quality_standard=models.CharField('质量标准', null=True, blank=True, max_length=50)
    old_tracker_id=models.CharField('跟单员', null=True, blank=True, max_length=20)
    old_get_sample_date=models.DateTimeField('来样日期', null=True, blank=True)
    old_dlv_sample_date=models.DateTimeField('要求交样日期', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('Revisions', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_ptsampleregist'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_8e6a608a16b80cfb')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（PTSampleRegist，待确认）'
        ordering=["-id"]

class SourceDyePTSampleRegistAtte(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PTSampleRegistAtte'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'FieldType': 'old_field_type', 'AtteCode': 'old_atte_code', 'AtteValue': 'old_atte_value', 'Description': 'old_description'}
    SOURCE_KEY=('SheetSeries', 'FieldType', 'AtteCode')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：PTSampleRegist', 'target': 'erp_sampling.SourceDyePTSampleRegist', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 PTSampleRegistAtte → PTSampleRegist']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_field_type=models.CharField('基础数据类别', null=False, blank=True, max_length=20)
    old_atte_code=models.CharField('事项代码', null=False, blank=True, max_length=10)
    old_atte_value=models.CharField('事项内容', null=True, blank=True, max_length=50)
    old_description=models.CharField('描述', null=True, blank=True, max_length=100)
    source_parent_1=models.ForeignKey('erp_sampling.SourceDyePTSampleRegist', verbose_name='原关系：PTSampleRegist', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_ptsampleregistatte'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_field_type', 'old_atte_code'],name='src_d6a05af98d47ef5a')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（PTSampleRegistAtte，待确认）'
        ordering=["-id"]

class SourceDyePTSampleRegistDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PTSampleRegistDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'GrayID': 'old_gray_id', 'ColorPlateCount': 'old_color_plate_count', 'SampleKind': 'old_sample_kind', 'SampleSource': 'old_sample_source', 'ScreenType': 'old_screen_type', 'ColorMatchCategory': 'old_color_match_category', 'ColorMatchRequire': 'old_color_match_require', 'PlateCompany': 'old_plate_company', 'PlateCount': 'old_plate_count'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：PTSampleRegist', 'target': 'erp_sampling.SourceDyePTSampleRegist', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 PTSampleRegistDetail → PTSampleRegist']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=30)
    old_gray_id=models.CharField('本厂规格', null=True, blank=True, max_length=20)
    old_color_plate_count=models.IntegerField('色位个数', null=True, blank=True)
    old_sample_kind=models.CharField('来样类别', null=True, blank=True, max_length=10)
    old_sample_source=models.CharField('样纱来源', null=True, blank=True, max_length=100)
    old_screen_type=models.CharField('网版类型', null=True, blank=True, max_length=20)
    old_color_match_category=models.CharField('配色类别', null=True, blank=True, max_length=20)
    old_color_match_require=models.CharField('配色要求', null=True, blank=True, max_length=100)
    old_plate_company=models.CharField('制版公司', null=True, blank=True, max_length=100)
    old_plate_count=models.IntegerField('制版份数', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_sampling.SourceDyePTSampleRegist', verbose_name='原关系：PTSampleRegist', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_ptsampleregistdetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_36a84a4a7b555173')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（PTSampleRegistDetail，待确认）'
        ordering=["-id"]

class SourceDyeSampleChoice(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SampleChoice'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'BusinessUnitID': 'old_business_unit_id', 'DetailCustName': 'old_detail_cust_name', 'CustomerID': 'old_customer_id', 'SalerGroupID': 'old_saler_group_id', 'SalerID': 'old_saler_id', 'Linker': 'old_linker', 'LinkerInfo': 'old_linker_info', 'StockUnit': 'old_stock_unit', 'Description': 'old_description', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_sheet_kind=models.IntegerField('SheetKind', null=True, blank=True)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_detail_cust_name=models.CharField('DetailCustName', null=True, blank=True, max_length=500)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('SalerGroupID', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('SalerID', null=True, blank=True, max_length=10)
    old_linker=models.CharField('Linker', null=True, blank=True, max_length=10)
    old_linker_info=models.CharField('LinkerInfo', null=True, blank=True, max_length=100)
    old_stock_unit=models.IntegerField('StockUnit', null=True, blank=True)
    old_description=models.CharField('Description', null=True, blank=True, max_length=100)
    old_sheet_status=models.IntegerField('SheetStatus', null=True, blank=True)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_print_times=models.IntegerField('PrintTimes', null=True, blank=True)
    old_revisions=models.IntegerField('Revisions', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=100)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_samplechoice'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_375585c4fd63a86a')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（SampleChoice，待确认）'
        ordering=["-id"]

class SourceDyeSampleIn(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SampleIn'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'FactID': 'old_fact_id', 'SalerID': 'old_saler_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'BusinessUnitID': 'old_business_unit_id', 'SampleInKindID': 'old_sample_in_kind_id', 'StepNo': 'old_step_no'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_fact_id=models.CharField('工厂代码', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('业务员代码', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_sample_in_kind_id=models.CharField('样品入库分类', null=True, blank=True, max_length=10)
    old_step_no=models.IntegerField('工作流节点号', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_samplein'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_0c4a9847237bb561')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（SampleIn，待确认）'
        ordering=["-id"]

class SourceDyeSampleInDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SampleInDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'FabricID': 'old_fabric_id', 'ContractNo': 'old_contract_no', 'OrderNo': 'old_order_no', 'StorageUnitID': 'old_storage_unit_id', 'SampleKindID': 'old_sample_kind_id', 'Rolls': 'old_rolls', 'Qty': 'old_qty', 'Price': 'old_price', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：SampleIn', 'target': 'erp_sampling.SourceDyeSampleIn', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 SampleInDetail → SampleIn']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=20)
    old_fabric_id=models.CharField('客户规格', null=True, blank=True, max_length=10)
    old_contract_no=models.CharField('客户单号', null=True, blank=True, max_length=20)
    old_order_no=models.CharField('订单号', null=True, blank=True, max_length=20)
    old_storage_unit_id=models.CharField('仓位代码', null=True, blank=True, max_length=10)
    old_sample_kind_id=models.CharField('样品形式', null=True, blank=True, max_length=10)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_qty=models.DecimalField('数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('价格', null=True, blank=True, max_digits=5, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    source_parent_1=models.ForeignKey('erp_sampling.SourceDyeSampleIn', verbose_name='原关系：SampleIn', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_sampleindetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_bc8119117fd11ef4')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（SampleInDetail，待确认）'
        ordering=["-id"]

class SourceDyeSampleOut(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SampleOut'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'CustomerID': 'old_customer_id', 'SalerID': 'old_saler_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'ExpressSettleID': 'old_express_settle_id', 'ExpressCompanyID': 'old_express_company_id', 'ExpressFee': 'old_express_fee', 'ExpressNo': 'old_express_no', 'ExpressPhoneNo': 'old_express_phone_no', 'ExpressReceiver': 'old_express_receiver', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'BusinessUnitID': 'old_business_unit_id', 'SampleOutKindID': 'old_sample_out_kind_id', 'StepNo': 'old_step_no'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_customer_id=models.CharField('客户代码', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('业务员代码', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    old_express_settle_id=models.CharField('快递费结算方式', null=True, blank=True, max_length=10)
    old_express_company_id=models.CharField('快递公司代码', null=True, blank=True, max_length=10)
    old_express_fee=models.DecimalField('快递费用', null=True, blank=True, max_digits=5, decimal_places=2)
    old_express_no=models.CharField('快递单号', null=True, blank=True, max_length=50)
    old_express_phone_no=models.CharField('快递收件人电话', null=True, blank=True, max_length=50)
    old_express_receiver=models.CharField('快递收件人', null=True, blank=True, max_length=10)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_sample_out_kind_id=models.CharField('样品出库分类', null=True, blank=True, max_length=10)
    old_step_no=models.IntegerField('工作流节点号', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_sampleout'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_9cf5bef24ba0f3de')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（SampleOut，待确认）'
        ordering=["-id"]

class SourceDyeSampleOutDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SampleOutDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'FabricID': 'old_fabric_id', 'SampleKindID': 'old_sample_kind_id', 'StorageUnitID': 'old_storage_unit_id', 'Rolls': 'old_rolls', 'Qty': 'old_qty', 'Price': 'old_price', 'InDetailNo': 'old_in_detail_no', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：SampleOut', 'target': 'erp_sampling.SourceDyeSampleOut', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 SampleOutDetail → SampleOut']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单明细号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=20)
    old_fabric_id=models.CharField('客户规格', null=True, blank=True, max_length=10)
    old_sample_kind_id=models.CharField('样品形式', null=True, blank=True, max_length=10)
    old_storage_unit_id=models.CharField('仓位代码', null=True, blank=True, max_length=10)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_qty=models.DecimalField('数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('价格', null=True, blank=True, max_digits=5, decimal_places=2)
    old_in_detail_no=models.CharField('入库明细单号', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    source_parent_1=models.ForeignKey('erp_sampling.SourceDyeSampleOut', verbose_name='原关系：SampleOut', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_sampleoutdetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_2926881eb09bdde1')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（SampleOutDetail，待确认）'
        ordering=["-id"]

class SourceDyeSampleStockBook(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SampleStockBook'
    SOURCE_FIELDS={'BookNo': 'old_book_no', 'BookDate': 'old_book_date', 'BookKind': 'old_book_kind', 'BusinessUnitID': 'old_business_unit_id', 'SampleInOutKindID': 'old_sample_in_out_kind_id', 'SampleKindID': 'old_sample_kind_id', 'CustomerID': 'old_customer_id', 'SalerID': 'old_saler_id', 'StorageUnitIDs': 'old_storage_unit_ids', 'FabricID': 'old_fabric_id', 'SheetNo': 'old_sheet_no', 'DetailNo': 'old_detail_no', 'InQty': 'old_in_qty', 'OutQty': 'old_out_qty', 'Price': 'old_price', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('BookNo',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_book_date': ('literal', '1900-01-01'), 'old_book_kind': ('literal', 0), 'old_business_unit_id': ('literal', ''), 'old_sample_in_out_kind_id': ('literal', ''), 'old_sample_kind_id': ('literal', ''), 'old_customer_id': ('literal', ''), 'old_saler_id': ('literal', ''), 'old_storage_unit_ids': ('literal', ''), 'old_fabric_id': ('literal', ''), 'old_sheet_no': ('literal', ''), 'old_detail_no': ('literal', ''), 'old_in_qty': ('literal', 0), 'old_out_qty': ('literal', 0), 'old_price': ('literal', 0), 'old_remarks': ('literal', '')}
    SOURCE_IDENTITIES=('old_book_no',)
    old_book_no=models.BigIntegerField('BookNo', null=False, blank=False)
    old_book_date=models.DateTimeField('BookDate', null=True, blank=True)
    old_book_kind=models.IntegerField('BookKind', null=True, blank=True)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_sample_in_out_kind_id=models.CharField('SampleInOutKindID', null=True, blank=True, max_length=10)
    old_sample_kind_id=models.CharField('SampleKindID', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('SalerID', null=True, blank=True, max_length=10)
    old_storage_unit_ids=models.CharField('StorageUnitIDs', null=True, blank=True, max_length=100)
    old_fabric_id=models.CharField('FabricID', null=True, blank=True, max_length=10)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=True, blank=True, max_length=20)
    old_in_qty=models.DecimalField('InQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_out_qty=models.DecimalField('OutQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=5, decimal_places=2)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_samplestockbook'
        indexes=[models.Index(fields=['source_batch', 'old_book_no'],name='src_2df3c1f16a21fab7')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（SampleStockBook，待确认）'
        ordering=["-id"]

class SourceDyeSmpPrescriptEntry(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='Smp_PrescriptEntry'
    SOURCE_FIELDS={'FInterID': 'old_finter_id', 'FEntryID': 'old_fentry_id', 'FParentID': 'old_fparent_id', 'PhaseNo': 'old_phase_no', 'StuffNo': 'old_stuff_no', 'FItemID': 'old_fitem_id', 'FTechID': 'old_ftech_id', 'FTechUnit': 'old_ftech_unit', 'FRatioQty': 'old_fratio_qty', 'FRealRatioQty': 'old_freal_ratio_qty', 'FPrice': 'old_fprice', 'FAmount': 'old_famount', 'FCost': 'old_fcost', 'FNote': 'old_fnote', 'FBomEntryID': 'old_fbom_entry_id', 'FCalculateID': 'old_fcalculate_id', 'FRoutingRequest': 'old_frouting_request', 'FC_SW': 'old_fc_sw', 'FC_PZYL': 'old_fc_pzyl', 'FC_SWater': 'old_fc_swater', 'FC_PZYLI': 'old_fc_pzyli', 'FC_PHZ': 'old_fc_phz', 'FC_DDL': 'old_fc_ddl', 'FC_TIME': 'old_fc_time', 'FC_WD': 'old_fc_wd', 'FC_SB': 'old_fc_sb'}
    SOURCE_KEY=('FInterID', 'FEntryID', 'FParentID')
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_finter_id=models.IntegerField('FInterID', null=False, blank=False)
    old_fentry_id=models.IntegerField('FEntryID', null=False, blank=False)
    old_fparent_id=models.IntegerField('FParentID', null=False, blank=False)
    old_phase_no=models.IntegerField('PhaseNo', null=True, blank=True)
    old_stuff_no=models.IntegerField('StuffNo', null=True, blank=True)
    old_fitem_id=models.IntegerField('FItemID', null=True, blank=True)
    old_ftech_id=models.IntegerField('FTechID', null=True, blank=True)
    old_ftech_unit=models.CharField('FTechUnit', null=True, blank=True, max_length=30)
    old_fratio_qty=models.DecimalField('FRatioQty', null=True, blank=True, max_digits=28, decimal_places=10)
    old_freal_ratio_qty=models.DecimalField('FRealRatioQty', null=True, blank=True, max_digits=28, decimal_places=10)
    old_fprice=models.DecimalField('FPrice', null=True, blank=True, max_digits=28, decimal_places=10)
    old_famount=models.DecimalField('FAmount', null=True, blank=True, max_digits=28, decimal_places=10)
    old_fcost=models.DecimalField('FCost', null=True, blank=True, max_digits=28, decimal_places=10)
    old_fnote=models.CharField('FNote', null=True, blank=True, max_length=255)
    old_fbom_entry_id=models.IntegerField('FBomEntryID', null=True, blank=True)
    old_fcalculate_id=models.IntegerField('FCalculateID', null=True, blank=True)
    old_frouting_request=models.CharField('FRoutingRequest', null=True, blank=True, max_length=200)
    old_fc_sw=models.CharField('FC_SW', null=True, blank=True, max_length=50)
    old_fc_pzyl=models.CharField('FC_PZYL', null=True, blank=True, max_length=50)
    old_fc_swater=models.CharField('FC_SWater', null=True, blank=True, max_length=50)
    old_fc_pzyli=models.CharField('FC_PZYLI', null=True, blank=True, max_length=50)
    old_fc_phz=models.CharField('FC_PHZ', null=True, blank=True, max_length=50)
    old_fc_ddl=models.CharField('FC_DDL', null=True, blank=True, max_length=50)
    old_fc_time=models.CharField('FC_TIME', null=True, blank=True, max_length=50)
    old_fc_wd=models.CharField('FC_WD', null=True, blank=True, max_length=50)
    old_fc_sb=models.CharField('FC_SB', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_smp_prescriptentry'
        indexes=[models.Index(fields=['source_batch', 'old_finter_id', 'old_fentry_id', 'old_fparent_id'],name='src_dc5472c59355830c')]
        verbose_name=verbose_name_plural='其他或待确认相关表（Smp_PrescriptEntry，待确认）'
        ordering=["-id"]

class SourceDyeYeDye(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ye.dye'
    SOURCE_FIELDS={'TimeZoneID': 'old_time_zone_id', 'Name': 'old_name', 'SunStart': 'old_sun_start', 'SunEnd': 'old_sun_end', 'MonStart': 'old_mon_start', 'MonEnd': 'old_mon_end', 'TuesStart': 'old_tues_start', 'TuesEnd': 'old_tues_end', 'WedStart': 'old_wed_start', 'WedEnd': 'old_wed_end', 'ThursStart': 'old_thurs_start', 'ThursEnd': 'old_thurs_end', 'FriStart': 'old_fri_start', 'FriEnd': 'old_fri_end', 'SatStart': 'old_sat_start', 'SatEnd': 'old_sat_end'}
    SOURCE_KEY=('TimeZoneID',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_time_zone_id=models.IntegerField('TimeZoneID', null=False, blank=False)
    old_name=models.CharField('Name', null=True, blank=True, max_length=30)
    old_sun_start=models.DateTimeField('SunStart', null=True, blank=True)
    old_sun_end=models.DateTimeField('SunEnd', null=True, blank=True)
    old_mon_start=models.DateTimeField('MonStart', null=True, blank=True)
    old_mon_end=models.DateTimeField('MonEnd', null=True, blank=True)
    old_tues_start=models.DateTimeField('TuesStart', null=True, blank=True)
    old_tues_end=models.DateTimeField('TuesEnd', null=True, blank=True)
    old_wed_start=models.DateTimeField('WedStart', null=True, blank=True)
    old_wed_end=models.DateTimeField('WedEnd', null=True, blank=True)
    old_thurs_start=models.DateTimeField('ThursStart', null=True, blank=True)
    old_thurs_end=models.DateTimeField('ThursEnd', null=True, blank=True)
    old_fri_start=models.DateTimeField('FriStart', null=True, blank=True)
    old_fri_end=models.DateTimeField('FriEnd', null=True, blank=True)
    old_sat_start=models.DateTimeField('SatStart', null=True, blank=True)
    old_sat_end=models.DateTimeField('SatEnd', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_ye_dye'
        indexes=[models.Index(fields=['source_batch', 'old_time_zone_id'],name='src_c4da9d19456ad431')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（ye.dye，待确认）'
        ordering=["-id"]
