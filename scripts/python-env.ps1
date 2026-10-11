function Initialize-ProjectPython {
    $projectRoot = Split-Path $PSScriptRoot -Parent
    $runtimePython = Join-Path $projectRoot 'runtime\python\python.exe'
    if (-not (Test-Path -LiteralPath $runtimePython -PathType Leaf)) {
        throw "缺少项目自带的 Python：$runtimePython。请一并复制 runtime\python 目录。"
    }
    & $runtimePython -I -X utf8 (Join-Path $PSScriptRoot 'ensure_python.py') | Out-Host
    if ($LASTEXITCODE -ne 0) { throw 'Python 环境准备失败，已停止启动。请根据上方提示处理后重试。' }
    return (Join-Path $projectRoot '.venv\Scripts\python.exe')
}
