@echo off
echo ========================================================
echo   Running EShop API Automated Tests for Member M4
echo ========================================================
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_tests.ps1"
echo.
echo ========================================================
echo   Execution Finished. Check report/newman_report.html
echo ========================================================
pause
