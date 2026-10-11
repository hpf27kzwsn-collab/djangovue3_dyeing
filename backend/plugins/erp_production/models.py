"""生产管理模型；字段来源见 docs/ERP模型实施说明.md。"""
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q
from plugins.erp_base.models import ErpModel
from plugins.erp_base import choices
from .calculations import calculate_adopted_dosage, calculate_elapsed_minutes


class PhysicalBatchExecution(ErpModel):
    """一次同缸物理执行；工卡执行只保存对应成员实际分配量。"""
    batch = models.ForeignKey('erp_production.DyeBatch', verbose_name='缸批', on_delete=models.PROTECT, related_name='physical_executions')
    process = models.ForeignKey('erp_base.Process', verbose_name='实际工序', on_delete=models.PROTECT, related_name='physical_executions')
    machine = models.ForeignKey('erp_base.Machine', verbose_name='实际机台', on_delete=models.PROTECT, related_name='physical_executions')
    execution_number = models.PositiveIntegerField('物理执行轮次')
    operator = models.ForeignKey('erp_base.Employee', verbose_name='操作人员', on_delete=models.PROTECT, related_name='physical_executions')
    shift = models.ForeignKey('erp_base.Shift', verbose_name='班次', null=True, blank=True, on_delete=models.PROTECT, related_name='physical_executions')
    started_at = models.DateTimeField('实际开工时间')
    ended_at = models.DateTimeField('实际完工时间', null=True, blank=True)
    output_mass_kg = models.DecimalField('本缸实际产出kg', max_digits=20, decimal_places=6, null=True, blank=True)
    status = models.CharField('执行状态', max_length=24, choices=choices.ExecutionStatus.choices, default='running')

    class Meta:
        db_table = 'erp_production_physicalbatchexecution'
        verbose_name = verbose_name_plural = '同缸物理执行'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(fields=['batch','process','execution_number'], name='erp_physical_execution_round_uniq'),
            models.UniqueConstraint(fields=['batch','process'], condition=Q(status='running'), name='erp_physical_execution_running_uniq'),
            models.CheckConstraint(condition=Q(ended_at__isnull=True)|Q(ended_at__gte=F('started_at')), name='erp_physical_execution_time_order'),
            models.CheckConstraint(condition=Q(output_mass_kg__isnull=True)|Q(output_mass_kg__gte=0), name='erp_physical_execution_mass_nonnegative'),
            models.CheckConstraint(condition=Q(status__in=choices.ExecutionStatus.values), name='erp_physical_execution_status_valid'),
        ]


class PhysicalExecutionCorrection(ErpModel):
    physical_execution = models.ForeignKey(PhysicalBatchExecution, verbose_name='原物理执行', on_delete=models.PROTECT, related_name='corrections')
    corrected_at = models.DateTimeField('更正时间')
    approved_by = models.ForeignKey('erp_base.Employee', verbose_name='确认员工', on_delete=models.PROTECT)
    reason = models.TextField('更正依据')
    before_values = models.JSONField('原有效整缸事实')
    after_values = models.JSONField('更正后整缸事实')
    member_changes = models.JSONField('逐工卡更正对照')

    class Meta:
        db_table = 'erp_production_physicalexecutioncorrection'
        verbose_name = verbose_name_plural = '整缸执行更正'
        ordering = ['-id']


