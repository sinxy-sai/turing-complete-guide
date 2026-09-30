param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Arguments
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$venvPython = Join-Path $root '.venv\Scripts\python.exe'

if (-not (Test-Path -LiteralPath $venvPython)) {
    & (Join-Path $PSScriptRoot 'setup.ps1')
}

Push-Location $PSScriptRoot
try {
    & $venvPython -m binary_speed @Arguments
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}
finally {
    Pop-Location
}
