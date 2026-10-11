"""基础信息模型；字段来源见 docs/ERP模型实施说明.md。"""
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q
from core.models import CoreModel
from . import choices


class ErpModel(CoreModel):
    remarks = models.TextField("业务备注", blank=True)
    legacy_id = models.TextField(
        "旧系统id",
        blank=True,
        null=True,
        help_text="旧来源的 JSON 文本：schema、table、key；复合主键保留全部键列，新建业务留空。",
    )

    class Meta:
        abstract = True
        ordering = ["-id"]


class BusinessAction(ErpModel):
    """业务动作发生时保存事实快照，不覆盖原操作记录。"""
    entity = models.CharField('业务对象', max_length=100)
    object_id = models.BigIntegerField('对象ID')
    action = models.CharField('动作', max_length=64)
    reason = models.TextField('原因', blank=True)
    before = models.JSONField('操作前事实')
    after = models.JSONField('操作后事实')

    class Meta:
        db_table = 'erp_base_businessaction'
        verbose_name = verbose_name_plural = '业务操作记录'
        ordering = ['-id']
        indexes = [models.Index(fields=['entity', 'object_id'], name='erp_business_action_source')]


class BusinessUnit(ErpModel):
    """经营单位。"""

    code = models.CharField(
        '经营单位代码',
        max_length=64,
        unique=True,
    )

    name = models.CharField(
        '经营单位名称',
        max_length=200,
    )

    department = models.ForeignKey(
        'system.Dept',
        verbose_name='平台归属部门',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_department_set",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        '启用',
        default=True,
    )

    class Meta:
        db_table = "erp_base_businessunit"
        verbose_name = '经营单位'
        verbose_name_plural = '经营单位'
        ordering = ["-id"]


class Factory(ErpModel):
    """工厂。"""

    # 原物理来源：p_Stuff.FactID
    code = models.CharField(
        '工厂代码',
        max_length=10,
        unique=True,
    )

    name = models.CharField(
        '工厂名称',
        max_length=200,
    )

    business_unit = models.ForeignKey(
        'erp_base.BusinessUnit',
        verbose_name='经营单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_business_unit_set",
        blank=True,
        null=True,
    )

    department = models.ForeignKey(
        'system.Dept',
        verbose_name='平台部门',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_department_set",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        '启用',
        default=True,
    )

    class Meta:
        db_table = "erp_base_factory"
        verbose_name = '工厂'
        verbose_name_plural = '工厂'
        ordering = ["-id"]


