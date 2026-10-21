param([Parameter(Mandatory=$true)][string]$EvidenceDirectory)
$ErrorActionPreference='Stop'
$directory=[IO.Path]::GetFullPath($EvidenceDirectory)
$connection=[System.Data.SqlClient.SqlConnection]::new('Server=localhost;Database=Textile_GXHFRS;Integrated Security=True;Encrypt=False;TrustServerCertificate=True;Application Name=ERP Phase6 SELECT Metadata Review;')
function Read-Rows([string]$sql,[string]$query) {
    $command=$connection.CreateCommand()
    $command.CommandText=$sql
    $command.CommandTimeout=30
    if ($query) { $null=$command.Parameters.Add('@query',[System.Data.SqlDbType]::NVarChar,-1); $command.Parameters['@query'].Value=$query }
    try {
        $reader=$command.ExecuteReader()
        $rows=[Collections.Generic.List[object]]::new()
        while ($reader.Read()) {
            $row=[ordered]@{}
            for ($i=0;$i -lt $reader.FieldCount;$i++) { $row[$reader.GetName($i)]=if ($reader.IsDBNull($i)) {$null} else {$reader.GetValue($i)} }
            $rows.Add([pscustomobject]$row)
        }
        $reader.Close()
        return ,$rows.ToArray()
    } finally { $command.Dispose() }
}
$connection.Open()
try {
    $result=[ordered]@{captured_at=[DateTimeOffset]::Now.ToString('o');statements='SELECT metadata only; original queries are described, never executed'}
    $result.databases=Read-Rows 'SELECT name,state_desc,HAS_DBACCESS(name) AS accessible FROM sys.databases' ''
    $result.servers=Read-Rows 'SELECT name,product,provider,data_source,is_linked FROM sys.servers' ''
    $result.synonyms=Read-Rows 'SELECT SCHEMA_NAME(schema_id) AS schema_name,name,base_object_name FROM sys.synonyms' ''
    $result.print_hashes=Read-Rows "SELECT RptID,DATALENGTH(Template) AS template_bytes,DATALENGTH(TemplateXml) AS xml_bytes,CONVERT(varchar(64),HASHBYTES('SHA2_256',CONVERT(varbinary(max),Template)),2) AS template_sha256,CONVERT(varchar(64),HASHBYTES('SHA2_256',CONVERT(varbinary(max),TemplateXml)),2) AS xml_sha256 FROM dye.s_RptInfo ORDER BY RptID" ''
    $results=[Collections.Generic.List[object]]::new()
    foreach ($entry in (Get-Content -LiteralPath (Join-Path $directory 'queries.json') -Raw | ConvertFrom-Json)) {
        try {
            $rows=Read-Rows 'SELECT column_ordinal,name,system_type_name,is_nullable,error_number,error_message FROM sys.dm_exec_describe_first_result_set(@query,NULL,0)' $entry.sql
            $results.Add([ordered]@{name=$entry.name;columns=$rows})
        } catch [System.Data.SqlClient.SqlException] {
            $results.Add([ordered]@{name=$entry.name;error_number=$_.Exception.Number;error=$_.Exception.Message})
        }
    }
    $result.queries=$results.ToArray()
    $result | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $directory 'query-metadata.json') -Encoding utf8NoBOM
    [ordered]@{queries=$results.Count;databases=$result.databases;servers=$result.servers} | ConvertTo-Json -Depth 5
} finally { $connection.Dispose() }
