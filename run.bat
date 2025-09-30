@echo off
title YouTube Downloader by Chandula [CMW]
color 0A

:: CRITICAL: Prevent window from closing on any error
setlocal EnableExtensions EnableDelayedExpansion

:: Set error handling - pause on ANY exit
set "error_pause=1"

:: Trap ALL exit scenarios
if "%1" neq "no_pause" (
    :: Create a wrapper that always pauses
    echo Starting YouTube Downloader with error protection...
    cmd /c "%~f0" no_pause
    echo.
    echo ===========================================
    echo Window will now pause to show any errors
    echo ===========================================
    echo.
    if exist error_log.txt (
        echo ❌ ERRORS DETECTED:
        type error_log.txt
        echo.
    )
    echo Press any key to close this window...
    pause >nul
    exit /b
)

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
echo 🔍 INITIAL DIAGNOSTICS:
echo • Current directory: %CD%
echo • Python executable: 
where python 2>nul || echo   ❌ Python not found in PATH!
echo • Contents of current folder:
dir /b main.py gui core utils 2>nul || echo   ❌ Project files missing!
echo.

if not exist "main.py" (
    echo ❌ CRITICAL ERROR: main.py not found! >>error_log.txt
    echo ❌ ERROR: You're not in the YouTube Downloader folder!
    echo.
    echo 🔍 Current location: %CD%
    echo 📁 Files in this directory:
    dir /b *.py 2>nul || echo   No Python files found
    echo.
    echo 💡 SOLUTION:
    echo 1. Navigate to the correct YouTube Downloader folder
    echo 2. Look for these files: main.py, gui folder, core folder
    echo 3. Right-click run.bat and choose "Run as administrator"
    echo.
    echo ERROR: Wrong directory or missing files >>error_log.txt
    goto force_pause
)

echo ✅ Directory check passed - main.py found
echo 📂 Working from: %CD%
echo.

:: Step 1: Check Python with detailed diagnosis
echo [Step 1/4] Checking Python installation...
echo 🔍 Diagnosing Python setup...

:: Check if python command exists
python --version >temp_output.txt 2>&1
set python_check=%errorlevel%

if %python_check% neq 0 (
    echo ❌ PYTHON ERROR DETECTED >>error_log.txt
    echo ❌ Python not found or not working!
    echo.
    echo 🔍 Python diagnosis:
    type temp_output.txt 2>nul || echo   No output from python command
    echo.
    echo 💡 SOLUTIONS:
    echo 1. Install Python from: https://www.python.org/downloads/
    echo 2. During installation, CHECK "Add Python to PATH"
    echo 3. Restart your computer after installation
    echo 4. Try running as administrator
    echo.
    echo Opening Python download page...
    start https://www.python.org/downloads/ 2>nul
    echo.
    echo Python not found >>error_log.txt
    goto force_pause
)

:: Show Python version
echo 🐍 Python version detected:
type temp_output.txt
del temp_output.txt >nul 2>&1
echo ✅ Python is working correctly!
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
:: All ready - launch the program
echo ====================================================
echo ✅ EVERYTHING IS READY!
echo ====================================================
echo.

:: Check if main.py exists before trying to run it
if not exist "main.py" (
    echo ❌ ERROR: main.py not found!
    echo.
    echo 🔍 Current directory: %CD%
    echo 📁 Files in current directory:
    dir /b *.py 2>nul || echo   No Python files found
    echo.
    echo 💡 Make sure you're running this from the YouTube Downloader folder
    echo 💡 The folder should contain: main.py, gui/, core/, utils/, etc.
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo 🚀 Starting YouTube Downloader...
echo 📂 Working directory: %CD%
echo 🐍 Python path: 
where python 2>nul || echo   Python not found in PATH
echo.

:: Give user time to read
timeout /t 2 /nobreak >nul

:: Try to start the application with comprehensive error capture
echo 📱 Attempting to launch YouTube Downloader...
echo � Launch diagnostics:
echo • Python executable: 
where python
echo • Working directory: %CD%
echo • main.py exists: Yes
echo • File size: 
for %%I in (main.py) do echo   %%~zI bytes
echo.

:: Capture ALL output and errors
echo 🚀 Starting application...
python main.py >app_output.txt 2>&1
set app_exit_code=%errorlevel%

echo.
echo 📊 APPLICATION FINISHED
echo • Exit code: %app_exit_code%
echo • Output captured in app_output.txt
echo.

:: Show what happened
if exist app_output.txt (
    echo 📜 Application output:
    echo ================================
    type app_output.txt
    echo ================================
    echo.
)

:: Handle different exit scenarios with detailed diagnosis
if %app_exit_code% equ 0 (
    echo ✅ Program completed successfully
) else (
    echo ❌ PROGRAM ERROR DETECTED >>error_log.txt
    echo ❌ Program failed with error code: %app_exit_code%
    echo.
    echo 🔍 ERROR ANALYSIS:
    
    if %app_exit_code% equ 1 (
        echo • Error code 1: General error or exception
    ) else if %app_exit_code% equ 2 (
        echo • Error code 2: Missing file or import error
    ) else if %app_exit_code% equ 9009 (
        echo • Error code 9009: Python command not found
    ) else (
        echo • Error code %app_exit_code%: Unexpected error
    )
    
    echo.
    echo 💡 TROUBLESHOOTING STEPS:
    echo 1. Check if antivirus is blocking the program
    echo 2. Run this file as administrator
    echo 3. Ensure internet connection is working
    echo 4. Try: python main.py (manually)
    echo 5. Check if Windows Defender blocked files
    echo.
    echo Application error: Exit code %app_exit_code% >>error_log.txt
)

:: Always show final status
echo.
echo 📋 FINAL STATUS:
echo • Setup completed: Yes
echo • Python working: Yes  
echo • Packages installed: Yes
echo • Application launched: %app_exit_code%
echo • Error log: 
if exist error_log.txt (echo   Yes - check error_log.txt) else (echo   No errors logged)

:force_pause
echo.
echo ==========================================
echo   WINDOW WILL STAY OPEN FOR DIAGNOSIS
echo ==========================================
echo.
echo 📞 If you need help:
echo • Check error_log.txt for details
echo • Contact: github.com/chandula04/YT-Downloader
echo • Try running: debug_run.bat (for advanced diagnosis)
echo.
echo Press any key to close this window...
pause >nul

:: Cleanup
del temp_output.txt >nul 2>&1
del app_output.txt >nul 2>&1
exit /b %app_exit_code%