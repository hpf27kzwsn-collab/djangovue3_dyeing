"""打样管理模型；字段来源见 docs/ERP模型实施说明.md。"""
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q
from plugins.erp_base.models import ErpModel
from plugins.erp_base import choices


class SampleRequest(ErpModel):
    """来样打样任务。"""

    # 原物理来源：DyeLabMain.SheetNo
    number = models.CharField(
        '任务单号',
        max_length=20,
        unique=True,
    )

    # 原物理来源：DyeLabMain.SheetDate
    document_at = models.DateTimeField(
        '单据日期',
    )

    # 原物理来源：DyeLabMain.CustomerID
    customer = models.ForeignKey(
        'erp_base.Party',
        verbose_name='客户',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_customer_set",
    )

    # 原物理来源：DyeLabMain.SalerID
    salesperson = models.ForeignKey(
        'erp_base.Employee',
        verbose_name='业务员',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_salesperson_set",
        blank=True,
        null=True,
    )

    # 原物理来源：DyeLabMain.OrderSheetNo
    sales_order = models.ForeignKey(
        'erp_sales.SalesOrder',
        verbose_name='来源订单',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_sales_order_set",
        blank=True,
        null=True,
    )

    # 原物理来源：DyeLabMain.GetSampleDate
    received_at = models.DateTimeField(
        '收样时间',
        blank=True,
        null=True,
    )

    # 原物理来源：DyeLabMain.DlvSampleDate
    due_at = models.DateTimeField(
        '交样日期',
        blank=True,
        null=True,
    )

    # 原物理来源：DyeLabMain.ToBackSample
    return_customer_sample = models.BooleanField(
        '客样退回',
        blank=True,
        null=True,
    )

    # 原物理来源：DyeLabMain.VerLight1ID
    primary_light = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='主光源',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_primary_light_set",
        blank=True,
        null=True,
    )

    # 原物理来源：DyeLabMain.VerLight2ID
    secondary_light = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='副光源',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_secondary_light_set",
        blank=True,
        null=True,
    )

    # 原物理来源：DyeLabMain.KindType
    requirement_text = models.CharField(
        '打板需求',
        max_length=10,
        blank=True,
        null=True,
    )

    # 原物理来源：DyeLabMain.SheetStatus
    status = models.CharField(
        '任务状态',
        max_length=24,
        choices=choices.SampleStatus.choices,
        default=choices.SampleStatus.DRAFT,
    )

    class Meta:
        db_table = "erp_sampling_samplerequest"
        verbose_name = '来样打样任务'
        verbose_name_plural = '来样打样任务'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(status__in=choices.SampleStatus.values), name='erp_sampling_samplerequest_status_valid'),
        ]
        indexes = [
            models.Index(fields=['status', 'document_at'], name='sam_samplerequest_1'),
        ]


