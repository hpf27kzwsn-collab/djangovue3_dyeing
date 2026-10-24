"""基础信息模型；字段来源见 docs/ERP模型实施说明.md。"""
from django.db import models
from core.models import CoreModel


class ErpModel(CoreModel):
    remarks = models.TextField("业务备注", blank=True)

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


from .legacy_models import LegacyImportBatch


from .source_models import (
    SourceDboAA,
    SourceDboAAA,
    SourceDboAAKC1,
    SourceDboABC,
    SourceDboADD,
    SourceDboAEE,
    SourceDboC,
    SourceDboCbbz1109,
    SourceDboCkpd20221024,
    SourceDboCkpd20221024bak,
    SourceDboCkpd20221027,
    SourceDboCksgz20221024,
    SourceDboCpdqkc20221024,
    SourceDboDXCHANLIANG,
    SourceDboHypf,
    SourceDboItbak20221120,
    SourceDboItbak20221121,
    SourceDboJxtbzyq,
    SourceDboJxtkckh,
    SourceDboNHTJ,
    SourceDboPbpd20230422,
    SourceDboPS20221218,
    SourceDboRansechugangtongji,
    SourceDboRansetongji,
    SourceDboRCDDZJB,
    SourceDboShda,
    SourceDboSHIFT,
    SourceDboSHLEIXING,
    SourceDboTmp20221104,
    SourceDboXxtcbkc20221023,
    SourceDboXxtzzp20221024,
    SourceDboZhenzhibaobiao,
    SourceDboZJHXMXBB,
    SourceDyeACGroup,
    SourceDyeAcholiday,
    SourceDyeACUnlockComb,
    SourceDyeAPPUploadFilesInfo,
    SourceDyeAPPUploadFilesInfoDel,
    SourceDyeArrivalNotice,
    SourceDyeArrivalNoticeDetail,
    SourceDyeAttachment,
    SourceDyeAttParam,
    SourceDyeAuditedExc,
    SourceDyeAUTHDEVICE,
    SourceDyeBalancingConditions,
    SourceDyeBaseCase,
    SourceDyeBaseCaseDetail,
    SourceDyeBiotemplate,
    SourceDyeClockShift,
    SourceDyeCompensatedetail,
    SourceDyeCompensatemain,
    SourceDyeCookIn,
    SourceDyeDEPARTMENTS,
    SourceDyeDeptUsedSchs,
    SourceDyeDyeProcessPrice,
    SourceDyeEmpRoom,
    SourceDyeEnableCard,
    SourceDyeEXCNOTES,
    SourceDyeFaceTemp,
    SourceDyeFeelOfferDetail,
    SourceDyeFeelOfferMain,
    SourceDyeFixedCanDetail,
    SourceDyeFixedCanRecord,
    SourceDyeGetJobSheetReceive,
    SourceDyeGWName,
    SourceDyeHContract,
    SourceDyeHEmpAppNotice,
    SourceDyeHEmpDeptPerm,
    SourceDyeHEmployee,
    SourceDyeHEmployee2,
    SourceDyeHEmployeeIORecord,
    SourceDyeHEmpRole,
    SourceDyeHLeave,
    SourceDyeHPositionChange,
    SourceDyeHRewardPunish,
    SourceDyeHOLIDAYS,
    SourceDyeHuman,
    SourceDyeITMANAGE,
    SourceDyeKindLimit,
    SourceDyeKQ,
    SourceDyeKQQuery,
    SourceDyeLeaveClass,
    SourceDyeLeaveClass1,
    SourceDyeLimit,
    SourceDyeLossBill,
    SourceDyeMaterialPriceAdjust,
    SourceDyeMaterialPriceAdjustDetail,
    SourceDyeNoLimit,
    SourceDyeNUMRUN,
    SourceDyeNUMRUNDEIL,
    SourceDyePArticle,
    SourceDyePArticleStorageUnitID,
    SourceDyePAtteSub,
    SourceDyePAtteType,
    SourceDyePAuxRule,
    SourceDyePAuxRuleDetail,
    SourceDyePBalanceType,
    SourceDyePColorNum,
    SourceDyePCommissionRatio,
    SourceDyePCommMethod,
    SourceDyePCommModule,
    SourceDyePCommPort,
    SourceDyePCook,
    SourceDyePCraftParam,
    SourceDyePCraftPParam,
    SourceDyePCustAddress,
    SourceDyePCustCategory,
    SourceDyePCustLinker,
    SourceDyePCustomer,
    SourceDyePCustRelation,
    SourceDyePDept,
    SourceDyePDyeCurve,
    SourceDyePDyeCurveDetail,
    SourceDyePDyeProgram,
    SourceDyePDyeProgramDetail,
    SourceDyePFabric,
    SourceDyePFabricCust,
    SourceDyePFabricFact,
    SourceDyePFabricOther,
    SourceDyePFeelCode,
    SourceDyePFieldMemo,
    SourceDyePFieldValid,
    SourceDyePFieldValidSub,
    SourceDyePFieldValidSubCust,
    SourceDyePGray,
    SourceDyePGrayBak,
    SourceDyePITOnRest,
    SourceDyePITWatch,
    SourceDyePLable,
    SourceDyePMachine,
    SourceDyePMachineColor,
    SourceDyePMachineFaultClass,
    SourceDyePMachineFaultStatus,
    SourceDyePMachinePart,
    SourceDyePMachinePoint,
    SourceDyePMachinePort,
    SourceDyePMachineProcess,
    SourceDyePMachineProd,
    SourceDyePMachineShift,
    SourceDyePMeter,
    SourceDyePMeterAlarm,
    SourceDyePMeterMachine,
    SourceDyePPDesign,
    SourceDyePPDesignDetail,
    SourceDyePPDesignSet,
    SourceDyePPriceList,
    SourceDyePPriceListAtte,
    SourceDyePPriceListColor,
    SourceDyePPriceListProcess,
    SourceDyePPriceListVat,
    SourceDyePProcess,
    SourceDyePProcessArea,
    SourceDyePProcessChemical,
    SourceDyePProcessCraft,
    SourceDyePProcessCraft1,
    SourceDyePProcessDefect,
    SourceDyePProcessPCraft,
    SourceDyePProcessPrice,
    SourceDyePProduct,
    SourceDyePShift,
    SourceDyePShiftArrange,
    SourceDyePShiftArrangeDetail,
    SourceDyePShiftEmp,
    SourceDyePShiftMachine,
    SourceDyePStorageUnitID,
    SourceDyePStuff,
    SourceDyePStuffStorageUnitID,
    SourceDyePVehicle,
    SourceDyePWareHouse,
    SourceDyePPasteDosage,
    SourceDyePPasteDosageDetail,
    SourceDyePrintDipsRecord,
    SourceDyePrintScreen,
    SourceDyePrintScreenDetail,
    SourceDyePrintScreenRecord,
    SourceDyeReportItem,
    SourceDyeRequestLimit,
    SourceDyeSchClass,
    SourceDyeSHIFT,
    SourceDyeSHOUPITONGZHIDAN,
    SourceDyeStaffEstablishing,
    SourceDyeSwipeEmpEdit,
    SourceDyeSwipeEmpEditDetail,
    SourceDyeTBKEY,
    SourceDyeTBSMSALLOT,
    SourceDyeTBSMSINFO,
    SourceDyeTEMPLATE,
    SourceDyeUSEROFRUN,
    SourceDyeUSERSPEDAY,
    SourceDyeUSERTEMPSCH,
    SourceDyeUSERINFO,
    SourceDyeUserUsedSClasses,
    SourceDyeYunfeibiaozhun,
)
from .source_sequences import SourceIdentitySequence
from .source_context import SourceDocumentContext, SourceBusinessParameter

