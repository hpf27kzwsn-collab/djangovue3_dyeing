"""销售管理模型；字段来源见 docs/ERP模型实施说明.md。"""
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q
from plugins.erp_base.models import ErpModel
from plugins.erp_base import choices


class SalesOrder(ErpModel):
    """加工销售订单。"""

    # 原物理来源：OrderMain.SheetNo
    number = models.CharField(
        '表单编号',
        max_length=20,
        unique=True,
    )

    # 原物理来源：OrderMain.SheetDate
    document_at = models.DateTimeField(
        '单据日期',
    )

    # 原物理来源：OrderMain.BusinessUnitID
    business_unit = models.ForeignKey(
        'erp_base.BusinessUnit',
        verbose_name='经营单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_business_unit_set",
        blank=True,
        null=True,
    )

    # 原物理来源：OrderMain.CustomerID
    customer = models.ForeignKey(
        'erp_base.Party',
        verbose_name='客户',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_customer_set",
    )

    # 原物理来源：OrderMain.DetailCustName
    detail_customer_name = models.CharField(
        '明细客户',
        max_length=150,
        blank=True,
        null=True,
    )

    # 原物理来源：OrderMain.SalerID
    salesperson = models.ForeignKey(
        'erp_base.Employee',
        verbose_name='业务员',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_salesperson_set",
        blank=True,
        null=True,
    )

    # 原物理来源：OrderMain.ContractNo
    customer_order_number = models.CharField(
        '客户单号',
        max_length=500,
        blank=True,
        null=True,
    )

    # 原物理来源：OrderMain.CustSelfNo
    customer_job_number = models.CharField(
        '制单号',
        max_length=500,
        blank=True,
        null=True,
    )

    # 原物理来源：OrderMain.OrderKindID
    order_kind = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='订单类型',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_order_kind_set",
        blank=True,
        null=True,
    )

    delivery_address = models.ForeignKey(
        'erp_base.PartyAddress',
        verbose_name='送货地址',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_delivery_address_set",
        blank=True,
        null=True,
    )

    # 原物理来源：OrderMain.AddrDlv
    delivery_address_snapshot = models.CharField(
        '交货地址',
        max_length=500,
        blank=True,
        null=True,
    )

    # 原物理来源：OrderMain.Linker
    brand_name = models.CharField(
        '品牌',
        max_length=250,
        blank=True,
        null=True,
    )

    # 原物理来源：OrderMain.LinkerInfo
    contact_information = models.CharField(
        '联系人信息',
        max_length=100,
        blank=True,
        null=True,
    )

    # 原物理来源：OrderMain.FirstDlvDate
    first_due_at = models.DateTimeField(
        '头缸交期',
        blank=True,
        null=True,
    )

    # 原物理来源：OrderMain.IsHurry
    is_urgent = models.BooleanField(
        '加急',
        blank=True,
        null=True,
    )

    # 原物理来源：OrderMain.VerLight1ID
    primary_light = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='主光源',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_primary_light_set",
        blank=True,
        null=True,
    )

    # 原物理来源：OrderMain.VerLight2ID
    secondary_light = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='副光源',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_secondary_light_set",
        blank=True,
        null=True,
    )

    # 原物理来源：OrderMain.SheetStatus
    status = models.CharField(
        '订单状态',
        max_length=24,
        choices=choices.OrderStatus.choices,
        default=choices.OrderStatus.DRAFT,
    )

    # 原物理来源：OrderMain.Approver
    confirmed_by = models.ForeignKey(
        'erp_base.Employee',
        verbose_name='确认人',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_confirmed_by_set",
        blank=True,
        null=True,
    )

    # 原物理来源：OrderMain.ApproveDate
    confirmed_at = models.DateTimeField(
        '审核时间',
        blank=True,
        null=True,
    )

    # 原物理来源：OrderMain.FinishDate
    closed_at = models.DateTimeField(
        '结案日期',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_sales_salesorder"
        verbose_name = '加工销售订单'
        verbose_name_plural = '加工销售订单'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(status__in=choices.OrderStatus.values), name='erp_sales_salesorder_status_valid'),
        ]
        indexes = [
            models.Index(fields=['status', 'document_at'], name='sal_salesorder_1'),
        ]


