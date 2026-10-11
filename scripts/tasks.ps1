param([ValidateSet('redis','worker','beat')][string]$Service='worker')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
Push-Location (Join-Path $projectRoot 'backend')
try {
  switch ($Service) {
    'redis' {
      $redisExecutable = Get-ChildItem (Join-Path $projectRoot 'runtime\redis') -Filter redis-server.exe -Recurse | Select-Object -First 1
      Push-Location (Join-Path $projectRoot 'runtime')
      try { & $redisExecutable.FullName 'redis.conf' }
      finally { Pop-Location }
    }
    'worker' { & (Join-Path $projectRoot '.venv\Scripts\python.exe') -m celery -A application.celery worker --pool=solo --loglevel=info }
    'beat' { & (Join-Path $projectRoot '.venv\Scripts\python.exe') -m celery -A application.celery beat --loglevel=info --pidfile= --schedule=celerybeat-schedule }
  }
}
finally { Pop-Location }
