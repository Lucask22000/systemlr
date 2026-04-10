$ErrorActionPreference = 'Stop'

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$PythonPath = Join-Path $ProjectRoot '.venv\Scripts\python.exe'
$RunPath = Join-Path $ProjectRoot 'run.py'
$LogDir = Join-Path $ProjectRoot 'logs'
$LogPath = Join-Path $LogDir 'systemlr.log'

if (-not (Test-Path $PythonPath)) {
    throw "Python da virtualenv nao encontrado em $PythonPath"
}

if (-not (Test-Path $RunPath)) {
    throw "Arquivo run.py nao encontrado em $RunPath"
}

if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

if (-not $env:FLASK_CONFIG) {
    $env:FLASK_CONFIG = 'development'
}
if (-not $env:SYSTEMLR_HOST) {
    $env:SYSTEMLR_HOST = '0.0.0.0'
}
if (-not $env:SYSTEMLR_PORT) {
    $env:SYSTEMLR_PORT = '5000'
}
$env:SYSTEMLR_DEBUG = '0'
$env:SYSTEMLR_USE_RELOADER = '0'
$env:PYTHONUNBUFFERED = '1'

$port = 5000
try {
    $port = [int]$env:SYSTEMLR_PORT
} catch {
    $port = 5000
}

$existing = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
if ($existing) {
    "[{0}] Porta {1} ja esta em uso. Inicializacao ignorada." -f (Get-Date -Format s), $port | Tee-Object -FilePath $LogPath -Append
    exit 0
}

Set-Location $ProjectRoot
"[{0}] Iniciando SystemLR em http://127.0.0.1:{1}" -f (Get-Date -Format s), $port | Tee-Object -FilePath $LogPath -Append
$commandLine = "`"$PythonPath`" `"$RunPath`" >> `"$LogPath`" 2>&1"
cmd.exe /d /c $commandLine
exit $LASTEXITCODE
