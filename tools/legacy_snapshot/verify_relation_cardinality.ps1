param([Parameter(Mandatory=$true)][string]$Plan,[Parameter(Mandatory=$true)][string]$Output)
$ErrorActionPreference='Stop'
$queries=Get-Content -LiteralPath $Plan -Raw | ConvertFrom-Json
$connection=[System.Data.SqlClient.SqlConnection]::new('Server=localhost;Database=Textile_GXHFRS;Integrated Security=True;Encrypt=False;TrustServerCertificate=True;Application Name=ERP ReadOnly Relation Counts;')
$results=[Collections.Generic.List[object]]::new()
$connection.Open()
try {
    foreach($query in $queries) {
        if(-not $query.sql.StartsWith('SELECT ')){throw 'Only SELECT plans are accepted'}
        $command=$connection.CreateCommand();$command.CommandText=$query.sql;$command.CommandTimeout=180
        $watch=[Diagnostics.Stopwatch]::StartNew()
        $result=[ordered]@{id=$query.id;started_at=[DateTimeOffset]::Now.ToString('o');source=$query.source;target=$query.target}
        try {
            $reader=$command.ExecuteReader()
            if($reader.Read()) {
                for($i=0;$i -lt $reader.FieldCount;$i++) {$result[$reader.GetName($i)]=$reader.GetValue($i)}
            }
            $reader.Close();$result.status='checked'
        } catch {$result.status='query_failed';$result.error=$_.Exception.Message}
        finally {$command.Dispose()}
        $result.seconds=$watch.Elapsed.TotalSeconds;$results.Add($result)
        ConvertTo-Json -InputObject $results.ToArray() -Depth 8 | Set-Content -LiteralPath $Output -Encoding utf8NoBOM
        Write-Output ($query.id+' '+$result.status+' '+$result.child_rows+' rows')
    }
} finally {$connection.Dispose()}