class Employee(ErpModel):
    """业务员工。"""

    # 原物理来源：h_Employee.EmpID
    code = models.CharField(
        '员工编码',
        max_length=50,
        unique=True,
    )

    # 原物理来源：h_Employee.Name
    name = models.CharField(
        '员工姓名',
        max_length=60,
        blank=True,
        null=True,
    )

    # 原物理来源：h_Employee.NameE
    english_name = models.CharField(
        '英文姓名',
        max_length=128,
        blank=True,
        null=True,
    )

    user = models.OneToOneField(
        'system.Users',
        verbose_name='平台登录账号',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_user_set",
        blank=True,
        null=True,
    )

    # 原物理来源：h_Employee.DeptID
    department = models.ForeignKey(
        'system.Dept',
        verbose_name='部门',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_department_set",
        blank=True,
        null=True,
    )

    # 原物理来源：h_Employee.BusinessUnitID
    business_unit = models.ForeignKey(
        'erp_base.BusinessUnit',
        verbose_name='经营单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_business_unit_set",
        blank=True,
        null=True,
    )

    # 原物理来源：h_Employee.ShiftID
    shift = models.ForeignKey(
        'erp_base.Shift',
        verbose_name='默认班次',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_shift_set",
        blank=True,
        null=True,
    )

    # 原物理来源：h_Employee.Mobile
    mobile = models.CharField(
        '移动电话',
        max_length=15,
        blank=True,
        null=True,
    )

    # 原物理来源：h_Employee.RFID
    card_identifier = models.CharField(
        'IC卡号',
        max_length=64,
        blank=True,
        null=True,
    )

    # 原物理来源：h_Employee.InDate
    joined_on = models.DateTimeField(
        '进厂日期',
        blank=True,
        null=True,
    )

    # 原物理来源：h_Employee.OutDate
    left_on = models.DateTimeField(
        '离职日期',
        blank=True,
        null=True,
    )

    # 原物理来源：h_Employee.IsOut
    is_active = models.BooleanField(
        '在岗启用',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_base_employee"
        verbose_name = '业务员工'
        verbose_name_plural = '业务员工'
        ordering = ["-id"]


class Shift(ErpModel):
    """班次。"""

    # 原物理来源：p_Shift.ShiftID
    code = models.CharField(
        '班组代码',
        max_length=10,
        unique=True,
    )

    # 原物理来源：p_Shift.Name
    name = models.CharField(
        '名称',
        max_length=60,
        blank=True,
        null=True,
    )

    business_unit = models.ForeignKey(
        'erp_base.BusinessUnit',
        verbose_name='经营单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_business_unit_set",
        blank=True,
        null=True,
    )

    starts_at = models.TimeField(
        '每日开始时间',
        blank=True,
        null=True,
    )

    ends_at = models.TimeField(
        '每日结束时间',
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        '启用',
        default=True,
    )

    class Meta:
        db_table = "erp_base_shift"
        verbose_name = '班次'
        verbose_name_plural = '班次'
        ordering = ["-id"]


class Party(ErpModel):
    """客户和供应商主体。"""

    # 原物理来源：p_Customer.CustomerID
    code = models.CharField(
        '往来单位代码',
        max_length=10,
        unique=True,
    )

    # 原物理来源：p_Customer.NameC
    name = models.CharField(
        '中文名称',
        max_length=128,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Customer.NameE
    english_name = models.CharField(
        '英文名称',
        max_length=128,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Customer.ShortName
    short_name = models.CharField(
        '客户简称',
        max_length=50,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Customer.Mnemonic
    mnemonic = models.CharField(
        '助记符',
        max_length=30,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Customer.ParentCustID
    parent = models.ForeignKey(
        'erp_base.Party',
        verbose_name='上级主体',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_parent_set",
        blank=True,
        null=True,
    )

    # 原物理来源：p_Customer.SalerID
    salesperson = models.ForeignKey(
        'erp_base.Employee',
        verbose_name='默认业务员',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_salesperson_set",
        blank=True,
        null=True,
    )

    # 原物理来源：p_Customer.CustKindID
    category = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='主体类别',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_category_set",
        blank=True,
        null=True,
    )

    # 原物理来源：p_Customer.Tel
    phone = models.CharField(
        '电话',
        max_length=50,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Customer.Fax
    fax = models.CharField(
        '传真',
        max_length=20,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Customer.Email
    email = models.CharField(
        'Email',
        max_length=60,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Customer.WebSite
    website = models.CharField(
        '网站',
        max_length=60,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Customer.IsAbroad
    automatic_packaging = models.BooleanField(
        '自动包装',
        blank=True,
        null=True,
    )

    # 原物理来源：p_Customer.LabelID
    default_label = models.ForeignKey(
        'erp_base.LabelTemplate',
        verbose_name='默认标签模板',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_default_label_set",
        blank=True,
        null=True,
    )

    # 原物理来源：p_Customer.EnableOrders
    orders_enabled = models.BooleanField(
        '是否启用订单',
        blank=True,
        null=True,
    )

    # 原物理来源：p_Customer.IsStop
    is_active = models.BooleanField(
        '启用',
        blank=True,
        null=True,
    )

    # 原物理来源：p_Customer.StopDate
    stopped_at = models.DateTimeField(
        '停用时间',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_base_party"
        verbose_name = '客户和供应商主体'
        verbose_name_plural = '客户和供应商主体'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(parent__isnull=True) | ~Q(parent=F("pk")), name='erp_base_party_parent_not_self'),
        ]


class PartyRole(ErpModel):
    """往来单位业务角色。"""

    party = models.ForeignKey(
        'erp_base.Party',
        verbose_name='主体',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_party_set",
    )

    role = models.CharField(
        '业务角色',
        max_length=24,
        choices=choices.PartyRole.choices,
    )

    is_active = models.BooleanField(
        '启用',
        default=True,
    )

    class Meta:
        db_table = "erp_base_partyrole"
        verbose_name = '往来单位业务角色'
        verbose_name_plural = '往来单位业务角色'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['party', 'role'], name='erp_base_partyrole_identity_uniq'),
            models.CheckConstraint(condition=Q(role__in=choices.PartyRole.values), name='erp_base_partyrole_role_valid'),
        ]


class PartyContact(ErpModel):
    """往来联系人。"""

    party = models.ForeignKey(
        'erp_base.Party',
        verbose_name='主体',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_party_set",
    )

    # 原物理来源：p_Customer.Contact
    name = models.CharField(
        '联系人',
        max_length=50,
    )

    phone = models.CharField(
        '联系人电话',
        max_length=100,
        blank=True,
    )

    email = models.CharField(
        '联系人邮箱',
        max_length=255,
        blank=True,
    )

    position = models.CharField(
        '职务',
        max_length=100,
        blank=True,
    )

    is_default = models.BooleanField(
        '默认联系人',
        default=False,
    )

    class Meta:
        db_table = "erp_base_partycontact"
        verbose_name = '往来联系人'
        verbose_name_plural = '往来联系人'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['party'], name='erp_base_partycontact_default_uniq', condition=Q(is_default=True)),
        ]


class PartyAddress(ErpModel):
    """业务地址。"""

    party = models.ForeignKey(
        'erp_base.Party',
        verbose_name='主体',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_party_set",
    )

    kind = models.CharField(
        '地址类型',
        max_length=24,
        choices=choices.AddressKind.choices,
    )

    # 原物理来源：p_Customer.Addr; p_Customer.AddrDlv
    address = models.TextField(
        '完整地址',
    )

    # 原物理来源：p_Customer.AddrE
    english_address = models.CharField(
        '英文地址名',
        max_length=160,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Customer.Zip
    postal_code = models.CharField(
        '邮编',
        max_length=10,
        blank=True,
        null=True,
    )

    contact = models.ForeignKey(
        'erp_base.PartyContact',
        verbose_name='联系人',
        on_delete=models.RESTRICT,
        related_name="%(app_label)s_%(class)s_contact_set",
        blank=True,
        null=True,
    )

    is_default = models.BooleanField(
        '该类型默认',
        default=False,
    )

    class Meta:
        db_table = "erp_base_partyaddress"
        verbose_name = '业务地址'
        verbose_name_plural = '业务地址'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['party', 'kind'], name='erp_base_partyaddress_default_uniq', condition=Q(is_default=True)),
            models.CheckConstraint(condition=Q(kind__in=choices.AddressKind.values), name='erp_base_partyaddress_kind_valid'),
        ]

    def clean(self):
        super().clean()
        if self.contact_id is not None and self.contact.party_id != self.party_id:
            raise ValidationError({'contact': '联系人必须属于本往来单位。'})


class BusinessChoice(ErpModel):
    """业务代码字典。"""

    # 原物理来源：p_FieldValid.FieldType
    namespace = models.CharField(
        '数据类型',
        max_length=20,
    )

    # 原物理来源：p_FieldValid.Code
    code = models.CharField(
        '编码',
        max_length=20,
    )

    # 原物理来源：p_FieldValid.Name
    name = models.CharField(
        '名称',
        max_length=100,
    )

    # 原物理来源：p_FieldValid.NumValue
    numeric_value = models.DecimalField(
        '数值值',
        max_digits=18,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：p_FieldValid.ParentCode
    parent = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='上级字典项',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_parent_set",
        blank=True,
        null=True,
    )

    # 原物理来源：p_FieldValid.SortValue
    sort = models.IntegerField(
        '排序值',
        blank=True,
        null=True,
    )

    # 原物理来源：p_FieldValid.IsStop
    is_active = models.BooleanField(
        '启用',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_base_businesschoice"
        verbose_name = '业务代码字典'
        verbose_name_plural = '业务代码字典'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['namespace', 'code'], name='erp_base_businesschoice_identity_uniq'),
            models.CheckConstraint(condition=Q(parent__isnull=True) | ~Q(parent=F("pk")), name='erp_base_businesschoice_parent_not_self'),
        ]

    def clean(self):
        super().clean()
        if self.parent_id is not None and self.parent.namespace != self.namespace:
            raise ValidationError({'parent': '上级字典必须属于同一类型。'})


class Unit(ErpModel):
    """计量单位。"""

    code = models.CharField(
        '新单位代码',
        max_length=32,
        unique=True,
    )

    name = models.CharField(
        '单位名称',
        max_length=100,
    )

    dimension = models.CharField(
        '计量维度',
        max_length=24,
        choices=choices.UnitDimension.choices,
    )

    base_unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='同维度基准单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_base_unit_set",
        blank=True,
        null=True,
    )

    factor_to_base = models.DecimalField(
        '换算倍率',
        max_digits=24,
        decimal_places=12,
    )

    decimal_places = models.IntegerField(
        '显示小数位',
    )

    is_active = models.BooleanField(
        '启用',
        default=True,
    )

    class Meta:
        db_table = "erp_base_unit"
        verbose_name = '计量单位'
        verbose_name_plural = '计量单位'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(dimension__in=choices.UnitDimension.values), name='erp_base_unit_dimension_valid'),
            models.CheckConstraint(condition=Q(base_unit__isnull=True) | ~Q(base_unit=F("pk")), name='erp_base_unit_base_unit_not_self'),
            models.CheckConstraint(condition=Q(factor_to_base__gt=0), name='erp_base_unit_factor_positive'),
            models.CheckConstraint(condition=Q(decimal_places__gte=0), name='erp_base_unit_display_nonnegative'),
            models.CheckConstraint(condition=Q(base_unit__isnull=False) | Q(factor_to_base=1), name='erp_base_unit_base_factor_one'),
        ]

    def clean(self):
        super().clean()
        if self.base_unit_id is not None:
            if self.base_unit.dimension != self.dimension or self.base_unit.base_unit_id is not None:
                raise ValidationError({'base_unit': '必须引用同维度的基准单位。'})
        if self.dimension == choices.UnitDimension.TEMPERATURE and (self.base_unit_id is not None or self.factor_to_base != 1):
            raise ValidationError({'factor_to_base': '首期温度仅使用摄氏度基准单位。'})

    def convert_quantity(self, quantity, target_unit):
        if self.dimension != target_unit.dimension:
            raise ValidationError('不同计量维度不能换算。')
        source_base = self.pk if self.base_unit_id is None else self.base_unit_id
        target_base = target_unit.pk if target_unit.base_unit_id is None else target_unit.base_unit_id
        if source_base != target_base:
            raise ValidationError('换算单位必须引用同一个基准单位。')
        return quantity * self.factor_to_base / target_unit.factor_to_base


