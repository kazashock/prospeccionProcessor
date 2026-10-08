# Arma LeadNormalizer_Portable.zip: codigo + Python embebido con dependencias
# ya instaladas. La maquina destino no necesita tener Python instalado.
#
# Uso: powershell -ExecutionPolicy Bypass -File scripts\build_portable_zip.ps1

$ErrorActionPreference = "Stop"

$ROOT = Split-Path -Parent $PSScriptRoot
$BUILD_DIR = Join-Path $ROOT "build"
$RUNTIME_DIR = Join-Path $BUILD_DIR "python"
$STAGING_DIR = Join-Path $BUILD_DIR "staging"
$DIST_DIR = Join-Path $ROOT "dist"
$ZIP_PATH = Join-Path $DIST_DIR "LeadNormalizer_Portable.zip"

$PYTHON_VERSION = "3.12.10"
$EMBED_URL = "https://www.python.org/ftp/python/$PYTHON_VERSION/python-$PYTHON_VERSION-embed-amd64.zip"
$GETPIP_URL = "https://bootstrap.pypa.io/get-pip.py"

New-Item -ItemType Directory -Force -Path $BUILD_DIR | Out-Null

# 1. Runtime embebido (se cachea en build/python; se reusa si ya existe)
if (-not (Test-Path (Join-Path $RUNTIME_DIR "python.exe"))) {
    Write-Host "Descargando Python embebido $PYTHON_VERSION..."
    $embedZip = Join-Path $BUILD_DIR "python-embed.zip"
    Invoke-WebRequest -Uri $EMBED_URL -OutFile $embedZip
    if (Test-Path $RUNTIME_DIR) { Remove-Item -Recurse -Force $RUNTIME_DIR }
    Expand-Archive -Path $embedZip -DestinationPath $RUNTIME_DIR -Force

    $pthFile = Get-ChildItem $RUNTIME_DIR -Filter "python3*._pth" | Select-Object -First 1
    @"
python312.zip
.
Lib\site-packages
import site
"@ | Set-Content -Path $pthFile.FullName -Encoding ascii

    Write-Host "Instalando pip..."
    $getPip = Join-Path $BUILD_DIR "get-pip.py"
    Invoke-WebRequest -Uri $GETPIP_URL -OutFile $getPip
    & "$RUNTIME_DIR\python.exe" $getPip --no-warn-script-location
}

# 2. Dependencias del proyecto dentro del runtime embebido
Write-Host "Instalando dependencias..."
& "$RUNTIME_DIR\python.exe" -m pip install --no-warn-script-location -r (Join-Path $ROOT "requirements.txt")

# Recortar peso: cache de bytecode y carpetas de tests de las dependencias
Write-Host "Optimizando tamano del runtime..."
$sitePackages = Join-Path $RUNTIME_DIR "Lib\site-packages"
Get-ChildItem -Path $sitePackages -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue |
    ForEach-Object { Remove-Item -Recurse -Force $_.FullName -ErrorAction SilentlyContinue }
Get-ChildItem -Path $sitePackages -Recurse -Directory -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -in @("tests", "test") } |
    ForEach-Object { if (Test-Path $_.FullName) { Remove-Item -Recurse -Force $_.FullName -ErrorAction SilentlyContinue } }

# 3. Staging: copiar codigo fuente (sin entornos de desarrollo ni cache)
if (Test-Path $STAGING_DIR) { Remove-Item -Recurse -Force $STAGING_DIR }
New-Item -ItemType Directory -Force -Path $STAGING_DIR | Out-Null

$incluir = @("app.py", "desktop_app.py", "core", "config", "data", "scripts", "outputs", "README.md", "requirements.txt", ".streamlit")
foreach ($item in $incluir) {
    $origen = Join-Path $ROOT $item
    if (Test-Path $origen) {
        Copy-Item -Path $origen -Destination (Join-Path $STAGING_DIR $item) -Recurse -Force
    }
}

# Limpiar __pycache__ y archivos .xlsx generados que no deben ir versionados
Get-ChildItem -Path $STAGING_DIR -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Path (Join-Path $STAGING_DIR "outputs") -Filter "*.xlsx" -ErrorAction SilentlyContinue | Remove-Item -Force

# 4. Runtime embebido con dependencias
Copy-Item -Path $RUNTIME_DIR -Destination (Join-Path $STAGING_DIR "python") -Recurse -Force

# 5. Launcher para el usuario final (sin consola, sin instalar nada)
@"
@echo off
cd /d "%~dp0"
start "" "python\pythonw.exe" desktop_app.py
"@ | Set-Content -Path (Join-Path $STAGING_DIR "LeadNormalizer.bat") -Encoding ascii

# 6. Zip final
New-Item -ItemType Directory -Force -Path $DIST_DIR | Out-Null
if (Test-Path $ZIP_PATH) { Remove-Item -Force $ZIP_PATH }
Compress-Archive -Path (Join-Path $STAGING_DIR "*") -DestinationPath $ZIP_PATH -CompressionLevel Optimal

$tamanoMB = [math]::Round((Get-Item $ZIP_PATH).Length / 1MB, 1)

# 7. staging es descartable (duplica build/python + el codigo ya empaquetado)
Remove-Item -Recurse -Force $STAGING_DIR

Write-Host "Listo: $ZIP_PATH ($tamanoMB MB)"
