"""静态旧业务字段；由tools/legacy_models生成，逐表来源见source_catalog.json。"""
from django.db import models
from plugins.erp_base.source_documents import SourceRecord


class SourceDyeColorShiftEmp(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ColorShiftEmp'
    SOURCE_FIELDS={'JobSheetNo': 'old_job_sheet_no', 'ShiftID': 'old_shift_id', 'EmpID': 'old_emp_id', 'EffiRate': 'old_effi_rate', 'Remarks': 'old_remarks', 'ProcessID': 'old_process_id', 'WProcessNo': 'old_wprocess_no'}
    SOURCE_KEY=('JobSheetNo', 'ShiftID', 'EmpID', 'WProcessNo')
    SOURCE_DOCUMENT=True
    old_job_sheet_no=models.CharField('JobSheetNo', null=False, blank=True, max_length=50)
    old_shift_id=models.CharField('ShiftID', null=False, blank=True, max_length=10)
    old_emp_id=models.CharField('EmpID', null=False, blank=True, max_length=10)
    old_effi_rate=models.DecimalField('EffiRate', null=True, blank=True, max_digits=6, decimal_places=4)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_process_id=models.CharField('ProcessID', null=True, blank=True, max_length=10)
    old_wprocess_no=models.CharField('WProcessNo', null=False, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_colorshiftemp'
        indexes=[models.Index(fields=['source_batch', 'old_job_sheet_no', 'old_shift_id', 'old_emp_id', 'old_wprocess_no'],name='src_a27ee7b01040e612')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（ColorShiftEmp，待确认）'
        ordering=["-id"]

class SourceDyeDPWorkQty(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DP_WorkQty'
    SOURCE_FIELDS={'ID': 'old_id', 'EmpID': 'old_emp_id', 'EmpCode': 'old_emp_code', 'dtDate': 'old_dt_date', 'ShiftID': 'old_shift_id', 'YEARS': 'old_years', 'Qty': 'old_qty', 'WorkMoney': 'old_work_money', 'DeptID': 'old_dept_id', 'TDAY': 'old_tday', 'SumMoney': 'old_sum_money', 'ShiftName': 'old_shift_name'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=True
    old_id=models.CharField('ID', null=False, blank=True, max_length=50)
    old_emp_id=models.CharField('EmpID', null=True, blank=True, max_length=20)
    old_emp_code=models.CharField('EmpCode', null=True, blank=True, max_length=20)
    old_dt_date=models.CharField('dtDate', null=True, blank=True, max_length=10)
    old_shift_id=models.CharField('ShiftID', null=True, blank=True, max_length=32)
    old_years=models.CharField('YEARS', null=True, blank=True, max_length=7)
    old_qty=models.FloatField('Qty', null=True, blank=True)
    old_work_money=models.FloatField('WorkMoney', null=True, blank=True)
    old_dept_id=models.CharField('DeptID', null=True, blank=True, max_length=10)
    old_tday=models.CharField('TDAY', null=True, blank=True, max_length=10)
    old_sum_money=models.FloatField('SumMoney', null=True, blank=True)
    old_shift_name=models.CharField('ShiftName', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_dp_workqty'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_c1e4f5bcb989c428')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（DP_WorkQty，待确认）'
        ordering=["-id"]

class SourceDyeEEnergyDay(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='e_Energy_day'
    SOURCE_FIELDS={'ID': 'old_id', 'MeterID': 'old_meter_id', 'CurrDate': 'old_curr_date', 'EnergyKind': 'old_energy_kind', 'BeginReadQty': 'old_begin_read_qty', 'BeginReadTime': 'old_begin_read_time', 'BeginUpID': 'old_begin_up_id', 'EndReadQty': 'old_end_read_qty', 'EndReadTime': 'old_end_read_time', 'EndUpID': 'old_end_up_id', 'RealQty': 'old_real_qty', 'ActualQty': 'old_actual_qty', 'Price': 'old_price', 'Amount': 'old_amount', 'Day': 'old_day'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=True
    old_id=models.BigIntegerField('ID', null=False, blank=False)
    old_meter_id=models.CharField('MeterID', null=True, blank=True, max_length=20)
    old_curr_date=models.DateTimeField('CurrDate', null=True, blank=True)
    old_energy_kind=models.IntegerField('EnergyKind', null=True, blank=True)
    old_begin_read_qty=models.DecimalField('BeginReadQty', null=True, blank=True, max_digits=18, decimal_places=2)
    old_begin_read_time=models.DateTimeField('BeginReadTime', null=True, blank=True)
    old_begin_up_id=models.BigIntegerField('BeginUpID', null=True, blank=True)
    old_end_read_qty=models.DecimalField('EndReadQty', null=True, blank=True, max_digits=18, decimal_places=2)
    old_end_read_time=models.DateTimeField('EndReadTime', null=True, blank=True)
    old_end_up_id=models.BigIntegerField('EndUpID', null=True, blank=True)
    old_real_qty=models.DecimalField('RealQty', null=True, blank=True, max_digits=18, decimal_places=2)
    old_actual_qty=models.DecimalField('ActualQty', null=True, blank=True, max_digits=18, decimal_places=2)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=8, decimal_places=2)
    old_amount=models.DecimalField('Amount', null=True, blank=True, max_digits=18, decimal_places=2)
    old_day=models.CharField('Day', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_e_energy_day'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_2f526884e3c091bf')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（e_Energy_day，待确认）'
        ordering=["-id"]

class SourceDyeEYardMeterGether(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='e_YardMeterGether'
    SOURCE_FIELDS={'ID': 'old_id', 'MachineID': 'old_machine_id', 'MeterID': 'old_meter_id', 'StartTime': 'old_start_time', 'EndTime': 'old_end_time', 'ReadLength': 'old_read_length', 'DoneLength': 'old_done_length', 'LastLength': 'old_last_length', 'Status': 'old_status', 'JobSheetSeries': 'old_job_sheet_series', 'ProcessNo': 'old_process_no'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=True
    old_id=models.CharField('编号', null=False, blank=True, max_length=50)
    old_machine_id=models.CharField('机台', null=True, blank=True, max_length=20)
    old_meter_id=models.CharField('码表', null=True, blank=True, max_length=10)
    old_start_time=models.DateTimeField('开始时间', null=True, blank=True)
    old_end_time=models.DateTimeField('结束时间', null=True, blank=True)
    old_read_length=models.DecimalField('读取长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_done_length=models.DecimalField('已用长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_last_length=models.DecimalField('剩余长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_status=models.IntegerField('状态', null=True, blank=True)
    old_job_sheet_series=models.CharField('工卡流水', null=True, blank=True, max_length=20)
    old_process_no=models.IntegerField('工序号', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_e_yardmetergether'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_8c2d656e295c217c')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（e_YardMeterGether，待确认）'
        ordering=["-id"]

class SourceDyeEmpShiftClock(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='EmpShiftClock'
    SOURCE_FIELDS={'EmpID': 'old_emp_id', 'dtDate': 'old_dt_date', 'ShiftID': 'old_shift_id', 'BeginTime': 'old_begin_time', 'EndTime': 'old_end_time', 'IsHoliday': 'old_is_holiday', 'ShiftName': 'old_shift_name', 'CopyClassID': 'old_copy_class_id', 'BeginLeaveTime': 'old_begin_leave_time', 'EndLeaveTime': 'old_end_leave_time', 'IsLeave': 'old_is_leave', 'DeptID': 'old_dept_id'}
    SOURCE_KEY=('EmpID', 'dtDate')
    SOURCE_DOCUMENT=True
    old_emp_id=models.CharField('EmpID', null=False, blank=True, max_length=10)
    old_dt_date=models.DateField('dtDate', null=False, blank=False)
    old_shift_id=models.CharField('ShiftID', null=True, blank=True, max_length=10)
    old_begin_time=models.DateTimeField('BeginTime', null=True, blank=True)
    old_end_time=models.DateTimeField('EndTime', null=True, blank=True)
    old_is_holiday=models.CharField('IsHoliday', null=True, blank=True, max_length=10)
    old_shift_name=models.CharField('ShiftName', null=True, blank=True, max_length=10)
    old_copy_class_id=models.CharField('CopyClassID', null=True, blank=True, max_length=10)
    old_begin_leave_time=models.DateTimeField('BeginLeaveTime', null=True, blank=True)
    old_end_leave_time=models.DateTimeField('EndLeaveTime', null=True, blank=True)
    old_is_leave=models.IntegerField('IsLeave', null=True, blank=True)
    old_dept_id=models.CharField('DeptID', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_empshiftclock'
        indexes=[models.Index(fields=['source_batch', 'old_emp_id', 'old_dt_date'],name='src_044af983c1786ed3')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（EmpShiftClock，待确认）'
        ordering=["-id"]

class SourceDyeEnergyConsumption(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='EnergyConsumption'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Remarks': 'old_remarks', 'StepNo': 'old_step_no', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('单号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('日期', null=True, blank=True)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_step_no=models.IntegerField('节点号', null=True, blank=True)
    old_creater=models.CharField('制单人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('制单时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_energyconsumption'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_68e192410ce0cbc8')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（EnergyConsumption，待确认）'
        ordering=["-id"]

class SourceDyeEnergyConsumptionDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='EnergyConsumptionDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'EnergyTableID': 'old_energy_table_id', 'UseQty': 'old_use_qty', 'LastReadQty': 'old_last_read_qty', 'ThisReadQty': 'old_this_read_qty', 'Price': 'old_price', 'Amount': 'old_amount', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    old_sheet_series=models.CharField('流水号', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('明细号', null=False, blank=True, max_length=36)
    old_energy_table_id=models.CharField('能源表', null=True, blank=True, max_length=20)
    old_use_qty=models.DecimalField('用量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_last_read_qty=models.DecimalField('上次读数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_this_read_qty=models.DecimalField('本次读数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=6, decimal_places=2)
    old_amount=models.DecimalField('金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeEnergyConsumption', verbose_name='原关系：EnergyConsumption', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_energyconsumptiondetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_ba4fdd6b6bfead26')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（EnergyConsumptionDetail，待确认）'
        ordering=["-id"]

class SourceDyeEnergyRecords(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='EnergyRecords'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'WaterRecords': 'old_water_records', 'ElectricRecords': 'old_electric_records', 'GasRecords': 'old_gas_records', 'Value1Records': 'old_value1_records', 'Value2Records': 'old_value2_records', 'Value3Records': 'old_value3_records', 'Creater': 'old_creater', 'CreaterDate': 'old_creater_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=False
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('记录单号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('记录日期', null=True, blank=True)
    old_water_records=models.FloatField('水表记录', null=True, blank=True)
    old_electric_records=models.FloatField('电表记录', null=True, blank=True)
    old_gas_records=models.FloatField('气表记录', null=True, blank=True)
    old_value1_records=models.FloatField('Value1Records', null=True, blank=True)
    old_value2_records=models.FloatField('Value2Records', null=True, blank=True)
    old_value3_records=models.FloatField('Value3Records', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_creater_date=models.DateTimeField('创建日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_energyrecords'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_2a775aeaebec3a1e')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（EnergyRecords，待确认）'
        ordering=["-id"]

class SourceDyeGetClothNotice(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GetClothNotice'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetKind': 'old_sheet_kind', 'SheetDate': 'old_sheet_date', 'Driver': 'old_driver', 'LicensePlate': 'old_license_plate', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'RightStatus': 'old_right_status', 'SheetStatus': 'old_sheet_status'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单号', null=False, blank=True, max_length=20)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_driver=models.CharField('收货司机', null=True, blank=True, max_length=20)
    old_license_plate=models.CharField('车牌号', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('审核日期', null=True, blank=True)
    old_right_status=models.IntegerField('单据状态', null=True, blank=True)
    old_sheet_status=models.IntegerField('SheetStatus', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_getclothnotice'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_e5887a5af2edfad4')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（GetClothNotice，待确认）'
        ordering=["-id"]

class SourceDyeGetClothNoticeDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GetClothNoticeDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'CustomerID': 'old_customer_id', 'AddrDlv': 'old_addr_dlv', 'ProdID': 'old_prod_id', 'Rolls': 'old_rolls', 'ReceivingType': 'old_receiving_type', 'ReceivingDate': 'old_receiving_date', 'ReceivingRolls': 'old_receiving_rolls', 'ReceivingPeople': 'old_receiving_people', 'Remarks': 'old_remarks', 'ClothGetDetailNo': 'old_cloth_get_detail_no'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    old_sheet_series=models.CharField('表单号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=20)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=20)
    old_addr_dlv=models.CharField('织纱厂/地址', null=True, blank=True, max_length=512)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=200)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_receiving_type=models.CharField('收货状态', null=True, blank=True, max_length=20)
    old_receiving_date=models.DateTimeField('收货时间', null=True, blank=True)
    old_receiving_rolls=models.DecimalField('收货条数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_receiving_people=models.CharField('收货人', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_cloth_get_detail_no=models.CharField('胚纱收单明细单号', null=True, blank=True, max_length=50)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeGetClothNotice', verbose_name='原关系：GetClothNotice', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_getclothnoticedetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_470b04b931e4f4ae')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（GetClothNoticeDetail，待确认）'
        ordering=["-id"]

class SourceDyeGrayReturnApply(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayReturnApply'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Remarks': 'old_remarks', 'StepNo': 'old_step_no', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=30)
    old_sheet_no=models.CharField('表单号', null=True, blank=True, max_length=30)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类别', null=True, blank=True)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_step_no=models.IntegerField('节点号', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_grayreturnapply'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_0ed901d9b7451455')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（GrayReturnApply，待确认）'
        ordering=["-id"]

class SourceDyeGrayReturnApplyDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayReturnApplyDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'CustomerID': 'old_customer_id', 'ReceSheetNo': 'old_rece_sheet_no', 'InSheetNo': 'old_in_sheet_no', 'LotNo': 'old_lot_no', 'Rolls': 'old_rolls', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    old_sheet_series=models.CharField('表单号', null=False, blank=True, max_length=30)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=30)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=30)
    old_rece_sheet_no=models.CharField('入库明细号', null=True, blank=True, max_length=30)
    old_in_sheet_no=models.CharField('入库单号', null=True, blank=True, max_length=30)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=100)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_length_qty=models.DecimalField('长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=2)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeGrayReturnApply', verbose_name='原关系：GrayReturnApply', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_grayreturnapplydetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_f0982097a96eb16e')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（GrayReturnApplyDetail，待确认）'
        ordering=["-id"]

class SourceDyeHSJobsheetNo(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='HS_JobsheetNo'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'JobsheetNo': 'old_jobsheet_no', 'HS_Code': 'old_hs_code', 'DE_Ption': 'old_de_ption', 'HS_Price': 'old_hs_price', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('单号', null=False, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('日期', null=True, blank=True)
    old_jobsheet_no=models.CharField('缸号', null=True, blank=True, max_length=200)
    old_hs_code=models.CharField('商品报关编码', null=True, blank=True, max_length=200)
    old_de_ption=models.CharField('货物品名', null=True, blank=True, max_length=200)
    old_hs_price=models.DecimalField('单价', null=True, blank=True, max_digits=10, decimal_places=4)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_hs_jobsheetno'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_b98b1d445250aaf1')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（HS_JobsheetNo，待确认）'
        ordering=["-id"]

class SourceDyeJingShaRegister(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='JingShaRegister'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'JobSheetNo': 'old_job_sheet_no', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'RightStatus': 'old_right_status'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=50)
    old_sheet_no=models.CharField('表单号', null=True, blank=True, max_length=50)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=50)
    old_prod_id=models.CharField('品名', null=True, blank=True, max_length=50)
    old_job_sheet_no=models.CharField('主卡缸号', null=True, blank=True, max_length=50)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=500)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=10)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_jingsharegister'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_c82db24fa8532b27')]
        verbose_name=verbose_name_plural='其他或待确认相关表（JingShaRegister，待确认）'
        ordering=["-id"]

class SourceDyeJingShaRegisterDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='JingShaRegisterDetail'
    SOURCE_FIELDS={'Sheetseries': 'old_sheetseries', 'DetailNo': 'old_detail_no', 'CustomerID': 'old_customer_id', 'JobSheetNo': 'old_job_sheet_no', 'ProdID': 'old_prod_id', 'ColorNum': 'old_color_num', 'ColorID': 'old_color_id', 'LotNo': 'old_lot_no', 'OrderQty': 'old_order_qty', 'Qty': 'old_qty', 'Rolls': 'old_rolls', 'Area': 'old_area', 'CustSelfNo': 'old_cust_self_no', 'ContractNo': 'old_contract_no', 'CustFabricName': 'old_cust_fabric_name', 'SumAssignedRolls': 'old_sum_assigned_rolls', 'SumAssignedWeightQty': 'old_sum_assigned_weight_qty', 'ColorRemarks': 'old_color_remarks', 'Remarks': 'old_remarks', 'DyeDate': 'old_dye_date', 'OrderSheetDate': 'old_order_sheet_date', 'DetailCustName': 'old_detail_cust_name', 'FenTou': 'old_fen_tou', 'RightStatus': 'old_right_status', 'SheetStatus': 'old_sheet_status', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    old_sheetseries=models.CharField('表单号', null=False, blank=True, max_length=50)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=50)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=30)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=30)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=30)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=30)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=30)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=50)
    old_order_qty=models.DecimalField('订单数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_qty=models.DecimalField('数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_area=models.CharField('区域', null=True, blank=True, max_length=100)
    old_cust_self_no=models.CharField('制单号', null=True, blank=True, max_length=100)
    old_contract_no=models.CharField('客户单号', null=True, blank=True, max_length=500)
    old_cust_fabric_name=models.CharField('客户规格', null=True, blank=True, max_length=250)
    old_sum_assigned_rolls=models.DecimalField('实际粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_sum_assigned_weight_qty=models.DecimalField('实际重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_color_remarks=models.CharField('用途', null=True, blank=True, max_length=500)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=1000)
    old_dye_date=models.CharField('络筒期', null=True, blank=True, max_length=100)
    old_order_sheet_date=models.DateTimeField('落单日期', null=True, blank=True)
    old_detail_cust_name=models.CharField('明细客户', null=True, blank=True, max_length=500)
    old_fen_tou=models.CharField('FenTou', null=True, blank=True, max_length=50)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=30)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=30)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_jingsharegisterdetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_d803bdc6e5b57f1b')]
        verbose_name=verbose_name_plural='其他或待确认相关表（JingShaRegisterDetail，待确认）'
        ordering=["-id"]

class SourceDyeJobAssign(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='JobAssign'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'AssignNo': 'old_assign_no', 'AssignDate': 'old_assign_date', 'ReceSheetNo': 'old_rece_sheet_no', 'SupplierID': 'old_supplier_id', 'GrayID': 'old_gray_id', 'LotNo': 'old_lot_no', 'Spec': 'old_spec', 'Rolls': 'old_rolls', 'Packs': 'old_packs', 'PCS': 'old_pcs', 'FixedQty': 'old_fixed_qty', 'StorageUnitID': 'old_storage_unit_id', 'RollAvgQty': 'old_roll_avg_qty', 'Remarks': 'old_remarks', 'IsChecked': 'old_is_checked', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'MachineID': 'old_machine_id', 'DetailsCustomer': 'old_details_customer', 'PreField1': 'old_pre_field1', 'PreField2': 'old_pre_field2', 'PreField3': 'old_pre_field3', 'PreField4': 'old_pre_field4', 'PreField5': 'old_pre_field5', 'Status': 'old_status', 'Area': 'old_area', 'InSheetDate': 'old_in_sheet_date', 'Semi_Owner': 'old_semi_owner', 'WareHouseID': 'old_ware_house_id', 'InSheetKind': 'old_in_sheet_kind', 'ColorID': 'old_color_id', 'PurchaseOrders': 'old_purchase_orders', 'A_A': 'old_a_a', 'A_B': 'old_a_b'}
    SOURCE_KEY=('SheetSeries', 'AssignNo')
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_assign_no=models.IntegerField('预配顺序号', null=False, blank=False)
    old_assign_date=models.DateTimeField('预配日期', null=True, blank=True)
    old_rece_sheet_no=models.CharField('入库明细号', null=True, blank=True, max_length=20)
    old_supplier_id=models.CharField('供应商', null=True, blank=True, max_length=30)
    old_gray_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_lot_no=models.TextField('批号', null=True, blank=True)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=128)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_packs=models.DecimalField('件数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_pcs=models.IntegerField('粒/件', null=True, blank=True)
    old_fixed_qty=models.DecimalField('锭重', null=True, blank=True, max_digits=5, decimal_places=2)
    old_storage_unit_id=models.CharField('仓位', null=True, blank=True, max_length=100)
    old_roll_avg_qty=models.DecimalField('平均粒长\\粒重', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_is_checked=models.BooleanField('检测', null=True, blank=True)
    old_length_qty=models.DecimalField('长度数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('重量数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_machine_id=models.CharField('机号', null=True, blank=True, max_length=100)
    old_details_customer=models.CharField('织厂', null=True, blank=True, max_length=10)
    old_pre_field1=models.TextField('捻度(H/S)', null=True, blank=True)
    old_pre_field2=models.TextField('氨纶', null=True, blank=True)
    old_pre_field3=models.TextField('针数', null=True, blank=True)
    old_pre_field4=models.TextField('寸数', null=True, blank=True)
    old_pre_field5=models.TextField('车架', null=True, blank=True)
    old_status=models.IntegerField('实配状态', null=True, blank=True)
    old_area=models.CharField('区域', null=True, blank=True, max_length=100)
    old_in_sheet_date=models.DateTimeField('入库日期', null=True, blank=True)
    old_semi_owner=models.CharField('半成品所有者', null=True, blank=True, max_length=30)
    old_ware_house_id=models.CharField('仓库', null=True, blank=True, max_length=30)
    old_in_sheet_kind=models.CharField('物料分类', null=True, blank=True, max_length=20)
    old_color_id=models.CharField('物料颜色', null=True, blank=True, max_length=20)
    old_purchase_orders=models.CharField('采购单号', null=True, blank=True, max_length=20)
    old_a_a=models.CharField('物料区域', null=True, blank=True, max_length=50)
    old_a_b=models.CharField('物料等级', null=True, blank=True, max_length=100)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeJobSheet', verbose_name='原关系：JobSheet', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_jobassign'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_assign_no'],name='src_ab619a4bb91f9883')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（JobAssign，待确认）'
        ordering=["-id"]

class SourceDyeJobAtte(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='JobAtte'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'FieldType': 'old_field_type', 'AtteCode': 'old_atte_code', 'AtteValue': 'old_atte_value', 'Description': 'old_description', 'Price': 'old_price', 'PriceUnit': 'old_price_unit'}
    SOURCE_KEY=('SheetSeries', 'FieldType', 'AtteCode')
    SOURCE_DOCUMENT=False
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_field_type=models.CharField('基础数据类别', null=False, blank=True, max_length=20)
    old_atte_code=models.CharField('事项代码', null=False, blank=True, max_length=10)
    old_atte_value=models.CharField('事项内容', null=True, blank=True, max_length=500)
    old_description=models.CharField('描述', null=True, blank=True, max_length=500)
    old_price=models.DecimalField('价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_price_unit=models.IntegerField('单位', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeJobSheet', verbose_name='原关系：JobSheet', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_jobatte'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_field_type', 'old_atte_code'],name='src_a26e5b98cb4f5b39')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（JobAtte，待确认）'
        ordering=["-id"]

class SourceDyeJobColor(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='JobColor'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'JobDetailNo': 'old_job_detail_no', 'CheckNo': 'old_check_no', 'FabricID': 'old_fabric_id', 'Spec': 'old_spec', 'Structure': 'old_structure', 'ColorID': 'old_color_id', 'ColorE': 'old_color_e', 'ColorNum': 'old_color_num', 'DesignNo': 'old_design_no', 'WidthDn': 'old_width_dn', 'WidthUp': 'old_width_up', 'WidthKindID': 'old_width_kind_id', 'WeightDn': 'old_weight_dn', 'WeightUp': 'old_weight_up', 'WeightUnit': 'old_weight_unit', 'ProdWeight': 'old_prod_weight', 'GrayRolls': 'old_gray_rolls', 'GrayQty': 'old_gray_qty', 'ProdQty': 'old_prod_qty', 'Price': 'old_price', 'IsTaxPrice': 'old_is_tax_price', 'Fee': 'old_fee', 'Amount': 'old_amount', 'DlvQty': 'old_dlv_qty', 'DlvRolls': 'old_dlv_rolls', 'DlvDate': 'old_dlv_date', 'ToPlace': 'old_to_place', 'RealGrayQty': 'old_real_gray_qty', 'RealLoss': 'old_real_loss', 'RealProdQty': 'old_real_prod_qty', 'Remarks': 'old_remarks', 'RealGrayPrice': 'old_real_gray_price', 'RealGrayMoney': 'old_real_gray_money', 'RealJobPrice': 'old_real_job_price', 'RealJobMoney': 'old_real_job_money', 'RealProfit': 'old_real_profit', 'OrderMoney': 'old_order_money'}
    SOURCE_KEY=('JobDetailNo',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_job_detail_no=models.CharField('JobDetailNo', null=False, blank=True, max_length=20)
    old_check_no=models.CharField('CheckNo', null=True, blank=True, max_length=20)
    old_fabric_id=models.CharField('FabricID', null=True, blank=True, max_length=10)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=50)
    old_structure=models.CharField('Structure', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=10)
    old_color_e=models.CharField('ColorE', null=True, blank=True, max_length=20)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=20)
    old_design_no=models.CharField('DesignNo', null=True, blank=True, max_length=20)
    old_width_dn=models.DecimalField('WidthDn', null=True, blank=True, max_digits=6, decimal_places=2)
    old_width_up=models.DecimalField('WidthUp', null=True, blank=True, max_digits=6, decimal_places=2)
    old_width_kind_id=models.CharField('WidthKindID', null=True, blank=True, max_length=10)
    old_weight_dn=models.DecimalField('WeightDn', null=True, blank=True, max_digits=6, decimal_places=2)
    old_weight_up=models.DecimalField('WeightUp', null=True, blank=True, max_digits=6, decimal_places=2)
    old_weight_unit=models.IntegerField('WeightUnit', null=True, blank=True)
    old_prod_weight=models.DecimalField('ProdWeight', null=True, blank=True, max_digits=6, decimal_places=2)
    old_gray_rolls=models.DecimalField('GrayRolls', null=True, blank=True, max_digits=7, decimal_places=2)
    old_gray_qty=models.DecimalField('GrayQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_prod_qty=models.DecimalField('ProdQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=5, decimal_places=2)
    old_is_tax_price=models.BooleanField('IsTaxPrice', null=True, blank=True)
    old_fee=models.DecimalField('Fee', null=True, blank=True, max_digits=10, decimal_places=2)
    old_amount=models.DecimalField('Amount', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dlv_qty=models.DecimalField('DlvQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dlv_rolls=models.DecimalField('DlvRolls', null=True, blank=True, max_digits=7, decimal_places=2)
    old_dlv_date=models.DateTimeField('DlvDate', null=True, blank=True)
    old_to_place=models.CharField('ToPlace', null=True, blank=True, max_length=50)
    old_real_gray_qty=models.DecimalField('RealGrayQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_loss=models.DecimalField('RealLoss', null=True, blank=True, max_digits=4, decimal_places=1)
    old_real_prod_qty=models.DecimalField('RealProdQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=100)
    old_real_gray_price=models.DecimalField('RealGrayPrice', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_gray_money=models.DecimalField('RealGrayMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_job_price=models.DecimalField('RealJobPrice', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_job_money=models.DecimalField('RealJobMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_profit=models.DecimalField('RealProfit', null=True, blank=True, max_digits=10, decimal_places=2)
    old_order_money=models.DecimalField('OrderMoney', null=True, blank=True, max_digits=10, decimal_places=2)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_jobcolor'
        indexes=[models.Index(fields=['source_batch', 'old_job_detail_no'],name='src_1cb10a8d01253979')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（JobColor，待确认）'
        ordering=["-id"]

class SourceDyeJobCombine(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='JobCombine'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'JobSheetNo': 'old_job_sheet_no', 'Remarks': 'old_remarks', 'Rolls': 'old_rolls', 'Qty': 'old_qty', 'CombineKind': 'old_combine_kind', 'CheckNo': 'old_check_no', 'RowNo': 'old_row_no'}
    SOURCE_KEY=('SheetSeries', 'JobSheetNo')
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('工卡流水', null=False, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('缸号', null=False, blank=True, max_length=50)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=300)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_qty=models.DecimalField('数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_combine_kind=models.IntegerField('合缸类别', null=True, blank=True)
    old_check_no=models.CharField('订单明细号', null=True, blank=True, max_length=30)
    old_row_no=models.CharField('行号', null=True, blank=True, max_length=20)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeJobSheet', verbose_name='原关系：JobSheet', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_jobcombine'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_job_sheet_no'],name='src_111f56dc7280a8e0')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（JobCombine，待确认）'
        ordering=["-id"]

class SourceDyeJobCombineOrder(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='JobCombineOrder'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'CheckNo': 'old_check_no', 'OrderSheetNo': 'old_order_sheet_no', 'CustomerID': 'old_customer_id', 'DetailCustName': 'old_detail_cust_name', 'CustSelfNo': 'old_cust_self_no', 'ContractNo': 'old_contract_no', 'ProdID': 'old_prod_id', 'CustFabricName': 'old_cust_fabric_name', 'ColorNum': 'old_color_num', 'ColorRemarks': 'old_color_remarks', 'CustSelfNoDetail': 'old_cust_self_no_detail', 'OrderQty': 'old_order_qty', 'LastQty': 'old_last_qty', 'CombineQty': 'old_combine_qty', 'IsMasterOrder': 'old_is_master_order', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('SheetSeries', 'CheckNo')
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('工卡流水号', null=False, blank=True, max_length=30)
    old_check_no=models.CharField('订单明细', null=False, blank=True, max_length=30)
    old_order_sheet_no=models.CharField('订单号', null=True, blank=True, max_length=30)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=20)
    old_detail_cust_name=models.CharField('明细客户', null=True, blank=True, max_length=50)
    old_cust_self_no=models.CharField('制单号', null=True, blank=True, max_length=30)
    old_contract_no=models.CharField('客户单号', null=True, blank=True, max_length=500)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_cust_fabric_name=models.CharField('客户规格', null=True, blank=True, max_length=250)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=50)
    old_color_remarks=models.CharField('用途', null=True, blank=True, max_length=500)
    old_cust_self_no_detail=models.CharField('客单号明细', null=True, blank=True, max_length=50)
    old_order_qty=models.DecimalField('订单数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_last_qty=models.DecimalField('未开卡数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_combine_qty=models.DecimalField('合染数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_is_master_order=models.BooleanField('是否主表订单', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeJobSheet', verbose_name='原关系：JobSheet', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_jobcombineorder'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_check_no'],name='src_8e96b9d0b67044e9')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（JobCombineOrder，待确认）'
        ordering=["-id"]

class SourceDyeJobExceptions(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='JobExceptions'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'RowNo': 'old_row_no', 'ProcessID': 'old_process_id', 'ProcessNo': 'old_process_no', 'DefectIDs': 'old_defect_ids', 'ExceptionMessage': 'old_exception_message', 'EmpID': 'old_emp_id', 'ShiftID': 'old_shift_id', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date'}
    SOURCE_KEY=('SheetSeries', 'RowNo')
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=50)
    old_row_no=models.IntegerField('RowNo', null=False, blank=False)
    old_process_id=models.CharField('ProcessID', null=True, blank=True, max_length=10)
    old_process_no=models.IntegerField('ProcessNo', null=True, blank=True)
    old_defect_ids=models.CharField('DefectIDs', null=True, blank=True, max_length=100)
    old_exception_message=models.CharField('ExceptionMessage', null=True, blank=True, max_length=200)
    old_emp_id=models.CharField('EmpID', null=True, blank=True, max_length=50)
    old_shift_id=models.CharField('ShiftID', null=True, blank=True, max_length=10)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeJobSheet', verbose_name='原关系：JobSheet', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_jobexceptions'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_row_no'],name='src_79a3a19504648f70')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（JobExceptions，待确认）'
        ordering=["-id"]

class SourceDyeJobGrayRecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='JobGrayRecord'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'ReceSheetNo': 'old_rece_sheet_no', 'RollNo': 'old_roll_no', 'GrayBarCode': 'old_gray_bar_code', 'AssignedNo': 'old_assigned_no', 'BarCode': 'old_bar_code', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'StorageUnitID': 'old_storage_unit_id', 'Status': 'old_status', 'Remarks': 'old_remarks', 'GUnit': 'old_gunit', 'Rolls': 'old_rolls', 'Kg': 'old_kg', 'Pound': 'old_pound'}
    SOURCE_KEY=('SheetSeries', 'ReceSheetNo', 'RollNo', 'GrayBarCode')
    SOURCE_DOCUMENT=False
    old_sheet_series=models.CharField('工卡流水号', null=False, blank=True, max_length=20)
    old_rece_sheet_no=models.CharField('入库明细号', null=False, blank=True, max_length=20)
    old_roll_no=models.CharField('箱号', null=False, blank=True, max_length=20)
    old_gray_bar_code=models.CharField('GrayBarCode', null=False, blank=True, max_length=50)
    old_assigned_no=models.CharField('投疋流水', null=True, blank=True, max_length=20)
    old_bar_code=models.CharField('条码', null=False, blank=True, max_length=50)
    old_length_qty=models.DecimalField('长度数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('重量数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_storage_unit_id=models.CharField('仓位代码', null=True, blank=True, max_length=10)
    old_status=models.CharField('状态', null=True, blank=True, max_length=10)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_gunit=models.IntegerField('GUnit', null=True, blank=True)
    old_rolls=models.FloatField('粒数', null=True, blank=True)
    old_kg=models.DecimalField('公斤', null=True, blank=True, max_digits=6, decimal_places=2)
    old_pound=models.DecimalField('磅数', null=True, blank=True, max_digits=6, decimal_places=2)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeJobSheet', verbose_name='原关系：JobSheet', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_jobgrayrecord'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_rece_sheet_no', 'old_roll_no', 'old_gray_bar_code'],name='src_6c2d91118563417a')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（JobGrayRecord，待确认）'
        ordering=["-id"]

class SourceDyeJobInWareEdit(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='JobInWareEdit'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'CustomerID': 'old_customer_id', 'JobSheetNo': 'old_job_sheet_no', 'ProdID': 'old_prod_id', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'Rolls': 'old_rolls', 'WeightQty': 'old_weight_qty', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=50)
    old_sheet_no=models.CharField('表单号', null=True, blank=True, max_length=36)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=30)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=40)
    old_prod_id=models.CharField('规格', null=True, blank=True, max_length=100)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=40)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=40)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_jobinwareedit'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_30a788f8ff6c0e50')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（JobInWareEdit，待确认）'
        ordering=["-id"]

class SourceDyeJobMain(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='JobMain'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'BusinessUnitID': 'old_business_unit_id', 'SheetKind': 'old_sheet_kind', 'FactID': 'old_fact_id', 'SalerGroupID': 'old_saler_group_id', 'Linker': 'old_linker', 'TrackerID': 'old_tracker_id', 'Loss': 'old_loss', 'RealLoss': 'old_real_loss', 'LossStr': 'old_loss_str', 'PriceUnit': 'old_price_unit', 'SettleID': 'old_settle_id', 'HandFeelID': 'old_hand_feel_id', 'VerLight1ID': 'old_ver_light1_id', 'VerLight2ID': 'old_ver_light2_id', 'SumDlvQty': 'old_sum_dlv_qty', 'SumDlvRolls': 'old_sum_dlv_rolls', 'DlvMannerID': 'old_dlv_manner_id', 'ProductionID': 'old_production_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'CloseTime': 'old_close_time', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'StepNo': 'old_step_no', 'LabelID': 'old_label_id'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('SheetNo', null=False, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_sheet_kind=models.IntegerField('SheetKind', null=True, blank=True)
    old_fact_id=models.CharField('FactID', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('SalerGroupID', null=True, blank=True, max_length=10)
    old_linker=models.CharField('Linker', null=True, blank=True, max_length=10)
    old_tracker_id=models.CharField('TrackerID', null=True, blank=True, max_length=10)
    old_loss=models.DecimalField('Loss', null=True, blank=True, max_digits=4, decimal_places=1)
    old_real_loss=models.DecimalField('RealLoss', null=True, blank=True, max_digits=4, decimal_places=1)
    old_loss_str=models.CharField('LossStr', null=True, blank=True, max_length=20)
    old_price_unit=models.IntegerField('PriceUnit', null=True, blank=True)
    old_settle_id=models.CharField('SettleID', null=True, blank=True, max_length=10)
    old_hand_feel_id=models.CharField('HandFeelID', null=True, blank=True, max_length=10)
    old_ver_light1_id=models.CharField('VerLight1ID', null=True, blank=True, max_length=10)
    old_ver_light2_id=models.CharField('VerLight2ID', null=True, blank=True, max_length=100)
    old_sum_dlv_qty=models.DecimalField('SumDlvQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sum_dlv_rolls=models.DecimalField('SumDlvRolls', null=True, blank=True, max_digits=7, decimal_places=2)
    old_dlv_manner_id=models.CharField('DlvMannerID', null=True, blank=True, max_length=10)
    old_production_id=models.CharField('ProductionID', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('SheetStatus', null=True, blank=True)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_print_times=models.IntegerField('PrintTimes', null=True, blank=True)
    old_close_time=models.DateTimeField('CloseTime', null=True, blank=True)
    old_revisions=models.IntegerField('Revisions', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=100)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_label_id=models.CharField('LabelID', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_jobmain'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_6ca319dec2e7635f')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（JobMain，待确认）'
        ordering=["-id"]

class SourceDyeJobOutWareEdit(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='JobOutWareEdit'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'InWareSheetNo': 'old_in_ware_sheet_no', 'CustomerID': 'old_customer_id', 'JobSheetNo': 'old_job_sheet_no', 'ProdID': 'old_prod_id', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'Rolls': 'old_rolls', 'WeightQty': 'old_weight_qty', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=50)
    old_sheet_no=models.CharField('表单号', null=True, blank=True, max_length=36)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_in_ware_sheet_no=models.CharField('进仓登记号', null=True, blank=True, max_length=40)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=30)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=40)
    old_prod_id=models.CharField('规格', null=True, blank=True, max_length=100)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=40)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=40)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_joboutwareedit'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_9148443b2bffe431')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（JobOutWareEdit，待确认）'
        ordering=["-id"]

class SourceDyeJobPreRegist(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='JobPreRegist'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'JobSheetNo': 'old_job_sheet_no', 'Rolls': 'old_rolls', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('SheetSeries', 'JobSheetNo')
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('工卡流水', null=False, blank=True, max_length=50)
    old_job_sheet_no=models.CharField('缸号', null=False, blank=True, max_length=20)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_length_qty=models.DecimalField('长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeJobSheet', verbose_name='原关系：JobSheet', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_jobpreregist'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_job_sheet_no'],name='src_0661e0c812fbab24')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（JobPreRegist，待确认）'
        ordering=["-id"]

class SourceDyeJobProcess(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='JobProcess'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'ProcessNo': 'old_process_no', 'ProcessID': 'old_process_id', 'StationID': 'old_station_id', 'PPName01': 'old_ppname01', 'TheoryValue01': 'old_theory_value01', 'ActualValue01': 'old_actual_value01', 'PPName02': 'old_ppname02', 'TheoryValue02': 'old_theory_value02', 'ActualValue02': 'old_actual_value02', 'PPName03': 'old_ppname03', 'TheoryValue03': 'old_theory_value03', 'ActualValue03': 'old_actual_value03', 'PPName04': 'old_ppname04', 'TheoryValue04': 'old_theory_value04', 'ActualValue04': 'old_actual_value04', 'PPName05': 'old_ppname05', 'TheoryValue05': 'old_theory_value05', 'ActualValue05': 'old_actual_value05', 'PPName06': 'old_ppname06', 'TheoryValue06': 'old_theory_value06', 'ActualValue06': 'old_actual_value06', 'PPName07': 'old_ppname07', 'TheoryValue07': 'old_theory_value07', 'ActualValue07': 'old_actual_value07', 'PPName08': 'old_ppname08', 'TheoryValue08': 'old_theory_value08', 'ActualValue08': 'old_actual_value08', 'PPName09': 'old_ppname09', 'TheoryValue09': 'old_theory_value09', 'ActualValue09': 'old_actual_value09', 'PPName10': 'old_ppname10', 'TheoryValue10': 'old_theory_value10', 'ActualValue10': 'old_actual_value10', 'PPName11': 'old_ppname11', 'TheoryValue11': 'old_theory_value11', 'ActualValue11': 'old_actual_value11', 'PPName12': 'old_ppname12', 'TheoryValue12': 'old_theory_value12', 'ActualValue12': 'old_actual_value12', 'PPName13': 'old_ppname13', 'TheoryValue13': 'old_theory_value13', 'ActualValue13': 'old_actual_value13', 'PPName14': 'old_ppname14', 'TheoryValue14': 'old_theory_value14', 'ActualValue14': 'old_actual_value14', 'PPName15': 'old_ppname15', 'TheoryValue15': 'old_theory_value15', 'ActualValue15': 'old_actual_value15', 'PPName16': 'old_ppname16', 'TheoryValue16': 'old_theory_value16', 'ActualValue16': 'old_actual_value16', 'PPName17': 'old_ppname17', 'TheoryValue17': 'old_theory_value17', 'ActualValue17': 'old_actual_value17', 'PPName18': 'old_ppname18', 'TheoryValue18': 'old_theory_value18', 'ActualValue18': 'old_actual_value18', 'PPName19': 'old_ppname19', 'TheoryValue19': 'old_theory_value19', 'ActualValue19': 'old_actual_value19', 'PPName20': 'old_ppname20', 'TheoryValue20': 'old_theory_value20', 'ActualValue20': 'old_actual_value20', 'MachineID': 'old_machine_id', 'VehicleNo': 'old_vehicle_no', 'StartTime': 'old_start_time', 'EndTime': 'old_end_time', 'WProcessNo': 'old_wprocess_no', 'Remarks': 'old_remarks', 'Status': 'old_status', 'Flag': 'old_flag', 'Place': 'old_place', 'LastTime': 'old_last_time', 'Price': 'old_price', 'PPPName01': 'old_pppname01', 'PValue01': 'old_pvalue01', 'PPPName02': 'old_pppname02', 'PValue02': 'old_pvalue02', 'PPPName03': 'old_pppname03', 'PValue03': 'old_pvalue03', 'PPPName04': 'old_pppname04', 'PValue04': 'old_pvalue04', 'PPPName05': 'old_pppname05', 'PValue05': 'old_pvalue05', 'PPPName06': 'old_pppname06', 'PValue06': 'old_pvalue06', 'PPPName07': 'old_pppname07', 'PValue07': 'old_pvalue07', 'PPPName08': 'old_pppname08', 'PValue08': 'old_pvalue08', 'PPPName09': 'old_pppname09', 'PValue09': 'old_pvalue09', 'PPPName10': 'old_pppname10', 'PValue10': 'old_pvalue10', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'SignedDate': 'old_signed_date', 'Signer': 'old_signer', 'OriJobSheetNo': 'old_ori_job_sheet_no', 'PPPName11': 'old_pppname11', 'PValue11': 'old_pvalue11', 'PPPName12': 'old_pppname12', 'PValue12': 'old_pvalue12', 'PPPName13': 'old_pppname13', 'PValue13': 'old_pvalue13', 'PPPName14': 'old_pppname14', 'PValue14': 'old_pvalue14', 'PPPName15': 'old_pppname15', 'PValue15': 'old_pvalue15', 'PPPName16': 'old_pppname16', 'PValue16': 'old_pvalue16', 'PPPName17': 'old_pppname17', 'PValue17': 'old_pvalue17', 'PPPName18': 'old_pppname18', 'PValue18': 'old_pvalue18', 'PPPName19': 'old_pppname19', 'PValue19': 'old_pvalue19', 'PPPName20': 'old_pppname20', 'PValue20': 'old_pvalue20', 'PPName21': 'old_ppname21', 'PPName22': 'old_ppname22', 'PPName23': 'old_ppname23', 'PPName24': 'old_ppname24', 'PPName25': 'old_ppname25', 'PPName26': 'old_ppname26', 'PPName27': 'old_ppname27', 'PPName28': 'old_ppname28', 'PPName29': 'old_ppname29', 'PPName30': 'old_ppname30', 'TheoryValue21': 'old_theory_value21', 'TheoryValue22': 'old_theory_value22', 'TheoryValue23': 'old_theory_value23', 'TheoryValue24': 'old_theory_value24', 'TheoryValue25': 'old_theory_value25', 'TheoryValue26': 'old_theory_value26', 'TheoryValue27': 'old_theory_value27', 'TheoryValue28': 'old_theory_value28', 'TheoryValue29': 'old_theory_value29', 'TheoryValue30': 'old_theory_value30', 'ActualValue21': 'old_actual_value21', 'ActualValue22': 'old_actual_value22', 'ActualValue23': 'old_actual_value23', 'ActualValue24': 'old_actual_value24', 'ActualValue25': 'old_actual_value25', 'ActualValue26': 'old_actual_value26', 'ActualValue27': 'old_actual_value27', 'ActualValue28': 'old_actual_value28', 'ActualValue29': 'old_actual_value29', 'ActualValue30': 'old_actual_value30', 'CraftParam': 'old_craft_param', 'IsODM': 'old_is_odm', 'WPWorker': 'old_wpworker', 'CurveIDs': 'old_curve_ids', 'CombineSheetNos': 'old_combine_sheet_nos', 'RecipeSeries': 'old_recipe_series', 'CraftCheck': 'old_craft_check', 'CraftChecker': 'old_craft_checker', 'CraftCheckTime': 'old_craft_check_time', 'DefectIDs': 'old_defect_ids', 'DefectApproveDate': 'old_defect_approve_date', 'MainProcessID': 'old_main_process_id', 'AreaID': 'old_area_id', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ColorMatching': 'old_color_matching', 'Reason': 'old_reason', 'Stereotypes': 'old_stereotypes', 'TeamName': 'old_team_name'}
    SOURCE_KEY=('SheetSeries', 'ProcessNo')
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('表单流水', null=False, blank=True, max_length=20)
    old_process_no=models.IntegerField('序号', null=False, blank=False)
    old_process_id=models.CharField('工序', null=True, blank=True, max_length=10)
    old_station_id=models.CharField('站别', null=True, blank=True, max_length=10)
    old_ppname01=models.CharField('参数名1', null=True, blank=True, max_length=20)
    old_theory_value01=models.CharField('设置值1', null=True, blank=True, max_length=20)
    old_actual_value01=models.CharField('ActualValue01', null=True, blank=True, max_length=20)
    old_ppname02=models.CharField('参数名2', null=True, blank=True, max_length=20)
    old_theory_value02=models.CharField('设置值2', null=True, blank=True, max_length=20)
    old_actual_value02=models.CharField('ActualValue02', null=True, blank=True, max_length=20)
    old_ppname03=models.CharField('参数名3', null=True, blank=True, max_length=20)
    old_theory_value03=models.CharField('设置值3', null=True, blank=True, max_length=20)
    old_actual_value03=models.CharField('ActualValue03', null=True, blank=True, max_length=20)
    old_ppname04=models.CharField('参数名4', null=True, blank=True, max_length=20)
    old_theory_value04=models.CharField('设置值4', null=True, blank=True, max_length=20)
    old_actual_value04=models.CharField('ActualValue04', null=True, blank=True, max_length=20)
    old_ppname05=models.CharField('参数名5', null=True, blank=True, max_length=20)
    old_theory_value05=models.CharField('设置值5', null=True, blank=True, max_length=20)
    old_actual_value05=models.CharField('ActualValue05', null=True, blank=True, max_length=20)
    old_ppname06=models.CharField('参数名6', null=True, blank=True, max_length=20)
    old_theory_value06=models.CharField('设置值6', null=True, blank=True, max_length=20)
    old_actual_value06=models.CharField('ActualValue06', null=True, blank=True, max_length=20)
    old_ppname07=models.CharField('参数名7', null=True, blank=True, max_length=20)
    old_theory_value07=models.CharField('设置值7', null=True, blank=True, max_length=20)
    old_actual_value07=models.CharField('ActualValue07', null=True, blank=True, max_length=20)
    old_ppname08=models.CharField('参数名8', null=True, blank=True, max_length=20)
    old_theory_value08=models.CharField('设置值8', null=True, blank=True, max_length=20)
    old_actual_value08=models.CharField('ActualValue08', null=True, blank=True, max_length=20)
    old_ppname09=models.CharField('参数名9', null=True, blank=True, max_length=20)
    old_theory_value09=models.CharField('设置值9', null=True, blank=True, max_length=20)
    old_actual_value09=models.CharField('ActualValue09', null=True, blank=True, max_length=20)
    old_ppname10=models.CharField('参数名10', null=True, blank=True, max_length=20)
    old_theory_value10=models.CharField('设置值10', null=True, blank=True, max_length=20)
    old_actual_value10=models.CharField('ActualValue10', null=True, blank=True, max_length=20)
    old_ppname11=models.CharField('参数名11', null=True, blank=True, max_length=20)
    old_theory_value11=models.CharField('设置值11', null=True, blank=True, max_length=20)
    old_actual_value11=models.CharField('ActualValue11', null=True, blank=True, max_length=20)
    old_ppname12=models.CharField('参数名12', null=True, blank=True, max_length=20)
    old_theory_value12=models.CharField('设置值12', null=True, blank=True, max_length=20)
    old_actual_value12=models.CharField('ActualValue12', null=True, blank=True, max_length=20)
    old_ppname13=models.CharField('参数名13', null=True, blank=True, max_length=20)
    old_theory_value13=models.CharField('设置值13', null=True, blank=True, max_length=100)
    old_actual_value13=models.CharField('ActualValue13', null=True, blank=True, max_length=20)
    old_ppname14=models.CharField('参数名14', null=True, blank=True, max_length=20)
    old_theory_value14=models.CharField('设置值14', null=True, blank=True, max_length=500)
    old_actual_value14=models.CharField('ActualValue14', null=True, blank=True, max_length=20)
    old_ppname15=models.CharField('参数名15', null=True, blank=True, max_length=20)
    old_theory_value15=models.CharField('设置值15', null=True, blank=True, max_length=20)
    old_actual_value15=models.CharField('ActualValue15', null=True, blank=True, max_length=20)
    old_ppname16=models.CharField('参数名16', null=True, blank=True, max_length=20)
    old_theory_value16=models.CharField('设置值16', null=True, blank=True, max_length=20)
    old_actual_value16=models.CharField('ActualValue16', null=True, blank=True, max_length=20)
    old_ppname17=models.CharField('参数名17', null=True, blank=True, max_length=20)
    old_theory_value17=models.CharField('设置值17', null=True, blank=True, max_length=20)
    old_actual_value17=models.CharField('ActualValue17', null=True, blank=True, max_length=20)
    old_ppname18=models.CharField('参数名18', null=True, blank=True, max_length=20)
    old_theory_value18=models.CharField('设置值18', null=True, blank=True, max_length=20)
    old_actual_value18=models.CharField('ActualValue18', null=True, blank=True, max_length=20)
    old_ppname19=models.CharField('参数名19', null=True, blank=True, max_length=20)
    old_theory_value19=models.CharField('设置值19', null=True, blank=True, max_length=20)
    old_actual_value19=models.CharField('ActualValue19', null=True, blank=True, max_length=20)
    old_ppname20=models.CharField('参数名20', null=True, blank=True, max_length=20)
    old_theory_value20=models.CharField('设置值20', null=True, blank=True, max_length=20)
    old_actual_value20=models.CharField('ActualValue20', null=True, blank=True, max_length=20)
    old_machine_id=models.CharField('机台', null=True, blank=True, max_length=10)
    old_vehicle_no=models.CharField('车号', null=True, blank=True, max_length=100)
    old_start_time=models.DateTimeField('开始时间', null=True, blank=True)
    old_end_time=models.DateTimeField('结束时间', null=True, blank=True)
    old_wprocess_no=models.CharField('刷卡记录号', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_status=models.CharField('状态', null=True, blank=True, max_length=2)
    old_flag=models.IntegerField('标记', null=True, blank=True)
    old_place=models.CharField('车位', null=True, blank=True, max_length=100)
    old_last_time=models.IntegerField('LastTime', null=True, blank=True)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=8, decimal_places=2)
    old_pppname01=models.CharField('幅宽', null=True, blank=True, max_length=20)
    old_pvalue01=models.CharField('PValue01', null=True, blank=True, max_length=20)
    old_pppname02=models.CharField('PPPName02', null=True, blank=True, max_length=20)
    old_pvalue02=models.CharField('PValue02', null=True, blank=True, max_length=20)
    old_pppname03=models.CharField('PPPName03', null=True, blank=True, max_length=20)
    old_pvalue03=models.CharField('PValue03', null=True, blank=True, max_length=20)
    old_pppname04=models.CharField('PPPName04', null=True, blank=True, max_length=20)
    old_pvalue04=models.CharField('PValue04', null=True, blank=True, max_length=20)
    old_pppname05=models.CharField('PPPName05', null=True, blank=True, max_length=20)
    old_pvalue05=models.CharField('PValue05', null=True, blank=True, max_length=20)
    old_pppname06=models.CharField('PPPName06', null=True, blank=True, max_length=20)
    old_pvalue06=models.CharField('PValue06', null=True, blank=True, max_length=20)
    old_pppname07=models.CharField('PPPName07', null=True, blank=True, max_length=20)
    old_pvalue07=models.CharField('PValue07', null=True, blank=True, max_length=20)
    old_pppname08=models.CharField('PPPName08', null=True, blank=True, max_length=20)
    old_pvalue08=models.CharField('PValue08', null=True, blank=True, max_length=20)
    old_pppname09=models.CharField('PPPName09', null=True, blank=True, max_length=20)
    old_pvalue09=models.CharField('PValue09', null=True, blank=True, max_length=20)
    old_pppname10=models.CharField('PPPName10', null=True, blank=True, max_length=20)
    old_pvalue10=models.CharField('PValue10', null=True, blank=True, max_length=20)
    old_create_date=models.DateTimeField('创建日期', null=True, blank=True)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_signed_date=models.DateTimeField('SignedDate', null=True, blank=True)
    old_signer=models.CharField('Signer', null=True, blank=True, max_length=10)
    old_ori_job_sheet_no=models.CharField('OriJobSheetNo', null=True, blank=True, max_length=20)
    old_pppname11=models.CharField('PPPName11', null=True, blank=True, max_length=20)
    old_pvalue11=models.CharField('PValue11', null=True, blank=True, max_length=20)
    old_pppname12=models.CharField('PPPName12', null=True, blank=True, max_length=20)
    old_pvalue12=models.CharField('PValue12', null=True, blank=True, max_length=20)
    old_pppname13=models.CharField('PPPName13', null=True, blank=True, max_length=20)
    old_pvalue13=models.CharField('PValue13', null=True, blank=True, max_length=20)
    old_pppname14=models.CharField('PPPName14', null=True, blank=True, max_length=20)
    old_pvalue14=models.CharField('PValue14', null=True, blank=True, max_length=20)
    old_pppname15=models.CharField('PPPName15', null=True, blank=True, max_length=20)
    old_pvalue15=models.CharField('PValue15', null=True, blank=True, max_length=20)
    old_pppname16=models.CharField('PPPName16', null=True, blank=True, max_length=20)
    old_pvalue16=models.CharField('PValue16', null=True, blank=True, max_length=20)
    old_pppname17=models.CharField('PPPName17', null=True, blank=True, max_length=20)
    old_pvalue17=models.CharField('PValue17', null=True, blank=True, max_length=20)
    old_pppname18=models.CharField('PPPName18', null=True, blank=True, max_length=20)
    old_pvalue18=models.CharField('PValue18', null=True, blank=True, max_length=20)
    old_pppname19=models.CharField('PPPName19', null=True, blank=True, max_length=20)
    old_pvalue19=models.CharField('PValue19', null=True, blank=True, max_length=20)
    old_pppname20=models.CharField('PPPName20', null=True, blank=True, max_length=20)
    old_pvalue20=models.CharField('PValue20', null=True, blank=True, max_length=20)
    old_ppname21=models.CharField('PPName21', null=True, blank=True, max_length=20)
    old_ppname22=models.CharField('PPName22', null=True, blank=True, max_length=20)
    old_ppname23=models.CharField('PPName23', null=True, blank=True, max_length=20)
    old_ppname24=models.CharField('PPName24', null=True, blank=True, max_length=20)
    old_ppname25=models.CharField('PPName25', null=True, blank=True, max_length=20)
    old_ppname26=models.CharField('PPName26', null=True, blank=True, max_length=20)
    old_ppname27=models.CharField('PPName27', null=True, blank=True, max_length=20)
    old_ppname28=models.CharField('PPName28', null=True, blank=True, max_length=20)
    old_ppname29=models.CharField('PPName29', null=True, blank=True, max_length=20)
    old_ppname30=models.CharField('PPName30', null=True, blank=True, max_length=20)
    old_theory_value21=models.CharField('TheoryValue21', null=True, blank=True, max_length=20)
    old_theory_value22=models.CharField('TheoryValue22', null=True, blank=True, max_length=20)
    old_theory_value23=models.CharField('TheoryValue23', null=True, blank=True, max_length=100)
    old_theory_value24=models.CharField('TheoryValue24', null=True, blank=True, max_length=500)
    old_theory_value25=models.CharField('TheoryValue25', null=True, blank=True, max_length=20)
    old_theory_value26=models.CharField('TheoryValue26', null=True, blank=True, max_length=26)
    old_theory_value27=models.CharField('TheoryValue27', null=True, blank=True, max_length=20)
    old_theory_value28=models.CharField('TheoryValue28', null=True, blank=True, max_length=20)
    old_theory_value29=models.CharField('TheoryValue29', null=True, blank=True, max_length=20)
    old_theory_value30=models.CharField('TheoryValue30', null=True, blank=True, max_length=20)
    old_actual_value21=models.CharField('ActualValue21', null=True, blank=True, max_length=20)
    old_actual_value22=models.CharField('ActualValue22', null=True, blank=True, max_length=20)
    old_actual_value23=models.CharField('ActualValue23', null=True, blank=True, max_length=20)
    old_actual_value24=models.CharField('ActualValue24', null=True, blank=True, max_length=20)
    old_actual_value25=models.CharField('ActualValue25', null=True, blank=True, max_length=20)
    old_actual_value26=models.CharField('ActualValue26', null=True, blank=True, max_length=20)
    old_actual_value27=models.CharField('ActualValue27', null=True, blank=True, max_length=20)
    old_actual_value28=models.CharField('ActualValue28', null=True, blank=True, max_length=20)
    old_actual_value29=models.CharField('ActualValue29', null=True, blank=True, max_length=20)
    old_actual_value30=models.CharField('ActualValue30', null=True, blank=True, max_length=20)
    old_craft_param=models.CharField('工艺参数', null=True, blank=True, max_length=100)
    old_is_odm=models.BooleanField('IsODM', null=True, blank=True)
    old_wpworker=models.CharField('WPWorker', null=True, blank=True, max_length=100)
    old_curve_ids=models.CharField('CurveIDs', null=True, blank=True, max_length=50)
    old_combine_sheet_nos=models.CharField('CombineSheetNos', null=True, blank=True, max_length=150)
    old_recipe_series=models.CharField('RecipeSeries', null=True, blank=True, max_length=50)
    old_craft_check=models.BooleanField('CraftCheck', null=True, blank=True)
    old_craft_checker=models.CharField('CraftChecker', null=True, blank=True, max_length=10)
    old_craft_check_time=models.DateTimeField('CraftCheckTime', null=True, blank=True)
    old_defect_ids=models.CharField('DefectIDs', null=True, blank=True, max_length=100)
    old_defect_approve_date=models.DateTimeField('DefectApproveDate', null=True, blank=True)
    old_main_process_id=models.CharField('MainProcessID', null=True, blank=True, max_length=50)
    old_area_id=models.CharField('AreaID', null=True, blank=True, max_length=50)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=50)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_color_matching=models.CharField('ColorMatching', null=True, blank=True, max_length=20)
    old_reason=models.CharField('更改/添加 原因', null=True, blank=True, max_length=521)
    old_stereotypes=models.IntegerField('定型次数', null=True, blank=True)
    old_team_name=models.CharField('TeamName', null=True, blank=True, max_length=100)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeJobSheet', verbose_name='原关系：JobSheet', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_jobprocess'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_process_no'],name='src_8d4abd7bfc50182b')]
        verbose_name=verbose_name_plural='计划工序'
        ordering=["-id"]

class SourceDyeJobProcessPre(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='JobProcessPre'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'ProcessNo': 'old_process_no', 'ProcessID': 'old_process_id', 'StationID': 'old_station_id', 'Price': 'old_price', 'MachineID': 'old_machine_id', 'CurveIDs': 'old_curve_ids', 'VehicleNo': 'old_vehicle_no', 'Place': 'old_place', 'OriJobSheetNo': 'old_ori_job_sheet_no', 'PPPName01': 'old_pppname01', 'PValue01': 'old_pvalue01', 'PPPName02': 'old_pppname02', 'PValue02': 'old_pvalue02', 'PPPName03': 'old_pppname03', 'PValue03': 'old_pvalue03', 'PPPName04': 'old_pppname04', 'PValue04': 'old_pvalue04', 'PPPName05': 'old_pppname05', 'PValue05': 'old_pvalue05', 'PPPName06': 'old_pppname06', 'PValue06': 'old_pvalue06', 'PPPName07': 'old_pppname07', 'PValue07': 'old_pvalue07', 'PPPName08': 'old_pppname08', 'PValue08': 'old_pvalue08', 'PPPName09': 'old_pppname09', 'PValue09': 'old_pvalue09', 'PPPName10': 'old_pppname10', 'PValue10': 'old_pvalue10', 'PPPName11': 'old_pppname11', 'PValue11': 'old_pvalue11', 'PPPName12': 'old_pppname12', 'PValue12': 'old_pvalue12', 'PPPName13': 'old_pppname13', 'PValue13': 'old_pvalue13', 'PPPName14': 'old_pppname14', 'PValue14': 'old_pvalue14', 'PPPName15': 'old_pppname15', 'PValue15': 'old_pvalue15', 'PPPName16': 'old_pppname16', 'PValue16': 'old_pvalue16', 'PPPName17': 'old_pppname17', 'PValue17': 'old_pvalue17', 'PPPName18': 'old_pppname18', 'PValue18': 'old_pvalue18', 'PPPName19': 'old_pppname19', 'PValue19': 'old_pvalue19', 'PPPName20': 'old_pppname20', 'PValue20': 'old_pvalue20', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'PPName01': 'old_ppname01', 'TheoryValue01': 'old_theory_value01', 'ActualValue01': 'old_actual_value01', 'PPName02': 'old_ppname02', 'TheoryValue02': 'old_theory_value02', 'ActualValue02': 'old_actual_value02', 'PPName03': 'old_ppname03', 'TheoryValue03': 'old_theory_value03', 'ActualValue03': 'old_actual_value03', 'PPName04': 'old_ppname04', 'TheoryValue04': 'old_theory_value04', 'ActualValue04': 'old_actual_value04', 'PPName05': 'old_ppname05', 'TheoryValue05': 'old_theory_value05', 'ActualValue05': 'old_actual_value05', 'PPName06': 'old_ppname06', 'TheoryValue06': 'old_theory_value06', 'ActualValue06': 'old_actual_value06', 'PPName07': 'old_ppname07', 'TheoryValue07': 'old_theory_value07', 'ActualValue07': 'old_actual_value07', 'PPName08': 'old_ppname08', 'TheoryValue08': 'old_theory_value08', 'ActualValue08': 'old_actual_value08', 'PPName09': 'old_ppname09', 'TheoryValue09': 'old_theory_value09', 'ActualValue09': 'old_actual_value09', 'PPName10': 'old_ppname10', 'TheoryValue10': 'old_theory_value10', 'ActualValue10': 'old_actual_value10', 'PPName11': 'old_ppname11', 'TheoryValue11': 'old_theory_value11', 'ActualValue11': 'old_actual_value11', 'PPName12': 'old_ppname12', 'TheoryValue12': 'old_theory_value12', 'ActualValue12': 'old_actual_value12', 'PPName13': 'old_ppname13', 'TheoryValue13': 'old_theory_value13', 'ActualValue13': 'old_actual_value13', 'PPName14': 'old_ppname14', 'TheoryValue14': 'old_theory_value14', 'ActualValue14': 'old_actual_value14', 'PPName15': 'old_ppname15', 'TheoryValue15': 'old_theory_value15', 'ActualValue15': 'old_actual_value15', 'PPName16': 'old_ppname16', 'TheoryValue16': 'old_theory_value16', 'ActualValue16': 'old_actual_value16', 'PPName17': 'old_ppname17', 'TheoryValue17': 'old_theory_value17', 'ActualValue17': 'old_actual_value17', 'PPName18': 'old_ppname18', 'TheoryValue18': 'old_theory_value18', 'ActualValue18': 'old_actual_value18', 'PPName19': 'old_ppname19', 'TheoryValue19': 'old_theory_value19', 'ActualValue19': 'old_actual_value19', 'PPName20': 'old_ppname20', 'TheoryValue20': 'old_theory_value20', 'ActualValue20': 'old_actual_value20', 'PPName21': 'old_ppname21', 'TheoryValue21': 'old_theory_value21', 'PPName22': 'old_ppname22', 'ActualValue21': 'old_actual_value21', 'TheoryValue22': 'old_theory_value22', 'ActualValue22': 'old_actual_value22', 'PPName23': 'old_ppname23', 'TheoryValue23': 'old_theory_value23', 'ActualValue23': 'old_actual_value23', 'PPName24': 'old_ppname24', 'TheoryValue24': 'old_theory_value24', 'ActualValue24': 'old_actual_value24', 'PPName25': 'old_ppname25', 'TheoryValue25': 'old_theory_value25', 'ActualValue25': 'old_actual_value25', 'PPName26': 'old_ppname26', 'TheoryValue26': 'old_theory_value26', 'ActualValue26': 'old_actual_value26', 'PPName27': 'old_ppname27', 'TheoryValue27': 'old_theory_value27', 'ActualValue27': 'old_actual_value27', 'PPName28': 'old_ppname28', 'TheoryValue28': 'old_theory_value28', 'ActualValue28': 'old_actual_value28', 'PPName29': 'old_ppname29', 'TheoryValue29': 'old_theory_value29', 'ActualValue29': 'old_actual_value29', 'PPName30': 'old_ppname30', 'TheoryValue30': 'old_theory_value30', 'CombineSheetNos': 'old_combine_sheet_nos', 'ActualValue30': 'old_actual_value30', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'SignedDate': 'old_signed_date', 'Signer': 'old_signer', 'StartTime': 'old_start_time', 'EndTime': 'old_end_time', 'WProcessNo': 'old_wprocess_no', 'Flag': 'old_flag', 'LastTime': 'old_last_time', 'Status': 'old_status', 'Remarks': 'old_remarks', 'IsODM': 'old_is_odm', 'RecipeSeries': 'old_recipe_series', 'CraftCheck': 'old_craft_check', 'CraftChecker': 'old_craft_checker', 'CraftCheckTime': 'old_craft_check_time', 'DefectIDs': 'old_defect_ids', 'DefectApproveDate': 'old_defect_approve_date', 'WPWorker': 'old_wpworker'}
    SOURCE_KEY=('SheetSeries', 'ProcessNo')
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=50)
    old_process_no=models.IntegerField('工序号', null=False, blank=False)
    old_process_id=models.CharField('工序代码', null=True, blank=True, max_length=10)
    old_station_id=models.CharField('站别代码', null=True, blank=True, max_length=10)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=10, decimal_places=4)
    old_machine_id=models.CharField('机台号', null=True, blank=True, max_length=10)
    old_curve_ids=models.CharField('CurveIDs', null=True, blank=True, max_length=50)
    old_vehicle_no=models.CharField('纱车号', null=True, blank=True, max_length=100)
    old_place=models.CharField('Place', null=True, blank=True, max_length=100)
    old_ori_job_sheet_no=models.CharField('OriJobSheetNo', null=True, blank=True, max_length=20)
    old_pppname01=models.CharField('PPPName01', null=True, blank=True, max_length=20)
    old_pvalue01=models.CharField('PValue01', null=True, blank=True, max_length=20)
    old_pppname02=models.CharField('PPPName02', null=True, blank=True, max_length=20)
    old_pvalue02=models.CharField('PValue02', null=True, blank=True, max_length=20)
    old_pppname03=models.CharField('PPPName03', null=True, blank=True, max_length=20)
    old_pvalue03=models.CharField('PValue03', null=True, blank=True, max_length=20)
    old_pppname04=models.CharField('PPPName04', null=True, blank=True, max_length=20)
    old_pvalue04=models.CharField('PValue04', null=True, blank=True, max_length=20)
    old_pppname05=models.CharField('PPPName05', null=True, blank=True, max_length=20)
    old_pvalue05=models.CharField('PValue05', null=True, blank=True, max_length=20)
    old_pppname06=models.CharField('PPPName06', null=True, blank=True, max_length=20)
    old_pvalue06=models.CharField('PValue06', null=True, blank=True, max_length=20)
    old_pppname07=models.CharField('PPPName07', null=True, blank=True, max_length=20)
    old_pvalue07=models.CharField('PValue07', null=True, blank=True, max_length=20)
    old_pppname08=models.CharField('PPPName08', null=True, blank=True, max_length=20)
    old_pvalue08=models.CharField('PValue08', null=True, blank=True, max_length=20)
    old_pppname09=models.CharField('PPPName09', null=True, blank=True, max_length=20)
    old_pvalue09=models.CharField('PValue09', null=True, blank=True, max_length=20)
    old_pppname10=models.CharField('PPPName10', null=True, blank=True, max_length=20)
    old_pvalue10=models.CharField('PValue10', null=True, blank=True, max_length=20)
    old_pppname11=models.CharField('PPPName11', null=True, blank=True, max_length=20)
    old_pvalue11=models.CharField('PValue11', null=True, blank=True, max_length=20)
    old_pppname12=models.CharField('PPPName12', null=True, blank=True, max_length=20)
    old_pvalue12=models.CharField('PValue12', null=True, blank=True, max_length=20)
    old_pppname13=models.CharField('PPPName13', null=True, blank=True, max_length=20)
    old_pvalue13=models.CharField('PValue13', null=True, blank=True, max_length=20)
    old_pppname14=models.CharField('PPPName14', null=True, blank=True, max_length=20)
    old_pvalue14=models.CharField('PValue14', null=True, blank=True, max_length=20)
    old_pppname15=models.CharField('PPPName15', null=True, blank=True, max_length=20)
    old_pvalue15=models.CharField('PValue15', null=True, blank=True, max_length=20)
    old_pppname16=models.CharField('PPPName16', null=True, blank=True, max_length=20)
    old_pvalue16=models.CharField('PValue16', null=True, blank=True, max_length=20)
    old_pppname17=models.CharField('PPPName17', null=True, blank=True, max_length=20)
    old_pvalue17=models.CharField('PValue17', null=True, blank=True, max_length=20)
    old_pppname18=models.CharField('PPPName18', null=True, blank=True, max_length=20)
    old_pvalue18=models.CharField('PValue18', null=True, blank=True, max_length=20)
    old_pppname19=models.CharField('PPPName19', null=True, blank=True, max_length=20)
    old_pvalue19=models.CharField('PValue19', null=True, blank=True, max_length=20)
    old_pppname20=models.CharField('PPPName20', null=True, blank=True, max_length=20)
    old_pvalue20=models.CharField('PValue20', null=True, blank=True, max_length=20)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_ppname01=models.CharField('参数名1', null=True, blank=True, max_length=20)
    old_theory_value01=models.CharField('设置值1', null=True, blank=True, max_length=20)
    old_actual_value01=models.CharField('ActualValue01', null=True, blank=True, max_length=50)
    old_ppname02=models.CharField('参数名2', null=True, blank=True, max_length=20)
    old_theory_value02=models.CharField('设置值2', null=True, blank=True, max_length=20)
    old_actual_value02=models.CharField('ActualValue02', null=True, blank=True, max_length=50)
    old_ppname03=models.CharField('参数名3', null=True, blank=True, max_length=20)
    old_theory_value03=models.CharField('设置值3', null=True, blank=True, max_length=20)
    old_actual_value03=models.CharField('ActualValue03', null=True, blank=True, max_length=500)
    old_ppname04=models.CharField('参数名4', null=True, blank=True, max_length=20)
    old_theory_value04=models.CharField('设置值4', null=True, blank=True, max_length=20)
    old_actual_value04=models.CharField('ActualValue04', null=True, blank=True, max_length=50)
    old_ppname05=models.CharField('参数名5', null=True, blank=True, max_length=20)
    old_theory_value05=models.CharField('设置值5', null=True, blank=True, max_length=20)
    old_actual_value05=models.CharField('ActualValue05', null=True, blank=True, max_length=50)
    old_ppname06=models.CharField('参数名6', null=True, blank=True, max_length=20)
    old_theory_value06=models.CharField('设置值6', null=True, blank=True, max_length=20)
    old_actual_value06=models.CharField('ActualValue06', null=True, blank=True, max_length=50)
    old_ppname07=models.CharField('参数名7', null=True, blank=True, max_length=20)
    old_theory_value07=models.CharField('设置值7', null=True, blank=True, max_length=20)
    old_actual_value07=models.CharField('ActualValue07', null=True, blank=True, max_length=50)
    old_ppname08=models.CharField('参数名8', null=True, blank=True, max_length=20)
    old_theory_value08=models.CharField('设置值8', null=True, blank=True, max_length=20)
    old_actual_value08=models.CharField('ActualValue08', null=True, blank=True, max_length=50)
    old_ppname09=models.CharField('参数名9', null=True, blank=True, max_length=20)
    old_theory_value09=models.CharField('设置值9', null=True, blank=True, max_length=20)
    old_actual_value09=models.CharField('ActualValue09', null=True, blank=True, max_length=50)
    old_ppname10=models.CharField('参数名10', null=True, blank=True, max_length=20)
    old_theory_value10=models.CharField('设置值10', null=True, blank=True, max_length=20)
    old_actual_value10=models.CharField('ActualValue10', null=True, blank=True, max_length=50)
    old_ppname11=models.CharField('参数名11', null=True, blank=True, max_length=20)
    old_theory_value11=models.CharField('设置值11', null=True, blank=True, max_length=20)
    old_actual_value11=models.CharField('ActualValue11', null=True, blank=True, max_length=50)
    old_ppname12=models.CharField('参数名12', null=True, blank=True, max_length=20)
    old_theory_value12=models.CharField('设置值12', null=True, blank=True, max_length=20)
    old_actual_value12=models.CharField('ActualValue12', null=True, blank=True, max_length=50)
    old_ppname13=models.CharField('参数名13', null=True, blank=True, max_length=20)
    old_theory_value13=models.CharField('设置值13', null=True, blank=True, max_length=20)
    old_actual_value13=models.CharField('ActualValue13', null=True, blank=True, max_length=50)
    old_ppname14=models.CharField('参数名14', null=True, blank=True, max_length=20)
    old_theory_value14=models.CharField('设置值14', null=True, blank=True, max_length=20)
    old_actual_value14=models.CharField('ActualValue14', null=True, blank=True, max_length=50)
    old_ppname15=models.CharField('参数名15', null=True, blank=True, max_length=20)
    old_theory_value15=models.CharField('设置值15', null=True, blank=True, max_length=20)
    old_actual_value15=models.CharField('ActualValue15', null=True, blank=True, max_length=50)
    old_ppname16=models.CharField('参数名16', null=True, blank=True, max_length=20)
    old_theory_value16=models.CharField('设置值16', null=True, blank=True, max_length=20)
    old_actual_value16=models.CharField('ActualValue16', null=True, blank=True, max_length=50)
    old_ppname17=models.CharField('参数名17', null=True, blank=True, max_length=20)
    old_theory_value17=models.CharField('设置值17', null=True, blank=True, max_length=20)
    old_actual_value17=models.CharField('ActualValue17', null=True, blank=True, max_length=50)
    old_ppname18=models.CharField('参数名18', null=True, blank=True, max_length=20)
    old_theory_value18=models.CharField('设置值18', null=True, blank=True, max_length=20)
    old_actual_value18=models.CharField('ActualValue18', null=True, blank=True, max_length=50)
    old_ppname19=models.CharField('参数名19', null=True, blank=True, max_length=20)
    old_theory_value19=models.CharField('设置值19', null=True, blank=True, max_length=20)
    old_actual_value19=models.CharField('ActualValue19', null=True, blank=True, max_length=50)
    old_ppname20=models.CharField('参数名20', null=True, blank=True, max_length=20)
    old_theory_value20=models.CharField('设置值20', null=True, blank=True, max_length=20)
    old_actual_value20=models.CharField('ActualValue20', null=True, blank=True, max_length=50)
    old_ppname21=models.CharField('PPName21', null=True, blank=True, max_length=20)
    old_theory_value21=models.CharField('TheoryValue21', null=True, blank=True, max_length=20)
    old_ppname22=models.CharField('PPName22', null=True, blank=True, max_length=20)
    old_actual_value21=models.CharField('ActualValue21', null=True, blank=True, max_length=50)
    old_theory_value22=models.CharField('TheoryValue22', null=True, blank=True, max_length=20)
    old_actual_value22=models.CharField('ActualValue22', null=True, blank=True, max_length=50)
    old_ppname23=models.CharField('PPName23', null=True, blank=True, max_length=20)
    old_theory_value23=models.CharField('TheoryValue23', null=True, blank=True, max_length=20)
    old_actual_value23=models.CharField('ActualValue23', null=True, blank=True, max_length=50)
    old_ppname24=models.CharField('PPName24', null=True, blank=True, max_length=20)
    old_theory_value24=models.CharField('TheoryValue24', null=True, blank=True, max_length=20)
    old_actual_value24=models.CharField('ActualValue24', null=True, blank=True, max_length=50)
    old_ppname25=models.CharField('PPName25', null=True, blank=True, max_length=20)
    old_theory_value25=models.CharField('TheoryValue25', null=True, blank=True, max_length=20)
    old_actual_value25=models.CharField('ActualValue25', null=True, blank=True, max_length=50)
    old_ppname26=models.CharField('PPName26', null=True, blank=True, max_length=20)
    old_theory_value26=models.CharField('TheoryValue26', null=True, blank=True, max_length=26)
    old_actual_value26=models.CharField('ActualValue26', null=True, blank=True, max_length=50)
    old_ppname27=models.CharField('PPName27', null=True, blank=True, max_length=20)
    old_theory_value27=models.CharField('TheoryValue27', null=True, blank=True, max_length=20)
    old_actual_value27=models.CharField('ActualValue27', null=True, blank=True, max_length=50)
    old_ppname28=models.CharField('PPName28', null=True, blank=True, max_length=20)
    old_theory_value28=models.CharField('TheoryValue28', null=True, blank=True, max_length=20)
    old_actual_value28=models.CharField('ActualValue28', null=True, blank=True, max_length=50)
    old_ppname29=models.CharField('PPName29', null=True, blank=True, max_length=20)
    old_theory_value29=models.CharField('TheoryValue29', null=True, blank=True, max_length=20)
    old_actual_value29=models.CharField('ActualValue29', null=True, blank=True, max_length=50)
    old_ppname30=models.CharField('PPName30', null=True, blank=True, max_length=20)
    old_theory_value30=models.CharField('TheoryValue30', null=True, blank=True, max_length=20)
    old_combine_sheet_nos=models.CharField('CombineSheetNos', null=True, blank=True, max_length=200)
    old_actual_value30=models.CharField('ActualValue30', null=True, blank=True, max_length=50)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_signed_date=models.DateTimeField('SignedDate', null=True, blank=True)
    old_signer=models.CharField('Signer', null=True, blank=True, max_length=10)
    old_start_time=models.DateTimeField('开始时间', null=True, blank=True)
    old_end_time=models.DateTimeField('结束时间', null=True, blank=True)
    old_wprocess_no=models.CharField('刷卡记录号', null=True, blank=True, max_length=20)
    old_flag=models.IntegerField('Flag', null=True, blank=True)
    old_last_time=models.IntegerField('LastTime', null=True, blank=True)
    old_status=models.CharField('状态', null=True, blank=True, max_length=10)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_is_odm=models.BooleanField('IsODM', null=True, blank=True)
    old_recipe_series=models.CharField('RecipeSeries', null=True, blank=True, max_length=20)
    old_craft_check=models.BooleanField('CraftCheck', null=True, blank=True)
    old_craft_checker=models.CharField('CraftChecker', null=True, blank=True, max_length=10)
    old_craft_check_time=models.DateTimeField('CraftCheckTime', null=True, blank=True)
    old_defect_ids=models.CharField('DefectIDs', null=True, blank=True, max_length=100)
    old_defect_approve_date=models.DateTimeField('DefectApproveDate', null=True, blank=True)
    old_wpworker=models.CharField('WPWorker', null=True, blank=True, max_length=50)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeJobSheet', verbose_name='原关系：JobSheet', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_jobprocesspre'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_process_no'],name='src_5e04aafdd44604e3')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（JobProcessPre，待确认）'
        ordering=["-id"]

class SourceDyeJobSheet(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='JobSheet'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'SheetType': 'old_sheet_type', 'JobKindID': 'old_job_kind_id', 'CheckNo': 'old_check_no', 'BusinessUnitID': 'old_business_unit_id', 'BusinessKind': 'old_business_kind', 'CustomerID': 'old_customer_id', 'DetailCustName': 'old_detail_cust_name', 'SalerGroupID': 'old_saler_group_id', 'SalerID': 'old_saler_id', 'ProdID': 'old_prod_id', 'LotNo': 'old_lot_no', 'Spec': 'old_spec', 'Structure': 'old_structure', 'ProductionID': 'old_production_id', 'Linker': 'old_linker', 'StockUnit': 'old_stock_unit', 'WidthKindID': 'old_width_kind_id', 'FactID': 'old_fact_id', 'OriJobsheetNo': 'old_ori_jobsheet_no', 'ColorDepthID': 'old_color_depth_id', 'ColorE': 'old_color_e', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'DesignNo': 'old_design_no', 'IsContinue': 'old_is_continue', 'IsHurry': 'old_is_hurry', 'IsSpecColor': 'old_is_spec_color', 'IsSpecVat': 'old_is_spec_vat', 'CustColorNum': 'old_cust_color_num', 'PreVatQty': 'old_pre_vat_qty', 'PreRolls': 'old_pre_rolls', 'PrePacks': 'old_pre_packs', 'SumAssignedWeightQty': 'old_sum_assigned_weight_qty', 'SumAssignedRolls': 'old_sum_assigned_rolls', 'SumAssignedPacks': 'old_sum_assigned_packs', 'SumProcessQty': 'old_sum_process_qty', 'VatNo': 'old_vat_no', 'DlvDate': 'old_dlv_date', 'FinishDate': 'old_finish_date', 'CurrProcessID': 'old_curr_process_id', 'CurrProcessNo': 'old_curr_process_no', 'CurrStationID': 'old_curr_station_id', 'StartDate': 'old_start_date', 'RedoEmpID': 'old_redo_emp_id', 'RedoProcessID': 'old_redo_process_id', 'RedoReasonID': 'old_redo_reason_id', 'RedoShiftID': 'old_redo_shift_id', 'WorkShopID': 'old_work_shop_id', 'MachineKindID': 'old_machine_kind_id', 'AssignUnit': 'old_assign_unit', 'OriOrderSeries': 'old_ori_order_series', 'SumProcessRolls': 'old_sum_process_rolls', 'LabelID': 'old_label_id', 'CustSelfNo': 'old_cust_self_no', 'CustSelfProduct': 'old_cust_self_product', 'CraftCheck': 'old_craft_check', 'OrderSheetNo': 'old_order_sheet_no', 'NextProcessID': 'old_next_process_id', 'NextStationID': 'old_next_station_id', 'ProgramID': 'old_program_id', 'Loss': 'old_loss', 'RealLoss': 'old_real_loss', 'AssignInfo': 'old_assign_info', 'StandCraftNo': 'old_stand_craft_no', 'ContractNo': 'old_contract_no', 'IsFirstVat': 'old_is_first_vat', 'ShippingMarkID': 'old_shipping_mark_id', 'PlanDetailNo': 'old_plan_detail_no', 'WidthDn': 'old_width_dn', 'WidthUp': 'old_width_up', 'WeightDn': 'old_weight_dn', 'WeightUp': 'old_weight_up', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'RelaLotNo': 'old_rela_lot_no', 'ColorRGB': 'old_color_rgb', 'IsPause': 'old_is_pause', 'PrintKind': 'old_print_kind', 'ProgramKindID': 'old_program_kind_id', 'OriColorID': 'old_ori_color_id', 'OriColorNum': 'old_ori_color_num', 'ConfirmSideID': 'old_confirm_side_id', 'PlanDate': 'old_plan_date', 'MainStuffKindID': 'old_main_stuff_kind_id', 'IsToLabDips': 'old_is_to_lab_dips', 'RedoDefectName': 'old_redo_defect_name', 'MachineID': 'old_machine_id', 'LossStr': 'old_loss_str', 'ProdQty': 'old_prod_qty', 'GWidth': 'old_gwidth', 'GWeight': 'old_gweight', 'WarpDensity': 'old_warp_density', 'WeftDensity': 'old_weft_density', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'AddrDlv': 'old_addr_dlv', 'WeightUnit': 'old_weight_unit', 'OrderSheetDate': 'old_order_sheet_date', 'Model1': 'old_model1', 'SumProcessLengthQty': 'old_sum_process_length_qty', 'SumProcessWeightQty': 'old_sum_process_weight_qty', 'Price': 'old_price', 'Code': 'old_code', 'Code1': 'old_code1', 'Weight': 'old_weight', 'Width': 'old_width', 'SumAssignedLengthQty': 'old_sum_assigned_length_qty', 'Pound': 'old_pound', 'Kg': 'old_kg', 'CustJobNo': 'old_cust_job_no', 'Sender': 'old_sender', 'Receiver': 'old_receiver', 'IsSplited': 'old_is_splited', 'WeightQty': 'old_weight_qty', 'OriSourceJobNo': 'old_ori_source_job_no', 'SetHurryTime': 'old_set_hurry_time', 'SetPauseBegTime': 'old_set_pause_beg_time', 'SetPauseEndTime': 'old_set_pause_end_time', 'HurryInfo': 'old_hurry_info', 'PauseInfo': 'old_pause_info', 'StorageUnitIDs': 'old_storage_unit_ids', 'RollAvgQtyStr': 'old_roll_avg_qty_str', 'IsProdInFinished': 'old_is_prod_in_finished', 'BarCode': 'old_bar_code', 'PhaseID': 'old_phase_id', 'Jobattes1': 'old_jobattes1', 'Finish': 'old_finish', 'OriSourceJobNo2': 'old_ori_source_job_no2', 'PenetrationNO': 'old_penetration_no', 'DetailNo': 'old_detail_no', 'OrderQty': 'old_order_qty', 'OrderQtyTotal': 'old_order_qty_total', 'Customer': 'old_customer', 'CHECKDots': 'old_checkdots', 'Checker': 'old_checker', 'IsOver': 'old_is_over', 'ProdWidth': 'old_prod_width', 'ProdWeight': 'old_prod_weight', 'ProdRePeatcnt': 'old_prod_re_peatcnt', 'ProdSkeWing': 'old_prod_ske_wing', 'Grade': 'old_grade', 'YAvgdots': 'old_yavgdots', 'PDots': 'old_pdots', 'PlengthQyt': 'old_plength_qyt', 'Pkg': 'old_pkg', 'PRolls': 'old_prolls', 'Inch': 'old_inch', 'FabricNO1': 'old_fabric_no1', 'FabricNO2': 'old_fabric_no2', 'FabricNO3': 'old_fabric_no3', 'EmpID': 'old_emp_id', 'RedoDeptID': 'old_redo_dept_id', 'PrintCode': 'old_print_code', 'ColorPlateID': 'old_color_plate_id', 'AddWeigth': 'old_add_weigth', 'TubeWeight': 'old_tube_weight', 'CustGrayID': 'old_cust_gray_id', 'LotSheetNo': 'old_lot_sheet_no', 'ShipMentType': 'old_ship_ment_type', 'ColorRemarks': 'old_color_remarks', 'WidthUnit': 'old_width_unit', 'WeightKindID': 'old_weight_kind_id', 'DB2BarCode': 'old_db2_bar_code', 'PackRemarks': 'old_pack_remarks', 'SplitCardReason': 'old_split_card_reason', 'ProcessName': 'old_process_name', 'GYYQ': 'old_gyyq', 'PBXX': 'old_pbxx', 'Suffix': 'old_suffix', 'Stereotypes': 'old_stereotypes', 'ProdUnit': 'old_prod_unit', 'ReleaseCardDate': 'old_release_card_date', 'NewLotNo': 'old_new_lot_no', 'StereotypesName': 'old_stereotypes_name', 'ReleaseCardDateTwo': 'old_release_card_date_two', 'NewProdID': 'old_new_prod_id', 'JobSheetType': 'old_job_sheet_type', 'YarnCategory': 'old_yarn_category', 'NewSheetNo': 'old_new_sheet_no', 'FixedQty': 'old_fixed_qty', 'Classify': 'old_classify', 'Q12': 'old_q12', 'Q13': 'old_q13', 'PreField1': 'old_pre_field1'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('表单流水', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('工卡号', null=True, blank=True, max_length=50)
    old_sheet_date=models.DateTimeField('开卡日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_sheet_type=models.IntegerField('工卡类型', null=True, blank=True)
    old_job_kind_id=models.CharField('流程卡类别', null=True, blank=True, max_length=10)
    old_check_no=models.CharField('订单明细号', null=True, blank=True, max_length=20)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_business_kind=models.IntegerField('业务类别', null=True, blank=True)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=10)
    old_detail_cust_name=models.CharField('明细客户', null=True, blank=True, max_length=150)
    old_saler_group_id=models.CharField('业务组别', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('业务员', null=True, blank=True, max_length=10)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=20)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=200)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=200)
    old_structure=models.CharField('组织', null=True, blank=True, max_length=500)
    old_production_id=models.CharField('生产工艺编码', null=True, blank=True, max_length=10)
    old_linker=models.CharField('联系人', null=True, blank=True, max_length=10)
    old_stock_unit=models.IntegerField('单位', null=True, blank=True)
    old_width_kind_id=models.CharField('幅宽单位', null=True, blank=True, max_length=20)
    old_fact_id=models.CharField('加工商', null=True, blank=True, max_length=10)
    old_ori_jobsheet_no=models.CharField('原卡号', null=True, blank=True, max_length=20)
    old_color_depth_id=models.CharField('颜色深浅', null=True, blank=True, max_length=10)
    old_color_e=models.CharField('颜色英文名', null=True, blank=True, max_length=20)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=150)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=50)
    old_design_no=models.CharField('花号', null=True, blank=True, max_length=20)
    old_is_continue=models.BooleanField('连缸', null=True, blank=True)
    old_is_hurry=models.BooleanField('加急', null=True, blank=True)
    old_is_spec_color=models.BooleanField('特殊颜色', null=True, blank=True)
    old_is_spec_vat=models.BooleanField('小缸', null=True, blank=True)
    old_cust_color_num=models.CharField('客户色号', null=True, blank=True, max_length=100)
    old_pre_vat_qty=models.DecimalField('排单数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pre_rolls=models.DecimalField('排单粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_pre_packs=models.DecimalField('排单件数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_sum_assigned_weight_qty=models.DecimalField('实发数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sum_assigned_rolls=models.DecimalField('实发粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_sum_assigned_packs=models.DecimalField('实发件数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_sum_process_qty=models.DecimalField('翻纱数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_vat_no=models.CharField('缸号', null=True, blank=True, max_length=20)
    old_dlv_date=models.DateTimeField('交期', null=True, blank=True)
    old_finish_date=models.DateTimeField('结案日期', null=True, blank=True)
    old_curr_process_id=models.CharField('本道工序代码', null=True, blank=True, max_length=50)
    old_curr_process_no=models.IntegerField('本道工序号', null=True, blank=True)
    old_curr_station_id=models.CharField('本道站别代码', null=True, blank=True, max_length=10)
    old_start_date=models.DateTimeField('开始日期', null=True, blank=True)
    old_redo_emp_id=models.CharField('重修责任人', null=True, blank=True, max_length=10)
    old_redo_process_id=models.CharField('重修工序', null=True, blank=True, max_length=10)
    old_redo_reason_id=models.CharField('重修原因代码', null=True, blank=True, max_length=500)
    old_redo_shift_id=models.CharField('重修班组', null=True, blank=True, max_length=50)
    old_work_shop_id=models.CharField('生产车间代码', null=True, blank=True, max_length=10)
    old_machine_kind_id=models.CharField('机型代码', null=True, blank=True, max_length=10)
    old_assign_unit=models.IntegerField('配纱方式', null=True, blank=True)
    old_ori_order_series=models.CharField('订单号', null=True, blank=True, max_length=20)
    old_sum_process_rolls=models.DecimalField('工序粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_label_id=models.CharField('标签号', null=True, blank=True, max_length=10)
    old_cust_self_no=models.CharField('制单号', null=True, blank=True, max_length=500)
    old_cust_self_product=models.CharField('客户规格', null=True, blank=True, max_length=200)
    old_craft_check=models.BooleanField('工艺审核状态', null=True, blank=True)
    old_order_sheet_no=models.CharField('订单号', null=True, blank=True, max_length=20)
    old_next_process_id=models.CharField('下道工序代码', null=True, blank=True, max_length=10)
    old_next_station_id=models.CharField('下道站别代码', null=True, blank=True, max_length=10)
    old_program_id=models.CharField('前道流程', null=True, blank=True, max_length=10)
    old_loss=models.CharField('缩率', null=True, blank=True, max_length=50)
    old_real_loss=models.DecimalField('实际缩率', null=True, blank=True, max_digits=4, decimal_places=1)
    old_assign_info=models.TextField('纱牌', null=True, blank=True)
    old_stand_craft_no=models.CharField('标准工艺', null=True, blank=True, max_length=20)
    old_contract_no=models.CharField('客户单号', null=True, blank=True, max_length=500)
    old_is_first_vat=models.BooleanField('头缸', null=True, blank=True)
    old_shipping_mark_id=models.CharField('唛头', null=True, blank=True, max_length=10)
    old_plan_detail_no=models.CharField('主计划明细号码', null=True, blank=True, max_length=30)
    old_width_dn=models.CharField('门幅下限', null=True, blank=True, max_length=50)
    old_width_up=models.CharField('门幅上限', null=True, blank=True, max_length=50)
    old_weight_dn=models.CharField('克重下限', null=True, blank=True, max_length=50)
    old_weight_up=models.CharField('克重上限', null=True, blank=True, max_length=50)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_step_no=models.IntegerField('工作流节点号', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.TextField('备注', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_rela_lot_no=models.CharField('RelaLotNo', null=True, blank=True, max_length=50)
    old_color_rgb=models.IntegerField('ColorRGB', null=True, blank=True)
    old_is_pause=models.BooleanField('IsPause', null=True, blank=True)
    old_print_kind=models.CharField('PrintKind', null=True, blank=True, max_length=1)
    old_program_kind_id=models.CharField('ProgramKindID', null=True, blank=True, max_length=10)
    old_ori_color_id=models.CharField('OriColorID', null=True, blank=True, max_length=10)
    old_ori_color_num=models.CharField('OriColorNum', null=True, blank=True, max_length=20)
    old_confirm_side_id=models.CharField('ConfirmSideID', null=True, blank=True, max_length=10)
    old_plan_date=models.DateTimeField('刷卡时间', null=True, blank=True)
    old_main_stuff_kind_id=models.CharField('MainStuffKindID', null=True, blank=True, max_length=10)
    old_is_to_lab_dips=models.BooleanField('IsToLabDips', null=True, blank=True)
    old_redo_defect_name=models.CharField('RedoDefectName', null=True, blank=True, max_length=100)
    old_machine_id=models.TextField('机台', null=True, blank=True)
    old_loss_str=models.CharField('LossStr', null=True, blank=True, max_length=20)
    old_prod_qty=models.DecimalField('ProdQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_gwidth=models.DecimalField('胚纱幅宽', null=True, blank=True, max_digits=6, decimal_places=2)
    old_gweight=models.DecimalField('胚纱克重', null=True, blank=True, max_digits=6, decimal_places=2)
    old_warp_density=models.CharField('经密', null=True, blank=True, max_length=50)
    old_weft_density=models.CharField('纬密', null=True, blank=True, max_length=50)
    old_approve_date=models.DateTimeField('审核日期', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_addr_dlv=models.CharField('送货地址', null=True, blank=True, max_length=150)
    old_weight_unit=models.CharField('克重种类', null=True, blank=True, max_length=20)
    old_order_sheet_date=models.DateTimeField('下单日期', null=True, blank=True)
    old_model1=models.CharField('款号', null=True, blank=True, max_length=200)
    old_sum_process_length_qty=models.DecimalField('工序长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sum_process_weight_qty=models.DecimalField('工序重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=8, decimal_places=2)
    old_code=models.CharField('Code', null=True, blank=True, max_length=20)
    old_code1=models.CharField('手感编码', null=True, blank=True, max_length=300)
    old_weight=models.CharField('克重', null=True, blank=True, max_length=200)
    old_width=models.CharField('幅宽', null=True, blank=True, max_length=200)
    old_sum_assigned_length_qty=models.DecimalField('实配长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pound=models.DecimalField('Pound', null=True, blank=True, max_digits=8, decimal_places=2)
    old_kg=models.DecimalField('Kg', null=True, blank=True, max_digits=8, decimal_places=2)
    old_cust_job_no=models.CharField('客户缸号', null=True, blank=True, max_length=100)
    old_sender=models.CharField('交胚人', null=True, blank=True, max_length=50)
    old_receiver=models.CharField('收胚人', null=True, blank=True, max_length=50)
    old_is_splited=models.IntegerField('IsSplited', null=True, blank=True)
    old_weight_qty=models.DecimalField('可入库重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_ori_source_job_no=models.CharField('原缸号', null=True, blank=True, max_length=50)
    old_set_hurry_time=models.DateTimeField('SetHurryTime', null=True, blank=True)
    old_set_pause_beg_time=models.DateTimeField('SetPauseBegTime', null=True, blank=True)
    old_set_pause_end_time=models.DateTimeField('SetPauseEndTime', null=True, blank=True)
    old_hurry_info=models.CharField('HurryInfo', null=True, blank=True, max_length=512)
    old_pause_info=models.CharField('PauseInfo', null=True, blank=True, max_length=512)
    old_storage_unit_ids=models.CharField('StorageUnitIDs', null=True, blank=True, max_length=100)
    old_roll_avg_qty_str=models.CharField('RollAvgQtyStr', null=True, blank=True, max_length=50)
    old_is_prod_in_finished=models.BooleanField('IsProdInFinished', null=True, blank=True)
    old_bar_code=models.CharField('条码', null=True, blank=True, max_length=100)
    old_phase_id=models.CharField('PhaseID', null=True, blank=True, max_length=10)
    old_jobattes1=models.CharField('Jobattes1', null=True, blank=True, max_length=1000)
    old_finish=models.IntegerField('Finish', null=True, blank=True)
    old_ori_source_job_no2=models.CharField('OriSourceJobNo2', null=True, blank=True, max_length=50)
    old_penetration_no=models.CharField('PenetrationNO', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=True, blank=True, max_length=20)
    old_order_qty=models.DecimalField('OrderQty', null=True, blank=True, max_digits=8, decimal_places=2)
    old_order_qty_total=models.DecimalField('OrderQtyTotal', null=True, blank=True, max_digits=8, decimal_places=2)
    old_customer=models.CharField('Customer', null=True, blank=True, max_length=200)
    old_checkdots=models.DecimalField('CHECKDots', null=True, blank=True, max_digits=18, decimal_places=0)
    old_checker=models.CharField('Checker', null=True, blank=True, max_length=10)
    old_is_over=models.BooleanField('IsOver', null=True, blank=True)
    old_prod_width=models.FloatField('ProdWidth', null=True, blank=True)
    old_prod_weight=models.FloatField('ProdWeight', null=True, blank=True)
    old_prod_re_peatcnt=models.CharField('ProdRePeatcnt', null=True, blank=True, max_length=10)
    old_prod_ske_wing=models.FloatField('ProdSkeWing', null=True, blank=True)
    old_grade=models.CharField('Grade', null=True, blank=True, max_length=10)
    old_yavgdots=models.FloatField('YAvgdots', null=True, blank=True)
    old_pdots=models.IntegerField('PDots', null=True, blank=True)
    old_plength_qyt=models.FloatField('PlengthQyt', null=True, blank=True)
    old_pkg=models.FloatField('Pkg', null=True, blank=True)
    old_prolls=models.IntegerField('PRolls', null=True, blank=True)
    old_inch=models.CharField('Inch', null=True, blank=True, max_length=20)
    old_fabric_no1=models.CharField('宝誉条码', null=True, blank=True, max_length=200)
    old_fabric_no2=models.CharField('任务单号', null=True, blank=True, max_length=200)
    old_fabric_no3=models.TextField('FabricNO3', null=True, blank=True)
    old_emp_id=models.CharField('EmpID', null=True, blank=True, max_length=10)
    old_redo_dept_id=models.CharField('责任部门', null=True, blank=True, max_length=50)
    old_print_code=models.CharField('花号', null=True, blank=True, max_length=50)
    old_color_plate_id=models.CharField('色位', null=True, blank=True, max_length=10)
    old_add_weigth=models.FloatField('成品空加', null=True, blank=True)
    old_tube_weight=models.FloatField('纸筒', null=True, blank=True)
    old_cust_gray_id=models.CharField('纱种编码', null=True, blank=True, max_length=50)
    old_lot_sheet_no=models.CharField('LotSheetNo', null=True, blank=True, max_length=20)
    old_ship_ment_type=models.CharField('出货方式', null=True, blank=True, max_length=10)
    old_color_remarks=models.TextField('用途', null=True, blank=True)
    old_width_unit=models.CharField('幅宽单位', null=True, blank=True, max_length=20)
    old_weight_kind_id=models.CharField('克重单位', null=True, blank=True, max_length=20)
    old_db2_bar_code=models.TextField('二维码睿程', null=True, blank=True)
    old_pack_remarks=models.TextField('PackRemarks', null=True, blank=True)
    old_split_card_reason=models.CharField('拆卡原因', null=True, blank=True, max_length=100)
    old_process_name=models.CharField('订单工序', null=True, blank=True, max_length=255)
    old_gyyq=models.CharField('工艺要求', null=True, blank=True, max_length=500)
    old_pbxx=models.CharField('配纱信息', null=True, blank=True, max_length=500)
    old_suffix=models.CharField('Suffix', null=True, blank=True, max_length=50)
    old_stereotypes=models.CharField('定型次数', null=True, blank=True, max_length=50)
    old_prod_unit=models.IntegerField('标签单位', null=True, blank=True)
    old_release_card_date=models.DateTimeField('放卡时间', null=True, blank=True)
    old_new_lot_no=models.CharField('新批号', null=True, blank=True, max_length=200)
    old_stereotypes_name=models.CharField('染缸编号', null=True, blank=True, max_length=50)
    old_release_card_date_two=models.DateTimeField('ReleaseCardDateTwo', null=True, blank=True)
    old_new_prod_id=models.CharField('成品规格', null=True, blank=True, max_length=20)
    old_job_sheet_type=models.CharField('工卡类型', null=True, blank=True, max_length=10)
    old_yarn_category=models.CharField('纱类别', null=True, blank=True, max_length=50)
    old_new_sheet_no=models.CharField('数字编号', null=True, blank=True, max_length=50)
    old_fixed_qty=models.DecimalField('锭重', null=True, blank=True, max_digits=5, decimal_places=2)
    old_classify=models.CharField('半成品分类', null=True, blank=True, max_length=50)
    old_q12=models.CharField('纸筒_N', null=True, blank=True, max_length=100)
    old_q13=models.CharField('包装_N', null=True, blank=True, max_length=100)
    old_pre_field1=models.CharField('捻度(H/S)', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_jobsheet'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_no'],name='src_dea827a5f6521057'),models.Index(fields=['source_batch', 'old_sheet_series'],name='src_8346bc23544fff24')]
        verbose_name=verbose_name_plural='生产工卡/缸卡'
        ordering=["-id"]

class SourceDyeJobSheetMasrkCar(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='JobSheetMasrkCar'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetKind': 'old_sheet_kind', 'JobSheetNo': 'old_job_sheet_no', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'ColorE': 'old_color_e', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'CustColorNum': 'old_cust_color_num', 'CustSelfNo': 'old_cust_self_no', 'CustSelfProduct': 'old_cust_self_product', 'Rolls': 'old_rolls', 'LengthQty': 'old_length_qty', 'DeptID': 'old_dept_id', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Remarks': 'old_remarks', 'Pound': 'old_pound', 'Kg': 'old_kg', 'Width': 'old_width', 'Weight': 'old_weight', 'ProgramItem': 'old_program_item', 'dyeDescription': 'old_dye_description', 'SheetType': 'old_sheet_type'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=50)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=36)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_customer_id=models.CharField('客户编码', null=True, blank=True, max_length=50)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=200)
    old_color_e=models.CharField('颜色英文名', null=True, blank=True, max_length=20)
    old_color_id=models.CharField('颜色编码', null=True, blank=True, max_length=200)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=100)
    old_cust_color_num=models.CharField('客户色号', null=True, blank=True, max_length=20)
    old_cust_self_no=models.CharField('制单号', null=True, blank=True, max_length=500)
    old_cust_self_product=models.CharField('客户规格', null=True, blank=True, max_length=200)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_length_qty=models.DecimalField('长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dept_id=models.CharField('部门', null=True, blank=True, max_length=10)
    old_creater=models.CharField('登记人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('登记时间', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_pound=models.DecimalField('磅数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_kg=models.DecimalField('公斤', null=True, blank=True, max_digits=10, decimal_places=2)
    old_width=models.CharField('幅宽', null=True, blank=True, max_length=200)
    old_weight=models.CharField('克重', null=True, blank=True, max_length=200)
    old_program_item=models.CharField('工艺', null=True, blank=True, max_length=500)
    old_dye_description=models.CharField('dyeDescription', null=True, blank=True, max_length=200)
    old_sheet_type=models.CharField('送版类别', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_jobsheetmasrkcar'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_a7a38766097b166c')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（JobSheetMasrkCar，待确认）'
        ordering=["-id"]

class SourceDyeJobSheetNoRushOrder(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='JobSheetNoRushOrder'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'CustomerID': 'old_customer_id', 'JobSheetNo': 'old_job_sheet_no', 'ProdID': 'old_prod_id', 'CustSelfProduct': 'old_cust_self_product', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'CustColorNum': 'old_cust_color_num', 'CurrProcessID': 'old_curr_process_id', 'CustSelfNo': 'old_cust_self_no', 'SWidth': 'old_swidth', 'SWeight': 'old_sweight', 'SumAssignedRolls': 'old_sum_assigned_rolls', 'SumAssignedWeightQty': 'old_sum_assigned_weight_qty', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'RightStatus': 'old_right_status', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=50)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_cust_self_product=models.CharField('客户规格', null=True, blank=True, max_length=200)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=50)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=50)
    old_cust_color_num=models.CharField('客户色号', null=True, blank=True, max_length=50)
    old_curr_process_id=models.CharField('当前进度', null=True, blank=True, max_length=50)
    old_cust_self_no=models.CharField('制单号', null=True, blank=True, max_length=50)
    old_swidth=models.CharField('幅宽', null=True, blank=True, max_length=50)
    old_sweight=models.CharField('克重', null=True, blank=True, max_length=50)
    old_sum_assigned_rolls=models.DecimalField('实发粒数', null=True, blank=True, max_digits=10, decimal_places=1)
    old_sum_assigned_weight_qty=models.DecimalField('实发数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_creater=models.CharField('制单人', null=True, blank=True, max_length=50)
    old_create_date=models.DateTimeField('制单日期', null=True, blank=True)
    old_right_status=models.IntegerField('状态', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=50)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=50)
    old_approve_date=models.DateTimeField('审核日期', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_jobsheetnorushorder'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_16b9a3c29ed9557f')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（JobSheetNoRushOrder，待确认）'
        ordering=["-id"]

class SourceDyeJobSheetOther(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='JobSheetOther'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'SheetType': 'old_sheet_type', 'JobKindID': 'old_job_kind_id', 'CheckNo': 'old_check_no', 'BusinessUnitID': 'old_business_unit_id', 'BusinessKind': 'old_business_kind', 'CustomerID': 'old_customer_id', 'DetailCustName': 'old_detail_cust_name', 'SalerGroupID': 'old_saler_group_id', 'SalerID': 'old_saler_id', 'ProdID': 'old_prod_id', 'LotNo': 'old_lot_no', 'Spec': 'old_spec', 'Structure': 'old_structure', 'ProductionID': 'old_production_id', 'Linker': 'old_linker', 'StockUnit': 'old_stock_unit', 'WidthKindID': 'old_width_kind_id', 'FactID': 'old_fact_id', 'OriJobsheetNo': 'old_ori_jobsheet_no', 'ColorDepthID': 'old_color_depth_id', 'ColorE': 'old_color_e', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'DesignNo': 'old_design_no', 'IsContinue': 'old_is_continue', 'IsHurry': 'old_is_hurry', 'IsSpecColor': 'old_is_spec_color', 'IsSpecVat': 'old_is_spec_vat', 'CustColorNum': 'old_cust_color_num', 'PreVatQty': 'old_pre_vat_qty', 'PreRolls': 'old_pre_rolls', 'SumAssignedWeightQty': 'old_sum_assigned_weight_qty', 'SumAssignedRolls': 'old_sum_assigned_rolls', 'SumProcessQty': 'old_sum_process_qty', 'VatNo': 'old_vat_no', 'DlvDate': 'old_dlv_date', 'FinishDate': 'old_finish_date', 'CurrProcessID': 'old_curr_process_id', 'CurrProcessNo': 'old_curr_process_no', 'CurrStationID': 'old_curr_station_id', 'StartDate': 'old_start_date', 'RedoEmpID': 'old_redo_emp_id', 'RedoProcessID': 'old_redo_process_id', 'RedoReasonID': 'old_redo_reason_id', 'RedoShiftID': 'old_redo_shift_id', 'WorkShopID': 'old_work_shop_id', 'MachineKindID': 'old_machine_kind_id', 'AssignUnit': 'old_assign_unit', 'OriOrderSeries': 'old_ori_order_series', 'SumProcessRolls': 'old_sum_process_rolls', 'LabelID': 'old_label_id', 'CustSelfNo': 'old_cust_self_no', 'CustSelfProduct': 'old_cust_self_product', 'CraftCheck': 'old_craft_check', 'OrderSheetNo': 'old_order_sheet_no', 'NextProcessID': 'old_next_process_id', 'NextStationID': 'old_next_station_id', 'ProgramID': 'old_program_id', 'Loss': 'old_loss', 'RealLoss': 'old_real_loss', 'AssignInfo': 'old_assign_info', 'StandCraftNo': 'old_stand_craft_no', 'ContractNo': 'old_contract_no', 'IsFirstVat': 'old_is_first_vat', 'ShippingMarkID': 'old_shipping_mark_id', 'PlanDetailNo': 'old_plan_detail_no', 'WidthDn': 'old_width_dn', 'WidthUp': 'old_width_up', 'WeightDn': 'old_weight_dn', 'WeightUp': 'old_weight_up', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'RelaLotNo': 'old_rela_lot_no', 'ColorRGB': 'old_color_rgb', 'IsPause': 'old_is_pause', 'PrintKind': 'old_print_kind', 'ProgramKindID': 'old_program_kind_id', 'OriColorID': 'old_ori_color_id', 'OriColorNum': 'old_ori_color_num', 'ConfirmSideID': 'old_confirm_side_id', 'PlanDate': 'old_plan_date', 'MainStuffKindID': 'old_main_stuff_kind_id', 'IsToLabDips': 'old_is_to_lab_dips', 'RedoDefectName': 'old_redo_defect_name', 'MachineID': 'old_machine_id', 'LossStr': 'old_loss_str', 'ProdQty': 'old_prod_qty', 'GWidth': 'old_gwidth', 'GWeight': 'old_gweight', 'WarpDensity': 'old_warp_density', 'WeftDensity': 'old_weft_density', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'AddrDlv': 'old_addr_dlv', 'WeightUnit': 'old_weight_unit', 'OrderSheetDate': 'old_order_sheet_date', 'Model1': 'old_model1', 'SumProcessLengthQty': 'old_sum_process_length_qty', 'SumProcessWeightQty': 'old_sum_process_weight_qty', 'Price': 'old_price', 'Code': 'old_code', 'Code1': 'old_code1', 'Weight': 'old_weight', 'Width': 'old_width', 'SumAssignedLengthQty': 'old_sum_assigned_length_qty', 'OrderQty': 'old_order_qty', 'OrderQtyTotal': 'old_order_qty_total', 'CustJobNo': 'old_cust_job_no', 'Sender': 'old_sender', 'Receiver': 'old_receiver', 'IsSplited': 'old_is_splited', 'WeightQty': 'old_weight_qty', 'OriSourceJobNo': 'old_ori_source_job_no', 'SetHurryTime': 'old_set_hurry_time', 'SetPauseBegTime': 'old_set_pause_beg_time', 'SetPauseEndTime': 'old_set_pause_end_time', 'HurryInfo': 'old_hurry_info', 'PauseInfo': 'old_pause_info', 'StorageUnitIDs': 'old_storage_unit_ids', 'RollAvgQtyStr': 'old_roll_avg_qty_str', 'IsProdInFinished': 'old_is_prod_in_finished', 'BarCode': 'old_bar_code', 'PhaseID': 'old_phase_id', 'Jobattes1': 'old_jobattes1', 'Finish': 'old_finish', 'OriSourceJobNo2': 'old_ori_source_job_no2', 'Customer': 'old_customer', 'CHECKDots': 'old_checkdots', 'Checker': 'old_checker', 'IsOver': 'old_is_over', 'ProdWidth': 'old_prod_width', 'ProdWeight': 'old_prod_weight', 'ProdRePeatcnt': 'old_prod_re_peatcnt', 'ProdSkeWing': 'old_prod_ske_wing', 'Grade': 'old_grade', 'YAvgdots': 'old_yavgdots', 'PDots': 'old_pdots', 'PlengthQyt': 'old_plength_qyt', 'Pkg': 'old_pkg', 'PRolls': 'old_prolls', 'DetailNo': 'old_detail_no', 'PenetrationNO': 'old_penetration_no', 'Inch': 'old_inch', 'FabricNO1': 'old_fabric_no1', 'FabricNO2': 'old_fabric_no2', 'FabricNO3': 'old_fabric_no3', 'EmpID': 'old_emp_id'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=100)
    old_sheet_date=models.DateTimeField('开卡日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('SheetKind', null=True, blank=True)
    old_sheet_type=models.IntegerField('SheetType', null=True, blank=True)
    old_job_kind_id=models.CharField('JobKindID', null=True, blank=True, max_length=10)
    old_check_no=models.CharField('CheckNo', null=True, blank=True, max_length=20)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_business_kind=models.IntegerField('BusinessKind', null=True, blank=True)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=200)
    old_detail_cust_name=models.CharField('明细客户', null=True, blank=True, max_length=50)
    old_saler_group_id=models.CharField('SalerGroupID', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('SalerID', null=True, blank=True, max_length=10)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=500)
    old_lot_no=models.CharField('LotNo', null=True, blank=True, max_length=200)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=200)
    old_structure=models.CharField('Structure', null=True, blank=True, max_length=150)
    old_production_id=models.CharField('ProductionID', null=True, blank=True, max_length=10)
    old_linker=models.CharField('Linker', null=True, blank=True, max_length=10)
    old_stock_unit=models.IntegerField('StockUnit', null=True, blank=True)
    old_width_kind_id=models.CharField('WidthKindID', null=True, blank=True, max_length=10)
    old_fact_id=models.CharField('FactID', null=True, blank=True, max_length=10)
    old_ori_jobsheet_no=models.CharField('OriJobsheetNo', null=True, blank=True, max_length=20)
    old_color_depth_id=models.CharField('颜色深浅', null=True, blank=True, max_length=10)
    old_color_e=models.CharField('ColorE', null=True, blank=True, max_length=20)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=200)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=200)
    old_design_no=models.CharField('DesignNo', null=True, blank=True, max_length=20)
    old_is_continue=models.BooleanField('IsContinue', null=True, blank=True)
    old_is_hurry=models.BooleanField('IsHurry', null=True, blank=True)
    old_is_spec_color=models.BooleanField('IsSpecColor', null=True, blank=True)
    old_is_spec_vat=models.BooleanField('IsSpecVat', null=True, blank=True)
    old_cust_color_num=models.CharField('CustColorNum', null=True, blank=True, max_length=20)
    old_pre_vat_qty=models.FloatField('排单数量', null=True, blank=True)
    old_pre_rolls=models.FloatField('排单粒数', null=True, blank=True)
    old_sum_assigned_weight_qty=models.FloatField('实发数量', null=True, blank=True)
    old_sum_assigned_rolls=models.FloatField('实发粒数', null=True, blank=True)
    old_sum_process_qty=models.DecimalField('SumProcessQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_vat_no=models.CharField('VatNo', null=True, blank=True, max_length=20)
    old_dlv_date=models.DateTimeField('DlvDate', null=True, blank=True)
    old_finish_date=models.DateTimeField('FinishDate', null=True, blank=True)
    old_curr_process_id=models.CharField('CurrProcessID', null=True, blank=True, max_length=10)
    old_curr_process_no=models.IntegerField('CurrProcessNo', null=True, blank=True)
    old_curr_station_id=models.CharField('CurrStationID', null=True, blank=True, max_length=10)
    old_start_date=models.DateTimeField('StartDate', null=True, blank=True)
    old_redo_emp_id=models.CharField('RedoEmpID', null=True, blank=True, max_length=10)
    old_redo_process_id=models.CharField('RedoProcessID', null=True, blank=True, max_length=10)
    old_redo_reason_id=models.CharField('RedoReasonID', null=True, blank=True, max_length=500)
    old_redo_shift_id=models.CharField('RedoShiftID', null=True, blank=True, max_length=50)
    old_work_shop_id=models.CharField('WorkShopID', null=True, blank=True, max_length=10)
    old_machine_kind_id=models.CharField('MachineKindID', null=True, blank=True, max_length=10)
    old_assign_unit=models.IntegerField('AssignUnit', null=True, blank=True)
    old_ori_order_series=models.CharField('OriOrderSeries', null=True, blank=True, max_length=20)
    old_sum_process_rolls=models.DecimalField('SumProcessRolls', null=True, blank=True, max_digits=7, decimal_places=2)
    old_label_id=models.CharField('LabelID', null=True, blank=True, max_length=10)
    old_cust_self_no=models.CharField('制单号', null=True, blank=True, max_length=200)
    old_cust_self_product=models.CharField('客户规格', null=True, blank=True, max_length=50)
    old_craft_check=models.BooleanField('CraftCheck', null=True, blank=True)
    old_order_sheet_no=models.CharField('OrderSheetNo', null=True, blank=True, max_length=20)
    old_next_process_id=models.CharField('NextProcessID', null=True, blank=True, max_length=10)
    old_next_station_id=models.CharField('NextStationID', null=True, blank=True, max_length=10)
    old_program_id=models.CharField('ProgramID', null=True, blank=True, max_length=10)
    old_loss=models.CharField('Loss', null=True, blank=True, max_length=50)
    old_real_loss=models.DecimalField('RealLoss', null=True, blank=True, max_digits=4, decimal_places=1)
    old_assign_info=models.CharField('AssignInfo', null=True, blank=True, max_length=500)
    old_stand_craft_no=models.CharField('StandCraftNo', null=True, blank=True, max_length=20)
    old_contract_no=models.CharField('客户单号', null=True, blank=True, max_length=200)
    old_is_first_vat=models.BooleanField('IsFirstVat', null=True, blank=True)
    old_shipping_mark_id=models.CharField('ShippingMarkID', null=True, blank=True, max_length=10)
    old_plan_detail_no=models.CharField('PlanDetailNo', null=True, blank=True, max_length=30)
    old_width_dn=models.DecimalField('WidthDn', null=True, blank=True, max_digits=6, decimal_places=2)
    old_width_up=models.DecimalField('WidthUp', null=True, blank=True, max_digits=6, decimal_places=2)
    old_weight_dn=models.DecimalField('WeightDn', null=True, blank=True, max_digits=6, decimal_places=2)
    old_weight_up=models.DecimalField('WeightUp', null=True, blank=True, max_digits=6, decimal_places=2)
    old_sheet_status=models.IntegerField('SheetStatus', null=True, blank=True)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_print_times=models.IntegerField('PrintTimes', null=True, blank=True)
    old_revisions=models.IntegerField('Revisions', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_rela_lot_no=models.CharField('RelaLotNo', null=True, blank=True, max_length=50)
    old_color_rgb=models.IntegerField('ColorRGB', null=True, blank=True)
    old_is_pause=models.BooleanField('IsPause', null=True, blank=True)
    old_print_kind=models.CharField('PrintKind', null=True, blank=True, max_length=1)
    old_program_kind_id=models.CharField('ProgramKindID', null=True, blank=True, max_length=10)
    old_ori_color_id=models.CharField('OriColorID', null=True, blank=True, max_length=10)
    old_ori_color_num=models.CharField('OriColorNum', null=True, blank=True, max_length=20)
    old_confirm_side_id=models.CharField('ConfirmSideID', null=True, blank=True, max_length=10)
    old_plan_date=models.DateTimeField('PlanDate', null=True, blank=True)
    old_main_stuff_kind_id=models.CharField('MainStuffKindID', null=True, blank=True, max_length=10)
    old_is_to_lab_dips=models.BooleanField('IsToLabDips', null=True, blank=True)
    old_redo_defect_name=models.CharField('RedoDefectName', null=True, blank=True, max_length=100)
    old_machine_id=models.CharField('MachineID', null=True, blank=True, max_length=10)
    old_loss_str=models.CharField('LossStr', null=True, blank=True, max_length=20)
    old_prod_qty=models.DecimalField('ProdQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_gwidth=models.DecimalField('GWidth', null=True, blank=True, max_digits=6, decimal_places=2)
    old_gweight=models.DecimalField('GWeight', null=True, blank=True, max_digits=6, decimal_places=2)
    old_warp_density=models.CharField('WarpDensity', null=True, blank=True, max_length=50)
    old_weft_density=models.CharField('WeftDensity', null=True, blank=True, max_length=50)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_addr_dlv=models.CharField('AddrDlv', null=True, blank=True, max_length=50)
    old_weight_unit=models.CharField('WeightUnit', null=True, blank=True, max_length=10)
    old_order_sheet_date=models.DateTimeField('OrderSheetDate', null=True, blank=True)
    old_model1=models.CharField('Model1', null=True, blank=True, max_length=10)
    old_sum_process_length_qty=models.DecimalField('SumProcessLengthQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sum_process_weight_qty=models.DecimalField('SumProcessWeightQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=8, decimal_places=2)
    old_code=models.CharField('Code', null=True, blank=True, max_length=20)
    old_code1=models.CharField('Code1', null=True, blank=True, max_length=20)
    old_weight=models.CharField('Weight', null=True, blank=True, max_length=200)
    old_width=models.CharField('Width', null=True, blank=True, max_length=200)
    old_sum_assigned_length_qty=models.DecimalField('SumAssignedLengthQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_order_qty=models.DecimalField('OrderQty', null=True, blank=True, max_digits=8, decimal_places=2)
    old_order_qty_total=models.DecimalField('OrderQtyTotal', null=True, blank=True, max_digits=8, decimal_places=2)
    old_cust_job_no=models.CharField('CustJobNo', null=True, blank=True, max_length=50)
    old_sender=models.CharField('Sender', null=True, blank=True, max_length=20)
    old_receiver=models.CharField('Receiver', null=True, blank=True, max_length=20)
    old_is_splited=models.IntegerField('IsSplited', null=True, blank=True)
    old_weight_qty=models.DecimalField('WeightQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_ori_source_job_no=models.CharField('OriSourceJobNo', null=True, blank=True, max_length=50)
    old_set_hurry_time=models.DateTimeField('SetHurryTime', null=True, blank=True)
    old_set_pause_beg_time=models.DateTimeField('SetPauseBegTime', null=True, blank=True)
    old_set_pause_end_time=models.DateTimeField('SetPauseEndTime', null=True, blank=True)
    old_hurry_info=models.CharField('HurryInfo', null=True, blank=True, max_length=512)
    old_pause_info=models.CharField('PauseInfo', null=True, blank=True, max_length=512)
    old_storage_unit_ids=models.CharField('StorageUnitIDs', null=True, blank=True, max_length=100)
    old_roll_avg_qty_str=models.CharField('RollAvgQtyStr', null=True, blank=True, max_length=50)
    old_is_prod_in_finished=models.BooleanField('IsProdInFinished', null=True, blank=True)
    old_bar_code=models.CharField('BarCode', null=True, blank=True, max_length=100)
    old_phase_id=models.CharField('PhaseID', null=True, blank=True, max_length=10)
    old_jobattes1=models.CharField('Jobattes1', null=True, blank=True, max_length=1000)
    old_finish=models.IntegerField('Finish', null=True, blank=True)
    old_ori_source_job_no2=models.CharField('OriSourceJobNo2', null=True, blank=True, max_length=50)
    old_customer=models.CharField('Customer', null=True, blank=True, max_length=200)
    old_checkdots=models.DecimalField('标准分值', null=True, blank=True, max_digits=18, decimal_places=0)
    old_checker=models.CharField('Checker', null=True, blank=True, max_length=10)
    old_is_over=models.BooleanField('IsOver', null=True, blank=True)
    old_prod_width=models.FloatField('ProdWidth', null=True, blank=True)
    old_prod_weight=models.FloatField('ProdWeight', null=True, blank=True)
    old_prod_re_peatcnt=models.CharField('ProdRePeatcnt', null=True, blank=True, max_length=10)
    old_prod_ske_wing=models.FloatField('ProdSkeWing', null=True, blank=True)
    old_grade=models.CharField('Grade', null=True, blank=True, max_length=10)
    old_yavgdots=models.FloatField('YAvgdots', null=True, blank=True)
    old_pdots=models.IntegerField('PDots', null=True, blank=True)
    old_plength_qyt=models.FloatField('PlengthQyt', null=True, blank=True)
    old_pkg=models.FloatField('Pkg', null=True, blank=True)
    old_prolls=models.IntegerField('PRolls', null=True, blank=True)
    old_detail_no=models.CharField('DetailNo', null=True, blank=True, max_length=20)
    old_penetration_no=models.CharField('PenetrationNO', null=True, blank=True, max_length=20)
    old_inch=models.CharField('Inch', null=True, blank=True, max_length=20)
    old_fabric_no1=models.CharField('FabricNO1', null=True, blank=True, max_length=200)
    old_fabric_no2=models.CharField('FabricNO2', null=True, blank=True, max_length=200)
    old_fabric_no3=models.CharField('FabricNO3', null=True, blank=True, max_length=200)
    old_emp_id=models.CharField('EmpID', null=True, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_jobsheetother'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_6254da08bf233136')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（JobSheetOther，待确认）'
        ordering=["-id"]

class SourceDyeJobSheetReceive(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='JobSheetReceive'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetKind': 'old_sheet_kind', 'SheetDate': 'old_sheet_date', 'JobSheetNo': 'old_job_sheet_no', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'ColorE': 'old_color_e', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'CustColorNum': 'old_cust_color_num', 'CustSelfNo': 'old_cust_self_no', 'CustSelfProduct': 'old_cust_self_product', 'Rolls': 'old_rolls', 'LengthQty': 'old_length_qty', 'DeptID': 'old_dept_id', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Remarks': 'old_remarks', 'WeightQty': 'old_weight_qty', 'Width': 'old_width', 'Weight': 'old_weight', 'ProgramItem': 'old_program_item', 'dyeDescription': 'old_dye_description', 'SheetType': 'old_sheet_type', 'BusinessUnitID': 'old_business_unit_id', 'CombineSheetNos': 'old_combine_sheet_nos', 'MachineNo': 'old_machine_no', 'ColorMatching': 'old_color_matching', 'Days': 'old_days', 'ShiftID': 'old_shift_id', 'Bigs': 'old_bigs', 'AddVat': 'old_add_vat', 'RTVat': 'old_rtvat', 'PassVat': 'old_pass_vat', 'BatchColor': 'old_batch_color', 'DyeFactoryOpinions': 'old_dye_factory_opinions', 'IsOK': 'old_is_ok'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=50)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=36)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_sheet_date=models.DateTimeField('单据时间', null=True, blank=True)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_customer_id=models.CharField('客户编码', null=True, blank=True, max_length=50)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=200)
    old_color_e=models.CharField('颜色英文名', null=True, blank=True, max_length=20)
    old_color_id=models.CharField('颜色编码', null=True, blank=True, max_length=200)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=100)
    old_cust_color_num=models.CharField('客户色号', null=True, blank=True, max_length=20)
    old_cust_self_no=models.CharField('制单号', null=True, blank=True, max_length=500)
    old_cust_self_product=models.CharField('客户规格', null=True, blank=True, max_length=200)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_length_qty=models.DecimalField('长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dept_id=models.CharField('部门', null=True, blank=True, max_length=10)
    old_creater=models.CharField('登记人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('登记时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_weight_qty=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_width=models.CharField('幅宽', null=True, blank=True, max_length=200)
    old_weight=models.CharField('克重', null=True, blank=True, max_length=200)
    old_program_item=models.CharField('单双染', null=True, blank=True, max_length=500)
    old_dye_description=models.CharField('是否首缸', null=True, blank=True, max_length=200)
    old_sheet_type=models.CharField('SheetType', null=True, blank=True, max_length=20)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=50)
    old_combine_sheet_nos=models.TextField('合缸缸号', null=True, blank=True)
    old_machine_no=models.CharField('机台', null=True, blank=True, max_length=50)
    old_color_matching=models.CharField('对色员', null=True, blank=True, max_length=50)
    old_days=models.CharField('日期', null=True, blank=True, max_length=10)
    old_shift_id=models.CharField('班别', null=True, blank=True, max_length=50)
    old_bigs=models.FloatField('Bigs', null=True, blank=True)
    old_add_vat=models.IntegerField('AddVat', null=True, blank=True)
    old_rtvat=models.FloatField('RTVat', null=True, blank=True)
    old_pass_vat=models.FloatField('PassVat', null=True, blank=True)
    old_batch_color=models.CharField('批复情况', null=True, blank=True, max_length=250)
    old_dye_factory_opinions=models.CharField('染厂意见', null=True, blank=True, max_length=250)
    old_is_ok=models.CharField('是否OK', null=True, blank=True, max_length=30)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_jobsheetreceive'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_3d543c2dcdea3cd7')]
        verbose_name=verbose_name_plural='工卡接收/结算记录'
        ordering=["-id"]

class SourceDyeJobSheetRegister(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='JobSheetRegister'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetKind': 'old_sheet_kind', 'SheetDate': 'old_sheet_date', 'JobSheetNo': 'old_job_sheet_no', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'ColorE': 'old_color_e', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'CustColorNum': 'old_cust_color_num', 'CustSelfNo': 'old_cust_self_no', 'CustSelfProduct': 'old_cust_self_product', 'Rolls': 'old_rolls', 'LengthQty': 'old_length_qty', 'DeptID': 'old_dept_id', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Remarks': 'old_remarks', 'WeightQty': 'old_weight_qty', 'Width': 'old_width', 'Weight': 'old_weight', 'ProgramItem': 'old_program_item', 'dyeDescription': 'old_dye_description', 'SheetType': 'old_sheet_type', 'BusinessUnitID': 'old_business_unit_id', 'CombineSheetNos': 'old_combine_sheet_nos', 'MachineNo': 'old_machine_no', 'ColorMatching': 'old_color_matching', 'Days': 'old_days', 'ShiftID': 'old_shift_id', 'Bigs': 'old_bigs', 'AddVat': 'old_add_vat', 'RTVat': 'old_rtvat', 'PassVat': 'old_pass_vat', 'BatchColor': 'old_batch_color', 'DyeFactoryOpinions': 'old_dye_factory_opinions', 'IsOK': 'old_is_ok'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=50)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=36)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_sheet_date=models.DateTimeField('单据时间', null=True, blank=True)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_customer_id=models.CharField('客户编码', null=True, blank=True, max_length=50)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=200)
    old_color_e=models.CharField('颜色英文名', null=True, blank=True, max_length=20)
    old_color_id=models.CharField('颜色编码', null=True, blank=True, max_length=200)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=100)
    old_cust_color_num=models.CharField('客户色号', null=True, blank=True, max_length=20)
    old_cust_self_no=models.CharField('制单号', null=True, blank=True, max_length=500)
    old_cust_self_product=models.CharField('客户规格', null=True, blank=True, max_length=200)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_length_qty=models.DecimalField('长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dept_id=models.CharField('部门', null=True, blank=True, max_length=10)
    old_creater=models.CharField('登记人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('登记时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_weight_qty=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_width=models.CharField('幅宽', null=True, blank=True, max_length=200)
    old_weight=models.CharField('克重', null=True, blank=True, max_length=200)
    old_program_item=models.CharField('单双染', null=True, blank=True, max_length=500)
    old_dye_description=models.CharField('是否首缸', null=True, blank=True, max_length=200)
    old_sheet_type=models.CharField('SheetType', null=True, blank=True, max_length=20)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=50)
    old_combine_sheet_nos=models.TextField('合缸缸号', null=True, blank=True)
    old_machine_no=models.CharField('机台', null=True, blank=True, max_length=50)
    old_color_matching=models.CharField('对色员', null=True, blank=True, max_length=50)
    old_days=models.CharField('日期', null=True, blank=True, max_length=10)
    old_shift_id=models.CharField('班别', null=True, blank=True, max_length=50)
    old_bigs=models.FloatField('Bigs', null=True, blank=True)
    old_add_vat=models.IntegerField('AddVat', null=True, blank=True)
    old_rtvat=models.FloatField('RTVat', null=True, blank=True)
    old_pass_vat=models.FloatField('PassVat', null=True, blank=True)
    old_batch_color=models.CharField('BatchColor', null=True, blank=True, max_length=250)
    old_dye_factory_opinions=models.CharField('加色次数', null=True, blank=True, max_length=250)
    old_is_ok=models.CharField('IsOK', null=True, blank=True, max_length=30)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_jobsheetregister'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_77995b60db477168')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（JobSheetRegister，待确认）'
        ordering=["-id"]

class SourceDyeJobSheetSchedule(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='JobSheetSchedule'
    SOURCE_FIELDS={'ID': 'old_id', 'JobSheetSeries': 'old_job_sheet_series', 'JobSheetNo': 'old_job_sheet_no', 'SequenceNo': 'old_sequence_no', 'Status': 'old_status', 'PlanDate': 'old_plan_date', 'StartTime': 'old_start_time', 'FinishTime': 'old_finish_time', 'TargetMin': 'old_target_min', 'ShiftID': 'old_shift_id', 'ClassID': 'old_class_id', 'ProgramID': 'old_program_id', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=True
    old_id=models.CharField('编码', null=False, blank=True, max_length=50)
    old_job_sheet_series=models.CharField('流程卡流水号', null=True, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_sequence_no=models.BigIntegerField('顺序号', null=True, blank=True)
    old_status=models.CharField('状态', null=True, blank=True, max_length=1)
    old_plan_date=models.DateTimeField('计划日期', null=True, blank=True)
    old_start_time=models.DateTimeField('开始时间', null=True, blank=True)
    old_finish_time=models.DateTimeField('结束时间', null=True, blank=True)
    old_target_min=models.IntegerField('预计分钟', null=True, blank=True)
    old_shift_id=models.CharField('班组', null=True, blank=True, max_length=10)
    old_class_id=models.CharField('班别', null=True, blank=True, max_length=10)
    old_program_id=models.CharField('前道流程', null=True, blank=True, max_length=10)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=300)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_jobsheetschedule'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_5b95cd17bf9ea859')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（JobSheetSchedule，待确认）'
        ordering=["-id"]

class SourceDyeJobShiftEmp(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='JobShiftEmp'
    SOURCE_FIELDS={'JobSheetNo': 'old_job_sheet_no', 'ShiftID': 'old_shift_id', 'EmpID': 'old_emp_id', 'EffiRate': 'old_effi_rate', 'Remarks': 'old_remarks', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer', 'ProcessNo': 'old_process_no', 'ProcessID': 'old_process_id', 'WProcessNo': 'old_wprocess_no', 'Post': 'old_post'}
    SOURCE_KEY=('JobSheetNo', 'ShiftID', 'EmpID', 'ProcessNo', 'WProcessNo')
    SOURCE_DOCUMENT=True
    old_job_sheet_no=models.CharField('缸号', null=False, blank=True, max_length=50)
    old_shift_id=models.CharField('班组', null=False, blank=True, max_length=10)
    old_emp_id=models.CharField('员工', null=False, blank=True, max_length=10)
    old_effi_rate=models.DecimalField('效率比例', null=True, blank=True, max_digits=6, decimal_places=4)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_process_no=models.IntegerField('工序号', null=False, blank=False)
    old_process_id=models.CharField('工序', null=True, blank=True, max_length=10)
    old_wprocess_no=models.CharField('刷卡号', null=False, blank=True, max_length=20)
    old_post=models.CharField('Post', null=True, blank=True, max_length=20)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeWProcess', verbose_name='原关系：WProcess', null=True, blank=True, on_delete=models.PROTECT, related_name='+')
    source_parent_2=models.ForeignKey('erp_production.SourceDyeWProcess', verbose_name='原关系：WProcess', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_jobshiftemp'
        indexes=[models.Index(fields=['source_batch', 'old_job_sheet_no', 'old_shift_id', 'old_emp_id', 'old_process_no', 'old_wprocess_no'],name='src_7e4ce22999529851')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（JobShiftEmp，待确认）'
        ordering=["-id"]

class SourceDyeJobShiftEmpBak(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='JobShiftEmpBak'
    SOURCE_FIELDS={'JobSheetNo': 'old_job_sheet_no', 'ShiftID': 'old_shift_id', 'EmpID': 'old_emp_id', 'EffiRate': 'old_effi_rate', 'Remarks': 'old_remarks', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer', 'ProcessNo': 'old_process_no', 'ProcessID': 'old_process_id', 'WProcessNo': 'old_wprocess_no'}
    SOURCE_KEY=('JobSheetNo', 'ShiftID', 'EmpID', 'ProcessNo', 'WProcessNo')
    SOURCE_DOCUMENT=True
    old_job_sheet_no=models.CharField('JobSheetNo', null=False, blank=True, max_length=50)
    old_shift_id=models.CharField('ShiftID', null=False, blank=True, max_length=10)
    old_emp_id=models.CharField('EmpID', null=False, blank=True, max_length=10)
    old_effi_rate=models.DecimalField('EffiRate', null=True, blank=True, max_digits=6, decimal_places=4)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_process_no=models.IntegerField('ProcessNo', null=False, blank=False)
    old_process_id=models.CharField('ProcessID', null=True, blank=True, max_length=10)
    old_wprocess_no=models.CharField('WProcessNo', null=False, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_jobshiftempbak'
        indexes=[models.Index(fields=['source_batch', 'old_job_sheet_no', 'old_shift_id', 'old_emp_id', 'old_process_no', 'old_wprocess_no'],name='src_f7c02906651541f1')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（JobShiftEmpBak，待确认）'
        ordering=["-id"]

class SourceDyeJobStartRollNo(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='JobStartRollNo'
    SOURCE_FIELDS={'CheckNo': 'old_check_no', 'OrderNo': 'old_order_no', 'JobSheetNo': 'old_job_sheet_no'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    old_check_no=models.CharField('CheckNo', null=True, blank=True, max_length=20)
    old_order_no=models.CharField('OrderNo', null=True, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_jobstartrollno'
        indexes=[]
        verbose_name=verbose_name_plural='生产工单与排程相关表（JobStartRollNo，待确认）'
        ordering=["-id"]

class SourceDyeMachineCarePlan(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='MachineCarePlan'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'DeptID': 'old_dept_id', 'StartTime': 'old_start_time', 'EndTime': 'old_end_time', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Remarks': 'old_remarks', 'Kind': 'old_kind', 'BusinessUnitID': 'old_business_unit_id', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('单据号码', null=True, blank=True, max_length=36)
    old_dept_id=models.CharField('部门', null=True, blank=True, max_length=10)
    old_start_time=models.DateTimeField('开始时间', null=True, blank=True)
    old_end_time=models.DateTimeField('结束时间', null=True, blank=True)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类别', null=True, blank=True)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_print_times=models.IntegerField('PrintTimes', null=True, blank=True)
    old_revisions=models.IntegerField('Revisions', null=True, blank=True)
    old_creater=models.CharField('制单人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('制单时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_kind=models.CharField('类别', null=True, blank=True, max_length=20)
    old_business_unit_id=models.CharField('经营单位', null=True, blank=True, max_length=10)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=10)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_machinecareplan'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_defa88fa327281a4')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（MachineCarePlan，待确认）'
        ordering=["-id"]

class SourceDyeMachineCarePlanDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='MachineCarePlanDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'DeptID': 'old_dept_id', 'MachineID': 'old_machine_id', 'ShiftID': 'old_shift_id', 'HandlerIDs': 'old_handler_ids', 'HandleDate': 'old_handle_date', 'HandleIdea': 'old_handle_idea', 'ResultID': 'old_result_id', 'Approver': 'old_approver', 'ApproveIdea': 'old_approve_idea', 'ApproveDate': 'old_approve_date', 'Remarks': 'old_remarks', 'PartID': 'old_part_id', 'ArticleID': 'old_article_id'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=False
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('明显号', null=False, blank=True, max_length=36)
    old_dept_id=models.CharField('部门', null=True, blank=True, max_length=10)
    old_machine_id=models.CharField('机台', null=True, blank=True, max_length=50)
    old_shift_id=models.CharField('班组', null=True, blank=True, max_length=10)
    old_handler_ids=models.CharField('保养人员', null=True, blank=True, max_length=100)
    old_handle_date=models.DateTimeField('保养日期', null=True, blank=True)
    old_handle_idea=models.CharField('相关意见', null=True, blank=True, max_length=512)
    old_result_id=models.CharField('保养结果', null=True, blank=True, max_length=200)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_approve_idea=models.CharField('审核意见', null=True, blank=True, max_length=200)
    old_approve_date=models.DateTimeField('审核日期', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_part_id=models.CharField('保养部位', null=True, blank=True, max_length=10)
    old_article_id=models.CharField('机配件', null=True, blank=True, max_length=10)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeMachineCarePlan', verbose_name='原关系：MachineCarePlan', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_machinecareplandetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_2b422470a7f02c08')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（MachineCarePlanDetail，待确认）'
        ordering=["-id"]

class SourceDyeMachineCareProject(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='MachineCareProject'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'SortNo': 'old_sort_no', 'SerialNum': 'old_serial_num', 'ProjectInfo': 'old_project_info', 'Value': 'old_value', 'DefaultValue': 'old_default_value', 'Remarks': 'old_remarks', 'CaseDetailNo': 'old_case_detail_no', 'Result': 'old_result', 'IsInputText': 'old_is_input_text'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=False, blank=True, max_length=36)
    old_sort_no=models.IntegerField('SortNo', null=True, blank=True)
    old_serial_num=models.CharField('SerialNum', null=True, blank=True, max_length=10)
    old_project_info=models.CharField('ProjectInfo', null=True, blank=True, max_length=200)
    old_value=models.CharField('Value', null=True, blank=True, max_length=100)
    old_default_value=models.CharField('DefaultValue', null=True, blank=True, max_length=100)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_case_detail_no=models.CharField('CaseDetailNo', null=True, blank=True, max_length=36)
    old_result=models.IntegerField('Result', null=True, blank=True)
    old_is_input_text=models.BooleanField('IsInputText', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_machinecareproject'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_6e5b923437a4ba8d')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（MachineCareProject，待确认）'
        ordering=["-id"]

class SourceDyeMachineCareRecords(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='MachineCareRecords'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'MachineID': 'old_machine_id', 'CarePlanDetailNo': 'old_care_plan_detail_no', 'EmpID': 'old_emp_id', 'CareDate': 'old_care_date', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'RightStatus': 'old_right_status', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'HandlerIDs': 'old_handler_ids', 'HandleIdea': 'old_handle_idea', 'ResultID': 'old_result_id', 'MachineName': 'old_machine_name', 'MachineLocation': 'old_machine_location'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=False
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('记录单号', null=True, blank=True, max_length=36)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_machine_id=models.CharField('保养设备', null=True, blank=True, max_length=20)
    old_care_plan_detail_no=models.CharField('保养计划明细单号', null=True, blank=True, max_length=50)
    old_emp_id=models.CharField('保养人', null=True, blank=True, max_length=50)
    old_care_date=models.DateTimeField('保养时间', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=1000)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_handler_ids=models.CharField('保养员', null=True, blank=True, max_length=100)
    old_handle_idea=models.CharField('相关意见', null=True, blank=True, max_length=50)
    old_result_id=models.CharField('处理结果', null=True, blank=True, max_length=200)
    old_machine_name=models.CharField('MachineName', null=True, blank=True, max_length=64)
    old_machine_location=models.CharField('MachineLocation', null=True, blank=True, max_length=64)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_machinecarerecords'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_9e841395ff7e0204')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（MachineCareRecords，待确认）'
        ordering=["-id"]

class SourceDyeMachineCase(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='MachineCase'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'ContentName': 'old_content_name', 'BaseCaseID': 'old_base_case_id', 'IsMultipleCase': 'old_is_multiple_case', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'RightStatus': 'old_right_status', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('类型', null=True, blank=True)
    old_content_name=models.CharField('内容名称', null=True, blank=True, max_length=50)
    old_base_case_id=models.CharField('基础方案', null=True, blank=True, max_length=20)
    old_is_multiple_case=models.BooleanField('IsMultipleCase', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('制单人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('制单日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('审核日期', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_machinecase'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_b8a413c3fdc64b7e')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（MachineCase，待确认）'
        ordering=["-id"]

class SourceDyeMachineCaseDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='MachineCaseDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'MachineID': 'old_machine_id', 'Cycle': 'old_cycle', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=False
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=36)
    old_machine_id=models.CharField('机台', null=True, blank=True, max_length=50)
    old_cycle=models.CharField('周期描述', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeMachineCase', verbose_name='原关系：MachineCase', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_machinecasedetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_3aecc424fdd83958')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（MachineCaseDetail，待确认）'
        ordering=["-id"]

class SourceDyeMachineCaseProject(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='MachineCaseProject'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'SortNo': 'old_sort_no', 'SerialNum': 'old_serial_num', 'ProjectInfo': 'old_project_info', 'DefaultValue': 'old_default_value', 'Remarks': 'old_remarks', 'BaseCaseDetailNo': 'old_base_case_detail_no', 'IsInputText': 'old_is_input_text'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=36)
    old_sort_no=models.IntegerField('排序号', null=True, blank=True)
    old_serial_num=models.CharField('序号', null=True, blank=True, max_length=10)
    old_project_info=models.CharField('项目内容', null=True, blank=True, max_length=200)
    old_default_value=models.CharField('常规值', null=True, blank=True, max_length=100)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_base_case_detail_no=models.CharField('基础方案明细号', null=True, blank=True, max_length=36)
    old_is_input_text=models.BooleanField('是否输入文本', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeMachineCase', verbose_name='原关系：MachineCase', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_machinecaseproject'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_6de187076d61251c')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（MachineCaseProject，待确认）'
        ordering=["-id"]

class SourceDyeMachineFault(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='MachineFault'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'MachineID': 'old_machine_id', 'EmpID': 'old_emp_id', 'HappenTime': 'old_happen_time', 'ApplyTime': 'old_apply_time', 'DeptID': 'old_dept_id', 'ShiftID': 'old_shift_id', 'FaultID': 'old_fault_id', 'SeverityID': 'old_severity_id', 'HandlerIDs': 'old_handler_ids', 'Handlers': 'old_handlers', 'StartTime': 'old_start_time', 'EndTime': 'old_end_time', 'ResultID': 'old_result_id', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'SheetStatus': 'old_sheet_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'HandleIdea': 'old_handle_idea', 'RightStatus': 'old_right_status', 'PhotoAddress': 'old_photo_address', 'ApproveIdea': 'old_approve_idea', 'PatrolDetailNo': 'old_patrol_detail_no', 'SheetType': 'old_sheet_type', 'StationID': 'old_station_id', 'BusinessUnitID': 'old_business_unit_id', 'FaultRemarks': 'old_fault_remarks', 'MachineName': 'old_machine_name', 'MachineLocation': 'old_machine_location', 'Urgent': 'old_urgent', 'FlowStatus': 'old_flow_status', 'ApplyMan': 'old_apply_man', 'ApplyIdea': 'old_apply_idea', 'EmpGroup': 'old_emp_group', 'FaultClass': 'old_fault_class', 'MachineClass': 'old_machine_class'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('报修单号', null=True, blank=True, max_length=36)
    old_sheet_date=models.DateTimeField('报修日期', null=True, blank=True)
    old_sheet_kind=models.CharField('单据类别', null=True, blank=True, max_length=20)
    old_machine_id=models.CharField('机台号', null=True, blank=True, max_length=50)
    old_emp_id=models.CharField('员工', null=True, blank=True, max_length=50)
    old_happen_time=models.DateTimeField('发生时间', null=True, blank=True)
    old_apply_time=models.DateTimeField('申请时间', null=True, blank=True)
    old_dept_id=models.CharField('部门', null=True, blank=True, max_length=20)
    old_shift_id=models.CharField('班别', null=True, blank=True, max_length=20)
    old_fault_id=models.CharField('故障', null=True, blank=True, max_length=512)
    old_severity_id=models.CharField('严重等级', null=True, blank=True, max_length=20)
    old_handler_ids=models.CharField('HandlerIDs', null=True, blank=True, max_length=100)
    old_handlers=models.CharField('Handlers', null=True, blank=True, max_length=100)
    old_start_time=models.DateTimeField('开始时间', null=True, blank=True)
    old_end_time=models.DateTimeField('结束时间', null=True, blank=True)
    old_result_id=models.CharField('维修结果', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('审核日期', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_print_times=models.IntegerField('PrintTimes', null=True, blank=True)
    old_revisions=models.IntegerField('Revisions', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('制单人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('制单日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_handle_idea=models.CharField('HandleIdea', null=True, blank=True, max_length=512)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_photo_address=models.CharField('PhotoAddress', null=True, blank=True, max_length=512)
    old_approve_idea=models.CharField('ApproveIdea', null=True, blank=True, max_length=200)
    old_patrol_detail_no=models.CharField('PatrolDetailNo', null=True, blank=True, max_length=100)
    old_sheet_type=models.CharField('报修类别', null=True, blank=True, max_length=10)
    old_station_id=models.CharField('站别', null=True, blank=True, max_length=30)
    old_business_unit_id=models.CharField('经营单位', null=True, blank=True, max_length=30)
    old_fault_remarks=models.CharField('故障描述', null=True, blank=True, max_length=200)
    old_machine_name=models.CharField('MachineName', null=True, blank=True, max_length=64)
    old_machine_location=models.CharField('MachineLocation', null=True, blank=True, max_length=64)
    old_urgent=models.IntegerField('Urgent', null=True, blank=True)
    old_flow_status=models.CharField('流转状态', null=True, blank=True, max_length=20)
    old_apply_man=models.CharField('ApplyMan', null=True, blank=True, max_length=10)
    old_apply_idea=models.CharField('ApplyIdea', null=True, blank=True, max_length=512)
    old_emp_group=models.CharField('维修分组', null=True, blank=True, max_length=20)
    old_fault_class=models.CharField('故障分类', null=True, blank=True, max_length=500)
    old_machine_class=models.CharField('设备分类', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_machinefault'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_3f1e2f6ea3b86614')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（MachineFault，待确认）'
        ordering=["-id"]

class SourceDyeMachineFaultArticleInfo(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='MachineFaultArticleInfo'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'Rounds': 'old_rounds', 'SerialNum': 'old_serial_num', 'ArticleID': 'old_article_id', 'ArticleName': 'old_article_name', 'Spec': 'old_spec', 'Qty': 'old_qty', 'Kind': 'old_kind', 'Unit': 'old_unit'}
    SOURCE_KEY=('SheetSeries', 'Rounds', 'SerialNum')
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_rounds=models.IntegerField('Rounds', null=False, blank=False)
    old_serial_num=models.IntegerField('SerialNum', null=False, blank=False)
    old_article_id=models.CharField('ArticleID', null=True, blank=True, max_length=100)
    old_article_name=models.CharField('ArticleName', null=True, blank=True, max_length=100)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=100)
    old_qty=models.DecimalField('Qty', null=True, blank=True, max_digits=10, decimal_places=1)
    old_kind=models.IntegerField('Kind', null=True, blank=True)
    old_unit=models.CharField('Unit', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_machinefaultarticleinfo'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_rounds', 'old_serial_num'],name='src_915acc7d946fea9f')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（MachineFaultArticleInfo，待确认）'
        ordering=["-id"]

class SourceDyeMachineFaultComment(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='MachineFaultComment'
    SOURCE_FIELDS={'RecordID': 'old_record_id', 'SheetSeries': 'old_sheet_series', 'SheetDate': 'old_sheet_date', 'Creater': 'old_creater', 'Remark': 'old_remark'}
    SOURCE_KEY=('RecordID',)
    SOURCE_DOCUMENT=True
    old_record_id=models.CharField('RecordID', null=False, blank=True, max_length=50)
    old_sheet_series=models.CharField('SheetSeries', null=True, blank=True, max_length=50)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=20)
    old_remark=models.CharField('Remark', null=True, blank=True, max_length=200)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_machinefaultcomment'
        indexes=[models.Index(fields=['source_batch', 'old_record_id'],name='src_2eee18120ba266a6')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（MachineFaultComment，待确认）'
        ordering=["-id"]

class SourceDyeMachineFaultFilter(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='MachineFaultFilter'
    SOURCE_FIELDS={'FlowType': 'old_flow_type', 'TabID': 'old_tab_id', 'TabTitle': 'old_tab_title', 'FilterSQL': 'old_filter_sql', 'SortNo': 'old_sort_no'}
    SOURCE_KEY=('FlowType', 'TabID')
    SOURCE_DOCUMENT=True
    old_flow_type=models.IntegerField('FlowType', null=False, blank=False)
    old_tab_id=models.CharField('TabID', null=False, blank=True, max_length=10)
    old_tab_title=models.CharField('TabTitle', null=False, blank=True, max_length=20)
    old_filter_sql=models.CharField('FilterSQL', null=False, blank=True, max_length=256)
    old_sort_no=models.IntegerField('SortNo', null=False, blank=False)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_machinefaultfilter'
        indexes=[models.Index(fields=['source_batch', 'old_flow_type', 'old_tab_id'],name='src_e2022cd99c9ccd4b')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（MachineFaultFilter，待确认）'
        ordering=["-id"]

class SourceDyeMachineFaultRecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='MachineFaultRecord'
    SOURCE_FIELDS={'RecordID': 'old_record_id', 'SheetSeries': 'old_sheet_series', 'Operator': 'old_operator', 'Action': 'old_action', 'ActionType': 'old_action_type', 'HandlerIDs': 'old_handler_ids', 'Handlers': 'old_handlers', 'Remark': 'old_remark', 'RecordDate': 'old_record_date', 'Score': 'old_score'}
    SOURCE_KEY=('RecordID',)
    SOURCE_DOCUMENT=False
    old_record_id=models.CharField('RecordID', null=False, blank=True, max_length=50)
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=50)
    old_operator=models.CharField('Operator', null=True, blank=True, max_length=50)
    old_action=models.CharField('Action', null=False, blank=True, max_length=20)
    old_action_type=models.CharField('ActionType', null=False, blank=True, max_length=20)
    old_handler_ids=models.CharField('HandlerIDs', null=True, blank=True, max_length=100)
    old_handlers=models.CharField('Handlers', null=True, blank=True, max_length=200)
    old_remark=models.CharField('Remark', null=False, blank=True, max_length=200)
    old_record_date=models.DateTimeField('RecordDate', null=False, blank=False)
    old_score=models.IntegerField('Score', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_machinefaultrecord'
        indexes=[models.Index(fields=['source_batch', 'old_record_id'],name='src_c9b3c030418792cc')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（MachineFaultRecord，待确认）'
        ordering=["-id"]

class SourceDyeMachines(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='Machines'
    SOURCE_FIELDS={'ID': 'old_id', 'MachineAlias': 'old_machine_alias', 'ConnectType': 'old_connect_type', 'IP': 'old_ip', 'SerialPort': 'old_serial_port', 'Port': 'old_port', 'Baudrate': 'old_baudrate', 'MachineNumber': 'old_machine_number', 'IsHost': 'old_is_host', 'Enabled': 'old_enabled', 'CommPassword': 'old_comm_password', 'UILanguage': 'old_uilanguage', 'DateFormat': 'old_date_format', 'InOutRecordWarn': 'old_in_out_record_warn', 'Idle': 'old_idle', 'Voice': 'old_voice', 'managercount': 'old_managercount', 'usercount': 'old_usercount', 'fingercount': 'old_fingercount', 'SecretCount': 'old_secret_count', 'FirmwareVersion': 'old_firmware_version', 'ProductType': 'old_product_type', 'LockControl': 'old_lock_control', 'Purpose': 'old_purpose', 'ProduceKind': 'old_produce_kind', 'sn': 'old_sn', 'PhotoStamp': 'old_photo_stamp', 'IsIfChangeConfigServer2': 'old_is_if_change_config_server2', 'IsAndroid': 'old_is_android', 'pushver': 'old_pushver', 'P2PUid': 'old_p2_puid'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=True
    old_id=models.IntegerField('ID', null=False, blank=False)
    old_machine_alias=models.CharField('MachineAlias', null=False, blank=True, max_length=20)
    old_connect_type=models.IntegerField('ConnectType', null=False, blank=False)
    old_ip=models.CharField('IP', null=True, blank=True, max_length=20)
    old_serial_port=models.IntegerField('SerialPort', null=True, blank=True)
    old_port=models.IntegerField('Port', null=True, blank=True)
    old_baudrate=models.IntegerField('Baudrate', null=True, blank=True)
    old_machine_number=models.IntegerField('MachineNumber', null=False, blank=False)
    old_is_host=models.BooleanField('IsHost', null=True, blank=True)
    old_enabled=models.BooleanField('Enabled', null=True, blank=True)
    old_comm_password=models.CharField('CommPassword', null=True, blank=True, max_length=12)
    old_uilanguage=models.IntegerField('UILanguage', null=True, blank=True)
    old_date_format=models.IntegerField('DateFormat', null=True, blank=True)
    old_in_out_record_warn=models.IntegerField('InOutRecordWarn', null=True, blank=True)
    old_idle=models.IntegerField('Idle', null=True, blank=True)
    old_voice=models.IntegerField('Voice', null=True, blank=True)
    old_managercount=models.IntegerField('managercount', null=True, blank=True)
    old_usercount=models.IntegerField('usercount', null=True, blank=True)
    old_fingercount=models.IntegerField('fingercount', null=True, blank=True)
    old_secret_count=models.IntegerField('SecretCount', null=True, blank=True)
    old_firmware_version=models.CharField('FirmwareVersion', null=True, blank=True, max_length=20)
    old_product_type=models.CharField('ProductType', null=True, blank=True, max_length=20)
    old_lock_control=models.IntegerField('LockControl', null=True, blank=True)
    old_purpose=models.IntegerField('Purpose', null=True, blank=True)
    old_produce_kind=models.IntegerField('ProduceKind', null=True, blank=True)
    old_sn=models.CharField('sn', null=True, blank=True, max_length=20)
    old_photo_stamp=models.CharField('PhotoStamp', null=True, blank=True, max_length=20)
    old_is_if_change_config_server2=models.IntegerField('IsIfChangeConfigServer2', null=True, blank=True)
    old_is_android=models.CharField('IsAndroid', null=True, blank=True, max_length=1)
    old_pushver=models.IntegerField('pushver', null=True, blank=True)
    old_p2_puid=models.CharField('P2PUid', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_machines'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_263cf1e469fc425e')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（Machines，待确认）'
        ordering=["-id"]

class SourceDyeMoveShiftBill(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='MoveShiftBill'
    SOURCE_FIELDS={'Code': 'old_code', 'EmpID': 'old_emp_id', 'BeginTime': 'old_begin_time', 'DayEnd': 'old_day_end', 'Shift': 'old_shift', 'Creater': 'old_creater', 'Note': 'old_note'}
    SOURCE_KEY=('Code',)
    SOURCE_DOCUMENT=True
    old_code=models.CharField('单据编号', null=False, blank=True, max_length=50)
    old_emp_id=models.CharField('员工ID', null=False, blank=True, max_length=20)
    old_begin_time=models.DateTimeField('开始时间', null=True, blank=True)
    old_day_end=models.DateTimeField('结束时间', null=True, blank=True)
    old_shift=models.CharField('临时考勤班别', null=True, blank=True, max_length=60)
    old_creater=models.CharField('制单人', null=True, blank=True, max_length=8)
    old_note=models.CharField('备注', null=True, blank=True, max_length=512)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_moveshiftbill'
        indexes=[models.Index(fields=['source_batch', 'old_code'],name='src_0d288f7616986c6e')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（MoveShiftBill，待确认）'
        ordering=["-id"]

class SourceDyeOutWorkApply(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='OutWorkApply'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetStatus': 'old_sheet_status', 'FactID': 'old_fact_id', 'ProcessID': 'old_process_id', 'Remarks': 'old_remarks', 'RightStatus': 'old_right_status', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('单号', null=False, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('日期', null=True, blank=True)
    old_sheet_status=models.IntegerField('SheetStatus', null=True, blank=True)
    old_fact_id=models.CharField('部门', null=True, blank=True, max_length=20)
    old_process_id=models.CharField('加工项目', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=500)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_creater=models.CharField('制单人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('制单日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_approver=models.CharField('审批人', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('审批时间', null=True, blank=True)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_print_times=models.IntegerField('PrintTimes', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_outworkapply'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_0e65abb8a2f4a0a8')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（OutWorkApply，待确认）'
        ordering=["-id"]

class SourceDyeOutWorkApplyDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='OutWorkApplyDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'JobTaskSheetNo': 'old_job_task_sheet_no', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'Spec': 'old_spec', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'Packs': 'old_packs', 'Rolls': 'old_rolls', 'Qty': 'old_qty', 'Remarks': 'old_remarks', 'LotNo': 'old_lot_no', 'Price': 'old_price', 'Amount': 'old_amount', 'ReceSheetNo': 'old_rece_sheet_no', 'InSheetKind': 'old_in_sheet_kind', 'FixedQty': 'old_fixed_qty', 'FabricID': 'old_fabric_id', 'PreField1': 'old_pre_field1', 'SupplierID': 'old_supplier_id', 'PurchaseOrders': 'old_purchase_orders', 'A_A': 'old_a_a', 'A_B': 'old_a_b'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=False
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=50)
    old_job_task_sheet_no=models.CharField('卡号', null=True, blank=True, max_length=50)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=20)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=200)
    old_color_id=models.CharField('物料颜色', null=True, blank=True, max_length=150)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=20)
    old_packs=models.DecimalField('件数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_qty=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=500)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=50)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=10, decimal_places=2)
    old_amount=models.DecimalField('金额', null=True, blank=True, max_digits=12, decimal_places=2)
    old_rece_sheet_no=models.CharField('入库明细单号', null=True, blank=True, max_length=30)
    old_in_sheet_kind=models.CharField('物料分类', null=True, blank=True, max_length=10)
    old_fixed_qty=models.DecimalField('锭重', null=True, blank=True, max_digits=5, decimal_places=2)
    old_fabric_id=models.CharField('成品规格', null=True, blank=True, max_length=50)
    old_pre_field1=models.CharField('捻度(H/S)', null=True, blank=True, max_length=50)
    old_supplier_id=models.CharField('供应商', null=True, blank=True, max_length=30)
    old_purchase_orders=models.CharField('采购单号', null=True, blank=True, max_length=20)
    old_a_a=models.CharField('物料区域', null=True, blank=True, max_length=50)
    old_a_b=models.CharField('物料等级', null=True, blank=True, max_length=100)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeOutWorkApply', verbose_name='原关系：OutWorkApply', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_outworkapplydetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_56d0932aa16c36f2')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（OutWorkApplyDetail，待确认）'
        ordering=["-id"]

class SourceDyePlanDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PlanDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'PlanDetailNo': 'old_plan_detail_no', 'SequenceNo': 'old_sequence_no', 'OrderSheetNo': 'old_order_sheet_no', 'CheckNo': 'old_check_no', 'Vats': 'old_vats', 'Rolls': 'old_rolls', 'Qty': 'old_qty', 'StartDate': 'old_start_date', 'FinishDate': 'old_finish_date', 'MainMemo': 'old_main_memo', 'AssignMemo': 'old_assign_memo', 'AtteMemo': 'old_atte_memo', 'ColorMemo': 'old_color_memo', 'ProcessMemo': 'old_process_memo', 'Status': 'old_status', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('PlanDetailNo',)
    SOURCE_DOCUMENT=False
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_plan_detail_no=models.CharField('主计划明细号', null=False, blank=True, max_length=30)
    old_sequence_no=models.BigIntegerField('顺序号', null=False, blank=False)
    old_order_sheet_no=models.CharField('订单号', null=True, blank=True, max_length=20)
    old_check_no=models.CharField('订单明细号', null=True, blank=True, max_length=20)
    old_vats=models.DecimalField('缸数', null=True, blank=True, max_digits=7, decimal_places=1)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_qty=models.DecimalField('数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_start_date=models.DateTimeField('开始日期', null=True, blank=True)
    old_finish_date=models.DateTimeField('预计交货日期', null=True, blank=True)
    old_main_memo=models.CharField('主要说明', null=True, blank=True, max_length=300)
    old_assign_memo=models.CharField('配纱说明', null=True, blank=True, max_length=300)
    old_atte_memo=models.CharField('要求说明', null=True, blank=True, max_length=300)
    old_color_memo=models.CharField('颜色说明', null=True, blank=True, max_length=300)
    old_process_memo=models.CharField('工序说明', null=True, blank=True, max_length=300)
    old_status=models.CharField('状态', null=True, blank=True, max_length=1)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    source_parent_1=models.ForeignKey('erp_production.SourceDyePlanMain', verbose_name='原关系：PlanMain', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_plandetail'
        indexes=[models.Index(fields=['source_batch', 'old_plan_detail_no'],name='src_80c3e933130b7303')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（PlanDetail，待确认）'
        ordering=["-id"]

class SourceDyePlanMain(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PlanMain'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'BusinessUnitID': 'old_business_unit_id', 'SalerGroupID': 'old_saler_group_id', 'SheetStatus': 'old_sheet_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'RightStatus': 'old_right_status', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('业务组别', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_step_no=models.IntegerField('流程节点号', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_planmain'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_f8ba8a481bcb7cdf')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（PlanMain，待确认）'
        ordering=["-id"]

class SourceDyePrePlanOrder(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PrePlanOrder'
    SOURCE_FIELDS={'ID': 'old_id', 'BusinessUnitID': 'old_business_unit_id', 'PlanDate': 'old_plan_date', 'StartDate': 'old_start_date', 'EndDate': 'old_end_date', 'FinishDate': 'old_finish_date', 'ProgramKindID': 'old_program_kind_id', 'CustomerID': 'old_customer_id', 'OrderSheetNo': 'old_order_sheet_no', 'CheckNo': 'old_check_no', 'Vats': 'old_vats', 'Rolls': 'old_rolls', 'Qty': 'old_qty', 'Remarks': 'old_remarks', 'Status': 'old_status', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=True
    old_id=models.BigIntegerField('ID', null=False, blank=False)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_plan_date=models.DateTimeField('PlanDate', null=True, blank=True)
    old_start_date=models.DateTimeField('StartDate', null=True, blank=True)
    old_end_date=models.DateTimeField('EndDate', null=True, blank=True)
    old_finish_date=models.DateTimeField('FinishDate', null=True, blank=True)
    old_program_kind_id=models.CharField('ProgramKindID', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=10)
    old_order_sheet_no=models.CharField('OrderSheetNo', null=True, blank=True, max_length=20)
    old_check_no=models.CharField('CheckNo', null=True, blank=True, max_length=20)
    old_vats=models.DecimalField('Vats', null=True, blank=True, max_digits=7, decimal_places=1)
    old_rolls=models.DecimalField('Rolls', null=True, blank=True, max_digits=7, decimal_places=2)
    old_qty=models.DecimalField('Qty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=100)
    old_status=models.CharField('Status', null=True, blank=True, max_length=1)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_preplanorder'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_cacc6fb879e87a28')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（PrePlanOrder，待确认）'
        ordering=["-id"]

class SourceDyeProcessCraft(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProcessCraft'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'CraftKindID': 'old_craft_kind_id', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'LotNo': 'old_lot_no', 'Spec': 'old_spec', 'Structure': 'old_structure', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'Width': 'old_width', 'Weight': 'old_weight', 'WarpDensity': 'old_warp_density', 'WeftDensity': 'old_weft_density', 'ProcessID': 'old_process_id', 'OrderSheetNo': 'old_order_sheet_no', 'JobSheetNo': 'old_job_sheet_no', 'ColorDepthID': 'old_color_depth_id', 'PPName01': 'old_ppname01', 'Value01': 'old_value01', 'PPName02': 'old_ppname02', 'Value02': 'old_value02', 'PPName03': 'old_ppname03', 'Value03': 'old_value03', 'PPName04': 'old_ppname04', 'Value04': 'old_value04', 'PPName05': 'old_ppname05', 'Value05': 'old_value05', 'PPName06': 'old_ppname06', 'Value06': 'old_value06', 'PPName07': 'old_ppname07', 'Value07': 'old_value07', 'PPName08': 'old_ppname08', 'Value08': 'old_value08', 'PPName09': 'old_ppname09', 'Value09': 'old_value09', 'PPName10': 'old_ppname10', 'Value10': 'old_value10', 'PPName11': 'old_ppname11', 'Value11': 'old_value11', 'PPName12': 'old_ppname12', 'Value12': 'old_value12', 'PPName13': 'old_ppname13', 'Value13': 'old_value13', 'PPName14': 'old_ppname14', 'Value14': 'old_value14', 'PPName15': 'old_ppname15', 'Value15': 'old_value15', 'PPName16': 'old_ppname16', 'Value16': 'old_value16', 'PPName17': 'old_ppname17', 'Value17': 'old_value17', 'PPName18': 'old_ppname18', 'Value18': 'old_value18', 'PPName19': 'old_ppname19', 'Value19': 'old_value19', 'PPName20': 'old_ppname20', 'Value20': 'old_value20', 'PPName21': 'old_ppname21', 'Value21': 'old_value21', 'PPName22': 'old_ppname22', 'Value22': 'old_value22', 'PPName23': 'old_ppname23', 'Value23': 'old_value23', 'PPName24': 'old_ppname24', 'Value24': 'old_value24', 'PPName25': 'old_ppname25', 'Value25': 'old_value25', 'PPName26': 'old_ppname26', 'Value26': 'old_value26', 'PPName27': 'old_ppname27', 'Value27': 'old_value27', 'PPName28': 'old_ppname28', 'Value28': 'old_value28', 'PPName29': 'old_ppname29', 'Value29': 'old_value29', 'PPName30': 'old_ppname30', 'Value30': 'old_value30', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'Maker': 'old_maker', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'CardQty': 'old_card_qty', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'PPName31': 'old_ppname31', 'Value31': 'old_value31', 'PPName32': 'old_ppname32', 'Value32': 'old_value32', 'PPName33': 'old_ppname33', 'Value33': 'old_value33', 'PPName34': 'old_ppname34', 'Value34': 'old_value34', 'PPName35': 'old_ppname35', 'Value35': 'old_value35', 'PPName36': 'old_ppname36', 'Value36': 'old_value36', 'PPName37': 'old_ppname37', 'Value37': 'old_value37', 'PPName38': 'old_ppname38', 'Value38': 'old_value38', 'PPName39': 'old_ppname39', 'Value39': 'old_value39', 'PPName40': 'old_ppname40', 'Value40': 'old_value40', 'PPName41': 'old_ppname41', 'Value41': 'old_value41', 'PPName42': 'old_ppname42', 'Value42': 'old_value42', 'PPName43': 'old_ppname43', 'Value43': 'old_value43', 'PPName44': 'old_ppname44', 'Value44': 'old_value44', 'PPName45': 'old_ppname45', 'Value45': 'old_value45', 'PPName46': 'old_ppname46', 'Value46': 'old_value46', 'PPName47': 'old_ppname47', 'Value47': 'old_value47', 'PPName48': 'old_ppname48', 'Value48': 'old_value48', 'PPName49': 'old_ppname49', 'Value49': 'old_value49', 'PPName50': 'old_ppname50', 'Value50': 'old_value50', 'PPName51': 'old_ppname51', 'Value51': 'old_value51', 'PPName52': 'old_ppname52', 'Value52': 'old_value52', 'PPName53': 'old_ppname53', 'Value53': 'old_value53', 'PPName54': 'old_ppname54', 'Value54': 'old_value54', 'PPName55': 'old_ppname55', 'Value55': 'old_value55', 'PPName56': 'old_ppname56', 'Value56': 'old_value56', 'PPName57': 'old_ppname57', 'Value57': 'old_value57', 'PPName58': 'old_ppname58', 'Value58': 'old_value58', 'PPName59': 'old_ppname59', 'Value59': 'old_value59', 'PPName60': 'old_ppname60', 'Value60': 'old_value60', 'PPName61': 'old_ppname61', 'Value61': 'old_value61', 'PPName62': 'old_ppname62', 'Value62': 'old_value62', 'PPName63': 'old_ppname63', 'Value63': 'old_value63', 'PPName64': 'old_ppname64', 'Value64': 'old_value64', 'PPName65': 'old_ppname65', 'Value65': 'old_value65', 'PPName66': 'old_ppname66', 'Value66': 'old_value66', 'PPName67': 'old_ppname67', 'Value67': 'old_value67', 'PPName68': 'old_ppname68', 'Value68': 'old_value68', 'PPName69': 'old_ppname69', 'Value69': 'old_value69', 'PPName70': 'old_ppname70', 'Value70': 'old_value70', 'AddrDlv': 'old_addr_dlv', 'Model1': 'old_model1', 'DetailCustName': 'old_detail_cust_name', 'MachineID': 'old_machine_id', 'DetailsCustomer': 'old_details_customer', 'PreField1': 'old_pre_field1', 'PreField2': 'old_pre_field2', 'PreField3': 'old_pre_field3', 'PreField4': 'old_pre_field4', 'WeightUnit': 'old_weight_unit', 'WidthKindID': 'old_width_kind_id', 'OrderSheetDate': 'old_order_sheet_date', 'IsFirstVat': 'old_is_first_vat', 'Atte': 'old_atte', 'OriSheetSeries': 'old_ori_sheet_series', 'Date1': 'old_date1', 'Date2': 'old_date2', 'Class1': 'old_class1', 'Class2': 'old_class2', 'Person1': 'old_person1', 'Person2': 'old_person2', 'FProductWidth': 'old_fproduct_width', 'FWeightOfLength': 'old_fweight_of_length', 'PreRolls': 'old_pre_rolls'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类别', null=True, blank=True)
    old_craft_kind_id=models.CharField('工艺类别', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户代码', null=True, blank=True, max_length=10)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=20)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=50)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=128)
    old_structure=models.CharField('组织', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('颜色代码', null=True, blank=True, max_length=20)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=20)
    old_width=models.DecimalField('幅宽', null=True, blank=True, max_digits=6, decimal_places=2)
    old_weight=models.DecimalField('克重', null=True, blank=True, max_digits=6, decimal_places=2)
    old_warp_density=models.DecimalField('经密', null=True, blank=True, max_digits=6, decimal_places=2)
    old_weft_density=models.DecimalField('纬密', null=True, blank=True, max_digits=6, decimal_places=2)
    old_process_id=models.CharField('工序', null=True, blank=True, max_length=10)
    old_order_sheet_no=models.CharField('订单号', null=True, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_color_depth_id=models.CharField('颜色深浅', null=True, blank=True, max_length=10)
    old_ppname01=models.CharField('参数名1', null=True, blank=True, max_length=20)
    old_value01=models.CharField('参数值01', null=True, blank=True, max_length=20)
    old_ppname02=models.CharField('参数名2', null=True, blank=True, max_length=20)
    old_value02=models.CharField('参数值02', null=True, blank=True, max_length=20)
    old_ppname03=models.CharField('参数名3', null=True, blank=True, max_length=20)
    old_value03=models.CharField('参数值03', null=True, blank=True, max_length=20)
    old_ppname04=models.CharField('参数名4', null=True, blank=True, max_length=20)
    old_value04=models.CharField('参数值04', null=True, blank=True, max_length=20)
    old_ppname05=models.CharField('参数名5', null=True, blank=True, max_length=20)
    old_value05=models.CharField('参数值05', null=True, blank=True, max_length=20)
    old_ppname06=models.CharField('参数名6', null=True, blank=True, max_length=20)
    old_value06=models.CharField('参数值06', null=True, blank=True, max_length=20)
    old_ppname07=models.CharField('参数名7', null=True, blank=True, max_length=20)
    old_value07=models.CharField('参数值07', null=True, blank=True, max_length=20)
    old_ppname08=models.CharField('参数名8', null=True, blank=True, max_length=20)
    old_value08=models.CharField('参数值08', null=True, blank=True, max_length=20)
    old_ppname09=models.CharField('参数名9', null=True, blank=True, max_length=20)
    old_value09=models.CharField('参数值09', null=True, blank=True, max_length=20)
    old_ppname10=models.CharField('参数名10', null=True, blank=True, max_length=20)
    old_value10=models.CharField('参数值10', null=True, blank=True, max_length=20)
    old_ppname11=models.CharField('参数名11', null=True, blank=True, max_length=20)
    old_value11=models.CharField('参数值11', null=True, blank=True, max_length=20)
    old_ppname12=models.CharField('参数名12', null=True, blank=True, max_length=20)
    old_value12=models.CharField('参数值12', null=True, blank=True, max_length=20)
    old_ppname13=models.CharField('参数名13', null=True, blank=True, max_length=20)
    old_value13=models.CharField('参数值13', null=True, blank=True, max_length=20)
    old_ppname14=models.CharField('参数名14', null=True, blank=True, max_length=20)
    old_value14=models.CharField('参数值14', null=True, blank=True, max_length=20)
    old_ppname15=models.CharField('参数名15', null=True, blank=True, max_length=20)
    old_value15=models.CharField('参数值15', null=True, blank=True, max_length=20)
    old_ppname16=models.CharField('参数名16', null=True, blank=True, max_length=20)
    old_value16=models.CharField('参数值16', null=True, blank=True, max_length=20)
    old_ppname17=models.CharField('参数名17', null=True, blank=True, max_length=20)
    old_value17=models.CharField('参数值17', null=True, blank=True, max_length=20)
    old_ppname18=models.CharField('参数名18', null=True, blank=True, max_length=20)
    old_value18=models.CharField('参数值18', null=True, blank=True, max_length=20)
    old_ppname19=models.CharField('参数名19', null=True, blank=True, max_length=20)
    old_value19=models.CharField('参数值19', null=True, blank=True, max_length=20)
    old_ppname20=models.CharField('参数名20', null=True, blank=True, max_length=20)
    old_value20=models.CharField('参数值20', null=True, blank=True, max_length=20)
    old_ppname21=models.CharField('参数名21', null=True, blank=True, max_length=20)
    old_value21=models.CharField('参数值21', null=True, blank=True, max_length=20)
    old_ppname22=models.CharField('参数名22', null=True, blank=True, max_length=20)
    old_value22=models.CharField('参数值22', null=True, blank=True, max_length=20)
    old_ppname23=models.CharField('参数名23', null=True, blank=True, max_length=20)
    old_value23=models.CharField('参数值23', null=True, blank=True, max_length=20)
    old_ppname24=models.CharField('参数名24', null=True, blank=True, max_length=20)
    old_value24=models.CharField('参数值24', null=True, blank=True, max_length=20)
    old_ppname25=models.CharField('参数名25', null=True, blank=True, max_length=20)
    old_value25=models.CharField('参数值25', null=True, blank=True, max_length=20)
    old_ppname26=models.CharField('参数名26', null=True, blank=True, max_length=20)
    old_value26=models.CharField('参数值26', null=True, blank=True, max_length=20)
    old_ppname27=models.CharField('参数名27', null=True, blank=True, max_length=20)
    old_value27=models.CharField('参数值27', null=True, blank=True, max_length=20)
    old_ppname28=models.CharField('参数名28', null=True, blank=True, max_length=20)
    old_value28=models.CharField('参数值28', null=True, blank=True, max_length=20)
    old_ppname29=models.CharField('参数名29', null=True, blank=True, max_length=20)
    old_value29=models.CharField('参数值29', null=True, blank=True, max_length=20)
    old_ppname30=models.CharField('参数名30', null=True, blank=True, max_length=20)
    old_value30=models.CharField('参数值30', null=True, blank=True, max_length=20)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_maker=models.CharField('业务人', null=True, blank=True, max_length=10)
    old_step_no=models.IntegerField('工作流节点号', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_card_qty=models.IntegerField('缸数', null=True, blank=True)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_ppname31=models.CharField('PPName31', null=True, blank=True, max_length=20)
    old_value31=models.CharField('Value31', null=True, blank=True, max_length=20)
    old_ppname32=models.CharField('PPName32', null=True, blank=True, max_length=20)
    old_value32=models.CharField('Value32', null=True, blank=True, max_length=20)
    old_ppname33=models.CharField('PPName33', null=True, blank=True, max_length=20)
    old_value33=models.CharField('Value33', null=True, blank=True, max_length=20)
    old_ppname34=models.CharField('PPName34', null=True, blank=True, max_length=20)
    old_value34=models.CharField('Value34', null=True, blank=True, max_length=20)
    old_ppname35=models.CharField('PPName35', null=True, blank=True, max_length=20)
    old_value35=models.CharField('Value35', null=True, blank=True, max_length=20)
    old_ppname36=models.CharField('PPName36', null=True, blank=True, max_length=20)
    old_value36=models.CharField('Value36', null=True, blank=True, max_length=20)
    old_ppname37=models.CharField('PPName37', null=True, blank=True, max_length=20)
    old_value37=models.CharField('Value37', null=True, blank=True, max_length=20)
    old_ppname38=models.CharField('PPName38', null=True, blank=True, max_length=20)
    old_value38=models.CharField('Value38', null=True, blank=True, max_length=20)
    old_ppname39=models.CharField('PPName39', null=True, blank=True, max_length=20)
    old_value39=models.CharField('Value39', null=True, blank=True, max_length=20)
    old_ppname40=models.CharField('PPName40', null=True, blank=True, max_length=20)
    old_value40=models.CharField('Value40', null=True, blank=True, max_length=20)
    old_ppname41=models.CharField('PPName41', null=True, blank=True, max_length=20)
    old_value41=models.CharField('Value41', null=True, blank=True, max_length=20)
    old_ppname42=models.CharField('PPName42', null=True, blank=True, max_length=20)
    old_value42=models.CharField('Value42', null=True, blank=True, max_length=20)
    old_ppname43=models.CharField('PPName43', null=True, blank=True, max_length=20)
    old_value43=models.CharField('Value43', null=True, blank=True, max_length=20)
    old_ppname44=models.CharField('PPName44', null=True, blank=True, max_length=20)
    old_value44=models.CharField('Value44', null=True, blank=True, max_length=20)
    old_ppname45=models.CharField('PPName45', null=True, blank=True, max_length=20)
    old_value45=models.CharField('Value45', null=True, blank=True, max_length=20)
    old_ppname46=models.CharField('PPName46', null=True, blank=True, max_length=20)
    old_value46=models.CharField('Value46', null=True, blank=True, max_length=20)
    old_ppname47=models.CharField('PPName47', null=True, blank=True, max_length=20)
    old_value47=models.CharField('Value47', null=True, blank=True, max_length=20)
    old_ppname48=models.CharField('PPName48', null=True, blank=True, max_length=20)
    old_value48=models.CharField('Value48', null=True, blank=True, max_length=20)
    old_ppname49=models.CharField('PPName49', null=True, blank=True, max_length=20)
    old_value49=models.CharField('Value49', null=True, blank=True, max_length=20)
    old_ppname50=models.CharField('PPName50', null=True, blank=True, max_length=20)
    old_value50=models.CharField('Value50', null=True, blank=True, max_length=20)
    old_ppname51=models.CharField('PPName51', null=True, blank=True, max_length=20)
    old_value51=models.CharField('Value51', null=True, blank=True, max_length=20)
    old_ppname52=models.CharField('PPName52', null=True, blank=True, max_length=20)
    old_value52=models.CharField('Value52', null=True, blank=True, max_length=20)
    old_ppname53=models.CharField('PPName53', null=True, blank=True, max_length=20)
    old_value53=models.CharField('Value53', null=True, blank=True, max_length=20)
    old_ppname54=models.CharField('PPName54', null=True, blank=True, max_length=20)
    old_value54=models.CharField('Value54', null=True, blank=True, max_length=20)
    old_ppname55=models.CharField('PPName55', null=True, blank=True, max_length=20)
    old_value55=models.CharField('Value55', null=True, blank=True, max_length=20)
    old_ppname56=models.CharField('PPName56', null=True, blank=True, max_length=20)
    old_value56=models.CharField('Value56', null=True, blank=True, max_length=20)
    old_ppname57=models.CharField('PPName57', null=True, blank=True, max_length=20)
    old_value57=models.CharField('Value57', null=True, blank=True, max_length=20)
    old_ppname58=models.CharField('PPName58', null=True, blank=True, max_length=20)
    old_value58=models.CharField('Value58', null=True, blank=True, max_length=20)
    old_ppname59=models.CharField('PPName59', null=True, blank=True, max_length=20)
    old_value59=models.CharField('Value59', null=True, blank=True, max_length=20)
    old_ppname60=models.CharField('PPName60', null=True, blank=True, max_length=20)
    old_value60=models.CharField('Value60', null=True, blank=True, max_length=20)
    old_ppname61=models.CharField('PPName61', null=True, blank=True, max_length=20)
    old_value61=models.CharField('Value61', null=True, blank=True, max_length=20)
    old_ppname62=models.CharField('PPName62', null=True, blank=True, max_length=20)
    old_value62=models.CharField('Value62', null=True, blank=True, max_length=20)
    old_ppname63=models.CharField('PPName63', null=True, blank=True, max_length=20)
    old_value63=models.CharField('Value63', null=True, blank=True, max_length=20)
    old_ppname64=models.CharField('PPName64', null=True, blank=True, max_length=20)
    old_value64=models.CharField('Value64', null=True, blank=True, max_length=20)
    old_ppname65=models.CharField('PPName65', null=True, blank=True, max_length=20)
    old_value65=models.CharField('Value65', null=True, blank=True, max_length=20)
    old_ppname66=models.CharField('PPName66', null=True, blank=True, max_length=20)
    old_value66=models.CharField('Value66', null=True, blank=True, max_length=20)
    old_ppname67=models.CharField('PPName67', null=True, blank=True, max_length=20)
    old_value67=models.CharField('Value67', null=True, blank=True, max_length=20)
    old_ppname68=models.CharField('PPName68', null=True, blank=True, max_length=20)
    old_value68=models.CharField('Value68', null=True, blank=True, max_length=20)
    old_ppname69=models.CharField('PPName69', null=True, blank=True, max_length=20)
    old_value69=models.CharField('Value69', null=True, blank=True, max_length=50)
    old_ppname70=models.CharField('PPName70', null=True, blank=True, max_length=20)
    old_value70=models.CharField('Value70', null=True, blank=True, max_length=20)
    old_addr_dlv=models.CharField('客户类型', null=True, blank=True, max_length=50)
    old_model1=models.CharField('模板', null=True, blank=True, max_length=10)
    old_detail_cust_name=models.CharField('明细客户', null=True, blank=True, max_length=50)
    old_machine_id=models.CharField('机号', null=True, blank=True, max_length=50)
    old_details_customer=models.CharField('织厂', null=True, blank=True, max_length=10)
    old_pre_field1=models.CharField('捻度(H/S)', null=True, blank=True, max_length=50)
    old_pre_field2=models.CharField('氨纶', null=True, blank=True, max_length=50)
    old_pre_field3=models.CharField('针数', null=True, blank=True, max_length=50)
    old_pre_field4=models.CharField('寸数', null=True, blank=True, max_length=50)
    old_weight_unit=models.CharField('克重单位', null=True, blank=True, max_length=10)
    old_width_kind_id=models.CharField('门幅单位', null=True, blank=True, max_length=10)
    old_order_sheet_date=models.DateTimeField('下单时间', null=True, blank=True)
    old_is_first_vat=models.BooleanField('是否头缸', null=True, blank=True)
    old_atte=models.CharField('Atte', null=True, blank=True, max_length=512)
    old_ori_sheet_series=models.CharField('OriSheetSeries', null=True, blank=True, max_length=20)
    old_date1=models.DateTimeField('日期', null=True, blank=True)
    old_date2=models.DateTimeField('日期', null=True, blank=True)
    old_class1=models.CharField('班次', null=True, blank=True, max_length=20)
    old_class2=models.CharField('班次', null=True, blank=True, max_length=20)
    old_person1=models.CharField('Person1', null=True, blank=True, max_length=20)
    old_person2=models.CharField('Person2', null=True, blank=True, max_length=20)
    old_fproduct_width=models.CharField('FProductWidth', null=True, blank=True, max_length=50)
    old_fweight_of_length=models.CharField('FWeightOfLength', null=True, blank=True, max_length=50)
    old_pre_rolls=models.DecimalField('PreRolls', null=True, blank=True, max_digits=6, decimal_places=2)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_processcraft'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_f9419984fd2cfb16')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（ProcessCraft，待确认）'
        ordering=["-id"]

class SourceDyeProcessCraftJobNo(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProcessCraftJobNo'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'JobSheetNo': 'old_job_sheet_no', 'Status': 'old_status', 'CurrTime': 'old_curr_time', 'Maker': 'old_maker'}
    SOURCE_KEY=('SheetSeries', 'JobSheetNo')
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('缸号', null=False, blank=True, max_length=50)
    old_status=models.CharField('状态', null=True, blank=True, max_length=1)
    old_curr_time=models.DateTimeField('时间', null=True, blank=True)
    old_maker=models.CharField('Maker', null=True, blank=True, max_length=10)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeProcessCraft', verbose_name='原关系：ProcessCraft', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_processcraftjobno'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_job_sheet_no'],name='src_b61c9b417a25ee6b')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（ProcessCraftJobNo，待确认）'
        ordering=["-id"]

class SourceDyeProcessCraftOrderNo(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProcessCraftOrderNo'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'OrderSheetNo': 'old_order_sheet_no', 'Status': 'old_status', 'CurrTime': 'old_curr_time', 'Maker': 'old_maker'}
    SOURCE_KEY=('SheetSeries', 'OrderSheetNo')
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=20)
    old_order_sheet_no=models.CharField('订单号', null=False, blank=True, max_length=20)
    old_status=models.CharField('状态', null=True, blank=True, max_length=1)
    old_curr_time=models.DateTimeField('时间', null=True, blank=True)
    old_maker=models.CharField('Maker', null=True, blank=True, max_length=10)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeProcessCraft', verbose_name='原关系：ProcessCraft', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_processcraftorderno'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_order_sheet_no'],name='src_eda9d945b36ddf15')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（ProcessCraftOrderNo，待确认）'
        ordering=["-id"]

class SourceDyeProcessSchedule(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProcessSchedule'
    SOURCE_FIELDS={'ID': 'old_id', 'JobSheetNo': 'old_job_sheet_no', 'ProcessNo': 'old_process_no', 'StationID': 'old_station_id', 'ProcessID': 'old_process_id', 'MachineID': 'old_machine_id', 'SequenceNo': 'old_sequence_no', 'Status': 'old_status', 'PlanDate': 'old_plan_date', 'StartTime': 'old_start_time', 'FinishTime': 'old_finish_time', 'TargetMin': 'old_target_min', 'ShiftID': 'old_shift_id', 'ClassID': 'old_class_id', 'ProgramID': 'old_program_id', 'EffiRate': 'old_effi_rate', 'JobSheetSeries': 'old_job_sheet_series', 'RecipeSheetNo': 'old_recipe_sheet_no', 'Remarks': 'old_remarks', 'CombineSheetNos': 'old_combine_sheet_nos', 'WorkSort': 'old_work_sort', 'BusinessUnitID': 'old_business_unit_id', 'ColorID': 'old_color_id', 'ColorRGB': 'old_color_rgb', 'PlanWeightQty': 'old_plan_weight_qty', 'PlanRolls': 'old_plan_rolls', 'Priority': 'old_priority', 'SheetKind': 'old_sheet_kind', 'StereotypesName': 'old_stereotypes_name', 'IsNot': 'old_is_not', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'StepNo': 'old_step_no'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=True
    old_id=models.CharField('自增ID', null=False, blank=True, max_length=50)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=20)
    old_process_no=models.IntegerField('工序号', null=True, blank=True)
    old_station_id=models.CharField('站别', null=True, blank=True, max_length=50)
    old_process_id=models.CharField('工序', null=True, blank=True, max_length=10)
    old_machine_id=models.CharField('机台', null=True, blank=True, max_length=10)
    old_sequence_no=models.BigIntegerField('顺序号', null=True, blank=True)
    old_status=models.CharField('状态', null=True, blank=True, max_length=2)
    old_plan_date=models.DateTimeField('时间', null=True, blank=True)
    old_start_time=models.DateTimeField('开始时间', null=True, blank=True)
    old_finish_time=models.DateTimeField('结束时间', null=True, blank=True)
    old_target_min=models.IntegerField('预计分钟', null=True, blank=True)
    old_shift_id=models.CharField('班组', null=True, blank=True, max_length=10)
    old_class_id=models.CharField('班别', null=True, blank=True, max_length=10)
    old_program_id=models.CharField('前道流程', null=True, blank=True, max_length=50)
    old_effi_rate=models.DecimalField('效率比例', null=True, blank=True, max_digits=6, decimal_places=4)
    old_job_sheet_series=models.CharField('工卡流水号', null=True, blank=True, max_length=20)
    old_recipe_sheet_no=models.CharField('配方单号', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    old_combine_sheet_nos=models.CharField('合缸', null=True, blank=True, max_length=200)
    old_work_sort=models.CharField('WorkSort', null=True, blank=True, max_length=50)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=50)
    old_color_rgb=models.IntegerField('ColorRGB', null=True, blank=True)
    old_plan_weight_qty=models.DecimalField('排产重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_plan_rolls=models.DecimalField('排产粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_priority=models.IntegerField('Priority', null=True, blank=True)
    old_sheet_kind=models.IntegerField('排产类型', null=True, blank=True)
    old_stereotypes_name=models.CharField('缸位', null=True, blank=True, max_length=20)
    old_is_not=models.BooleanField('是否插队', null=True, blank=True)
    old_sheet_status=models.IntegerField('SheetStatus', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('PrintTimes', null=True, blank=True)
    old_revisions=models.IntegerField('Revisions', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_processschedule'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_72b8a097c3f6f5ff')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（ProcessSchedule，待确认）'
        ordering=["-id"]

class SourceDyeProcessSchedulebak(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProcessSchedulebak'
    SOURCE_FIELDS={'ID': 'old_id', 'JobSheetNo': 'old_job_sheet_no', 'ProcessNo': 'old_process_no', 'StationID': 'old_station_id', 'ProcessID': 'old_process_id', 'MachineID': 'old_machine_id', 'SequenceNo': 'old_sequence_no', 'Status': 'old_status', 'PlanDate': 'old_plan_date', 'StartTime': 'old_start_time', 'FinishTime': 'old_finish_time', 'TargetMin': 'old_target_min', 'ShiftID': 'old_shift_id', 'ClassID': 'old_class_id', 'ProgramID': 'old_program_id', 'EffiRate': 'old_effi_rate', 'JobSheetSeries': 'old_job_sheet_series', 'RecipeSheetNo': 'old_recipe_sheet_no', 'Remarks': 'old_remarks', 'CombineSheetNos': 'old_combine_sheet_nos', 'WorkSort': 'old_work_sort', 'BusinessUnitID': 'old_business_unit_id', 'ColorID': 'old_color_id', 'ColorRGB': 'old_color_rgb'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=True
    old_id=models.BigIntegerField('ID', null=False, blank=False)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=20)
    old_process_no=models.IntegerField('ProcessNo', null=True, blank=True)
    old_station_id=models.CharField('StationID', null=True, blank=True, max_length=50)
    old_process_id=models.CharField('ProcessID', null=True, blank=True, max_length=10)
    old_machine_id=models.CharField('MachineID', null=True, blank=True, max_length=10)
    old_sequence_no=models.BigIntegerField('SequenceNo', null=True, blank=True)
    old_status=models.CharField('Status', null=True, blank=True, max_length=2)
    old_plan_date=models.DateTimeField('PlanDate', null=True, blank=True)
    old_start_time=models.DateTimeField('StartTime', null=True, blank=True)
    old_finish_time=models.DateTimeField('FinishTime', null=True, blank=True)
    old_target_min=models.IntegerField('TargetMin', null=True, blank=True)
    old_shift_id=models.CharField('ShiftID', null=True, blank=True, max_length=10)
    old_class_id=models.CharField('ClassID', null=True, blank=True, max_length=10)
    old_program_id=models.CharField('ProgramID', null=True, blank=True, max_length=50)
    old_effi_rate=models.DecimalField('EffiRate', null=True, blank=True, max_digits=6, decimal_places=4)
    old_job_sheet_series=models.CharField('JobSheetSeries', null=True, blank=True, max_length=20)
    old_recipe_sheet_no=models.CharField('RecipeSheetNo', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=100)
    old_combine_sheet_nos=models.CharField('CombineSheetNos', null=True, blank=True, max_length=200)
    old_work_sort=models.CharField('WorkSort', null=True, blank=True, max_length=50)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=50)
    old_color_rgb=models.IntegerField('ColorRGB', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_processschedulebak'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_605aba546ed65af0')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（ProcessSchedulebak，待确认）'
        ordering=["-id"]

class SourceDyePStuffWeight(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PStuffWeight'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'RecipeType': 'old_recipe_type', 'DeptID': 'old_dept_id', 'BusinessUnitID': 'old_business_unit_id', 'PrintSheetNo': 'old_print_sheet_no', 'PrintCode': 'old_print_code', 'CustomerID': 'old_customer_id', 'DetailCustName': 'old_detail_cust_name', 'ProdID': 'old_prod_id', 'PrintQty': 'old_print_qty', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'RightStatus': 'old_right_status'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('印花领料单号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_recipe_type=models.IntegerField('料单类型', null=True, blank=True)
    old_dept_id=models.CharField('部门', null=True, blank=True, max_length=10)
    old_business_unit_id=models.CharField('经营单位', null=True, blank=True, max_length=10)
    old_print_sheet_no=models.CharField('来源单号', null=True, blank=True, max_length=50)
    old_print_code=models.CharField('花号', null=True, blank=True, max_length=50)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=10)
    old_detail_cust_name=models.CharField('明细客户', null=True, blank=True, max_length=150)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=20)
    old_print_qty=models.DecimalField('印花数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_approve_date=models.DateTimeField('审核日期', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_pstuffweight'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_120c0e2b3f74e5dc')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（PStuffWeight，待确认）'
        ordering=["-id"]

class SourceDyePStuffWeightDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PStuffWeightDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'PhaseNo': 'old_phase_no', 'StuffNo': 'old_stuff_no', 'StuffID': 'old_stuff_id', 'StuffType': 'old_stuff_type', 'Rate': 'old_rate', 'UpPercent': 'old_up_percent', 'DownPercent': 'old_down_percent', 'WeightUnit': 'old_weight_unit', 'Dosage': 'old_dosage', 'RecipeUnit': 'old_recipe_unit', 'AddDosage': 'old_add_dosage', 'DetailNote': 'old_detail_note', 'IsConfirmed': 'old_is_confirmed', 'Status': 'old_status', 'OriDosage': 'old_ori_dosage'}
    SOURCE_KEY=('SheetSeries', 'PhaseNo', 'StuffNo')
    SOURCE_DOCUMENT=False
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_phase_no=models.IntegerField('PhaseNo', null=False, blank=False)
    old_stuff_no=models.IntegerField('StuffNo', null=False, blank=False)
    old_stuff_id=models.CharField('StuffID', null=True, blank=True, max_length=10)
    old_stuff_type=models.CharField('StuffType', null=True, blank=True, max_length=1)
    old_rate=models.DecimalField('Rate', null=True, blank=True, max_digits=8, decimal_places=2)
    old_up_percent=models.DecimalField('UpPercent', null=True, blank=True, max_digits=8, decimal_places=2)
    old_down_percent=models.DecimalField('DownPercent', null=True, blank=True, max_digits=8, decimal_places=2)
    old_weight_unit=models.CharField('WeightUnit', null=True, blank=True, max_length=1)
    old_dosage=models.DecimalField('Dosage', null=True, blank=True, max_digits=15, decimal_places=6)
    old_recipe_unit=models.IntegerField('RecipeUnit', null=True, blank=True)
    old_add_dosage=models.DecimalField('AddDosage', null=True, blank=True, max_digits=15, decimal_places=6)
    old_detail_note=models.CharField('DetailNote', null=True, blank=True, max_length=256)
    old_is_confirmed=models.BooleanField('IsConfirmed', null=True, blank=True)
    old_status=models.IntegerField('Status', null=True, blank=True)
    old_ori_dosage=models.DecimalField('OriDosage', null=True, blank=True, max_digits=15, decimal_places=6)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_pstuffweightdetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_phase_no', 'old_stuff_no'],name='src_ac832ef3f8a582c3')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（PStuffWeightDetail，待确认）'
        ordering=["-id"]

class SourceDyePStuffWeightPhase(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PStuffWeightPhase'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'PhaseNo': 'old_phase_no', 'ColorPlateID': 'old_color_plate_id', 'ColorID': 'old_color_id', 'ColorName': 'old_color_name', 'Qty': 'old_qty', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('SheetSeries', 'PhaseNo')
    SOURCE_DOCUMENT=False
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_phase_no=models.IntegerField('色位颜色序号', null=False, blank=False)
    old_color_plate_id=models.CharField('花号色位', null=True, blank=True, max_length=20)
    old_color_id=models.CharField('颜色编号', null=True, blank=True, max_length=500)
    old_color_name=models.CharField('颜色名称', null=True, blank=True, max_length=10)
    old_qty=models.DecimalField('色浆用量', null=True, blank=True, max_digits=6, decimal_places=2)
    old_remarks=models.CharField('颜色备注', null=True, blank=True, max_length=512)
    source_parent_1=models.ForeignKey('erp_production.SourceDyePStuffWeight', verbose_name='原关系：PStuffWeight', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_pstuffweightphase'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_phase_no'],name='src_8e5646a4d3ed89d4')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（PStuffWeightPhase，待确认）'
        ordering=["-id"]

class SourceDyeRecordEmp(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='RecordEmp'
    SOURCE_FIELDS={'BarCode': 'old_bar_code', 'EmpID': 'old_emp_id'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    old_bar_code=models.CharField('条码', null=False, blank=True, max_length=20)
    old_emp_id=models.CharField('业务员代码', null=False, blank=True, max_length=10)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeRecordYield', verbose_name='原关系：RecordYield', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_recordemp'
        indexes=[]
        verbose_name=verbose_name_plural='基础主数据相关表（RecordEmp，待确认）'
        ordering=["-id"]

class SourceDyeSemiOutWorkApply(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SemiOutWorkApply'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetStatus': 'old_sheet_status', 'FactID': 'old_fact_id', 'ProcessID': 'old_process_id', 'Remarks': 'old_remarks', 'RightStatus': 'old_right_status', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'DetailCustName': 'old_detail_cust_name', 'CustomerID': 'old_customer_id'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('单号', null=False, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('日期', null=True, blank=True)
    old_sheet_status=models.IntegerField('SheetStatus', null=True, blank=True)
    old_fact_id=models.CharField('加工厂', null=True, blank=True, max_length=20)
    old_process_id=models.CharField('加工项目', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=500)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_creater=models.CharField('制单人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('制单日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_approver=models.CharField('审批人', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('审批时间', null=True, blank=True)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_print_times=models.IntegerField('PrintTimes', null=True, blank=True)
    old_detail_cust_name=models.CharField('明细客户', null=True, blank=True, max_length=100)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_semioutworkapply'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_56082fc0011c28a7')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（SemiOutWorkApply，待确认）'
        ordering=["-id"]

class SourceDyeSemiOutWorkApplyDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SemiOutWorkApplyDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'JobTaskSheetNo': 'old_job_task_sheet_no', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'Spec': 'old_spec', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'Packs': 'old_packs', 'Rolls': 'old_rolls', 'Qty': 'old_qty', 'Remarks': 'old_remarks', 'LotNo': 'old_lot_no', 'Price': 'old_price', 'Amount': 'old_amount', 'ReceSheetNo': 'old_rece_sheet_no', 'InSheetKind': 'old_in_sheet_kind', 'FixedQty': 'old_fixed_qty', 'FabricID': 'old_fabric_id', 'PreField1': 'old_pre_field1', 'SupplierID': 'old_supplier_id', 'PurchaseOrders': 'old_purchase_orders', 'A_A': 'old_a_a', 'A_B': 'old_a_b', 'CheckNo': 'old_check_no', 'DetailCustName': 'old_detail_cust_name', 'ColorRemarks': 'old_color_remarks', 'CustSelfNo': 'old_cust_self_no', 'ContractNo': 'old_contract_no', 'OrderSheetNo': 'old_order_sheet_no', 'OrderRemarks': 'old_order_remarks', 'WorkMaterials': 'old_work_materials'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=False
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=50)
    old_job_task_sheet_no=models.CharField('卡号', null=True, blank=True, max_length=50)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=20)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=200)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=150)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=20)
    old_packs=models.DecimalField('件数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_qty=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=500)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=50)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=10, decimal_places=2)
    old_amount=models.DecimalField('金额', null=True, blank=True, max_digits=12, decimal_places=2)
    old_rece_sheet_no=models.CharField('入库明细单号', null=True, blank=True, max_length=30)
    old_in_sheet_kind=models.CharField('入库类别', null=True, blank=True, max_length=10)
    old_fixed_qty=models.DecimalField('锭重', null=True, blank=True, max_digits=5, decimal_places=2)
    old_fabric_id=models.CharField('客户规格', null=True, blank=True, max_length=50)
    old_pre_field1=models.CharField('捻度(H/S)', null=True, blank=True, max_length=50)
    old_supplier_id=models.CharField('供应商', null=True, blank=True, max_length=30)
    old_purchase_orders=models.CharField('采购单号', null=True, blank=True, max_length=20)
    old_a_a=models.CharField('物料区域', null=True, blank=True, max_length=50)
    old_a_b=models.CharField('A_B', null=True, blank=True, max_length=100)
    old_check_no=models.CharField('订单明细号', null=True, blank=True, max_length=30)
    old_detail_cust_name=models.CharField('明细客户', null=True, blank=True, max_length=20)
    old_color_remarks=models.CharField('用途', null=True, blank=True, max_length=200)
    old_cust_self_no=models.CharField('制单号', null=True, blank=True, max_length=200)
    old_contract_no=models.CharField('客户单号', null=True, blank=True, max_length=200)
    old_order_sheet_no=models.CharField('订单号', null=True, blank=True, max_length=50)
    old_order_remarks=models.CharField('订单备注', null=True, blank=True, max_length=200)
    old_work_materials=models.BooleanField('是否包工包料', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeSemiOutWorkApply', verbose_name='原关系：SemiOutWorkApply', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_semioutworkapplydetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_69505c4cb8fb1d2d')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（SemiOutWorkApplyDetail，待确认）'
        ordering=["-id"]

class SourceDyeShiftArrange(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ShiftArrange'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'DeptID': 'old_dept_id', 'Remarks': 'old_remarks', 'Creator': 'old_creator', 'CreateDate': 'old_create_date', 'Modifier': 'old_modifier', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'RightStatus': 'old_right_status', 'ShiftID': 'old_shift_id', 'StartTime': 'old_start_time', 'EndTime': 'old_end_time', 'SumShiftCount': 'old_sum_shift_count'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('单据流水号', null=False, blank=True, max_length=50)
    old_sheet_no=models.CharField('单号', null=True, blank=True, max_length=50)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_dept_id=models.CharField('部门', null=True, blank=True, max_length=10)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=500)
    old_creator=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifier=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=10)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_shift_id=models.CharField('默认班别', null=True, blank=True, max_length=10)
    old_start_time=models.DateTimeField('StartTime', null=True, blank=True)
    old_end_time=models.DateTimeField('EndTime', null=True, blank=True)
    old_sum_shift_count=models.IntegerField('SumShiftCount', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_shiftarrange'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_60030dd92400d02f')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（ShiftArrange，待确认）'
        ordering=["-id"]

class SourceDyeShiftArrangeDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ShiftArrangeDetail'
    SOURCE_FIELDS={'Sheetseries': 'old_sheetseries', 'DetailNo': 'old_detail_no', 'ShiftID': 'old_shift_id', 'EmpID': 'old_emp_id', 'DeptID': 'old_dept_id', 'Post': 'old_post', 'EffiRate': 'old_effi_rate'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    old_sheetseries=models.CharField('表单流水号', null=False, blank=True, max_length=50)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=50)
    old_shift_id=models.CharField('班组名称', null=True, blank=True, max_length=10)
    old_emp_id=models.CharField('员工', null=True, blank=True, max_length=10)
    old_dept_id=models.CharField('部门', null=True, blank=True, max_length=10)
    old_post=models.CharField('岗位', null=True, blank=True, max_length=30)
    old_effi_rate=models.DecimalField('比例', null=True, blank=True, max_digits=6, decimal_places=2)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_shiftarrangedetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_576c8688bd2a4e78')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（ShiftArrangeDetail，待确认）'
        ordering=["-id"]

class SourceDyeShiftPlan(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ShiftPlan'
    SOURCE_FIELDS={'ClassID': 'old_class_id', 'ShiftName': 'old_shift_name', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer', 'SheetSeries': 'old_sheet_series', 'ShiftID': 'old_shift_id', 'BeginDate': 'old_begin_date', 'EndDate': 'old_end_date', 'BeginTime': 'old_begin_time', 'EndTime': 'old_end_time'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_class_id=models.CharField('班组', null=True, blank=True, max_length=10)
    old_shift_name=models.CharField('排班名称', null=True, blank=True, max_length=60)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=50)
    old_shift_id=models.CharField('排班编码', null=False, blank=True, max_length=20)
    old_begin_date=models.IntegerField('排班开始日期', null=False, blank=False)
    old_end_date=models.IntegerField('排班结束日期', null=False, blank=False)
    old_begin_time=models.CharField('上班时间', null=True, blank=True, max_length=20)
    old_end_time=models.CharField('下班时间', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_shiftplan'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_0cefecfe73c7d7dd')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（ShiftPlan，待确认）'
        ordering=["-id"]

class SourceDyeShiftPlanDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ShiftPlanDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'ShiftDay': 'old_shift_day', 'BeginTime': 'old_begin_time', 'EndTime': 'old_end_time', 'IsHoliday': 'old_is_holiday', 'DetailNo': 'old_detail_no'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=50)
    old_shift_day=models.CharField('日期', null=False, blank=True, max_length=10)
    old_begin_time=models.CharField('上班时间', null=True, blank=True, max_length=20)
    old_end_time=models.CharField('下班时间', null=True, blank=True, max_length=20)
    old_is_holiday=models.BooleanField('是否假日', null=True, blank=True)
    old_detail_no=models.CharField('明细号', null=False, blank=True, max_length=50)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeShiftPlan', verbose_name='原关系：ShiftPlan', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_shiftplandetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_6982263b47644f32')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（ShiftPlanDetail，待确认）'
        ordering=["-id"]

class SourceDyeStandCraft(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StandCraft'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'LotNo': 'old_lot_no', 'Spec': 'old_spec', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'JobSheetNo': 'old_job_sheet_no', 'ColorDepthID': 'old_color_depth_id', 'ProductionID': 'old_production_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'Maker': 'old_maker', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'CraftKindID': 'old_craft_kind_id', 'Structure': 'old_structure', 'WeftDensity': 'old_weft_density', 'WarpDensity': 'old_warp_density', 'Weight': 'old_weight', 'Width': 'old_width', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'BusinessUnitID': 'old_business_unit_id'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=120)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('SheetKind', null=True, blank=True)
    old_customer_id=models.CharField('客户代码', null=True, blank=True, max_length=10)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=20)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=200)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=128)
    old_color_id=models.CharField('颜色代码', null=True, blank=True, max_length=20)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_color_depth_id=models.CharField('颜色深浅', null=True, blank=True, max_length=10)
    old_production_id=models.CharField('生产工艺编码', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_maker=models.CharField('业务人', null=True, blank=True, max_length=10)
    old_step_no=models.IntegerField('流程节点号', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_craft_kind_id=models.CharField('工艺类别', null=True, blank=True, max_length=10)
    old_structure=models.CharField('组织', null=True, blank=True, max_length=50)
    old_weft_density=models.CharField('WeftDensity', null=True, blank=True, max_length=32)
    old_warp_density=models.CharField('WarpDensity', null=True, blank=True, max_length=32)
    old_weight=models.DecimalField('Weight', null=True, blank=True, max_digits=6, decimal_places=2)
    old_width=models.CharField('Width', null=True, blank=True, max_length=32)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_business_unit_id=models.CharField('经营单位', null=True, blank=True, max_length=16)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_standcraft'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_d3be71b9c2f29be7')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（StandCraft，待确认）'
        ordering=["-id"]

class SourceDyeStandCraftBeforeDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StandCraftBeforeDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'ProcessNo': 'old_process_no', 'ProcessID': 'old_process_id', 'StationID': 'old_station_id', 'Remarks': 'old_remarks', 'MachineID': 'old_machine_id', 'LastTime': 'old_last_time', 'PPName01': 'old_ppname01', 'Value01': 'old_value01', 'PPName02': 'old_ppname02', 'Value02': 'old_value02', 'PPName03': 'old_ppname03', 'Value03': 'old_value03', 'PPName04': 'old_ppname04', 'Value04': 'old_value04', 'PPName05': 'old_ppname05', 'Value05': 'old_value05', 'PPName06': 'old_ppname06', 'Value06': 'old_value06', 'PPName07': 'old_ppname07', 'Value07': 'old_value07', 'PPName08': 'old_ppname08', 'Value08': 'old_value08', 'PPName09': 'old_ppname09', 'Value09': 'old_value09', 'PPName10': 'old_ppname10', 'Value10': 'old_value10', 'PPName11': 'old_ppname11', 'Value11': 'old_value11', 'PPName12': 'old_ppname12', 'Value12': 'old_value12', 'PPName13': 'old_ppname13', 'Value13': 'old_value13', 'PPName14': 'old_ppname14', 'Value14': 'old_value14', 'PPName15': 'old_ppname15', 'Value15': 'old_value15', 'PPName16': 'old_ppname16', 'Value16': 'old_value16', 'PPName17': 'old_ppname17', 'Value17': 'old_value17', 'PPName18': 'old_ppname18', 'Value18': 'old_value18', 'PPName19': 'old_ppname19', 'Value19': 'old_value19', 'PPName20': 'old_ppname20', 'Value20': 'old_value20', 'Status': 'old_status', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer'}
    SOURCE_KEY=('SheetSeries', 'ProcessNo')
    SOURCE_DOCUMENT=False
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_process_no=models.IntegerField('ProcessNo', null=False, blank=False)
    old_process_id=models.CharField('ProcessID', null=True, blank=True, max_length=10)
    old_station_id=models.CharField('StationID', null=True, blank=True, max_length=10)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_machine_id=models.CharField('MachineID', null=True, blank=True, max_length=10)
    old_last_time=models.IntegerField('LastTime', null=True, blank=True)
    old_ppname01=models.CharField('PPName01', null=True, blank=True, max_length=20)
    old_value01=models.CharField('Value01', null=True, blank=True, max_length=20)
    old_ppname02=models.CharField('PPName02', null=True, blank=True, max_length=20)
    old_value02=models.CharField('Value02', null=True, blank=True, max_length=20)
    old_ppname03=models.CharField('PPName03', null=True, blank=True, max_length=20)
    old_value03=models.CharField('Value03', null=True, blank=True, max_length=20)
    old_ppname04=models.CharField('PPName04', null=True, blank=True, max_length=20)
    old_value04=models.CharField('Value04', null=True, blank=True, max_length=20)
    old_ppname05=models.CharField('PPName05', null=True, blank=True, max_length=20)
    old_value05=models.CharField('Value05', null=True, blank=True, max_length=20)
    old_ppname06=models.CharField('PPName06', null=True, blank=True, max_length=20)
    old_value06=models.CharField('Value06', null=True, blank=True, max_length=20)
    old_ppname07=models.CharField('PPName07', null=True, blank=True, max_length=20)
    old_value07=models.CharField('Value07', null=True, blank=True, max_length=20)
    old_ppname08=models.CharField('PPName08', null=True, blank=True, max_length=20)
    old_value08=models.CharField('Value08', null=True, blank=True, max_length=20)
    old_ppname09=models.CharField('PPName09', null=True, blank=True, max_length=20)
    old_value09=models.CharField('Value09', null=True, blank=True, max_length=20)
    old_ppname10=models.CharField('PPName10', null=True, blank=True, max_length=20)
    old_value10=models.CharField('Value10', null=True, blank=True, max_length=20)
    old_ppname11=models.CharField('PPName11', null=True, blank=True, max_length=20)
    old_value11=models.CharField('Value11', null=True, blank=True, max_length=20)
    old_ppname12=models.CharField('PPName12', null=True, blank=True, max_length=20)
    old_value12=models.CharField('Value12', null=True, blank=True, max_length=20)
    old_ppname13=models.CharField('PPName13', null=True, blank=True, max_length=20)
    old_value13=models.CharField('Value13', null=True, blank=True, max_length=20)
    old_ppname14=models.CharField('PPName14', null=True, blank=True, max_length=20)
    old_value14=models.CharField('Value14', null=True, blank=True, max_length=20)
    old_ppname15=models.CharField('PPName15', null=True, blank=True, max_length=20)
    old_value15=models.CharField('Value15', null=True, blank=True, max_length=20)
    old_ppname16=models.CharField('PPName16', null=True, blank=True, max_length=20)
    old_value16=models.CharField('Value16', null=True, blank=True, max_length=20)
    old_ppname17=models.CharField('PPName17', null=True, blank=True, max_length=20)
    old_value17=models.CharField('Value17', null=True, blank=True, max_length=20)
    old_ppname18=models.CharField('PPName18', null=True, blank=True, max_length=20)
    old_value18=models.CharField('Value18', null=True, blank=True, max_length=20)
    old_ppname19=models.CharField('PPName19', null=True, blank=True, max_length=20)
    old_value19=models.CharField('Value19', null=True, blank=True, max_length=20)
    old_ppname20=models.CharField('PPName20', null=True, blank=True, max_length=20)
    old_value20=models.CharField('Value20', null=True, blank=True, max_length=20)
    old_status=models.CharField('Status', null=True, blank=True, max_length=2)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_standcraftbeforedetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_process_no'],name='src_76cf4f76a6dbb997')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（StandCraftBeforeDetail，待确认）'
        ordering=["-id"]

class SourceDyeStandCraftDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StandCraftDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'ProcessNo': 'old_process_no', 'ProcessID': 'old_process_id', 'Remarks': 'old_remarks', 'MachineID': 'old_machine_id', 'PPName01': 'old_ppname01', 'Value01': 'old_value01', 'PPName02': 'old_ppname02', 'Value02': 'old_value02', 'PPName03': 'old_ppname03', 'Value03': 'old_value03', 'PPName04': 'old_ppname04', 'Value04': 'old_value04', 'PPName05': 'old_ppname05', 'Value05': 'old_value05', 'PPName06': 'old_ppname06', 'Value06': 'old_value06', 'PPName07': 'old_ppname07', 'Value07': 'old_value07', 'PPName08': 'old_ppname08', 'Value08': 'old_value08', 'PPName09': 'old_ppname09', 'Value09': 'old_value09', 'PPName10': 'old_ppname10', 'Value10': 'old_value10', 'PPName11': 'old_ppname11', 'Value11': 'old_value11', 'PPName12': 'old_ppname12', 'Value12': 'old_value12', 'PPName13': 'old_ppname13', 'Value13': 'old_value13', 'PPName14': 'old_ppname14', 'Value14': 'old_value14', 'PPName15': 'old_ppname15', 'Value15': 'old_value15', 'PPName16': 'old_ppname16', 'Value16': 'old_value16', 'PPName17': 'old_ppname17', 'Value17': 'old_value17', 'PPName18': 'old_ppname18', 'Value18': 'old_value18', 'PPName19': 'old_ppname19', 'Value19': 'old_value19', 'PPName20': 'old_ppname20', 'Value20': 'old_value20', 'Status': 'old_status', 'StationID': 'old_station_id', 'LastTime': 'old_last_time'}
    SOURCE_KEY=('SheetSeries', 'ProcessNo')
    SOURCE_DOCUMENT=False
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=120)
    old_process_no=models.IntegerField('工序号', null=False, blank=False)
    old_process_id=models.CharField('工序代码', null=True, blank=True, max_length=10)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_machine_id=models.CharField('机台编码', null=True, blank=True, max_length=10)
    old_ppname01=models.CharField('参数名1', null=True, blank=True, max_length=20)
    old_value01=models.CharField('标准值01', null=True, blank=True, max_length=20)
    old_ppname02=models.CharField('参数名2', null=True, blank=True, max_length=20)
    old_value02=models.CharField('标准值02', null=True, blank=True, max_length=20)
    old_ppname03=models.CharField('参数名3', null=True, blank=True, max_length=20)
    old_value03=models.CharField('标准值03', null=True, blank=True, max_length=20)
    old_ppname04=models.CharField('参数名4', null=True, blank=True, max_length=20)
    old_value04=models.CharField('标准值04', null=True, blank=True, max_length=20)
    old_ppname05=models.CharField('参数名5', null=True, blank=True, max_length=20)
    old_value05=models.CharField('标准值05', null=True, blank=True, max_length=20)
    old_ppname06=models.CharField('参数名6', null=True, blank=True, max_length=20)
    old_value06=models.CharField('标准值06', null=True, blank=True, max_length=20)
    old_ppname07=models.CharField('参数名7', null=True, blank=True, max_length=20)
    old_value07=models.CharField('标准值07', null=True, blank=True, max_length=20)
    old_ppname08=models.CharField('参数名8', null=True, blank=True, max_length=20)
    old_value08=models.CharField('标准值08', null=True, blank=True, max_length=20)
    old_ppname09=models.CharField('参数名9', null=True, blank=True, max_length=20)
    old_value09=models.CharField('标准值09', null=True, blank=True, max_length=20)
    old_ppname10=models.CharField('参数名10', null=True, blank=True, max_length=20)
    old_value10=models.CharField('标准值10', null=True, blank=True, max_length=20)
    old_ppname11=models.CharField('参数名11', null=True, blank=True, max_length=20)
    old_value11=models.CharField('标准值11', null=True, blank=True, max_length=20)
    old_ppname12=models.CharField('参数名12', null=True, blank=True, max_length=20)
    old_value12=models.CharField('标准值12', null=True, blank=True, max_length=20)
    old_ppname13=models.CharField('参数名13', null=True, blank=True, max_length=20)
    old_value13=models.CharField('标准值13', null=True, blank=True, max_length=20)
    old_ppname14=models.CharField('参数名14', null=True, blank=True, max_length=20)
    old_value14=models.CharField('标准值14', null=True, blank=True, max_length=20)
    old_ppname15=models.CharField('参数名15', null=True, blank=True, max_length=20)
    old_value15=models.CharField('标准值15', null=True, blank=True, max_length=20)
    old_ppname16=models.CharField('参数名16', null=True, blank=True, max_length=20)
    old_value16=models.CharField('标准值16', null=True, blank=True, max_length=20)
    old_ppname17=models.CharField('参数名17', null=True, blank=True, max_length=20)
    old_value17=models.CharField('标准值17', null=True, blank=True, max_length=20)
    old_ppname18=models.CharField('参数名18', null=True, blank=True, max_length=20)
    old_value18=models.CharField('标准值18', null=True, blank=True, max_length=20)
    old_ppname19=models.CharField('参数名19', null=True, blank=True, max_length=20)
    old_value19=models.CharField('标准值19', null=True, blank=True, max_length=20)
    old_ppname20=models.CharField('参数名20', null=True, blank=True, max_length=20)
    old_value20=models.CharField('标准值20', null=True, blank=True, max_length=20)
    old_status=models.CharField('状态', null=True, blank=True, max_length=1)
    old_station_id=models.CharField('站别代码', null=True, blank=True, max_length=10)
    old_last_time=models.IntegerField('LastTime', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeStandCraft', verbose_name='原关系：StandCraft', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_standcraftdetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_process_no'],name='src_aded76e8909c35df')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（StandCraftDetail，待确认）'
        ordering=["-id"]

class SourceDyeStandCraftJobNo(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StandCraftJobNo'
    SOURCE_FIELDS={'JobSheetNo': 'old_job_sheet_no', 'Status': 'old_status', 'CurrTime': 'old_curr_time', 'SheetSeries': 'old_sheet_series', 'Maker': 'old_maker'}
    SOURCE_KEY=('SheetSeries', 'JobSheetNo')
    SOURCE_DOCUMENT=True
    old_job_sheet_no=models.CharField('缸号', null=False, blank=True, max_length=50)
    old_status=models.CharField('状态', null=True, blank=True, max_length=1)
    old_curr_time=models.DateTimeField('当前时间', null=True, blank=True)
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_maker=models.CharField('制单人', null=True, blank=True, max_length=10)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeStandCraft', verbose_name='原关系：StandCraft', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_standcraftjobno'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_job_sheet_no'],name='src_b8fff1dee228310f')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（StandCraftJobNo，待确认）'
        ordering=["-id"]

class SourceDyeSterotypeTech(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SterotypeTech'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'JobSheetNo': 'old_job_sheet_no', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'WeightQtyOrRolls': 'old_weight_qty_or_rolls', 'TechColorNum': 'old_tech_color_num', 'Width': 'old_width', 'Weight': 'old_weight', 'AddrDlv': 'old_addr_dlv', 'ProductionID': 'old_production_id', 'DQDataWidth': 'old_dqdata_width', 'DQDataWeight': 'old_dqdata_weight', 'DQDataNumber': 'old_dqdata_number', 'DQDataXHWidth': 'old_dqdata_xhwidth', 'DQDataXHWeight': 'old_dqdata_xhweight', 'DQDataXHNumber': 'old_dqdata_xhnumber', 'HGTechTemperature': 'old_hgtech_temperature', 'HGTechSpeed': 'old_hgtech_speed', 'HGTechQty': 'old_hgtech_qty', 'HGTechWindPower': 'old_hgtech_wind_power', 'HGTechSmoke': 'old_hgtech_smoke', 'HGTechBrush': 'old_hgtech_brush', 'HGTechOverfeeding': 'old_hgtech_overfeeding', 'QDTechTemperature': 'old_qdtech_temperature', 'QDTechSpeed': 'old_qdtech_speed', 'QDTechQty': 'old_qdtech_qty', 'QDTechWindPower': 'old_qdtech_wind_power', 'QDTechSmoke': 'old_qdtech_smoke', 'QDTechBrush': 'old_qdtech_brush', 'QDTechOverfeeding': 'old_qdtech_overfeeding', 'QDTechJJWidth': 'old_qdtech_jjwidth', 'QDTechSJNumber': 'old_qdtech_sjnumber', 'QDTechXJWidth': 'old_qdtech_xjwidth', 'QDTechXJNumber': 'old_qdtech_xjnumber', 'QDTechWeight': 'old_qdtech_weight', 'QDTechAuxiliary': 'old_qdtech_auxiliary', 'CDTechTemperature': 'old_cdtech_temperature', 'CDTechSpeed': 'old_cdtech_speed', 'CDTechQty': 'old_cdtech_qty', 'CDTechWindPower': 'old_cdtech_wind_power', 'CDTechSmoke': 'old_cdtech_smoke', 'CDTechBrush': 'old_cdtech_brush', 'CDTechOverfeeding': 'old_cdtech_overfeeding', 'CDTechDQWidth': 'old_cdtech_dqwidth', 'CDTechJJWidth': 'old_cdtech_jjwidth', 'CDTechSJNumber': 'old_cdtech_sjnumber', 'CDTechXJWidth': 'old_cdtech_xjwidth', 'CDTechXJNumber': 'old_cdtech_xjnumber', 'CDTechWeight': 'old_cdtech_weight', 'CDTechAuxiliary': 'old_cdtech_auxiliary', 'Demand': 'old_demand', 'Remarks': 'old_remarks', 'RightStatus': 'old_right_status', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'SheetStatus': 'old_sheet_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单号', null=False, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=30)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=20)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_weight_qty_or_rolls=models.CharField('重量/缸数', null=True, blank=True, max_length=20)
    old_tech_color_num=models.CharField('工艺色号', null=True, blank=True, max_length=20)
    old_width=models.CharField('Width', null=True, blank=True, max_length=20)
    old_weight=models.CharField('Weight', null=True, blank=True, max_length=20)
    old_addr_dlv=models.CharField('织纱厂名', null=True, blank=True, max_length=100)
    old_production_id=models.CharField('工艺路线', null=True, blank=True, max_length=100)
    old_dqdata_width=models.CharField('定前资料幅宽', null=True, blank=True, max_length=20)
    old_dqdata_weight=models.CharField('定前资料克重', null=True, blank=True, max_length=20)
    old_dqdata_number=models.CharField('定前资料线数', null=True, blank=True, max_length=20)
    old_dqdata_xhwidth=models.CharField('定前资料洗后幅宽', null=True, blank=True, max_length=20)
    old_dqdata_xhweight=models.CharField('定前资料洗后克重', null=True, blank=True, max_length=20)
    old_dqdata_xhnumber=models.CharField('定前资料洗后线数', null=True, blank=True, max_length=20)
    old_hgtech_temperature=models.CharField('烘干工艺温度', null=True, blank=True, max_length=20)
    old_hgtech_speed=models.CharField('烘干工艺车速', null=True, blank=True, max_length=20)
    old_hgtech_qty=models.CharField('烘干工艺张力', null=True, blank=True, max_length=20)
    old_hgtech_wind_power=models.CharField('烘干工艺风力', null=True, blank=True, max_length=20)
    old_hgtech_smoke=models.CharField('烘干工艺排烟', null=True, blank=True, max_length=20)
    old_hgtech_brush=models.CharField('烘干工艺毛刷', null=True, blank=True, max_length=20)
    old_hgtech_overfeeding=models.CharField('烘干工艺超喂', null=True, blank=True, max_length=20)
    old_qdtech_temperature=models.CharField('定前工艺温度', null=True, blank=True, max_length=20)
    old_qdtech_speed=models.CharField('定前工艺车速', null=True, blank=True, max_length=20)
    old_qdtech_qty=models.CharField('定前工艺张力', null=True, blank=True, max_length=20)
    old_qdtech_wind_power=models.CharField('定前工艺风力', null=True, blank=True, max_length=20)
    old_qdtech_smoke=models.CharField('定前工艺排烟', null=True, blank=True, max_length=20)
    old_qdtech_brush=models.CharField('定前工艺毛刷', null=True, blank=True, max_length=20)
    old_qdtech_overfeeding=models.CharField('定前工艺超喂', null=True, blank=True, max_length=20)
    old_qdtech_jjwidth=models.CharField('定前工艺机架幅宽', null=True, blank=True, max_length=20)
    old_qdtech_sjnumber=models.CharField('定前工艺上级线数', null=True, blank=True, max_length=20)
    old_qdtech_xjwidth=models.CharField('定前工艺下机幅宽', null=True, blank=True, max_length=20)
    old_qdtech_xjnumber=models.CharField('定前工艺下机线数', null=True, blank=True, max_length=20)
    old_qdtech_weight=models.CharField('定前工艺克重', null=True, blank=True, max_length=20)
    old_qdtech_auxiliary=models.CharField('定前工艺助剂', null=True, blank=True, max_length=100)
    old_cdtech_temperature=models.CharField('成定工艺温度', null=True, blank=True, max_length=20)
    old_cdtech_speed=models.CharField('成定工艺车速', null=True, blank=True, max_length=20)
    old_cdtech_qty=models.CharField('成定工艺张力', null=True, blank=True, max_length=20)
    old_cdtech_wind_power=models.CharField('成定工艺风力', null=True, blank=True, max_length=20)
    old_cdtech_smoke=models.CharField('成定工艺排烟', null=True, blank=True, max_length=20)
    old_cdtech_brush=models.CharField('成定工艺毛刷', null=True, blank=True, max_length=20)
    old_cdtech_overfeeding=models.CharField('成定工艺超喂', null=True, blank=True, max_length=20)
    old_cdtech_dqwidth=models.CharField('成定工艺定前幅宽', null=True, blank=True, max_length=20)
    old_cdtech_jjwidth=models.CharField('成定工艺机架幅宽', null=True, blank=True, max_length=20)
    old_cdtech_sjnumber=models.CharField('成定工艺上机线数', null=True, blank=True, max_length=20)
    old_cdtech_xjwidth=models.CharField('成定工艺下机幅宽', null=True, blank=True, max_length=20)
    old_cdtech_xjnumber=models.CharField('成定工艺下机线数', null=True, blank=True, max_length=20)
    old_cdtech_weight=models.CharField('成定工艺克重', null=True, blank=True, max_length=20)
    old_cdtech_auxiliary=models.CharField('成定工艺助剂', null=True, blank=True, max_length=100)
    old_demand=models.CharField('客户要求', null=True, blank=True, max_length=800)
    old_remarks=models.CharField('备注信息', null=True, blank=True, max_length=500)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_step_no=models.IntegerField('节点号', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_sterotypetech'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_3c084e3b07bc8850')]
        verbose_name=verbose_name_plural='其他或待确认相关表（SterotypeTech，待确认）'
        ordering=["-id"]

class SourceDyeStuffCombineSheets(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StuffCombineSheets'
    SOURCE_FIELDS={'StuffSheetNo': 'old_stuff_sheet_no', 'SheetDate': 'old_sheet_date', 'JobSheetNo': 'old_job_sheet_no'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    old_stuff_sheet_no=models.CharField('StuffSheetNo', null=True, blank=True, max_length=30)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=30)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_stuffcombinesheets'
        indexes=[]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（StuffCombineSheets，待确认）'
        ordering=["-id"]

class SourceDyeStuffDeptApply(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StuffDeptApply'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'RightStatus': 'old_right_status'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('SheetNo', null=False, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_stuffdeptapply'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_ed17da35de4753bf')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（StuffDeptApply，待确认）'
        ordering=["-id"]

class SourceDyeStuffDeptApplyDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StuffDeptApplyDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'DeptSheetNo': 'old_dept_sheet_no', 'Name': 'old_name', 'StuffID': 'old_stuff_id', 'StuffKindID': 'old_stuff_kind_id', 'Unit': 'old_unit', 'Qty': 'old_qty', 'Amount': 'old_amount', 'Remarks': 'old_remarks', 'DeptID': 'old_dept_id', 'ApplySheetNo': 'old_apply_sheet_no'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=False
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=False, blank=True, max_length=20)
    old_dept_sheet_no=models.CharField('DeptSheetNo', null=True, blank=True, max_length=30)
    old_name=models.CharField('Name', null=True, blank=True, max_length=50)
    old_stuff_id=models.CharField('StuffID', null=True, blank=True, max_length=30)
    old_stuff_kind_id=models.CharField('StuffKindID', null=True, blank=True, max_length=30)
    old_unit=models.CharField('Unit', null=True, blank=True, max_length=40)
    old_qty=models.DecimalField('Qty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_amount=models.DecimalField('Amount', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_dept_id=models.CharField('DeptID', null=True, blank=True, max_length=30)
    old_apply_sheet_no=models.CharField('ApplySheetNo', null=True, blank=True, max_length=40)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_stuffdeptapplydetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_891938c0e45d7d74')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（StuffDeptApplyDetail，待确认）'
        ordering=["-id"]

class SourceDyeStuffOutApply(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StuffOutApply'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'Applyer': 'old_applyer', 'ApplyDept': 'old_apply_dept', 'ApplyFactory': 'old_apply_factory', 'SheetDate': 'old_sheet_date', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'Remarks': 'old_remarks', 'UseInfo': 'old_use_info'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('SheetNo', null=False, blank=True, max_length=20)
    old_applyer=models.CharField('Applyer', null=True, blank=True, max_length=20)
    old_apply_dept=models.CharField('ApplyDept', null=True, blank=True, max_length=30)
    old_apply_factory=models.CharField('ApplyFactory', null=True, blank=True, max_length=30)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_use_info=models.CharField('UseInfo', null=True, blank=True, max_length=512)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_stuffoutapply'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_1bbe390e2bd3f1b7')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（StuffOutApply，待确认）'
        ordering=["-id"]

class SourceDyeStuffOutApplyDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StuffOutApplyDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'Name': 'old_name', 'StuffID': 'old_stuff_id', 'StuffKindID': 'old_stuff_kind_id', 'Spec': 'old_spec', 'Unit': 'old_unit', 'Qty': 'old_qty', 'Amount': 'old_amount', 'Price': 'old_price', 'Remarks': 'old_remarks', 'KCQty': 'old_kcqty'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=False
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=False, blank=True, max_length=20)
    old_name=models.CharField('Name', null=True, blank=True, max_length=50)
    old_stuff_id=models.CharField('StuffID', null=True, blank=True, max_length=30)
    old_stuff_kind_id=models.CharField('StuffKindID', null=True, blank=True, max_length=30)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=100)
    old_unit=models.CharField('Unit', null=True, blank=True, max_length=40)
    old_qty=models.DecimalField('Qty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_amount=models.DecimalField('Amount', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_kcqty=models.DecimalField('KCQty', null=True, blank=True, max_digits=10, decimal_places=2)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_stuffoutapplydetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_8c24deab943c1374')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（StuffOutApplyDetail，待确认）'
        ordering=["-id"]

class SourceDyeStuffWeight(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StuffWeight'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'RecipeType': 'old_recipe_type', 'DeptID': 'old_dept_id', 'BusinessUnitID': 'old_business_unit_id', 'CustomerID': 'old_customer_id', 'DetailCustName': 'old_detail_cust_name', 'ProdID': 'old_prod_id', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'ClothQtyKg': 'old_cloth_qty_kg', 'SubRate': 'old_sub_rate', 'ClothNetKg': 'old_cloth_net_kg', 'Cost': 'old_cost', 'Rolls': 'old_rolls', 'Price': 'old_price', 'JobSheetNo': 'old_job_sheet_no', 'RecipeSheetNo': 'old_recipe_sheet_no', 'ProcessID': 'old_process_id', 'Receiver': 'old_receiver', 'FinishDate': 'old_finish_date', 'IsFirstVat': 'old_is_first_vat', 'WareHouseID': 'old_ware_house_id', 'ShiftID': 'old_shift_id', 'MachineNo': 'old_machine_no', 'SheetStatus': 'old_sheet_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'WeighterID': 'old_weighter_id', 'RightStatus': 'old_right_status', 'StandRecipeNo': 'old_stand_recipe_no', 'Width': 'old_width', 'StartTime': 'old_start_time', 'CompleteTime': 'old_complete_time', 'LastTime': 'old_last_time', 'Speed': 'old_speed', 'Pressure1': 'old_pressure1', 'Pressure2': 'old_pressure2', 'Pressure3': 'old_pressure3', 'Weight1': 'old_weight1', 'Weight2': 'old_weight2', 'Weight3': 'old_weight3', 'Moisture1': 'old_moisture1', 'Moisture2': 'old_moisture2', 'Moisture3': 'old_moisture3', 'TakeRate1': 'old_take_rate1', 'TakeRate2': 'old_take_rate2', 'TakeRate3': 'old_take_rate3', 'Weight': 'old_weight', 'CombineSheetNos': 'old_combine_sheet_nos', 'RecipeCreater': 'old_recipe_creater', 'ColorE': 'old_color_e', 'LengthQty': 'old_length_qty', 'PreField1': 'old_pre_field1', 'PreField3': 'old_pre_field3', 'StationID': 'old_station_id', 'Rate': 'old_rate', 'JobKindID': 'old_job_kind_id', 'CostMoney': 'old_cost_money', 'BathRatio': 'old_bath_ratio', 'DivideQty': 'old_divide_qty', 'CustColorNum': 'old_cust_color_num', 'CustSelfProduct': 'old_cust_self_product', 'MachineTypeID': 'old_machine_type_id', 'ColorDepthID': 'old_color_depth_id', 'ColorMatching': 'old_color_matching', 'DyeEmpID': 'old_dye_emp_id', 'EmpID': 'old_emp_id', 'Votl': 'old_votl', 'MachineId': 'old_machine_id', 'PreField2': 'old_pre_field2', 'PreField4': 'old_pre_field4', 'GYYQ': 'old_gyyq', 'AddColorNum': 'old_add_color_num', 'WProcessNo': 'old_wprocess_no'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('称料单号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_recipe_type=models.IntegerField('配方类型', null=True, blank=True)
    old_dept_id=models.CharField('部门', null=True, blank=True, max_length=10)
    old_business_unit_id=models.CharField('经营单位', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户名称', null=True, blank=True, max_length=10)
    old_detail_cust_name=models.CharField('明细客户', null=True, blank=True, max_length=150)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=20)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=128)
    old_lot_no=models.TextField('批号', null=True, blank=True)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=150)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=20)
    old_cloth_qty_kg=models.DecimalField('胚重', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sub_rate=models.DecimalField('减量率', null=True, blank=True, max_digits=5, decimal_places=3)
    old_cloth_net_kg=models.DecimalField('胚纱净重', null=True, blank=True, max_digits=10, decimal_places=2)
    old_cost=models.DecimalField('成本', null=True, blank=True, max_digits=10, decimal_places=2)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=16, decimal_places=6)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_recipe_sheet_no=models.CharField('配方单号', null=True, blank=True, max_length=20)
    old_process_id=models.CharField('工序名称', null=True, blank=True, max_length=50)
    old_receiver=models.CharField('接收人', null=True, blank=True, max_length=10)
    old_finish_date=models.DateTimeField('最后领料日期', null=True, blank=True)
    old_is_first_vat=models.BooleanField('是否头缸', null=True, blank=True)
    old_ware_house_id=models.CharField('仓库名称', null=True, blank=True, max_length=10)
    old_shift_id=models.CharField('班别', null=True, blank=True, max_length=10)
    old_machine_no=models.CharField('机台', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_step_no=models.IntegerField('节点号', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改人', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_weighter_id=models.CharField('WeighterID', null=True, blank=True, max_length=10)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_stand_recipe_no=models.CharField('StandRecipeNo', null=True, blank=True, max_length=20)
    old_width=models.CharField('幅宽', null=True, blank=True, max_length=80)
    old_start_time=models.DateTimeField('StartTime', null=True, blank=True)
    old_complete_time=models.DateTimeField('CompleteTime', null=True, blank=True)
    old_last_time=models.DateTimeField('LastTime', null=True, blank=True)
    old_speed=models.DecimalField('Speed', null=True, blank=True, max_digits=8, decimal_places=2)
    old_pressure1=models.DecimalField('Pressure1', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pressure2=models.DecimalField('Pressure2', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pressure3=models.DecimalField('Pressure3', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight1=models.DecimalField('Weight1', null=True, blank=True, max_digits=6, decimal_places=2)
    old_weight2=models.DecimalField('Weight2', null=True, blank=True, max_digits=6, decimal_places=2)
    old_weight3=models.DecimalField('Weight3', null=True, blank=True, max_digits=6, decimal_places=2)
    old_moisture1=models.DecimalField('Moisture1', null=True, blank=True, max_digits=5, decimal_places=3)
    old_moisture2=models.DecimalField('Moisture2', null=True, blank=True, max_digits=5, decimal_places=3)
    old_moisture3=models.DecimalField('Moisture3', null=True, blank=True, max_digits=5, decimal_places=3)
    old_take_rate1=models.DecimalField('TakeRate1', null=True, blank=True, max_digits=5, decimal_places=3)
    old_take_rate2=models.DecimalField('TakeRate2', null=True, blank=True, max_digits=5, decimal_places=3)
    old_take_rate3=models.DecimalField('TakeRate3', null=True, blank=True, max_digits=5, decimal_places=3)
    old_weight=models.CharField('克重', null=True, blank=True, max_length=80)
    old_combine_sheet_nos=models.TextField('CombineSheetNos', null=True, blank=True)
    old_recipe_creater=models.CharField('RecipeCreater', null=True, blank=True, max_length=20)
    old_color_e=models.CharField('ColorE', null=True, blank=True, max_length=500)
    old_length_qty=models.CharField('LengthQty', null=True, blank=True, max_length=50)
    old_pre_field1=models.CharField('捻度(H/S)', null=True, blank=True, max_length=500)
    old_pre_field3=models.CharField('干纱工艺', null=True, blank=True, max_length=500)
    old_station_id=models.CharField('StationID', null=True, blank=True, max_length=10)
    old_rate=models.DecimalField('Rate', null=True, blank=True, max_digits=10, decimal_places=2)
    old_job_kind_id=models.CharField('JobKindID', null=True, blank=True, max_length=10)
    old_cost_money=models.DecimalField('金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_bath_ratio=models.DecimalField('BathRatio', null=True, blank=True, max_digits=6, decimal_places=2)
    old_divide_qty=models.DecimalField('DivideQty', null=True, blank=True, max_digits=8, decimal_places=2)
    old_cust_color_num=models.CharField('CustColorNum', null=True, blank=True, max_length=100)
    old_cust_self_product=models.CharField('客户规格', null=True, blank=True, max_length=250)
    old_machine_type_id=models.IntegerField('MachineTypeID', null=True, blank=True)
    old_color_depth_id=models.CharField('颜色深浅', null=True, blank=True, max_length=50)
    old_color_matching=models.CharField('对色员', null=True, blank=True, max_length=20)
    old_dye_emp_id=models.CharField('看缸员', null=True, blank=True, max_length=50)
    old_emp_id=models.CharField('EmpID', null=True, blank=True, max_length=50)
    old_votl=models.FloatField('Votl', null=True, blank=True)
    old_machine_id=models.IntegerField('中控机台', null=True, blank=True)
    old_pre_field2=models.CharField('成定工艺', null=True, blank=True, max_length=500)
    old_pre_field4=models.CharField('预缩工艺', null=True, blank=True, max_length=500)
    old_gyyq=models.CharField('工艺要求', null=True, blank=True, max_length=1000)
    old_add_color_num=models.IntegerField('加色次数', null=True, blank=True)
    old_wprocess_no=models.CharField('复版完成编码', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_stuffweight'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_e9035a10165eaef9')]
        verbose_name=verbose_name_plural='称料/配料主单'
        ordering=["-id"]

class SourceDyeStuffWeightDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StuffWeightDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'PhaseNo': 'old_phase_no', 'StuffNo': 'old_stuff_no', 'StuffID': 'old_stuff_id', 'LotNo': 'old_lot_no', 'StuffType': 'old_stuff_type', 'Price': 'old_price', 'WeightUnit': 'old_weight_unit', 'Dosage': 'old_dosage', 'RecipeUnit': 'old_recipe_unit', 'NeedQty': 'old_need_qty', 'RealQty': 'old_real_qty', 'NeedMoney': 'old_need_money', 'RealMoney': 'old_real_money', 'OutTime': 'old_out_time', 'IsConfirmed': 'old_is_confirmed', 'DetailNote': 'old_detail_note', 'AddScale': 'old_add_scale', 'Status': 'old_status', 'AddQty': 'old_add_qty', 'OriNeedQty': 'old_ori_need_qty', 'OutDate': 'old_out_date', 'AddDosage': 'old_add_dosage', 'AddNeedQty': 'old_add_need_qty', 'Money': 'old_money', 'CarryIndex': 'old_carry_index', 'StepName': 'old_step_name', 'StepNo': 'old_step_no', 'IsFinished': 'old_is_finished', 'AutoSysIDs': 'old_auto_sys_ids', 'OirDosage': 'old_oir_dosage', 'AdjustDosage': 'old_adjust_dosage'}
    SOURCE_KEY=('SheetSeries', 'PhaseNo', 'StuffNo')
    SOURCE_DOCUMENT=False
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_phase_no=models.IntegerField('PhaseNo', null=False, blank=False)
    old_stuff_no=models.IntegerField('StuffNo', null=False, blank=False)
    old_stuff_id=models.CharField('StuffID', null=True, blank=True, max_length=10)
    old_lot_no=models.CharField('LotNo', null=True, blank=True, max_length=50)
    old_stuff_type=models.CharField('StuffType', null=True, blank=True, max_length=1)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=16, decimal_places=6)
    old_weight_unit=models.CharField('WeightUnit', null=True, blank=True, max_length=1)
    old_dosage=models.DecimalField('Dosage', null=True, blank=True, max_digits=15, decimal_places=6)
    old_recipe_unit=models.IntegerField('RecipeUnit', null=True, blank=True)
    old_need_qty=models.DecimalField('NeedQty', null=True, blank=True, max_digits=12, decimal_places=4)
    old_real_qty=models.DecimalField('RealQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_need_money=models.DecimalField('NeedMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_money=models.DecimalField('RealMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_out_time=models.DateTimeField('OutTime', null=True, blank=True)
    old_is_confirmed=models.BooleanField('IsConfirmed', null=True, blank=True)
    old_detail_note=models.CharField('DetailNote', null=True, blank=True, max_length=256)
    old_add_scale=models.DecimalField('AddScale', null=True, blank=True, max_digits=10, decimal_places=4)
    old_status=models.IntegerField('Status', null=True, blank=True)
    old_add_qty=models.DecimalField('AddQty', null=True, blank=True, max_digits=10, decimal_places=0)
    old_ori_need_qty=models.DecimalField('OriNeedQty', null=True, blank=True, max_digits=12, decimal_places=4)
    old_out_date=models.CharField('OutDate', null=True, blank=True, max_length=20)
    old_add_dosage=models.DecimalField('AddDosage', null=True, blank=True, max_digits=15, decimal_places=6)
    old_add_need_qty=models.DecimalField('AddNeedQty', null=True, blank=True, max_digits=12, decimal_places=4)
    old_money=models.DecimalField('Money', null=True, blank=True, max_digits=10, decimal_places=2)
    old_carry_index=models.CharField('CarryIndex', null=True, blank=True, max_length=20)
    old_step_name=models.CharField('StepName', null=True, blank=True, max_length=50)
    old_step_no=models.CharField('StepNo', null=True, blank=True, max_length=50)
    old_is_finished=models.IntegerField('IsFinished', null=True, blank=True)
    old_auto_sys_ids=models.CharField('AutoSysIDs', null=True, blank=True, max_length=10)
    old_oir_dosage=models.DecimalField('OirDosage', null=True, blank=True, max_digits=15, decimal_places=6)
    old_adjust_dosage=models.DecimalField('AdjustDosage', null=True, blank=True, max_digits=15, decimal_places=6)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_stuffweightdetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_phase_no', 'old_stuff_no'],name='src_0482bc5ad976ac84')]
        verbose_name=verbose_name_plural='称料/配料明细'
        ordering=["-id"]

class SourceDyeStuffWeightJobSheetNo(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StuffWeightJobSheetNo'
    SOURCE_FIELDS={'AutoID': 'old_auto_id', 'SheetSeries': 'old_sheet_series', 'CLSheetNo': 'old_clsheet_no', 'JobSheetNo': 'old_job_sheet_no', 'AllJobSheetNo': 'old_all_job_sheet_no', 'SumAssignedRolls': 'old_sum_assigned_rolls', 'SumAssignedWeightQty': 'old_sum_assigned_weight_qty', 'Rolls': 'old_rolls', 'ClothQtyKg': 'old_cloth_qty_kg', 'Rate': 'old_rate', 'SumAssignedLengthQty': 'old_sum_assigned_length_qty', 'LengthQty': 'old_length_qty', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'ColorNum': 'old_color_num', 'ColorID': 'old_color_id'}
    SOURCE_KEY=('AutoID',)
    SOURCE_DOCUMENT=True
    old_auto_id=models.IntegerField('AutoID', null=False, blank=False)
    old_sheet_series=models.CharField('SheetSeries', null=True, blank=True, max_length=50)
    old_clsheet_no=models.CharField('CLSheetNo', null=True, blank=True, max_length=50)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)
    old_all_job_sheet_no=models.CharField('AllJobSheetNo', null=True, blank=True, max_length=200)
    old_sum_assigned_rolls=models.DecimalField('SumAssignedRolls', null=True, blank=True, max_digits=8, decimal_places=2)
    old_sum_assigned_weight_qty=models.DecimalField('SumAssignedWeightQty', null=True, blank=True, max_digits=8, decimal_places=2)
    old_rolls=models.DecimalField('Rolls', null=True, blank=True, max_digits=8, decimal_places=2)
    old_cloth_qty_kg=models.DecimalField('ClothQtyKg', null=True, blank=True, max_digits=8, decimal_places=2)
    old_rate=models.DecimalField('Rate', null=True, blank=True, max_digits=6, decimal_places=4)
    old_sum_assigned_length_qty=models.DecimalField('SumAssignedLengthQty', null=True, blank=True, max_digits=8, decimal_places=2)
    old_length_qty=models.DecimalField('LengthQty', null=True, blank=True, max_digits=8, decimal_places=2)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=10)
    old_prod_id=models.CharField('ProdID', null=True, blank=True, max_length=200)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_stuffweightjobsheetno'
        indexes=[models.Index(fields=['source_batch', 'old_auto_id'],name='src_78621d651089844f')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（StuffWeightJobSheetNo，待确认）'
        ordering=["-id"]

class SourceDyeStuffWeightPhase(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StuffWeightPhase'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'PhaseNo': 'old_phase_no', 'PhaseID': 'old_phase_id', 'BathRatio': 'old_bath_ratio', 'ProgramID': 'old_program_id', 'PH': 'old_ph', 'WaterQty': 'old_water_qty', 'PrintTimes': 'old_print_times', 'Remarks': 'old_remarks', 'Minutes': 'old_minutes', 'Temperature': 'old_temperature', 'MachineTypeID': 'old_machine_type_id', 'StepIndex': 'old_step_index'}
    SOURCE_KEY=('SheetSeries', 'PhaseNo')
    SOURCE_DOCUMENT=False
    old_sheet_series=models.CharField('明细流水号', null=False, blank=True, max_length=20)
    old_phase_no=models.IntegerField('序号', null=False, blank=False)
    old_phase_id=models.CharField('染程名称', null=True, blank=True, max_length=10)
    old_bath_ratio=models.DecimalField('浴比', null=True, blank=True, max_digits=6, decimal_places=2)
    old_program_id=models.CharField('工艺编码', null=True, blank=True, max_length=10)
    old_ph=models.CharField('PH值', null=True, blank=True, max_length=10)
    old_water_qty=models.DecimalField('水量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_minutes=models.DecimalField('分钟', null=True, blank=True, max_digits=10, decimal_places=2)
    old_temperature=models.DecimalField('温度', null=True, blank=True, max_digits=5, decimal_places=1)
    old_machine_type_id=models.CharField('MachineTypeID', null=True, blank=True, max_length=50)
    old_step_index=models.CharField('StepIndex', null=True, blank=True, max_length=250)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeStuffWeight', verbose_name='原关系：StuffWeight', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_stuffweightphase'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_phase_no'],name='src_177743b714af6b29')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（StuffWeightPhase，待确认）'
        ordering=["-id"]

class SourceDyeStuffWeightPrint(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StuffWeightPrint'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'PhaseNo': 'old_phase_no', 'StuffNo': 'old_stuff_no', 'FormatNo': 'old_format_no', 'PrintNo': 'old_print_no', 'StuffID': 'old_stuff_id', 'StuffType': 'old_stuff_type', 'Price': 'old_price', 'Dosage': 'old_dosage', 'WaterQty': 'old_water_qty', 'NeedQty': 'old_need_qty', 'WeightUnit': 'old_weight_unit', 'PhaseID': 'old_phase_id', 'ProgramID': 'old_program_id'}
    SOURCE_KEY=('SheetSeries', 'PhaseNo', 'StuffNo', 'FormatNo', 'PrintNo')
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=50)
    old_phase_no=models.IntegerField('PhaseNo', null=False, blank=False)
    old_stuff_no=models.IntegerField('StuffNo', null=False, blank=False)
    old_format_no=models.IntegerField('FormatNo', null=False, blank=False)
    old_print_no=models.CharField('PrintNo', null=False, blank=True, max_length=10)
    old_stuff_id=models.CharField('StuffID', null=True, blank=True, max_length=10)
    old_stuff_type=models.CharField('StuffType', null=True, blank=True, max_length=10)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=10, decimal_places=4)
    old_dosage=models.DecimalField('Dosage', null=True, blank=True, max_digits=15, decimal_places=6)
    old_water_qty=models.DecimalField('WaterQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_need_qty=models.DecimalField('NeedQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_unit=models.CharField('WeightUnit', null=True, blank=True, max_length=10)
    old_phase_id=models.CharField('PhaseID', null=True, blank=True, max_length=10)
    old_program_id=models.CharField('ProgramID', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_stuffweightprint'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_phase_no', 'old_stuff_no', 'old_format_no', 'old_print_no'],name='src_736882fb953f0a79')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（StuffWeightPrint，待确认）'
        ordering=["-id"]

class SourceDyeTightTube(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='TightTube'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'RightStatus': 'old_right_status'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=50)
    old_sheet_no=models.CharField('表单号', null=True, blank=True, max_length=50)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=50)
    old_prod_id=models.CharField('品名', null=True, blank=True, max_length=50)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=500)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=10)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_tighttube'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_9908a20939d38db9')]
        verbose_name=verbose_name_plural='其他或待确认相关表（TightTube，待确认）'
        ordering=["-id"]

class SourceDyeTightTubeDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='TightTubeDetail'
    SOURCE_FIELDS={'Sheetseries': 'old_sheetseries', 'DetailNo': 'old_detail_no', 'CustomerID': 'old_customer_id', 'JobSheetNo': 'old_job_sheet_no', 'ProdID': 'old_prod_id', 'ColorNum': 'old_color_num', 'ColorID': 'old_color_id', 'LotNo': 'old_lot_no', 'OrderQty': 'old_order_qty', 'Qty': 'old_qty', 'Rolls': 'old_rolls', 'Area': 'old_area', 'CustSelfNo': 'old_cust_self_no', 'ContractNo': 'old_contract_no', 'CustFabricName': 'old_cust_fabric_name', 'SumAssignedRolls': 'old_sum_assigned_rolls', 'SumAssignedWeightQty': 'old_sum_assigned_weight_qty', 'ColorRemarks': 'old_color_remarks', 'Remarks': 'old_remarks', 'DyeDate': 'old_dye_date', 'OrderSheetDate': 'old_order_sheet_date', 'DetailCustName': 'old_detail_cust_name', 'FenTou': 'old_fen_tou', 'RightStatus': 'old_right_status', 'SheetStatus': 'old_sheet_status', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    old_sheetseries=models.CharField('表单号', null=False, blank=True, max_length=50)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=50)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=30)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=30)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=30)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=30)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=30)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=50)
    old_order_qty=models.DecimalField('订单数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_qty=models.DecimalField('数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_area=models.CharField('区域', null=True, blank=True, max_length=100)
    old_cust_self_no=models.CharField('制单号', null=True, blank=True, max_length=100)
    old_contract_no=models.CharField('客户单号', null=True, blank=True, max_length=500)
    old_cust_fabric_name=models.CharField('客户规格', null=True, blank=True, max_length=250)
    old_sum_assigned_rolls=models.DecimalField('实际粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_sum_assigned_weight_qty=models.DecimalField('实际重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_color_remarks=models.CharField('用途', null=True, blank=True, max_length=500)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=1000)
    old_dye_date=models.CharField('络筒期', null=True, blank=True, max_length=100)
    old_order_sheet_date=models.DateTimeField('落单日期', null=True, blank=True)
    old_detail_cust_name=models.CharField('明细客户', null=True, blank=True, max_length=500)
    old_fen_tou=models.CharField('FenTou', null=True, blank=True, max_length=50)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=30)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=30)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_tighttubedetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_bb6deb9bc13a7da1')]
        verbose_name=verbose_name_plural='其他或待确认相关表（TightTubeDetail，待确认）'
        ordering=["-id"]

class SourceDyeTightTubePlan(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='TightTubePlan'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'RightStatus': 'old_right_status'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=50)
    old_sheet_no=models.CharField('制单单号', null=True, blank=True, max_length=50)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=50)
    old_prod_id=models.CharField('品名', null=True, blank=True, max_length=50)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=500)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=10)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_tighttubeplan'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_e164821a768e1492')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（TightTubePlan，待确认）'
        ordering=["-id"]

class SourceDyeTightTubePlanDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='TightTubePlanDetail'
    SOURCE_FIELDS={'Sheetseries': 'old_sheetseries', 'DetailNo': 'old_detail_no', 'CustomerID': 'old_customer_id', 'JobSheetNo': 'old_job_sheet_no', 'ProdID': 'old_prod_id', 'ColorNum': 'old_color_num', 'ColorID': 'old_color_id', 'LotNo': 'old_lot_no', 'OrderQty': 'old_order_qty', 'Qty': 'old_qty', 'Rolls': 'old_rolls', 'Area': 'old_area', 'CustSelfNo': 'old_cust_self_no', 'ContractNo': 'old_contract_no', 'SumAssignedRolls': 'old_sum_assigned_rolls', 'SumAssignedWeightQty': 'old_sum_assigned_weight_qty', 'ColorRemarks': 'old_color_remarks', 'CheckNo': 'old_check_no', 'LabelWareHouse': 'old_label_ware_house', 'LabelRemarks': 'old_label_remarks', 'WindingID': 'old_winding_id', 'TubeWeight': 'old_tube_weight', 'PackBag': 'old_pack_bag', 'MachineID': 'old_machine_id', 'GY': 'old_gy', 'CustFabricName': 'old_cust_fabric_name', 'LTSheetNo': 'old_ltsheet_no', 'FenTou': 'old_fen_tou'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    old_sheetseries=models.CharField('表单号', null=False, blank=True, max_length=50)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=50)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=30)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=30)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=30)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=30)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=30)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=50)
    old_order_qty=models.DecimalField('订单数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_qty=models.DecimalField('数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_area=models.CharField('区域', null=True, blank=True, max_length=100)
    old_cust_self_no=models.CharField('制单号', null=True, blank=True, max_length=100)
    old_contract_no=models.CharField('客户单号', null=True, blank=True, max_length=500)
    old_sum_assigned_rolls=models.DecimalField('生产个数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_sum_assigned_weight_qty=models.DecimalField('生产重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_color_remarks=models.CharField('用途', null=True, blank=True, max_length=500)
    old_check_no=models.CharField('订单明细号', null=True, blank=True, max_length=50)
    old_label_ware_house=models.CharField('标签仓库', null=True, blank=True, max_length=100)
    old_label_remarks=models.CharField('标签用途', null=True, blank=True, max_length=500)
    old_winding_id=models.CharField('络筒员工', null=True, blank=True, max_length=30)
    old_tube_weight=models.DecimalField('纸筒', null=True, blank=True, max_digits=7, decimal_places=3)
    old_pack_bag=models.DecimalField('包装', null=True, blank=True, max_digits=7, decimal_places=3)
    old_machine_id=models.CharField('机台', null=True, blank=True, max_length=100)
    old_gy=models.CharField('工艺', null=True, blank=True, max_length=200)
    old_cust_fabric_name=models.CharField('客户规格', null=True, blank=True, max_length=200)
    old_ltsheet_no=models.CharField('排产号', null=True, blank=True, max_length=30)
    old_fen_tou=models.CharField('分头', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_tighttubeplandetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_8021661a3071ada3')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（TightTubePlanDetail，待确认）'
        ordering=["-id"]

class SourceDyeUserACMachines(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='UserACMachines'
    SOURCE_FIELDS={'UserID': 'old_user_id', 'Deviceid': 'old_deviceid'}
    SOURCE_KEY=('UserID', 'Deviceid')
    SOURCE_DOCUMENT=True
    old_user_id=models.IntegerField('UserID', null=False, blank=False)
    old_deviceid=models.IntegerField('Deviceid', null=False, blank=False)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_useracmachines'
        indexes=[models.Index(fields=['source_batch', 'old_user_id', 'old_deviceid'],name='src_ef0fafe3593d2bd1')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（UserACMachines，待确认）'
        ordering=["-id"]

class SourceDyeUsersMachines(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='UsersMachines'
    SOURCE_FIELDS={'ID': 'old_id', 'USERID': 'old_userid', 'DEVICEID': 'old_deviceid'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    old_id=models.IntegerField('ID', null=False, blank=False)
    old_userid=models.IntegerField('USERID', null=False, blank=False)
    old_deviceid=models.IntegerField('DEVICEID', null=False, blank=False)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_usersmachines'
        indexes=[]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（UsersMachines，待确认）'
        ordering=["-id"]

class SourceDyeWashTheTankDye(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='WashTheTankDye'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'StuffID': 'old_stuff_id', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=30)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=30)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_stuff_id=models.CharField('StuffID', null=True, blank=True, max_length=10)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=20)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=20)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_washthetankdye'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_a19878fc0c47f645')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（WashTheTankDye，待确认）'
        ordering=["-id"]

class SourceDyeWProcess(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='WProcess'
    SOURCE_FIELDS={'WProcessNo': 'old_wprocess_no', 'JobSheetNo': 'old_job_sheet_no', 'OrderSheetNo': 'old_order_sheet_no', 'ProcessNo': 'old_process_no', 'ProcessID': 'old_process_id', 'EmpID': 'old_emp_id', 'ClassID': 'old_class_id', 'ShiftID': 'old_shift_id', 'GroupID': 'old_group_id', 'StationID': 'old_station_id', 'MachineID': 'old_machine_id', 'PrevProcessID': 'old_prev_process_id', 'NextProcessNo': 'old_next_process_no', 'NextProcessID': 'old_next_process_id', 'NextStationID': 'old_next_station_id', 'StartTime': 'old_start_time', 'EndTime': 'old_end_time', 'AssignedQty': 'old_assigned_qty', 'AssingedKg': 'old_assinged_kg', 'AssignedMeter': 'old_assigned_meter', 'PrevWProcessNo': 'old_prev_wprocess_no', 'PrevRolls': 'old_prev_rolls', 'PrevQty': 'old_prev_qty', 'PrevMeter': 'old_prev_meter', 'PrevKg': 'old_prev_kg', 'PrevWeight': 'old_prev_weight', 'PrevWidth': 'old_prev_width', 'PrevEndTime': 'old_prev_end_time', 'CurrRolls': 'old_curr_rolls', 'CurrMeter': 'old_curr_meter', 'CurrKg': 'old_curr_kg', 'CurrWeight': 'old_curr_weight', 'CurrWidth': 'old_curr_width', 'CurrVats': 'old_curr_vats', 'CurrEffirate': 'old_curr_effirate', 'WorkQty': 'old_work_qty', 'WorkMoney': 'old_work_money', 'DefectRolls': 'old_defect_rolls', 'DefectQty': 'old_defect_qty', 'Status': 'old_status', 'Memo': 'old_memo', 'ModifyDate': 'old_modify_date', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModuleNo': 'old_module_no', 'Kind': 'old_kind', 'SampleQty': 'old_sample_qty', 'IPAddress': 'old_ipaddress', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'StepNo': 'old_step_no', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'ColorMatching': 'old_color_matching', 'QualityMemo': 'old_quality_memo', 'CurrDosage': 'old_curr_dosage', 'DyeState': 'old_dye_state', 'SheetKind': 'old_sheet_kind', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('WProcessNo',)
    SOURCE_DOCUMENT=True
    old_wprocess_no=models.CharField('刷卡号', null=False, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_order_sheet_no=models.CharField('订单号', null=True, blank=True, max_length=20)
    old_process_no=models.IntegerField('工序号', null=True, blank=True)
    old_process_id=models.CharField('工序', null=True, blank=True, max_length=10)
    old_emp_id=models.CharField('员工代码', null=True, blank=True, max_length=10)
    old_class_id=models.CharField('班别', null=True, blank=True, max_length=10)
    old_shift_id=models.CharField('班组', null=True, blank=True, max_length=10)
    old_group_id=models.CharField('车间代码', null=True, blank=True, max_length=10)
    old_station_id=models.CharField('站别', null=True, blank=True, max_length=10)
    old_machine_id=models.CharField('机台', null=True, blank=True, max_length=20)
    old_prev_process_id=models.CharField('上一道工序代码', null=True, blank=True, max_length=10)
    old_next_process_no=models.IntegerField('下一道工序号', null=True, blank=True)
    old_next_process_id=models.CharField('下一道工序代码', null=True, blank=True, max_length=10)
    old_next_station_id=models.CharField('下一道站别代码', null=True, blank=True, max_length=10)
    old_start_time=models.DateTimeField('开始时间', null=True, blank=True)
    old_end_time=models.DateTimeField('结束时间', null=True, blank=True)
    old_assigned_qty=models.DecimalField('配纱数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_assinged_kg=models.DecimalField('配纱公斤', null=True, blank=True, max_digits=10, decimal_places=2)
    old_assigned_meter=models.DecimalField('配纱米数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_prev_wprocess_no=models.CharField('上一道刷卡流水号', null=True, blank=True, max_length=20)
    old_prev_rolls=models.DecimalField('上一道粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_prev_qty=models.DecimalField('上一道数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_prev_meter=models.DecimalField('上一道米数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_prev_kg=models.DecimalField('上一道重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_prev_weight=models.DecimalField('上一道克重', null=True, blank=True, max_digits=6, decimal_places=2)
    old_prev_width=models.DecimalField('上一道幅宽', null=True, blank=True, max_digits=6, decimal_places=2)
    old_prev_end_time=models.DateTimeField('上一道结束时间', null=True, blank=True)
    old_curr_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=8, decimal_places=3)
    old_curr_meter=models.DecimalField('长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_curr_kg=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=3)
    old_curr_weight=models.DecimalField('克重', null=True, blank=True, max_digits=6, decimal_places=2)
    old_curr_width=models.DecimalField('幅宽', null=True, blank=True, max_digits=6, decimal_places=2)
    old_curr_vats=models.DecimalField('缸数', null=True, blank=True, max_digits=8, decimal_places=3)
    old_curr_effirate=models.DecimalField('本道系数', null=True, blank=True, max_digits=6, decimal_places=2)
    old_work_qty=models.DecimalField('产量', null=True, blank=True, max_digits=10, decimal_places=3)
    old_work_money=models.DecimalField('计件工资', null=True, blank=True, max_digits=10, decimal_places=2)
    old_defect_rolls=models.DecimalField('疵品粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_defect_qty=models.DecimalField('疵品数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_status=models.CharField('状态', null=True, blank=True, max_length=1)
    old_memo=models.CharField('摘要', null=True, blank=True, max_length=100)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_module_no=models.IntegerField('ModuleNo', null=True, blank=True)
    old_kind=models.IntegerField('类别', null=True, blank=True)
    old_sample_qty=models.DecimalField('SampleQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_ipaddress=models.CharField('IPAddress', null=True, blank=True, max_length=25)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_step_no=models.CharField('StepNo', null=True, blank=True, max_length=50)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_color_matching=models.CharField('ColorMatching', null=True, blank=True, max_length=50)
    old_quality_memo=models.CharField('QualityMemo', null=True, blank=True, max_length=20)
    old_curr_dosage=models.DecimalField('本道百分比', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dye_state=models.CharField('染色状态', null=True, blank=True, max_length=10)
    old_sheet_kind=models.CharField('类别（1为录入单据）', null=True, blank=True, max_length=10)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=500)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_wprocess'
        indexes=[models.Index(fields=['source_batch', 'old_wprocess_no'],name='src_ce48b52947fb1606'),models.Index(fields=['source_batch', 'old_wprocess_no', 'old_job_sheet_no', 'old_process_no', 'old_process_id', 'old_shift_id'],name='src_a43fa4419178d950')]
        verbose_name=verbose_name_plural='实际工序执行'
        ordering=["-id"]

class SourceDyeWProcessBak(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='WProcessBak'
    SOURCE_FIELDS={'WProcessNo': 'old_wprocess_no', 'JobSheetNo': 'old_job_sheet_no', 'OrderSheetNo': 'old_order_sheet_no', 'ProcessNo': 'old_process_no', 'ProcessID': 'old_process_id', 'EmpID': 'old_emp_id', 'ClassID': 'old_class_id', 'ShiftID': 'old_shift_id', 'GroupID': 'old_group_id', 'StationID': 'old_station_id', 'MachineID': 'old_machine_id', 'PrevProcessID': 'old_prev_process_id', 'NextProcessNo': 'old_next_process_no', 'NextProcessID': 'old_next_process_id', 'NextStationID': 'old_next_station_id', 'StartTime': 'old_start_time', 'EndTime': 'old_end_time', 'AssignedQty': 'old_assigned_qty', 'AssingedKg': 'old_assinged_kg', 'AssignedMeter': 'old_assigned_meter', 'PrevWProcessNo': 'old_prev_wprocess_no', 'PrevRolls': 'old_prev_rolls', 'PrevQty': 'old_prev_qty', 'PrevMeter': 'old_prev_meter', 'PrevKg': 'old_prev_kg', 'PrevWeight': 'old_prev_weight', 'PrevWidth': 'old_prev_width', 'PrevEndTime': 'old_prev_end_time', 'CurrRolls': 'old_curr_rolls', 'CurrMeter': 'old_curr_meter', 'CurrKg': 'old_curr_kg', 'CurrWeight': 'old_curr_weight', 'CurrWidth': 'old_curr_width', 'CurrVats': 'old_curr_vats', 'CurrEffirate': 'old_curr_effirate', 'WorkQty': 'old_work_qty', 'WorkMoney': 'old_work_money', 'DefectRolls': 'old_defect_rolls', 'DefectQty': 'old_defect_qty', 'Status': 'old_status', 'Memo': 'old_memo', 'ModifyDate': 'old_modify_date', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModuleNo': 'old_module_no', 'Kind': 'old_kind', 'SampleQty': 'old_sample_qty', 'IPAddress': 'old_ipaddress', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'StepNo': 'old_step_no', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver'}
    SOURCE_KEY=('WProcessNo',)
    SOURCE_DOCUMENT=True
    old_wprocess_no=models.CharField('WProcessNo', null=False, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)
    old_order_sheet_no=models.CharField('OrderSheetNo', null=True, blank=True, max_length=20)
    old_process_no=models.IntegerField('ProcessNo', null=True, blank=True)
    old_process_id=models.CharField('ProcessID', null=True, blank=True, max_length=10)
    old_emp_id=models.CharField('EmpID', null=True, blank=True, max_length=10)
    old_class_id=models.CharField('ClassID', null=True, blank=True, max_length=10)
    old_shift_id=models.CharField('ShiftID', null=True, blank=True, max_length=10)
    old_group_id=models.CharField('GroupID', null=True, blank=True, max_length=10)
    old_station_id=models.CharField('StationID', null=True, blank=True, max_length=10)
    old_machine_id=models.CharField('MachineID', null=True, blank=True, max_length=20)
    old_prev_process_id=models.CharField('PrevProcessID', null=True, blank=True, max_length=10)
    old_next_process_no=models.IntegerField('NextProcessNo', null=True, blank=True)
    old_next_process_id=models.CharField('NextProcessID', null=True, blank=True, max_length=10)
    old_next_station_id=models.CharField('NextStationID', null=True, blank=True, max_length=10)
    old_start_time=models.DateTimeField('StartTime', null=True, blank=True)
    old_end_time=models.DateTimeField('EndTime', null=True, blank=True)
    old_assigned_qty=models.DecimalField('AssignedQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_assinged_kg=models.DecimalField('AssingedKg', null=True, blank=True, max_digits=10, decimal_places=2)
    old_assigned_meter=models.DecimalField('AssignedMeter', null=True, blank=True, max_digits=10, decimal_places=2)
    old_prev_wprocess_no=models.CharField('PrevWProcessNo', null=True, blank=True, max_length=20)
    old_prev_rolls=models.DecimalField('PrevRolls', null=True, blank=True, max_digits=7, decimal_places=2)
    old_prev_qty=models.DecimalField('PrevQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_prev_meter=models.DecimalField('PrevMeter', null=True, blank=True, max_digits=10, decimal_places=2)
    old_prev_kg=models.DecimalField('PrevKg', null=True, blank=True, max_digits=10, decimal_places=2)
    old_prev_weight=models.DecimalField('PrevWeight', null=True, blank=True, max_digits=6, decimal_places=2)
    old_prev_width=models.DecimalField('PrevWidth', null=True, blank=True, max_digits=6, decimal_places=2)
    old_prev_end_time=models.DateTimeField('PrevEndTime', null=True, blank=True)
    old_curr_rolls=models.DecimalField('CurrRolls', null=True, blank=True, max_digits=8, decimal_places=3)
    old_curr_meter=models.DecimalField('CurrMeter', null=True, blank=True, max_digits=10, decimal_places=2)
    old_curr_kg=models.DecimalField('CurrKg', null=True, blank=True, max_digits=10, decimal_places=3)
    old_curr_weight=models.DecimalField('CurrWeight', null=True, blank=True, max_digits=6, decimal_places=2)
    old_curr_width=models.DecimalField('CurrWidth', null=True, blank=True, max_digits=6, decimal_places=2)
    old_curr_vats=models.DecimalField('CurrVats', null=True, blank=True, max_digits=8, decimal_places=3)
    old_curr_effirate=models.DecimalField('CurrEffirate', null=True, blank=True, max_digits=6, decimal_places=2)
    old_work_qty=models.DecimalField('WorkQty', null=True, blank=True, max_digits=10, decimal_places=3)
    old_work_money=models.DecimalField('WorkMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_defect_rolls=models.DecimalField('DefectRolls', null=True, blank=True, max_digits=10, decimal_places=2)
    old_defect_qty=models.DecimalField('DefectQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_status=models.CharField('Status', null=True, blank=True, max_length=1)
    old_memo=models.CharField('Memo', null=True, blank=True, max_length=100)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_module_no=models.IntegerField('ModuleNo', null=True, blank=True)
    old_kind=models.IntegerField('Kind', null=True, blank=True)
    old_sample_qty=models.DecimalField('SampleQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_ipaddress=models.CharField('IPAddress', null=True, blank=True, max_length=25)
    old_sheet_status=models.IntegerField('SheetStatus', null=True, blank=True)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_step_no=models.CharField('StepNo', null=True, blank=True, max_length=50)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_wprocessbak'
        indexes=[models.Index(fields=['source_batch', 'old_wprocess_no'],name='src_948b05bce5bc7c1e')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（WProcessBak，待确认）'
        ordering=["-id"]

class SourceDyeWProcessStep(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='WProcessStep'
    SOURCE_FIELDS={'WPStepNo': 'old_wpstep_no', 'WProcessNo': 'old_wprocess_no', 'JobSheetNo': 'old_job_sheet_no', 'ProcessNo': 'old_process_no', 'ProcessID': 'old_process_id', 'DyeProcessID': 'old_dye_process_id', 'RealValue': 'old_real_value', 'RecordID': 'old_record_id', 'CurrTime': 'old_curr_time', 'Remarks': 'old_remarks', 'ProgramID': 'old_program_id'}
    SOURCE_KEY=('WPStepNo',)
    SOURCE_DOCUMENT=False
    old_wpstep_no=models.CharField('刷卡步骤号', null=False, blank=True, max_length=20)
    old_wprocess_no=models.CharField('刷卡记录号', null=True, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_process_no=models.IntegerField('工序号', null=True, blank=True)
    old_process_id=models.CharField('工序代码', null=True, blank=True, max_length=10)
    old_dye_process_id=models.CharField('染色工序', null=True, blank=True, max_length=50)
    old_real_value=models.DecimalField('实际值', null=True, blank=True, max_digits=10, decimal_places=2)
    old_record_id=models.CharField('记录ID', null=True, blank=True, max_length=38)
    old_curr_time=models.DateTimeField('当前时间', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    old_program_id=models.CharField('ProgramID', null=True, blank=True, max_length=50)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeWProcess', verbose_name='原关系：WProcess', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_wprocessstep'
        indexes=[models.Index(fields=['source_batch', 'old_wpstep_no'],name='src_4cd8a63ce28cab60')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（WProcessStep，待确认）'
        ordering=["-id"]

class SourceDyeWProcessStepBak(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='WProcessStepBak'
    SOURCE_FIELDS={'WPStepNo': 'old_wpstep_no', 'WProcessNo': 'old_wprocess_no', 'JobSheetNo': 'old_job_sheet_no', 'ProcessNo': 'old_process_no', 'ProcessID': 'old_process_id', 'DyeProcessID': 'old_dye_process_id', 'RealValue': 'old_real_value', 'RecordID': 'old_record_id', 'CurrTime': 'old_curr_time', 'Remarks': 'old_remarks', 'ProgramID': 'old_program_id'}
    SOURCE_KEY=('WPStepNo',)
    SOURCE_DOCUMENT=True
    old_wpstep_no=models.CharField('WPStepNo', null=False, blank=True, max_length=20)
    old_wprocess_no=models.CharField('WProcessNo', null=True, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)
    old_process_no=models.IntegerField('ProcessNo', null=True, blank=True)
    old_process_id=models.CharField('ProcessID', null=True, blank=True, max_length=10)
    old_dye_process_id=models.CharField('DyeProcessID', null=True, blank=True, max_length=50)
    old_real_value=models.DecimalField('RealValue', null=True, blank=True, max_digits=10, decimal_places=2)
    old_record_id=models.CharField('RecordID', null=True, blank=True, max_length=38)
    old_curr_time=models.DateTimeField('CurrTime', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=100)
    old_program_id=models.CharField('ProgramID', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_wprocessstepbak'
        indexes=[models.Index(fields=['source_batch', 'old_wpstep_no'],name='src_7ddcbf8e063bcd96')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（WProcessStepBak，待确认）'
        ordering=["-id"]

class SourceDyeWVehicle(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='WVehicle'
    SOURCE_FIELDS={'WProcessNo': 'old_wprocess_no', 'VehicleNo': 'old_vehicle_no', 'Place': 'old_place'}
    SOURCE_KEY=('WProcessNo', 'VehicleNo')
    SOURCE_DOCUMENT=True
    old_wprocess_no=models.CharField('WProcessNo', null=False, blank=True, max_length=20)
    old_vehicle_no=models.CharField('VehicleNo', null=False, blank=True, max_length=10)
    old_place=models.CharField('Place', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_wvehicle'
        indexes=[models.Index(fields=['source_batch', 'old_wprocess_no', 'old_vehicle_no'],name='src_6721998217afd212')]
        verbose_name=verbose_name_plural='其他或待确认相关表（WVehicle，待确认）'
        ordering=["-id"]

class SourceDyeWWorkRecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='WWorkRecord'
    SOURCE_FIELDS={'WorkRecordNo': 'old_work_record_no', 'EmpID': 'old_emp_id', 'ShiftID': 'old_shift_id', 'CurrDate': 'old_curr_date', 'StartTime': 'old_start_time', 'EndTime': 'old_end_time', 'WorkTime': 'old_work_time', 'CurrTime': 'old_curr_time', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('WorkRecordNo',)
    SOURCE_DOCUMENT=False
    old_work_record_no=models.CharField('工时登记记录号', null=False, blank=True, max_length=20)
    old_emp_id=models.CharField('员工', null=True, blank=True, max_length=10)
    old_shift_id=models.CharField('班组', null=True, blank=True, max_length=10)
    old_curr_date=models.DateTimeField('当前日期', null=True, blank=True)
    old_start_time=models.DateTimeField('开始上班时间', null=True, blank=True)
    old_end_time=models.DateTimeField('结束下班时间', null=True, blank=True)
    old_work_time=models.DecimalField('工时（小时）', null=True, blank=True, max_digits=5, decimal_places=2)
    old_curr_time=models.DateTimeField('当前时间', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_wworkrecord'
        indexes=[models.Index(fields=['source_batch', 'old_work_record_no'],name='src_8556a39044c4abdb')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（WWorkRecord，待确认）'
        ordering=["-id"]

class SourceDyeWWorkTime(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='WWorkTime'
    SOURCE_FIELDS={'WWorkTimeNo': 'old_wwork_time_no', 'EmpID': 'old_emp_id', 'CurrDate': 'old_curr_date', 'ShiftID': 'old_shift_id', 'EffiRate': 'old_effi_rate', 'WorkTime': 'old_work_time', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('WWorkTimeNo',)
    SOURCE_DOCUMENT=True
    old_wwork_time_no=models.CharField('工时记录标识符', null=False, blank=True, max_length=40)
    old_emp_id=models.CharField('员工', null=False, blank=True, max_length=10)
    old_curr_date=models.DateTimeField('日期', null=False, blank=False)
    old_shift_id=models.CharField('班组', null=False, blank=True, max_length=10)
    old_effi_rate=models.DecimalField('效率比例', null=True, blank=True, max_digits=6, decimal_places=4)
    old_work_time=models.DecimalField('工时', null=True, blank=True, max_digits=5, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_wworktime'
        indexes=[models.Index(fields=['source_batch', 'old_wwork_time_no'],name='src_8ae9d200afc0c959')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（WWorkTime，待确认）'
        ordering=["-id"]