class SalesOrderLine(ErpModel):
    """订单颜色规格明细。"""

    price_source = models.ForeignKey('erp_sales.CommercialPriceLine', verbose_name='采用价格明细',
        on_delete=models.PROTECT, null=True, blank=True, related_name='adopted_order_lines')
    manual_price_reason = models.TextField('手工定价原因', blank=True)
    adopted_price_snapshot = models.DecimalField('来源价格精确快照', max_digits=20, decimal_places=6,
                                                null=True, blank=True)

    # 原物理来源：OrderColor.SheetSeries
    order = models.ForeignKey(
        'erp_sales.SalesOrder',
        verbose_name='订单',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_order_set",
    )

    line_number = models.IntegerField(
        '行号',
    )

    # 原物理来源：OrderColor.ProdID
    material = models.ForeignKey(
        'erp_base.Material',
        verbose_name='本厂物料',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_material_set",
    )

    customer_material = models.ForeignKey(
        'erp_base.CustomerMaterial',
        verbose_name='客户物料对照',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_customer_material_set",
        blank=True,
        null=True,
    )

    # 原物理来源：OrderColor.Spec
    specification_snapshot = models.CharField(
        '规格',
        max_length=200,
        blank=True,
        null=True,
    )

    # 原物理来源：OrderColor.CustSelfProduct
    customer_product_snapshot = models.CharField(
        '客户规格',
        max_length=250,
        blank=True,
        null=True,
    )

    # 原物理来源：OrderColor.CustSelfNoDetail
    customer_line_number = models.CharField(
        '客户单号明细',
        max_length=150,
        blank=True,
        null=True,
    )

    # 原物理来源：OrderColor.LotNo
    supplier_lot_number = models.CharField(
        '批号',
        max_length=200,
        blank=True,
        null=True,
    )

    # 原物理来源：OrderColor.ColorNum
    color_standard = models.ForeignKey(
        'erp_base.ColorStandard',
        verbose_name='标准色号',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_color_standard_set",
        blank=True,
        null=True,
    )

    # 原物理来源：OrderColor.ColorNum
    color_number_snapshot = models.CharField(
        '色号',
        max_length=50,
        blank=True,
        null=True,
    )

    # 原物理来源：OrderColor.CustColorNum
    customer_color_number = models.CharField(
        '客户色号',
        max_length=100,
        blank=True,
        null=True,
    )

    # 原物理来源：OrderColor.ColorDepthID
    color_depth = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='色深',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_color_depth_set",
        blank=True,
        null=True,
    )

    # 原物理来源：OrderColor.OrderQty
    ordered_quantity = models.DecimalField(
        '成品数量',
        max_digits=20,
        decimal_places=6,
    )

    # 原物理来源：OrderColor.Unit
    ordered_unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='订货单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_ordered_unit_set",
    )

    # 原物理来源：OrderColor.GrayQty
    required_raw_quantity = models.DecimalField(
        '投坏数量',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    required_raw_unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='坯纱数量单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_required_raw_unit_set",
        blank=True,
        null=True,
    )

    # 原物理来源：OrderColor.OrderRolls
    piece_quantity = models.DecimalField(
        '订单粒数',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：OrderColor.DlvDate
    dyeing_due_at = models.DateTimeField(
        '染色日期',
        blank=True,
        null=True,
    )

    # 原物理来源：OrderColor.FinalDlvDate
    final_due_at = models.DateTimeField(
        '协议交货日期',
        blank=True,
        null=True,
    )

    # 原物理来源：OrderColor.ColorRemarks
    intended_use = models.CharField(
        '用途',
        max_length=500,
        blank=True,
        null=True,
    )

    # 原物理来源：OrderColor.Atte
    special_requirements = models.CharField(
        '特殊事项',
        max_length=100,
        blank=True,
        null=True,
    )

    # 原物理来源：OrderColor.ProductionID
    default_route = models.ForeignKey(
        'erp_base.RouteVersion',
        verbose_name='路线版本',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_default_route_set",
        blank=True,
        null=True,
    )

    approved_recipe = models.ForeignKey(
        'erp_sampling.RecipeVersion',
        verbose_name='已确认配方版本',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_approved_recipe_set",
        blank=True,
        null=True,
    )

    # 原物理来源：OrderColor.Price
    unit_price = models.DecimalField(
        '染整价格',
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
    )

    price_unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='计价单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_price_unit_set",
        blank=True,
        null=True,
    )

    # 原物理来源：OrderColor.IsFinished
    is_closed = models.BooleanField(
        '明细业务结案',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_sales_salesorderline"
        verbose_name = '订单颜色规格明细'
        verbose_name_plural = '订单颜色规格明细'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['order', 'line_number'], name='erp_sales_salesorderline_identity_uniq'),
            models.CheckConstraint(condition=Q(line_number__gt=0), name='erp_sales_salesorderline_line_number_positive'),
            models.CheckConstraint(condition=Q(ordered_quantity__gt=0), name='erp_sales_salesorderline_ordered_quantity_positive'),
        ]

    def clean(self):
        super().clean()
        if self.required_raw_quantity is not None and self.required_raw_unit_id is None:
            raise ValidationError({'required_raw_unit': '已填写数量时必须明确计量单位。'})


