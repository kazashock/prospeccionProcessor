@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\pythonw.exe" (
    echo No se encontro el entorno virtual. Corre primero install.bat
    pause
    exit /b 1
)
start "" ".venv\Scripts\pythonw.exe" desktop_app.py