class WorkCard(ErpModel):
    """生产工卡。"""

    manual_creation_reason = models.TextField('无订单建卡原因', blank=True)

    # 原物理来源：JobSheet.SheetNo
    number = models.CharField(
        '缸号',
        max_length=50,
        unique=True,
    )

    # 原物理来源：JobSheet.SheetDate
    document_at = models.DateTimeField(
        '单据日期',
    )

    # 原物理来源：JobSheet.FactID
    factory = models.ForeignKey(
        'erp_base.Factory',
        verbose_name='工厂',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_factory_set",
        blank=True,
        null=True,
    )

    # 原物理来源：JobSheet.BusinessUnitID
    business_unit = models.ForeignKey(
        'erp_base.BusinessUnit',
        verbose_name='经营单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_business_unit_set",
        blank=True,
        null=True,
    )

    # 原物理来源：JobSheet.ProdID
    material = models.ForeignKey(
        'erp_base.Material',
        verbose_name='生产物料',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_material_set",
    )

    # 原物理来源：JobSheet.Spec
    specification_snapshot = models.CharField(
        '规格',
        max_length=200,
        blank=True,
        null=True,
    )

    # 原物理来源：JobSheet.ColorNum
    color_standard = models.ForeignKey(
        'erp_base.ColorStandard',
        verbose_name='色标准',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_color_standard_set",
        blank=True,
        null=True,
    )

    # 原物理来源：JobSheet.ColorNum
    color_number_snapshot = models.CharField(
        '色号',
        max_length=50,
        blank=True,
        null=True,
    )

    # 原物理来源：JobSheet.ProductionID
    route_version = models.ForeignKey(
        'erp_base.RouteVersion',
        verbose_name='采用路线版本',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_route_version_set",
    )

    # 原物理来源：JobSheet.PreVatQty
    planned_quantity = models.DecimalField(
        '计划投产量',
        max_digits=20,
        decimal_places=6,
    )

    quantity_unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='计划单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_quantity_unit_set",
    )

    # 原物理来源：JobSheet.PreRolls
    planned_pieces = models.DecimalField(
        '排单粒数',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：JobSheet.PrePacks
    planned_packages = models.DecimalField(
        '计划包件数',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：JobSheet.DlvDate
    due_at = models.DateTimeField(
        '交货日期',
        blank=True,
        null=True,
    )

    # 原物理来源：JobSheet.IsHurry
    is_urgent = models.BooleanField(
        '加急',
        blank=True,
        null=True,
    )

    is_paused = models.BooleanField(
        '暂停',
        default=False,
    )

    # 原物理来源：JobSheet.OriJobsheetNo
    original_work_card = models.ForeignKey(
        'erp_production.WorkCard',
        verbose_name='原工卡',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_original_work_card_set",
        blank=True,
        null=True,
    )

    # 原物理来源：JobSheet.SheetStatus
    status = models.CharField(
        '工卡状态',
        max_length=24,
        choices=choices.WorkCardStatus.choices,
        default=choices.WorkCardStatus.DRAFT,
    )

    released_at = models.DateTimeField(
        '下达时间',
        blank=True,
        null=True,
    )

    # 新系统实际生产完成时间；旧 FinishDate 对应 closed_at。
    completed_at = models.DateTimeField(
        '生产完成时间',
        blank=True,
        null=True,
    )

    # 原物理来源：JobSheet.FinishDate（旧界面：结案日期）
    closed_at = models.DateTimeField(
        '结案日期',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_production_workcard"
        verbose_name = '生产工卡'
        verbose_name_plural = '生产工卡'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(original_work_card__isnull=True) | ~Q(original_work_card=F("pk")), name='erp_production_workcard_original_work_card_not_self'),
            models.CheckConstraint(condition=Q(status__in=choices.WorkCardStatus.values), name='erp_production_workcard_status_valid'),
            models.CheckConstraint(condition=Q(planned_quantity__gt=0), name='erp_production_workcard_planned_quantity_positive'),
        ]
        indexes = [
            models.Index(fields=['status', 'document_at'], name='pro_workcard_1'),
            models.Index(fields=['factory', 'status', 'due_at'], name='pro_workcard_2'),
        ]


    def clean(self):
        super().clean()
        ancestor=self.original_work_card
        seen={self.pk} if self.pk is not None else set()
        while ancestor is not None:
            if ancestor.pk in seen:raise ValidationError({'original_work_card':'原工卡关联不能形成循环。'})
            seen.add(ancestor.pk);ancestor=ancestor.original_work_card


class WorkCardOrderAllocation(ErpModel):
    """订单工卡数量分配。"""

    adopted_order_snapshot = models.JSONField('下达时订单事实', default=dict, blank=True)
    original_allocation = models.ForeignKey('self',verbose_name='原工卡需求分配',on_delete=models.PROTECT,null=True,blank=True,related_name='rework_allocations')
    released_unfulfilled_quantity = models.DecimalField('明确释放未完成需求量',max_digits=20,decimal_places=6,default=0)
    demand_release_at = models.DateTimeField('需求释放时间',null=True,blank=True)
    demand_release_reason = models.TextField('需求释放依据',blank=True)

    # 原物理来源：JobCombineOrder.SheetSeries
    work_card = models.ForeignKey(
        'erp_production.WorkCard',
        verbose_name='工卡',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_work_card_set",
    )

    # 原物理来源：JobCombineOrder.CheckNo
    order_line = models.ForeignKey(
        'erp_sales.SalesOrderLine',
        verbose_name='订单明细',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_order_line_set",
    )

    # 原物理来源：JobCombineOrder.CombineQty
    allocated_quantity = models.DecimalField(
        '合染数量',
        max_digits=20,
        decimal_places=6,
    )

    unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='分配单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_unit_set",
    )

    # 原物理来源：JobCombineOrder.IsMasterOrder
    is_primary = models.BooleanField(
        '是否主表订单',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_production_workcardorderallocation"
        verbose_name = '订单工卡数量分配'
        verbose_name_plural = '订单工卡数量分配'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['work_card', 'order_line'], name='erp_production_workcardorderallocation_identity_uniq'),
            models.CheckConstraint(condition=Q(allocated_quantity__gt=0), name='erp_production_workcardorderallocation_allocated_quantity_posit'),
        ]


class DyeBatch(ErpModel):
    """染色缸批。"""

    number = models.CharField(
        '缸批号',
        max_length=64,
        unique=True,
    )

    factory = models.ForeignKey(
        'erp_base.Factory',
        verbose_name='染色工厂',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_factory_set",
    )

    original_batch = models.ForeignKey(
        'erp_production.DyeBatch',
        verbose_name='来源缸批',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_original_batch_set",
        blank=True,
        null=True,
    )

    planned_mass_kg = models.DecimalField(
        '计划染色重量kg',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    planned_machine = models.ForeignKey(
        'erp_base.Machine',
        verbose_name='计划染机',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_planned_machine_set",
        blank=True,
        null=True,
    )

    status = models.CharField(
        '缸批状态',
        max_length=24,
        choices=choices.BatchStatus.choices,
        default=choices.BatchStatus.PLANNED,
    )

    class Meta:
        db_table = "erp_production_dyebatch"
        verbose_name = '染色缸批'
        verbose_name_plural = '染色缸批'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(original_batch__isnull=True) | ~Q(original_batch=F("pk")), name='erp_production_dyebatch_original_batch_not_self'),
            models.CheckConstraint(condition=Q(status__in=choices.BatchStatus.values), name='erp_production_dyebatch_status_valid'),
        ]


class DyeBatchWorkCard(ErpModel):
    """缸批与工卡关联。"""

    batch = models.ForeignKey(
        'erp_production.DyeBatch',
        verbose_name='缸批',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_batch_set",
    )

    work_card = models.ForeignKey(
        'erp_production.WorkCard',
        verbose_name='工卡',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_work_card_set",
    )

    # 原物理来源：JobCombine.RowNo
    sequence = models.IntegerField(
        '本缸工卡顺序',
    )

    # 原物理来源：JobCombine.Qty
    quantity = models.DecimalField(
        '本工卡分配量',
        max_digits=20,
        decimal_places=6,
    )

    unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='分配单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_unit_set",
    )

    class Meta:
        db_table = "erp_production_dyebatchworkcard"
        verbose_name = '缸批与工卡关联'
        verbose_name_plural = '缸批与工卡关联'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['batch', 'work_card'], name='erp_production_dyebatchworkcard_identity_uniq'),
            models.UniqueConstraint(fields=['batch', 'sequence'], name='erp_production_dyebatchworkcard_sequence_uniq'),
            models.CheckConstraint(condition=Q(sequence__gt=0), name='erp_production_dyebatchworkcard_sequence_positive'),
            models.CheckConstraint(condition=Q(quantity__gt=0), name='erp_production_dyebatchworkcard_quantity_positive'),
        ]


