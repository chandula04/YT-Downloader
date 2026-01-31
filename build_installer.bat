@echo off
setlocal

cd /d "%~dp0"

REM Build a standalone EXE with PyInstaller
python -m pip install --upgrade pyinstaller
pyinstaller --noconfirm --onefile --windowed --name "YouTube Downloader" main.py --add-data "assets;assets" --add-data "ffmpeg;ffmpeg" --add-data "config;config"

REM Build installer with Inno Setup if available
IF EXIST "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" (
  "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" installer\yt_downloader.iss
  echo Installer created in installer\Output
) ELSE (
  echo Inno Setup not found. Install it from https://jrsoftware.org/isdl.php
  echo Then run: "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" installer\yt_downloader.iss
)

endlocal
