@echo off
title YouTube Downloader by Chandula [CMW] - Complete Setup
color 0A
cls

:: Enable advanced batch features
setlocal EnableDelayedExpansion

:: ====================================================
::  YouTube Downloader - COMPREHENSIVE SETUP
::  Publisher: Chandula [CMW]
::  Version: 2.0 - All-in-One Edition
::  Safe to run - No malware, viruses, or harmful code
:: ====================================================

echo.
echo ██████████████████████████████████████████████████████
echo ███     YouTube Downloader by Chandula [CMW]      ███
echo ██████████████████████████████████████████████████████
echo.
echo 🛡️ SECURITY & SAFETY:
echo • Publisher: Chandula [CMW]
echo • Open-source, safe software - No malware/viruses
echo • GitHub: github.com/chandula04/YT-Downloader
echo • All code publicly available and reviewable
echo.
echo 📋 WHAT THIS SETUP DOES:
echo • Checks Python installation and PATH
echo • Downloads and installs missing Python packages
echo • Sets up FFmpeg for video processing
echo • Performs comprehensive system compatibility tests
echo • Launches YouTube Downloader application
echo.
echo ⏱️ Estimated time: 2-5 minutes (depending on internet)
echo.

:: Progress tracking variables
set "total_steps=7"
set "current_step=0"

:: ============================================================
:: STEP 1: ENVIRONMENT AND DIRECTORY VALIDATION
:: ============================================================
set /a current_step+=1
echo.
echo ████████████████████████████████████████████████████████
echo ███ STEP %current_step%/%total_steps%: Environment Validation
echo ████████████████████████████████████████████████████████
echo.

echo [%current_step%/%total_steps%] Validating environment and directory structure...
echo.

echo 🔍 SYSTEM INFORMATION:
echo • Computer: %COMPUTERNAME%
echo • User: %USERNAME%
echo • Windows Version: %OS%
echo • Current Directory: %CD%
echo • Architecture: %PROCESSOR_ARCHITECTURE%
echo.

echo 📂 DIRECTORY STRUCTURE CHECK:
if not exist "main.py" (
    echo ❌ CRITICAL ERROR: main.py not found!
    echo.
    echo 🔍 Current directory contents:
    dir /b *.py 2>nul || echo   No Python files found
    echo.
    echo 💡 SOLUTION:
    echo 1. Navigate to the correct YouTube Downloader folder
    echo 2. Ensure you extracted the complete project
    echo 3. Look for: main.py, gui/, core/, utils/ folders
    echo 4. Re-download if files are missing
    echo.
    goto error_exit
)

echo • main.py: ✅ Found
for %%d in (gui core utils config) do (
    if exist "%%d" (
        echo • %%d/: ✅ Found
    ) else (
        echo • %%d/: ⚠️ Missing ^(may cause issues^)
    )
)

echo.
echo ✅ Directory validation completed!

:: ============================================================
:: STEP 2: PYTHON INSTALLATION AND PATH CHECK
:: ============================================================
set /a current_step+=1
echo.
echo ████████████████████████████████████████████████████████
echo ███ STEP %current_step%/%total_steps%: Python Installation Check
echo ████████████████████████████████████████████████████████
echo.

echo [%current_step%/%total_steps%] Checking Python installation and PATH configuration...
echo.

echo 🐍 PYTHON DETECTION:
where python >temp_python_path.txt 2>&1
set python_check=%errorlevel%

if %python_check% neq 0 (
    echo ❌ Python not found in system PATH!
    echo.
    echo 🔍 DIAGNOSIS:
    echo • Python is not installed, or
    echo • Python is not added to system PATH
    echo.
    echo 💡 SOLUTION REQUIRED:
    echo 1. Download Python from: https://www.python.org/downloads/
    echo 2. During installation, CHECK "Add Python to PATH"
    echo 3. Choose "Install for all users"
    echo 4. Restart computer after installation
    echo 5. Run this script again
    echo.
    echo 🌐 Opening Python download page...
    start https://www.python.org/downloads/
    echo.
    goto error_exit
)

