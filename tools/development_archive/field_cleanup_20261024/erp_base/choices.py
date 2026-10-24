"""染色 ERP 固定业务状态；基础代码字典由 BusinessChoice 维护。"""
from django.db import models


class PartyRole(models.TextChoices):
    CUSTOMER = 'customer', '客户'
    SUPPLIER = 'supplier', '供应商'
    SUBCONTRACTOR = 'subcontractor', '外协方'

class AddressKind(models.TextChoices):
    REGISTERED = 'registered', '单位地址'
    DELIVERY = 'delivery', '收货地址'
    RETURN = 'return', '退回地址'

class UnitDimension(models.TextChoices):
    MASS = 'mass', '质量'
    LENGTH = 'length', '长度'
    VOLUME = 'volume', '体积'
    COUNT = 'count', '计数'
    AREA = 'area', '面积'
    TIME = 'time', '时间'
    TEMPERATURE = 'temperature', '温度'

class MaterialKind(models.TextChoices):
    YARN = 'yarn', '纱线'
    FABRIC = 'fabric', '织物'
    CHEMICAL = 'chemical', '染化料'
    ACCESSORY = 'accessory', '机物料'
    PACKAGING = 'packaging', '包装物料'
    FUEL = 'fuel', '燃料'

class WarehouseKind(models.TextChoices):
    RAW = 'raw', '坯料'
    SEMI = 'semi', '半成品'
    FINISHED = 'finished', '成品'
    CHEMICAL = 'chemical', '染化料'
    ACCESSORY = 'accessory', '机物料'
    PACKAGING = 'packaging', '包装物料'
    FUEL = 'fuel', '燃料'
    MIXED = 'mixed', '混合仓'

class LocationKind(models.TextChoices):
    ZONE = 'zone', '库区'
    BIN = 'bin', '实际库位'

class PackagingKind(models.TextChoices):
    BAG = 'bag', '袋'
    CARTON = 'carton', '箱'
    TUBE = 'tube', '筒管'
    OTHER = 'other', '其他'

class OrderStatus(models.TextChoices):
    DRAFT = 'draft', '草稿'
    CONFIRMED = 'confirmed', '已确认'
    RUNNING = 'running', '执行中'
    COMPLETED = 'completed', '业务完成'
    CLOSED = 'closed', '结案'
    CANCELLED = 'cancelled', '取消'

class ApprovalStatus(models.TextChoices):
    DRAFT = 'draft', '草稿'
    CONFIRMED = 'confirmed', '已确认'
    CANCELLED = 'cancelled', '取消'

class PurchaseRequestStatus(models.TextChoices):
    DRAFT = 'draft', '草稿'
    CONFIRMED = 'confirmed', '已确认'
    CLOSED = 'closed', '结案'
    CANCELLED = 'cancelled', '取消'

class PriceDocumentKind(models.TextChoices):
    QUOTATION = 'quotation', '报价'
    AGREED = 'agreed', '确价'

class DeliveryStatus(models.TextChoices):
    DRAFT = 'draft', '草稿'
    CONFIRMED = 'confirmed', '已确认'
    ISSUED = 'issued', '已出库'
    DELIVERED = 'delivered', '已交付'
    CANCELLED = 'cancelled', '取消'

class ReturnStatus(models.TextChoices):
    DRAFT = 'draft', '草稿'
    CONFIRMED = 'confirmed', '已确认'
    RECEIVED = 'received', '已收回'
    ISSUED = 'issued', '已退货出库'
    CLOSED = 'closed', '结案'
    CANCELLED = 'cancelled', '取消'

class ComplaintStatus(models.TextChoices):
    OPEN = 'open', '已登记'
    HANDLING = 'handling', '处理中'
    CLOSED = 'closed', '已关闭'

class PurchaseStatus(models.TextChoices):
    DRAFT = 'draft', '草稿'
    CONFIRMED = 'confirmed', '已确认'
    PARTIAL_RECEIVED = 'partial_received', '部分收货'
    RECEIVED = 'received', '已收货'
    CLOSED = 'closed', '结案'
    CANCELLED = 'cancelled', '取消'