class SampleLine(ErpModel):
    """打样颜色规格明细。"""

    # 原物理来源：DyeLabColor.SheetSeries
    request = models.ForeignKey(
        'erp_sampling.SampleRequest',
        verbose_name='打样任务',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_request_set",
    )

    line_number = models.IntegerField(
        '行号',
    )

    # 原物理来源：DyeLabColor.ProdID
    material = models.ForeignKey(
        'erp_base.Material',
        verbose_name='物料',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_material_set",
    )

    # 原物理来源：DyeLabColor.CheckNo
    order_line = models.ForeignKey(
        'erp_sales.SalesOrderLine',
        verbose_name='订单明细',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_order_line_set",
        blank=True,
        null=True,
    )

    # 原物理来源：DyeLabColor.Spec
    specification_snapshot = models.CharField(
        '规格',
        max_length=128,
        blank=True,
        null=True,
    )

    # 原物理来源：DyeLabColor.CustSelfProduct
    customer_specification = models.CharField(
        '客户规格',
        max_length=200,
        blank=True,
        null=True,
    )

    # 原物理来源：DyeLabColor.CustColorNum
    customer_color_number = models.CharField(
        '客户色号',
        max_length=100,
        blank=True,
        null=True,
    )

    # 原物理来源：DyeLabColor.ColorNum
    color_number = models.CharField(
        '色号',
        max_length=20,
        blank=True,
        null=True,
    )

    # 原物理来源：DyeLabColor.ColorNumInput
    color_number_input = models.CharField(
        '输入色号',
        max_length=20,
        blank=True,
        null=True,
    )

    # 原物理来源：DyeLabColor.ColorMarkt
    color_prefix = models.CharField(
        '色号前缀',
        max_length=10,
        blank=True,
        null=True,
    )

    # 原物理来源：DyeLabColor.ColorAfter
    color_suffix = models.CharField(
        '色号后缀',
        max_length=10,
        blank=True,
        null=True,
    )

    # 原物理来源：DyeLabColor.ColorDepthID
    color_depth = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='色深',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_color_depth_set",
        blank=True,
        null=True,
    )

    # 原物理来源：DyeLabColor.EmpID
    assigned_employee = models.ForeignKey(
        'erp_base.Employee',
        verbose_name='打样员',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_assigned_employee_set",
        blank=True,
        null=True,
    )

    # 原物理来源：DyeLabColor.OriColorNo
    original_sample_line = models.ForeignKey(
        'erp_sampling.SampleLine',
        verbose_name='原打样明细',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_original_sample_line_set",
        blank=True,
        null=True,
    )

    # 原物理来源：DyeLabColor.Status
    status = models.CharField(
        '打样状态',
        max_length=24,
        choices=choices.SampleLineStatus.choices,
        default=choices.SampleLineStatus.PENDING,
    )

    class Meta:
        db_table = "erp_sampling_sampleline"
        verbose_name = '打样颜色规格明细'
        verbose_name_plural = '打样颜色规格明细'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['request', 'line_number'], name='erp_sampling_sampleline_identity_uniq'),
            models.CheckConstraint(condition=Q(line_number__gt=0), name='erp_sampling_sampleline_line_number_positive'),
            models.CheckConstraint(condition=Q(original_sample_line__isnull=True) | ~Q(original_sample_line=F("pk")), name='erp_sampling_sampleline_original_sample_line_not_self'),
            models.CheckConstraint(condition=Q(status__in=choices.SampleLineStatus.values), name='erp_sampling_sampleline_status_valid'),
        ]

    def clean(self):
        super().clean()
        if self.order_line_id is not None and self.request_id is not None:
            if self.order_line.order.customer_id != self.request.customer_id:
                raise ValidationError({'order_line': '订单来源必须属于本打样客户。'})


class SampleTrial(ErpModel):
    """一次打样试验。"""

    sample_line = models.ForeignKey(
        'erp_sampling.SampleLine',
        verbose_name='打样明细',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_sample_line_set",
    )

    trial_number = models.IntegerField(
        '轮次',
    )

    recipe_version = models.ForeignKey(
        'erp_sampling.RecipeVersion',
        verbose_name='采用配方版本',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_recipe_version_set",
        blank=True,
        null=True,
    )

    # 原物理来源：DyeLabColor.EmpID
    operator = models.ForeignKey(
        'erp_base.Employee',
        verbose_name='打样员',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_operator_set",
        blank=True,
        null=True,
    )

    # 原物理来源：DyeLabColor.ShiftID
    shift = models.ForeignKey(
        'erp_base.Shift',
        verbose_name='班次',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_shift_set",
        blank=True,
        null=True,
    )

    # 原物理来源：DyeLabColor.StartTime
    started_at = models.DateTimeField(
        '开始时间',
        blank=True,
        null=True,
    )

    finished_at = models.DateTimeField(
        '结束时间',
        blank=True,
        null=True,
    )

    result_text = models.TextField(
        '试验结果',
        blank=True,
    )

    status = models.CharField(
        '试验状态',
        max_length=24,
        choices=choices.TrialStatus.choices,
        default=choices.TrialStatus.PLANNED,
    )

    class Meta:
        db_table = "erp_sampling_sampletrial"
        verbose_name = '一次打样试验'
        verbose_name_plural = '一次打样试验'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['sample_line', 'trial_number'], name='erp_sampling_sampletrial_identity_uniq'),
            models.CheckConstraint(condition=Q(trial_number__gt=0), name='erp_sampling_sampletrial_trial_number_positive'),
            models.CheckConstraint(condition=Q(status__in=choices.TrialStatus.values), name='erp_sampling_sampletrial_status_valid'),
            models.CheckConstraint(condition=Q(started_at__isnull=True) | Q(finished_at__isnull=True) | Q(finished_at__gte=F("started_at")), name='erp_sampling_sampletrial_time_order'),
        ]


