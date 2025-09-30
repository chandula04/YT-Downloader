"""
Enhanced FFmpeg setup with automatic compatibility detection and download
Fixes 16-bit application errors on 64-bit Windows systems
"""

import os
import sys
import platform
import zipfile
import requests
import subprocess
import shutil
from pathlib import Path


def detect_system_info():
    """Detect system architecture and compatibility"""
    system = platform.system()
    machine = platform.machine().lower()
    version = platform.version()
    
    print(f"🔍 System: {system} {version}")
    print(f"🔍 Architecture: {machine}")
    
    # More comprehensive architecture detection
    is_64bit = False
    arch = 'x86'
    
    # Check multiple indicators for 64-bit
    if machine in ['amd64', 'x86_64', 'arm64']:
        is_64bit = True
        arch = 'x64'
    elif 'win64' in version.lower() or 'x64' in version.lower():
        is_64bit = True
        arch = 'x64'
    elif hasattr(platform, 'architecture'):
        arch_info = platform.architecture()[0]
        if '64bit' in arch_info:
            is_64bit = True
            arch = 'x64'
    
    # Check Windows environment variables as fallback
    try:
        processor_arch = os.environ.get('PROCESSOR_ARCHITECTURE', '').lower()
        if 'amd64' in processor_arch or 'x64' in processor_arch:
            is_64bit = True
            arch = 'x64'
    except:
        pass
    
    print(f"🔍 Detected: Windows {arch} ({'64-bit' if is_64bit else '32-bit'})")
    
    # Force 64-bit detection if any 64-bit indicators are found
    if any(indicator in str(platform.platform()).lower() for indicator in ['amd64', 'x64', 'win64']):
        arch = 'x64'
        print(f"🔍 Platform string indicates 64-bit: {platform.platform()}")
    
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


def clean_incompatible_ffmpeg():
    """Remove incompatible FFmpeg versions that cause 16-bit application errors"""
    ffmpeg_dir = Path("ffmpeg")
    
    if not ffmpeg_dir.exists():
        return True
    
    print("🧹 Checking for incompatible FFmpeg versions...")
    
    # List of files that might cause compatibility issues
    problem_files = []
    
    for file_path in ffmpeg_dir.rglob("*"):
        if file_path.is_file():
            try:
                # Try to identify problematic files
                if file_path.suffix.lower() == '.exe':
                    # Test if the executable is compatible
                    result = subprocess.run([str(file_path), '-version'], 
                                          capture_output=True, timeout=3)
                    if result.returncode != 0:
                        problem_files.append(file_path)
            except Exception as e:
                # If we can't run it, it's probably incompatible
                if any(error in str(e).lower() for error in [
                    'winerror 216', 'not compatible', '16-bit', 'invalid win32'
                ]):
                    problem_files.append(file_path)
                    print(f"🗑️ Found incompatible file: {file_path.name}")
    
    # Remove problematic files
    if problem_files:
        print(f"🗑️ Removing {len(problem_files)} incompatible files...")
        for file_path in problem_files:
            try:
                file_path.unlink()
                print(f"   Removed: {file_path.name}")
            except Exception as e:
                print(f"   Warning: Could not remove {file_path.name}: {e}")
        
        # If we removed files, check if directory is empty
        remaining_files = list(ffmpeg_dir.rglob("*"))
        if not remaining_files or all(f.is_dir() for f in remaining_files):
            print("🗑️ Removing empty FFmpeg directory...")
            try:
                import shutil
                shutil.rmtree(ffmpeg_dir)
            except:
                pass
        
        return True
    else:
        print("✅ No incompatible files found")
        return False


def test_ffmpeg():
    """Test if FFmpeg is working"""
    ffmpeg_paths = [
        Path("ffmpeg") / "ffmpeg.exe",
        "ffmpeg"  # System PATH
    ]
    
    for ffmpeg_path in ffmpeg_paths:
        try:
            print(f"🧪 Testing: {ffmpeg_path}")
            result = subprocess.run([str(ffmpeg_path), '-version'], 
                                  capture_output=True, timeout=10, 
                                  creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            if result.returncode == 0:
                print(f"✅ FFmpeg working: {ffmpeg_path}")
                # Check if it's actually compatible (not just returns 0)
                output = result.stdout.decode('utf-8', errors='ignore')
                if 'ffmpeg version' in output.lower():
                    return True
                else:
                    print(f"⚠️ FFmpeg returned success but output seems wrong")
            else:
                print(f"❌ FFmpeg test failed with return code: {result.returncode}")
        except subprocess.TimeoutExpired:
            print(f"⏱️ FFmpeg test timed out for {ffmpeg_path}")
            continue
        except Exception as e:
            error_str = str(e).lower()
            if any(error in error_str for error in [
                'winerror 216', 'not compatible', '16-bit', 'invalid win32'
            ]):
                print(f"🚫 FFmpeg compatibility issue: {ffmpeg_path}")
                print(f"   Error: This version is incompatible with your system")
                return False
            else:
                print(f"❌ FFmpeg test failed for {ffmpeg_path}: {e}")
            continue
    
    return False


def setup_ffmpeg():
    """Main FFmpeg setup function with enhanced compatibility checking"""
    print("🎬 FFmpeg Setup - Enhanced Compatibility Check")
    print("=" * 55)
    
    # Clean up any incompatible versions first
    print("🔍 Step 1: Checking for incompatible FFmpeg versions...")
    cleaned = clean_incompatible_ffmpeg()
    
    # Check if FFmpeg already works
    print("🔍 Step 2: Testing current FFmpeg installation...")
    if test_ffmpeg():
        print("✅ FFmpeg is already working perfectly!")
        print("💡 No download needed - using existing FFmpeg")
        return True
    
    # Detect system architecture
    print("🔍 Step 3: Detecting system architecture...")
    arch, system = detect_system_info()
    
    if system != "Windows":
        print("❌ Auto-setup only supports Windows")
        print("💡 Please install FFmpeg manually for your system")
        return False
    
    # Download compatible version
    print(f"📥 Step 4: Downloading FFmpeg for {arch} architecture...")
    if download_ffmpeg(arch):
        print("🔍 Step 5: Verifying new installation...")
        if test_ffmpeg():
            print("🎉 FFmpeg setup completed successfully!")
            print(f"✅ Compatible {arch} version installed and verified")
            return True
        else:
            print("❌ FFmpeg downloaded but compatibility test failed")
            print("� This may indicate a deeper system compatibility issue")
            return False
    else:
        print("❌ FFmpeg download failed")
        return False


if __name__ == "__main__":
    success = setup_ffmpeg()
    if not success:
        print("\n💡 Manual Installation Instructions:")
        print("1. Go to https://ffmpeg.org/download.html")
        print("2. Download FFmpeg for your Windows version")
        print("3. Extract ffmpeg.exe to the 'ffmpeg' folder")
        sys.exit(1)