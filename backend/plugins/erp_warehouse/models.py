"""仓储管理模型；字段来源见 docs/ERP模型实施说明.md。"""
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q
from plugins.erp_base.models import ErpModel
from plugins.erp_base import choices
from .calculations import fixed_net_mass_kg, weighed_net_mass_kg


class InventoryLot(ErpModel):
    """库存批次。"""

    code = models.CharField(
        '内部批次号',
        max_length=64,
        unique=True,
    )

    material = models.ForeignKey(
        'erp_base.Material',
        verbose_name='物料',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_material_set",
    )

    owner = models.ForeignKey(
        'erp_base.Party',
        verbose_name='所有者主体',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_owner_set",
    )

    supplier = models.ForeignKey(
        'erp_base.Party',
        verbose_name='供应来源',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_supplier_set",
        blank=True,
        null=True,
    )

    # 原物理来源：GrayInDetail.LotNo; SemiInDetail.LotNo; StuffInDetail.LotNo
    supplier_lot_number = models.CharField(
        '供应商或客户原批号',
        max_length=255,
        blank=True,
    )

    production_batch = models.ForeignKey(
        'erp_production.DyeBatch',
        verbose_name='生产缸批',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_production_batch_set",
        blank=True,
        null=True,
    )

    received_at = models.DateTimeField(
        '首次入库时间',
        blank=True,
        null=True,
    )

    expiry_at = models.DateTimeField(
        '到期时间',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_warehouse_inventorylot"
        verbose_name = '库存批次'
        verbose_name_plural = '库存批次'
        ordering = ["-id"]


class StockReceipt(ErpModel):
    """实物入库单。"""

    number = models.CharField(
        '入库单号',
        max_length=64,
        unique=True,
    )

    # 原物理来源：GrayIn.SheetDate; SemiIn.SheetDate; StuffIn.SheetDate; ProdIn.SheetDate
    document_at = models.DateTimeField(
        '单据时间',
    )

    kind = models.CharField(
        '入库类型',
        max_length=24,
        choices=choices.ReceiptKind.choices,
    )

    warehouse = models.ForeignKey(
        'erp_base.Warehouse',
        verbose_name='收货仓库',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_warehouse_set",
    )

    source_party = models.ForeignKey(
        'erp_base.Party',
        verbose_name='送货或退料方',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_source_party_set",
        blank=True,
        null=True,
    )

    status = models.CharField(
        '库存单据状态',
        max_length=24,
        choices=choices.StockDocumentStatus.choices,
        default=choices.StockDocumentStatus.DRAFT,
    )

    posted_at = models.DateTimeField(
        '生效时间',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_warehouse_stockreceipt"
        verbose_name = '实物入库单'
        verbose_name_plural = '实物入库单'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(kind__in=choices.ReceiptKind.values), name='erp_warehouse_stockreceipt_kind_valid'),
            models.CheckConstraint(condition=Q(status__in=choices.StockDocumentStatus.values), name='erp_warehouse_stockreceipt_status_valid'),
        ]
        indexes = [
            models.Index(fields=['status', 'document_at'], name='war_stockreceipt_1'),
        ]