class SampleConfirmation(ErpModel):
    """送版和确板记录。"""

    sample_line = models.ForeignKey(
        'erp_sampling.SampleLine',
        verbose_name='打样明细',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_sample_line_set",
    )

    trial = models.ForeignKey(
        'erp_sampling.SampleTrial',
        verbose_name='试验轮次',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_trial_set",
        blank=True,
        null=True,
    )

    # 原物理来源：P_ColorNum.IsToSampleDaTe
    sent_at = models.DateTimeField(
        '送版时间',
        blank=True,
        null=True,
    )

    # 原物理来源：P_ColorNum.OKTime
    confirmed_at = models.DateTimeField(
        '确板时间',
        blank=True,
        null=True,
    )

    result = models.CharField(
        '确认结果',
        max_length=24,
        choices=choices.SampleConfirmation.choices,
        default=choices.SampleConfirmation.PENDING,
    )

    confirmed_color = models.ForeignKey(
        'erp_base.ColorStandard',
        verbose_name='确认色标准',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_confirmed_color_set",
        blank=True,
        null=True,
    )

    confirmed_recipe = models.ForeignKey(
        'erp_sampling.RecipeVersion',
        verbose_name='确认配方版本',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_confirmed_recipe_set",
        blank=True,
        null=True,
    )

    customer_reply = models.TextField(
        '客户意见',
        blank=True,
    )

    class Meta:
        db_table = "erp_sampling_sampleconfirmation"
        verbose_name = '送版和确板记录'
        verbose_name_plural = '送版和确板记录'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(result__in=choices.SampleConfirmation.values), name='erp_sampling_sampleconfirmation_result_valid'),
        ]

    def clean(self):
        super().clean()
        if self.trial_id is not None and self.trial.sample_line_id != self.sample_line_id:
            raise ValidationError({'trial': '试验轮次必须属于本打样明细。'})


class Recipe(ErpModel):
    """配方主体。"""

    # 原物理来源：DyeRecipe.SheetNo
    code = models.CharField(
        '配方编号',
        max_length=20,
        unique=True,
    )

    name = models.CharField(
        '配方名称',
        max_length=255,
    )

    # 原物理来源：DyeRecipe.CustomerID
    customer = models.ForeignKey(
        'erp_base.Party',
        verbose_name='适用客户',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_customer_set",
        blank=True,
        null=True,
    )

    # 原物理来源：DyeRecipe.ProdID
    material = models.ForeignKey(
        'erp_base.Material',
        verbose_name='适用物料',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_material_set",
        blank=True,
        null=True,
    )

    # 原物理来源：DyeRecipe.ColorNum
    color_standard = models.ForeignKey(
        'erp_base.ColorStandard',
        verbose_name='适用色标准',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_color_standard_set",
        blank=True,
        null=True,
    )

    # 原物理来源：DyeRecipe.SheetKind
    purpose = models.CharField(
        '配方用途',
        max_length=24,
        choices=choices.RecipePurpose.choices,
    )

    is_active = models.BooleanField(
        '启用',
        default=True,
    )

    class Meta:
        db_table = "erp_sampling_recipe"
        verbose_name = '配方主体'
        verbose_name_plural = '配方主体'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(purpose__in=choices.RecipePurpose.values), name='erp_sampling_recipe_purpose_valid'),
        ]


