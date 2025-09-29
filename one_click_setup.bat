@echo off
title YouTube Downloader - One-Click Setup
color 0A

echo.
echo ██╗   ██╗ ██████╗ ██╗   ██╗████████╗██╗   ██╗██████╗ ███████╗
echo ╚██╗ ██╔╝██╔═══██╗██║   ██║╚══██╔══╝██║   ██║██╔══██╗██╔════╝
echo  ╚████╔╝ ██║   ██║██║   ██║   ██║   ██║   ██║██████╔╝█████╗  
echo   ╚██╔╝  ██║   ██║██║   ██║   ██║   ██║   ██║██╔══██╗██╔══╝  
echo    ██║   ╚██████╔╝╚██████╔╝   ██║   ╚██████╔╝██████╔╝███████╗
echo    ╚═╝    ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝ ╚═════╝ ╚══════╝
echo.
echo ████████╗ ██████╗ ██╗    ██╗███╗   ██╗██╗      ██████╗  █████╗ ██████╗ ███████╗██████╗ 
echo ╚══██╔══╝██╔═══██╗██║    ██║████╗  ██║██║     ██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
echo    ██║   ██║   ██║██║ █╗ ██║██╔██╗ ██║██║     ██║   ██║███████║██║  ██║█████╗  ██████╔╝
echo    ██║   ██║   ██║██║███╗██║██║╚██╗██║██║     ██║   ██║██╔══██║██║  ██║██╔══╝  ██╔══██╗
echo    ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║███████╗╚██████╔╝██║  ██║██████╔╝███████╗██║  ██║
echo    ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
echo.
echo ========================================
echo   One-Click Setup and Launch
echo ========================================
echo.

:: Step 1: Check Python
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found - Opening installation guide...
    echo.
    echo Please:
    echo 1. Install Python from python.org
    echo 2. Check "Add Python to PATH" 
    echo 3. Restart this script
    echo.
    start https://www.python.org/downloads/
    pause
    exit /b 1
) else (
    python --version
    echo ✅ Python is ready!
)

echo.
:: Step 2: Install packages  
echo [2/4] Installing required packages...
pip install customtkinter==5.2.0 pytubefix==6.0.0 Pillow requests --quiet --disable-pip-version-check
if %errorlevel% neq 0 (
    echo ❌ Package installation failed
    pause
    exit /b 1
) else (
    echo ✅ All packages installed!
)

echo.
:: Step 3: Setup FFmpeg
echo [3/4] Setting up FFmpeg...
if exist "ffmpeg\ffmpeg.exe" (
    echo ✅ FFmpeg already available
) else (
    echo Setting up FFmpeg...
    python setup_ffmpeg.py >nul 2>&1
    if exist "ffmpeg\ffmpeg.exe" (
        echo ✅ FFmpeg setup complete!
    ) else (
        echo ⚠️ FFmpeg setup failed - continuing without it
    )
)

echo.
:: Step 4: Launch application
echo [4/4] Launching YouTube Downloader...
echo.
echo ✅ SETUP COMPLETE - Starting application...
echo.
timeout /t 2 /nobreak >nul

python main.py

echo.
if %errorlevel% neq 0 (
    echo ❌ Application encountered an error
    echo.
    echo Troubleshooting:
    echo - Run check_dependencies.bat to diagnose issues
    echo - Run setup.bat for detailed setup
    echo.
) else (
    echo ✅ Application closed normally
)

pause