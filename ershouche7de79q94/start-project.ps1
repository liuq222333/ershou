$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $ProjectRoot

$LogDir = Join-Path $ProjectRoot "logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

function Write-Info {
    param(
        [string]$Message
    )

    Write-Host ("[INFO] {0}" -f $Message)
}

function Write-Pass {
    param(
        [string]$Message
    )

    Write-Host ("[PASS] {0}" -f $Message)
}

function Write-Warn {
    param(
        [string]$Message
    )

    Write-Host ("[WARN] {0}" -f $Message)
}

function Stop-WithError {
    param(
        [string]$Message
    )

    Write-Host ("[FAIL] {0}" -f $Message)
    exit 1
}

function Get-CommandPath {
    param(
        [string]$Name
    )

    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if ($null -eq $cmd) {
        return $null
    }

    return $cmd.Source
}

function Get-ListeningPortInfo {
    param(
        [int]$Port
    )

    try {
        $conn = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction Stop | Select-Object -First 1
        if ($null -ne $conn) {
            return [pscustomobject]@{
                Port = $Port
                Pid = $conn.OwningProcess
            }
        }
    } catch {
    }

    $lines = netstat -ano -p tcp 2>$null
    foreach ($line in $lines) {
        if ($line -match "^\s*TCP\s+\S+:$Port\s+\S+\s+LISTENING\s+(\d+)\s*$") {
            return [pscustomobject]@{
                Port = $Port
                Pid = [int]$matches[1]
            }
        }
    }

    return $null
}

function Get-ProcessNameSafe {
    param(
        [int]$ProcessId
    )

    try {
        return (Get-Process -Id $ProcessId -ErrorAction Stop).ProcessName
    } catch {
        return "unknown"
    }
}

