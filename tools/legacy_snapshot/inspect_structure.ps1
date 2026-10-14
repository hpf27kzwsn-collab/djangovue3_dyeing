param([Parameter(Mandatory=$true)][string]$OutputDirectory)
$ErrorActionPreference = 'Stop'
$erpEvidenceDirectory = [IO.Path]::GetFullPath($OutputDirectory)
New-Item -ItemType Directory -Path $erpEvidenceDirectory -ErrorAction Stop | Out-Null
$erpEvidenceConnection = [System.Data.SqlClient.SqlConnection]::new('Server=localhost;Database=Textile_GXHFRS;Integrated Security=True;Encrypt=False;TrustServerCertificate=True;Application Name=ERP ReadOnly Structure And Logic Inspection;')
function Read-Evidence([string]$Sql) {
    $erpEvidenceCommand = $erpEvidenceConnection.CreateCommand()
    $erpEvidenceCommand.CommandText = $Sql
    $erpEvidenceCommand.CommandTimeout = 180
    $erpEvidenceRows = [Collections.Generic.List[object]]::new()
    $erpEvidenceReader = $erpEvidenceCommand.ExecuteReader()
    while ($erpEvidenceReader.Read()) {
        $erpEvidenceRow = [ordered]@{}
        for ($erpEvidenceColumn = 0; $erpEvidenceColumn -lt $erpEvidenceReader.FieldCount; $erpEvidenceColumn++) {
            $erpEvidenceValue = $erpEvidenceReader.GetValue($erpEvidenceColumn)
            $erpEvidenceRow[$erpEvidenceReader.GetName($erpEvidenceColumn)] = if ($erpEvidenceValue -is [DBNull]) { $null } else { $erpEvidenceValue }
        }
        $erpEvidenceRows.Add([pscustomobject]$erpEvidenceRow)
    }
    $erpEvidenceReader.Close()
    $erpEvidenceCommand.Dispose()
    return ,$erpEvidenceRows.ToArray()
}
$erpEvidenceConnection.Open()
try {
    $erpEvidence = [ordered]@{ captured_at = [DateTimeOffset]::Now.ToString('o'); database = 'Textile_GXHFRS'; statements = 'SELECT only' }
    $erpEvidence.database_properties = Read-Evidence @'
SELECT name,collation_name,snapshot_isolation_state_desc,is_read_committed_snapshot_on,compatibility_level
FROM sys.databases WHERE database_id=DB_ID()
'@
    $erpEvidence.tables = Read-Evidence @'
SELECT s.name AS schema_name,t.name AS table_name,t.create_date,t.modify_date,
 CAST(ep.value AS nvarchar(max)) AS description,
 (SELECT SUM(p.rows) FROM sys.partitions p WHERE p.object_id=t.object_id AND p.index_id IN (0,1)) AS approximate_rows
FROM sys.tables t JOIN sys.schemas s ON s.schema_id=t.schema_id
LEFT JOIN sys.extended_properties ep ON ep.major_id=t.object_id AND ep.minor_id=0 AND ep.name='MS_Description'
ORDER BY s.name,t.name
'@
    $erpEvidence.fields = Read-Evidence @'
SELECT s.name AS schema_name,t.name AS table_name,c.column_id,c.name AS field_name,ty.name AS data_type,
 c.max_length,c.precision,c.scale,c.is_nullable,c.is_identity,c.is_computed,c.collation_name,
 CAST(ep.value AS nvarchar(max)) AS description,dc.definition AS default_definition,cc.definition AS computed_definition
FROM sys.tables t JOIN sys.schemas s ON s.schema_id=t.schema_id
JOIN sys.columns c ON c.object_id=t.object_id JOIN sys.types ty ON ty.user_type_id=c.user_type_id
LEFT JOIN sys.extended_properties ep ON ep.major_id=c.object_id AND ep.minor_id=c.column_id AND ep.name='MS_Description'
LEFT JOIN sys.default_constraints dc ON dc.object_id=c.default_object_id
LEFT JOIN sys.computed_columns cc ON cc.object_id=c.object_id AND cc.column_id=c.column_id
ORDER BY s.name,t.name,c.column_id
'@
    $erpEvidence.indexes = Read-Evidence @'
SELECT s.name AS schema_name,t.name AS table_name,i.name AS index_name,i.is_primary_key,i.is_unique,
 i.filter_definition,ic.key_ordinal,ic.is_included_column,c.name AS field_name
FROM sys.tables t JOIN sys.schemas s ON s.schema_id=t.schema_id
JOIN sys.indexes i ON i.object_id=t.object_id JOIN sys.index_columns ic ON ic.object_id=i.object_id AND ic.index_id=i.index_id
JOIN sys.columns c ON c.object_id=ic.object_id AND c.column_id=ic.column_id
WHERE i.name IS NOT NULL ORDER BY s.name,t.name,i.name,ic.key_ordinal,ic.index_column_id
'@
    $erpEvidence.foreign_keys = Read-Evidence @'
SELECT fk.name,ps.name AS source_schema,pt.name AS source_table,pc.name AS source_field,
 rs.name AS target_schema,rt.name AS target_table,rc.name AS target_field,
 fk.delete_referential_action_desc,fk.update_referential_action_desc,fk.is_disabled,fk.is_not_trusted
FROM sys.foreign_keys fk JOIN sys.foreign_key_columns fkc ON fkc.constraint_object_id=fk.object_id
JOIN sys.tables pt ON pt.object_id=fkc.parent_object_id JOIN sys.schemas ps ON ps.schema_id=pt.schema_id
JOIN sys.columns pc ON pc.object_id=pt.object_id AND pc.column_id=fkc.parent_column_id
JOIN sys.tables rt ON rt.object_id=fkc.referenced_object_id JOIN sys.schemas rs ON rs.schema_id=rt.schema_id
JOIN sys.columns rc ON rc.object_id=rt.object_id AND rc.column_id=fkc.referenced_column_id
ORDER BY ps.name,pt.name,fk.name,fkc.constraint_column_id
'@
    $erpEvidence.identities = Read-Evidence @'
SELECT s.name AS schema_name,t.name AS table_name,c.name AS field_name,
 CONVERT(nvarchar(100),c.seed_value) AS seed,CONVERT(nvarchar(100),c.increment_value) AS increment,
 CONVERT(nvarchar(100),c.last_value) AS last_value
FROM sys.identity_columns c JOIN sys.tables t ON t.object_id=c.object_id JOIN sys.schemas s ON s.schema_id=t.schema_id
ORDER BY s.name,t.name,c.column_id
'@
    $erpEvidence.check_constraints = Read-Evidence @'
SELECT s.name AS schema_name,t.name AS table_name,c.name,c.definition,c.is_disabled,c.is_not_trusted
FROM sys.check_constraints c JOIN sys.tables t ON t.object_id=c.parent_object_id JOIN sys.schemas s ON s.schema_id=t.schema_id
ORDER BY s.name,t.name,c.name
'@
    $erpEvidence.modules = Read-Evidence @'
SELECT s.name AS schema_name,o.name AS object_name,o.type,o.type_desc,o.create_date,o.modify_date,
 m.definition,m.uses_ansi_nulls,m.uses_quoted_identifier,m.is_schema_bound,
 OBJECTPROPERTY(o.object_id,'IsEncrypted') AS is_encrypted
FROM sys.objects o JOIN sys.schemas s ON s.schema_id=o.schema_id
JOIN sys.sql_modules m ON m.object_id=o.object_id ORDER BY s.name,o.type,o.name
'@
    $erpEvidence.parameters = Read-Evidence @'
SELECT s.name AS schema_name,o.name AS object_name,p.parameter_id,p.name AS parameter_name,
 ty.name AS data_type,p.max_length,p.precision,p.scale,p.is_output
FROM sys.parameters p JOIN sys.objects o ON o.object_id=p.object_id
JOIN sys.schemas s ON s.schema_id=o.schema_id JOIN sys.types ty ON ty.user_type_id=p.user_type_id
ORDER BY s.name,o.name,p.parameter_id
'@
    $erpEvidence.dependencies = Read-Evidence @'
SELECT OBJECT_SCHEMA_NAME(d.referencing_id) AS source_schema,OBJECT_NAME(d.referencing_id) AS source_name,
 d.referenced_server_name,d.referenced_database_name,d.referenced_schema_name,d.referenced_entity_name,
 d.is_schema_bound_reference,d.is_ambiguous
FROM sys.sql_expression_dependencies d ORDER BY source_schema,source_name,d.referenced_entity_name
'@
    $erpEvidence.triggers = Read-Evidence @'
SELECT OBJECT_SCHEMA_NAME(t.object_id) AS schema_name,t.name,OBJECT_SCHEMA_NAME(t.parent_id) AS parent_schema,
 OBJECT_NAME(t.parent_id) AS parent_name,t.is_disabled,t.is_instead_of_trigger,m.definition
FROM sys.triggers t JOIN sys.sql_modules m ON m.object_id=t.object_id ORDER BY t.name
'@
    $erpEvidence.ui_tables = Read-Evidence 'SELECT * FROM dye.s_DataTable ORDER BY DataTableName'
    $erpEvidence.ui_fields = Read-Evidence 'SELECT * FROM dye.s_DataTableField ORDER BY DataTableName,FieldName'
    $erpEvidence | ConvertTo-Json -Depth 14 | Set-Content -LiteralPath (Join-Path $erpEvidenceDirectory 'structure-and-logic.json') -Encoding utf8NoBOM
    [ordered]@{ captured_at=$erpEvidence.captured_at; tables=$erpEvidence.tables.Count; fields=$erpEvidence.fields.Count;
        modules=$erpEvidence.modules.Count; identities=$erpEvidence.identities.Count;
        ui_tables=$erpEvidence.ui_tables.Count; ui_fields=$erpEvidence.ui_fields.Count;
        database_properties=$erpEvidence.database_properties } | ConvertTo-Json -Depth 5 -Compress
}
finally { $erpEvidenceConnection.Dispose() }