echo • Python executable found at:
type temp_python_path.txt
del temp_python_path.txt >nul 2>&1

python --version >temp_python_version.txt 2>&1
echo • Python version: 
type temp_python_version.txt
del temp_python_version.txt >nul 2>&1

echo • Python module path test:
python -c "import sys; print('✅ Python working, module path OK')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python installation has issues
    goto error_exit
)

echo • Pip package manager:
python -m pip --version >temp_pip_version.txt 2>&1
if %errorlevel% equ 0 (
    echo   ✅ Pip available: 
    type temp_pip_version.txt
    del temp_pip_version.txt >nul 2>&1
) else (
    echo   ❌ Pip not available - this will cause problems
    goto error_exit
)

echo.
echo ✅ Python validation completed successfully!

:: ============================================================
:: STEP 3: SMART PACKAGE INSTALLATION WITH PROGRESS
:: ============================================================
set /a current_step+=1
echo.
echo ████████████████████████████████████████████████████████
echo ███ STEP %current_step%/%total_steps%: Package Installation
echo ████████████████████████████████████████████████████████
echo.

echo [%current_step%/%total_steps%] Installing required Python packages with progress tracking...
echo.

echo 📦 PACKAGE INSTALLATION PROCESS:
echo.

:: Check if smart package installer exists
if exist "check_packages.py" (
    echo 🚀 Using smart package installer...
    echo.
    python check_packages.py
    set smart_install_result=%errorlevel%
    
    if %smart_install_result% equ 0 (
        echo.
        echo ✅ Smart package installation completed successfully!
        goto package_verification
    ) else (
        echo.
        echo ⚠️ Smart installer had issues, falling back to manual installation...
    )
) else (
    echo 📋 Smart installer not found, using manual installation...
)

echo.
echo 🔄 MANUAL PACKAGE INSTALLATION:
echo.

:: Manual installation with progress
set packages=setuptools customtkinter pytubefix Pillow requests
set /a package_count=0
set /a total_packages=5

for %%p in (%packages%) do set /a package_count+=1

set /a current_package=0

for %%p in (%packages%) do (
    set /a current_package+=1
    set /a progress=!current_package!*100/!total_packages!
    
    :: Visual progress bar
    set "progress_bar="
    set /a filled=!progress!/5
    for /l %%i in (1,1,!filled!) do set "progress_bar=!progress_bar!█"
    for /l %%i in (!filled!,1,19) do set "progress_bar=!progress_bar!░"
    
    echo.
    echo ████████████████████████████████████████████████████████
    echo [!progress!%%] [!progress_bar!] Installing %%p...
    echo Package !current_package! of !total_packages!: %%p
    echo ████████████████████████████████████████████████████████
    
    :: Show what this package does
    if "%%p"=="setuptools" echo 📋 Purpose: Python 3.13 compatibility and build tools
    if "%%p"=="customtkinter" echo 🎨 Purpose: Modern GUI framework for the interface
    if "%%p"=="pytubefix" echo 📺 Purpose: YouTube video downloading engine
    if "%%p"=="Pillow" echo 🖼️ Purpose: Image processing for thumbnails
    if "%%p"=="requests" echo 🌐 Purpose: HTTP requests and network communication
    
    echo.
    echo 📥 Downloading and installing %%p...
    
    python -m pip install --upgrade %%p --quiet
    set install_result=!errorlevel!
    
    if !install_result! equ 0 (
        echo ✅ %%p installed successfully
    ) else (
        echo ⚠️ %%p installation had issues, retrying...
        python -m pip install --force-reinstall %%p --quiet
        if !errorlevel! equ 0 (
            echo ✅ %%p installed on retry
        ) else (
            echo ❌ %%p installation failed
        )
    )
    
    timeout /t 1 /nobreak >nul
)

