@echo off
title YouTube Downloader - One-Click Setup
color 0A

echo.
echo ====================================================
echo    __   __          _______         _          
echo    \ \ / /         ^|__   __^|       ^| ^|         
echo     \ V /___  _   _   ^| ^| _   _  ^| ^|__   ___ 
echo      ^> ^< / _ \^| ^| ^| ^|  ^| ^|^| ^| ^| ^|^| '_ \ / _ \
echo     / . \ (_) ^| ^|_^| ^|  ^| ^|^| ^|_^| ^|^| ^|_) ^|  __/
echo    /_/ \_\___/ \__,_^|  ^|_^| \__,_^|^|_.__/ \___^|
echo.                                               
echo    ____                      _                 _           
echo   ^|  _ \  _____      ___ __ ^| ^|  ___   __ _  __^| ^| ___ _ __ 
echo   ^| ^| ^| ^|/ _ \ \ /\ / / '_ \^| ^| / _ \ / _` ^|/ _` ^|/ _ \ '__^|
echo   ^| ^|_^| ^| (_) \ V  V /^| ^| ^| ^| ^|^| (_) ^| (_^| ^| (_^| ^|  __/ ^|   
echo   ^|____/ \___/ \_/\_/ ^|_^| ^|_^|_^| \___/ \__,_^|\__,_^|\___^|_^|   
echo.
echo ====================================================
echo        One-Click Setup and Launch System
echo ====================================================
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
python -m pip install customtkinter==5.2.0 pytubefix==6.0.0 Pillow requests --quiet --disable-pip-version-check
if %errorlevel% neq 0 (
    echo ❌ Package installation failed - trying alternative method...
    echo Installing packages one by one...
    python -m pip install customtkinter==5.2.0
    python -m pip install pytubefix==6.0.0  
    python -m pip install Pillow
    python -m pip install requests
    echo ✅ Packages installed using alternative method!
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