class SalesLineRequirement(ErpModel):
    """订单技术要求。"""

    order_line = models.ForeignKey(
        'erp_sales.SalesOrderLine',
        verbose_name='订单明细',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_order_line_set",
    )

    # 原物理来源：OrderAtte.FieldType
    namespace = models.CharField(
        '基础数据类别',
        max_length=20,
    )

    # 原物理来源：OrderAtte.AtteCode
    requirement_code = models.CharField(
        '事项代码',
        max_length=10,
    )

    # 原物理来源：OrderAtte.Description
    name = models.CharField(
        '描述',
        max_length=500,
        blank=True,
        null=True,
    )

    # 原物理来源：OrderAtte.AtteValue
    value_text = models.CharField(
        '事项内容',
        max_length=500,
    )

    class Meta:
        db_table = "erp_sales_saleslinerequirement"
        verbose_name = '订单技术要求'
        verbose_name_plural = '订单技术要求'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['order_line', 'namespace', 'requirement_code'], name='erp_sales_saleslinerequirement_identity_uniq'),
        ]


class SalesOrderChange(ErpModel):
    """订单变更。"""

    order = models.ForeignKey(
        'erp_sales.SalesOrder',
        verbose_name='订单',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_order_set",
    )

    change_number = models.CharField(
        '变更号',
        max_length=64,
        unique=True,
    )

    requested_at = models.DateTimeField(
        '申请时间',
    )

    reason = models.TextField(
        '变更原因',
    )

    status = models.CharField(
        '变更状态',
        max_length=24,
        choices=choices.ApprovalStatus.choices,
        default=choices.ApprovalStatus.DRAFT,
    )

    confirmed_by = models.ForeignKey(
        'erp_base.Employee',
        verbose_name='确认人',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_confirmed_by_set",
        blank=True,
        null=True,
    )

    confirmed_at = models.DateTimeField(
        '确认时间',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_sales_salesorderchange"
        verbose_name = '订单变更'
        verbose_name_plural = '订单变更'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(status__in=choices.ApprovalStatus.values), name='erp_sales_salesorderchange_status_valid'),
        ]


class SalesOrderChangeLine(ErpModel):
    """订单变更明细。"""

    before_values = models.JSONField('变更前订单事实', default=dict, blank=True)

    change = models.ForeignKey(
        'erp_sales.SalesOrderChange',
        verbose_name='变更单',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_change_set",
    )

    order_line = models.ForeignKey(
        'erp_sales.SalesOrderLine',
        verbose_name='原订单明细',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_order_line_set",
    )

    new_quantity = models.DecimalField(
        '变更后的订货数量',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    new_due_at = models.DateTimeField(
        '变更后的交期',
        blank=True,
        null=True,
    )

    new_requirements = models.TextField(
        '变更后的要求',
        blank=True,
    )

    class Meta:
        db_table = "erp_sales_salesorderchangeline"
        verbose_name = '订单变更明细'
        verbose_name_plural = '订单变更明细'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['change', 'order_line'], name='erp_sales_salesorderchangeline_identity_uniq'),
            models.CheckConstraint(condition=Q(new_quantity__isnull=False) | Q(new_due_at__isnull=False) | ~Q(new_requirements=""), name='erp_sales_salesorderchangeline_has_change'),
        ]

    def clean(self):
        super().clean()
        if self.change_id is not None and self.order_line_id is not None and self.change.order_id != self.order_line.order_id:
            raise ValidationError({'order_line': '变更明细必须属于原订单。'})


