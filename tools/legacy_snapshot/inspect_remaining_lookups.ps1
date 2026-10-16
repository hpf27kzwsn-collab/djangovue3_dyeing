param([Parameter(Mandatory=$true)][string]$OutputPath,[Parameter(Mandatory=$true)][string]$CandidatesPath)
$ErrorActionPreference='Stop'
$catalog=Get-Content -LiteralPath (Join-Path $PSScriptRoot '../../backend/plugins/erp_base/source_foundation_lookups.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$candidates=Get-Content -LiteralPath $CandidatesPath -Raw -Encoding UTF8 | ConvertFrom-Json
$connection=[System.Data.SqlClient.SqlConnection]::new('Server=localhost;Database=Textile_GXHFRS;Integrated Security=True;Encrypt=False;TrustServerCertificate=True;Application Name=ERP ReadOnly Lookup Comparison;')
$connection.Open()
try {
    $result=[ordered]@{captured_at=[DateTimeOffset]::Now.ToString('o');statements='SELECT only';qualification='Unqualified physical tables explicitly use dye, as the original business source';lookups=@()}
    foreach($candidate in $candidates) {
        if(-not $candidate.ok){continue}
        $spec=$catalog.lookups.($candidate.id)
        $sql=$spec.query;$offset=$sql.IndexOf('1=1')
        if($offset -ge 0){$sql=$sql.Substring(0,$offset)}
        elseif($sql -match '(?i)where'){$sql+=' and '}
        else{$sql+=' where '}
        $sql+=$(if([string]::IsNullOrWhiteSpace($spec.LookupDataFilter)){'1=1'}else{$spec.LookupDataFilter})
        foreach($table in $candidate.models) {
            $sql=[regex]::Replace($sql,'(?i)\b(FROM|JOIN)(\s+)('+[regex]::Escape($table)+')\b','$1$2dye.$3')
        }
        $cmd=$connection.CreateCommand();$cmd.CommandTimeout=180
        $cmd.CommandText='SELECT t.['+$spec.KeyField.Replace(']',']]')+'] AS id,t.['+$spec.DisplayField.Replace(']',']]')+'] AS text FROM ('+$sql+') t'
        $rows=[Collections.Generic.List[object]]::new()
        try {
            $reader=$cmd.ExecuteReader()
            while($reader.Read()) {
                $rows.Add(@{id=$(if($reader.IsDBNull(0)){$null}else{$reader.GetValue(0)});text=$(if($reader.IsDBNull(1)){$null}else{$reader.GetValue(1)})})
            }
            $reader.Close()
            $result.lookups+=@{id=$candidate.id;ok=$true;rows=$rows.ToArray()}
            Write-Output ($candidate.id+' '+$rows.Count)
        } catch [Data.SqlClient.SqlException] {
            $result.lookups+=@{id=$candidate.id;ok=$false;number=$_.Exception.Number;message=$_.Exception.Message}
            Write-Output ($candidate.id+' original error '+$_.Exception.Number)
        } finally {$cmd.Dispose()}
    }
    $result | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $OutputPath -Encoding UTF8
} finally {$connection.Close();$connection.Dispose()}
