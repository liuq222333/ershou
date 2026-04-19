@echo off
setlocal

set "NODE_HOME=%LOCALAPPDATA%\nvm\v16.20.2"
if not exist "%NODE_HOME%\node.exe" (
  echo [ERROR] Node 16.20.2 not found at: %NODE_HOME%
  echo Please install it first with nvm.
  exit /b 1
)

"%NODE_HOME%\node.exe" "%NODE_HOME%\node_modules\npm\bin\npm-cli.js" run build

endlocal
