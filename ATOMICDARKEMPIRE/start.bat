@echo off
echo.
echo ========================================
echo   DARK EMPIRE BOT LAUNCHER
echo ========================================
echo.

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found!
    echo.
    echo Please create a .env file with:
    echo DISCORD_TOKEN=your_token_here
    echo OWNER_ID=your_user_id_here
    echo PREFIX=!
    echo.
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [1/3] Checking dependencies...
pip install -r requirements.txt --quiet

echo [2/3] Creating data directory...
if not exist data mkdir data

echo [3/3] Starting Dark Empire Bot...
echo.
echo ========================================
echo   BOT IS STARTING...
echo   Press Ctrl+C to stop
echo ========================================
echo.

python bot.py

pause
