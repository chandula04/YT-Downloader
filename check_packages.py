#!/usr/bin/env python3
"""
Smart package checker - only installs what's missing
"""

import subprocess
import sys

def test_import(package_name, import_name=None):
    """Test if a package can be imported"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        return True
    except ImportError:
        return False

def install_package(package_name):
    """Install a package using pip"""
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', 
            package_name, '--quiet'
        ])
        return True
    except subprocess.CalledProcessError:
        return False

def smart_package_setup():
    """Smart package setup - only install what's needed"""
    print("🔍 Smart Package Check")
    print("=" * 30)
    
    packages_to_check = [
        ("setuptools", "setuptools"),
        ("customtkinter>=5.2.2", "customtkinter"),
        ("pytubefix", "pytubefix"), 
        ("yt-dlp[default]", "yt_dlp"),
        ("Pillow", "PIL"),
        ("requests", "requests")
    ]
    
    installed_count = 0
    skipped_count = 0
    
    for package_name, import_name in packages_to_check:
        print(f"\n• Checking {import_name}...")
        
        if test_import(package_name, import_name):
            print(f"  ✅ {import_name} is already working")
            skipped_count += 1
        else:
            print(f"  📥 Installing {package_name}...")
            if install_package(package_name):
                print(f"  ✅ {import_name} installed successfully")
                installed_count += 1
            else:
                print(f"  ❌ Failed to install {package_name}")
    
    print(f"\n📊 Summary:")
    print(f"   • Installed: {installed_count} packages")
    print(f"   • Already working: {skipped_count} packages")
    
    # Final verification
    print(f"\n🔍 Final verification...")
    try:
        import customtkinter
        import pytubefix
        import yt_dlp
        import PIL
        import requests
        print("✅ All packages verified and ready!")
        return True
    except ImportError as e:
        print(f"❌ Verification failed: {e}")
        return False

if __name__ == "__main__":
    success = smart_package_setup()
    if not success:
        print("\n💡 Try running: pip install -r requirements.txt")
        sys.exit(1)