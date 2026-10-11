$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$projectOriginalPath = $env:Path
$env:Path = (Join-Path $projectRoot 'runtime\node')+';'+$env:Path
Push-Location (Join-Path $projectRoot 'web')
try { & (Join-Path $projectRoot 'runtime\node\npm.cmd') run dev }
finally { Pop-Location; $env:Path = $projectOriginalPath }
