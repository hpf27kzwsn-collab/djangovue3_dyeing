"""缺失中间表时展示现存原行的明确关联，不制造配件数量或导入暂存记录。"""
from sqlglot import parse_one, exp

NOTES = {
    'vw_DyeMachine': '原视图的本地p_Machine及MachineType=50筛选保留，MachineNo/MachineID/Name/MaxWaitVats逐行取原值。外部CCS Machines来源缺失，LX_MachineId未知为NULL；不把MachineNo冒充已确认中控编号。重复本地机台保留，外部重复匹配造成的行数仍无法复原。',
    'MachineCarePlanArticle': '原配件耗用明细表缺失；明确展示现存MachineCarePlanDetail的配件引用及全部同代码资料。DetailNo为计划明细号，Qty/RowNo未知为NULL，Unit为当前资料单位；不是已恢复历史耗用明细。无配件代码、重复代码和孤立引用均保留。',
    'GrayInRecord_Test': '缺原导入暂存表；明确用现存GrayInRecord左连全部同ReceSheetNo的GrayInDetail及同流水GrayIn供复核。17个配置列分别来自细码/明细/头；StorageUnitIDs取细码StorageUnitID。此入口只读展示已存在细码，不冒充外部待导入记录或恢复原导入功能。',
    'qry_MachineArticle': '报修配件与保养计划引用按UNION ALL展示，并标明SourceKind。保养数量/行号未知为NULL，DetailNo为计划明细号；日期/人员取计划明细，SheetType未知。所有重复资料/表头与孤立引用保留，不能把保养引用数量NULL当作0耗用。',
}

CARE = '''SELECT d.ArticleID,d.DetailNo,d.HandleDate,d.HandlerIDs,d.MachineID,
    NULL AS Qty,NULL AS RowNo,d.SheetSeries,NULL AS SheetType,p.Unit AS unit,p.LastPrice,
    NULL AS Rounds,NULL AS Kind,p.Name AS ArticleName,p.Spec,h.SheetNo,h.StartTime,h.EndTime,
    'care_plan_reference' AS SourceKind
    FROM dye.MachineCarePlanDetail d
    LEFT JOIN dye.MachineCarePlan h ON d.SheetSeries=h.SheetSeries
    LEFT JOIN dye.p_Article p ON d.ArticleID=p.ArticleID WHERE 1=1 AND 1=2'''


def adapt(name, tree):
    if name == 'vw_DyeMachine':
        return parse_one('''SELECT NULL AS LX_MachineId,a.MachineNo,a.MachineID,a.Name,a.MaxWaitVats
            FROM dye.p_Machine a WHERE a.MachineType=50 AND 1=1''',read='tsql')
    if name == 'MachineCarePlanArticle':
        return parse_one('''SELECT d.ArticleID,d.DetailNo,NULL AS Qty,NULL AS RowNo,d.SheetSeries,p.Unit,
            d.MachineID,d.HandleDate,d.HandlerIDs,d.PartID,d.Remarks,p.Name AS ArticleName,p.Spec,
            'care_plan_reference' AS SourceKind FROM dye.MachineCarePlanDetail d
            LEFT JOIN dye.p_Article p ON d.ArticleID=p.ArticleID WHERE 1=1 AND 1=2''',read='tsql')
    if name == 'qry_MachineArticle':
        from .source_phase6_local_queries import QUERIES
        repair=parse_one(QUERIES[name],read='tsql')
        repair.append('expressions',exp.alias_(exp.Literal.string('fault_article_detail'),'SourceKind'))
        return exp.Union(this=repair,expression=parse_one(CARE,read='tsql'),distinct=False)
    if name == 'GrayInRecord_Test':
        return parse_one('''SELECT d.Area,r.BarCode,d.CustJobNo,h.CustomerID,d.GrayID,r.GUnit,
            r.LengthQty,d.MachineID,d.PreField1,d.PreField3,d.PreField5,r.RollNo,r.Rolls,
            h.SheetDate,d.SheetSeries,r.StorageUnitID AS StorageUnitIDs,r.WeightQty,
            r.ReceSheetNo,r.OriReceSheetNo,r.OriBarCode,r.InputDetailCode,
            'existing_gray_record_review' AS SourceKind FROM dye.GrayInRecord r
            LEFT JOIN dye.GrayInDetail d ON r.ReceSheetNo=d.ReceSheetNo
            LEFT JOIN dye.GrayIn h ON d.SheetSeries=h.SheetSeries WHERE 1=1 AND 1=2''',read='tsql')
    return tree


def differences(name):
    if name not in NOTES:return None
    return {'mode':'explicit_existing_reference','missing_columns':[], 'join_note':NOTES[name],
            'historical_reconciliation':'缺原中间表、取数时机和完整来源，未完成同口径历史对账。','field_acceptance':'未现场验收'}
