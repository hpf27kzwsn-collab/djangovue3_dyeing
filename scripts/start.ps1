$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$projectPython = Join-Path $projectRoot '.venv\Scripts\python.exe'
$env:PYTHONUTF8 = '1'
Push-Location (Join-Path $projectRoot 'backend')
try { & $projectPython -m uvicorn application.asgi:application --host 127.0.0.1 --port 8000 }
finally { Pop-Location }
