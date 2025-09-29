@echo off
echo ========================================
echo    YouTube Downloader Setup Script
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo.
    echo Please choose an option:
    echo 1. Auto-install Python (recommended)
    echo 2. Manual installation instructions
    echo 3. Exit
    echo.
    set /p choice="Enter your choice (1-3): "
    
    if "%choice%"=="1" goto install_python
    if "%choice%"=="2" goto manual_instructions
    if "%choice%"=="3" goto end
    goto end
)

echo Python is installed. Checking version...
python --version
echo.

:: Check and install required packages
echo Installing required Python packages...
echo.

echo Installing customtkinter...
python -m pip install customtkinter==5.2.0
if %errorlevel% neq 0 (
    echo Failed to install customtkinter
    pause
    goto end
)

echo Installing pytubefix...
python -m pip install pytubefix==6.0.0
if %errorlevel% neq 0 (
    echo Failed to install pytubefix
    pause
    goto end
)

echo Installing Pillow...
python -m pip install Pillow>=9.0.0
if %errorlevel% neq 0 (
    echo Failed to install Pillow
    pause
    goto end
)

echo Installing requests...
python -m pip install requests>=2.28.0
if %errorlevel% neq 0 (
    echo Failed to install requests
    pause
    goto end
)

echo.
echo ========================================
echo All packages installed successfully!
echo ========================================
echo.

:: Check FFmpeg
echo Checking FFmpeg...
if exist "ffmpeg\ffmpeg.exe" (
    echo FFmpeg found in local directory.
) else (
    echo FFmpeg not found in local directory.
    echo Running FFmpeg setup...
    python setup_ffmpeg.py
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo You can now run the YouTube Downloader using:
echo   run.bat
echo   OR
echo   python main.py
echo.
pause
goto end

:install_python
echo.
echo Downloading and installing Python...
echo.
echo Opening Python download page...
echo Please download Python 3.10 or later from python.org
echo Make sure to check "Add Python to PATH" during installation!
echo.
start https://www.python.org/downloads/
echo.
echo After installing Python:
echo 1. Restart this script
echo 2. Or run this script again
echo.
pause
goto end

:manual_instructions
echo.
echo ========================================
echo Manual Installation Instructions:
echo ========================================
echo.
echo 1. Download Python from: https://www.python.org/downloads/
echo 2. Install Python (Make sure to check "Add Python to PATH")
echo 3. Restart your computer
echo 4. Run this setup script again
echo.
echo Required Python packages:
echo - customtkinter==5.2.0
echo - pytubefix==6.0.0  
echo - Pillow>=9.0.0
echo - requests>=2.28.0
echo.
echo You can install them manually using:
echo python -m pip install customtkinter==5.2.0 pytubefix==6.0.0 Pillow requests
echo.
pause
goto end

:end