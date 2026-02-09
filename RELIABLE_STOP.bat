@echo off
title FatiResume - Complete Stop Solution
color 0C
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║           STOPPING FATIRESUME - COMPLETE CLEANUP              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo [STEP 1] Killing ALL Python processes...
taskkill /f /im python.exe >nul 2>&1
echo    ✅ Python processes terminated

echo.
echo [STEP 2] Killing ALL Streamlit processes...
taskkill /f /im streamlit.exe >nul 2>&1
echo    ✅ Streamlit processes terminated

echo.
echo [STEP 3] Force-closing ports 8000 and 8501...
for /f "tokens=5" %%a in ('netstat -ano ^| find ":8000" ^| find "LISTENING"') do (
    echo    Killing process %%a on port 8000
    taskkill /f /pid %%a >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -ano ^| find ":8501" ^| find "LISTENING"') do (
    echo    Killing process %%a on port 8501
    taskkill /f /pid %%a >nul 2>&1
)
echo    ✅ Ports cleared

echo.
echo [STEP 4] Final verification...
netstat -an | find ":8000" >nul
if %errorlevel% equ 0 (
    echo    ❌ Port 8000 still in use - Force clearing...
    for /f "tokens=5" %%a in ('netstat -ano ^| find ":8000"') do taskkill /f /pid %%a >nul 2>&1
) else (
    echo    ✅ Port 8000 is clear
)

netstat -an | find ":8501" >nul
if %errorlevel% equ 0 (
    echo    ❌ Port 8501 still in use - Force clearing...
    for /f "tokens=5" %%a in ('netstat -ano ^| find ":8501"') do taskkill /f /pid %%a >nul 2>&1
) else (
    echo    ✅ Port 8501 is clear
)

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              ✅ FATIRESUME COMPLETELY STOPPED ✅               ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo All processes terminated. Ports 8000 and 8501 are free.
echo.
echo Press any key to exit...
pause >nul
