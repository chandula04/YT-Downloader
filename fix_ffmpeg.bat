@echo off
title FFmpeg Compatibility Fix
color 0C
cls

echo.
echo ====================================================
echo       FFmpeg Windows Compatibility Fix
echo ====================================================
echo.
echo This will fix the "WinError 216" compatibility issue
echo by downloading the correct FFmpeg for your Windows.
echo.

:: Check if ffmpeg folder exists
if exist "ffmpeg" (
    echo 🗑️ Removing incompatible FFmpeg...
    rmdir /s /q "ffmpeg" 2>nul
    echo ✅ Old FFmpeg removed
) else (
    echo 📁 No existing FFmpeg found
)

echo.
echo 📥 Downloading compatible FFmpeg...
python setup_ffmpeg.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Auto-fix failed!
    echo.
    echo Manual fix:
    echo 1. Go to https://ffmpeg.org/download.html
    echo 2. Download FFmpeg for your Windows version
    echo 3. Extract ffmpeg.exe to a new 'ffmpeg' folder
    echo.
) else (
    echo.
    echo ✅ FFmpeg compatibility fix completed!
    echo.
    echo You can now run the YouTube Downloader normally.
)

echo.
pause