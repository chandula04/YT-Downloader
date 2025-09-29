@echo off
title YouTube Downloader
echo ========================================
echo    Starting YouTube Downloader...
echo ========================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please run setup.bat first to install Python and dependencies.
    echo.
    pause
    exit /b 1
)

:: Check if required packages are installed
echo Checking required packages...

python -c "import customtkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: customtkinter not installed!
    echo Running setup script...
    call setup.bat
    goto end
)

python -c "import pytubefix" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pytubefix not installed!
    echo Running setup script...
    call setup.bat
    goto end
)

python -c "from PIL import Image" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Pillow not installed!
    echo Running setup script...
    call setup.bat
    goto end
)

echo All dependencies are available.
echo.

REM Check if FFmpeg exists locally
if exist "ffmpeg\ffmpeg.exe" (
    echo ✅ FFmpeg found: Local installation ready
) else (
    echo ⚠️ FFmpeg not found. Setting up...
    python setup_ffmpeg.py
    if errorlevel 1 (
        echo ❌ Failed to setup FFmpeg
        pause
        exit /b 1
    )
    echo ✅ FFmpeg setup completed!
    echo.
)

echo 🚀 Starting YouTube Downloader...
echo.
python main.py

:end
REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ❌ Application ended with an error
    pause
) else (
    echo.
    echo ✅ Application closed successfully
)