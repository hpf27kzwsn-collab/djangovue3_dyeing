param([Parameter(Mandatory=$true)][string]$OutputPath,[Parameter(Mandatory=$true)][string]$CandidatesPath)
$ErrorActionPreference='Stop'
$candidates=Get-Content -LiteralPath $CandidatesPath -Raw -Encoding UTF8 | ConvertFrom-Json
$connection=[System.Data.SqlClient.SqlConnection]::new('Server=localhost;Database=Textile_GXHFRS;Integrated Security=True;Encrypt=False;TrustServerCertificate=True;Application Name=ERP ReadOnly Defined Lookup Reference;')
$connection.Open()
try {
    $result=[ordered]@{captured_at=[DateTimeOffset]::Now.ToString('o');statements='SELECT only';kind='Defined repaired reference, original errors recorded separately';lookups=@()}
    foreach($candidate in $candidates) {
        if(-not $candidate.ok){continue}
        $cmd=$connection.CreateCommand();$cmd.CommandTimeout=180
        $cmd.CommandText='SELECT t.['+$candidate.key.Replace(']',']]')+'] AS id,t.['+$candidate.label.Replace(']',']]')+'] AS text FROM ('+$candidate.reference+') t'
        $rows=[Collections.Generic.List[object]]::new()
        try {
            $reader=$cmd.ExecuteReader()
            while($reader.Read()) {$rows.Add(@{id=$(if($reader.IsDBNull(0)){$null}else{$reader.GetValue(0)});text=$(if($reader.IsDBNull(1)){$null}else{$reader.GetValue(1)})})}
            $reader.Close()
            $result.lookups+=@{id=$candidate.id;ok=$true;rows=$rows.ToArray()}
            Write-Output ($candidate.id+' '+$rows.Count)
        } catch [Data.SqlClient.SqlException] {
            $result.lookups+=@{id=$candidate.id;ok=$false;number=$_.Exception.Number;message=$_.Exception.Message}
            Write-Output ($candidate.id+' reference error '+$_.Exception.Number)
        } finally {$cmd.Dispose()}
    }
    $result | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $OutputPath -Encoding UTF8
} finally {$connection.Close();$connection.Dispose()}
