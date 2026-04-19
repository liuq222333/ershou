@echo off
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0deploy-check.ps1"
set EXITCODE=%ERRORLEVEL%
echo.
pause
exit /b %EXITCODE%
