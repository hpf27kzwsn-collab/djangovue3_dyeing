"""静态旧业务字段；由tools/legacy_models生成，逐表来源见source_catalog.json。"""
from django.db import models
from django.db.models.functions import Upper,RTrim
from plugins.erp_base.source_documents import SourceRecord


class SourceDboProdin1029(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='prodin1029'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'JobSheetNo': 'old_job_sheet_no', 'SheetDate': 'old_sheet_date', 'CustomerID': 'old_customer_id', 'StockUnit': 'old_stock_unit', 'ProdID': 'old_prod_id', 'FabricID': 'old_fabric_id', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'CustColorNum': 'old_cust_color_num', 'Spec': 'old_spec', 'StorageUnitID': 'old_storage_unit_id', 'Area': 'old_area', 'SumRolls': 'old_sum_rolls', 'SumWeightQty': 'old_sum_weight_qty', 'SumGaryWeight': 'old_sum_gary_weight', 'SumLengthQty': 'old_sum_length_qty', 'AtteFee': 'old_atte_fee', 'VatFee': 'old_vat_fee', 'Width': 'old_width', 'Weight': 'old_weight', 'BarCode': 'old_bar_code', 'RollNo': 'old_roll_no', 'GrayQty': 'old_gray_qty', 'WeightQty': 'old_weight_qty', 'LengthQty': 'old_length_qty'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_fabric_id': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_cust_color_num': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_storage_unit_id': 'Chinese_PRC_CI_AS', 'old_area': 'Chinese_PRC_CI_AS', 'old_bar_code': 'Chinese_PRC_CI_AS', 'old_roll_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('SheetSeries', null=True, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=10)
    old_stock_unit=models.IntegerField('StockUnit', null=True, blank=True)
    old_prod_id=models.CharField('ProdID', null=True, blank=True, max_length=250)
    old_fabric_id=models.CharField('FabricID', null=True, blank=True, max_length=250)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=150)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=20)
    old_cust_color_num=models.CharField('CustColorNum', null=True, blank=True, max_length=100)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=128)
    old_storage_unit_id=models.CharField('StorageUnitID', null=True, blank=True, max_length=10)
    old_area=models.CharField('Area', null=True, blank=True, max_length=100)
    old_sum_rolls=models.DecimalField('SumRolls', null=True, blank=True, max_digits=7, decimal_places=2)
    old_sum_weight_qty=models.DecimalField('SumWeightQty', null=True, blank=True, max_digits=10, decimal_places=1)
    old_sum_gary_weight=models.DecimalField('SumGaryWeight', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sum_length_qty=models.DecimalField('SumLengthQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_atte_fee=models.DecimalField('AtteFee', null=True, blank=True, max_digits=10, decimal_places=2)
    old_vat_fee=models.DecimalField('VatFee', null=True, blank=True, max_digits=10, decimal_places=2)
    old_width=models.DecimalField('Width', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight=models.DecimalField('Weight', null=True, blank=True, max_digits=10, decimal_places=2)
    old_bar_code=models.CharField('BarCode', null=False, blank=True, max_length=50)
    old_roll_no=models.CharField('RollNo', null=True, blank=True, max_length=20)
    old_gray_qty=models.DecimalField('GrayQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('WeightQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_length_qty=models.DecimalField('LengthQty', null=True, blank=True, max_digits=10, decimal_places=2)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_prodin1029'
        indexes=[]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（prodin1029，待确认）'
        ordering=["-id"]

class SourceDyeAProdRecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='A_ProdRecord'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'Row1': 'old_row1', 'Row3': 'old_row3', 'Rolls': 'old_rolls'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('SheetSeries', null=True, blank=True, max_length=30)
    old_detail_no=models.CharField('DetailNo', null=True, blank=True, max_length=30)
    old_row1=models.IntegerField('Row1', null=True, blank=True)
    old_row3=models.BigIntegerField('Row3', null=True, blank=True)
    old_rolls=models.IntegerField('Rolls', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_a_prodrecord'
        indexes=[]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（A_ProdRecord，待确认）'
        ordering=["-id"]

class SourceDyeArticleDeptApply(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ArticleDeptApply'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'RightStatus': 'old_right_status'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
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
        db_table='src_dye_articledeptapply'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_d9a652328869012d'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_d9a652328869012d')]
        verbose_name=verbose_name_plural='其他或待确认相关表（ArticleDeptApply，待确认）'
        ordering=["-id"]

class SourceDyeArticleDeptApplyDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ArticleDeptApplyDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'DeptSheetNo': 'old_dept_sheet_no', 'Name': 'old_name', 'ArticleID': 'old_article_id', 'ArticleKindID': 'old_article_kind_id', 'Unit': 'old_unit', 'Qty': 'old_qty', 'Amount': 'old_amount', 'Remarks': 'old_remarks', 'DeptID': 'old_dept_id', 'ApplySheetNo': 'old_apply_sheet_no'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_dept_sheet_no': 'Chinese_PRC_CI_AS', 'old_name': 'Chinese_PRC_CI_AS', 'old_article_id': 'Chinese_PRC_CI_AS', 'old_article_kind_id': 'Chinese_PRC_CI_AS', 'old_unit': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_dept_id': 'Chinese_PRC_CI_AS', 'old_apply_sheet_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=False, blank=True, max_length=20)
    old_dept_sheet_no=models.CharField('DeptSheetNo', null=True, blank=True, max_length=30)
    old_name=models.CharField('Name', null=True, blank=True, max_length=50)
    old_article_id=models.CharField('ArticleID', null=True, blank=True, max_length=30)
    old_article_kind_id=models.CharField('ArticleKindID', null=True, blank=True, max_length=30)
    old_unit=models.CharField('Unit', null=True, blank=True, max_length=40)
    old_qty=models.DecimalField('Qty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_amount=models.DecimalField('Amount', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_dept_id=models.CharField('DeptID', null=True, blank=True, max_length=30)
    old_apply_sheet_no=models.CharField('ApplySheetNo', null=True, blank=True, max_length=40)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_articledeptapplydetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_308a57b83ddf18fe'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_308a57b83ddf18fe')]
        verbose_name=verbose_name_plural='其他或待确认相关表（ArticleDeptApplyDetail，待确认）'
        ordering=["-id"]

class SourceDyeArticleIn(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ArticleIn'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'InKindID': 'old_in_kind_id', 'BuyerID': 'old_buyer_id', 'WareHouseID': 'old_ware_house_id', 'SupplierID': 'old_supplier_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'StepNo': 'old_step_no', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'BusinessUnitID': 'old_business_unit_id', 'Keeper': 'old_keeper', 'Reason': 'old_reason', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'Settle': 'old_settle', 'deliverynum': 'old_deliverynum', 'APMoney': 'old_apmoney', 'APQty': 'old_apqty', 'UnClearQty': 'old_un_clear_qty', 'UnClearMoney': 'old_un_clear_money', 'UnClearInvoiceQty': 'old_un_clear_invoice_qty', 'UnClearInvoiceMoney': 'old_un_clear_invoice_money', 'DiscountMoney': 'old_discount_money', 'SumAmount': 'old_sum_amount', 'InvoiceClearStatus': 'old_invoice_clear_status', 'MoneyClearStatus': 'old_money_clear_status', 'DeptID': 'old_dept_id', 'FactID': 'old_fact_id', 'invoice': 'old_invoice'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_in_kind_id': 'Chinese_PRC_CI_AS', 'old_buyer_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_supplier_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_keeper': 'Chinese_PRC_CI_AS', 'old_reason': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_settle': 'Chinese_PRC_CI_AS', 'old_deliverynum': 'Chinese_PRC_CI_AS', 'old_dept_id': 'Chinese_PRC_CI_AS', 'old_fact_id': 'Chinese_PRC_CI_AS', 'old_invoice': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_in_kind_id=models.CharField('入库类别', null=True, blank=True, max_length=10)
    old_buyer_id=models.CharField('业务员', null=True, blank=True, max_length=50)
    old_ware_house_id=models.CharField('仓库代码', null=True, blank=True, max_length=10)
    old_supplier_id=models.CharField('供应商代码', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_step_no=models.IntegerField('流程节点号', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_keeper=models.CharField('仓管员', null=True, blank=True, max_length=10)
    old_reason=models.CharField('Reason', null=True, blank=True, max_length=256)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_settle=models.CharField('Settle', null=True, blank=True, max_length=50)
    old_deliverynum=models.CharField('deliverynum', null=True, blank=True, max_length=50)
    old_apmoney=models.DecimalField('APMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_apqty=models.DecimalField('APQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_un_clear_qty=models.DecimalField('UnClearQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_un_clear_money=models.DecimalField('UnClearMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_un_clear_invoice_qty=models.DecimalField('UnClearInvoiceQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_un_clear_invoice_money=models.DecimalField('UnClearInvoiceMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_discount_money=models.DecimalField('DiscountMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sum_amount=models.DecimalField('SumAmount', null=True, blank=True, max_digits=10, decimal_places=2)
    old_invoice_clear_status=models.IntegerField('InvoiceClearStatus', null=True, blank=True)
    old_money_clear_status=models.IntegerField('MoneyClearStatus', null=True, blank=True)
    old_dept_id=models.CharField('部门', null=True, blank=True, max_length=50)
    old_fact_id=models.CharField('所属分厂', null=True, blank=True, max_length=50)
    old_invoice=models.CharField('invoice', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_articlein'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_c110dbf537133bdd'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_c110dbf537133bdd')]
        verbose_name=verbose_name_plural='辅料入库单'
        ordering=["-id"]

class SourceDyeArticleInDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ArticleInDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'ArticleID': 'old_article_id', 'ArticleKindID': 'old_article_kind_id', 'Spec': 'old_spec', 'InQty': 'old_in_qty', 'Price': 'old_price', 'TaxRate': 'old_tax_rate', 'TaxPrice': 'old_tax_price', 'TaxMoney': 'old_tax_money', 'Total': 'old_total', 'PurDetailNo': 'old_pur_detail_no', 'APDetailNo': 'old_apdetail_no', 'InvoiceNo': 'old_invoice_no', 'FactDlvNo': 'old_fact_dlv_no', 'Remarks': 'old_remarks', 'PackQty': 'old_pack_qty', 'PackUnit': 'old_pack_unit', 'Discount': 'old_discount', 'DiscountMoney': 'old_discount_money', 'OriDetailNo': 'old_ori_detail_no', 'Amount': 'old_amount', 'StorageUnitIDs': 'old_storage_unit_ids', 'batch': 'old_batch'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_article_id': 'Chinese_PRC_CI_AS', 'old_article_kind_id': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_pur_detail_no': 'Chinese_PRC_CI_AS', 'old_apdetail_no': 'Chinese_PRC_CI_AS', 'old_invoice_no': 'Chinese_PRC_CI_AS', 'old_fact_dlv_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_pack_unit': 'Chinese_PRC_CI_AS', 'old_ori_detail_no': 'Chinese_PRC_CI_AS', 'old_storage_unit_ids': 'Chinese_PRC_CI_AS', 'old_batch': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：ArticleIn', 'target': 'erp_warehouse.SourceDyeArticleIn', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 FabricArticleInDetail → FabricArticleIn', '原界面主从 ArticleInDetail → ArticleIn']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('表单明细号（子表）', null=False, blank=True, max_length=36)
    old_article_id=models.CharField('物料编码', null=True, blank=True, max_length=200)
    old_article_kind_id=models.CharField('物料种类', null=True, blank=True, max_length=20)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=100)
    old_in_qty=models.DecimalField('入库数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=16, decimal_places=6)
    old_tax_rate=models.DecimalField('税率', null=True, blank=True, max_digits=4, decimal_places=2)
    old_tax_price=models.DecimalField('含税价', null=True, blank=True, max_digits=16, decimal_places=6)
    old_tax_money=models.DecimalField('税金', null=True, blank=True, max_digits=10, decimal_places=2)
    old_total=models.DecimalField('合计', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pur_detail_no=models.CharField('采购单明细号', null=True, blank=True, max_length=20)
    old_apdetail_no=models.CharField('应付单细号', null=True, blank=True, max_length=20)
    old_invoice_no=models.CharField('发票号码', null=True, blank=True, max_length=30)
    old_fact_dlv_no=models.CharField('送货单号', null=True, blank=True, max_length=80)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_pack_qty=models.DecimalField('包装数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pack_unit=models.CharField('PackUnit', null=True, blank=True, max_length=10)
    old_discount=models.DecimalField('Discount', null=True, blank=True, max_digits=3, decimal_places=2)
    old_discount_money=models.DecimalField('DiscountMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_ori_detail_no=models.CharField('OriDetailNo', null=True, blank=True, max_length=36)
    old_amount=models.DecimalField('不含税金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_storage_unit_ids=models.CharField('货区', null=True, blank=True, max_length=50)
    old_batch=models.CharField('批次', null=True, blank=True, max_length=250)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeArticleIn', verbose_name='原关系：ArticleIn', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_articleindetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_577555f5b7fb1708'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_577555f5b7fb1708')]
        verbose_name=verbose_name_plural='辅料入库明细'
        ordering=["-id"]

class SourceDyeArticleOut(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ArticleOut'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'WareHouseID': 'old_ware_house_id', 'ProjectNo': 'old_project_no', 'EmpID': 'old_emp_id', 'OutKindID': 'old_out_kind_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'StepNo': 'old_step_no', 'BusinessUnitID': 'old_business_unit_id', 'DeptID': 'old_dept_id', 'UseID': 'old_use_id', 'CustomerID': 'old_customer_id', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'SupplierID': 'old_supplier_id', 'leaders': 'old_leaders', 'purpose': 'old_purpose', 'FactID': 'old_fact_id'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_project_no': 'Chinese_PRC_CI_AS', 'old_emp_id': 'Chinese_PRC_CI_AS', 'old_out_kind_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_dept_id': 'Chinese_PRC_CI_AS', 'old_use_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_supplier_id': 'Chinese_PRC_CI_AS', 'old_leaders': 'Chinese_PRC_CI_AS', 'old_purpose': 'Chinese_PRC_CI_AS', 'old_fact_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_ware_house_id=models.CharField('仓库代码', null=True, blank=True, max_length=10)
    old_project_no=models.CharField('项目', null=True, blank=True, max_length=20)
    old_emp_id=models.CharField('员工编号', null=True, blank=True, max_length=10)
    old_out_kind_id=models.CharField('出库类型', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_step_no=models.IntegerField('流程节点号', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_dept_id=models.CharField('部门编码', null=True, blank=True, max_length=10)
    old_use_id=models.CharField('用途', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户代码', null=True, blank=True, max_length=10)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_supplier_id=models.CharField('SupplierID', null=True, blank=True, max_length=10)
    old_leaders=models.CharField('领用人', null=True, blank=True, max_length=50)
    old_purpose=models.CharField('用途', null=True, blank=True, max_length=500)
    old_fact_id=models.CharField('所属分厂', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_articleout'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_e3022bdb2fbd5b44'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_e3022bdb2fbd5b44')]
        verbose_name=verbose_name_plural='辅料出库单'
        ordering=["-id"]

class SourceDyeArticleOutApply(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ArticleOutApply'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'Applyer': 'old_applyer', 'ApplyDept': 'old_apply_dept', 'ApplyFactory': 'old_apply_factory', 'SheetDate': 'old_sheet_date', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'Remarks': 'old_remarks', 'UseInfo': 'old_use_info'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_applyer': 'Chinese_PRC_CI_AS', 'old_apply_dept': 'Chinese_PRC_CI_AS', 'old_apply_factory': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_use_info': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
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
        db_table='src_dye_articleoutapply'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_a49f6fe152966950'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_a49f6fe152966950')]
        verbose_name=verbose_name_plural='其他或待确认相关表（ArticleOutApply，待确认）'
        ordering=["-id"]

class SourceDyeArticleOutApplyDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ArticleOutApplyDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'Name': 'old_name', 'ArticleID': 'old_article_id', 'ArticleKindID': 'old_article_kind_id', 'Spec': 'old_spec', 'Unit': 'old_unit', 'Qty': 'old_qty', 'Amount': 'old_amount', 'Price': 'old_price', 'Remarks': 'old_remarks', 'StorageUnitIDs': 'old_storage_unit_ids', 'KCQty': 'old_kcqty'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_name': 'Chinese_PRC_CI_AS', 'old_article_id': 'Chinese_PRC_CI_AS', 'old_article_kind_id': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_unit': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_storage_unit_ids': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=False, blank=True, max_length=20)
    old_name=models.CharField('Name', null=True, blank=True, max_length=50)
    old_article_id=models.CharField('ArticleID', null=True, blank=True, max_length=30)
    old_article_kind_id=models.CharField('ArticleKindID', null=True, blank=True, max_length=30)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=100)
    old_unit=models.CharField('Unit', null=True, blank=True, max_length=40)
    old_qty=models.DecimalField('Qty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_amount=models.DecimalField('Amount', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_storage_unit_ids=models.CharField('StorageUnitIDs', null=True, blank=True, max_length=20)
    old_kcqty=models.DecimalField('KCQty', null=True, blank=True, max_digits=10, decimal_places=2)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_articleoutapplydetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_9b486388bacde7d1'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_9b486388bacde7d1')]
        verbose_name=verbose_name_plural='其他或待确认相关表（ArticleOutApplyDetail，待确认）'
        ordering=["-id"]

class SourceDyeArticleOutDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ArticleOutDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'ArticleID': 'old_article_id', 'ArticleKindID': 'old_article_kind_id', 'MachineID': 'old_machine_id', 'OutQty': 'old_out_qty', 'Price': 'old_price', 'Total': 'old_total', 'InDetailNo': 'old_in_detail_no', 'Remarks': 'old_remarks', 'ProjectNo': 'old_project_no', 'SupplierID': 'old_supplier_id', 'EmpID': 'old_emp_id', 'StorageUnitIDs': 'old_storage_unit_ids', 'Spec': 'old_spec'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_article_id': 'Chinese_PRC_CI_AS', 'old_article_kind_id': 'Chinese_PRC_CI_AS', 'old_machine_id': 'Chinese_PRC_CI_AS', 'old_in_detail_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_project_no': 'Chinese_PRC_CI_AS', 'old_supplier_id': 'Chinese_PRC_CI_AS', 'old_emp_id': 'Chinese_PRC_CI_AS', 'old_storage_unit_ids': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：ArticleOut', 'target': 'erp_warehouse.SourceDyeArticleOut', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 FabricArticleOutDetail → FabricArticleOut', '原界面主从 ArticleOutDetail → ArticleOut']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('表单明细号（子表）', null=False, blank=True, max_length=36)
    old_article_id=models.CharField('物料编码', null=True, blank=True, max_length=20)
    old_article_kind_id=models.CharField('物料种类', null=True, blank=True, max_length=20)
    old_machine_id=models.CharField('机台号', null=True, blank=True, max_length=10)
    old_out_qty=models.DecimalField('出库数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=16, decimal_places=6)
    old_total=models.DecimalField('合计', null=True, blank=True, max_digits=10, decimal_places=2)
    old_in_detail_no=models.CharField('入库单明细号', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('明细备注', null=True, blank=True, max_length=512)
    old_project_no=models.CharField('工程项目', null=True, blank=True, max_length=20)
    old_supplier_id=models.CharField('SupplierID', null=True, blank=True, max_length=20)
    old_emp_id=models.CharField('领用人', null=True, blank=True, max_length=10)
    old_storage_unit_ids=models.CharField('货区', null=True, blank=True, max_length=50)
    old_spec=models.CharField('供应商来货名称', null=True, blank=True, max_length=100)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeArticleOut', verbose_name='原关系：ArticleOut', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_articleoutdetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_ebcb5d1bfcbf544b'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_ebcb5d1bfcbf544b')]
        verbose_name=verbose_name_plural='辅料出库明细'
        ordering=["-id"]

class SourceDyeArticleStock(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ArticleStock'
    SOURCE_FIELDS={'StockDate': 'old_stock_date', 'ArticleKindID': 'old_article_kind_id', 'ArticleID': 'old_article_id', 'WareHouseID': 'old_ware_house_id', 'PreMonthQty': 'old_pre_month_qty', 'Price': 'old_price', 'PreMonthMoney': 'old_pre_month_money', 'CarryDate': 'old_carry_date', 'Remarks': 'old_remarks', 'BusinessUnitID': 'old_business_unit_id', 'InDetailNo': 'old_in_detail_no'}
    SOURCE_KEY=('StockDate', 'ArticleKindID', 'ArticleID', 'WareHouseID', 'InDetailNo')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_article_kind_id': 'Chinese_PRC_CI_AS', 'old_article_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_in_detail_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_stock_date=models.DateTimeField('StockDate', null=False, blank=False)
    old_article_kind_id=models.CharField('ArticleKindID', null=False, blank=True, max_length=20)
    old_article_id=models.CharField('ArticleID', null=False, blank=True, max_length=20)
    old_ware_house_id=models.CharField('WareHouseID', null=False, blank=True, max_length=10)
    old_pre_month_qty=models.DecimalField('PreMonthQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=16, decimal_places=6)
    old_pre_month_money=models.DecimalField('PreMonthMoney', null=True, blank=True, max_digits=12, decimal_places=4)
    old_carry_date=models.DateTimeField('CarryDate', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_in_detail_no=models.CharField('InDetailNo', null=False, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_articlestock'
        indexes=[models.Index(fields=['source_batch', 'old_stock_date', 'old_article_kind_id', 'old_article_id', 'old_ware_house_id', 'old_in_detail_no'],name='src_6149c5a260e54fe4'),models.Index(models.F('source_batch'),models.F('old_stock_date'),Upper(RTrim(models.F('old_article_kind_id'))),Upper(RTrim(models.F('old_article_id'))),Upper(RTrim(models.F('old_ware_house_id'))),Upper(RTrim(models.F('old_in_detail_no'))),name='src_ci_6149c5a260e54fe4')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（ArticleStock，待确认）'
        ordering=["-id"]

class SourceDyeArticleStockAdjust(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ArticleStockAdjust'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'WareHouseID': 'old_ware_house_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'BusinessUnitID': 'old_business_unit_id', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_ware_house_id=models.CharField('仓库', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_step_no=models.IntegerField('流程节点号', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_articlestockadjust'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_52620b6efd7c1f6b'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_52620b6efd7c1f6b')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（ArticleStockAdjust，待确认）'
        ordering=["-id"]

class SourceDyeArticleStockAdjustDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ArticleStockAdjustDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'ArticleKindID': 'old_article_kind_id', 'ArticleID': 'old_article_id', 'PaperQty': 'old_paper_qty', 'RealQty': 'old_real_qty', 'AdjustQty': 'old_adjust_qty', 'Price': 'old_price', 'Remarks': 'old_remarks', 'PaperMoney': 'old_paper_money', 'RealMoney': 'old_real_money', 'AdjustMoney': 'old_adjust_money', 'InDetailNo': 'old_in_detail_no'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_article_kind_id': 'Chinese_PRC_CI_AS', 'old_article_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_in_detail_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：ArticleStockAdjust', 'target': 'erp_warehouse.SourceDyeArticleStockAdjust', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 ArticleStockAdjustDetail → ArticleStockAdjust']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=36)
    old_article_kind_id=models.CharField('机物料种类', null=True, blank=True, max_length=20)
    old_article_id=models.CharField('机物料编码', null=True, blank=True, max_length=200)
    old_paper_qty=models.DecimalField('账面数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_qty=models.DecimalField('盘点数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_adjust_qty=models.DecimalField('调整数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=10, decimal_places=4)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_paper_money=models.DecimalField('账面金额', null=True, blank=True, max_digits=14, decimal_places=2)
    old_real_money=models.DecimalField('盘点金额', null=True, blank=True, max_digits=14, decimal_places=2)
    old_adjust_money=models.DecimalField('调整金额', null=True, blank=True, max_digits=14, decimal_places=2)
    old_in_detail_no=models.CharField('入库明细号', null=True, blank=True, max_length=20)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeArticleStockAdjust', verbose_name='原关系：ArticleStockAdjust', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_articlestockadjustdetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_72eaaa786083758a'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_72eaaa786083758a')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（ArticleStockAdjustDetail，待确认）'
        ordering=["-id"]

class SourceDyeArticleStockBook(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ArticleStockBook'
    SOURCE_FIELDS={'BookNo': 'old_book_no', 'BookDate': 'old_book_date', 'AccDate': 'old_acc_date', 'BookKind': 'old_book_kind', 'ArticleKindID': 'old_article_kind_id', 'ArticleID': 'old_article_id', 'SupplierID': 'old_supplier_id', 'WareHouseID': 'old_ware_house_id', 'StorageUnitIDs': 'old_storage_unit_ids', 'SheetNo': 'old_sheet_no', 'DetailNo': 'old_detail_no', 'InQty': 'old_in_qty', 'OutQty': 'old_out_qty', 'Price': 'old_price', 'Remarks': 'old_remarks', 'BusinessUnitID': 'old_business_unit_id', 'DeptID': 'old_dept_id', 'SheetSeries': 'old_sheet_series', 'StockFlag': 'old_stock_flag', 'InMoney': 'old_in_money', 'OutMoney': 'old_out_money', 'CurrDate': 'old_curr_date', 'InDetailNo': 'old_in_detail_no', 'OriDetailNo': 'old_ori_detail_no'}
    SOURCE_KEY=('BookNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_article_kind_id': 'Chinese_PRC_CI_AS', 'old_article_id': 'Chinese_PRC_CI_AS', 'old_supplier_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_storage_unit_ids': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_dept_id': 'Chinese_PRC_CI_AS', 'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_stock_flag': 'Chinese_PRC_CI_AS', 'old_in_detail_no': 'Chinese_PRC_CI_AS', 'old_ori_detail_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=('old_book_no',)
    SOURCE_IDENTITY_RULES={'old_book_no': (1, 1)}
    old_book_no=models.BigIntegerField('BookNo', null=False, blank=False)
    old_book_date=models.DateTimeField('BookDate', null=True, blank=True)
    old_acc_date=models.DateTimeField('AccDate', null=True, blank=True)
    old_book_kind=models.IntegerField('BookKind', null=True, blank=True)
    old_article_kind_id=models.CharField('ArticleKindID', null=True, blank=True, max_length=20)
    old_article_id=models.CharField('ArticleID', null=True, blank=True, max_length=200)
    old_supplier_id=models.CharField('SupplierID', null=True, blank=True, max_length=10)
    old_ware_house_id=models.CharField('WareHouseID', null=True, blank=True, max_length=10)
    old_storage_unit_ids=models.CharField('StorageUnitIDs', null=True, blank=True, max_length=100)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=True, blank=True, max_length=36)
    old_in_qty=models.DecimalField('InQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_out_qty=models.DecimalField('OutQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=14, decimal_places=4)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_dept_id=models.CharField('DeptID', null=True, blank=True, max_length=10)
    old_sheet_series=models.CharField('SheetSeries', null=True, blank=True, max_length=20)
    old_stock_flag=models.CharField('StockFlag', null=True, blank=True, max_length=10)
    old_in_money=models.DecimalField('InMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_out_money=models.DecimalField('OutMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_curr_date=models.DateTimeField('CurrDate', null=True, blank=True)
    old_in_detail_no=models.CharField('InDetailNo', null=True, blank=True, max_length=20)
    old_ori_detail_no=models.CharField('OriDetailNo', null=True, blank=True, max_length=36)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_articlestockbook'
        indexes=[models.Index(fields=['source_batch', 'old_book_no'],name='src_d18ef7a405cf1b14')]
        verbose_name=verbose_name_plural='辅料库存流水'
        ordering=["-id"]

class SourceDyeCarryMaterial(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='CarryMaterial'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'RightStatus': 'old_right_status'}
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

    class Meta(SourceRecord.Meta):
        db_table='src_dye_carrymaterial'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_cdcf306646401500'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_cdcf306646401500')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（CarryMaterial，待确认）'
        ordering=["-id"]

class SourceDyeCarryMaterialDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='CarryMaterialDetail'
    SOURCE_FIELDS={'Sheetseries': 'old_sheetseries', 'DetailNo': 'old_detail_no', 'CustomerID': 'old_customer_id', 'JobSheetNo': 'old_job_sheet_no', 'ProdID': 'old_prod_id', 'ColorNum': 'old_color_num', 'ColorID': 'old_color_id', 'LotNo': 'old_lot_no', 'OrderQty': 'old_order_qty', 'Qty': 'old_qty', 'Rolls': 'old_rolls', 'Area': 'old_area', 'CustSelfNo': 'old_cust_self_no', 'ContractNo': 'old_contract_no', 'Semi_Owner': 'old_semi_owner', 'InSheetKind': 'old_in_sheet_kind', 'ReceSheetNo': 'old_rece_sheet_no', 'WeightQty': 'old_weight_qty', 'SupplierID': 'old_supplier_id', 'JobColorID': 'old_job_color_id', 'FixedQty': 'old_fixed_qty', 'PurchaseOrders': 'old_purchase_orders', 'A_A': 'old_a_a', 'A_B': 'old_a_b', 'PDRolls': 'old_pdrolls', 'PDQty': 'old_pdqty', 'PreField1': 'old_pre_field1'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheetseries': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_area': 'Chinese_PRC_CI_AS', 'old_cust_self_no': 'Chinese_PRC_CI_AS', 'old_contract_no': 'Chinese_PRC_CI_AS', 'old_semi_owner': 'Chinese_PRC_CI_AS', 'old_in_sheet_kind': 'Chinese_PRC_CI_AS', 'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_supplier_id': 'Chinese_PRC_CI_AS', 'old_job_color_id': 'Chinese_PRC_CI_AS', 'old_purchase_orders': 'Chinese_PRC_CI_AS', 'old_a_a': 'Chinese_PRC_CI_AS', 'old_a_b': 'Chinese_PRC_CI_AS', 'old_pre_field1': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheetseries=models.CharField('表单号', null=False, blank=True, max_length=50)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=50)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=30)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=30)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=30)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=30)
    old_color_id=models.CharField('物料颜色', null=True, blank=True, max_length=30)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=50)
    old_order_qty=models.DecimalField('订单数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_qty=models.DecimalField('数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_area=models.CharField('区域', null=True, blank=True, max_length=100)
    old_cust_self_no=models.CharField('制单号', null=True, blank=True, max_length=100)
    old_contract_no=models.CharField('客户单号', null=True, blank=True, max_length=500)
    old_semi_owner=models.CharField('半成品所有者', null=True, blank=True, max_length=30)
    old_in_sheet_kind=models.CharField('物料分类', null=True, blank=True, max_length=30)
    old_rece_sheet_no=models.CharField('入库明细号', null=True, blank=True, max_length=30)
    old_weight_qty=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_supplier_id=models.CharField('供应商', null=True, blank=True, max_length=20)
    old_job_color_id=models.CharField('工卡颜色', null=True, blank=True, max_length=30)
    old_fixed_qty=models.DecimalField('锭重', null=True, blank=True, max_digits=5, decimal_places=2)
    old_purchase_orders=models.CharField('采购单号', null=True, blank=True, max_length=20)
    old_a_a=models.CharField('物料区域', null=True, blank=True, max_length=50)
    old_a_b=models.CharField('物料等级', null=True, blank=True, max_length=100)
    old_pdrolls=models.DecimalField('排单粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pdqty=models.DecimalField('排单重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pre_field1=models.CharField('捻度(H/S)', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_carrymaterialdetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_2a01b4e0239eed01'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_2a01b4e0239eed01')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（CarryMaterialDetail，待确认）'
        ordering=["-id"]

class SourceDyeCookInDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='CookInDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'CookID': 'old_cook_id', 'ArticleKindID': 'old_article_kind_id', 'InQty': 'old_in_qty', 'Price': 'old_price', 'TaxRate': 'old_tax_rate', 'TaxPrice': 'old_tax_price', 'TaxMoney': 'old_tax_money', 'Total': 'old_total', 'PurDetailNo': 'old_pur_detail_no', 'APDetailNo': 'old_apdetail_no', 'InvoiceNo': 'old_invoice_no', 'FactDlvNo': 'old_fact_dlv_no', 'Remarks': 'old_remarks', 'PackQty': 'old_pack_qty', 'PackUnit': 'old_pack_unit', 'Discount': 'old_discount', 'DiscountMoney': 'old_discount_money', 'OriDetailNo': 'old_ori_detail_no', 'Amount': 'old_amount'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_cook_id': 'Chinese_PRC_CI_AS', 'old_article_kind_id': 'Chinese_PRC_CI_AS', 'old_pur_detail_no': 'Chinese_PRC_CI_AS', 'old_apdetail_no': 'Chinese_PRC_CI_AS', 'old_invoice_no': 'Chinese_PRC_CI_AS', 'old_fact_dlv_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_pack_unit': 'Chinese_PRC_CI_AS', 'old_ori_detail_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：CookIn', 'target': 'erp_base.SourceDyeCookIn', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 CookInDetail → CookIn']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('表单明细号（子表）', null=False, blank=True, max_length=36)
    old_cook_id=models.CharField('物料编码', null=True, blank=True, max_length=200)
    old_article_kind_id=models.CharField('物料种类', null=True, blank=True, max_length=20)
    old_in_qty=models.DecimalField('入库数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=16, decimal_places=6)
    old_tax_rate=models.DecimalField('税率', null=True, blank=True, max_digits=4, decimal_places=2)
    old_tax_price=models.DecimalField('含税价', null=True, blank=True, max_digits=16, decimal_places=6)
    old_tax_money=models.DecimalField('税金', null=True, blank=True, max_digits=10, decimal_places=2)
    old_total=models.DecimalField('合计', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pur_detail_no=models.CharField('采购单明细号', null=True, blank=True, max_length=20)
    old_apdetail_no=models.CharField('应付单细号', null=True, blank=True, max_length=20)
    old_invoice_no=models.CharField('发票号码', null=True, blank=True, max_length=30)
    old_fact_dlv_no=models.CharField('送货单号', null=True, blank=True, max_length=80)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_pack_qty=models.DecimalField('包装数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pack_unit=models.CharField('PackUnit', null=True, blank=True, max_length=10)
    old_discount=models.DecimalField('Discount', null=True, blank=True, max_digits=3, decimal_places=2)
    old_discount_money=models.DecimalField('DiscountMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_ori_detail_no=models.CharField('OriDetailNo', null=True, blank=True, max_length=36)
    old_amount=models.FloatField('不含税金额', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_base.SourceDyeCookIn', verbose_name='原关系：CookIn', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_cookindetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_171d6bba5b5da6e0'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_171d6bba5b5da6e0')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（CookInDetail，待确认）'
        ordering=["-id"]

class SourceDyeDyeStuffOut(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DyeStuffOut'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'BusinessUnitID': 'old_business_unit_id', 'WareHouseID': 'old_ware_house_id', 'DeptID': 'old_dept_id', 'CustomerID': 'old_customer_id', 'Keeper': 'old_keeper', 'EmpID': 'old_emp_id', 'RightStatus': 'old_right_status', 'SheetStatus': 'old_sheet_status', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'WeightSheetNo': 'old_weight_sheet_no', 'InDetailNo': 'old_in_detail_no', 'JobSheetNo': 'old_job_sheet_no', 'OutDate': 'old_out_date', 'MachineID': 'old_machine_id', 'FactID': 'old_fact_id', 'SQSheetNo': 'old_sqsheet_no', 'Status': 'old_status'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_dept_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_keeper': 'Chinese_PRC_CI_AS', 'old_emp_id': 'Chinese_PRC_CI_AS', 'old_sheet_status': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_weight_sheet_no': 'Chinese_PRC_CI_AS', 'old_in_detail_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_machine_id': 'Chinese_PRC_CI_AS', 'old_fact_id': 'Chinese_PRC_CI_AS', 'old_sqsheet_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_sheet_kind=models.IntegerField('SheetKind', null=True, blank=True)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_print_times=models.IntegerField('PrintTimes', null=True, blank=True)
    old_revisions=models.IntegerField('Revisions', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=50)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=20)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_ware_house_id=models.CharField('WareHouseID', null=True, blank=True, max_length=20)
    old_dept_id=models.CharField('DeptID', null=True, blank=True, max_length=20)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=50)
    old_keeper=models.CharField('Keeper', null=True, blank=True, max_length=100)
    old_emp_id=models.CharField('EmpID', null=True, blank=True, max_length=50)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_sheet_status=models.CharField('SheetStatus', null=True, blank=True, max_length=1)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=50)
    old_weight_sheet_no=models.CharField('WeightSheetNo', null=True, blank=True, max_length=50)
    old_in_detail_no=models.CharField('InDetailNo', null=True, blank=True, max_length=50)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)
    old_out_date=models.DateTimeField('OutDate', null=True, blank=True)
    old_machine_id=models.CharField('MachineID', null=True, blank=True, max_length=255)
    old_fact_id=models.CharField('FactID', null=True, blank=True, max_length=50)
    old_sqsheet_no=models.CharField('SQSheetNo', null=True, blank=True, max_length=50)
    old_status=models.IntegerField('Status', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_dyestuffout'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_e4010771efa123b6'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_e4010771efa123b6')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（DyeStuffOut，待确认）'
        ordering=["-id"]

class SourceDyeDyeStuffOutDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DyeStuffOutDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'PurDetailNo': 'old_pur_detail_no', 'StuffID': 'old_stuff_id', 'Price': 'old_price', 'TaxPrice': 'old_tax_price', 'TaxRate': 'old_tax_rate', 'TaxMoney': 'old_tax_money', 'Amount': 'old_amount', 'Qty': 'old_qty', 'APDetailNo': 'old_apdetail_no', 'LotNo': 'old_lot_no', 'DlvQty': 'old_dlv_qty', 'Remarks': 'old_remarks', 'InDetailNo': 'old_in_detail_no', 'PhaseNo': 'old_phase_no', 'PhaseID': 'old_phase_id', 'StuffNo': 'old_stuff_no', 'Unit': 'old_unit'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_pur_detail_no': 'Chinese_PRC_CI_AS', 'old_stuff_id': 'Chinese_PRC_CI_AS', 'old_apdetail_no': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_in_detail_no': 'Chinese_PRC_CI_AS', 'old_phase_id': 'Chinese_PRC_CI_AS', 'old_unit': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('SheetSeries', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=False, blank=True, max_length=40)
    old_pur_detail_no=models.CharField('PurDetailNo', null=True, blank=True, max_length=20)
    old_stuff_id=models.CharField('StuffID', null=True, blank=True, max_length=10)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=16, decimal_places=6)
    old_tax_price=models.DecimalField('TaxPrice', null=True, blank=True, max_digits=16, decimal_places=6)
    old_tax_rate=models.DecimalField('TaxRate', null=True, blank=True, max_digits=16, decimal_places=6)
    old_tax_money=models.DecimalField('TaxMoney', null=True, blank=True, max_digits=16, decimal_places=6)
    old_amount=models.DecimalField('Amount', null=True, blank=True, max_digits=16, decimal_places=6)
    old_qty=models.DecimalField('Qty', null=True, blank=True, max_digits=15, decimal_places=6)
    old_apdetail_no=models.CharField('APDetailNo', null=True, blank=True, max_length=20)
    old_lot_no=models.CharField('LotNo', null=True, blank=True, max_length=200)
    old_dlv_qty=models.DecimalField('DlvQty', null=True, blank=True, max_digits=15, decimal_places=6)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_in_detail_no=models.CharField('InDetailNo', null=True, blank=True, max_length=50)
    old_phase_no=models.IntegerField('PhaseNo', null=True, blank=True)
    old_phase_id=models.CharField('PhaseID', null=True, blank=True, max_length=50)
    old_stuff_no=models.IntegerField('StuffNo', null=True, blank=True)
    old_unit=models.CharField('Unit', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_dyestuffoutdetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_f0fe767f0ccd79c5'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_f0fe767f0ccd79c5')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（DyeStuffOutDetail，待确认）'
        ordering=["-id"]

class SourceDyeGrayBalance(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayBalance'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'BusinessUnitID': 'old_business_unit_id', 'WareHouseID': 'old_ware_house_id', 'SheetKind': 'old_sheet_kind', 'Keeper': 'old_keeper', 'PrintTimes': 'old_print_times', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'StepNo': 'old_step_no', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_keeper': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('单号', null=False, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_ware_house_id=models.CharField('仓库', null=True, blank=True, max_length=10)
    old_sheet_kind=models.IntegerField('调整类别', null=True, blank=True)
    old_keeper=models.CharField('仓管员', null=True, blank=True, max_length=20)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('制单人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('制单日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('审核日期', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_graybalance'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_8b9c07b225e63d1a'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_8b9c07b225e63d1a')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（GrayBalance，待确认）'
        ordering=["-id"]

class SourceDyeGrayBalanceDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayBalanceDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'ReceSheetNo': 'old_rece_sheet_no', 'GrayID': 'old_gray_id', 'WareHouseID': 'old_ware_house_id', 'StorageUnitIDs': 'old_storage_unit_ids', 'Piece': 'old_piece', 'WeightQty': 'old_weight_qty', 'GrainQty': 'old_grain_qty', 'Price': 'old_price', 'Amount': 'old_amount', 'Remarks': 'old_remarks', 'LastBookDate': 'old_last_book_date', 'CustomerID': 'old_customer_id', 'LotNo': 'old_lot_no'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_gray_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_storage_unit_ids': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：GrayBalance', 'target': 'erp_warehouse.SourceDyeGrayBalance', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 GrayBalanceDetail → GrayBalance']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=20)
    old_rece_sheet_no=models.CharField('入库明细号', null=False, blank=True, max_length=20)
    old_gray_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_ware_house_id=models.CharField('仓库', null=True, blank=True, max_length=10)
    old_storage_unit_ids=models.CharField('仓位', null=True, blank=True, max_length=100)
    old_piece=models.DecimalField('粒数', null=True, blank=True, max_digits=8, decimal_places=2)
    old_weight_qty=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_grain_qty=models.DecimalField('长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=8, decimal_places=2)
    old_amount=models.DecimalField('金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_last_book_date=models.DateTimeField('最后流水日期', null=True, blank=True)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=10)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=50)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeGrayBalance', verbose_name='原关系：GrayBalance', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_graybalancedetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_4d1cf9fabb7ccdf7'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_4d1cf9fabb7ccdf7')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（GrayBalanceDetail，待确认）'
        ordering=["-id"]

class SourceDyeGrayIn(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayIn'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'BusinessUnitID': 'old_business_unit_id', 'WareHouseID': 'old_ware_house_id', 'SalerGroupID': 'old_saler_group_id', 'IsInputRecord': 'old_is_input_record', 'SheetKind': 'old_sheet_kind', 'GrayKindID': 'old_gray_kind_id', 'SupplierID': 'old_supplier_id', 'FactDlvNo': 'old_fact_dlv_no', 'StockUnit': 'old_stock_unit', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'StepNo': 'old_step_no', 'BusinessKind': 'old_business_kind', 'CustomerID': 'old_customer_id', 'FactID': 'old_fact_id', 'Driver': 'old_driver', 'CarNo': 'old_car_no', 'ShiftID': 'old_shift_id', 'GeterID': 'old_geter_id', 'GetDate': 'old_get_date', 'CheckerID': 'old_checker_id', 'DefectDate': 'old_defect_date', 'DefectShiftID': 'old_defect_shift_id', 'SalerID': 'old_saler_id', 'DetailCustName': 'old_detail_cust_name', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'TakeOver': 'old_take_over', 'Cargador1': 'old_cargador1', 'Cargador2': 'old_cargador2', 'Cargador3': 'old_cargador3', 'Cargador4': 'old_cargador4', 'Cargador5': 'old_cargador5', 'Driver1': 'old_driver1', 'Driver2': 'old_driver2', 'Driver3': 'old_driver3', 'Sender': 'old_sender', 'Discharger1': 'old_discharger1', 'Discharger2': 'old_discharger2', 'Water': 'old_water', 'Ingredients': 'old_ingredients', 'Toosoft': 'old_toosoft', 'Isdecrement': 'old_isdecrement', 'Loss': 'old_loss', 'PackageHtt': 'old_package_htt', 'Width': 'old_width', 'HandFeel': 'old_hand_feel', 'Receiver': 'old_receiver', 'DlvRolls': 'old_dlv_rolls', 'DlvWeightQty': 'old_dlv_weight_qty', 'CustomerCode': 'old_customer_code', 'DlvAddress': 'old_dlv_address', 'KTYY': 'old_ktyy', 'WLLX': 'old_wllx', 'combo1': 'old_combo1', 'SPYSPC': 'old_spyspc', 'SemiOutSheetNo': 'old_semi_out_sheet_no', 'A_A': 'old_a_a'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_saler_group_id': 'Chinese_PRC_CI_AS', 'old_gray_kind_id': 'Chinese_PRC_CI_AS', 'old_supplier_id': 'Chinese_PRC_CI_AS', 'old_fact_dlv_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_fact_id': 'Chinese_PRC_CI_AS', 'old_driver': 'Chinese_PRC_CI_AS', 'old_car_no': 'Chinese_PRC_CI_AS', 'old_shift_id': 'Chinese_PRC_CI_AS', 'old_geter_id': 'Chinese_PRC_CI_AS', 'old_checker_id': 'Chinese_PRC_CI_AS', 'old_defect_shift_id': 'Chinese_PRC_CI_AS', 'old_saler_id': 'Chinese_PRC_CI_AS', 'old_detail_cust_name': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_take_over': 'Chinese_PRC_CI_AS', 'old_cargador1': 'Chinese_PRC_CI_AS', 'old_cargador2': 'Chinese_PRC_CI_AS', 'old_cargador3': 'Chinese_PRC_CI_AS', 'old_cargador4': 'Chinese_PRC_CI_AS', 'old_cargador5': 'Chinese_PRC_CI_AS', 'old_driver1': 'Chinese_PRC_CI_AS', 'old_driver2': 'Chinese_PRC_CI_AS', 'old_driver3': 'Chinese_PRC_CI_AS', 'old_sender': 'Chinese_PRC_CI_AS', 'old_discharger1': 'Chinese_PRC_CI_AS', 'old_discharger2': 'Chinese_PRC_CI_AS', 'old_water': 'Chinese_PRC_CI_AS', 'old_ingredients': 'Chinese_PRC_CI_AS', 'old_toosoft': 'Chinese_PRC_CI_AS', 'old_isdecrement': 'Chinese_PRC_CI_AS', 'old_loss': 'Chinese_PRC_CI_AS', 'old_package_htt': 'Chinese_PRC_CI_AS', 'old_width': 'Chinese_PRC_CI_AS', 'old_hand_feel': 'Chinese_PRC_CI_AS', 'old_receiver': 'Chinese_PRC_CI_AS', 'old_customer_code': 'Chinese_PRC_CI_AS', 'old_dlv_address': 'Chinese_PRC_CI_AS', 'old_ktyy': 'Chinese_PRC_CI_AS', 'old_wllx': 'Chinese_PRC_CI_AS', 'old_combo1': 'Chinese_PRC_CI_AS', 'old_spyspc': 'Chinese_PRC_CI_AS', 'old_semi_out_sheet_no': 'Chinese_PRC_CI_AS', 'old_a_a': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=False, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_ware_house_id=models.CharField('仓库代码', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('业务组别', null=True, blank=True, max_length=10)
    old_is_input_record=models.BooleanField('录入码单明细否', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类别', null=True, blank=True)
    old_gray_kind_id=models.CharField('胚纱类别', null=True, blank=True, max_length=10)
    old_supplier_id=models.CharField('供应商代码', null=True, blank=True, max_length=10)
    old_fact_dlv_no=models.CharField('送货单号', null=True, blank=True, max_length=20)
    old_stock_unit=models.IntegerField('库存单位', null=True, blank=True)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_step_no=models.IntegerField('工作流节点号', null=True, blank=True)
    old_business_kind=models.IntegerField('业务类别', null=True, blank=True)
    old_customer_id=models.CharField('客户名称', null=True, blank=True, max_length=10)
    old_fact_id=models.CharField('加工商', null=True, blank=True, max_length=10)
    old_driver=models.CharField('司机', null=True, blank=True, max_length=20)
    old_car_no=models.CharField('车牌号', null=True, blank=True, max_length=20)
    old_shift_id=models.CharField('班组', null=True, blank=True, max_length=10)
    old_geter_id=models.CharField('GeterID', null=True, blank=True, max_length=10)
    old_get_date=models.DateTimeField('GetDate', null=True, blank=True)
    old_checker_id=models.CharField('CheckerID', null=True, blank=True, max_length=10)
    old_defect_date=models.DateTimeField('DefectDate', null=True, blank=True)
    old_defect_shift_id=models.CharField('DefectShiftID', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('业务员', null=True, blank=True, max_length=10)
    old_detail_cust_name=models.CharField('明细客户', null=True, blank=True, max_length=50)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_take_over=models.CharField('收货员', null=True, blank=True, max_length=10)
    old_cargador1=models.CharField('搬运工1', null=True, blank=True, max_length=10)
    old_cargador2=models.CharField('搬运工2', null=True, blank=True, max_length=10)
    old_cargador3=models.CharField('搬运工3', null=True, blank=True, max_length=10)
    old_cargador4=models.CharField('送货地址', null=True, blank=True, max_length=10)
    old_cargador5=models.CharField('搬运工5', null=True, blank=True, max_length=10)
    old_driver1=models.CharField('叉车1', null=True, blank=True, max_length=10)
    old_driver2=models.CharField('叉车2', null=True, blank=True, max_length=10)
    old_driver3=models.CharField('叉车3', null=True, blank=True, max_length=10)
    old_sender=models.CharField('交胚人', null=True, blank=True, max_length=10)
    old_discharger1=models.CharField('装卸工1', null=True, blank=True, max_length=10)
    old_discharger2=models.CharField('装卸工2', null=True, blank=True, max_length=10)
    old_water=models.CharField('水量', null=True, blank=True, max_length=10)
    old_ingredients=models.CharField('Ingredients', null=True, blank=True, max_length=20)
    old_toosoft=models.CharField('过软', null=True, blank=True, max_length=20)
    old_isdecrement=models.CharField('Isdecrement', null=True, blank=True, max_length=20)
    old_loss=models.CharField('Loss', null=True, blank=True, max_length=50)
    old_package_htt=models.CharField('包装', null=True, blank=True, max_length=20)
    old_width=models.CharField('Width', null=True, blank=True, max_length=50)
    old_hand_feel=models.CharField('手感', null=True, blank=True, max_length=20)
    old_receiver=models.CharField('收货人', null=True, blank=True, max_length=20)
    old_dlv_rolls=models.DecimalField('收胚粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dlv_weight_qty=models.DecimalField('收胚重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_customer_code=models.CharField('客户全称', null=True, blank=True, max_length=50)
    old_dlv_address=models.CharField('送货地址', null=True, blank=True, max_length=500)
    old_ktyy=models.CharField('客退原因', null=True, blank=True, max_length=250)
    old_wllx=models.CharField('物流类型', null=True, blank=True, max_length=255)
    old_combo1=models.CharField('收发地点', null=True, blank=True, max_length=10)
    old_spyspc=models.CharField('收胚运输编号', null=True, blank=True, max_length=20)
    old_semi_out_sheet_no=models.CharField('SemiOutSheetNo', null=True, blank=True, max_length=50)
    old_a_a=models.CharField('物料屈戌', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_grayin'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_2e23e5cebb387f53'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_2e23e5cebb387f53')]
        verbose_name=verbose_name_plural='坯布入库单'
        ordering=["-id"]

class SourceDyeGrayInDefect(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayInDefect'
    SOURCE_FIELDS={'ReceSheetNo': 'old_rece_sheet_no', 'DefectNo': 'old_defect_no', 'DefectID': 'old_defect_id', 'Qty': 'old_qty'}
    SOURCE_KEY=('ReceSheetNo', 'DefectNo')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_defect_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_rece_sheet_no=models.CharField('ReceSheetNo', null=False, blank=True, max_length=20)
    old_defect_no=models.IntegerField('DefectNo', null=False, blank=False)
    old_defect_id=models.CharField('DefectID', null=True, blank=True, max_length=10)
    old_qty=models.DecimalField('Qty', null=True, blank=True, max_digits=10, decimal_places=2)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_grayindefect'
        indexes=[models.Index(fields=['source_batch', 'old_rece_sheet_no', 'old_defect_no'],name='src_6b8cef2c93ce2f0b'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_rece_sheet_no'))),models.F('old_defect_no'),name='src_ci_6b8cef2c93ce2f0b')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（GrayInDefect，待确认）'
        ordering=["-id"]

class SourceDyeGrayInDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayInDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'ReceSheetNo': 'old_rece_sheet_no', 'Spec': 'old_spec', 'StorageUnitIDs': 'old_storage_unit_ids', 'Rolls': 'old_rolls', 'Packs': 'old_packs', 'WeightQty': 'old_weight_qty', 'LengthQty': 'old_length_qty', 'Price': 'old_price', 'Amount': 'old_amount', 'Weight': 'old_weight', 'Width': 'old_width', 'DlvRolls': 'old_dlv_rolls', 'DlvPacks': 'old_dlv_packs', 'DlvQty': 'old_dlv_qty', 'CheckNo': 'old_check_no', 'PurDetailNo': 'old_pur_detail_no', 'APDetailNo': 'old_apdetail_no', 'OriReceSheetNo': 'old_ori_rece_sheet_no', 'Remarks': 'old_remarks', 'ColorID': 'old_color_id', 'RollAvgQty': 'old_roll_avg_qty', 'WeftDensity': 'old_weft_density', 'WarpDensity': 'old_warp_density', 'CheckResult': 'old_check_result', 'GradeID': 'old_grade_id', 'OriJobsheetNo': 'old_ori_jobsheet_no', 'MachineID': 'old_machine_id', 'ProcessID': 'old_process_id', 'DetailsCustomer': 'old_details_customer', 'GrayID': 'old_gray_id', 'LotNo': 'old_lot_no', 'PreField1': 'old_pre_field1', 'PreField2': 'old_pre_field2', 'PreField3': 'old_pre_field3', 'PreField4': 'old_pre_field4', 'PreField5': 'old_pre_field5', 'PCS': 'old_pcs', 'FixedQty': 'old_fixed_qty', 'ColorNum': 'old_color_num', 'ColorLv': 'old_color_lv', 'Yardage': 'old_yardage', 'CustJobNo': 'old_cust_job_no', 'GUnit': 'old_gunit', 'InputCode': 'old_input_code', 'Area': 'old_area', 'GrayApplyNo': 'old_gray_apply_no', 'YarnCategory': 'old_yarn_category', 'TrunReceSheetNo': 'old_trun_rece_sheet_no', 'PurchaseOrders': 'old_purchase_orders', 'A_A': 'old_a_a', 'A_B': 'old_a_b', 'ProdID': 'old_prod_id', 'InSheetKind': 'old_in_sheet_kind', 'JobSheetNo': 'old_job_sheet_no'}
    SOURCE_KEY=('ReceSheetNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_storage_unit_ids': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_pur_detail_no': 'Chinese_PRC_CI_AS', 'old_apdetail_no': 'Chinese_PRC_CI_AS', 'old_ori_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_check_result': 'Chinese_PRC_CI_AS', 'old_grade_id': 'Chinese_PRC_CI_AS', 'old_ori_jobsheet_no': 'Chinese_PRC_CI_AS', 'old_machine_id': 'Chinese_PRC_CI_AS', 'old_process_id': 'Chinese_PRC_CI_AS', 'old_details_customer': 'Chinese_PRC_CI_AS', 'old_gray_id': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_pre_field1': 'Chinese_PRC_CI_AS', 'old_pre_field2': 'Chinese_PRC_CI_AS', 'old_pre_field3': 'Chinese_PRC_CI_AS', 'old_pre_field4': 'Chinese_PRC_CI_AS', 'old_pre_field5': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_color_lv': 'Chinese_PRC_CI_AS', 'old_cust_job_no': 'Chinese_PRC_CI_AS', 'old_input_code': 'Chinese_PRC_CI_AS', 'old_area': 'Chinese_PRC_CI_AS', 'old_gray_apply_no': 'Chinese_PRC_CI_AS', 'old_yarn_category': 'Chinese_PRC_CI_AS', 'old_trun_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_purchase_orders': 'Chinese_PRC_CI_AS', 'old_a_a': 'Chinese_PRC_CI_AS', 'old_a_b': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_in_sheet_kind': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：GrayIn', 'target': 'erp_warehouse.SourceDyeGrayIn', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 PurGrayInDetail → PurGrayIn', '原界面主从 TuiHuoGrayInDetail → TuiHuoGrayIn', '原界面主从 SemiToGrayInDetail → SemiToGrayIn', '原界面主从 KeTuiGrayInDetail → KeTuiGrayIn', '原界面主从 GrayAllotInDetail → GrayAllotIn', '原界面主从 JiaNianGrayInDetail → JiaNianGrayIn', '原界面主从 GrayInWorkDetail → GrayInWork', '原界面主从 GrayInDetail → GrayIn']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=True, blank=True, max_length=20)
    old_rece_sheet_no=models.CharField('入库明细号', null=False, blank=True, max_length=20)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=128)
    old_storage_unit_ids=models.CharField('库位代码复合', null=True, blank=True, max_length=100)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_packs=models.DecimalField('件数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_weight_qty=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_length_qty=models.DecimalField('长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_amount=models.DecimalField('金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight=models.DecimalField('克重', null=True, blank=True, max_digits=8, decimal_places=4)
    old_width=models.DecimalField('幅宽', null=True, blank=True, max_digits=6, decimal_places=2)
    old_dlv_rolls=models.DecimalField('交货粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_dlv_packs=models.DecimalField('交货包数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_dlv_qty=models.DecimalField('交货数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_check_no=models.CharField('订单明细号', null=True, blank=True, max_length=20)
    old_pur_detail_no=models.CharField('采购单明细号', null=True, blank=True, max_length=20)
    old_apdetail_no=models.CharField('应付单细号', null=True, blank=True, max_length=20)
    old_ori_rece_sheet_no=models.CharField('原收纱明细编号', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=60)
    old_roll_avg_qty=models.DecimalField('粒长', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weft_density=models.DecimalField('纬密', null=True, blank=True, max_digits=6, decimal_places=2)
    old_warp_density=models.DecimalField('经密', null=True, blank=True, max_digits=6, decimal_places=2)
    old_check_result=models.CharField('检验意见', null=True, blank=True, max_length=100)
    old_grade_id=models.CharField('色号等级', null=True, blank=True, max_length=10)
    old_ori_jobsheet_no=models.CharField('原工卡号', null=True, blank=True, max_length=20)
    old_machine_id=models.CharField('机号', null=True, blank=True, max_length=50)
    old_process_id=models.CharField('ProcessID', null=True, blank=True, max_length=10)
    old_details_customer=models.CharField('织厂', null=True, blank=True, max_length=50)
    old_gray_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=50)
    old_pre_field1=models.CharField('捻度(H/S)', null=True, blank=True, max_length=50)
    old_pre_field2=models.CharField('氨纶', null=True, blank=True, max_length=50)
    old_pre_field3=models.CharField('针数', null=True, blank=True, max_length=50)
    old_pre_field4=models.CharField('寸数', null=True, blank=True, max_length=50)
    old_pre_field5=models.CharField('纱批', null=True, blank=True, max_length=200)
    old_pcs=models.IntegerField('粒/件', null=True, blank=True)
    old_fixed_qty=models.DecimalField('锭重', null=True, blank=True, max_digits=5, decimal_places=2)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=20)
    old_color_lv=models.CharField('色级', null=True, blank=True, max_length=20)
    old_yardage=models.DecimalField('码数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_cust_job_no=models.CharField('收料单号', null=True, blank=True, max_length=100)
    old_gunit=models.IntegerField('GUnit', null=True, blank=True)
    old_input_code=models.CharField('打包明细', null=True, blank=True, max_length=50)
    old_area=models.CharField('区域', null=True, blank=True, max_length=100)
    old_gray_apply_no=models.CharField('胚纱退货申请单号', null=True, blank=True, max_length=30)
    old_yarn_category=models.CharField('纱类别', null=True, blank=True, max_length=30)
    old_trun_rece_sheet_no=models.CharField('转仓前入库明细单号', null=True, blank=True, max_length=50)
    old_purchase_orders=models.CharField('采购单号', null=True, blank=True, max_length=20)
    old_a_a=models.CharField('物料区域', null=True, blank=True, max_length=50)
    old_a_b=models.CharField('物料等级', null=True, blank=True, max_length=100)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=30)
    old_in_sheet_kind=models.CharField('物料分类', null=True, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('工卡号', null=True, blank=True, max_length=20)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeGrayIn', verbose_name='原关系：GrayIn', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_grayindetail'
        indexes=[models.Index(fields=['source_batch', 'old_rece_sheet_no'],name='src_6ba0eb6b305ead41'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_rece_sheet_no'))),name='src_ci_6ba0eb6b305ead41')]
        verbose_name=verbose_name_plural='坯布入库明细'
        ordering=["-id"]

class SourceDyeGrayInRecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayInRecord'
    SOURCE_FIELDS={'ReceSheetNo': 'old_rece_sheet_no', 'RollNo': 'old_roll_no', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'DlvQty': 'old_dlv_qty', 'StorageUnitID': 'old_storage_unit_id', 'Defects': 'old_defects', 'Status': 'old_status', 'BarCode': 'old_bar_code', 'AssignedNo': 'old_assigned_no', 'JobSheetNo': 'old_job_sheet_no', 'OriReceSheetNo': 'old_ori_rece_sheet_no', 'RollNo2': 'old_roll_no2', 'GUnit': 'old_gunit', 'OriBarCode': 'old_ori_bar_code', 'Remark': 'old_remark', 'GraySpec': 'old_gray_spec', 'Num': 'old_num', 'CBz': 'old_cbz', 'Rolls': 'old_rolls', 'Packs': 'old_packs', 'InputDetailCode': 'old_input_detail_code', 'Kg': 'old_kg', 'CustQty': 'old_cust_qty', 'TubeWeight': 'old_tube_weight'}
    SOURCE_KEY=('ReceSheetNo', 'RollNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_roll_no': 'Chinese_PRC_CI_AS', 'old_storage_unit_id': 'Chinese_PRC_CI_AS', 'old_defects': 'Chinese_PRC_CI_AS', 'old_status': 'Chinese_PRC_CI_AS', 'old_bar_code': 'Chinese_PRC_CI_AS', 'old_assigned_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_ori_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_roll_no2': 'Chinese_PRC_CI_AS', 'old_ori_bar_code': 'Chinese_PRC_CI_AS', 'old_remark': 'Chinese_PRC_CI_AS', 'old_gray_spec': 'Chinese_PRC_CI_AS', 'old_cbz': 'Chinese_PRC_CI_AS', 'old_input_detail_code': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：GrayInDetail', 'target': 'erp_warehouse.SourceDyeGrayInDetail', 'source_fields': ['ReceSheetNo'], 'target_fields': ['ReceSheetNo'], 'evidence': ['原界面主从 TuiHuoGrayInRecord → TuiHuoGrayInDetail', '原界面主从 GrayInRecord → GrayInDetail', '原界面主从 JiaNianGrayInRecord → JiaNianGrayInDetail', '原界面主从 KeTuiGrayInRecord → KeTuiGrayInDetail', '原界面主从 PurGrayInRecord → PurGrayInDetail', '原界面主从 GrayAllotInRecord → GrayAllotInDetail', '原界面主从 GrayInWorkRecord → GrayInWorkDetail']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_rece_sheet_no=models.CharField('入库明细号', null=False, blank=True, max_length=20)
    old_roll_no=models.CharField('箱号', null=False, blank=True, max_length=20)
    old_length_qty=models.DecimalField('长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dlv_qty=models.DecimalField('交货数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_storage_unit_id=models.CharField('仓位', null=True, blank=True, max_length=10)
    old_defects=models.CharField('疵点', null=True, blank=True, max_length=100)
    old_status=models.CharField('状态', null=True, blank=True, max_length=1)
    old_bar_code=models.CharField('条码', null=True, blank=True, max_length=50)
    old_assigned_no=models.CharField('投胚流水号', null=True, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_ori_rece_sheet_no=models.CharField('OriReceSheetNo', null=True, blank=True, max_length=20)
    old_roll_no2=models.CharField('RollNo2', null=True, blank=True, max_length=20)
    old_gunit=models.IntegerField('GUnit', null=True, blank=True)
    old_ori_bar_code=models.CharField('OriBarCode', null=True, blank=True, max_length=50)
    old_remark=models.CharField('备注', null=True, blank=True, max_length=300)
    old_gray_spec=models.CharField('GraySpec', null=True, blank=True, max_length=50)
    old_num=models.DecimalField('Num', null=True, blank=True, max_digits=8, decimal_places=0)
    old_cbz=models.CharField('CBz', null=True, blank=True, max_length=10)
    old_rolls=models.FloatField('粒数', null=True, blank=True)
    old_packs=models.DecimalField('件数', null=True, blank=True, max_digits=4, decimal_places=1)
    old_input_detail_code=models.CharField('标签打印细码', null=True, blank=True, max_length=100)
    old_kg=models.DecimalField('磅重', null=True, blank=True, max_digits=10, decimal_places=2)
    old_cust_qty=models.DecimalField('毛重', null=True, blank=True, max_digits=10, decimal_places=1)
    old_tube_weight=models.DecimalField('纸筒', null=True, blank=True, max_digits=6, decimal_places=2)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeGrayInDetail', verbose_name='原关系：GrayInDetail', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_grayinrecord'
        indexes=[models.Index(fields=['source_batch', 'old_rece_sheet_no', 'old_roll_no'],name='src_6233e63e7e409470'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_rece_sheet_no'))),Upper(RTrim(models.F('old_roll_no'))),name='src_ci_6233e63e7e409470')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（GrayInRecord，待确认）'
        ordering=["-id"]

class SourceDyeGrayMaterial(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayMaterial'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'RightStatus': 'old_right_status'}
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

    class Meta(SourceRecord.Meta):
        db_table='src_dye_graymaterial'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_a81f50041470599c'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_a81f50041470599c')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（GrayMaterial，待确认）'
        ordering=["-id"]

class SourceDyeGrayMaterialDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayMaterialDetail'
    SOURCE_FIELDS={'Sheetseries': 'old_sheetseries', 'DetailNo': 'old_detail_no', 'CustomerID': 'old_customer_id', 'JobSheetNo': 'old_job_sheet_no', 'ProdID': 'old_prod_id', 'ColorNum': 'old_color_num', 'ColorID': 'old_color_id', 'LotNo': 'old_lot_no', 'OrderQty': 'old_order_qty', 'Qty': 'old_qty', 'Rolls': 'old_rolls', 'Area': 'old_area', 'CustSelfNo': 'old_cust_self_no', 'ContractNo': 'old_contract_no', 'CustFabricName': 'old_cust_fabric_name', 'SumAssignedRolls': 'old_sum_assigned_rolls', 'SumAssignedWeightQty': 'old_sum_assigned_weight_qty', 'ColorRemarks': 'old_color_remarks', 'Remarks': 'old_remarks', 'DyeDate': 'old_dye_date', 'OrderSheetDate': 'old_order_sheet_date', 'DetailCustName': 'old_detail_cust_name', 'FenTou': 'old_fen_tou', 'RightStatus': 'old_right_status', 'SheetStatus': 'old_sheet_status', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheetseries': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_area': 'Chinese_PRC_CI_AS', 'old_cust_self_no': 'Chinese_PRC_CI_AS', 'old_contract_no': 'Chinese_PRC_CI_AS', 'old_cust_fabric_name': 'Chinese_PRC_CI_AS', 'old_color_remarks': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_dye_date': 'Chinese_PRC_CI_AS', 'old_detail_cust_name': 'Chinese_PRC_CI_AS', 'old_fen_tou': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关联：GrayMaterial', 'target': 'erp_warehouse.SourceDyeGrayMaterial', 'source_fields': ['Sheetseries'], 'target_fields': ['SheetSeries'], 'evidence': ['2026-10-11有效入口GrayMaterialDetail的MasterDataTableName及RelaFieldNames']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
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
    old_sum_assigned_rolls=models.DecimalField('实发粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_sum_assigned_weight_qty=models.DecimalField('实发重量', null=True, blank=True, max_digits=10, decimal_places=2)
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
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeGrayMaterial', verbose_name='原关联：GrayMaterial', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_graymaterialdetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_d58c3ed50f2b475e'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_d58c3ed50f2b475e')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（GrayMaterialDetail，待确认）'
        ordering=["-id"]

class SourceDyeGrayOut(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayOut'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'GrayKindID': 'old_gray_kind_id', 'BusinessUnitID': 'old_business_unit_id', 'SalerGroupID': 'old_saler_group_id', 'WareHouseID': 'old_ware_house_id', 'CustomerID': 'old_customer_id', 'SalerID': 'old_saler_id', 'FactID': 'old_fact_id', 'StockUnit': 'old_stock_unit', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'StepNo': 'old_step_no', 'BusinessKind': 'old_business_kind', 'SupplierID': 'old_supplier_id', 'CarNo': 'old_car_no', 'Driver': 'old_driver', 'ToPlace': 'old_to_place', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'FabricID': 'old_fabric_id', 'Cargador1': 'old_cargador1', 'Cargador2': 'old_cargador2', 'Cargador3': 'old_cargador3', 'Cargador4': 'old_cargador4', 'Cargador5': 'old_cargador5', 'Rolls': 'old_rolls', 'WProcessNo': 'old_wprocess_no', 'CheckNo': 'old_check_no'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_gray_kind_id': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_saler_group_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_saler_id': 'Chinese_PRC_CI_AS', 'old_fact_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_supplier_id': 'Chinese_PRC_CI_AS', 'old_car_no': 'Chinese_PRC_CI_AS', 'old_driver': 'Chinese_PRC_CI_AS', 'old_to_place': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_fabric_id': 'Chinese_PRC_CI_AS', 'old_cargador1': 'Chinese_PRC_CI_AS', 'old_cargador2': 'Chinese_PRC_CI_AS', 'old_cargador3': 'Chinese_PRC_CI_AS', 'old_cargador4': 'Chinese_PRC_CI_AS', 'old_cargador5': 'Chinese_PRC_CI_AS', 'old_wprocess_no': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_sheet_no': ('literal', ''), 'old_sheet_date': ('literal', '1900-01-01'), 'old_sheet_kind': ('literal', 0), 'old_gray_kind_id': ('literal', ''), 'old_business_unit_id': ('literal', ''), 'old_saler_group_id': ('literal', ''), 'old_ware_house_id': ('literal', ''), 'old_customer_id': ('literal', ''), 'old_fact_id': ('literal', ''), 'old_stock_unit': ('literal', 0), 'old_sheet_status': ('literal', 0), 'old_right_status': ('literal', 0), 'old_print_times': ('literal', 0), 'old_revisions': ('literal', 0), 'old_remarks': ('literal', ''), 'old_creater': ('literal', ''), 'old_create_date': ('literal', '1900-01-01'), 'old_modifyer': ('literal', ''), 'old_modify_date': ('literal', '1900-01-01')}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=False, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类别', null=True, blank=True)
    old_gray_kind_id=models.CharField('胚纱类别', null=True, blank=True, max_length=10)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('业务组别', null=True, blank=True, max_length=10)
    old_ware_house_id=models.CharField('仓库代码', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户代码', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('业务员', null=True, blank=True, max_length=10)
    old_fact_id=models.CharField('工厂代码', null=True, blank=True, max_length=1000)
    old_stock_unit=models.IntegerField('库存单位', null=True, blank=True)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_step_no=models.IntegerField('工作流节点号', null=True, blank=True)
    old_business_kind=models.IntegerField('业务类别', null=True, blank=True)
    old_supplier_id=models.CharField('供应商', null=True, blank=True, max_length=10)
    old_car_no=models.CharField('配纱员', null=True, blank=True, max_length=20)
    old_driver=models.CharField('Driver', null=True, blank=True, max_length=20)
    old_to_place=models.CharField('ToPlace', null=True, blank=True, max_length=500)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_fabric_id=models.CharField('客户规格', null=True, blank=True, max_length=50)
    old_cargador1=models.CharField('Cargador1', null=True, blank=True, max_length=10)
    old_cargador2=models.CharField('Cargador2', null=True, blank=True, max_length=10)
    old_cargador3=models.CharField('Cargador3', null=True, blank=True, max_length=10)
    old_cargador4=models.CharField('Cargador4', null=True, blank=True, max_length=10)
    old_cargador5=models.CharField('Cargador5', null=True, blank=True, max_length=10)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_wprocess_no=models.CharField('WProcessNo', null=True, blank=True, max_length=1000)
    old_check_no=models.CharField('订单明细', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_grayout'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_1a6a13e96cc191be'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_1a6a13e96cc191be')]
        verbose_name=verbose_name_plural='坯布出库单'
        ordering=["-id"]

class SourceDyeGrayOutDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayOutDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'AssignedNo': 'old_assigned_no', 'ReceSheetNo': 'old_rece_sheet_no', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'Rolls': 'old_rolls', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'Price': 'old_price', 'Amount': 'old_amount', 'Weight': 'old_weight', 'Width': 'old_width', 'CheckNo': 'old_check_no', 'Remarks': 'old_remarks', 'Packs': 'old_packs', 'PCS': 'old_pcs', 'FixedQty': 'old_fixed_qty', 'GrayID': 'old_gray_id', 'ColorNum': 'old_color_num', 'ColorID': 'old_color_id', 'ColorE': 'old_color_e', 'ColorDepthID': 'old_color_depth_id', 'JobSheetNo': 'old_job_sheet_no', 'StorageUnitIDs': 'old_storage_unit_ids', 'MachineID': 'old_machine_id', 'CustJobNo': 'old_cust_job_no', 'BasicQty': 'old_basic_qty', 'LWRate': 'old_lwrate', 'JobSheetSeries': 'old_job_sheet_series', 'FabricID': 'old_fabric_id', 'DetailCustName': 'old_detail_cust_name', 'Area': 'old_area', 'PreField1': 'old_pre_field1', 'PreField2': 'old_pre_field2', 'PreField3': 'old_pre_field3', 'PreField4': 'old_pre_field4', 'PreField5': 'old_pre_field5', 'SupplierID': 'old_supplier_id', 'InSheetKind': 'old_in_sheet_kind', 'PurchaseOrders': 'old_purchase_orders', 'A_A': 'old_a_a', 'A_B': 'old_a_b', 'InputCode': 'old_input_code'}
    SOURCE_KEY=('AssignedNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_assigned_no': 'Chinese_PRC_CI_AS', 'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_gray_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_e': 'Chinese_PRC_CI_AS', 'old_color_depth_id': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_storage_unit_ids': 'Chinese_PRC_CI_AS', 'old_machine_id': 'Chinese_PRC_CI_AS', 'old_cust_job_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_series': 'Chinese_PRC_CI_AS', 'old_fabric_id': 'Chinese_PRC_CI_AS', 'old_detail_cust_name': 'Chinese_PRC_CI_AS', 'old_area': 'Chinese_PRC_CI_AS', 'old_pre_field1': 'Chinese_PRC_CI_AS', 'old_pre_field2': 'Chinese_PRC_CI_AS', 'old_pre_field3': 'Chinese_PRC_CI_AS', 'old_pre_field4': 'Chinese_PRC_CI_AS', 'old_pre_field5': 'Chinese_PRC_CI_AS', 'old_supplier_id': 'Chinese_PRC_CI_AS', 'old_in_sheet_kind': 'Chinese_PRC_CI_AS', 'old_purchase_orders': 'Chinese_PRC_CI_AS', 'old_a_a': 'Chinese_PRC_CI_AS', 'old_a_b': 'Chinese_PRC_CI_AS', 'old_input_code': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：GrayOut', 'target': 'erp_warehouse.SourceDyeGrayOut', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 GrayOutDetailTurn → GrayOutTurn', '原界面主从 GrayOutDetail → GrayOut', '原界面主从 TSGrayOutDetail → TSGrayOut', '原界面主从 GrayOutDetailJob → GrayOutJob', '原界面主从 GrayAllotOutDetail → GrayAllotOut', '原界面主从 GrayOutDetailShenHe → GrayOutShenHe', '原界面主从 GrayOutSaleDetail → GrayOutSale', '原界面主从 GrayOutWorkDetail → GrayOutWork']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_assigned_no=models.CharField('投胚流水号', null=False, blank=True, max_length=20)
    old_rece_sheet_no=models.CharField('入库明细号', null=True, blank=True, max_length=20)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=128)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=50)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_length_qty=models.DecimalField('长度数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('重量数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_amount=models.DecimalField('金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight=models.DecimalField('克重', null=True, blank=True, max_digits=6, decimal_places=2)
    old_width=models.DecimalField('幅宽', null=True, blank=True, max_digits=6, decimal_places=2)
    old_check_no=models.CharField('订单明细号', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_packs=models.DecimalField('件数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_pcs=models.IntegerField('粒/件', null=True, blank=True)
    old_fixed_qty=models.DecimalField('锭重', null=True, blank=True, max_digits=5, decimal_places=2)
    old_gray_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=20)
    old_color_id=models.CharField('物料颜色', null=True, blank=True, max_length=20)
    old_color_e=models.CharField('ColorE', null=True, blank=True, max_length=20)
    old_color_depth_id=models.CharField('颜色深浅', null=True, blank=True, max_length=10)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_storage_unit_ids=models.CharField('库位', null=True, blank=True, max_length=100)
    old_machine_id=models.CharField('MachineID', null=True, blank=True, max_length=10)
    old_cust_job_no=models.CharField('客户缸号', null=True, blank=True, max_length=20)
    old_basic_qty=models.DecimalField('BasicQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_lwrate=models.DecimalField('LWRate', null=True, blank=True, max_digits=6, decimal_places=4)
    old_job_sheet_series=models.CharField('JobSheetSeries', null=True, blank=True, max_length=20)
    old_fabric_id=models.CharField('客户规格', null=True, blank=True, max_length=50)
    old_detail_cust_name=models.CharField('明细客户', null=True, blank=True, max_length=50)
    old_area=models.CharField('区域', null=True, blank=True, max_length=100)
    old_pre_field1=models.CharField('捻度(H/S)', null=True, blank=True, max_length=50)
    old_pre_field2=models.CharField('PreField2', null=True, blank=True, max_length=50)
    old_pre_field3=models.CharField('PreField3', null=True, blank=True, max_length=50)
    old_pre_field4=models.CharField('PreField4', null=True, blank=True, max_length=50)
    old_pre_field5=models.CharField('PreField5', null=True, blank=True, max_length=200)
    old_supplier_id=models.CharField('供应商', null=True, blank=True, max_length=30)
    old_in_sheet_kind=models.CharField('物料分类', null=True, blank=True, max_length=20)
    old_purchase_orders=models.CharField('采购单号', null=True, blank=True, max_length=20)
    old_a_a=models.CharField('物料区域', null=True, blank=True, max_length=50)
    old_a_b=models.CharField('物料等级', null=True, blank=True, max_length=100)
    old_input_code=models.CharField('打包条码', null=True, blank=True, max_length=40)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeGrayOut', verbose_name='原关系：GrayOut', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_grayoutdetail'
        indexes=[models.Index(fields=['source_batch', 'old_assigned_no'],name='src_c25656a797fc5f2a'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_assigned_no'))),name='src_ci_c25656a797fc5f2a')]
        verbose_name=verbose_name_plural='坯布出库明细'
        ordering=["-id"]

class SourceDyeGrayOutRecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayOutRecord'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'AssignedNo': 'old_assigned_no', 'RollNo': 'old_roll_no', 'BarCode': 'old_bar_code', 'ReceSheetNo': 'old_rece_sheet_no', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'StorageUnitID': 'old_storage_unit_id', 'Status': 'old_status', 'Remarks': 'old_remarks', 'GUnit': 'old_gunit', 'Rolls': 'old_rolls', 'JobSheetNo': 'old_job_sheet_no', 'Packs': 'old_packs'}
    SOURCE_KEY=('AssignedNo', 'RollNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_assigned_no': 'Chinese_PRC_CI_AS', 'old_roll_no': 'Chinese_PRC_CI_AS', 'old_bar_code': 'Chinese_PRC_CI_AS', 'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_storage_unit_id': 'Chinese_PRC_CI_AS', 'old_status': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：GrayOutDetail', 'target': 'erp_warehouse.SourceDyeGrayOutDetail', 'source_fields': ['AssignedNo'], 'target_fields': ['AssignedNo'], 'evidence': ['原界面主从 GrayOutRecord → GrayOutDetail', '原界面主从 GrayOutSaleRecord → GrayOutSaleDetail', '原界面主从 GrayOutRecordShenHe → GrayOutDetailShenHe', '原界面主从 GrayOutRecordTurn → GrayOutDetailTurn', '原界面主从 GrayOutRecordMatch → GrayOutDetail', '原界面主从 GrayOutWorkRecord → GrayOutWorkDetail', '原界面主从 GrayOutRecordJob → GrayOutDetailJob', '原界面主从 TSGrayOutRecordMatch → TSGrayOutDetail']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('工卡流水', null=True, blank=True, max_length=20)
    old_assigned_no=models.CharField('投胚流水号', null=False, blank=True, max_length=20)
    old_roll_no=models.CharField('箱号', null=False, blank=True, max_length=20)
    old_bar_code=models.CharField('胚纱条码', null=True, blank=True, max_length=50)
    old_rece_sheet_no=models.CharField('入库明细号', null=True, blank=True, max_length=20)
    old_length_qty=models.DecimalField('长度数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('重量数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_storage_unit_id=models.CharField('仓位代码', null=True, blank=True, max_length=10)
    old_status=models.CharField('状态', null=True, blank=True, max_length=10)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_gunit=models.IntegerField('GUnit', null=True, blank=True)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=4, decimal_places=1)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_packs=models.DecimalField('件数', null=True, blank=True, max_digits=4, decimal_places=1)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeGrayOutDetail', verbose_name='原关系：GrayOutDetail', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_grayoutrecord'
        indexes=[models.Index(fields=['source_batch', 'old_assigned_no', 'old_roll_no'],name='src_693e7060e2dd1e79'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_assigned_no'))),Upper(RTrim(models.F('old_roll_no'))),name='src_ci_693e7060e2dd1e79')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（GrayOutRecord，待确认）'
        ordering=["-id"]

class SourceDyeGrayPostionUp(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayPostionUp'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'JobSheetNo': 'old_job_sheet_no', 'SupplierID': 'old_supplier_id', 'CustomerID': 'old_customer_id', 'InSheetKind': 'old_in_sheet_kind', 'ProdID': 'old_prod_id', 'LotNo': 'old_lot_no', 'ColorID': 'old_color_id', 'PreField1': 'old_pre_field1', 'FixedQty': 'old_fixed_qty', 'PurchaseOrders': 'old_purchase_orders', 'A_A': 'old_a_a', 'A_B': 'old_a_b', 'Rolls': 'old_rolls', 'WeightQty': 'old_weight_qty', 'LengthQty': 'old_length_qty', 'Packs': 'old_packs', 'PCS': 'old_pcs', 'Area': 'old_area', 'NewArea': 'old_new_area', 'SheetStatus': 'old_sheet_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'InDetailNo': 'old_in_detail_no'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_supplier_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_in_sheet_kind': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_pre_field1': 'Chinese_PRC_CI_AS', 'old_purchase_orders': 'Chinese_PRC_CI_AS', 'old_a_a': 'Chinese_PRC_CI_AS', 'old_a_b': 'Chinese_PRC_CI_AS', 'old_area': 'Chinese_PRC_CI_AS', 'old_new_area': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_in_detail_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=36)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_supplier_id=models.CharField('供应商', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=50)
    old_in_sheet_kind=models.CharField('物料分类', null=True, blank=True, max_length=20)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=200)
    old_color_id=models.CharField('物料颜色', null=True, blank=True, max_length=50)
    old_pre_field1=models.CharField('捻度(H/S)', null=True, blank=True, max_length=50)
    old_fixed_qty=models.DecimalField('锭重', null=True, blank=True, max_digits=5, decimal_places=2)
    old_purchase_orders=models.CharField('采购单号', null=True, blank=True, max_length=20)
    old_a_a=models.CharField('物料区域', null=True, blank=True, max_length=50)
    old_a_b=models.CharField('物料等级', null=True, blank=True, max_length=100)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_weight_qty=models.DecimalField('重量数量', null=True, blank=True, max_digits=8, decimal_places=2)
    old_length_qty=models.DecimalField('长度数量', null=True, blank=True, max_digits=8, decimal_places=2)
    old_packs=models.DecimalField('件数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_pcs=models.IntegerField('粒/件', null=True, blank=True)
    old_area=models.CharField('原区域', null=True, blank=True, max_length=100)
    old_new_area=models.CharField('新区域', null=True, blank=True, max_length=100)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_step_no=models.IntegerField('流程节点号', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_in_detail_no=models.CharField('InDetailNo', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_graypostionup'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_f1651c2ae6f057f2'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_f1651c2ae6f057f2')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（GrayPostionUp，待确认）'
        ordering=["-id"]

class SourceDyeGrayRecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayRecord'
    SOURCE_FIELDS={'BarCode': 'old_bar_code', 'JobSheetNo': 'old_job_sheet_no', 'Qty': 'old_qty', 'CurrTime': 'old_curr_time', 'Geter': 'old_geter', 'StorageUnitID': 'old_storage_unit_id', 'IsInput': 'old_is_input'}
    SOURCE_KEY=('BarCode',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_bar_code': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_geter': 'Chinese_PRC_CI_AS', 'old_storage_unit_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_bar_code=models.CharField('条码', null=False, blank=True, max_length=50)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_qty=models.DecimalField('数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_curr_time=models.DateTimeField('CurrTime', null=True, blank=True)
    old_geter=models.CharField('收货员', null=True, blank=True, max_length=10)
    old_storage_unit_id=models.CharField('仓位', null=True, blank=True, max_length=10)
    old_is_input=models.BooleanField('IsInput', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_grayrecord'
        indexes=[models.Index(fields=['source_batch', 'old_bar_code'],name='src_011c31554a9a7218'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_bar_code'))),name='src_ci_011c31554a9a7218')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（GrayRecord，待确认）'
        ordering=["-id"]

class SourceDyeGrayRecordCutLogs(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayRecordCutLogs'
    SOURCE_FIELDS={'ID': 'old_id', 'Kind': 'old_kind', 'OriReceSheetNoList': 'old_ori_rece_sheet_no_list', 'NewReceSheetNoList': 'old_new_rece_sheet_no_list', 'OriRollNoList': 'old_ori_roll_no_list', 'NewRollNoList': 'old_new_roll_no_list', 'OriBarCodeList': 'old_ori_bar_code_list', 'NewBarCodeList': 'old_new_bar_code_list', 'OriQtyList': 'old_ori_qty_list', 'NewQtyList': 'old_new_qty_list', 'JobSheetNo': 'old_job_sheet_no', 'Operator': 'old_operator', 'OperateDate': 'old_operate_date', 'Status': 'old_status', 'Remarks': 'old_remarks', 'DataTableName': 'old_data_table_name'}
    SOURCE_KEY=('OperateDate', 'ID')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_id': 'Chinese_PRC_CI_AS', 'old_ori_rece_sheet_no_list': 'Chinese_PRC_CI_AS', 'old_new_rece_sheet_no_list': 'Chinese_PRC_CI_AS', 'old_ori_roll_no_list': 'Chinese_PRC_CI_AS', 'old_new_roll_no_list': 'Chinese_PRC_CI_AS', 'old_ori_bar_code_list': 'Chinese_PRC_CI_AS', 'old_new_bar_code_list': 'Chinese_PRC_CI_AS', 'old_ori_qty_list': 'Chinese_PRC_CI_AS', 'old_new_qty_list': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_operator': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_data_table_name': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_id=models.CharField('ID', null=False, blank=True, max_length=50)
    old_kind=models.IntegerField('Kind', null=False, blank=False)
    old_ori_rece_sheet_no_list=models.CharField('OriReceSheetNoList', null=True, blank=True, max_length=2000)
    old_new_rece_sheet_no_list=models.CharField('NewReceSheetNoList', null=True, blank=True, max_length=2000)
    old_ori_roll_no_list=models.CharField('OriRollNoList', null=True, blank=True, max_length=200)
    old_new_roll_no_list=models.CharField('NewRollNoList', null=True, blank=True, max_length=200)
    old_ori_bar_code_list=models.CharField('OriBarCodeList', null=True, blank=True, max_length=2000)
    old_new_bar_code_list=models.CharField('NewBarCodeList', null=True, blank=True, max_length=2000)
    old_ori_qty_list=models.CharField('OriQtyList', null=True, blank=True, max_length=1000)
    old_new_qty_list=models.CharField('NewQtyList', null=True, blank=True, max_length=1000)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)
    old_operator=models.CharField('Operator', null=True, blank=True, max_length=20)
    old_operate_date=models.DateTimeField('OperateDate', null=False, blank=False)
    old_status=models.IntegerField('Status', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_data_table_name=models.CharField('DataTableName', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_grayrecordcutlogs'
        indexes=[models.Index(fields=['source_batch', 'old_operate_date', 'old_id'],name='src_d9bfb89d5030414d'),models.Index(models.F('source_batch'),models.F('old_operate_date'),Upper(RTrim(models.F('old_id'))),name='src_ci_d9bfb89d5030414d')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（GrayRecordCutLogs，待确认）'
        ordering=["-id"]

class SourceDyeGrayStock(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayStock'
    SOURCE_FIELDS={'StockDate': 'old_stock_date', 'BusinessUnitID': 'old_business_unit_id', 'ColorID': 'old_color_id', 'CustomerID': 'old_customer_id', 'WareHouseID': 'old_ware_house_id', 'GrayKindID': 'old_gray_kind_id', 'SalerGroupID': 'old_saler_group_id', 'SupplierID': 'old_supplier_id', 'BusinessKind': 'old_business_kind', 'GrayID': 'old_gray_id', 'StockKind': 'old_stock_kind', 'SalerID': 'old_saler_id', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'PreMonthPacks': 'old_pre_month_packs', 'PreMonthRolls': 'old_pre_month_rolls', 'Price': 'old_price', 'CarryDate': 'old_carry_date', 'Remarks': 'old_remarks', 'PreMonthWeightQty': 'old_pre_month_weight_qty', 'PreMonthLengthQty': 'old_pre_month_length_qty', 'StorageUnitIDs': 'old_storage_unit_ids', 'ReceSheetNo': 'old_rece_sheet_no', 'PreField1': 'old_pre_field1', 'PurchaseOrders': 'old_purchase_orders', 'A_A': 'old_a_a', 'A_B': 'old_a_b', 'FixedQty': 'old_fixed_qty'}
    SOURCE_KEY=('StockDate', 'ColorID', 'CustomerID', 'WareHouseID', 'SupplierID', 'GrayID', 'SalerID', 'Spec', 'LotNo', 'ReceSheetNo', 'PreField1', 'PurchaseOrders', 'A_A', 'A_B', 'FixedQty')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_gray_kind_id': 'Chinese_PRC_CI_AS', 'old_saler_group_id': 'Chinese_PRC_CI_AS', 'old_supplier_id': 'Chinese_PRC_CI_AS', 'old_gray_id': 'Chinese_PRC_CI_AS', 'old_saler_id': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_storage_unit_ids': 'Chinese_PRC_CI_AS', 'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_pre_field1': 'Chinese_PRC_CI_AS', 'old_purchase_orders': 'Chinese_PRC_CI_AS', 'old_a_a': 'Chinese_PRC_CI_AS', 'old_a_b': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_stock_date=models.DateTimeField('StockDate', null=False, blank=False)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_color_id=models.CharField('ColorID', null=False, blank=True, max_length=20)
    old_customer_id=models.CharField('CustomerID', null=False, blank=True, max_length=10)
    old_ware_house_id=models.CharField('WareHouseID', null=False, blank=True, max_length=10)
    old_gray_kind_id=models.CharField('GrayKindID', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('SalerGroupID', null=True, blank=True, max_length=10)
    old_supplier_id=models.CharField('SupplierID', null=False, blank=True, max_length=10)
    old_business_kind=models.IntegerField('BusinessKind', null=True, blank=True)
    old_gray_id=models.CharField('GrayID', null=False, blank=True, max_length=50)
    old_stock_kind=models.IntegerField('StockKind', null=True, blank=True)
    old_saler_id=models.CharField('SalerID', null=False, blank=True, max_length=10)
    old_spec=models.CharField('Spec', null=False, blank=True, max_length=128)
    old_lot_no=models.CharField('LotNo', null=False, blank=True, max_length=50)
    old_pre_month_packs=models.DecimalField('PreMonthPacks', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pre_month_rolls=models.DecimalField('PreMonthRolls', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=8, decimal_places=2)
    old_carry_date=models.DateTimeField('CarryDate', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_pre_month_weight_qty=models.DecimalField('PreMonthWeightQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pre_month_length_qty=models.DecimalField('PreMonthLengthQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_storage_unit_ids=models.CharField('StorageUnitIDs', null=True, blank=True, max_length=100)
    old_rece_sheet_no=models.CharField('ReceSheetNo', null=False, blank=True, max_length=20)
    old_pre_field1=models.CharField('PreField1', null=False, blank=True, max_length=50)
    old_purchase_orders=models.CharField('PurchaseOrders', null=False, blank=True, max_length=20)
    old_a_a=models.CharField('A_A', null=False, blank=True, max_length=50)
    old_a_b=models.CharField('A_B', null=False, blank=True, max_length=100)
    old_fixed_qty=models.DecimalField('FixedQty', null=False, blank=False, max_digits=5, decimal_places=1)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_graystock'
        indexes=[models.Index(fields=['source_batch', 'old_stock_date', 'old_color_id', 'old_customer_id', 'old_ware_house_id', 'old_supplier_id', 'old_gray_id', 'old_saler_id', 'old_spec', 'old_lot_no', 'old_rece_sheet_no', 'old_pre_field1', 'old_purchase_orders', 'old_a_a', 'old_a_b', 'old_fixed_qty'],name='src_a92ae489977eedcb'),models.Index(models.F('source_batch'),models.F('old_stock_date'),Upper(RTrim(models.F('old_color_id'))),Upper(RTrim(models.F('old_customer_id'))),Upper(RTrim(models.F('old_ware_house_id'))),Upper(RTrim(models.F('old_supplier_id'))),Upper(RTrim(models.F('old_gray_id'))),Upper(RTrim(models.F('old_saler_id'))),Upper(RTrim(models.F('old_spec'))),Upper(RTrim(models.F('old_lot_no'))),Upper(RTrim(models.F('old_rece_sheet_no'))),Upper(RTrim(models.F('old_pre_field1'))),Upper(RTrim(models.F('old_purchase_orders'))),Upper(RTrim(models.F('old_a_a'))),Upper(RTrim(models.F('old_a_b'))),models.F('old_fixed_qty'),name='src_ci_a92ae489977eedcb')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（GrayStock，待确认）'
        ordering=["-id"]

class SourceDyeGrayStockAdjust(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayStockAdjust'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'BusinessUnitID': 'old_business_unit_id', 'BusinessKind': 'old_business_kind', 'GrayKindID': 'old_gray_kind_id', 'SalerGroupID': 'old_saler_group_id', 'CustomerID': 'old_customer_id', 'WareHouseID': 'old_ware_house_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_gray_kind_id': 'Chinese_PRC_CI_AS', 'old_saler_group_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类别', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位', null=True, blank=True, max_length=10)
    old_business_kind=models.IntegerField('业务类别', null=True, blank=True)
    old_gray_kind_id=models.CharField('胚纱类别', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('业务组别', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=10)
    old_ware_house_id=models.CharField('仓库代码', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_step_no=models.IntegerField('工作流节点号', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_graystockadjust'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_25f9b4cb95644fb0'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_25f9b4cb95644fb0')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（GrayStockAdjust，待确认）'
        ordering=["-id"]

class SourceDyeGrayStockAdjustDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayStockAdjustDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'JobSheetNo': 'old_job_sheet_no', 'CheckNo': 'old_check_no', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'PaperRolls': 'old_paper_rolls', 'RealRolls': 'old_real_rolls', 'AdjustRolls': 'old_adjust_rolls', 'Price': 'old_price', 'StockUnit': 'old_stock_unit', 'Remarks': 'old_remarks', 'GrayID': 'old_gray_id', 'PaperLength': 'old_paper_length', 'PaperWeight': 'old_paper_weight', 'RealLengthQty': 'old_real_length_qty', 'RealWeightQty': 'old_real_weight_qty', 'AdjustLengthQty': 'old_adjust_length_qty', 'AdjustWeightQty': 'old_adjust_weight_qty', 'StorageUnitIDs': 'old_storage_unit_ids', 'ReceSheetNo': 'old_rece_sheet_no', 'CustomerID': 'old_customer_id', 'AdjustPacks': 'old_adjust_packs', 'PaperPacks': 'old_paper_packs', 'RealPacks': 'old_real_packs', 'InSheetKind': 'old_in_sheet_kind', 'PreField1': 'old_pre_field1', 'PurchaseOrders': 'old_purchase_orders', 'A_A': 'old_a_a', 'A_B': 'old_a_b', 'FixedQty': 'old_fixed_qty'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_gray_id': 'Chinese_PRC_CI_AS', 'old_storage_unit_ids': 'Chinese_PRC_CI_AS', 'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_in_sheet_kind': 'Chinese_PRC_CI_AS', 'old_pre_field1': 'Chinese_PRC_CI_AS', 'old_purchase_orders': 'Chinese_PRC_CI_AS', 'old_a_a': 'Chinese_PRC_CI_AS', 'old_a_b': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：GrayStockAdjust', 'target': 'erp_warehouse.SourceDyeGrayStockAdjust', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 GrayStockAdjustDetail → GrayStockAdjust']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('调整明细单号', null=False, blank=True, max_length=36)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_check_no=models.CharField('订单明细号', null=True, blank=True, max_length=20)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=128)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('物料颜色', null=True, blank=True, max_length=20)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=20)
    old_paper_rolls=models.DecimalField('帐面粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_rolls=models.DecimalField('实际粒数', null=True, blank=True, max_digits=16, decimal_places=2)
    old_adjust_rolls=models.DecimalField('调整粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=8, decimal_places=2)
    old_stock_unit=models.IntegerField('库存单位', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_gray_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_paper_length=models.DecimalField('账面长度', null=True, blank=True, max_digits=10, decimal_places=5)
    old_paper_weight=models.DecimalField('账面重量', null=True, blank=True, max_digits=10, decimal_places=5)
    old_real_length_qty=models.DecimalField('实际长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_weight_qty=models.DecimalField('实际重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_adjust_length_qty=models.DecimalField('调整长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_adjust_weight_qty=models.DecimalField('调整重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_storage_unit_ids=models.CharField('库位', null=True, blank=True, max_length=100)
    old_rece_sheet_no=models.CharField('入库明细号', null=True, blank=True, max_length=20)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=50)
    old_adjust_packs=models.DecimalField('调整件数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_paper_packs=models.DecimalField('账面件数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_packs=models.DecimalField('实际件数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_in_sheet_kind=models.CharField('物料分类', null=True, blank=True, max_length=20)
    old_pre_field1=models.CharField('捻度(H/S)', null=True, blank=True, max_length=50)
    old_purchase_orders=models.CharField('采购单号', null=True, blank=True, max_length=20)
    old_a_a=models.CharField('物料区域', null=True, blank=True, max_length=50)
    old_a_b=models.CharField('物料等级', null=True, blank=True, max_length=100)
    old_fixed_qty=models.DecimalField('锭重', null=True, blank=True, max_digits=5, decimal_places=2)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeGrayStockAdjust', verbose_name='原关系：GrayStockAdjust', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_graystockadjustdetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_ac4856e3db1c9b2a'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_ac4856e3db1c9b2a')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（GrayStockAdjustDetail，待确认）'
        ordering=["-id"]

class SourceDyeGrayStockAllot(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayStockAllot'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'GrayKindID': 'old_gray_kind_id', 'FromSaleGroupID': 'old_from_sale_group_id', 'ToSalerGroupID': 'old_to_saler_group_id', 'FromWareHouseID': 'old_from_ware_house_id', 'FromCustomerID': 'old_from_customer_id', 'ToCustomerID': 'old_to_customer_id', 'FromReceSheetNo': 'old_from_rece_sheet_no', 'ToWareHouseID': 'old_to_ware_house_id', 'Rolls': 'old_rolls', 'Packs': 'old_packs', 'WeightQty': 'old_weight_qty', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'FromBusinessUnitID': 'old_from_business_unit_id', 'ToBusinessUnitID': 'old_to_business_unit_id', 'FromSalerID': 'old_from_saler_id', 'ToSalerID': 'old_to_saler_id', 'FromLotNo': 'old_from_lot_no', 'ToLotNo': 'old_to_lot_no', 'FromSpec': 'old_from_spec', 'ToSpec': 'old_to_spec', 'FromPrice': 'old_from_price', 'ToPrice': 'old_to_price', 'FromStructure': 'old_from_structure', 'ToStructure': 'old_to_structure', 'StepNo': 'old_step_no', 'BusinessKind': 'old_business_kind', 'FromGrayID': 'old_from_gray_id', 'ToGrayID': 'old_to_gray_id', 'StockUnit': 'old_stock_unit', 'FromSheetKind': 'old_from_sheet_kind', 'LengthQty': 'old_length_qty', 'ToReceSheetNo': 'old_to_rece_sheet_no', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'AssignedNo': 'old_assigned_no'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_gray_kind_id': 'Chinese_PRC_CI_AS', 'old_from_sale_group_id': 'Chinese_PRC_CI_AS', 'old_to_saler_group_id': 'Chinese_PRC_CI_AS', 'old_from_ware_house_id': 'Chinese_PRC_CI_AS', 'old_from_customer_id': 'Chinese_PRC_CI_AS', 'old_to_customer_id': 'Chinese_PRC_CI_AS', 'old_from_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_to_ware_house_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_from_business_unit_id': 'Chinese_PRC_CI_AS', 'old_to_business_unit_id': 'Chinese_PRC_CI_AS', 'old_from_saler_id': 'Chinese_PRC_CI_AS', 'old_to_saler_id': 'Chinese_PRC_CI_AS', 'old_from_lot_no': 'Chinese_PRC_CI_AS', 'old_to_lot_no': 'Chinese_PRC_CI_AS', 'old_from_spec': 'Chinese_PRC_CI_AS', 'old_to_spec': 'Chinese_PRC_CI_AS', 'old_from_structure': 'Chinese_PRC_CI_AS', 'old_to_structure': 'Chinese_PRC_CI_AS', 'old_from_gray_id': 'Chinese_PRC_CI_AS', 'old_to_gray_id': 'Chinese_PRC_CI_AS', 'old_to_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_assigned_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_gray_kind_id=models.CharField('胚纱类别', null=True, blank=True, max_length=10)
    old_from_sale_group_id=models.CharField('来源业务组别', null=True, blank=True, max_length=10)
    old_to_saler_group_id=models.CharField('目标业务组别', null=True, blank=True, max_length=10)
    old_from_ware_house_id=models.CharField('来源仓库', null=True, blank=True, max_length=10)
    old_from_customer_id=models.CharField('来源客户', null=True, blank=True, max_length=10)
    old_to_customer_id=models.CharField('目标客户', null=True, blank=True, max_length=10)
    old_from_rece_sheet_no=models.CharField('来源收纱明细编号', null=True, blank=True, max_length=20)
    old_to_ware_house_id=models.CharField('目标仓库', null=True, blank=True, max_length=10)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_packs=models.DecimalField('件数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_weight_qty=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_from_business_unit_id=models.CharField('来源经营单位', null=True, blank=True, max_length=10)
    old_to_business_unit_id=models.CharField('目标经营单位', null=True, blank=True, max_length=10)
    old_from_saler_id=models.CharField('来源业务员', null=True, blank=True, max_length=10)
    old_to_saler_id=models.CharField('目标业务员', null=True, blank=True, max_length=10)
    old_from_lot_no=models.CharField('来源批号', null=True, blank=True, max_length=50)
    old_to_lot_no=models.CharField('目标批号', null=True, blank=True, max_length=50)
    old_from_spec=models.CharField('来源规格', null=True, blank=True, max_length=50)
    old_to_spec=models.CharField('目标规格', null=True, blank=True, max_length=50)
    old_from_price=models.DecimalField('来源价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_to_price=models.DecimalField('目标价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_from_structure=models.CharField('来源组织', null=True, blank=True, max_length=50)
    old_to_structure=models.CharField('目标组织', null=True, blank=True, max_length=50)
    old_step_no=models.IntegerField('工作流节点号', null=True, blank=True)
    old_business_kind=models.IntegerField('BusinessKind', null=True, blank=True)
    old_from_gray_id=models.CharField('来原品名', null=True, blank=True, max_length=10)
    old_to_gray_id=models.CharField('目标品名', null=True, blank=True, max_length=10)
    old_stock_unit=models.IntegerField('StockUnit', null=True, blank=True)
    old_from_sheet_kind=models.IntegerField('来源单据类型', null=True, blank=True)
    old_length_qty=models.DecimalField('长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_to_rece_sheet_no=models.CharField('目标收胚明细号', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_assigned_no=models.CharField('AssignedNo', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_graystockallot'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_4a7f0e98c49a1424'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_4a7f0e98c49a1424')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（GrayStockAllot，待确认）'
        ordering=["-id"]

class SourceDyeGrayStockBook(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayStockBook'
    SOURCE_FIELDS={'BookNo': 'old_book_no', 'BookKind': 'old_book_kind', 'GrayKindID': 'old_gray_kind_id', 'BusinessUnitID': 'old_business_unit_id', 'BusinessKind': 'old_business_kind', 'GradeID': 'old_grade_id', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'SupplierID': 'old_supplier_id', 'CustomerID': 'old_customer_id', 'FactID': 'old_fact_id', 'WareHouseID': 'old_ware_house_id', 'StorageUnitIDs': 'old_storage_unit_ids', 'GrayID': 'old_gray_id', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'SalerGroupID': 'old_saler_group_id', 'SalerID': 'old_saler_id', 'CheckNo': 'old_check_no', 'SheetNo': 'old_sheet_no', 'DetailNo': 'old_detail_no', 'JobSheetNo': 'old_job_sheet_no', 'InRolls': 'old_in_rolls', 'InPacks': 'old_in_packs', 'OutRolls': 'old_out_rolls', 'OutPacks': 'old_out_packs', 'Price': 'old_price', 'Remarks': 'old_remarks', 'BookDate': 'old_book_date', 'AccDate': 'old_acc_date', 'ReceSheetNo': 'old_rece_sheet_no', 'Memo': 'old_memo', 'StockFlag': 'old_stock_flag', 'StockKind': 'old_stock_kind', 'SheetKind': 'old_sheet_kind', 'InLengthQty': 'old_in_length_qty', 'InWeightQty': 'old_in_weight_qty', 'OutWeightQty': 'old_out_weight_qty', 'OutLengthQty': 'old_out_length_qty', 'SheetSeries': 'old_sheet_series', 'InMoney': 'old_in_money', 'OutMoney': 'old_out_money', 'CurrDate': 'old_curr_date', 'InSheetKind': 'old_in_sheet_kind', 'PreField1': 'old_pre_field1', 'PurchaseOrders': 'old_purchase_orders', 'A_A': 'old_a_a', 'A_B': 'old_a_b', 'FixedQty': 'old_fixed_qty'}
    SOURCE_KEY=('BookNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_gray_kind_id': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_grade_id': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_supplier_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_fact_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_storage_unit_ids': 'Chinese_PRC_CI_AS', 'old_gray_id': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_saler_group_id': 'Chinese_PRC_CI_AS', 'old_saler_id': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_memo': 'Chinese_PRC_CI_AS', 'old_stock_flag': 'Chinese_PRC_CI_AS', 'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_in_sheet_kind': 'Chinese_PRC_CI_AS', 'old_pre_field1': 'Chinese_PRC_CI_AS', 'old_purchase_orders': 'Chinese_PRC_CI_AS', 'old_a_a': 'Chinese_PRC_CI_AS', 'old_a_b': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_acc_date': ('literal', '1900-01-01'), 'old_rece_sheet_no': ('literal', '')}
    SOURCE_IDENTITIES=('old_book_no',)
    SOURCE_IDENTITY_RULES={'old_book_no': (1, 1)}
    old_book_no=models.BigIntegerField('BookNo', null=False, blank=False)
    old_book_kind=models.IntegerField('BookKind', null=True, blank=True)
    old_gray_kind_id=models.CharField('GrayKindID', null=True, blank=True, max_length=10)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_business_kind=models.IntegerField('BusinessKind', null=True, blank=True)
    old_grade_id=models.CharField('GradeID', null=True, blank=True, max_length=10)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=20)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=20)
    old_supplier_id=models.CharField('SupplierID', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=10)
    old_fact_id=models.CharField('FactID', null=True, blank=True, max_length=10)
    old_ware_house_id=models.CharField('WareHouseID', null=True, blank=True, max_length=10)
    old_storage_unit_ids=models.CharField('StorageUnitIDs', null=True, blank=True, max_length=100)
    old_gray_id=models.CharField('GrayID', null=True, blank=True, max_length=50)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=128)
    old_lot_no=models.CharField('LotNo', null=True, blank=True, max_length=50)
    old_saler_group_id=models.CharField('SalerGroupID', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('SalerID', null=True, blank=True, max_length=10)
    old_check_no=models.CharField('CheckNo', null=True, blank=True, max_length=20)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=True, blank=True, max_length=36)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)
    old_in_rolls=models.DecimalField('InRolls', null=True, blank=True, max_digits=7, decimal_places=2)
    old_in_packs=models.DecimalField('InPacks', null=True, blank=True, max_digits=7, decimal_places=2)
    old_out_rolls=models.DecimalField('OutRolls', null=True, blank=True, max_digits=7, decimal_places=2)
    old_out_packs=models.DecimalField('OutPacks', null=True, blank=True, max_digits=7, decimal_places=2)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=8, decimal_places=2)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_book_date=models.DateTimeField('BookDate', null=True, blank=True)
    old_acc_date=models.DateTimeField('AccDate', null=True, blank=True)
    old_rece_sheet_no=models.CharField('ReceSheetNo', null=True, blank=True, max_length=20)
    old_memo=models.CharField('Memo', null=True, blank=True, max_length=100)
    old_stock_flag=models.CharField('StockFlag', null=True, blank=True, max_length=1)
    old_stock_kind=models.IntegerField('StockKind', null=True, blank=True)
    old_sheet_kind=models.IntegerField('SheetKind', null=True, blank=True)
    old_in_length_qty=models.DecimalField('InLengthQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_in_weight_qty=models.DecimalField('InWeightQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_out_weight_qty=models.DecimalField('OutWeightQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_out_length_qty=models.DecimalField('OutLengthQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sheet_series=models.CharField('SheetSeries', null=True, blank=True, max_length=50)
    old_in_money=models.DecimalField('InMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_out_money=models.DecimalField('OutMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_curr_date=models.DateTimeField('CurrDate', null=True, blank=True)
    old_in_sheet_kind=models.CharField('InSheetKind', null=True, blank=True, max_length=20)
    old_pre_field1=models.CharField('PreField1', null=True, blank=True, max_length=50)
    old_purchase_orders=models.CharField('PurchaseOrders', null=True, blank=True, max_length=20)
    old_a_a=models.CharField('A_A', null=True, blank=True, max_length=50)
    old_a_b=models.CharField('A_B', null=True, blank=True, max_length=100)
    old_fixed_qty=models.DecimalField('FixedQty', null=True, blank=True, max_digits=5, decimal_places=2)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_graystockbook'
        indexes=[models.Index(fields=['source_batch', 'old_book_no'],name='src_ad70bc572eb9c532')]
        verbose_name=verbose_name_plural='坯布库存流水'
        ordering=["-id"]

class SourceDyeGrayStockCheck(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayStockCheck'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'GrayKindID': 'old_gray_kind_id', 'BusinessUnitID': 'old_business_unit_id', 'SalerGroupID': 'old_saler_group_id', 'WareHouseID': 'old_ware_house_id', 'CustomerID': 'old_customer_id', 'FactID': 'old_fact_id', 'CheckNo': 'old_check_no', 'JobDetailNo': 'old_job_detail_no', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'PaperRolls': 'old_paper_rolls', 'PaperPacks': 'old_paper_packs', 'PaperQty': 'old_paper_qty', 'AdjustPacks': 'old_adjust_packs', 'AdjustQty': 'old_adjust_qty', 'AdjustRolls': 'old_adjust_rolls', 'Price': 'old_price', 'StockUnit': 'old_stock_unit', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'FlowID': 'old_flow_id', 'StepNo': 'old_step_no', 'ReceSheetNo': 'old_rece_sheet_no', 'BusinessKind': 'old_business_kind', 'SalerID': 'old_saler_id', 'GrayID': 'old_gray_id'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_gray_kind_id': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_saler_group_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_fact_id': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_job_detail_no': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_flow_id': 'Chinese_PRC_CI_AS', 'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_saler_id': 'Chinese_PRC_CI_AS', 'old_gray_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_sheet_kind=models.IntegerField('SheetKind', null=True, blank=True)
    old_gray_kind_id=models.CharField('GrayKindID', null=True, blank=True, max_length=10)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('业务组别', null=True, blank=True, max_length=10)
    old_ware_house_id=models.CharField('仓库代码', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户代码', null=True, blank=True, max_length=10)
    old_fact_id=models.CharField('FactID', null=True, blank=True, max_length=10)
    old_check_no=models.CharField('CheckNo', null=True, blank=True, max_length=20)
    old_job_detail_no=models.CharField('JobDetailNo', null=True, blank=True, max_length=20)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=50)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=50)
    old_paper_rolls=models.DecimalField('帐面粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_paper_packs=models.DecimalField('PaperPacks', null=True, blank=True, max_digits=10, decimal_places=2)
    old_paper_qty=models.DecimalField('PaperQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_adjust_packs=models.DecimalField('AdjustPacks', null=True, blank=True, max_digits=7, decimal_places=2)
    old_adjust_qty=models.DecimalField('AdjustQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_adjust_rolls=models.DecimalField('调整粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=8, decimal_places=2)
    old_stock_unit=models.IntegerField('StockUnit', null=True, blank=True)
    old_sheet_status=models.IntegerField('SheetStatus', null=True, blank=True)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_print_times=models.IntegerField('PrintTimes', null=True, blank=True)
    old_revisions=models.IntegerField('Revisions', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=100)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_flow_id=models.CharField('FlowID', null=True, blank=True, max_length=10)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_rece_sheet_no=models.CharField('入库明细号', null=True, blank=True, max_length=20)
    old_business_kind=models.IntegerField('BusinessKind', null=True, blank=True)
    old_saler_id=models.CharField('SalerID', null=True, blank=True, max_length=10)
    old_gray_id=models.CharField('本厂规格', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_graystockcheck'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_d0666e21cb375622'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_d0666e21cb375622')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（GrayStockCheck，待确认）'
        ordering=["-id"]

class SourceDyeGrayStockSpecUp(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayStockSpecUp'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'GrayKindID': 'old_gray_kind_id', 'BusinessUnitID': 'old_business_unit_id', 'WareHouseID': 'old_ware_house_id', 'SalerID': 'old_saler_id', 'FactID': 'old_fact_id', 'StockUnit': 'old_stock_unit', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'StepNo': 'old_step_no', 'BusinessKind': 'old_business_kind', 'CarNo': 'old_car_no', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'FabricID': 'old_fabric_id', 'SalerGroupID': 'old_saler_group_id'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_gray_kind_id': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_saler_id': 'Chinese_PRC_CI_AS', 'old_fact_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_car_no': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_fabric_id': 'Chinese_PRC_CI_AS', 'old_saler_group_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=False, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类别', null=True, blank=True)
    old_gray_kind_id=models.CharField('胚纱类别', null=True, blank=True, max_length=10)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_ware_house_id=models.CharField('仓库代码', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('业务员', null=True, blank=True, max_length=10)
    old_fact_id=models.CharField('工厂代码', null=True, blank=True, max_length=1000)
    old_stock_unit=models.IntegerField('库存单位', null=True, blank=True)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_step_no=models.IntegerField('工作流节点号', null=True, blank=True)
    old_business_kind=models.IntegerField('业务类别', null=True, blank=True)
    old_car_no=models.CharField('配纱员', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_fabric_id=models.CharField('客户规格', null=True, blank=True, max_length=50)
    old_saler_group_id=models.CharField('SalerGroupID', null=True, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_graystockspecup'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_e08fbd4e7a3510bd'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_e08fbd4e7a3510bd')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（GrayStockSpecUp，待确认）'
        ordering=["-id"]

class SourceDyeGrayStockSpecUpDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayStockSpecUpDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'AssignedNo': 'old_assigned_no', 'ReceSheetNo': 'old_rece_sheet_no', 'PCS': 'old_pcs', 'Rolls': 'old_rolls', 'Packs': 'old_packs', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'Price': 'old_price', 'CheckNo': 'old_check_no', 'Remarks': 'old_remarks', 'Area': 'old_area', 'StorageUnitIDs': 'old_storage_unit_ids', 'WareHouseID': 'old_ware_house_id', 'CustomerID': 'old_customer_id', 'InSheetKind': 'old_in_sheet_kind', 'GrayID': 'old_gray_id', 'LotNo': 'old_lot_no', 'ColorID': 'old_color_id', 'FixedQty': 'old_fixed_qty', 'SupplierID': 'old_supplier_id', 'PreField1': 'old_pre_field1', 'PurchaseOrders': 'old_purchase_orders', 'A_A': 'old_a_a', 'A_B': 'old_a_b', 'UPCustomerID': 'old_upcustomer_id', 'UPInSheetKind': 'old_upin_sheet_kind', 'UPGrayID': 'old_upgray_id', 'UPLotNo': 'old_uplot_no', 'UPColorID': 'old_upcolor_id', 'UPFixedQty': 'old_upfixed_qty', 'UPPreField1': 'old_uppre_field1', 'UPPurchaseOrders': 'old_uppurchase_orders', 'UPA_A': 'old_upa_a', 'UPA_B': 'old_upa_b'}
    SOURCE_KEY=('AssignedNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_assigned_no': 'Chinese_PRC_CI_AS', 'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_area': 'Chinese_PRC_CI_AS', 'old_storage_unit_ids': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_in_sheet_kind': 'Chinese_PRC_CI_AS', 'old_gray_id': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_supplier_id': 'Chinese_PRC_CI_AS', 'old_pre_field1': 'Chinese_PRC_CI_AS', 'old_purchase_orders': 'Chinese_PRC_CI_AS', 'old_a_a': 'Chinese_PRC_CI_AS', 'old_a_b': 'Chinese_PRC_CI_AS', 'old_upcustomer_id': 'Chinese_PRC_CI_AS', 'old_upin_sheet_kind': 'Chinese_PRC_CI_AS', 'old_upgray_id': 'Chinese_PRC_CI_AS', 'old_uplot_no': 'Chinese_PRC_CI_AS', 'old_upcolor_id': 'Chinese_PRC_CI_AS', 'old_uppre_field1': 'Chinese_PRC_CI_AS', 'old_uppurchase_orders': 'Chinese_PRC_CI_AS', 'old_upa_a': 'Chinese_PRC_CI_AS', 'old_upa_b': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：GrayStockSpecUp', 'target': 'erp_warehouse.SourceDyeGrayStockSpecUp', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 GrayStockSpecUpDetail → GrayStockSpecUp']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_assigned_no=models.CharField('出库明细号', null=False, blank=True, max_length=20)
    old_rece_sheet_no=models.CharField('入库明细号', null=True, blank=True, max_length=20)
    old_pcs=models.IntegerField('粒/件', null=True, blank=True)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_packs=models.DecimalField('件数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_length_qty=models.DecimalField('长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_check_no=models.CharField('订单明细号', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_area=models.CharField('区域', null=True, blank=True, max_length=100)
    old_storage_unit_ids=models.CharField('库位', null=True, blank=True, max_length=100)
    old_ware_house_id=models.CharField('仓库', null=True, blank=True, max_length=20)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=30)
    old_in_sheet_kind=models.CharField('物料分类', null=True, blank=True, max_length=20)
    old_gray_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('物料颜色', null=True, blank=True, max_length=20)
    old_fixed_qty=models.DecimalField('锭重', null=True, blank=True, max_digits=5, decimal_places=2)
    old_supplier_id=models.CharField('供应商', null=True, blank=True, max_length=30)
    old_pre_field1=models.CharField('捻度(H/S)', null=True, blank=True, max_length=50)
    old_purchase_orders=models.CharField('采购单号', null=True, blank=True, max_length=20)
    old_a_a=models.CharField('物料区域', null=True, blank=True, max_length=50)
    old_a_b=models.CharField('物料等级', null=True, blank=True, max_length=100)
    old_upcustomer_id=models.CharField('调整客户', null=True, blank=True, max_length=30)
    old_upin_sheet_kind=models.CharField('调整物料分类', null=True, blank=True, max_length=20)
    old_upgray_id=models.CharField('调整规格', null=True, blank=True, max_length=50)
    old_uplot_no=models.CharField('调整批号', null=True, blank=True, max_length=50)
    old_upcolor_id=models.CharField('调整物料颜色', null=True, blank=True, max_length=20)
    old_upfixed_qty=models.DecimalField('调整锭重', null=True, blank=True, max_digits=5, decimal_places=2)
    old_uppre_field1=models.CharField('调整捻度(H/S)', null=True, blank=True, max_length=50)
    old_uppurchase_orders=models.CharField('调整采购单号', null=True, blank=True, max_length=20)
    old_upa_a=models.CharField('调整物料区域', null=True, blank=True, max_length=50)
    old_upa_b=models.CharField('调整物料等级', null=True, blank=True, max_length=100)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeGrayStockSpecUp', verbose_name='原关系：GrayStockSpecUp', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_graystockspecupdetail'
        indexes=[models.Index(fields=['source_batch', 'old_assigned_no'],name='src_923fa2221d507ce1'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_assigned_no'))),name='src_ci_923fa2221d507ce1')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（GrayStockSpecUpDetail，待确认）'
        ordering=["-id"]

class SourceDyeGrayStorageAdjust(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayStorageAdjust'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetKind': 'old_sheet_kind', 'SheetDate': 'old_sheet_date', 'StepNo': 'old_step_no', 'RightStatus': 'old_right_status', 'SheetStatus': 'old_sheet_status', 'SalerID': 'old_saler_id', 'CustomerID': 'old_customer_id', 'WareHouseID': 'old_ware_house_id', 'ToWareHouseID': 'old_to_ware_house_id', 'PrintTimes': 'old_print_times', 'CarryerID': 'old_carryer_id', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'Approved': 'old_approved', 'ApproveDate': 'old_approve_date', 'Remarks': 'old_remarks', 'CarryerID1': 'old_carryer_id1', 'CarryerID2': 'old_carryer_id2', 'CarryerID3': 'old_carryer_id3', 'CarryerID4': 'old_carryer_id4'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_saler_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_to_ware_house_id': 'Chinese_PRC_CI_AS', 'old_carryer_id': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_carryer_id1': 'Chinese_PRC_CI_AS', 'old_carryer_id2': 'Chinese_PRC_CI_AS', 'old_carryer_id3': 'Chinese_PRC_CI_AS', 'old_carryer_id4': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('单据号', null=True, blank=True, max_length=20)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_sheet_status=models.IntegerField('SheetStatus', null=True, blank=True)
    old_saler_id=models.CharField('业务员', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=10)
    old_ware_house_id=models.CharField('调出仓库', null=True, blank=True, max_length=10)
    old_to_ware_house_id=models.CharField('调入仓库', null=True, blank=True, max_length=10)
    old_print_times=models.IntegerField('PrintTimes', null=True, blank=True)
    old_carryer_id=models.CharField('搬运工', null=True, blank=True, max_length=20)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_approved=models.BooleanField('Approved', null=True, blank=True)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_carryer_id1=models.CharField('CarryerID1', null=True, blank=True, max_length=20)
    old_carryer_id2=models.CharField('CarryerID2', null=True, blank=True, max_length=20)
    old_carryer_id3=models.CharField('CarryerID3', null=True, blank=True, max_length=20)
    old_carryer_id4=models.CharField('CarryerID4', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_graystorageadjust'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_ecfe8671902330af'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_ecfe8671902330af')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（GrayStorageAdjust，待确认）'
        ordering=["-id"]

class SourceDyeGrayStorageAdjustDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayStorageAdjustDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'ReceSheetNo': 'old_rece_sheet_no', 'FromReceSheetNo': 'old_from_rece_sheet_no', 'GrayID': 'old_gray_id', 'LotNo': 'old_lot_no', 'Spec': 'old_spec', 'StorageUnitIDs': 'old_storage_unit_ids', 'ToStorageUnitIDs': 'old_to_storage_unit_ids', 'Rolls': 'old_rolls', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'Remarks': 'old_remarks', 'Area': 'old_area', 'ToArea': 'old_to_area', 'CustJobNo': 'old_cust_job_no', 'InSheetKind': 'old_in_sheet_kind', 'PreField1': 'old_pre_field1', 'PurchaseOrders': 'old_purchase_orders', 'A_A': 'old_a_a', 'A_B': 'old_a_b'}
    SOURCE_KEY=('SheetSeries', 'DetailNo', 'FromReceSheetNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_from_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_gray_id': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_storage_unit_ids': 'Chinese_PRC_CI_AS', 'old_to_storage_unit_ids': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_area': 'Chinese_PRC_CI_AS', 'old_to_area': 'Chinese_PRC_CI_AS', 'old_cust_job_no': 'Chinese_PRC_CI_AS', 'old_in_sheet_kind': 'Chinese_PRC_CI_AS', 'old_pre_field1': 'Chinese_PRC_CI_AS', 'old_purchase_orders': 'Chinese_PRC_CI_AS', 'old_a_a': 'Chinese_PRC_CI_AS', 'old_a_b': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：GrayStorageAdjust', 'target': 'erp_warehouse.SourceDyeGrayStorageAdjust', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 GrayStorageAdjustDetail → GrayStorageAdjust']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('明细号', null=False, blank=True, max_length=36)
    old_rece_sheet_no=models.CharField('入库明细号', null=True, blank=True, max_length=100)
    old_from_rece_sheet_no=models.CharField('转仓明细', null=False, blank=True, max_length=20)
    old_gray_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=200)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=200)
    old_storage_unit_ids=models.CharField('调出库位', null=True, blank=True, max_length=100)
    old_to_storage_unit_ids=models.CharField('调入库位', null=True, blank=True, max_length=100)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_length_qty=models.DecimalField('长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_area=models.CharField('调出区域', null=True, blank=True, max_length=100)
    old_to_area=models.CharField('调入区域', null=True, blank=True, max_length=100)
    old_cust_job_no=models.CharField('收料编号', null=True, blank=True, max_length=50)
    old_in_sheet_kind=models.CharField('InSheetKind', null=True, blank=True, max_length=20)
    old_pre_field1=models.CharField('PreField1', null=True, blank=True, max_length=50)
    old_purchase_orders=models.CharField('PurchaseOrders', null=True, blank=True, max_length=20)
    old_a_a=models.CharField('A_A', null=True, blank=True, max_length=50)
    old_a_b=models.CharField('A_B', null=True, blank=True, max_length=100)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeGrayStorageAdjust', verbose_name='原关系：GrayStorageAdjust', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_graystorageadjustdetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no', 'old_from_rece_sheet_no'],name='src_edb4dbf998f001b0'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),Upper(RTrim(models.F('old_from_rece_sheet_no'))),name='src_ci_edb4dbf998f001b0')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（GrayStorageAdjustDetail，待确认）'
        ordering=["-id"]

class SourceDyeGrayStorageAdjustRecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GrayStorageAdjustRecord'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'RollNo': 'old_roll_no', 'ReceSheetNo': 'old_rece_sheet_no', 'FromReceSheetNo': 'old_from_rece_sheet_no', 'BarCode': 'old_bar_code', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'StorageUnitID': 'old_storage_unit_id', 'ToStorageUnitID': 'old_to_storage_unit_id', 'Remarks': 'old_remarks', 'RollNo2': 'old_roll_no2', 'Rolls': 'old_rolls'}
    SOURCE_KEY=('SheetSeries', 'DetailNo', 'RollNo', 'FromReceSheetNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_roll_no': 'Chinese_PRC_CI_AS', 'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_from_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_bar_code': 'Chinese_PRC_CI_AS', 'old_storage_unit_id': 'Chinese_PRC_CI_AS', 'old_to_storage_unit_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_roll_no2': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：GrayStorageAdjustDetail', 'target': 'erp_warehouse.SourceDyeGrayStorageAdjustDetail', 'source_fields': ['SheetSeries', 'DetailNo', 'FromReceSheetNo'], 'target_fields': ['SheetSeries', 'DetailNo', 'FromReceSheetNo'], 'evidence': ['原界面主从 GrayStorageAdjustRecord → GrayStorageAdjustDetail']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('明细号', null=False, blank=True, max_length=36)
    old_roll_no=models.CharField('箱号', null=False, blank=True, max_length=20)
    old_rece_sheet_no=models.CharField('入库明细号', null=True, blank=True, max_length=100)
    old_from_rece_sheet_no=models.CharField('转仓明细', null=False, blank=True, max_length=20)
    old_bar_code=models.CharField('条码', null=True, blank=True, max_length=100)
    old_length_qty=models.DecimalField('长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_storage_unit_id=models.CharField('调出库位', null=True, blank=True, max_length=100)
    old_to_storage_unit_id=models.CharField('调入库位', null=True, blank=True, max_length=100)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_roll_no2=models.CharField('RollNo2', null=True, blank=True, max_length=50)
    old_rolls=models.FloatField('粒数', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeGrayStorageAdjustDetail', verbose_name='原关系：GrayStorageAdjustDetail', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_graystorageadjustrecord'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no', 'old_roll_no', 'old_from_rece_sheet_no'],name='src_a8a6595d6ae3f633'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),Upper(RTrim(models.F('old_roll_no'))),Upper(RTrim(models.F('old_from_rece_sheet_no'))),name='src_ci_a8a6595d6ae3f633')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（GrayStorageAdjustRecord，待确认）'
        ordering=["-id"]

class SourceDyeODMIn(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ODMIn'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetKind': 'old_sheet_kind', 'SheetType': 'old_sheet_type', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'StepNo': 'old_step_no', 'SheetDate': 'old_sheet_date', 'CustomerID': 'old_customer_id', 'BusinessUnitID': 'old_business_unit_id', 'Keeper': 'old_keeper', 'Driver': 'old_driver', 'CarNo': 'old_car_no', 'CarryerID': 'old_carryer_id', 'WareHouseID': 'old_ware_house_id', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Remarks': 'old_remarks', 'StockUnit': 'old_stock_unit', 'Cargador1': 'old_cargador1', 'Cargador2': 'old_cargador2', 'Cargador3': 'old_cargador3', 'Cargador4': 'old_cargador4', 'Cargador5': 'old_cargador5'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_keeper': 'Chinese_PRC_CI_AS', 'old_driver': 'Chinese_PRC_CI_AS', 'old_car_no': 'Chinese_PRC_CI_AS', 'old_carryer_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_cargador1': 'Chinese_PRC_CI_AS', 'old_cargador2': 'Chinese_PRC_CI_AS', 'old_cargador3': 'Chinese_PRC_CI_AS', 'old_cargador4': 'Chinese_PRC_CI_AS', 'old_cargador5': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_sheet_type=models.IntegerField('单据类型', null=True, blank=True)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_step_no=models.IntegerField('流程节点号', null=True, blank=True)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_customer_id=models.CharField('客户代码', null=True, blank=True, max_length=10)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_keeper=models.CharField('仓管员', null=True, blank=True, max_length=100)
    old_driver=models.CharField('司机', null=True, blank=True, max_length=20)
    old_car_no=models.CharField('车牌号', null=True, blank=True, max_length=20)
    old_carryer_id=models.CharField('搬运工1', null=True, blank=True, max_length=20)
    old_ware_house_id=models.CharField('仓库代码', null=True, blank=True, max_length=10)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_stock_unit=models.IntegerField('库存单位', null=True, blank=True)
    old_cargador1=models.CharField('搬运工2', null=True, blank=True, max_length=10)
    old_cargador2=models.CharField('搬运工3', null=True, blank=True, max_length=10)
    old_cargador3=models.CharField('搬运工4', null=True, blank=True, max_length=10)
    old_cargador4=models.CharField('Cargador4', null=True, blank=True, max_length=10)
    old_cargador5=models.CharField('Cargador5', null=True, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_odmin'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_752366991d1e2142'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_752366991d1e2142')]
        verbose_name=verbose_name_plural='其他或待确认相关表（ODMIn，待确认）'
        ordering=["-id"]

class SourceDyeODMInDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ODMInDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'OutDetailNo': 'old_out_detail_no', 'JobSheetNo': 'old_job_sheet_no', 'InRolls': 'old_in_rolls', 'InLengthQty': 'old_in_length_qty', 'InWeightQty': 'old_in_weight_qty', 'Remarks': 'old_remarks', 'ColorID': 'old_color_id', 'CustomerID': 'old_customer_id', 'ColorNum': 'old_color_num', 'GrayID': 'old_gray_id', 'WarpDensity': 'old_warp_density', 'WeftDensity': 'old_weft_density', 'StockUnit': 'old_stock_unit', 'OutSheetNo': 'old_out_sheet_no', 'Weight': 'old_weight', 'CustSelfProduct': 'old_cust_self_product'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_out_detail_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_gray_id': 'Chinese_PRC_CI_AS', 'old_warp_density': 'Chinese_PRC_CI_AS', 'old_weft_density': 'Chinese_PRC_CI_AS', 'old_out_sheet_no': 'Chinese_PRC_CI_AS', 'old_cust_self_product': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：ODMIn', 'target': 'erp_warehouse.SourceDyeODMIn', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 ODMInDetail → ODMIn']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('表单明细号（子表）', null=False, blank=True, max_length=36)
    old_out_detail_no=models.CharField('出库单明细号', null=True, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_in_rolls=models.DecimalField('入库粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_in_length_qty=models.DecimalField('入库长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_in_weight_qty=models.DecimalField('入库重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=50)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=50)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=50)
    old_gray_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_warp_density=models.CharField('WarpDensity', null=True, blank=True, max_length=50)
    old_weft_density=models.CharField('WeftDensity', null=True, blank=True, max_length=50)
    old_stock_unit=models.IntegerField('单位', null=True, blank=True)
    old_out_sheet_no=models.CharField('OutSheetNo', null=True, blank=True, max_length=50)
    old_weight=models.DecimalField('Weight', null=True, blank=True, max_digits=6, decimal_places=2)
    old_cust_self_product=models.CharField('客户规格', null=True, blank=True, max_length=200)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeODMIn', verbose_name='原关系：ODMIn', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_odmindetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_a7f684940b96b0c0'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_a7f684940b96b0c0')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（ODMInDetail，待确认）'
        ordering=["-id"]

class SourceDyeODMInRecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ODMInRecord'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'RollNo': 'old_roll_no', 'DetailNo': 'old_detail_no', 'BarCode': 'old_bar_code', 'Rolls': 'old_rolls', 'ReceSheetNo': 'old_rece_sheet_no', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'StorageUnitID': 'old_storage_unit_id', 'Status': 'old_status', 'Remarks': 'old_remarks', 'WProcessNo': 'old_wprocess_no', 'MachineID': 'old_machine_id', 'Kind': 'old_kind'}
    SOURCE_KEY=('RollNo', 'DetailNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_roll_no': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_bar_code': 'Chinese_PRC_CI_AS', 'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_storage_unit_id': 'Chinese_PRC_CI_AS', 'old_status': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_wprocess_no': 'Chinese_PRC_CI_AS', 'old_machine_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：ODMInDetail', 'target': 'erp_warehouse.SourceDyeODMInDetail', 'source_fields': ['SheetSeries', 'DetailNo'], 'target_fields': ['SheetSeries', 'DetailNo'], 'evidence': ['原界面主从 ODMInRecord → ODMInDetail']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('工卡流水', null=True, blank=True, max_length=50)
    old_roll_no=models.CharField('箱号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('明细流水号', null=False, blank=True, max_length=36)
    old_bar_code=models.CharField('BarCode', null=True, blank=True, max_length=100)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_rece_sheet_no=models.CharField('入库明细号', null=True, blank=True, max_length=20)
    old_length_qty=models.DecimalField('长度数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('发外重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_storage_unit_id=models.CharField('仓位代码', null=True, blank=True, max_length=10)
    old_status=models.CharField('状态', null=True, blank=True, max_length=10)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_wprocess_no=models.CharField('WProcessNo', null=True, blank=True, max_length=20)
    old_machine_id=models.CharField('MachineID', null=True, blank=True, max_length=20)
    old_kind=models.IntegerField('Kind', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeODMInDetail', verbose_name='原关系：ODMInDetail', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_odminrecord'
        indexes=[models.Index(fields=['source_batch', 'old_roll_no', 'old_detail_no'],name='src_4d93c19815c1c813'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_roll_no'))),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_4d93c19815c1c813')]
        verbose_name=verbose_name_plural='其他或待确认相关表（ODMInRecord，待确认）'
        ordering=["-id"]

class SourceDyeODMOut(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ODMOut'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetKind': 'old_sheet_kind', 'SheetType': 'old_sheet_type', 'BusinessUnitID': 'old_business_unit_id', 'CustomerID': 'old_customer_id', 'Keeper': 'old_keeper', 'CarNo': 'old_car_no', 'FactID': 'old_fact_id', 'Driver': 'old_driver', 'OutKindID': 'old_out_kind_id', 'OutTime': 'old_out_time', 'PackID': 'old_pack_id', 'ProcessID': 'old_process_id', 'CarryerID': 'old_carryer_id', 'Remarks': 'old_remarks', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'StepNo': 'old_step_no', 'SheetDate': 'old_sheet_date', 'DlvDate': 'old_dlv_date', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'StockUnit': 'old_stock_unit', 'Cargador1': 'old_cargador1', 'Cargador2': 'old_cargador2', 'Cargador3': 'old_cargador3', 'Cargador4': 'old_cargador4', 'Cargador5': 'old_cargador5'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_keeper': 'Chinese_PRC_CI_AS', 'old_car_no': 'Chinese_PRC_CI_AS', 'old_fact_id': 'Chinese_PRC_CI_AS', 'old_driver': 'Chinese_PRC_CI_AS', 'old_out_kind_id': 'Chinese_PRC_CI_AS', 'old_pack_id': 'Chinese_PRC_CI_AS', 'old_process_id': 'Chinese_PRC_CI_AS', 'old_carryer_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_cargador1': 'Chinese_PRC_CI_AS', 'old_cargador2': 'Chinese_PRC_CI_AS', 'old_cargador3': 'Chinese_PRC_CI_AS', 'old_cargador4': 'Chinese_PRC_CI_AS', 'old_cargador5': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_sheet_type=models.IntegerField('单据类型', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户代码', null=True, blank=True, max_length=10)
    old_keeper=models.CharField('仓管员', null=True, blank=True, max_length=100)
    old_car_no=models.CharField('车牌号', null=True, blank=True, max_length=20)
    old_fact_id=models.CharField('工厂代码', null=True, blank=True, max_length=10)
    old_driver=models.CharField('司机', null=True, blank=True, max_length=20)
    old_out_kind_id=models.CharField('发货类型', null=True, blank=True, max_length=10)
    old_out_time=models.DateTimeField('领料时间', null=True, blank=True)
    old_pack_id=models.CharField('包装形式代码', null=True, blank=True, max_length=10)
    old_process_id=models.CharField('工序代码', null=True, blank=True, max_length=50)
    old_carryer_id=models.CharField('搬运工1', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_step_no=models.IntegerField('流程节点号', null=True, blank=True)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_dlv_date=models.DateTimeField('交货日期', null=True, blank=True)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_stock_unit=models.IntegerField('库存单位', null=True, blank=True)
    old_cargador1=models.CharField('搬运工2', null=True, blank=True, max_length=10)
    old_cargador2=models.CharField('搬运工3', null=True, blank=True, max_length=10)
    old_cargador3=models.CharField('搬运工4', null=True, blank=True, max_length=10)
    old_cargador4=models.CharField('Cargador4', null=True, blank=True, max_length=10)
    old_cargador5=models.CharField('Cargador5', null=True, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_odmout'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_822b8f637c3c9430'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_822b8f637c3c9430')]
        verbose_name=verbose_name_plural='其他或待确认相关表（ODMOut，待确认）'
        ordering=["-id"]

class SourceDyeODMOutDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ODMOutDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'JobSheetNo': 'old_job_sheet_no', 'GrayID': 'old_gray_id', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'ColorID': 'old_color_id', 'WeftDensity': 'old_weft_density', 'WarpDensity': 'old_warp_density', 'OutRolls': 'old_out_rolls', 'OutLengthQty': 'old_out_length_qty', 'OutWeightQty': 'old_out_weight_qty', 'Remarks': 'old_remarks', 'ColorNum': 'old_color_num', 'CustomerID': 'old_customer_id', 'GWidth': 'old_gwidth', 'Width': 'old_width', 'StockUnit': 'old_stock_unit', 'Weight': 'old_weight', 'CustSelfProduct': 'old_cust_self_product'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_gray_id': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_weft_density': 'Chinese_PRC_CI_AS', 'old_warp_density': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_gwidth': 'Chinese_PRC_CI_AS', 'old_width': 'Chinese_PRC_CI_AS', 'old_cust_self_product': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：ODMOut', 'target': 'erp_warehouse.SourceDyeODMOut', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 ODMOutDetail → ODMOut']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('表单明细号（子表）', null=False, blank=True, max_length=36)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_gray_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=128)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('颜色编码', null=True, blank=True, max_length=50)
    old_weft_density=models.CharField('纬密', null=True, blank=True, max_length=50)
    old_warp_density=models.CharField('经密', null=True, blank=True, max_length=50)
    old_out_rolls=models.DecimalField('出库粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_out_length_qty=models.DecimalField('出库长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_out_weight_qty=models.DecimalField('出库重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=50)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=50)
    old_gwidth=models.CharField('GWidth', null=True, blank=True, max_length=50)
    old_width=models.CharField('Width', null=True, blank=True, max_length=50)
    old_stock_unit=models.IntegerField('单位', null=True, blank=True)
    old_weight=models.DecimalField('Weight', null=True, blank=True, max_digits=6, decimal_places=2)
    old_cust_self_product=models.CharField('客户规格', null=True, blank=True, max_length=200)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeODMOut', verbose_name='原关系：ODMOut', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_odmoutdetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_028cfea78d1a80a4'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_028cfea78d1a80a4')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（ODMOutDetail，待确认）'
        ordering=["-id"]

class SourceDyeODMOutRecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ODMOutRecord'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'RollNo': 'old_roll_no', 'DetailNo': 'old_detail_no', 'BarCode': 'old_bar_code', 'Rolls': 'old_rolls', 'ReceSheetNo': 'old_rece_sheet_no', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'StorageUnitID': 'old_storage_unit_id', 'Status': 'old_status', 'Remarks': 'old_remarks', 'WProcessNo': 'old_wprocess_no', 'MachineID': 'old_machine_id', 'Kind': 'old_kind'}
    SOURCE_KEY=('RollNo', 'DetailNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_roll_no': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_bar_code': 'Chinese_PRC_CI_AS', 'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_storage_unit_id': 'Chinese_PRC_CI_AS', 'old_status': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_wprocess_no': 'Chinese_PRC_CI_AS', 'old_machine_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：ODMOutDetail', 'target': 'erp_warehouse.SourceDyeODMOutDetail', 'source_fields': ['SheetSeries', 'DetailNo'], 'target_fields': ['SheetSeries', 'DetailNo'], 'evidence': ['原界面主从 ODMOutRecord → ODMOutDetail']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('工卡流水', null=True, blank=True, max_length=50)
    old_roll_no=models.CharField('箱号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('明细流水号', null=False, blank=True, max_length=36)
    old_bar_code=models.CharField('BarCode', null=True, blank=True, max_length=100)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_rece_sheet_no=models.CharField('入库明细号', null=True, blank=True, max_length=20)
    old_length_qty=models.DecimalField('长度数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('发外重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_storage_unit_id=models.CharField('仓位代码', null=True, blank=True, max_length=10)
    old_status=models.CharField('状态', null=True, blank=True, max_length=10)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_wprocess_no=models.CharField('WProcessNo', null=True, blank=True, max_length=20)
    old_machine_id=models.CharField('MachineID', null=True, blank=True, max_length=20)
    old_kind=models.IntegerField('Kind', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeODMOutDetail', verbose_name='原关系：ODMOutDetail', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_odmoutrecord'
        indexes=[models.Index(fields=['source_batch', 'old_roll_no', 'old_detail_no'],name='src_ca7167b7d545de61'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_roll_no'))),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_ca7167b7d545de61')]
        verbose_name=verbose_name_plural='其他或待确认相关表（ODMOutRecord，待确认）'
        ordering=["-id"]

class SourceDyeOtherIn(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='OtherIn'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'InKindID': 'old_in_kind_id', 'BuyerID': 'old_buyer_id', 'WareHouseID': 'old_ware_house_id', 'SupplierID': 'old_supplier_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'StepNo': 'old_step_no', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'BusinessUnitID': 'old_business_unit_id', 'Keeper': 'old_keeper', 'Reason': 'old_reason', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'Settle': 'old_settle', 'deliverynum': 'old_deliverynum', 'APMoney': 'old_apmoney', 'APQty': 'old_apqty', 'UnClearQty': 'old_un_clear_qty', 'UnClearMoney': 'old_un_clear_money', 'UnClearInvoiceQty': 'old_un_clear_invoice_qty', 'UnClearInvoiceMoney': 'old_un_clear_invoice_money', 'DiscountMoney': 'old_discount_money', 'SumAmount': 'old_sum_amount', 'InvoiceClearStatus': 'old_invoice_clear_status', 'MoneyClearStatus': 'old_money_clear_status'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_in_kind_id': 'Chinese_PRC_CI_AS', 'old_buyer_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_supplier_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_keeper': 'Chinese_PRC_CI_AS', 'old_reason': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_settle': 'Chinese_PRC_CI_AS', 'old_deliverynum': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_in_kind_id=models.CharField('入库类别', null=True, blank=True, max_length=10)
    old_buyer_id=models.CharField('采购员', null=True, blank=True, max_length=50)
    old_ware_house_id=models.CharField('仓库代码', null=True, blank=True, max_length=10)
    old_supplier_id=models.CharField('供应商代码', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_step_no=models.IntegerField('流程节点号', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_keeper=models.CharField('仓管员', null=True, blank=True, max_length=10)
    old_reason=models.CharField('Reason', null=True, blank=True, max_length=256)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_settle=models.CharField('Settle', null=True, blank=True, max_length=50)
    old_deliverynum=models.CharField('deliverynum', null=True, blank=True, max_length=50)
    old_apmoney=models.DecimalField('APMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_apqty=models.DecimalField('APQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_un_clear_qty=models.DecimalField('UnClearQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_un_clear_money=models.DecimalField('UnClearMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_un_clear_invoice_qty=models.DecimalField('UnClearInvoiceQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_un_clear_invoice_money=models.DecimalField('UnClearInvoiceMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_discount_money=models.DecimalField('DiscountMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sum_amount=models.DecimalField('SumAmount', null=True, blank=True, max_digits=10, decimal_places=2)
    old_invoice_clear_status=models.IntegerField('InvoiceClearStatus', null=True, blank=True)
    old_money_clear_status=models.IntegerField('MoneyClearStatus', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_otherin'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_64085f856a5a0b13'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_64085f856a5a0b13')]
        verbose_name=verbose_name_plural='其他或待确认相关表（OtherIn，待确认）'
        ordering=["-id"]

class SourceDyeOtherInDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='OtherInDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'CookID': 'old_cook_id', 'ArticleKindID': 'old_article_kind_id', 'InQty': 'old_in_qty', 'Price': 'old_price', 'TaxRate': 'old_tax_rate', 'TaxPrice': 'old_tax_price', 'TaxMoney': 'old_tax_money', 'Total': 'old_total', 'PurDetailNo': 'old_pur_detail_no', 'APDetailNo': 'old_apdetail_no', 'InvoiceNo': 'old_invoice_no', 'FactDlvNo': 'old_fact_dlv_no', 'Remarks': 'old_remarks', 'PackQty': 'old_pack_qty', 'PackUnit': 'old_pack_unit', 'Discount': 'old_discount', 'DiscountMoney': 'old_discount_money', 'OriDetailNo': 'old_ori_detail_no', 'Amount': 'old_amount'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_cook_id': 'Chinese_PRC_CI_AS', 'old_article_kind_id': 'Chinese_PRC_CI_AS', 'old_pur_detail_no': 'Chinese_PRC_CI_AS', 'old_apdetail_no': 'Chinese_PRC_CI_AS', 'old_invoice_no': 'Chinese_PRC_CI_AS', 'old_fact_dlv_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_pack_unit': 'Chinese_PRC_CI_AS', 'old_ori_detail_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：OtherIn', 'target': 'erp_warehouse.SourceDyeOtherIn', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 OtherInDetail → OtherIn']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('表单明细号（子表）', null=False, blank=True, max_length=36)
    old_cook_id=models.CharField('物料编码', null=True, blank=True, max_length=200)
    old_article_kind_id=models.CharField('报账类别', null=True, blank=True, max_length=20)
    old_in_qty=models.DecimalField('入库数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=16, decimal_places=6)
    old_tax_rate=models.DecimalField('税率', null=True, blank=True, max_digits=4, decimal_places=2)
    old_tax_price=models.DecimalField('含税价', null=True, blank=True, max_digits=16, decimal_places=6)
    old_tax_money=models.DecimalField('税金', null=True, blank=True, max_digits=10, decimal_places=2)
    old_total=models.DecimalField('合计', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pur_detail_no=models.CharField('采购单明细号', null=True, blank=True, max_length=20)
    old_apdetail_no=models.CharField('应付单细号', null=True, blank=True, max_length=20)
    old_invoice_no=models.CharField('发票号码', null=True, blank=True, max_length=30)
    old_fact_dlv_no=models.CharField('送货单号', null=True, blank=True, max_length=80)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_pack_qty=models.DecimalField('包装数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pack_unit=models.CharField('PackUnit', null=True, blank=True, max_length=10)
    old_discount=models.DecimalField('Discount', null=True, blank=True, max_digits=3, decimal_places=2)
    old_discount_money=models.DecimalField('DiscountMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_ori_detail_no=models.CharField('OriDetailNo', null=True, blank=True, max_length=36)
    old_amount=models.FloatField('不含税金额', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeOtherIn', verbose_name='原关系：OtherIn', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_otherindetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_5c95a1e6f9bce79e'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_5c95a1e6f9bce79e')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（OtherInDetail，待确认）'
        ordering=["-id"]

class SourceDyeOutGoingBill(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='OutGoingBill'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'ShiftCode': 'old_shift_code', 'StartTime': 'old_start_time', 'EndTime': 'old_end_time', 'Creator': 'old_creator', 'CreateDate': 'old_create_date', 'Modifier': 'old_modifier', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'RightStatus': 'old_right_status', 'Remark': 'old_remark'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_shift_code': 'Chinese_PRC_CI_AS', 'old_creator': 'Chinese_PRC_CI_AS', 'old_modifier': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_remark': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('单号', null=False, blank=True, max_length=50)
    old_shift_code=models.CharField('班别', null=True, blank=True, max_length=50)
    old_start_time=models.DateTimeField('放行开始时间', null=True, blank=True)
    old_end_time=models.DateTimeField('放行结束时间', null=True, blank=True)
    old_creator=models.CharField('创建人', null=True, blank=True, max_length=20)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifier=models.CharField('修改人', null=True, blank=True, max_length=20)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_remark=models.CharField('Remark', null=True, blank=True, max_length=200)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_outgoingbill'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_df7b00dc8cfdf9f0'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_df7b00dc8cfdf9f0')]
        verbose_name=verbose_name_plural='其他或待确认相关表（OutGoingBill，待确认）'
        ordering=["-id"]

class SourceDyeOutGoingBillDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='OutGoingBillDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'EmpID': 'old_emp_id', 'Note': 'old_note'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_emp_id': 'Chinese_PRC_CI_AS', 'old_note': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：OutGoingBill', 'target': 'erp_warehouse.SourceDyeOutGoingBill', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 OutGoingBillDetail → OutGoingBill']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=50)
    old_detail_no=models.CharField('DetailNo', null=False, blank=True, max_length=50)
    old_emp_id=models.CharField('EmpID', null=True, blank=True, max_length=50)
    old_note=models.CharField('Note', null=True, blank=True, max_length=200)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeOutGoingBill', verbose_name='原关系：OutGoingBill', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_outgoingbilldetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_c0e3cf07b838f5c5'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_c0e3cf07b838f5c5')]
        verbose_name=verbose_name_plural='其他或待确认相关表（OutGoingBillDetail，待确认）'
        ordering=["-id"]

class SourceDyeOutPlan(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='OutPlan'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'BusinessUnitID': 'old_business_unit_id', 'PriorityID': 'old_priority_id', 'OutKindID': 'old_out_kind_id', 'CreditNo': 'old_credit_no', 'ShipDate': 'old_ship_date', 'BoxDate': 'old_box_date', 'BoxTypeID': 'old_box_type_id', 'ForwarderID': 'old_forwarder_id', 'Linker': 'old_linker', 'LinkerInfo': 'old_linker_info', 'Fee1': 'old_fee1', 'Fee2': 'old_fee2', 'Fee3': 'old_fee3', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'CustomerID': 'old_customer_id', 'SalerID': 'old_saler_id', 'CustomsCheckNo': 'old_customs_check_no', 'ToPlace': 'old_to_place', 'DetailCustName': 'old_detail_cust_name', 'StorageUnitID': 'old_storage_unit_id', 'StepNo': 'old_step_no', 'SalerGroupID': 'old_saler_group_id'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_priority_id': 'Chinese_PRC_CI_AS', 'old_out_kind_id': 'Chinese_PRC_CI_AS', 'old_credit_no': 'Chinese_PRC_CI_AS', 'old_box_type_id': 'Chinese_PRC_CI_AS', 'old_forwarder_id': 'Chinese_PRC_CI_AS', 'old_linker': 'Chinese_PRC_CI_AS', 'old_linker_info': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_saler_id': 'Chinese_PRC_CI_AS', 'old_customs_check_no': 'Chinese_PRC_CI_AS', 'old_to_place': 'Chinese_PRC_CI_AS', 'old_detail_cust_name': 'Chinese_PRC_CI_AS', 'old_storage_unit_id': 'Chinese_PRC_CI_AS', 'old_saler_group_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_sheet_no': ('literal', ''), 'old_sheet_date': ('literal', '1900-01-01'), 'old_sheet_kind': ('literal', 0), 'old_business_unit_id': ('literal', ''), 'old_priority_id': ('literal', ''), 'old_out_kind_id': ('literal', ''), 'old_credit_no': ('literal', ''), 'old_ship_date': ('literal', '1900-01-01'), 'old_box_date': ('literal', '1900-01-01'), 'old_box_type_id': ('literal', ''), 'old_forwarder_id': ('literal', ''), 'old_linker': ('literal', ''), 'old_linker_info': ('literal', ''), 'old_fee1': ('literal', 0), 'old_fee2': ('literal', 0), 'old_fee3': ('literal', 0), 'old_sheet_status': ('literal', 0), 'old_right_status': ('literal', 0), 'old_print_times': ('literal', 0), 'old_revisions': ('literal', 0), 'old_remarks': ('literal', ''), 'old_creater': ('literal', ''), 'old_create_date': ('literal', '1900-01-01'), 'old_modifyer': ('literal', ''), 'old_modify_date': ('literal', '1900-01-01')}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=False, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类别', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_priority_id=models.CharField('优先级', null=True, blank=True, max_length=10)
    old_out_kind_id=models.CharField('发货类型', null=True, blank=True, max_length=10)
    old_credit_no=models.CharField('信用证号', null=True, blank=True, max_length=50)
    old_ship_date=models.DateTimeField('船期', null=True, blank=True)
    old_box_date=models.DateTimeField('装箱日期', null=True, blank=True)
    old_box_type_id=models.CharField('箱型', null=True, blank=True, max_length=10)
    old_forwarder_id=models.CharField('货运公司', null=True, blank=True, max_length=10)
    old_linker=models.CharField('联系人', null=True, blank=True, max_length=10)
    old_linker_info=models.CharField('联系人信息', null=True, blank=True, max_length=100)
    old_fee1=models.DecimalField('费用1', null=True, blank=True, max_digits=10, decimal_places=2)
    old_fee2=models.DecimalField('费用2', null=True, blank=True, max_digits=10, decimal_places=2)
    old_fee3=models.DecimalField('费用3', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_customer_id=models.CharField('客户代码', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('业务员代码', null=True, blank=True, max_length=10)
    old_customs_check_no=models.CharField('海关核销单号', null=True, blank=True, max_length=20)
    old_to_place=models.CharField('交货地点', null=True, blank=True, max_length=50)
    old_detail_cust_name=models.CharField('明细客户', null=True, blank=True, max_length=500)
    old_storage_unit_id=models.CharField('仓位代码', null=True, blank=True, max_length=10)
    old_step_no=models.IntegerField('工作流节点号', null=True, blank=True)
    old_saler_group_id=models.CharField('业务组别', null=True, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_outplan'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_48a641fd766bb168'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_48a641fd766bb168')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（OutPlan，待确认）'
        ordering=["-id"]

class SourceDyeOutPlanDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='OutPlanDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'FabricID': 'old_fabric_id', 'Spec': 'old_spec', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'ColorE': 'old_color_e', 'Rolls': 'old_rolls', 'OutQty': 'old_out_qty', 'Price': 'old_price', 'Amount': 'old_amount', 'CheckNo': 'old_check_no', 'Remarks': 'old_remarks', 'JobDetailNo': 'old_job_detail_no', 'Structure': 'old_structure', 'JobSheetNo': 'old_job_sheet_no', 'ProdID': 'old_prod_id', 'CustColorNum': 'old_cust_color_num', 'toaddress': 'old_toaddress', 'WeightQty': 'old_weight_qty', 'CurrStatus': 'old_curr_status'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_fabric_id': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_color_e': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_job_detail_no': 'Chinese_PRC_CI_AS', 'old_structure': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_cust_color_num': 'Chinese_PRC_CI_AS', 'old_toaddress': 'Chinese_PRC_CI_AS', 'old_curr_status': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：OutPlan', 'target': 'erp_warehouse.SourceDyeOutPlan', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 OutPlanDetail → OutPlan']}]
    SOURCE_DEFAULTS={'old_fabric_id': ('literal', ''), 'old_spec': ('literal', ''), 'old_color_id': ('literal', ''), 'old_color_num': ('literal', ''), 'old_color_e': ('literal', ''), 'old_rolls': ('literal', 0), 'old_out_qty': ('literal', 0), 'old_price': ('literal', 0), 'old_amount': ('literal', 0), 'old_check_no': ('literal', ''), 'old_remarks': ('literal', '')}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('表单明细号（子表）', null=False, blank=True, max_length=20)
    old_fabric_id=models.CharField('客户规格', null=True, blank=True, max_length=20)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=20)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=20)
    old_color_e=models.CharField('ColorE', null=True, blank=True, max_length=20)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_out_qty=models.DecimalField('出库数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_amount=models.DecimalField('Amount', null=True, blank=True, max_digits=10, decimal_places=2)
    old_check_no=models.CharField('订单明细号', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    old_job_detail_no=models.CharField('加工作业号', null=True, blank=True, max_length=20)
    old_structure=models.CharField('组织', null=True, blank=True, max_length=50)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=30)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=20)
    old_cust_color_num=models.CharField('客户色号', null=True, blank=True, max_length=50)
    old_toaddress=models.CharField('送货地址', null=True, blank=True, max_length=500)
    old_weight_qty=models.DecimalField('数量', null=True, blank=True, max_digits=9, decimal_places=2)
    old_curr_status=models.CharField('当前状态', null=True, blank=True, max_length=500)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeOutPlan', verbose_name='原关系：OutPlan', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_outplandetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_0a576686c5b23e71'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_0a576686c5b23e71')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（OutPlanDetail，待确认）'
        ordering=["-id"]

class SourceDyePackQty(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PackQty'
    SOURCE_FIELDS={'JobSheetNo': 'old_job_sheet_no', 'ShiftID': 'old_shift_id', 'EmpID': 'old_emp_id', 'Qty': 'old_qty', 'EndTime': 'old_end_time', 'ProcessID': 'old_process_id'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_shift_id': 'Chinese_PRC_CI_AS', 'old_emp_id': 'Chinese_PRC_CI_AS', 'old_end_time': 'Chinese_PRC_CI_AS', 'old_process_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)
    old_shift_id=models.CharField('ShiftID', null=True, blank=True, max_length=50)
    old_emp_id=models.CharField('EmpID', null=True, blank=True, max_length=50)
    old_qty=models.FloatField('Qty', null=True, blank=True)
    old_end_time=models.CharField('EndTime', null=True, blank=True, max_length=10)
    old_process_id=models.CharField('ProcessID', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_packqty'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（PackQty，待确认）'
        ordering=["-id"]

class SourceDyePackQty1(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PackQty1'
    SOURCE_FIELDS={'JobSheetNo': 'old_job_sheet_no', 'ShiftID': 'old_shift_id', 'CurrRolls': 'old_curr_rolls', 'CurrKg': 'old_curr_kg'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_shift_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)
    old_shift_id=models.CharField('ShiftID', null=True, blank=True, max_length=50)
    old_curr_rolls=models.IntegerField('CurrRolls', null=True, blank=True)
    old_curr_kg=models.FloatField('CurrKg', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_packqty1'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（PackQty1，待确认）'
        ordering=["-id"]

class SourceDyePackWorkQty(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PackWorkQty'
    SOURCE_FIELDS={'ID': 'old_id', 'OrderSheetNo': 'old_order_sheet_no', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'ColorNum': 'old_color_num', 'ColorID': 'old_color_id', 'JobSheetNo': 'old_job_sheet_no', 'ProcessID': 'old_process_id', 'ShiftName': 'old_shift_name', 'ShiftID': 'old_shift_id', 'EmpID': 'old_emp_id', 'YEARS': 'old_years', 'StartTime': 'old_start_time', 'DAYS': 'old_days', 'CurrRolls': 'old_curr_rolls', 'CurrKg': 'old_curr_kg', 'Qty': 'old_qty', 'Price': 'old_price', 'WorkMoney': 'old_work_money'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_id': 'Chinese_PRC_CI_AS', 'old_order_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_process_id': 'Chinese_PRC_CI_AS', 'old_shift_name': 'Chinese_PRC_CI_AS', 'old_shift_id': 'Chinese_PRC_CI_AS', 'old_emp_id': 'Chinese_PRC_CI_AS', 'old_years': 'Chinese_PRC_CI_AS', 'old_start_time': 'Chinese_PRC_CI_AS', 'old_days': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_id=models.CharField('ID', null=False, blank=True, max_length=50)
    old_order_sheet_no=models.CharField('OrderSheetNo', null=True, blank=True, max_length=50)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=50)
    old_prod_id=models.CharField('ProdID', null=True, blank=True, max_length=150)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=150)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=150)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=150)
    old_process_id=models.CharField('ProcessID', null=True, blank=True, max_length=150)
    old_shift_name=models.CharField('ShiftName', null=True, blank=True, max_length=150)
    old_shift_id=models.CharField('ShiftID', null=True, blank=True, max_length=150)
    old_emp_id=models.CharField('EmpID', null=True, blank=True, max_length=150)
    old_years=models.CharField('YEARS', null=True, blank=True, max_length=10)
    old_start_time=models.CharField('StartTime', null=True, blank=True, max_length=10)
    old_days=models.CharField('DAYS', null=True, blank=True, max_length=10)
    old_curr_rolls=models.IntegerField('CurrRolls', null=True, blank=True)
    old_curr_kg=models.FloatField('CurrKg', null=True, blank=True)
    old_qty=models.FloatField('Qty', null=True, blank=True)
    old_price=models.FloatField('Price', null=True, blank=True)
    old_work_money=models.FloatField('WorkMoney', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_packworkqty'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_de2d770fdd1dc4ba'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_id'))),name='src_ci_de2d770fdd1dc4ba')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（PackWorkQty，待确认）'
        ordering=["-id"]

class SourceDyePackWorkQty1(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PackWorkQty1'
    SOURCE_FIELDS={'ID': 'old_id', 'OrderSheetNo': 'old_order_sheet_no', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'ColorNum': 'old_color_num', 'ColorID': 'old_color_id', 'JobSheetNo': 'old_job_sheet_no', 'ProcessID': 'old_process_id', 'ShiftName': 'old_shift_name', 'ShiftID': 'old_shift_id', 'EmpID': 'old_emp_id', 'YEARS': 'old_years', 'StartTime': 'old_start_time', 'DAYS': 'old_days', 'CurrRolls': 'old_curr_rolls', 'CurrKg': 'old_curr_kg', 'Qty': 'old_qty', 'Price': 'old_price', 'WorkMoney': 'old_work_money'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_id': 'Chinese_PRC_CI_AS', 'old_order_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_process_id': 'Chinese_PRC_CI_AS', 'old_shift_name': 'Chinese_PRC_CI_AS', 'old_shift_id': 'Chinese_PRC_CI_AS', 'old_emp_id': 'Chinese_PRC_CI_AS', 'old_years': 'Chinese_PRC_CI_AS', 'old_start_time': 'Chinese_PRC_CI_AS', 'old_days': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_id=models.CharField('ID', null=False, blank=True, max_length=50)
    old_order_sheet_no=models.CharField('OrderSheetNo', null=True, blank=True, max_length=50)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=50)
    old_prod_id=models.CharField('ProdID', null=True, blank=True, max_length=150)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=150)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=150)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=150)
    old_process_id=models.CharField('ProcessID', null=True, blank=True, max_length=150)
    old_shift_name=models.CharField('ShiftName', null=True, blank=True, max_length=150)
    old_shift_id=models.CharField('ShiftID', null=True, blank=True, max_length=150)
    old_emp_id=models.CharField('EmpID', null=True, blank=True, max_length=150)
    old_years=models.CharField('YEARS', null=True, blank=True, max_length=10)
    old_start_time=models.CharField('StartTime', null=True, blank=True, max_length=10)
    old_days=models.CharField('DAYS', null=True, blank=True, max_length=10)
    old_curr_rolls=models.IntegerField('CurrRolls', null=True, blank=True)
    old_curr_kg=models.FloatField('CurrKg', null=True, blank=True)
    old_qty=models.FloatField('Qty', null=True, blank=True)
    old_price=models.FloatField('Price', null=True, blank=True)
    old_work_money=models.FloatField('WorkMoney', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_packworkqty1'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_a84176d192defd72'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_id'))),name='src_ci_a84176d192defd72')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（PackWorkQty1，待确认）'
        ordering=["-id"]

class SourceDyePackWorkQtyDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PackWorkQtyDetail'
    SOURCE_FIELDS={'JobSheetNo': 'old_job_sheet_no', 'ShiftID': 'old_shift_id', 'EmpID': 'old_emp_id', 'Qty': 'old_qty', 'EndTime': 'old_end_time', 'ProcessID': 'old_process_id'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_shift_id': 'Chinese_PRC_CI_AS', 'old_emp_id': 'Chinese_PRC_CI_AS', 'old_end_time': 'Chinese_PRC_CI_AS', 'old_process_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)
    old_shift_id=models.CharField('ShiftID', null=True, blank=True, max_length=50)
    old_emp_id=models.CharField('EmpID', null=True, blank=True, max_length=50)
    old_qty=models.FloatField('Qty', null=True, blank=True)
    old_end_time=models.CharField('EndTime', null=True, blank=True, max_length=10)
    old_process_id=models.CharField('ProcessID', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_packworkqtydetail'
        indexes=[]
        verbose_name=verbose_name_plural='生产工单与排程相关表（PackWorkQtyDetail，待确认）'
        ordering=["-id"]

class SourceDyePackWorkSumQty(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PackWorkSumQty'
    SOURCE_FIELDS={'JobSheetNo': 'old_job_sheet_no', 'ShiftID': 'old_shift_id', 'CurrRolls': 'old_curr_rolls', 'CurrKg': 'old_curr_kg'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_shift_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)
    old_shift_id=models.CharField('ShiftID', null=True, blank=True, max_length=50)
    old_curr_rolls=models.IntegerField('CurrRolls', null=True, blank=True)
    old_curr_kg=models.FloatField('CurrKg', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_packworksumqty'
        indexes=[]
        verbose_name=verbose_name_plural='生产工单与排程相关表（PackWorkSumQty，待确认）'
        ordering=["-id"]

class SourceDyeProdIn(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProdIn'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'JobSheetNo': 'old_job_sheet_no', 'SheetDate': 'old_sheet_date', 'IsInputRecord': 'old_is_input_record', 'SheetKind': 'old_sheet_kind', 'CustomerID': 'old_customer_id', 'BusinessUnitID': 'old_business_unit_id', 'StockUnit': 'old_stock_unit', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'SalerGroupID': 'old_saler_group_id', 'SalerID': 'old_saler_id', 'StepNo': 'old_step_no', 'BusinessKind': 'old_business_kind', 'ProdID': 'old_prod_id', 'LotNo': 'old_lot_no', 'Spec': 'old_spec', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'StorageUnitID': 'old_storage_unit_id', 'WareHouseID': 'old_ware_house_id', 'Rolls': 'old_rolls', 'WeightQty': 'old_weight_qty', 'LengthQty': 'old_length_qty', 'Price': 'old_price', 'Amount': 'old_amount', 'Total': 'old_total', 'TubeWeight': 'old_tube_weight', 'ProcessPrice': 'old_process_price', 'ProcessMemo': 'old_process_memo', 'AtteMemo': 'old_atte_memo', 'AtteFee': 'old_atte_fee', 'VatFee': 'old_vat_fee', 'RealLoss': 'old_real_loss', 'Loss': 'old_loss', 'AdjustedLoss': 'old_adjusted_loss', 'Weight': 'old_weight', 'Width': 'old_width', 'WidthKindID': 'old_width_kind_id', 'WeightUnit': 'old_weight_unit', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'DetailsCustomer': 'old_details_customer', 'BaseBoard': 'old_base_board', 'CustJobNo': 'old_cust_job_no', 'SumAssignedLengthQty': 'old_sum_assigned_length_qty', 'ColorDepthID': 'old_color_depth_id', 'Keeper': 'old_keeper', 'WarpDensity': 'old_warp_density', 'WeftDensity': 'old_weft_density', 'FabricID': 'old_fabric_id', 'Cargador1': 'old_cargador1', 'Cargador2': 'old_cargador2', 'Cargador3': 'old_cargador3', 'Cargador4': 'old_cargador4', 'Cargador5': 'old_cargador5', 'PhaseID': 'old_phase_id', 'GaryWeight': 'old_gary_weight', 'CustColorNum': 'old_cust_color_num', 'CheckNo': 'old_check_no', 'CustSelfNo': 'old_cust_self_no', 'Area': 'old_area', 'ShipMentType': 'old_ship_ment_type', 'PlasticBags': 'old_plastic_bags', 'ColorE': 'old_color_e', 'ColorRemarks': 'old_color_remarks', 'packremarks': 'old_packremarks', 'JXTDDH': 'old_jxtddh', 'ProdInOriSheetNo': 'old_prod_in_ori_sheet_no', 'YarnCategory': 'old_yarn_category', 'NetKg': 'old_net_kg', 'ContractNo': 'old_contract_no', 'ProdOutSheetSeries': 'old_prod_out_sheet_series'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_saler_group_id': 'Chinese_PRC_CI_AS', 'old_saler_id': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_storage_unit_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_process_memo': 'Chinese_PRC_CI_AS', 'old_atte_memo': 'Chinese_PRC_CI_AS', 'old_loss': 'Chinese_PRC_CI_AS', 'old_weight': 'Chinese_PRC_CI_AS', 'old_width': 'Chinese_PRC_CI_AS', 'old_width_kind_id': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_details_customer': 'Chinese_PRC_CI_AS', 'old_base_board': 'Chinese_PRC_CI_AS', 'old_cust_job_no': 'Chinese_PRC_CI_AS', 'old_color_depth_id': 'Chinese_PRC_CI_AS', 'old_keeper': 'Chinese_PRC_CI_AS', 'old_warp_density': 'Chinese_PRC_CI_AS', 'old_weft_density': 'Chinese_PRC_CI_AS', 'old_fabric_id': 'Chinese_PRC_CI_AS', 'old_cargador1': 'Chinese_PRC_CI_AS', 'old_cargador2': 'Chinese_PRC_CI_AS', 'old_cargador3': 'Chinese_PRC_CI_AS', 'old_cargador4': 'Chinese_PRC_CI_AS', 'old_cargador5': 'Chinese_PRC_CI_AS', 'old_phase_id': 'Chinese_PRC_CI_AS', 'old_cust_color_num': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_cust_self_no': 'Chinese_PRC_CI_AS', 'old_area': 'Chinese_PRC_CI_AS', 'old_ship_ment_type': 'Chinese_PRC_CI_AS', 'old_color_e': 'Chinese_PRC_CI_AS', 'old_color_remarks': 'Chinese_PRC_CI_AS', 'old_packremarks': 'Chinese_PRC_CI_AS', 'old_jxtddh': 'Chinese_PRC_CI_AS', 'old_prod_in_ori_sheet_no': 'Chinese_PRC_CI_AS', 'old_yarn_category': 'Chinese_PRC_CI_AS', 'old_contract_no': 'Chinese_PRC_CI_AS', 'old_prod_out_sheet_series': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=False, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_is_input_record=models.BooleanField('录入码单明细否', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类别', null=True, blank=True)
    old_customer_id=models.CharField('客户代码', null=True, blank=True, max_length=10)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_stock_unit=models.IntegerField('单位', null=True, blank=True)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_saler_group_id=models.CharField('业务组别', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('业务员代码', null=True, blank=True, max_length=10)
    old_step_no=models.IntegerField('工作流节点号', null=True, blank=True)
    old_business_kind=models.IntegerField('业务类别', null=True, blank=True)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=20)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=250)
    old_spec=models.CharField('捻度(H/S)', null=True, blank=True, max_length=128)
    old_color_id=models.CharField('颜色编码', null=True, blank=True, max_length=150)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=50)
    old_storage_unit_id=models.CharField('仓位代码', null=True, blank=True, max_length=200)
    old_ware_house_id=models.CharField('仓库代码', null=True, blank=True, max_length=10)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_weight_qty=models.DecimalField('毛重', null=True, blank=True, max_digits=10, decimal_places=2)
    old_length_qty=models.DecimalField('长度数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_amount=models.DecimalField('金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_total=models.DecimalField('合计', null=True, blank=True, max_digits=10, decimal_places=2)
    old_tube_weight=models.DecimalField('筒管重', null=True, blank=True, max_digits=6, decimal_places=2)
    old_process_price=models.DecimalField('特殊工艺价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_process_memo=models.CharField('另收费项目', null=True, blank=True, max_length=300)
    old_atte_memo=models.CharField('AtteMemo', null=True, blank=True, max_length=300)
    old_atte_fee=models.DecimalField('特殊要求价格', null=True, blank=True, max_digits=10, decimal_places=2)
    old_vat_fee=models.DecimalField('VatFee', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_loss=models.DecimalField('损耗', null=True, blank=True, max_digits=6, decimal_places=2)
    old_loss=models.CharField('损耗', null=True, blank=True, max_length=50)
    old_adjusted_loss=models.DecimalField('AdjustedLoss', null=True, blank=True, max_digits=6, decimal_places=2)
    old_weight=models.CharField('克重', null=True, blank=True, max_length=50)
    old_width=models.CharField('幅宽', null=True, blank=True, max_length=50)
    old_width_kind_id=models.CharField('WidthKindID', null=True, blank=True, max_length=50)
    old_weight_unit=models.IntegerField('WeightUnit', null=True, blank=True)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_details_customer=models.CharField('DetailsCustomer', null=True, blank=True, max_length=150)
    old_base_board=models.CharField('底板号', null=True, blank=True, max_length=50)
    old_cust_job_no=models.CharField('客户缸号', null=True, blank=True, max_length=100)
    old_sum_assigned_length_qty=models.DecimalField('投胚米数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_color_depth_id=models.CharField('颜色深浅', null=True, blank=True, max_length=20)
    old_keeper=models.CharField('仓管员', null=True, blank=True, max_length=16)
    old_warp_density=models.CharField('经密', null=True, blank=True, max_length=50)
    old_weft_density=models.CharField('纬密', null=True, blank=True, max_length=50)
    old_fabric_id=models.CharField('客户规格', null=True, blank=True, max_length=250)
    old_cargador1=models.CharField('装/配工', null=True, blank=True, max_length=10)
    old_cargador2=models.CharField('装/配工', null=True, blank=True, max_length=10)
    old_cargador3=models.CharField('装/配工', null=True, blank=True, max_length=10)
    old_cargador4=models.CharField('装/配工', null=True, blank=True, max_length=10)
    old_cargador5=models.CharField('装/配工', null=True, blank=True, max_length=10)
    old_phase_id=models.CharField('PhaseID', null=True, blank=True, max_length=10)
    old_gary_weight=models.DecimalField('胚重', null=True, blank=True, max_digits=10, decimal_places=2)
    old_cust_color_num=models.CharField('客户色号', null=True, blank=True, max_length=100)
    old_check_no=models.CharField('订单明细号', null=True, blank=True, max_length=50)
    old_cust_self_no=models.CharField('制单号', null=True, blank=True, max_length=500)
    old_area=models.CharField('区域', null=True, blank=True, max_length=100)
    old_ship_ment_type=models.CharField('出货方式', null=True, blank=True, max_length=50)
    old_plastic_bags=models.DecimalField('胶袋', null=True, blank=True, max_digits=4, decimal_places=2)
    old_color_e=models.CharField('ColorE', null=True, blank=True, max_length=20)
    old_color_remarks=models.CharField('用途', null=True, blank=True, max_length=500)
    old_packremarks=models.CharField('packremarks', null=True, blank=True, max_length=255)
    old_jxtddh=models.CharField('JXTDDH', null=True, blank=True, max_length=255)
    old_prod_in_ori_sheet_no=models.CharField('ProdInOriSheetNo', null=True, blank=True, max_length=50)
    old_yarn_category=models.CharField('纱类别', null=True, blank=True, max_length=50)
    old_net_kg=models.DecimalField('净重', null=True, blank=True, max_digits=10, decimal_places=2)
    old_contract_no=models.CharField('客户单号', null=True, blank=True, max_length=500)
    old_prod_out_sheet_series=models.CharField('ProdOutSheetSeries', null=True, blank=True, max_length=30)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_prodin'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_49c3be2561ca203d'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_49c3be2561ca203d')]
        verbose_name=verbose_name_plural='成品入库单'
        ordering=["-id"]

class SourceDyeProdInTo(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProdIn_to'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'JobSheetNo': 'old_job_sheet_no', 'SheetDate': 'old_sheet_date', 'CustomerID': 'old_customer_id', 'StockUnit': 'old_stock_unit', 'ProdID': 'old_prod_id', 'FabricID': 'old_fabric_id', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'CustColorNum': 'old_cust_color_num', 'Spec': 'old_spec', 'StorageUnitID': 'old_storage_unit_id', 'Area': 'old_area', 'SumRolls': 'old_sum_rolls', 'SumWeightQty': 'old_sum_weight_qty', 'SumGaryWeight': 'old_sum_gary_weight', 'SumLengthQty': 'old_sum_length_qty', 'AtteFee': 'old_atte_fee', 'VatFee': 'old_vat_fee', 'Width': 'old_width', 'Weight': 'old_weight', 'BarCode': 'old_bar_code', 'RollNo': 'old_roll_no', 'GrayQty': 'old_gray_qty', 'WeightQty': 'old_weight_qty', 'LengthQty': 'old_length_qty'}
    SOURCE_KEY=('BarCode',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_fabric_id': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_cust_color_num': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_storage_unit_id': 'Chinese_PRC_CI_AS', 'old_area': 'Chinese_PRC_CI_AS', 'old_bar_code': 'Chinese_PRC_CI_AS', 'old_roll_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('SheetSeries', null=True, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=10)
    old_stock_unit=models.IntegerField('StockUnit', null=True, blank=True)
    old_prod_id=models.CharField('ProdID', null=True, blank=True, max_length=250)
    old_fabric_id=models.CharField('FabricID', null=True, blank=True, max_length=250)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=150)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=20)
    old_cust_color_num=models.CharField('CustColorNum', null=True, blank=True, max_length=100)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=128)
    old_storage_unit_id=models.CharField('StorageUnitID', null=True, blank=True, max_length=10)
    old_area=models.CharField('Area', null=True, blank=True, max_length=100)
    old_sum_rolls=models.DecimalField('SumRolls', null=True, blank=True, max_digits=7, decimal_places=2)
    old_sum_weight_qty=models.DecimalField('SumWeightQty', null=True, blank=True, max_digits=10, decimal_places=1)
    old_sum_gary_weight=models.DecimalField('SumGaryWeight', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sum_length_qty=models.DecimalField('SumLengthQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_atte_fee=models.DecimalField('AtteFee', null=True, blank=True, max_digits=10, decimal_places=2)
    old_vat_fee=models.DecimalField('VatFee', null=True, blank=True, max_digits=10, decimal_places=2)
    old_width=models.DecimalField('Width', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight=models.DecimalField('Weight', null=True, blank=True, max_digits=10, decimal_places=2)
    old_bar_code=models.CharField('BarCode', null=False, blank=True, max_length=50)
    old_roll_no=models.CharField('RollNo', null=True, blank=True, max_length=20)
    old_gray_qty=models.DecimalField('GrayQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('WeightQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_length_qty=models.DecimalField('LengthQty', null=True, blank=True, max_digits=10, decimal_places=2)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_prodin_to'
        indexes=[models.Index(fields=['source_batch', 'old_bar_code'],name='src_1ff961c59381f1f5'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_bar_code'))),name='src_ci_1ff961c59381f1f5')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（ProdIn_to，待确认）'
        ordering=["-id"]

class SourceDyeProdInPDARecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProdInPDARecord'
    SOURCE_FIELDS={'BarCode': 'old_bar_code', 'CurrTime': 'old_curr_time', 'Geter': 'old_geter', 'StorageUnitID': 'old_storage_unit_id', 'Status': 'old_status'}
    SOURCE_KEY=('BarCode',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_bar_code': 'Chinese_PRC_CI_AS', 'old_geter': 'Chinese_PRC_CI_AS', 'old_storage_unit_id': 'Chinese_PRC_CI_AS', 'old_status': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_bar_code=models.CharField('BarCode', null=False, blank=True, max_length=50)
    old_curr_time=models.DateTimeField('CurrTime', null=True, blank=True)
    old_geter=models.CharField('Geter', null=True, blank=True, max_length=10)
    old_storage_unit_id=models.CharField('StorageUnitID', null=True, blank=True, max_length=10)
    old_status=models.CharField('Status', null=True, blank=True, max_length=1)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_prodinpdarecord'
        indexes=[models.Index(fields=['source_batch', 'old_bar_code'],name='src_7bf425de5efbca5d'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_bar_code'))),name='src_ci_7bf425de5efbca5d')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（ProdInPDARecord，待确认）'
        ordering=["-id"]

class SourceDyeProdInPriceAtte(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProdInPriceAtte'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'AtteCode': 'old_atte_code', 'Price': 'old_price', 'PriceUnit': 'old_price_unit', 'FieldType': 'old_field_type', 'AtteValue': 'old_atte_value', 'Description': 'old_description'}
    SOURCE_KEY=('SheetSeries', 'FieldType', 'AtteCode')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_atte_code': 'Chinese_PRC_CI_AS', 'old_field_type': 'Chinese_PRC_CI_AS', 'old_atte_value': 'Chinese_PRC_CI_AS', 'old_description': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：ProdIn', 'target': 'erp_warehouse.SourceDyeProdIn', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 ProdInPriceAtte → ProdIn']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=20)
    old_atte_code=models.CharField('要求代码', null=False, blank=True, max_length=10)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=8, decimal_places=2)
    old_price_unit=models.IntegerField('计价单位', null=True, blank=True)
    old_field_type=models.CharField('要求类别', null=False, blank=True, max_length=20)
    old_atte_value=models.CharField('事项内容', null=True, blank=True, max_length=500)
    old_description=models.CharField('描述', null=True, blank=True, max_length=500)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeProdIn', verbose_name='原关系：ProdIn', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_prodinpriceatte'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_field_type', 'old_atte_code'],name='src_e73f1b8e8f433659'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_field_type'))),Upper(RTrim(models.F('old_atte_code'))),name='src_ci_e73f1b8e8f433659')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（ProdInPriceAtte，待确认）'
        ordering=["-id"]

class SourceDyeProdInPriceProcess(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProdInPriceProcess'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'ProcessID': 'old_process_id', 'Price': 'old_price', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('SheetSeries', 'ProcessID')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_process_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：ProdIn', 'target': 'erp_warehouse.SourceDyeProdIn', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 ProdInPriceProcess → ProdIn']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=20)
    old_process_id=models.CharField('工序', null=False, blank=True, max_length=50)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=8, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=300)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeProdIn', verbose_name='原关系：ProdIn', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_prodinpriceprocess'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_process_id'],name='src_31f0d1ee2898cae8'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_process_id'))),name='src_ci_31f0d1ee2898cae8')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（ProdInPriceProcess，待确认）'
        ordering=["-id"]

class SourceDyeProdInRecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProdInRecord'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'RollNo': 'old_roll_no', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'StorageUnitID': 'old_storage_unit_id', 'Status': 'old_status', 'OutDetailNo': 'old_out_detail_no', 'BarCode': 'old_bar_code', 'GradeID': 'old_grade_id', 'GrayQty': 'old_gray_qty', 'AdjustQty': 'old_adjust_qty', 'RealQty': 'old_real_qty', 'Meter': 'old_meter', 'Yard': 'old_yard', 'Note': 'old_note', 'GrayBarCode': 'old_gray_bar_code', 'RollNo3': 'old_roll_no3', 'GUnit': 'old_gunit', 'PUnit': 'old_punit', 'ProdBarCode': 'old_prod_bar_code', 'InPacks': 'old_in_packs', 'InRolls': 'old_in_rolls', 'EmptyPlus': 'old_empty_plus', 'LabelLength': 'old_label_length', 'NetKg': 'old_net_kg', 'PackBag': 'old_pack_bag', 'TubeWeight': 'old_tube_weight', 'ProdCode': 'old_prod_code', 'LabelWareHouse': 'old_label_ware_house', 'LabelRemarks': 'old_label_remarks', 'WindingID': 'old_winding_id', 'CheckNo': 'old_check_no', 'ColorRemarks': 'old_color_remarks', 'OutDetatilNo': 'old_out_detatil_no', 'FenTou': 'old_fen_tou'}
    SOURCE_KEY=('SheetSeries', 'RollNo', 'BarCode')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_roll_no': 'Chinese_PRC_CI_AS', 'old_storage_unit_id': 'Chinese_PRC_CI_AS', 'old_status': 'Chinese_PRC_CI_AS', 'old_out_detail_no': 'Chinese_PRC_CI_AS', 'old_bar_code': 'Chinese_PRC_CI_AS', 'old_grade_id': 'Chinese_PRC_CI_AS', 'old_note': 'Chinese_PRC_CI_AS', 'old_gray_bar_code': 'Chinese_PRC_CI_AS', 'old_roll_no3': 'Chinese_PRC_CI_AS', 'old_prod_bar_code': 'Chinese_PRC_CI_AS', 'old_prod_code': 'Chinese_PRC_CI_AS', 'old_label_ware_house': 'Chinese_PRC_CI_AS', 'old_label_remarks': 'Chinese_PRC_CI_AS', 'old_winding_id': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_color_remarks': 'Chinese_PRC_CI_AS', 'old_out_detatil_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：ProdIn', 'target': 'erp_warehouse.SourceDyeProdIn', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 ProdInRecordWork → ProdInWork', '原界面主从 ProdInRecord_ht → ProdIn_ht', '原界面主从 ProdInRecord → ProdIn']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=20)
    old_roll_no=models.CharField('箱号', null=False, blank=True, max_length=20)
    old_length_qty=models.DecimalField('长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('成品重(毛重)', null=True, blank=True, max_digits=10, decimal_places=1)
    old_storage_unit_id=models.CharField('仓位代码', null=True, blank=True, max_length=10)
    old_status=models.CharField('状态', null=True, blank=True, max_length=1)
    old_out_detail_no=models.CharField('出库单明细号', null=True, blank=True, max_length=20)
    old_bar_code=models.CharField('条码', null=False, blank=True, max_length=50)
    old_grade_id=models.CharField('等级', null=True, blank=True, max_length=10)
    old_gray_qty=models.DecimalField('GrayQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_adjust_qty=models.DecimalField('AdjustQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_qty=models.DecimalField('磅重', null=True, blank=True, max_digits=10, decimal_places=2)
    old_meter=models.DecimalField('成品长', null=True, blank=True, max_digits=10, decimal_places=2)
    old_yard=models.DecimalField('码数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_note=models.CharField('备注', null=True, blank=True, max_length=50)
    old_gray_bar_code=models.CharField('GrayBarCode', null=True, blank=True, max_length=100)
    old_roll_no3=models.CharField('RollNo3', null=True, blank=True, max_length=20)
    old_gunit=models.IntegerField('GUnit', null=True, blank=True)
    old_punit=models.IntegerField('PUnit', null=True, blank=True)
    old_prod_bar_code=models.CharField('包装条码', null=True, blank=True, max_length=200)
    old_in_packs=models.DecimalField('件数', null=True, blank=True, max_digits=6, decimal_places=1)
    old_in_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=6, decimal_places=1)
    old_empty_plus=models.DecimalField('空加', null=True, blank=True, max_digits=6, decimal_places=2)
    old_label_length=models.DecimalField('LabelLength', null=True, blank=True, max_digits=6, decimal_places=2)
    old_net_kg=models.DecimalField('净重', null=True, blank=True, max_digits=6, decimal_places=2)
    old_pack_bag=models.DecimalField('包装重量', null=True, blank=True, max_digits=7, decimal_places=3)
    old_tube_weight=models.DecimalField('纸筒重', null=True, blank=True, max_digits=7, decimal_places=3)
    old_prod_code=models.CharField('二维码字段', null=True, blank=True, max_length=50)
    old_label_ware_house=models.CharField('标签仓库', null=True, blank=True, max_length=100)
    old_label_remarks=models.CharField('标签用途', null=True, blank=True, max_length=500)
    old_winding_id=models.CharField('络筒员工', null=True, blank=True, max_length=30)
    old_check_no=models.CharField('订单明细号', null=True, blank=True, max_length=20)
    old_color_remarks=models.CharField('用途', null=True, blank=True, max_length=500)
    old_out_detatil_no=models.CharField('出库明细单号', null=True, blank=True, max_length=30)
    old_fen_tou=models.DecimalField('分头', null=True, blank=True, max_digits=6, decimal_places=2)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeProdIn', verbose_name='原关系：ProdIn', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_prodinrecord'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_roll_no', 'old_bar_code'],name='src_2db02b5e8e60d6eb'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_roll_no'))),Upper(RTrim(models.F('old_bar_code'))),name='src_ci_2db02b5e8e60d6eb')]
        verbose_name=verbose_name_plural='成品入库卷记录'
        ordering=["-id"]

class SourceDyeProdLoading(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProdLoading'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'IsInputRecord': 'old_is_input_record', 'BusinessUnitID': 'old_business_unit_id', 'SalerGroupID': 'old_saler_group_id', 'SalerID': 'old_saler_id', 'CustomerID': 'old_customer_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'FactID': 'old_fact_id', 'StepNo': 'old_step_no', 'BusinessKind': 'old_business_kind', 'Discount': 'old_discount', 'PriceCheck': 'old_price_check', 'PriceChecker': 'old_price_checker', 'PriceCheckIdea': 'old_price_check_idea', 'PriceCheckTime': 'old_price_check_time', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'WareHouseID': 'old_ware_house_id', 'Cargador1': 'old_cargador1', 'Cargador2': 'old_cargador2', 'Cargador3': 'old_cargador3', 'Cargador4': 'old_cargador4', 'Cargador5': 'old_cargador5', 'Driver1': 'old_driver1', 'Driver2': 'old_driver2', 'Driver3': 'old_driver3', 'Discharger1': 'old_discharger1', 'Discharger2': 'old_discharger2', 'Driver': 'old_driver', 'CarNo': 'old_car_no', 'Keeper': 'old_keeper', 'DlvRolls': 'old_dlv_rolls', 'DlvLengthQty': 'old_dlv_length_qty', 'DlvWeightQty': 'old_dlv_weight_qty', 'DlvAddress': 'old_dlv_address', 'Phone': 'old_phone', 'CustomerCode': 'old_customer_code', 'WLLX': 'old_wllx', 'combo1': 'old_combo1', 'FHYSPC': 'old_fhyspc', 'RoundTrip': 'old_round_trip', 'Contacter': 'old_contacter', 'ContactNumber': 'old_contact_number', 'ContractNumber': 'old_contract_number', 'DHSD_FEI': 'old_dhsd_fei', 'TY_FEI': 'old_ty_fei'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_saler_group_id': 'Chinese_PRC_CI_AS', 'old_saler_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_fact_id': 'Chinese_PRC_CI_AS', 'old_price_checker': 'Chinese_PRC_CI_AS', 'old_price_check_idea': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_cargador1': 'Chinese_PRC_CI_AS', 'old_cargador2': 'Chinese_PRC_CI_AS', 'old_cargador3': 'Chinese_PRC_CI_AS', 'old_cargador4': 'Chinese_PRC_CI_AS', 'old_cargador5': 'Chinese_PRC_CI_AS', 'old_driver1': 'Chinese_PRC_CI_AS', 'old_driver2': 'Chinese_PRC_CI_AS', 'old_driver3': 'Chinese_PRC_CI_AS', 'old_discharger1': 'Chinese_PRC_CI_AS', 'old_discharger2': 'Chinese_PRC_CI_AS', 'old_driver': 'Chinese_PRC_CI_AS', 'old_car_no': 'Chinese_PRC_CI_AS', 'old_keeper': 'Chinese_PRC_CI_AS', 'old_dlv_address': 'Chinese_PRC_CI_AS', 'old_phone': 'Chinese_PRC_CI_AS', 'old_customer_code': 'Chinese_PRC_CI_AS', 'old_wllx': 'Chinese_PRC_CI_AS', 'old_combo1': 'Chinese_PRC_CI_AS', 'old_fhyspc': 'Chinese_PRC_CI_AS', 'old_round_trip': 'Chinese_PRC_CI_AS', 'old_contacter': 'Chinese_PRC_CI_AS', 'old_contact_number': 'Chinese_PRC_CI_AS', 'old_contract_number': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=False, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类别', null=True, blank=True)
    old_is_input_record=models.BooleanField('录入码单明细否', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('业务组别', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('业务员代码', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户代码', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_fact_id=models.CharField('工厂代码', null=True, blank=True, max_length=10)
    old_step_no=models.IntegerField('工作流节点号', null=True, blank=True)
    old_business_kind=models.IntegerField('BusinessKind', null=True, blank=True)
    old_discount=models.DecimalField('折扣', null=True, blank=True, max_digits=3, decimal_places=2)
    old_price_check=models.BooleanField('价格审核', null=True, blank=True)
    old_price_checker=models.CharField('价格审核人', null=True, blank=True, max_length=10)
    old_price_check_idea=models.CharField('价格审核意见', null=True, blank=True, max_length=300)
    old_price_check_time=models.DateTimeField('价格审核时间', null=True, blank=True)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_ware_house_id=models.CharField('存放仓库', null=True, blank=True, max_length=10)
    old_cargador1=models.CharField('目标客户', null=True, blank=True, max_length=10)
    old_cargador2=models.CharField('搬运工', null=True, blank=True, max_length=10)
    old_cargador3=models.CharField('搬运工', null=True, blank=True, max_length=10)
    old_cargador4=models.CharField('搬运工', null=True, blank=True, max_length=10)
    old_cargador5=models.CharField('搬运工', null=True, blank=True, max_length=10)
    old_driver1=models.CharField('司机电话', null=True, blank=True, max_length=10)
    old_driver2=models.CharField('叉车', null=True, blank=True, max_length=10)
    old_driver3=models.CharField('叉车', null=True, blank=True, max_length=10)
    old_discharger1=models.CharField('装卸工', null=True, blank=True, max_length=10)
    old_discharger2=models.CharField('装卸工', null=True, blank=True, max_length=10)
    old_driver=models.CharField('司机', null=True, blank=True, max_length=10)
    old_car_no=models.CharField('车牌号', null=True, blank=True, max_length=10)
    old_keeper=models.CharField('仓管员', null=True, blank=True, max_length=16)
    old_dlv_rolls=models.DecimalField('DlvRolls', null=True, blank=True, max_digits=6, decimal_places=1)
    old_dlv_length_qty=models.DecimalField('DlvLengthQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dlv_weight_qty=models.DecimalField('DlvWeightQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dlv_address=models.CharField('送货地址', null=True, blank=True, max_length=300)
    old_phone=models.CharField('司机电话', null=True, blank=True, max_length=20)
    old_customer_code=models.CharField('客户全称', null=True, blank=True, max_length=50)
    old_wllx=models.CharField('物流类型', null=True, blank=True, max_length=255)
    old_combo1=models.CharField('收发地点', null=True, blank=True, max_length=10)
    old_fhyspc=models.CharField('送货运输编号', null=True, blank=True, max_length=20)
    old_round_trip=models.CharField('往返', null=True, blank=True, max_length=20)
    old_contacter=models.CharField('联系人', null=True, blank=True, max_length=50)
    old_contact_number=models.CharField('联系电话', null=True, blank=True, max_length=50)
    old_contract_number=models.CharField('合同号码', null=True, blank=True, max_length=50)
    old_dhsd_fei=models.DecimalField('大货速递费', null=True, blank=True, max_digits=18, decimal_places=4)
    old_ty_fei=models.DecimalField('托运费', null=True, blank=True, max_digits=18, decimal_places=4)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_prodloading'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_973c9940ca0a83b5'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_973c9940ca0a83b5')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（ProdLoading，待确认）'
        ordering=["-id"]

class SourceDyeProdLoadingDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProdLoadingDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'LineNumber': 'old_line_number', 'CustomerIDName': 'old_customer_idname', 'Spec': 'old_spec', 'Structure': 'old_structure', 'LotNo': 'old_lot_no', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'OutRolls': 'old_out_rolls', 'WeightQty': 'old_weight_qty', 'LengthQty': 'old_length_qty', 'Price': 'old_price', 'Amount': 'old_amount', 'Weight': 'old_weight', 'Width': 'old_width', 'CheckNo': 'old_check_no', 'ARDetailNo': 'old_ardetail_no', 'Remarks': 'old_remarks', 'JobSheetNo': 'old_job_sheet_no', 'ProdID': 'old_prod_id', 'StockUnit': 'old_stock_unit', 'Total': 'old_total', 'ProcessPrice': 'old_process_price', 'AtteFee': 'old_atte_fee', 'VatFee': 'old_vat_fee', 'ProcessMemo': 'old_process_memo', 'Atte': 'old_atte', 'InSheetNo': 'old_in_sheet_no', 'InPrice': 'old_in_price', 'InProcessPrice': 'old_in_process_price', 'InAtteFee': 'old_in_atte_fee', 'InVatFee': 'old_in_vat_fee', 'Rolls': 'old_rolls', 'WidthDn': 'old_width_dn', 'WidthUp': 'old_width_up', 'WeightDn': 'old_weight_dn', 'WeightUp': 'old_weight_up', 'WeightUnit': 'old_weight_unit', 'WidthKindID': 'old_width_kind_id', 'PreRolls': 'old_pre_rolls', 'DetailsCustomer': 'old_details_customer', 'OrderSheetDate': 'old_order_sheet_date', 'AttPrice': 'old_att_price', 'ColorAddPrice': 'old_color_add_price', 'ColorAddFee': 'old_color_add_fee', 'SumAssignedLengthQty': 'old_sum_assigned_length_qty', 'CustJobNo': 'old_cust_job_no', 'ColorDepthID': 'old_color_depth_id', 'WarpDensity': 'old_warp_density', 'WeftDensity': 'old_weft_density', 'FabricID': 'old_fabric_id', 'GrayQty': 'old_gray_qty', 'Jobattes1': 'old_jobattes1', 'Jobattes2': 'old_jobattes2', 'CustColorNum': 'old_cust_color_num', 'PriceUnit': 'old_price_unit', 'PhaseID': 'old_phase_id', 'Jobattes3': 'old_jobattes3', 'Jobattes4': 'old_jobattes4', 'Jobattes5': 'old_jobattes5', 'Jobattes6': 'old_jobattes6', 'Jobattes7': 'old_jobattes7', 'Jobattes8': 'old_jobattes8', 'ContractNo': 'old_contract_no', 'CustGrayID': 'old_cust_gray_id', 'GRealLoss': 'old_greal_loss', 'ColorE': 'old_color_e', 'ColorRemarks': 'old_color_remarks', 'OrderSheetNo': 'old_order_sheet_no', 'Model1': 'old_model1', 'PackRemarks': 'old_pack_remarks', 'jobattes9': 'old_jobattes9', 'jobattes10': 'old_jobattes10', 'OutDetailNo': 'old_out_detail_no', 'ProdBarCode': 'old_prod_bar_code'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_line_number': 'Chinese_PRC_CI_AS', 'old_customer_idname': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_structure': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_weight': 'Chinese_PRC_CI_AS', 'old_width': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_ardetail_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_process_memo': 'Chinese_PRC_CI_AS', 'old_atte': 'Chinese_PRC_CI_AS', 'old_in_sheet_no': 'Chinese_PRC_CI_AS', 'old_weight_unit': 'Chinese_PRC_CI_AS', 'old_width_kind_id': 'Chinese_PRC_CI_AS', 'old_details_customer': 'Chinese_PRC_CI_AS', 'old_cust_job_no': 'Chinese_PRC_CI_AS', 'old_color_depth_id': 'Chinese_PRC_CI_AS', 'old_warp_density': 'Chinese_PRC_CI_AS', 'old_weft_density': 'Chinese_PRC_CI_AS', 'old_fabric_id': 'Chinese_PRC_CI_AS', 'old_jobattes2': 'Chinese_PRC_CI_AS', 'old_cust_color_num': 'Chinese_PRC_CI_AS', 'old_phase_id': 'Chinese_PRC_CI_AS', 'old_jobattes5': 'Chinese_PRC_CI_AS', 'old_jobattes6': 'Chinese_PRC_CI_AS', 'old_jobattes7': 'Chinese_PRC_CI_AS', 'old_jobattes8': 'Chinese_PRC_CI_AS', 'old_contract_no': 'Chinese_PRC_CI_AS', 'old_cust_gray_id': 'Chinese_PRC_CI_AS', 'old_color_e': 'Chinese_PRC_CI_AS', 'old_color_remarks': 'Chinese_PRC_CI_AS', 'old_order_sheet_no': 'Chinese_PRC_CI_AS', 'old_model1': 'Chinese_PRC_CI_AS', 'old_pack_remarks': 'Chinese_PRC_CI_AS', 'old_jobattes9': 'Chinese_PRC_CI_AS', 'old_out_detail_no': 'Chinese_PRC_CI_AS', 'old_prod_bar_code': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：ProdLoading', 'target': 'erp_warehouse.SourceDyeProdLoading', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 ProdLoadingDetail → ProdLoading', '原界面主从 ProdLoadApproveDetail → ProdLoadApprove']}]
    SOURCE_DEFAULTS={'old_sheet_series': ('literal', ''), 'old_spec': ('literal', ''), 'old_structure': ('literal', ''), 'old_lot_no': ('literal', ''), 'old_color_id': ('literal', ''), 'old_color_num': ('literal', ''), 'old_out_rolls': ('literal', 0), 'old_weight_qty': ('literal', 0), 'old_length_qty': ('literal', 0), 'old_price': ('literal', 0), 'old_amount': ('literal', 0), 'old_check_no': ('literal', ''), 'old_ardetail_no': ('literal', ''), 'old_remarks': ('literal', '')}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=False, blank=True, max_length=36)
    old_line_number=models.CharField('行号', null=True, blank=True, max_length=20)
    old_customer_idname=models.CharField('客户', null=True, blank=True, max_length=50)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=500)
    old_structure=models.CharField('Structure', null=True, blank=True, max_length=500)
    old_lot_no=models.CharField('LotNo', null=True, blank=True, max_length=350)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=150)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=50)
    old_out_rolls=models.DecimalField('OutRolls', null=True, blank=True, max_digits=7, decimal_places=2)
    old_weight_qty=models.DecimalField('WeightQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_length_qty=models.DecimalField('LengthQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=8, decimal_places=2)
    old_amount=models.DecimalField('Amount', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight=models.CharField('Weight', null=True, blank=True, max_length=50)
    old_width=models.CharField('Width', null=True, blank=True, max_length=50)
    old_check_no=models.CharField('CheckNo', null=True, blank=True, max_length=20)
    old_ardetail_no=models.CharField('ARDetailNo', null=True, blank=True, max_length=20)
    old_remarks=models.TextField('备注', null=True, blank=True)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=20)
    old_stock_unit=models.IntegerField('StockUnit', null=True, blank=True)
    old_total=models.DecimalField('Total', null=True, blank=True, max_digits=10, decimal_places=2)
    old_process_price=models.DecimalField('ProcessPrice', null=True, blank=True, max_digits=8, decimal_places=2)
    old_atte_fee=models.DecimalField('AtteFee', null=True, blank=True, max_digits=10, decimal_places=2)
    old_vat_fee=models.DecimalField('VatFee', null=True, blank=True, max_digits=10, decimal_places=2)
    old_process_memo=models.TextField('ProcessMemo', null=True, blank=True)
    old_atte=models.CharField('Atte', null=True, blank=True, max_length=100)
    old_in_sheet_no=models.CharField('InSheetNo', null=True, blank=True, max_length=20)
    old_in_price=models.DecimalField('InPrice', null=True, blank=True, max_digits=8, decimal_places=2)
    old_in_process_price=models.DecimalField('InProcessPrice', null=True, blank=True, max_digits=8, decimal_places=2)
    old_in_atte_fee=models.DecimalField('InAtteFee', null=True, blank=True, max_digits=10, decimal_places=2)
    old_in_vat_fee=models.DecimalField('InVatFee', null=True, blank=True, max_digits=10, decimal_places=2)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_width_dn=models.DecimalField('WidthDn', null=True, blank=True, max_digits=6, decimal_places=2)
    old_width_up=models.DecimalField('WidthUp', null=True, blank=True, max_digits=6, decimal_places=2)
    old_weight_dn=models.DecimalField('WeightDn', null=True, blank=True, max_digits=6, decimal_places=2)
    old_weight_up=models.DecimalField('WeightUp', null=True, blank=True, max_digits=6, decimal_places=2)
    old_weight_unit=models.CharField('WeightUnit', null=True, blank=True, max_length=10)
    old_width_kind_id=models.CharField('WidthKindID', null=True, blank=True, max_length=10)
    old_pre_rolls=models.DecimalField('排单粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_details_customer=models.CharField('DetailsCustomer', null=True, blank=True, max_length=120)
    old_order_sheet_date=models.DateTimeField('OrderSheetDate', null=True, blank=True)
    old_att_price=models.DecimalField('AttPrice', null=True, blank=True, max_digits=8, decimal_places=2)
    old_color_add_price=models.DecimalField('ColorAddPrice', null=True, blank=True, max_digits=8, decimal_places=2)
    old_color_add_fee=models.DecimalField('ColorAddFee', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sum_assigned_length_qty=models.DecimalField('SumAssignedLengthQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_cust_job_no=models.CharField('CustJobNo', null=True, blank=True, max_length=200)
    old_color_depth_id=models.CharField('颜色深浅', null=True, blank=True, max_length=20)
    old_warp_density=models.CharField('WarpDensity', null=True, blank=True, max_length=50)
    old_weft_density=models.CharField('WeftDensity', null=True, blank=True, max_length=50)
    old_fabric_id=models.CharField('客户规格', null=True, blank=True, max_length=250)
    old_gray_qty=models.DecimalField('GrayQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_jobattes1=models.DecimalField('Jobattes1', null=True, blank=True, max_digits=10, decimal_places=2)
    old_jobattes2=models.TextField('Jobattes2', null=True, blank=True)
    old_cust_color_num=models.CharField('CustColorNum', null=True, blank=True, max_length=100)
    old_price_unit=models.IntegerField('PriceUnit', null=True, blank=True)
    old_phase_id=models.CharField('PhaseID', null=True, blank=True, max_length=10)
    old_jobattes3=models.DecimalField('Jobattes3', null=True, blank=True, max_digits=10, decimal_places=1)
    old_jobattes4=models.DecimalField('Jobattes4', null=True, blank=True, max_digits=10, decimal_places=1)
    old_jobattes5=models.TextField('Jobattes5', null=True, blank=True)
    old_jobattes6=models.CharField('Jobattes6', null=True, blank=True, max_length=200)
    old_jobattes7=models.CharField('Jobattes7', null=True, blank=True, max_length=200)
    old_jobattes8=models.CharField('Jobattes8', null=True, blank=True, max_length=200)
    old_contract_no=models.CharField('客户单号', null=True, blank=True, max_length=500)
    old_cust_gray_id=models.CharField('CustGrayID', null=True, blank=True, max_length=50)
    old_greal_loss=models.DecimalField('GRealLoss', null=True, blank=True, max_digits=10, decimal_places=2)
    old_color_e=models.CharField('ColorE', null=True, blank=True, max_length=20)
    old_color_remarks=models.CharField('用途', null=True, blank=True, max_length=500)
    old_order_sheet_no=models.CharField('OrderSheetNo', null=True, blank=True, max_length=50)
    old_model1=models.CharField('Model1', null=True, blank=True, max_length=200)
    old_pack_remarks=models.TextField('PackRemarks', null=True, blank=True)
    old_jobattes9=models.CharField('jobattes9', null=True, blank=True, max_length=100)
    old_jobattes10=models.DecimalField('jobattes10', null=True, blank=True, max_digits=10, decimal_places=1)
    old_out_detail_no=models.CharField('出库明细单号', null=True, blank=True, max_length=40)
    old_prod_bar_code=models.CharField('条码', null=True, blank=True, max_length=50)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeProdLoading', verbose_name='原关系：ProdLoading', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_prodloadingdetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_dc01c7a0bc2316fe'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_dc01c7a0bc2316fe')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（ProdLoadingDetail，待确认）'
        ordering=["-id"]

class SourceDyeProdOut(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProdOut'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'IsInputRecord': 'old_is_input_record', 'BusinessUnitID': 'old_business_unit_id', 'SalerGroupID': 'old_saler_group_id', 'SalerID': 'old_saler_id', 'CustomerID': 'old_customer_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'FactID': 'old_fact_id', 'StepNo': 'old_step_no', 'BusinessKind': 'old_business_kind', 'Discount': 'old_discount', 'PriceCheck': 'old_price_check', 'PriceChecker': 'old_price_checker', 'PriceCheckIdea': 'old_price_check_idea', 'PriceCheckTime': 'old_price_check_time', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'WareHouseID': 'old_ware_house_id', 'Cargador1': 'old_cargador1', 'Cargador2': 'old_cargador2', 'Cargador3': 'old_cargador3', 'Cargador4': 'old_cargador4', 'Cargador5': 'old_cargador5', 'Driver1': 'old_driver1', 'Driver2': 'old_driver2', 'Driver3': 'old_driver3', 'Discharger1': 'old_discharger1', 'Discharger2': 'old_discharger2', 'Driver': 'old_driver', 'CarNo': 'old_car_no', 'Keeper': 'old_keeper', 'DlvRolls': 'old_dlv_rolls', 'DlvLengthQty': 'old_dlv_length_qty', 'DlvWeightQty': 'old_dlv_weight_qty', 'DlvAddress': 'old_dlv_address', 'Phone': 'old_phone', 'CustomerCode': 'old_customer_code', 'WLLX': 'old_wllx', 'combo1': 'old_combo1', 'FHYSPC': 'old_fhyspc', 'UpCheckNo': 'old_up_check_no', 'UpLabelRemarks': 'old_up_label_remarks', 'UpLabelWareHouse': 'old_up_label_ware_house'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_saler_group_id': 'Chinese_PRC_CI_AS', 'old_saler_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_fact_id': 'Chinese_PRC_CI_AS', 'old_price_checker': 'Chinese_PRC_CI_AS', 'old_price_check_idea': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_cargador1': 'Chinese_PRC_CI_AS', 'old_cargador2': 'Chinese_PRC_CI_AS', 'old_cargador3': 'Chinese_PRC_CI_AS', 'old_cargador4': 'Chinese_PRC_CI_AS', 'old_cargador5': 'Chinese_PRC_CI_AS', 'old_driver1': 'Chinese_PRC_CI_AS', 'old_driver2': 'Chinese_PRC_CI_AS', 'old_driver3': 'Chinese_PRC_CI_AS', 'old_discharger1': 'Chinese_PRC_CI_AS', 'old_discharger2': 'Chinese_PRC_CI_AS', 'old_driver': 'Chinese_PRC_CI_AS', 'old_car_no': 'Chinese_PRC_CI_AS', 'old_keeper': 'Chinese_PRC_CI_AS', 'old_dlv_address': 'Chinese_PRC_CI_AS', 'old_phone': 'Chinese_PRC_CI_AS', 'old_customer_code': 'Chinese_PRC_CI_AS', 'old_wllx': 'Chinese_PRC_CI_AS', 'old_combo1': 'Chinese_PRC_CI_AS', 'old_fhyspc': 'Chinese_PRC_CI_AS', 'old_up_check_no': 'Chinese_PRC_CI_AS', 'old_up_label_remarks': 'Chinese_PRC_CI_AS', 'old_up_label_ware_house': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=False, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类别', null=True, blank=True)
    old_is_input_record=models.BooleanField('录入码单明细否', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('业务组别', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('业务员代码', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户代码', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_fact_id=models.CharField('工厂代码', null=True, blank=True, max_length=10)
    old_step_no=models.IntegerField('工作流节点号', null=True, blank=True)
    old_business_kind=models.IntegerField('BusinessKind', null=True, blank=True)
    old_discount=models.DecimalField('折扣', null=True, blank=True, max_digits=3, decimal_places=2)
    old_price_check=models.BooleanField('价格审核', null=True, blank=True)
    old_price_checker=models.CharField('价格审核人', null=True, blank=True, max_length=10)
    old_price_check_idea=models.CharField('价格审核意见', null=True, blank=True, max_length=300)
    old_price_check_time=models.DateTimeField('价格审核时间', null=True, blank=True)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_ware_house_id=models.CharField('存放仓库', null=True, blank=True, max_length=10)
    old_cargador1=models.CharField('目标客户', null=True, blank=True, max_length=10)
    old_cargador2=models.CharField('搬运工', null=True, blank=True, max_length=10)
    old_cargador3=models.CharField('搬运工', null=True, blank=True, max_length=10)
    old_cargador4=models.CharField('搬运工', null=True, blank=True, max_length=10)
    old_cargador5=models.CharField('搬运工', null=True, blank=True, max_length=10)
    old_driver1=models.CharField('司机电话', null=True, blank=True, max_length=10)
    old_driver2=models.CharField('叉车', null=True, blank=True, max_length=10)
    old_driver3=models.CharField('叉车', null=True, blank=True, max_length=10)
    old_discharger1=models.CharField('装卸工', null=True, blank=True, max_length=10)
    old_discharger2=models.CharField('装卸工', null=True, blank=True, max_length=10)
    old_driver=models.CharField('司机', null=True, blank=True, max_length=10)
    old_car_no=models.CharField('车牌号', null=True, blank=True, max_length=10)
    old_keeper=models.CharField('仓管员', null=True, blank=True, max_length=16)
    old_dlv_rolls=models.DecimalField('DlvRolls', null=True, blank=True, max_digits=6, decimal_places=1)
    old_dlv_length_qty=models.DecimalField('DlvLengthQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dlv_weight_qty=models.DecimalField('毛重', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dlv_address=models.CharField('送货地址', null=True, blank=True, max_length=300)
    old_phone=models.CharField('司机电话', null=True, blank=True, max_length=20)
    old_customer_code=models.CharField('客户全称', null=True, blank=True, max_length=50)
    old_wllx=models.CharField('物流类型', null=True, blank=True, max_length=255)
    old_combo1=models.CharField('收发地点', null=True, blank=True, max_length=10)
    old_fhyspc=models.CharField('送货运输编号', null=True, blank=True, max_length=20)
    old_up_check_no=models.CharField('调整订单号', null=True, blank=True, max_length=30)
    old_up_label_remarks=models.CharField('UpLabelRemarks', null=True, blank=True, max_length=500)
    old_up_label_ware_house=models.CharField('UpLabelWareHouse', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_prodout'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_e76d918302e49bb8'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_e76d918302e49bb8')]
        verbose_name=verbose_name_plural='成品出库单'
        ordering=["-id"]

class SourceDyeProdOutDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProdOutDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'Spec': 'old_spec', 'Structure': 'old_structure', 'LotNo': 'old_lot_no', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'OutRolls': 'old_out_rolls', 'WeightQty': 'old_weight_qty', 'LengthQty': 'old_length_qty', 'Price': 'old_price', 'Amount': 'old_amount', 'Weight': 'old_weight', 'Width': 'old_width', 'CheckNo': 'old_check_no', 'ARDetailNo': 'old_ardetail_no', 'Remarks': 'old_remarks', 'JobSheetNo': 'old_job_sheet_no', 'ProdID': 'old_prod_id', 'StockUnit': 'old_stock_unit', 'Total': 'old_total', 'ProcessPrice': 'old_process_price', 'AtteFee': 'old_atte_fee', 'VatFee': 'old_vat_fee', 'ProcessMemo': 'old_process_memo', 'Atte': 'old_atte', 'InSheetNo': 'old_in_sheet_no', 'InPrice': 'old_in_price', 'InProcessPrice': 'old_in_process_price', 'InAtteFee': 'old_in_atte_fee', 'InVatFee': 'old_in_vat_fee', 'Rolls': 'old_rolls', 'WidthDn': 'old_width_dn', 'WidthUp': 'old_width_up', 'WeightDn': 'old_weight_dn', 'WeightUp': 'old_weight_up', 'WeightUnit': 'old_weight_unit', 'WidthKindID': 'old_width_kind_id', 'PreRolls': 'old_pre_rolls', 'DetailsCustomer': 'old_details_customer', 'OrderSheetDate': 'old_order_sheet_date', 'AttPrice': 'old_att_price', 'ColorAddPrice': 'old_color_add_price', 'ColorAddFee': 'old_color_add_fee', 'SumAssignedLengthQty': 'old_sum_assigned_length_qty', 'CustJobNo': 'old_cust_job_no', 'ColorDepthID': 'old_color_depth_id', 'WarpDensity': 'old_warp_density', 'WeftDensity': 'old_weft_density', 'FabricID': 'old_fabric_id', 'GrayQty': 'old_gray_qty', 'Jobattes1': 'old_jobattes1', 'Jobattes2': 'old_jobattes2', 'CustColorNum': 'old_cust_color_num', 'PriceUnit': 'old_price_unit', 'PhaseID': 'old_phase_id', 'Jobattes3': 'old_jobattes3', 'Jobattes4': 'old_jobattes4', 'Jobattes5': 'old_jobattes5', 'Jobattes6': 'old_jobattes6', 'Jobattes7': 'old_jobattes7', 'Jobattes8': 'old_jobattes8', 'ContractNo': 'old_contract_no', 'CustGrayID': 'old_cust_gray_id', 'GRealLoss': 'old_greal_loss', 'ColorE': 'old_color_e', 'ColorRemarks': 'old_color_remarks', 'OrderSheetNo': 'old_order_sheet_no', 'Model1': 'old_model1', 'PackRemarks': 'old_pack_remarks', 'jobattes9': 'old_jobattes9', 'jobattes10': 'old_jobattes10', 'BarCode': 'old_bar_code', 'RollNo': 'old_roll_no', 'RealQty': 'old_real_qty', 'ProdBarCode': 'old_prod_bar_code', 'OutPacks': 'old_out_packs', 'NetKg': 'old_net_kg', 'PackBag': 'old_pack_bag', 'TubeWeight': 'old_tube_weight', 'ProdCode': 'old_prod_code', 'CustSelfNo': 'old_cust_self_no', 'YarnCategory': 'old_yarn_category', 'LabelWareHouse': 'old_label_ware_house', 'LabelRemarks': 'old_label_remarks', 'WindingID': 'old_winding_id', 'GradeID': 'old_grade_id', 'FenTou': 'old_fen_tou'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_structure': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_weight': 'Chinese_PRC_CI_AS', 'old_width': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_ardetail_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_process_memo': 'Chinese_PRC_CI_AS', 'old_atte': 'Chinese_PRC_CI_AS', 'old_in_sheet_no': 'Chinese_PRC_CI_AS', 'old_weight_unit': 'Chinese_PRC_CI_AS', 'old_width_kind_id': 'Chinese_PRC_CI_AS', 'old_details_customer': 'Chinese_PRC_CI_AS', 'old_cust_job_no': 'Chinese_PRC_CI_AS', 'old_color_depth_id': 'Chinese_PRC_CI_AS', 'old_warp_density': 'Chinese_PRC_CI_AS', 'old_weft_density': 'Chinese_PRC_CI_AS', 'old_fabric_id': 'Chinese_PRC_CI_AS', 'old_jobattes1': 'Chinese_PRC_CI_AS', 'old_jobattes2': 'Chinese_PRC_CI_AS', 'old_cust_color_num': 'Chinese_PRC_CI_AS', 'old_phase_id': 'Chinese_PRC_CI_AS', 'old_jobattes3': 'Chinese_PRC_CI_AS', 'old_jobattes4': 'Chinese_PRC_CI_AS', 'old_jobattes5': 'Chinese_PRC_CI_AS', 'old_jobattes6': 'Chinese_PRC_CI_AS', 'old_jobattes7': 'Chinese_PRC_CI_AS', 'old_jobattes8': 'Chinese_PRC_CI_AS', 'old_contract_no': 'Chinese_PRC_CI_AS', 'old_cust_gray_id': 'Chinese_PRC_CI_AS', 'old_color_e': 'Chinese_PRC_CI_AS', 'old_color_remarks': 'Chinese_PRC_CI_AS', 'old_order_sheet_no': 'Chinese_PRC_CI_AS', 'old_model1': 'Chinese_PRC_CI_AS', 'old_pack_remarks': 'Chinese_PRC_CI_AS', 'old_jobattes9': 'Chinese_PRC_CI_AS', 'old_jobattes10': 'Chinese_PRC_CI_AS', 'old_bar_code': 'Chinese_PRC_CI_AS', 'old_roll_no': 'Chinese_PRC_CI_AS', 'old_prod_bar_code': 'Chinese_PRC_CI_AS', 'old_prod_code': 'Chinese_PRC_CI_AS', 'old_cust_self_no': 'Chinese_PRC_CI_AS', 'old_yarn_category': 'Chinese_PRC_CI_AS', 'old_label_ware_house': 'Chinese_PRC_CI_AS', 'old_label_remarks': 'Chinese_PRC_CI_AS', 'old_winding_id': 'Chinese_PRC_CI_AS', 'old_grade_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：ProdOut', 'target': 'erp_warehouse.SourceDyeProdOut', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 ProdOutDetail → ProdOut', '原界面主从 ProdOutDetailUpdate → ProdOutUpdate']}]
    SOURCE_DEFAULTS={'old_sheet_series': ('literal', ''), 'old_spec': ('literal', ''), 'old_structure': ('literal', ''), 'old_lot_no': ('literal', ''), 'old_color_id': ('literal', ''), 'old_color_num': ('literal', ''), 'old_out_rolls': ('literal', 0), 'old_weight_qty': ('literal', 0), 'old_length_qty': ('literal', 0), 'old_price': ('literal', 0), 'old_amount': ('literal', 0), 'old_check_no': ('literal', ''), 'old_ardetail_no': ('literal', ''), 'old_remarks': ('literal', '')}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('表单明细号（子表）', null=False, blank=True, max_length=36)
    old_spec=models.CharField('捻度(H/S)', null=True, blank=True, max_length=500)
    old_structure=models.CharField('组织', null=True, blank=True, max_length=500)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=350)
    old_color_id=models.CharField('颜色编码', null=True, blank=True, max_length=150)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=50)
    old_out_rolls=models.DecimalField('出库粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_weight_qty=models.DecimalField('毛重', null=True, blank=True, max_digits=10, decimal_places=2)
    old_length_qty=models.DecimalField('成品长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_amount=models.DecimalField('金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight=models.CharField('克重', null=True, blank=True, max_length=50)
    old_width=models.CharField('幅宽', null=True, blank=True, max_length=50)
    old_check_no=models.CharField('订单明细号', null=True, blank=True, max_length=20)
    old_ardetail_no=models.CharField('应收单细号', null=True, blank=True, max_length=20)
    old_remarks=models.TextField('备注', null=True, blank=True)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=20)
    old_stock_unit=models.IntegerField('库存单位', null=True, blank=True)
    old_total=models.DecimalField('合计', null=True, blank=True, max_digits=10, decimal_places=2)
    old_process_price=models.DecimalField('特殊工序单价', null=True, blank=True, max_digits=8, decimal_places=2)
    old_atte_fee=models.DecimalField('纸筒', null=True, blank=True, max_digits=10, decimal_places=2)
    old_vat_fee=models.DecimalField('空加', null=True, blank=True, max_digits=10, decimal_places=2)
    old_process_memo=models.TextField('ProcessMemo', null=True, blank=True)
    old_atte=models.CharField('事项', null=True, blank=True, max_length=100)
    old_in_sheet_no=models.CharField('InSheetNo', null=True, blank=True, max_length=20)
    old_in_price=models.DecimalField('InPrice', null=True, blank=True, max_digits=8, decimal_places=2)
    old_in_process_price=models.DecimalField('InProcessPrice', null=True, blank=True, max_digits=8, decimal_places=2)
    old_in_atte_fee=models.DecimalField('InAtteFee', null=True, blank=True, max_digits=10, decimal_places=2)
    old_in_vat_fee=models.DecimalField('InVatFee', null=True, blank=True, max_digits=10, decimal_places=2)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_width_dn=models.DecimalField('门幅下限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_width_up=models.DecimalField('门幅上限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_weight_dn=models.DecimalField('克重下限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_weight_up=models.DecimalField('克重上限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_weight_unit=models.CharField('克重单位', null=True, blank=True, max_length=10)
    old_width_kind_id=models.CharField('门幅单位', null=True, blank=True, max_length=10)
    old_pre_rolls=models.DecimalField('排单粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_details_customer=models.CharField('织厂', null=True, blank=True, max_length=120)
    old_order_sheet_date=models.DateTimeField('下单日期', null=True, blank=True)
    old_att_price=models.DecimalField('特殊要求单价', null=True, blank=True, max_digits=8, decimal_places=2)
    old_color_add_price=models.DecimalField('色号加价', null=True, blank=True, max_digits=8, decimal_places=2)
    old_color_add_fee=models.DecimalField('ColorAddFee', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sum_assigned_length_qty=models.DecimalField('胚纱长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_cust_job_no=models.CharField('客户缸号', null=True, blank=True, max_length=200)
    old_color_depth_id=models.CharField('颜色深浅', null=True, blank=True, max_length=20)
    old_warp_density=models.CharField('WarpDensity', null=True, blank=True, max_length=50)
    old_weft_density=models.CharField('WeftDensity', null=True, blank=True, max_length=50)
    old_fabric_id=models.CharField('客户规格', null=True, blank=True, max_length=250)
    old_gray_qty=models.DecimalField('胚重', null=True, blank=True, max_digits=10, decimal_places=2)
    old_jobattes1=models.TextField('加工要求', null=True, blank=True)
    old_jobattes2=models.TextField('收费项目', null=True, blank=True)
    old_cust_color_num=models.CharField('CustColorNum', null=True, blank=True, max_length=100)
    old_price_unit=models.IntegerField('单价单位', null=True, blank=True)
    old_phase_id=models.CharField('套染', null=True, blank=True, max_length=10)
    old_jobattes3=models.CharField('幅宽', null=True, blank=True, max_length=500)
    old_jobattes4=models.CharField('克重', null=True, blank=True, max_length=100)
    old_jobattes5=models.TextField('Jobattes5', null=True, blank=True)
    old_jobattes6=models.CharField('Jobattes6', null=True, blank=True, max_length=200)
    old_jobattes7=models.CharField('胶袋', null=True, blank=True, max_length=200)
    old_jobattes8=models.CharField('加重', null=True, blank=True, max_length=200)
    old_contract_no=models.CharField('客户单号', null=True, blank=True, max_length=500)
    old_cust_gray_id=models.CharField('CustGrayID', null=True, blank=True, max_length=50)
    old_greal_loss=models.DecimalField('GRealLoss', null=True, blank=True, max_digits=10, decimal_places=2)
    old_color_e=models.CharField('ColorE', null=True, blank=True, max_length=20)
    old_color_remarks=models.CharField('用途', null=True, blank=True, max_length=500)
    old_order_sheet_no=models.CharField('本厂订单号', null=True, blank=True, max_length=50)
    old_model1=models.CharField('款号', null=True, blank=True, max_length=200)
    old_pack_remarks=models.TextField('包装要求', null=True, blank=True)
    old_jobattes9=models.CharField('jobattes9', null=True, blank=True, max_length=100)
    old_jobattes10=models.CharField('jobattes10', null=True, blank=True, max_length=100)
    old_bar_code=models.CharField('条码', null=True, blank=True, max_length=30)
    old_roll_no=models.CharField('箱号', null=False, blank=True, max_length=20)
    old_real_qty=models.DecimalField('磅重', null=True, blank=True, max_digits=10, decimal_places=2)
    old_prod_bar_code=models.CharField('包装条码', null=True, blank=True, max_length=200)
    old_out_packs=models.DecimalField('件数', null=True, blank=True, max_digits=6, decimal_places=1)
    old_net_kg=models.DecimalField('净重', null=True, blank=True, max_digits=6, decimal_places=2)
    old_pack_bag=models.DecimalField('包装重量', null=True, blank=True, max_digits=7, decimal_places=3)
    old_tube_weight=models.DecimalField('纸筒重', null=True, blank=True, max_digits=7, decimal_places=3)
    old_prod_code=models.CharField('二维码字段', null=True, blank=True, max_length=50)
    old_cust_self_no=models.CharField('制单号', null=True, blank=True, max_length=150)
    old_yarn_category=models.CharField('纱类别', null=True, blank=True, max_length=50)
    old_label_ware_house=models.CharField('标签仓库', null=True, blank=True, max_length=100)
    old_label_remarks=models.CharField('标签用途', null=True, blank=True, max_length=500)
    old_winding_id=models.CharField('络筒员工', null=True, blank=True, max_length=30)
    old_grade_id=models.CharField('等级', null=True, blank=True, max_length=10)
    old_fen_tou=models.DecimalField('分头', null=True, blank=True, max_digits=6, decimal_places=2)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeProdOut', verbose_name='原关系：ProdOut', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_prodoutdetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_1b7df9115e62a065'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_1b7df9115e62a065'),models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_3ed5380494e7c8ed'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_3ed5380494e7c8ed')]
        verbose_name=verbose_name_plural='成品出库明细'
        ordering=["-id"]

class SourceDyeProdOutPDARecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProdOutPDARecord'
    SOURCE_FIELDS={'BarCode': 'old_bar_code', 'CurrTime': 'old_curr_time', 'Geter': 'old_geter', 'Status': 'old_status'}
    SOURCE_KEY=('BarCode',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_bar_code': 'Chinese_PRC_CI_AS', 'old_geter': 'Chinese_PRC_CI_AS', 'old_status': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_bar_code=models.CharField('BarCode', null=False, blank=True, max_length=50)
    old_curr_time=models.DateTimeField('CurrTime', null=True, blank=True)
    old_geter=models.CharField('Geter', null=True, blank=True, max_length=10)
    old_status=models.CharField('Status', null=True, blank=True, max_length=1)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_prodoutpdarecord'
        indexes=[models.Index(fields=['source_batch', 'old_bar_code'],name='src_3266e499599da8cc'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_bar_code'))),name='src_ci_3266e499599da8cc')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（ProdOutPDARecord，待确认）'
        ordering=["-id"]

class SourceDyeProdOutPriceAtte(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProdOutPriceAtte'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'AtteCode': 'old_atte_code', 'Price': 'old_price', 'PriceUnit': 'old_price_unit', 'InPrice': 'old_in_price', 'FieldType': 'old_field_type', 'AtteValue': 'old_atte_value', 'Description': 'old_description'}
    SOURCE_KEY=('SheetSeries', 'DetailNo', 'FieldType', 'AtteCode')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_atte_code': 'Chinese_PRC_CI_AS', 'old_field_type': 'Chinese_PRC_CI_AS', 'old_atte_value': 'Chinese_PRC_CI_AS', 'old_description': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：ProdOutDetail', 'target': 'erp_warehouse.SourceDyeProdOutDetail', 'source_fields': ['SheetSeries', 'DetailNo'], 'target_fields': ['SheetSeries', 'DetailNo'], 'evidence': ['原界面主从 ProdOutPriceAtte → ProdOutDetail']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('明细号', null=False, blank=True, max_length=36)
    old_atte_code=models.CharField('事项代码', null=False, blank=True, max_length=10)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=8, decimal_places=2)
    old_price_unit=models.IntegerField('计价单位', null=True, blank=True)
    old_in_price=models.DecimalField('单价', null=True, blank=True, max_digits=8, decimal_places=2)
    old_field_type=models.CharField('要求类别', null=False, blank=True, max_length=20)
    old_atte_value=models.CharField('事项内容', null=True, blank=True, max_length=500)
    old_description=models.CharField('描述', null=True, blank=True, max_length=500)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeProdOutDetail', verbose_name='原关系：ProdOutDetail', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_prodoutpriceatte'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no', 'old_field_type', 'old_atte_code'],name='src_d66dcc17f27212ae'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),Upper(RTrim(models.F('old_field_type'))),Upper(RTrim(models.F('old_atte_code'))),name='src_ci_d66dcc17f27212ae')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（ProdOutPriceAtte，待确认）'
        ordering=["-id"]

class SourceDyeProdOutPriceProcess(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProdOutPriceProcess'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'ProcessID': 'old_process_id', 'Price': 'old_price', 'Remarks': 'old_remarks', 'InPrice': 'old_in_price'}
    SOURCE_KEY=('SheetSeries', 'DetailNo', 'ProcessID')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_process_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=False, blank=True, max_length=36)
    old_process_id=models.CharField('ProcessID', null=False, blank=True, max_length=50)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=8, decimal_places=2)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=300)
    old_in_price=models.DecimalField('InPrice', null=True, blank=True, max_digits=8, decimal_places=2)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_prodoutpriceprocess'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no', 'old_process_id'],name='src_562a2f01d8a9577c'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),Upper(RTrim(models.F('old_process_id'))),name='src_ci_562a2f01d8a9577c')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（ProdOutPriceProcess，待确认）'
        ordering=["-id"]

class SourceDyeProdOutRecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProdOutRecord'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'RollNo': 'old_roll_no', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'StorageUnitID': 'old_storage_unit_id', 'Status': 'old_status', 'OutDetailNo': 'old_out_detail_no', 'BarCode': 'old_bar_code', 'GradeID': 'old_grade_id', 'GrayQty': 'old_gray_qty', 'AdjustQty': 'old_adjust_qty', 'DetailNo': 'old_detail_no', 'RealQty': 'old_real_qty', 'Meter': 'old_meter', 'Yard': 'old_yard', 'GrayBarCode': 'old_gray_bar_code', 'RollNo3': 'old_roll_no3', 'GUnit': 'old_gunit', 'PUnit': 'old_punit', 'Rolls': 'old_rolls', 'GKg': 'old_gkg', 'GPound': 'old_gpound', 'PKg': 'old_pkg', 'PPound': 'old_ppound'}
    SOURCE_KEY=('SheetSeries', 'RollNo', 'BarCode', 'DetailNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_roll_no': 'Chinese_PRC_CI_AS', 'old_storage_unit_id': 'Chinese_PRC_CI_AS', 'old_status': 'Chinese_PRC_CI_AS', 'old_out_detail_no': 'Chinese_PRC_CI_AS', 'old_bar_code': 'Chinese_PRC_CI_AS', 'old_grade_id': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_gray_bar_code': 'Chinese_PRC_CI_AS', 'old_roll_no3': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：ProdOutDetail', 'target': 'erp_warehouse.SourceDyeProdOutDetail', 'source_fields': ['SheetSeries', 'DetailNo'], 'target_fields': ['SheetSeries', 'DetailNo'], 'evidence': ['原界面主从 ProdOutRecord → ProdOutDetail', '原界面主从 ProdOutRecordUpdate → ProdOutDetailUpdate']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('出库单流水号', null=False, blank=True, max_length=20)
    old_roll_no=models.CharField('箱号', null=False, blank=True, max_length=20)
    old_length_qty=models.DecimalField('成品长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('毛重', null=True, blank=True, max_digits=10, decimal_places=1)
    old_storage_unit_id=models.CharField('库位', null=True, blank=True, max_length=10)
    old_status=models.CharField('状态', null=True, blank=True, max_length=1)
    old_out_detail_no=models.CharField('OutDetailNo', null=True, blank=True, max_length=20)
    old_bar_code=models.CharField('条码', null=False, blank=True, max_length=50)
    old_grade_id=models.CharField('色号等级', null=True, blank=True, max_length=10)
    old_gray_qty=models.DecimalField('胚纱重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_adjust_qty=models.DecimalField('AdjustQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_detail_no=models.CharField('出库明细号', null=False, blank=True, max_length=36)
    old_real_qty=models.DecimalField('实重', null=True, blank=True, max_digits=10, decimal_places=2)
    old_meter=models.DecimalField('长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_yard=models.DecimalField('胚纱长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_gray_bar_code=models.CharField('GrayBarCode', null=True, blank=True, max_length=100)
    old_roll_no3=models.CharField('箱号2', null=True, blank=True, max_length=20)
    old_gunit=models.IntegerField('GUnit', null=True, blank=True)
    old_punit=models.IntegerField('PUnit', null=True, blank=True)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=5, decimal_places=1)
    old_gkg=models.DecimalField('GKg', null=True, blank=True, max_digits=6, decimal_places=2)
    old_gpound=models.DecimalField('GPound', null=True, blank=True, max_digits=6, decimal_places=2)
    old_pkg=models.DecimalField('PKg', null=True, blank=True, max_digits=6, decimal_places=2)
    old_ppound=models.DecimalField('PPound', null=True, blank=True, max_digits=6, decimal_places=2)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeProdOutDetail', verbose_name='原关系：ProdOutDetail', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_prodoutrecord'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_roll_no', 'old_bar_code', 'old_detail_no'],name='src_3c04fb62f2e0cca8'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_roll_no'))),Upper(RTrim(models.F('old_bar_code'))),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_3c04fb62f2e0cca8')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（ProdOutRecord，待确认）'
        ordering=["-id"]

class SourceDyeProdStock(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProdStock'
    SOURCE_FIELDS={'StockDate': 'old_stock_date', 'BusinessUnitID': 'old_business_unit_id', 'CustomerID': 'old_customer_id', 'FactID': 'old_fact_id', 'WareHouseID': 'old_ware_house_id', 'SalerGroupID': 'old_saler_group_id', 'ProdID': 'old_prod_id', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'JobSheetNo': 'old_job_sheet_no', 'SalerID': 'old_saler_id', 'BusinessKind': 'old_business_kind', 'PreMonthRolls': 'old_pre_month_rolls', 'Price': 'old_price', 'CarryDate': 'old_carry_date', 'Remarks': 'old_remarks', 'PreMonthLengthQty': 'old_pre_month_length_qty', 'PreMonthWeightQty': 'old_pre_month_weight_qty'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_fact_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_saler_group_id': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_saler_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_stock_date=models.DateTimeField('StockDate', null=False, blank=False)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('CustomerID', null=False, blank=True, max_length=10)
    old_fact_id=models.CharField('FactID', null=True, blank=True, max_length=10)
    old_ware_house_id=models.CharField('WareHouseID', null=False, blank=True, max_length=10)
    old_saler_group_id=models.CharField('SalerGroupID', null=True, blank=True, max_length=10)
    old_prod_id=models.CharField('ProdID', null=True, blank=True, max_length=20)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=128)
    old_lot_no=models.CharField('LotNo', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=20)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)
    old_saler_id=models.CharField('SalerID', null=True, blank=True, max_length=10)
    old_business_kind=models.IntegerField('BusinessKind', null=True, blank=True)
    old_pre_month_rolls=models.DecimalField('PreMonthRolls', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=8, decimal_places=2)
    old_carry_date=models.DateTimeField('CarryDate', null=False, blank=False)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_pre_month_length_qty=models.DecimalField('PreMonthLengthQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pre_month_weight_qty=models.DecimalField('PreMonthWeightQty', null=True, blank=True, max_digits=10, decimal_places=2)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_prodstock'
        indexes=[]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（ProdStock，待确认）'
        ordering=["-id"]

class SourceDyeProdStockAdjust(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProdStockAdjust'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'BusinessUnitID': 'old_business_unit_id', 'BusinessKind': 'old_business_kind', 'SalerGroupID': 'old_saler_group_id', 'CustomerID': 'old_customer_id', 'WareHouseID': 'old_ware_house_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_saler_group_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('单号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('类型', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位', null=True, blank=True, max_length=10)
    old_business_kind=models.IntegerField('业务类型', null=True, blank=True)
    old_saler_group_id=models.CharField('业务组别', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=10)
    old_ware_house_id=models.CharField('仓库', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核', null=True, blank=True)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_print_times=models.IntegerField('PrintTimes', null=True, blank=True)
    old_revisions=models.IntegerField('Revisions', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_prodstockadjust'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_0d805c41c31eb647'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_0d805c41c31eb647')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（ProdStockAdjust，待确认）'
        ordering=["-id"]

class SourceDyeProdStockAdjustDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProdStockAdjustDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'JobSheetNo': 'old_job_sheet_no', 'CheckNo': 'old_check_no', 'ProdID': 'old_prod_id', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'PaperRolls': 'old_paper_rolls', 'RealRolls': 'old_real_rolls', 'AdjustRolls': 'old_adjust_rolls', 'Price': 'old_price', 'StockUnit': 'old_stock_unit', 'Remarks': 'old_remarks', 'PaperLength': 'old_paper_length', 'PaperWeight': 'old_paper_weight', 'RealWeightQty': 'old_real_weight_qty', 'RealLengthQty': 'old_real_length_qty', 'AdjustLengthQty': 'old_adjust_length_qty', 'AdjustWeightQty': 'old_adjust_weight_qty', 'CustomerID': 'old_customer_id'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：ProdStockAdjust', 'target': 'erp_warehouse.SourceDyeProdStockAdjust', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 ProdStockAdjustDetail → ProdStockAdjust']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('明细号', null=False, blank=True, max_length=36)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_check_no=models.CharField('订单明细号', null=True, blank=True, max_length=20)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=20)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=128)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=20)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=20)
    old_paper_rolls=models.DecimalField('账面粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_rolls=models.IntegerField('实际粒数', null=True, blank=True)
    old_adjust_rolls=models.DecimalField('调整粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=8, decimal_places=2)
    old_stock_unit=models.IntegerField('单位', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_paper_length=models.DecimalField('账面长度', null=True, blank=True, max_digits=10, decimal_places=5)
    old_paper_weight=models.DecimalField('账面重量', null=True, blank=True, max_digits=10, decimal_places=5)
    old_real_weight_qty=models.DecimalField('实际重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_length_qty=models.DecimalField('实际长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_adjust_length_qty=models.DecimalField('调整长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_adjust_weight_qty=models.DecimalField('调整重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=50)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeProdStockAdjust', verbose_name='原关系：ProdStockAdjust', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_prodstockadjustdetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_c03d1e21c3799ca7'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_c03d1e21c3799ca7')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（ProdStockAdjustDetail，待确认）'
        ordering=["-id"]

class SourceDyeProdStockAllot(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProdStockAllot'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'FromSaleGroupID': 'old_from_sale_group_id', 'ToSalerGroupID': 'old_to_saler_group_id', 'FromWareHouseID': 'old_from_ware_house_id', 'ToReceSheetNo': 'old_to_rece_sheet_no', 'FromCustomerID': 'old_from_customer_id', 'ToCustomerID': 'old_to_customer_id', 'FromJobDetailNo': 'old_from_job_detail_no', 'ToJobDetailNo': 'old_to_job_detail_no', 'FromCheckNo': 'old_from_check_no', 'ToCheckNo': 'old_to_check_no', 'FromReceSheetNo': 'old_from_rece_sheet_no', 'ToWareHouseID': 'old_to_ware_house_id', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'Rolls': 'old_rolls', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'FromBusinessUnitID': 'old_from_business_unit_id', 'ToBusinessUnitID': 'old_to_business_unit_id', 'FromFabricID': 'old_from_fabric_id', 'ToFabricID': 'old_to_fabric_id', 'FromLotNo': 'old_from_lot_no', 'ToLotNo': 'old_to_lot_no', 'FromPrice': 'old_from_price', 'ToPrice': 'old_to_price', 'FromSalerID': 'old_from_saler_id', 'ToSalerID': 'old_to_saler_id', 'FromSpec': 'old_from_spec', 'ToSpec': 'old_to_spec', 'FromStructure': 'old_from_structure', 'ToStructure': 'old_to_structure', 'StockUnit': 'old_stock_unit', 'StepNo': 'old_step_no', 'BusinessKind': 'old_business_kind', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_from_sale_group_id': 'Chinese_PRC_CI_AS', 'old_to_saler_group_id': 'Chinese_PRC_CI_AS', 'old_from_ware_house_id': 'Chinese_PRC_CI_AS', 'old_to_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_from_customer_id': 'Chinese_PRC_CI_AS', 'old_to_customer_id': 'Chinese_PRC_CI_AS', 'old_from_job_detail_no': 'Chinese_PRC_CI_AS', 'old_to_job_detail_no': 'Chinese_PRC_CI_AS', 'old_from_check_no': 'Chinese_PRC_CI_AS', 'old_to_check_no': 'Chinese_PRC_CI_AS', 'old_from_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_to_ware_house_id': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_from_business_unit_id': 'Chinese_PRC_CI_AS', 'old_to_business_unit_id': 'Chinese_PRC_CI_AS', 'old_from_fabric_id': 'Chinese_PRC_CI_AS', 'old_to_fabric_id': 'Chinese_PRC_CI_AS', 'old_from_lot_no': 'Chinese_PRC_CI_AS', 'old_to_lot_no': 'Chinese_PRC_CI_AS', 'old_from_saler_id': 'Chinese_PRC_CI_AS', 'old_to_saler_id': 'Chinese_PRC_CI_AS', 'old_from_spec': 'Chinese_PRC_CI_AS', 'old_to_spec': 'Chinese_PRC_CI_AS', 'old_from_structure': 'Chinese_PRC_CI_AS', 'old_to_structure': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=False, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_from_sale_group_id=models.CharField('来源业务组别', null=True, blank=True, max_length=10)
    old_to_saler_group_id=models.CharField('目标业务组别', null=True, blank=True, max_length=10)
    old_from_ware_house_id=models.CharField('来源仓库', null=True, blank=True, max_length=10)
    old_to_rece_sheet_no=models.CharField('目标明细单号', null=True, blank=True, max_length=20)
    old_from_customer_id=models.CharField('来源客户', null=True, blank=True, max_length=10)
    old_to_customer_id=models.CharField('目标客户', null=True, blank=True, max_length=10)
    old_from_job_detail_no=models.CharField('来源加工作业单号', null=True, blank=True, max_length=20)
    old_to_job_detail_no=models.CharField('目标加工作业编号', null=True, blank=True, max_length=20)
    old_from_check_no=models.CharField('来源订单号', null=True, blank=True, max_length=20)
    old_to_check_no=models.CharField('目标订单号', null=True, blank=True, max_length=20)
    old_from_rece_sheet_no=models.CharField('来源收纱单号', null=True, blank=True, max_length=20)
    old_to_ware_house_id=models.CharField('目标仓库', null=True, blank=True, max_length=10)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=20)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=20)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_from_business_unit_id=models.CharField('源经营单位', null=True, blank=True, max_length=10)
    old_to_business_unit_id=models.CharField('目标经营单位', null=True, blank=True, max_length=10)
    old_from_fabric_id=models.CharField('来源产品编码', null=True, blank=True, max_length=10)
    old_to_fabric_id=models.CharField('目标产品编码', null=True, blank=True, max_length=10)
    old_from_lot_no=models.CharField('来源批号', null=True, blank=True, max_length=50)
    old_to_lot_no=models.CharField('目标批号', null=True, blank=True, max_length=50)
    old_from_price=models.DecimalField('来源价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_to_price=models.DecimalField('目标价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_from_saler_id=models.CharField('来源业务员', null=True, blank=True, max_length=10)
    old_to_saler_id=models.CharField('目标业务员', null=True, blank=True, max_length=10)
    old_from_spec=models.CharField('来源规格', null=True, blank=True, max_length=50)
    old_to_spec=models.CharField('目标规格', null=True, blank=True, max_length=50)
    old_from_structure=models.CharField('来源组织', null=True, blank=True, max_length=50)
    old_to_structure=models.CharField('目标组织', null=True, blank=True, max_length=50)
    old_stock_unit=models.IntegerField('库存单位', null=True, blank=True)
    old_step_no=models.IntegerField('工作流节点号', null=True, blank=True)
    old_business_kind=models.IntegerField('BusinessKind', null=True, blank=True)
    old_length_qty=models.DecimalField('LengthQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('WeightQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_prodstockallot'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_70696acacc98f59f'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_70696acacc98f59f')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（ProdStockAllot，待确认）'
        ordering=["-id"]

class SourceDyeProdStockBook(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProdStockBook'
    SOURCE_FIELDS={'BookNo': 'old_book_no', 'BookKind': 'old_book_kind', 'BookDate': 'old_book_date', 'BusinessUnitID': 'old_business_unit_id', 'CustomerID': 'old_customer_id', 'FactID': 'old_fact_id', 'WareHouseID': 'old_ware_house_id', 'StorageUnitIDs': 'old_storage_unit_ids', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'SalerGroupID': 'old_saler_group_id', 'CheckNo': 'old_check_no', 'SheetNo': 'old_sheet_no', 'DetailNo': 'old_detail_no', 'InRolls': 'old_in_rolls', 'OutRolls': 'old_out_rolls', 'Price': 'old_price', 'Remarks': 'old_remarks', 'BusinessKind': 'old_business_kind', 'ProdID': 'old_prod_id', 'JobSheetNo': 'old_job_sheet_no', 'SalerID': 'old_saler_id', 'InLengthQty': 'old_in_length_qty', 'InWeightQty': 'old_in_weight_qty', 'InGrayQty': 'old_in_gray_qty', 'OutLengthQty': 'old_out_length_qty', 'OutWeightQty': 'old_out_weight_qty', 'OutGrayQty': 'old_out_gray_qty', 'StockFlag': 'old_stock_flag', 'SheetSeries': 'old_sheet_series', 'InMoney': 'old_in_money', 'OutMoney': 'old_out_money', 'InNetKg': 'old_in_net_kg', 'OutNetKg': 'old_out_net_kg', 'CurrDate': 'old_curr_date'}
    SOURCE_KEY=('BookNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_fact_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_storage_unit_ids': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_saler_group_id': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_saler_id': 'Chinese_PRC_CI_AS', 'old_stock_flag': 'Chinese_PRC_CI_AS', 'old_sheet_series': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=('old_book_no',)
    SOURCE_IDENTITY_RULES={'old_book_no': (1, 1)}
    old_book_no=models.BigIntegerField('BookNo', null=False, blank=False)
    old_book_kind=models.IntegerField('BookKind', null=True, blank=True)
    old_book_date=models.DateTimeField('BookDate', null=True, blank=True)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=10)
    old_fact_id=models.CharField('FactID', null=True, blank=True, max_length=250)
    old_ware_house_id=models.CharField('WareHouseID', null=True, blank=True, max_length=10)
    old_storage_unit_ids=models.CharField('StorageUnitIDs', null=True, blank=True, max_length=100)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=128)
    old_lot_no=models.CharField('LotNo', null=True, blank=True, max_length=250)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=150)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=50)
    old_saler_group_id=models.CharField('SalerGroupID', null=True, blank=True, max_length=10)
    old_check_no=models.CharField('CheckNo', null=True, blank=True, max_length=20)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=True, blank=True, max_length=36)
    old_in_rolls=models.DecimalField('InRolls', null=True, blank=True, max_digits=7, decimal_places=2)
    old_out_rolls=models.DecimalField('OutRolls', null=True, blank=True, max_digits=7, decimal_places=2)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=8, decimal_places=2)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_business_kind=models.IntegerField('BusinessKind', null=True, blank=True)
    old_prod_id=models.CharField('ProdID', null=True, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)
    old_saler_id=models.CharField('SalerID', null=True, blank=True, max_length=10)
    old_in_length_qty=models.DecimalField('InLengthQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_in_weight_qty=models.DecimalField('InWeightQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_in_gray_qty=models.DecimalField('InGrayQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_out_length_qty=models.DecimalField('OutLengthQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_out_weight_qty=models.DecimalField('OutWeightQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_out_gray_qty=models.DecimalField('OutGrayQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_stock_flag=models.CharField('StockFlag', null=True, blank=True, max_length=1)
    old_sheet_series=models.CharField('SheetSeries', null=True, blank=True, max_length=50)
    old_in_money=models.DecimalField('InMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_out_money=models.DecimalField('OutMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_in_net_kg=models.DecimalField('InNetKg', null=True, blank=True, max_digits=10, decimal_places=2)
    old_out_net_kg=models.DecimalField('OutNetKg', null=True, blank=True, max_digits=10, decimal_places=2)
    old_curr_date=models.DateTimeField('CurrDate', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_prodstockbook'
        indexes=[models.Index(fields=['source_batch', 'old_book_no'],name='src_25354ba05df640c6')]
        verbose_name=verbose_name_plural='成品库存流水'
        ordering=["-id"]

class SourceDyeProdStockCheck(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProdStockCheck'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'BusinessUnitID': 'old_business_unit_id', 'SalerGroupID': 'old_saler_group_id', 'WareHouseID': 'old_ware_house_id', 'ProdKindID': 'old_prod_kind_id', 'CustomerID': 'old_customer_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'StepNo': 'old_step_no', 'BusinessKind': 'old_business_kind'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_saler_group_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_prod_kind_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类别', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('业务组别', null=True, blank=True, max_length=10)
    old_ware_house_id=models.CharField('仓库代码', null=True, blank=True, max_length=10)
    old_prod_kind_id=models.CharField('成品类别编码', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户代码', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_step_no=models.IntegerField('工作流节点号', null=True, blank=True)
    old_business_kind=models.IntegerField('BusinessKind', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_prodstockcheck'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_3177ffe1184a1954'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_3177ffe1184a1954')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（ProdStockCheck，待确认）'
        ordering=["-id"]

class SourceDyeProdStockCheckDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProdStockCheckDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'JobSheetNo': 'old_job_sheet_no', 'CheckNo': 'old_check_no', 'ProdID': 'old_prod_id', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'PaperRolls': 'old_paper_rolls', 'PaperQty': 'old_paper_qty', 'RealQty': 'old_real_qty', 'RealRolls': 'old_real_rolls', 'AdjustQty': 'old_adjust_qty', 'AdjustRolls': 'old_adjust_rolls', 'Price': 'old_price', 'StockUnit': 'old_stock_unit', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=True, blank=True, max_length=36)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)
    old_check_no=models.CharField('CheckNo', null=True, blank=True, max_length=20)
    old_prod_id=models.CharField('ProdID', null=True, blank=True, max_length=20)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=50)
    old_lot_no=models.CharField('LotNo', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=20)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=20)
    old_paper_rolls=models.DecimalField('PaperRolls', null=True, blank=True, max_digits=10, decimal_places=2)
    old_paper_qty=models.DecimalField('PaperQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_qty=models.DecimalField('RealQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_rolls=models.IntegerField('RealRolls', null=True, blank=True)
    old_adjust_qty=models.DecimalField('AdjustQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_adjust_rolls=models.DecimalField('AdjustRolls', null=True, blank=True, max_digits=7, decimal_places=2)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=8, decimal_places=2)
    old_stock_unit=models.IntegerField('StockUnit', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_prodstockcheckdetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_754849f745a78393'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_754849f745a78393')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（ProdStockCheckDetail，待确认）'
        ordering=["-id"]

class SourceDyeProdStorageAdjust(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProdStorageAdjust'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetKind': 'old_sheet_kind', 'SheetDate': 'old_sheet_date', 'StepNo': 'old_step_no', 'RightStatus': 'old_right_status', 'SheetStatus': 'old_sheet_status', 'SalerID': 'old_saler_id', 'CustomerID': 'old_customer_id', 'WareHouseID': 'old_ware_house_id', 'ToWareHouseID': 'old_to_ware_house_id', 'PrintTimes': 'old_print_times', 'CarryerID': 'old_carryer_id', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_saler_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_to_ware_house_id': 'Chinese_PRC_CI_AS', 'old_carryer_id': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('单据号', null=True, blank=True, max_length=20)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_sheet_status=models.IntegerField('SheetStatus', null=True, blank=True)
    old_saler_id=models.CharField('业务员', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=10)
    old_ware_house_id=models.CharField('调出仓库', null=True, blank=True, max_length=10)
    old_to_ware_house_id=models.CharField('调入仓库', null=True, blank=True, max_length=10)
    old_print_times=models.IntegerField('PrintTimes', null=True, blank=True)
    old_carryer_id=models.CharField('搬运工', null=True, blank=True, max_length=20)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_prodstorageadjust'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_e3b2f1046526d26a'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_e3b2f1046526d26a')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（ProdStorageAdjust，待确认）'
        ordering=["-id"]

class SourceDyeProdStorageAdjustDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProdStorageAdjustDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'FromInSheetNo': 'old_from_in_sheet_no', 'CheckNo': 'old_check_no', 'JobSheetNo': 'old_job_sheet_no', 'LotNo': 'old_lot_no', 'Spec': 'old_spec', 'StorageUnitIDs': 'old_storage_unit_ids', 'ToStorageUnitIDs': 'old_to_storage_unit_ids', 'Rolls': 'old_rolls', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'Remarks': 'old_remarks', 'StockUnit': 'old_stock_unit', 'ProdID': 'old_prod_id', 'CustSelfProduct': 'old_cust_self_product', 'ColorNum': 'old_color_num', 'ColorID': 'old_color_id', 'CustColorNum': 'old_cust_color_num', 'OrderSheetDate': 'old_order_sheet_date', 'Weight': 'old_weight', 'Width': 'old_width', 'Structure': 'old_structure'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_from_in_sheet_no': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_storage_unit_ids': 'Chinese_PRC_CI_AS', 'old_to_storage_unit_ids': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_cust_self_product': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_cust_color_num': 'Chinese_PRC_CI_AS', 'old_weight': 'Chinese_PRC_CI_AS', 'old_width': 'Chinese_PRC_CI_AS', 'old_structure': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：ProdStorageAdjust', 'target': 'erp_warehouse.SourceDyeProdStorageAdjust', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 ProdStorageAdjustDetail → ProdStorageAdjust']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('明细号', null=False, blank=True, max_length=36)
    old_from_in_sheet_no=models.CharField('(调出)入库单号', null=True, blank=True, max_length=50)
    old_check_no=models.CharField('订单明细号', null=True, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=20)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=200)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=200)
    old_storage_unit_ids=models.CharField('调出库位', null=True, blank=True, max_length=100)
    old_to_storage_unit_ids=models.CharField('调入库位', null=True, blank=True, max_length=100)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_length_qty=models.DecimalField('长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_stock_unit=models.IntegerField('单位', null=True, blank=True)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=20)
    old_cust_self_product=models.CharField('客户规格', null=True, blank=True, max_length=250)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=150)
    old_cust_color_num=models.CharField('客户色号', null=True, blank=True, max_length=100)
    old_order_sheet_date=models.DateTimeField('订单日期', null=True, blank=True)
    old_weight=models.CharField('克重', null=True, blank=True, max_length=50)
    old_width=models.CharField('幅宽', null=True, blank=True, max_length=50)
    old_structure=models.CharField('织厂', null=True, blank=True, max_length=50)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeProdStorageAdjust', verbose_name='原关系：ProdStorageAdjust', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_prodstorageadjustdetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_5f7fab14cf173ea0'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_5f7fab14cf173ea0')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（ProdStorageAdjustDetail，待确认）'
        ordering=["-id"]

class SourceDyeProdStorageAdjustRecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ProdStorageAdjustRecord'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'RollNo': 'old_roll_no', 'FromInSheetNo': 'old_from_in_sheet_no', 'BarCode': 'old_bar_code', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'StorageUnitID': 'old_storage_unit_id', 'ToStorageUnitID': 'old_to_storage_unit_id', 'Remarks': 'old_remarks', 'GrayBarCode': 'old_gray_bar_code', 'GrayQty': 'old_gray_qty', 'GUnit': 'old_gunit', 'PUnit': 'old_punit', 'Yard': 'old_yard', 'RollNo3': 'old_roll_no3'}
    SOURCE_KEY=('SheetSeries', 'DetailNo', 'BarCode')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_roll_no': 'Chinese_PRC_CI_AS', 'old_from_in_sheet_no': 'Chinese_PRC_CI_AS', 'old_bar_code': 'Chinese_PRC_CI_AS', 'old_storage_unit_id': 'Chinese_PRC_CI_AS', 'old_to_storage_unit_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_gray_bar_code': 'Chinese_PRC_CI_AS', 'old_roll_no3': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：ProdStorageAdjustDetail', 'target': 'erp_warehouse.SourceDyeProdStorageAdjustDetail', 'source_fields': ['SheetSeries', 'DetailNo'], 'target_fields': ['SheetSeries', 'DetailNo'], 'evidence': ['原界面主从 ProdStorageAdjustRecord → ProdStorageAdjustDetail']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('明细号', null=False, blank=True, max_length=36)
    old_roll_no=models.CharField('箱号', null=False, blank=True, max_length=20)
    old_from_in_sheet_no=models.CharField('(调出)入库单号', null=True, blank=True, max_length=50)
    old_bar_code=models.CharField('条码', null=False, blank=True, max_length=50)
    old_length_qty=models.DecimalField('长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_storage_unit_id=models.CharField('调出库位', null=True, blank=True, max_length=10)
    old_to_storage_unit_id=models.CharField('调入库位', null=True, blank=True, max_length=10)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_gray_bar_code=models.CharField('GrayBarCode', null=True, blank=True, max_length=50)
    old_gray_qty=models.DecimalField('GrayQty', null=True, blank=True, max_digits=8, decimal_places=2)
    old_gunit=models.IntegerField('GUnit', null=True, blank=True)
    old_punit=models.IntegerField('PUnit', null=True, blank=True)
    old_yard=models.DecimalField('Yard', null=True, blank=True, max_digits=8, decimal_places=2)
    old_roll_no3=models.CharField('RollNo3', null=True, blank=True, max_length=50)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeProdStorageAdjustDetail', verbose_name='原关系：ProdStorageAdjustDetail', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_prodstorageadjustrecord'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no', 'old_bar_code'],name='src_8b6801ee9135db2f'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),Upper(RTrim(models.F('old_bar_code'))),name='src_ci_8b6801ee9135db2f')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（ProdStorageAdjustRecord，待确认）'
        ordering=["-id"]

class SourceDyeRecordYield(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='RecordYield'
    SOURCE_FIELDS={'Guid': 'old_guid', 'BarCode': 'old_bar_code', 'MachineID': 'old_machine_id', 'RollNo': 'old_roll_no', 'Unit': 'old_unit', 'Rolls': 'old_rolls', 'Kg': 'old_kg', 'Meter': 'old_meter', 'Pound': 'old_pound', 'Yard': 'old_yard', 'RealQty': 'old_real_qty', 'StorageUnitID': 'old_storage_unit_id', 'DefectCount': 'old_defect_count', 'Dots': 'old_dots', 'Status': 'old_status', 'GradeID': 'old_grade_id', 'PackTime': 'old_pack_time', 'EmpID': 'old_emp_id', 'TubeWeight': 'old_tube_weight', 'Tubes': 'old_tubes', 'Thick': 'old_thick', 'Width': 'old_width', 'PackID': 'old_pack_id', 'Bowing': 'old_bowing', 'Remarks': 'old_remarks', 'JobSheetNo': 'old_job_sheet_no', 'AddQty': 'old_add_qty', 'SampleQty': 'old_sample_qty', 'CutQty': 'old_cut_qty', 'CutTimes': 'old_cut_times', 'FullWidth': 'old_full_width', 'T1': 'old_t1', 'T2': 'old_t2', 'T3': 'old_t3', 'T4': 'old_t4', 'T5': 'old_t5', 'Q1': 'old_q1', 'Q2': 'old_q2', 'Q3': 'old_q3', 'Q4': 'old_q4', 'Q5': 'old_q5', 'Q6': 'old_q6', 'Q7': 'old_q7', 'Q8': 'old_q8', 'Q9': 'old_q9', 'Q10': 'old_q10', 'Q11': 'old_q11', 'Q12': 'old_q12', 'Q13': 'old_q13', 'Q14': 'old_q14', 'Q15': 'old_q15', 'LotNo': 'old_lot_no', 'ColorNum': 'old_color_num', 'InSheetNo': 'old_in_sheet_no', 'CustQty': 'old_cust_qty', 'CustomerID': 'old_customer_id', 'LabelID': 'old_label_id', 'Weight': 'old_weight', 'ColorDiff': 'old_color_diff', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer', 'GradeReasonID': 'old_grade_reason_id', 'StandardWidth': 'old_standard_width', 'DetailCustName': 'old_detail_cust_name', 'OriDetailCustomer': 'old_ori_detail_customer', 'OrderSheetNo': 'old_order_sheet_no', 'OriOderSheetNo': 'old_ori_oder_sheet_no', 'QCResultID': 'old_qcresult_id', 'MainNo': 'old_main_no', 'DetailNo': 'old_detail_no', 'ProdID': 'old_prod_id', 'DefectEmpID': 'old_defect_emp_id', 'GrayBarCode': 'old_gray_bar_code', 'CheckNo': 'old_check_no', 'InScanTime': 'old_in_scan_time', 'InScaner': 'old_in_scaner', 'OutScanTime': 'old_out_scan_time', 'OutScaner': 'old_out_scaner', 'OutPlanSheetNo': 'old_out_plan_sheet_no', 'OutPlanDetailNo': 'old_out_plan_detail_no', 'DlvSheetNo': 'old_dlv_sheet_no', 'NetKg': 'old_net_kg', 'SumAssignedWeightQty': 'old_sum_assigned_weight_qty', 'SumAssignedRolls': 'old_sum_assigned_rolls', 'Scroll': 'old_scroll', 'PackBag': 'old_pack_bag', 'AddWeight': 'old_add_weight', 'CustomerGrayName': 'old_customer_gray_name', 'ColorID': 'old_color_id', 'Spec': 'old_spec', 'WidthSpec': 'old_width_spec', 'WeightSpec': 'old_weight_spec', 'Qty': 'old_qty', 'CountUnit': 'old_count_unit', 'JobDetailNo': 'old_job_detail_no', 'PrintTimes': 'old_print_times', 'CustSelfNo': 'old_cust_self_no', 'RedoLengthQty': 'old_redo_length_qty', 'ProcessID': 'old_process_id', 'Addkg': 'old_addkg', 'ShiftID': 'old_shift_id', 'BusinessUnitID': 'old_business_unit_id', 'Kind': 'old_kind', 'SpecDefects': 'old_spec_defects', 'GrayWeight': 'old_gray_weight', 'CombineSheetNos': 'old_combine_sheet_nos', 'ContractNo': 'old_contract_no', 'LotCheckNo': 'old_lot_check_no', 'DefectProcessID': 'old_defect_process_id', 'RollNoType': 'old_roll_no_type', 'StyleNo': 'old_style_no', 'RedoWeightQty': 'old_redo_weight_qty', 'LotDetailNo': 'old_lot_detail_no', 'SortNo': 'old_sort_no', 'SkeWing1': 'old_ske_wing1', 'SkeWing2': 'old_ske_wing2', 'RePeatcnt': 'old_re_peatcnt', 'RepeatFrontL': 'old_repeat_front_l', 'RepeatFrontM': 'old_repeat_front_m', 'RepeatFrontR': 'old_repeat_front_r', 'RepeatMiddleL': 'old_repeat_middle_l', 'RepeatMiddleM': 'old_repeat_middle_m', 'RepeatMiddleR': 'old_repeat_middle_r', 'RepeatEndL': 'old_repeat_end_l', 'RepeatEndM': 'old_repeat_end_m', 'RepeatEndR': 'old_repeat_end_r', 'RightStatus': 'old_right_status', 'YardAvgdots': 'old_yard_avgdots', 'OrderWeight': 'old_order_weight', 'PAWeight': 'old_paweight', 'PAYard': 'old_payard', 'PAMeter': 'old_pameter', 'WidthUnit': 'old_width_unit', 'OrderWidth': 'old_order_width', 'CustColorNum': 'old_cust_color_num', 'DB2Code': 'old_db2_code', 'AddWeigth': 'old_add_weigth', 'LabelWeight': 'old_label_weight', 'LabelLength': 'old_label_length', 'LabelRemarks': 'old_label_remarks', 'FabricLoss': 'old_fabric_loss', 'ShipMentType': 'old_ship_ment_type', 'WeightQty': 'old_weight_qty', 'ProdCode': 'old_prod_code', 'Model1': 'old_model1', 'ColorRemarks': 'old_color_remarks', 'ColorE': 'old_color_e', 'WeightUnit': 'old_weight_unit', 'WeightKindID': 'old_weight_kind_id', 'WidthKindID': 'old_width_kind_id', 'ProdName': 'old_prod_name', 'FabricNO2': 'old_fabric_no2', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'ProdUnit': 'old_prod_unit', 'LabelWareHouse': 'old_label_ware_house', 'WindingID': 'old_winding_id', 'LTSheetNo': 'old_ltsheet_no', 'FenTou': 'old_fen_tou', 'SheetDate': 'old_sheet_date', 'PreField1': 'old_pre_field1', 'Long_CM': 'old_long_cm', 'Wide_CM': 'old_wide_cm', 'High_CM': 'old_high_cm', 'Whether': 'old_whether', 'FixedQty': 'old_fixed_qty', 'FabricKindID': 'old_fabric_kind_id'}
    SOURCE_KEY=('JobSheetNo', 'CheckNo', 'RollNo', 'Guid')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_guid': 'Chinese_PRC_CI_AS', 'old_bar_code': 'Chinese_PRC_CI_AS', 'old_machine_id': 'Chinese_PRC_CI_AS', 'old_roll_no': 'Chinese_PRC_CI_AS', 'old_unit': 'Chinese_PRC_CI_AS', 'old_storage_unit_id': 'Chinese_PRC_CI_AS', 'old_grade_id': 'Chinese_PRC_CI_AS', 'old_emp_id': 'Chinese_PRC_CI_AS', 'old_width': 'Chinese_PRC_CI_AS', 'old_pack_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_q1': 'Chinese_PRC_CI_AS', 'old_q2': 'Chinese_PRC_CI_AS', 'old_q3': 'Chinese_PRC_CI_AS', 'old_q4': 'Chinese_PRC_CI_AS', 'old_q5': 'Chinese_PRC_CI_AS', 'old_q6': 'Chinese_PRC_CI_AS', 'old_q7': 'Chinese_PRC_CI_AS', 'old_q8': 'Chinese_PRC_CI_AS', 'old_q9': 'Chinese_PRC_CI_AS', 'old_q10': 'Chinese_PRC_CI_AS', 'old_q11': 'Chinese_PRC_CI_AS', 'old_q12': 'Chinese_PRC_CI_AS', 'old_q13': 'Chinese_PRC_CI_AS', 'old_q14': 'Chinese_PRC_CI_AS', 'old_q15': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_in_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_label_id': 'Chinese_PRC_CI_AS', 'old_weight': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_grade_reason_id': 'Chinese_PRC_CI_AS', 'old_detail_cust_name': 'Chinese_PRC_CI_AS', 'old_ori_detail_customer': 'Chinese_PRC_CI_AS', 'old_order_sheet_no': 'Chinese_PRC_CI_AS', 'old_ori_oder_sheet_no': 'Chinese_PRC_CI_AS', 'old_qcresult_id': 'Chinese_PRC_CI_AS', 'old_main_no': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_defect_emp_id': 'Chinese_PRC_CI_AS', 'old_gray_bar_code': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_in_scaner': 'Chinese_PRC_CI_AS', 'old_out_scaner': 'Chinese_PRC_CI_AS', 'old_out_plan_sheet_no': 'Chinese_PRC_CI_AS', 'old_out_plan_detail_no': 'Chinese_PRC_CI_AS', 'old_dlv_sheet_no': 'Chinese_PRC_CI_AS', 'old_scroll': 'Chinese_PRC_CI_AS', 'old_add_weight': 'Chinese_PRC_CI_AS', 'old_customer_gray_name': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_width_spec': 'Chinese_PRC_CI_AS', 'old_weight_spec': 'Chinese_PRC_CI_AS', 'old_count_unit': 'Chinese_PRC_CI_AS', 'old_job_detail_no': 'Chinese_PRC_CI_AS', 'old_cust_self_no': 'Chinese_PRC_CI_AS', 'old_process_id': 'Chinese_PRC_CI_AS', 'old_shift_id': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_kind': 'Chinese_PRC_CI_AS', 'old_spec_defects': 'Chinese_PRC_CI_AS', 'old_combine_sheet_nos': 'Chinese_PRC_CI_AS', 'old_contract_no': 'Chinese_PRC_CI_AS', 'old_lot_check_no': 'Chinese_PRC_CI_AS', 'old_defect_process_id': 'Chinese_PRC_CI_AS', 'old_roll_no_type': 'Chinese_PRC_CI_AS', 'old_style_no': 'Chinese_PRC_CI_AS', 'old_lot_detail_no': 'Chinese_PRC_CI_AS', 'old_sort_no': 'Chinese_PRC_CI_AS', 'old_ske_wing1': 'Chinese_PRC_CI_AS', 'old_ske_wing2': 'Chinese_PRC_CI_AS', 'old_re_peatcnt': 'Chinese_PRC_CI_AS', 'old_order_weight': 'Chinese_PRC_CI_AS', 'old_width_unit': 'Chinese_PRC_CI_AS', 'old_order_width': 'Chinese_PRC_CI_AS', 'old_cust_color_num': 'Chinese_PRC_CI_AS', 'old_db2_code': 'Chinese_PRC_CI_AS', 'old_add_weigth': 'Chinese_PRC_CI_AS', 'old_label_weight': 'Chinese_PRC_CI_AS', 'old_label_length': 'Chinese_PRC_CI_AS', 'old_label_remarks': 'Chinese_PRC_CI_AS', 'old_ship_ment_type': 'Chinese_PRC_CI_AS', 'old_prod_code': 'Chinese_PRC_CI_AS', 'old_model1': 'Chinese_PRC_CI_AS', 'old_color_remarks': 'Chinese_PRC_CI_AS', 'old_color_e': 'Chinese_PRC_CI_AS', 'old_weight_unit': 'Chinese_PRC_CI_AS', 'old_weight_kind_id': 'Chinese_PRC_CI_AS', 'old_width_kind_id': 'Chinese_PRC_CI_AS', 'old_prod_name': 'Chinese_PRC_CI_AS', 'old_fabric_no2': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_label_ware_house': 'Chinese_PRC_CI_AS', 'old_winding_id': 'Chinese_PRC_CI_AS', 'old_ltsheet_no': 'Chinese_PRC_CI_AS', 'old_pre_field1': 'Chinese_PRC_CI_AS', 'old_fabric_kind_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：JobSheet', 'target': 'erp_production.SourceDyeJobSheet', 'source_fields': ['JobSheetNo'], 'target_fields': ['SheetNo'], 'evidence': ['原界面主从 JobRecordDetail → JobRecord']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_guid=models.CharField('唯一标识符', null=False, blank=True, max_length=38)
    old_bar_code=models.CharField('条码', null=True, blank=True, max_length=100)
    old_machine_id=models.CharField('机台', null=True, blank=True, max_length=20)
    old_roll_no=models.CharField('箱号', null=False, blank=True, max_length=50)
    old_unit=models.CharField('单位', null=True, blank=True, max_length=20)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=1)
    old_kg=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_meter=models.DecimalField('长度', null=True, blank=True, max_digits=10, decimal_places=0)
    old_pound=models.DecimalField('镑数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_yard=models.DecimalField('码数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_qty=models.DecimalField('缴库长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_storage_unit_id=models.CharField('仓位代码', null=True, blank=True, max_length=10)
    old_defect_count=models.IntegerField('疵点数', null=True, blank=True)
    old_dots=models.IntegerField('扣分', null=True, blank=True)
    old_status=models.IntegerField('状态', null=True, blank=True)
    old_grade_id=models.CharField('色号等级', null=True, blank=True, max_length=10)
    old_pack_time=models.DateTimeField('包装时间', null=True, blank=True)
    old_emp_id=models.CharField('员工编号', null=True, blank=True, max_length=50)
    old_tube_weight=models.DecimalField('筒管重', null=True, blank=True, max_digits=7, decimal_places=3)
    old_tubes=models.IntegerField('筒管数', null=True, blank=True)
    old_thick=models.DecimalField('厚度', null=True, blank=True, max_digits=6, decimal_places=2)
    old_width=models.CharField('幅宽', null=True, blank=True, max_length=50)
    old_pack_id=models.CharField('纱种编号', null=True, blank=True, max_length=10)
    old_bowing=models.DecimalField('纬斜', null=True, blank=True, max_digits=5, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_job_sheet_no=models.CharField('缸号', null=False, blank=True, max_length=150)
    old_add_qty=models.DecimalField('补码', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sample_qty=models.DecimalField('样纱长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_cut_qty=models.DecimalField('开剪值', null=True, blank=True, max_digits=10, decimal_places=2)
    old_cut_times=models.IntegerField('开剪次数', null=True, blank=True)
    old_full_width=models.DecimalField('全幅', null=True, blank=True, max_digits=6, decimal_places=2)
    old_t1=models.DecimalField('厚度一', null=True, blank=True, max_digits=6, decimal_places=2)
    old_t2=models.DecimalField('厚度二', null=True, blank=True, max_digits=6, decimal_places=2)
    old_t3=models.DecimalField('厚度三', null=True, blank=True, max_digits=6, decimal_places=2)
    old_t4=models.DecimalField('厚度四', null=True, blank=True, max_digits=6, decimal_places=2)
    old_t5=models.DecimalField('厚度五', null=True, blank=True, max_digits=6, decimal_places=2)
    old_q1=models.CharField('客纱种编码', null=True, blank=True, max_length=50)
    old_q2=models.CharField('开卡粒数', null=True, blank=True, max_length=10)
    old_q3=models.CharField('品质3级数', null=True, blank=True, max_length=10)
    old_q4=models.CharField('品质4级数', null=True, blank=True, max_length=10)
    old_q5=models.CharField('品质5级数', null=True, blank=True, max_length=10)
    old_q6=models.CharField('品质6级数', null=True, blank=True, max_length=10)
    old_q7=models.CharField('品质7级数', null=True, blank=True, max_length=10)
    old_q8=models.CharField('品质8级数', null=True, blank=True, max_length=10)
    old_q9=models.CharField('品质9级数', null=True, blank=True, max_length=10)
    old_q10=models.CharField('品质10级数', null=True, blank=True, max_length=10)
    old_q11=models.CharField('品质11级数', null=True, blank=True, max_length=10)
    old_q12=models.CharField('品质12级数', null=True, blank=True, max_length=100)
    old_q13=models.CharField('品质13级数', null=True, blank=True, max_length=100)
    old_q14=models.CharField('品质14级数', null=True, blank=True, max_length=100)
    old_q15=models.CharField('新利二维码', null=True, blank=True, max_length=500)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=200)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=100)
    old_in_sheet_no=models.CharField('入库单号', null=True, blank=True, max_length=20)
    old_cust_qty=models.DecimalField('客户数量', null=True, blank=True, max_digits=10, decimal_places=1)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=50)
    old_label_id=models.CharField('标签号', null=True, blank=True, max_length=10)
    old_weight=models.CharField('克重', null=True, blank=True, max_length=50)
    old_color_diff=models.IntegerField('色差', null=True, blank=True)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_grade_reason_id=models.CharField('降等', null=True, blank=True, max_length=100)
    old_standard_width=models.DecimalField('标准幅宽', null=True, blank=True, max_digits=6, decimal_places=2)
    old_detail_cust_name=models.CharField('明细客户', null=True, blank=True, max_length=150)
    old_ori_detail_customer=models.CharField('原始客户', null=True, blank=True, max_length=50)
    old_order_sheet_no=models.CharField('发货订单', null=True, blank=True, max_length=20)
    old_ori_oder_sheet_no=models.CharField('原始订单', null=True, blank=True, max_length=20)
    old_qcresult_id=models.CharField('QCResultID', null=True, blank=True, max_length=10)
    old_main_no=models.CharField('主单号', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('明细单号', null=True, blank=True, max_length=36)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=150)
    old_defect_emp_id=models.CharField('DefectEmpID', null=True, blank=True, max_length=20)
    old_gray_bar_code=models.CharField('宝誉/丽业二维码组合', null=True, blank=True, max_length=100)
    old_check_no=models.CharField('订单明细号', null=False, blank=True, max_length=50)
    old_in_scan_time=models.DateTimeField('InScanTime', null=True, blank=True)
    old_in_scaner=models.CharField('InScaner', null=True, blank=True, max_length=10)
    old_out_scan_time=models.DateTimeField('OutScanTime', null=True, blank=True)
    old_out_scaner=models.CharField('OutScaner', null=True, blank=True, max_length=10)
    old_out_plan_sheet_no=models.CharField('OutPlanSheetNo', null=True, blank=True, max_length=20)
    old_out_plan_detail_no=models.CharField('OutPlanDetailNo', null=True, blank=True, max_length=20)
    old_dlv_sheet_no=models.CharField('DlvSheetNo', null=True, blank=True, max_length=20)
    old_net_kg=models.DecimalField('净重', null=True, blank=True, max_digits=10, decimal_places=1)
    old_sum_assigned_weight_qty=models.DecimalField('实发数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sum_assigned_rolls=models.DecimalField('实发粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_scroll=models.CharField('Scroll', null=True, blank=True, max_length=100)
    old_pack_bag=models.DecimalField('包装重', null=True, blank=True, max_digits=7, decimal_places=3)
    old_add_weight=models.CharField('AddWeight', null=True, blank=True, max_length=50)
    old_customer_gray_name=models.CharField('CustomerGrayName', null=True, blank=True, max_length=200)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=150)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=500)
    old_width_spec=models.CharField('幅宽（测量）', null=True, blank=True, max_length=128)
    old_weight_spec=models.CharField('克重（测量）', null=True, blank=True, max_length=150)
    old_qty=models.DecimalField('张力', null=True, blank=True, max_digits=12, decimal_places=6)
    old_count_unit=models.CharField('CountUnit', null=True, blank=True, max_length=16)
    old_job_detail_no=models.CharField('JobDetailNo', null=True, blank=True, max_length=150)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_cust_self_no=models.CharField('制单号', null=True, blank=True, max_length=500)
    old_redo_length_qty=models.DecimalField('RedoLengthQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_process_id=models.CharField('ProcessID', null=True, blank=True, max_length=10)
    old_addkg=models.FloatField('加空重', null=True, blank=True)
    old_shift_id=models.CharField('班组', null=True, blank=True, max_length=10)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_kind=models.CharField('Kind', null=True, blank=True, max_length=1)
    old_spec_defects=models.CharField('特判', null=True, blank=True, max_length=100)
    old_gray_weight=models.DecimalField('GrayWeight', null=True, blank=True, max_digits=6, decimal_places=2)
    old_combine_sheet_nos=models.CharField('CombineSheetNos', null=True, blank=True, max_length=200)
    old_contract_no=models.CharField('客户单号', null=True, blank=True, max_length=500)
    old_lot_check_no=models.CharField('LotCheckNo', null=True, blank=True, max_length=500)
    old_defect_process_id=models.CharField('DefectProcessID', null=True, blank=True, max_length=50)
    old_roll_no_type=models.CharField('RollNoType', null=True, blank=True, max_length=150)
    old_style_no=models.CharField('StyleNo', null=True, blank=True, max_length=150)
    old_redo_weight_qty=models.DecimalField('RedoWeightQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_lot_detail_no=models.CharField('LotDetailNo', null=True, blank=True, max_length=50)
    old_sort_no=models.CharField('SortNo', null=True, blank=True, max_length=10)
    old_ske_wing1=models.CharField('宝誉条码', null=True, blank=True, max_length=150)
    old_ske_wing2=models.CharField('SkeWing2', null=True, blank=True, max_length=150)
    old_re_peatcnt=models.CharField('RePeatcnt', null=True, blank=True, max_length=150)
    old_repeat_front_l=models.DecimalField('RepeatFrontL', null=True, blank=True, max_digits=10, decimal_places=2)
    old_repeat_front_m=models.DecimalField('RepeatFrontM', null=True, blank=True, max_digits=10, decimal_places=2)
    old_repeat_front_r=models.DecimalField('RepeatFrontR', null=True, blank=True, max_digits=10, decimal_places=2)
    old_repeat_middle_l=models.DecimalField('RepeatMiddleL', null=True, blank=True, max_digits=10, decimal_places=2)
    old_repeat_middle_m=models.DecimalField('RepeatMiddleM', null=True, blank=True, max_digits=10, decimal_places=2)
    old_repeat_middle_r=models.DecimalField('RepeatMiddleR', null=True, blank=True, max_digits=10, decimal_places=2)
    old_repeat_end_l=models.DecimalField('RepeatEndL', null=True, blank=True, max_digits=10, decimal_places=2)
    old_repeat_end_m=models.DecimalField('RepeatEndM', null=True, blank=True, max_digits=10, decimal_places=2)
    old_repeat_end_r=models.DecimalField('RepeatEndR', null=True, blank=True, max_digits=10, decimal_places=2)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_yard_avgdots=models.FloatField('百码扣分', null=True, blank=True)
    old_order_weight=models.CharField('要求克重', null=True, blank=True, max_length=20)
    old_paweight=models.DecimalField('克重（公式计算）', null=True, blank=True, max_digits=18, decimal_places=0)
    old_payard=models.DecimalField('码数(公式计算)', null=True, blank=True, max_digits=18, decimal_places=0)
    old_pameter=models.DecimalField('米数(公式计算）', null=True, blank=True, max_digits=18, decimal_places=0)
    old_width_unit=models.CharField('纱封单位', null=True, blank=True, max_length=20)
    old_order_width=models.CharField('要求幅宽', null=True, blank=True, max_length=20)
    old_cust_color_num=models.CharField('CustColorNum', null=True, blank=True, max_length=100)
    old_db2_code=models.CharField('DB2Code', null=True, blank=True, max_length=500)
    old_add_weigth=models.CharField('成品加重', null=True, blank=True, max_length=50)
    old_label_weight=models.CharField('LabelWeight', null=True, blank=True, max_length=100)
    old_label_length=models.CharField('LabelLength', null=True, blank=True, max_length=100)
    old_label_remarks=models.CharField('标签备注', null=True, blank=True, max_length=500)
    old_fabric_loss=models.DecimalField('胚纱损耗', null=True, blank=True, max_digits=18, decimal_places=2)
    old_ship_ment_type=models.CharField('出货方式', null=True, blank=True, max_length=50)
    old_weight_qty=models.DecimalField('WeightQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_prod_code=models.CharField('成品编号', null=True, blank=True, max_length=50)
    old_model1=models.CharField('款号', null=True, blank=True, max_length=200)
    old_color_remarks=models.CharField('用途', null=True, blank=True, max_length=500)
    old_color_e=models.CharField('ColorE', null=True, blank=True, max_length=20)
    old_weight_unit=models.CharField('WeightUnit', null=True, blank=True, max_length=20)
    old_weight_kind_id=models.CharField('WeightKindID', null=True, blank=True, max_length=20)
    old_width_kind_id=models.CharField('WidthKindID', null=True, blank=True, max_length=20)
    old_prod_name=models.CharField('成品品名', null=True, blank=True, max_length=500)
    old_fabric_no2=models.CharField('计划单号', null=True, blank=True, max_length=200)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_prod_unit=models.IntegerField('成品单位', null=True, blank=True)
    old_label_ware_house=models.CharField('标签仓库', null=True, blank=True, max_length=100)
    old_winding_id=models.CharField('络筒员工', null=True, blank=True, max_length=30)
    old_ltsheet_no=models.CharField('LTSheetNo', null=True, blank=True, max_length=30)
    old_fen_tou=models.DecimalField('分头', null=True, blank=True, max_digits=6, decimal_places=2)
    old_sheet_date=models.DateTimeField('络筒日期', null=True, blank=True)
    old_pre_field1=models.CharField('捻度', null=True, blank=True, max_length=50)
    old_long_cm=models.DecimalField('长(CM)', null=True, blank=True, max_digits=6, decimal_places=1)
    old_wide_cm=models.DecimalField('宽(CM)', null=True, blank=True, max_digits=6, decimal_places=1)
    old_high_cm=models.DecimalField('高(CM)', null=True, blank=True, max_digits=6, decimal_places=1)
    old_whether=models.BooleanField('是否', null=True, blank=True)
    old_fixed_qty=models.DecimalField('锭重', null=True, blank=True, max_digits=5, decimal_places=2)
    old_fabric_kind_id=models.CharField('胚纱类别', null=True, blank=True, max_length=30)
    source_parent_1=models.ForeignKey('erp_production.SourceDyeJobSheet', verbose_name='原关系：JobSheet', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_recordyield'
        indexes=[models.Index(fields=['source_batch', 'old_guid'],name='src_43742016e7db612b'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_guid'))),name='src_ci_43742016e7db612b'),models.Index(fields=['source_batch', 'old_job_sheet_no', 'old_check_no', 'old_roll_no', 'old_guid'],name='src_b983d6ccd9959c1a'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_job_sheet_no'))),Upper(RTrim(models.F('old_check_no'))),Upper(RTrim(models.F('old_roll_no'))),Upper(RTrim(models.F('old_guid'))),name='src_ci_b983d6ccd9959c1a')]
        verbose_name=verbose_name_plural='产量/卷记录'
        ordering=["-id"]

class SourceDyeSemiAxisBook(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SemiAxisBook'
    SOURCE_FIELDS={'AxisNo': 'old_axis_no', 'SequenceNo': 'old_sequence_no', 'Flag': 'old_flag', 'ReceSheetNo': 'old_rece_sheet_no', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'CheckNo': 'old_check_no', 'JobSheetNo': 'old_job_sheet_no', 'Vats': 'old_vats', 'Rolls': 'old_rolls', 'Qty': 'old_qty', 'StockUnit': 'old_stock_unit', 'CurrTime': 'old_curr_time', 'ShiftID': 'old_shift_id', 'EmpID': 'old_emp_id', 'Status': 'old_status', 'Place': 'old_place', 'Remarks': 'old_remarks', 'SheetSeries': 'old_sheet_series'}
    SOURCE_KEY=('AxisNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_axis_no': 'Chinese_PRC_CI_AS', 'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_shift_id': 'Chinese_PRC_CI_AS', 'old_emp_id': 'Chinese_PRC_CI_AS', 'old_status': 'Chinese_PRC_CI_AS', 'old_place': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_sheet_series': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_axis_no=models.CharField('AxisNo', null=False, blank=True, max_length=20)
    old_sequence_no=models.BigIntegerField('SequenceNo', null=True, blank=True)
    old_flag=models.IntegerField('Flag', null=True, blank=True)
    old_rece_sheet_no=models.CharField('ReceSheetNo', null=True, blank=True, max_length=20)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=10)
    old_prod_id=models.CharField('ProdID', null=True, blank=True, max_length=20)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=128)
    old_lot_no=models.CharField('LotNo', null=True, blank=True, max_length=50)
    old_check_no=models.CharField('CheckNo', null=True, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)
    old_vats=models.DecimalField('Vats', null=True, blank=True, max_digits=7, decimal_places=1)
    old_rolls=models.DecimalField('Rolls', null=True, blank=True, max_digits=7, decimal_places=2)
    old_qty=models.DecimalField('Qty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_stock_unit=models.IntegerField('StockUnit', null=True, blank=True)
    old_curr_time=models.DateTimeField('CurrTime', null=True, blank=True)
    old_shift_id=models.CharField('ShiftID', null=True, blank=True, max_length=10)
    old_emp_id=models.CharField('EmpID', null=True, blank=True, max_length=10)
    old_status=models.CharField('Status', null=True, blank=True, max_length=1)
    old_place=models.CharField('Place', null=True, blank=True, max_length=100)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=100)
    old_sheet_series=models.CharField('SheetSeries', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_semiaxisbook'
        indexes=[models.Index(fields=['source_batch', 'old_axis_no'],name='src_da2f7c68ce7de6f5'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_axis_no'))),name='src_ci_da2f7c68ce7de6f5')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（SemiAxisBook，待确认）'
        ordering=["-id"]

class SourceDyeSemiAxisRemain(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SemiAxisRemain'
    SOURCE_FIELDS={'AxisNo': 'old_axis_no', 'SequenceNo': 'old_sequence_no', 'ReceSheetNo': 'old_rece_sheet_no', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'CheckNo': 'old_check_no', 'JobSheetNo': 'old_job_sheet_no', 'Qty': 'old_qty', 'StockUnit': 'old_stock_unit', 'CurrTime': 'old_curr_time', 'ShiftID': 'old_shift_id', 'EmpID': 'old_emp_id', 'Place': 'old_place', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('AxisNo',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_axis_no': 'Chinese_PRC_CI_AS', 'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_shift_id': 'Chinese_PRC_CI_AS', 'old_emp_id': 'Chinese_PRC_CI_AS', 'old_place': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_axis_no=models.CharField('AxisNo', null=False, blank=True, max_length=20)
    old_sequence_no=models.BigIntegerField('SequenceNo', null=True, blank=True)
    old_rece_sheet_no=models.CharField('ReceSheetNo', null=True, blank=True, max_length=20)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=10)
    old_prod_id=models.CharField('ProdID', null=True, blank=True, max_length=20)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=128)
    old_lot_no=models.CharField('LotNo', null=True, blank=True, max_length=50)
    old_check_no=models.CharField('CheckNo', null=True, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)
    old_qty=models.DecimalField('Qty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_stock_unit=models.IntegerField('StockUnit', null=True, blank=True)
    old_curr_time=models.DateTimeField('CurrTime', null=True, blank=True)
    old_shift_id=models.CharField('ShiftID', null=True, blank=True, max_length=10)
    old_emp_id=models.CharField('EmpID', null=True, blank=True, max_length=10)
    old_place=models.CharField('Place', null=True, blank=True, max_length=100)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_semiaxisremain'
        indexes=[models.Index(fields=['source_batch', 'old_axis_no'],name='src_5c316c5e8c88a23a'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_axis_no'))),name='src_ci_5c316c5e8c88a23a')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（SemiAxisRemain，待确认）'
        ordering=["-id"]

class SourceDyeSemiIn(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SemiIn'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'SemiKindID': 'old_semi_kind_id', 'CustomerID': 'old_customer_id', 'SalerGroupID': 'old_saler_group_id', 'SalerID': 'old_saler_id', 'StockUnit': 'old_stock_unit', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'StepNo': 'old_step_no', 'BusinessUnitID': 'old_business_unit_id', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'WareHouseID': 'old_ware_house_id', 'SupplierID': 'old_supplier_id', 'GrayOutSheetNo': 'old_gray_out_sheet_no', 'A_A': 'old_a_a'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_semi_kind_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_saler_group_id': 'Chinese_PRC_CI_AS', 'old_saler_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_supplier_id': 'Chinese_PRC_CI_AS', 'old_gray_out_sheet_no': 'Chinese_PRC_CI_AS', 'old_a_a': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('单据号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_semi_kind_id=models.CharField('半成品类别', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('业务组别', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('业务员', null=True, blank=True, max_length=10)
    old_stock_unit=models.IntegerField('单位', null=True, blank=True)
    old_sheet_status=models.IntegerField('SheetStatus', null=True, blank=True)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_print_times=models.IntegerField('PrintTimes', null=True, blank=True)
    old_revisions=models.IntegerField('Revisions', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位', null=True, blank=True, max_length=10)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_ware_house_id=models.CharField('仓库', null=True, blank=True, max_length=50)
    old_supplier_id=models.CharField('供应商', null=True, blank=True, max_length=50)
    old_gray_out_sheet_no=models.CharField('胚纱转仓出库单号', null=True, blank=True, max_length=30)
    old_a_a=models.CharField('物料区域', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_semiin'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_418f03d4154769f7'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_418f03d4154769f7')]
        verbose_name=verbose_name_plural='半成品入库单'
        ordering=["-id"]

class SourceDyeSemiInDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SemiInDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'ReceSheetNo': 'old_rece_sheet_no', 'FabricID': 'old_fabric_id', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'ColorID': 'old_color_id', 'InRolls': 'old_in_rolls', 'InQty': 'old_in_qty', 'StorageUnitID': 'old_storage_unit_id', 'OrderNo': 'old_order_no', 'CheckNo': 'old_check_no', 'ShiftID': 'old_shift_id', 'EmpID': 'old_emp_id', 'MachineID': 'old_machine_id', 'OriReceSheetNo': 'old_ori_rece_sheet_no', 'Remarks': 'old_remarks', 'NewLotNo': 'old_new_lot_no', 'Width': 'old_width', 'JobSheetNo': 'old_job_sheet_no', 'Area': 'old_area', 'ProdID': 'old_prod_id', 'GrainQty': 'old_grain_qty', 'Rolls': 'old_rolls', 'WeightQty': 'old_weight_qty', 'LengthQty': 'old_length_qty', 'Packs': 'old_packs', 'PCS': 'old_pcs', 'FixedQty': 'old_fixed_qty', 'Price': 'old_price', 'PreField1': 'old_pre_field1', 'PreField2': 'old_pre_field2', 'PreField3': 'old_pre_field3', 'PreField4': 'old_pre_field4', 'PreField5': 'old_pre_field5', 'Amount': 'old_amount', 'PurDetailNo': 'old_pur_detail_no', 'YarnCategory': 'old_yarn_category', 'Classify': 'old_classify', 'ColorNum': 'old_color_num', 'PurchaseOrders': 'old_purchase_orders', 'A_A': 'old_a_a', 'A_B': 'old_a_b', 'TrunReceSheetNo': 'old_trun_rece_sheet_no', 'InSheetKind': 'old_in_sheet_kind', 'GrayOutDetailNo': 'old_gray_out_detail_no', 'InputCode': 'old_input_code'}
    SOURCE_KEY=('ReceSheetNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_fabric_id': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_storage_unit_id': 'Chinese_PRC_CI_AS', 'old_order_no': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_shift_id': 'Chinese_PRC_CI_AS', 'old_emp_id': 'Chinese_PRC_CI_AS', 'old_machine_id': 'Chinese_PRC_CI_AS', 'old_ori_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_new_lot_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_area': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_pre_field1': 'Chinese_PRC_CI_AS', 'old_pre_field2': 'Chinese_PRC_CI_AS', 'old_pre_field3': 'Chinese_PRC_CI_AS', 'old_pre_field4': 'Chinese_PRC_CI_AS', 'old_pre_field5': 'Chinese_PRC_CI_AS', 'old_pur_detail_no': 'Chinese_PRC_CI_AS', 'old_yarn_category': 'Chinese_PRC_CI_AS', 'old_classify': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_purchase_orders': 'Chinese_PRC_CI_AS', 'old_a_a': 'Chinese_PRC_CI_AS', 'old_a_b': 'Chinese_PRC_CI_AS', 'old_trun_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_in_sheet_kind': 'Chinese_PRC_CI_AS', 'old_gray_out_detail_no': 'Chinese_PRC_CI_AS', 'old_input_code': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：SemiIn', 'target': 'erp_warehouse.SourceDyeSemiIn', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 PurSemiInDetail → PurSemiIn', '原界面主从 CusReturnSemiInDetail → CusReturnSemiIn', '原界面主从 TurnSemiInDetail → TurnSemiIn', '原界面主从 MaterialSemiInDetail → MaterialSemiIn', '原界面主从 SemiInDetail → SemiIn', '原界面主从 SemiInDetailBack → SemiInBack', '原界面主从 GrayOutToSemiInDetail → GrayOutToSemiIn']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=True, blank=True, max_length=20)
    old_rece_sheet_no=models.CharField('入库明细号', null=False, blank=True, max_length=20)
    old_fabric_id=models.CharField('客户规格', null=True, blank=True, max_length=128)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=128)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('物料颜色', null=True, blank=True, max_length=20)
    old_in_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_in_qty=models.DecimalField('数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_storage_unit_id=models.CharField('仓位', null=True, blank=True, max_length=30)
    old_order_no=models.CharField('订单号', null=True, blank=True, max_length=20)
    old_check_no=models.CharField('订单明细号', null=True, blank=True, max_length=20)
    old_shift_id=models.CharField('班组', null=True, blank=True, max_length=10)
    old_emp_id=models.CharField('员工', null=True, blank=True, max_length=10)
    old_machine_id=models.CharField('机台', null=True, blank=True, max_length=20)
    old_ori_rece_sheet_no=models.CharField('原入库明细号', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_new_lot_no=models.CharField('新批号', null=True, blank=True, max_length=200)
    old_width=models.DecimalField('Width', null=True, blank=True, max_digits=6, decimal_places=2)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_area=models.CharField('区域', null=True, blank=True, max_length=30)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=200)
    old_grain_qty=models.DecimalField('GrainQty', null=True, blank=True, max_digits=8, decimal_places=2)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_weight_qty=models.DecimalField('重量', null=True, blank=True, max_digits=8, decimal_places=2)
    old_length_qty=models.DecimalField('长度', null=True, blank=True, max_digits=8, decimal_places=2)
    old_packs=models.DecimalField('件数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_pcs=models.IntegerField('粒/件', null=True, blank=True)
    old_fixed_qty=models.DecimalField('锭重', null=True, blank=True, max_digits=5, decimal_places=2)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=8, decimal_places=2)
    old_pre_field1=models.CharField('捻度(H/S)', null=True, blank=True, max_length=50)
    old_pre_field2=models.CharField('PreField2', null=True, blank=True, max_length=50)
    old_pre_field3=models.CharField('PreField3', null=True, blank=True, max_length=50)
    old_pre_field4=models.CharField('PreField4', null=True, blank=True, max_length=50)
    old_pre_field5=models.CharField('PreField5', null=True, blank=True, max_length=200)
    old_amount=models.DecimalField('金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pur_detail_no=models.CharField('采购入库明细', null=True, blank=True, max_length=50)
    old_yarn_category=models.CharField('纱类别', null=True, blank=True, max_length=30)
    old_classify=models.CharField('半成品分类', null=True, blank=True, max_length=50)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=20)
    old_purchase_orders=models.CharField('采购单号', null=True, blank=True, max_length=20)
    old_a_a=models.CharField('物料区域', null=True, blank=True, max_length=50)
    old_a_b=models.CharField('物料等级', null=True, blank=True, max_length=100)
    old_trun_rece_sheet_no=models.CharField('转仓前入库明细单号', null=True, blank=True, max_length=30)
    old_in_sheet_kind=models.CharField('物料分类', null=True, blank=True, max_length=20)
    old_gray_out_detail_no=models.CharField('发外出库明细单号', null=True, blank=True, max_length=30)
    old_input_code=models.CharField('打包条码', null=True, blank=True, max_length=30)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeSemiIn', verbose_name='原关系：SemiIn', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_semiindetail'
        indexes=[models.Index(fields=['source_batch', 'old_rece_sheet_no'],name='src_ed118088bc5b6e4e'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_rece_sheet_no'))),name='src_ci_ed118088bc5b6e4e')]
        verbose_name=verbose_name_plural='半成品入库明细'
        ordering=["-id"]

class SourceDyeSemiInRecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SemiInRecord'
    SOURCE_FIELDS={'ReceSheetNo': 'old_rece_sheet_no', 'RollNo': 'old_roll_no', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'DlvQty': 'old_dlv_qty', 'StorageUnitID': 'old_storage_unit_id', 'Defects': 'old_defects', 'Status': 'old_status', 'BarCode': 'old_bar_code', 'AssignedNo': 'old_assigned_no', 'JobSheetNo': 'old_job_sheet_no', 'OriReceSheetNo': 'old_ori_rece_sheet_no', 'RollNo2': 'old_roll_no2', 'GUnit': 'old_gunit', 'OriBarCode': 'old_ori_bar_code', 'Remark': 'old_remark', 'GraySpec': 'old_gray_spec', 'Num': 'old_num', 'CBz': 'old_cbz', 'Rolls': 'old_rolls', 'Packs': 'old_packs', 'InputDetailCode': 'old_input_detail_code', 'Kg': 'old_kg', 'CustQty': 'old_cust_qty', 'TubeWeight': 'old_tube_weight'}
    SOURCE_KEY=('ReceSheetNo', 'RollNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_roll_no': 'Chinese_PRC_CI_AS', 'old_storage_unit_id': 'Chinese_PRC_CI_AS', 'old_defects': 'Chinese_PRC_CI_AS', 'old_status': 'Chinese_PRC_CI_AS', 'old_bar_code': 'Chinese_PRC_CI_AS', 'old_assigned_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_ori_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_roll_no2': 'Chinese_PRC_CI_AS', 'old_ori_bar_code': 'Chinese_PRC_CI_AS', 'old_remark': 'Chinese_PRC_CI_AS', 'old_gray_spec': 'Chinese_PRC_CI_AS', 'old_cbz': 'Chinese_PRC_CI_AS', 'old_input_detail_code': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：SemiInDetail', 'target': 'erp_warehouse.SourceDyeSemiInDetail', 'source_fields': ['ReceSheetNo'], 'target_fields': ['ReceSheetNo'], 'evidence': ['原界面主从 TurnSemiInRecord → TurnSemiInDetail', '原界面主从 PurSemiInRecord → PurSemiInDetail', '原界面主从 MaterialSemiInRecord → MaterialSemiInDetail', '原界面主从 GrayOutToSemiInRecord → GrayOutToSemiInDetail', '原界面主从 SemiInRecord → SemiInDetail', '原界面主从 CusReturnSemiInRecord → CusReturnSemiInDetail', '原界面主从 SemiInRecordBack → SemiInDetailBack']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_rece_sheet_no=models.CharField('入库明细号', null=False, blank=True, max_length=20)
    old_roll_no=models.CharField('箱号', null=False, blank=True, max_length=20)
    old_length_qty=models.DecimalField('长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dlv_qty=models.DecimalField('交货数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_storage_unit_id=models.CharField('仓位', null=True, blank=True, max_length=10)
    old_defects=models.CharField('疵点', null=True, blank=True, max_length=100)
    old_status=models.CharField('状态', null=True, blank=True, max_length=1)
    old_bar_code=models.CharField('条码', null=True, blank=True, max_length=50)
    old_assigned_no=models.CharField('投胚流水号', null=True, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_ori_rece_sheet_no=models.CharField('OriReceSheetNo', null=True, blank=True, max_length=20)
    old_roll_no2=models.CharField('RollNo2', null=True, blank=True, max_length=20)
    old_gunit=models.IntegerField('GUnit', null=True, blank=True)
    old_ori_bar_code=models.CharField('OriBarCode', null=True, blank=True, max_length=50)
    old_remark=models.CharField('备注', null=True, blank=True, max_length=300)
    old_gray_spec=models.CharField('GraySpec', null=True, blank=True, max_length=50)
    old_num=models.DecimalField('Num', null=True, blank=True, max_digits=8, decimal_places=0)
    old_cbz=models.CharField('CBz', null=True, blank=True, max_length=10)
    old_rolls=models.FloatField('粒数', null=True, blank=True)
    old_packs=models.DecimalField('件数', null=True, blank=True, max_digits=4, decimal_places=1)
    old_input_detail_code=models.CharField('标签打印细码', null=True, blank=True, max_length=100)
    old_kg=models.DecimalField('磅重', null=True, blank=True, max_digits=10, decimal_places=2)
    old_cust_qty=models.DecimalField('毛重', null=True, blank=True, max_digits=10, decimal_places=1)
    old_tube_weight=models.DecimalField('纸筒重', null=True, blank=True, max_digits=6, decimal_places=2)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeSemiInDetail', verbose_name='原关系：SemiInDetail', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_semiinrecord'
        indexes=[models.Index(fields=['source_batch', 'old_rece_sheet_no', 'old_roll_no'],name='src_09e8e89770641ef7'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_rece_sheet_no'))),Upper(RTrim(models.F('old_roll_no'))),name='src_ci_09e8e89770641ef7')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（SemiInRecord，待确认）'
        ordering=["-id"]

class SourceDyeSemiOut(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SemiOut'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'SemiKindID': 'old_semi_kind_id', 'SalerGroupID': 'old_saler_group_id', 'SalerID': 'old_saler_id', 'CustomerID': 'old_customer_id', 'StockUnit': 'old_stock_unit', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'StepNo': 'old_step_no', 'BusinessUnitID': 'old_business_unit_id', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'WareHouseID': 'old_ware_house_id'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_semi_kind_id': 'Chinese_PRC_CI_AS', 'old_saler_group_id': 'Chinese_PRC_CI_AS', 'old_saler_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('出库日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类别', null=True, blank=True)
    old_semi_kind_id=models.CharField('半成品类别', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('业务组别', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('业务员', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户名称', null=True, blank=True, max_length=10)
    old_stock_unit=models.IntegerField('库存单位', null=True, blank=True)
    old_sheet_status=models.IntegerField('SheetStatus', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('Revisions', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_approve_date=models.DateTimeField('审核日期', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_ware_house_id=models.CharField('仓库', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_semiout'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_c21923e80f7f6250'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_c21923e80f7f6250')]
        verbose_name=verbose_name_plural='半成品出库单'
        ordering=["-id"]

class SourceDyeSemiOutDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SemiOutDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'AssignedNo': 'old_assigned_no', 'ReceSheetNo': 'old_rece_sheet_no', 'FabricID': 'old_fabric_id', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'ColorID': 'old_color_id', 'StorageUnitID': 'old_storage_unit_id', 'OutRolls': 'old_out_rolls', 'OutQty': 'old_out_qty', 'OrderNo': 'old_order_no', 'CheckNo': 'old_check_no', 'ShiftID': 'old_shift_id', 'EmpID': 'old_emp_id', 'MachineID': 'old_machine_id', 'Remarks': 'old_remarks', 'JobSheetNo': 'old_job_sheet_no', 'Price': 'old_price', 'GrainQty': 'old_grain_qty', 'Rolls': 'old_rolls', 'WeightQty': 'old_weight_qty', 'LengthQty': 'old_length_qty', 'Packs': 'old_packs', 'PCS': 'old_pcs', 'FixedQty': 'old_fixed_qty', 'Amount': 'old_amount', 'ProdID': 'old_prod_id', 'PreField1': 'old_pre_field1', 'PreField2': 'old_pre_field2', 'PreField3': 'old_pre_field3', 'PreField4': 'old_pre_field4', 'PreField5': 'old_pre_field5', 'WareHouseID': 'old_ware_house_id', 'DetailNo': 'old_detail_no', 'SupplierID': 'old_supplier_id', 'PurchaseOrders': 'old_purchase_orders', 'InSheetKind': 'old_in_sheet_kind', 'A_A': 'old_a_a', 'A_B': 'old_a_b', 'InputCode': 'old_input_code'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_assigned_no': 'Chinese_PRC_CI_AS', 'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_fabric_id': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_storage_unit_id': 'Chinese_PRC_CI_AS', 'old_order_no': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_shift_id': 'Chinese_PRC_CI_AS', 'old_emp_id': 'Chinese_PRC_CI_AS', 'old_machine_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_pre_field1': 'Chinese_PRC_CI_AS', 'old_pre_field2': 'Chinese_PRC_CI_AS', 'old_pre_field3': 'Chinese_PRC_CI_AS', 'old_pre_field4': 'Chinese_PRC_CI_AS', 'old_pre_field5': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_supplier_id': 'Chinese_PRC_CI_AS', 'old_purchase_orders': 'Chinese_PRC_CI_AS', 'old_in_sheet_kind': 'Chinese_PRC_CI_AS', 'old_a_a': 'Chinese_PRC_CI_AS', 'old_a_b': 'Chinese_PRC_CI_AS', 'old_input_code': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：SemiOut', 'target': 'erp_warehouse.SourceDyeSemiOut', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 SemiOutDetail → SemiOut', '原界面主从 SemiOutDetailTurn → SemiOutTurn', '原界面主从 SemiOutSaleDetail → SemiOutSale', '原界面主从 SemiOutWorkDetail → SemiOutWork', '原界面主从 SemiOutDetailJob → SemiOutJob']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=True, blank=True, max_length=20)
    old_assigned_no=models.CharField('投胚流水号', null=True, blank=True, max_length=20)
    old_rece_sheet_no=models.CharField('入库明细号', null=True, blank=True, max_length=20)
    old_fabric_id=models.CharField('客户规格', null=True, blank=True, max_length=128)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=128)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('物料颜色', null=True, blank=True, max_length=20)
    old_storage_unit_id=models.CharField('库位', null=True, blank=True, max_length=10)
    old_out_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_out_qty=models.DecimalField('数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_order_no=models.CharField('订单号', null=True, blank=True, max_length=20)
    old_check_no=models.CharField('订单明细号', null=True, blank=True, max_length=20)
    old_shift_id=models.CharField('班组', null=True, blank=True, max_length=10)
    old_emp_id=models.CharField('员工', null=True, blank=True, max_length=10)
    old_machine_id=models.CharField('机台', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=8, decimal_places=2)
    old_grain_qty=models.DecimalField('GrainQty', null=True, blank=True, max_digits=8, decimal_places=2)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_weight_qty=models.DecimalField('重量', null=True, blank=True, max_digits=8, decimal_places=2)
    old_length_qty=models.DecimalField('长度', null=True, blank=True, max_digits=8, decimal_places=2)
    old_packs=models.DecimalField('件数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_pcs=models.IntegerField('件/粒', null=True, blank=True)
    old_fixed_qty=models.DecimalField('锭重', null=True, blank=True, max_digits=5, decimal_places=2)
    old_amount=models.DecimalField('金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=200)
    old_pre_field1=models.CharField('捻度(H/S)', null=True, blank=True, max_length=50)
    old_pre_field2=models.CharField('PreField2', null=True, blank=True, max_length=50)
    old_pre_field3=models.CharField('PreField3', null=True, blank=True, max_length=50)
    old_pre_field4=models.CharField('PreField4', null=True, blank=True, max_length=50)
    old_pre_field5=models.CharField('PreField5', null=True, blank=True, max_length=200)
    old_ware_house_id=models.CharField('仓库', null=True, blank=True, max_length=50)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=50)
    old_supplier_id=models.CharField('供应商', null=True, blank=True, max_length=30)
    old_purchase_orders=models.CharField('采购单号', null=True, blank=True, max_length=20)
    old_in_sheet_kind=models.CharField('物料分类', null=True, blank=True, max_length=20)
    old_a_a=models.CharField('物料区域', null=True, blank=True, max_length=50)
    old_a_b=models.CharField('物料等级', null=True, blank=True, max_length=100)
    old_input_code=models.CharField('打包条码', null=True, blank=True, max_length=40)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeSemiOut', verbose_name='原关系：SemiOut', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_semioutdetail'
        indexes=[models.Index(fields=['source_batch', 'old_assigned_no'],name='src_4f6f2cf7c081581b'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_assigned_no'))),name='src_ci_4f6f2cf7c081581b'),models.Index(fields=['source_batch', 'old_detail_no'],name='src_ef9c245435b4038d'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_ef9c245435b4038d')]
        verbose_name=verbose_name_plural='半成品出库明细'
        ordering=["-id"]

class SourceDyeSemiOutRecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SemiOutRecord'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'AssignedNo': 'old_assigned_no', 'RollNo': 'old_roll_no', 'BarCode': 'old_bar_code', 'ReceSheetNo': 'old_rece_sheet_no', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'StorageUnitID': 'old_storage_unit_id', 'Status': 'old_status', 'Remarks': 'old_remarks', 'GUnit': 'old_gunit', 'Rolls': 'old_rolls', 'Packs': 'old_packs', 'JobSheetNo': 'old_job_sheet_no'}
    SOURCE_KEY=('AssignedNo', 'RollNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_assigned_no': 'Chinese_PRC_CI_AS', 'old_roll_no': 'Chinese_PRC_CI_AS', 'old_bar_code': 'Chinese_PRC_CI_AS', 'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_storage_unit_id': 'Chinese_PRC_CI_AS', 'old_status': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：SemiOutDetail', 'target': 'erp_warehouse.SourceDyeSemiOutDetail', 'source_fields': ['AssignedNo'], 'target_fields': ['AssignedNo'], 'evidence': ['原界面主从 SemiOutRecordTurn → SemiOutDetailTurn', '原界面主从 SemiOutRecordJob → SemiOutDetailJob', '原界面主从 SemiOutRecord → SemiOutDetail', '原界面主从 SemiOutSaleRecord → SemiOutSaleDetail', '原界面主从 SemiOutWorkRecord → SemiOutWorkDetail']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('工卡流水', null=True, blank=True, max_length=20)
    old_assigned_no=models.CharField('投胚流水号', null=False, blank=True, max_length=20)
    old_roll_no=models.CharField('箱号', null=False, blank=True, max_length=20)
    old_bar_code=models.CharField('胚纱条码', null=True, blank=True, max_length=50)
    old_rece_sheet_no=models.CharField('入库明细号', null=True, blank=True, max_length=20)
    old_length_qty=models.DecimalField('长度数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('重量数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_storage_unit_id=models.CharField('仓位代码', null=True, blank=True, max_length=10)
    old_status=models.CharField('状态', null=True, blank=True, max_length=10)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_gunit=models.IntegerField('GUnit', null=True, blank=True)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=4, decimal_places=1)
    old_packs=models.DecimalField('件数', null=True, blank=True, max_digits=4, decimal_places=1)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeSemiOutDetail', verbose_name='原关系：SemiOutDetail', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_semioutrecord'
        indexes=[models.Index(fields=['source_batch', 'old_assigned_no', 'old_roll_no'],name='src_941b12ccd9bb3b39'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_assigned_no'))),Upper(RTrim(models.F('old_roll_no'))),name='src_ci_941b12ccd9bb3b39')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（SemiOutRecord，待确认）'
        ordering=["-id"]

class SourceDyeSemiPostionUp(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SemiPostionUp'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'JobSheetNo': 'old_job_sheet_no', 'SupplierID': 'old_supplier_id', 'CustomerID': 'old_customer_id', 'InSheetKind': 'old_in_sheet_kind', 'ProdID': 'old_prod_id', 'LotNo': 'old_lot_no', 'ColorID': 'old_color_id', 'PreField1': 'old_pre_field1', 'FixedQty': 'old_fixed_qty', 'PurchaseOrders': 'old_purchase_orders', 'A_A': 'old_a_a', 'A_B': 'old_a_b', 'Rolls': 'old_rolls', 'WeightQty': 'old_weight_qty', 'LengthQty': 'old_length_qty', 'Packs': 'old_packs', 'PCS': 'old_pcs', 'Area': 'old_area', 'NewArea': 'old_new_area', 'SheetStatus': 'old_sheet_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'InDetailNo': 'old_in_detail_no'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_supplier_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_in_sheet_kind': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_pre_field1': 'Chinese_PRC_CI_AS', 'old_purchase_orders': 'Chinese_PRC_CI_AS', 'old_a_a': 'Chinese_PRC_CI_AS', 'old_a_b': 'Chinese_PRC_CI_AS', 'old_area': 'Chinese_PRC_CI_AS', 'old_new_area': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_in_detail_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=36)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_supplier_id=models.CharField('供应商', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=50)
    old_in_sheet_kind=models.CharField('物料分类', null=True, blank=True, max_length=20)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=200)
    old_color_id=models.CharField('物料颜色', null=True, blank=True, max_length=50)
    old_pre_field1=models.CharField('捻度(H/S)', null=True, blank=True, max_length=50)
    old_fixed_qty=models.DecimalField('锭重', null=True, blank=True, max_digits=5, decimal_places=2)
    old_purchase_orders=models.CharField('采购单号', null=True, blank=True, max_length=20)
    old_a_a=models.CharField('物料区域', null=True, blank=True, max_length=50)
    old_a_b=models.CharField('物料等级', null=True, blank=True, max_length=100)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_weight_qty=models.DecimalField('重量数量', null=True, blank=True, max_digits=8, decimal_places=2)
    old_length_qty=models.DecimalField('长度数量', null=True, blank=True, max_digits=8, decimal_places=2)
    old_packs=models.DecimalField('件数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_pcs=models.IntegerField('粒/件', null=True, blank=True)
    old_area=models.CharField('原区域', null=True, blank=True, max_length=100)
    old_new_area=models.CharField('新区域', null=True, blank=True, max_length=100)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_step_no=models.IntegerField('流程节点号', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_in_detail_no=models.CharField('InDetailNo', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_semipostionup'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_1f4a72f8503f14fd'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_1f4a72f8503f14fd')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（SemiPostionUp，待确认）'
        ordering=["-id"]

class SourceDyeSemiStock(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SemiStock'
    SOURCE_FIELDS={'StockDate': 'old_stock_date', 'BusinessUnitID': 'old_business_unit_id', 'CustomerID': 'old_customer_id', 'WareHouseID': 'old_ware_house_id', 'GrayKindID': 'old_gray_kind_id', 'SalerGroupID': 'old_saler_group_id', 'SupplierID': 'old_supplier_id', 'BusinessKind': 'old_business_kind', 'ProdID': 'old_prod_id', 'StockKind': 'old_stock_kind', 'SalerID': 'old_saler_id', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'PreMonthPacks': 'old_pre_month_packs', 'PreMonthRolls': 'old_pre_month_rolls', 'Price': 'old_price', 'CarryDate': 'old_carry_date', 'Remarks': 'old_remarks', 'PreMonthWeightQty': 'old_pre_month_weight_qty', 'PreMonthLengthQty': 'old_pre_month_length_qty', 'StorageUnitIDs': 'old_storage_unit_ids', 'ReceSheetNo': 'old_rece_sheet_no', 'PreField1': 'old_pre_field1', 'PurchaseOrders': 'old_purchase_orders', 'A_A': 'old_a_a', 'A_B': 'old_a_b', 'FixedQty': 'old_fixed_qty', 'ColorID': 'old_color_id'}
    SOURCE_KEY=('StockDate', 'CustomerID', 'WareHouseID', 'SupplierID', 'ProdID', 'SalerID', 'ColorID', 'Spec', 'LotNo', 'ReceSheetNo', 'PreField1', 'PurchaseOrders', 'A_A', 'A_B', 'FixedQty')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_gray_kind_id': 'Chinese_PRC_CI_AS', 'old_saler_group_id': 'Chinese_PRC_CI_AS', 'old_supplier_id': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_saler_id': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_storage_unit_ids': 'Chinese_PRC_CI_AS', 'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_pre_field1': 'Chinese_PRC_CI_AS', 'old_purchase_orders': 'Chinese_PRC_CI_AS', 'old_a_a': 'Chinese_PRC_CI_AS', 'old_a_b': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_stock_date=models.DateTimeField('StockDate', null=False, blank=False)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('CustomerID', null=False, blank=True, max_length=10)
    old_ware_house_id=models.CharField('WareHouseID', null=False, blank=True, max_length=10)
    old_gray_kind_id=models.CharField('GrayKindID', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('SalerGroupID', null=True, blank=True, max_length=10)
    old_supplier_id=models.CharField('SupplierID', null=False, blank=True, max_length=10)
    old_business_kind=models.IntegerField('BusinessKind', null=True, blank=True)
    old_prod_id=models.CharField('ProdID', null=False, blank=True, max_length=50)
    old_stock_kind=models.IntegerField('StockKind', null=True, blank=True)
    old_saler_id=models.CharField('SalerID', null=False, blank=True, max_length=10)
    old_spec=models.CharField('Spec', null=False, blank=True, max_length=128)
    old_lot_no=models.CharField('LotNo', null=False, blank=True, max_length=50)
    old_pre_month_packs=models.DecimalField('PreMonthPacks', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pre_month_rolls=models.DecimalField('PreMonthRolls', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=8, decimal_places=2)
    old_carry_date=models.DateTimeField('CarryDate', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_pre_month_weight_qty=models.DecimalField('PreMonthWeightQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pre_month_length_qty=models.DecimalField('PreMonthLengthQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_storage_unit_ids=models.CharField('StorageUnitIDs', null=True, blank=True, max_length=100)
    old_rece_sheet_no=models.CharField('ReceSheetNo', null=False, blank=True, max_length=20)
    old_pre_field1=models.CharField('PreField1', null=False, blank=True, max_length=50)
    old_purchase_orders=models.CharField('PurchaseOrders', null=False, blank=True, max_length=20)
    old_a_a=models.CharField('A_A', null=False, blank=True, max_length=50)
    old_a_b=models.CharField('A_B', null=False, blank=True, max_length=100)
    old_fixed_qty=models.DecimalField('FixedQty', null=False, blank=False, max_digits=5, decimal_places=1)
    old_color_id=models.CharField('ColorID', null=False, blank=True, max_length=30)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_semistock'
        indexes=[models.Index(fields=['source_batch', 'old_stock_date', 'old_customer_id', 'old_ware_house_id', 'old_supplier_id', 'old_prod_id', 'old_saler_id', 'old_color_id', 'old_spec', 'old_lot_no', 'old_rece_sheet_no', 'old_pre_field1', 'old_purchase_orders', 'old_a_a', 'old_a_b', 'old_fixed_qty'],name='src_99fb667b0d77e557'),models.Index(models.F('source_batch'),models.F('old_stock_date'),Upper(RTrim(models.F('old_customer_id'))),Upper(RTrim(models.F('old_ware_house_id'))),Upper(RTrim(models.F('old_supplier_id'))),Upper(RTrim(models.F('old_prod_id'))),Upper(RTrim(models.F('old_saler_id'))),Upper(RTrim(models.F('old_color_id'))),Upper(RTrim(models.F('old_spec'))),Upper(RTrim(models.F('old_lot_no'))),Upper(RTrim(models.F('old_rece_sheet_no'))),Upper(RTrim(models.F('old_pre_field1'))),Upper(RTrim(models.F('old_purchase_orders'))),Upper(RTrim(models.F('old_a_a'))),Upper(RTrim(models.F('old_a_b'))),models.F('old_fixed_qty'),name='src_ci_99fb667b0d77e557')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（SemiStock，待确认）'
        ordering=["-id"]

class SourceDyeSemiStockAdjust(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SemiStockAdjust'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'BusinessUnitID': 'old_business_unit_id', 'BusinessKind': 'old_business_kind', 'GrayKindID': 'old_gray_kind_id', 'SalerGroupID': 'old_saler_group_id', 'CustomerID': 'old_customer_id', 'WareHouseID': 'old_ware_house_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_gray_kind_id': 'Chinese_PRC_CI_AS', 'old_saler_group_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类别', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位', null=True, blank=True, max_length=10)
    old_business_kind=models.IntegerField('业务类别', null=True, blank=True)
    old_gray_kind_id=models.CharField('胚纱类别', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('业务组别', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=10)
    old_ware_house_id=models.CharField('仓库代码', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_step_no=models.IntegerField('工作流节点号', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_semistockadjust'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_ababb2a39dab5166'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_ababb2a39dab5166')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（SemiStockAdjust，待确认）'
        ordering=["-id"]

class SourceDyeSemiStockAdjustDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SemiStockAdjustDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'JobSheetNo': 'old_job_sheet_no', 'CheckNo': 'old_check_no', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'PaperRolls': 'old_paper_rolls', 'RealRolls': 'old_real_rolls', 'AdjustRolls': 'old_adjust_rolls', 'Price': 'old_price', 'StockUnit': 'old_stock_unit', 'Remarks': 'old_remarks', 'ProdID': 'old_prod_id', 'PaperLength': 'old_paper_length', 'PaperWeight': 'old_paper_weight', 'RealLengthQty': 'old_real_length_qty', 'RealWeightQty': 'old_real_weight_qty', 'AdjustLengthQty': 'old_adjust_length_qty', 'AdjustWeightQty': 'old_adjust_weight_qty', 'StorageUnitIDs': 'old_storage_unit_ids', 'ReceSheetNo': 'old_rece_sheet_no', 'CustomerID': 'old_customer_id', 'InSheetKind': 'old_in_sheet_kind', 'PurchaseOrders': 'old_purchase_orders', 'A_A': 'old_a_a', 'A_B': 'old_a_b', 'FixedQty': 'old_fixed_qty', 'PreField1': 'old_pre_field1'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_storage_unit_ids': 'Chinese_PRC_CI_AS', 'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_in_sheet_kind': 'Chinese_PRC_CI_AS', 'old_purchase_orders': 'Chinese_PRC_CI_AS', 'old_a_a': 'Chinese_PRC_CI_AS', 'old_a_b': 'Chinese_PRC_CI_AS', 'old_pre_field1': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：SemiStockAdjust', 'target': 'erp_warehouse.SourceDyeSemiStockAdjust', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 SemiStockAdjustDetail → SemiStockAdjust']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('调整明细单号', null=False, blank=True, max_length=36)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_check_no=models.CharField('订单明细号', null=True, blank=True, max_length=20)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=128)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('物料颜色', null=True, blank=True, max_length=20)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=20)
    old_paper_rolls=models.DecimalField('帐面粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_rolls=models.DecimalField('实际粒数', null=True, blank=True, max_digits=16, decimal_places=2)
    old_adjust_rolls=models.DecimalField('调整粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=8, decimal_places=2)
    old_stock_unit=models.IntegerField('库存单位', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_paper_length=models.DecimalField('账面长度', null=True, blank=True, max_digits=10, decimal_places=5)
    old_paper_weight=models.DecimalField('账面重量', null=True, blank=True, max_digits=10, decimal_places=5)
    old_real_length_qty=models.DecimalField('实际长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_weight_qty=models.DecimalField('实际重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_adjust_length_qty=models.DecimalField('调整长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_adjust_weight_qty=models.DecimalField('调整重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_storage_unit_ids=models.CharField('库位', null=True, blank=True, max_length=100)
    old_rece_sheet_no=models.CharField('入库明细号', null=True, blank=True, max_length=20)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=50)
    old_in_sheet_kind=models.CharField('物料分类', null=True, blank=True, max_length=20)
    old_purchase_orders=models.CharField('采购单号', null=True, blank=True, max_length=20)
    old_a_a=models.CharField('物料区域', null=True, blank=True, max_length=50)
    old_a_b=models.CharField('物料等级', null=True, blank=True, max_length=100)
    old_fixed_qty=models.DecimalField('锭重', null=True, blank=True, max_digits=5, decimal_places=2)
    old_pre_field1=models.CharField('捻度(H/S)', null=True, blank=True, max_length=50)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeSemiStockAdjust', verbose_name='原关系：SemiStockAdjust', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_semistockadjustdetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_ea8bedc626c20344'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_ea8bedc626c20344')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（SemiStockAdjustDetail，待确认）'
        ordering=["-id"]

class SourceDyeSemiStockBook(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SemiStockBook'
    SOURCE_FIELDS={'BookNo': 'old_book_no', 'BookKind': 'old_book_kind', 'DeptID': 'old_dept_id', 'CustomerID': 'old_customer_id', 'SemiKindID': 'old_semi_kind_id', 'WareHouseID': 'old_ware_house_id', 'FabricID': 'old_fabric_id', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'StorageUnitID': 'old_storage_unit_id', 'SalerGroupID': 'old_saler_group_id', 'SalerID': 'old_saler_id', 'OrderNo': 'old_order_no', 'SheetNo': 'old_sheet_no', 'CheckNo': 'old_check_no', 'InQty': 'old_in_qty', 'InRolls': 'old_in_rolls', 'OutQty': 'old_out_qty', 'OutRolls': 'old_out_rolls', 'StockUnit': 'old_stock_unit', 'Remarks': 'old_remarks', 'BookDate': 'old_book_date', 'BusinessUnitID': 'old_business_unit_id', 'JobSheetNo': 'old_job_sheet_no', 'SheetSeries': 'old_sheet_series', 'SheetKind': 'old_sheet_kind', 'CurrDate': 'old_curr_date', 'ProdID': 'old_prod_id', 'ReceSheetNo': 'old_rece_sheet_no', 'DetailNo': 'old_detail_no', 'InPacks': 'old_in_packs', 'OutPacks': 'old_out_packs', 'Price': 'old_price', 'InWeightQty': 'old_in_weight_qty', 'InLengthQty': 'old_in_length_qty', 'InMoney': 'old_in_money', 'StorageUnitIDs': 'old_storage_unit_ids', 'OutWeightQty': 'old_out_weight_qty', 'OutLengthQty': 'old_out_length_qty', 'OutMoney': 'old_out_money', 'SupplierID': 'old_supplier_id', 'ColorNum': 'old_color_num', 'ColorID': 'old_color_id', 'InSheetKind': 'old_in_sheet_kind', 'PurchaseOrders': 'old_purchase_orders', 'FixedQty': 'old_fixed_qty', 'A_A': 'old_a_a', 'A_B': 'old_a_b', 'PreField1': 'old_pre_field1', 'StockFlag': 'old_stock_flag'}
    SOURCE_KEY=('BookNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_dept_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_semi_kind_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_fabric_id': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_storage_unit_id': 'Chinese_PRC_CI_AS', 'old_saler_group_id': 'Chinese_PRC_CI_AS', 'old_saler_id': 'Chinese_PRC_CI_AS', 'old_order_no': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_kind': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_storage_unit_ids': 'Chinese_PRC_CI_AS', 'old_supplier_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_in_sheet_kind': 'Chinese_PRC_CI_AS', 'old_purchase_orders': 'Chinese_PRC_CI_AS', 'old_a_a': 'Chinese_PRC_CI_AS', 'old_a_b': 'Chinese_PRC_CI_AS', 'old_pre_field1': 'Chinese_PRC_CI_AS', 'old_stock_flag': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=('old_book_no',)
    SOURCE_IDENTITY_RULES={'old_book_no': (1, 1)}
    old_book_no=models.BigIntegerField('BookNo', null=False, blank=False)
    old_book_kind=models.IntegerField('BookKind', null=True, blank=True)
    old_dept_id=models.CharField('DeptID', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=10)
    old_semi_kind_id=models.CharField('SemiKindID', null=True, blank=True, max_length=10)
    old_ware_house_id=models.CharField('WareHouseID', null=True, blank=True, max_length=10)
    old_fabric_id=models.CharField('FabricID', null=True, blank=True, max_length=128)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=128)
    old_lot_no=models.CharField('LotNo', null=True, blank=True, max_length=50)
    old_storage_unit_id=models.CharField('StorageUnitID', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('SalerGroupID', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('SalerID', null=True, blank=True, max_length=10)
    old_order_no=models.CharField('OrderNo', null=True, blank=True, max_length=20)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=20)
    old_check_no=models.CharField('CheckNo', null=True, blank=True, max_length=20)
    old_in_qty=models.DecimalField('InQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_in_rolls=models.DecimalField('InRolls', null=True, blank=True, max_digits=7, decimal_places=2)
    old_out_qty=models.DecimalField('OutQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_out_rolls=models.DecimalField('OutRolls', null=True, blank=True, max_digits=7, decimal_places=2)
    old_stock_unit=models.IntegerField('StockUnit', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_book_date=models.DateTimeField('BookDate', null=True, blank=True)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)
    old_sheet_series=models.CharField('SheetSeries', null=True, blank=True, max_length=50)
    old_sheet_kind=models.CharField('SheetKind', null=True, blank=True, max_length=30)
    old_curr_date=models.DateTimeField('CurrDate', null=True, blank=True)
    old_prod_id=models.CharField('ProdID', null=True, blank=True, max_length=200)
    old_rece_sheet_no=models.CharField('ReceSheetNo', null=True, blank=True, max_length=50)
    old_detail_no=models.CharField('DetailNo', null=True, blank=True, max_length=50)
    old_in_packs=models.DecimalField('InPacks', null=True, blank=True, max_digits=7, decimal_places=2)
    old_out_packs=models.DecimalField('OutPacks', null=True, blank=True, max_digits=7, decimal_places=2)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=8, decimal_places=2)
    old_in_weight_qty=models.DecimalField('InWeightQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_in_length_qty=models.DecimalField('InLengthQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_in_money=models.DecimalField('InMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_storage_unit_ids=models.CharField('StorageUnitIDs', null=True, blank=True, max_length=100)
    old_out_weight_qty=models.DecimalField('OutWeightQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_out_length_qty=models.DecimalField('OutLengthQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_out_money=models.DecimalField('OutMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_supplier_id=models.CharField('SupplierID', null=True, blank=True, max_length=30)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=20)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=20)
    old_in_sheet_kind=models.CharField('InSheetKind', null=True, blank=True, max_length=20)
    old_purchase_orders=models.CharField('PurchaseOrders', null=True, blank=True, max_length=20)
    old_fixed_qty=models.DecimalField('FixedQty', null=True, blank=True, max_digits=5, decimal_places=2)
    old_a_a=models.CharField('A_A', null=True, blank=True, max_length=50)
    old_a_b=models.CharField('A_B', null=True, blank=True, max_length=100)
    old_pre_field1=models.CharField('PreField1', null=True, blank=True, max_length=50)
    old_stock_flag=models.CharField('StockFlag', null=True, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_semistockbook'
        indexes=[models.Index(fields=['source_batch', 'old_book_no'],name='src_d7102df70e800ac8')]
        verbose_name=verbose_name_plural='半成品库存流水'
        ordering=["-id"]

class SourceDyeSemiStockSpecUp(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SemiStockSpecUp'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'SalerGroupID': 'old_saler_group_id', 'SalerID': 'old_saler_id', 'StockUnit': 'old_stock_unit', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'StepNo': 'old_step_no', 'BusinessUnitID': 'old_business_unit_id', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'WareHouseID': 'old_ware_house_id'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_saler_group_id': 'Chinese_PRC_CI_AS', 'old_saler_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('出库日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类别', null=True, blank=True)
    old_saler_group_id=models.CharField('业务组别', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('业务员', null=True, blank=True, max_length=10)
    old_stock_unit=models.IntegerField('库存单位', null=True, blank=True)
    old_sheet_status=models.IntegerField('SheetStatus', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('Revisions', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_approve_date=models.DateTimeField('审核日期', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_ware_house_id=models.CharField('仓库', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_semistockspecup'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_0d32b69812e76f28'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_0d32b69812e76f28')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（SemiStockSpecUp，待确认）'
        ordering=["-id"]

class SourceDyeSemiStockSpecUpDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SemiStockSpecUpDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'AssignedNo': 'old_assigned_no', 'ReceSheetNo': 'old_rece_sheet_no', 'DetailNo': 'old_detail_no', 'PCS': 'old_pcs', 'Rolls': 'old_rolls', 'Packs': 'old_packs', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'Price': 'old_price', 'CheckNo': 'old_check_no', 'Remarks': 'old_remarks', 'Area': 'old_area', 'StorageUnitIDs': 'old_storage_unit_ids', 'WareHouseID': 'old_ware_house_id', 'CustomerID': 'old_customer_id', 'InSheetKind': 'old_in_sheet_kind', 'ProdID': 'old_prod_id', 'LotNo': 'old_lot_no', 'ColorID': 'old_color_id', 'FixedQty': 'old_fixed_qty', 'SupplierID': 'old_supplier_id', 'PreField1': 'old_pre_field1', 'PurchaseOrders': 'old_purchase_orders', 'A_A': 'old_a_a', 'A_B': 'old_a_b', 'UPCustomerID': 'old_upcustomer_id', 'UPInSheetKind': 'old_upin_sheet_kind', 'UPProdID': 'old_upprod_id', 'UPLotNo': 'old_uplot_no', 'UPColorID': 'old_upcolor_id', 'UPFixedQty': 'old_upfixed_qty', 'UPPreField1': 'old_uppre_field1', 'UPPurchaseOrders': 'old_uppurchase_orders', 'UPA_A': 'old_upa_a', 'UPA_B': 'old_upa_b'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_assigned_no': 'Chinese_PRC_CI_AS', 'old_rece_sheet_no': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_area': 'Chinese_PRC_CI_AS', 'old_storage_unit_ids': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_in_sheet_kind': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_supplier_id': 'Chinese_PRC_CI_AS', 'old_pre_field1': 'Chinese_PRC_CI_AS', 'old_purchase_orders': 'Chinese_PRC_CI_AS', 'old_a_a': 'Chinese_PRC_CI_AS', 'old_a_b': 'Chinese_PRC_CI_AS', 'old_upcustomer_id': 'Chinese_PRC_CI_AS', 'old_upin_sheet_kind': 'Chinese_PRC_CI_AS', 'old_upprod_id': 'Chinese_PRC_CI_AS', 'old_uplot_no': 'Chinese_PRC_CI_AS', 'old_upcolor_id': 'Chinese_PRC_CI_AS', 'old_uppre_field1': 'Chinese_PRC_CI_AS', 'old_uppurchase_orders': 'Chinese_PRC_CI_AS', 'old_upa_a': 'Chinese_PRC_CI_AS', 'old_upa_b': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：SemiStockSpecUp', 'target': 'erp_warehouse.SourceDyeSemiStockSpecUp', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 SemiStockSpecUpDetail → SemiStockSpecUp']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=True, blank=True, max_length=20)
    old_assigned_no=models.CharField('投胚流水号', null=True, blank=True, max_length=20)
    old_rece_sheet_no=models.CharField('入库明细号', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=50)
    old_pcs=models.IntegerField('粒/件', null=True, blank=True)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_packs=models.DecimalField('件数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_length_qty=models.DecimalField('长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=8, decimal_places=2)
    old_check_no=models.CharField('订单明细号', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_area=models.CharField('区域', null=True, blank=True, max_length=100)
    old_storage_unit_ids=models.CharField('库位', null=True, blank=True, max_length=100)
    old_ware_house_id=models.CharField('仓库', null=True, blank=True, max_length=20)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=30)
    old_in_sheet_kind=models.CharField('物料分类', null=True, blank=True, max_length=20)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=50)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('物料颜色', null=True, blank=True, max_length=20)
    old_fixed_qty=models.DecimalField('锭重', null=True, blank=True, max_digits=5, decimal_places=2)
    old_supplier_id=models.CharField('供应商', null=True, blank=True, max_length=30)
    old_pre_field1=models.CharField('捻度(H/S)', null=True, blank=True, max_length=50)
    old_purchase_orders=models.CharField('采购单号', null=True, blank=True, max_length=20)
    old_a_a=models.CharField('物料区域', null=True, blank=True, max_length=50)
    old_a_b=models.CharField('物料等级', null=True, blank=True, max_length=100)
    old_upcustomer_id=models.CharField('调整客户', null=True, blank=True, max_length=30)
    old_upin_sheet_kind=models.CharField('调整物料分类', null=True, blank=True, max_length=20)
    old_upprod_id=models.CharField('调整规格', null=True, blank=True, max_length=50)
    old_uplot_no=models.CharField('调整批号', null=True, blank=True, max_length=50)
    old_upcolor_id=models.CharField('调整物料颜色', null=True, blank=True, max_length=20)
    old_upfixed_qty=models.DecimalField('调整锭重', null=True, blank=True, max_digits=5, decimal_places=2)
    old_uppre_field1=models.CharField('调整捻度(H/S)', null=True, blank=True, max_length=50)
    old_uppurchase_orders=models.CharField('调整采购单号', null=True, blank=True, max_length=20)
    old_upa_a=models.CharField('调整物料缸号', null=True, blank=True, max_length=50)
    old_upa_b=models.CharField('调整物料等级', null=True, blank=True, max_length=100)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeSemiStockSpecUp', verbose_name='原关系：SemiStockSpecUp', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_semistockspecupdetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_ba0430cc235b3809'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_ba0430cc235b3809')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（SemiStockSpecUpDetail，待确认）'
        ordering=["-id"]

class SourceDyeStuffStep(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='Stuff_Step'
    SOURCE_FIELDS={'Code': 'old_code', 'Name': 'old_name', 'Reserved1': 'old_reserved1', 'CodeNo': 'old_code_no', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('Code',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_code': 'Chinese_PRC_CI_AS', 'old_name': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_code=models.CharField('编码', null=False, blank=True, max_length=20)
    old_name=models.CharField('备料步骤', null=False, blank=True, max_length=100)
    old_reserved1=models.IntegerField('Reserved1', null=True, blank=True)
    old_code_no=models.IntegerField('步骤号', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_stuff_step'
        indexes=[models.Index(fields=['source_batch', 'old_code'],name='src_2f83c4f22a44033e'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_code'))),name='src_ci_2f83c4f22a44033e')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（Stuff_Step，待确认）'
        ordering=["-id"]

class SourceDyeStuffAllot(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StuffAllot'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'BusinessUnitID': 'old_business_unit_id', 'WareHouseID': 'old_ware_house_id', 'DeptID': 'old_dept_id', 'CustomerID': 'old_customer_id', 'Keeper': 'old_keeper', 'EmpID': 'old_emp_id', 'WeightSheetNo': 'old_weight_sheet_no', 'RightStatus': 'old_right_status', 'SheetStatus': 'old_sheet_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'ToWareHouseID': 'old_to_ware_house_id'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_dept_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_keeper': 'Chinese_PRC_CI_AS', 'old_emp_id': 'Chinese_PRC_CI_AS', 'old_weight_sheet_no': 'Chinese_PRC_CI_AS', 'old_sheet_status': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_to_ware_house_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=50)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=36)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_ware_house_id=models.CharField('调出仓库', null=True, blank=True, max_length=10)
    old_dept_id=models.CharField('申领部门', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=50)
    old_keeper=models.CharField('仓管员', null=True, blank=True, max_length=100)
    old_emp_id=models.CharField('领料人', null=True, blank=True, max_length=50)
    old_weight_sheet_no=models.CharField('WeightSheetNo', null=True, blank=True, max_length=20)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_sheet_status=models.CharField('SheetStatus', null=True, blank=True, max_length=1)
    old_step_no=models.IntegerField('流程节点号', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_to_ware_house_id=models.CharField('调入仓库', null=True, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_stuffallot'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_f546f0cb8ae39481'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_f546f0cb8ae39481')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（StuffAllot，待确认）'
        ordering=["-id"]

class SourceDyeStuffAllotDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StuffAllotDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'PurDetailNo': 'old_pur_detail_no', 'StuffID': 'old_stuff_id', 'LotNo': 'old_lot_no', 'Qty': 'old_qty', 'Price': 'old_price', 'TaxPrice': 'old_tax_price', 'TaxRate': 'old_tax_rate', 'TaxMoney': 'old_tax_money', 'Amount': 'old_amount', 'APDetailNo': 'old_apdetail_no', 'InDetailNo': 'old_in_detail_no', 'DlvQty': 'old_dlv_qty', 'Remarks': 'old_remarks', 'StockUnit': 'old_stock_unit'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_pur_detail_no': 'Chinese_PRC_CI_AS', 'old_stuff_id': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_apdetail_no': 'Chinese_PRC_CI_AS', 'old_in_detail_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_stock_unit': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：StuffAllot', 'target': 'erp_warehouse.SourceDyeStuffAllot', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 StuffAllotDetail → StuffAllot']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=True, blank=True, max_length=50)
    old_detail_no=models.CharField('表单明细号（子表）', null=False, blank=True, max_length=36)
    old_pur_detail_no=models.CharField('采购单明细号', null=True, blank=True, max_length=20)
    old_stuff_id=models.CharField('染化料代码', null=True, blank=True, max_length=10)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=200)
    old_qty=models.DecimalField('数量', null=True, blank=True, max_digits=12, decimal_places=6)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=16, decimal_places=6)
    old_tax_price=models.DecimalField('含税价', null=True, blank=True, max_digits=16, decimal_places=6)
    old_tax_rate=models.DecimalField('税率', null=True, blank=True, max_digits=4, decimal_places=2)
    old_tax_money=models.DecimalField('税金', null=True, blank=True, max_digits=10, decimal_places=2)
    old_amount=models.DecimalField('金额', null=True, blank=True, max_digits=16, decimal_places=2)
    old_apdetail_no=models.CharField('应付单细号', null=True, blank=True, max_length=20)
    old_in_detail_no=models.CharField('InDetailNo', null=True, blank=True, max_length=50)
    old_dlv_qty=models.DecimalField('交货数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_stock_unit=models.CharField('单位', null=True, blank=True, max_length=1)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeStuffAllot', verbose_name='原关系：StuffAllot', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_stuffallotdetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_ea92fb489b1df2e6'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_ea92fb489b1df2e6')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（StuffAllotDetail，待确认）'
        ordering=["-id"]

class SourceDyeStuffChange(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StuffChange'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'StartTime': 'old_start_time', 'Reason': 'old_reason', 'OriStuffID': 'old_ori_stuff_id', 'OriLotNo': 'old_ori_lot_no', 'RemainQty': 'old_remain_qty', 'StuffID': 'old_stuff_id', 'LotNo': 'old_lot_no', 'InQty': 'old_in_qty', 'InDate': 'old_in_date', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_start_time': 'Chinese_PRC_CI_AS', 'old_reason': 'Chinese_PRC_CI_AS', 'old_ori_stuff_id': 'Chinese_PRC_CI_AS', 'old_ori_lot_no': 'Chinese_PRC_CI_AS', 'old_stuff_id': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_start_time=models.CharField('StartTime', null=True, blank=True, max_length=14)
    old_reason=models.CharField('Reason', null=True, blank=True, max_length=256)
    old_ori_stuff_id=models.CharField('OriStuffID', null=True, blank=True, max_length=10)
    old_ori_lot_no=models.CharField('OriLotNo', null=True, blank=True, max_length=50)
    old_remain_qty=models.DecimalField('RemainQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_stuff_id=models.CharField('StuffID', null=True, blank=True, max_length=10)
    old_lot_no=models.CharField('LotNo', null=True, blank=True, max_length=50)
    old_in_qty=models.DecimalField('InQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_in_date=models.DateTimeField('InDate', null=True, blank=True)
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
        db_table='src_dye_stuffchange'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_0b7dc82289f8dc42'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_0b7dc82289f8dc42')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（StuffChange，待确认）'
        ordering=["-id"]

class SourceDyeStuffIn(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StuffIn'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'WareHouseID': 'old_ware_house_id', 'SupplierID': 'old_supplier_id', 'BusinessUnitID': 'old_business_unit_id', 'RightStatus': 'old_right_status', 'SheetStatus': 'old_sheet_status', 'Keeper': 'old_keeper', 'Reason': 'old_reason', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'APMoney': 'old_apmoney', 'APQty': 'old_apqty', 'UnClearQty': 'old_un_clear_qty', 'UnClearMoney': 'old_un_clear_money', 'UnClearInvoiceQty': 'old_un_clear_invoice_qty', 'UnClearInvoiceMoney': 'old_un_clear_invoice_money', 'Discount': 'old_discount', 'DiscountMoney': 'old_discount_money', 'Total': 'old_total', 'BuyerID': 'old_buyer_id', 'invoice': 'old_invoice'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_supplier_id': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_sheet_status': 'Chinese_PRC_CI_AS', 'old_keeper': 'Chinese_PRC_CI_AS', 'old_reason': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_buyer_id': 'Chinese_PRC_CI_AS', 'old_invoice': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_step_no=models.IntegerField('流程节点号', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_ware_house_id=models.CharField('仓库', null=True, blank=True, max_length=10)
    old_supplier_id=models.CharField('供应商', null=True, blank=True, max_length=10)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_sheet_status=models.CharField('SheetStatus', null=True, blank=True, max_length=1)
    old_keeper=models.CharField('仓管员', null=True, blank=True, max_length=10)
    old_reason=models.CharField('Reason', null=True, blank=True, max_length=256)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_apmoney=models.DecimalField('APMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_apqty=models.DecimalField('APQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_un_clear_qty=models.DecimalField('UnClearQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_un_clear_money=models.DecimalField('UnClearMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_un_clear_invoice_qty=models.DecimalField('UnClearInvoiceQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_un_clear_invoice_money=models.DecimalField('UnClearInvoiceMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_discount=models.DecimalField('Discount', null=True, blank=True, max_digits=3, decimal_places=2)
    old_discount_money=models.DecimalField('DiscountMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_total=models.DecimalField('Total', null=True, blank=True, max_digits=10, decimal_places=2)
    old_buyer_id=models.CharField('采购员', null=True, blank=True, max_length=50)
    old_invoice=models.CharField('发票单号', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_stuffin'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_436e4545efafe40e'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_436e4545efafe40e')]
        verbose_name=verbose_name_plural='染化料入库单'
        ordering=["-id"]

class SourceDyeStuffInDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StuffInDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'PurDetailNo': 'old_pur_detail_no', 'StuffID': 'old_stuff_id', 'Price': 'old_price', 'TaxPrice': 'old_tax_price', 'TaxRate': 'old_tax_rate', 'TaxMoney': 'old_tax_money', 'Amount': 'old_amount', 'Qty': 'old_qty', 'APDetailNo': 'old_apdetail_no', 'LotNo': 'old_lot_no', 'Remarks': 'old_remarks', 'PackUnit': 'old_pack_unit', 'PackQty': 'old_pack_qty', 'NewStuffID': 'old_new_stuff_id', 'StuffType': 'old_stuff_type', 'StuffKindID': 'old_stuff_kind_id', 'StuffName': 'old_stuff_name', 'OriInDetailNo': 'old_ori_in_detail_no'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_pur_detail_no': 'Chinese_PRC_CI_AS', 'old_stuff_id': 'Chinese_PRC_CI_AS', 'old_apdetail_no': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_pack_unit': 'Chinese_PRC_CI_AS', 'old_new_stuff_id': 'Chinese_PRC_CI_AS', 'old_stuff_type': 'Chinese_PRC_CI_AS', 'old_stuff_kind_id': 'Chinese_PRC_CI_AS', 'old_stuff_name': 'Chinese_PRC_CI_AS', 'old_ori_in_detail_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：StuffIn', 'target': 'erp_warehouse.SourceDyeStuffIn', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 SmallStuffInDetail → SmallStuffIn', '原界面主从 StuffInDetail → StuffIn']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('表单明细号（子表）', null=False, blank=True, max_length=36)
    old_pur_detail_no=models.CharField('采购单明细号', null=True, blank=True, max_length=20)
    old_stuff_id=models.CharField('染化料代码', null=True, blank=True, max_length=10)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=16, decimal_places=6)
    old_tax_price=models.DecimalField('含税价', null=True, blank=True, max_digits=16, decimal_places=6)
    old_tax_rate=models.DecimalField('税率', null=True, blank=True, max_digits=4, decimal_places=2)
    old_tax_money=models.DecimalField('税金', null=True, blank=True, max_digits=10, decimal_places=2)
    old_amount=models.DecimalField('金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_qty=models.DecimalField('数量', null=True, blank=True, max_digits=12, decimal_places=6)
    old_apdetail_no=models.CharField('应付单细号', null=True, blank=True, max_length=100)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=50)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_pack_unit=models.CharField('包装单位', null=True, blank=True, max_length=10)
    old_pack_qty=models.DecimalField('包装数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_new_stuff_id=models.CharField('NewStuffID', null=True, blank=True, max_length=20)
    old_stuff_type=models.CharField('StuffType', null=True, blank=True, max_length=1)
    old_stuff_kind_id=models.CharField('StuffKindID', null=True, blank=True, max_length=50)
    old_stuff_name=models.CharField('StuffName', null=True, blank=True, max_length=300)
    old_ori_in_detail_no=models.CharField('原入库明细', null=True, blank=True, max_length=30)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeStuffIn', verbose_name='原关系：StuffIn', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_stuffindetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_bef67ab2c25ac5fa'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_bef67ab2c25ac5fa')]
        verbose_name=verbose_name_plural='染化料入库明细'
        ordering=["-id"]

class SourceDyeStuffOut(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StuffOut'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'BusinessUnitID': 'old_business_unit_id', 'WareHouseID': 'old_ware_house_id', 'DeptID': 'old_dept_id', 'CustomerID': 'old_customer_id', 'Keeper': 'old_keeper', 'EmpID': 'old_emp_id', 'RightStatus': 'old_right_status', 'SheetStatus': 'old_sheet_status', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'WeightSheetNo': 'old_weight_sheet_no', 'InDetailNo': 'old_in_detail_no', 'JobSheetNo': 'old_job_sheet_no', 'OutDate': 'old_out_date', 'MachineID': 'old_machine_id', 'SQSheetNo': 'old_sqsheet_no', 'FactID': 'old_fact_id', 'CombineSheetNos': 'old_combine_sheet_nos', 'ShiftID': 'old_shift_id'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_dept_id': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_keeper': 'Chinese_PRC_CI_AS', 'old_emp_id': 'Chinese_PRC_CI_AS', 'old_sheet_status': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_weight_sheet_no': 'Chinese_PRC_CI_AS', 'old_in_detail_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_machine_id': 'Chinese_PRC_CI_AS', 'old_sqsheet_no': 'Chinese_PRC_CI_AS', 'old_fact_id': 'Chinese_PRC_CI_AS', 'old_combine_sheet_nos': 'Chinese_PRC_CI_AS', 'old_shift_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_step_no=models.IntegerField('流程节点号', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位', null=True, blank=True, max_length=10)
    old_ware_house_id=models.CharField('仓库', null=True, blank=True, max_length=10)
    old_dept_id=models.CharField('申领部门', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=10)
    old_keeper=models.CharField('仓管员', null=True, blank=True, max_length=100)
    old_emp_id=models.CharField('领料人', null=True, blank=True, max_length=10)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_sheet_status=models.CharField('SheetStatus', null=True, blank=True, max_length=1)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_weight_sheet_no=models.CharField('称料单号', null=True, blank=True, max_length=20)
    old_in_detail_no=models.CharField('InDetailNo', null=True, blank=True, max_length=50)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_out_date=models.DateTimeField('出库日期', null=True, blank=True)
    old_machine_id=models.CharField('机台号', null=True, blank=True, max_length=255)
    old_sqsheet_no=models.CharField('申请单号', null=True, blank=True, max_length=50)
    old_fact_id=models.CharField('领用分厂', null=True, blank=True, max_length=50)
    old_combine_sheet_nos=models.CharField('合染缸号', null=True, blank=True, max_length=100)
    old_shift_id=models.CharField('班别', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_stuffout'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_0b80b199c2bce7cc'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_0b80b199c2bce7cc')]
        verbose_name=verbose_name_plural='染化料出库单'
        ordering=["-id"]

class SourceDyeStuffOutDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StuffOutDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'PurDetailNo': 'old_pur_detail_no', 'StuffID': 'old_stuff_id', 'Price': 'old_price', 'TaxPrice': 'old_tax_price', 'TaxRate': 'old_tax_rate', 'TaxMoney': 'old_tax_money', 'Amount': 'old_amount', 'Qty': 'old_qty', 'APDetailNo': 'old_apdetail_no', 'LotNo': 'old_lot_no', 'DlvQty': 'old_dlv_qty', 'Remarks': 'old_remarks', 'InDetailNo': 'old_in_detail_no', 'PhaseNo': 'old_phase_no', 'PhaseID': 'old_phase_id', 'StuffNo': 'old_stuff_no'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_pur_detail_no': 'Chinese_PRC_CI_AS', 'old_stuff_id': 'Chinese_PRC_CI_AS', 'old_apdetail_no': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_in_detail_no': 'Chinese_PRC_CI_AS', 'old_phase_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：StuffOut', 'target': 'erp_warehouse.SourceDyeStuffOut', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 StuffOutDetail → StuffOut', '原界面主从 DStuffOutDetail → DStuffOut', '原界面主从 SmallStuffOutDetail → SmallStuffOut']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('表单明细号（子表）', null=False, blank=True, max_length=36)
    old_pur_detail_no=models.CharField('采购单明细号', null=True, blank=True, max_length=20)
    old_stuff_id=models.CharField('染化料代码', null=True, blank=True, max_length=10)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=16, decimal_places=6)
    old_tax_price=models.DecimalField('含税价', null=True, blank=True, max_digits=16, decimal_places=6)
    old_tax_rate=models.DecimalField('税率', null=True, blank=True, max_digits=16, decimal_places=6)
    old_tax_money=models.DecimalField('税金', null=True, blank=True, max_digits=16, decimal_places=2)
    old_amount=models.DecimalField('金额', null=True, blank=True, max_digits=16, decimal_places=2)
    old_qty=models.DecimalField('数量', null=True, blank=True, max_digits=15, decimal_places=6)
    old_apdetail_no=models.CharField('应付单细号', null=True, blank=True, max_length=20)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=200)
    old_dlv_qty=models.DecimalField('交货数量', null=True, blank=True, max_digits=12, decimal_places=6)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_in_detail_no=models.CharField('InDetailNo', null=True, blank=True, max_length=50)
    old_phase_no=models.IntegerField('染程号', null=True, blank=True)
    old_phase_id=models.CharField('染程', null=True, blank=True, max_length=50)
    old_stuff_no=models.IntegerField('序号', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeStuffOut', verbose_name='原关系：StuffOut', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_stuffoutdetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_7ba01b78c129dfeb'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_7ba01b78c129dfeb')]
        verbose_name=verbose_name_plural='染化料出库明细'
        ordering=["-id"]

class SourceDyeStuffStock(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StuffStock'
    SOURCE_FIELDS={'StockDate': 'old_stock_date', 'StuffID': 'old_stuff_id', 'WareHouseID': 'old_ware_house_id', 'PreMonthQty': 'old_pre_month_qty', 'Price': 'old_price', 'PreMonthMoney': 'old_pre_month_money', 'CarryDate': 'old_carry_date', 'Remarks': 'old_remarks', 'LotNo': 'old_lot_no', 'LastStockQty': 'old_last_stock_qty', 'LastStockMoney': 'old_last_stock_money', 'InQty': 'old_in_qty', 'InMoney': 'old_in_money', 'OutQty': 'old_out_qty', 'OutMoney': 'old_out_money', 'InDetailNo': 'old_in_detail_no'}
    SOURCE_KEY=('StockDate', 'StuffID', 'WareHouseID', 'InDetailNo')
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_stuff_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_in_detail_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_in_detail_no': ('literal', '')}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_stock_date=models.DateTimeField('StockDate', null=False, blank=False)
    old_stuff_id=models.CharField('StuffID', null=False, blank=True, max_length=10)
    old_ware_house_id=models.CharField('WareHouseID', null=False, blank=True, max_length=10)
    old_pre_month_qty=models.DecimalField('PreMonthQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=10, decimal_places=4)
    old_pre_month_money=models.DecimalField('PreMonthMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_carry_date=models.DateTimeField('CarryDate', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_lot_no=models.CharField('LotNo', null=True, blank=True, max_length=50)
    old_last_stock_qty=models.DecimalField('LastStockQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_last_stock_money=models.DecimalField('LastStockMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_in_qty=models.DecimalField('InQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_in_money=models.DecimalField('InMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_out_qty=models.DecimalField('OutQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_out_money=models.DecimalField('OutMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_in_detail_no=models.CharField('InDetailNo', null=False, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_stuffstock'
        indexes=[models.Index(fields=['source_batch', 'old_stock_date', 'old_stuff_id', 'old_ware_house_id', 'old_in_detail_no'],name='src_f91f3941ab7db2e5'),models.Index(models.F('source_batch'),models.F('old_stock_date'),Upper(RTrim(models.F('old_stuff_id'))),Upper(RTrim(models.F('old_ware_house_id'))),Upper(RTrim(models.F('old_in_detail_no'))),name='src_ci_f91f3941ab7db2e5')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（StuffStock，待确认）'
        ordering=["-id"]

class SourceDyeStuffStockAdjust(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StuffStockAdjust'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'WareHouseID': 'old_ware_house_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'BusinessUnitID': 'old_business_unit_id'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_business_unit_id': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_ware_house_id=models.CharField('仓库代码', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_step_no=models.IntegerField('流程节点号', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_stuffstockadjust'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_effccab581e835bf'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_effccab581e835bf')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（StuffStockAdjust，待确认）'
        ordering=["-id"]

class SourceDyeStuffStockAdjustDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StuffStockAdjustDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'StuffID': 'old_stuff_id', 'LotNo': 'old_lot_no', 'PaperQty': 'old_paper_qty', 'RealQty': 'old_real_qty', 'AdjustQty': 'old_adjust_qty', 'Price': 'old_price', 'Remarks': 'old_remarks', 'PaperMoney': 'old_paper_money', 'RealMoney': 'old_real_money', 'AdjustMoney': 'old_adjust_money', 'InDetailNo': 'old_in_detail_no'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_stuff_id': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_in_detail_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：StuffStockAdjust', 'target': 'erp_warehouse.SourceDyeStuffStockAdjust', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 StuffStockAdjustDetail → StuffStockAdjust']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('关联单号', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('表单明细号', null=False, blank=True, max_length=36)
    old_stuff_id=models.CharField('染化料编码', null=True, blank=True, max_length=10)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=200)
    old_paper_qty=models.DecimalField('账面数量', null=True, blank=True, max_digits=12, decimal_places=6)
    old_real_qty=models.DecimalField('实际数量', null=True, blank=True, max_digits=12, decimal_places=6)
    old_adjust_qty=models.DecimalField('调整数量', null=True, blank=True, max_digits=12, decimal_places=6)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=8, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_paper_money=models.DecimalField('账面金额', null=True, blank=True, max_digits=14, decimal_places=6)
    old_real_money=models.DecimalField('实际金额', null=True, blank=True, max_digits=14, decimal_places=6)
    old_adjust_money=models.DecimalField('调整金额', null=True, blank=True, max_digits=14, decimal_places=6)
    old_in_detail_no=models.CharField('入库明细单号', null=True, blank=True, max_length=50)
    source_parent_1=models.ForeignKey('erp_warehouse.SourceDyeStuffStockAdjust', verbose_name='原关系：StuffStockAdjust', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_stuffstockadjustdetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_4c93d36157442b92'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_4c93d36157442b92')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（StuffStockAdjustDetail，待确认）'
        ordering=["-id"]

class SourceDyeStuffStockBook(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StuffStockBook'
    SOURCE_FIELDS={'BookNo': 'old_book_no', 'BookDate': 'old_book_date', 'AccDate': 'old_acc_date', 'BookKind': 'old_book_kind', 'SupplierID': 'old_supplier_id', 'WareHouseID': 'old_ware_house_id', 'StuffID': 'old_stuff_id', 'StorageUnitIDs': 'old_storage_unit_ids', 'SheetNo': 'old_sheet_no', 'DetailNo': 'old_detail_no', 'InQty': 'old_in_qty', 'OutQty': 'old_out_qty', 'Price': 'old_price', 'Remarks': 'old_remarks', 'DeptID': 'old_dept_id', 'LotNo': 'old_lot_no', 'SheetSeries': 'old_sheet_series', 'StockFlag': 'old_stock_flag', 'InMoney': 'old_in_money', 'OutMoney': 'old_out_money', 'CurrDate': 'old_curr_date', 'InDetailNo': 'old_in_detail_no'}
    SOURCE_KEY=('BookNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_supplier_id': 'Chinese_PRC_CI_AS', 'old_ware_house_id': 'Chinese_PRC_CI_AS', 'old_stuff_id': 'Chinese_PRC_CI_AS', 'old_storage_unit_ids': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_dept_id': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_stock_flag': 'Chinese_PRC_CI_AS', 'old_in_detail_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=('old_book_no',)
    SOURCE_IDENTITY_RULES={'old_book_no': (1, 1)}
    old_book_no=models.BigIntegerField('BookNo', null=False, blank=False)
    old_book_date=models.DateTimeField('BookDate', null=True, blank=True)
    old_acc_date=models.DateTimeField('AccDate', null=True, blank=True)
    old_book_kind=models.IntegerField('BookKind', null=True, blank=True)
    old_supplier_id=models.CharField('SupplierID', null=True, blank=True, max_length=10)
    old_ware_house_id=models.CharField('WareHouseID', null=True, blank=True, max_length=10)
    old_stuff_id=models.CharField('StuffID', null=True, blank=True, max_length=10)
    old_storage_unit_ids=models.CharField('StorageUnitIDs', null=True, blank=True, max_length=100)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=True, blank=True, max_length=36)
    old_in_qty=models.DecimalField('InQty', null=True, blank=True, max_digits=12, decimal_places=6)
    old_out_qty=models.DecimalField('OutQty', null=True, blank=True, max_digits=15, decimal_places=6)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=14, decimal_places=4)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_dept_id=models.CharField('DeptID', null=True, blank=True, max_length=10)
    old_lot_no=models.CharField('LotNo', null=True, blank=True, max_length=200)
    old_sheet_series=models.CharField('SheetSeries', null=True, blank=True, max_length=20)
    old_stock_flag=models.CharField('StockFlag', null=True, blank=True, max_length=1)
    old_in_money=models.DecimalField('InMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_out_money=models.DecimalField('OutMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_curr_date=models.DateTimeField('CurrDate', null=True, blank=True)
    old_in_detail_no=models.CharField('InDetailNo', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_stuffstockbook'
        indexes=[models.Index(fields=['source_batch', 'old_book_no'],name='src_dce9eacf2906eecf')]
        verbose_name=verbose_name_plural='染化料库存流水'
        ordering=["-id"]

class SourceDyeSwipeLabelPrint(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SwipeLabelPrint'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'JobSheetNo': 'old_job_sheet_no', 'MachineID': 'old_machine_id', 'GradeID': 'old_grade_id', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'RightStatus': 'old_right_status', 'RptID': 'old_rpt_id', 'PrintNumber': 'old_print_number', 'PrintCount': 'old_print_count', 'CheckNo': 'old_check_no', 'CustColorNum': 'old_cust_color_num', 'CustSelfNo': 'old_cust_self_no', 'ProdIDName': 'old_prod_idname', 'LotNo': 'old_lot_no', 'PreField1': 'old_pre_field1', 'CustSelfProduct': 'old_cust_self_product', 'ColorID': 'old_color_id', 'CustomerRemarks': 'old_customer_remarks', 'EmpID': 'old_emp_id', 'ColorNum': 'old_color_num', 'CustJobNo': 'old_cust_job_no'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_machine_id': 'Chinese_PRC_CI_AS', 'old_grade_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_rpt_id': 'Chinese_PRC_CI_AS', 'old_check_no': 'Chinese_PRC_CI_AS', 'old_cust_color_num': 'Chinese_PRC_CI_AS', 'old_cust_self_no': 'Chinese_PRC_CI_AS', 'old_prod_idname': 'Chinese_PRC_CI_AS', 'old_lot_no': 'Chinese_PRC_CI_AS', 'old_pre_field1': 'Chinese_PRC_CI_AS', 'old_cust_self_product': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_customer_remarks': 'Chinese_PRC_CI_AS', 'old_emp_id': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_cust_job_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=50)
    old_sheet_no=models.CharField('制单单号', null=True, blank=True, max_length=50)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_machine_id=models.CharField('机台', null=True, blank=True, max_length=20)
    old_grade_id=models.CharField('等级', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=500)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=10)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_rpt_id=models.CharField('报表菜单', null=True, blank=True, max_length=20)
    old_print_number=models.IntegerField('打印份数', null=True, blank=True)
    old_print_count=models.IntegerField('打印次数', null=True, blank=True)
    old_check_no=models.CharField('订单明细', null=True, blank=True, max_length=50)
    old_cust_color_num=models.CharField('客户色号', null=True, blank=True, max_length=150)
    old_cust_self_no=models.CharField('制单', null=True, blank=True, max_length=150)
    old_prod_idname=models.CharField('本厂规格', null=True, blank=True, max_length=150)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=150)
    old_pre_field1=models.CharField('捻度', null=True, blank=True, max_length=150)
    old_cust_self_product=models.CharField('客户规格', null=True, blank=True, max_length=150)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=150)
    old_customer_remarks=models.CharField('客户备注', null=True, blank=True, max_length=150)
    old_emp_id=models.CharField('员工编号', null=True, blank=True, max_length=150)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=150)
    old_cust_job_no=models.CharField('CustJobNo', null=True, blank=True, max_length=150)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_swipelabelprint'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_6dff9c7cbce9ac04'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_6dff9c7cbce9ac04')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（SwipeLabelPrint，待确认）'
        ordering=["-id"]

class SourceDyeUrgentInStruct(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='UrgentInStruct'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'SheetStatus': 'old_sheet_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'RightStatus': 'old_right_status', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'CustomerID': 'old_customer_id', 'DlvAddress': 'old_dlv_address', 'CarNo': 'old_car_no', 'Driver': 'old_driver'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_approver': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_dlv_address': 'Chinese_PRC_CI_AS', 'old_car_no': 'Chinese_PRC_CI_AS', 'old_driver': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=50)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=36)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_sheet_kind=models.IntegerField('SheetKind', null=True, blank=True)
    old_sheet_status=models.IntegerField('SheetStatus', null=True, blank=True)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_print_times=models.IntegerField('PrintTimes', null=True, blank=True)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_revisions=models.IntegerField('Revisions', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=50)
    old_dlv_address=models.CharField('DlvAddress', null=True, blank=True, max_length=200)
    old_car_no=models.CharField('CarNo', null=True, blank=True, max_length=50)
    old_driver=models.CharField('Driver', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_urgentinstruct'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_d375f108f1991c37'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_d375f108f1991c37')]
        verbose_name=verbose_name_plural='其他或待确认相关表（UrgentInStruct，待确认）'
        ordering=["-id"]

class SourceDyeUrgentInStructDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='UrgentInStructDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'JobSheetNo': 'old_job_sheet_no', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'Rolls': 'old_rolls', 'LengthQty': 'old_length_qty', 'WeightQty': 'old_weight_qty', 'StockUnit': 'old_stock_unit', 'ContractNo': 'old_contract_no', 'Spec': 'old_spec', 'Structure': 'old_structure', 'SalerID': 'old_saler_id', 'Remarks': 'old_remarks', 'CustSelfProduct': 'old_cust_self_product', 'CustSelfNo': 'old_cust_self_no', 'OrderSheetNo': 'old_order_sheet_no', 'ColorNum': 'old_color_num', 'ColorID': 'old_color_id', 'CustColorNum': 'old_cust_color_num', 'Weight': 'old_weight', 'Width': 'old_width', 'DetailCustName': 'old_detail_cust_name', 'OrderSheetDate': 'old_order_sheet_date', 'CurrProcessID': 'old_curr_process_id', 'CustJobNo': 'old_cust_job_no', 'Jobattes1': 'old_jobattes1', 'RealLotNo': 'old_real_lot_no'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer_id': 'Chinese_PRC_CI_AS', 'old_prod_id': 'Chinese_PRC_CI_AS', 'old_stock_unit': 'Chinese_PRC_CI_AS', 'old_contract_no': 'Chinese_PRC_CI_AS', 'old_spec': 'Chinese_PRC_CI_AS', 'old_structure': 'Chinese_PRC_CI_AS', 'old_saler_id': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS', 'old_cust_self_product': 'Chinese_PRC_CI_AS', 'old_cust_self_no': 'Chinese_PRC_CI_AS', 'old_order_sheet_no': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_cust_color_num': 'Chinese_PRC_CI_AS', 'old_weight': 'Chinese_PRC_CI_AS', 'old_width': 'Chinese_PRC_CI_AS', 'old_detail_cust_name': 'Chinese_PRC_CI_AS', 'old_curr_process_id': 'Chinese_PRC_CI_AS', 'old_cust_job_no': 'Chinese_PRC_CI_AS', 'old_jobattes1': 'Chinese_PRC_CI_AS', 'old_real_lot_no': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('SheetSeries', null=True, blank=True, max_length=50)
    old_detail_no=models.CharField('DetailNo', null=False, blank=True, max_length=36)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=50)
    old_prod_id=models.CharField('ProdID', null=True, blank=True, max_length=50)
    old_rolls=models.DecimalField('Rolls', null=True, blank=True, max_digits=10, decimal_places=2)
    old_length_qty=models.DecimalField('LengthQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight_qty=models.DecimalField('WeightQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_stock_unit=models.CharField('StockUnit', null=True, blank=True, max_length=50)
    old_contract_no=models.CharField('ContractNo', null=True, blank=True, max_length=20)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=200)
    old_structure=models.CharField('Structure', null=True, blank=True, max_length=200)
    old_saler_id=models.CharField('SalerID', null=True, blank=True, max_length=10)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_cust_self_product=models.CharField('CustSelfProduct', null=True, blank=True, max_length=250)
    old_cust_self_no=models.CharField('CustSelfNo', null=True, blank=True, max_length=50)
    old_order_sheet_no=models.CharField('OrderSheetNo', null=True, blank=True, max_length=50)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=50)
    old_cust_color_num=models.CharField('CustColorNum', null=True, blank=True, max_length=50)
    old_weight=models.CharField('Weight', null=True, blank=True, max_length=50)
    old_width=models.CharField('Width', null=True, blank=True, max_length=50)
    old_detail_cust_name=models.CharField('DetailCustName', null=True, blank=True, max_length=50)
    old_order_sheet_date=models.DateTimeField('OrderSheetDate', null=True, blank=True)
    old_curr_process_id=models.CharField('CurrProcessID', null=True, blank=True, max_length=50)
    old_cust_job_no=models.CharField('CustJobNo', null=True, blank=True, max_length=50)
    old_jobattes1=models.CharField('Jobattes1', null=True, blank=True, max_length=100)
    old_real_lot_no=models.CharField('RealLotNo', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_urgentinstructdetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_f7fd9fdb19baae4d'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_f7fd9fdb19baae4d')]
        verbose_name=verbose_name_plural='其他或待确认相关表（UrgentInStructDetail，待确认）'
        ordering=["-id"]

class SourceDyeWareHouseProdCount(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='WareHouseProdCount'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetDate': 'old_sheet_date', 'SheetNo': 'old_sheet_no', 'SheetKind': 'old_sheet_kind', 'JobSheetNo': 'old_job_sheet_no', 'Customer': 'old_customer', 'ColorNum': 'old_color_num', 'ColorID': 'old_color_id', 'Rolls': 'old_rolls', 'WeightQty': 'old_weight_qty', 'Cargador1': 'old_cargador1', 'Cargador2': 'old_cargador2', 'Cargador3': 'old_cargador3', 'Cargador4': 'old_cargador4', 'Cargador5': 'old_cargador5', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_sheet_no': 'Chinese_PRC_CI_AS', 'old_job_sheet_no': 'Chinese_PRC_CI_AS', 'old_customer': 'Chinese_PRC_CI_AS', 'old_color_num': 'Chinese_PRC_CI_AS', 'old_color_id': 'Chinese_PRC_CI_AS', 'old_cargador1': 'Chinese_PRC_CI_AS', 'old_cargador2': 'Chinese_PRC_CI_AS', 'old_cargador3': 'Chinese_PRC_CI_AS', 'old_cargador4': 'Chinese_PRC_CI_AS', 'old_cargador5': 'Chinese_PRC_CI_AS', 'old_remarks': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_kind=models.IntegerField('单据类别', null=True, blank=True)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_customer=models.CharField('客户', null=True, blank=True, max_length=10)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=20)
    old_color_id=models.CharField('颜色编码', null=True, blank=True, max_length=150)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_weight_qty=models.DecimalField('重量数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_cargador1=models.CharField('装/配工', null=True, blank=True, max_length=10)
    old_cargador2=models.CharField('装/配工', null=True, blank=True, max_length=10)
    old_cargador3=models.CharField('装/配工', null=True, blank=True, max_length=10)
    old_cargador4=models.CharField('装/配工', null=True, blank=True, max_length=10)
    old_cargador5=models.CharField('装/配工', null=True, blank=True, max_length=10)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_warehouseprodcount'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_1001583a311f9752'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),name='src_ci_1001583a311f9752')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（WareHouseProdCount，待确认）'
        ordering=["-id"]

class SourceDyeWeightTechInfo(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='WeightTechInfo'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'Tech': 'old_tech', 'ParameterNo': 'old_parameter_no', 'ParameterID': 'old_parameter_id', 'ParameterName': 'old_parameter_name', 'ParameterValue': 'old_parameter_value', 'ProgId': 'old_prog_id'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_sheet_series': 'Chinese_PRC_CI_AS', 'old_detail_no': 'Chinese_PRC_CI_AS', 'old_tech': 'Chinese_PRC_CI_AS', 'old_parameter_no': 'Chinese_PRC_CI_AS', 'old_parameter_id': 'Chinese_PRC_CI_AS', 'old_parameter_name': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=False, blank=True, max_length=30)
    old_tech=models.CharField('Tech', null=True, blank=True, max_length=50)
    old_parameter_no=models.CharField('ParameterNo', null=True, blank=True, max_length=10)
    old_parameter_id=models.CharField('ParameterID', null=True, blank=True, max_length=20)
    old_parameter_name=models.CharField('ParameterName', null=True, blank=True, max_length=50)
    old_parameter_value=models.DecimalField('ParameterValue', null=True, blank=True, max_digits=10, decimal_places=2)
    old_prog_id=models.IntegerField('ProgId', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_weighttechinfo'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_692c9debdd8328ef'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_692c9debdd8328ef')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（WeightTechInfo，待确认）'
        ordering=["-id"]

class SourceDyeWidthGramWeight(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='WidthGramWeight'
    SOURCE_FIELDS={'Code': 'old_code', 'NameC': 'old_name_c', 'NumValue': 'old_num_value', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Kind': 'old_kind'}
    SOURCE_KEY=('Code',)
    SOURCE_DOCUMENT=True
    SOURCE_COLLATIONS={'old_code': 'Chinese_PRC_CI_AS', 'old_name_c': 'Chinese_PRC_CI_AS', 'old_creater': 'Chinese_PRC_CI_AS', 'old_modifyer': 'Chinese_PRC_CI_AS', 'old_kind': 'Chinese_PRC_CI_AS'}
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    SOURCE_IDENTITY_RULES={}
    old_code=models.CharField('Code', null=False, blank=True, max_length=20)
    old_name_c=models.CharField('名称', null=True, blank=True, max_length=50)
    old_num_value=models.DecimalField('NumValue', null=True, blank=True, max_digits=18, decimal_places=2)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=50)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=50)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_kind=models.CharField('类型', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_widthgramweight'
        indexes=[models.Index(fields=['source_batch', 'old_code'],name='src_051a950ab92c566f'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_code'))),name='src_ci_051a950ab92c566f')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（WidthGramWeight，待确认）'
        ordering=["-id"]
