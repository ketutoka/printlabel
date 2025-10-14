@echo off
echo Setting up Print Label Backend...
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo Creating .env from example...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file with your database and email settings!
    echo.
)

echo.
echo Setup complete! 
echo.
echo To start the server, run:
echo   uvicorn main:app --reload
echo.
echo Make sure to:
echo 1. Update .env with your PostgreSQL database URL
echo 2. Update .env with your email settings for password reset
echo.
pause