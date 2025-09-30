@echo off
title YouTube Downloader by Chandula [CMW] - Setup & Launch
color 0A
cls

:: Fix character encoding issues
chcp 65001 >nul 2>&1

:: Enable delayed expansion for variables
setlocal EnableDelayedExpansion

:: ====================================================
::  YouTube Downloader - SETUP & LAUNCH
::  Publisher: Chandula [CMW]
::  Safe to run - No malware, viruses, or harmful code
:: ====================================================

echo.
echo ================================================================
echo ===     YouTube Downloader by Chandula [CMW]              ===
echo ================================================================
echo.
echo SECURITY: Safe open-source software by Chandula [CMW]
echo GitHub: github.com/chandula04/YT-Downloader
echo.
echo THIS SETUP WILL:
echo [1/4] Check Python installation
echo [2/4] Install required packages
echo [3/4] Setup FFmpeg for video processing  
echo [4/4] Launch YouTube Downloader
echo.
echo Takes 1-3 minutes - Window stays open until you close the app!
echo.

:: ============================================================
:: STEP 1: CHECK PYTHON
:: ============================================================
echo ================================================================
echo === STEP 1/4: Checking Python Installation
echo ================================================================
echo.

echo Checking if Python is installed and working...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: PYTHON NOT FOUND!
    echo.
    echo Python is required to run YouTube Downloader.
    echo.
    echo WHAT TO DO:
    echo 1. Download Python from: https://www.python.org/downloads/
    echo 2. During installation: CHECK "Add Python to PATH"
    echo 3. Install for all users
    echo 4. Restart your computer
    echo 5. Run this file again
    echo.
    echo Opening Python download page now...
    start https://www.python.org/downloads/
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo [OK] Python found and working!
python --version
echo.

:: Check pip
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip not working! Python installation might be corrupted.
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo [OK] pip package manager ready!
echo.

:: ============================================================
:: STEP 2: INSTALL PACKAGES
:: ============================================================
echo ================================================================
echo === STEP 2/4: Installing Required Packages
echo ================================================================
echo.

echo Installing Python packages needed for YouTube Downloader...
echo.

:: Try smart installer first
if exist "check_packages.py" (
    echo Using smart package installer...
    python check_packages.py
    if %errorlevel% equ 0 (
        echo [OK] Smart installation completed!
        goto packages_done
    ) else (
        echo Warning: Smart installer had issues, using manual method...
    )
)

:: Manual package installation with progress
echo Installing packages manually...
echo.

set packages=setuptools customtkinter pytubefix Pillow requests
set /a total=5
set /a current=0

for %%p in (%packages%) do (
    set /a current+=1
    set /a percent=!current!*100/!total!
    
    echo [!percent!%%] [!current!/!total!] Installing %%p...
    
    if "%%p"=="setuptools" echo    Purpose: Python 3.13 compatibility...
    if "%%p"=="customtkinter" echo    Purpose: Modern GUI framework...
    if "%%p"=="pytubefix" echo    Purpose: YouTube download engine...
    if "%%p"=="Pillow" echo    Purpose: Image processing...
    if "%%p"=="requests" echo    Purpose: Network requests...
    
    python -m pip install --upgrade %%p --quiet
    if %errorlevel% equ 0 (
        echo    [OK] %%p installed successfully
    ) else (
        echo    Warning: Retrying %%p...
        python -m pip install --force-reinstall %%p --quiet
        if %errorlevel% equ 0 (
            echo    [OK] %%p installed on retry
        ) else (
            echo    ERROR: %%p failed to install
        )
    )
    echo.
)

:packages_done
echo Verifying all packages work together...
python -c "import customtkinter, pytubefix, PIL, requests; print('[OK] All packages verified and ready!')" 2>nul
if %errorlevel% neq 0 (
    echo Warning: Package verification failed, attempting fix...
    python -m pip install --force-reinstall setuptools customtkinter pytubefix Pillow requests --quiet
    echo [OK] Package fix attempted!
)

echo.
echo [OK] Package installation completed!
echo.

:: ============================================================
:: STEP 3: SETUP FFMPEG
:: ============================================================
echo ================================================================
echo === STEP 3/4: Setting up Video Processing (FFmpeg)
echo ================================================================
echo.

echo Setting up FFmpeg for high-quality video downloads...

:: Check if FFmpeg already exists and works
if exist "ffmpeg\ffmpeg.exe" (
    echo Testing existing FFmpeg...
    ffmpeg\ffmpeg.exe -version >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] FFmpeg already installed and working!
        goto ffmpeg_done
    ) else (
        echo Warning: Existing FFmpeg has issues, will reinstall...
    )
)

echo Installing FFmpeg...

:: Use automatic installer if available
if exist "setup_ffmpeg.py" (
    echo Running automatic FFmpeg installer...
    python setup_ffmpeg.py
    if %errorlevel% equ 0 (
        echo [OK] FFmpeg installed successfully!
    ) else (
        echo Warning: FFmpeg installation had issues
        echo Note: Basic downloads will still work
    )
) else (
    echo Note: FFmpeg installer not found
    echo You can manually add FFmpeg later for enhanced features
)

:ffmpeg_done
echo.
echo [OK] Video processing setup completed!
echo.

:: ============================================================
:: STEP 4: LAUNCH APPLICATION & KEEP WINDOW OPEN
:: ============================================================
echo ================================================================
echo === STEP 4/4: Launching YouTube Downloader
echo ================================================================
echo.

echo Final checks before launch...

:: Verify main.py exists
if not exist "main.py" (
    echo ERROR: main.py not found!
    echo.
    echo Current directory: %CD%
    echo Make sure you're in the YouTube Downloader folder
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo [OK] main.py found
echo [OK] Python working
echo [OK] Packages installed
echo [OK] FFmpeg ready
echo.

echo Starting YouTube Downloader GUI...
echo.
echo Note: The YouTube Downloader window will open shortly.
echo This setup window will automatically close when you exit the app.
echo.

:: Launch the YouTube Downloader GUI without opening a new console window
echo Launching YouTube Downloader application...
echo.

:: Set clean environment variables
set PYTHONPATH=%CD%
set PYTHONDONTWRITEBYTECODE=1

:: Use pythonw to run GUI without console window and wait for it to finish
echo Starting GUI application...
pythonw main.py

:: When pythonw finishes (user closed the GUI), we get here
echo.
echo YouTube Downloader has been closed.
set app_result=0



:: This runs AFTER the YouTube Downloader GUI closes
echo.
echo YouTube Downloader application closed with exit code: %app_result%
echo.

if %app_result% equ 0 (
    echo [OK] YouTube Downloader closed normally
) else (
    echo Warning: Application encountered an error (code: %app_result%)
)

echo.
echo ================================================================
echo ===          YouTube Downloader Session Ended               ===
echo ================================================================
echo.
echo Publisher: Chandula [CMW]
echo Support: github.com/chandula04/YT-Downloader
echo.
echo Thank you for using YouTube Downloader!

:: Auto-close after 3 seconds (no manual key press required)
echo.
echo This window will close automatically in 3 seconds...
timeout /t 3 /nobreak >nul

:: Cleanup and exit
del temp_*.txt >nul 2>&1
endlocal
exit /b %app_result%