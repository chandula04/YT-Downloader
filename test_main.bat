@echo off
title Quick Test - What's Wrong?
color 0C
cls

echo ==========================================
echo   QUICK DIAGNOSTIC - Find the Problem
echo ==========================================
echo.

echo This will quickly identify why main.py won't start.
echo.

echo 🔍 BASIC TESTS:
echo.

echo • Current directory:
echo   %CD%
echo.

echo • Python test:
python --version 2>nul
if %errorlevel% neq 0 (
    echo   ❌ Python not found!
    goto quick_end
) else (
    echo   ✅ Python working
)

echo • main.py exists:
if exist main.py (
    echo   ✅ main.py found
) else (
    echo   ❌ main.py missing!
    goto quick_end
)

echo • Quick import test:
python -c "print('Python import system working')" 2>nul
if %errorlevel% neq 0 (
    echo   ❌ Python import system broken
    goto quick_end
) else (
    echo   ✅ Python imports working
)

echo.
echo 🧪 TRYING TO RUN MAIN.PY DIRECTLY:
echo ========================================
echo.

echo Starting main.py with visible errors...
echo If it fails here, we'll see exactly why!
echo.

python main.py
set result=%errorlevel%

echo.
echo ========================================
echo Result: Exit code %result%
echo ========================================

if %result% equ 0 (
    echo ✅ SUCCESS! main.py ran successfully!
    echo If you didn't see the GUI, check taskbar.
) else (
    echo ❌ FAILED! This is why run.bat closes fast.
    echo The error messages above show the exact problem.
)

:quick_end
echo.
echo This window will stay open so you can read everything.
echo.
echo Press any key to close...
pause >nul