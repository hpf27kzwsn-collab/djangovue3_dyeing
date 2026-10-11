$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$projectPython = Join-Path $projectRoot '.venv\Scripts\python.exe'
$manager = Join-Path $projectRoot 'backend\manage.py'
& $projectPython $manager migrate
& $projectPython $manager init_data
& $projectPython $manager init_area
