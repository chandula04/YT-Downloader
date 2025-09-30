@echo off
title YouTube Downloader - ADVANCED DIAGNOSTICS by Chandula [CMW]
color 0E
cls

:: Advanced diagnostic script that will help identify why the app won't start
setlocal EnableDelayedExpansion

echo =========================================================
echo    YouTube Downloader - COMPREHENSIVE DIAGNOSIS
echo    Publisher: Chandula [CMW]
echo    This will help identify why the app won't start
echo =========================================================
echo.

:: Create detailed log file with timestamp
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set "log_file=diagnostic_report_%datetime:~0,8%_%datetime:~8,6%.txt"

echo Creating diagnostic report: %log_file%
echo This will capture everything to help solve the problem...
echo.

echo YouTube Downloader Advanced Diagnostic Report > %log_file%
echo Generated: %date% %time% >> %log_file%
echo Publisher: Chandula [CMW] >> %log_file%
echo ================================================ >> %log_file%
echo. >> %log_file%

:: 1. System Environment
echo [1/12] Analyzing system environment...
echo SYSTEM ENVIRONMENT: >> %log_file%
echo • Computer Name: %COMPUTERNAME% >> %log_file%
echo • Username: %USERNAME% >> %log_file%
echo • Windows Version: >> %log_file%
ver >> %log_file%
echo • Processor: %PROCESSOR_ARCHITECTURE% >> %log_file%
echo • Current Directory: %CD% >> %log_file%
echo • Script Location: %~dp0 >> %log_file%
echo • PATH Variable: >> %log_file%
echo %PATH% >> %log_file%
echo. >> %log_file%

:: 2. Directory Structure Analysis
echo [2/12] Checking directory structure...
echo DIRECTORY STRUCTURE: >> %log_file%
echo Current directory contents: >> %log_file%
dir >> %log_file% 2>&1
echo. >> %log_file%

echo Python files in directory: >> %log_file%
dir *.py >> %log_file% 2>&1
echo. >> %log_file%

echo Required project folders: >> %log_file%
for %%d in (gui core utils config ffmpeg) do (
    if exist "%%d" (
        echo • %%d: EXISTS >> %log_file%
        echo   Contents of %%d: >> %log_file%
        dir "%%d" /b >> %log_file% 2>&1
    ) else (
        echo • %%d: MISSING >> %log_file%
    )
    echo. >> %log_file%
)

:: 3. Python Installation Analysis
echo [3/12] Analyzing Python installation...
echo PYTHON INSTALLATION: >> %log_file%
echo Python location: >> %log_file%
where python >> %log_file% 2>&1
echo. >> %log_file%

echo Python version: >> %log_file%
python --version >> %log_file% 2>&1
echo Python exit code: %errorlevel% >> %log_file%
echo. >> %log_file%

echo Python executable path: >> %log_file%
python -c "import sys; print('Executable:', sys.executable)" >> %log_file% 2>&1
echo. >> %log_file%

echo Python installation details: >> %log_file%
python -c "import sys; print('Version:', sys.version); print('Platform:', sys.platform); print('Architecture:', sys.maxsize > 2**32 and '64-bit' or '32-bit')" >> %log_file% 2>&1
echo. >> %log_file%

echo Python module search path: >> %log_file%
python -c "import sys; [print('  ', p) for p in sys.path if p]" >> %log_file% 2>&1
echo. >> %log_file%

:: 4. Pip and Package Manager
echo [4/12] Checking pip and package management...
echo PIP INFORMATION: >> %log_file%
python -m pip --version >> %log_file% 2>&1
echo. >> %log_file%

echo Pip configuration: >> %log_file%
python -m pip config list >> %log_file% 2>&1
echo. >> %log_file%

:: 5. Installed Packages
echo [5/12] Checking installed packages...
echo INSTALLED PACKAGES: >> %log_file%
python -m pip list >> %log_file% 2>&1
echo. >> %log_file%

echo Package locations: >> %log_file%
python -c "import site; print('Site packages:'); [print('  ', p) for p in site.getsitepackages()]" >> %log_file% 2>&1
echo. >> %log_file%

:: 6. Critical Package Import Tests
echo [6/12] Testing critical package imports...
echo PACKAGE IMPORT TESTS: >> %log_file%

:: Test each package individually with detailed error reporting
echo Testing tkinter (GUI base): >> %log_file%
python -c "
try:
    import tkinter as tk
    print('✅ tkinter: OK - Version:', tk.TkVersion)
    root = tk.Tk()
    root.withdraw()
    print('✅ tkinter window creation: OK')
    root.destroy()
except Exception as e:
    print('❌ tkinter: FAILED -', str(e))
    import traceback
    traceback.print_exc()
" >> %log_file% 2>&1
echo. >> %log_file%

echo Testing customtkinter (Modern GUI): >> %log_file%
python -c "
try:
    import customtkinter as ctk
    print('✅ customtkinter: OK - Version:', ctk.__version__)
    ctk.set_appearance_mode('dark')
    print('✅ customtkinter configuration: OK')
