"""
Advanced setup script for YouTube Downloader
This script handles Python installation and dependency management
"""

import sys
import subprocess
import os
import platform
import urllib.request
import zipfile
import shutil
from pathlib import Path

def check_python():
    """Check if Python is installed and accessible"""
    try:
        result = subprocess.run([sys.executable, '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ {version} is installed")
            return True
    except:
        pass
    
    print("❌ Python is not accessible")
    return False

def install_packages():
    """Install required Python packages"""
    packages = [
        "customtkinter==5.2.0",
        "pytubefix==6.0.0", 
        "Pillow>=10.0.0",
        "requests>=2.31.0"
    ]
    
    print("\n📦 Installing required packages...")
    
    for package in packages:
        print(f"Installing {package}...")
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {package} installed successfully")
            else:
                print(f"❌ Failed to install {package}")
                print(f"Error: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error installing {package}: {e}")
            return False
    
    return True

def check_dependencies():
    """Check if all required dependencies are installed"""
    dependencies = [
        ("customtkinter", "import customtkinter"),
        ("pytubefix", "import pytubefix"),
        ("Pillow", "from PIL import Image"),
        ("requests", "import requests")
    ]
    
    print("\n🔍 Checking dependencies...")
    all_good = True
    
    for name, import_cmd in dependencies:
        try:
            subprocess.run([sys.executable, "-c", import_cmd], 
                         check=True, capture_output=True)
            print(f"✅ {name} is available")
        except subprocess.CalledProcessError:
            print(f"❌ {name} is missing")
            all_good = False
        except Exception as e:
            print(f"❌ Error checking {name}: {e}")
            all_good = False
    
    return all_good

def setup_ffmpeg():
    """Setup FFmpeg if not present"""
    ffmpeg_path = Path("ffmpeg/ffmpeg.exe")
    
    if ffmpeg_path.exists():
        print("✅ FFmpeg is already installed")
        return True
    
    print("\n🎥 Setting up FFmpeg...")
    try:
        result = subprocess.run([sys.executable, "setup_ffmpeg.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ FFmpeg setup completed")
            return True
        else:
            print(f"❌ FFmpeg setup failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error setting up FFmpeg: {e}")
        return False

def test_application():
    """Test if the application can start"""
    print("\n🧪 Testing application startup...")
    try:
        # Test imports only, don't start GUI
        result = subprocess.run([
            sys.executable, "-c", 
            "import gui; import core; print('✅ All modules load successfully')"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Application modules load successfully")
            return True
        else:
            print(f"❌ Application test failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Application test timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing application: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 50)
    print("    YouTube Downloader - Advanced Setup")
    print("=" * 50)
    
    # Check Python
    if not check_python():
        print("\n❌ Python is required but not found!")
        print("Please install Python from: https://www.python.org/downloads/")
        print("Make sure to check 'Add Python to PATH' during installation")
        input("\nPress Enter to exit...")
        return False
    
    # Install packages
    if not install_packages():
        print("\n❌ Failed to install required packages!")
        input("Press Enter to exit...")
        return False
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Some dependencies are still missing!")
        input("Press Enter to exit...")
        return False
    
    # Setup FFmpeg
    if not setup_ffmpeg():
        print("\n⚠️ FFmpeg setup failed, but you can continue without it")
        print("Some features may not work properly")
    
    # Test application
    if not test_application():
        print("\n⚠️ Application test failed, but setup is complete")
        print("Try running the application manually")
    
    print("\n" + "=" * 50)
    print("✅ SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print("\nYou can now run the YouTube Downloader using:")
    print("  • Double-click run.bat")
    print("  • Or run: python main.py")
    print("\nIf you encounter any issues, run check_dependencies.bat")
    
    input("\nPress Enter to exit...")
    return True

if __name__ == "__main__":
    main()