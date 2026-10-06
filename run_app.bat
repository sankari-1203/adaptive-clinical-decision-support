@echo off
title Adaptive Clinical Decision Support System
echo ========================================================
echo Starting Adaptive Clinical Decision Support System (CDSS)
echo ========================================================
echo.

cd /d "%~dp0backend"

if exist "..\..\project 1\.venv\Scripts\python.exe" (
    set "PYTHON_EXE=..\..\project 1\.venv\Scripts\python.exe"
) else (
    set "PYTHON_EXE=python"
)

echo Using Python: %PYTHON_EXE%
echo Starting Uvicorn API on http://localhost:8000 ...
echo Clinical Dashboard will be available at http://localhost:8000/
echo Interactive Swagger Docs available at http://localhost:8000/docs
echo.

"%PYTHON_EXE%" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause
