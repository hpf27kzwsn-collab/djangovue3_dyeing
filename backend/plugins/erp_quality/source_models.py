"""静态旧业务字段；由tools/legacy_models生成，逐表来源见source_catalog.json。"""
from django.db import models
from django.db.models.functions import Upper,RTrim
from plugins.erp_base.source_documents import SourceRecord


class SourceDyeCHECKEXACT(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='CHECKEXACT'
    SOURCE_FIELDS={'EXACTID': 'old_exactid', 'USERID': 'old_userid', 'CHECKTIME': 'old_checktime', 'CHECKTYPE': 'old_checktype', 'ISADD': 'old_isadd', 'YUYIN': 'old_yuyin', 'ISMODIFY': 'old_ismodify', 'ISDELETE': 'old_isdelete', 'INCOUNT': 'old_incount', 'ISCOUNT': 'old_iscount', 'MODIFYBY': 'old_modifyby', 'DATE': 'old_date'}
    SOURCE_KEY=('EXACTID',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_checktype': 'Chinese_PRC_CI_AS', 'old_yuyin': 'Chinese_PRC_CI_AS', 'old_modifyby': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_userid': ('literal', 0), 'old_checktime': ('literal', 0), 'old_checktype': ('literal', 0), 'old_isadd': ('literal', 0), 'old_ismodify': ('literal', 0), 'old_isdelete': ('literal', 0), 'old_incount': ('literal', 0), 'old_iscount': ('literal', 0), 'old_modifyby': ('literal', '-')}
    SOURCE_IDENTITIES=('old_exactid',)
    SOURCE_IDENTITY_RULES={'old_exactid': (1, 1)}
    old_exactid=models.IntegerField('EXACTID', null=False, blank=False)
    old_userid=models.IntegerField('USERID', null=True, blank=True)
    old_checktime=models.DateTimeField('CHECKTIME', null=True, blank=True)
    old_checktype=models.CharField('CHECKTYPE', null=True, blank=True, max_length=2)
    old_isadd=models.IntegerField('ISADD', null=True, blank=True)
    old_yuyin=models.CharField('YUYIN', null=True, blank=True, max_length=25)
    old_ismodify=models.IntegerField('ISMODIFY', null=True, blank=True)
    old_isdelete=models.IntegerField('ISDELETE', null=True, blank=True)
    old_incount=models.IntegerField('INCOUNT', null=True, blank=True)
    old_iscount=models.IntegerField('ISCOUNT', null=True, blank=True)
    old_modifyby=models.CharField('MODIFYBY', null=True, blank=True, max_length=20)
    old_date=models.DateTimeField('DATE', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_checkexact'
        indexes=[models.Index(fields=['source_batch', 'old_exactid'],name='src_5472b4954751790e')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（CHECKEXACT，待确认）'
        ordering=["-id"]

class SourceDyeCHECKINOUT(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='CHECKINOUT'
    SOURCE_FIELDS={'USERID': 'old_userid', 'CHECKTIME': 'old_checktime', 'CHECKTYPE': 'old_checktype', 'VERIFYCODE': 'old_verifycode', 'SENSORID': 'old_sensorid', 'Memoinfo': 'old_memoinfo', 'WorkCode': 'old_work_code', 'sn': 'old_sn', 'UserExtFmt': 'old_user_ext_fmt', 'mask_flag': 'old_mask_flag', 'temperature': 'old_temperature'}
    SOURCE_KEY=('USERID', 'CHECKTIME')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_checktype': 'Chinese_PRC_CI_AS', 'old_sensorid': 'Chinese_PRC_CI_AS', 'old_memoinfo': 'Chinese_PRC_CI_AS', 'old_work_code': 'Chinese_PRC_CI_AS', 'old_sn': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_checktime': ('now', None), 'old_checktype': ('literal', 'I'), 'old_verifycode': ('literal', 0), 'old_work_code': ('literal', 0), 'old_user_ext_fmt': ('literal', 0), 'old_mask_flag': ('literal', 0), 'old_temperature': ('literal', 0)}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_userid=models.IntegerField('USERID', null=False, blank=False)
    old_checktime=models.DateTimeField('CHECKTIME', null=False, blank=False)
    old_checktype=models.CharField('CHECKTYPE', null=True, blank=True, max_length=1)
    old_verifycode=models.IntegerField('VERIFYCODE', null=True, blank=True)
    old_sensorid=models.CharField('SENSORID', null=True, blank=True, max_length=5)
    old_memoinfo=models.CharField('Memoinfo', null=True, blank=True, max_length=30)
    old_work_code=models.CharField('WorkCode', null=True, blank=True, max_length=50)
    old_sn=models.CharField('sn', null=True, blank=True, max_length=20)
    old_user_ext_fmt=models.IntegerField('UserExtFmt', null=True, blank=True)
    old_mask_flag=models.IntegerField('mask_flag', null=True, blank=True)
    old_temperature=models.FloatField('temperature', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_checkinout'
        indexes=[models.Index(fields=['source_batch', 'old_userid', 'old_checktime'],name='src_c41231df3b35e71d')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（CHECKINOUT，待确认）'
        ordering=["-id"]

class SourceDyeColoringCheck(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ColoringCheck'
    SOURCE_FIELDS={'ID': 'old_id', 'JobSheetNo': 'old_job_sheet_no', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'ProcessID': 'old_process_id', 'DefectID': 'old_defect_id', 'ProdID': 'old_prod_id', 'CustomerID': 'old_customer_id', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'Rolls': 'old_rolls', 'WeightQty': 'old_weight_qty', 'EmpID': 'old_emp_id', 'ShiftID': 'old_shift_id', 'SheetDate': 'old_sheet_date', 'DyeProcessID': 'old_dye_process_id', 'RealValue': 'old_real_value', 'CurveID': 'old_curve_id', 'Remarks': 'old_remarks', 'WProcessNo': 'old_wprocess_no', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_process_id': 'Chinese_PRC_CI_AS', 'old_defect_id': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_emp_id': 'Chinese_PRC_CI_AS', 'old_shift_id': 'Chinese_PRC_CI_AS', 'old_dye_process_id': 'Chinese_PRC_CI_AS', 'old_curve_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_wprocess_no': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_id=models.BigIntegerField('ID', null=False, blank=False)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_creater=models.CharField('登记人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('登记日期', null=True, blank=True)
    old_process_id=models.CharField('工序', null=True, blank=True, max_length=20)
    old_defect_id=models.CharField('DefectID', null=True, blank=True, max_length=50)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=100)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=100)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=100)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=100)
    old_rolls=models.IntegerField('粒数', null=True, blank=True)
    old_weight_qty=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_emp_id=models.CharField('员工', null=True, blank=True, max_length=20)
    old_shift_id=models.CharField('生产班组', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_dye_process_id=models.CharField('完成步骤', null=True, blank=True, max_length=100)
    old_real_value=models.FloatField('RealValue', null=True, blank=True)
    old_curve_id=models.CharField('染色工序', null=True, blank=True, max_length=10)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    old_wprocess_no=models.CharField('记录号', null=True, blank=True, max_length=20)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_coloringcheck'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_473cdfaac184f489')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（ColoringCheck，待确认）'
        ordering=["-id"]

class SourceDyeDefectiveIn(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DefectiveIn'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'PendOutSheetSeries': 'old_pend_out_sheet_series'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_pend_out_sheet_series': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('单号', null=False, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_pend_out_sheet_series=models.CharField('PendOutSheetSeries', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_defectivein'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_8184ceee09ecaebf'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_8184ceee09ecaebf')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（DefectiveIn，待确认）'
        ordering=["-id"]

class SourceDyeDefectiveInDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DefectiveInDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'JobSheetNo': 'old_job_sheet_no', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'CustomerProdName': 'old_customer_prod_name', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'CustColorNum': 'old_cust_color_num', 'Weight': 'old_weight', 'Width': 'old_width', 'Rolls': 'old_rolls', 'WeightQty': 'old_weight_qty', 'LengthQty': 'old_length_qty', 'Description': 'old_description', 'Remarks': 'old_remarks', 'QualityDeductionSheetNo': 'old_quality_deduction_sheet_no', 'GrayQty': 'old_gray_qty', 'qy': 'old_qy', 'kw': 'old_kw'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_customer_prod_name': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_cust_color_num': 'Chinese_PRC_CI_AS', 'old_weight': 'Chinese_PRC_CI_AS', 'old_width': 'Chinese_PRC_CI_AS', 'old_description': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_quality_deduction_sheet_no': 'Chinese_PRC_CI_AS', 'old_qy': 'Chinese_PRC_CI_AS', 'old_kw': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：DefectiveIn', 'target': 'erp_quality.SourceDyeDefectiveIn', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 DefectiveInDetail → DefectiveIn']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=20)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=20)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=200)
    old_customer_prod_name=models.CharField('客户纱种', null=True, blank=True, max_length=200)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=150)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=20)
    old_cust_color_num=models.CharField('客户色号', null=True, blank=True, max_length=150)
    old_weight=models.CharField('克重', null=True, blank=True, max_length=256)
    old_width=models.CharField('幅宽', null=True, blank=True, max_length=256)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_weight_qty=models.DecimalField('实重', null=True, blank=True, max_digits=10, decimal_places=2)
    old_length_qty=models.DecimalField('长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_description=models.CharField('质量描述', null=True, blank=True, max_length=512)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_quality_deduction_sheet_no=models.CharField('扣罚单号', null=True, blank=True, max_length=32)
    old_gray_qty=models.DecimalField('胚重', null=True, blank=True, max_digits=10, decimal_places=2)
    old_qy=models.CharField('区域', null=True, blank=True, max_length=150)
    old_kw=models.CharField('库位', null=True, blank=True, max_length=150)
    source_parent_1=models.ForeignKey('erp_quality.SourceDyeDefectiveIn', verbose_name='原关系：DefectiveIn', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_defectiveindetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_8d0ed72422293d7d'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_8d0ed72422293d7d')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（DefectiveInDetail，待确认）'
        ordering=["-id"]

class SourceDyeDefectiveInRecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DefectiveInRecord'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'RollNo': 'old_roll_no', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'StorageUnitID': 'old_storage_unit_id', 'Status': 'old_status', 'OutDetailNo': 'old_out_detail_no', 'BarCode': 'old_bar_code', 'GradeID': 'old_grade_id', 'GrayQty': 'old_gray_qty', 'AdjustQty': 'old_adjust_qty', 'RealQty': 'old_real_qty', 'Meter': 'old_meter', 'Yard': 'old_yard', 'Note': 'old_note', 'GrayBarCode': 'old_gray_bar_code', 'RollNo3': 'old_roll_no3', 'GUnit': 'old_gunit', 'PUnit': 'old_punit'}
    SOURCE_KEY=('SheetSeries', 'DetailNo', 'RollNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_roll_no': 'Chinese_PRC_CI_AS', 'old_storage_unit_id': 'Chinese_PRC_CI_AS', 'old_status': 'Chinese_PRC_CI_AS', 'old_out_detail_no': 'Chinese_PRC_CI_AS', 'old_bar_code': 'Chinese_PRC_CI_AS', 'old_grade_id': 'Chinese_PRC_CI_AS', 'old_note': 'Chinese_PRC_CI_AS', 'old_gray_bar_code': 'Chinese_PRC_CI_AS', 'old_roll_no3': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=50)
    old_roll_no=models.CharField('箱号', null=False, blank=True, max_length=20)
    old_length_qty=models.DecimalField('长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('毛重', null=True, blank=True, max_digits=10, decimal_places=2)
    old_storage_unit_id=models.CharField('仓位', null=True, blank=True, max_length=100)
    old_status=models.CharField('状态', null=True, blank=True, max_length=1)
    old_out_detail_no=models.CharField('出库明细单号', null=True, blank=True, max_length=20)
    old_bar_code=models.CharField('条码', null=False, blank=True, max_length=50)
    old_grade_id=models.CharField('色号等级', null=True, blank=True, max_length=10)
    old_gray_qty=models.DecimalField('GrayQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_adjust_qty=models.DecimalField('AdjustQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_qty=models.DecimalField('实重', null=True, blank=True, max_digits=10, decimal_places=2)
    old_meter=models.DecimalField('米数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_yard=models.DecimalField('码数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_note=models.CharField('备注', null=True, blank=True, max_length=50)
    old_gray_bar_code=models.CharField('GrayBarCode', null=True, blank=True, max_length=100)
    old_roll_no3=models.CharField('RollNo3', null=True, blank=True, max_length=20)
    old_gunit=models.IntegerField('GUnit', null=True, blank=True)
    old_punit=models.IntegerField('PUnit', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_defectiveinrecord'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no', 'old_roll_no'],name='src_d0f466e2bdf95b5e'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),Upper(RTrim(models.F('old_roll_no'))),name='src_ci_d0f466e2bdf95b5e')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（DefectiveInRecord，待确认）'
        ordering=["-id"]

class SourceDyeDefectiveOut(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DefectiveOut'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('单号', null=False, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('审核日期', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_defectiveout'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_44680fa9d15d3f5d'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_44680fa9d15d3f5d')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（DefectiveOut，待确认）'
        ordering=["-id"]

class SourceDyeDefectiveOutDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DefectiveOutDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'JobSheetNo': 'old_job_sheet_no', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'CustomerProdName': 'old_customer_prod_name', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'CustColorNum': 'old_cust_color_num', 'Weight': 'old_weight', 'Width': 'old_width', 'Rolls': 'old_rolls', 'WeightQty': 'old_weight_qty', 'LengthQty': 'old_length_qty', 'Description': 'old_description', 'Remarks': 'old_remarks', 'DefectiveInDetailNo': 'old_defective_in_detail_no', 'GrayQty': 'old_gray_qty', 'JingZhong': 'old_jing_zhong', 'ShiZhong': 'old_shi_zhong', 'ZhiTong': 'old_zhi_tong', 'KongJia': 'old_kong_jia', 'OrderSheetDate': 'old_order_sheet_date'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_customer_prod_name': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_cust_color_num': 'Chinese_PRC_CI_AS', 'old_weight': 'Chinese_PRC_CI_AS', 'old_width': 'Chinese_PRC_CI_AS', 'old_description': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_defective_in_detail_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：DefectiveOut', 'target': 'erp_quality.SourceDyeDefectiveOut', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 DefectiveOutDetail → DefectiveOut']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=20)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=20)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=10)
    old_customer_prod_name=models.CharField('客户纱种', null=True, blank=True, max_length=100)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=150)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=20)
    old_cust_color_num=models.CharField('客户色号', null=True, blank=True, max_length=150)
    old_weight=models.CharField('克重', null=True, blank=True, max_length=256)
    old_width=models.CharField('幅宽', null=True, blank=True, max_length=256)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_weight_qty=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_length_qty=models.DecimalField('长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_description=models.CharField('描述', null=True, blank=True, max_length=512)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_defective_in_detail_no=models.CharField('次品入库明细', null=True, blank=True, max_length=20)
    old_gray_qty=models.DecimalField('胚重', null=True, blank=True, max_digits=8, decimal_places=2)
    old_jing_zhong=models.DecimalField('净重', null=True, blank=True, max_digits=10, decimal_places=2)
    old_shi_zhong=models.DecimalField('实重', null=True, blank=True, max_digits=10, decimal_places=2)
    old_zhi_tong=models.DecimalField('纸筒', null=True, blank=True, max_digits=6, decimal_places=1)
    old_kong_jia=models.DecimalField('空加', null=True, blank=True, max_digits=6, decimal_places=1)
    old_order_sheet_date=models.DateTimeField('OrderSheetDate', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_quality.SourceDyeDefectiveOut', verbose_name='原关系：DefectiveOut', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_defectiveoutdetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_637ce9b38cd8e0bc'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_637ce9b38cd8e0bc')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（DefectiveOutDetail，待确认）'
        ordering=["-id"]

class SourceDyeDefectiveOutRecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DefectiveOutRecord'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'BarCode': 'old_bar_code', 'RollNo': 'old_roll_no', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'StorageUnitID': 'old_storage_unit_id', 'Status': 'old_status', 'OutDetailNo': 'old_out_detail_no', 'GradeID': 'old_grade_id', 'GrayQty': 'old_gray_qty', 'AdjustQty': 'old_adjust_qty', 'RealQty': 'old_real_qty', 'Meter': 'old_meter', 'Yard': 'old_yard', 'GrayBarCode': 'old_gray_bar_code', 'RollNo3': 'old_roll_no3', 'GUnit': 'old_gunit', 'PUnit': 'old_punit', 'GKg': 'old_gkg', 'GPound': 'old_gpound', 'PKg': 'old_pkg', 'PPound': 'old_ppound', 'Rolls': 'old_rolls'}
    SOURCE_KEY=('SheetSeries', 'DetailNo', 'BarCode', 'RollNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_bar_code': 'Chinese_PRC_CI_AS', 'old_roll_no': 'Chinese_PRC_CI_AS', 'old_storage_unit_id': 'Chinese_PRC_CI_AS', 'old_status': 'Chinese_PRC_CI_AS', 'old_out_detail_no': 'Chinese_PRC_CI_AS', 'old_grade_id': 'Chinese_PRC_CI_AS', 'old_gray_bar_code': 'Chinese_PRC_CI_AS', 'old_roll_no3': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：DefectiveOutDetail', 'target': 'erp_quality.SourceDyeDefectiveOutDetail', 'source_fields': ['SheetSeries', 'DetailNo'], 'target_fields': ['SheetSeries', 'DetailNo'], 'evidence': ['原界面主从 DefectiveOutRecord → DefectiveOutDetail']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('出库单流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('出库明细号', null=False, blank=True, max_length=36)
    old_bar_code=models.CharField('条码', null=False, blank=True, max_length=50)
    old_roll_no=models.CharField('箱号', null=False, blank=True, max_length=20)
    old_length_qty=models.DecimalField('成品长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('成品重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_storage_unit_id=models.CharField('库位', null=True, blank=True, max_length=100)
    old_status=models.CharField('状态', null=True, blank=True, max_length=1)
    old_out_detail_no=models.CharField('OutDetailNo', null=True, blank=True, max_length=20)
    old_grade_id=models.CharField('色号等级', null=True, blank=True, max_length=10)
    old_gray_qty=models.DecimalField('胚纱重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_adjust_qty=models.DecimalField('AdjustQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_qty=models.DecimalField('实重', null=True, blank=True, max_digits=10, decimal_places=2)
    old_meter=models.DecimalField('米数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_yard=models.DecimalField('胚纱长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_gray_bar_code=models.CharField('GrayBarCode', null=True, blank=True, max_length=100)
    old_roll_no3=models.CharField('箱号2', null=True, blank=True, max_length=20)
    old_gunit=models.IntegerField('GUnit', null=True, blank=True)
    old_punit=models.IntegerField('PUnit', null=True, blank=True)
    old_gkg=models.DecimalField('GKg', null=True, blank=True, max_digits=6, decimal_places=2)
    old_gpound=models.DecimalField('GPound', null=True, blank=True, max_digits=6, decimal_places=2)
    old_pkg=models.DecimalField('PKg', null=True, blank=True, max_digits=6, decimal_places=2)
    old_ppound=models.DecimalField('PPound', null=True, blank=True, max_digits=6, decimal_places=2)
    old_rolls=models.DecimalField('Rolls', null=True, blank=True, max_digits=4, decimal_places=2)
    source_parent_1=models.ForeignKey('erp_quality.SourceDyeDefectiveOutDetail', verbose_name='原关系：DefectiveOutDetail', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_defectiveoutrecord'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no', 'old_bar_code', 'old_roll_no'],name='src_d2935d46b200f99e'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),Upper(RTrim(models.F('old_bar_code'))),Upper(RTrim(models.F('old_roll_no'))),name='src_ci_d2935d46b200f99e')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（DefectiveOutRecord，待确认）'
        ordering=["-id"]

class SourceDyeDyeCheck(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DyeCheck'
    SOURCE_FIELDS={'ID': 'old_id', 'JobSheetNo': 'old_job_sheet_no', 'DyePhaseID': 'old_dye_phase_id', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'ProcessID': 'old_process_id'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_dye_phase_id': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_process_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_id=models.BigIntegerField('ID', null=False, blank=False)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)
    old_dye_phase_id=models.CharField('DyePhaseID', null=True, blank=True, max_length=10)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_process_id=models.CharField('ProcessID', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_dyecheck'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_f5e070e36ec9c592')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（DyeCheck，待确认）'
        ordering=["-id"]

class SourceDyeDyeCheckout(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='dyeCheckout'
    SOURCE_FIELDS={'WProcessNo': 'old_wprocess_no', 'DAYS': 'old_days', 'JobSheetNo': 'old_job_sheet_no', 'ProdID': 'old_prod_id', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'CustomerID': 'old_customer_id', 'ShiftID': 'old_shift_id', 'Class': 'old_class', 'ClassID': 'old_class_id', 'StationID': 'old_station_id', 'EndTime': 'old_end_time', 'JobProdKind': 'old_job_prod_kind', 'MachineID': 'old_machine_id', 'ColorMatching': 'old_color_matching', 'ZNum': 'old_znum', 'JNum': 'old_jnum', 'JKg': 'old_jkg', 'RNum': 'old_rnum', 'RTKg': 'old_rtkg', 'TNum': 'old_tnum', 'Rolls': 'old_rolls', 'ClothQtyKg': 'old_cloth_qty_kg', 'NumNo': 'old_num_no', 'ZKg': 'old_zkg', 'FBEmpID': 'old_fbemp_id', 'StartTime': 'old_start_time', 'DTime': 'old_dtime', 'JTimes': 'old_jtimes', 'IsDown': 'old_is_down', 'dyeEmpID': 'old_dye_emp_id', 'dyeEmpName': 'old_dye_emp_name', 'ProcessID': 'old_process_id', 'ColorDepthID': 'old_color_depth_id', 'TMonth': 'old_tmonth', 'AddNumber1': 'old_add_number1', 'AddNumber2': 'old_add_number2', 'WDNum': 'old_wdnum', 'DefectClassID': 'old_defect_class_id', 'DefectEmpID': 'old_defect_emp_id'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_wprocess_no': 'Chinese_PRC_CI_AS', 'old_days': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_shift_id': 'Chinese_PRC_CI_AS', 'old_class': 'Chinese_PRC_CI_AS', 'old_class_id': 'Chinese_PRC_CI_AS', 'old_station_id': 'Chinese_PRC_CI_AS', 'old_job_prod_kind': 'Chinese_PRC_CI_AS', 'old_machine_id': 'Chinese_PRC_CI_AS', 'old_color_matching': 'Chinese_PRC_CI_AS', 'old_num_no': 'Chinese_PRC_CI_AS', 'old_fbemp_id': 'Chinese_PRC_CI_AS', 'old_dye_emp_id': 'Chinese_PRC_CI_AS', 'old_dye_emp_name': 'Chinese_PRC_CI_AS', 'old_process_id': 'Chinese_PRC_CI_AS', 'old_color_depth_id': 'Chinese_PRC_CI_AS', 'old_tmonth': 'Chinese_PRC_CI_AS', 'old_defect_class_id': 'Chinese_PRC_CI_AS', 'old_defect_emp_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_wprocess_no=models.CharField('WProcessNo', null=True, blank=True, max_length=50)
    old_days=models.CharField('DAYS', null=True, blank=True, max_length=10)
    old_job_sheet_no=models.CharField('JobSheetNo', null=False, blank=True, max_length=50)
    old_prod_id=models.CharField('ProdID', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=50)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=50)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=50)
    old_shift_id=models.CharField('ShiftID', null=True, blank=True, max_length=50)
    old_class=models.CharField('Class', null=True, blank=True, max_length=50)
    old_class_id=models.CharField('ClassID', null=True, blank=True, max_length=50)
    old_station_id=models.CharField('StationID', null=True, blank=True, max_length=50)
    old_end_time=models.DateTimeField('EndTime', null=True, blank=True)
    old_job_prod_kind=models.CharField('JobProdKind', null=True, blank=True, max_length=50)
    old_machine_id=models.CharField('MachineID', null=True, blank=True, max_length=50)
    old_color_matching=models.CharField('ColorMatching', null=True, blank=True, max_length=50)
    old_znum=models.IntegerField('ZNum', null=True, blank=True)
    old_jnum=models.IntegerField('JNum', null=True, blank=True)
    old_jkg=models.FloatField('JKg', null=True, blank=True)
    old_rnum=models.IntegerField('RNum', null=True, blank=True)
    old_rtkg=models.FloatField('RTKg', null=True, blank=True)
    old_tnum=models.IntegerField('TNum', null=True, blank=True)
    old_rolls=models.IntegerField('Rolls', null=True, blank=True)
    old_cloth_qty_kg=models.FloatField('ClothQtyKg', null=True, blank=True)
    old_num_no=models.CharField('NumNo', null=True, blank=True, max_length=50)
    old_zkg=models.FloatField('ZKg', null=True, blank=True)
    old_fbemp_id=models.CharField('FBEmpID', null=True, blank=True, max_length=50)
    old_start_time=models.DateTimeField('StartTime', null=True, blank=True)
    old_dtime=models.FloatField('DTime', null=True, blank=True)
    old_jtimes=models.IntegerField('JTimes', null=True, blank=True)
    old_is_down=models.BooleanField('IsDown', null=True, blank=True)
    old_dye_emp_id=models.CharField('dyeEmpID', null=True, blank=True, max_length=50)
    old_dye_emp_name=models.CharField('dyeEmpName', null=True, blank=True, max_length=50)
    old_process_id=models.CharField('ProcessID', null=False, blank=True, max_length=50)
    old_color_depth_id=models.CharField('ColorDepthID', null=True, blank=True, max_length=50)
    old_tmonth=models.CharField('TMonth', null=True, blank=True, max_length=10)
    old_add_number1=models.IntegerField('AddNumber1', null=True, blank=True)
    old_add_number2=models.IntegerField('AddNumber2', null=True, blank=True)
    old_wdnum=models.IntegerField('WDNum', null=True, blank=True)
    old_defect_class_id=models.CharField('DefectClassID', null=True, blank=True, max_length=50)
    old_defect_emp_id=models.CharField('DefectEmpID', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_dyecheckout'
        indexes=[]
        verbose_name=verbose_name_plural='财务结算与成本相关表（dyeCheckout，待确认）'
        ordering=["-id"]

class SourceDyeInspectionLog(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='InspectionLog'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'EmpID': 'old_emp_id', 'InspectDetailNo': 'old_inspect_detail_no', 'Inspector': 'old_inspector', 'InspectorList': 'old_inspector_list', 'InspectDate': 'old_inspect_date', 'InspectionSurvey': 'old_inspection_survey', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'MachineID': 'old_machine_id', 'MachineName': 'old_machine_name', 'MachineLocation': 'old_machine_location'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_emp_id': 'Chinese_PRC_CI_AS', 'old_inspect_detail_no': 'Chinese_PRC_CI_AS', 'old_inspector': 'Chinese_PRC_CI_AS', 'old_inspector_list': 'Chinese_PRC_CI_AS', 'old_inspection_survey': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_machine_id': 'Chinese_PRC_CI_AS', 'old_machine_name': 'Chinese_PRC_CI_AS', 'old_machine_location': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('单号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('巡检日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('巡检类型', null=True, blank=True)
    old_emp_id=models.CharField('EmpID', null=True, blank=True, max_length=50)
    old_inspect_detail_no=models.CharField('InspectDetailNo', null=True, blank=True, max_length=50)
    old_inspector=models.CharField('巡检人', null=True, blank=True, max_length=20)
    old_inspector_list=models.CharField('InspectorList', null=True, blank=True, max_length=200)
    old_inspect_date=models.DateTimeField('InspectDate', null=True, blank=True)
    old_inspection_survey=models.CharField('巡检概况', null=True, blank=True, max_length=200)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=1000)
    old_creater=models.CharField('制单人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('制单日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_machine_id=models.CharField('MachineID', null=True, blank=True, max_length=50)
    old_machine_name=models.CharField('MachineName', null=True, blank=True, max_length=50)
    old_machine_location=models.CharField('MachineLocation', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_inspectionlog'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_eb49f9ad4fd018a4'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_eb49f9ad4fd018a4')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（InspectionLog，待确认）'
        ordering=["-id"]

class SourceDyeInspectionLogDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='InspectionLogDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'FaultSheetSeries': 'old_fault_sheet_series', 'FaultSheetNo': 'old_fault_sheet_no', 'FaultSheetDate': 'old_fault_sheet_date', 'FaultSheetKind': 'old_fault_sheet_kind', 'MachineID': 'old_machine_id', 'EmpID': 'old_emp_id', 'HappenTime': 'old_happen_time', 'ApplyTime': 'old_apply_time', 'DeptID': 'old_dept_id', 'ShiftID': 'old_shift_id', 'FaultID': 'old_fault_id', 'SeverityID': 'old_severity_id', 'HandlerIDs': 'old_handler_ids', 'Handlers': 'old_handlers', 'StartTime': 'old_start_time', 'EndTime': 'old_end_time', 'ResultID': 'old_result_id', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'SheetStatus': 'old_sheet_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'HandleIdea': 'old_handle_idea', 'PhotoAddress': 'old_photo_address', 'ApproveIdea': 'old_approve_idea', 'PatrolDetailNo': 'old_patrol_detail_no', 'SheetType': 'old_sheet_type', 'StationID': 'old_station_id', 'BusinessUnitID': 'old_business_unit_id', 'FaultRemarks': 'old_fault_remarks', 'MachineName': 'old_machine_name', 'MachineLocation': 'old_machine_location', 'Urgent': 'old_urgent', 'FlowStatus': 'old_flow_status'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_fault_sheet_series': 'Chinese_PRC_CI_AS', 'old_fault_sheet_no': 'Chinese_PRC_CI_AS', 'old_fault_sheet_kind': 'Chinese_PRC_CI_AS', 'old_machine_id': 'Chinese_PRC_CI_AS', 'old_emp_id': 'Chinese_PRC_CI_AS', 'old_dept_id': 'Chinese_PRC_CI_AS', 'old_shift_id': 'Chinese_PRC_CI_AS', 'old_fault_id': 'Chinese_PRC_CI_AS', 'old_severity_id': 'Chinese_PRC_CI_AS', 'old_handler_ids': 'Chinese_PRC_CI_AS', 'old_handlers': 'Chinese_PRC_CI_AS', 'old_result_id': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_handle_idea': 'Chinese_PRC_CI_AS', 'old_photo_address': 'Chinese_PRC_CI_AS', 'old_approve_idea': 'Chinese_PRC_CI_AS', 'old_patrol_detail_no': 'Chinese_PRC_CI_AS', 'old_sheet_type': 'Chinese_PRC_CI_AS', 'old_station_id': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_fault_remarks': 'Chinese_PRC_CI_AS', 'old_machine_name': 'Chinese_PRC_CI_AS', 'old_machine_location': 'Chinese_PRC_CI_AS', 'old_flow_status': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：InspectionLog', 'target': 'erp_quality.SourceDyeInspectionLog', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 InspectionLogDetail → InspectionLog']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=False, blank=True, max_length=36)
    old_fault_sheet_series=models.CharField('报修单流水号', null=True, blank=True, max_length=20)
    old_fault_sheet_no=models.CharField('报修单号', null=True, blank=True, max_length=20)
    old_fault_sheet_date=models.DateTimeField('报修日期', null=True, blank=True)
    old_fault_sheet_kind=models.CharField('报修类型', null=True, blank=True, max_length=20)
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
    old_handle_idea=models.CharField('HandleIdea', null=True, blank=True, max_length=512)
    old_photo_address=models.CharField('PhotoAddress', null=True, blank=True, max_length=512)
    old_approve_idea=models.CharField('ApproveIdea', null=True, blank=True, max_length=200)
    old_patrol_detail_no=models.CharField('PatrolDetailNo', null=True, blank=True, max_length=100)
    old_sheet_type=models.CharField('报修类别', null=True, blank=True, max_length=10)
    old_station_id=models.CharField('站别', null=True, blank=True, max_length=30)
    old_business_unit_id=models.CharField('经营单位', null=True, blank=True, max_length=30)
    old_fault_remarks=models.CharField('报修备注', null=True, blank=True, max_length=200)
    old_machine_name=models.CharField('MachineName', null=True, blank=True, max_length=64)
    old_machine_location=models.CharField('MachineLocation', null=True, blank=True, max_length=64)
    old_urgent=models.IntegerField('Urgent', null=True, blank=True)
    old_flow_status=models.CharField('FlowStatus', null=True, blank=True, max_length=20)
    source_parent_1=models.ForeignKey('erp_quality.SourceDyeInspectionLog', verbose_name='原关系：InspectionLog', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_inspectionlogdetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_a253eebccee88bc2'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_a253eebccee88bc2')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（InspectionLogDetail，待确认）'
        ordering=["-id"]

class SourceDyeInspectionProject(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='InspectionProject'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'SortNo': 'old_sort_no', 'SerialNum': 'old_serial_num', 'ProjectInfo': 'old_project_info', 'Value': 'old_value', 'DefaultValue': 'old_default_value', 'Remarks': 'old_remarks', 'CaseDetailNo': 'old_case_detail_no', 'Result': 'old_result', 'IsInputText': 'old_is_input_text'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_serial_num': 'Chinese_PRC_CI_AS', 'old_project_info': 'Chinese_PRC_CI_AS', 'old_value': 'Chinese_PRC_CI_AS', 'old_default_value': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_case_detail_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
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
        db_table='src_dye_inspectionproject'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_9f02085334aee7df'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_9f02085334aee7df')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（InspectionProject，待确认）'
        ordering=["-id"]

class SourceDyePTestItem(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_TestItem'
    SOURCE_FIELDS={'ItemID': 'old_item_id', 'ItemName': 'old_item_name', 'FieldType': 'old_field_type', 'UnitStr': 'old_unit_str', 'Standard': 'old_standard', 'SortNo': 'old_sort_no', 'IsStop': 'old_is_stop', 'Description': 'old_description'}
    SOURCE_KEY=('ItemID',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_item_id': 'Chinese_PRC_CI_AS', 'old_item_name': 'Chinese_PRC_CI_AS', 'old_unit_str': 'Chinese_PRC_CI_AS', 'old_standard': 'Chinese_PRC_CI_AS', 'old_description': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_item_id=models.CharField('ItemID', null=False, blank=True, max_length=10)
    old_item_name=models.CharField('ItemName', null=True, blank=True, max_length=50)
    old_field_type=models.IntegerField('FieldType', null=True, blank=True)
    old_unit_str=models.CharField('UnitStr', null=True, blank=True, max_length=6)
    old_standard=models.CharField('Standard', null=True, blank=True, max_length=50)
    old_sort_no=models.IntegerField('SortNo', null=True, blank=True)
    old_is_stop=models.BooleanField('IsStop', null=True, blank=True)
    old_description=models.CharField('Description', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_testitem'
        indexes=[models.Index(fields=['source_batch', 'old_item_id'],name='src_2babd68e0b1f86cd'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_item_id'))),name='src_ci_2babd68e0b1f86cd')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（p_TestItem，待确认）'
        ordering=["-id"]

class SourceDyeProdTest(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProdTest'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'JobSheetNo': 'old_job_sheet_no', 'CustomerID': 'old_customer_id', 'DetailCustName': 'old_detail_cust_name', 'ProdID': 'old_prod_id', 'LotNo': 'old_lot_no', 'Spec': 'old_spec', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'Weight': 'old_weight', 'WeightQty': 'old_weight_qty', 'LengthQty': 'old_length_qty', 'ShiftID': 'old_shift_id', 'Maker': 'old_maker', 'CheckResult': 'old_check_result', 'ItemID01': 'old_item_id01', 'ItemName01': 'old_item_name01', 'Value01': 'old_value01', 'ItemID02': 'old_item_id02', 'ItemName02': 'old_item_name02', 'Value02': 'old_value02', 'ItemID03': 'old_item_id03', 'ItemName03': 'old_item_name03', 'Value03': 'old_value03', 'ItemID04': 'old_item_id04', 'ItemName04': 'old_item_name04', 'Value04': 'old_value04', 'ItemID05': 'old_item_id05', 'ItemName05': 'old_item_name05', 'Value05': 'old_value05', 'ItemID06': 'old_item_id06', 'ItemName06': 'old_item_name06', 'Value06': 'old_value06', 'ItemID07': 'old_item_id07', 'ItemName07': 'old_item_name07', 'Value07': 'old_value07', 'ItemID08': 'old_item_id08', 'ItemName08': 'old_item_name08', 'Value08': 'old_value08', 'ItemID09': 'old_item_id09', 'ItemName09': 'old_item_name09', 'Value09': 'old_value09', 'ItemID10': 'old_item_id10', 'ItemName10': 'old_item_name10', 'Value10': 'old_value10', 'ItemID11': 'old_item_id11', 'ItemName11': 'old_item_name11', 'Value11': 'old_value11', 'ItemID12': 'old_item_id12', 'ItemName12': 'old_item_name12', 'Value12': 'old_value12', 'ItemID13': 'old_item_id13', 'ItemName13': 'old_item_name13', 'Value13': 'old_value13', 'ItemID14': 'old_item_id14', 'ItemName14': 'old_item_name14', 'Value14': 'old_value14', 'ItemID15': 'old_item_id15', 'ItemName15': 'old_item_name15', 'Value15': 'old_value15', 'ItemID16': 'old_item_id16', 'ItemName16': 'old_item_name16', 'Value16': 'old_value16', 'ItemID17': 'old_item_id17', 'ItemName17': 'old_item_name17', 'Value17': 'old_value17', 'ItemID18': 'old_item_id18', 'ItemName18': 'old_item_name18', 'Value18': 'old_value18', 'ItemID19': 'old_item_id19', 'ItemName19': 'old_item_name19', 'Value19': 'old_value19', 'ItemID20': 'old_item_id20', 'ItemName20': 'old_item_name20', 'Value20': 'old_value20', 'ItemID21': 'old_item_id21', 'ItemName21': 'old_item_name21', 'Value21': 'old_value21', 'ItemID22': 'old_item_id22', 'ItemName22': 'old_item_name22', 'Value22': 'old_value22', 'ItemID23': 'old_item_id23', 'ItemName23': 'old_item_name23', 'Value23': 'old_value23', 'ItemID24': 'old_item_id24', 'ItemName24': 'old_item_name24', 'Value24': 'old_value24', 'ItemID25': 'old_item_id25', 'ItemName25': 'old_item_name25', 'Value25': 'old_value25', 'ItemID26': 'old_item_id26', 'ItemName26': 'old_item_name26', 'Value26': 'old_value26', 'ItemID27': 'old_item_id27', 'ItemName27': 'old_item_name27', 'Value27': 'old_value27', 'ItemID28': 'old_item_id28', 'ItemName28': 'old_item_name28', 'Value28': 'old_value28', 'ItemID29': 'old_item_id29', 'ItemName29': 'old_item_name29', 'Value29': 'old_value29', 'ItemID30': 'old_item_id30', 'ItemName30': 'old_item_name30', 'Value30': 'old_value30', 'ItemID31': 'old_item_id31', 'ItemName31': 'old_item_name31', 'Value31': 'old_value31', 'ItemID32': 'old_item_id32', 'ItemName32': 'old_item_name32', 'Value32': 'old_value32', 'ItemID33': 'old_item_id33', 'ItemName33': 'old_item_name33', 'Value33': 'old_value33', 'ItemID34': 'old_item_id34', 'ItemName34': 'old_item_name34', 'Value34': 'old_value34', 'ItemID35': 'old_item_id35', 'ItemName35': 'old_item_name35', 'Value35': 'old_value35', 'ItemID36': 'old_item_id36', 'ItemName36': 'old_item_name36', 'Value36': 'old_value36', 'ItemID37': 'old_item_id37', 'ItemName37': 'old_item_name37', 'Value37': 'old_value37', 'ItemID38': 'old_item_id38', 'ItemName38': 'old_item_name38', 'Value38': 'old_value38', 'ItemID39': 'old_item_id39', 'ItemName39': 'old_item_name39', 'Value39': 'old_value39', 'ItemID40': 'old_item_id40', 'ItemName40': 'old_item_name40', 'Value40': 'old_value40', 'SheetStatus': 'old_sheet_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Rolls': 'old_rolls', 'EmpID': 'old_emp_id', 'DeptID': 'old_dept_id', 'CheckNo': 'old_check_no', 'StuffID': 'old_stuff_id', 'CompareStuffID': 'old_compare_stuff_id', 'SupplierID': 'old_supplier_id', 'CompareSupplierID': 'old_compare_supplier_id', 'CompareLotNo': 'old_compare_lot_no'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_detail_cust_name': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_shift_id': 'Chinese_PRC_CI_AS', 'old_maker': 'Chinese_PRC_CI_AS', 'old_check_result': 'Chinese_PRC_CI_AS', 'old_item_id01': 'Chinese_PRC_CI_AS', 'old_item_name01': 'Chinese_PRC_CI_AS', 'old_value01': 'Chinese_PRC_CI_AS', 'old_item_id02': 'Chinese_PRC_CI_AS', 'old_item_name02': 'Chinese_PRC_CI_AS', 'old_value02': 'Chinese_PRC_CI_AS', 'old_item_id03': 'Chinese_PRC_CI_AS', 'old_item_name03': 'Chinese_PRC_CI_AS', 'old_value03': 'Chinese_PRC_CI_AS', 'old_item_id04': 'Chinese_PRC_CI_AS', 'old_item_name04': 'Chinese_PRC_CI_AS', 'old_value04': 'Chinese_PRC_CI_AS', 'old_item_id05': 'Chinese_PRC_CI_AS', 'old_item_name05': 'Chinese_PRC_CI_AS', 'old_value05': 'Chinese_PRC_CI_AS', 'old_item_id06': 'Chinese_PRC_CI_AS', 'old_item_name06': 'Chinese_PRC_CI_AS', 'old_value06': 'Chinese_PRC_CI_AS', 'old_item_id07': 'Chinese_PRC_CI_AS', 'old_item_name07': 'Chinese_PRC_CI_AS', 'old_value07': 'Chinese_PRC_CI_AS', 'old_item_id08': 'Chinese_PRC_CI_AS', 'old_item_name08': 'Chinese_PRC_CI_AS', 'old_value08': 'Chinese_PRC_CI_AS', 'old_item_id09': 'Chinese_PRC_CI_AS', 'old_item_name09': 'Chinese_PRC_CI_AS', 'old_value09': 'Chinese_PRC_CI_AS', 'old_item_id10': 'Chinese_PRC_CI_AS', 'old_item_name10': 'Chinese_PRC_CI_AS', 'old_value10': 'Chinese_PRC_CI_AS', 'old_item_id11': 'Chinese_PRC_CI_AS', 'old_item_name11': 'Chinese_PRC_CI_AS', 'old_value11': 'Chinese_PRC_CI_AS', 'old_item_id12': 'Chinese_PRC_CI_AS', 'old_item_name12': 'Chinese_PRC_CI_AS', 'old_value12': 'Chinese_PRC_CI_AS', 'old_item_id13': 'Chinese_PRC_CI_AS', 'old_item_name13': 'Chinese_PRC_CI_AS', 'old_value13': 'Chinese_PRC_CI_AS', 'old_item_id14': 'Chinese_PRC_CI_AS', 'old_item_name14': 'Chinese_PRC_CI_AS', 'old_value14': 'Chinese_PRC_CI_AS', 'old_item_id15': 'Chinese_PRC_CI_AS', 'old_item_name15': 'Chinese_PRC_CI_AS', 'old_value15': 'Chinese_PRC_CI_AS', 'old_item_id16': 'Chinese_PRC_CI_AS', 'old_item_name16': 'Chinese_PRC_CI_AS', 'old_value16': 'Chinese_PRC_CI_AS', 'old_item_id17': 'Chinese_PRC_CI_AS', 'old_item_name17': 'Chinese_PRC_CI_AS', 'old_value17': 'Chinese_PRC_CI_AS', 'old_item_id18': 'Chinese_PRC_CI_AS', 'old_item_name18': 'Chinese_PRC_CI_AS', 'old_value18': 'Chinese_PRC_CI_AS', 'old_item_id19': 'Chinese_PRC_CI_AS', 'old_item_name19': 'Chinese_PRC_CI_AS', 'old_value19': 'Chinese_PRC_CI_AS', 'old_item_id20': 'Chinese_PRC_CI_AS', 'old_item_name20': 'Chinese_PRC_CI_AS', 'old_value20': 'Chinese_PRC_CI_AS', 'old_item_id21': 'Chinese_PRC_CI_AS', 'old_item_name21': 'Chinese_PRC_CI_AS', 'old_value21': 'Chinese_PRC_CI_AS', 'old_item_id22': 'Chinese_PRC_CI_AS', 'old_item_name22': 'Chinese_PRC_CI_AS', 'old_value22': 'Chinese_PRC_CI_AS', 'old_item_id23': 'Chinese_PRC_CI_AS', 'old_item_name23': 'Chinese_PRC_CI_AS', 'old_value23': 'Chinese_PRC_CI_AS', 'old_item_id24': 'Chinese_PRC_CI_AS', 'old_item_name24': 'Chinese_PRC_CI_AS', 'old_value24': 'Chinese_PRC_CI_AS', 'old_item_id25': 'Chinese_PRC_CI_AS', 'old_item_name25': 'Chinese_PRC_CI_AS', 'old_value25': 'Chinese_PRC_CI_AS', 'old_item_id26': 'Chinese_PRC_CI_AS', 'old_item_name26': 'Chinese_PRC_CI_AS', 'old_value26': 'Chinese_PRC_CI_AS', 'old_item_id27': 'Chinese_PRC_CI_AS', 'old_item_name27': 'Chinese_PRC_CI_AS', 'old_value27': 'Chinese_PRC_CI_AS', 'old_item_id28': 'Chinese_PRC_CI_AS', 'old_item_name28': 'Chinese_PRC_CI_AS', 'old_value28': 'Chinese_PRC_CI_AS', 'old_item_id29': 'Chinese_PRC_CI_AS', 'old_item_name29': 'Chinese_PRC_CI_AS', 'old_value29': 'Chinese_PRC_CI_AS', 'old_item_id30': 'Chinese_PRC_CI_AS', 'old_item_name30': 'Chinese_PRC_CI_AS', 'old_value30': 'Chinese_PRC_CI_AS', 'old_item_id31': 'Chinese_PRC_CI_AS', 'old_item_name31': 'Chinese_PRC_CI_AS', 'old_value31': 'Chinese_PRC_CI_AS', 'old_item_id32': 'Chinese_PRC_CI_AS', 'old_item_name32': 'Chinese_PRC_CI_AS', 'old_value32': 'Chinese_PRC_CI_AS', 'old_item_id33': 'Chinese_PRC_CI_AS', 'old_item_name33': 'Chinese_PRC_CI_AS', 'old_value33': 'Chinese_PRC_CI_AS', 'old_item_id34': 'Chinese_PRC_CI_AS', 'old_item_name34': 'Chinese_PRC_CI_AS', 'old_value34': 'Chinese_PRC_CI_AS', 'old_item_id35': 'Chinese_PRC_CI_AS', 'old_item_name35': 'Chinese_PRC_CI_AS', 'old_value35': 'Chinese_PRC_CI_AS', 'old_item_id36': 'Chinese_PRC_CI_AS', 'old_item_name36': 'Chinese_PRC_CI_AS', 'old_value36': 'Chinese_PRC_CI_AS', 'old_item_id37': 'Chinese_PRC_CI_AS', 'old_item_name37': 'Chinese_PRC_CI_AS', 'old_value37': 'Chinese_PRC_CI_AS', 'old_item_id38': 'Chinese_PRC_CI_AS', 'old_item_name38': 'Chinese_PRC_CI_AS', 'old_value38': 'Chinese_PRC_CI_AS', 'old_item_id39': 'Chinese_PRC_CI_AS', 'old_item_name39': 'Chinese_PRC_CI_AS', 'old_value39': 'Chinese_PRC_CI_AS', 'old_item_id40': 'Chinese_PRC_CI_AS', 'old_item_name40': 'Chinese_PRC_CI_AS', 'old_value40': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_emp_id': 'Chinese_PRC_CI_AS', 'old_dept_id': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_stuff_id': 'Chinese_PRC_CI_AS', 'old_compare_stuff_id': 'Chinese_PRC_CI_AS', 'old_supplier_id': 'Chinese_PRC_CI_AS', 'old_compare_supplier_id': 'Chinese_PRC_CI_AS', 'old_compare_lot_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=36)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_customer_id=models.CharField('客户代码', null=True, blank=True, max_length=50)
    old_detail_cust_name=models.CharField('明细客户', null=True, blank=True, max_length=150)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=200)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=200)
    old_color_id=models.CharField('颜色编码', null=True, blank=True, max_length=50)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=100)
    old_weight=models.DecimalField('克重', null=True, blank=True, max_digits=6, decimal_places=2)
    old_weight_qty=models.DecimalField('重量数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_length_qty=models.DecimalField('长度数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_shift_id=models.CharField('班组代码', null=True, blank=True, max_length=50)
    old_maker=models.CharField('测试人', null=True, blank=True, max_length=50)
    old_check_result=models.CharField('检测意见', null=True, blank=True, max_length=100)
    old_item_id01=models.CharField('测试项目01', null=True, blank=True, max_length=10)
    old_item_name01=models.CharField('测试项目名称1', null=True, blank=True, max_length=50)
    old_value01=models.CharField('标准值01', null=True, blank=True, max_length=20)
    old_item_id02=models.CharField('测试项目02', null=True, blank=True, max_length=10)
    old_item_name02=models.CharField('测试项目名称2', null=True, blank=True, max_length=50)
    old_value02=models.CharField('标准值02', null=True, blank=True, max_length=20)
    old_item_id03=models.CharField('测试项目03', null=True, blank=True, max_length=10)
    old_item_name03=models.CharField('测试项目名称3', null=True, blank=True, max_length=50)
    old_value03=models.CharField('标准值03', null=True, blank=True, max_length=20)
    old_item_id04=models.CharField('测试项目04', null=True, blank=True, max_length=10)
    old_item_name04=models.CharField('测试项目名称4', null=True, blank=True, max_length=50)
    old_value04=models.CharField('标准值04', null=True, blank=True, max_length=20)
    old_item_id05=models.CharField('测试项目05', null=True, blank=True, max_length=10)
    old_item_name05=models.CharField('ItemName05', null=True, blank=True, max_length=50)
    old_value05=models.CharField('标准值05', null=True, blank=True, max_length=20)
    old_item_id06=models.CharField('测试项目06', null=True, blank=True, max_length=10)
    old_item_name06=models.CharField('ItemName06', null=True, blank=True, max_length=50)
    old_value06=models.CharField('标准值06', null=True, blank=True, max_length=20)
    old_item_id07=models.CharField('测试项目07', null=True, blank=True, max_length=10)
    old_item_name07=models.CharField('ItemName07', null=True, blank=True, max_length=50)
    old_value07=models.CharField('标准值07', null=True, blank=True, max_length=20)
    old_item_id08=models.CharField('测试项目08', null=True, blank=True, max_length=10)
    old_item_name08=models.CharField('ItemName08', null=True, blank=True, max_length=50)
    old_value08=models.CharField('标准值08', null=True, blank=True, max_length=20)
    old_item_id09=models.CharField('测试项目09', null=True, blank=True, max_length=10)
    old_item_name09=models.CharField('ItemName09', null=True, blank=True, max_length=50)
    old_value09=models.CharField('标准值09', null=True, blank=True, max_length=20)
    old_item_id10=models.CharField('测试项目10', null=True, blank=True, max_length=10)
    old_item_name10=models.CharField('ItemName10', null=True, blank=True, max_length=50)
    old_value10=models.CharField('标准值10', null=True, blank=True, max_length=20)
    old_item_id11=models.CharField('测试项目11', null=True, blank=True, max_length=10)
    old_item_name11=models.CharField('ItemName11', null=True, blank=True, max_length=50)
    old_value11=models.CharField('标准值11', null=True, blank=True, max_length=500)
    old_item_id12=models.CharField('测试项目12', null=True, blank=True, max_length=10)
    old_item_name12=models.CharField('ItemName12', null=True, blank=True, max_length=50)
    old_value12=models.CharField('标准值12', null=True, blank=True, max_length=20)
    old_item_id13=models.CharField('测试项目13', null=True, blank=True, max_length=10)
    old_item_name13=models.CharField('ItemName13', null=True, blank=True, max_length=50)
    old_value13=models.CharField('标准值13', null=True, blank=True, max_length=20)
    old_item_id14=models.CharField('测试项目14', null=True, blank=True, max_length=10)
    old_item_name14=models.CharField('ItemName14', null=True, blank=True, max_length=50)
    old_value14=models.CharField('标准值14', null=True, blank=True, max_length=20)
    old_item_id15=models.CharField('测试项目15', null=True, blank=True, max_length=10)
    old_item_name15=models.CharField('ItemName15', null=True, blank=True, max_length=50)
    old_value15=models.CharField('标准值15', null=True, blank=True, max_length=20)
    old_item_id16=models.CharField('测试项目16', null=True, blank=True, max_length=10)
    old_item_name16=models.CharField('ItemName16', null=True, blank=True, max_length=50)
    old_value16=models.CharField('标准值16', null=True, blank=True, max_length=20)
    old_item_id17=models.CharField('测试项目17', null=True, blank=True, max_length=10)
    old_item_name17=models.CharField('ItemName17', null=True, blank=True, max_length=50)
    old_value17=models.CharField('标准值17', null=True, blank=True, max_length=20)
    old_item_id18=models.CharField('测试项目18', null=True, blank=True, max_length=10)
    old_item_name18=models.CharField('ItemName18', null=True, blank=True, max_length=50)
    old_value18=models.CharField('标准值18', null=True, blank=True, max_length=20)
    old_item_id19=models.CharField('测试项目19', null=True, blank=True, max_length=10)
    old_item_name19=models.CharField('ItemName19', null=True, blank=True, max_length=50)
    old_value19=models.CharField('标准值19', null=True, blank=True, max_length=20)
    old_item_id20=models.CharField('测试项目20', null=True, blank=True, max_length=10)
    old_item_name20=models.CharField('ItemName20', null=True, blank=True, max_length=50)
    old_value20=models.CharField('标准值20', null=True, blank=True, max_length=20)
    old_item_id21=models.CharField('测试项目21', null=True, blank=True, max_length=10)
    old_item_name21=models.CharField('ItemName21', null=True, blank=True, max_length=50)
    old_value21=models.CharField('标准值21', null=True, blank=True, max_length=20)
    old_item_id22=models.CharField('测试项目22', null=True, blank=True, max_length=10)
    old_item_name22=models.CharField('ItemName22', null=True, blank=True, max_length=50)
    old_value22=models.CharField('标准值22', null=True, blank=True, max_length=20)
    old_item_id23=models.CharField('测试项目23', null=True, blank=True, max_length=10)
    old_item_name23=models.CharField('ItemName23', null=True, blank=True, max_length=50)
    old_value23=models.CharField('标准值23', null=True, blank=True, max_length=20)
    old_item_id24=models.CharField('测试项目24', null=True, blank=True, max_length=10)
    old_item_name24=models.CharField('ItemName24', null=True, blank=True, max_length=50)
    old_value24=models.CharField('标准值24', null=True, blank=True, max_length=20)
    old_item_id25=models.CharField('测试项目25', null=True, blank=True, max_length=10)
    old_item_name25=models.CharField('ItemName25', null=True, blank=True, max_length=50)
    old_value25=models.CharField('标准值25', null=True, blank=True, max_length=20)
    old_item_id26=models.CharField('测试项目26', null=True, blank=True, max_length=10)
    old_item_name26=models.CharField('ItemName26', null=True, blank=True, max_length=50)
    old_value26=models.CharField('标准值26', null=True, blank=True, max_length=20)
    old_item_id27=models.CharField('测试项目27', null=True, blank=True, max_length=10)
    old_item_name27=models.CharField('ItemName27', null=True, blank=True, max_length=50)
    old_value27=models.CharField('标准值27', null=True, blank=True, max_length=20)
    old_item_id28=models.CharField('测试项目28', null=True, blank=True, max_length=10)
    old_item_name28=models.CharField('ItemName28', null=True, blank=True, max_length=50)
    old_value28=models.CharField('标准值28', null=True, blank=True, max_length=20)
    old_item_id29=models.CharField('测试项目29', null=True, blank=True, max_length=10)
    old_item_name29=models.CharField('测试项目名称29', null=True, blank=True, max_length=50)
    old_value29=models.CharField('标准值29', null=True, blank=True, max_length=20)
    old_item_id30=models.CharField('测试项目30', null=True, blank=True, max_length=10)
    old_item_name30=models.CharField('ItemName30', null=True, blank=True, max_length=50)
    old_value30=models.CharField('标准值30', null=True, blank=True, max_length=20)
    old_item_id31=models.CharField('测试项目31', null=True, blank=True, max_length=10)
    old_item_name31=models.CharField('ItemName31', null=True, blank=True, max_length=50)
    old_value31=models.CharField('标准值31', null=True, blank=True, max_length=20)
    old_item_id32=models.CharField('测试项目32', null=True, blank=True, max_length=10)
    old_item_name32=models.CharField('测试项目名称32', null=True, blank=True, max_length=50)
    old_value32=models.CharField('标准值32', null=True, blank=True, max_length=20)
    old_item_id33=models.CharField('测试项目33', null=True, blank=True, max_length=10)
    old_item_name33=models.CharField('测试项目名称33', null=True, blank=True, max_length=50)
    old_value33=models.CharField('标准值33', null=True, blank=True, max_length=20)
    old_item_id34=models.CharField('测试项目34', null=True, blank=True, max_length=10)
    old_item_name34=models.CharField('测试项目名称34', null=True, blank=True, max_length=50)
    old_value34=models.CharField('标准值34', null=True, blank=True, max_length=20)
    old_item_id35=models.CharField('测试项目35', null=True, blank=True, max_length=10)
    old_item_name35=models.CharField('测试项目名称35', null=True, blank=True, max_length=50)
    old_value35=models.CharField('标准值35', null=True, blank=True, max_length=20)
    old_item_id36=models.CharField('测试项目36', null=True, blank=True, max_length=10)
    old_item_name36=models.CharField('测试项目名称36', null=True, blank=True, max_length=50)
    old_value36=models.CharField('标准值36', null=True, blank=True, max_length=20)
    old_item_id37=models.CharField('测试项目37', null=True, blank=True, max_length=10)
    old_item_name37=models.CharField('测试项目名称37', null=True, blank=True, max_length=50)
    old_value37=models.CharField('标准值37', null=True, blank=True, max_length=20)
    old_item_id38=models.CharField('测试项目38', null=True, blank=True, max_length=10)
    old_item_name38=models.CharField('测试项目名称38', null=True, blank=True, max_length=50)
    old_value38=models.CharField('加色类别', null=True, blank=True, max_length=20)
    old_item_id39=models.CharField('测试项目39', null=True, blank=True, max_length=10)
    old_item_name39=models.CharField('测试项目名称39', null=True, blank=True, max_length=50)
    old_value39=models.CharField('机台', null=True, blank=True, max_length=20)
    old_item_id40=models.CharField('测试项目40', null=True, blank=True, max_length=10)
    old_item_name40=models.CharField('测试项目名称40', null=True, blank=True, max_length=50)
    old_value40=models.CharField('染程', null=True, blank=True, max_length=20)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_step_no=models.IntegerField('流程节点号', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_emp_id=models.CharField('责任人', null=True, blank=True, max_length=20)
    old_dept_id=models.CharField('DeptID', null=True, blank=True, max_length=50)
    old_check_no=models.CharField('检测单号', null=True, blank=True, max_length=30)
    old_stuff_id=models.CharField('样品名称', null=True, blank=True, max_length=10)
    old_compare_stuff_id=models.CharField('对比名称', null=True, blank=True, max_length=10)
    old_supplier_id=models.CharField('样品供方', null=True, blank=True, max_length=10)
    old_compare_supplier_id=models.CharField('对比供方', null=True, blank=True, max_length=10)
    old_compare_lot_no=models.CharField('对比批号', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_prodtest'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_fb2f3985ac77e407'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_fb2f3985ac77e407')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（ProdTest，待确认）'
        ordering=["-id"]

class SourceDyeQualityAccident(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='QualityAccident'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'JobSheetNo': 'old_job_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'CustSelfProduct': 'old_cust_self_product', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'CustColorNum': 'old_cust_color_num', 'Weight': 'old_weight', 'Width': 'old_width', 'SumAssignedWeightQty': 'old_sum_assigned_weight_qty', 'SumAssignedRolls': 'old_sum_assigned_rolls', 'QualityDescription': 'old_quality_description', 'Remarks': 'old_remarks', 'DepartMent': 'old_depart_ment', 'Suggestion': 'old_suggestion', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_cust_self_product': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_cust_color_num': 'Chinese_PRC_CI_AS', 'old_weight': 'Chinese_PRC_CI_AS', 'old_width': 'Chinese_PRC_CI_AS', 'old_quality_description': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_depart_ment': 'Chinese_PRC_CI_AS', 'old_suggestion': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('单据流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('单据号', null=True, blank=True, max_length=50)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('SheetKind', null=True, blank=True)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=200)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=500)
    old_cust_self_product=models.CharField('客户规格', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=200)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=200)
    old_cust_color_num=models.CharField('客户色号', null=True, blank=True, max_length=20)
    old_weight=models.CharField('克重', null=True, blank=True, max_length=200)
    old_width=models.CharField('幅宽', null=True, blank=True, max_length=200)
    old_sum_assigned_weight_qty=models.DecimalField('实发数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sum_assigned_rolls=models.DecimalField('实发粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_quality_description=models.CharField('质量描述', null=True, blank=True, max_length=512)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_depart_ment=models.CharField('责任部门', null=True, blank=True, max_length=10)
    old_suggestion=models.CharField('处理意见', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_qualityaccident'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_9d0957970b05e0a7'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_9d0957970b05e0a7')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（QualityAccident，待确认）'
        ordering=["-id"]

class SourceDyeQualityDeduction(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='QualityDeduction'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'JobSheetNo': 'old_job_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'CustSelfProduct': 'old_cust_self_product', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'CustColorNum': 'old_cust_color_num', 'Weight': 'old_weight', 'Width': 'old_width', 'SumAssignedWeightQty': 'old_sum_assigned_weight_qty', 'SumAssignedRolls': 'old_sum_assigned_rolls', 'QualityDescription': 'old_quality_description', 'Remarks': 'old_remarks', 'DepartMent': 'old_depart_ment', 'DeductionMoney': 'old_deduction_money', 'AccidentPerson': 'old_accident_person', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'LSheetSeries': 'old_lsheet_series'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_cust_self_product': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_cust_color_num': 'Chinese_PRC_CI_AS', 'old_weight': 'Chinese_PRC_CI_AS', 'old_width': 'Chinese_PRC_CI_AS', 'old_quality_description': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_depart_ment': 'Chinese_PRC_CI_AS', 'old_accident_person': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_lsheet_series': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('单据流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('单据号', null=True, blank=True, max_length=50)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('SheetKind', null=True, blank=True)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=200)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=500)
    old_cust_self_product=models.CharField('客户规格', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=200)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=200)
    old_cust_color_num=models.CharField('客户色号', null=True, blank=True, max_length=20)
    old_weight=models.CharField('克重', null=True, blank=True, max_length=200)
    old_width=models.CharField('幅宽', null=True, blank=True, max_length=200)
    old_sum_assigned_weight_qty=models.DecimalField('实发数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sum_assigned_rolls=models.DecimalField('实发粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_quality_description=models.CharField('质量描述', null=True, blank=True, max_length=512)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_depart_ment=models.CharField('责任部门', null=True, blank=True, max_length=10)
    old_deduction_money=models.DecimalField('扣罚金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_accident_person=models.CharField('责任人', null=True, blank=True, max_length=10)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_lsheet_series=models.CharField('LSheetSeries', null=True, blank=True, max_length=32)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_qualitydeduction'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_d3bb7fa9ef9ba991'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_d3bb7fa9ef9ba991')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（QualityDeduction，待确认）'
        ordering=["-id"]

class SourceDyeQualityRegister(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='QualityRegister'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetDate': 'old_sheet_date', 'JobSheetNo': 'old_job_sheet_no', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'ColorNum': 'old_color_num', 'ColorID': 'old_color_id', 'Rolls': 'old_rolls', 'WeightQty': 'old_weight_qty', 'Reason': 'old_reason', 'ShiftID': 'old_shift_id', 'ProcessMethod': 'old_process_method', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'RightStatus': 'old_right_status', 'AutoID': 'old_auto_id', 'EmpID': 'old_emp_id', 'Description1': 'old_description1', 'Description2': 'old_description2'}
    SOURCE_KEY=('SheetSeries', 'AutoID')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_reason': 'Chinese_PRC_CI_AS', 'old_shift_id': 'Chinese_PRC_CI_AS', 'old_process_method': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_auto_id': 'Chinese_PRC_CI_AS', 'old_emp_id': 'Chinese_PRC_CI_AS', 'old_description1': 'Chinese_PRC_CI_AS', 'old_description2': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('登记号', null=False, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('登记时间', null=True, blank=True)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=10)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=20)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=20)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=20)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_weight_qty=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_reason=models.CharField('原因', null=True, blank=True, max_length=512)
    old_shift_id=models.CharField('班组', null=True, blank=True, max_length=20)
    old_process_method=models.CharField('处理方法', null=True, blank=True, max_length=512)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=10)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_right_status=models.IntegerField('状态', null=True, blank=True)
    old_auto_id=models.CharField('流水号', null=False, blank=True, max_length=50)
    old_emp_id=models.CharField('员工', null=True, blank=True, max_length=10)
    old_description1=models.CharField('Description1', null=True, blank=True, max_length=500)
    old_description2=models.CharField('Description2', null=True, blank=True, max_length=500)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_qualityregister'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_auto_id'],name='src_289e0be27632493d'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_auto_id'))),name='src_ci_289e0be27632493d')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（QualityRegister，待确认）'
        ordering=["-id"]

class SourceDyeRecordDefect(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='RecordDefect'
    SOURCE_FIELDS={'BarCode': 'old_bar_code', 'DefectNo': 'old_defect_no', 'DefectID': 'old_defect_id', 'StartPos': 'old_start_pos', 'EndPos': 'old_end_pos', 'Speed': 'old_speed', 'IsContinuity': 'old_is_continuity', 'IsRepairable': 'old_is_repairable', 'Dots': 'old_dots', 'Times': 'old_times', 'Qty': 'old_qty', 'Status': 'old_status', 'Remarks': 'old_remarks', 'LotNo': 'old_lot_no', 'DefectGroupID': 'old_defect_group_id', 'CUTQTY': 'old_cutqty', 'DefectDot': 'old_defect_dot', 'SumDots': 'old_sum_dots', 'BarCodeRollNo': 'old_bar_code_roll_no', 'StatusDescription': 'old_status_description', 'DefectType': 'old_defect_type'}
    SOURCE_KEY=('BarCode', 'DefectNo')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_bar_code': 'Chinese_PRC_CI_AS', 'old_defect_id': 'Chinese_PRC_CI_AS', 'old_status': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_defect_group_id': 'Chinese_PRC_CI_AS', 'old_defect_dot': 'Chinese_PRC_CI_AS', 'old_bar_code_roll_no': 'Chinese_PRC_CI_AS', 'old_status_description': 'Chinese_PRC_CI_AS', 'old_defect_type': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：RecordYield', 'target': 'erp_warehouse.SourceDyeRecordYield', 'source_fields': ['BarCode'], 'target_fields': ['Guid'], 'evidence': ['原界面主从 QueryRecordDefect → QueryRecord']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_bar_code=models.CharField('条码', null=False, blank=True, max_length=20)
    old_defect_no=models.IntegerField('疵点顺序', null=False, blank=False)
    old_defect_id=models.CharField('疵点编码', null=True, blank=True, max_length=10)
    old_start_pos=models.DecimalField('开始位置', null=True, blank=True, max_digits=8, decimal_places=2)
    old_end_pos=models.DecimalField('结束位置', null=True, blank=True, max_digits=8, decimal_places=2)
    old_speed=models.DecimalField('速度', null=True, blank=True, max_digits=8, decimal_places=2)
    old_is_continuity=models.BooleanField('是否连续疵点', null=True, blank=True)
    old_is_repairable=models.BooleanField('是否可重修', null=True, blank=True)
    old_dots=models.IntegerField('疵点类型名称', null=True, blank=True)
    old_times=models.IntegerField('状态', null=True, blank=True)
    old_qty=models.DecimalField('数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_status=models.CharField('疵点状态', null=True, blank=True, max_length=1)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    old_lot_no=models.CharField('LotNo', null=True, blank=True, max_length=50)
    old_defect_group_id=models.CharField('疵点类别', null=True, blank=True, max_length=10)
    old_cutqty=models.DecimalField('CUTQTY', null=True, blank=True, max_digits=10, decimal_places=1)
    old_defect_dot=models.CharField('疵点分数', null=True, blank=True, max_length=30)
    old_sum_dots=models.DecimalField('疵点总扣分', null=True, blank=True, max_digits=8, decimal_places=2)
    old_bar_code_roll_no=models.CharField('细码条码', null=True, blank=True, max_length=20)
    old_status_description=models.CharField('状态说明', null=True, blank=True, max_length=50)
    old_defect_type=models.CharField('DefectType', null=True, blank=True, max_length=30)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeRecordYield', verbose_name='原关系：RecordYield', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_recorddefect'
        indexes=[models.Index(fields=['source_batch', 'old_bar_code', 'old_defect_no'],name='src_ac6f826135f3fb08'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_bar_code'))),models.F('old_defect_no'),name='src_ci_ac6f826135f3fb08')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（RecordDefect，待确认）'
        ordering=["-id"]

class SourceDyeTestDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='Test_Detail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：Test_Main', 'target': 'erp_quality.SourceDyeTestMain', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 Test_Detail → Test_Main']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=50)
    old_detail_no=models.CharField('行号', null=False, blank=True, max_length=50)
    old_color_id=models.CharField('颜色号', null=True, blank=True, max_length=50)
    old_color_num=models.CharField('颜色代码', null=True, blank=True, max_length=50)
    old_remarks=models.TextField('备注', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_quality.SourceDyeTestMain', verbose_name='原关系：Test_Main', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_test_detail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_e280bd93ca901769'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_e280bd93ca901769')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（Test_Detail，待确认）'
        ordering=["-id"]

class SourceDyeTestMain(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='Test_Main'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'CustomerID': 'old_customer_id', 'SalerID': 'old_saler_id', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_saler_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=50)
    old_customer_id=models.CharField('客户名', null=True, blank=True, max_length=50)
    old_saler_id=models.CharField('业务员', null=True, blank=True, max_length=50)
    old_remarks=models.TextField('备注', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_test_main'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_556eb3ea463b17d3'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_556eb3ea463b17d3')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（Test_Main，待确认）'
        ordering=["-id"]

class SourceDyeWDefect(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='WDefect'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetType': 'old_sheet_type', 'SheetDate': 'old_sheet_date', 'SheetNo': 'old_sheet_no', 'WDefectNo': 'old_wdefect_no', 'WProcessNo': 'old_wprocess_no', 'JobSheetNo': 'old_job_sheet_no', 'CustomerID': 'old_customer_id', 'DetailCustName': 'old_detail_cust_name', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'ProdID': 'old_prod_id', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'Kind': 'old_kind', 'MachineID': 'old_machine_id', 'DefectIDs': 'old_defect_ids', 'Defects': 'old_defects', 'DefectDate': 'old_defect_date', 'DefectDept': 'old_defect_dept', 'DefectRolls': 'old_defect_rolls', 'DefectQty': 'old_defect_qty', 'DefectLengthQty': 'old_defect_length_qty', 'DefectShiftID': 'old_defect_shift_id', 'DefectEmpID': 'old_defect_emp_id', 'DefectProcessID': 'old_defect_process_id', 'AwardMoney': 'old_award_money', 'ProcessNo': 'old_process_no', 'ProcessID': 'old_process_id', 'ShiftID': 'old_shift_id', 'EmpID': 'old_emp_id', 'Signer': 'old_signer', 'SignedDate': 'old_signed_date', 'Status': 'old_status', 'Remarks': 'old_remarks', 'StationID': 'old_station_id', 'DefectStationID': 'old_defect_station_id', 'CheckDesc': 'old_check_desc', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'Approved': 'old_approved', 'FromRolls': 'old_from_rolls', 'FromWeightQty': 'old_from_weight_qty', 'FromLengthQty': 'old_from_length_qty', 'Result': 'old_result', 'KindType': 'old_kind_type', 'DefectKind': 'old_defect_kind', 'DefectType': 'old_defect_type', 'DefectFactory': 'old_defect_factory', 'DefectClassID': 'old_defect_class_id', 'QCCD': 'old_qccd', 'PiSheWenTi': 'old_pi_she_wen_ti', 'Outputdeduction': 'old_outputdeduction'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_wdefect_no': 'Chinese_PRC_CI_AS', 'old_wprocess_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_detail_cust_name': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_kind': 'Chinese_PRC_CI_AS', 'old_machine_id': 'Chinese_PRC_CI_AS', 'old_defect_ids': 'Chinese_PRC_CI_AS', 'old_defects': 'Chinese_PRC_CI_AS', 'old_defect_dept': 'Chinese_PRC_CI_AS', 'old_defect_shift_id': 'Chinese_PRC_CI_AS', 'old_defect_emp_id': 'Chinese_PRC_CI_AS', 'old_defect_process_id': 'Chinese_PRC_CI_AS', 'old_process_id': 'Chinese_PRC_CI_AS', 'old_shift_id': 'Chinese_PRC_CI_AS', 'old_emp_id': 'Chinese_PRC_CI_AS', 'old_signer': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_station_id': 'Chinese_PRC_CI_AS', 'old_defect_station_id': 'Chinese_PRC_CI_AS', 'old_check_desc': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_result': 'Chinese_PRC_CI_AS', 'old_kind_type': 'Chinese_PRC_CI_AS', 'old_defect_kind': 'Chinese_PRC_CI_AS', 'old_defect_type': 'Chinese_PRC_CI_AS', 'old_defect_factory': 'Chinese_PRC_CI_AS', 'old_defect_class_id': 'Chinese_PRC_CI_AS', 'old_qccd': 'Chinese_PRC_CI_AS', 'old_pi_she_wen_ti': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_type=models.IntegerField('类型', null=True, blank=True)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_no=models.CharField('检验单号', null=True, blank=True, max_length=36)
    old_wdefect_no=models.CharField('质量流水号', null=True, blank=True, max_length=20)
    old_wprocess_no=models.CharField('刷卡流水号', null=True, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_customer_id=models.CharField('客户代码', null=True, blank=True, max_length=50)
    old_detail_cust_name=models.CharField('明细客户', null=True, blank=True, max_length=150)
    old_color_id=models.CharField('颜色编码', null=True, blank=True, max_length=250)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=100)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=200)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=200)
    old_kind=models.CharField('类别', null=True, blank=True, max_length=10)
    old_machine_id=models.CharField('机台号', null=True, blank=True, max_length=10)
    old_defect_ids=models.TextField('疵点代码', null=True, blank=True)
    old_defects=models.CharField('疵点', null=True, blank=True, max_length=100)
    old_defect_date=models.DateTimeField('出疵时间', null=True, blank=True)
    old_defect_dept=models.CharField('责任部门', null=True, blank=True, max_length=30)
    old_defect_rolls=models.DecimalField('疵品粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_defect_qty=models.DecimalField('疵品数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_defect_length_qty=models.DecimalField('疵品长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_defect_shift_id=models.CharField('出疵班组', null=True, blank=True, max_length=10)
    old_defect_emp_id=models.CharField('出疵员工', null=True, blank=True, max_length=20)
    old_defect_process_id=models.CharField('出疵工序', null=True, blank=True, max_length=50)
    old_award_money=models.DecimalField('奖金', null=True, blank=True, max_digits=10, decimal_places=2)
    old_process_no=models.IntegerField('工序号', null=True, blank=True)
    old_process_id=models.CharField('工序', null=True, blank=True, max_length=10)
    old_shift_id=models.CharField('班组', null=True, blank=True, max_length=10)
    old_emp_id=models.CharField('员工', null=True, blank=True, max_length=50)
    old_signer=models.CharField('签核人姓名', null=True, blank=True, max_length=10)
    old_signed_date=models.DateTimeField('签核日期', null=True, blank=True)
    old_status=models.IntegerField('评定状态', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_station_id=models.CharField('站别', null=True, blank=True, max_length=10)
    old_defect_station_id=models.CharField('出疵站别', null=True, blank=True, max_length=50)
    old_check_desc=models.CharField('初判', null=True, blank=True, max_length=80)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_approved=models.BooleanField('已审核', null=True, blank=True)
    old_from_rolls=models.DecimalField('检验粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_from_weight_qty=models.DecimalField('检验重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_from_length_qty=models.DecimalField('检验长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_result=models.CharField('评审结果', null=True, blank=True, max_length=2000)
    old_kind_type=models.CharField('责任类别', null=True, blank=True, max_length=10)
    old_defect_kind=models.CharField('质量问题', null=True, blank=True, max_length=50)
    old_defect_type=models.CharField('质量类型', null=True, blank=True, max_length=20)
    old_defect_factory=models.CharField('工厂分类', null=True, blank=True, max_length=50)
    old_defect_class_id=models.CharField('DefectClassID', null=True, blank=True, max_length=50)
    old_qccd=models.CharField('质检问题', null=True, blank=True, max_length=150)
    old_pi_she_wen_ti=models.CharField('批色问题', null=True, blank=True, max_length=50)
    old_outputdeduction=models.DecimalField('产量扣除%', null=True, blank=True, max_digits=10, decimal_places=2)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_wdefect'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_04d48aebdfffc7c8'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_04d48aebdfffc7c8'),models.Index(fields=['source_batch', 'old_wdefect_no'],name='src_f837fcea6ac789ca'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_wdefect_no'))),name='src_ci_f837fcea6ac789ca')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（WDefect，待确认）'
        ordering=["-id"]

class SourceDyeWDefectPenalty(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='WDefectPenalty'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'WDefectNo': 'old_wdefect_no', 'RowNo': 'old_row_no', 'DutyKind': 'old_duty_kind', 'EmpID': 'old_emp_id', 'Name': 'old_name', 'Rolls': 'old_rolls', 'Qty': 'old_qty', 'Penalty': 'old_penalty', 'Reward': 'old_reward', 'Remarks': 'old_remarks', 'SheetDate': 'old_sheet_date'}
    SOURCE_KEY=('SheetSeries', 'RowNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_wdefect_no': 'Chinese_PRC_CI_AS', 'old_duty_kind': 'Chinese_PRC_CI_AS', 'old_emp_id': 'Chinese_PRC_CI_AS', 'old_name': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：WDefect', 'target': 'erp_quality.SourceDyeWDefect', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 WDefectPenaltyOther → WDefectJudgeOther', '原界面主从 WDefectPenaltyInterior → WDefectJudgeInterior', '原界面主从 WDefectOtherDetail → WDefectOther', '原界面主从 WDefectPayoutsDetail → WDefectPayouts', '原界面主从 WDefectPenaltyBack → WDefectJudgeBack']}, {'field': 'source_parent_2', 'title': '原关系：WDefect', 'target': 'erp_quality.SourceDyeWDefect', 'source_fields': ['WDefectNo'], 'target_fields': ['WDefectNo'], 'evidence': ['原界面主从 WDefectPenalty → WDefect']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_wdefect_no=models.CharField('质量流水号', null=True, blank=True, max_length=20)
    old_row_no=models.IntegerField('行号', null=False, blank=False)
    old_duty_kind=models.CharField('责任类型', null=True, blank=True, max_length=1)
    old_emp_id=models.CharField('员工编号', null=True, blank=True, max_length=50)
    old_name=models.CharField('名称', null=True, blank=True, max_length=60)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_qty=models.DecimalField('扣数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_penalty=models.DecimalField('扣款', null=True, blank=True, max_digits=10, decimal_places=2)
    old_reward=models.DecimalField('奖励', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_quality.SourceDyeWDefect', verbose_name='原关系：WDefect', null=True, blank=True, on_delete=models.PROTECT, related_name='+')
    source_parent_2=models.ForeignKey('erp_quality.SourceDyeWDefect', verbose_name='原关系：WDefect', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_wdefectpenalty'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_row_no'],name='src_c2340b85754bec67'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),models.F('old_row_no'),name='src_ci_c2340b85754bec67')]
        verbose_name=verbose_name_plural='旧质量责任及扣奖明细'
        ordering=["-id"]

class SourceDyeZhijianwenti(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='zhijianwenti'
    SOURCE_FIELDS={'FieldType': 'old_field_type', 'Code': 'old_code', 'Name': 'old_name', 'Mnemonic': 'old_mnemonic', 'NumValue': 'old_num_value', 'SortValue': 'old_sort_value', 'DefectFactory': 'old_defect_factory', 'Reserved1': 'old_reserved1', 'Reserved2': 'old_reserved2', 'Reserved3': 'old_reserved3', 'Reserved4': 'old_reserved4', 'Reserved5': 'old_reserved5', 'StopDate': 'old_stop_date', 'ParentCode': 'old_parent_code', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'IsStop': 'old_is_stop', 'BusinessUnitID': 'old_business_unit_id', 'NumValueNo': 'old_num_value_no', 'CustomerID': 'old_customer_id', 'Kind_01': 'old_kind_01', 'Kind_02': 'old_kind_02'}
    SOURCE_KEY=('FieldType', 'Code')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_field_type': 'Chinese_PRC_CI_AS', 'old_code': 'Chinese_PRC_CI_AS', 'old_name': 'Chinese_PRC_CI_AS', 'old_mnemonic': 'Chinese_PRC_CI_AS', 'old_defect_factory': 'Chinese_PRC_CI_AS', 'old_reserved1': 'Chinese_PRC_CI_AS', 'old_reserved2': 'Chinese_PRC_CI_AS', 'old_reserved3': 'Chinese_PRC_CI_AS', 'old_reserved4': 'Chinese_PRC_CI_AS', 'old_reserved5': 'Chinese_PRC_CI_AS', 'old_parent_code': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_kind_01': 'Chinese_PRC_CI_AS', 'old_kind_02': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_field_type=models.CharField('数据类型', null=False, blank=True, max_length=20)
    old_code=models.CharField('编码', null=False, blank=True, max_length=20)
    old_name=models.CharField('名称', null=False, blank=True, max_length=100)
    old_mnemonic=models.CharField('助记符', null=True, blank=True, max_length=100)
    old_num_value=models.DecimalField('数值值', null=True, blank=True, max_digits=18, decimal_places=6)
    old_sort_value=models.IntegerField('排序值', null=True, blank=True)
    old_defect_factory=models.CharField('工厂分类', null=True, blank=True, max_length=100)
    old_reserved1=models.CharField('保留值1', null=True, blank=True, max_length=1000)
    old_reserved2=models.CharField('保留值2', null=True, blank=True, max_length=100)
    old_reserved3=models.CharField('保留值3', null=True, blank=True, max_length=100)
    old_reserved4=models.CharField('保留值4', null=True, blank=True, max_length=100)
    old_reserved5=models.CharField('保留值5', null=True, blank=True, max_length=100)
    old_stop_date=models.DateTimeField('停用时间', null=True, blank=True)
    old_parent_code=models.CharField('父级代码', null=True, blank=True, max_length=10)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_is_stop=models.BooleanField('是否停用', null=True, blank=True)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=20)
    old_num_value_no=models.IntegerField('NumValueNo', null=True, blank=True)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=20)
    old_kind_01=models.CharField('异常分类', null=True, blank=True, max_length=100)
    old_kind_02=models.CharField('Kind_02', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_zhijianwenti'
        indexes=[models.Index(fields=['source_batch', 'old_field_type', 'old_code'],name='src_130057b181586db9'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_field_type'))),Upper(RTrim(models.F('old_code'))),name='src_ci_130057b181586db9')]
        verbose_name=verbose_name_plural='其他或待确认相关表（zhijianwenti，待确认）'
        ordering=["-id"]
