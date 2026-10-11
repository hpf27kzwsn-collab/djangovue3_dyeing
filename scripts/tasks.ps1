param([ValidateSet('redis','worker','beat')][string]$Service='worker')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
if ($Service -ne 'redis') {
  . (Join-Path $PSScriptRoot 'python-env.ps1')
  $projectPython = Initialize-ProjectPython
}
Push-Location (Join-Path $projectRoot 'backend')
try {
  switch ($Service) {
    'redis' {
      $redisExecutable = Get-ChildItem (Join-Path $projectRoot 'runtime\redis') -Filter redis-server.exe -Recurse | Select-Object -First 1
      Push-Location (Join-Path $projectRoot 'runtime')
      try { & $redisExecutable.FullName 'redis.conf' }
      finally { Pop-Location }
    }
    'worker' { & $projectPython -m celery -A application.celery worker --pool=solo --loglevel=info }
    'beat' { & $projectPython -m celery -A application.celery beat --loglevel=info --pidfile= --schedule=celerybeat-schedule }
  }
}
finally { Pop-Location }
