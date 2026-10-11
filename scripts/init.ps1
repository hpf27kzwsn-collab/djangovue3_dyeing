$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
. (Join-Path $PSScriptRoot 'python-env.ps1')
$projectPython = Initialize-ProjectPython
$manager = Join-Path $projectRoot 'backend\manage.py'
& $projectPython $manager migrate
& $projectPython $manager init_data
& $projectPython $manager init_area