class RecipeVersion(ErpModel):
    """配方版本。"""

    recipe = models.ForeignKey(
        'erp_sampling.Recipe',
        verbose_name='配方主体',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_recipe_set",
    )

    version = models.IntegerField(
        '版本号',
        default=1,
    )

    # 原物理来源：DyeRecipe.OriRecipeSheetNo
    original_version = models.ForeignKey(
        'erp_sampling.RecipeVersion',
        verbose_name='来源配方版本',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_original_version_set",
        blank=True,
        null=True,
    )

    sample_trial = models.ForeignKey(
        'erp_sampling.SampleTrial',
        verbose_name='来源试验',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_sample_trial_set",
        blank=True,
        null=True,
    )

    # 原物理来源：DyeRecipe.VerLight1ID
    primary_light = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='主光源',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_primary_light_set",
        blank=True,
        null=True,
    )

    # 原物理来源：DyeRecipe.L
    color_l = models.DecimalField(
        'CIE色度L值',
        max_digits=7,
        decimal_places=3,
        blank=True,
        null=True,
    )

    # 原物理来源：DyeRecipe.A
    color_a = models.DecimalField(
        'CIE色度A值',
        max_digits=7,
        decimal_places=3,
        blank=True,
        null=True,
    )

    # 原物理来源：DyeRecipe.B
    color_b = models.DecimalField(
        'CIE色度B值',
        max_digits=7,
        decimal_places=3,
        blank=True,
        null=True,
    )

    # 原物理来源：DyeRecipe.RightStatus
    status = models.CharField(
        '版本状态',
        max_length=24,
        choices=choices.VersionStatus.choices,
        default=choices.VersionStatus.DRAFT,
    )

    # 原物理来源：DyeRecipe.Approver
    approved_by = models.ForeignKey(
        'erp_base.Employee',
        verbose_name='确认人',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_approved_by_set",
        blank=True,
        null=True,
    )

    # 原物理来源：DyeRecipe.ApproveDate
    approved_at = models.DateTimeField(
        '审核时间',
        blank=True,
        null=True,
    )

    valid_from = models.DateTimeField(
        '生效时间',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_sampling_recipeversion"
        verbose_name = '配方版本'
        verbose_name_plural = '配方版本'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'version'], name='erp_sampling_recipeversion_identity_uniq'),
            models.CheckConstraint(condition=Q(version__gt=0), name='erp_sampling_recipeversion_version_positive'),
            models.CheckConstraint(condition=Q(original_version__isnull=True) | ~Q(original_version=F("pk")), name='erp_sampling_recipeversion_original_version_not_self'),
            models.CheckConstraint(condition=Q(status__in=choices.VersionStatus.values), name='erp_sampling_recipeversion_status_valid'),
        ]


class RecipeStage(ErpModel):
    """配方染程阶段。"""

    # 原物理来源：DyeRecipePhase.SheetSeries
    version = models.ForeignKey(
        'erp_sampling.RecipeVersion',
        verbose_name='配方版本',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_version_set",
    )

    # 原物理来源：DyeRecipePhase.PhaseNo
    sequence = models.IntegerField(
        '染程序号',
    )

    # 原物理来源：DyeRecipePhase.PhaseID
    phase = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='染程类型',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_phase_set",
        blank=True,
        null=True,
    )

    # 原物理来源：DyeRecipePhase.BathRatio
    bath_ratio = models.DecimalField(
        '浴比',
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
    )

    bath_ratio_basis = models.CharField(
        '浴比定义',
        max_length=24,
        choices=choices.BathRatioBasis.choices,
        blank=True,
        null=True,
    )

    # 原物理来源：DyeRecipePhase.PH
    ph_text = models.CharField(
        'PH值',
        max_length=10,
        blank=True,
        null=True,
    )

    # 原物理来源：DyeRecipePhase.ProgramID
    curve_version = models.ForeignKey(
        'erp_sampling.ProcessCurveVersion',
        verbose_name='工艺曲线版本',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_curve_version_set",
        blank=True,
        null=True,
    )

    # 原物理来源：DyeRecipePhase.WaterQty
    water_reference = models.DecimalField(
        '水重',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    water_reference_unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='参考水量单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_water_reference_unit_set",
        blank=True,
        null=True,
    )

    # 原物理来源：DyeRecipePhase.Minutes
    hold_minutes = models.DecimalField(
        '保温或阶段分钟',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    # 原物理来源：DyeRecipePhase.Temperature
    temperature_c = models.DecimalField(
        '阶段温度℃',
        max_digits=5,
        decimal_places=1,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_sampling_recipestage"
        verbose_name = '配方染程阶段'
        verbose_name_plural = '配方染程阶段'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['version', 'sequence'], name='erp_sampling_recipestage_identity_uniq'),
            models.CheckConstraint(condition=Q(sequence__gt=0), name='erp_sampling_recipestage_sequence_positive'),
            models.CheckConstraint(condition=Q(bath_ratio_basis__isnull=True) | Q(bath_ratio_basis__in=choices.BathRatioBasis.values), name='erp_sampling_recipestage_bath_ratio_basis_valid'),
        ]

    def clean(self):
        super().clean()
        if self.water_reference is not None and self.water_reference_unit_id is None:
            raise ValidationError({'water_reference_unit': '已填写数量时必须明确计量单位。'})


