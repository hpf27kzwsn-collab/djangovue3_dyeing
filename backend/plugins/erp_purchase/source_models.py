"""静态旧业务字段；由tools/legacy_models生成，逐表来源见source_catalog.json。"""
from django.db import models
from plugins.erp_base.source_documents import SourceRecord


class SourceDyeArticlePurDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ArticlePurDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'ApplySheetNo': 'old_apply_sheet_no', 'SupplierID': 'old_supplier_id', 'ArticleKindID': 'old_article_kind_id', 'ArticleID': 'old_article_id', 'Unit': 'old_unit', 'Price': 'old_price', 'NeedQty': 'old_need_qty', 'Qty': 'old_qty', 'Amount': 'old_amount', 'UseID': 'old_use_id', 'DlvDate': 'old_dlv_date', 'Remarks': 'old_remarks', 'PackQty': 'old_pack_qty', 'PackUnit': 'old_pack_unit', 'FinishDate': 'old_finish_date'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=False, blank=True, max_length=36)
    old_apply_sheet_no=models.CharField('ApplySheetNo', null=True, blank=True, max_length=20)
    old_supplier_id=models.CharField('SupplierID', null=True, blank=True, max_length=10)
    old_article_kind_id=models.CharField('ArticleKindID', null=True, blank=True, max_length=20)
    old_article_id=models.CharField('ArticleID', null=True, blank=True, max_length=20)
    old_unit=models.CharField('Unit', null=True, blank=True, max_length=20)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=8, decimal_places=2)
    old_need_qty=models.DecimalField('NeedQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_qty=models.DecimalField('Qty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_amount=models.DecimalField('Amount', null=True, blank=True, max_digits=10, decimal_places=2)
    old_use_id=models.CharField('UseID', null=True, blank=True, max_length=10)
    old_dlv_date=models.DateTimeField('DlvDate', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_pack_qty=models.DecimalField('PackQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pack_unit=models.CharField('PackUnit', null=True, blank=True, max_length=10)
    old_finish_date=models.DateTimeField('FinishDate', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_articlepurdetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_0619be01baca9eb2')]
        verbose_name=verbose_name_plural='其他或待确认相关表（ArticlePurDetail，待确认）'
        ordering=["-id"]

class SourceDyeArticlePurMain(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ArticlePurMain'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'DeptID': 'old_dept_id', 'PurKindID': 'old_pur_kind_id', 'BusinessUnitID': 'old_business_unit_id', 'CurrencyID': 'old_currency_id', 'ExchangeRate': 'old_exchange_rate', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer', 'BuyerID': 'old_buyer_id', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_dept_id=models.CharField('部门编码', null=True, blank=True, max_length=10)
    old_pur_kind_id=models.CharField('采购类别代码', null=True, blank=True, max_length=10)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_currency_id=models.CharField('币别', null=True, blank=True, max_length=10)
    old_exchange_rate=models.DecimalField('汇率', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_step_no=models.IntegerField('流程节点号', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_buyer_id=models.CharField('采购员', null=True, blank=True, max_length=10)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_articlepurmain'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_766d301a58cae34d')]
        verbose_name=verbose_name_plural='其他或待确认相关表（ArticlePurMain，待确认）'
        ordering=["-id"]

class SourceDyeFabricPurDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='FabricPurDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'ApplySheetNo': 'old_apply_sheet_no', 'FabricID': 'old_fabric_id', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'Structure': 'old_structure', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'DesignNo': 'old_design_no', 'Price': 'old_price', 'PriceUnit': 'old_price_unit', 'Rolls': 'old_rolls', 'Qty': 'old_qty', 'Fee': 'old_fee', 'Amount': 'old_amount', 'DlvDate': 'old_dlv_date', 'CheckNo': 'old_check_no', 'OrderDn': 'old_order_dn', 'OrderUp': 'old_order_up', 'ToPlace': 'old_to_place', 'WeightDn': 'old_weight_dn', 'WeightUp': 'old_weight_up', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=False, blank=True, max_length=36)
    old_apply_sheet_no=models.CharField('ApplySheetNo', null=True, blank=True, max_length=20)
    old_fabric_id=models.CharField('FabricID', null=True, blank=True, max_length=128)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=128)
    old_lot_no=models.CharField('LotNo', null=True, blank=True, max_length=50)
    old_structure=models.CharField('Structure', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=20)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=20)
    old_design_no=models.CharField('DesignNo', null=True, blank=True, max_length=20)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=8, decimal_places=2)
    old_price_unit=models.IntegerField('PriceUnit', null=True, blank=True)
    old_rolls=models.DecimalField('Rolls', null=True, blank=True, max_digits=7, decimal_places=2)
    old_qty=models.DecimalField('Qty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_fee=models.DecimalField('Fee', null=True, blank=True, max_digits=10, decimal_places=2)
    old_amount=models.DecimalField('Amount', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dlv_date=models.DateTimeField('DlvDate', null=True, blank=True)
    old_check_no=models.CharField('CheckNo', null=True, blank=True, max_length=20)
    old_order_dn=models.IntegerField('OrderDn', null=True, blank=True)
    old_order_up=models.IntegerField('OrderUp', null=True, blank=True)
    old_to_place=models.CharField('ToPlace', null=True, blank=True, max_length=500)
    old_weight_dn=models.DecimalField('WeightDn', null=True, blank=True, max_digits=6, decimal_places=2)
    old_weight_up=models.DecimalField('WeightUp', null=True, blank=True, max_digits=6, decimal_places=2)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_fabricpurdetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_b3c81a863e6f4eea')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（FabricPurDetail，待确认）'
        ordering=["-id"]

class SourceDyeFabricPurMain(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='FabricPurMain'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'PurKindID': 'old_pur_kind_id', 'SupplierID': 'old_supplier_id', 'BuyerID': 'old_buyer_id', 'BusinessUnitID': 'old_business_unit_id', 'SalerGroupID': 'old_saler_group_id', 'ContractNo': 'old_contract_no', 'DlvMannerID': 'old_dlv_manner_id', 'SumAmount': 'old_sum_amount', 'SumFee': 'old_sum_fee', 'SettleID': 'old_settle_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_sheet_kind=models.IntegerField('SheetKind', null=True, blank=True)
    old_pur_kind_id=models.CharField('PurKindID', null=True, blank=True, max_length=10)
    old_supplier_id=models.CharField('SupplierID', null=True, blank=True, max_length=10)
    old_buyer_id=models.CharField('BuyerID', null=True, blank=True, max_length=10)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('SalerGroupID', null=True, blank=True, max_length=10)
    old_contract_no=models.CharField('ContractNo', null=True, blank=True, max_length=20)
    old_dlv_manner_id=models.CharField('DlvMannerID', null=True, blank=True, max_length=10)
    old_sum_amount=models.DecimalField('SumAmount', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sum_fee=models.DecimalField('SumFee', null=True, blank=True, max_digits=10, decimal_places=2)
    old_settle_id=models.CharField('SettleID', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('SheetStatus', null=True, blank=True)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_print_times=models.IntegerField('PrintTimes', null=True, blank=True)
    old_revisions=models.IntegerField('Revisions', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_fabricpurmain'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_f3eb2eb4b74c443c')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（FabricPurMain，待确认）'
        ordering=["-id"]

class SourceDyePurApplyDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PurApplyDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'OrderNo': 'old_order_no', 'FabricID': 'old_fabric_id', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'Structure': 'old_structure', 'FabricID2': 'old_fabric_id2', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'DesignNo': 'old_design_no', 'FirstDlvDate': 'old_first_dlv_date', 'GrayQty': 'old_gray_qty', 'RollAvgQty': 'old_roll_avg_qty', 'GrayPrice': 'old_gray_price', 'PriceUnit': 'old_price_unit', 'Amount': 'old_amount', 'GrayMoney': 'old_gray_money', 'GrayWeight': 'old_gray_weight', 'GrayWidth': 'old_gray_width', 'GrayDlvDate': 'old_gray_dlv_date', 'ProdQty': 'old_prod_qty', 'ProdDlvDate': 'old_prod_dlv_date', 'ProdWeight': 'old_prod_weight', 'ProdWidth': 'old_prod_width', 'Loss': 'old_loss', 'Remarks': 'old_remarks', 'GrayWeightDn': 'old_gray_weight_dn', 'GrayWidthDn': 'old_gray_width_dn', 'ProdWeightDn': 'old_prod_weight_dn', 'ProdWidthDn': 'old_prod_width_dn', 'ArticleID': 'old_article_id', 'ArticleName': 'old_article_name', 'ArticleKindID': 'old_article_kind_id', 'StuffID': 'old_stuff_id', 'StuffName': 'old_stuff_name', 'StuffKindID': 'old_stuff_kind_id', 'ArticleUnit': 'old_article_unit', 'StuffUnit': 'old_stuff_unit', 'Price': 'old_price', 'Qty': 'old_qty', 'remarks2': 'old_remarks2'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：PurApplyMain', 'target': 'erp_purchase.SourceDyePurApplyMain', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 ArticlePurApplyDetail → ArticlePurApplyMain', '原界面主从 StuffPurApplyDetail → StuffPurApplyMain', '原界面主从 PurApplyDetail → PurApplyMain']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('表单明细号（子表）', null=False, blank=True, max_length=20)
    old_order_no=models.CharField('订单号', null=True, blank=True, max_length=20)
    old_fabric_id=models.CharField('客户规格', null=True, blank=True, max_length=10)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=50)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=20)
    old_structure=models.CharField('组织', null=True, blank=True, max_length=50)
    old_fabric_id2=models.CharField('供应商胚纱编号', null=True, blank=True, max_length=10)
    old_color_id=models.CharField('颜色编码', null=True, blank=True, max_length=10)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=20)
    old_design_no=models.CharField('花号', null=True, blank=True, max_length=20)
    old_first_dlv_date=models.DateTimeField('头缸交期', null=True, blank=True)
    old_gray_qty=models.DecimalField('投胚数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_roll_avg_qty=models.DecimalField('平均粒长/粒重', null=True, blank=True, max_digits=10, decimal_places=2)
    old_gray_price=models.DecimalField('胚纱价格', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price_unit=models.IntegerField('计价单位编码', null=True, blank=True)
    old_amount=models.DecimalField('金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_gray_money=models.DecimalField('胚纱金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_gray_weight=models.DecimalField('胚纱克重', null=True, blank=True, max_digits=6, decimal_places=2)
    old_gray_width=models.DecimalField('胚纱门幅', null=True, blank=True, max_digits=6, decimal_places=2)
    old_gray_dlv_date=models.DateTimeField('胚纱交期', null=True, blank=True)
    old_prod_qty=models.DecimalField('成品数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_prod_dlv_date=models.DateTimeField('大货交期', null=True, blank=True)
    old_prod_weight=models.DecimalField('成品克重', null=True, blank=True, max_digits=6, decimal_places=2)
    old_prod_width=models.DecimalField('成品门幅', null=True, blank=True, max_digits=6, decimal_places=2)
    old_loss=models.DecimalField('数值缩率', null=True, blank=True, max_digits=4, decimal_places=1)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    old_gray_weight_dn=models.DecimalField('胚纱克重下限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_gray_width_dn=models.DecimalField('胚纱门幅下限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_prod_weight_dn=models.DecimalField('成品克重下限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_prod_width_dn=models.DecimalField('成品门幅下限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_article_id=models.CharField('物料编码', null=True, blank=True, max_length=20)
    old_article_name=models.CharField('物料名称', null=True, blank=True, max_length=20)
    old_article_kind_id=models.CharField('物料种类', null=True, blank=True, max_length=20)
    old_stuff_id=models.CharField('染化料编码', null=True, blank=True, max_length=20)
    old_stuff_name=models.CharField('染化料名称', null=True, blank=True, max_length=20)
    old_stuff_kind_id=models.CharField('染化料种类', null=True, blank=True, max_length=20)
    old_article_unit=models.CharField('物料单位', null=True, blank=True, max_length=20)
    old_stuff_unit=models.CharField('染化料单位', null=True, blank=True, max_length=20)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=10, decimal_places=2)
    old_qty=models.DecimalField('数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks2=models.CharField('remarks2', null=True, blank=True, max_length=255)
    source_parent_1=models.ForeignKey('erp_purchase.SourceDyePurApplyMain', verbose_name='原关系：PurApplyMain', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_purapplydetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_ee46cf712c70fdef')]
        verbose_name=verbose_name_plural='其他或待确认相关表（PurApplyDetail，待确认）'
        ordering=["-id"]

class SourceDyePurApplyMain(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PurApplyMain'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'PurKindID': 'old_pur_kind_id', 'SupplierID': 'old_supplier_id', 'BusinessUnitID': 'old_business_unit_id', 'SalerGroupID': 'old_saler_group_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'SalerID': 'old_saler_id', 'BuyerID': 'old_buyer_id', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer', 'StepNo': 'old_step_no', 'DeptID': 'old_dept_id', 'FactID': 'old_fact_id', 'DlvMannerID': 'old_dlv_manner_id', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'Applicant': 'old_applicant'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类别', null=True, blank=True)
    old_pur_kind_id=models.CharField('采购类别代码', null=True, blank=True, max_length=10)
    old_supplier_id=models.CharField('供应商代码', null=True, blank=True, max_length=10)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('业务组别', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_saler_id=models.CharField('业务员代码', null=True, blank=True, max_length=10)
    old_buyer_id=models.CharField('采购员', null=True, blank=True, max_length=10)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    old_create_date=models.DateTimeField('创建日期', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_step_no=models.IntegerField('工作流节点号', null=True, blank=True)
    old_dept_id=models.CharField('部门名称', null=True, blank=True, max_length=50)
    old_fact_id=models.CharField('所属分厂', null=True, blank=True, max_length=50)
    old_dlv_manner_id=models.CharField('交货方式', null=True, blank=True, max_length=200)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=50)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_applicant=models.CharField('申请人', null=True, blank=True, max_length=30)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_purapplymain'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_bb492a8c217d5b5f')]
        verbose_name=verbose_name_plural='其他或待确认相关表（PurApplyMain，待确认）'
        ordering=["-id"]

class SourceDyePurDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PurDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'ApplySheetNo': 'old_apply_sheet_no', 'FabricID': 'old_fabric_id', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'Structure': 'old_structure', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'DesignNo': 'old_design_no', 'Price': 'old_price', 'PriceUnit': 'old_price_unit', 'Rolls': 'old_rolls', 'Qty': 'old_qty', 'Fee': 'old_fee', 'Amount': 'old_amount', 'DlvDate': 'old_dlv_date', 'OrderDn': 'old_order_dn', 'OrderUp': 'old_order_up', 'ToPlace': 'old_to_place', 'WeightDn': 'old_weight_dn', 'WeightUp': 'old_weight_up', 'Remarks': 'old_remarks', 'CheckNo': 'old_check_no', 'ArticleID': 'old_article_id', 'ArticleName': 'old_article_name', 'ArticleKindID': 'old_article_kind_id', 'ArticleUnit': 'old_article_unit', 'StuffID': 'old_stuff_id', 'StuffName': 'old_stuff_name', 'StuffKindID': 'old_stuff_kind_id', 'StuffUnit': 'old_stuff_unit', 'GrayID': 'old_gray_id'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：ArticlePurMain', 'target': 'erp_purchase.SourceDyeArticlePurMain', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 ArticlePurDetail → ArticlePurMain']}, {'field': 'source_parent_2', 'title': '原关系：PurMain', 'target': 'erp_purchase.SourceDyePurMain', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 PurDetail → PurMain']}, {'field': 'source_parent_3', 'title': '原关系：StuffPurMain', 'target': 'erp_purchase.SourceDyeStuffPurMain', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 StuffPurDetail → StuffPurMain']}]
    SOURCE_DEFAULTS={'old_apply_sheet_no': ('literal', ''), 'old_fabric_id': ('literal', ''), 'old_spec': ('literal', ''), 'old_lot_no': ('literal', ''), 'old_structure': ('literal', ''), 'old_color_id': ('literal', ''), 'old_color_num': ('literal', ''), 'old_design_no': ('literal', ''), 'old_price': ('literal', 0), 'old_price_unit': ('literal', 0), 'old_rolls': ('literal', 0), 'old_qty': ('literal', 0), 'old_fee': ('literal', 0), 'old_amount': ('literal', 0), 'old_dlv_date': ('literal', '1900-01-01'), 'old_order_dn': ('literal', 0), 'old_order_up': ('literal', 0), 'old_to_place': ('literal', ''), 'old_weight_dn': ('literal', 0), 'old_weight_up': ('literal', 0), 'old_remarks': ('literal', '')}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('表单明细号（子表）', null=False, blank=True, max_length=20)
    old_apply_sheet_no=models.CharField('审购单号', null=True, blank=True, max_length=20)
    old_fabric_id=models.CharField('客户规格', null=True, blank=True, max_length=150)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=50)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=20)
    old_structure=models.CharField('组织', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=10)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=20)
    old_design_no=models.CharField('花稿号', null=True, blank=True, max_length=20)
    old_price=models.DecimalField('价格', null=True, blank=True, max_digits=8, decimal_places=4)
    old_price_unit=models.IntegerField('计价单位编码', null=True, blank=True)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_qty=models.DecimalField('数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_fee=models.DecimalField('费用', null=True, blank=True, max_digits=10, decimal_places=2)
    old_amount=models.DecimalField('金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dlv_date=models.DateTimeField('交货日期', null=True, blank=True)
    old_order_dn=models.IntegerField('订量下限', null=True, blank=True)
    old_order_up=models.IntegerField('订量上限', null=True, blank=True)
    old_to_place=models.CharField('交货地点', null=True, blank=True, max_length=50)
    old_weight_dn=models.DecimalField('克重下限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_weight_up=models.DecimalField('克重上限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_remarks=models.CharField('备注', null=False, blank=True, max_length=100)
    old_check_no=models.CharField('订单明细号', null=True, blank=True, max_length=20)
    old_article_id=models.CharField('物料编码', null=True, blank=True, max_length=50)
    old_article_name=models.CharField('物料名称', null=True, blank=True, max_length=50)
    old_article_kind_id=models.CharField('物料种类', null=True, blank=True, max_length=50)
    old_article_unit=models.CharField('ArticleUnit', null=True, blank=True, max_length=50)
    old_stuff_id=models.CharField('染化料编码', null=True, blank=True, max_length=50)
    old_stuff_name=models.CharField('染化料名称', null=True, blank=True, max_length=50)
    old_stuff_kind_id=models.CharField('染化料种类', null=True, blank=True, max_length=50)
    old_stuff_unit=models.CharField('染化料单位', null=True, blank=True, max_length=50)
    old_gray_id=models.CharField('本厂规格', null=True, blank=True, max_length=100)
    source_parent_1=models.ForeignKey('erp_purchase.SourceDyeArticlePurMain', verbose_name='原关系：ArticlePurMain', null=True, blank=True, on_delete=models.PROTECT, related_name='+')
    source_parent_2=models.ForeignKey('erp_purchase.SourceDyePurMain', verbose_name='原关系：PurMain', null=True, blank=True, on_delete=models.PROTECT, related_name='+')
    source_parent_3=models.ForeignKey('erp_purchase.SourceDyeStuffPurMain', verbose_name='原关系：StuffPurMain', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_purdetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_a2e0f9cfbd3300ac')]
        verbose_name=verbose_name_plural='其他或待确认相关表（PurDetail，待确认）'
        ordering=["-id"]

class SourceDyePurMain(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PurMain'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'PurKindID': 'old_pur_kind_id', 'SupplierID': 'old_supplier_id', 'Factory': 'old_factory', 'BusinessUnitID': 'old_business_unit_id', 'SalerGroupID': 'old_saler_group_id', 'BuyerID': 'old_buyer_id', 'ContractNo': 'old_contract_no', 'OrderNo': 'old_order_no', 'DlvDate': 'old_dlv_date', 'DlvMannerID': 'old_dlv_manner_id', 'SumAmount': 'old_sum_amount', 'SumFee': 'old_sum_fee', 'SettleID': 'old_settle_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer', 'StepNo': 'old_step_no'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_sheet_no': ('literal', ''), 'old_sheet_date': ('literal', '1900-01-01'), 'old_sheet_kind': ('literal', 0), 'old_pur_kind_id': ('literal', ''), 'old_supplier_id': ('literal', ''), 'old_business_unit_id': ('literal', ''), 'old_saler_group_id': ('literal', ''), 'old_buyer_id': ('literal', ''), 'old_contract_no': ('literal', ''), 'old_order_no': ('literal', ''), 'old_dlv_date': ('literal', '1900-01-01'), 'old_dlv_manner_id': ('literal', ''), 'old_sum_amount': ('literal', 0), 'old_sum_fee': ('literal', 0), 'old_settle_id': ('literal', ''), 'old_sheet_status': ('literal', ''), 'old_right_status': ('literal', 0), 'old_print_times': ('literal', 0), 'old_revisions': ('literal', 0), 'old_remarks': ('literal', ''), 'old_create_date': ('literal', '1900-01-01'), 'old_creater': ('literal', ''), 'old_modify_date': ('literal', '1900-01-01'), 'old_modifyer': ('literal', '')}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=False, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类别', null=True, blank=True)
    old_pur_kind_id=models.CharField('采购类别代码', null=True, blank=True, max_length=10)
    old_supplier_id=models.CharField('供应商', null=True, blank=True, max_length=10)
    old_factory=models.CharField('加工厂', null=True, blank=True, max_length=50)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('业务组别', null=True, blank=True, max_length=10)
    old_buyer_id=models.CharField('采购员', null=True, blank=True, max_length=10)
    old_contract_no=models.CharField('客户单号', null=True, blank=True, max_length=20)
    old_order_no=models.CharField('订单号', null=True, blank=True, max_length=20)
    old_dlv_date=models.DateTimeField('交货日期', null=True, blank=True)
    old_dlv_manner_id=models.CharField('交货方式编码', null=True, blank=True, max_length=10)
    old_sum_amount=models.DecimalField('总金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sum_fee=models.DecimalField('总费用', null=True, blank=True, max_digits=10, decimal_places=2)
    old_settle_id=models.CharField('结算方式', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_step_no=models.IntegerField('工作流节点号', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_purmain'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_97ad8b8806d8a544')]
        verbose_name=verbose_name_plural='其他或待确认相关表（PurMain，待确认）'
        ordering=["-id"]

class SourceDyeStuffPurDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StuffPurDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'ApplySheetNo': 'old_apply_sheet_no', 'SupplierID': 'old_supplier_id', 'StuffID': 'old_stuff_id', 'LotNo': 'old_lot_no', 'Price': 'old_price', 'NeedQty': 'old_need_qty', 'Qty': 'old_qty', 'Amount': 'old_amount', 'PackQty': 'old_pack_qty', 'PackUnit': 'old_pack_unit', 'DlvDate': 'old_dlv_date', 'FinishDate': 'old_finish_date', 'Remarks': 'old_remarks', 'PriceUnit': 'old_price_unit'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=False, blank=True, max_length=36)
    old_apply_sheet_no=models.CharField('ApplySheetNo', null=True, blank=True, max_length=20)
    old_supplier_id=models.CharField('SupplierID', null=True, blank=True, max_length=10)
    old_stuff_id=models.CharField('StuffID', null=True, blank=True, max_length=10)
    old_lot_no=models.CharField('LotNo', null=True, blank=True, max_length=50)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=8, decimal_places=2)
    old_need_qty=models.DecimalField('NeedQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_qty=models.DecimalField('Qty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_amount=models.DecimalField('Amount', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pack_qty=models.DecimalField('PackQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pack_unit=models.CharField('PackUnit', null=True, blank=True, max_length=10)
    old_dlv_date=models.DateTimeField('DlvDate', null=True, blank=True)
    old_finish_date=models.DateTimeField('FinishDate', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_price_unit=models.IntegerField('PriceUnit', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_stuffpurdetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_cd2d1814200a2526')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（StuffPurDetail，待确认）'
        ordering=["-id"]

class SourceDyeStuffPurMain(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StuffPurMain'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'DeptID': 'old_dept_id', 'SheetKind': 'old_sheet_kind', 'PurKindID': 'old_pur_kind_id', 'BuyerID': 'old_buyer_id', 'BusinessUnitID': 'old_business_unit_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_dept_id=models.CharField('部门编码', null=True, blank=True, max_length=10)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_pur_kind_id=models.CharField('采购类别代码', null=True, blank=True, max_length=10)
    old_buyer_id=models.CharField('采购员', null=True, blank=True, max_length=10)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_step_no=models.IntegerField('流程节点号', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_stuffpurmain'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_10e8c7ea572251f7')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（StuffPurMain，待确认）'
        ordering=["-id"]