class CommercialPrice(ErpModel):
    """客户报价与加工价格。"""

    kind = models.CharField(
        '价格资料类别',
        max_length=24,
        choices=choices.PriceDocumentKind.choices,
    )

    # 原物理来源：FixedPrice.SheetNo; Quote.SheetNo
    number = models.CharField(
        '价格资料号',
        max_length=64,
        unique=True,
    )

    # 原物理来源：FixedPrice.CustomerID; Quote.CustomerID
    customer = models.ForeignKey(
        'erp_base.Party',
        verbose_name='客户',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_customer_set",
    )

    # 原物理来源：FixedPrice.SheetDate; Quote.SheetDate
    document_at = models.DateTimeField(
        '资料时间',
        blank=True,
        null=True,
    )

    # 原物理来源：FixedPrice.RightStatus; Quote.RightStatus
    status = models.CharField(
        '状态',
        max_length=24,
        choices=choices.ApprovalStatus.choices,
        default=choices.ApprovalStatus.DRAFT,
    )

    class Meta:
        db_table = "erp_sales_commercialprice"
        verbose_name = '客户报价与加工价格'
        verbose_name_plural = '客户报价与加工价格'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(kind__in=choices.PriceDocumentKind.values), name='erp_sales_commercialprice_kind_valid'),
            models.CheckConstraint(condition=Q(status__in=choices.ApprovalStatus.values), name='erp_sales_commercialprice_status_valid'),
        ]
        indexes = [
            models.Index(fields=['status', 'document_at'], name='sal_commercialprice_1'),
        ]


class CommercialPriceLine(ErpModel):
    """客户价格版本明细。"""

    # 原物理来源：FixedPriceDetail.SheetSeries; QuoteDetail.SheetSeries
    price_document = models.ForeignKey(
        'erp_sales.CommercialPrice',
        verbose_name='价格资料',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_price_document_set",
    )

    line_number = models.IntegerField(
        '价格项目行号',
    )

    # 原物理来源：FixedPriceDetail.ProdID; QuoteDetail.ProdID
    material = models.ForeignKey(
        'erp_base.Material',
        verbose_name='物料',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_material_set",
    )

    # 原物理来源：FixedPriceDetail.ColorNum; QuoteDetail.ColorNum
    color_standard = models.ForeignKey(
        'erp_base.ColorStandard',
        verbose_name='色号',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_color_standard_set",
        blank=True,
        null=True,
    )

    version = models.IntegerField(
        '版本号',
        default=1,
    )

    # 原物理来源：FixedPriceDetail.Price; QuoteDetail.Price
    confirmed_base_price = models.DecimalField(
        '客确基础单价',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：FixedPriceDetail.ProcessPrice; QuoteDetail.ProcessPrice
    additional_price = models.DecimalField(
        '另计单价',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：FixedPriceDetail.ProcessMemo; QuoteDetail.ProcessMemo
    additional_price_description = models.TextField(
        '另计或套价项目说明',
        blank=True,
    )

    # 原物理来源：FixedPriceDetail.CusPrice; QuoteDetail.CusPrice
    customer_quote_price = models.DecimalField(
        '对客报价',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：FixedPriceDetail.Pricesum; QuoteDetail.Pricesum
    unit_price = models.DecimalField(
        '采用合同总单价快照',
        max_digits=20,
        decimal_places=6,
    )

    # 原物理来源：FixedPriceDetail.PriceUnit; QuoteDetail.PriceUnit
    unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='计价单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_unit_set",
    )

    # 原物理来源：FixedPriceDetail.StartDate; QuoteDetail.StartDate
    valid_from = models.DateTimeField(
        '生效时间',
        blank=True,
        null=True,
    )

    valid_to = models.DateTimeField(
        '失效时间',
        blank=True,
        null=True,
    )

    # 原物理来源：FixedPriceDetail.IsConfirmed; QuoteDetail.IsConfirmed
    is_confirmed = models.BooleanField(
        '已确认价格',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_sales_commercialpriceline"
        verbose_name = '客户价格版本明细'
        verbose_name_plural = '客户价格版本明细'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['price_document', 'line_number', 'version'], name='erp_sales_commercialpriceline_identity_uniq'),
            models.CheckConstraint(condition=Q(line_number__gt=0), name='erp_sales_commercialpriceline_line_number_positive'),
            models.CheckConstraint(condition=Q(version__gt=0), name='erp_sales_commercialpriceline_version_positive'),
            models.CheckConstraint(condition=Q(valid_from__isnull=True) | Q(valid_to__isnull=True) | Q(valid_to__gt=F("valid_from")), name='erp_sales_commercialpriceline_valid_interval'),
            models.CheckConstraint(condition=Q(unit_price__gte=0), name='erp_sales_commercialpriceline_unit_price_nonnegative'),
        ]

    @property
    def calculated_unit_price(self):
        if self.confirmed_base_price is None or self.additional_price is None:
            return None
        return self.confirmed_base_price + self.additional_price


class Delivery(ErpModel):
    """送货单。"""

    # 原物理来源：ProdOut.SheetNo
    number = models.CharField(
        '表单编号',
        max_length=20,
        unique=True,
    )

    # 原物理来源：ProdOut.SheetDate
    document_at = models.DateTimeField(
        '单据日期',
    )

    # 原物理来源：ProdOut.CustomerID
    customer = models.ForeignKey(
        'erp_base.Party',
        verbose_name='客户',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_customer_set",
    )

    address_snapshot = models.TextField(
        '送货地址快照',
        blank=True,
    )

    # 原物理来源：ProdOut.SheetStatus
    status = models.CharField(
        '交付状态',
        max_length=24,
        choices=choices.DeliveryStatus.choices,
        default=choices.DeliveryStatus.DRAFT,
    )

    delivered_at = models.DateTimeField(
        '客户交付时间',
        blank=True,
        null=True,
    )

    warehouse_issue = models.OneToOneField(
        'erp_warehouse.StockIssue',
        verbose_name='实际库存出库单',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_warehouse_issue_set",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_sales_delivery"
        verbose_name = '送货单'
        verbose_name_plural = '送货单'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(status__in=choices.DeliveryStatus.values), name='erp_sales_delivery_status_valid'),
        ]
        indexes = [
            models.Index(fields=['status', 'document_at'], name='sal_delivery_1'),
        ]


