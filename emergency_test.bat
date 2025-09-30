@echo off
title Emergency Test - YouTube Downloader
color 0C
cls

echo ==========================================
echo   EMERGENCY DIAGNOSTIC TEST
echo   Publisher: Chandula [CMW]
echo ==========================================
echo.
echo This is a minimal test to find the basic problem.
echo.

:: FORCE window to stay open no matter what
set "stay_open=1"

:: Test 1: Basic environment
echo ✓ Testing basic environment...
echo • Current folder: %CD%
echo • User: %USERNAME%
echo • Computer: %COMPUTERNAME%
echo.

:: Test 2: Python availability  
echo ✓ Testing Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ PROBLEM FOUND: Python is not installed or not in PATH
    echo.
    echo SOLUTION:
    echo 1. Install Python from python.org
    echo 2. During installation, check "Add Python to PATH"
    echo 3. Restart computer after installation
    goto emergency_end
)
echo ✅ Python is available
python --version
echo.

:: Test 3: File existence
echo ✓ Testing required files...
if not exist "main.py" (
    echo ❌ PROBLEM FOUND: main.py is missing
    echo.
    echo Current directory contents:
    dir /b *.py 2>nul || echo   No Python files found
    echo.
    echo SOLUTION:
    echo 1. Make sure you're in the YouTube Downloader folder
    echo 2. Look for main.py in the folder
    echo 3. If missing, re-download the complete project
    goto emergency_end
)
echo ✅ main.py exists
echo.

:: Test 4: Basic import test
echo ✓ Testing basic Python imports...
python -c "import sys; print('Python working:', sys.version)" 2>nul
if %errorlevel% neq 0 (
    echo ❌ PROBLEM FOUND: Python has issues
    goto emergency_end
)
echo ✅ Python imports working
echo.

:: Test 5: Critical package test
echo ✓ Testing critical packages...
python -c "
try:
    import tkinter
    print('✅ tkinter: OK')
except:
    print('❌ tkinter: FAILED')
try:
    import customtkinter
    print('✅ customtkinter: OK')
except:
    print('❌ customtkinter: MISSING - This is likely the problem!')
try:
    import pytubefix
    print('✅ pytubefix: OK')  
except:
    print('❌ pytubefix: MISSING - This is likely the problem!')
" 2>&1

echo.

:: Test 6: Try to run the app
echo ✓ Attempting to start YouTube Downloader...
echo   (If it hangs here, press Ctrl+C and run check_packages.py)
echo.
echo Starting in 3 seconds...
timeout /t 3 /nobreak >nul

echo ========== APPLICATION OUTPUT ==========
python main.py 2>&1
set result=%errorlevel%
echo ========== END OUTPUT ==========
echo.

if %result% equ 0 (
    echo ✅ SUCCESS: Application should have started!
    echo If you don't see it, check your taskbar or Task Manager
) else (
    echo ❌ FAILED: Application error (Exit code: %result%)
    echo.
    echo NEXT STEPS:
    echo 1. Run 'check_packages.py' to install missing packages
    echo 2. Run 'super_debug.bat' for detailed diagnosis  
    echo 3. Try running as administrator
)

:emergency_end
echo.
echo ==========================================
echo   EMERGENCY TEST COMPLETE
echo ==========================================
echo.
echo If problems found:
echo • Run 'check_packages.py' (fixes package issues)
echo • Run 'super_debug.bat' (detailed diagnosis)
echo • Try 'run.bat' as administrator
echo.
echo Press any key to close...
pause >nul