class StockReceiptLine(ErpModel):
    """入库明细。"""

    quantity_source = models.CharField('实际数量来源', max_length=24, default='manual', choices=[
        ('manual', '人工实录'), ('scale', '实称记录'), ('correction', '已批准更正'),
        ('legacy_confirmed', '核实旧事实'), ('legacy_unverified', '旧事实待核实')])

    receipt = models.ForeignKey(
        'erp_warehouse.StockReceipt',
        verbose_name='入库单',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_receipt_set",
    )

    line_number = models.IntegerField(
        '行号',
    )

    lot = models.ForeignKey(
        'erp_warehouse.InventoryLot',
        verbose_name='库存批次',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_lot_set",
    )

    # 原物理来源：GrayInDetail.StorageUnitIDs; SemiInDetail.StorageUnitID; ProdInRecord.StorageUnitID
    location = models.ForeignKey(
        'erp_base.StorageLocation',
        verbose_name='入库库位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_location_set",
    )

    # 原物理来源：GrayInDetail.WeightQty; GrayInDetail.LengthQty; SemiInDetail.InQty; StuffInDetail.Qty
    quantity = models.DecimalField(
        '入库基本单位量',
        max_digits=20,
        decimal_places=6,
    )

    unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='入库基本单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_unit_set",
    )

    # 原物理来源：GrayInDetail.WeightQty; SemiInDetail.WeightQty; ProdInRecord.NetKg
    auxiliary_mass_kg = models.DecimalField(
        '辅助重量kg',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：GrayInDetail.Rolls; SemiInDetail.Rolls; ProdInRecord.InRolls
    auxiliary_pieces = models.DecimalField(
        '辅助粒数',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    quality_state = models.CharField(
        '入库质量状态',
        max_length=24,
        choices=choices.QualityState.choices,
    )

    # 原物理来源：SemiInDetail.PurDetailNo
    purchase_order_line = models.ForeignKey(
        'erp_purchase.PurchaseOrderLine',
        verbose_name='采购来源明细',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_purchase_order_line_set",
        blank=True,
        null=True,
    )

    # 原物理来源：SemiInDetail.JobSheetNo
    work_card = models.ForeignKey(
        'erp_production.WorkCard',
        verbose_name='生产来源工卡',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_work_card_set",
        blank=True,
        null=True,
    )

    # 原物理来源：ProdInRecord.BarCode
    package = models.ForeignKey(
        'erp_warehouse.Package',
        verbose_name='包装单元',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_package_set",
        blank=True,
        null=True,
    )

    original_issue_line = models.ForeignKey(
        'erp_warehouse.StockIssueLine',
        verbose_name='退料来源出库行',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_original_issue_line_set",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_warehouse_stockreceiptline"
        verbose_name = '入库明细'
        verbose_name_plural = '入库明细'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['receipt', 'line_number'], name='erp_warehouse_stockreceiptline_identity_uniq'),
            models.CheckConstraint(condition=Q(line_number__gt=0), name='erp_warehouse_stockreceiptline_line_number_positive'),
            models.CheckConstraint(condition=Q(quality_state__in=choices.QualityState.values), name='erp_warehouse_stockreceiptline_quality_state_valid'),
            models.CheckConstraint(condition=Q(quantity__gt=0), name='erp_warehouse_stockreceiptline_quantity_positive'),
        ]

    def clean(self):
        super().clean()
        if self.receipt_id is not None and self.location_id is not None:
            if self.receipt.warehouse_id != self.location.warehouse_id:
                raise ValidationError({'location': '库位必须属于本单据仓库。'})
        if self.package_id is not None and self.package.lot_id != self.lot_id:
            raise ValidationError({'package': '包装单元必须属于本库存批次。'})
        if self.lot_id is not None and self.unit_id != self.lot.material.stock_unit_id:
            raise ValidationError({'unit': '库存数量必须使用物料库存基本单位。'})
        if self.location_id is not None and self.location.kind != choices.LocationKind.BIN:
            raise ValidationError({'location': '库存只记录在实际库位，不记录在库区。'})


class StockIssue(ErpModel):
    """实物出库单。"""

    number = models.CharField(
        '出库单号',
        max_length=64,
        unique=True,
    )

    # 原物理来源：GrayOut.SheetDate; SemiOut.SheetDate; StuffOut.SheetDate; ProdOut.SheetDate
    document_at = models.DateTimeField(
        '单据时间',
    )

    kind = models.CharField(
        '出库类型',
        max_length=24,
        choices=choices.IssueKind.choices,
    )

    warehouse = models.ForeignKey(
        'erp_base.Warehouse',
        verbose_name='发出仓库',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_warehouse_set",
    )

    destination_party = models.ForeignKey(
        'erp_base.Party',
        verbose_name='领用或收货方',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_destination_party_set",
        blank=True,
        null=True,
    )

    status = models.CharField(
        '库存单据状态',
        max_length=24,
        choices=choices.StockDocumentStatus.choices,
        default=choices.StockDocumentStatus.DRAFT,
    )

    posted_at = models.DateTimeField(
        '生效时间',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_warehouse_stockissue"
        verbose_name = '实物出库单'
        verbose_name_plural = '实物出库单'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(kind__in=choices.IssueKind.values), name='erp_warehouse_stockissue_kind_valid'),
            models.CheckConstraint(condition=Q(status__in=choices.StockDocumentStatus.values), name='erp_warehouse_stockissue_status_valid'),
        ]
        indexes = [
            models.Index(fields=['status', 'document_at'], name='war_stockissue_1'),
        ]


class StockIssueLine(ErpModel):
    """出库明细。"""

    quantity_source = models.CharField('实际数量来源', max_length=24, default='manual', choices=[
        ('manual', '人工实录'), ('scale', '实称记录'), ('correction', '已批准更正'),
        ('legacy_confirmed', '核实旧事实'), ('legacy_unverified', '旧事实待核实')])
    measurement_record = models.ForeignKey('erp_production.WeighingRecord', verbose_name='实称数量记录',
        null=True, blank=True, on_delete=models.PROTECT, related_name='stock_issue_lines')

    issue = models.ForeignKey(
        'erp_warehouse.StockIssue',
        verbose_name='出库单',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_issue_set",
    )

    line_number = models.IntegerField(
        '行号',
    )

    lot = models.ForeignKey(
        'erp_warehouse.InventoryLot',
        verbose_name='实际领用批次',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_lot_set",
    )

    location = models.ForeignKey(
        'erp_base.StorageLocation',
        verbose_name='发出库位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_location_set",
    )

    quantity = models.DecimalField(
        '实际出库量',
        max_digits=20,
        decimal_places=6,
    )

    unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='库存基本单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_unit_set",
    )

    quality_state = models.CharField(
        '发出时质量状态',
        max_length=24,
        choices=choices.QualityState.choices,
    )

    work_card = models.ForeignKey(
        'erp_production.WorkCard',
        verbose_name='领用工卡',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_work_card_set",
        blank=True,
        null=True,
    )

    weighing_line = models.ForeignKey(
        'erp_production.WeighingLine',
        verbose_name='化工料单明细',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_weighing_line_set",
        blank=True,
        null=True,
    )

    delivery_line = models.ForeignKey(
        'erp_sales.DeliveryLine',
        verbose_name='送货明细',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_delivery_line_set",
        blank=True,
        null=True,
    )

    package = models.ForeignKey(
        'erp_warehouse.Package',
        verbose_name='实际包装单元',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_package_set",
        blank=True,
        null=True,
    )

    original_receipt_line = models.ForeignKey(
        'erp_warehouse.StockReceiptLine',
        verbose_name='原入库行',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_original_receipt_line_set",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_warehouse_stockissueline"
        verbose_name = '出库明细'
        verbose_name_plural = '出库明细'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['issue', 'line_number'], name='erp_warehouse_stockissueline_identity_uniq'),
            models.CheckConstraint(condition=Q(line_number__gt=0), name='erp_warehouse_stockissueline_line_number_positive'),
            models.CheckConstraint(condition=Q(quality_state__in=choices.QualityState.values), name='erp_warehouse_stockissueline_quality_state_valid'),
            models.CheckConstraint(condition=Q(quantity__gt=0), name='erp_warehouse_stockissueline_quantity_positive'),
        ]

    def clean(self):
        super().clean()
        if self.issue_id is not None and self.location_id is not None:
            if self.issue.warehouse_id != self.location.warehouse_id:
                raise ValidationError({'location': '库位必须属于本单据仓库。'})
        if self.package_id is not None and self.package.lot_id != self.lot_id:
            raise ValidationError({'package': '包装单元必须属于本库存批次。'})
        if self.lot_id is not None and self.unit_id != self.lot.material.stock_unit_id:
            raise ValidationError({'unit': '库存数量必须使用物料库存基本单位。'})
        if self.location_id is not None and self.location.kind != choices.LocationKind.BIN:
            raise ValidationError({'location': '库存只记录在实际库位，不记录在库区。'})


