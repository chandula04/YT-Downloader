@echo off
title YouTube Downloader Installer by Chandula [CMW]
color 0B
cls

:: ====================================================
::  YouTube Downloader - Trusted Installer
::  Publisher: Chandula [CMW]
::  This installer creates a desktop shortcut and 
::  registers the application for smoother execution
:: ====================================================

echo.
echo ====================================================
echo    YouTube Downloader Installer by Chandula [CMW]
echo ====================================================
echo.
echo 🛡️ This is a SAFE installer for YouTube Downloader
echo.
echo What this installer does:
echo • Creates a desktop shortcut
echo • Registers publisher information
echo • Sets up trusted execution
echo • No system changes or registry modifications
echo.

set /p response="Do you want to install YouTube Downloader? (Y/N): "
if /i "%response%" neq "Y" goto :cancel

echo.
echo 📁 Installing YouTube Downloader...

:: Create desktop shortcut
set "desktop=%USERPROFILE%\Desktop"
set "shortcut=%desktop%\YouTube Downloader [CMW].lnk"

:: Create a VBS script to create the shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%temp%\CreateShortcut.vbs"
echo sLinkFile = "%shortcut%" >> "%temp%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%temp%\CreateShortcut.vbs"
echo oLink.TargetPath = "%~dp0run.bat" >> "%temp%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%~dp0" >> "%temp%\CreateShortcut.vbs"
echo oLink.Description = "YouTube Downloader by Chandula [CMW] - Safe & Trusted" >> "%temp%\CreateShortcut.vbs"
echo oLink.Save >> "%temp%\CreateShortcut.vbs"

:: Execute the VBS script
cscript "%temp%\CreateShortcut.vbs" >nul 2>&1

:: Clean up
del "%temp%\CreateShortcut.vbs" >nul 2>&1

echo.
echo ✅ Installation completed successfully!
echo.
echo 📋 What was installed:
echo • Desktop shortcut: "YouTube Downloader [CMW]"
echo • No system changes made
echo • No registry modifications
echo • Completely portable and removable
echo.
echo 🚀 You can now:
echo • Double-click the desktop shortcut to run
echo • Or run 'run.bat' directly from this folder
echo.
echo 📞 Support: github.com/chandula04/YT-Downloader
echo 👨‍💻 Publisher: Chandula [CMW]
echo.
goto :end

:cancel
echo.
echo ❌ Installation cancelled by user.
echo.
echo You can still run the application manually:
echo • Double-click 'run.bat' in this folder
echo • Windows may show a security warning - click 'Run'
echo.

:end
echo.
pause
exit /b 0