class Material(ErpModel):
    """物料和产品。"""

    # 原物理来源：p_Gray.GrayID; p_Stuff.StuffID; p_Article.ArticleID
    code = models.CharField(
        '新物料代码',
        max_length=200,
        unique=True,
    )

    # 原物理来源：p_Gray.NameC; p_Stuff.Name; p_Article.Name
    name = models.CharField(
        '名称',
        max_length=255,
    )

    # 原物理来源：p_Stuff.NameE; p_Article.NameE
    english_name = models.CharField(
        '英文名称',
        max_length=255,
        blank=True,
    )

    kind = models.CharField(
        '物料类型',
        max_length=24,
        choices=choices.MaterialKind.choices,
    )

    # 原物理来源：p_Gray.Spec; p_Stuff.Spec; p_Article.Spec
    specification = models.TextField(
        '规格描述',
        blank=True,
    )

    # 原物理来源：p_Gray.FabricKindID; p_Stuff.StuffKindID; p_Article.ArticleKindID
    category = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='业务分类',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_category_set",
        blank=True,
        null=True,
    )

    # 原物理来源：p_Gray.StockUnit; p_Stuff.StockUnit; p_Article.Unit
    stock_unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='库存基本单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_stock_unit_set",
    )

    # 原物理来源：p_Stuff.IsBatch; p_Article.IsBatch
    batch_managed = models.BooleanField(
        '批次管理',
        blank=True,
        null=True,
    )

    # 原物理来源：p_Stuff.SupplierID; p_Article.SupplierID
    default_supplier = models.ForeignKey(
        'erp_base.Party',
        verbose_name='默认供应商',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_default_supplier_set",
        blank=True,
        null=True,
    )

    # 原物理来源：p_Stuff.SafeQty; p_Article.SafeQty
    safety_quantity = models.DecimalField(
        '安全库存量',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Stuff.LeadDays; p_Article.LeadDays
    lead_days = models.IntegerField(
        '供货前置天数',
        blank=True,
        null=True,
    )

    # 原物理来源：p_Gray.Mnemonic; p_Stuff.Mnemonic; p_Article.Mnemonic
    mnemonic = models.CharField(
        '助记码',
        max_length=100,
        blank=True,
    )

    # 原物理来源：p_Gray.IsStop
    is_active = models.BooleanField(
        '启用',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_base_material"
        verbose_name = '物料和产品'
        verbose_name_plural = '物料和产品'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(kind__in=choices.MaterialKind.values), name='erp_base_material_kind_valid'),
        ]


