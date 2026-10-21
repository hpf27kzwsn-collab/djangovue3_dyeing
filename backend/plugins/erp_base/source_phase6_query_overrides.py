"""三处旧平台查询的等价关系式；原SQL继续完整保存在入口目录。"""

DEPARTMENTS=['棉布分厂','棉整分厂','化纤分厂','浆染分厂','拉经车间','抓毛车间','电厂','基建','仓库','厂部','水处理','化验室','空压机','其他']
PRODUCT_GROUP=['SheetSeries','DetailNo','JobSheetNo','Jobattes2','Width','Weight','AddWeigth','TubeWeight','ProdID','FabricID','ColorID','ColorNum','Rolls','SumWeightQty','Num']


def replacement(name):
    if name=='ArticleDeptCount':
        amounts=','.join(f"SUM(CASE WHEN ad.Name=N'{name}' THEN aod.Total END) AS [{name}]" for name in DEPARTMENTS)
        total='+'.join(f'ISNULL(b.[{name}],0)' for name in DEPARTMENTS)
        return f"""SELECT fv.Code,fv.Name,c.* FROM dye.p_FieldValid fv
          LEFT JOIN (SELECT b.*,{total} AS 小计 FROM
            (SELECT ap.Code AS ProjectCode,ap.Name AS ProjectName,{amounts}
             FROM dye.ArticleOut ao JOIN dye.ArticleOutDetail aod ON ao.SheetSeries=aod.SheetSeries
             LEFT JOIN dye.p_FieldValid ap ON aod.ProjectNo=ap.Code AND ap.FieldType='ArticleProject'
             LEFT JOIN dye.p_FieldValid ad ON ao.DeptID=ad.Code AND ad.FieldType='ArticleDept'
             GROUP BY ap.Code,ap.Name) b) c ON fv.Code=c.ProjectCode
          WHERE 1=1 AND 1=2 AND fv.FieldType='ArticleProject'"""
    if name=='ProdOutRecordReport':
        group=','.join(PRODUCT_GROUP)
        amounts=','.join(f'MAX(CASE WHEN ColNo={number} THEN WeightQty END) AS [{number}]' for number in range(1,11))
        return f"""SELECT c.*,d.* FROM
          (SELECT {group},{amounts} FROM dye.v_ProdOutRecord GROUP BY {group}) c
          LEFT JOIN (SELECT SheetSeries AS FS,DetailNo AS CN,Num AS NU,SUM(WeightQty) AS SumQty,
            COUNT(DetailNo) AS SumRolls FROM dye.v_ProdOutRecord GROUP BY SheetSeries,DetailNo,Num) d
          ON c.DetailNo=d.CN AND c.SheetSeries=d.FS AND c.Num=d.NU WHERE 1=1 AND 1=2"""
    if name=='qry_Static_EmpDetail':
        # 两个临时表改为CTE，原三次UPDATE的顺序用最终投影表达；不合并重复刷卡。
        return """WITH employees AS (
          SELECT EmpID FROM dye.h_Employee WHERE ISNULL(IsOut,0)=0 AND 1=2
        ), attendance AS (
          SELECT es.EmpID,es.EmpID AS EmpCode,dtDate,ci.InTime,co.OutTime,BeginTime,EndTime,ClassID,ShiftName,
            (DATEDIFF(MINUTE,BeginTime,ci.InTime)+ABS(DATEDIFF(MINUTE,BeginTime,ci.InTime)))/2/60.0 AS LateTime,
            (DATEDIFF(MINUTE,co.OutTime,EndTime)+ABS(DATEDIFF(MINUTE,co.OutTime,EndTime)))/2/60.0 AS BeforTime,
            CASE WHEN DATEDIFF(MINUTE,ci.InTime,co.OutTime)/60.0>0 THEN 1 ELSE 0 END AS WorkCount,
            DATEDIFF(MINUTE,ci.InTime,co.OutTime)/60.0 AS WorkTime,
            CASE WHEN ISNULL(ci.InTime,0)=0 AND ISNULL(IsHoliday,0)=0 THEN 1 ELSE 0 END AS NoWork,
            ISNULL(IsHoliday,0) AS IsHoliday
          FROM dye.v_KQ_EmpShiftClock es
          LEFT JOIN dye.v_KQ_InRecord ci ON ci.EmpID=es.EmpID AND ci.CheckDate=es.dtDate
          LEFT JOIN dye.v_KQ_OutRecord co ON co.EmpID=es.EmpID AND co.CheckDate=es.dtDate
          WHERE EXISTS(SELECT 1 FROM employees e WHERE e.EmpID=es.EmpID) AND 1=2
        ) SELECT NEWID() AS ID,EmpID,EmpCode,dtDate,InTime,OutTime,BeginTime,EndTime,ClassID,ShiftName,
          LateTime,CASE WHEN LateTime>0 THEN 1 ELSE 0 END AS LateCount,
          CASE WHEN BeforTime>0 THEN 1 ELSE 0 END AS BeforCount,BeforTime,
          CASE WHEN (LateTime>0.5 OR ISNULL(WorkTime,0)=0) AND IsHoliday=0 THEN 0 ELSE WorkCount END AS WorkCount,
          WorkTime,CASE WHEN (LateTime>0.5 OR ISNULL(WorkTime,0)=0) AND IsHoliday=0 THEN 1 ELSE NoWork END AS NoWork,
          IsHoliday,0 AS LeaveTime,0 AS IsLeave,'' AS DeptID,'' AS Remarks FROM attendance ORDER BY EmpID,dtDate"""

