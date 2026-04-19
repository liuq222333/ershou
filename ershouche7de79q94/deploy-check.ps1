$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $ProjectRoot

$LogDir = Join-Path $ProjectRoot "logs"
$LogFile = Join-Path $LogDir "deploy-check.log"

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
Set-Content -LiteralPath $LogFile -Value "" -Encoding UTF8

$script:HasFail = $false
$script:HasWarn = $false

function Write-Line {
    param(
        [string]$Text
    )

    Write-Host $Text
    Add-Content -LiteralPath $LogFile -Value $Text -Encoding UTF8
}

function Write-Status {
    param(
        [ValidateSet("PASS", "WARN", "FAIL", "INFO")]
        [string]$Level,
        [string]$Message
    )

    if ($Level -eq "WARN") { $script:HasWarn = $true }
    if ($Level -eq "FAIL") { $script:HasFail = $true }

    Write-Line ("[{0}] {1}" -f $Level, $Message)
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

$PythonExe = Join-Path $ProjectRoot ".venv311\Scripts\python.exe"
$ConfigPath = Join-Path $ProjectRoot "config.ini"
$AdminDir = Join-Path $ProjectRoot "api\templates\front\admin"
$FrontDir = Join-Path $ProjectRoot "api\templates\front\front"
$AdminPackage = Join-Path $AdminDir "package.json"
$FrontPackage = Join-Path $FrontDir "package.json"
$AdminNodeModules = Join-Path $AdminDir "node_modules"
$FrontNodeModules = Join-Path $FrontDir "node_modules"

Write-Status INFO "Project root: $ProjectRoot"
Write-Status INFO "Check log: $LogFile"
Write-Line ""

if (Test-Path -LiteralPath $ConfigPath) {
    Write-Status PASS "config.ini found"
    $configRaw = Get-Content -LiteralPath $ConfigPath -Raw
    foreach ($pattern in @("(?m)^\[sql\]\s*$", "(?m)^host\s*=", "(?m)^port\s*=", "(?m)^user\s*=", "(?m)^db\s*=")) {
        if ($configRaw -match $pattern) {
            Write-Status PASS "config.ini contains required setting: $pattern"
        } else {
            Write-Status FAIL "config.ini missing required setting: $pattern"
        }
    }
} else {
    Write-Status FAIL "config.ini missing"
}

if (Test-Path -LiteralPath $PythonExe) {
    Write-Status PASS "Python virtualenv found: $PythonExe"
    $pythonVersion = & $PythonExe --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Status PASS ("Python version: {0}" -f (($pythonVersion | Out-String).Trim()))
    } else {
        Write-Status FAIL "Unable to read Python version from virtualenv"
    }

    $pyCheck = & $PythonExe -c "import flask; import pymysql; print('python imports ok')" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Status PASS "Python dependency smoke check passed"
    } else {
        Write-Status FAIL ("Python dependency smoke check failed: {0}" -f (($pyCheck | Out-String).Trim()))
    }
} else {
    Write-Status FAIL "Python virtualenv missing: .venv311\\Scripts\\python.exe"
}

if (Test-Path -LiteralPath $AdminPackage) {
    Write-Status PASS "Admin package.json found"
} else {
    Write-Status FAIL "Admin package.json missing"
}

if (Test-Path -LiteralPath $FrontPackage) {
    Write-Status PASS "Front package.json found"
} else {
    Write-Status FAIL "Front package.json missing"
}

if (Test-Path -LiteralPath $AdminNodeModules) {
    Write-Status PASS "Admin node_modules found"
} else {
    Write-Status FAIL "Admin node_modules missing"
}

if (Test-Path -LiteralPath $FrontNodeModules) {
    Write-Status PASS "Front node_modules found"
} else {
    Write-Status FAIL "Front node_modules missing"
}

$NodeCmd = Get-CommandPath -Name "node"
if ($null -eq $NodeCmd) {
    Write-Status FAIL "node command not found"
} else {
    $nodeVersion = & $NodeCmd -v 2>&1
    if ($LASTEXITCODE -eq 0) {
        $nodeVersion = (($nodeVersion | Out-String).Trim())
        if ($nodeVersion -match "^v16\.") {
            Write-Status PASS "Node version is compatible: $nodeVersion"
        } else {
            Write-Status WARN "Node version is not the recommended 16.x: $nodeVersion"
        }
    } else {
        Write-Status FAIL "Unable to read Node version"
    }
}

$NpmCmd = Get-CommandPath -Name "npm"
if ($null -eq $NpmCmd) {
    Write-Status FAIL "npm command not found"
} else {
    $npmVersion = & $NpmCmd -v 2>&1
    if ($LASTEXITCODE -eq 0) {
        $npmText = (($npmVersion | Out-String).Trim())
        $npmLines = @($npmText -split "\r?\n" | Where-Object { $_.Trim() -ne "" })
        $npmVersionOnly = $npmLines[-1]
        if ($npmText -match "(?im)^npm warn") {
            Write-Status WARN "npm reports warnings in the current shell"
            Write-Status PASS ("npm version: {0}" -f $npmVersionOnly)
        } else {
            Write-Status PASS ("npm version: {0}" -f $npmVersionOnly)
        }
    } else {
        Write-Status FAIL "Unable to read npm version"
    }
}

foreach ($port in @(8080, 8081, 8082)) {
    $portInfo = Get-ListeningPortInfo -Port $port
    if ($null -eq $portInfo) {
        Write-Status PASS "Port $port is free"
    } else {
        $processName = Get-ProcessNameSafe -ProcessId $portInfo.Pid
        Write-Status WARN "Port $port is already in use by PID $($portInfo.Pid) ($processName)"
    }
}

Write-Line ""
if ($script:HasFail) {
    Write-Status FAIL "Environment check completed with failures"
    exit 1
}

if ($script:HasWarn) {
    Write-Status WARN "Environment check completed with warnings"
    exit 0
}

Write-Status PASS "Environment check completed successfully"
exit 0
