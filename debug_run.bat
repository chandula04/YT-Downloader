@echo off
title YouTube Downloader - Debug Mode
color 0E
cls

echo.
echo ====================================================
echo    YouTube Downloader - DEBUG MODE
echo ====================================================
echo.
echo This debug version shows detailed information
echo to help diagnose issues.
echo.

:: Step 1: Environment Check
echo [DEBUG] Environment Information
echo ================================
echo • Windows Version: 
ver
echo • Current Directory: %CD%
echo • User: %USERNAME%
echo • Date/Time: %DATE% %TIME%
echo.

:: Step 2: Python Check
echo [DEBUG] Python Environment
echo ===========================
echo • Python Path:
where python 2>nul || echo   Python not found in PATH
echo • Python Version:
python --version 2>nul || echo   Python not accessible
echo • Pip Version:
python -m pip --version 2>nul || echo   Pip not accessible
echo.

:: Step 3: File Structure Check
echo [DEBUG] File Structure
echo ======================
echo • Current folder contents:
dir /b
echo.
echo • Python files:
dir /b *.py 2>nul || echo   No Python files found
echo.
echo • Required folders:
if exist "gui" (echo   ✅ gui folder exists) else (echo   ❌ gui folder missing)
if exist "core" (echo   ✅ core folder exists) else (echo   ❌ core folder missing) 
if exist "utils" (echo   ✅ utils folder exists) else (echo   ❌ utils folder missing)
if exist "config" (echo   ✅ config folder exists) else (echo   ❌ config folder missing)
echo.

:: Step 4: Package Check
echo [DEBUG] Package Status
echo ======================
echo • Testing imports:
python -c "
import sys
print('  • Python executable:', sys.executable)
try:
    import customtkinter
    print('  ✅ CustomTkinter: OK')
except Exception as e:
    print('  ❌ CustomTkinter:', str(e))

try:
    import pytubefix
    print('  ✅ PyTubeFix: OK')
except Exception as e:
    print('  ❌ PyTubeFix:', str(e))

try:
    import PIL
    print('  ✅ Pillow: OK')
except Exception as e:
    print('  ❌ Pillow:', str(e))

try:
    import requests
    print('  ✅ Requests: OK')
except Exception as e:
    print('  ❌ Requests:', str(e))
" 2>&1
echo.

:: Step 5: Try to run main.py
echo [DEBUG] Application Launch
echo ============================
if not exist "main.py" (
    echo ❌ CRITICAL ERROR: main.py not found!
    echo.
    echo This is likely why the application won't start.
    echo Make sure you're in the correct folder.
    goto debug_end
)

echo • main.py found: ✅
echo • Attempting to start application...
echo • Press Ctrl+C to stop if it hangs
echo.
echo =================== APPLICATION OUTPUT ===================
python main.py
set exit_code=%errorlevel%
echo =================== END APPLICATION OUTPUT ===============
echo.

echo • Application exit code: %exit_code%
if %exit_code% equ 0 (
    echo • Status: Normal exit
) else (
    echo • Status: Error exit
)

:debug_end
echo.
echo [DEBUG] End of Debug Session
echo =============================
echo.
echo If you found the issue, you can:
echo • Run the normal run.bat
echo • Or share this debug output for help
echo.
echo Press any key to close...
pause >nul