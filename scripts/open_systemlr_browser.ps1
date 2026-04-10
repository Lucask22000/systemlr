$ErrorActionPreference = 'Stop'

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$LogDir = Join-Path $ProjectRoot 'logs'
$LogPath = Join-Path $LogDir 'systemlr-browser.log'

if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

$url = if ($env:SYSTEMLR_BROWSER_URL) {
    $env:SYSTEMLR_BROWSER_URL
} else {
    'http://127.0.0.1:5000'
}

$maxAttempts = 12
$sleepSeconds = 5

for ($attempt = 1; $attempt -le $maxAttempts; $attempt++) {
    try {
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 5
        if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 500) {
            "[{0}] Abrindo navegador em {1}" -f (Get-Date -Format s), $url | Tee-Object -FilePath $LogPath -Append
            Start-Process $url
            exit 0
        }
    } catch {
        if ($attempt -eq 1) {
            "[{0}] Aguardando o SystemLR responder em {1}" -f (Get-Date -Format s), $url | Tee-Object -FilePath $LogPath -Append
        }
    }

    Start-Sleep -Seconds $sleepSeconds
}

"[{0}] Nao foi possivel abrir o navegador automaticamente. URL indisponivel: {1}" -f (Get-Date -Format s), $url | Tee-Object -FilePath $LogPath -Append
exit 1
