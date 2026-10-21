param([Parameter(Mandatory=$true)][string]$OutputPath)
$ErrorActionPreference='Stop'
$connection=[System.Data.SqlClient.SqlConnection]::new('Server=localhost;Database=Textile_GXHFRS;Integrated Security=True;Encrypt=False;TrustServerCertificate=True;Application Name=ERP Field Links SELECT Only;')
$queries=[ordered]@{
    field_copy='SELECT DataTableName,FieldName,DestDataTableName,DestFieldName FROM dye.s_FieldCopy ORDER BY DataTableName,FieldName,DestDataTableName,DestFieldName'
    lookups='SELECT * FROM dye.s_Lookup ORDER BY LookupID'
    lookup_columns='SELECT * FROM dye.s_LookupColumn ORDER BY LookUpID,DisplayIndex,FieldName'
    data_relations='SELECT * FROM dye.s_DataRelation ORDER BY DataTableName,FieldName,DestDataTableName,LinkFieldName'
    table_relations='SELECT * FROM dye.s_DataTableRelation ORDER BY DataTableName,FieldName,DestDataTableName,LinkFieldName'
}
$result=[ordered]@{captured_at=[DateTimeOffset]::Now.ToString('o');mode='SELECT only; configuration rows including duplicates'}
$connection.Open()
try {
    foreach($key in $queries.Keys){
        $command=$connection.CreateCommand();$command.CommandText=$queries[$key];$command.CommandTimeout=60
        $reader=$command.ExecuteReader();$rows=[Collections.Generic.List[object]]::new()
        while($reader.Read()){
            $row=[ordered]@{}
            for($i=0;$i -lt $reader.FieldCount;$i++){$row[$reader.GetName($i)]=if($reader.IsDBNull($i)){$null}else{$reader.GetValue($i)}}
            $rows.Add([pscustomobject]$row)
        }
        $reader.Close();$command.Dispose();$result[$key]=$rows.ToArray()
    }
    $result|ConvertTo-Json -Depth 8|Set-Content -LiteralPath $OutputPath -Encoding utf8NoBOM
    foreach($key in $queries.Keys){Write-Output "$key : $($result[$key].Count)"}
} finally {$connection.Dispose()}
