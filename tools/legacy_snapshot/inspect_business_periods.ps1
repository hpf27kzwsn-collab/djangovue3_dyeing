param([Parameter(Mandatory=$true)][string]$OutputPath)
$ErrorActionPreference='Stop'
$connection=[Data.SqlClient.SqlConnection]::new('Server=localhost;Database=Textile_GXHFRS;Integrated Security=True;Encrypt=False;TrustServerCertificate=True;Application Name=ERP ReadOnly Business Periods;')
$connection.Open()
function Read-Rows([string]$sql) {
    $command=$connection.CreateCommand();$command.CommandText=$sql
    try {
        $reader=$command.ExecuteReader();$rows=[Collections.Generic.List[object]]::new()
        while($reader.Read()) {
            $row=[ordered]@{}
            for($i=0;$i -lt $reader.FieldCount;$i++) {$row[$reader.GetName($i)]=$(if($reader.IsDBNull($i)){$null}else{$reader.GetValue($i)})}
            $rows.Add($row)
        }
        $reader.Close();return ,$rows.ToArray()
    } finally {$command.Dispose()}
}
try {
    $months=Read-Rows 'SELECT AccMonth,StartTime,EndTime FROM dye.s_AccMonth'
    $parameters=Read-Rows "SELECT ParamName,Description FROM dye.s_SysParams WHERE ParamName LIKE 'Beg%' OR ParamName LIKE 'End%'"
    $probes=@()
    foreach($date in @('2024-01-01','2024-01-26','2024-02-01','2024-02-27','2024-02-28','2024-02-29','2024-03-01','2024-12-25','2024-12-26','2024-12-31','2025-01-01','2026-10-16')) {
        $rows=Read-Rows ("SELECT dye.GetAccBeginDate('"+$date+"') AS BeginDate,dye.GetAccEndDate('"+$date+"') AS EndDate,dye.ufn_GetAccFirstDate('"+$date+"') AS FirstDate")
        $probes+=@{input=$date;result=$rows[0]}
    }
    @{months=$months;parameters=$parameters;probes=$probes} | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $OutputPath -Encoding UTF8
} finally {$connection.Close();$connection.Dispose()}