class DyeBatchAllocation(ErpModel):
    """工卡分配到缸批的数量。"""

    batch_work_card = models.ForeignKey(
        'erp_production.DyeBatchWorkCard',
        verbose_name='缸批工卡关联',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_batch_work_card_set",
    )

    work_card_allocation = models.ForeignKey(
        'erp_production.WorkCardOrderAllocation',
        verbose_name='工卡订单分配',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_work_card_allocation_set",
    )

    quantity = models.DecimalField(
        '缸批分配量',
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
        db_table = "erp_production_dyebatchallocation"
        verbose_name = '工卡分配到缸批的数量'
        verbose_name_plural = '工卡分配到缸批的数量'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['batch_work_card', 'work_card_allocation'], name='erp_production_dyebatchallocation_identity_uniq'),
            models.CheckConstraint(condition=Q(quantity__gt=0), name='erp_production_dyebatchallocation_quantity_positive'),
        ]

    def clean(self):
        super().clean()
        if self.batch_work_card_id is not None and self.work_card_allocation_id is not None:
            if self.batch_work_card.work_card_id != self.work_card_allocation.work_card_id:
                raise ValidationError({'work_card_allocation': '订单分配必须属于本缸批工卡。'})


class WorkCardOperation(ErpModel):
    """工卡计划工序。"""

    is_skipped = models.BooleanField('已明确跳过', default=False)
    skip_reason = models.TextField('跳过原因', blank=True)

    # 原物理来源：JobProcess.SheetSeries
    work_card = models.ForeignKey(
        'erp_production.WorkCard',
        verbose_name='工卡',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_work_card_set",
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

    route_step = models.ForeignKey(
        'erp_base.RouteStep',
        verbose_name='来源路线节点',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_route_step_set",
        blank=True,
        null=True,
    )

    # 原物理来源：JobProcess.StationID
    work_center = models.ForeignKey(
        'erp_base.WorkCenter',
        verbose_name='计划工作中心',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_work_center_set",
        blank=True,
        null=True,
    )

    is_required = models.BooleanField(
        '必经节点快照',
    )

    planned_minutes = models.DecimalField(
        '计划时长分钟',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    predecessor = models.ForeignKey(
        'erp_production.WorkCardOperation',
        verbose_name='工卡前置节点',
        on_delete=models.RESTRICT,
        related_name="%(app_label)s_%(class)s_predecessor_set",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_production_workcardoperation"
        verbose_name = '工卡计划工序'
        verbose_name_plural = '工卡计划工序'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['work_card', 'sequence'], name='erp_production_workcardoperation_identity_uniq'),
            models.CheckConstraint(condition=Q(sequence__gt=0), name='erp_production_workcardoperation_sequence_positive'),
            models.CheckConstraint(condition=Q(predecessor__isnull=True) | ~Q(predecessor=F("pk")), name='erp_production_workcardoperation_predecessor_not_self'),
        ]

    def clean(self):
        super().clean()
        if self.predecessor_id is not None:
            if self.predecessor.work_card_id != self.work_card_id or self.predecessor.sequence >= self.sequence:
                raise ValidationError({'predecessor': '前置节点必须在同一对象内，且顺序早于当前节点。'})


class OperationParameter(ErpModel):
    """工卡工艺参数快照。"""

    operation = models.ForeignKey(
        'erp_production.WorkCardOperation',
        verbose_name='工卡计划工序',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_operation_set",
    )

    sequence = models.IntegerField(
        '参数序号',
    )

    # 原物理来源：JobProcess.PPName01 … JobProcess.PPName30
    name = models.CharField(
        '参数名',
        max_length=255,
    )

    # 原物理来源：JobProcess.TheoryValue01 … JobProcess.TheoryValue30
    required_value_text = models.TextField(
        '设定值快照',
        blank=True,
    )

    unit_text = models.CharField(
        '单位说明',
        max_length=64,
        blank=True,
    )

    class Meta:
        db_table = "erp_production_operationparameter"
        verbose_name = '工卡工艺参数快照'
        verbose_name_plural = '工卡工艺参数快照'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['operation', 'sequence'], name='erp_production_operationparameter_identity_uniq'),
            models.CheckConstraint(condition=Q(sequence__gt=0), name='erp_production_operationparameter_sequence_positive'),
        ]


class WorkCardRequirement(ErpModel):
    """工卡附加技术与包装要求。"""

    # 原物理来源：JobAtte.SheetSeries
    work_card = models.ForeignKey(
        'erp_production.WorkCard',
        verbose_name='工卡',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_work_card_set",
    )

    source_order_requirement = models.ForeignKey(
        'erp_sales.SalesLineRequirement',
        verbose_name='来源订单要求',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_source_order_requirement_set",
        blank=True,
        null=True,
    )

    # 原物理来源：JobAtte.FieldType
    namespace = models.CharField(
        '基础数据类别',
        max_length=20,
    )

    # 原物理来源：JobAtte.AtteCode
    code = models.CharField(
        '事项代码',
        max_length=10,
    )

    # 原物理来源：JobAtte.Description
    name_snapshot = models.CharField(
        '描述',
        max_length=500,
        blank=True,
        null=True,
    )

    # 原物理来源：JobAtte.AtteValue
    value_text = models.CharField(
        '事项内容',
        max_length=500,
    )

    class Meta:
        db_table = "erp_production_workcardrequirement"
        verbose_name = '工卡附加技术与包装要求'
        verbose_name_plural = '工卡附加技术与包装要求'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['work_card', 'namespace', 'code'], name='erp_production_workcardrequirement_identity_uniq'),
        ]


