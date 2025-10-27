@echo off
title YouTube Downloader by Chandula [CMW] - Setup & Launch
color 0A
cls

:: Fix character encoding issues
chcp 65001 >nul 2>&1

:: Enable delayed expansion for variables
setlocal EnableDelayedExpansion

:: Always run from the script's directory to keep relative paths stable
cd /d "%~dp0"

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
:: STEP 3: SETUP FFMPEG WITH ENHANCED COMPATIBILITY CHECK
:: ============================================================
echo ================================================================
echo === STEP 3/4: Setting up Video Processing (FFmpeg)
echo ================================================================
echo.

echo Setting up FFmpeg for high-quality video downloads...

:: Enhanced FFmpeg compatibility testing
echo Performing comprehensive FFmpeg compatibility check...

set "ffmpeg_compatible=false"
set "ffmpeg_exists=false"

:: HARD SKIP: If ffmpeg.exe already exists, don't delete or reinstall
if exist "ffmpeg\ffmpeg.exe" (
    echo Detected existing FFmpeg at "ffmpeg\ffmpeg.exe".
    echo Skipping installation and compatibility checks as requested.
    set "ffmpeg_compatible=true"
    goto ffmpeg_done
)
:: Check if FFmpeg exists
if exist "ffmpeg\" (
    set "ffmpeg_exists=true"
    echo Found FFmpeg folder but no executable. Will install fresh version...
) else (
    echo No existing FFmpeg found, will install fresh version...
)

:: Install or reinstall FFmpeg with architecture detection
echo.
echo Installing architecture-compatible FFmpeg...
echo =============================================

:: Use enhanced automatic installer
if exist "setup_ffmpeg.py" (
    echo Running enhanced FFmpeg installer with compatibility detection...
    echo This will:
    echo - Detect your system architecture (32-bit vs 64-bit)
    echo - Download the correct FFmpeg version
    echo - Test compatibility before confirming installation
    echo.
    
    python setup_ffmpeg.py
    set ffmpeg_install_result=%errorlevel%
    
    if !ffmpeg_install_result! equ 0 (
        echo [OK] FFmpeg installation completed!
        
        :: Perform final verification test
        echo.
        echo Performing final compatibility verification...
        
        if exist "ffmpeg\ffmpeg.exe" (
            :: Test the new installation
            ffmpeg\ffmpeg.exe -version >nul 2>&1
            if %errorlevel% equ 0 (
                echo [OK] FFmpeg verified and ready for use!
                set "ffmpeg_compatible=true"
            ) else (
                echo [WARNING] FFmpeg installed but verification failed
                echo This may indicate a deeper system compatibility issue
                set "ffmpeg_compatible=false"
            )
        ) else (
            echo [ERROR] FFmpeg installation completed but executable not found
            set "ffmpeg_compatible=false"
        )
    ) else (
        echo [ERROR] FFmpeg installation failed (exit code: !ffmpeg_install_result!)
        set "ffmpeg_compatible=false"
        
        echo.
        echo INSTALLATION TROUBLESHOOTING
        echo =============================
        echo.
        echo Possible causes and solutions:
        echo.
        echo 1. NETWORK ISSUES:
        echo    - Check your internet connection
        echo    - Try running as administrator
        echo    - Temporarily disable antivirus/firewall
        echo.
        echo 2. SYSTEM REQUIREMENTS:
        echo    - Install Visual C++ Redistributable from Microsoft
        echo    - Update Windows to latest version
        echo    - Ensure sufficient disk space
        echo.
        echo 3. MANUAL INSTALLATION:
        echo    - Go to: https://ffmpeg.org/download.html
        echo    - Download correct version for your Windows (32-bit or 64-bit)
        echo    - Extract ffmpeg.exe to the 'ffmpeg' folder
        echo.
    )
) else (
    echo [ERROR] FFmpeg installer (setup_ffmpeg.py) not found!
    echo.
    echo MANUAL INSTALLATION REQUIRED:
    echo ==============================
    echo 1. Create a 'ffmpeg' folder in this directory
    echo 2. Go to: https://ffmpeg.org/download.html
    echo 3. Download FFmpeg for Windows (choose correct architecture)
    echo 4. Extract ffmpeg.exe to the 'ffmpeg' folder
    echo 5. Run this setup again
    echo.
    set "ffmpeg_compatible=false"
)

:ffmpeg_done
echo.
echo FFmpeg Setup Summary:
echo =====================
if "!ffmpeg_compatible!"=="true" (
    echo [OK] FFmpeg is ready for high-quality video processing
    echo [OK] Adaptive stream downloads will work perfectly
    echo [OK] Video/audio merging is available
) else (
    echo [WARNING] FFmpeg setup encountered issues
    echo [INFO] Basic video downloads will still work
    echo [INFO] Only adaptive streams and merging will be unavailable
    echo [TIP] You can run 'python setup_ffmpeg.py' later to retry
)
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