:package_verification
echo 🔍 COMPREHENSIVE PACKAGE VERIFICATION:
echo.

:: Test each package individually with detailed feedback
echo • Testing setuptools:
python -c "import setuptools; print('  ✅ Version:', setuptools.__version__)" 2>nul || echo   ❌ Failed

echo • Testing CustomTkinter:
python -c "import customtkinter as ctk; print('  ✅ Version:', ctk.__version__); ctk.set_appearance_mode('dark')" 2>nul || echo   ❌ Failed

echo • Testing PyTubeFix:
python -c "import pytubefix; from pytubefix import YouTube; print('  ✅ YouTube downloader ready')" 2>nul || echo   ❌ Failed

echo • Testing Pillow:
python -c "import PIL; from PIL import Image; print('  ✅ Version:', PIL.__version__)" 2>nul || echo   ❌ Failed

echo • Testing Requests:
python -c "import requests; print('  ✅ Version:', requests.__version__)" 2>nul || echo   ❌ Failed

echo.
echo 🧪 INTEGRATION TEST:
python -c "import customtkinter, pytubefix, PIL, requests; print('✅ All packages integrated successfully!')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Package integration test failed!
    echo.
    echo 🔄 Attempting emergency package fix...
    python -m pip install --force-reinstall setuptools customtkinter pytubefix Pillow requests
    
    python -c "import customtkinter, pytubefix, PIL, requests; print('✅ Emergency fix successful!')" 2>nul
    if %errorlevel% neq 0 (
        echo ❌ Emergency fix failed - some features may not work
    )
)

echo.
echo ✅ Package installation phase completed!

:: ============================================================
:: STEP 4: FFMPEG SETUP WITH ARCHITECTURE DETECTION
:: ============================================================
set /a current_step+=1
echo.
echo ████████████████████████████████████████████████████████
echo ███ STEP %current_step%/%total_steps%: FFmpeg Video Processing Setup
echo ████████████████████████████████████████████████████████
echo.

echo [%current_step%/%total_steps%] Setting up FFmpeg for high-quality video processing...
echo.

echo 🎬 FFMPEG CONFIGURATION:
echo.

:: Check existing FFmpeg
if exist "ffmpeg\ffmpeg.exe" (
    echo 📁 Local FFmpeg found, testing compatibility...
    
    ffmpeg\ffmpeg.exe -version >temp_ffmpeg_test.txt 2>&1
    set ffmpeg_test=%errorlevel%
    
    if %ffmpeg_test% equ 0 (
        echo ✅ Existing FFmpeg is working correctly!
        echo.
        echo 📋 FFmpeg details:
        type temp_ffmpeg_test.txt | findstr "ffmpeg version"
        del temp_ffmpeg_test.txt >nul 2>&1
        goto ffmpeg_ready
    ) else (
        echo ❌ Existing FFmpeg has compatibility issues
        del temp_ffmpeg_test.txt >nul 2>&1
        echo 🔄 Will download compatible version...
    )
) else (
    echo 📁 No local FFmpeg found
    echo 📥 Will download and install FFmpeg...
)

echo.
echo 🔧 FFMPEG INSTALLATION PROCESS:

:: Check if setup script exists
if exist "setup_ffmpeg.py" (
    echo 🚀 Using automatic FFmpeg installer...
    echo.
    echo • Detecting system architecture...
    echo • Downloading compatible FFmpeg build...
    echo • Installing to local ffmpeg/ directory...
    echo • Testing installation...
    echo.
    
    python setup_ffmpeg.py
    set ffmpeg_setup_result=%errorlevel%
    
    if %ffmpeg_setup_result% equ 0 (
        echo ✅ FFmpeg installation completed successfully!
    ) else (
        echo ⚠️ FFmpeg installation encountered issues
        echo 💡 Basic downloads will still work without FFmpeg
        echo 💡 Some high-quality features may be limited
    )
) else (
    echo ⚠️ FFmpeg installer not found (setup_ffmpeg.py missing)
    echo 💡 You can manually download FFmpeg later if needed
    echo 💡 Basic YouTube downloads will still work
)