class ScheduleAssignment(ErpModel):
    """排产记录。"""

    change_reason = models.TextField('改排或取消原因', blank=True)
    previous_assignment = models.ForeignKey('self', verbose_name='原安排', null=True,
        blank=True, on_delete=models.PROTECT, related_name='replacement_assignments')

    batch = models.ForeignKey(
        'erp_production.DyeBatch',
        verbose_name='缸批',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_batch_set",
        blank=True,
        null=True,
    )

    operation = models.ForeignKey(
        'erp_production.WorkCardOperation',
        verbose_name='计划工序',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_operation_set",
    )

    machine = models.ForeignKey(
        'erp_base.Machine',
        verbose_name='机台',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_machine_set",
    )

    planned_start = models.DateTimeField(
        '计划开始',
    )

    planned_end = models.DateTimeField(
        '计划结束',
    )

    version = models.IntegerField(
        '排程版本',
        default=1,
    )

    status = models.CharField(
        '排程状态',
        max_length=24,
        choices=choices.ScheduleStatus.choices,
        default=choices.ScheduleStatus.PLANNED,
    )

    class Meta:
        db_table = "erp_production_scheduleassignment"
        verbose_name = '排产记录'
        verbose_name_plural = '排产记录'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['operation', 'version'], name='erp_production_scheduleassignment_identity_uniq'),
            models.UniqueConstraint(fields=['operation'], name='erp_production_scheduleassignment_active_no_batch_uniq', condition=Q(status__in=[choices.ScheduleStatus.PLANNED, choices.ScheduleStatus.RELEASED], batch__isnull=True)),
            models.UniqueConstraint(fields=['operation', 'batch'], name='erp_production_scheduleassignment_active_batch_uniq', condition=Q(status__in=[choices.ScheduleStatus.PLANNED, choices.ScheduleStatus.RELEASED], batch__isnull=False)),
            models.CheckConstraint(condition=Q(version__gt=0), name='erp_production_scheduleassignment_version_positive'),
            models.CheckConstraint(condition=Q(status__in=choices.ScheduleStatus.values), name='erp_production_scheduleassignment_status_valid'),
            models.CheckConstraint(condition=Q(planned_end__gt=F("planned_start")), name='erp_production_scheduleassignment_time_order'),
        ]
        indexes = [
            models.Index(fields=['machine', 'planned_start'], name='pro_scheduleassignment_1'),
        ]

    def clean(self):
        super().clean()
        if self.batch_id is not None and self.operation_id is not None:
            if not DyeBatchWorkCard.objects.filter(batch_id=self.batch_id, work_card_id=self.operation.work_card_id).exists():
                raise ValidationError({'batch': '缸批必须包含本计划工序的工卡。'})


