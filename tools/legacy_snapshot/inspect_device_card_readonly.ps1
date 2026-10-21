param([string]$OutputFile = '.runtime-temp/device-card-investigation/live.json')
$ErrorActionPreference = 'Stop'
$connection = [System.Data.SqlClient.SqlConnection]::new('Server=localhost;Database=Textile_GXHFRS;Integrated Security=True;Encrypt=False;TrustServerCertificate=True;Application Name=ERP Device Card Readonly Investigation;Connect Timeout=10;')
function Read-Rows([string]$Sql) {
    $command = $connection.CreateCommand()
    $command.CommandText = $Sql
    $command.CommandTimeout = 180
    $rows = [Collections.Generic.List[object]]::new()
    $reader = $command.ExecuteReader()
    while ($reader.Read()) {
        $row = [ordered]@{}
        for ($i = 0; $i -lt $reader.FieldCount; $i++) {
            $value = $reader.GetValue($i)
            $row[$reader.GetName($i)] = if ($value -is [DBNull]) { $null } else { $value }
        }
        $rows.Add([pscustomobject]$row)
    }
    $reader.Close()
    $command.Dispose()
    return ,$rows.ToArray()
}
$connection.Open()
try {
    $result = [ordered]@{ captured_at = [DateTimeOffset]::Now.ToString('o'); statements = 'SELECT only' }
    $result.comm_ports = Read-Rows 'SELECT * FROM dye.p_CommPort ORDER BY PortID'
    $result.machines = Read-Rows 'SELECT MachineID,Name,StationID,WorkShopID,IPAddress,Ports,OPCs,IsStop,MachineNo,MachineType FROM dye.p_Machine ORDER BY MachineID'
    $result.meters = Read-Rows 'SELECT MeterID,Name,IPAddress,PortID,GatherWay,CommunicatWay,CommStr,FuncCode,IsStop FROM dye.p_Meter ORDER BY MeterID'
    $result.params = Read-Rows @'
SELECT ParamName,ParamType,
 CASE WHEN ParamName LIKE '%pass%' OR ParamName LIKE '%pwd%' OR ParamName LIKE '%secret%' THEN '[redacted]' ELSE ParamValue END AS ParamValue,
 Description,ModuleNo FROM dye.s_SysParams
WHERE ParamName LIKE '%Comm%' OR ParamName LIKE '%Card%' OR ParamName LIKE '%Device%' OR ParamName LIKE '%Swipe%'
 OR ParamName LIKE '%IP%' OR ParamName LIKE '%Port%' OR ParamName LIKE '%RFID%' OR ParamName LIKE '%DP%'
 OR Description LIKE N'%刷卡%' OR Description LIKE N'%打卡%' OR Description LIKE N'%采集%' OR Description LIKE N'%通讯%'
ORDER BY ParamName
'@
    $result.modules = Read-Rows 'SELECT ModuleNo,ModuleName,ModuleCaption,IsEnable FROM dye.s_Module ORDER BY ModuleNo'
    $result.forms = Read-Rows @'
SELECT FormName,FuncNo,FormKind,Description,MasterDataTableName,DATALENGTH(Stream) AS stream_bytes,
 CONVERT(varchar(128),CONVERT(varbinary(64),Stream),2) AS stream_prefix_hex
FROM dye.s_FormParam
WHERE FormName LIKE '%DP%' OR FormName LIKE '%Swipe%' OR FormName LIKE '%Comm%' OR FormName LIKE '%RFID%'
 OR Description LIKE N'%刷卡%' OR Description LIKE N'%打卡%' OR Description LIKE N'%通讯%'
'@
    $result.timer_jobs = Read-Rows 'SELECT ItemID,ItemName,CommandType,ItemSQL,ExecKind,IsStop,Description FROM dye.s_TimerJob'
    $result.functions = Read-Rows @'
SELECT FuncNo,FuncName,FullName,IsEnable,ModuleNo,DllPath,NameSpace,FormName,FormCaption,FormParam,FuncParams,Description,ParamDescription
FROM dye.s_Functions
WHERE ModuleNo=60 OR FormName LIKE '%DProcess%' OR FormName LIKE '%DyeSwipe%'
 OR FuncName LIKE N'%通讯%' OR FuncName LIKE N'%刷卡%' OR FuncName LIKE N'%采集%' OR FuncName LIKE N'%打卡%'
'@
    $result.form_xml = Read-Rows @'
SELECT FormName,FuncNo,
 CAST('' AS xml).value('xs:base64Binary(sql:column("Stream"))','varchar(max)') AS stream_base64
FROM (SELECT FormName,FuncNo,CONVERT(varbinary(max),Stream) AS Stream FROM dye.s_FormParam
WHERE FormName IN ('F_DProcess','F_DProcess1','F_DyeSwipe','F_DyeSwipe1')) f
'@
    $result.ip_station = Read-Rows @'
SELECT w.IPAddress,w.StationID,f.Name AS station_name,COUNT_BIG(*) AS rows
FROM dye.WProcess w LEFT JOIN dye.p_FieldValid f ON f.FieldType='Station' AND f.Code=w.StationID
GROUP BY w.IPAddress,w.StationID,f.Name ORDER BY COUNT_BIG(*) DESC
'@
    $result.production_ips = Read-Rows @'
SELECT IPAddress,COUNT_BIG(*) AS rows,MIN(StartTime) AS first_start,MAX(StartTime) AS last_start,
 MIN(CreateDate) AS first_create,MAX(CreateDate) AS last_create,
 COUNT(DISTINCT MachineID) AS distinct_machines,COUNT(DISTINCT StationID) AS distinct_stations
FROM dye.WProcess GROUP BY IPAddress ORDER BY COUNT_BIG(*) DESC
'@
    $result.production_modules = Read-Rows 'SELECT ModuleNo,COUNT_BIG(*) AS rows FROM dye.WProcess GROUP BY ModuleNo ORDER BY COUNT_BIG(*) DESC'
    $result.employee_card_counts = Read-Rows @'
SELECT COUNT_BIG(*) AS employees,
 SUM(CASE WHEN NULLIF(LTRIM(RTRIM(RFID)),'') IS NOT NULL THEN 1 ELSE 0 END) AS with_rfid
FROM dye.h_Employee
'@
    $result.live_employee_triggers = Read-Rows @'
SELECT t.name,t.is_disabled,m.definition FROM sys.triggers t JOIN sys.sql_modules m ON m.object_id=t.object_id
WHERE t.parent_id=OBJECT_ID('dye.h_Employee')
'@
    $result.production_stations = Read-Rows @'
SELECT w.StationID,f.Name AS station_name,COUNT_BIG(*) AS rows,
 SUM(CASE WHEN NULLIF(LTRIM(RTRIM(w.IPAddress)),'') IS NOT NULL THEN 1 ELSE 0 END) AS with_ip,
 MIN(w.StartTime) AS first_start,MAX(w.StartTime) AS last_start
FROM dye.WProcess w LEFT JOIN dye.p_FieldValid f ON f.FieldType='Station' AND f.Code=w.StationID
GROUP BY w.StationID,f.Name ORDER BY w.StationID
'@
    $result.counts = Read-Rows @'
SELECT 'WProcess' AS table_name,COUNT_BIG(*) AS rows FROM dye.WProcess
UNION ALL SELECT 'JobShiftEmp',COUNT_BIG(*) FROM dye.JobShiftEmp
UNION ALL SELECT 'RecordYield',COUNT_BIG(*) FROM dye.RecordYield
UNION ALL SELECT 'RecordEmp',COUNT_BIG(*) FROM dye.RecordEmp
UNION ALL SELECT 'CHECKINOUT',COUNT_BIG(*) FROM dye.CHECKINOUT
UNION ALL SELECT 'Machines',COUNT_BIG(*) FROM dye.Machines
UNION ALL SELECT 'p_MachinePoint',COUNT_BIG(*) FROM dye.p_MachinePoint
UNION ALL SELECT 'p_MachinePort',COUNT_BIG(*) FROM dye.p_MachinePort
UNION ALL SELECT 'p_CommMethod',COUNT_BIG(*) FROM dye.p_CommMethod
UNION ALL SELECT 'WProcessStep',COUNT_BIG(*) FROM dye.WProcessStep
UNION ALL SELECT 's_AccessLog',COUNT_BIG(*) FROM dye.s_AccessLog
'@
    $result.samples = Read-Rows @'
SELECT TOP (12) WProcessNo,JobSheetNo,ProcessNo,ProcessID,StationID,MachineID,ShiftID,
 IPAddress,ModuleNo,StartTime,EndTime,CreateDate,CurrKg,CurrRolls,Kind,DyeState
FROM dye.WProcess WHERE NULLIF(LTRIM(RTRIM(IPAddress)),'') IS NOT NULL ORDER BY CreateDate DESC
'@
    $result.live_modules = Read-Rows @'
SELECT s.name AS schema_name,o.name AS object_name,o.type_desc,m.definition
FROM sys.objects o JOIN sys.schemas s ON s.schema_id=o.schema_id
JOIN sys.sql_modules m ON m.object_id=o.object_id
WHERE o.name IN ('WProcess_Insert','WProcess_InsertNew','WProcess_DELETE','sp_AuTo_RecordYield','JobGrayRecordInsert')
'@
    $result | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $OutputFile -Encoding utf8
    Write-Output ('Saved readonly evidence: ' + $OutputFile)
} finally { $connection.Close(); $connection.Dispose() }
