param([Parameter(Mandatory=$true)][string]$OutputPath)
$ErrorActionPreference='Stop'
$connection=[System.Data.SqlClient.SqlConnection]::new('Server=localhost;Database=Textile_GXHFRS;Integrated Security=True;Encrypt=False;TrustServerCertificate=True;Application Name=ERP ReadOnly Remaining Foundation;')
$connection.Open()
try {
    $result=[ordered]@{captured_at=[DateTimeOffset]::Now.ToString('o');statements='SELECT only';probes=@();pinyin=@()}
    $cases=@(
        @{name='fn_ExpandRange'; args=@($null)}, @{name='fn_ExpandRange'; args=@('')},
        @{name='fn_ExpandRange'; args=@('1-4')}, @{name='fn_ExpandRange'; args=@('4-1')},
        @{name='fn_ExpandRange'; args=@('1-3 ')}, @{name='fn_ExpandRange'; args=@('-3')},
        @{name='fn_ExpandRange'; args=@('A-3')}, @{name='fn_ExpandRange'; args=@('2147483647-2147483647')}
    )
    foreach($n in @($null,-1,0,0.5,299.999,300,450,999,1234.567)) { $cases+=@{name='fn_GetDyeVat';args=@($n)} }
    foreach($n in @($null,-1,0,0.01,0.1,0.99,1,1.005,10,100,1001,100000001.01,9999999999999.99)) {
        foreach($kind in @(0,1,2)) { $cases+=@{name='L2U';args=@($n,$kind)} }
    }
    foreach($case in $cases) {
        $cmd=$connection.CreateCommand();$parameters=@()
        for($i=0;$i -lt $case.args.Count;$i++) {
            $parameters+=('@p'+$i)
            $p=$cmd.Parameters.Add('@p'+$i,[Data.SqlDbType]::NVarChar,-1)
            $p.Value=if($null -eq $case.args[$i]){[DBNull]::Value}else{[string]$case.args[$i]}
        }
        $cmd.CommandText='SELECT dye.['+$case.name+']('+($parameters -join ',')+')'
        try {$value=$cmd.ExecuteScalar();$result.probes+=@{name=$case.name;args=$case.args;ok=$true;value=$(if($value -is [DBNull]){$null}else{$value})}}
        catch [Data.SqlClient.SqlException] {$result.probes+=@{name=$case.name;args=$case.args;ok=$false;error_number=$_.Exception.Number}}
        finally {$cmd.Dispose()}
    }
    $cmd=$connection.CreateCommand();$cmd.CommandTimeout=1800
    $cmd.CommandText="SELECT n,dbo.f_GetPy(NCHAR(n)) AS first_py,dye.fun_getPY(NCHAR(n)) AS second_py FROM (SELECT TOP(65536) ROW_NUMBER()OVER(ORDER BY (SELECT NULL))-1 AS n FROM sys.all_objects a CROSS JOIN sys.all_objects b) t WHERE n NOT BETWEEN 55296 AND 57343 ORDER BY n"
    $reader=$cmd.ExecuteReader();$pinyin=[Collections.Generic.List[object]]::new()
    while($reader.Read()) {
        $pinyin.Add(@{code=$reader.GetInt64(0);first=$(if($reader.IsDBNull(1)){$null}else{$reader.GetString(1)});second=$(if($reader.IsDBNull(2)){$null}else{$reader.GetString(2)})})
    }
    $reader.Close();$cmd.Dispose();$result.pinyin=$pinyin.ToArray()
    $result | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $OutputPath -Encoding UTF8
    Write-Output ('SELECT verification: '+$result.probes.Count+' scalar cases; '+$pinyin.Count+' character pairs')
} finally {$connection.Close();$connection.Dispose()}