from .source_models import SourceDyeFMoneyInDetail

from .source_models import SourceDyeSTimerJob, SourceDyeZAccessLog

from .source_models import SourceDyeSAlertFormat

from .source_models import SourceDyeSAlertItem

from .source_models import SourceDyeSAlertLog

from .source_models import SourceDyeSAlertParams

from .source_models import SourceDyeSAlertUser

from .source_models import SourceDyeSApp

from .source_models import SourceDyeSAppFuncs

from .source_models import SourceDyeSAppQuerys

from .source_models import SourceDyeSAppTables

from .source_models import SourceDyeSDataTableCopy

from .source_models import SourceDyeSDataTableFieldRely

from .source_models import SourceDyeSFormButton

from .source_models import SourceDyeSGridCondition

from .source_models import SourceDyeSGridParamChart

from .source_models import SourceDyeSGridUser

from .source_models import SourceDyeSLanguage

from .source_models import SourceDyeSLookupColumn

from .source_models import SourceDyeSManagerSQL

from .source_models import SourceDyeSMessage

from .source_models import SourceDyeSNotice

from .source_models import SourceDyeSPanelFieldParam

from .source_models import SourceDyeSQueryParam

from .source_models import SourceDyeSRecordRight

from .source_models import SourceDyeSRptInfoDetail

from .source_models import SourceDyeSRptInfoSub

from .source_models import SourceDyeSRptParam

from .source_models import SourceDyeSSubscribePage

from .source_models import SourceDyeSTimerJobField

from .source_models import SourceDyeSTimerJobParams

from .source_models import SourceDyeSUIModule

from .source_models import SourceDyeSUpgradeFile

from .source_models import SourceDyeAlarmLog

from .source_models import SourceDyeEmOpLog

from .source_models import SourceDyeRpPermission

from .source_models import SourceDyeSAccessLog

from .source_models import SourceDyeSAlertEmp

from .source_models import SourceDyeSAlertSender

from .source_models import SourceDyeSAppApiLog

from .source_models import SourceDyeSClientMacAddress

from .source_models import SourceDyeSDataRelation

from .source_models import SourceDyeSDataTableRelation

from .source_models import SourceDyeSException

from .source_models import SourceDyeSFieldCopy

from .source_models import SourceDyeSFormFormat

from .source_models import SourceDyeSFunDesktop

from .source_models import SourceDyeSLanguage1

from .source_models import SourceDyeSLocalAdmins

from .source_models import SourceDyeSManagerSetting

from .source_models import SourceDyeSModuleDesktop

from .source_models import SourceDyeSMonthEnd

from .source_models import SourceDyeSPersonalDataRight

from .source_models import SourceDyeSSecurityInfo

from .source_models import SourceDyeSSysAdmins

from .source_models import SourceDyeSTVScreenReport

from .source_models import SourceDyeSTVScreenReportDetail

from .source_models import SourceDyeSWeiXinAgent

from .source_models import SourceDyeSWeiXinMenu

from .source_models import SourceDyeSECURITYDETAILS

from .source_models import SourceDyeServerLog

from .source_models import SourceDyeSystemLog

from .source_models import SourceDyeUserACPrivilege

from .source_models import SourceDyeUserUpdates

from .source_models import SourceDyeSManagerSQLDash

from .numbering_models import NumberingRule
