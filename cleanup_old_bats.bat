@echo off
echo Cleaning up old batch files...
echo Only keeping the comprehensive run.bat

if exist "debug_run.bat" del "debug_run.bat" && echo Deleted debug_run.bat
if exist "emergency_test.bat" del "emergency_test.bat" && echo Deleted emergency_test.bat
if exist "fix_ffmpeg.bat" del "fix_ffmpeg.bat" && echo Deleted fix_ffmpeg.bat
if exist "fix_python313.bat" del "fix_python313.bat" && echo Deleted fix_python313.bat
if exist "install_trusted.bat" del "install_trusted.bat" && echo Deleted install_trusted.bat
if exist "run_clean.bat" del "run_clean.bat" && echo Deleted run_clean.bat
if exist "super_debug.bat" del "super_debug.bat" && echo Deleted super_debug.bat

echo.
echo Cleanup completed! Only run.bat remains.
echo The comprehensive run.bat now includes all functionality.
pause
del "%~f0"