class DeliveryLine(ErpModel):
    """送货明细。"""

    # 原物理来源：ProdOutDetail.SheetSeries
    delivery = models.ForeignKey(
        'erp_sales.Delivery',
        verbose_name='送货单',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_delivery_set",
    )

    line_number = models.IntegerField(
        '行号',
    )

    # 原物理来源：ProdOutDetail.CheckNo
    order_line = models.ForeignKey(
        'erp_sales.SalesOrderLine',
        verbose_name='订单明细',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_order_line_set",
    )

    quantity = models.DecimalField(
        '本次计划交付量',
        max_digits=20,
        decimal_places=6,
    )

    unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='交付单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_unit_set",
    )

    # 原物理来源：ProdOutDetail.Price
    unit_price_snapshot = models.DecimalField(
        '价格',
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_sales_deliveryline"
        verbose_name = '送货明细'
        verbose_name_plural = '送货明细'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['delivery', 'line_number'], name='erp_sales_deliveryline_identity_uniq'),
            models.CheckConstraint(condition=Q(line_number__gt=0), name='erp_sales_deliveryline_line_number_positive'),
            models.CheckConstraint(condition=Q(quantity__gt=0), name='erp_sales_deliveryline_quantity_positive'),
        ]

    def clean(self):
        super().clean()
        if self.order_line_id is not None and self.delivery_id is not None:
            if self.order_line.order.customer_id != self.delivery.customer_id:
                raise ValidationError({'order_line': '送货明细必须属于本送货客户。'})


class SalesReturn(ErpModel):
    """客户退回单。"""

    number = models.CharField(
        '退回单号',
        max_length=64,
        unique=True,
    )

    customer = models.ForeignKey(
        'erp_base.Party',
        verbose_name='客户',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_customer_set",
    )

    returned_at = models.DateTimeField(
        '退回时间',
    )

    reason = models.TextField(
        '退回原因',
    )

    status = models.CharField(
        '退回状态',
        max_length=24,
        choices=choices.ReturnStatus.choices,
        default=choices.ReturnStatus.DRAFT,
    )

    class Meta:
        db_table = "erp_sales_salesreturn"
        verbose_name = '客户退回单'
        verbose_name_plural = '客户退回单'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(status__in=choices.ReturnStatus.values), name='erp_sales_salesreturn_status_valid'),
        ]


