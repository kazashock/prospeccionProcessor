@echo off
setlocal
cd /d "%~dp0"

python --version >nul 2>nul
if errorlevel 1 (
    echo Python no esta instalado o no esta en el PATH.
    echo Instalalo desde https://www.python.org/downloads/ ^(tildando "Add to PATH"^) y volve a correr este script.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creando entorno virtual en .venv ...
    python -m venv .venv
)

echo Instalando dependencias...
".venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
".venv\Scripts\python.exe" -m pip install -r requirements-dev.txt --quiet
if errorlevel 1 (
    echo Fallo la instalacion de dependencias.
    pause
    exit /b 1
)

echo Generando datos de ejemplo...
".venv\Scripts\python.exe" scripts\generate_sample_data.py

echo.
echo Listo. Para abrir la app: LeadNormalizer.bat
echo Para correr los tests: .venv\Scripts\python.exe -m pytest
pause
