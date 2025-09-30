@echo off
title YouTube Downloader
color 0A
cls

echo.
echo ====================================================
echo          YouTube Downloader - Easy Setup
echo ====================================================
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

:: Step 3: Final verification
echo [Step 3/4] Final verification...
echo 🔍 Running comprehensive package test...

:: Test all packages together
python -c "
try:
    import customtkinter as ctk
    import pytubefix
    import PIL
    import requests
    print('✅ All libraries verified and ready!')
    print('   • CustomTkinter: ' + ctk.__version__)
    print('   • PyTubeFix: Working')
    print('   • Pillow: Working') 
    print('   • Requests: Working')
except ImportError as e:
    print('❌ Import error:', str(e))
    exit(1)
" 2>&1

if %errorlevel% neq 0 (
    echo.
    echo ⚠️ Some packages failed verification
    echo 🔄 Attempting emergency reinstall...
    echo.
    
    :: Emergency reinstall of failed packages
    python -m pip install --force-reinstall setuptools customtkinter pytubefix Pillow requests --quiet
    
    echo 🔍 Testing again...
    python -c "import customtkinter, pytubefix, PIL, requests; print('✅ Emergency fix successful!')" 2>nul
    if %errorlevel% neq 0 (
        echo ❌ Packages still have issues - continuing anyway
        echo 💡 Some features might not work properly
    )
)

echo.

:: Step 4: Setup FFmpeg with enhanced compatibility
echo [Step 4/4] Setting up video processing...
echo 🎬 Checking FFmpeg status...

:: Check if FFmpeg already exists and works
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

:: All ready - launch the program
echo ====================================================
echo ✅ EVERYTHING IS READY!
echo ====================================================
echo.
echo 🚀 Starting YouTube Downloader...
echo.

timeout /t 2 /nobreak >nul
python main.py

:: Handle exit
echo.
if %errorlevel% neq 0 (
    echo ❌ Program ended with an error
    echo.
    echo Common solutions:
    echo • Make sure you have internet connection
    echo • Try running this file as administrator
    echo • Check if antivirus is blocking the program
    echo.
) else (
    echo ✅ Program closed normally
)

echo.
echo Thanks for using YouTube Downloader!
pause