class OperationExecution(ErpModel):
    """实际工序执行。"""

    physical_execution = models.ForeignKey('erp_production.PhysicalBatchExecution',
        verbose_name='同缸物理执行', null=True, blank=True, on_delete=models.PROTECT,
        related_name='member_executions')

    # 原物理来源：WProcess.JobSheetNo; WProcess.ProcessNo
    operation = models.ForeignKey(
        'erp_production.WorkCardOperation',
        verbose_name='工卡计划节点',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_operation_set",
    )

    batch = models.ForeignKey(
        'erp_production.DyeBatch',
        verbose_name='缸批',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_batch_set",
        blank=True,
        null=True,
    )

    execution_number = models.IntegerField(
        '执行轮次',
    )

    # 原物理来源：WProcess.MachineID
    machine = models.ForeignKey(
        'erp_base.Machine',
        verbose_name='实际机台',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_machine_set",
        blank=True,
        null=True,
    )

    # 原物理来源：WProcess.ShiftID
    shift = models.ForeignKey(
        'erp_base.Shift',
        verbose_name='实际班次',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_shift_set",
        blank=True,
        null=True,
    )

    # 原物理来源：WProcess.StartTime
    started_at = models.DateTimeField(
        '开始时间',
        blank=True,
        null=True,
    )

    # 原物理来源：WProcess.EndTime
    ended_at = models.DateTimeField(
        '结束时间',
        blank=True,
        null=True,
    )

    # 原物理来源：WProcess.PrevQty
    input_quantity = models.DecimalField(
        '投入数量',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    input_unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='投入单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_input_unit_set",
        blank=True,
        null=True,
    )

    # 原物理来源：WProcess.WorkQty
    output_quantity = models.DecimalField(
        '有效产出数量',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    output_unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='产出单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_output_unit_set",
        blank=True,
        null=True,
    )

    # 原物理来源：WProcess.CurrKg
    output_mass_kg = models.DecimalField(
        '重量',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：WProcess.CurrMeter
    output_length_m = models.DecimalField(
        '长度',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：WProcess.CurrRolls
    output_pieces = models.DecimalField(
        '粒数',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：WProcess.DefectQty
    defect_quantity = models.DecimalField(
        '缺陷数量',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：WProcess.Status
    status = models.CharField(
        '执行状态',
        max_length=24,
        choices=choices.ExecutionStatus.choices,
        default=choices.ExecutionStatus.PLANNED,
    )

    # 原物理来源：WProcess.QualityMemo
    quality_note = models.CharField(
        '现场质量说明',
        max_length=20,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_production_operationexecution"
        verbose_name = '实际工序执行'
        verbose_name_plural = '实际工序执行'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['operation', 'execution_number'], name='erp_production_operationexecution_identity_uniq'),
            models.CheckConstraint(condition=Q(execution_number__gt=0), name='erp_production_operationexecution_execution_number_positive'),
            models.CheckConstraint(condition=Q(status__in=choices.ExecutionStatus.values), name='erp_production_operationexecution_status_valid'),
            models.CheckConstraint(condition=Q(started_at__isnull=True) | Q(ended_at__isnull=True) | Q(ended_at__gte=F("started_at")), name='erp_production_operationexecution_time_order'),
        ]
        indexes = [
            models.Index(fields=['operation', 'status'], name='pro_operationexecution_1'),
            models.Index(fields=['machine', 'started_at'], name='pro_operationexecution_2'),
        ]

    def clean(self):
        super().clean()
        if self.batch_id is not None and self.operation_id is not None:
            if not DyeBatchWorkCard.objects.filter(batch_id=self.batch_id, work_card_id=self.operation.work_card_id).exists():
                raise ValidationError({'batch': '缸批必须包含本计划工序的工卡。'})
        if self.input_quantity is not None and self.input_unit_id is None:
            raise ValidationError({'input_unit': '已填写数量时必须明确计量单位。'})
        if self.output_quantity is not None and self.output_unit_id is None:
            raise ValidationError({'output_unit': '已填写数量时必须明确计量单位。'})

    @property
    def elapsed_minutes(self):
        return calculate_elapsed_minutes(self.started_at, self.ended_at)


class ExecutionWorker(ErpModel):
    """执行人员。"""

    execution = models.ForeignKey(
        'erp_production.OperationExecution',
        verbose_name='执行记录',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_execution_set",
    )

    # 原物理来源：WProcess.EmpID
    employee = models.ForeignKey(
        'erp_base.Employee',
        verbose_name='员工',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_employee_set",
    )

    role = models.CharField(
        '参与角色',
        max_length=64,
        blank=True,
    )

    participation_minutes = models.DecimalField(
        '参与分钟',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_production_executionworker"
        verbose_name = '执行人员'
        verbose_name_plural = '执行人员'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['execution', 'employee', 'role'], name='erp_production_executionworker_identity_uniq'),
        ]


class ExecutionMeasurement(ErpModel):
    """执行实际参数。"""

    execution = models.ForeignKey(
        'erp_production.OperationExecution',
        verbose_name='执行记录',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_execution_set",
    )

    planned_parameter = models.ForeignKey(
        'erp_production.OperationParameter',
        verbose_name='计划参数',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_planned_parameter_set",
        blank=True,
        null=True,
    )

    # 原物理来源：JobProcess.PPName01 … JobProcess.PPName30
    name = models.CharField(
        '参数名称快照',
        max_length=255,
    )

    # 原物理来源：JobProcess.ActualValue01 … JobProcess.ActualValue30
    value_text = models.TextField(
        '实际值文本',
    )

    measured_at = models.DateTimeField(
        '采集时间',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_production_executionmeasurement"
        verbose_name = '执行实际参数'
        verbose_name_plural = '执行实际参数'
        ordering = ["-id"]

    def clean(self):
        super().clean()
        if self.planned_parameter_id is not None and self.execution_id is not None:
            if self.planned_parameter.operation_id != self.execution.operation_id:
                raise ValidationError({'planned_parameter': '实际参数必须对应本次执行的计划节点。'})


class ExecutionCorrection(ErpModel):
    """报工更正。"""

    before_values = models.JSONField('更正前有效事实', default=dict, blank=True)
    after_values = models.JSONField('更正后有效事实', default=dict, blank=True)

    execution = models.ForeignKey(
        'erp_production.OperationExecution',
        verbose_name='原执行记录',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_execution_set",
    )

    reason = models.TextField(
        '原因',
    )

    corrected_at = models.DateTimeField(
        '更正时间',
    )

    changes_quantity = models.BooleanField(
        '本次是否更正产出量',
        default=False,
    )

    new_output_quantity = models.DecimalField(
        '更正后的产出量',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    changes_mass = models.BooleanField(
        '本次是否更正重量',
        default=False,
    )

    new_output_mass_kg = models.DecimalField(
        '更正后的重量kg',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    changes_start_time = models.BooleanField(
        '本次是否更正开始时间',
        default=False,
    )

    new_started_at = models.DateTimeField(
        '更正后的开始',
        blank=True,
        null=True,
    )

    changes_end_time = models.BooleanField(
        '本次是否更正结束时间',
        default=False,
    )

    new_ended_at = models.DateTimeField(
        '更正后的结束',
        blank=True,
        null=True,
    )

    approved_by = models.ForeignKey(
        'erp_base.Employee',
        verbose_name='确认人',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_approved_by_set",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_production_executioncorrection"
        verbose_name = '报工更正'
        verbose_name_plural = '报工更正'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(changes_quantity=True) | Q(changes_mass=True) | Q(changes_start_time=True) | Q(changes_end_time=True), name='erp_production_executioncorrection_has_change'),
        ]


class ProductionRecipe(ErpModel):
    """生产采用配方快照。"""

    batch = models.ForeignKey(
        'erp_production.DyeBatch',
        verbose_name='缸批',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_batch_set",
    )

    recipe_version = models.ForeignKey(
        'erp_sampling.RecipeVersion',
        verbose_name='来源配方版本',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_recipe_version_set",
    )

    adoption_number = models.IntegerField(
        '采用轮次',
    )

    adopted_at = models.DateTimeField(
        '采用时间',
    )

    dry_mass_kg = models.DecimalField(
        '计算用干料重量kg',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    status = models.CharField(
        '采用状态',
        max_length=24,
        choices=choices.AdoptionStatus.choices,
        default=choices.AdoptionStatus.ACTIVE,
    )

    class Meta:
        db_table = "erp_production_productionrecipe"
        verbose_name = '生产采用配方快照'
        verbose_name_plural = '生产采用配方快照'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['batch', 'adoption_number'], name='erp_production_productionrecipe_identity_uniq'),
            models.UniqueConstraint(fields=['batch'], name='erp_production_productionrecipe_active_uniq', condition=Q(status=choices.AdoptionStatus.ACTIVE)),
            models.CheckConstraint(condition=Q(adoption_number__gt=0), name='erp_production_productionrecipe_adoption_number_positive'),
            models.CheckConstraint(condition=Q(status__in=choices.AdoptionStatus.values), name='erp_production_productionrecipe_status_valid'),
        ]


class MaterialPlanStage(ErpModel):
    """生产用料阶段。"""

    bath_density_kg_per_litre = models.DecimalField('浴液密度kg/L', max_digits=20,
        decimal_places=6, null=True, blank=True)

    production_recipe = models.ForeignKey(
        'erp_production.ProductionRecipe',
        verbose_name='生产采用配方',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_production_recipe_set",
    )

    # 原物理来源：StuffWeightPhase.PhaseNo
    sequence = models.IntegerField(
        '阶段顺序',
    )

    recipe_stage = models.ForeignKey(
        'erp_sampling.RecipeStage',
        verbose_name='来源配方阶段',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_recipe_stage_set",
        blank=True,
        null=True,
    )

    phase_name_snapshot = models.CharField(
        '染程名称快照',
        max_length=200,
        blank=True,
    )

    # 原物理来源：StuffWeightPhase.PhaseID
    phase = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='染程类型',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_phase_set",
        blank=True,
        null=True,
    )

    # 原物理来源：StuffWeightPhase.ProgramID
    curve_version = models.ForeignKey(
        'erp_sampling.ProcessCurveVersion',
        verbose_name='采用工艺曲线版本',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_curve_version_set",
        blank=True,
        null=True,
    )

    # 原物理来源：StuffWeightPhase.PH
    ph_text = models.CharField(
        'pH要求快照',
        max_length=10,
        blank=True,
        null=True,
    )

    # 原物理来源：StuffWeightPhase.BathRatio
    bath_ratio = models.DecimalField(
        '浴比快照',
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
    )

    bath_ratio_basis = models.CharField(
        '浴比定义快照',
        max_length=24,
        choices=choices.BathRatioBasis.choices,
        blank=True,
        null=True,
    )

    # 原物理来源：StuffWeightPhase.WaterQty
    water_amount = models.DecimalField(
        '采用水量',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    water_unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='水量单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_water_unit_set",
        blank=True,
        null=True,
    )

    # 原物理来源：StuffWeightPhase.Temperature
    temperature_c = models.DecimalField(
        '温度快照℃',
        max_digits=5,
        decimal_places=1,
        blank=True,
        null=True,
    )

    # 原物理来源：StuffWeightPhase.Minutes
    minutes = models.DecimalField(
        '阶段分钟',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_production_materialplanstage"
        verbose_name = '生产用料阶段'
        verbose_name_plural = '生产用料阶段'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['production_recipe', 'sequence'], name='erp_production_materialplanstage_identity_uniq'),
            models.CheckConstraint(condition=Q(sequence__gt=0), name='erp_production_materialplanstage_sequence_positive'),
            models.CheckConstraint(condition=Q(bath_ratio_basis__isnull=True) | Q(bath_ratio_basis__in=choices.BathRatioBasis.values), name='erp_production_materialplanstage_bath_ratio_basis_valid'),
        ]

    def clean(self):
        super().clean()
        if self.recipe_stage_id is not None and self.production_recipe_id is not None:
            if self.recipe_stage.version_id != self.production_recipe.recipe_version_id:
                raise ValidationError({'recipe_stage': '计划阶段必须来自所采用的配方版本。'})
        if self.water_amount is not None and self.water_unit_id is None:
            raise ValidationError({'water_unit': '已填写数量时必须明确计量单位。'})


class MaterialPlanLine(ErpModel):
    """生产用料计划。"""

    calculation_snapshot = models.JSONField('计划计算依据', default=dict, blank=True)

    stage = models.ForeignKey(
        'erp_production.MaterialPlanStage',
        verbose_name='生产阶段',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_stage_set",
    )

    # 原物理来源：StuffWeightDetail.StuffNo
    sequence = models.IntegerField(
        '行顺序',
    )

    recipe_ingredient = models.ForeignKey(
        'erp_sampling.RecipeIngredient',
        verbose_name='来源配方物料行',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_recipe_ingredient_set",
        blank=True,
        null=True,
    )

    # 原物理来源：StuffWeightDetail.StuffID
    material = models.ForeignKey(
        'erp_base.Material',
        verbose_name='实际计划物料',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_material_set",
    )

    # 原物理来源：StuffWeightDetail.OirDosage
    original_dosage = models.DecimalField(
        '原剂量',
        max_digits=15,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：StuffWeightDetail.AdjustDosage
    adjustment_percent = models.DecimalField(
        '剂量调整百分比',
        max_digits=15,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：StuffWeightDetail.Dosage
    adopted_dosage = models.DecimalField(
        '采用剂量',
        max_digits=20,
        decimal_places=6,
    )

    # 原物理来源：StuffWeightDetail.RecipeUnit
    dosage_basis = models.CharField(
        '剂量基准',
        max_length=24,
        choices=choices.DosageBasis.choices,
    )

    # 原物理来源：StuffWeightDetail.OriNeedQty
    original_required_quantity = models.DecimalField(
        '原需求量',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # 原物理来源：StuffWeightDetail.NeedQty
    required_quantity = models.DecimalField(
        '本次计划需用量',
        max_digits=20,
        decimal_places=6,
    )

    # 原物理来源：StuffWeightDetail.WeightUnit
    quantity_unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='需用单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_quantity_unit_set",
    )

    class Meta:
        db_table = "erp_production_materialplanline"
        verbose_name = '生产用料计划'
        verbose_name_plural = '生产用料计划'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['stage', 'sequence'], name='erp_production_materialplanline_identity_uniq'),
            models.CheckConstraint(condition=Q(sequence__gt=0), name='erp_production_materialplanline_sequence_positive'),
            models.CheckConstraint(condition=Q(dosage_basis__in=choices.DosageBasis.values), name='erp_production_materialplanline_dosage_basis_valid'),
            models.CheckConstraint(condition=Q(adopted_dosage__gte=0), name='erp_production_materialplanline_adopted_dosage_nonnegative'),
            models.CheckConstraint(condition=Q(required_quantity__gte=0), name='erp_production_materialplanline_required_quantity_nonnegative'),
        ]

    def clean(self):
        super().clean()
        if self.material_id is not None and self.material.kind != choices.MaterialKind.CHEMICAL:
            raise ValidationError({'material': '配方和称料只能引用染化料。'})
        if self.recipe_ingredient_id is not None and self.stage_id is not None:
            if self.recipe_ingredient.stage_id != self.stage.recipe_stage_id:
                raise ValidationError({'recipe_ingredient': '物料来源必须属于本采用阶段的配方阶段。'})

    @property
    def calculated_adopted_dosage(self):
        return calculate_adopted_dosage(self.original_dosage, self.adjustment_percent)


class WeighingOrder(ErpModel):
    """称料及加料单。"""

    # 原物理来源：StuffWeight.SheetNo
    number = models.CharField(
        '称料单号',
        max_length=20,
        unique=True,
    )

    # 原物理来源：StuffWeight.SheetDate
    document_at = models.DateTimeField(
        '单据日期',
    )

    batch = models.ForeignKey(
        'erp_production.DyeBatch',
        verbose_name='缸批',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_batch_set",
    )

    # 原物理来源：StuffWeight.SheetKind
    kind = models.CharField(
        '料单类型',
        max_length=24,
        choices=choices.WeighingKind.choices,
    )

    production_recipe = models.ForeignKey(
        'erp_production.ProductionRecipe',
        verbose_name='采用配方',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_production_recipe_set",
        blank=True,
        null=True,
    )

    reason = models.TextField(
        '加料或后处理原因',
        blank=True,
    )

    # 原物理来源：StuffWeight.SheetStatus
    status = models.CharField(
        '料单状态',
        max_length=24,
        choices=choices.WeighingStatus.choices,
        default=choices.WeighingStatus.DRAFT,
    )

    class Meta:
        db_table = "erp_production_weighingorder"
        verbose_name = '称料及加料单'
        verbose_name_plural = '称料及加料单'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(kind__in=choices.WeighingKind.values), name='erp_production_weighingorder_kind_valid'),
            models.CheckConstraint(condition=Q(status__in=choices.WeighingStatus.values), name='erp_production_weighingorder_status_valid'),
        ]
        indexes = [
            models.Index(fields=['status', 'document_at'], name='pro_weighingorder_1'),
        ]

    def clean(self):
        super().clean()
        if self.production_recipe_id is not None and self.production_recipe.batch_id != self.batch_id:
            raise ValidationError({'production_recipe': '采用配方必须属于本缸批。'})


