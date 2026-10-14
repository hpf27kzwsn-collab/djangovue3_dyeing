param([int]$Port = 8000)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
. (Join-Path $PSScriptRoot 'python-env.ps1')
$projectPython = Initialize-ProjectPython
$env:PYTHONUTF8 = '1'
Push-Location (Join-Path $projectRoot 'backend')
try { & $projectPython -m uvicorn application.asgi:application --host 127.0.0.1 --port $Port }
finally { Pop-Location }