class InventoryMovement(ErpModel):
    """库存数量流水。"""

    occurred_at = models.DateTimeField(
        '业务发生时间',
    )

    lot = models.ForeignKey(
        'erp_warehouse.InventoryLot',
        verbose_name='批次',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_lot_set",
    )

    location = models.ForeignKey(
        'erp_base.StorageLocation',
        verbose_name='库位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_location_set",
    )

    quality_state = models.CharField(
        '质量状态',
        max_length=24,
        choices=choices.QualityState.choices,
    )

    package = models.ForeignKey(
        'erp_warehouse.Package',
        verbose_name='可追溯包装单元',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_package_set",
        blank=True,
        null=True,
    )

    quantity_delta = models.DecimalField(
        '数量增减',
        max_digits=20,
        decimal_places=6,
    )

    unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='库存基本单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_unit_set",
    )

    receipt_line = models.ForeignKey(
        'erp_warehouse.StockReceiptLine',
        verbose_name='入库来源行',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_receipt_line_set",
        blank=True,
        null=True,
    )

    issue_line = models.ForeignKey(
        'erp_warehouse.StockIssueLine',
        verbose_name='出库来源行',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_issue_line_set",
        blank=True,
        null=True,
    )

    transfer_line = models.ForeignKey(
        'erp_warehouse.StockTransferLine',
        verbose_name='调拨来源行',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_transfer_line_set",
        blank=True,
        null=True,
    )

    adjustment_line = models.ForeignKey(
        'erp_warehouse.StockAdjustmentLine',
        verbose_name='调整来源行',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_adjustment_line_set",
        blank=True,
        null=True,
    )

    leg_number = models.IntegerField(
        '来源行分腿号',
    )

    reverses = models.OneToOneField(
        'erp_warehouse.InventoryMovement',
        verbose_name='被冲销流水',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_reverses_set",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_warehouse_inventorymovement"
        verbose_name = '库存数量流水'
        verbose_name_plural = '库存数量流水'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['receipt_line', 'leg_number'], name='erp_warehouse_inventorymovement_receipt_line_leg_uniq', condition=Q(receipt_line__isnull=False, reverses__isnull=True)),
            models.UniqueConstraint(fields=['issue_line', 'leg_number'], name='erp_warehouse_inventorymovement_issue_line_leg_uniq', condition=Q(issue_line__isnull=False, reverses__isnull=True)),
            models.UniqueConstraint(fields=['transfer_line', 'leg_number'], name='erp_warehouse_inventorymovement_transfer_line_leg_uniq', condition=Q(transfer_line__isnull=False, reverses__isnull=True)),
            models.UniqueConstraint(fields=['adjustment_line', 'leg_number'], name='erp_warehouse_inventorymovement_adjustment_line_leg_uniq', condition=Q(adjustment_line__isnull=False, reverses__isnull=True)),
            models.CheckConstraint(condition=Q(quality_state__in=choices.QualityState.values), name='erp_warehouse_inventorymovement_quality_state_valid'),
            models.CheckConstraint(condition=Q(reverses__isnull=True) | ~Q(reverses=F("pk")), name='erp_warehouse_inventorymovement_reverses_not_self'),
            models.CheckConstraint(condition=Q(receipt_line__isnull=False, issue_line__isnull=True, transfer_line__isnull=True, adjustment_line__isnull=True) | Q(receipt_line__isnull=True, issue_line__isnull=False, transfer_line__isnull=True, adjustment_line__isnull=True) | Q(receipt_line__isnull=True, issue_line__isnull=True, transfer_line__isnull=False, adjustment_line__isnull=True) | Q(receipt_line__isnull=True, issue_line__isnull=True, transfer_line__isnull=True, adjustment_line__isnull=False), name='erp_warehouse_inventorymovement_one_source'),
            models.CheckConstraint(condition=Q(leg_number__in=[1, 2]), name='erp_warehouse_inventorymovement_leg_valid'),
            models.CheckConstraint(condition=~Q(quantity_delta=0), name='erp_warehouse_inventorymovement_nonzero_delta'),
            models.CheckConstraint(condition=Q(reverses__isnull=False) | Q(transfer_line__isnull=False) | Q(adjustment_line__isnull=False) | Q(leg_number=1), name='erp_warehouse_inventorymovement_single_leg'),
        ]
        indexes = [
            models.Index(fields=['lot', 'location', 'quality_state', 'occurred_at', 'id'], name='war_inventorymovement_1'),
        ]

    def clean(self):
        super().clean()
        if self.package_id is not None and self.package.lot_id != self.lot_id:
            raise ValidationError({'package': '包装单元必须属于本库存批次。'})
        if self.lot_id is not None and self.unit_id != self.lot.material.stock_unit_id:
            raise ValidationError({'unit': '库存数量必须使用物料库存基本单位。'})
        if self.location_id is not None and self.location.kind != choices.LocationKind.BIN:
            raise ValidationError({'location': '库存只记录在实际库位，不记录在库区。'})
        if self.reverses_id is not None:
            original = self.reverses
            if original.reverses_id is not None:
                raise ValidationError({'reverses': '不能冲销已经用于冲销的流水。'})
            if (self.lot_id, self.location_id, self.quality_state, self.package_id, self.unit_id) != (original.lot_id, original.location_id, original.quality_state, original.package_id, original.unit_id):
                raise ValidationError({'reverses': '冲销必须保持原流水的实物和计量维度。'})
            if self.quantity_delta != -original.quantity_delta:
                raise ValidationError({'quantity_delta': '冲销量必须与原流水等量反向。'})
            if (self.receipt_line_id, self.issue_line_id, self.transfer_line_id, self.adjustment_line_id, self.leg_number) != (original.receipt_line_id, original.issue_line_id, original.transfer_line_id, original.adjustment_line_id, original.leg_number):
                raise ValidationError({'reverses': '冲销必须沿用原业务来源行及分腿号。'})


