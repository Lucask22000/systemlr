# powerShell/autocommit.ps1
# Executar na raiz do repositório:
# .\powerShell\autocommit.ps1

$root = (Get-Location).Path
Write-Host "Iniciando watcher em: $root"

$global:isCommitting = $false
$global:lastCommitTime = Get-Date "2000-01-01"

$ignoredPatterns = @(
    "\\.git\\",
    "\\.venv\\",
    "\\__pycache__\\",
    "\\node_modules\\",
    "\\migrations\\__pycache__\\",
    "\\instance\\.*\.db$",
    "\.pyc$",
    "\.log$"
)

function Should-Ignore($path) {
    foreach ($pattern in $ignoredPatterns) {
        if ($path -match $pattern) {
            return $true
        }
    }
    return $false
}

function Invoke-AutoCommit {
    param (
        [string]$ChangedPath
    )

    if (Should-Ignore $ChangedPath) {
        return
    }

    if ($global:isCommitting) {
        return
    }

    $now = Get-Date
    $secondsSinceLastCommit = ($now - $global:lastCommitTime).TotalSeconds

    # debounce global para evitar enxurrada de commits
    if ($secondsSinceLastCommit -lt 3) {
        return
    }

    $global:isCommitting = $true

    try {
        Start-Sleep -Milliseconds 800

        git add -A | Out-Null

        $status = git status --porcelain
        if ([string]::IsNullOrWhiteSpace($status)) {
            return
        }

        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        git commit -m "auto: atualização $timestamp" | Out-Null

        if ($LASTEXITCODE -eq 0) {
            $global:lastCommitTime = Get-Date
            Write-Host "Commit criado em $timestamp"
        }
    }
    catch {
        Write-Host "Erro no auto-commit: $($_.Exception.Message)"
    }
    finally {
        $global:isCommitting = $false
    }
}

$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = $root
$watcher.IncludeSubdirectories = $true
$watcher.EnableRaisingEvents = $true
$watcher.NotifyFilter = [System.IO.NotifyFilters]'FileName, DirectoryName, LastWrite, Size'

$action = {
    $path = $Event.SourceEventArgs.FullPath
    Invoke-AutoCommit -ChangedPath $path
}

$createdEvent = Register-ObjectEvent $watcher Created -Action $action
$changedEvent = Register-ObjectEvent $watcher Changed -Action $action
$deletedEvent = Register-ObjectEvent $watcher Deleted -Action $action
$renamedEvent = Register-ObjectEvent $watcher Renamed -Action $action

Write-Host "Monitorando alterações..."
Write-Host "Pressione Enter para parar."
[void](Read-Host)

Unregister-Event -SourceIdentifier $createdEvent.Name
Unregister-Event -SourceIdentifier $changedEvent.Name
Unregister-Event -SourceIdentifier $deletedEvent.Name
Unregister-Event -SourceIdentifier $renamedEvent.Name

$watcher.Dispose()
Write-Host "Watcher finalizado."