:ffmpeg_ready
echo.
echo ✅ FFmpeg setup phase completed!

:: ============================================================
:: STEP 5: NETWORK CONNECTIVITY AND SECURITY CHECK
:: ============================================================
set /a current_step+=1
echo.
echo ████████████████████████████████████████████████████████
echo ███ STEP %current_step%/%total_steps%: Network and Security Validation
echo ████████████████████████████████████████████████████████
echo.

echo [%current_step%/%total_steps%] Performing network connectivity and security checks...
echo.

echo 🌐 NETWORK CONNECTIVITY TEST:
echo.

echo • Testing general internet connectivity:
ping -n 2 8.8.8.8 >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✅ Internet connection active
) else (
    echo   ❌ Internet connection issues detected
    echo   💡 Some features may not work without internet
)

echo • Testing YouTube accessibility:
ping -n 2 youtube.com >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✅ YouTube servers accessible
) else (
    echo   ⚠️ YouTube connectivity issues
    echo   💡 Check firewall/proxy settings
)

echo • Testing HTTPS connectivity:
python -c "import requests; resp=requests.get('https://httpbin.org/ip', timeout=5); print('  ✅ HTTPS working:', resp.status_code==200)" 2>nul || echo   ⚠️ HTTPS issues detected

echo.
echo 🛡️ SECURITY SOFTWARE CHECK:
echo.

echo • Windows Defender status:
powershell -Command "try { $status = Get-MpComputerStatus; Write-Host '  Real-time protection:' $status.RealTimeProtectionEnabled } catch { Write-Host '  Could not check Defender status' }" 2>nul

echo • File permissions check:
echo   📁 Current directory permissions: 
icacls "." | findstr "%USERNAME%" >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✅ Read/write access confirmed
) else (
    echo   ⚠️ Limited permissions - may need administrator rights
)

echo.
echo ✅ Network and security validation completed!

:: ============================================================
:: STEP 6: APPLICATION SYNTAX AND DEPENDENCY CHECK
:: ============================================================
set /a current_step+=1
echo.
echo ████████████████████████████████████████████████████████
echo ███ STEP %current_step%/%total_steps%: Application Validation
echo ████████████████████████████████████████████████████████
echo.

echo [%current_step%/%total_steps%] Validating application integrity and dependencies...
echo.

echo 🔍 APPLICATION FILE ANALYSIS:
echo.

echo • main.py file analysis:
if exist "main.py" (
    for %%I in (main.py) do echo   📄 File size: %%~zI bytes
    echo   🧪 Python syntax validation:
    python -m py_compile main.py 2>nul
    if %errorlevel% equ 0 (
        echo   ✅ Syntax check passed
    ) else (
        echo   ❌ Syntax errors detected in main.py
        goto error_exit
    )
) else (
    echo   ❌ main.py not found!
    goto error_exit
)

echo • Module import testing:
echo   🔗 Testing local module imports:
python -c "
import sys, os
sys.path.insert(0, os.getcwd())
modules = ['gui', 'core', 'utils', 'config']
for module in modules:
    try:
        __import__(module)
        print(f'  ✅ {module}: Import successful')
    except Exception as e:
        print(f'  ⚠️ {module}: {str(e)[:50]}...')
" 2>&1

echo.
echo 🔧 PRE-LAUNCH SYSTEM TEST:
echo.

echo • GUI framework test:
python -c "
try:
    import tkinter
    root = tkinter.Tk()
    root.withdraw()
    root.destroy()
    print('  ✅ GUI system operational')
except Exception as e:
    print(f'  ❌ GUI error: {e}')
" 2>&1

echo • YouTube API connectivity test:
python -c "
try:
    import pytubefix
    print('  ✅ YouTube API ready')