class StockBalance(ErpModel):
    """当前库存数量。"""

    lot = models.ForeignKey(
        'erp_warehouse.InventoryLot',
        verbose_name='批次',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_lot_set",
    )

    location = models.ForeignKey(
        'erp_base.StorageLocation',
        verbose_name='库位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_location_set",
    )

    quality_state = models.CharField(
        '质量状态',
        max_length=24,
        choices=choices.QualityState.choices,
    )

    package = models.ForeignKey(
        'erp_warehouse.Package',
        verbose_name='包装单元',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_package_set",
        blank=True,
        null=True,
    )

    quantity = models.DecimalField(
        '当前实存量',
        max_digits=20,
        decimal_places=6,
        default=Decimal("0"),
    )

    class Meta:
        db_table = "erp_warehouse_stockbalance"
        verbose_name = '当前库存数量'
        verbose_name_plural = '当前库存数量'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['lot', 'location', 'quality_state'], name='erp_warehouse_stockbalance_bulk_uniq', condition=Q(package__isnull=True)),
            models.UniqueConstraint(fields=['lot', 'location', 'quality_state', 'package'], name='erp_warehouse_stockbalance_package_uniq', condition=Q(package__isnull=False)),
            models.CheckConstraint(condition=Q(quality_state__in=choices.QualityState.values), name='erp_warehouse_stockbalance_quality_state_valid'),
            models.CheckConstraint(condition=Q(quantity__gte=0), name='erp_warehouse_stockbalance_quantity_nonnegative'),
        ]

    def clean(self):
        super().clean()
        if self.package_id is not None and self.package.lot_id != self.lot_id:
            raise ValidationError({'package': '包装单元必须属于本库存批次。'})
        if self.location_id is not None and self.location.kind != choices.LocationKind.BIN:
            raise ValidationError({'location': '库存只记录在实际库位，不记录在库区。'})


class StockTransfer(ErpModel):
    """库存调拨单。"""

    number = models.CharField(
        '调拨号',
        max_length=64,
        unique=True,
    )

    document_at = models.DateTimeField(
        '单据时间',
    )

    from_warehouse = models.ForeignKey(
        'erp_base.Warehouse',
        verbose_name='发出仓库',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_from_warehouse_set",
    )

    to_warehouse = models.ForeignKey(
        'erp_base.Warehouse',
        verbose_name='接收仓库',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_to_warehouse_set",
    )

    status = models.CharField(
        '状态',
        max_length=24,
        choices=choices.StockDocumentStatus.choices,
        default=choices.StockDocumentStatus.DRAFT,
    )

    posted_at = models.DateTimeField(
        '库存生效时间',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_warehouse_stocktransfer"
        verbose_name = '库存调拨单'
        verbose_name_plural = '库存调拨单'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(status__in=choices.StockDocumentStatus.values), name='erp_warehouse_stocktransfer_status_valid'),
        ]
        indexes = [
            models.Index(fields=['status', 'document_at'], name='war_stocktransfer_1'),
        ]