class WeighingStage(ErpModel):
    """料单染程阶段。"""

    # 原物理来源：StuffWeightPhase.SheetSeries
    order = models.ForeignKey(
        'erp_production.WeighingOrder',
        verbose_name='称料单',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_order_set",
    )

    # 原物理来源：StuffWeightPhase.PhaseNo
    sequence = models.IntegerField(
        '本料单染程序号',
    )

    plan_stage = models.ForeignKey(
        'erp_production.MaterialPlanStage',
        verbose_name='来源采用计划阶段',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_plan_stage_set",
        blank=True,
        null=True,
    )

    phase_name_snapshot = models.CharField(
        '采用阶段名称快照',
        max_length=200,
        blank=True,
    )

    # 原物理来源：StuffWeightPhase.PhaseID
    phase = models.ForeignKey(
        'erp_base.BusinessChoice',
        verbose_name='采用染程类型',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_phase_set",
        blank=True,
        null=True,
    )

    # 原物理来源：StuffWeightPhase.ProgramID
    curve_version = models.ForeignKey(
        'erp_sampling.ProcessCurveVersion',
        verbose_name='本料单工艺曲线版本',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_curve_version_set",
        blank=True,
        null=True,
    )

    # 原物理来源：StuffWeightPhase.PH
    ph_text = models.CharField(
        'pH要求文本',
        max_length=10,
        blank=True,
        null=True,
    )

    # 原物理来源：StuffWeightPhase.BathRatio
    bath_ratio = models.DecimalField(
        '采用浴比',
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
    )

    bath_ratio_basis = models.CharField(
        '本阶段浴比定义',
        max_length=24,
        choices=choices.BathRatioBasis.choices,
        blank=True,
        null=True,
    )

    # 原物理来源：StuffWeightPhase.WaterQty
    water_amount = models.DecimalField(
        '本阶段采用水量',
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True,
    )

    water_unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='水量单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_water_unit_set",
        blank=True,
        null=True,
    )

    # 原物理来源：StuffWeightPhase.Temperature
    temperature_c = models.DecimalField(
        '阶段温度℃',
        max_digits=5,
        decimal_places=1,
        blank=True,
        null=True,
    )

    # 原物理来源：StuffWeightPhase.Minutes
    minutes = models.DecimalField(
        '阶段分钟参数',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "erp_production_weighingstage"
        verbose_name = '料单染程阶段'
        verbose_name_plural = '料单染程阶段'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['order', 'sequence'], name='erp_production_weighingstage_identity_uniq'),
            models.CheckConstraint(condition=Q(sequence__gt=0), name='erp_production_weighingstage_sequence_positive'),
            models.CheckConstraint(condition=Q(bath_ratio_basis__isnull=True) | Q(bath_ratio_basis__in=choices.BathRatioBasis.values), name='erp_production_weighingstage_bath_ratio_basis_valid'),
        ]

    def clean(self):
        super().clean()
        if self.plan_stage_id is not None and self.order_id is not None:
            if self.plan_stage.production_recipe_id != self.order.production_recipe_id:
                raise ValidationError({'plan_stage': '来源阶段必须属于本料单的采用配方。'})
        if self.water_amount is not None and self.water_unit_id is None:
            raise ValidationError({'water_unit': '已填写数量时必须明确计量单位。'})


