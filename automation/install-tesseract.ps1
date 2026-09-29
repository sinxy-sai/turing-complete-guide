$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$toolsRoot = Join-Path $root '.tools'
$installRoot = Join-Path $toolsRoot 'tesseract'
$version = '5.4.0.20240606'
$installer = Join-Path $toolsRoot "tesseract-ocr-w64-setup-$version.exe"
$downloadUrl = "https://github.com/UB-Mannheim/tesseract/releases/download/v$version/tesseract-ocr-w64-setup-$version.exe"

New-Item -ItemType Directory -Force -Path $toolsRoot | Out-Null

if (-not (Test-Path -LiteralPath (Join-Path $installRoot 'tesseract.exe'))) {
    if (-not (Test-Path -LiteralPath $installer)) {
        Invoke-WebRequest -Uri $downloadUrl -OutFile $installer
    }
    $process = Start-Process -FilePath $installer -ArgumentList @('/S', "/D=$installRoot") -Wait -PassThru
    if ($process.ExitCode -ne 0) {
        throw "Tesseract installer failed with exit code $($process.ExitCode)."
    }
}

$tessData = Join-Path $installRoot 'tessdata'
$chiSim = Join-Path $tessData 'chi_sim.traineddata'
if (-not (Test-Path -LiteralPath $chiSim)) {
    New-Item -ItemType Directory -Force -Path $tessData | Out-Null
    Invoke-WebRequest -Uri 'https://github.com/tesseract-ocr/tessdata_fast/raw/main/chi_sim.traineddata' -OutFile $chiSim
}

$tesseract = Join-Path $installRoot 'tesseract.exe'
if (-not (Test-Path -LiteralPath $tesseract)) {
    throw "Tesseract was not found after installation: $tesseract"
}

Remove-Item -LiteralPath $installer -Force -ErrorAction SilentlyContinue
Write-Host "Tesseract installed in $installRoot"
