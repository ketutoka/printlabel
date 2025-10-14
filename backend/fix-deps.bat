@echo off
echo Fixing dependencies...
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Uninstall problematic packages
echo Uninstalling existing packages...
pip uninstall fastapi uvicorn pydantic -y

REM Install fixed versions
echo Installing fixed dependencies...
pip install -r requirements.txt

echo.
echo ✅ Dependencies fixed!
echo.
echo Now you can run:
echo   python start.py
echo.
pause