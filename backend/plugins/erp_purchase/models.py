"""采购管理模型；字段来源见 docs/ERP模型实施说明.md。"""
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q
from plugins.erp_base.models import ErpModel
from plugins.erp_base import choices


class PurchaseRequest(ErpModel):
    """采购申请。"""

    # 原物理来源：PurApplyMain.SheetNo
    number = models.CharField(
        '表单编号',
        max_length=20,
        unique=True,
    )

    # 原物理来源：PurApplyMain.SheetDate
    document_at = models.DateTimeField(
        '单据日期',
    )

    # 原物理来源：PurApplyMain.Applicant
    applicant = models.ForeignKey(
        'erp_base.Employee',
        verbose_name='申请人',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_applicant_set",
        blank=True,
        null=True,
    )

    # 原物理来源：PurApplyMain.DeptID
    department = models.ForeignKey(
        'system.Dept',
        verbose_name='申请部门',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_department_set",
        blank=True,
        null=True,
    )

    # 原物理来源：PurApplyMain.FactID
    factory = models.ForeignKey(
        'erp_base.Factory',
        verbose_name='需求工厂',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_factory_set",
        blank=True,
        null=True,
    )

    # 原物理来源：PurApplyMain.PurKindID
    purchase_kind = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='采购类别',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_purchase_kind_set",
        blank=True,
        null=True,
    )

    # 原物理来源：PurApplyMain.SheetStatus
    status = models.CharField(
        '申请状态',
        max_length=24,
        choices=choices.PurchaseRequestStatus.choices,
        default=choices.PurchaseRequestStatus.DRAFT,
    )

    # 原物理来源：PurApplyMain.Approver
    confirmed_by = models.ForeignKey(
        'erp_base.Employee',
        verbose_name='确认人',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_confirmed_by_set",
        blank=True,
        null=True,
    )

    # 原物理来源：PurApplyMain.ApproveDate
    confirmed_at = models.DateTimeField(
        '确认时间',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_purchase_purchaserequest"
        verbose_name = '采购申请'
        verbose_name_plural = '采购申请'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(status__in=choices.PurchaseRequestStatus.values), name='erp_purchase_purchaserequest_status_valid'),
        ]
        indexes = [
            models.Index(fields=['status', 'document_at'], name='pur_purchaserequest_1'),
        ]


class PurchaseRequestLine(ErpModel):
    """采购申请明细。"""

    request = models.ForeignKey(
        'erp_purchase.PurchaseRequest',
        verbose_name='采购申请',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_request_set",
    )

    line_number = models.IntegerField(
        '行号',
    )

    material = models.ForeignKey(
        'erp_base.Material',
        verbose_name='物料',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_material_set",
    )

    quantity = models.DecimalField(
        '申请量',
        max_digits=20,
        decimal_places=6,
    )

    unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='申请单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_unit_set",
    )

    required_at = models.DateTimeField(
        '要求到货时间',
        blank=True,
        null=True,
    )

    order_line = models.ForeignKey(
        'erp_sales.SalesOrderLine',
        verbose_name='销售订单需求',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_order_line_set",
        blank=True,
        null=True,
    )

    work_card = models.ForeignKey(
        'erp_production.WorkCard',
        verbose_name='生产任务需求',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_work_card_set",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_purchase_purchaserequestline"
        verbose_name = '采购申请明细'
        verbose_name_plural = '采购申请明细'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['request', 'line_number'], name='erp_purchase_purchaserequestline_identity_uniq'),
            models.CheckConstraint(condition=Q(line_number__gt=0), name='erp_purchase_purchaserequestline_line_number_positive'),
            models.CheckConstraint(condition=Q(quantity__gt=0), name='erp_purchase_purchaserequestline_quantity_positive'),
        ]


class PurchaseOrder(ErpModel):
    """采购订单。"""

    # 原物理来源：PurMain.SheetNo
    number = models.CharField(
        '表单编号',
        max_length=20,
        unique=True,
    )

    # 原物理来源：PurMain.SheetDate
    document_at = models.DateTimeField(
        '单据日期',
    )

    # 原物理来源：PurMain.SupplierID
    supplier = models.ForeignKey(
        'erp_base.Party',
        verbose_name='供应商',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_supplier_set",
    )

    # 原物理来源：PurMain.BuyerID
    buyer = models.ForeignKey(
        'erp_base.Employee',
        verbose_name='采购员',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_buyer_set",
        blank=True,
        null=True,
    )

    # 原物理来源：PurMain.BusinessUnitID
    business_unit = models.ForeignKey(
        'erp_base.BusinessUnit',
        verbose_name='经营单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_business_unit_set",
        blank=True,
        null=True,
    )

    # 原物理来源：PurMain.PurKindID
    purchase_kind = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='采购类别',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_purchase_kind_set",
        blank=True,
        null=True,
    )

    # 原物理来源：PurMain.ContractNo
    supplier_contract_number = models.CharField(
        '合同号',
        max_length=20,
        blank=True,
        null=True,
    )

    # 原物理来源：PurMain.DlvDate
    due_at = models.DateTimeField(
        '交货日期',
        blank=True,
        null=True,
    )

    # 原物理来源：PurMain.SheetStatus
    status = models.CharField(
        '采购状态',
        max_length=24,
        choices=choices.PurchaseStatus.choices,
        default=choices.PurchaseStatus.DRAFT,
    )

    class Meta:
        db_table = "erp_purchase_purchaseorder"
        verbose_name = '采购订单'
        verbose_name_plural = '采购订单'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(status__in=choices.PurchaseStatus.values), name='erp_purchase_purchaseorder_status_valid'),
        ]
        indexes = [
            models.Index(fields=['status', 'document_at'], name='pur_purchaseorder_1'),
        ]


