param([Parameter(Mandatory=$true)][string]$OutputPath)
$ErrorActionPreference = 'Stop'
$erpFoundationConnection = [System.Data.SqlClient.SqlConnection]::new('Server=localhost;Database=Textile_GXHFRS;Integrated Security=True;Encrypt=False;TrustServerCertificate=True;Application Name=ERP ReadOnly Foundation Verification;')
function Read-Foundation([string]$Sql) {
    $erpFoundationCommand = $erpFoundationConnection.CreateCommand()
    $erpFoundationCommand.CommandText = $Sql
    $erpFoundationCommand.CommandTimeout = 180
    $erpFoundationReader = $erpFoundationCommand.ExecuteReader()
    $erpFoundationRows = [Collections.Generic.List[object]]::new()
    while ($erpFoundationReader.Read()) {
        $erpFoundationRow = [ordered]@{}
        for ($erpFoundationIndex=0; $erpFoundationIndex -lt $erpFoundationReader.FieldCount; $erpFoundationIndex++) {
            $erpFoundationValue = $erpFoundationReader.GetValue($erpFoundationIndex)
            $erpFoundationRow[$erpFoundationReader.GetName($erpFoundationIndex)] = if ($erpFoundationValue -is [DBNull]) { $null } else { $erpFoundationValue }
        }
        $erpFoundationRows.Add([pscustomobject]$erpFoundationRow)
    }
    $erpFoundationReader.Close()
    $erpFoundationCommand.Dispose()
    return ,$erpFoundationRows.ToArray()
}
$erpFoundationConnection.Open()
try {
    $erpFoundationEvidence = [ordered]@{ captured_at=[DateTimeOffset]::Now.ToString('o'); statements='SELECT only' }
    $erpFoundationEvidence.lookups = Read-Foundation @'
SELECT LookupID,LookupName,DataTableName,LookupDataFilter,KeyField,DisplayField,DropSQL
FROM dye.s_Lookup WHERE LookupID IN ('B062','B084','B085','B049') ORDER BY LookupID
'@
    $erpFoundationEvidence.lookup_queries = Read-Foundation @'
SELECT DataTableName,Alias,SQL FROM dye.s_DataTable
WHERE DataTableName IN (SELECT DataTableName FROM dye.s_Lookup WHERE LookupID IN ('B062','B084','B085','B049'))
ORDER BY DataTableName
'@
    $erpFoundationEvidence.units = Read-Foundation @'
SELECT s.u AS source_unit,d.u AS destination_unit,q.quantity,dye.convertUnit(s.u,d.u,q.quantity) AS result
FROM (VALUES (0),(1),(2),(3),(4),(5),(255),(NULL))s(u)
CROSS JOIN (VALUES (0),(1),(2),(3),(4),(5),(255),(NULL))d(u)
CROSS JOIN (VALUES (CAST('-10.125' AS decimal(10,2))),(CAST('0' AS decimal(10,2))),
 (CAST('1.005' AS decimal(10,2))),(CAST('99.99' AS decimal(10,2))),(CAST(NULL AS decimal(10,2))))q(quantity)
'@
    $erpFoundationEvidence.business_units = Read-Foundation @'
SELECT EmpID,dye.fn_ConcatBusinessUnitID(EmpID) AS unit_ids,dye.fn_ConcatBusinessUnitName(EmpID) AS unit_names
FROM dye.h_Employee ORDER BY EmpID
'@
    $erpFoundationEvidence.days = Read-Foundation @'
SELECT 'dbo' AS source_schema,days FROM dbo.fn_GetDays('2024-02-28','2024-03-01')
UNION ALL SELECT 'dye',days FROM dye.fn_GetDays('2024-02-28','2024-03-01')
'@
    $erpFoundationEvidence.day_numbers = Read-Foundation "SELECT MIN(number) AS first_number,MAX(number) AS last_number,COUNT(*) AS count FROM master..spt_values WHERE type='P'"
    $erpFoundationEvidence | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $OutputPath -Encoding utf8NoBOM
    Write-Output ('Read-only foundation evidence saved; unit probes='+$erpFoundationEvidence.units.Count+'; employee scopes='+$erpFoundationEvidence.business_units.Count)
}
finally { $erpFoundationConnection.Dispose() }
