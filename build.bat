@echo off
REM Build script for TikTok Live Bubble Application
REM This will create a standalone .exe file

echo ===============================================
echo Building TikTok Live Bubble Application
echo ===============================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Build with PyInstaller
echo Building executable...
pyinstaller build.spec

echo ===============================================
echo Build complete!
echo Executable location: dist\TikTokLiveBubble.exe
echo ===============================================

pause
