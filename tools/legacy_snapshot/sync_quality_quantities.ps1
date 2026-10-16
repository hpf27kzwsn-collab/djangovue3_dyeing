param([Parameter(Mandatory=$true)][string]$Actor)
$ErrorActionPreference='Stop'
$projectRoot=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..'))
$outputFile=Join-Path $projectRoot ('.runtime-temp/quality-quantities-'+[DateTime]::Now.ToString('yyyyMMdd-HHmmss-fffffff')+'.json')
& (Join-Path $PSScriptRoot 'export_quality_quantities.ps1') -OutputFile $outputFile
& (Join-Path $projectRoot '.venv/Scripts/python.exe') (Join-Path $projectRoot 'backend/manage.py') legacy_import_quality_quantities $outputFile --actor $Actor
if($LASTEXITCODE -ne 0){throw '质量数量映射失败；原导出文件已保留。'}