class PurchaseOrderLine(ErpModel):
    """采购订单明细。"""

    # 原物理来源：PurDetail.SheetSeries
    order = models.ForeignKey(
        'erp_purchase.PurchaseOrder',
        verbose_name='采购订单',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_order_set",
    )

    line_number = models.IntegerField(
        '行号',
    )

    # 原物理来源：PurDetail.ApplySheetNo
    request_line = models.ForeignKey(
        'erp_purchase.PurchaseRequestLine',
        verbose_name='申请明细',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_request_line_set",
        blank=True,
        null=True,
    )

    # 原物理来源：PurDetail.GrayID; PurDetail.StuffID; PurDetail.ArticleID
    material = models.ForeignKey(
        'erp_base.Material',
        verbose_name='物料',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_material_set",
    )

    # 原物理来源：PurDetail.FabricID
    supplier_specification = models.CharField(
        '供应商规格',
        max_length=150,
        blank=True,
        null=True,
    )

    # 原物理来源：PurDetail.Spec
    specification_snapshot = models.CharField(
        '规格',
        max_length=50,
        blank=True,
        null=True,
    )

    # 原物理来源：PurDetail.LotNo
    supplier_lot_number = models.CharField(
        '批号',
        max_length=20,
        blank=True,
        null=True,
    )

    # 原物理来源：PurDetail.Qty
    quantity = models.DecimalField(
        '数量',
        max_digits=20,
        decimal_places=6,
    )

    # 原物理来源：PurDetail.ArticleUnit; PurDetail.StuffUnit
    unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='采购单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_unit_set",
    )

    # 原物理来源：PurDetail.Rolls
    piece_quantity = models.DecimalField(
        '粒数',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：PurDetail.Price
    unit_price = models.DecimalField(
        '价格',
        max_digits=8,
        decimal_places=4,
        blank=True,
        null=True,
    )

    # 原物理来源：PurDetail.PriceUnit
    price_unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='计价单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_price_unit_set",
        blank=True,
        null=True,
    )

    # 原物理来源：PurDetail.DlvDate
    due_at = models.DateTimeField(
        '交货日期',
        blank=True,
        null=True,
    )

    # 原物理来源：PurDetail.CheckNo
    order_line = models.ForeignKey(
        'erp_sales.SalesOrderLine',
        verbose_name='销售需求明细',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_order_line_set",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_purchase_purchaseorderline"
        verbose_name = '采购订单明细'
        verbose_name_plural = '采购订单明细'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['order', 'line_number'], name='erp_purchase_purchaseorderline_identity_uniq'),
            models.CheckConstraint(condition=Q(line_number__gt=0), name='erp_purchase_purchaseorderline_line_number_positive'),
            models.CheckConstraint(condition=Q(quantity__gt=0), name='erp_purchase_purchaseorderline_quantity_positive'),
        ]


class PurchaseReturn(ErpModel):
    """采购退货申请。"""

    number = models.CharField(
        '采购退货号',
        max_length=64,
        unique=True,
    )

    supplier = models.ForeignKey(
        'erp_base.Party',
        verbose_name='退货供应商',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_supplier_set",
    )

    returned_at = models.DateTimeField(
        '退货时间',
    )

    reason = models.TextField(
        '退货原因',
    )

    status = models.CharField(
        '退货状态',
        max_length=24,
        choices=choices.ReturnStatus.choices,
        default=choices.ReturnStatus.DRAFT,
    )

    warehouse_issue = models.OneToOneField(
        'erp_warehouse.StockIssue',
        verbose_name='退货出库单',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_warehouse_issue_set",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_purchase_purchasereturn"
        verbose_name = '采购退货申请'
        verbose_name_plural = '采购退货申请'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(status__in=choices.ReturnStatus.values), name='erp_purchase_purchasereturn_status_valid'),
        ]


class PurchaseReturnLine(ErpModel):
    """采购退货明细。"""

    return_order = models.ForeignKey(
        'erp_purchase.PurchaseReturn',
        verbose_name='采购退货单',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_return_order_set",
    )

    original_receipt_line = models.ForeignKey(
        'erp_warehouse.StockReceiptLine',
        verbose_name='原收货入库行',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_original_receipt_line_set",
    )

    quantity = models.DecimalField(
        '退货量',
        max_digits=20,
        decimal_places=6,
    )

    unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='退货单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_unit_set",
    )

    class Meta:
        db_table = "erp_purchase_purchasereturnline"
        verbose_name = '采购退货明细'
        verbose_name_plural = '采购退货明细'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(quantity__gt=0), name='erp_purchase_purchasereturnline_quantity_positive'),
        ]
