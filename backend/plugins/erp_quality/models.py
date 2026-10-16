"""独立质量管理；原质量表名、主键和事实保持一致。"""
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F,Q
from plugins.erp_base.models import ErpModel
from plugins.erp_base import choices
from .quantity_models import QualityQuantityBatch,QualityQuantitySource


class QualityInspection(ErpModel):
    """生产检验单。"""

    is_void = models.BooleanField('检验已取消采用', default=False)
    voided_at = models.DateTimeField('取消采用时间', null=True, blank=True)
    void_reason = models.TextField('取消采用原因', blank=True)

    inspected_quantity = models.DecimalField('明确检验范围量', max_digits=20,
        decimal_places=6, null=True, blank=True)
    quantity_unit = models.ForeignKey('erp_base.Unit', verbose_name='检验范围单位',
        null=True, blank=True, on_delete=models.PROTECT, related_name='inspection_scopes')

    lot = models.ForeignKey('erp_warehouse.InventoryLot', verbose_name='检验库存批次',
        null=True, blank=True, on_delete=models.PROTECT, related_name='quality_inspections')
    receipt_line = models.ForeignKey('erp_warehouse.StockReceiptLine', verbose_name='来料收货行',
        null=True, blank=True, on_delete=models.PROTECT, related_name='quality_inspections')

    number = models.CharField(
        '检验单号',
        max_length=64,
        unique=True,
    )

    # 原物理来源：RecordYield.JobSheetNo
    work_card = models.ForeignKey(
        'erp_production.WorkCard',
        verbose_name='工卡',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_work_card_set",
        null=True,
        blank=True,
    )

    execution = models.ForeignKey(
        'erp_production.OperationExecution',
        verbose_name='工序执行',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_execution_set",
        blank=True,
        null=True,
    )

    # 原物理来源：RecordYield.Guid
    package = models.ForeignKey(
        'erp_warehouse.Package',
        verbose_name='包装单元',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_package_set",
        blank=True,
        null=True,
    )

    kind = models.CharField(
        '检验类型',
        max_length=24,
        choices=choices.InspectionKind.choices,
    )

    inspected_at = models.DateTimeField(
        '检验时间',
    )

    inspector = models.ForeignKey(
        'erp_base.Employee',
        verbose_name='检验员',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_inspector_set",
        blank=True,
        null=True,
    )

    # 原物理来源：RecordYield.QCResultID
    result = models.CharField(
        '检验结果',
        max_length=24,
        choices=choices.InspectionResult.choices,
        default=choices.InspectionResult.PENDING,
    )

    # 原物理来源：RecordYield.GradeID
    grade = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='等级',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_grade_set",
        blank=True,
        null=True,
    )

    previous_inspection = models.ForeignKey(
        'erp_quality.QualityInspection',
        verbose_name='原检验',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_previous_inspection_set",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_production_qualityinspection"
        verbose_name = '生产检验单'
        verbose_name_plural = '生产检验单'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(kind__in=choices.InspectionKind.values), name='erp_production_qualityinspection_kind_valid'),
            models.CheckConstraint(condition=Q(result__in=choices.InspectionResult.values), name='erp_production_qualityinspection_result_valid'),
            models.CheckConstraint(condition=Q(previous_inspection__isnull=True) | ~Q(previous_inspection=F("pk")), name='erp_production_qualityinspection_previous_inspection_not_self'),
        ]

    def clean(self):
        super().clean()
        if self.package_id is not None and self.package.work_card_id != self.work_card_id:
            raise ValidationError({'package': '检验包装必须属于本工卡。'})
        if self.execution_id is not None and self.execution.operation.work_card_id != self.work_card_id:
            raise ValidationError({'execution': '检验执行必须属于本工卡。'})
        if self.kind == 'incoming':
            if self.work_card_id is not None or self.execution_id is not None or self.package_id is not None:
                raise ValidationError({'work_card': '来料检验不能使用生产工卡、执行或包装作为检验范围。'})
            if self.lot_id is None or self.receipt_line_id is None:
                raise ValidationError({'lot': '来料检验必须明确批次和收货行。'})
            if self.receipt_line.lot_id != self.lot_id:
                raise ValidationError({'receipt_line': '收货行必须属于所检验批次。'})
        elif self.work_card_id is None:
            raise ValidationError({'work_card': '生产检验必须明确工卡。'})


class InspectionResultLine(ErpModel):
    """检验项目结果。"""

    inspection = models.ForeignKey(
        'erp_quality.QualityInspection',
        verbose_name='检验单',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_inspection_set",
    )

    item_code = models.CharField(
        '项目代码',
        max_length=64,
    )

    item_name_snapshot = models.CharField(
        '项目名称快照',
        max_length=200,
    )

    value_text = models.TextField(
        '实测或判定文本',
        blank=True,
    )

    numeric_value = models.DecimalField(
        '实测数值',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='测量单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_unit_set",
        blank=True,
        null=True,
    )

    result = models.CharField(
        '项目结果',
        max_length=24,
        choices=choices.InspectionResult.choices,
        default=choices.InspectionResult.PENDING,
    )

    class Meta:
        db_table = "erp_production_inspectionresultline"
        verbose_name = '检验项目结果'
        verbose_name_plural = '检验项目结果'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['inspection', 'item_code'], name='erp_production_inspectionresultline_identity_uniq'),
            models.CheckConstraint(condition=Q(result__in=choices.InspectionResult.values), name='erp_production_inspectionresultline_result_valid'),
        ]


