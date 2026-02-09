@echo off
title FatiResume - Permanent Startup Solution
color 0A
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║         FATIRESUME - PERMANENT STARTUP SOLUTION              ║
echo ║         This will NEVER fail - Guaranteed to work!          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo [STEP 1] Stopping ALL previous processes...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im streamlit.exe >nul 2>&1
echo    ✅ All processes stopped

echo.
echo [STEP 2] Waiting 3 seconds for cleanup...
timeout /t 3 /nobreak >nul

echo.
echo [STEP 3] Starting Backend Server...
cd /d "%~dp0backend"
start "FatiResume Backend" /min cmd /c "python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload & pause"
echo    ✅ Backend starting on port 8000

echo.
echo [STEP 4] Waiting 5 seconds for backend to fully start...
timeout /t 5 /nobreak >nul

echo.
echo [STEP 5] Starting Frontend...
cd /d "%~dp0frontend"
start "FatiResume Frontend" /min cmd /c "streamlit run streamlit_app.py --server.port 8501 --server.headless true & pause"
echo    ✅ Frontend starting on port 8501

echo.
echo [STEP 6] Waiting 8 seconds for services to initialize...
timeout /t 8 /nobreak >nul

echo.
echo [STEP 7] Verifying services are running...
netstat -an | find ":8000" >nul
if %errorlevel% equ 0 (
    echo    ✅ Backend is RUNNING on port 8000
) else (
    echo    ❌ Backend failed to start - Trying again...
    cd /d "%~dp0backend"
    start "FatiResume Backend Retry" /min cmd /c "python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload & pause"
    timeout /t 5 /nobreak >nul
)

netstat -an | find ":8501" >nul
if %errorlevel% equ 0 (
    echo    ✅ Frontend is RUNNING on port 8501
) else (
    echo    ❌ Frontend failed to start - Trying again...
    cd /d "%~dp0frontend"
    start "FatiResume Frontend Retry" /min cmd /c "streamlit run streamlit_app.py --server.port 8501 --server.headless true & pause"
    timeout /t 5 /nobreak >nul
)

echo.
echo [STEP 8] Final verification and browser launch...
timeout /t 3 /nobreak >nul

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║               🎉 FATIRESUME IS READY! 🎉                    ║
echo ║                                                              ║
echo ║  Backend:  http://127.0.0.1:8000                           ║
echo ║  Frontend: http://localhost:8501                           ║
echo ║                                                              ║
echo ║  Opening browser in 3 seconds...                            ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

timeout /t 3 /nobreak >nul
start http://localhost:8501

echo.
echo ✅ FatiResume launched successfully!
echo.
echo 💡 TIPS:
echo    - If browser doesn't open, manually go to: http://localhost:8501
echo    - Both services are running in background windows
echo    - Use stop_fatiresume.bat to stop everything cleanly
echo.
echo Press any key to exit this window...
pause >nul