class SalesReturnLine(ErpModel):
    """客户退回明细。"""

    return_order = models.ForeignKey(
        'erp_sales.SalesReturn',
        verbose_name='退回单',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_return_order_set",
    )

    original_delivery_line = models.ForeignKey(
        'erp_sales.DeliveryLine',
        verbose_name='原送货明细',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_original_delivery_line_set",
    )

    quantity = models.DecimalField(
        '退回量',
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
        verbose_name='实际收回入库行',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_receipt_line_set",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_sales_salesreturnline"
        verbose_name = '客户退回明细'
        verbose_name_plural = '客户退回明细'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(quantity__gt=0), name='erp_sales_salesreturnline_quantity_positive'),
        ]

    def clean(self):
        super().clean()
        if self.return_order_id is not None and self.original_delivery_line_id is not None:
            if self.return_order.customer_id != self.original_delivery_line.delivery.customer_id:
                raise ValidationError({'original_delivery_line': '退回来源必须属于本客户。'})


class CustomerComplaint(ErpModel):
    """客户投诉。"""

    # 原物理来源：CustomerTS.SheetNo
    number = models.CharField(
        '表单号',
        max_length=50,
        unique=True,
    )

    # 原物理来源：CustomerTS.CustomerID
    customer = models.ForeignKey(
        'erp_base.Party',
        verbose_name='客户',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_customer_set",
    )

    # 原物理来源：CustomerTS.SheetDate
    complained_at = models.DateTimeField(
        '单据日期',
    )

    # 原物理来源：CustomerTS.Remarks
    content = models.CharField(
        '备注',
        max_length=500,
        blank=True,
        null=True,
    )

    status = models.CharField(
        '处理状态',
        max_length=24,
        choices=choices.ComplaintStatus.choices,
        default=choices.ComplaintStatus.OPEN,
    )

    class Meta:
        db_table = "erp_sales_customercomplaint"
        verbose_name = '客户投诉'
        verbose_name_plural = '客户投诉'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(status__in=choices.ComplaintStatus.values), name='erp_sales_customercomplaint_status_valid'),
        ]


class CustomerComplaintLine(ErpModel):
    """客户投诉明细。"""

    # 原物理来源：CustomerTSDetail.Sheetseries
    complaint = models.ForeignKey(
        'erp_sales.CustomerComplaint',
        verbose_name='客诉单',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_complaint_set",
    )

    line_number = models.IntegerField(
        '行号',
    )

    # 原物理来源：CustomerTSDetail.JobSheetNo
    work_card = models.ForeignKey(
        'erp_production.WorkCard',
        verbose_name='工卡',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_work_card_set",
        blank=True,
        null=True,
    )

    # 原物理来源：CustomerTSDetail.BarCode
    package = models.ForeignKey(
        'erp_warehouse.Package',
        verbose_name='投诉包装',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_package_set",
        blank=True,
        null=True,
    )

    # 原物理来源：CustomerTSDetail.ProdID
    material = models.ForeignKey(
        'erp_base.Material',
        verbose_name='物料',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_material_set",
        blank=True,
        null=True,
    )

    order_line = models.ForeignKey(
        'erp_sales.SalesOrderLine',
        verbose_name='订单明细',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_order_line_set",
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

    # 原物理来源：CustomerTSDetail.Qty
    quantity = models.DecimalField(
        '数量',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='涉及单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_unit_set",
        blank=True,
        null=True,
    )

    # 原物理来源：CustomerTSDetail.Remarks
    content = models.CharField(
        '投诉问题',
        max_length=526,
    )

    # 原物理来源：CustomerTSDetail.Result
    handling_text = models.CharField(
        '处理意见',
        max_length=526,
        blank=True,
        null=True,
    )

    disposition = models.ForeignKey(
        'erp_production.QualityDisposition',
        verbose_name='质量处置',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_disposition_set",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_sales_customercomplaintline"
        verbose_name = '客户投诉明细'
        verbose_name_plural = '客户投诉明细'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['complaint', 'line_number'], name='erp_sales_customercomplaintline_identity_uniq'),
            models.CheckConstraint(condition=Q(line_number__gt=0), name='erp_sales_customercomplaintline_line_number_positive'),
        ]