class YarnSpecification(ErpModel):
    """纱线和织物规格。"""

    material = models.OneToOneField(
        'erp_base.Material',
        verbose_name='物料',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_material_set",
    )

    # 原物理来源：p_Gray.Structure
    structure = models.CharField(
        '组织',
        max_length=50,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Gray.CustSelfProduct
    customer_specification = models.CharField(
        '客户规格',
        max_length=150,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Gray.FatherGrayID
    parent_material = models.ForeignKey(
        'erp_base.Material',
        verbose_name='原规格物料',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_parent_material_set",
        blank=True,
        null=True,
    )

    # 原物理来源：p_Gray.GrayWeight
    raw_areal_mass = models.DecimalField(
        '胚纱克重',
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Gray.ProdWeight
    finished_areal_mass = models.DecimalField(
        '成品克重',
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Gray.Density
    density_description = models.CharField(
        '密度',
        max_length=20,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Gray.WidthDn
    width_lower = models.DecimalField(
        '门幅下限',
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Gray.WidthUp
    width_upper = models.DecimalField(
        '门幅上限',
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
    )

    width_unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='确认门幅单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_width_unit_set",
        blank=True,
        null=True,
    )

    # 原物理来源：p_Gray.FabricStyleID
    style = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='风格分类',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_style_set",
        blank=True,
        null=True,
    )

    # 原物理来源：p_Gray.Graphic
    pattern_file = models.ForeignKey(
        'system.FileList',
        verbose_name='图案文件',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_pattern_file_set",
        blank=True,
        null=True,
    )

    # 原物理来源：p_Gray.JNKind
    twisting_class = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='加捻分类',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_twisting_class_set",
        blank=True,
        null=True,
    )

    # 原物理来源：p_Gray.STKind
    loose_winding_class = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='松筒分类',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_loose_winding_class_set",
        blank=True,
        null=True,
    )

    # 原物理来源：p_Gray.RSKind
    dyeing_class = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='染色分类',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_dyeing_class_set",
        blank=True,
        null=True,
    )

    # 原物理来源：p_Gray.ZTKind
    loading_class = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='装缸脱水分类',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_loading_class_set",
        blank=True,
        null=True,
    )

    # 原物理来源：p_Gray.JTKind
    rewinding_class = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='紧筒分类',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_rewinding_class_set",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_base_yarnspecification"
        verbose_name = '纱线和织物规格'
        verbose_name_plural = '纱线和织物规格'
        ordering = ["-id"]

    def clean(self):
        super().clean()
        if self.material_id is not None and self.material.kind not in [choices.MaterialKind.YARN, choices.MaterialKind.FABRIC]:
            raise ValidationError({'material': '物料类型与本规格资料不一致。'})


