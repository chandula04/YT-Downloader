@echo off
setlocal enabledelayedexpansion

echo ========================================
echo  YouTube Downloader - Portable Setup
echo ========================================
echo.
echo This script will prepare everything needed
echo to run YouTube Downloader on any Windows PC
echo.

:: Create a portable directory structure
if not exist "portable" mkdir portable
cd portable

:: Check if Python portable exists
if exist "python\python.exe" (
    echo ✅ Portable Python found
    set PYTHON_CMD=python\python.exe
    goto check_packages
)

echo Python portable version not found.
echo.
echo Options:
echo 1. Download portable Python (recommended for distribution)
echo 2. Use system Python (if available)
echo 3. Get installation instructions
echo.
set /p choice="Choose option (1-3): "

if "%choice%"=="1" goto download_python
if "%choice%"=="2" goto use_system_python
if "%choice%"=="3" goto instructions

:download_python
echo.
echo ========================================
echo Downloading Portable Python...
echo ========================================
echo.
echo Opening Python.org downloads page...
echo Please download "Windows embeddable package" for your system:
echo - For 64-bit: python-3.11.x-embed-amd64.zip
echo - For 32-bit: python-3.11.x-embed-win32.zip
echo.
echo Extract it to: %cd%\python\
echo.
start https://www.python.org/downloads/windows/
echo.
echo After downloading and extracting:
echo 1. Create a folder called 'python' here
echo 2. Extract the downloaded zip into that folder
echo 3. Run this script again
echo.
pause
goto end

:use_system_python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo System Python not found!
    goto instructions
)
set PYTHON_CMD=python
goto check_packages

:check_packages
echo.
echo ========================================
echo Installing/Checking Packages...
echo ========================================
echo.

:: Install pip for embedded Python if needed
if exist "python\python.exe" (
    if not exist "python\Scripts\pip.exe" (
        echo Installing pip for portable Python...
        python\python.exe -m ensurepip --default-pip
    )
    set PIP_CMD=python\Scripts\pip.exe
) else (
    set PIP_CMD=pip
)

:: Install required packages
echo Installing customtkinter...
%PIP_CMD% install customtkinter==5.2.0

echo Installing pytubefix...
%PIP_CMD% install pytubefix==6.0.0

echo Installing Pillow...
%PIP_CMD% install Pillow

echo Installing requests...
%PIP_CMD% install requests

:: Copy main application files
echo.
echo ========================================
echo Setting up application files...
echo ========================================
echo.

if not exist "..\main.py" (
    echo Error: main.py not found in parent directory!
    pause
    goto end
)

:: Copy essential files
xcopy "..\*.py" . /Y >nul 2>&1
xcopy "..\gui" "gui\" /E /Y >nul 2>&1
xcopy "..\core" "core\" /E /Y >nul 2>&1
xcopy "..\utils" "utils\" /E /Y >nul 2>&1
xcopy "..\config" "config\" /E /Y >nul 2>&1
if exist "..\ffmpeg" xcopy "..\ffmpeg" "ffmpeg\" /E /Y >nul 2>&1

:: Create portable run script
echo @echo off > run_portable.bat
echo title YouTube Downloader - Portable >> run_portable.bat
if exist "python\python.exe" (
    echo python\python.exe main.py >> run_portable.bat
) else (
    echo python main.py >> run_portable.bat
)
echo pause >> run_portable.bat

echo.
echo ========================================
echo ✅ PORTABLE SETUP COMPLETE!
echo ========================================
echo.
echo The portable version is ready in the 'portable' folder.
echo You can copy this folder to any Windows PC and run:
echo   run_portable.bat
echo.
echo No installation required on target PCs!
echo.
pause
goto end

:instructions
echo.
echo ========================================
echo Manual Installation Instructions
echo ========================================
echo.
echo For computers without Python:
echo.
echo 1. Download Python from: https://www.python.org/downloads/
echo 2. During installation, check "Add Python to PATH"
echo 3. Restart the computer
echo 4. Copy the YouTube Downloader folder
echo 5. Run setup.bat in the folder
echo.
echo OR use the portable version:
echo 1. Run this script and choose option 1
echo 2. Follow the portable Python setup
echo 3. Copy the 'portable' folder to any PC
echo.
pause

:end
cd ..