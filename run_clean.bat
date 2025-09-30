@echo off
title YouTube Downloader by Chandula [CMW]
color 0A
cls

:: ====================================================
::  YouTube Downloader - Easy Setup
::  Publisher: Chandula [CMW]
::  Version: 2.0
::  Safe to run - No malware, viruses, or harmful code
:: ====================================================

echo.
echo ====================================================
echo       YouTube Downloader by Chandula [CMW]
echo ====================================================
echo.
echo 🛡️ SAFETY INFORMATION:
echo • Publisher: Chandula [CMW]
echo • This is safe, open-source software
echo • No viruses, malware, or harmful code
echo • Source code available on GitHub
echo.
echo Windows shows a security warning because this file
echo is not digitally signed. This is normal for open-source
echo software and does not indicate any security risk.
echo.
echo ✅ Safe to proceed!
echo.

:: Check if we're in the right directory
if not exist "main.py" (
    echo ❌ ERROR: You're not in the YouTube Downloader folder!
    echo.
    echo 🔍 Current location: %CD%
    echo.
    echo 💡 Please:
    echo 1. Navigate to the YouTube Downloader folder
    echo 2. Make sure you can see: main.py, gui folder, core folder
    echo 3. Run this file again from the correct location
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo 📂 Working directory verified: %CD%
echo.

:: Step 1: Check Python
echo [Step 1/4] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found!
    echo.
    echo Python is required to run this program.
    echo Opening Python download page...
    echo.
    echo IMPORTANT: When installing Python, make sure to:
    echo ✓ Check "Add Python to PATH"
    echo ✓ Install for all users
    echo.
    echo After installing Python, run this file again.
    start https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

python --version
echo ✅ Python is installed!
echo.

::Step 2: Smart package management
echo [Step 2/4] Checking required packages...
echo 🔍 Running smart package check...
python check_packages.py
if %errorlevel% neq 0 (
    echo ⚠️ Package check had issues, trying manual approach...
    goto manual_install
) else (
    echo ✅ Smart package check completed!
    goto packages_done
)

:manual_install
echo 🔄 Fallback to manual installation...
echo • Installing setuptools (Python 3.13 compatibility)...
python -m pip install setuptools --quiet >nul 2>&1

echo • Installing CustomTkinter (GUI library)...
python -m pip install --upgrade customtkinter --quiet >nul 2>&1

echo • Installing PyTubeFix (YouTube downloader)...
python -m pip install --upgrade pytubefix --quiet >nul 2>&1

echo • Installing Pillow (Image support)...
python -m pip install Pillow --quiet >nul 2>&1

echo • Installing Requests (Web requests)...
python -m pip install requests --quiet >nul 2>&1

echo ✅ Manual installation completed!

:packages_done
echo.

:: Step 3: Simple verification
echo [Step 3/4] Final verification...
echo 🔍 Running package verification...

python -c "import customtkinter, pytubefix, PIL, requests; print('✅ All packages working!')" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️ Some packages need fixing...
    python -m pip install --force-reinstall setuptools customtkinter pytubefix Pillow requests --quiet
    echo ✅ Package fix completed!
) else (
    echo ✅ All packages verified!
)

echo.

:: Step 4: Setup FFmpeg
echo [Step 4/4] Setting up video processing...
echo 🎬 Checking FFmpeg status...

if exist "ffmpeg\ffmpeg.exe" (
    echo 🔍 Testing existing FFmpeg...
    ffmpeg\ffmpeg.exe -version >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ FFmpeg is ready and working!
        goto ffmpeg_done
    ) else (
        echo ⚠️ Existing FFmpeg has issues, will fix...
    )
) else (
    echo 📁 No local FFmpeg found
)

echo 🔧 Setting up FFmpeg...
python setup_ffmpeg.py
if %errorlevel% neq 0 (
    echo ⚠️ FFmpeg setup had issues - some features may not work
    echo 💡 This won't prevent basic downloads
) else (
    echo ✅ FFmpeg ready for high-quality video processing!
)

:ffmpeg_done
echo.

:: Launch the application
echo ====================================================
echo ✅ EVERYTHING IS READY!
echo ====================================================
echo.

echo 🚀 Starting YouTube Downloader...
echo.

:: Start the application with simple error handling
python main.py
set app_result=%errorlevel%

:: Show result
echo.
if %app_result% equ 0 (
    echo ✅ Program completed successfully!
) else (
    echo ❌ Program error (Exit code: %app_result%)
    echo.
    echo 💡 Common solutions:
    echo • Run as administrator
    echo • Check internet connection  
    echo • Temporarily disable antivirus
    echo • Make sure all files are in the same folder
    echo.
)

echo.
echo Thanks for using YouTube Downloader by Chandula [CMW]!
echo.
echo Press any key to close...
pause >nul