class ChemicalSpecification(ErpModel):
    """染化料资料。"""

    material = models.OneToOneField(
        'erp_base.Material',
        verbose_name='物料',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_material_set",
    )

    # 原物理来源：p_Stuff.StuffType
    chemical_type = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='染化料类型',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_chemical_type_set",
        blank=True,
        null=True,
    )

    # 原物理来源：p_Stuff.Brand
    brand = models.CharField(
        '牌号',
        max_length=20,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Stuff.WOF
    strength_value = models.DecimalField(
        '力份',
        max_digits=6,
        decimal_places=3,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Stuff.RecipeUnit
    default_dosage_basis = models.CharField(
        '默认配方计量基准',
        max_length=24,
        choices=choices.DosageBasis.choices,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Stuff.WeightMode
    weighing_mode_code = models.CharField(
        '称料方式',
        max_length=32,
        blank=True,
    )

    # 原物理来源：p_Stuff.AutoSysID
    dispensing_code = models.CharField(
        '配送方式',
        max_length=10,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Stuff.WeightNo
    weighing_system_code = models.CharField(
        '称料系统编号',
        max_length=20,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Stuff.CupNo
    cup_code = models.CharField(
        '滴液系统编号',
        max_length=20,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Stuff.GaoLaodu
    is_high_fastness = models.BooleanField(
        '高牢度',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_base_chemicalspecification"
        verbose_name = '染化料资料'
        verbose_name_plural = '染化料资料'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(default_dosage_basis__isnull=True) | Q(default_dosage_basis__in=choices.DosageBasis.values), name='erp_base_chemicalspecification_default_dosage_basis_valid'),
        ]

    def clean(self):
        super().clean()
        if self.material_id is not None and self.material.kind not in [choices.MaterialKind.CHEMICAL]:
            raise ValidationError({'material': '物料类型与本规格资料不一致。'})


class CustomerMaterial(ErpModel):
    """客户物料对照。"""

    # 原物理来源：p_Gray.CustomerID; p_Fabric_Cust.CustomerID
    customer = models.ForeignKey(
        'erp_base.Party',
        verbose_name='客户',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_customer_set",
    )

    # 原物理来源：p_Gray.GrayID
    material = models.ForeignKey(
        'erp_base.Material',
        verbose_name='本厂物料',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_material_set",
    )

    customer_code = models.CharField(
        '客户物料号',
        max_length=255,
        blank=True,
    )

    # 原物理来源：p_Gray.CustSelfProduct; OrderColor.CustSelfProduct
    customer_specification = models.CharField(
        '客户规格描述',
        max_length=255,
        blank=True,
    )

    # 原物理来源：OrderColor.CustFabricName
    customer_name = models.CharField(
        '客户规格',
        max_length=250,
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        '启用',
        default=True,
    )

    class Meta:
        db_table = "erp_base_customermaterial"
        verbose_name = '客户物料对照'
        verbose_name_plural = '客户物料对照'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['customer', 'customer_code'], name='erp_base_customermaterial_customer_code_uniq', condition=~Q(customer_code="")),
        ]


class Warehouse(ErpModel):
    """仓库。"""

    # 原物理来源：p_FieldValid.Code
    code = models.CharField(
        '编码',
        max_length=20,
    )

    # 原物理来源：p_FieldValid.Name
    name = models.CharField(
        '名称',
        max_length=100,
    )

    factory = models.ForeignKey(
        'erp_base.Factory',
        verbose_name='工厂',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_factory_set",
    )

    kind = models.CharField(
        '仓库类型',
        max_length=24,
        choices=choices.WarehouseKind.choices,
    )

    is_active = models.BooleanField(
        '启用',
        default=True,
    )

    class Meta:
        db_table = "erp_base_warehouse"
        verbose_name = '仓库'
        verbose_name_plural = '仓库'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['factory', 'code'], name='erp_base_warehouse_identity_uniq'),
            models.CheckConstraint(condition=Q(kind__in=choices.WarehouseKind.values), name='erp_base_warehouse_kind_valid'),
        ]


class StorageLocation(ErpModel):
    """库区和库位。"""

    warehouse = models.ForeignKey(
        'erp_base.Warehouse',
        verbose_name='仓库',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_warehouse_set",
    )

    # 原物理来源：p_StorageUnitID.Code
    code = models.CharField(
        '编码',
        max_length=20,
    )

    name = models.CharField(
        '位置名称',
        max_length=200,
        blank=True,
    )

    # 原物理来源：p_StorageUnitID.Name
    source_note = models.CharField(
        '旧位置备注',
        max_length=100,
        blank=True,
    )

    parent = models.ForeignKey(
        'erp_base.StorageLocation',
        verbose_name='上级位置',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_parent_set",
        blank=True,
        null=True,
    )

    kind = models.CharField(
        '位置类型',
        max_length=24,
        choices=choices.LocationKind.choices,
    )

    is_active = models.BooleanField(
        '启用',
        default=True,
    )

    class Meta:
        db_table = "erp_base_storagelocation"
        verbose_name = '库区和库位'
        verbose_name_plural = '库区和库位'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['warehouse', 'code'], name='erp_base_storagelocation_identity_uniq'),
            models.CheckConstraint(condition=Q(parent__isnull=True) | ~Q(parent=F("pk")), name='erp_base_storagelocation_parent_not_self'),
            models.CheckConstraint(condition=Q(kind__in=choices.LocationKind.values), name='erp_base_storagelocation_kind_valid'),
        ]

    def clean(self):
        super().clean()
        if self.parent_id is not None and self.parent.warehouse_id != self.warehouse_id:
            raise ValidationError({'parent': '上级位置必须属于同一仓库。'})