class SampleStatus(models.TextChoices):
    DRAFT = 'draft', '草稿'
    RECEIVED = 'received', '已收样'
    ASSIGNED = 'assigned', '已分配'
    RUNNING = 'running', '试验中'
    SENT = 'sent', '已送版'
    CONFIRMED = 'confirmed', '已确板'
    CLOSED = 'closed', '结案'
    CANCELLED = 'cancelled', '取消'

class SampleLineStatus(models.TextChoices):
    PENDING = 'pending', '待分配'
    ASSIGNED = 'assigned', '已分配'
    RUNNING = 'running', '试验中'
    SENT = 'sent', '已送版'
    ACCEPTED = 'accepted', '客户接受'
    REJECTED = 'rejected', '客户拒绝'
    CANCELLED = 'cancelled', '取消'

class TrialStatus(models.TextChoices):
    PLANNED = 'planned', '待试验'
    RUNNING = 'running', '试验中'
    COMPLETED = 'completed', '试验完成'
    CANCELLED = 'cancelled', '取消'

class SampleConfirmation(models.TextChoices):
    PENDING = 'pending', '待回复'
    ACCEPTED = 'accepted', '已接受'
    REJECTED = 'rejected', '已拒绝'

class RecipePurpose(models.TextChoices):
    TRIAL = 'trial', '试验配方'
    CONFIRMED = 'confirmed', '客户确板配方'
    STANDARD = 'standard', '通用标准配方'

class VersionStatus(models.TextChoices):
    DRAFT = 'draft', '草稿'
    APPROVED = 'approved', '已审核'
    ACTIVE = 'active', '使用中'
    RETIRED = 'retired', '停用'

class DosageBasis(models.TextChoices):
    OWF_PERCENT = 'owf_percent', '干料质量百分比'
    G_PER_LITRE = 'g_per_litre', '每升浴液克数'

class BathRatioBasis(models.TextChoices):
    MASS_PER_MASS = 'mass_per_mass', '浴液kg每干料kg'
    VOLUME_PER_MASS = 'volume_per_mass', '浴液L每干料kg'

class WorkCardStatus(models.TextChoices):
    DRAFT = 'draft', '草稿'
    RELEASED = 'released', '已下达'
    RUNNING = 'running', '生产中'
    COMPLETED = 'completed', '生产完成'
    CLOSED = 'closed', '结案'
    CANCELLED = 'cancelled', '取消'

class BatchStatus(models.TextChoices):
    PLANNED = 'planned', '待排产'
    SCHEDULED = 'scheduled', '已排产'
    RUNNING = 'running', '生产中'
    COMPLETED = 'completed', '生产完成'
    CLOSED = 'closed', '结案'
    CANCELLED = 'cancelled', '取消'

class ScheduleStatus(models.TextChoices):
    PLANNED = 'planned', '计划'
    RELEASED = 'released', '已下达'
    REPLACED = 'replaced', '已被替换'
    CANCELLED = 'cancelled', '取消'

class ExecutionStatus(models.TextChoices):
    PLANNED = 'planned', '待开工'
    RUNNING = 'running', '执行中'
    COMPLETED = 'completed', '已完成'
    CANCELLED = 'cancelled', '取消'

class AdoptionStatus(models.TextChoices):
    ACTIVE = 'active', '当前采用'
    REPLACED = 'replaced', '已替换'
    CANCELLED = 'cancelled', '取消'

class WeighingKind(models.TextChoices):
    NORMAL = 'normal', '常规'
    ADDITION = 'addition', '加料'
    AFTER_TREATMENT = 'after_treatment', '后处理'
    WASH = 'wash', '洗缸'

class WeighingStatus(models.TextChoices):
    DRAFT = 'draft', '草稿'
    CONFIRMED = 'confirmed', '已确认'
    PARTIAL_ISSUED = 'partial_issued', '部分领出'
    ISSUED = 'issued', '已领出'
    CLOSED = 'closed', '结束'
    CANCELLED = 'cancelled', '取消'