class StockTransferLine(ErpModel):
    """调拨明细。"""

    transfer = models.ForeignKey(
        'erp_warehouse.StockTransfer',
        verbose_name='调拨单',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_transfer_set",
    )

    line_number = models.IntegerField(
        '行号',
    )

    lot = models.ForeignKey(
        'erp_warehouse.InventoryLot',
        verbose_name='批次',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_lot_set",
    )

    package = models.ForeignKey(
        'erp_warehouse.Package',
        verbose_name='调拨包装单元',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_package_set",
        blank=True,
        null=True,
    )

    from_location = models.ForeignKey(
        'erp_base.StorageLocation',
        verbose_name='发出库位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_from_location_set",
    )

    to_location = models.ForeignKey(
        'erp_base.StorageLocation',
        verbose_name='接收库位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_to_location_set",
    )

    quantity = models.DecimalField(
        '调拨量',
        max_digits=20,
        decimal_places=6,
    )

    quality_state = models.CharField(
        '质量状态',
        max_length=24,
        choices=choices.QualityState.choices,
    )

    class Meta:
        db_table = "erp_warehouse_stocktransferline"
        verbose_name = '调拨明细'
        verbose_name_plural = '调拨明细'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['transfer', 'line_number'], name='erp_warehouse_stocktransferline_identity_uniq'),
            models.CheckConstraint(condition=Q(line_number__gt=0), name='erp_warehouse_stocktransferline_line_number_positive'),
            models.CheckConstraint(condition=Q(quality_state__in=choices.QualityState.values), name='erp_warehouse_stocktransferline_quality_state_valid'),
            models.CheckConstraint(condition=Q(quantity__gt=0), name='erp_warehouse_stocktransferline_quantity_positive'),
            models.CheckConstraint(condition=~Q(from_location=F("to_location")), name='erp_warehouse_stocktransferline_different_locations'),
        ]

    def clean(self):
        super().clean()
        if self.transfer_id is not None:
            if self.from_location_id is not None and self.from_location.warehouse_id != self.transfer.from_warehouse_id:
                raise ValidationError({'from_location': '发出库位必须属于发出仓库。'})
            if self.to_location_id is not None and self.to_location.warehouse_id != self.transfer.to_warehouse_id:
                raise ValidationError({'to_location': '接收库位必须属于接收仓库。'})
        if self.package_id is not None and self.package.lot_id != self.lot_id:
            raise ValidationError({'package': '包装单元必须属于本库存批次。'})


class StockCount(ErpModel):
    """盘点单。"""

    number = models.CharField(
        '盘点号',
        max_length=64,
        unique=True,
    )

    warehouse = models.ForeignKey(
        'erp_base.Warehouse',
        verbose_name='盘点仓库',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_warehouse_set",
    )

    snapshot_at = models.DateTimeField(
        '冻结账面时间',
        null=True,
        blank=True,
    )

    counted_at = models.DateTimeField(
        '实际盘点时间',
        blank=True,
        null=True,
    )

    status = models.CharField(
        '盘点状态',
        max_length=24,
        choices=choices.CountStatus.choices,
        default=choices.CountStatus.DRAFT,
    )

    class Meta:
        db_table = "erp_warehouse_stockcount"
        verbose_name = '盘点单'
        verbose_name_plural = '盘点单'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(status__in=choices.CountStatus.values), name='erp_warehouse_stockcount_status_valid'),
        ]


class StockCountLine(ErpModel):
    """盘点明细。"""

    count = models.ForeignKey(
        'erp_warehouse.StockCount',
        verbose_name='盘点单',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_count_set",
    )

    lot = models.ForeignKey(
        'erp_warehouse.InventoryLot',
        verbose_name='批次',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_lot_set",
    )

    location = models.ForeignKey(
        'erp_base.StorageLocation',
        verbose_name='库位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_location_set",
    )

    quality_state = models.CharField(
        '质量状态',
        max_length=24,
        choices=choices.QualityState.choices,
    )

    package = models.ForeignKey(
        'erp_warehouse.Package',
        verbose_name='盘点包装单元',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_package_set",
        blank=True,
        null=True,
    )

    book_quantity = models.DecimalField(
        '盘点冻结账面量',
        max_digits=20,
        decimal_places=6,
    )

    counted_quantity = models.DecimalField(
        '实盘量',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    reason = models.TextField(
        '差异原因',
        blank=True,
    )

    class Meta:
        db_table = "erp_warehouse_stockcountline"
        verbose_name = '盘点明细'
        verbose_name_plural = '盘点明细'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['count', 'lot', 'location', 'quality_state'], name='erp_warehouse_stockcountline_bulk_uniq', condition=Q(package__isnull=True)),
            models.UniqueConstraint(fields=['count', 'lot', 'location', 'quality_state', 'package'], name='erp_warehouse_stockcountline_package_uniq', condition=Q(package__isnull=False)),
            models.CheckConstraint(condition=Q(quality_state__in=choices.QualityState.values), name='erp_warehouse_stockcountline_quality_state_valid'),
            models.CheckConstraint(condition=Q(book_quantity__gte=0), name='erp_warehouse_stockcountline_book_quantity_nonnegative'),
            models.CheckConstraint(condition=Q(counted_quantity__isnull=True) | Q(counted_quantity__gte=0), name='erp_warehouse_stockcountline_counted_quantity_nonnegative'),
        ]

    def clean(self):
        super().clean()
        if self.count_id is not None and self.location_id is not None:
            if self.count.warehouse_id != self.location.warehouse_id:
                raise ValidationError({'location': '库位必须属于本单据仓库。'})
        if self.package_id is not None and self.package.lot_id != self.lot_id:
            raise ValidationError({'package': '包装单元必须属于本库存批次。'})
        if self.location_id is not None and self.location.kind != choices.LocationKind.BIN:
            raise ValidationError({'location': '库存只记录在实际库位，不记录在库区。'})

    @property
    def difference(self):
        if self.counted_quantity is None:
            return None
        return self.counted_quantity - self.book_quantity


