param([Parameter(Mandatory=$true)][string]$EvidenceDirectory)
$ErrorActionPreference='Stop'
$connection=[System.Data.SqlClient.SqlConnection]::new('Server=localhost;Database=Textile_GXHFRS;Integrated Security=True;Encrypt=False;TrustServerCertificate=True;Application Name=ERP ReadOnly Unit Formula Review;')
function Read-Rows([string]$sql) {
    $command=$connection.CreateCommand();$command.CommandText=$sql;$command.CommandTimeout=120
    try {
        $reader=$command.ExecuteReader();$rows=[Collections.Generic.List[object]]::new()
        while ($reader.Read()) {
            $row=[ordered]@{}
            for ($i=0;$i -lt $reader.FieldCount;$i++) {$row[$reader.GetName($i)]=if($reader.IsDBNull($i)){$null}else{$reader.GetValue($i)}}
            $rows.Add([pscustomobject]$row)
        }
        $reader.Close();return ,$rows.ToArray()
    } finally {$command.Dispose()}
}
$connection.Open()
try {
    $result=[ordered]@{captured_at=[DateTimeOffset]::Now.ToString('o');mode='SELECT only; aggregate source profiling, not new/old record reconciliation'}
    $result.unit_groups=Read-Rows @'
SELECT GUnit,PUnit,COUNT_BIG(*) AS row_count,
 SUM(CONVERT(bigint,CASE WHEN GrayQty IS NULL THEN 1 ELSE 0 END)) AS gray_null,
 SUM(CONVERT(bigint,CASE WHEN WeightQty IS NULL THEN 1 ELSE 0 END)) AS weight_null,
 SUM(CONVERT(bigint,CASE WHEN GrayQty<0 OR WeightQty<0 THEN 1 ELSE 0 END)) AS negative_rows
FROM dye.ProdOutRecord GROUP BY GUnit,PUnit ORDER BY GUnit,PUnit
'@
    $result.defect_totals=Read-Rows @'
SELECT COUNT_BIG(*) AS row_count,
 SUM(CONVERT(bigint,CASE WHEN Dots IS NULL OR Times IS NULL THEN 1 ELSE 0 END)) AS input_null_rows,
 SUM(CONVERT(bigint,CASE WHEN Dots<0 OR Times<0 THEN 1 ELSE 0 END)) AS negative_input_rows,
 SUM(CONVERT(bigint,CASE WHEN SumDots IS NULL THEN 1 ELSE 0 END)) AS stored_null_rows,
 SUM(CONVERT(bigint,CASE WHEN SumDots<>CASE WHEN ISNULL(CONVERT(decimal(20,2),Dots)*Times,0)>0 THEN CONVERT(decimal(20,2),Dots)*Times ELSE 0 END
   OR SumDots IS NULL THEN 1 ELSE 0 END)) AS stored_formula_different_rows
FROM dye.RecordDefect
'@
    $result.duplicate_keys=Read-Rows @'
SELECT 'ProdOutRecord(SheetSeries,RollNo,BarCode)' AS key_name,COUNT_BIG(*) AS duplicate_groups,SUM(n) AS rows_in_groups
FROM (SELECT COUNT_BIG(*) AS n FROM dye.ProdOutRecord GROUP BY SheetSeries,RollNo,BarCode HAVING COUNT_BIG(*)>1) a
UNION ALL
SELECT 'RecordDefect(BarCode,DefectNo)',COUNT_BIG(*),SUM(n)
FROM (SELECT COUNT_BIG(*) AS n FROM dye.RecordDefect GROUP BY BarCode,DefectNo HAVING COUNT_BIG(*)>1) b
'@
    $result | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $EvidenceDirectory 'source-units-profile.json') -Encoding utf8NoBOM
    $result | ConvertTo-Json -Depth 8
} finally {$connection.Dispose()}
