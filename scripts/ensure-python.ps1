$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'python-env.ps1')
$projectPython = Initialize-ProjectPython
Write-Host "Python 环境已就绪：$projectPython"
