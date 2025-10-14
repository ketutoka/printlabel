@echo off
echo Starting Print Label Backend Server...
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

echo Starting server on port 8002...
echo Server will be available at: http://localhost:8002
echo API docs will be available at: http://localhost:8002/docs
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn main:app --reload --port 8002 --host 0.0.0.0