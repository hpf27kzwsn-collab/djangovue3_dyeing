"""DyeDipsRecord_Add原49列插入；页面沿用完整原表录入。"""
from .source_quality_reports import rows
from .source_services import write
from .source_calculations import store_value

ADD_FIELDS='''SheetSeries SheetNo SheetKind SheetDate SheetStatus BusinessUnitID
CustomerID SalerGroupID SalerID ColorNo ColorVersion ConfirmVersion DeptID
CheckNo MainStuffKindID ProdID Spec LotNo Structure ColorID
ColorDepthID ColorNum CustColorNum ColorE ColorRGB RecipePriceSource FabricSource
Weight CostEffirate Cost CostUnit VerLight1ID VerLight2ID ConfirmSideID
EmpID ShiftID CheckerID DlvSampleDate RightStatus StepNo PrintTimes
Revisions Remarks Creater CreateDate Modifyer ModifyDate ApproveDate Approver'''.split()


def add(parameters,actor):
    model=rows('DyeDipsRecord','erp_sampling').model
    return write(model,dict(store_value(model(),field,parameters[field]) for field in ADD_FIELDS),actor=actor)