class StockAdjustment(ErpModel):
    """库存调整单。"""

    number = models.CharField(
        '调整号',
        max_length=64,
        unique=True,
    )

    document_at = models.DateTimeField(
        '单据时间',
    )

    warehouse = models.ForeignKey(
        'erp_base.Warehouse',
        verbose_name='仓库',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_warehouse_set",
    )

    count = models.ForeignKey(
        'erp_warehouse.StockCount',
        verbose_name='来源盘点',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_count_set",
        blank=True,
        null=True,
    )

    reason = models.TextField(
        '调整原因',
    )

    status = models.CharField(
        '状态',
        max_length=24,
        choices=choices.StockDocumentStatus.choices,
        default=choices.StockDocumentStatus.DRAFT,
    )

    posted_at = models.DateTimeField(
        '库存生效时间',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_warehouse_stockadjustment"
        verbose_name = '库存调整单'
        verbose_name_plural = '库存调整单'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(status__in=choices.StockDocumentStatus.values), name='erp_warehouse_stockadjustment_status_valid'),
        ]
        indexes = [
            models.Index(fields=['status', 'document_at'], name='war_stockadjustment_1'),
        ]


class StockAdjustmentLine(ErpModel):
    """库存调整明细。"""

    adjustment = models.ForeignKey(
        'erp_warehouse.StockAdjustment',
        verbose_name='调整单',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_adjustment_set",
    )

    line_number = models.IntegerField(
        '行号',
    )

    lot = models.ForeignKey(
        'erp_warehouse.InventoryLot',
        verbose_name='批次',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_lot_set",
    )

    location = models.ForeignKey(
        'erp_base.StorageLocation',
        verbose_name='库位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_location_set",
    )

    quality_state = models.CharField(
        '原质量状态',
        max_length=24,
        choices=choices.QualityState.choices,
    )

    package = models.ForeignKey(
        'erp_warehouse.Package',
        verbose_name='调整包装单元',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_package_set",
        blank=True,
        null=True,
    )

    quantity_delta = models.DecimalField(
        '数量增减或状态转换覆盖量',
        max_digits=20,
        decimal_places=6,
    )

    new_quality_state = models.CharField(
        '目标质量状态',
        max_length=24,
        choices=choices.QualityState.choices,
        blank=True,
        null=True,
    )

    count_line = models.OneToOneField(
        'erp_warehouse.StockCountLine',
        verbose_name='盘点来源',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_count_line_set",
        blank=True,
        null=True,
    )

    disposition = models.ForeignKey(
        'erp_production.QualityDisposition',
        verbose_name='质量处置来源',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_disposition_set",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_warehouse_stockadjustmentline"
        verbose_name = '库存调整明细'
        verbose_name_plural = '库存调整明细'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['adjustment', 'line_number'], name='erp_warehouse_stockadjustmentline_identity_uniq'),
            models.CheckConstraint(condition=Q(line_number__gt=0), name='erp_warehouse_stockadjustmentline_line_number_positive'),
            models.CheckConstraint(condition=Q(quality_state__in=choices.QualityState.values), name='erp_warehouse_stockadjustmentline_quality_state_valid'),
            models.CheckConstraint(condition=Q(new_quality_state__isnull=True) | Q(new_quality_state__in=choices.QualityState.values), name='erp_warehouse_stockadjustmentline_new_quality_state_valid'),
            models.CheckConstraint(condition=Q(new_quality_state__isnull=True) | (Q(quantity_delta__gt=0, disposition__isnull=False) & ~Q(new_quality_state=F("quality_state"))), name='erp_warehouse_stockadjustmentline_quality_transfer'),
            models.CheckConstraint(condition=~Q(quantity_delta=0), name='erp_warehouse_stockadjustmentline_nonzero_delta'),
        ]

    def clean(self):
        super().clean()
        if self.adjustment_id is not None and self.location_id is not None:
            if self.adjustment.warehouse_id != self.location.warehouse_id:
                raise ValidationError({'location': '库位必须属于本单据仓库。'})
        if self.package_id is not None and self.package.lot_id != self.lot_id:
            raise ValidationError({'package': '包装单元必须属于本库存批次。'})


class LotTransformation(ErpModel):
    """半成品和生产批次转换。"""

    number = models.CharField(
        '转换号',
        max_length=64,
        unique=True,
    )

    work_card = models.ForeignKey(
        'erp_production.WorkCard',
        verbose_name='工卡',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_work_card_set",
        blank=True,
        null=True,
    )

    execution = models.ForeignKey(
        'erp_production.OperationExecution',
        verbose_name='实际工序',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_execution_set",
        blank=True,
        null=True,
    )

    occurred_at = models.DateTimeField(
        '转换时间',
    )

    reason = models.TextField(
        '转换说明',
        blank=True,
    )

    class Meta:
        db_table = "erp_warehouse_lottransformation"
        verbose_name = '半成品和生产批次转换'
        verbose_name_plural = '半成品和生产批次转换'
        ordering = ["-id"]


