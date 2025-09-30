@echo off
title Python 3.13 Compatibility Fix
color 0E
cls

echo.
echo ====================================================
echo        Python 3.13 Compatibility Fix
echo ====================================================
echo.
echo This fixes the "distutils" error in Python 3.13
echo.

echo 🔧 Installing Python 3.13 compatibility packages...
python -m pip install --upgrade setuptools
python -m pip install --upgrade pip
python -m pip install --upgrade wheel

echo.
echo 🎨 Updating CustomTkinter for Python 3.13...
python -m pip uninstall customtkinter -y
python -m pip install customtkinter>=5.2.2

echo.
echo 📦 Updating other packages...
python -m pip install --upgrade pytubefix
python -m pip install --upgrade Pillow
python -m pip install --upgrade requests

echo.
echo ✅ Python 3.13 compatibility fix completed!
echo.
echo You can now run the YouTube Downloader normally.
echo.
pause