class WeighingLineStatus(models.TextChoices):
    PLANNED = 'planned', '计划'
    WEIGHED = 'weighed', '已称料'
    ISSUED = 'issued', '已领出'
    CLOSED = 'closed', '结束'

class MeasurementSource(models.TextChoices):
    MANUAL = 'manual', '人工实测'
    SCALE = 'scale', '秤采集'

class InspectionKind(models.TextChoices):
    INCOMING = 'incoming', '来料检验'
    IN_PROCESS = 'in_process', '过程检验'
    COLOR_SAMPLE = 'color_sample', '对色'
    FINAL = 'final', '终检'
    REINSPECTION = 'reinspection', '复检'

class InspectionResult(models.TextChoices):
    PENDING = 'pending', '待判定'
    PASS = 'pass', '合格'
    FAIL = 'fail', '不合格'

class DispositionKind(models.TextChoices):
    RELEASE = 'release', '放行'
    CONCESSION = 'concession', '让步放行'
    REWORK = 'rework', '返修'
    DOWNGRADE = 'downgrade', '降级'
    SCRAP = 'scrap', '报废'
    HOLD = 'hold', '隔离'

class ReworkStatus(models.TextChoices):
    DRAFT = 'draft', '草稿'
    RELEASED = 'released', '已下达'
    RUNNING = 'running', '返修中'
    REINSPECTED = 'reinspected', '已复检'
    CLOSED = 'closed', '结案'
    CANCELLED = 'cancelled', '取消'

class ReceiptKind(models.TextChoices):
    PURCHASE = 'purchase', '采购收货'
    CUSTOMER_MATERIAL = 'customer_material', '客供料'
    SEMI_OUTPUT = 'semi_output', '半成品产出'
    FINISHED_OUTPUT = 'finished_output', '成品产出'
    MATERIAL_RETURN = 'material_return', '生产退料'
    SALES_RETURN = 'sales_return', '客户退回'
    OPENING = 'opening', '期初'

class IssueKind(models.TextChoices):
    PRODUCTION = 'production', '生产领料'
    CHEMICAL = 'chemical', '化工领料'
    DELIVERY = 'delivery', '销售交付'
    PURCHASE_RETURN = 'purchase_return', '采购退货'
    CUSTOMER_MATERIAL_RETURN = 'customer_material_return', '客料退回'
    SUBCONTRACT = 'subcontract', '发外协'
    SCRAP = 'scrap', '报废'

class StockDocumentStatus(models.TextChoices):
    DRAFT = 'draft', '草稿'
    CONFIRMED = 'confirmed', '已确认'
    POSTED = 'posted', '已生效'
    REVERSED = 'reversed', '已冲销'
    CANCELLED = 'cancelled', '取消'

class QualityState(models.TextChoices):
    PENDING = 'pending', '待检'
    RELEASED = 'released', '可用'
    HELD = 'held', '隔离'
    REJECTED = 'rejected', '不合格'
    SCRAP = 'scrap', '待报废'

class CountStatus(models.TextChoices):
    DRAFT = 'draft', '草稿'
    COUNTING = 'counting', '盘点中'
    CONFIRMED = 'confirmed', '差异已确认'
    ADJUSTED = 'adjusted', '已调整'
    CANCELLED = 'cancelled', '取消'

class TransformationDirection(models.TextChoices):
    INPUT = 'input', '投入'
    OUTPUT = 'output', '产出'

class PackageStatus(models.TextChoices):
    DRAFT = 'draft', '草稿'
    PACKED = 'packed', '包装完成'
    RECEIVED = 'received', '已入库'
    ISSUED = 'issued', '已出库'
    RETURNED = 'returned', '已退回'
    VOID = 'void', '作废'

class NetMassBasis(models.TextChoices):
    WEIGHED_LESS_TARE = 'weighed_less_tare', '实称毛重扣皮重'
    FIXED_PIECE_MASS = 'fixed_piece_mass', '固定单粒质量'

class LabelPrintKind(models.TextChoices):
    FIRST = 'first', '首次'
    REPRINT = 'reprint', '重打'
