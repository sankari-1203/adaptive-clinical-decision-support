@echo off
title Adaptive Clinical Decision Support System Launcher
echo ======================================================================
echo    Starting Adaptive Clinical Decision Support System (CDSS)
echo    Backend: http://localhost:8000
echo    Frontend: http://localhost:3000
echo ======================================================================

set "PROJECT_DIR=C:\ADAPTIVE CLINICAL DECISION"
set "PYTHON_EXE=d:\project 1\.venv\Scripts\python.exe"

if not exist "%PYTHON_EXE%" (
    set "PYTHON_EXE=python"
)

echo Starting FastAPI Backend...
start "CDSS Backend [Port 8000]" cmd /k "cd /d \"%PROJECT_DIR%\backend\" && \"%PYTHON_EXE%\" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

echo Starting React Frontend...
start "CDSS Frontend [Port 3000]" cmd /k "cd /d \"%PROJECT_DIR%\frontend\" && npm run dev"

echo Waiting 3 seconds for services to initialize...
timeout /t 3 /nobreak >nul

echo Opening Clinical Decision Support Dashboard at http://localhost:3000 ...
start http://localhost:3000

echo Done! Both Backend and Frontend are running.
