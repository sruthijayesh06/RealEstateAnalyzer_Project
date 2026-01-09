@echo off
REM Frontend Setup Script for Windows
REM This script installs all required dependencies for the frontend

echo.
echo ================================
echo Real Estate Analyzer - Frontend Setup
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed. Please install Python 3.11+
    pause
    exit /b 1
)

echo [OK] Python found:
python --version
echo.

REM Upgrade pip
echo Installing/Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install Flask
echo Installing Flask...
pip install Flask>=3.0.0
echo.

REM Install other dependencies
echo Installing other dependencies from requirements.txt...
pip install -r requirements.txt
echo.

echo.
echo ================================
echo [OK] Frontend Setup Complete!
echo ================================
echo.
echo To start the application, run:
echo   python app.py
echo.
echo Then open your browser to:
echo   http://localhost:5000
echo.
pause
