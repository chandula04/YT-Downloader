@echo off
setlocal EnableDelayedExpansion

cd /d "%~dp0"

REM Build a standalone EXE with PyInstaller
python -m pip install --upgrade -r requirements.txt pyinstaller

REM FFmpeg is bundled so friends do not need to install it.
if not exist "ffmpeg\ffmpeg.exe" (
  echo FFmpeg is missing. Downloading a compatible copy...
  python setup_ffmpeg.py
  if errorlevel 1 (
    echo ERROR: FFmpeg setup failed. Build cancelled.
    exit /b 1
  )
)

REM Single-file portable build (plug and play).
set "PYI_ARGS=--noconfirm --clean --onefile --windowed --noupx --name YouTubeDownloader main.py --collect-all yt_dlp"
if exist "assets" set "PYI_ARGS=%PYI_ARGS% --add-data assets;assets"
if exist "config" set "PYI_ARGS=%PYI_ARGS% --add-data config;config"
if exist "ffmpeg" set "PYI_ARGS=%PYI_ARGS% --add-data ffmpeg;ffmpeg"
python -m PyInstaller %PYI_ARGS%
if errorlevel 1 (
  echo ERROR: PyInstaller build failed.
  exit /b 1
)
echo Portable EXE created at: dist\YouTubeDownloader.exe

REM Build installer with Inno Setup if available
IF EXIST "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" (
  "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" installer\yt_downloader.iss
  echo Installer created in installer\Output
) ELSE (
  echo Inno Setup not found or installer script is missing. Skipping optional installer.
)

endlocal
