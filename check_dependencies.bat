@echo off
echo ========================================
echo    Dependency Checker for YouTube Downloader
echo ========================================
echo.

set all_good=1

:: Check Python
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is NOT installed or not in PATH
    set all_good=0
) else (
    python --version
    echo ✅ Python is installed
)
echo.

:: Check customtkinter
echo [2/5] Checking customtkinter...
python -c "import customtkinter; print('✅ customtkinter version:', customtkinter.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo ❌ customtkinter is NOT installed
    set all_good=0
)
echo.

:: Check pytubefix
echo [3/5] Checking pytubefix...
python -c "import pytubefix; print('✅ pytubefix version:', pytubefix.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo ❌ pytubefix is NOT installed
    set all_good=0
)
echo.

:: Check Pillow
echo [4/5] Checking Pillow...
python -c "from PIL import Image; import PIL; print('✅ Pillow version:', PIL.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Pillow is NOT installed
    set all_good=0
)
echo.

:: Check FFmpeg
echo [5/5] Checking FFmpeg...
if exist "ffmpeg\ffmpeg.exe" (
    echo ✅ FFmpeg found in local directory
) else (
    echo ❌ FFmpeg not found in local directory
    set all_good=0
)
echo.

:: Summary
echo ========================================
if %all_good%==1 (
    echo ✅ ALL DEPENDENCIES ARE READY!
    echo You can run the YouTube Downloader with run.bat
) else (
    echo ❌ SOME DEPENDENCIES ARE MISSING!
    echo Please run setup.bat to install missing dependencies
)
echo ========================================
echo.

pause