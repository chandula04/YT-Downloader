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

:: Step 2: Install/Check packages
echo [Step 2/4] Installing required packages...
echo This may take a few minutes on first run...
echo.

echo • Installing CustomTkinter (GUI library)...
python -m pip install customtkinter==5.2.0 --quiet >nul 2>&1

echo • Installing PyTubeFix (YouTube downloader)...
python -m pip install pytubefix==6.0.0 --quiet >nul 2>&1

echo • Installing Pillow (Image support)...
python -m pip install Pillow --quiet >nul 2>&1

echo • Installing Requests (Web requests)...
python -m pip install requests --quiet >nul 2>&1

echo ✅ All packages ready!
echo.

:: Step 3: Check if packages work
echo [Step 3/4] Verifying installation...

python -c "import customtkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ CustomTkinter failed to load
    echo Trying to reinstall...
    python -m pip install --force-reinstall customtkinter==5.2.0
)

python -c "import pytubefix" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ PyTubeFix failed to load
    echo Trying to reinstall...
    python -m pip install --force-reinstall pytubefix==6.0.0
)

echo ✅ All libraries verified!
echo.

:: Step 4: Setup FFmpeg
echo [Step 4/4] Setting up video processing...
if exist "ffmpeg\ffmpeg.exe" (
    echo ✅ FFmpeg already ready
) else (
    echo Setting up FFmpeg for video processing...
    python setup_ffmpeg.py >nul 2>&1
    if exist "ffmpeg\ffmpeg.exe" (
        echo ✅ FFmpeg ready!
    ) else (
        echo ⚠️ FFmpeg setup failed - some features may not work
    )
)
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