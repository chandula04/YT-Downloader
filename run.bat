@echo off
echo ================================
echo  YouTube Downloader v1.0.0
echo ================================
echo.

REM Check if FFmpeg exists locally
if exist "ffmpeg\ffmpeg.exe" (
    echo ✅ FFmpeg found: Local installation ready
) else (
    echo ⚠️ FFmpeg not found. Setting up...
    python setup_ffmpeg.py
    if errorlevel 1 (
        echo ❌ Failed to setup FFmpeg
        pause
        exit /b 1
    )
    echo ✅ FFmpeg setup completed!
    echo.
)

echo 🚀 Starting YouTube Downloader...
echo.
python main.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ❌ Application ended with an error
    pause
) else (
    echo.
    echo ✅ Application closed successfully
)