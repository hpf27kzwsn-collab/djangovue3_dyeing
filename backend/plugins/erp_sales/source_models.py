"""静态旧业务字段；由tools/legacy_models生成，逐表来源见source_catalog.json。"""
from django.db import models
from django.db.models.functions import Upper,RTrim
from plugins.erp_base.source_documents import SourceRecord


class SourceDyeCusAddPrice(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='CusAddPrice'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'CustomerID': 'old_customer_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=30)
    old_sheet_no=models.CharField('表单号', null=True, blank=True, max_length=30)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approve_date=models.DateTimeField('审核日期', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_cusaddprice'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_67283cbedb918381'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_67283cbedb918381')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（CusAddPrice，待确认）'
        ordering=["-id"]

class SourceDyeCusAddPriceDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='CusAddPriceDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'ProdID': 'old_prod_id', 'Remarks1': 'old_remarks1', 'Remarks2': 'old_remarks2', 'ColorDepthID': 'old_color_depth_id', 'MinTwist': 'old_min_twist', 'MaxTwist': 'old_max_twist', 'Price': 'old_price', 'PriceUnit': 'old_price_unit'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_remarks1': 'Chinese_PRC_CI_AS', 'old_remarks2': 'Chinese_PRC_CI_AS', 'old_color_depth_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：CusAddPrice', 'target': 'erp_sales.SourceDyeCusAddPrice', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 CusAddPriceDetail → CusAddPrice']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单号', null=True, blank=True, max_length=30)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=30)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=30)
    old_remarks1=models.CharField('备注1', null=True, blank=True, max_length=512)
    old_remarks2=models.CharField('备注2', null=True, blank=True, max_length=512)
    old_color_depth_id=models.CharField('颜色深浅', null=True, blank=True, max_length=30)
    old_min_twist=models.DecimalField('捻度>', null=True, blank=True, max_digits=10, decimal_places=2)
    old_max_twist=models.DecimalField('捻度<=', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price_unit=models.IntegerField('报价单位', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_sales.SourceDyeCusAddPrice', verbose_name='原关系：CusAddPrice', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_cusaddpricedetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_f87340c2d373f178'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_f87340c2d373f178')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（CusAddPriceDetail，待确认）'
        ordering=["-id"]

class SourceDyeCusBasicsPrice(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='CusBasicsPrice'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'CustomerID': 'old_customer_id', 'CurrencyID': 'old_currency_id', 'IsTax': 'old_is_tax', 'Remarks': 'old_remarks', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'TaxRate': 'old_tax_rate', 'Approver': 'old_approver', 'ApproverDate': 'old_approver_date'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_currency_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单号', null=False, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据时间', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=30)
    old_currency_id=models.CharField('币别', null=True, blank=True, max_length=50)
    old_is_tax=models.BooleanField('是否含税', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_tax_rate=models.DecimalField('税率', null=True, blank=True, max_digits=10, decimal_places=2)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_approver_date=models.DateTimeField('审核时间', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_cusbasicsprice'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_0f102e4f8bed114e'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_0f102e4f8bed114e')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（CusBasicsPrice，待确认）'
        ordering=["-id"]

class SourceDyeCusBasicsPriceDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='CusBasicsPriceDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'GradeID': 'old_grade_id', 'FabricKindID': 'old_fabric_kind_id', 'ColorLevel': 'old_color_level', 'TaxPrice': 'old_tax_price', 'Price': 'old_price', 'StuffRatio1': 'old_stuff_ratio1', 'StuffRatio2': 'old_stuff_ratio2', 'FormulaCost1': 'old_formula_cost1', 'FormulaCost2': 'old_formula_cost2', 'Remarks': 'old_remarks', 'Weight1': 'old_weight1', 'Weight2': 'old_weight2', 'GrayID': 'old_gray_id', 'RSKind': 'old_rskind', 'KindName': 'old_kind_name'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_grade_id': 'Chinese_PRC_CI_AS', 'old_fabric_kind_id': 'Chinese_PRC_CI_AS', 'old_color_level': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_gray_id': 'Chinese_PRC_CI_AS', 'old_rskind': 'Chinese_PRC_CI_AS', 'old_kind_name': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：CusBasicsPrice', 'target': 'erp_sales.SourceDyeCusBasicsPrice', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 CusBasicsPriceDetail → CusBasicsPrice']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=50)
    old_grade_id=models.CharField('色号等级', null=True, blank=True, max_length=30)
    old_fabric_kind_id=models.CharField('纱种类别', null=True, blank=True, max_length=30)
    old_color_level=models.CharField('色级', null=True, blank=True, max_length=30)
    old_tax_price=models.DecimalField('含税单价', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('不含税单价', null=True, blank=True, max_digits=10, decimal_places=2)
    old_stuff_ratio1=models.DecimalField('染料溶度>', null=True, blank=True, max_digits=10, decimal_places=2)
    old_stuff_ratio2=models.DecimalField('染料溶度<=', null=True, blank=True, max_digits=10, decimal_places=2)
    old_formula_cost1=models.DecimalField('配方成本>', null=True, blank=True, max_digits=10, decimal_places=2)
    old_formula_cost2=models.DecimalField('配方成本<=', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_weight1=models.DecimalField('克重>', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight2=models.DecimalField('克重<=', null=True, blank=True, max_digits=10, decimal_places=2)
    old_gray_id=models.CharField('本厂规格', null=True, blank=True, max_length=20)
    old_rskind=models.CharField('染色分类', null=True, blank=True, max_length=50)
    old_kind_name=models.CharField('机台分类', null=True, blank=True, max_length=100)
    source_parent_1=models.ForeignKey('erp_sales.SourceDyeCusBasicsPrice', verbose_name='原关系：CusBasicsPrice', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_cusbasicspricedetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_3eca8c5530280357'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_3eca8c5530280357')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（CusBasicsPriceDetail，待确认）'
        ordering=["-id"]

class SourceDyeCusExtraCharge(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='CusExtraCharge'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'Price': 'old_price', 'PriceUnit': 'old_price_unit', 'Remarks': 'old_remarks', 'PayService': 'old_pay_service', 'TaxPrice': 'old_tax_price', 'GradeID': 'old_grade_id'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_price_unit': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_pay_service': 'Chinese_PRC_CI_AS', 'old_grade_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：CusBasicsPrice', 'target': 'erp_sales.SourceDyeCusBasicsPrice', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 CusExtraCharge → CusBasicsPrice']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=50)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price_unit=models.CharField('单价单位', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_pay_service=models.CharField('收费项目', null=True, blank=True, max_length=40)
    old_tax_price=models.FloatField('含税单价', null=True, blank=True)
    old_grade_id=models.CharField('色号等级', null=True, blank=True, max_length=10)
    source_parent_1=models.ForeignKey('erp_sales.SourceDyeCusBasicsPrice', verbose_name='原关系：CusBasicsPrice', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_cusextracharge'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_02df07c90dc2933a'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_02df07c90dc2933a')]
        verbose_name=verbose_name_plural='其他或待确认相关表（CusExtraCharge，待确认）'
        ordering=["-id"]

class SourceDyeCustomerNoLimit(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='CustomerNoLimit'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'CustomerID': 'old_customer_id', 'Kind': 'old_kind', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'RightStatus': 'old_right_status', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'NoLimitAmount': 'old_no_limit_amount'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=30)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=30)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=30)
    old_kind=models.IntegerField('Kind', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=200)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=30)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=30)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=30)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_no_limit_amount=models.DecimalField('NoLimitAmount', null=True, blank=True, max_digits=10, decimal_places=2)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_customernolimit'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_5fba8342882b4a1a'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_5fba8342882b4a1a')]
        verbose_name=verbose_name_plural='客户订单与销售相关表（CustomerNoLimit，待确认）'
        ordering=["-id"]

class SourceDyeCustomerTS(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='CustomerTS'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'RightStatus': 'old_right_status', 'SheetStatus': 'old_sheet_status'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=50)
    old_sheet_no=models.CharField('表单号', null=True, blank=True, max_length=50)
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
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_customerts'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_381b032699fba103'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_381b032699fba103')]
        verbose_name=verbose_name_plural='客户订单与销售相关表（CustomerTS，待确认）'
        ordering=["-id"]

class SourceDyeCustomerTSDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='CustomerTSDetail'
    SOURCE_FIELDS={'Sheetseries': 'old_sheetseries', 'DetailNo': 'old_detail_no', 'JobSheetNo': 'old_job_sheet_no', 'BarCode': 'old_bar_code', 'ProdID': 'old_prod_id', 'ColorNum': 'old_color_num', 'ColorID': 'old_color_id', 'Qty': 'old_qty', 'Result': 'old_result', 'Remarks': 'old_remarks', 'SheetDate': 'old_sheet_date'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheetseries': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_bar_code': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_result': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关联：CustomerTS', 'target': 'erp_sales.SourceDyeCustomerTS', 'source_fields': ['Sheetseries'], 'target_fields': ['SheetSeries'], 'evidence': ['2026-10-11有效入口CustomerTSDetail的MasterDataTableName及RelaFieldNames']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheetseries=models.CharField('表单号', null=False, blank=True, max_length=50)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=50)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=30)
    old_bar_code=models.CharField('条码', null=True, blank=True, max_length=30)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=30)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=30)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=30)
    old_qty=models.DecimalField('数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_result=models.CharField('处理意见', null=True, blank=True, max_length=526)
    old_remarks=models.CharField('投诉问题', null=True, blank=True, max_length=526)
    old_sheet_date=models.DateTimeField('日期', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_sales.SourceDyeCustomerTS', verbose_name='原关联：CustomerTS', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_customertsdetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_667f7e662ed5baf1'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_667f7e662ed5baf1')]
        verbose_name=verbose_name_plural='客户订单与销售相关表（CustomerTSDetail，待确认）'
        ordering=["-id"]

class SourceDyeFixedPrice(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='FixedPrice'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'BusinessUnitID': 'old_business_unit_id', 'SheetKind': 'old_sheet_kind', 'SheetDate': 'old_sheet_date', 'QuoteKindID': 'old_quote_kind_id', 'SalerGroupID': 'old_saler_group_id', 'SalerID': 'old_saler_id', 'CustomerID': 'old_customer_id', 'Linker': 'old_linker', 'CurrencyID': 'old_currency_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Remarks': 'old_remarks', 'Revisions': 'old_revisions', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'SettleID': 'old_settle_id', 'ExchangeRate': 'old_exchange_rate', 'StepNo': 'old_step_no', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'IsConfirmed': 'old_is_confirmed', 'BeiZhu': 'old_bei_zhu', 'IsTax': 'old_is_tax', 'TaxRate': 'old_tax_rate', 'Tel': 'old_tel', 'CustomerCode': 'old_customer_code', 'LastTime': 'old_last_time'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_quote_kind_id': 'Chinese_PRC_CI_AS', 'old_saler_group_id': 'Chinese_PRC_CI_AS', 'old_saler_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_linker': 'Chinese_PRC_CI_AS', 'old_currency_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_settle_id': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_bei_zhu': 'Chinese_PRC_CI_AS', 'old_is_tax': 'Chinese_PRC_CI_AS', 'old_tel': 'Chinese_PRC_CI_AS', 'old_customer_code': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=False, blank=True, max_length=20)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_sheet_kind=models.IntegerField('单据类别', null=True, blank=True)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_quote_kind_id=models.CharField('报价类别', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('业务组别', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('业务员代码', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=10)
    old_linker=models.CharField('联系人', null=True, blank=True, max_length=10)
    old_currency_id=models.CharField('币别', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_remarks=models.TextField('备注', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_settle_id=models.CharField('结算方式', null=True, blank=True, max_length=10)
    old_exchange_rate=models.DecimalField('汇率', null=True, blank=True, max_digits=10, decimal_places=2)
    old_step_no=models.IntegerField('工作流节点号', null=True, blank=True)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_is_confirmed=models.IntegerField('确价', null=True, blank=True)
    old_bei_zhu=models.CharField('BeiZhu', null=True, blank=True, max_length=150)
    old_is_tax=models.CharField('单价类别', null=True, blank=True, max_length=10)
    old_tax_rate=models.DecimalField('税率%', null=True, blank=True, max_digits=10, decimal_places=2)
    old_tel=models.CharField('Tel', null=True, blank=True, max_length=100)
    old_customer_code=models.CharField('客户全称', null=True, blank=True, max_length=50)
    old_last_time=models.DateTimeField('LastTime', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_fixedprice'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_eba099c20e022ca4'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_eba099c20e022ca4')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（FixedPrice，待确认）'
        ordering=["-id"]

class SourceDyeFixedPriceAtte(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='FixedPriceAtte'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'FieldType': 'old_field_type', 'AtteCode': 'old_atte_code', 'AtteValue': 'old_atte_value', 'PriceUnit': 'old_price_unit', 'Price': 'old_price', 'Description': 'old_description', 'DetailNo': 'old_detail_no'}
    SOURCE_KEY=('SheetSeries', 'FieldType', 'AtteCode', 'DetailNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_field_type': 'Chinese_PRC_CI_AS', 'old_atte_code': 'Chinese_PRC_CI_AS', 'old_atte_value': 'Chinese_PRC_CI_AS', 'old_description': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：FixedPriceDetail', 'target': 'erp_sales.SourceDyeFixedPriceDetail', 'source_fields': ['DetailNo'], 'target_fields': ['DetailNo'], 'evidence': ['原界面主从 c → QuoteDetail', '原界面主从 QuoteAtte → QuoteDetail']}, {'field': 'source_parent_2', 'title': '原关系：QuoteItemPrice', 'target': 'erp_sales.SourceDyeQuoteItemPrice', 'source_fields': ['DetailNo'], 'target_fields': ['DetailNo'], 'evidence': ['原界面主从 QuotePriceAtte → QuoteItemPrice']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_field_type=models.CharField('基础数据类别', null=False, blank=True, max_length=20)
    old_atte_code=models.CharField('事项代码', null=False, blank=True, max_length=10)
    old_atte_value=models.CharField('事项内容', null=True, blank=True, max_length=500)
    old_price_unit=models.IntegerField('计价单位', null=True, blank=True)
    old_price=models.DecimalField('价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_description=models.CharField('描述', null=True, blank=True, max_length=500)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=30)
    source_parent_1=models.ForeignKey('erp_sales.SourceDyeFixedPriceDetail', verbose_name='原关系：FixedPriceDetail', null=True, blank=True, on_delete=models.PROTECT, related_name='+')
    source_parent_2=models.ForeignKey('erp_sales.SourceDyeQuoteItemPrice', verbose_name='原关系：QuoteItemPrice', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_fixedpriceatte'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_field_type', 'old_atte_code', 'old_detail_no'],name='src_c145e94acb85f523'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_field_type'))),Upper(RTrim(models.F('old_atte_code'))),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_c145e94acb85f523')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（FixedPriceAtte，待确认）'
        ordering=["-id"]

class SourceDyeFixedPriceDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='FixedPriceDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'Spec': 'old_spec', 'Structure': 'old_structure', 'Width': 'old_width', 'Weight': 'old_weight', 'Price': 'old_price', 'PriceUnit': 'old_price_unit', 'Remarks': 'old_remarks', 'Loss': 'old_loss', 'ProdID': 'old_prod_id', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'MainStuffKindID': 'old_main_stuff_kind_id', 'ColorDepthID': 'old_color_depth_id', 'RecipePrice': 'old_recipe_price', 'ProcessMemo': 'old_process_memo', 'ProcessPrice': 'old_process_price', 'CustColorNum': 'old_cust_color_num', 'Pricesum': 'old_pricesum', 'CusPrice': 'old_cus_price', 'JobSheetNo': 'old_job_sheet_no', 'AdjustPrice': 'old_adjust_price', 'StartDate': 'old_start_date', 'DateType': 'old_date_type', 'IsConfirmed': 'old_is_confirmed', 'CustSelfProduct': 'old_cust_self_product', 'ColorNumNO': 'old_color_num_no', 'StuffDosage': 'old_stuff_dosage', 'DyePhaseName': 'old_dye_phase_name', 'GaoLaodu': 'old_gao_laodu', 'Note': 'old_note', 'Customer': 'old_customer', 'Photo': 'old_photo', 'StanPrice': 'old_stan_price', 'ConPrice': 'old_con_price', 'GradeID': 'old_grade_id', 'RightStatus': 'old_right_status', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'FabricKind': 'old_fabric_kind', 'YarnCategory': 'old_yarn_category', 'SumPrice': 'old_sum_price', 'SumChengBen': 'old_sum_cheng_ben', 'ChengBen0': 'old_cheng_ben0', 'ChengBen1': 'old_cheng_ben1', 'ChengBen2': 'old_cheng_ben2', 'ChengBen3': 'old_cheng_ben3', 'ChengBen4': 'old_cheng_ben4', 'ChengBen5': 'old_cheng_ben5', 'FenTouPrice': 'old_fen_tou_price', 'MinAmount': 'old_min_amount'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_structure': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_main_stuff_kind_id': 'Chinese_PRC_CI_AS', 'old_color_depth_id': 'Chinese_PRC_CI_AS', 'old_process_memo': 'Chinese_PRC_CI_AS', 'old_cust_color_num': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_cust_self_product': 'Chinese_PRC_CI_AS', 'old_color_num_no': 'Chinese_PRC_CI_AS', 'old_dye_phase_name': 'Chinese_PRC_CI_AS', 'old_gao_laodu': 'Chinese_PRC_CI_AS', 'old_note': 'Chinese_PRC_CI_AS', 'old_customer': 'Chinese_PRC_CI_AS', 'old_grade_id': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_fabric_kind': 'Chinese_PRC_CI_AS', 'old_yarn_category': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：FixedPrice', 'target': 'erp_sales.SourceDyeFixedPrice', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 QuoteDetail → Quote']}]
    SOURCE_DEFAULTS={'old_sheet_series': ('literal', ''), 'old_spec': ('literal', ''), 'old_structure': ('literal', ''), 'old_width': ('literal', 0), 'old_weight': ('literal', 0), 'old_price': ('literal', 0), 'old_price_unit': ('literal', 0), 'old_remarks': ('literal', ''), 'old_loss': ('literal', 0)}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('表单明细号（子表）', null=False, blank=True, max_length=36)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=128)
    old_structure=models.CharField('组织', null=True, blank=True, max_length=50)
    old_width=models.DecimalField('幅宽', null=False, blank=False, max_digits=6, decimal_places=2)
    old_weight=models.DecimalField('克重', null=False, blank=False, max_digits=6, decimal_places=2)
    old_price=models.DecimalField('客确价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_price_unit=models.IntegerField('单位', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_loss=models.DecimalField('数值缩率', null=True, blank=True, max_digits=4, decimal_places=1)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=20)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=50)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=20)
    old_main_stuff_kind_id=models.CharField('主染料类别', null=True, blank=True, max_length=10)
    old_color_depth_id=models.CharField('颜色深浅', null=True, blank=True, max_length=10)
    old_recipe_price=models.DecimalField('配方成本', null=True, blank=True, max_digits=8, decimal_places=2)
    old_process_memo=models.CharField('套价项目', null=True, blank=True, max_length=300)
    old_process_price=models.DecimalField('另计价', null=True, blank=True, max_digits=8, decimal_places=2)
    old_cust_color_num=models.CharField('客户色号', null=True, blank=True, max_length=100)
    old_pricesum=models.DecimalField('总单价', null=True, blank=True, max_digits=8, decimal_places=2)
    old_cus_price=models.DecimalField('对客报价', null=True, blank=True, max_digits=8, decimal_places=2)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=20)
    old_adjust_price=models.DecimalField('AdjustPrice', null=True, blank=True, max_digits=12, decimal_places=2)
    old_start_date=models.DateTimeField('StartDate', null=True, blank=True)
    old_date_type=models.IntegerField('DateType', null=True, blank=True)
    old_is_confirmed=models.IntegerField('是否确价', null=True, blank=True)
    old_cust_self_product=models.CharField('客户规格', null=True, blank=True, max_length=32)
    old_color_num_no=models.CharField('确版号', null=True, blank=True, max_length=10)
    old_stuff_dosage=models.FloatField('染料用量', null=True, blank=True)
    old_dye_phase_name=models.CharField('染色工艺', null=True, blank=True, max_length=100)
    old_gao_laodu=models.CharField('高牢度', null=True, blank=True, max_length=100)
    old_note=models.CharField('配方', null=True, blank=True, max_length=1000)
    old_customer=models.CharField('客户', null=True, blank=True, max_length=50)
    old_photo=models.BinaryField('Photo', null=True, blank=True, editable=True)
    old_stan_price=models.DecimalField('标准单价', null=True, blank=True, max_digits=9, decimal_places=2)
    old_con_price=models.DecimalField('参考单价', null=True, blank=True, max_digits=9, decimal_places=2)
    old_grade_id=models.CharField('色号等级', null=True, blank=True, max_length=20)
    old_right_status=models.IntegerField('审核', null=True, blank=True)
    old_approve_date=models.DateTimeField('审核日期', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=50)
    old_fabric_kind=models.CharField('纱种类别', null=True, blank=True, max_length=50)
    old_yarn_category=models.CharField('服务方式', null=True, blank=True, max_length=50)
    old_sum_price=models.DecimalField('SumPrice', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sum_cheng_ben=models.DecimalField('总成本', null=True, blank=True, max_digits=6, decimal_places=2)
    old_cheng_ben0=models.DecimalField('染色成本', null=True, blank=True, max_digits=6, decimal_places=2)
    old_cheng_ben1=models.DecimalField('前纺成本', null=True, blank=True, max_digits=6, decimal_places=2)
    old_cheng_ben2=models.DecimalField('后纺成本', null=True, blank=True, max_digits=6, decimal_places=2)
    old_cheng_ben3=models.DecimalField('加捻成本', null=True, blank=True, max_digits=6, decimal_places=2)
    old_cheng_ben4=models.DecimalField('包装成本', null=True, blank=True, max_digits=6, decimal_places=2)
    old_cheng_ben5=models.DecimalField('合股夹纱成本', null=True, blank=True, max_digits=6, decimal_places=2)
    old_fen_tou_price=models.DecimalField('分头报价', null=True, blank=True, max_digits=6, decimal_places=2)
    old_min_amount=models.DecimalField('最低消费', null=True, blank=True, max_digits=8, decimal_places=2)
    source_parent_1=models.ForeignKey('erp_sales.SourceDyeFixedPrice', verbose_name='原关系：FixedPrice', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_fixedpricedetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_54fb7676bb42aa6e'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_54fb7676bb42aa6e')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（FixedPriceDetail，待确认）'
        ordering=["-id"]

class SourceDyeFixedPriceProcess(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='FixedPriceProcess'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'ProcessID': 'old_process_id', 'Price': 'old_price', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('SheetSeries', 'DetailNo', 'ProcessID')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_process_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：FixedPrice', 'target': 'erp_sales.SourceDyeFixedPrice', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 QuotePriceProcess → Quote']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号(子表)', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('表单明细号', null=False, blank=True, max_length=36)
    old_process_id=models.CharField('工序', null=False, blank=True, max_length=50)
    old_price=models.DecimalField('价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=300)
    source_parent_1=models.ForeignKey('erp_sales.SourceDyeFixedPrice', verbose_name='原关系：FixedPrice', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_fixedpriceprocess'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no', 'old_process_id'],name='src_96645dc5308078b9'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),Upper(RTrim(models.F('old_process_id'))),name='src_ci_96645dc5308078b9')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（FixedPriceProcess，待确认）'
        ordering=["-id"]

class SourceDyeOrderAssign(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='OrderAssign'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'CheckNo': 'old_check_no', 'ReceSheetNo': 'old_rece_sheet_no', 'GrayID': 'old_gray_id', 'LotNo': 'old_lot_no', 'Spec': 'old_spec', 'Rolls': 'old_rolls', 'Packs': 'old_packs', 'GWeight': 'old_gweight', 'GWidth': 'old_gwidth', 'StorageUnitID': 'old_storage_unit_id', 'RollAvgQty': 'old_roll_avg_qty', 'Remarks': 'old_remarks', 'AssignNo': 'old_assign_no', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'MachineID': 'old_machine_id', 'DetailsCustomer': 'old_details_customer', 'PreField1': 'old_pre_field1', 'PreField2': 'old_pre_field2', 'PreField3': 'old_pre_field3', 'PreField4': 'old_pre_field4', 'PreField5': 'old_pre_field5', 'AssignFabKind': 'old_assign_fab_kind'}
    SOURCE_KEY=('SheetSeries', 'CheckNo', 'AssignNo')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_gray_id': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_storage_unit_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_machine_id': 'Chinese_PRC_CI_AS', 'old_details_customer': 'Chinese_PRC_CI_AS', 'old_pre_field1': 'Chinese_PRC_CI_AS', 'old_pre_field2': 'Chinese_PRC_CI_AS', 'old_pre_field3': 'Chinese_PRC_CI_AS', 'old_pre_field4': 'Chinese_PRC_CI_AS', 'old_pre_field5': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：OrderColor', 'target': 'erp_sales.SourceDyeOrderColor', 'source_fields': ['SheetSeries', 'CheckNo'], 'target_fields': ['SheetSeries', 'CheckNo'], 'evidence': ['原界面主从 OrderAssign → OrderColor', '原界面主从 PrintOrderAssign → PrintOrderColor', '原界面主从 OrderAssignSup → OrderColorSup', '原界面主从 OrderAssignChange → OrderColorChange']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_check_no=models.CharField('订单明细号', null=False, blank=True, max_length=20)
    old_rece_sheet_no=models.CharField('入库明细号', null=True, blank=True, max_length=20)
    old_gray_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=50)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=128)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_packs=models.DecimalField('件数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_gweight=models.DecimalField('胚纱克重', null=True, blank=True, max_digits=6, decimal_places=2)
    old_gwidth=models.DecimalField('坏纱门幅', null=True, blank=True, max_digits=6, decimal_places=2)
    old_storage_unit_id=models.CharField('仓位代码', null=True, blank=True, max_length=10)
    old_roll_avg_qty=models.DecimalField('平均粒长\\粒重', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_assign_no=models.IntegerField('预配单号', null=False, blank=False)
    old_length_qty=models.DecimalField('长度数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('重量数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_machine_id=models.CharField('机号', null=True, blank=True, max_length=10)
    old_details_customer=models.CharField('织厂', null=True, blank=True, max_length=10)
    old_pre_field1=models.CharField('捻度(H/S)', null=True, blank=True, max_length=50)
    old_pre_field2=models.CharField('氨纶', null=True, blank=True, max_length=50)
    old_pre_field3=models.CharField('针数', null=True, blank=True, max_length=50)
    old_pre_field4=models.CharField('寸数', null=True, blank=True, max_length=50)
    old_pre_field5=models.CharField('车架', null=True, blank=True, max_length=50)
    old_assign_fab_kind=models.IntegerField('AssignFabKind', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_sales.SourceDyeOrderColor', verbose_name='原关系：OrderColor', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_orderassign'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_check_no', 'old_assign_no'],name='src_943190f7da61057b'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_check_no'))),models.F('old_assign_no'),name='src_ci_943190f7da61057b')]
        verbose_name=verbose_name_plural='客户订单与销售相关表（OrderAssign，待确认）'
        ordering=["-id"]

class SourceDyeOrderAssign2(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='OrderAssign2'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'AssignNo': 'old_assign_no', 'ReceSheetNo': 'old_rece_sheet_no', 'GrayID': 'old_gray_id', 'LotNo': 'old_lot_no', 'Spec': 'old_spec', 'Packs': 'old_packs', 'Rolls': 'old_rolls', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'GWeight': 'old_gweight', 'GWidth': 'old_gwidth', 'StorageUnitID': 'old_storage_unit_id', 'RollAvgQty': 'old_roll_avg_qty', 'Remarks': 'old_remarks', 'AssignFabKind': 'old_assign_fab_kind', 'LastPacks': 'old_last_packs', 'LastRolls': 'old_last_rolls', 'LastLengthQty': 'old_last_length_qty', 'LastWeightQty': 'old_last_weight_qty'}
    SOURCE_KEY=('SheetSeries', 'AssignNo')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_gray_id': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_storage_unit_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：OrderMain', 'target': 'erp_sales.SourceDyeOrderMain', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 PrintOrderAssign2 → PrintOrderMain', '原界面主从 OrderAssign2 → OrderMain', '原界面主从 OrderAssign2Sup → OrderMainSup']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_assign_no=models.IntegerField('预配单号', null=False, blank=False)
    old_rece_sheet_no=models.CharField('入库明细号', null=True, blank=True, max_length=20)
    old_gray_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=200)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=200)
    old_packs=models.DecimalField('件数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_length_qty=models.DecimalField('长度数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('重量数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_gweight=models.DecimalField('胚纱克重', null=True, blank=True, max_digits=6, decimal_places=2)
    old_gwidth=models.DecimalField('坏纱门幅', null=True, blank=True, max_digits=6, decimal_places=2)
    old_storage_unit_id=models.CharField('仓位代码', null=True, blank=True, max_length=10)
    old_roll_avg_qty=models.DecimalField('平均粒长\\粒重', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_assign_fab_kind=models.IntegerField('纱来源类型', null=True, blank=True)
    old_last_packs=models.DecimalField('剩余包数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_last_rolls=models.DecimalField('剩余粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_last_length_qty=models.DecimalField('剩余长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_last_weight_qty=models.DecimalField('剩余重量', null=True, blank=True, max_digits=10, decimal_places=2)
    source_parent_1=models.ForeignKey('erp_sales.SourceDyeOrderMain', verbose_name='原关系：OrderMain', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_orderassign2'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_assign_no'],name='src_effccb327c2324ef'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),models.F('old_assign_no'),name='src_ci_effccb327c2324ef')]
        verbose_name=verbose_name_plural='客户订单与销售相关表（OrderAssign2，待确认）'
        ordering=["-id"]

class SourceDyeOrderAtte(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='OrderAtte'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'FieldType': 'old_field_type', 'AtteCode': 'old_atte_code', 'AtteValue': 'old_atte_value', 'Description': 'old_description', 'Price': 'old_price', 'PriceUnit': 'old_price_unit', 'CheckNo': 'old_check_no'}
    SOURCE_KEY=('SheetSeries', 'FieldType', 'AtteCode', 'CheckNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_field_type': 'Chinese_PRC_CI_AS', 'old_atte_code': 'Chinese_PRC_CI_AS', 'old_atte_value': 'Chinese_PRC_CI_AS', 'old_description': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：OrderColor', 'target': 'erp_sales.SourceDyeOrderColor', 'source_fields': ['SheetSeries', 'CheckNo'], 'target_fields': ['SheetSeries', 'CheckNo'], 'evidence': ['原界面主从 OrderAtte → OrderColor', '原界面主从 qry_GetOrderAtteToJob → qry_GetOrderInfoToJob']}, {'field': 'source_parent_2', 'title': '原关系：OrderMain', 'target': 'erp_sales.SourceDyeOrderMain', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 OrderAtteChange → OrderMainChange', '原界面主从 OrderAtteSup → OrderMainSup', '原界面主从 PrintOrderAtte → PrintOrderMain']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_field_type=models.CharField('基础数据类别', null=False, blank=True, max_length=20)
    old_atte_code=models.CharField('事项代码', null=False, blank=True, max_length=10)
    old_atte_value=models.CharField('事项内容', null=True, blank=True, max_length=500)
    old_description=models.CharField('描述', null=True, blank=True, max_length=500)
    old_price=models.DecimalField('价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_price_unit=models.IntegerField('计价单位', null=True, blank=True)
    old_check_no=models.CharField('订单号', null=False, blank=True, max_length=30)
    source_parent_1=models.ForeignKey('erp_sales.SourceDyeOrderColor', verbose_name='原关系：OrderColor', null=True, blank=True, on_delete=models.PROTECT, related_name='+')
    source_parent_2=models.ForeignKey('erp_sales.SourceDyeOrderMain', verbose_name='原关系：OrderMain', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_orderatte'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_field_type', 'old_atte_code', 'old_check_no'],name='src_612697093e456e29'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_field_type'))),Upper(RTrim(models.F('old_atte_code'))),Upper(RTrim(models.F('old_check_no'))),name='src_ci_612697093e456e29')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（OrderAtte，待确认）'
        ordering=["-id"]

class SourceDyeOrderColor(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='OrderColor'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'CheckNo': 'old_check_no', 'ProdID': 'old_prod_id', 'LotNo': 'old_lot_no', 'Spec': 'old_spec', 'RelaLotNo': 'old_rela_lot_no', 'ColorID': 'old_color_id', 'ColorE': 'old_color_e', 'ColorNum': 'old_color_num', 'DesignNo': 'old_design_no', 'WidthDn': 'old_width_dn', 'WidthUp': 'old_width_up', 'WidthKindID': 'old_width_kind_id', 'WeightDn': 'old_weight_dn', 'WeightUp': 'old_weight_up', 'OrderQty': 'old_order_qty', 'OrderRolls': 'old_order_rolls', 'GrayQty': 'old_gray_qty', 'Price': 'old_price', 'Fee': 'old_fee', 'Amount': 'old_amount', 'DlvDate': 'old_dlv_date', 'SumDlvRolls': 'old_sum_dlv_rolls', 'SumDlvQty': 'old_sum_dlv_qty', 'ToPlace': 'old_to_place', 'Remarks': 'old_remarks', 'CustSelfProduct': 'old_cust_self_product', 'ColorDepthID': 'old_color_depth_id', 'CustColorNum': 'old_cust_color_num', 'ProductionID': 'old_production_id', 'CardQty': 'old_card_qty', 'StandCraftNo': 'old_stand_craft_no', 'CraftCheck': 'old_craft_check', 'TechCheck': 'old_tech_check', 'PlanCheck': 'old_plan_check', 'CustFabricName': 'old_cust_fabric_name', 'DetailCustName': 'old_detail_cust_name', 'ContractNo': 'old_contract_no', 'CustSelfNo': 'old_cust_self_no', 'CustSelfNoDetail': 'old_cust_self_no_detail', 'MainStuffKindID': 'old_main_stuff_kind_id', 'FinalDlvDate': 'old_final_dlv_date', 'IsToDoSample': 'old_is_to_do_sample', 'IsSampleCharge': 'old_is_sample_charge', 'CraftCheckIdea': 'old_craft_check_idea', 'CraftCheckTime': 'old_craft_check_time', 'PlanCheckIdea': 'old_plan_check_idea', 'PlanCheckTime': 'old_plan_check_time', 'TechCheckIdea': 'old_tech_check_idea', 'TechCheckTime': 'old_tech_check_time', 'ColorRGB': 'old_color_rgb', 'SumProdRolls': 'old_sum_prod_rolls', 'SumProdQty': 'old_sum_prod_qty', 'IsContinue': 'old_is_continue', 'IsToConfirmed': 'old_is_to_confirmed', 'IsSpecColor': 'old_is_spec_color', 'IsSpecVat': 'old_is_spec_vat', 'ColorCards': 'old_color_cards', 'Atte': 'old_atte', 'ProgramKindID': 'old_program_kind_id', 'IsHaveFirstVat': 'old_is_have_first_vat', 'ConfirmSideID': 'old_confirm_side_id', 'ProcessPrice': 'old_process_price', 'PriceCheck': 'old_price_check', 'PriceCheckIdea': 'old_price_check_idea', 'PriceCheckTime': 'old_price_check_time', 'CraftChecker': 'old_craft_checker', 'TechChecker': 'old_tech_checker', 'PriceChecker': 'old_price_checker', 'PlanChecker': 'old_plan_checker', 'PrepareVats': 'old_prepare_vats', 'WeightUnit': 'old_weight_unit', 'Model1': 'old_model1', 'ColorKind': 'old_color_kind', 'Code': 'old_code', 'StorageUnitIDs': 'old_storage_unit_ids', 'RollAvgQtyStr': 'old_roll_avg_qty_str', 'Unit': 'old_unit', 'IsFinished': 'old_is_finished', 'PreProductionID': 'old_pre_production_id', 'FabricKindID': 'old_fabric_kind_id', 'LOT': 'old_lot', 'ColorMatch': 'old_color_match', 'NeedleCountUp': 'old_needle_count_up', 'NeedleCountDn': 'old_needle_count_dn', 'Twist': 'old_twist', 'Tenters': 'old_tenters', 'Plaiting': 'old_plaiting', 'Edge': 'old_edge', 'CodeFront': 'old_code_front', 'ProviderCode': 'old_provider_code', 'DlvAddress': 'old_dlv_address', 'PlanDate': 'old_plan_date', 'RequireWeight': 'old_require_weight', 'RequireKG': 'old_require_kg', 'MachinePin': 'old_machine_pin', 'MachineDozen': 'old_machine_dozen', 'FabricID': 'old_fabric_id', 'OutQty': 'old_out_qty', 'OutYard': 'old_out_yard', 'DryFub': 'old_dry_fub', 'WetFub': 'old_wet_fub', 'WashFastness': 'old_wash_fastness', 'SolarFastness': 'old_solar_fastness', 'ShrinV': 'old_shrin_v', 'ShrinL': 'old_shrin_l', 'CutYard': 'old_cut_yard', 'Remarks01': 'old_remarks01', 'Remarks02': 'old_remarks02', 'Remarks03': 'old_remarks03', 'Remarks04': 'old_remarks04', 'PrintCode': 'old_print_code', 'ColorPlateID': 'old_color_plate_id', 'FilmNo': 'old_film_no', 'Width': 'old_width', 'Weight': 'old_weight', 'AddWeigth': 'old_add_weigth', 'TubeWeight': 'old_tube_weight', 'CustGrayID': 'old_cust_gray_id', 'Rate': 'old_rate', 'ColorRemarks': 'old_color_remarks', 'WidthUnit': 'old_width_unit', 'WeightKindID': 'old_weight_kind_id', 'IsSupplement': 'old_is_supplement', 'bhd': 'old_bhd', 'GradeID': 'old_grade_id', 'GWName': 'old_gwname', 'DyeDate': 'old_dye_date', 'Postpone_Advance': 'old_postpone_advance', 'BatchColorCase': 'old_batch_color_case', 'IsPurAplNo': 'old_is_pur_apl_no', 'CustJobNo': 'old_cust_job_no', 'RightStatus': 'old_right_status', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'SheetStatus': 'old_sheet_status'}
    SOURCE_KEY=('CheckNo',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_rela_lot_no': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_e': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_design_no': 'Chinese_PRC_CI_AS', 'old_width_dn': 'Chinese_PRC_CI_AS', 'old_width_kind_id': 'Chinese_PRC_CI_AS', 'old_weight_dn': 'Chinese_PRC_CI_AS', 'old_to_place': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_cust_self_product': 'Chinese_PRC_CI_AS', 'old_color_depth_id': 'Chinese_PRC_CI_AS', 'old_cust_color_num': 'Chinese_PRC_CI_AS', 'old_production_id': 'Chinese_PRC_CI_AS', 'old_stand_craft_no': 'Chinese_PRC_CI_AS', 'old_cust_fabric_name': 'Chinese_PRC_CI_AS', 'old_detail_cust_name': 'Chinese_PRC_CI_AS', 'old_contract_no': 'Chinese_PRC_CI_AS', 'old_cust_self_no': 'Chinese_PRC_CI_AS', 'old_cust_self_no_detail': 'Chinese_PRC_CI_AS', 'old_main_stuff_kind_id': 'Chinese_PRC_CI_AS', 'old_is_to_do_sample': 'Chinese_PRC_CI_AS', 'old_craft_check_idea': 'Chinese_PRC_CI_AS', 'old_plan_check_idea': 'Chinese_PRC_CI_AS', 'old_tech_check_idea': 'Chinese_PRC_CI_AS', 'old_atte': 'Chinese_PRC_CI_AS', 'old_program_kind_id': 'Chinese_PRC_CI_AS', 'old_confirm_side_id': 'Chinese_PRC_CI_AS', 'old_price_check_idea': 'Chinese_PRC_CI_AS', 'old_craft_checker': 'Chinese_PRC_CI_AS', 'old_tech_checker': 'Chinese_PRC_CI_AS', 'old_price_checker': 'Chinese_PRC_CI_AS', 'old_plan_checker': 'Chinese_PRC_CI_AS', 'old_weight_unit': 'Chinese_PRC_CI_AS', 'old_model1': 'Chinese_PRC_CI_AS', 'old_color_kind': 'Chinese_PRC_CI_AS', 'old_code': 'Chinese_PRC_CI_AS', 'old_storage_unit_ids': 'Chinese_PRC_CI_AS', 'old_roll_avg_qty_str': 'Chinese_PRC_CI_AS', 'old_unit': 'Chinese_PRC_CI_AS', 'old_pre_production_id': 'Chinese_PRC_CI_AS', 'old_fabric_kind_id': 'Chinese_PRC_CI_AS', 'old_lot': 'Chinese_PRC_CI_AS', 'old_color_match': 'Chinese_PRC_CI_AS', 'old_plaiting': 'Chinese_PRC_CI_AS', 'old_edge': 'Chinese_PRC_CI_AS', 'old_code_front': 'Chinese_PRC_CI_AS', 'old_provider_code': 'Chinese_PRC_CI_AS', 'old_dlv_address': 'Chinese_PRC_CI_AS', 'old_machine_pin': 'Chinese_PRC_CI_AS', 'old_fabric_id': 'Chinese_PRC_CI_AS', 'old_dry_fub': 'Chinese_PRC_CI_AS', 'old_wet_fub': 'Chinese_PRC_CI_AS', 'old_wash_fastness': 'Chinese_PRC_CI_AS', 'old_solar_fastness': 'Chinese_PRC_CI_AS', 'old_shrin_v': 'Chinese_PRC_CI_AS', 'old_shrin_l': 'Chinese_PRC_CI_AS', 'old_remarks01': 'Chinese_PRC_CI_AS', 'old_remarks02': 'Chinese_PRC_CI_AS', 'old_remarks03': 'Chinese_PRC_CI_AS', 'old_remarks04': 'Chinese_PRC_CI_AS', 'old_print_code': 'Chinese_PRC_CI_AS', 'old_color_plate_id': 'Chinese_PRC_CI_AS', 'old_film_no': 'Chinese_PRC_CI_AS', 'old_width': 'Chinese_PRC_CI_AS', 'old_weight': 'Chinese_PRC_CI_AS', 'old_cust_gray_id': 'Chinese_PRC_CI_AS', 'old_color_remarks': 'Chinese_PRC_CI_AS', 'old_width_unit': 'Chinese_PRC_CI_AS', 'old_weight_kind_id': 'Chinese_PRC_CI_AS', 'old_grade_id': 'Chinese_PRC_CI_AS', 'old_gwname': 'Chinese_PRC_CI_AS', 'old_dye_date': 'Chinese_PRC_CI_AS', 'old_postpone_advance': 'Chinese_PRC_CI_AS', 'old_batch_color_case': 'Chinese_PRC_CI_AS', 'old_cust_job_no': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：OrderMain', 'target': 'erp_sales.SourceDyeOrderMain', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 OrderColorSup → OrderMainSup', '原界面主从 OrderColor → OrderMain', '原界面主从 PrintOrderColor → PrintOrderMain', '原界面主从 OrderColorChange → OrderMainChange']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_check_no=models.CharField('订单明细号', null=False, blank=True, max_length=20)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=20)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=200)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=200)
    old_rela_lot_no=models.CharField('参考批号', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('颜色编码', null=True, blank=True, max_length=150)
    old_color_e=models.CharField('颜色英文名', null=True, blank=True, max_length=20)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=50)
    old_design_no=models.CharField('花号', null=True, blank=True, max_length=20)
    old_width_dn=models.CharField('门幅下限', null=True, blank=True, max_length=150)
    old_width_up=models.DecimalField('门幅上限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_width_kind_id=models.CharField('幅宽种类', null=True, blank=True, max_length=20)
    old_weight_dn=models.CharField('克重下限', null=True, blank=True, max_length=150)
    old_weight_up=models.DecimalField('克重上限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_order_qty=models.DecimalField('成品数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_order_rolls=models.DecimalField('订单粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_gray_qty=models.DecimalField('投坏数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('染整价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_fee=models.DecimalField('费用', null=True, blank=True, max_digits=10, decimal_places=2)
    old_amount=models.DecimalField('金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dlv_date=models.DateTimeField('染色日期', null=True, blank=True)
    old_sum_dlv_rolls=models.DecimalField('合计交货粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_sum_dlv_qty=models.DecimalField('合计交货数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_to_place=models.CharField('交货地点', null=True, blank=True, max_length=500)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_cust_self_product=models.CharField('客户规格', null=True, blank=True, max_length=250)
    old_color_depth_id=models.CharField('颜色深浅', null=True, blank=True, max_length=10)
    old_cust_color_num=models.CharField('客户色号', null=True, blank=True, max_length=100)
    old_production_id=models.CharField('工艺线路', null=True, blank=True, max_length=10)
    old_card_qty=models.IntegerField('缸数', null=True, blank=True)
    old_stand_craft_no=models.CharField('标准工艺号', null=True, blank=True, max_length=20)
    old_craft_check=models.BooleanField('工艺审核状态', null=True, blank=True)
    old_tech_check=models.BooleanField('技术审核状态', null=True, blank=True)
    old_plan_check=models.BooleanField('计划审核状态', null=True, blank=True)
    old_cust_fabric_name=models.CharField('客户规格', null=True, blank=True, max_length=250)
    old_detail_cust_name=models.CharField('明细客户', null=True, blank=True, max_length=150)
    old_contract_no=models.TextField('客户单号', null=True, blank=True)
    old_cust_self_no=models.CharField('制单号', null=True, blank=True, max_length=150)
    old_cust_self_no_detail=models.CharField('客户单号明细', null=True, blank=True, max_length=150)
    old_main_stuff_kind_id=models.CharField('主染料类别', null=True, blank=True, max_length=10)
    old_final_dlv_date=models.DateTimeField('协议交货日期', null=True, blank=True)
    old_is_to_do_sample=models.CharField('打样安排', null=True, blank=True, max_length=10)
    old_is_sample_charge=models.BooleanField('打样是否收费', null=True, blank=True)
    old_craft_check_idea=models.CharField('工艺审核意见', null=True, blank=True, max_length=300)
    old_craft_check_time=models.DateTimeField('工艺审核时间', null=True, blank=True)
    old_plan_check_idea=models.CharField('计划审核意见', null=True, blank=True, max_length=300)
    old_plan_check_time=models.DateTimeField('计划审核时间', null=True, blank=True)
    old_tech_check_idea=models.CharField('技术审核意见', null=True, blank=True, max_length=300)
    old_tech_check_time=models.DateTimeField('技术审核时间', null=True, blank=True)
    old_color_rgb=models.IntegerField('颜色RGB', null=True, blank=True)
    old_sum_prod_rolls=models.DecimalField('合计成品粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_sum_prod_qty=models.DecimalField('合计成品数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_is_continue=models.BooleanField('连缸', null=True, blank=True)
    old_is_to_confirmed=models.BooleanField('是否要确认', null=True, blank=True)
    old_is_spec_color=models.BooleanField('特殊颜色', null=True, blank=True)
    old_is_spec_vat=models.BooleanField('小缸', null=True, blank=True)
    old_color_cards=models.IntegerField('色卡份数', null=True, blank=True)
    old_atte=models.CharField('特殊事项', null=True, blank=True, max_length=100)
    old_program_kind_id=models.CharField('染色工艺分类', null=True, blank=True, max_length=10)
    old_is_have_first_vat=models.BooleanField('有头缸', null=True, blank=True)
    old_confirm_side_id=models.CharField('对色面', null=True, blank=True, max_length=10)
    old_process_price=models.DecimalField('另收费项目单价', null=True, blank=True, max_digits=8, decimal_places=2)
    old_price_check=models.BooleanField('价格审核状态', null=True, blank=True)
    old_price_check_idea=models.CharField('价格审核意见', null=True, blank=True, max_length=300)
    old_price_check_time=models.DateTimeField('价格审核时间', null=True, blank=True)
    old_craft_checker=models.CharField('工艺审核人', null=True, blank=True, max_length=10)
    old_tech_checker=models.CharField('技术审核人', null=True, blank=True, max_length=10)
    old_price_checker=models.CharField('价格审核人', null=True, blank=True, max_length=10)
    old_plan_checker=models.CharField('计划审核人', null=True, blank=True, max_length=10)
    old_prepare_vats=models.DecimalField('前处理缸数', null=True, blank=True, max_digits=5, decimal_places=1)
    old_weight_unit=models.CharField('克重单位', null=True, blank=True, max_length=20)
    old_model1=models.CharField('款号', null=True, blank=True, max_length=200)
    old_color_kind=models.CharField('ColorKind', null=True, blank=True, max_length=20)
    old_code=models.CharField('颜色备用', null=True, blank=True, max_length=20)
    old_storage_unit_ids=models.CharField('StorageUnitIDs', null=True, blank=True, max_length=100)
    old_roll_avg_qty_str=models.CharField('RollAvgQtyStr', null=True, blank=True, max_length=50)
    old_unit=models.CharField('单位', null=True, blank=True, max_length=50)
    old_is_finished=models.BooleanField('IsFinished', null=True, blank=True)
    old_pre_production_id=models.CharField('PreProductionID', null=True, blank=True, max_length=50)
    old_fabric_kind_id=models.CharField('FabricKindID', null=True, blank=True, max_length=10)
    old_lot=models.CharField('LOT', null=True, blank=True, max_length=50)
    old_color_match=models.CharField('ColorMatch', null=True, blank=True, max_length=500)
    old_needle_count_up=models.IntegerField('NeedleCountUp', null=True, blank=True)
    old_needle_count_dn=models.IntegerField('NeedleCountDn', null=True, blank=True)
    old_twist=models.IntegerField('Twist', null=True, blank=True)
    old_tenters=models.IntegerField('Tenters', null=True, blank=True)
    old_plaiting=models.CharField('Plaiting', null=True, blank=True, max_length=50)
    old_edge=models.CharField('手感', null=True, blank=True, max_length=50)
    old_code_front=models.CharField('CodeFront', null=True, blank=True, max_length=50)
    old_provider_code=models.CharField('ProviderCode', null=True, blank=True, max_length=16)
    old_dlv_address=models.CharField('DlvAddress', null=True, blank=True, max_length=200)
    old_plan_date=models.DateTimeField('PlanDate', null=True, blank=True)
    old_require_weight=models.DecimalField('RequireWeight', null=True, blank=True, max_digits=10, decimal_places=2)
    old_require_kg=models.DecimalField('RequireKG', null=True, blank=True, max_digits=10, decimal_places=2)
    old_machine_pin=models.CharField('织厂', null=True, blank=True, max_length=200)
    old_machine_dozen=models.FloatField('MachineDozen', null=True, blank=True)
    old_fabric_id=models.CharField('客户规格', null=True, blank=True, max_length=50)
    old_out_qty=models.DecimalField('OutQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_out_yard=models.DecimalField('OutYard', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dry_fub=models.CharField('DryFub', null=True, blank=True, max_length=20)
    old_wet_fub=models.CharField('WetFub', null=True, blank=True, max_length=20)
    old_wash_fastness=models.CharField('WashFastness', null=True, blank=True, max_length=20)
    old_solar_fastness=models.CharField('SolarFastness', null=True, blank=True, max_length=20)
    old_shrin_v=models.CharField('ShrinV', null=True, blank=True, max_length=30)
    old_shrin_l=models.CharField('ShrinL', null=True, blank=True, max_length=30)
    old_cut_yard=models.DecimalField('CutYard', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks01=models.CharField('备注01', null=True, blank=True, max_length=512)
    old_remarks02=models.CharField('明细状态', null=True, blank=True, max_length=512)
    old_remarks03=models.CharField('参考缸号', null=True, blank=True, max_length=512)
    old_remarks04=models.CharField('Remarks04', null=True, blank=True, max_length=512)
    old_print_code=models.CharField('花号', null=True, blank=True, max_length=50)
    old_color_plate_id=models.CharField('色位号', null=True, blank=True, max_length=10)
    old_film_no=models.CharField('菲林号', null=True, blank=True, max_length=50)
    old_width=models.CharField('幅宽', null=True, blank=True, max_length=200)
    old_weight=models.CharField('克重', null=True, blank=True, max_length=200)
    old_add_weigth=models.FloatField('空计', null=True, blank=True)
    old_tube_weight=models.FloatField('纸筒', null=True, blank=True)
    old_cust_gray_id=models.CharField('客纱种编码', null=True, blank=True, max_length=50)
    old_rate=models.FloatField('浮动百分比', null=True, blank=True)
    old_color_remarks=models.CharField('用途', null=True, blank=True, max_length=500)
    old_width_unit=models.CharField('WidthUnit', null=True, blank=True, max_length=20)
    old_weight_kind_id=models.CharField('克重单位', null=True, blank=True, max_length=20)
    old_is_supplement=models.BooleanField('补单', null=True, blank=True)
    old_bhd=models.BooleanField('备货单', null=True, blank=True)
    old_grade_id=models.CharField('色号等级', null=True, blank=True, max_length=50)
    old_gwname=models.CharField('缸位字母', null=True, blank=True, max_length=20)
    old_dye_date=models.CharField('交货日期', null=True, blank=True, max_length=150)
    old_postpone_advance=models.CharField('Postpone_Advance', null=True, blank=True, max_length=150)
    old_batch_color_case=models.CharField('BatchColorCase', null=True, blank=True, max_length=150)
    old_is_pur_apl_no=models.BooleanField('是否采购申请单(旧ERP申请单)', null=True, blank=True)
    old_cust_job_no=models.CharField('客户缸号', null=True, blank=True, max_length=100)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_approve_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=30)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=30)
    old_modify_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_sheet_status=models.IntegerField('中止状态', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_sales.SourceDyeOrderMain', verbose_name='原关系：OrderMain', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_ordercolor'
        indexes=[models.Index(fields=['source_batch', 'old_check_no'],name='src_066fa9cb9b5015d3'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_check_no'))),name='src_ci_066fa9cb9b5015d3'),models.Index(fields=['source_batch', 'old_sheet_series', 'old_check_no'],name='src_4eadb49ce5cc10bb'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_check_no'))),name='src_ci_4eadb49ce5cc10bb')]
        verbose_name=verbose_name_plural='订单颜色/规格明细'
        ordering=["-id"]

class SourceDyeOrderCombine(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='OrderCombine'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'CheckNo': 'old_check_no', 'Rolls': 'old_rolls', 'Qty': 'old_qty', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('SheetSeries', 'CheckNo')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_check_no=models.CharField('CheckNo', null=False, blank=True, max_length=20)
    old_rolls=models.DecimalField('Rolls', null=True, blank=True, max_digits=7, decimal_places=2)
    old_qty=models.DecimalField('Qty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=300)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_ordercombine'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_check_no'],name='src_a92689dc716f0c34'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_check_no'))),name='src_ci_a92689dc716f0c34')]
        verbose_name=verbose_name_plural='客户订单与销售相关表（OrderCombine，待确认）'
        ordering=["-id"]

class SourceDyeOrderDlvApply(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='OrderDlvApply'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'BusinessKind': 'old_business_kind', 'BusinessUnitID': 'old_business_unit_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'StepNo': 'old_step_no', 'SalerID': 'old_saler_id', 'CustomerID': 'old_customer_id', 'Rolls': 'old_rolls', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'ApproveIdea': 'old_approve_idea', 'Remarks': 'old_remarks', 'ApplyDlvDate': 'old_apply_dlv_date', 'SheetKind': 'old_sheet_kind', 'SheetType': 'old_sheet_type', 'ApplyKindID': 'old_apply_kind_id', 'Status': 'old_status', 'OrderSheetSeries': 'old_order_sheet_series', 'Reason': 'old_reason', 'PreField1': 'old_pre_field1', 'PreField2': 'old_pre_field2', 'PreField3': 'old_pre_field3', 'PreField4': 'old_pre_field4', 'PreField5': 'old_pre_field5', 'IsVIP': 'old_is_vip', 'VipReason': 'old_vip_reason'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_saler_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_approve_idea': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_apply_kind_id': 'Chinese_PRC_CI_AS', 'old_order_sheet_series': 'Chinese_PRC_CI_AS', 'old_reason': 'Chinese_PRC_CI_AS', 'old_pre_field1': 'Chinese_PRC_CI_AS', 'old_pre_field2': 'Chinese_PRC_CI_AS', 'old_pre_field3': 'Chinese_PRC_CI_AS', 'old_pre_field4': 'Chinese_PRC_CI_AS', 'old_pre_field5': 'Chinese_PRC_CI_AS', 'old_vip_reason': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=50)
    old_sheet_no=models.CharField('编号', null=True, blank=True, max_length=36)
    old_business_kind=models.IntegerField('BusinessKind', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('SheetStatus', null=True, blank=True)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_saler_id=models.CharField('业务员', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=50)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_length_qty=models.DecimalField('长度数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('重量数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_create_date=models.DateTimeField('创建日期', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_approve_date=models.DateTimeField('审核日期', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_approve_idea=models.CharField('ApproveIdea', null=True, blank=True, max_length=200)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_apply_dlv_date=models.DateField('交货日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('SheetKind', null=True, blank=True)
    old_sheet_type=models.IntegerField('SheetType', null=True, blank=True)
    old_apply_kind_id=models.CharField('申请种类', null=True, blank=True, max_length=50)
    old_status=models.IntegerField('状态', null=True, blank=True)
    old_order_sheet_series=models.CharField('订单流水号', null=True, blank=True, max_length=20)
    old_reason=models.CharField('原因', null=True, blank=True, max_length=256)
    old_pre_field1=models.CharField('捻度(H/S)', null=True, blank=True, max_length=50)
    old_pre_field2=models.CharField('打回原因', null=True, blank=True, max_length=50)
    old_pre_field3=models.CharField('PreField3', null=True, blank=True, max_length=50)
    old_pre_field4=models.CharField('PreField4', null=True, blank=True, max_length=50)
    old_pre_field5=models.CharField('PreField5', null=True, blank=True, max_length=50)
    old_is_vip=models.BooleanField('是否VIP', null=True, blank=True)
    old_vip_reason=models.CharField('VIP原因', null=True, blank=True, max_length=500)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_orderdlvapply'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_5934ae36169a4817'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_5934ae36169a4817')]
        verbose_name=verbose_name_plural='客户订单与销售相关表（OrderDlvApply，待确认）'
        ordering=["-id"]

class SourceDyeOrderDlvApplyLock(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='OrderDlvApplyLock'
    SOURCE_FIELDS={'ApplyDlvDate': 'old_apply_dlv_date', 'Rolls': 'old_rolls', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'Status': 'old_status', 'Remarks': 'old_remarks', 'ApplyKindID': 'old_apply_kind_id'}
    SOURCE_KEY=('ApplyKindID', 'ApplyDlvDate')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_creater': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_apply_kind_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_apply_dlv_date=models.DateField('申请日期', null=False, blank=False)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_length_qty=models.DecimalField('长度数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('重量数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_create_date=models.DateTimeField('创建日期', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_status=models.IntegerField('状态', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_apply_kind_id=models.CharField('申请种类', null=False, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_orderdlvapplylock'
        indexes=[models.Index(fields=['source_batch', 'old_apply_kind_id', 'old_apply_dlv_date'],name='src_87a57b072b6b344e'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_apply_kind_id'))),models.F('old_apply_dlv_date'),name='src_ci_87a57b072b6b344e')]
        verbose_name=verbose_name_plural='客户订单与销售相关表（OrderDlvApplyLock，待确认）'
        ordering=["-id"]

class SourceDyeOrderDlvApplySheet(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='OrderDlvApplySheet'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'OrderSheetSeries': 'old_order_sheet_series', 'OrderSheetNo': 'old_order_sheet_no', 'CheckNo': 'old_check_no', 'SheetDate': 'old_sheet_date', 'Rolls': 'old_rolls', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'Status': 'old_status', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('SheetSeries', 'OrderSheetSeries')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_order_sheet_series': 'Chinese_PRC_CI_AS', 'old_order_sheet_no': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：OrderMain', 'target': 'erp_sales.SourceDyeOrderMain', 'source_fields': ['OrderSheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 OrderDlvApplySheet → OrderMain', '原界面主从 PrintOrderDlvApplySheet → PrintOrderMain', '原界面主从 OrderDlvApplySheetSup → OrderMainSup']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=50)
    old_order_sheet_series=models.CharField('订单流水号', null=False, blank=True, max_length=20)
    old_order_sheet_no=models.CharField('订单号', null=True, blank=True, max_length=20)
    old_check_no=models.CharField('订单明细号', null=True, blank=True, max_length=50)
    old_sheet_date=models.DateTimeField('下单日期', null=True, blank=True)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_length_qty=models.DecimalField('长度数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('重量数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_status=models.IntegerField('状态', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    source_parent_1=models.ForeignKey('erp_sales.SourceDyeOrderMain', verbose_name='原关系：OrderMain', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_orderdlvapplysheet'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_order_sheet_series'],name='src_370e95c47e06cec4'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_order_sheet_series'))),name='src_ci_370e95c47e06cec4')]
        verbose_name=verbose_name_plural='客户订单与销售相关表（OrderDlvApplySheet，待确认）'
        ordering=["-id"]

class SourceDyeOrderFee(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='OrderFee'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'FeeKindID': 'old_fee_kind_id', 'PreValue': 'old_pre_value', 'Remarks': 'old_remarks', 'RealValue': 'old_real_value', 'Description': 'old_description', 'CurrDate': 'old_curr_date', 'Maker': 'old_maker'}
    SOURCE_KEY=('SheetSeries', 'FeeKindID')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_fee_kind_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_description': 'Chinese_PRC_CI_AS', 'old_maker': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_fee_kind_id=models.CharField('FeeKindID', null=False, blank=True, max_length=10)
    old_pre_value=models.DecimalField('PreValue', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=100)
    old_real_value=models.DecimalField('RealValue', null=True, blank=True, max_digits=10, decimal_places=2)
    old_description=models.CharField('Description', null=True, blank=True, max_length=100)
    old_curr_date=models.DateTimeField('CurrDate', null=True, blank=True)
    old_maker=models.CharField('Maker', null=True, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_orderfee'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_fee_kind_id'],name='src_acd3a927dea1960e'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_fee_kind_id'))),name='src_ci_acd3a927dea1960e')]
        verbose_name=verbose_name_plural='客户订单与销售相关表（OrderFee，待确认）'
        ordering=["-id"]

class SourceDyeOrderInfo(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='OrderInfo'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'SheetStatus': 'old_sheet_status', 'SheetType': 'old_sheet_type', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'Revisions': 'old_revisions', 'BusinessUnitID': 'old_business_unit_id', 'StepNo': 'old_step_no', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'CheckNo': 'old_check_no', 'ProdID': 'old_prod_id', 'LotNo': 'old_lot_no', 'FabricKindID': 'old_fabric_kind_id', 'ColorKind': 'old_color_kind', 'LOT': 'old_lot', 'ColorMatch': 'old_color_match', 'ColorNum': 'old_color_num', 'NeedleCountUp': 'old_needle_count_up', 'NeedleCountDn': 'old_needle_count_dn', 'ColorID': 'old_color_id', 'Twist': 'old_twist', 'Tenters': 'old_tenters', 'WeightDn': 'old_weight_dn', 'Plaiting': 'old_plaiting', 'WeightUp': 'old_weight_up', 'Edge': 'old_edge', 'CodeFront': 'old_code_front', 'ProviderCode': 'old_provider_code', 'DlvAddress': 'old_dlv_address', 'DlvDate': 'old_dlv_date', 'PlanDate': 'old_plan_date', 'RequireWeight': 'old_require_weight', 'RequireKG': 'old_require_kg', 'MachinePin': 'old_machine_pin', 'MachineDozen': 'old_machine_dozen', 'FabricID': 'old_fabric_id', 'OutQty': 'old_out_qty', 'OutYard': 'old_out_yard', 'DryFub': 'old_dry_fub', 'WetFub': 'old_wet_fub', 'WashFastness': 'old_wash_fastness', 'SolarFastness': 'old_solar_fastness', 'ShrinV': 'old_shrin_v', 'ShrinL': 'old_shrin_l', 'CutYard': 'old_cut_yard', 'Remarks01': 'old_remarks01', 'Remarks02': 'old_remarks02', 'Remarks03': 'old_remarks03', 'Remarks04': 'old_remarks04'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_fabric_kind_id': 'Chinese_PRC_CI_AS', 'old_color_kind': 'Chinese_PRC_CI_AS', 'old_lot': 'Chinese_PRC_CI_AS', 'old_color_match': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_plaiting': 'Chinese_PRC_CI_AS', 'old_edge': 'Chinese_PRC_CI_AS', 'old_code_front': 'Chinese_PRC_CI_AS', 'old_provider_code': 'Chinese_PRC_CI_AS', 'old_dlv_address': 'Chinese_PRC_CI_AS', 'old_machine_pin': 'Chinese_PRC_CI_AS', 'old_fabric_id': 'Chinese_PRC_CI_AS', 'old_dry_fub': 'Chinese_PRC_CI_AS', 'old_wet_fub': 'Chinese_PRC_CI_AS', 'old_wash_fastness': 'Chinese_PRC_CI_AS', 'old_solar_fastness': 'Chinese_PRC_CI_AS', 'old_shrin_v': 'Chinese_PRC_CI_AS', 'old_shrin_l': 'Chinese_PRC_CI_AS', 'old_remarks01': 'Chinese_PRC_CI_AS', 'old_remarks02': 'Chinese_PRC_CI_AS', 'old_remarks03': 'Chinese_PRC_CI_AS', 'old_remarks04': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_sheet_type=models.IntegerField('订单分型', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_create_date=models.DateTimeField('创建日期', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_step_no=models.IntegerField('流程节点号', null=True, blank=True)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_check_no=models.CharField('订单明细号', null=False, blank=True, max_length=20)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=20)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=200)
    old_fabric_kind_id=models.CharField('纱编类别', null=True, blank=True, max_length=10)
    old_color_kind=models.CharField('颜色类别', null=True, blank=True, max_length=20)
    old_lot=models.CharField('LOT号', null=True, blank=True, max_length=50)
    old_color_match=models.CharField('对色资料', null=True, blank=True, max_length=500)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=20)
    old_needle_count_up=models.IntegerField('针数/寸数', null=True, blank=True)
    old_needle_count_dn=models.IntegerField('针数/寸数', null=True, blank=True)
    old_color_id=models.CharField('颜色编码', null=True, blank=True, max_length=150)
    old_twist=models.IntegerField('扭度', null=True, blank=True)
    old_tenters=models.IntegerField('定型', null=True, blank=True)
    old_weight_dn=models.DecimalField('(折纱)克重', null=True, blank=True, max_digits=6, decimal_places=2)
    old_plaiting=models.CharField('折纱', null=True, blank=True, max_length=50)
    old_weight_up=models.DecimalField('(定型)克重', null=True, blank=True, max_digits=6, decimal_places=2)
    old_edge=models.CharField('连边', null=True, blank=True, max_length=50)
    old_code_front=models.CharField('编号头', null=True, blank=True, max_length=50)
    old_provider_code=models.CharField('供应商', null=True, blank=True, max_length=16)
    old_dlv_address=models.CharField('送交', null=True, blank=True, max_length=200)
    old_dlv_date=models.DateTimeField('交货日期', null=True, blank=True)
    old_plan_date=models.DateTimeField('排交日期', null=True, blank=True)
    old_require_weight=models.DecimalField('要求重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_require_kg=models.DecimalField('(要求)公斤', null=True, blank=True, max_digits=10, decimal_places=2)
    old_machine_pin=models.CharField('扁机尺寸', null=True, blank=True, max_length=50)
    old_machine_dozen=models.FloatField('扁机打数', null=True, blank=True)
    old_fabric_id=models.CharField('客户规格', null=True, blank=True, max_length=50)
    old_out_qty=models.DecimalField('客户要求出货数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_out_yard=models.DecimalField('客户要求出货码数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dry_fub=models.CharField('干擦级数', null=True, blank=True, max_length=20)
    old_wet_fub=models.CharField('湿擦级数', null=True, blank=True, max_length=20)
    old_wash_fastness=models.CharField('洗水级数', null=True, blank=True, max_length=20)
    old_solar_fastness=models.CharField('日晒级数', null=True, blank=True, max_length=20)
    old_shrin_v=models.CharField('横缩', null=True, blank=True, max_length=30)
    old_shrin_l=models.CharField('直缩', null=True, blank=True, max_length=30)
    old_cut_yard=models.DecimalField('成品剪码数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks01=models.CharField('工场备注1', null=True, blank=True, max_length=512)
    old_remarks02=models.CharField('工场备注2', null=True, blank=True, max_length=512)
    old_remarks03=models.CharField('仓库备注', null=True, blank=True, max_length=512)
    old_remarks04=models.CharField('执胚单', null=True, blank=True, max_length=512)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_orderinfo'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_54b66f675194425c'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_54b66f675194425c')]
        verbose_name=verbose_name_plural='客户订单与销售相关表（OrderInfo，待确认）'
        ordering=["-id"]

class SourceDyeOrderInfoProcess(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='OrderInfoProcess'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'ProcessNo': 'old_process_no', 'ProcessID': 'old_process_id', 'ProcessName': 'old_process_name', 'ProcessClass': 'old_process_class'}
    SOURCE_KEY=('SheetSeries', 'ProcessNo')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_process_id': 'Chinese_PRC_CI_AS', 'old_process_name': 'Chinese_PRC_CI_AS', 'old_process_class': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：OrderInfo', 'target': 'erp_sales.SourceDyeOrderInfo', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 OrderInfoProcess → OrderInfo']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=50)
    old_process_no=models.IntegerField('顺序', null=False, blank=False)
    old_process_id=models.CharField('工序编号', null=True, blank=True, max_length=10)
    old_process_name=models.CharField('工序名称', null=True, blank=True, max_length=100)
    old_process_class=models.CharField('类别', null=True, blank=True, max_length=50)
    source_parent_1=models.ForeignKey('erp_sales.SourceDyeOrderInfo', verbose_name='原关系：OrderInfo', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_orderinfoprocess'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_process_no'],name='src_b9f38ea38bd2bd6f'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),models.F('old_process_no'),name='src_ci_b9f38ea38bd2bd6f')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（OrderInfoProcess，待确认）'
        ordering=["-id"]

class SourceDyeOrderMain(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='OrderMain'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'SheetType': 'old_sheet_type', 'OrderKindID': 'old_order_kind_id', 'BusinessUnitID': 'old_business_unit_id', 'SalerGroupID': 'old_saler_group_id', 'CustomerID': 'old_customer_id', 'DetailCustName': 'old_detail_cust_name', 'SalerID': 'old_saler_id', 'ContractNo': 'old_contract_no', 'Linker': 'old_linker', 'ExchangeRate': 'old_exchange_rate', 'PriceUnit': 'old_price_unit', 'CurrencyID': 'old_currency_id', 'PaymentID': 'old_payment_id', 'SettleID': 'old_settle_id', 'DlvMannerID': 'old_dlv_manner_id', 'HandFeelID': 'old_hand_feel_id', 'VerLight1ID': 'old_ver_light1_id', 'FirstDlvDate': 'old_first_dlv_date', 'OrderUp': 'old_order_up', 'OrderDn': 'old_order_dn', 'RealGrayQty': 'old_real_gray_qty', 'RealGrayPrice': 'old_real_gray_price', 'RealGrayMoney': 'old_real_gray_money', 'RealProdQty': 'old_real_prod_qty', 'RealProdPrice': 'old_real_prod_price', 'RealProdMoney': 'old_real_prod_money', 'RealLoss': 'old_real_loss', 'RealProfit': 'old_real_profit', 'RealUnitProfit': 'old_real_unit_profit', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'StepNo': 'old_step_no', 'BusinessKind': 'old_business_kind', 'CustSelfNo': 'old_cust_self_no', 'VerLight2ID': 'old_ver_light2_id', 'IsHurry': 'old_is_hurry', 'FinishDate': 'old_finish_date', 'AssignUnit': 'old_assign_unit', 'RollCodeManner': 'old_roll_code_manner', 'VatCodeManner': 'old_vat_code_manner', 'LabelID': 'old_label_id', 'ShippingMarkID': 'old_shipping_mark_id', 'Unit': 'old_unit', 'AddQty': 'old_add_qty', 'Discount': 'old_discount', 'ClothInspection': 'old_cloth_inspection', 'FactID': 'old_fact_id', 'ToPlace': 'old_to_place', 'WeftDensity': 'old_weft_density', 'WarpDensity': 'old_warp_density', 'TakeFabStatus': 'old_take_fab_status', 'LinkerInfo': 'old_linker_info', 'Loss': 'old_loss', 'LossStr': 'old_loss_str', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'InvoiceKind': 'old_invoice_kind', 'AddrDlv': 'old_addr_dlv', 'RedoReasonID': 'old_redo_reason_id', 'IsFinished': 'old_is_finished', 'PrepareSheetNo': 'old_prepare_sheet_no', 'ProdID': 'old_prod_id', 'PrintCode': 'old_print_code', 'BHD': 'old_bhd', 'JiaGong': 'old_jia_gong'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_order_kind_id': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_saler_group_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_detail_cust_name': 'Chinese_PRC_CI_AS', 'old_saler_id': 'Chinese_PRC_CI_AS', 'old_contract_no': 'Chinese_PRC_CI_AS', 'old_linker': 'Chinese_PRC_CI_AS', 'old_currency_id': 'Chinese_PRC_CI_AS', 'old_payment_id': 'Chinese_PRC_CI_AS', 'old_settle_id': 'Chinese_PRC_CI_AS', 'old_dlv_manner_id': 'Chinese_PRC_CI_AS', 'old_hand_feel_id': 'Chinese_PRC_CI_AS', 'old_ver_light1_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_cust_self_no': 'Chinese_PRC_CI_AS', 'old_ver_light2_id': 'Chinese_PRC_CI_AS', 'old_label_id': 'Chinese_PRC_CI_AS', 'old_shipping_mark_id': 'Chinese_PRC_CI_AS', 'old_fact_id': 'Chinese_PRC_CI_AS', 'old_to_place': 'Chinese_PRC_CI_AS', 'old_take_fab_status': 'Chinese_PRC_CI_AS', 'old_linker_info': 'Chinese_PRC_CI_AS', 'old_loss_str': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_addr_dlv': 'Chinese_PRC_CI_AS', 'old_redo_reason_id': 'Chinese_PRC_CI_AS', 'old_prepare_sheet_no': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_print_code': 'Chinese_PRC_CI_AS', 'old_jia_gong': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_sheet_no': ('literal', ''), 'old_sheet_date': ('literal', '1900-01-01'), 'old_sheet_kind': ('literal', 0), 'old_order_kind_id': ('literal', ''), 'old_business_unit_id': ('literal', ''), 'old_saler_group_id': ('literal', ''), 'old_customer_id': ('literal', ''), 'old_detail_cust_name': ('literal', ''), 'old_saler_id': ('literal', ''), 'old_contract_no': ('literal', ''), 'old_linker': ('literal', ''), 'old_exchange_rate': ('literal', 0), 'old_price_unit': ('literal', 0), 'old_currency_id': ('literal', ''), 'old_payment_id': ('literal', ''), 'old_settle_id': ('literal', ''), 'old_dlv_manner_id': ('literal', ''), 'old_hand_feel_id': ('literal', ''), 'old_ver_light1_id': ('literal', ''), 'old_first_dlv_date': ('literal', '1900-01-01'), 'old_order_up': ('literal', 0), 'old_order_dn': ('literal', 0), 'old_real_gray_qty': ('literal', 0), 'old_real_gray_price': ('literal', 0), 'old_real_gray_money': ('literal', 0), 'old_real_prod_qty': ('literal', 0), 'old_real_prod_price': ('literal', 0), 'old_real_prod_money': ('literal', 0), 'old_real_loss': ('literal', 0), 'old_real_profit': ('literal', 0), 'old_real_unit_profit': ('literal', 0), 'old_sheet_status': ('literal', 0), 'old_right_status': ('literal', 0), 'old_print_times': ('literal', 0), 'old_revisions': ('literal', 0), 'old_remarks': ('literal', ''), 'old_creater': ('literal', ''), 'old_create_date': ('literal', '1900-01-01'), 'old_modifyer': ('literal', ''), 'old_modify_date': ('literal', '1900-01-01')}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_sheet_type=models.IntegerField('订单分型', null=True, blank=True)
    old_order_kind_id=models.CharField('订单类别代码', null=True, blank=True, max_length=10)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('业务组别', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户代码', null=True, blank=True, max_length=10)
    old_detail_cust_name=models.CharField('明细客户', null=True, blank=True, max_length=150)
    old_saler_id=models.CharField('业务员', null=True, blank=True, max_length=10)
    old_contract_no=models.CharField('客户单号', null=True, blank=True, max_length=500)
    old_linker=models.CharField('品牌', null=True, blank=True, max_length=250)
    old_exchange_rate=models.DecimalField('汇率', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price_unit=models.IntegerField('计价单位编码', null=True, blank=True)
    old_currency_id=models.CharField('币别', null=True, blank=True, max_length=10)
    old_payment_id=models.CharField('付款方式', null=True, blank=True, max_length=10)
    old_settle_id=models.CharField('结算方式', null=True, blank=True, max_length=10)
    old_dlv_manner_id=models.CharField('交货方式编码', null=True, blank=True, max_length=10)
    old_hand_feel_id=models.CharField('手感编码', null=True, blank=True, max_length=10)
    old_ver_light1_id=models.CharField('主对色光源', null=True, blank=True, max_length=10)
    old_first_dlv_date=models.DateTimeField('头缸交期', null=True, blank=True)
    old_order_up=models.IntegerField('订量上限', null=True, blank=True)
    old_order_dn=models.IntegerField('订量下限', null=True, blank=True)
    old_real_gray_qty=models.DecimalField('实际投坏数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_gray_price=models.DecimalField('实际坏纱价格', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_gray_money=models.DecimalField('实际坏纱成本', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_prod_qty=models.DecimalField('实际成品数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_prod_price=models.DecimalField('实际成品价格', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_prod_money=models.DecimalField('实际成品金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_loss=models.DecimalField('实际缩率', null=True, blank=True, max_digits=4, decimal_places=1)
    old_real_profit=models.DecimalField('实际毛利', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_unit_profit=models.DecimalField('实际毛利率', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.TextField('备注', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_step_no=models.IntegerField('流程节点号', null=True, blank=True)
    old_business_kind=models.IntegerField('业务类别', null=True, blank=True)
    old_cust_self_no=models.CharField('制单号', null=True, blank=True, max_length=500)
    old_ver_light2_id=models.CharField('副光源', null=True, blank=True, max_length=10)
    old_is_hurry=models.BooleanField('加急', null=True, blank=True)
    old_finish_date=models.DateTimeField('结案日期', null=True, blank=True)
    old_assign_unit=models.IntegerField('配纱单位', null=True, blank=True)
    old_roll_code_manner=models.IntegerField('箱号编码规则', null=True, blank=True)
    old_vat_code_manner=models.IntegerField('缸号编码规则', null=True, blank=True)
    old_label_id=models.CharField('标签', null=True, blank=True, max_length=10)
    old_shipping_mark_id=models.CharField('唛头', null=True, blank=True, max_length=10)
    old_unit=models.IntegerField('单位', null=True, blank=True)
    old_add_qty=models.DecimalField('加码数量', null=True, blank=True, max_digits=6, decimal_places=2)
    old_discount=models.DecimalField('折扣', null=True, blank=True, max_digits=3, decimal_places=2)
    old_cloth_inspection=models.IntegerField('检验方法', null=True, blank=True)
    old_fact_id=models.CharField('工厂', null=True, blank=True, max_length=10)
    old_to_place=models.CharField('交货地点', null=True, blank=True, max_length=500)
    old_weft_density=models.DecimalField('纬密', null=True, blank=True, max_digits=6, decimal_places=2)
    old_warp_density=models.DecimalField('经密', null=True, blank=True, max_digits=6, decimal_places=2)
    old_take_fab_status=models.CharField('带纱状态', null=True, blank=True, max_length=1)
    old_linker_info=models.CharField('联系人信息', null=True, blank=True, max_length=100)
    old_loss=models.DecimalField('数值缩率', null=True, blank=True, max_digits=4, decimal_places=1)
    old_loss_str=models.CharField('文字缩率', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_invoice_kind=models.IntegerField('InvoiceKind', null=True, blank=True)
    old_addr_dlv=models.CharField('交货地址', null=True, blank=True, max_length=500)
    old_redo_reason_id=models.CharField('RedoReasonID', null=True, blank=True, max_length=500)
    old_is_finished=models.BooleanField('IsFinished', null=True, blank=True)
    old_prepare_sheet_no=models.CharField('计划单号', null=True, blank=True, max_length=50)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=20)
    old_print_code=models.CharField('印花', null=True, blank=True, max_length=50)
    old_bhd=models.BooleanField('备货单', null=True, blank=True)
    old_jia_gong=models.CharField('加工要求', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_ordermain'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_77170313981f59ca'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_77170313981f59ca')]
        verbose_name=verbose_name_plural='订单主表'
        ordering=["-id"]

class SourceDyeOrderPriceProcess(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='OrderPriceProcess'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'CheckNo': 'old_check_no', 'ProcessID': 'old_process_id', 'Price': 'old_price', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('SheetSeries', 'CheckNo', 'ProcessID')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_process_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_check_no=models.CharField('CheckNo', null=False, blank=True, max_length=20)
    old_process_id=models.CharField('ProcessID', null=False, blank=True, max_length=50)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=8, decimal_places=2)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=300)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_orderpriceprocess'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_check_no', 'old_process_id'],name='src_db2203ccfe7cc62c'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_check_no'))),Upper(RTrim(models.F('old_process_id'))),name='src_ci_db2203ccfe7cc62c')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（OrderPriceProcess，待确认）'
        ordering=["-id"]

class SourceDyeOrderProcess(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='OrderProcess'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'CheckNo': 'old_check_no', 'ProcessNo': 'old_process_no', 'ProcessID': 'old_process_id', 'StationID': 'old_station_id', 'MachineID': 'old_machine_id', 'PPName01': 'old_ppname01', 'TheoryValue01': 'old_theory_value01', 'PPName02': 'old_ppname02', 'TheoryValue02': 'old_theory_value02', 'PPName03': 'old_ppname03', 'TheoryValue03': 'old_theory_value03', 'PPName04': 'old_ppname04', 'TheoryValue04': 'old_theory_value04', 'PPName05': 'old_ppname05', 'TheoryValue05': 'old_theory_value05', 'PPName06': 'old_ppname06', 'TheoryValue06': 'old_theory_value06', 'PPName07': 'old_ppname07', 'TheoryValue07': 'old_theory_value07', 'PPName08': 'old_ppname08', 'TheoryValue08': 'old_theory_value08', 'PPName09': 'old_ppname09', 'TheoryValue09': 'old_theory_value09', 'PPName10': 'old_ppname10', 'TheoryValue10': 'old_theory_value10', 'PPName11': 'old_ppname11', 'TheoryValue11': 'old_theory_value11', 'PPName12': 'old_ppname12', 'TheoryValue12': 'old_theory_value12', 'PPName13': 'old_ppname13', 'TheoryValue13': 'old_theory_value13', 'PPName14': 'old_ppname14', 'TheoryValue14': 'old_theory_value14', 'PPName15': 'old_ppname15', 'TheoryValue15': 'old_theory_value15', 'PPName16': 'old_ppname16', 'TheoryValue16': 'old_theory_value16', 'PPName17': 'old_ppname17', 'TheoryValue17': 'old_theory_value17', 'PPName18': 'old_ppname18', 'TheoryValue18': 'old_theory_value18', 'PPName19': 'old_ppname19', 'TheoryValue19': 'old_theory_value19', 'PPName20': 'old_ppname20', 'TheoryValue20': 'old_theory_value20', 'Price': 'old_price', 'RecipeCheck': 'old_recipe_check', 'RecipeSeries': 'old_recipe_series'}
    SOURCE_KEY=('SheetSeries', 'CheckNo', 'ProcessNo')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_process_id': 'Chinese_PRC_CI_AS', 'old_station_id': 'Chinese_PRC_CI_AS', 'old_machine_id': 'Chinese_PRC_CI_AS', 'old_ppname01': 'Chinese_PRC_CI_AS', 'old_theory_value01': 'Chinese_PRC_CI_AS', 'old_ppname02': 'Chinese_PRC_CI_AS', 'old_theory_value02': 'Chinese_PRC_CI_AS', 'old_ppname03': 'Chinese_PRC_CI_AS', 'old_theory_value03': 'Chinese_PRC_CI_AS', 'old_ppname04': 'Chinese_PRC_CI_AS', 'old_theory_value04': 'Chinese_PRC_CI_AS', 'old_ppname05': 'Chinese_PRC_CI_AS', 'old_theory_value05': 'Chinese_PRC_CI_AS', 'old_ppname06': 'Chinese_PRC_CI_AS', 'old_theory_value06': 'Chinese_PRC_CI_AS', 'old_ppname07': 'Chinese_PRC_CI_AS', 'old_theory_value07': 'Chinese_PRC_CI_AS', 'old_ppname08': 'Chinese_PRC_CI_AS', 'old_theory_value08': 'Chinese_PRC_CI_AS', 'old_ppname09': 'Chinese_PRC_CI_AS', 'old_theory_value09': 'Chinese_PRC_CI_AS', 'old_ppname10': 'Chinese_PRC_CI_AS', 'old_theory_value10': 'Chinese_PRC_CI_AS', 'old_ppname11': 'Chinese_PRC_CI_AS', 'old_theory_value11': 'Chinese_PRC_CI_AS', 'old_ppname12': 'Chinese_PRC_CI_AS', 'old_theory_value12': 'Chinese_PRC_CI_AS', 'old_ppname13': 'Chinese_PRC_CI_AS', 'old_theory_value13': 'Chinese_PRC_CI_AS', 'old_ppname14': 'Chinese_PRC_CI_AS', 'old_theory_value14': 'Chinese_PRC_CI_AS', 'old_ppname15': 'Chinese_PRC_CI_AS', 'old_theory_value15': 'Chinese_PRC_CI_AS', 'old_ppname16': 'Chinese_PRC_CI_AS', 'old_theory_value16': 'Chinese_PRC_CI_AS', 'old_ppname17': 'Chinese_PRC_CI_AS', 'old_theory_value17': 'Chinese_PRC_CI_AS', 'old_ppname18': 'Chinese_PRC_CI_AS', 'old_theory_value18': 'Chinese_PRC_CI_AS', 'old_ppname19': 'Chinese_PRC_CI_AS', 'old_theory_value19': 'Chinese_PRC_CI_AS', 'old_ppname20': 'Chinese_PRC_CI_AS', 'old_theory_value20': 'Chinese_PRC_CI_AS', 'old_recipe_series': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：OrderColor', 'target': 'erp_sales.SourceDyeOrderColor', 'source_fields': ['SheetSeries', 'CheckNo'], 'target_fields': ['SheetSeries', 'CheckNo'], 'evidence': ['原界面主从 OrderProcessChange → OrderColorChange', '原界面主从 PrintOrderProcess → PrintOrderColor', '原界面主从 OrderProcess → OrderColor', '原界面主从 qry_GetOrderProcessToJob → qry_GetOrderColorToJob', '原界面主从 OrderProcessSup → OrderColorSup', '原界面主从 OrderProcessExtraChange → OrderColorChange', '原界面主从 OrderProcessExtra → OrderColor', '原界面主从 OrderProcessExtraSup → OrderColorSup']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_check_no=models.CharField('订单明细号', null=False, blank=True, max_length=20)
    old_process_no=models.IntegerField('工序号', null=False, blank=False)
    old_process_id=models.CharField('工序代码', null=False, blank=True, max_length=10)
    old_station_id=models.CharField('站别代码', null=True, blank=True, max_length=10)
    old_machine_id=models.CharField('机台号', null=True, blank=True, max_length=10)
    old_ppname01=models.CharField('参数名1', null=True, blank=True, max_length=20)
    old_theory_value01=models.CharField('设定值1', null=True, blank=True, max_length=20)
    old_ppname02=models.CharField('参数名2', null=True, blank=True, max_length=20)
    old_theory_value02=models.CharField('设定值2', null=True, blank=True, max_length=20)
    old_ppname03=models.CharField('参数名3', null=True, blank=True, max_length=20)
    old_theory_value03=models.CharField('设定值3', null=True, blank=True, max_length=20)
    old_ppname04=models.CharField('PPName04', null=True, blank=True, max_length=20)
    old_theory_value04=models.CharField('TheoryValue04', null=True, blank=True, max_length=20)
    old_ppname05=models.CharField('PPName05', null=True, blank=True, max_length=20)
    old_theory_value05=models.CharField('TheoryValue05', null=True, blank=True, max_length=20)
    old_ppname06=models.CharField('PPName06', null=True, blank=True, max_length=20)
    old_theory_value06=models.CharField('TheoryValue06', null=True, blank=True, max_length=20)
    old_ppname07=models.CharField('PPName07', null=True, blank=True, max_length=20)
    old_theory_value07=models.CharField('TheoryValue07', null=True, blank=True, max_length=20)
    old_ppname08=models.CharField('PPName08', null=True, blank=True, max_length=20)
    old_theory_value08=models.CharField('TheoryValue08', null=True, blank=True, max_length=20)
    old_ppname09=models.CharField('PPName09', null=True, blank=True, max_length=20)
    old_theory_value09=models.CharField('TheoryValue09', null=True, blank=True, max_length=20)
    old_ppname10=models.CharField('PPName10', null=True, blank=True, max_length=20)
    old_theory_value10=models.CharField('TheoryValue10', null=True, blank=True, max_length=20)
    old_ppname11=models.CharField('PPName11', null=True, blank=True, max_length=20)
    old_theory_value11=models.CharField('TheoryValue11', null=True, blank=True, max_length=20)
    old_ppname12=models.CharField('PPName12', null=True, blank=True, max_length=20)
    old_theory_value12=models.CharField('TheoryValue12', null=True, blank=True, max_length=20)
    old_ppname13=models.CharField('PPName13', null=True, blank=True, max_length=20)
    old_theory_value13=models.CharField('TheoryValue13', null=True, blank=True, max_length=20)
    old_ppname14=models.CharField('PPName14', null=True, blank=True, max_length=20)
    old_theory_value14=models.CharField('TheoryValue14', null=True, blank=True, max_length=20)
    old_ppname15=models.CharField('PPName15', null=True, blank=True, max_length=20)
    old_theory_value15=models.CharField('TheoryValue15', null=True, blank=True, max_length=20)
    old_ppname16=models.CharField('PPName16', null=True, blank=True, max_length=20)
    old_theory_value16=models.CharField('TheoryValue16', null=True, blank=True, max_length=20)
    old_ppname17=models.CharField('PPName17', null=True, blank=True, max_length=20)
    old_theory_value17=models.CharField('TheoryValue17', null=True, blank=True, max_length=20)
    old_ppname18=models.CharField('PPName18', null=True, blank=True, max_length=20)
    old_theory_value18=models.CharField('TheoryValue18', null=True, blank=True, max_length=20)
    old_ppname19=models.CharField('PPName19', null=True, blank=True, max_length=20)
    old_theory_value19=models.CharField('TheoryValue19', null=True, blank=True, max_length=20)
    old_ppname20=models.CharField('PPName20', null=True, blank=True, max_length=20)
    old_theory_value20=models.CharField('TheoryValue20', null=True, blank=True, max_length=20)
    old_price=models.DecimalField('另收费价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_recipe_check=models.BooleanField('工序配方审核', null=True, blank=True)
    old_recipe_series=models.CharField('工序配方流水号', null=True, blank=True, max_length=20)
    source_parent_1=models.ForeignKey('erp_sales.SourceDyeOrderColor', verbose_name='原关系：OrderColor', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_orderprocess'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_check_no', 'old_process_no'],name='src_02481e2fd24560fe'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_check_no'))),models.F('old_process_no'),name='src_ci_02481e2fd24560fe')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（OrderProcess，待确认）'
        ordering=["-id"]

class SourceDyeOrderProcessPre(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='OrderProcessPre'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'CheckNo': 'old_check_no', 'ProcessNo': 'old_process_no', 'ProcessID': 'old_process_id', 'StationID': 'old_station_id', 'Price': 'old_price', 'PPName01': 'old_ppname01', 'TheoryValue01': 'old_theory_value01', 'PPName02': 'old_ppname02', 'TheoryValue02': 'old_theory_value02', 'PPName03': 'old_ppname03', 'TheoryValue03': 'old_theory_value03', 'PPName04': 'old_ppname04', 'TheoryValue04': 'old_theory_value04', 'PPName05': 'old_ppname05', 'TheoryValue05': 'old_theory_value05', 'PPName06': 'old_ppname06', 'TheoryValue06': 'old_theory_value06', 'PPName07': 'old_ppname07', 'TheoryValue07': 'old_theory_value07', 'PPName08': 'old_ppname08', 'TheoryValue08': 'old_theory_value08', 'PPName09': 'old_ppname09', 'TheoryValue09': 'old_theory_value09', 'PPName10': 'old_ppname10', 'TheoryValue10': 'old_theory_value10', 'PPName11': 'old_ppname11', 'TheoryValue11': 'old_theory_value11', 'PPName12': 'old_ppname12', 'TheoryValue12': 'old_theory_value12', 'PPName13': 'old_ppname13', 'TheoryValue13': 'old_theory_value13', 'PPName14': 'old_ppname14', 'TheoryValue14': 'old_theory_value14', 'PPName15': 'old_ppname15', 'TheoryValue15': 'old_theory_value15', 'PPName16': 'old_ppname16', 'TheoryValue16': 'old_theory_value16', 'PPName17': 'old_ppname17', 'TheoryValue17': 'old_theory_value17', 'PPName18': 'old_ppname18', 'TheoryValue18': 'old_theory_value18', 'PPName19': 'old_ppname19', 'TheoryValue19': 'old_theory_value19', 'PPName20': 'old_ppname20', 'TheoryValue20': 'old_theory_value20', 'MachineID': 'old_machine_id', 'RecipeCheck': 'old_recipe_check', 'RecipeSeries': 'old_recipe_series', 'DetailNo': 'old_detail_no'}
    SOURCE_KEY=('SheetSeries', 'CheckNo', 'ProcessNo')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_process_id': 'Chinese_PRC_CI_AS', 'old_station_id': 'Chinese_PRC_CI_AS', 'old_ppname01': 'Chinese_PRC_CI_AS', 'old_theory_value01': 'Chinese_PRC_CI_AS', 'old_ppname02': 'Chinese_PRC_CI_AS', 'old_theory_value02': 'Chinese_PRC_CI_AS', 'old_ppname03': 'Chinese_PRC_CI_AS', 'old_theory_value03': 'Chinese_PRC_CI_AS', 'old_ppname04': 'Chinese_PRC_CI_AS', 'old_theory_value04': 'Chinese_PRC_CI_AS', 'old_ppname05': 'Chinese_PRC_CI_AS', 'old_theory_value05': 'Chinese_PRC_CI_AS', 'old_ppname06': 'Chinese_PRC_CI_AS', 'old_theory_value06': 'Chinese_PRC_CI_AS', 'old_ppname07': 'Chinese_PRC_CI_AS', 'old_theory_value07': 'Chinese_PRC_CI_AS', 'old_ppname08': 'Chinese_PRC_CI_AS', 'old_theory_value08': 'Chinese_PRC_CI_AS', 'old_ppname09': 'Chinese_PRC_CI_AS', 'old_theory_value09': 'Chinese_PRC_CI_AS', 'old_ppname10': 'Chinese_PRC_CI_AS', 'old_theory_value10': 'Chinese_PRC_CI_AS', 'old_ppname11': 'Chinese_PRC_CI_AS', 'old_theory_value11': 'Chinese_PRC_CI_AS', 'old_ppname12': 'Chinese_PRC_CI_AS', 'old_theory_value12': 'Chinese_PRC_CI_AS', 'old_ppname13': 'Chinese_PRC_CI_AS', 'old_theory_value13': 'Chinese_PRC_CI_AS', 'old_ppname14': 'Chinese_PRC_CI_AS', 'old_theory_value14': 'Chinese_PRC_CI_AS', 'old_ppname15': 'Chinese_PRC_CI_AS', 'old_theory_value15': 'Chinese_PRC_CI_AS', 'old_ppname16': 'Chinese_PRC_CI_AS', 'old_theory_value16': 'Chinese_PRC_CI_AS', 'old_ppname17': 'Chinese_PRC_CI_AS', 'old_theory_value17': 'Chinese_PRC_CI_AS', 'old_ppname18': 'Chinese_PRC_CI_AS', 'old_theory_value18': 'Chinese_PRC_CI_AS', 'old_ppname19': 'Chinese_PRC_CI_AS', 'old_theory_value19': 'Chinese_PRC_CI_AS', 'old_ppname20': 'Chinese_PRC_CI_AS', 'old_theory_value20': 'Chinese_PRC_CI_AS', 'old_machine_id': 'Chinese_PRC_CI_AS', 'old_recipe_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：OrderColor', 'target': 'erp_sales.SourceDyeOrderColor', 'source_fields': ['SheetSeries', 'CheckNo'], 'target_fields': ['SheetSeries', 'CheckNo'], 'evidence': ['原界面主从 PrintOrderProcessPre → PrintOrderColor', '原界面主从 OrderProcessPreSup → OrderColorSup']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('流水', null=False, blank=True, max_length=50)
    old_check_no=models.CharField('订单明细号', null=False, blank=True, max_length=20)
    old_process_no=models.IntegerField('工序号', null=False, blank=False)
    old_process_id=models.CharField('工序', null=True, blank=True, max_length=10)
    old_station_id=models.CharField('站别', null=True, blank=True, max_length=10)
    old_price=models.DecimalField('价格', null=True, blank=True, max_digits=10, decimal_places=4)
    old_ppname01=models.CharField('参数名1', null=True, blank=True, max_length=20)
    old_theory_value01=models.CharField('设定值1', null=True, blank=True, max_length=20)
    old_ppname02=models.CharField('参数名2', null=True, blank=True, max_length=20)
    old_theory_value02=models.CharField('设定值2', null=True, blank=True, max_length=20)
    old_ppname03=models.CharField('参数名3', null=True, blank=True, max_length=20)
    old_theory_value03=models.CharField('设定值3', null=True, blank=True, max_length=20)
    old_ppname04=models.CharField('参数名4', null=True, blank=True, max_length=20)
    old_theory_value04=models.CharField('设定值4', null=True, blank=True, max_length=20)
    old_ppname05=models.CharField('参数名5', null=True, blank=True, max_length=20)
    old_theory_value05=models.CharField('设定值5', null=True, blank=True, max_length=20)
    old_ppname06=models.CharField('参数名6', null=True, blank=True, max_length=20)
    old_theory_value06=models.CharField('设定值6', null=True, blank=True, max_length=20)
    old_ppname07=models.CharField('参数名7', null=True, blank=True, max_length=20)
    old_theory_value07=models.CharField('设定值7', null=True, blank=True, max_length=20)
    old_ppname08=models.CharField('参数名8', null=True, blank=True, max_length=20)
    old_theory_value08=models.CharField('设定值8', null=True, blank=True, max_length=20)
    old_ppname09=models.CharField('参数名9', null=True, blank=True, max_length=20)
    old_theory_value09=models.CharField('设定值9', null=True, blank=True, max_length=20)
    old_ppname10=models.CharField('参数名10', null=True, blank=True, max_length=20)
    old_theory_value10=models.CharField('设定值10', null=True, blank=True, max_length=20)
    old_ppname11=models.CharField('参数名11', null=True, blank=True, max_length=20)
    old_theory_value11=models.CharField('设定值11', null=True, blank=True, max_length=20)
    old_ppname12=models.CharField('参数名12', null=True, blank=True, max_length=20)
    old_theory_value12=models.CharField('设定值12', null=True, blank=True, max_length=20)
    old_ppname13=models.CharField('参数名13', null=True, blank=True, max_length=20)
    old_theory_value13=models.CharField('设定值13', null=True, blank=True, max_length=20)
    old_ppname14=models.CharField('参数名14', null=True, blank=True, max_length=20)
    old_theory_value14=models.CharField('设定值14', null=True, blank=True, max_length=20)
    old_ppname15=models.CharField('参数名15', null=True, blank=True, max_length=20)
    old_theory_value15=models.CharField('设定值15', null=True, blank=True, max_length=20)
    old_ppname16=models.CharField('参数名16', null=True, blank=True, max_length=20)
    old_theory_value16=models.CharField('设定值16', null=True, blank=True, max_length=20)
    old_ppname17=models.CharField('参数名17', null=True, blank=True, max_length=20)
    old_theory_value17=models.CharField('设定值17', null=True, blank=True, max_length=20)
    old_ppname18=models.CharField('参数名18', null=True, blank=True, max_length=20)
    old_theory_value18=models.CharField('设定值18', null=True, blank=True, max_length=20)
    old_ppname19=models.CharField('参数名19', null=True, blank=True, max_length=20)
    old_theory_value19=models.CharField('设定值19', null=True, blank=True, max_length=20)
    old_ppname20=models.CharField('参数名20', null=True, blank=True, max_length=20)
    old_theory_value20=models.CharField('设定值20', null=True, blank=True, max_length=20)
    old_machine_id=models.CharField('机台号', null=True, blank=True, max_length=10)
    old_recipe_check=models.BooleanField('工序配方审核', null=True, blank=True)
    old_recipe_series=models.CharField('配方流水号', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=True, blank=True, max_length=36)
    source_parent_1=models.ForeignKey('erp_sales.SourceDyeOrderColor', verbose_name='原关系：OrderColor', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_orderprocesspre'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_check_no', 'old_process_no'],name='src_ebff49b8652f92c1'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_check_no'))),models.F('old_process_no'),name='src_ci_ebff49b8652f92c1')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（OrderProcessPre，待确认）'
        ordering=["-id"]

class SourceDyePriceAdjust(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PriceAdjust'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetKind': 'old_sheet_kind', 'SheetDate': 'old_sheet_date', 'SheetStatus': 'old_sheet_status', 'DateType': 'old_date_type', 'StartDate': 'old_start_date', 'AdjustMoney': 'old_adjust_money', 'AdjustRatio': 'old_adjust_ratio', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'RightStatus': 'old_right_status'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_date_type': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('单据流水号', null=False, blank=True, max_length=50)
    old_sheet_no=models.CharField('单据编号', null=True, blank=True, max_length=36)
    old_sheet_kind=models.IntegerField('单据类别', null=True, blank=True)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_date_type=models.CharField('日期类型', null=True, blank=True, max_length=10)
    old_start_date=models.DateTimeField('实行日期', null=True, blank=True)
    old_adjust_money=models.DecimalField('调整金额', null=True, blank=True, max_digits=14, decimal_places=6)
    old_adjust_ratio=models.DecimalField('调整比例', null=True, blank=True, max_digits=8, decimal_places=4)
    old_creater=models.CharField('调价人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('调价日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_priceadjust'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_f9d0fc1865eaa04d'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_f9d0fc1865eaa04d')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（PriceAdjust，待确认）'
        ordering=["-id"]

class SourceDyePriceAdjustDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PriceAdjustDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'QuoteDetailNo': 'old_quote_detail_no', 'AdjustPrice': 'old_adjust_price', 'OldPrice': 'old_old_price', 'ColorNum': 'old_color_num', 'ColorID': 'old_color_id', 'ColorDepthID': 'old_color_depth_id', 'CustColorNum': 'old_cust_color_num', 'FlowMain': 'old_flow_main', 'CustSelfProduct': 'old_cust_self_product', 'ProdID': 'old_prod_id', 'CustomerID': 'old_customer_id', 'SheetDate': 'old_sheet_date', 'SheetNo': 'old_sheet_no', 'CustSelfProdCode': 'old_cust_self_prod_code', 'ProcessMemo': 'old_process_memo', 'FabricKindID': 'old_fabric_kind_id'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_quote_detail_no': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_depth_id': 'Chinese_PRC_CI_AS', 'old_cust_color_num': 'Chinese_PRC_CI_AS', 'old_flow_main': 'Chinese_PRC_CI_AS', 'old_cust_self_product': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_cust_self_prod_code': 'Chinese_PRC_CI_AS', 'old_process_memo': 'Chinese_PRC_CI_AS', 'old_fabric_kind_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：PriceAdjust', 'target': 'erp_sales.SourceDyePriceAdjust', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 PriceAdjustDetail → PriceAdjust']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('单据编号', null=False, blank=True, max_length=50)
    old_detail_no=models.CharField('明细编号', null=False, blank=True, max_length=36)
    old_quote_detail_no=models.CharField('报价单明细号', null=True, blank=True, max_length=50)
    old_adjust_price=models.DecimalField('调整后价格', null=True, blank=True, max_digits=16, decimal_places=4)
    old_old_price=models.DecimalField('调价前价格', null=True, blank=True, max_digits=16, decimal_places=4)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=50)
    old_color_depth_id=models.CharField('颜色深浅', null=True, blank=True, max_length=20)
    old_cust_color_num=models.CharField('客户色号', null=True, blank=True, max_length=20)
    old_flow_main=models.CharField('加工主流程', null=True, blank=True, max_length=50)
    old_cust_self_product=models.CharField('客户规格', null=True, blank=True, max_length=100)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=50)
    old_sheet_date=models.DateTimeField('报价日期', null=True, blank=True)
    old_sheet_no=models.CharField('报价单号', null=True, blank=True, max_length=50)
    old_cust_self_prod_code=models.CharField('客纱类编码', null=True, blank=True, max_length=100)
    old_process_memo=models.CharField('备注', null=True, blank=True, max_length=50)
    old_fabric_kind_id=models.CharField('类别', null=True, blank=True, max_length=10)
    source_parent_1=models.ForeignKey('erp_sales.SourceDyePriceAdjust', verbose_name='原关系：PriceAdjust', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_priceadjustdetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_3f947475361085f0'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_3f947475361085f0')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（PriceAdjustDetail，待确认）'
        ordering=["-id"]

class SourceDyeQuote(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='Quote'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'BusinessUnitID': 'old_business_unit_id', 'SheetKind': 'old_sheet_kind', 'SheetDate': 'old_sheet_date', 'QuoteKindID': 'old_quote_kind_id', 'SalerGroupID': 'old_saler_group_id', 'SalerID': 'old_saler_id', 'CustomerID': 'old_customer_id', 'Linker': 'old_linker', 'CurrencyID': 'old_currency_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Remarks': 'old_remarks', 'Revisions': 'old_revisions', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'SettleID': 'old_settle_id', 'ExchangeRate': 'old_exchange_rate', 'StepNo': 'old_step_no', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'IsConfirmed': 'old_is_confirmed', 'BeiZhu': 'old_bei_zhu', 'IsTax': 'old_is_tax', 'TaxRate': 'old_tax_rate', 'Tel': 'old_tel', 'CustomerCode': 'old_customer_code', 'LastTime': 'old_last_time'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_quote_kind_id': 'Chinese_PRC_CI_AS', 'old_saler_group_id': 'Chinese_PRC_CI_AS', 'old_saler_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_linker': 'Chinese_PRC_CI_AS', 'old_currency_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_settle_id': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_bei_zhu': 'Chinese_PRC_CI_AS', 'old_is_tax': 'Chinese_PRC_CI_AS', 'old_tel': 'Chinese_PRC_CI_AS', 'old_customer_code': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=False, blank=True, max_length=20)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_sheet_kind=models.IntegerField('单据类别', null=True, blank=True)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_quote_kind_id=models.CharField('报价类别', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('业务组别', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('业务员代码', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=10)
    old_linker=models.CharField('联系人', null=True, blank=True, max_length=10)
    old_currency_id=models.CharField('币别', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_settle_id=models.CharField('结算方式', null=True, blank=True, max_length=10)
    old_exchange_rate=models.DecimalField('汇率', null=True, blank=True, max_digits=10, decimal_places=2)
    old_step_no=models.IntegerField('工作流节点号', null=True, blank=True)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_is_confirmed=models.IntegerField('确价', null=True, blank=True)
    old_bei_zhu=models.CharField('BeiZhu', null=True, blank=True, max_length=150)
    old_is_tax=models.CharField('单价类别', null=True, blank=True, max_length=10)
    old_tax_rate=models.DecimalField('税率%', null=True, blank=True, max_digits=10, decimal_places=2)
    old_tel=models.CharField('Tel', null=True, blank=True, max_length=100)
    old_customer_code=models.CharField('客户全称', null=True, blank=True, max_length=50)
    old_last_time=models.DateTimeField('LastTime', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_quote'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_f78e30599ac76033'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_f78e30599ac76033')]
        verbose_name=verbose_name_plural='其他或待确认相关表（Quote，待确认）'
        ordering=["-id"]

class SourceDyeQuoteAtte(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='QuoteAtte'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'FieldType': 'old_field_type', 'AtteCode': 'old_atte_code', 'AtteValue': 'old_atte_value', 'PriceUnit': 'old_price_unit', 'Price': 'old_price', 'Description': 'old_description'}
    SOURCE_KEY=('SheetSeries', 'FieldType', 'AtteCode')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_field_type': 'Chinese_PRC_CI_AS', 'old_atte_code': 'Chinese_PRC_CI_AS', 'old_atte_value': 'Chinese_PRC_CI_AS', 'old_description': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：Quote', 'target': 'erp_sales.SourceDyeQuote', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 FixedPriceAtte → FixedPrice']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_field_type=models.CharField('基础数据类别', null=False, blank=True, max_length=20)
    old_atte_code=models.CharField('事项代码', null=False, blank=True, max_length=10)
    old_atte_value=models.CharField('事项内容', null=True, blank=True, max_length=50)
    old_price_unit=models.IntegerField('计价单位', null=True, blank=True)
    old_price=models.DecimalField('价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_description=models.CharField('描述', null=True, blank=True, max_length=100)
    source_parent_1=models.ForeignKey('erp_sales.SourceDyeQuote', verbose_name='原关系：Quote', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_quoteatte'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_field_type', 'old_atte_code'],name='src_9fdab6087578e786'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_field_type'))),Upper(RTrim(models.F('old_atte_code'))),name='src_ci_9fdab6087578e786')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（QuoteAtte，待确认）'
        ordering=["-id"]

class SourceDyeQuoteDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='QuoteDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'Spec': 'old_spec', 'Structure': 'old_structure', 'Width': 'old_width', 'Weight': 'old_weight', 'Price': 'old_price', 'PriceUnit': 'old_price_unit', 'Remarks': 'old_remarks', 'Loss': 'old_loss', 'ProdID': 'old_prod_id', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'MainStuffKindID': 'old_main_stuff_kind_id', 'ColorDepthID': 'old_color_depth_id', 'RecipePrice': 'old_recipe_price', 'ProcessMemo': 'old_process_memo', 'ProcessPrice': 'old_process_price', 'CustColorNum': 'old_cust_color_num', 'Pricesum': 'old_pricesum', 'CusPrice': 'old_cus_price', 'JobSheetNo': 'old_job_sheet_no', 'AdjustPrice': 'old_adjust_price', 'StartDate': 'old_start_date', 'DateType': 'old_date_type', 'IsConfirmed': 'old_is_confirmed', 'CustSelfProduct': 'old_cust_self_product', 'ColorNumNO': 'old_color_num_no', 'StuffDosage': 'old_stuff_dosage', 'DyePhaseName': 'old_dye_phase_name', 'GaoLaodu': 'old_gao_laodu', 'Note': 'old_note', 'Customer': 'old_customer', 'Photo': 'old_photo', 'StanPrice': 'old_stan_price', 'ConPrice': 'old_con_price', 'GradeID': 'old_grade_id', 'RightStatus': 'old_right_status', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'FixedSheetNo': 'old_fixed_sheet_no', 'YarnCategory': 'old_yarn_category', 'SumPrice': 'old_sum_price', 'SumChengBen': 'old_sum_cheng_ben', 'ChengBen0': 'old_cheng_ben0', 'ChengBen1': 'old_cheng_ben1', 'ChengBen2': 'old_cheng_ben2', 'ChengBen3': 'old_cheng_ben3', 'ChengBen4': 'old_cheng_ben4', 'ChengBen5': 'old_cheng_ben5'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_structure': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_main_stuff_kind_id': 'Chinese_PRC_CI_AS', 'old_color_depth_id': 'Chinese_PRC_CI_AS', 'old_process_memo': 'Chinese_PRC_CI_AS', 'old_cust_color_num': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_cust_self_product': 'Chinese_PRC_CI_AS', 'old_color_num_no': 'Chinese_PRC_CI_AS', 'old_dye_phase_name': 'Chinese_PRC_CI_AS', 'old_gao_laodu': 'Chinese_PRC_CI_AS', 'old_note': 'Chinese_PRC_CI_AS', 'old_customer': 'Chinese_PRC_CI_AS', 'old_grade_id': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_fixed_sheet_no': 'Chinese_PRC_CI_AS', 'old_yarn_category': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：Quote', 'target': 'erp_sales.SourceDyeQuote', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 FixedPriceDetail → FixedPrice']}]
    SOURCE_DEFAULTS={'old_sheet_series': ('literal', ''), 'old_spec': ('literal', ''), 'old_structure': ('literal', ''), 'old_width': ('literal', 0), 'old_weight': ('literal', 0), 'old_price': ('literal', 0), 'old_price_unit': ('literal', 0), 'old_remarks': ('literal', ''), 'old_loss': ('literal', 0)}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('表单明细号（子表）', null=False, blank=True, max_length=36)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=128)
    old_structure=models.CharField('组织', null=True, blank=True, max_length=50)
    old_width=models.DecimalField('幅宽', null=False, blank=False, max_digits=6, decimal_places=2)
    old_weight=models.DecimalField('克重', null=False, blank=False, max_digits=6, decimal_places=2)
    old_price=models.DecimalField('客确价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_price_unit=models.IntegerField('单位', null=False, blank=False)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_loss=models.DecimalField('数值缩率', null=True, blank=True, max_digits=4, decimal_places=1)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=20)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=50)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=20)
    old_main_stuff_kind_id=models.CharField('主染料类别', null=True, blank=True, max_length=10)
    old_color_depth_id=models.CharField('颜色深浅', null=True, blank=True, max_length=10)
    old_recipe_price=models.DecimalField('配方成本', null=True, blank=True, max_digits=8, decimal_places=2)
    old_process_memo=models.CharField('套价项目', null=True, blank=True, max_length=300)
    old_process_price=models.DecimalField('另计价', null=True, blank=True, max_digits=8, decimal_places=2)
    old_cust_color_num=models.CharField('客户色号', null=True, blank=True, max_length=100)
    old_pricesum=models.DecimalField('总单价', null=True, blank=True, max_digits=8, decimal_places=2)
    old_cus_price=models.DecimalField('对客报价', null=True, blank=True, max_digits=8, decimal_places=2)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=20)
    old_adjust_price=models.DecimalField('AdjustPrice', null=True, blank=True, max_digits=12, decimal_places=2)
    old_start_date=models.DateTimeField('调价实行日期', null=True, blank=True)
    old_date_type=models.IntegerField('调价日期类型', null=True, blank=True)
    old_is_confirmed=models.IntegerField('是否确价', null=True, blank=True)
    old_cust_self_product=models.CharField('客户规格', null=True, blank=True, max_length=32)
    old_color_num_no=models.CharField('确版号', null=True, blank=True, max_length=10)
    old_stuff_dosage=models.FloatField('染料用量', null=True, blank=True)
    old_dye_phase_name=models.CharField('染色工艺', null=True, blank=True, max_length=100)
    old_gao_laodu=models.CharField('高牢度', null=True, blank=True, max_length=100)
    old_note=models.CharField('配方', null=True, blank=True, max_length=1000)
    old_customer=models.CharField('客户', null=True, blank=True, max_length=50)
    old_photo=models.BinaryField('Photo', null=True, blank=True, editable=True)
    old_stan_price=models.DecimalField('标准单价', null=True, blank=True, max_digits=9, decimal_places=2)
    old_con_price=models.DecimalField('参考单价', null=True, blank=True, max_digits=9, decimal_places=2)
    old_grade_id=models.CharField('色号等级', null=True, blank=True, max_length=20)
    old_right_status=models.IntegerField('审核', null=True, blank=True)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=50)
    old_fixed_sheet_no=models.CharField('报价单号', null=True, blank=True, max_length=50)
    old_yarn_category=models.CharField('YarnCategory', null=True, blank=True, max_length=50)
    old_sum_price=models.DecimalField('SumPrice', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sum_cheng_ben=models.DecimalField('SumChengBen', null=True, blank=True, max_digits=6, decimal_places=2)
    old_cheng_ben0=models.DecimalField('ChengBen0', null=True, blank=True, max_digits=6, decimal_places=2)
    old_cheng_ben1=models.DecimalField('ChengBen1', null=True, blank=True, max_digits=6, decimal_places=2)
    old_cheng_ben2=models.DecimalField('ChengBen2', null=True, blank=True, max_digits=6, decimal_places=2)
    old_cheng_ben3=models.DecimalField('ChengBen3', null=True, blank=True, max_digits=6, decimal_places=2)
    old_cheng_ben4=models.DecimalField('ChengBen4', null=True, blank=True, max_digits=6, decimal_places=2)
    old_cheng_ben5=models.DecimalField('ChengBen5', null=True, blank=True, max_digits=6, decimal_places=2)
    source_parent_1=models.ForeignKey('erp_sales.SourceDyeQuote', verbose_name='原关系：Quote', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_quotedetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_34943f6dfd3f927c'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_34943f6dfd3f927c')]
        verbose_name=verbose_name_plural='其他或待确认相关表（QuoteDetail，待确认）'
        ordering=["-id"]

class SourceDyeQuoteItemPrice(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='QuoteItemPrice'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'Price': 'old_price', 'Unit': 'old_unit', 'RightStatus': 'old_right_status', 'Remarks': 'old_remarks', 'Item': 'old_item', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'IsConfirmed': 'old_is_confirmed', 'FabricKindID': 'old_fabric_kind_id'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_unit': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_item': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_fabric_kind_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：FixedPrice', 'target': 'erp_sales.SourceDyeFixedPrice', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 QuoteItemPrice → Quote']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=False, blank=True, max_length=30)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=20)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=100)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=6, decimal_places=1)
    old_unit=models.CharField('Unit', null=True, blank=True, max_length=20)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=100)
    old_item=models.CharField('Item', null=True, blank=True, max_length=50)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=50)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=50)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=50)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_is_confirmed=models.IntegerField('IsConfirmed', null=True, blank=True)
    old_fabric_kind_id=models.CharField('胚纱类别', null=True, blank=True, max_length=50)
    source_parent_1=models.ForeignKey('erp_sales.SourceDyeFixedPrice', verbose_name='原关系：FixedPrice', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_quoteitemprice'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_c5767ae44e278655'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_c5767ae44e278655')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（QuoteItemPrice，待确认）'
        ordering=["-id"]

class SourceDyeQuotePriceAtte(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='QuotePriceAtte'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'FieldType': 'old_field_type', 'AtteCode': 'old_atte_code', 'AtteValue': 'old_atte_value', 'PriceUnit': 'old_price_unit', 'Price': 'old_price', 'Description': 'old_description', 'DetailNo': 'old_detail_no'}
    SOURCE_KEY=('SheetSeries', 'FieldType', 'AtteCode', 'DetailNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_field_type': 'Chinese_PRC_CI_AS', 'old_atte_code': 'Chinese_PRC_CI_AS', 'old_atte_value': 'Chinese_PRC_CI_AS', 'old_description': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_field_type=models.CharField('FieldType', null=False, blank=True, max_length=20)
    old_atte_code=models.CharField('AtteCode', null=False, blank=True, max_length=10)
    old_atte_value=models.CharField('AtteValue', null=True, blank=True, max_length=500)
    old_price_unit=models.IntegerField('PriceUnit', null=True, blank=True)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=8, decimal_places=2)
    old_description=models.CharField('Description', null=True, blank=True, max_length=500)
    old_detail_no=models.CharField('DetailNo', null=False, blank=True, max_length=30)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_quotepriceatte'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_field_type', 'old_atte_code', 'old_detail_no'],name='src_39217312641c7ee9'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_field_type'))),Upper(RTrim(models.F('old_atte_code'))),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_39217312641c7ee9')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（QuotePriceAtte，待确认）'
        ordering=["-id"]

class SourceDyeQuotePriceProcess(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='QuotePriceProcess'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'ProcessID': 'old_process_id', 'Price': 'old_price', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('SheetSeries', 'DetailNo', 'ProcessID')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_process_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：Quote', 'target': 'erp_sales.SourceDyeQuote', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 FixedPriceProcess → FixedPrice']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号(子表)', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('表单明细号', null=False, blank=True, max_length=36)
    old_process_id=models.CharField('工序', null=False, blank=True, max_length=50)
    old_price=models.DecimalField('价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=300)
    source_parent_1=models.ForeignKey('erp_sales.SourceDyeQuote', verbose_name='原关系：Quote', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_quotepriceprocess'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no', 'old_process_id'],name='src_883c005377816950'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),Upper(RTrim(models.F('old_process_id'))),name='src_ci_883c005377816950')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（QuotePriceProcess，待确认）'
        ordering=["-id"]

class SourceDyeRCORDERCOLOR(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='RCORDERCOLOR'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'ProdID': 'old_prod_id', 'CustFabricName': 'old_cust_fabric_name', 'ColorNum': 'old_color_num', 'ColorID': 'old_color_id', 'CustColorNum': 'old_cust_color_num', 'Width': 'old_width', 'WidthUnit': 'old_width_unit', 'Weight': 'old_weight', 'WeightKindID': 'old_weight_kind_id', 'OrderRolls': 'old_order_rolls', 'TubeWeight': 'old_tube_weight', 'AddWeigth': 'old_add_weigth', 'DlvDate': 'old_dlv_date', 'CustSelfNo': 'old_cust_self_no'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_cust_fabric_name': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_cust_color_num': 'Chinese_PRC_CI_AS', 'old_width': 'Chinese_PRC_CI_AS', 'old_width_unit': 'Chinese_PRC_CI_AS', 'old_weight': 'Chinese_PRC_CI_AS', 'old_weight_kind_id': 'Chinese_PRC_CI_AS', 'old_cust_self_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('SheetSeries', null=True, blank=True, max_length=20)
    old_prod_id=models.CharField('ProdID', null=True, blank=True, max_length=20)
    old_cust_fabric_name=models.CharField('CustFabricName', null=True, blank=True, max_length=250)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=20)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=150)
    old_cust_color_num=models.CharField('CustColorNum', null=True, blank=True, max_length=20)
    old_width=models.CharField('Width', null=True, blank=True, max_length=200)
    old_width_unit=models.CharField('WidthUnit', null=True, blank=True, max_length=20)
    old_weight=models.CharField('Weight', null=True, blank=True, max_length=200)
    old_weight_kind_id=models.CharField('WeightKindID', null=True, blank=True, max_length=20)
    old_order_rolls=models.DecimalField('OrderRolls', null=True, blank=True, max_digits=10, decimal_places=2)
    old_tube_weight=models.FloatField('TubeWeight', null=True, blank=True)
    old_add_weigth=models.FloatField('AddWeigth', null=True, blank=True)
    old_dlv_date=models.DateTimeField('DlvDate', null=True, blank=True)
    old_cust_self_no=models.CharField('CustSelfNo', null=True, blank=True, max_length=500)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_rcordercolor'
        indexes=[]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（RCORDERCOLOR，待确认）'
        ordering=["-id"]

class SourceDyeRCORDERMAIN(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='RCORDERMAIN'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'CustSelfNo': 'old_cust_self_no', 'Remarks': 'old_remarks'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_cust_self_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('SheetSeries', null=True, blank=True, max_length=20)
    old_cust_self_no=models.CharField('CustSelfNo', null=True, blank=True, max_length=500)
    old_remarks=models.TextField('Remarks', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_rcordermain'
        indexes=[]
        verbose_name=verbose_name_plural='客户订单与销售相关表（RCORDERMAIN，待确认）'
        ordering=["-id"]

class SourceDyeZDAddPrice(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ZDAddPrice'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'CustomerID': 'old_customer_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=30)
    old_sheet_no=models.CharField('表单号', null=True, blank=True, max_length=30)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approve_date=models.DateTimeField('审核日期', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_zdaddprice'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_9eedf422f6306148'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_9eedf422f6306148')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（ZDAddPrice，待确认）'
        ordering=["-id"]

class SourceDyeZDAddPriceDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ZDAddPriceDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'ProdID': 'old_prod_id', 'ColorDepthID': 'old_color_depth_id', 'Price': 'old_price', 'PriceUnit': 'old_price_unit', 'Remarks1': 'old_remarks1', 'Remarks2': 'old_remarks2'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_color_depth_id': 'Chinese_PRC_CI_AS', 'old_remarks1': 'Chinese_PRC_CI_AS', 'old_remarks2': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：ZDAddPrice', 'target': 'erp_sales.SourceDyeZDAddPrice', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 ZDAddPriceDetail → ZDAddPrice']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单号', null=True, blank=True, max_length=30)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=30)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=30)
    old_color_depth_id=models.CharField('颜色深浅', null=True, blank=True, max_length=30)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price_unit=models.IntegerField('报价单位', null=True, blank=True)
    old_remarks1=models.CharField('备注1', null=True, blank=True, max_length=512)
    old_remarks2=models.CharField('备注2', null=True, blank=True, max_length=512)
    source_parent_1=models.ForeignKey('erp_sales.SourceDyeZDAddPrice', verbose_name='原关系：ZDAddPrice', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_zdaddpricedetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_92921be510974f12'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_92921be510974f12')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（ZDAddPriceDetail，待确认）'
        ordering=["-id"]