except Exception as e:
    print('❌ customtkinter: FAILED -', str(e))
    import traceback
    traceback.print_exc()
" >> %log_file% 2>&1
echo. >> %log_file%

echo Testing pytubefix (YouTube downloader): >> %log_file%
python -c "
try:
    import pytubefix
    print('✅ pytubefix: OK')
    from pytubefix import YouTube
    print('✅ pytubefix YouTube class: OK')
except Exception as e:
    print('❌ pytubefix: FAILED -', str(e))
    import traceback
    traceback.print_exc()
" >> %log_file% 2>&1
echo. >> %log_file%

echo Testing PIL/Pillow (Image processing): >> %log_file%
python -c "
try:
    import PIL
    from PIL import Image
    print('✅ PIL: OK - Version:', PIL.__version__)
    print('✅ PIL Image module: OK')
except Exception as e:
    print('❌ PIL: FAILED -', str(e))
    import traceback
    traceback.print_exc()
" >> %log_file% 2>&1
echo. >> %log_file%

echo Testing requests (HTTP library): >> %log_file%
python -c "
try:
    import requests
    print('✅ requests: OK - Version:', requests.__version__)
    resp = requests.get('https://httpbin.org/ip', timeout=5)
    print('✅ requests network test: OK')
except Exception as e:
    print('❌ requests: FAILED -', str(e))
    import traceback
    traceback.print_exc()
" >> %log_file% 2>&1
echo. >> %log_file%

:: 7. Main Application Analysis
echo [7/12] Analyzing main application file...
echo MAIN APPLICATION ANALYSIS: >> %log_file%

if exist "main.py" (
    echo • main.py exists: YES >> %log_file%
    for %%I in (main.py) do echo • File size: %%~zI bytes >> %log_file%
    echo • File permissions: >> %log_file%
    icacls "main.py" >> %log_file% 2>&1
    echo. >> %log_file%
    
    echo • First 10 lines of main.py: >> %log_file%
    powershell -Command "Get-Content main.py | Select-Object -First 10" >> %log_file% 2>&1
    echo. >> %log_file%
    
    echo • Python syntax check: >> %log_file%
    python -m py_compile main.py >> %log_file% 2>&1
    if %errorlevel% equ 0 (
        echo ✅ main.py syntax: OK >> %log_file%
    ) else (
        echo ❌ main.py syntax: FAILED >> %log_file%
    )
    echo. >> %log_file%
    
    echo • Import analysis of main.py: >> %log_file%
    python -c "
import ast
import sys
try:
    with open('main.py', 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read())
    
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module if node.module else ''
            for alias in node.names:
                imports.append(f'{module}.{alias.name}' if module else alias.name)
    
    print('Imports found in main.py:')
    for imp in sorted(set(imports)):
        print(f'  • {imp}')
except Exception as e:
    print('Could not analyze imports:', str(e))
" >> %log_file% 2>&1
    echo. >> %log_file%
) else (
    echo • main.py exists: NO >> %log_file%
    echo • ❌ CRITICAL: Main application file not found! >> %log_file%
    echo • This is likely the primary reason the app won't start >> %log_file%
)
echo. >> %log_file%

:: 8. Module Path Analysis
echo [8/12] Analyzing module import paths...
echo MODULE PATH ANALYSIS: >> %log_file%

echo Testing local module imports: >> %log_file%
python -c "
import sys
import os
sys.path.insert(0, os.getcwd())

modules_to_test = ['gui', 'core', 'utils', 'config']
for module in modules_to_test:
    try:
        __import__(module)
        print(f'✅ {module}: Import OK')
    except Exception as e:
        print(f'❌ {module}: Import FAILED - {str(e)}')
        
    # Check if __init__.py exists
    init_file = os.path.join(module, '__init__.py')
    if os.path.exists(init_file):
        print(f'✅ {module}/__init__.py: EXISTS')
    else:
        print(f'❌ {module}/__init__.py: MISSING')
" >> %log_file% 2>&1
echo. >> %log_file%

:: 9. Network Connectivity
echo [9/12] Testing network connectivity...
echo NETWORK CONNECTIVITY: >> %log_file%
echo Testing general internet: >> %log_file%
ping -n 2 8.8.8.8 >> %log_file% 2>&1
echo. >> %log_file%
echo Testing YouTube connectivity: >> %log_file%
ping -n 2 youtube.com >> %log_file% 2>&1
echo. >> %log_file%

echo Testing HTTPS connectivity: >> %log_file%
python -c "
import requests
try:
    resp = requests.get('https://www.youtube.com', timeout=10)
    print(f'✅ YouTube HTTPS: OK - Status {resp.status_code}')
except Exception as e:
    print(f'❌ YouTube HTTPS: FAILED - {str(e)}')
" >> %log_file% 2>&1
echo. >> %log_file%