class LotTransformationLine(ErpModel):
    """批次转换投入和产出。"""

    transformation = models.ForeignKey(
        'erp_warehouse.LotTransformation',
        verbose_name='转换单',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_transformation_set",
    )

    direction = models.CharField(
        '投入或产出',
        max_length=24,
        choices=choices.TransformationDirection.choices,
    )

    lot = models.ForeignKey(
        'erp_warehouse.InventoryLot',
        verbose_name='批次',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_lot_set",
    )

    quantity = models.DecimalField(
        '数量',
        max_digits=20,
        decimal_places=6,
    )

    unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_unit_set",
    )

    receipt_line = models.OneToOneField(
        'erp_warehouse.StockReceiptLine',
        verbose_name='产出入库行',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_receipt_line_set",
        blank=True,
        null=True,
    )

    issue_line = models.OneToOneField(
        'erp_warehouse.StockIssueLine',
        verbose_name='投入出库行',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_issue_line_set",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_warehouse_lottransformationline"
        verbose_name = '批次转换投入和产出'
        verbose_name_plural = '批次转换投入和产出'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(direction__in=choices.TransformationDirection.values), name='erp_warehouse_lottransformationline_direction_valid'),
            models.CheckConstraint(condition=Q(quantity__gt=0), name='erp_warehouse_lottransformationline_quantity_positive'),
            models.CheckConstraint(condition=(Q(direction=choices.TransformationDirection.INPUT, issue_line__isnull=False, receipt_line__isnull=True) | Q(direction=choices.TransformationDirection.OUTPUT, receipt_line__isnull=False, issue_line__isnull=True)), name='erp_warehouse_lottransformationline_direction_source'),
        ]


