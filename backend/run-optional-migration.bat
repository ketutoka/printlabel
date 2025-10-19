@echo off
echo ====================================================
echo Running Migration: Make Recipient Fields Optional
echo ====================================================
echo.

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

echo Running migration script...
python migrate_optional_fields.py

echo.
echo ====================================================
echo Migration completed. Check output above for status.
echo ====================================================
pause