"""
Application auto-update system for YouTube Downloader
Checks GitHub releases and downloads new versions
"""

import requests
import os
import sys
import subprocess
import tempfile
from pathlib import Path
from config.settings import APP_VERSION


class AppUpdater:
    """Handles application updates from GitHub releases"""
    
    # GitHub repository info
    GITHUB_OWNER = "chandula04"
    GITHUB_REPO = "YT-Downloader"
    RELEASES_API = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
    
    def __init__(self):
        self.current_version = APP_VERSION
        self.latest_version = None
        self.download_url = None
        self.release_notes = None
        
    def check_for_updates(self):
        """
        Check if a new version is available
        
        Returns:
            tuple: (has_update: bool, version: str, notes: str)
        """
        try:
            print(f"🔍 Checking for updates... Current version: {self.current_version}")
            
            # Get latest release info from GitHub
            response = requests.get(self.RELEASES_API, timeout=10)
            
            if response.status_code != 200:
                print(f"❌ Failed to check updates: HTTP {response.status_code}")
                return False, None, None
            
            data = response.json()
            
            # Extract version info
            self.latest_version = data.get('tag_name', '').replace('v', '')
            self.release_notes = data.get('body', 'No release notes available')
            
            # Find the .exe download URL
            assets = data.get('assets', [])
            for asset in assets:
                if asset['name'].endswith('.exe'):
                    self.download_url = asset['browser_download_url']
                    break
            
            if not self.download_url:
                print("❌ No .exe file found in latest release")
                return False, None, None
            
            # Compare versions
            has_update = self._compare_versions(self.current_version, self.latest_version)
            
            if has_update:
                print(f"✅ New version available: {self.latest_version}")
            else:
                print(f"✅ You're up to date! ({self.current_version})")
            
            return has_update, self.latest_version, self.release_notes
            
        except Exception as e:
            print(f"❌ Update check failed: {e}")
            return False, None, None
    
    def _compare_versions(self, current, latest):
        """
        Compare version numbers
        
        Args:
            current (str): Current version (e.g., "1.0.0")
            latest (str): Latest version (e.g., "1.1.0")
            
        Returns:
            bool: True if update available
        """
        try:
            current_parts = [int(x) for x in current.split('.')]
            latest_parts = [int(x) for x in latest.split('.')]
            
            # Pad with zeros if lengths differ
            max_len = max(len(current_parts), len(latest_parts))
            current_parts += [0] * (max_len - len(current_parts))
            latest_parts += [0] * (max_len - len(latest_parts))
            
            return latest_parts > current_parts
        except:
            return False
    
    def download_update(self, progress_callback=None):
        """
        Download the latest version
        
        Args:
            progress_callback: Optional callback(downloaded, total, percentage)
            
        Returns:
            str: Path to downloaded file, or None on failure
        """
        if not self.download_url:
            print("❌ No download URL available")
            return None
        
        try:
            print(f"⬇️ Downloading update from: {self.download_url}")
            
            # Create temp directory for download
            temp_dir = tempfile.gettempdir()
            filename = f"YouTubeDownloader_v{self.latest_version}.exe"
            temp_path = os.path.join(temp_dir, filename)
            
            # Download with progress tracking
            response = requests.get(self.download_url, stream=True, timeout=30)
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress_callback and total_size > 0:
                            percentage = (downloaded / total_size) * 100
                            progress_callback(downloaded, total_size, percentage)
            
            print(f"✅ Update downloaded to: {temp_path}")
            return temp_path
            
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return None
    
    def apply_update(self, downloaded_file):
        """
        Apply the update by replacing the current executable
        
        Args:
            downloaded_file (str): Path to downloaded .exe
            
        Returns:
            bool: True if update script created successfully
        """
        try:
            # Get current executable path
            if getattr(sys, 'frozen', False):
                # Running as compiled .exe
                current_exe = sys.executable
            else:
                # Running as script (development mode)
                print("⚠️ Cannot update in development mode")
                return False
            
            print(f"📦 Current exe: {current_exe}")
            print(f"📦 New exe: {downloaded_file}")
            
            # Create update batch script
            update_script = self._create_update_script(current_exe, downloaded_file)
            
            if update_script:
                print("✅ Update script created, restarting application...")
                # Run the update script and exit
                subprocess.Popen(update_script, shell=True)
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ Failed to apply update: {e}")
            return False
    
    def _create_update_script(self, current_exe, new_exe):
        """
        Create a batch script to replace the executable
        
        Args:
            current_exe (str): Path to current .exe
            new_exe (str): Path to new .exe
            
        Returns:
            str: Path to update script
        """
        try:
            # Create update script in temp directory
            temp_dir = tempfile.gettempdir()
            script_path = os.path.join(temp_dir, "yt_downloader_update.bat")
            
            # Batch script that:
            # 1. Waits for current process to close
            # 2. Backs up old exe
            # 3. Copies new exe to old location
            # 4. Starts new exe
            # 5. Deletes itself
            
            script_content = f"""@echo off
echo YouTube Downloader - Update in Progress...
echo.
echo Please wait while we update your application...
timeout /t 2 /nobreak >nul

:WAIT_LOOP
tasklist /FI "IMAGENAME eq YouTube Downloader.exe" 2>NUL | find /I /N "YouTube Downloader.exe">NUL
if "%ERRORLEVEL%"=="0" (
    timeout /t 1 /nobreak >nul
    goto WAIT_LOOP
)

echo Backing up old version...
if exist "{current_exe}.backup" del /f /q "{current_exe}.backup"
move /y "{current_exe}" "{current_exe}.backup" >nul 2>&1

echo Installing new version...
copy /y "{new_exe}" "{current_exe}" >nul

echo Starting new version...
start "" "{current_exe}"

echo Cleaning up...
timeout /t 2 /nobreak >nul
del /f /q "{new_exe}" >nul 2>&1
del /f /q "%~f0" >nul 2>&1
"""
            
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            return script_path
            
        except Exception as e:
            print(f"❌ Failed to create update script: {e}")
            return None


def check_for_app_updates():
    """
    Convenience function to check for updates
    
    Returns:
        tuple: (has_update: bool, version: str, notes: str)
    """
    updater = AppUpdater()
    return updater.check_for_updates()