class Package(ErpModel):
    """包装单元和细码。"""

    code = models.CharField(
        '内部包装号',
        max_length=64,
    )

    # 原物理来源：RecordYield.BarCode; ProdInRecord.ProdBarCode
    barcode = models.CharField(
        '条码',
        max_length=255,
    )

    # 原物理来源：RecordYield.RollNo; ProdInRecord.RollNo
    display_number = models.CharField(
        '箱筒卷显示号',
        max_length=64,
        blank=True,
    )

    lot = models.ForeignKey(
        'erp_warehouse.InventoryLot',
        verbose_name='产出库存批次',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_lot_set",
    )

    # 原物理来源：RecordYield.JobSheetNo
    work_card = models.ForeignKey(
        'erp_production.WorkCard',
        verbose_name='来源工卡',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_work_card_set",
    )

    batch = models.ForeignKey(
        'erp_production.DyeBatch',
        verbose_name='来源缸批',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_batch_set",
        blank=True,
        null=True,
    )

    # 原物理来源：RecordYield.PackTime
    packed_at = models.DateTimeField(
        '包装时间',
        blank=True,
        null=True,
    )

    # 原物理来源：RecordYield.EmpID
    packer = models.ForeignKey(
        'erp_base.Employee',
        verbose_name='包装人员',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_packer_set",
        blank=True,
        null=True,
    )

    # 原物理来源：RecordYield.Rolls
    piece_quantity = models.DecimalField(
        '粒筒数',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    tube_specification = models.ForeignKey(
        'erp_base.PackagingSpecification',
        verbose_name='筒管规格',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_tube_specification_set",
        blank=True,
        null=True,
    )

    # 原物理来源：RecordYield.TubeWeight; ProdInRecord.TubeWeight
    tube_unit_tare_kg = models.DecimalField(
        '单筒皮重kg快照',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    outer_packaging = models.ForeignKey(
        'erp_base.PackagingSpecification',
        verbose_name='外包装规格',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_outer_packaging_set",
        blank=True,
        null=True,
    )

    # 原物理来源：RecordYield.PackBag; ProdInRecord.PackBag
    outer_tare_kg = models.DecimalField(
        '该包装外包装总皮重kg',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：RecordYield.Kg
    gross_mass_kg = models.DecimalField(
        '毛重kg',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：RecordYield.NetKg; ProdInRecord.NetKg
    net_mass_kg = models.DecimalField(
        '采用净重kg',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    net_mass_basis = models.CharField(
        '净重采用方式',
        max_length=24,
        choices=choices.NetMassBasis.choices,
        blank=True,
        null=True,
    )

    # 原物理来源：RecordYield.FixedQty
    fixed_piece_mass_kg = models.DecimalField(
        '固定单粒质量kg',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：RecordYield.Meter
    length_m = models.DecimalField(
        '长度m',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：RecordYield.LabelID
    label_template = models.ForeignKey(
        'erp_base.LabelTemplate',
        verbose_name='采用标签版本',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_label_template_set",
        blank=True,
        null=True,
    )

    # 原物理来源：RecordYield.LabelRemarks
    label_remarks = models.CharField(
        '标签备注',
        max_length=500,
        blank=True,
        null=True,
    )

    status = models.CharField(
        '包装状态',
        max_length=24,
        choices=choices.PackageStatus.choices,
        default=choices.PackageStatus.DRAFT,
    )

    class Meta:
        db_table = "erp_warehouse_package"
        verbose_name = '包装单元和细码'
        verbose_name_plural = '包装单元和细码'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['barcode'], name='erp_warehouse_package_barcode_uniq'),
            models.UniqueConstraint(fields=['code'], name='erp_warehouse_package_code_uniq'),
            models.CheckConstraint(condition=Q(net_mass_basis__isnull=True) | Q(net_mass_basis__in=choices.NetMassBasis.values), name='erp_warehouse_package_net_mass_basis_valid'),
            models.CheckConstraint(condition=Q(status__in=choices.PackageStatus.values), name='erp_warehouse_package_status_valid'),
            models.CheckConstraint(condition=Q(gross_mass_kg__isnull=True) | Q(gross_mass_kg__gte=0), name='erp_warehouse_package_gross_mass_kg_nonnegative'),
            models.CheckConstraint(condition=Q(tube_unit_tare_kg__isnull=True) | Q(tube_unit_tare_kg__gte=0), name='erp_warehouse_package_tube_unit_tare_kg_nonnegative'),
            models.CheckConstraint(condition=Q(outer_tare_kg__isnull=True) | Q(outer_tare_kg__gte=0), name='erp_warehouse_package_outer_tare_kg_nonnegative'),
            models.CheckConstraint(condition=Q(fixed_piece_mass_kg__isnull=True) | Q(fixed_piece_mass_kg__gte=0), name='erp_warehouse_package_fixed_piece_mass_kg_nonnegative'),
            models.CheckConstraint(condition=Q(net_mass_kg__isnull=True) | Q(net_mass_kg__gte=0), name='erp_warehouse_package_net_mass_kg_nonnegative'),
            models.CheckConstraint(condition=Q(piece_quantity__isnull=True) | Q(piece_quantity__gte=0), name='erp_warehouse_package_piece_quantity_nonnegative'),
        ]
        indexes = [
            models.Index(fields=['work_card'], name='war_package_1'),
            models.Index(fields=['batch'], name='war_package_2'),
        ]

    def clean(self):
        super().clean()
        if self.work_card_id is not None and self.lot_id is not None:
            if self.work_card.material_id != self.lot.material_id:
                raise ValidationError({'lot': '包装批次物料必须与来源工卡一致。'})
        if self.batch_id is not None and self.work_card_id is not None:
            if not self.batch.erp_production_dyebatchworkcard_batch_set.filter(work_card_id=self.work_card_id).exists():
                raise ValidationError({'batch': '缸批必须包含本包装的来源工卡。'})

    @property
    def calculated_net_mass_kg(self):
        if self.net_mass_basis is None:
            return None
        if self.net_mass_basis == choices.NetMassBasis.WEIGHED_LESS_TARE:
            return weighed_net_mass_kg(self.gross_mass_kg, self.tube_unit_tare_kg, self.piece_quantity, self.outer_tare_kg)
        if self.net_mass_basis == choices.NetMassBasis.FIXED_PIECE_MASS:
            return fixed_net_mass_kg(self.fixed_piece_mass_kg, self.piece_quantity)
        raise ValidationError({'net_mass_basis': '必须明确选择净重计算方法。'})


class PackageOrderAllocation(ErpModel):
    """包装订单数量分配。"""

    package = models.ForeignKey(
        'erp_warehouse.Package',
        verbose_name='包装单元',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_package_set",
    )

    work_card_allocation = models.ForeignKey(
        'erp_production.WorkCardOrderAllocation',
        verbose_name='工卡订单分配',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_work_card_allocation_set",
    )

    quantity = models.DecimalField(
        '分配基本单位量',
        max_digits=20,
        decimal_places=6,
    )

    unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_unit_set",
    )

    class Meta:
        db_table = "erp_warehouse_packageorderallocation"
        verbose_name = '包装订单数量分配'
        verbose_name_plural = '包装订单数量分配'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['package', 'work_card_allocation'], name='erp_warehouse_packageorderallocation_identity_uniq'),
            models.CheckConstraint(condition=Q(quantity__gt=0), name='erp_warehouse_packageorderallocation_quantity_positive'),
        ]

    def clean(self):
        super().clean()
        if self.package_id is not None and self.work_card_allocation_id is not None:
            if self.package.work_card_id != self.work_card_allocation.work_card_id:
                raise ValidationError({'work_card_allocation': '包装订单分配必须属于本包装的来源工卡。'})


class LabelPrint(ErpModel):
    """标签打印记录。"""

    package = models.ForeignKey(
        'erp_warehouse.Package',
        verbose_name='包装单元',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_package_set",
    )

    template = models.ForeignKey(
        'erp_base.LabelTemplate',
        verbose_name='标签版本',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_template_set",
    )

    printed_at = models.DateTimeField(
        '打印时间',
    )

    copies = models.IntegerField(
        '份数',
    )

    kind = models.CharField(
        '打印类型',
        max_length=24,
        choices=choices.LabelPrintKind.choices,
    )

    reason = models.TextField(
        '重打原因',
        blank=True,
    )

    operator = models.ForeignKey(
        'erp_base.Employee',
        verbose_name='操作人',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_operator_set",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_warehouse_labelprint"
        verbose_name = '标签打印记录'
        verbose_name_plural = '标签打印记录'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(copies__gt=0), name='erp_warehouse_labelprint_copies_positive'),
            models.CheckConstraint(condition=Q(kind__in=choices.LabelPrintKind.values), name='erp_warehouse_labelprint_kind_valid'),
        ]
