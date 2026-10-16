param([Parameter(Mandatory=$true)][string]$OutputPath)
$ErrorActionPreference='Stop'
$connection=[Data.SqlClient.SqlConnection]::new('Server=localhost;Database=Textile_GXHFRS;Integrated Security=True;Encrypt=False;TrustServerCertificate=True;Application Name=ERP ReadOnly Number Functions;')
$connection.Open()
try {
    $result=@()
    foreach($name in @('F_Get_No','Fn_Get_No')) {
        foreach($value in @($null,'','A123B','１２a３','1234567890123456789012345','甲１２乙34567890','A-1.2','   ')) {
            $command=$connection.CreateCommand();$command.CommandText='SELECT dye.['+$name+'](@value)'
            $parameter=$command.Parameters.Add('@value',[Data.SqlDbType]::NVarChar,1000)
            $parameter.Value=$(if($null -eq $value){[DBNull]::Value}else{$value})
            $actual=$command.ExecuteScalar()
            $result+=@{name=$name;input=$value;result=$(if($actual -is [DBNull]){$null}else{$actual})}
            $command.Dispose()
        }
    }
    $result | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $OutputPath -Encoding UTF8
} finally {$connection.Close();$connection.Dispose()}