class WorkCenter(ErpModel):
    """工作中心。"""

    # 原物理来源：p_Process.StationID
    code = models.CharField(
        '站别代码',
        max_length=10,
    )

    name = models.CharField(
        '名称',
        max_length=200,
    )

    factory = models.ForeignKey(
        'erp_base.Factory',
        verbose_name='工厂',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_factory_set",
    )

    department = models.ForeignKey(
        'system.Dept',
        verbose_name='车间部门',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_department_set",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        '启用',
        default=True,
    )

    class Meta:
        db_table = "erp_base_workcenter"
        verbose_name = '工作中心'
        verbose_name_plural = '工作中心'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['factory', 'code'], name='erp_base_workcenter_identity_uniq'),
        ]


class Process(ErpModel):
    """工序。"""

    # 原物理来源：p_Process.ProcessID
    code = models.CharField(
        '工序代码',
        max_length=10,
        unique=True,
    )

    # 原物理来源：p_Process.Name
    name = models.CharField(
        '名称',
        max_length=60,
    )

    # 原物理来源：p_Process.StationID
    work_center = models.ForeignKey(
        'erp_base.WorkCenter',
        verbose_name='默认工作中心',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_work_center_set",
        blank=True,
        null=True,
    )

    # 原物理来源：p_Process.Unit
    quantity_unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='默认报工单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_quantity_unit_set",
        blank=True,
        null=True,
    )

    # 原物理来源：p_Process.IsNeedRecipe
    requires_recipe = models.BooleanField(
        '工序配方',
        blank=True,
        null=True,
    )

    # 原物理来源：p_Process.ToInputMachine
    requires_machine = models.BooleanField(
        '输入机台',
        blank=True,
        null=True,
    )

    # 原物理来源：p_Process.ToInputQty
    requires_quantity = models.BooleanField(
        '输入数量',
        blank=True,
        null=True,
    )

    # 原物理来源：p_Process.ToWeight
    requires_weight = models.BooleanField(
        '称重',
        blank=True,
        null=True,
    )

    # 原物理来源：p_Process.IsAllowedToBack
    allow_back_scan = models.BooleanField(
        '允许回刷',
        blank=True,
        null=True,
    )

    # 原物理来源：p_Process.CanSkip
    may_skip = models.BooleanField(
        '跳过',
        blank=True,
        null=True,
    )

    # 原物理来源：p_Process.IsODM
    is_subcontracted = models.BooleanField(
        '是否委外',
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        '启用',
        default=True,
    )

    # 原物理来源：p_Process.StopDate
    stopped_at = models.DateTimeField(
        '停用时间',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_base_process"
        verbose_name = '工序'
        verbose_name_plural = '工序'
        ordering = ["-id"]


class Machine(ErpModel):
    """生产机台。"""

    # 原物理来源：p_Machine.MachineID
    code = models.CharField(
        '机台编码',
        max_length=20,
    )

    # 原物理来源：p_Machine.MachineNo
    number = models.CharField(
        '机台编号',
        max_length=64,
        blank=True,
        null=True,

    )

    # 原物理来源：p_Machine.Name
    name = models.CharField(
        '机台名称',
        max_length=60,
        blank=True,
        null=True,
    )

    factory = models.ForeignKey(
        'erp_base.Factory',
        verbose_name='工厂',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_factory_set",
        blank=True,
        null=True,
    )

    # 原物理来源：p_Machine.BusinessUnitID
    business_unit = models.ForeignKey(
        'erp_base.BusinessUnit',
        verbose_name='经营单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_business_unit_set",
        blank=True,
        null=True,
    )

    # 原物理来源：p_Machine.StationID
    work_center = models.ForeignKey(
        'erp_base.WorkCenter',
        verbose_name='工作中心',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_work_center_set",
        blank=True,
        null=True,
    )

    # 原物理来源：p_Machine.WorkShopID
    workshop_code = models.CharField(
        '生产车间代码',
        max_length=10,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Machine.MachineKindID
    machine_kind = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='机型分类',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_machine_kind_set",
        blank=True,
        null=True,
    )

    # 原物理来源：p_Machine.Capacity
    capacity_description = models.CharField(
        '原容量描述',
        max_length=255,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Machine.MinVatQty
    load_capacity_kg = models.DecimalField(
        '可承重量kg',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    minimum_load_kg = models.DecimalField(
        '确认后的最小装载量kg',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Machine.MaxRolls
    maximum_pieces = models.DecimalField(
        '最大粒数',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Machine.MAxSpindles
    maximum_spindles = models.IntegerField(
        '最大锭数',
        blank=True,
        null=True,
    )

    # 原物理来源：p_Machine.Rate
    bath_ratio = models.DecimalField(
        '水比',
        max_digits=7,
        decimal_places=1,
        blank=True,
        null=True,
    )

    bath_ratio_basis = models.CharField(
        '默认浴比定义',
        max_length=24,
        choices=choices.BathRatioBasis.choices,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Machine.Manufacturer
    manufacturer = models.CharField(
        '制造商',
        max_length=64,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Machine.SequenceNo
    controller_number = models.CharField(
        '中控机号',
        max_length=50,
        blank=True,
        null=True,
    )

    # 原物理来源：p_Machine.IsProcess
    is_scheduled = models.BooleanField(
        '参与排产',
        blank=True,
        null=True,
    )

    # 原物理来源：p_Machine.IsStop
    is_active = models.BooleanField(
        '启用',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_base_machine"
        verbose_name = '生产机台'
        verbose_name_plural = '生产机台'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['factory', 'code'], name='erp_base_machine_identity_uniq'),
            models.CheckConstraint(condition=Q(bath_ratio_basis__isnull=True) | Q(bath_ratio_basis__in=choices.BathRatioBasis.values), name='erp_base_machine_bath_ratio_basis_valid'),
        ]

    def clean(self):
        super().clean()
        if self.work_center_id is not None and self.work_center.factory_id != self.factory_id:
            raise ValidationError({'work_center': '机台工作中心必须属于同一工厂。'})


class MachineProcess(ErpModel):
    """机台工序适用关系。"""

    machine = models.ForeignKey(
        'erp_base.Machine',
        verbose_name='机台',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_machine_set",
    )

    process = models.ForeignKey(
        'erp_base.Process',
        verbose_name='工序',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_process_set",
    )

    is_active = models.BooleanField(
        '启用',
        default=True,
    )

    class Meta:
        db_table = "erp_base_machineprocess"
        verbose_name = '机台工序适用关系'
        verbose_name_plural = '机台工序适用关系'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['machine', 'process'], name='erp_base_machineprocess_identity_uniq'),
        ]


class Route(ErpModel):
    """工艺路线。"""

    code = models.CharField(
        '路线代码',
        max_length=64,
        unique=True,
    )

    name = models.CharField(
        '路线名称',
        max_length=200,
    )

    is_active = models.BooleanField(
        '启用',
        default=True,
    )

    class Meta:
        db_table = "erp_base_route"
        verbose_name = '工艺路线'
        verbose_name_plural = '工艺路线'
        ordering = ["-id"]


class RouteVersion(ErpModel):
    """路线版本。"""

    route = models.ForeignKey(
        'erp_base.Route',
        verbose_name='路线',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_route_set",
    )

    version = models.IntegerField(
        '版本号',
        default=1,
    )

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

    status = models.CharField(
        '版本状态',
        max_length=24,
        choices=choices.VersionStatus.choices,
        default=choices.VersionStatus.DRAFT,
    )

    class Meta:
        db_table = "erp_base_routeversion"
        verbose_name = '路线版本'
        verbose_name_plural = '路线版本'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['route', 'version'], name='erp_base_routeversion_identity_uniq'),
            models.CheckConstraint(condition=Q(version__gt=0), name='erp_base_routeversion_version_positive'),
            models.CheckConstraint(condition=Q(status__in=choices.VersionStatus.values), name='erp_base_routeversion_status_valid'),
        ]


class RouteStep(ErpModel):
    """路线节点。"""

    route_version = models.ForeignKey(
        'erp_base.RouteVersion',
        verbose_name='路线版本',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_route_version_set",
    )

    # 原物理来源：JobProcess.ProcessNo
    sequence = models.IntegerField(
        '工序号',
    )

    # 原物理来源：JobProcess.ProcessID
    process = models.ForeignKey(
        'erp_base.Process',
        verbose_name='工序',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_process_set",
    )

    is_required = models.BooleanField(
        '是否必经',
    )

    predecessor = models.ForeignKey(
        'erp_base.RouteStep',
        verbose_name='直接前置节点',
        on_delete=models.RESTRICT,
        related_name="%(app_label)s_%(class)s_predecessor_set",
        blank=True,
        null=True,
    )

    standard_minutes = models.DecimalField(
        '标准时长分钟',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_base_routestep"
        verbose_name = '路线节点'
        verbose_name_plural = '路线节点'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['route_version', 'sequence'], name='erp_base_routestep_identity_uniq'),
            models.CheckConstraint(condition=Q(sequence__gt=0), name='erp_base_routestep_sequence_positive'),
            models.CheckConstraint(condition=Q(predecessor__isnull=True) | ~Q(predecessor=F("pk")), name='erp_base_routestep_predecessor_not_self'),
        ]

    def clean(self):
        super().clean()
        if self.predecessor_id is not None:
            if self.predecessor.route_version_id != self.route_version_id or self.predecessor.sequence >= self.sequence:
                raise ValidationError({'predecessor': '前置节点必须在同一对象内，且顺序早于当前节点。'})


class ColorStandard(ErpModel):
    """标准色号。"""

    # 原物理来源：P_ColorNum.ColorNo
    code = models.CharField(
        '内部色标准编号',
        max_length=50,
        unique=True,
    )

    # 原物理来源：P_ColorNum.ColorNum
    color_number = models.CharField(
        '显示色号',
        max_length=50,
    )

    # 原物理来源：P_ColorNum.CustomerID
    customer = models.ForeignKey(
        'erp_base.Party',
        verbose_name='客户',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_customer_set",
        blank=True,
        null=True,
    )

    # 原物理来源：P_ColorNum.ProdID
    material = models.ForeignKey(
        'erp_base.Material',
        verbose_name='适用物料',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_material_set",
        blank=True,
        null=True,
    )

    # 原物理来源：P_ColorNum.CustColorNum
    customer_color_number = models.CharField(
        '客户色号',
        max_length=100,
        blank=True,
        null=True,
    )

    # 原物理来源：P_ColorNum.ColorDepthID
    depth = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='色深分类',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_depth_set",
        blank=True,
        null=True,
    )

    # 原物理来源：P_ColorNum.ColorRGB
    rgb = models.IntegerField(
        '展示RGB',
        blank=True,
        null=True,
    )

    # 原物理来源：P_ColorNum.VerLight1ID
    primary_light = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='主光源',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_primary_light_set",
        blank=True,
        null=True,
    )

    # 原物理来源：P_ColorNum.VerLight2ID
    secondary_light = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='副光源',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_secondary_light_set",
        blank=True,
        null=True,
    )

    source_sample = models.ForeignKey(
        'erp_sampling.SampleLine',
        verbose_name='来源打样明细',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_source_sample_set",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        '启用',
        default=True,
    )

    class Meta:
        db_table = "erp_base_colorstandard"
        verbose_name = '标准色号'
        verbose_name_plural = '标准色号'
        ordering = ["-id"]


