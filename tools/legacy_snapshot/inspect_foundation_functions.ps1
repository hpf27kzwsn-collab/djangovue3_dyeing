param([Parameter(Mandatory=$true)][string]$OutputPath)
$ErrorActionPreference = 'Stop'
$erpFoundationConnection = [System.Data.SqlClient.SqlConnection]::new('Server=localhost;Database=Textile_GXHFRS;Integrated Security=True;Encrypt=False;TrustServerCertificate=True;Application Name=ERP ReadOnly Foundation Verification;')
function Read-Foundation([string]$Sql) {
    $erpFoundationCommand = $erpFoundationConnection.CreateCommand()
    $erpFoundationCommand.CommandText = $Sql
    $erpFoundationCommand.CommandTimeout = 180
    $erpFoundationReader = $erpFoundationCommand.ExecuteReader()
    $erpFoundationRows = [Collections.Generic.List[object]]::new()
    while ($erpFoundationReader.Read()) {
        $erpFoundationRow = [ordered]@{}
        for ($erpFoundationIndex=0; $erpFoundationIndex -lt $erpFoundationReader.FieldCount; $erpFoundationIndex++) {
            $erpFoundationValue = $erpFoundationReader.GetValue($erpFoundationIndex)
            $erpFoundationRow[$erpFoundationReader.GetName($erpFoundationIndex)] = if ($erpFoundationValue -is [DBNull]) { $null } else { $erpFoundationValue }
        }
        $erpFoundationRows.Add([pscustomobject]$erpFoundationRow)
    }
    $erpFoundationReader.Close()
    $erpFoundationCommand.Dispose()
    return ,$erpFoundationRows.ToArray()
}
$erpFoundationConnection.Open()
try {
    $result = [ordered]@{ captured_at=[DateTimeOffset]::Now.ToString('o'); statements='SELECT only'; probes=@() }
    $functions = @('Fn_Get_AZ','Fn_Get_NumNo','GET_NUMBER','GetNumberFromString3','NormalizeTextFast','SafeVarToFloat','SafeVarToInt')
    $samples = @($null,'','  ','AB12cd-3.4','a-12.34kg56','-','-.','1..2','1.2.3','+12','1e3','1,234','2147483647.5','。；！【】￥＋','Ａ１２．３Ｂ','éäZ09',"a`r`nb`t c",'12.5  ',('9'*110),'.','１２．３','0.00005','2147483647.49',"a$([char]1)b",'。，；：！？、（）【】｛｝《》「」『』～＠＃￥％＆＊＋－＝／｜＼')
    foreach ($fn in $functions) {
        foreach ($value in $samples) {
            $command=$erpFoundationConnection.CreateCommand()
            $command.CommandText='SELECT dye.['+$fn+'](@value) AS value'
            $param=$command.Parameters.Add('@value',[Data.SqlDbType]::NVarChar,-1)
            $param.Value=if($null -eq $value){[DBNull]::Value}else{$value}
            try { $answer=$command.ExecuteScalar();$result.probes += [ordered]@{name=$fn;input=$value;ok=$true;value=if($answer -is [DBNull]){$null}else{$answer}} }
            catch [Data.SqlClient.SqlException] { $result.probes += [ordered]@{name=$fn;input=$value;ok=$false;error_number=$_.Exception.Number;message=$_.Exception.Message} }
            finally { $command.Dispose() }
        }
    }
    $result.parameters = Read-Foundation "SELECT ParamName,ParamValue,dye.GetSysParamValue(ParamName) AS result FROM dye.s_SysParams ORDER BY ParamName"
    $result.lookups = Read-Foundation 'SELECT LookupID,LookupName,DataTableName,LookupDataFilter,KeyField,DisplayField FROM dye.s_Lookup ORDER BY LookupID'
    $result.lookup_results = @()
    $catalog = Get-Content -LiteralPath (Join-Path $PSScriptRoot '../../backend/plugins/erp_base/source_foundation_lookups.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    foreach ($property in $catalog.lookups.PSObject.Properties) {
        $spec = $property.Value
        if ($null -eq $spec.adapter) { continue }
        $sql = $spec.query
        $offset = $sql.IndexOf('1=1')
        if ($offset -ge 0) { $sql = $sql.Substring(0,$offset) }
        elseif ($sql -match '(?i)where') { $sql += ' and ' }
        else { $sql += ' where ' }
        $sql += $(if ([string]::IsNullOrWhiteSpace($spec.LookupDataFilter)) { '1=1' } else { $spec.LookupDataFilter })
        $sql = [regex]::Replace($sql,'(?i)(?<![\w.])p_(FieldValid|Customer|Gray|Dept)\b','dye.p_$1')
        $extras = switch ($spec.LookupID) {
            'B001' { ',EbOd,Linker,LinkerTel' }
            'B006' { ',IsOut,DeptID,EmpKind,DeptIDName' }
            'B154' { ',IsOut,DeptID,EmpKind,DeptIDName' }
            'A002' { ',CustKindID' }
            'B405' { ',unit' }
            default { '' }
        }
        $statement = 'SELECT ['+$spec.KeyField+'] as id,['+$spec.DisplayField+'] as text'+$extras+' FROM ('+$sql+') xx'
        $result.lookup_results += [ordered]@{lookup=$spec.LookupID;statement=$statement;other_fields=@($extras.Split(',') | Where-Object { $_ });rows=(Read-Foundation $statement)}
    }
    $result.combos = Read-Foundation 'SELECT ComboID,DisplayIndex AS [index],KeyValue AS id,DisplayValue AS [text] FROM dye.s_DBComboValue'
    $result.dates = @()
    foreach ($kind in @('year','mon','d','ym','md','bad',$null)) {
        foreach ($pair in @(@(2,2),@(0,0),@(26,25),@(-2,-1),@($null,$null))) {
            $command=$erpFoundationConnection.CreateCommand();$command.CommandText="SELECT * FROM dbo.fn_GetContinuousDate('2024-02-29',@kind,@prev,@next)"
            $p=$command.Parameters.Add('@kind',[Data.SqlDbType]::NVarChar,10);$p.Value=if($null -eq $kind){[DBNull]::Value}else{$kind}
            $p=$command.Parameters.Add('@prev',[Data.SqlDbType]::Int);$p.Value=if($null -eq $pair[0]){[DBNull]::Value}else{$pair[0]}
            $p=$command.Parameters.Add('@next',[Data.SqlDbType]::Int);$p.Value=if($null -eq $pair[1]){[DBNull]::Value}else{$pair[1]}
            $reader=$command.ExecuteReader();$rows=@()
            while($reader.Read()){$rows += [ordered]@{DataDate=$reader.GetDateTime(0).ToString('yyyy-MM-dd');DateAlis=$reader.GetValue(1);DateCommon=$reader.GetValue(2)}}
            $reader.Close();$command.Dispose();$result.dates += [ordered]@{kind=$kind;prev=$pair[0];next=$pair[1];rows=$rows}
        }
    }
    $result | ConvertTo-Json -Depth 15 | Set-Content -LiteralPath $OutputPath -Encoding utf8NoBOM
    Write-Output ('Scalar probes='+$result.probes.Count+'; parameters='+$result.parameters.Count+'; lookup definitions='+$result.lookups.Count+'; date groups='+$result.dates.Count)
}
finally { $erpFoundationConnection.Dispose() }
