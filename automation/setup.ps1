$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$venvPython = Join-Path $root '.venv\Scripts\python.exe'

if (-not (Test-Path -LiteralPath $venvPython)) {
    python -m venv (Join-Path $root '.venv')
}

& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r (Join-Path $PSScriptRoot 'requirements.txt')
Write-Host '依赖已安装到 .venv。'
