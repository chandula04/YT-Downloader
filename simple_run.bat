@echo off
title Simple YouTube Downloader Setup
color 0A
cls

:: Force window to stay open no matter what happens
if "%1" neq "stay_open" (
    call "%~f0" stay_open
    echo.
    echo ==========================================
    echo      SETUP FINISHED - READING RESULTS
    echo ==========================================
    echo.
    echo The setup process completed.
    echo This window stays open so you can see any errors.
    echo.
    echo Press any key to close...
    pause >nul
    exit /b
)

echo ==========================================
echo   YouTube Downloader Simple Setup
echo ==========================================
echo.

:: Step 1: Basic checks
echo [1/4] Basic environment check...
if not exist "main.py" (
    echo ❌ main.py not found in current directory!
    echo Current directory: %CD%
    echo Please run this from the YouTube Downloader folder.
    exit /b 1
)
echo ✅ main.py found

:: Step 2: Python check
echo.
echo [2/4] Python check...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Install Python and add to PATH.
    exit /b 1
)
python --version
echo ✅ Python working

:: Step 3: Package check and install
echo.
echo [3/4] Package installation...
echo Installing required packages...
python -m pip install setuptools customtkinter pytubefix Pillow requests --quiet
echo ✅ Package installation completed

:: Step 4: Launch application
echo.
echo [4/4] Launching YouTube Downloader...
echo.
echo Starting main.py...
echo ==========================================

python main.py
set app_result=%errorlevel%

echo ==========================================
echo Application finished with code: %app_result%
echo.

if %app_result% equ 0 (
    echo ✅ Application ran successfully!
) else (
    echo ❌ Application failed with error code %app_result%
    echo.
    echo Try these solutions:
    echo • Run as administrator
    echo • Check if antivirus is blocking
    echo • Make sure all files are in same folder
)

echo.
echo Setup completed!
exit /b %app_result%