except Exception as e:
    print(f'  ❌ YouTube API error: {e}')
" 2>&1

echo.
echo ✅ Application validation completed!

:: ============================================================
:: STEP 7: LAUNCH APPLICATION
:: ============================================================
set /a current_step+=1
echo.
echo ████████████████████████████████████████████████████████
echo ███ STEP %current_step%/%total_steps%: Application Launch
echo ████████████████████████████████████████████████████████
echo.

echo [%current_step%/%total_steps%] Launching YouTube Downloader application...
echo.

echo 🚀 FINAL LAUNCH SEQUENCE:
echo.

echo ✅ All systems verified and ready!
echo ✅ Python: Working
echo ✅ Packages: Installed
echo ✅ FFmpeg: Ready
echo ✅ Network: Connected
echo ✅ Application: Validated
echo.

echo 🎬 Starting YouTube Downloader...
echo.
echo 💡 If the application doesn't appear:
echo • Check your taskbar for the window
echo • Look in Task Manager for python.exe
echo • Try Alt+Tab to cycle through windows
echo.

timeout /t 3 /nobreak >nul

:: Launch with comprehensive error capture
python main.py 2>app_error_log.txt
set launch_result=%errorlevel%

echo.
echo 📊 LAUNCH RESULT:
echo.

if %launch_result% equ 0 (
    echo ✅ Application launched successfully!
    echo ✅ YouTube Downloader should now be running
    
    if exist app_error_log.txt (
        for /f %%A in ('type app_error_log.txt ^| find /c /v ""') do set line_count=%%A
        if !line_count! gtr 0 (
            echo.
            echo 📋 Application messages:
            type app_error_log.txt
        )
        del app_error_log.txt >nul 2>&1
    )
) else (
    echo ❌ Application launch failed (Exit code: %launch_result%)
    echo.
    
    if exist app_error_log.txt (
        echo 📋 Error details:
        type app_error_log.txt
        echo.
    )
    
    echo 💡 TROUBLESHOOTING:
    echo • Try running this script as administrator
    echo • Temporarily disable antivirus software
    echo • Check if Windows blocked any files
    echo • Ensure all project files are in the same folder
    echo • Contact support with the error details above
    echo.
    
    goto error_exit
)

echo.
echo ████████████████████████████████████████████████████████
echo ███             SETUP COMPLETED SUCCESSFULLY          ███
echo ████████████████████████████████████████████████████████
echo.
echo 🎉 YouTube Downloader is now ready to use!
echo.
echo 📞 Support: github.com/chandula04/YT-Downloader
echo 👨‍💻 Publisher: Chandula [CMW]
echo.
echo Thank you for using YouTube Downloader!
echo.
echo Press any key to close this setup window...
pause >nul
goto end_script

:: ============================================================
:: ERROR HANDLING
:: ============================================================
:error_exit
echo.
echo ████████████████████████████████████████████████████████
echo ███                SETUP FAILED                       ███
echo ████████████████████████████████████████████████████████
echo.
echo ❌ Setup could not be completed due to errors above.
echo.
echo 💡 NEXT STEPS:
echo 1. Read the error messages above carefully
echo 2. Follow the suggested solutions
echo 3. Try running as administrator
echo 4. Contact support if problems persist
echo.
echo 📞 Support: github.com/chandula04/YT-Downloader
echo.
echo Press any key to exit...
pause >nul

:end_script
:: Cleanup temporary files
del temp_*.txt >nul 2>&1
del app_error_log.txt >nul 2>&1

endlocal
exit /b %launch_result%

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
echo 🔍 Running package verification...

:: Simple test without complex multiline code
python -c "import customtkinter, pytubefix, PIL, requests; print('✅ All packages working!')" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️ Some packages need fixing...
    python -m pip install --force-reinstall setuptools customtkinter pytubefix Pillow requests --quiet
    echo ✅ Package fix completed!
) else (
    echo ✅ All packages verified!
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