class WeighingLine(ErpModel):
    """称料明细。"""

    # 原物理来源：StuffWeightDetail.SheetSeries; StuffWeightDetail.PhaseNo
    stage = models.ForeignKey(
        'erp_production.WeighingStage',
        verbose_name='料单染程阶段',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_stage_set",
    )

    sequence = models.IntegerField(
        '明细顺序',
    )

    plan_line = models.ForeignKey(
        'erp_production.MaterialPlanLine',
        verbose_name='计划物料行',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_plan_line_set",
        blank=True,
        null=True,
    )

    # 原物理来源：StuffWeightDetail.StuffID
    material = models.ForeignKey(
        'erp_base.Material',
        verbose_name='染化料',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_material_set",
    )

    # 原物理来源：StuffWeightDetail.NeedQty
    planned_quantity = models.DecimalField(
        '采用计划量快照',
        max_digits=20,
        decimal_places=6,
    )

    # 原物理来源：StuffWeightDetail.WeightUnit
    unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='称料单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_unit_set",
    )

    # 原物理来源：StuffWeightDetail.Status
    status = models.CharField(
        '明细状态',
        max_length=24,
        choices=choices.WeighingLineStatus.choices,
        default=choices.WeighingLineStatus.PLANNED,
    )

    class Meta:
        db_table = "erp_production_weighingline"
        verbose_name = '称料明细'
        verbose_name_plural = '称料明细'
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=['stage', 'sequence'], name='erp_production_weighingline_identity_uniq'),
            models.CheckConstraint(condition=Q(sequence__gt=0), name='erp_production_weighingline_sequence_positive'),
            models.CheckConstraint(condition=Q(status__in=choices.WeighingLineStatus.values), name='erp_production_weighingline_status_valid'),
            models.CheckConstraint(condition=Q(planned_quantity__gte=0), name='erp_production_weighingline_planned_quantity_nonnegative'),
        ]

    def clean(self):
        super().clean()
        if self.material_id is not None and self.material.kind != choices.MaterialKind.CHEMICAL:
            raise ValidationError({'material': '配方和称料只能引用染化料。'})
        if self.plan_line_id is not None and self.stage_id is not None:
            if self.plan_line.stage_id != self.stage.plan_stage_id or self.plan_line.material_id != self.material_id:
                raise ValidationError({'plan_line': '计划行必须属于本料单阶段，并引用相同物料。'})


