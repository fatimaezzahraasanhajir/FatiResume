@echo off
echo Stopping FatiResume Application...
echo.

echo Killing processes on port 8000 (Backend)...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do (
    echo Stopping backend process %%a
    taskkill /f /pid %%a >nul 2>&1
)

echo Killing processes on port 8501 (Frontend)...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8501" ^| find "LISTENING"') do (
    echo Stopping frontend process %%a
    taskkill /f /pid %%a >nul 2>&1
)

echo.
echo FatiResume has been stopped completely!
echo.
pause