class PackagingSpecification(ErpModel):
    """包装规格。"""

    # 原物理来源：p_FieldValid.Code
    code = models.CharField(
        '编码',
        max_length=20,
    )

    # 原物理来源：p_FieldValid.Name
    name = models.CharField(
        '名称',
        max_length=100,
    )

    kind = models.CharField(
        '包装类型',
        max_length=24,
        choices=choices.PackagingKind.choices,
    )

    # 原物理来源：p_FieldValid.NumValue
    unit_tare_kg = models.DecimalField(
        '单件皮重kg',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：p_FieldValid.Long_CM
    length_cm = models.DecimalField(
        '长cm',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：p_FieldValid.Wide_CM
    width_cm = models.DecimalField(
        '宽cm',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：p_FieldValid.High_CM
    height_cm = models.DecimalField(
        '高cm',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：p_FieldValid.IsStop
    is_active = models.BooleanField(
        '启用',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_base_packagingspecification"
        verbose_name = '包装规格'
        verbose_name_plural = '包装规格'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['kind', 'code'], name='erp_base_packagingspecification_identity_uniq'),
            models.CheckConstraint(condition=Q(kind__in=choices.PackagingKind.values), name='erp_base_packagingspecification_kind_valid'),
        ]


class LabelTemplate(ErpModel):
    """标签模板。"""

    code = models.CharField(
        '模板代码',
        max_length=64,
    )

    name = models.CharField(
        '模板名称',
        max_length=200,
    )

    version = models.IntegerField(
        '版本号',
        default=1,
    )

    customer = models.ForeignKey(
        'erp_base.Party',
        verbose_name='专用客户',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_customer_set",
        blank=True,
        null=True,
    )

    template_file = models.ForeignKey(
        'system.FileList',
        verbose_name='模板文件',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_template_file_set",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        '启用',
        default=True,
    )

    class Meta:
        db_table = "erp_base_labeltemplate"
        verbose_name = '标签模板'
        verbose_name_plural = '标签模板'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['code', 'version'], name='erp_base_labeltemplate_identity_uniq'),
            models.CheckConstraint(condition=Q(version__gt=0), name='erp_base_labeltemplate_version_positive'),
        ]


from .legacy_models import LegacyImportBatch,LegacySourceTable,LegacyObjectMap,LegacyImportIssue