:: 10. Security Software Analysis
echo [10/12] Analyzing security software...
echo SECURITY SOFTWARE ANALYSIS: >> %log_file%
echo Windows Defender status: >> %log_file%
powershell -Command "
try {
    $status = Get-MpComputerStatus
    Write-Host 'AntivirusEnabled:' $status.AntivirusEnabled
    Write-Host 'RealTimeProtectionEnabled:' $status.RealTimeProtectionEnabled
    Write-Host 'IoavProtectionEnabled:' $status.IoavProtectionEnabled
    Write-Host 'BehaviorMonitorEnabled:' $status.BehaviorMonitorEnabled
} catch {
    Write-Host 'Could not retrieve Windows Defender status'
}
" >> %log_file% 2>&1
echo. >> %log_file%

echo Checking for exclusions: >> %log_file%
powershell -Command "
try {
    $prefs = Get-MpPreference
    Write-Host 'Exclusion Paths:'
    $prefs.ExclusionPath | ForEach-Object { Write-Host '  ' $_ }
} catch {
    Write-Host 'Could not check exclusion paths'
}
" >> %log_file% 2>&1
echo. >> %log_file%

:: 11. FFmpeg Analysis
echo [11/12] Analyzing FFmpeg setup...
echo FFMPEG ANALYSIS: >> %log_file%
if exist "ffmpeg\ffmpeg.exe" (
    echo • Local FFmpeg: EXISTS >> %log_file%
    "ffmpeg\ffmpeg.exe" -version >> %log_file% 2>&1
) else (
    echo • Local FFmpeg: NOT FOUND >> %log_file%
)

echo System FFmpeg: >> %log_file%
where ffmpeg >> %log_file% 2>&1
echo. >> %log_file%

:: 12. Application Launch Attempt with Full Monitoring
echo [12/12] Attempting comprehensive application launch...
echo APPLICATION LAUNCH TEST: >> %log_file%
echo ============================================ >> %log_file%

if exist "main.py" (
    echo Starting application with full monitoring... >> %log_file%
    echo Launch time: %date% %time% >> %log_file%
    echo. >> %log_file%
    
    :: Try to launch with comprehensive error capture
    python -u main.py >> %log_file% 2>&1
    set launch_result=%errorlevel%
    
    echo. >> %log_file%
    echo Launch completed at: %date% %time% >> %log_file%
    echo Exit code: %launch_result% >> %log_file%
    echo ============================================ >> %log_file%
) else (
    echo Cannot launch: main.py not found >> %log_file%
    set launch_result=404
)

echo. >> %log_file%
echo DIAGNOSTIC COMPLETE >> %log_file%
echo =================== >> %log_file%

:: Display comprehensive results
cls
echo =========================================================
echo                 COMPREHENSIVE DIAGNOSIS COMPLETE
echo =========================================================
echo.

echo 📊 RESULTS SUMMARY:
echo.

if %launch_result% equ 0 (
    echo ✅ SUCCESS: Application launched successfully!
    echo.
    echo If you don't see the YouTube Downloader window:
    echo • Check the taskbar for the application
    echo • Look in Task Manager for python.exe processes
    echo • Try Alt+Tab to cycle through open windows
    echo • The application might have opened minimized
) else if %launch_result% equ 404 (
    echo ❌ CRITICAL ERROR: main.py file not found!
    echo.
    echo 🔧 IMMEDIATE SOLUTIONS:
    echo 1. Verify you're in the correct YouTube Downloader folder
    echo 2. Check if the download/extraction was complete
    echo 3. Look for main.py in the current directory
    echo 4. Ensure antivirus didn't quarantine files
    echo 5. Re-download the complete project if necessary
) else (
    echo ❌ APPLICATION LAUNCH ERROR: Exit code %launch_result%
    echo.
    echo 🔧 TROUBLESHOOTING CHECKLIST:
    echo 1. Check the diagnostic report for specific errors
    echo 2. Look for package import failures
    echo 3. Verify Python installation and PATH
    echo 4. Check antivirus exclusions
    echo 5. Try running as administrator
    echo 6. Ensure all dependencies are installed
)

echo.
echo 📋 DETAILED DIAGNOSTIC REPORT: %log_file%
echo.

echo 🔍 CRITICAL ISSUES FOUND:
findstr /I "FAILED ERROR MISSING CRITICAL" %log_file% 2>nul | findstr /V "No string" || echo   No critical issues detected in scan

echo.
echo ==========================================
echo           NEXT STEPS & SUPPORT
echo ==========================================
echo.
echo 1. 📖 Review the complete diagnostic report: %log_file%
echo 2. 🔧 Address any FAILED, ERROR, or MISSING items
echo 3. 🛡️ Add the project folder to antivirus exclusions
echo 4. 🐍 Reinstall Python if PATH issues are detected
echo 5. 📦 Run check_packages.py if package issues found
echo 6. 🔄 Try running as administrator
echo.
echo 📞 For Support:
echo • GitHub: github.com/chandula04/YT-Downloader
echo • Include this diagnostic report when asking for help
echo • Report Issue: Create a new issue with the diagnostic file
echo.
echo Press any key to view the diagnostic report...
pause >nul

:: Try to open the report
notepad %log_file% 2>nul || (
    echo Opening report in console...
    echo.
    type %log_file%
)

echo.
echo Press any key to exit diagnostic tool...
pause >nul

endlocal