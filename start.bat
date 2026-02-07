@echo off
title MovieWizard Starter
setlocal

echo ==========================================
echo    🧙‍♂️ MovieWizard is starting...
echo ==========================================
echo.

:: 1. Open the UI
if exist "interface.html" (
    echo [1/2] Opening Web Interface...
    start "" "interface.html"
) else (
    echo [!] Error: interface.html not found.
)

echo.
echo ------------------------------------------
echo NEXT STEPS:
echo 1. Enter your TMDb API Key on the webpage.
echo 2. Follow the wizard to find movies.
echo ------------------------------------------
echo.
echo If you want to use the CLI Bulk Downloader:
echo   - Ensure Python is installed.
echo   - Run: pip install -r requirements.txt
echo   - Run: python smart_filter.py
echo.
echo ==========================================
pause
