$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$projectOriginalPath = $env:Path
$env:Path = (Join-Path $projectRoot 'runtime\node')+';'+$env:Path
Push-Location (Join-Path $projectRoot 'web')
try { & (Join-Path $projectRoot 'runtime\node\npm.cmd') run build; if ($LASTEXITCODE -ne 0) {throw '前端构建失败'} }
finally { Pop-Location; $env:Path = $projectOriginalPath }
& (Join-Path $projectRoot '.venv\Scripts\python.exe') (Join-Path $projectRoot 'backend\manage.py') collectstatic --noinput
