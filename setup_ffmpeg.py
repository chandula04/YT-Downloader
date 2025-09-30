import os
import platform
import zipfile
import requests
import subprocess
import shutil
from pathlib import Path

def get_architecture():
    """Detect Windows architecture"""
    if platform.machine().lower() in ['amd64', 'x86_64']:
        return 'x64'
    if platform.architecture()[0] == '64bit':
        return 'x64'
    if os.environ.get('PROCESSOR_ARCHITECTURE', '').lower() == 'amd64':
        return 'x64'
    return 'x86'

def test_ffmpeg():
    """Test if FFmpeg works"""
    ffmpeg_path = Path("ffmpeg/ffmpeg.exe")
    if not ffmpeg_path.exists():
        return False
    
    try:
        result = subprocess.run([str(ffmpeg_path), '-version'], 
                               capture_output=True, timeout=5)
        return result.returncode == 0
    except:
        return False

def clean_ffmpeg():
    """Remove old FFmpeg"""
    ffmpeg_dir = Path("ffmpeg")
    if ffmpeg_dir.exists():
        try:
            shutil.rmtree(ffmpeg_dir)
            print("Removed old FFmpeg")
        except:
            print("Warning: Could not remove old FFmpeg")

def download_ffmpeg(arch):
    """Download correct FFmpeg version"""
    urls = {
        'x64': 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip',
        'x86': 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win32-gpl.zip'
    }
    
    try:
        print(f"Downloading FFmpeg for {arch}...")
        Path("ffmpeg").mkdir(exist_ok=True)
        
        response = requests.get(urls[arch])
        with open("ffmpeg/temp.zip", "wb") as f:
            f.write(response.content)
        
        print("Extracting...")
        with zipfile.ZipFile("ffmpeg/temp.zip", 'r') as zip_ref:
            for file in zip_ref.filelist:
                if file.filename.endswith('ffmpeg.exe'):
                    with zip_ref.open(file) as source:
                        with open("ffmpeg/ffmpeg.exe", "wb") as target:
                            target.write(source.read())
                    break
        
        os.remove("ffmpeg/temp.zip")
        return True
    except Exception as e:
        print(f"Download failed: {e}")
        return False

def main():
    print("FFmpeg Compatibility Fix")
    print("=" * 25)
    
    # Test current FFmpeg
    if test_ffmpeg():
        print("✅ FFmpeg already working!")
        return
    
    # Get system architecture
    arch = get_architecture()
    print(f"System: Windows {arch}")
    
    # Clean and reinstall
    clean_ffmpeg()
    
    if download_ffmpeg(arch):
        if test_ffmpeg():
            print("✅ FFmpeg fixed successfully!")
        else:
            print("❌ Still having issues")
    else:
        print("❌ Download failed")

if __name__ == "__main__":
    main()