class RecipeIngredient(ErpModel):
    """配方物料明细。"""

    # 原物理来源：DyeRecipeDetail.SheetSeries; DyeRecipeDetail.PhaseNo
    stage = models.ForeignKey(
        'erp_sampling.RecipeStage',
        verbose_name='染程阶段',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_stage_set",
    )

    # 原物理来源：DyeRecipeDetail.StuffNo
    sequence = models.IntegerField(
        '染程明细序号',
    )

    # 原物理来源：DyeRecipeDetail.StuffID
    material = models.ForeignKey(
        'erp_base.Material',
        verbose_name='染化料',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_material_set",
    )

    # 原物理来源：DyeRecipeDetail.Dosage
    dosage = models.DecimalField(
        '比例',
        max_digits=15,
        decimal_places=6,
    )

    # 原物理来源：DyeRecipeDetail.RecipeUnit
    dosage_basis = models.CharField(
        '剂量基准',
        max_length=24,
        choices=choices.DosageBasis.choices,
    )

    # 原物理来源：DyeRecipeDetail.StepName
    process_step_name = models.CharField(
        '加料步骤说明',
        max_length=50,
        blank=True,
        null=True,
    )

    # 原物理来源：DyeRecipeDetail.DetailNote
    note = models.CharField(
        '明细说明',
        max_length=256,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_sampling_recipeingredient"
        verbose_name = '配方物料明细'
        verbose_name_plural = '配方物料明细'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['stage', 'sequence'], name='erp_sampling_recipeingredient_identity_uniq'),
            models.CheckConstraint(condition=Q(sequence__gt=0), name='erp_sampling_recipeingredient_sequence_positive'),
            models.CheckConstraint(condition=Q(dosage_basis__in=choices.DosageBasis.values), name='erp_sampling_recipeingredient_dosage_basis_valid'),
            models.CheckConstraint(condition=Q(dosage__gte=0), name='erp_sampling_recipeingredient_dosage_nonnegative'),
        ]

    def clean(self):
        super().clean()
        if self.material_id is not None and self.material.kind != choices.MaterialKind.CHEMICAL:
            raise ValidationError({'material': '配方和称料只能引用染化料。'})


class ProcessCurveVersion(ErpModel):
    """染色工艺曲线版本。"""

    # 原物理来源：p_DyeCurve.CurveID
    code = models.CharField(
        '编号',
        max_length=10,
    )

    # 原物理来源：p_DyeCurve.Name
    name = models.CharField(
        '曲线名称',
        max_length=60,
    )

    version = models.IntegerField(
        '版本号',
        default=1,
    )

    # 原物理来源：p_DyeCurve.PreMinutes
    preparation_minutes = models.DecimalField(
        '准备时间',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：p_DyeCurve.ProgramKindID
    category = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='曲线分类',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_category_set",
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
        db_table = "erp_sampling_processcurveversion"
        verbose_name = '染色工艺曲线版本'
        verbose_name_plural = '染色工艺曲线版本'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['code', 'version'], name='erp_sampling_processcurveversion_identity_uniq'),
            models.CheckConstraint(condition=Q(version__gt=0), name='erp_sampling_processcurveversion_version_positive'),
            models.CheckConstraint(condition=Q(status__in=choices.VersionStatus.values), name='erp_sampling_processcurveversion_status_valid'),
        ]


