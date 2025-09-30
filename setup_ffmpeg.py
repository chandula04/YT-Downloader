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
    """Test if FFmpeg works and detect specific compatibility errors"""
    ffmpeg_path = Path("ffmpeg/ffmpeg.exe")
    if not ffmpeg_path.exists():
        print("❌ No FFmpeg found")
        return False, "missing"
    
    try:
        print("🧪 Testing existing FFmpeg...")
        result = subprocess.run([str(ffmpeg_path), '-version'], 
                               capture_output=True, timeout=5, text=True)
        
        if result.returncode == 0:
            print("✅ FFmpeg is working perfectly!")
            return True, "working"
        else:
            print("❌ FFmpeg test failed")
            return False, "failed"
            
    except Exception as e:
        error_msg = str(e).lower()
        print(f"❌ FFmpeg error: {e}")
        
        # Check for specific 16-bit compatibility error
        if any(x in error_msg for x in ['winerror 216', '16-bit', 'not compatible']):
            print("🚫 COMPATIBILITY ERROR: 16-bit application on 64-bit system!")
            return False, "compatibility"
        
        return False, "error"

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
    """Download correct FFmpeg version with progress indicator"""
    urls = {
        'x64': 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip',
        'x86': 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win32-gpl.zip'
    }
    
    try:
        print(f"📥 Downloading FFmpeg for Windows {arch}...")
        Path("ffmpeg").mkdir(exist_ok=True)
        
        # Download with progress
        response = requests.get(urls[arch], stream=True)
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open("ffmpeg/temp.zip", "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r📥 Download Progress: {percent:.1f}%", end='', flush=True)
        
        print("\n📦 Extracting FFmpeg...")
        with zipfile.ZipFile("ffmpeg/temp.zip", 'r') as zip_ref:
            for file in zip_ref.filelist:
                if file.filename.endswith('ffmpeg.exe'):
                    with zip_ref.open(file) as source:
                        with open("ffmpeg/ffmpeg.exe", "wb") as target:
                            target.write(source.read())
                    break
        
        os.remove("ffmpeg/temp.zip")
        print("✅ FFmpeg installed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Download failed: {e}")
        return False

def main():
    print("🎬 FFmpeg Compatibility Check")
    print("=" * 30)
    
    # STEP 1: Test current FFmpeg first
    working, status = test_ffmpeg()
    
    if working:
        print("✅ FFmpeg is already working correctly!")
        print("💡 No action needed - keeping existing FFmpeg")
        return
    
    # STEP 2: Only proceed if there's an actual problem
    if status == "missing":
        print("📥 No FFmpeg found - will install fresh copy")
    elif status == "compatibility":
        print("🔧 Compatibility issue detected - will fix architecture mismatch")
    else:
        print("🔧 FFmpeg has issues - will reinstall")
    
    # STEP 3: Get system architecture
    arch = get_architecture()
    print(f"🔍 Detected: Windows {arch}")
    
    # STEP 4: Clean and reinstall only if needed
    if status != "missing":  # Don't clean if nothing exists
        clean_ffmpeg()
    
    # STEP 5: Download correct version
    if download_ffmpeg(arch):
        # STEP 6: Verify the fix worked
        working_after, _ = test_ffmpeg()
        if working_after:
            print("🎉 FFmpeg compatibility issue fixed!")
        else:
            print("❌ Still having issues after reinstall")
            print("💡 Manual installation may be required")
    else:
        print("❌ Download failed - check internet connection")

if __name__ == "__main__":
    main()
