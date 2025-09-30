"""
Enhanced FFmpeg setup with automatic compatibility detection and download
"""

import os
import sys
import platform
import zipfile
import requests
import subprocess
from pathlib import Path


def detect_system_info():
    """Detect system architecture and compatibility"""
    system = platform.system()
    machine = platform.machine().lower()
    version = platform.version()
    
    print(f"🔍 System: {system} {version}")
    print(f"🔍 Architecture: {machine}")
    
    # Determine architecture
    is_64bit = machine in ['amd64', 'x86_64', 'arm64']
    arch = 'x64' if is_64bit else 'x86'
    
    print(f"🔍 Detected: Windows {arch}")
    return arch, system


def download_ffmpeg(arch):
    """Download compatible FFmpeg for the detected architecture"""
    try:
        print(f"📥 Downloading FFmpeg for Windows {arch}...")
        
        # FFmpeg download URLs
        urls = {
            'x64': 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip',
            'x86': 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win32-gpl.zip'
        }
        
        if arch not in urls:
            print(f"❌ No FFmpeg available for {arch}")
            return False
        
        url = urls[arch]
        
        # Create ffmpeg directory
        ffmpeg_dir = Path("ffmpeg")
        ffmpeg_dir.mkdir(exist_ok=True)
        
        print("📥 Downloading...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        zip_path = ffmpeg_dir / "ffmpeg.zip"
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r📥 Progress: {percent:.1f}%", end='', flush=True)
        
        print("\n📦 Extracting FFmpeg...")
        
        # Extract only ffmpeg.exe
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file_info in zip_ref.filelist:
                if file_info.filename.endswith('ffmpeg.exe'):
                    file_info.filename = 'ffmpeg.exe'
                    zip_ref.extract(file_info, ffmpeg_dir)
                    break
        
        # Clean up
        zip_path.unlink(missing_ok=True)
        
        # Verify
        ffmpeg_exe = ffmpeg_dir / "ffmpeg.exe"
        if ffmpeg_exe.exists():
            print("✅ FFmpeg installed successfully!")
            return True
        else:
            print("❌ FFmpeg extraction failed")
            return False
            
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False


def test_ffmpeg():
    """Test if FFmpeg is working"""
    ffmpeg_paths = [
        Path("ffmpeg") / "ffmpeg.exe",
        "ffmpeg"  # System PATH
    ]
    
    for ffmpeg_path in ffmpeg_paths:
        try:
            result = subprocess.run([str(ffmpeg_path), '-version'], 
                                  capture_output=True, timeout=5)
            if result.returncode == 0:
                print(f"✅ FFmpeg working: {ffmpeg_path}")
                return True
        except Exception as e:
            print(f"❌ FFmpeg test failed for {ffmpeg_path}: {e}")
            continue
    
    return False


def setup_ffmpeg():
    """Main FFmpeg setup function"""
    print("🎬 FFmpeg Setup - Enhanced Compatibility")
    print("=" * 50)
    
    # Check if FFmpeg already works
    if test_ffmpeg():
        print("✅ FFmpeg is already working!")
        return True
    
    # Detect system
    arch, system = detect_system_info()
    
    if system != "Windows":
        print("❌ Auto-setup only supports Windows")
        print("💡 Please install FFmpeg manually for your system")
        return False
    
    # Remove incompatible existing version
    old_ffmpeg = Path("ffmpeg") / "ffmpeg.exe"
    if old_ffmpeg.exists():
        print("🗑️ Removing incompatible FFmpeg version...")
        try:
            old_ffmpeg.unlink()
        except:
            pass
    
    # Download compatible version
    if download_ffmpeg(arch):
        if test_ffmpeg():
            print("🎉 FFmpeg setup completed successfully!")
            return True
        else:
            print("❌ FFmpeg downloaded but not working")
            return False
    else:
        print("❌ FFmpeg setup failed")
        return False


if __name__ == "__main__":
    success = setup_ffmpeg()
    if not success:
        print("\n💡 Manual Installation Instructions:")
        print("1. Go to https://ffmpeg.org/download.html")
        print("2. Download FFmpeg for your Windows version")
        print("3. Extract ffmpeg.exe to the 'ffmpeg' folder")
        sys.exit(1)