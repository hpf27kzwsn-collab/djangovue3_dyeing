param([Parameter(Mandatory=$true)][string]$OutputFile)
$ErrorActionPreference='Stop'
[Threading.Thread]::CurrentThread.CurrentCulture=[Globalization.CultureInfo]::InvariantCulture
$connection=[System.Data.SqlClient.SqlConnection]::new('Server=localhost;Database=Textile_GXHFRS;Integrated Security=True;Encrypt=False;TrustServerCertificate=True;Application Name=ERP Quality Quantity ReadOnly Export;')
function Read-QualityRows([string]$sql) {
    $command=$connection.CreateCommand();$command.Transaction=$transaction;$command.CommandText=$sql;$command.CommandTimeout=180
    $reader=$command.ExecuteReader();$result=[System.Collections.Generic.List[object]]::new()
    try {
        while($reader.Read()) {
            $row=[ordered]@{}
            for($i=0;$i -lt $reader.FieldCount;$i++) {
                $value=$reader.GetValue($i)
                if($value -is [DBNull]) {$value=$null}
                elseif($value -is [decimal]) {$value=$value.ToString([Globalization.CultureInfo]::InvariantCulture)}
                elseif($value -is [datetime]) {$value=$value.ToString('yyyy-MM-ddTHH:mm:ss.fff')}
                $row[$reader.GetName($i)]=$value
            }
            $result.Add([pscustomobject]$row)
        }
    } finally {$reader.Close();$command.Dispose()}
    return ,$result.ToArray()
}
$connection.Open()
try {
    # 固定SELECT；可串行化读事务使表头、明细与字段证据属于同一抽取时点。
    $transaction=$connection.BeginTransaction([System.Data.IsolationLevel]::Serializable)
    $columns=Read-QualityRows "SELECT t.name AS table_name,c.name AS field_name,ty.name AS data_type,c.precision,c.scale,c.is_nullable FROM sys.tables t JOIN sys.columns c ON c.object_id=t.object_id JOIN sys.types ty ON ty.user_type_id=c.user_type_id WHERE SCHEMA_NAME(t.schema_id)='dye' AND t.name IN ('FARMain','FARDetail') ORDER BY t.name,c.column_id"
    $hasLength=@($columns | Where-Object {$_.table_name -eq 'FARDetail' -and $_.field_name -eq 'PreMeter'}).Count -gt 0
    $length=if($hasLength){'d.PreMeter'}else{'CAST(NULL AS decimal(24,6))'}
    $headers=Read-QualityRows 'SELECT SheetSeries AS header_key,SheetDate AS sheet_date,SheetKind AS sheet_kind,BusinessUnitID AS business_unit FROM dye.FARMain ORDER BY SheetSeries'
    $sql=@"
SELECT d.DetailNo AS detail_key,d.SheetSeries AS detail_sheet_series,
h.SheetSeries AS header_key,h.SheetDate AS sheet_date,h.SheetKind AS sheet_kind,h.BusinessUnitID AS business_unit,
d.JobSheetNo AS job_number,d.OutDetailNo AS out_detail_no,d.Qty AS quantity,d.StockUnit AS stock_unit,
CASE WHEN d.ARMoney IS NULL THEN CAST(NULL AS bit) WHEN d.ARMoney=0 THEN CAST(1 AS bit) ELSE CAST(0 AS bit) END AS zero_amount,
$length AS metres
FROM dye.FARDetail d LEFT JOIN dye.FARMain h ON h.SheetSeries=d.SheetSeries
ORDER BY d.DetailNo,h.SheetSeries
"@
    $rows=Read-QualityRows $sql
    $data=[ordered]@{format='erp-quality-quantity-v1';database='Textile_GXHFRS';captured_at=[DateTimeOffset]::Now.ToString('o');
        isolation='SERIALIZABLE read transaction';query=$sql;columns=$columns;length_available=$hasLength;
        headers=$headers;row_count=$rows.Count;rows=$rows}
    $transaction.Commit()
    $data | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $OutputFile -Encoding utf8NoBOM
    Write-Output "Quality quantities: $($rows.Count) rows, $($headers.Count) headers; PreMeter available: $hasLength"
} finally {$connection.Dispose()}