class QualityDisposition(ErpModel):
    """质量处置和放行。"""

    status = models.CharField('采用状态', max_length=24, default='active', choices=choices.AdoptionStatus.choices)
    supersedes = models.ForeignKey('self', verbose_name='被替换处置', null=True,
        blank=True, on_delete=models.PROTECT, related_name='replacement_dispositions')

    inspection = models.ForeignKey(
        'erp_quality.QualityInspection',
        verbose_name='检验单',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_inspection_set",
    )

    kind = models.CharField(
        '处置类型',
        max_length=24,
        choices=choices.DispositionKind.choices,
    )

    quantity = models.DecimalField(
        '覆盖数量',
        max_digits=20,
        decimal_places=6,
    )

    unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='覆盖单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_unit_set",
    )

    reason = models.TextField(
        '处置原因',
    )

    approved_by = models.ForeignKey(
        'erp_base.Employee',
        verbose_name='处置人',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_approved_by_set",
    )

    approved_at = models.DateTimeField(
        '处置时间',
    )

    class Meta:
        db_table = "erp_production_qualitydisposition"
        verbose_name = '质量处置和放行'
        verbose_name_plural = '质量处置和放行'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(kind__in=choices.DispositionKind.values), name='erp_production_qualitydisposition_kind_valid'),
            models.CheckConstraint(condition=Q(quantity__gt=0), name='erp_production_qualitydisposition_quantity_positive'),
        ]


class QualityDefect(ErpModel):
    """现场疵点与质量异常。"""

    # 原物理来源：WDefect.WDefectNo
    number = models.CharField(
        '质量流水号',
        max_length=20,
        unique=True,
    )

    # 原物理来源：WDefect.JobSheetNo
    work_card = models.ForeignKey(
        'erp_production.WorkCard',
        verbose_name='工卡',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_work_card_set",
    )

    # 原物理来源：WDefect.WProcessNo
    execution = models.ForeignKey(
        'erp_production.OperationExecution',
        verbose_name='发现执行记录',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_execution_set",
        blank=True,
        null=True,
    )

    inspection = models.ForeignKey(
        'erp_quality.QualityInspection',
        verbose_name='关联检验单',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_inspection_set",
        blank=True,
        null=True,
    )

    # 原物理来源：WDefect.DefectDate
    occurred_at = models.DateTimeField(
        '出疵时间',
        blank=True,
        null=True,
    )

    # 原物理来源：WDefect.Defects
    defect_description = models.CharField(
        '疵点',
        max_length=100,
        blank=True,
        null=True,
    )

    # 原物理来源：WDefect.DefectIDs
    source_defect_codes = models.TextField(
        '疵点代码',
        blank=True,
        null=True,
    )

    # 原物理来源：WDefect.DefectQty
    quantity = models.DecimalField(
        '疵品数量',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='疵品计量单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_unit_set",
        blank=True,
        null=True,
    )

    # 原物理来源：WDefect.DefectRolls
    pieces = models.DecimalField(
        '疵品粒数',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：WDefect.DefectProcessID
    responsible_process = models.ForeignKey(
        'erp_base.Process',
        verbose_name='认定出疵工序',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_responsible_process_set",
        blank=True,
        null=True,
    )

    # 原物理来源：WDefect.DefectEmpID
    responsible_employee = models.ForeignKey(
        'erp_base.Employee',
        verbose_name='认定出疵员工',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_responsible_employee_set",
        blank=True,
        null=True,
    )

    # 原物理来源：WDefect.ProcessID
    discovering_process = models.ForeignKey(
        'erp_base.Process',
        verbose_name='发现工序',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_discovering_process_set",
        blank=True,
        null=True,
    )

    # 原物理来源：WDefect.EmpID
    discovering_employee = models.ForeignKey(
        'erp_base.Employee',
        verbose_name='发现人',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_discovering_employee_set",
        blank=True,
        null=True,
    )

    disposition = models.ForeignKey(
        'erp_quality.QualityDisposition',
        verbose_name='处置记录',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_disposition_set",
        blank=True,
        null=True,
    )

    # 原物理来源：WDefect.Status
    status = models.CharField(
        '异常处理状态',
        max_length=24,
        choices=choices.ComplaintStatus.choices,
        default=choices.ComplaintStatus.OPEN,
    )

    class Meta:
        db_table = "erp_production_qualitydefect"
        verbose_name = '现场疵点与质量异常'
        verbose_name_plural = '现场疵点与质量异常'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(status__in=choices.ComplaintStatus.values), name='erp_production_qualitydefect_status_valid'),
        ]

    def clean(self):
        super().clean()
        if self.quantity is not None and self.unit_id is None:
            raise ValidationError({'unit': '已填写数量时必须明确计量单位。'})



from .source_models import (
    SourceDyeCHECKEXACT,
    SourceDyeCHECKINOUT,
    SourceDyeColoringCheck,
    SourceDyeDefectiveIn,
    SourceDyeDefectiveInDetail,
    SourceDyeDefectiveInRecord,
    SourceDyeDefectiveOut,
    SourceDyeDefectiveOutDetail,
    SourceDyeDefectiveOutRecord,
    SourceDyeDyeCheck,
    SourceDyeDyeCheckout,
    SourceDyeInspectionLog,
    SourceDyeInspectionLogDetail,
    SourceDyeInspectionProject,
    SourceDyePTestItem,
    SourceDyeProdTest,
    SourceDyeQualityAccident,
    SourceDyeQualityDeduction,
    SourceDyeQualityRegister,
    SourceDyeRecordDefect,
    SourceDyeTestDetail,
    SourceDyeTestMain,
    SourceDyeWDefect,
    SourceDyeZhijianwenti,
)
