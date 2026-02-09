@echo off
echo Starting FatiResume Application...
echo.

echo Killing any existing processes on ports 8000 and 8501...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do (
    echo Killing process %%a on port 8000
    taskkill /f /pid %%a >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8501" ^| find "LISTENING"') do (
    echo Killing process %%a on port 8501
    taskkill /f /pid %%a >nul 2>&1
)

echo.
echo Starting Backend Server...
cd /d "%~dp0backend"
start "FatiResume Backend" cmd /k "python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo.
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo Starting Frontend...
cd /d "%~dp0frontend"
start "FatiResume Frontend" cmd /k "streamlit run streamlit_app.py --server.port 8501"

echo.
echo ========================================
echo   FatiResume is starting up...
echo   Backend: http://127.0.0.1:8000
echo   Frontend: http://localhost:8501
echo ========================================
echo.
echo Please wait 10 seconds for services to fully start...
echo The app will open automatically in your browser.
echo.

timeout /t 10 /nobreak >nul

echo.
echo Opening FatiResume in your browser...
start http://localhost:8501

echo.
echo FatiResume is ready! 🎉
echo.
echo Press any key to exit this window (services will continue running)...
pause >nul
