param([Parameter(Mandatory=$true)][string]$OutputPath)
$ErrorActionPreference='Stop'
$connection=[System.Data.SqlClient.SqlConnection]::new('Server=localhost;Database=Textile_GXHFRS;Integrated Security=True;Encrypt=False;TrustServerCertificate=True;Application Name=ERP Remaining Save Sources SELECT Only;Connect Timeout=5;')
function Read-Rows([string]$sql){
    $command=$connection.CreateCommand();$command.CommandText=$sql;$command.CommandTimeout=30
    try{
        $reader=$command.ExecuteReader();$rows=[Collections.Generic.List[object]]::new()
        while($reader.Read()){
            $row=[ordered]@{}
            for($i=0;$i -lt $reader.FieldCount;$i++){$row[$reader.GetName($i)]=if($reader.IsDBNull($i)){$null}else{$reader.GetValue($i)}}
            $rows.Add([pscustomobject]$row)
        }
        $reader.Close();return ,$rows.ToArray()
    }finally{$command.Dispose()}
}
$connection.Open()
try{
    $result=[ordered]@{captured_at=[DateTimeOffset]::Now.ToString('o');mode='SELECT only; no source business writes or procedures executed'}
    $result.tables=Read-Rows "SELECT SCHEMA_NAME(t.schema_id) AS schema_name,t.name,c.name AS column_name,TYPE_NAME(c.user_type_id) AS type_name,c.max_length,c.precision,c.scale FROM sys.tables t JOIN sys.columns c ON c.object_id=t.object_id WHERE t.name IN ('StuffWeight','FixedPrice','RecordYieldCheck','WareHouseProdCount','ProdInRecord') ORDER BY t.name,c.column_id"
    $result.entries=Read-Rows "SELECT * FROM dye.s_DataTable WHERE DataTableName IN ('AddStuffWeight','Quote','QueryRecordCheck','QueryWorkList2','WareHouseProdCount')"
    $result.fields=Read-Rows "SELECT * FROM dye.s_DataTableField WHERE (DataTableName='AddStuffWeight' AND FieldName='Moisture1') OR (DataTableName='Quote' AND FieldName='IsConfirmed') OR (DataTableName='QueryRecordCheck' AND FieldName IN ('GradeID','avgdots','Dots','Length')) OR (DataTableName='WareHouseProdCount' AND FieldName IN ('Rolls','WeightQty'))"
    $result.references=Read-Rows "SELECT SCHEMA_NAME(o.schema_id) AS schema_name,o.name,o.type_desc,m.definition FROM sys.sql_modules m JOIN sys.objects o ON o.object_id=m.object_id WHERE m.definition LIKE '%WareHouseProdCount%' OR m.definition LIKE '%RecordYieldCheck%' ORDER BY o.name"
    $result | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $OutputPath -Encoding utf8NoBOM
    [ordered]@{tables=$result.tables.Count;entries=$result.entries.Count;fields=$result.fields.Count;references=$result.references.Count;output=$OutputPath}|ConvertTo-Json
}finally{$connection.Dispose()}
