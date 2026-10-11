param([Parameter(Mandatory=$true)][string]$OutputDirectory)
$ErrorActionPreference='Stop'
$erpSnapshotDirectory=[IO.Path]::GetFullPath($OutputDirectory)
New-Item -ItemType Directory -Path $erpSnapshotDirectory -ErrorAction Stop | Out-Null
$erpTableDefinitions=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'source_tables.json') -Raw -Encoding utf8 | ConvertFrom-Json
$erpReadConnection=[System.Data.SqlClient.SqlConnection]::new('Server=localhost;Database=Textile_GXHFRS;Integrated Security=True;Encrypt=False;TrustServerCertificate=True;Application Name=ERP ReadOnly Business Snapshot;')
function Read-SchemaQuery([string]$Sql) {
    $erpSchemaCommand=$erpReadConnection.CreateCommand();$erpSchemaCommand.CommandText=$Sql
    $erpSchemaReader=$erpSchemaCommand.ExecuteReader();$erpSchemaRows=[Collections.Generic.List[object]]::new()
    while($erpSchemaReader.Read()) {
        $erpSchemaRow=[ordered]@{}
        for($erpColumn=0;$erpColumn -lt $erpSchemaReader.FieldCount;$erpColumn++) {
            $erpValue=$erpSchemaReader.GetValue($erpColumn)
            $erpSchemaRow[$erpSchemaReader.GetName($erpColumn)]=if($erpValue -is [DBNull]) {$null} else {$erpValue}
        }
        $erpSchemaRows.Add([pscustomobject]$erpSchemaRow)
    }
    $erpSchemaReader.Close();$erpSchemaCommand.Dispose()
    return ,$erpSchemaRows.ToArray()
}
Add-Type -Path (Join-Path $PSScriptRoot 'ReadOnlySnapshot.cs') -ReferencedAssemblies (Get-ChildItem -LiteralPath (Join-Path $PSHOME 'ref') -Filter '*.dll' | ForEach-Object FullName)
$erpReadConnection.Open()
try {
    $erpCurrentFields=Read-SchemaQuery @'
SELECT s.name AS schema_name,t.name AS table_name,c.column_id,c.name AS field_name,ty.name AS data_type,
 c.max_length,c.precision,c.scale,c.is_nullable,c.is_identity,c.is_computed,
 CAST(ep.value AS nvarchar(max)) AS description,dc.definition AS default_definition,cc.definition AS computed_definition
FROM sys.tables t JOIN sys.schemas s ON s.schema_id=t.schema_id
JOIN sys.columns c ON c.object_id=t.object_id JOIN sys.types ty ON ty.user_type_id=c.user_type_id
LEFT JOIN sys.extended_properties ep ON ep.major_id=t.object_id AND ep.minor_id=c.column_id AND ep.name=N'MS_Description'
LEFT JOIN sys.default_constraints dc ON dc.object_id=c.default_object_id
LEFT JOIN sys.computed_columns cc ON cc.object_id=c.object_id AND cc.column_id=c.column_id
WHERE s.name=N'dye' ORDER BY t.name,c.column_id
'@
    $erpPrimaryKeys=Read-SchemaQuery @'
SELECT s.name AS schema_name,t.name AS table_name,c.name AS field_name,ic.key_ordinal
FROM sys.tables t JOIN sys.schemas s ON s.schema_id=t.schema_id
JOIN sys.indexes i ON i.object_id=t.object_id AND i.is_primary_key=1
JOIN sys.index_columns ic ON ic.object_id=i.object_id AND ic.index_id=i.index_id
JOIN sys.columns c ON c.object_id=ic.object_id AND c.column_id=ic.column_id
WHERE s.name=N'dye' AND ic.key_ordinal>0 ORDER BY t.name,ic.key_ordinal
'@
    $erpStartedAt=(Get-Date).ToUniversalTime().ToString('o')
    $erpManifest=[ordered]@{database='Textile_GXHFRS';started_at=$erpStartedAt;isolation='READ COMMITTED';
        source_scope='six ERP modules; finance tables excluded';numeric_encoding='SQL numeric values stored as invariant strings; type, precision and scale in columns';
        no_primary_key_identity='key is null; row is extraction ordinal, not a fabricated old-system id';tables=@()}
    foreach($erpDefinition in $erpTableDefinitions) {
        $erpFields=@($erpCurrentFields | Where-Object table_name -EQ $erpDefinition.table)
        $erpKeys=[string[]]@($erpPrimaryKeys | Where-Object table_name -EQ $erpDefinition.table | ForEach-Object field_name)
        $erpColumns=[string[]]@($erpFields | ForEach-Object field_name)
        if($erpColumns.Count -eq 0) {throw "Source table dye.$($erpDefinition.table) has no current columns."}
        $erpFileName='dye.'+$erpDefinition.table+'.jsonl'
        $erpFilePath=Join-Path $erpSnapshotDirectory $erpFileName
        $erpTableStart=(Get-Date).ToUniversalTime().ToString('o')
        $erpRowCount=[ErpReadOnlySnapshot]::Export($erpReadConnection,'dye',$erpDefinition.table,$erpColumns,$erpKeys,$erpFilePath)
        $erpManifest.tables+= [ordered]@{schema='dye';table=$erpDefinition.table;modules=@($erpDefinition.modules);columns=$erpFields;primary_key=$erpKeys;
            rows=$erpRowCount;file=$erpFileName;sha256=(Get-FileHash -LiteralPath $erpFilePath -Algorithm SHA256).Hash.ToLowerInvariant();
            bytes=(Get-Item -LiteralPath $erpFilePath).Length;started_at=$erpTableStart;finished_at=(Get-Date).ToUniversalTime().ToString('o')}
        $erpManifest | ConvertTo-Json -Depth 14 | Set-Content -LiteralPath (Join-Path $erpSnapshotDirectory 'manifest.in-progress.json') -Encoding utf8NoBOM
        Write-Output ($erpDefinition.table+' : '+$erpRowCount+' rows')
    }
    $erpManifest.finished_at=(Get-Date).ToUniversalTime().ToString('o')
    $erpManifest | ConvertTo-Json -Depth 14 | Set-Content -LiteralPath (Join-Path $erpSnapshotDirectory 'manifest.json') -Encoding utf8NoBOM
}
finally {$erpReadConnection.Dispose()}