class ProcessCurveStep(ErpModel):
    """工艺曲线步骤。"""

    # 原物理来源：p_DyeCurveDetail.CurveID
    curve_version = models.ForeignKey(
        'erp_sampling.ProcessCurveVersion',
        verbose_name='曲线版本',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_curve_version_set",
    )

    # 原物理来源：p_DyeCurveDetail.StepNo
    sequence = models.IntegerField(
        '步号',
    )

    # 原物理来源：p_DyeCurveDetail.DyeProcessID
    process_code_snapshot = models.CharField(
        '染色工序',
        max_length=50,
        blank=True,
        null=True,
    )

    name = models.CharField(
        '步骤名称',
        max_length=200,
        blank=True,
    )

    # 原物理来源：p_DyeCurveDetail.Temperature
    target_temperature_c = models.DecimalField(
        '温度',
        max_digits=5,
        decimal_places=1,
        blank=True,
        null=True,
    )

    # 原物理来源：p_DyeCurveDetail.Minutes
    hold_minutes = models.DecimalField(
        '分钟',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    # 原物理来源：p_DyeCurveDetail.SpeedRate
    rate_c_per_minute = models.DecimalField(
        '速率',
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True,
    )

    # 原物理来源：p_DyeCurveDetail.DefaultValue
    handover_ratio = models.DecimalField(
        '交接比例原值',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    # 原物理来源：p_DyeCurveDetail.Memo
    instruction = models.CharField(
        '操作说明',
        max_length=50,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_sampling_processcurvestep"
        verbose_name = '工艺曲线步骤'
        verbose_name_plural = '工艺曲线步骤'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['curve_version', 'sequence'], name='erp_sampling_processcurvestep_identity_uniq'),
            models.CheckConstraint(condition=Q(sequence__gt=0), name='erp_sampling_processcurvestep_sequence_positive'),
        ]


from .source_models import (
    SourceDboBackDyeRecipePhase,
    SourceDyeAddDyeWProcessStep,
    SourceDyeColorCard,
    SourceDyeColorCardDetail,
    SourceDyeColorCardFlow,
    SourceDyeColorChangeRisk,
    SourceDyeCptLabRecipe,
    SourceDyeCptLabRecipeDetail,
    SourceDyeCurSmpPrescriptEntry,
    SourceDyeDyeColor,
    SourceDyeDyeDipsRecord,
    SourceDyeDyeDipsRecordDetail,
    SourceDyeDyeDipsRecordEmp,
    SourceDyeDyeDipsRecordNote,
    SourceDyeDyeDipsRecordPhase,
    SourceDyeDyeLabAtte,
    SourceDyeDyeLabColor,
    SourceDyeDyeLabColorRecord,
    SourceDyeDyeLabMain,
    SourceDyeDyeProduceItem,
    SourceDyeDyeRecipe,
    SourceDyeDyeRecipeDetail,
    SourceDyeDyeRecipeJob,
    SourceDyeDyeRecipePhase,
    SourceDyeDyeReprint,
    SourceDyeDyeStartDateTime,
    SourceDyeLabDips,
    SourceDyePrintColorSeparate,
    SourceDyePrintColorSeparateDetail,
    SourceDyePrintColorSeparateRecord,
    SourceDyePrintingTest,
    SourceDyePrintingTestColor,
    SourceDyePrintingTestDetail,
    SourceDyePrintingTestStuff,
    SourceDyePrintLabAttach,
    SourceDyePrintLabAtte,
    SourceDyePrintLabMain,
    SourceDyePrintRecipe,
    SourceDyePrintRecipeColor,
    SourceDyePrintRecipeDetail,
    SourceDyePTSampleRegist,
    SourceDyePTSampleRegistAtte,
    SourceDyePTSampleRegistDetail,
    SourceDyeSampleChoice,
    SourceDyeSampleIn,
    SourceDyeSampleInDetail,
    SourceDyeSampleOut,
    SourceDyeSampleOutDetail,
    SourceDyeSampleStockBook,
    SourceDyeSmpPrescriptEntry,
    SourceDyeYeDye,
)