function Start-LoggedProcess {
    param(
        [string]$Name,
        [string]$FilePath,
        [string[]]$ArgumentList,
        [string]$WorkingDirectory,
        [string]$StdOutPath,
        [string]$StdErrPath
    )

    if (Test-Path -LiteralPath $StdOutPath) {
        Remove-Item -LiteralPath $StdOutPath -Force
    }

    if (Test-Path -LiteralPath $StdErrPath) {
        Remove-Item -LiteralPath $StdErrPath -Force
    }

    $process = Start-Process `
        -FilePath $FilePath `
        -ArgumentList $ArgumentList `
        -WorkingDirectory $WorkingDirectory `
        -RedirectStandardOutput $StdOutPath `
        -RedirectStandardError $StdErrPath `
        -PassThru `
        -WindowStyle Hidden

    Write-Pass "$Name started with PID $($process.Id)"
}

$PythonExe = Join-Path $ProjectRoot ".venv311\Scripts\python.exe"
$ConfigPath = Join-Path $ProjectRoot "config.ini"
$AdminDir = Join-Path $ProjectRoot "api\templates\front\admin"
$FrontDir = Join-Path $ProjectRoot "api\templates\front\front"
$AdminPackage = Join-Path $AdminDir "package.json"
$FrontPackage = Join-Path $FrontDir "package.json"
$AdminNodeModules = Join-Path $AdminDir "node_modules"
$FrontNodeModules = Join-Path $FrontDir "node_modules"
$BackendOut = Join-Path $LogDir "backend.log"
$BackendErr = Join-Path $LogDir "backend-error.log"
$AdminOut = Join-Path $LogDir "admin.log"
$AdminErr = Join-Path $LogDir "admin-error.log"
$FrontOut = Join-Path $LogDir "front.log"
$FrontErr = Join-Path $LogDir "front-error.log"

Write-Info "Project root: $ProjectRoot"
Write-Info "Log directory: $LogDir"

if (-not (Test-Path -LiteralPath $ConfigPath)) {
    Stop-WithError "config.ini is missing"
}

if (-not (Test-Path -LiteralPath $PythonExe)) {
    Stop-WithError "Python virtualenv is missing: .venv311\\Scripts\\python.exe"
}

$pythonVersion = & $PythonExe --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Stop-WithError "Unable to read Python version from virtualenv"
}
Write-Pass ("Python ready: {0}" -f (($pythonVersion | Out-String).Trim()))

$pyCheck = & $PythonExe -c "import flask; import pymysql; print('python imports ok')" 2>&1
if ($LASTEXITCODE -ne 0) {
    Stop-WithError ("Python dependency smoke check failed: {0}" -f (($pyCheck | Out-String).Trim()))
}
Write-Pass "Python dependency smoke check passed"

$NodeCmd = Get-CommandPath -Name "node"
if ($null -eq $NodeCmd) {
    Stop-WithError "node command not found"
}

$nodeVersion = & $NodeCmd -v 2>&1
if ($LASTEXITCODE -ne 0) {
    Stop-WithError "Unable to read Node version"
}
$nodeVersion = (($nodeVersion | Out-String).Trim())
if ($nodeVersion -match "^v16\.") {
    Write-Pass "Node ready: $nodeVersion"
} else {
    Write-Warn "Node version is not the recommended 16.x: $nodeVersion"
}

$NpmCmd = Get-CommandPath -Name "npm"
if ($null -eq $NpmCmd) {
    Stop-WithError "npm command not found"
}

$npmVersion = & $NpmCmd -v 2>&1
if ($LASTEXITCODE -ne 0) {
    Stop-WithError "Unable to read npm version"
}
$npmText = (($npmVersion | Out-String).Trim())
$npmLines = @($npmText -split "\r?\n" | Where-Object { $_.Trim() -ne "" })
$npmVersionOnly = $npmLines[-1]
if ($npmText -match "(?im)^npm warn") {
    Write-Warn "npm reports warnings in the current shell"
}
Write-Pass ("npm ready: {0}" -f $npmVersionOnly)

if (-not (Test-Path -LiteralPath $AdminPackage)) {
    Stop-WithError "Admin package.json is missing"
}

if (-not (Test-Path -LiteralPath $FrontPackage)) {
    Stop-WithError "Front package.json is missing"
}

if (-not (Test-Path -LiteralPath $AdminNodeModules)) {
    Stop-WithError "Admin node_modules is missing. Run npm install in api\\templates\\front\\admin first."
}

if (-not (Test-Path -LiteralPath $FrontNodeModules)) {
    Stop-WithError "Front node_modules is missing. Run npm install in api\\templates\\front\\front first."
}

$backendPort = Get-ListeningPortInfo -Port 8080
if ($null -eq $backendPort) {
    Start-LoggedProcess `
        -Name "Backend" `
        -FilePath $PythonExe `
        -ArgumentList @(".\run.py") `
        -WorkingDirectory $ProjectRoot `
        -StdOutPath $BackendOut `
        -StdErrPath $BackendErr
} else {
    Write-Warn ("Port 8080 already in use by PID {0} ({1}). Backend start skipped." -f $backendPort.Pid, (Get-ProcessNameSafe -ProcessId $backendPort.Pid))
}

$adminPort = Get-ListeningPortInfo -Port 8081
if ($null -eq $adminPort) {
    Start-LoggedProcess `
        -Name "Admin frontend" `
        -FilePath $NpmCmd `
        -ArgumentList @("run", "serve") `
        -WorkingDirectory $AdminDir `
        -StdOutPath $AdminOut `
        -StdErrPath $AdminErr
} else {
    Write-Warn ("Port 8081 already in use by PID {0} ({1}). Admin start skipped." -f $adminPort.Pid, (Get-ProcessNameSafe -ProcessId $adminPort.Pid))
}

$frontPort = Get-ListeningPortInfo -Port 8082
if ($null -eq $frontPort) {
    Start-LoggedProcess `
        -Name "Front frontend" `
        -FilePath $NpmCmd `
        -ArgumentList @("run", "serve") `
        -WorkingDirectory $FrontDir `
        -StdOutPath $FrontOut `
        -StdErrPath $FrontErr
} else {
    Write-Warn ("Port 8082 already in use by PID {0} ({1}). Front start skipped." -f $frontPort.Pid, (Get-ProcessNameSafe -ProcessId $frontPort.Pid))
}

Start-Sleep -Seconds 2

Write-Host ""
Write-Info "Access URLs:"
Write-Host "  Backend: http://localhost:8080"
Write-Host "  Admin:   http://localhost:8081/#/login"
Write-Host "  Front:   http://localhost:8082"
Write-Host ""
Write-Info "Logs:"
Write-Host "  $BackendOut"
Write-Host "  $BackendErr"
Write-Host "  $AdminOut"
Write-Host "  $AdminErr"
Write-Host "  $FrontOut"
Write-Host "  $FrontErr"
Write-Host ""
Write-Info "Admin login: admin / admin"
exit 0
