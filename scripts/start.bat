@echo off
cd %~dp0\..
cls
echo ==========================================
echo           MovieWizard Launcher
echo ==========================================
echo.
echo [1] Launch Web Interface (Local Server)
echo [2] Launch Deep Search CLI (Terminal)
echo.
set /p choice="Select an option (1-2): "

if "%choice%"=="1" (
    echo Starting local server at http://localhost:8000...
    start "" "http://localhost:8000/interface.html"
    python -m http.server 8000
) else if "%choice%"=="2" (
    cls
    echo Starting MovieWizard CLI...
    python -m src.app.cli
    pause
) else (
    echo Invalid choice.
    pause
)
