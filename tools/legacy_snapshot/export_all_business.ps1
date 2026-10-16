param(
    [Parameter(Mandatory=$true)][string]$OutputDirectory,
    [Parameter(Mandatory=$true)][string]$EvidencePath,
    [string[]]$Tables
)
$ErrorActionPreference = 'Stop'
[Threading.Thread]::CurrentThread.CurrentCulture = [Globalization.CultureInfo]::InvariantCulture
$erpFullDirectory = [IO.Path]::GetFullPath($OutputDirectory)
New-Item -ItemType Directory -Path $erpFullDirectory -ErrorAction Stop | Out-Null
$erpFullCatalog = Get-Content -LiteralPath (Join-Path $PSScriptRoot '../legacy_models/source_catalog.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$erpFullEvidence = Get-Content -LiteralPath $EvidencePath -Raw -Encoding UTF8 | ConvertFrom-Json
$erpFullDefinitions = @($erpFullCatalog.tables | Where-Object handling -EQ 'business_model')
if ($Tables) {
    $erpFullDefinitions = @($erpFullDefinitions | Where-Object { $_.table -in $Tables })
    if ($erpFullDefinitions.Count -ne $Tables.Count) { throw '所选表必须是目录中明确的业务表且不能重复。' }
}
$erpFullDefinitions = @($erpFullDefinitions | Sort-Object @{Expression={
    $erpFullDefinition = $_
    ($erpFullEvidence.tables | Where-Object { $_.schema_name -eq $erpFullDefinition.schema -and $_.table_name -eq $erpFullDefinition.table }).approximate_rows
}},schema,table)
$erpFullConnection = [System.Data.SqlClient.SqlConnection]::new('Server=localhost;Database=Textile_GXHFRS;Integrated Security=True;Encrypt=False;TrustServerCertificate=True;Application Name=ERP ReadOnly Full Business Export;')
Add-Type -Path (Join-Path $PSScriptRoot 'ReadOnlySnapshot.cs') -ReferencedAssemblies (Get-ChildItem -LiteralPath (Join-Path $PSHOME 'ref') -Filter '*.dll' | ForEach-Object FullName)
$erpFullConnection.Open()
try {
    $erpFullManifest = [ordered]@{ database='Textile_GXHFRS'; started_at=[DateTimeOffset]::Now.ToString('o');
        structure_captured_at=$erpFullEvidence.captured_at; statements='SELECT only'; isolation='READ COMMITTED';
        source_scope=if($Tables){'selected business tables: '+($Tables -join ',')}else{'all seven-module business_model tables in source_catalog; independent finance excluded'};
        numeric_encoding='SQL numeric values stored as invariant strings, including SqlDecimal precision up to 38';
        no_primary_key_identity='key is null; row is extraction ordinal, not a fabricated old-system id'; tables=@() }
    foreach ($erpFullDefinition in $erpFullDefinitions) {
        $erpFullFields = @($erpFullEvidence.fields | Where-Object { $_.schema_name -eq $erpFullDefinition.schema -and $_.table_name -eq $erpFullDefinition.table })
        $erpFullKeys = [string[]]@($erpFullDefinition.primary_key)
        $erpFullColumns = [string[]]@($erpFullFields | ForEach-Object field_name)
        if ($erpFullColumns.Count -ne $erpFullDefinition.fields.Count) { throw "最新字段与已建模型字段数不一致：$($erpFullDefinition.table)" }
        $erpFullFile = $erpFullDefinition.schema + '.' + $erpFullDefinition.table + '.jsonl'
        $erpFullPath = Join-Path $erpFullDirectory $erpFullFile
        $erpFullStarted = [DateTimeOffset]::Now.ToString('o')
        Write-Output ('START ' + $erpFullDefinition.schema + '.' + $erpFullDefinition.table)
        $erpFullRows = [ErpReadOnlySnapshot]::Export($erpFullConnection,$erpFullDefinition.schema,$erpFullDefinition.table,$erpFullColumns,$erpFullKeys,$erpFullPath)
        $erpFullManifest.tables += [ordered]@{ schema=$erpFullDefinition.schema; table=$erpFullDefinition.table;
            modules=@($erpFullDefinition.module); columns=$erpFullFields; primary_key=$erpFullKeys; rows=$erpFullRows;
            file=$erpFullFile; sha256=(Get-FileHash -LiteralPath $erpFullPath -Algorithm SHA256).Hash.ToLowerInvariant();
            bytes=(Get-Item -LiteralPath $erpFullPath).Length; started_at=$erpFullStarted; finished_at=[DateTimeOffset]::Now.ToString('o') }
        $erpFullManifest | ConvertTo-Json -Depth 15 | Set-Content -LiteralPath (Join-Path $erpFullDirectory 'manifest.in-progress.json') -Encoding utf8NoBOM
        Write-Output ('DONE ' + $erpFullDefinition.schema + '.' + $erpFullDefinition.table + ' ' + $erpFullRows + ' rows; ' + $erpFullManifest.tables.Count + '/' + $erpFullDefinitions.Count)
    }
    $erpFullManifest.finished_at = [DateTimeOffset]::Now.ToString('o')
    $erpFullManifest | ConvertTo-Json -Depth 15 | Set-Content -LiteralPath (Join-Path $erpFullDirectory 'manifest.json') -Encoding utf8NoBOM
    Write-Output ('COMPLETE ' + $erpFullDefinitions.Count + ' business tables')
}
finally { $erpFullConnection.Dispose() }
