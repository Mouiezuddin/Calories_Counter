@echo off
REM NutriCore Setup Script for Windows

echo.
echo 🍎 NutriCore Calorie Tracker - Setup
echo ====================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH. Please install Python 3.8+ first.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ Python found: %PYTHON_VERSION%

REM Create virtual environment
echo.
echo 📦 Creating virtual environment...
python -m venv venv

if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

echo ✓ Virtual environment created

REM Activate virtual environment
echo.
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

echo ✓ Virtual environment activated

REM Install dependencies
echo.
echo 📥 Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✓ Dependencies installed

REM Create .env file if it doesn't exist
echo.
if not exist .env (
    echo 📝 Creating .env file from template...
    copy .env.example .env
    echo ✓ .env file created (update with your settings if needed)
) else (
    echo ✓ .env file already exists
)

echo.
echo ✅ Setup complete!
echo.
echo To start the app, run:
echo   venv\Scripts\activate.bat
echo   python app.py
echo.
echo Then visit: http://localhost:5000
echo.
pause
