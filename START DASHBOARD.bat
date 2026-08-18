@echo off
echo.
echo  ==========================================
echo   VIP Audit Dashboard - Starting Server...
echo  ==========================================
echo.
echo  Opening dashboard at http://localhost:8080
echo.
start "" "http://localhost:8080"
node "%~dp0serve.js"
pause
