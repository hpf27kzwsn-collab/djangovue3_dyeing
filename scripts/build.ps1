$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
. (Join-Path $PSScriptRoot 'python-env.ps1')
$projectPython = Initialize-ProjectPython
$projectOriginalPath = $env:Path
$env:Path = (Join-Path $projectRoot 'runtime\node')+';'+$env:Path
Push-Location (Join-Path $projectRoot 'web')
try { & (Join-Path $projectRoot 'runtime\node\npm.cmd') run build; if ($LASTEXITCODE -ne 0) {throw '前端构建失败'} }
finally { Pop-Location; $env:Path = $projectOriginalPath }
& $projectPython (Join-Path $projectRoot 'backend\manage.py') collectstatic --noinput
