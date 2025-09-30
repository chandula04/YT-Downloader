# YouTube Downloader Installer
# Publisher: Chandula [CMW]
# Safe Installation Script

param(
    [switch]$Force = $false
)

# Set execution policy for this session only
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

Write-Host "=====================================================" -ForegroundColor Green
Write-Host "      YouTube Downloader by Chandula [CMW]" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
Write-Host ""
Write-Host "🛡️ SAFETY INFORMATION:" -ForegroundColor Yellow
Write-Host "• Publisher: Chandula [CMW]" -ForegroundColor White
Write-Host "• This is safe, open-source software" -ForegroundColor White
Write-Host "• No viruses, malware, or harmful code" -ForegroundColor White
Write-Host "• Source code available on GitHub" -ForegroundColor White
Write-Host ""

# Check if user wants to continue
if (-not $Force) {
    $response = Read-Host "Do you want to continue with the installation? (Y/N)"
    if ($response -ne "Y" -and $response -ne "y") {
        Write-Host "Installation cancelled by user." -ForegroundColor Red
        exit 1
    }
}

Write-Host "🚀 Starting YouTube Downloader..." -ForegroundColor Green
Write-Host ""

# Run the batch file
try {
    & ".\run.bat"
} catch {
    Write-Host "Error running installer: $_" -ForegroundColor Red
    Write-Host "Please run 'run.bat' manually or contact support." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Installation completed!" -ForegroundColor Green
Read-Host "Press Enter to exit"