class WeighingRecord(ErpModel):
    """一次实际称量。"""

    void_reason = models.TextField('作废原因', blank=True)
    voided_at = models.DateTimeField('作废时间', null=True, blank=True)

    line = models.ForeignKey(
        'erp_production.WeighingLine',
        verbose_name='称料明细',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_line_set",
    )

    # 原物理来源：StuffWeightDetail.RealQty
    quantity = models.DecimalField(
        '实称数量',
        max_digits=20,
        decimal_places=6,
    )

    unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='实称单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_unit_set",
    )

    source = models.CharField(
        '数量来源',
        max_length=24,
        choices=choices.MeasurementSource.choices,
    )

    measured_at = models.DateTimeField(
        '称量时间',
    )

    operator = models.ForeignKey(
        'erp_base.Employee',
        verbose_name='称料人员',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_operator_set",
        blank=True,
        null=True,
    )

    original_record = models.ForeignKey(
        'erp_production.WeighingRecord',
        verbose_name='被更正称量',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_original_record_set",
        blank=True,
        null=True,
    )

    is_void = models.BooleanField(
        '该称量已作废',
        default=False,
    )

    class Meta:
        db_table = "erp_production_weighingrecord"
        verbose_name = '一次实际称量'
        verbose_name_plural = '一次实际称量'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(source__in=choices.MeasurementSource.values), name='erp_production_weighingrecord_source_valid'),
            models.CheckConstraint(condition=Q(original_record__isnull=True) | ~Q(original_record=F("pk")), name='erp_production_weighingrecord_original_record_not_self'),
            models.CheckConstraint(condition=Q(quantity__gt=0), name='erp_production_weighingrecord_quantity_positive'),
        ]


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
        'erp_production.QualityInspection',
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
        'erp_production.QualityInspection',
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
        'erp_production.QualityInspection',
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
        'erp_production.QualityInspection',
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
        'erp_production.QualityDisposition',
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


class ReworkOrder(ErpModel):
    """返修任务。"""

    number = models.CharField(
        '返修号',
        max_length=64,
        unique=True,
    )

    # 原物理来源：JobSheet.OriJobsheetNo
    original_work_card = models.ForeignKey(
        'erp_production.WorkCard',
        verbose_name='原工卡',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_original_work_card_set",
    )

    disposition = models.ForeignKey(
        'erp_production.QualityDisposition',
        verbose_name='返修处置',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_disposition_set",
    )

    rework_work_card = models.OneToOneField(
        'erp_production.WorkCard',
        verbose_name='返修工卡',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_rework_work_card_set",
        blank=True,
        null=True,
    )

    quantity = models.DecimalField(
        '返修量',
        max_digits=20,
        decimal_places=6,
    )

    unit = models.ForeignKey(
        'erp_base.Unit',
        verbose_name='单位',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_unit_set",
    )

    # 原物理来源：JobSheet.RedoReasonID
    reason = models.TextField(
        '返修原因',
    )

    status = models.CharField(
        '返修状态',
        max_length=24,
        choices=choices.ReworkStatus.choices,
        default=choices.ReworkStatus.DRAFT,
    )

    class Meta:
        db_table = "erp_production_reworkorder"
        verbose_name = '返修任务'
        verbose_name_plural = '返修任务'
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(condition=Q(status__in=choices.ReworkStatus.values), name='erp_production_reworkorder_status_valid'),
            models.CheckConstraint(condition=Q(quantity__gt=0), name='erp_production_reworkorder_quantity_positive'),
        ]
