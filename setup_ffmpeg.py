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
                               capture_output=True, timeout=10, text=True)
        
        combined = (result.stdout or "") + "\n" + (result.stderr or "")
        if result.returncode == 0 and 'ffmpeg version' in combined.lower():
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
    """Remove old FFmpeg with better error handling"""
    ffmpeg_dir = Path("ffmpeg")
    if ffmpeg_dir.exists():
        try:
            # Try to remove all files first
            for file in ffmpeg_dir.glob("*"):
                if file.is_file():
                    try:
                        file.unlink()
                        print(f"🗑️ Removed {file.name}")
                    except PermissionError:
                        print(f"⚠️ Could not remove {file.name} (permission denied)")
                        # Try to make it writable and remove again
                        try:
                            file.chmod(0o777)
                            file.unlink()
                            print(f"🗑️ Force removed {file.name}")
                        except:
                            print(f"❌ Failed to remove {file.name}")
            
            # Try to remove directory if empty
            try:
                ffmpeg_dir.rmdir()
                print("🗑️ Removed ffmpeg directory")
            except OSError:
                print("📁 FFmpeg directory not empty, will reuse")
                
        except Exception as e:
            print(f"⚠️ Warning: Could not fully clean FFmpeg directory: {e}")
    
    # Ensure directory exists
    ffmpeg_dir.mkdir(exist_ok=True)

def download_ffmpeg(arch):
    """Download correct FFmpeg version with progress indicator"""
    urls = {
        'x64': 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip',
        'x86': 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win32-gpl.zip'
    }
    
    try:
        print(f"📥 Downloading FFmpeg for Windows {arch}...")
        
        # Ensure ffmpeg directory exists and is accessible
        ffmpeg_dir = Path("ffmpeg")
        if not ffmpeg_dir.exists():
            ffmpeg_dir.mkdir(exist_ok=True)
        
        # Check if we can write to the directory
        test_file = ffmpeg_dir / "test_write.tmp"
        try:
            test_file.touch()
            test_file.unlink()
        except PermissionError:
            print("❌ Cannot write to ffmpeg directory - permission denied")
            print("💡 Try running as administrator or check folder permissions")
            return False
        
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
        
        print("\n📦 Extracting FFmpeg (including required DLLs)...")
        ffmpeg_found = False
        with zipfile.ZipFile("ffmpeg/temp.zip", 'r') as zip_ref:
            # First, let's see what files are in the zip
            all_files = [f.filename for f in zip_ref.filelist]
            print(f"🔍 Found {len(all_files)} files in archive")
            
            # Find ffmpeg.exe and extract its bin directory contents
            exe_path_in_zip = None
            for name in all_files:
                low = name.lower().replace('\\', '/')
                if low.endswith('/bin/ffmpeg.exe') or low.endswith('ffmpeg.exe'):
                    exe_path_in_zip = name
                    print(f"✅ Found FFmpeg at: {name}")
                    break
            
            if not exe_path_in_zip:
                print("❌ FFmpeg.exe not found! Archive contents (first 10 files):")
                for i, filename in enumerate(all_files[:10]):
                    print(f"  - {filename}")
                return False
            
            # Determine bin directory prefix and extract all files from it
            norm = exe_path_in_zip.replace('\\', '/')
            bin_prefix = norm.rsplit('/', 1)[0]
            if not bin_prefix.endswith('/'):
                bin_prefix += '/'
            extracted = 0
            for file in zip_ref.filelist:
                name = file.filename.replace('\\', '/')
                if name.startswith(bin_prefix) and not name.endswith('/'):
                    target = Path("ffmpeg") / Path(name).name
                    with zip_ref.open(file) as source, open(target, "wb") as out:
                        out.write(source.read())
                    extracted += 1
                    if name.lower().endswith('ffmpeg.exe'):
                        ffmpeg_found = True
            
            if not ffmpeg_found or extracted == 0:
                print("❌ Failed to extract FFmpeg bin contents")
                return False
        
        # Clean up temp file only if extraction succeeded
        try:
            os.remove("ffmpeg/temp.zip")
            print("🧹 Cleaned up temporary files")
        except:
            print("⚠️ Warning: Could not remove temp.zip")
        
        print("✅ FFmpeg installed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Download failed: {e}")
        return False

def main():
    print("🎬 FFmpeg Compatibility Check")
    print("=" * 30)
    
    # HARD SKIP: If ffmpeg.exe already exists, do nothing (no delete/reinstall)
    exe_path = Path("ffmpeg/ffmpeg.exe")
    if exe_path.exists():
        print("✅ Found existing FFmpeg at ffmpeg/ffmpeg.exe - skipping installation.")
        return True

    # STEP 1: Test current FFmpeg first
    working, status = test_ffmpeg()
    
    if working and status == "working":
        print("✅ FFmpeg is already working correctly!")
        print("💡 No action needed - launching YouTube Downloader")
        print("🚀 Skipping download - FFmpeg ready!")
        return True  # Return True to indicate success
    
    # STEP 1.5: Check if we have a temp.zip to extract from
    temp_zip = Path("ffmpeg/temp.zip")
    if temp_zip.exists() and status == "missing":
        print("📦 Found existing download, attempting extraction...")
        try:
            with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
                ffmpeg_found = False
                for file in zip_ref.filelist:
                    if 'ffmpeg.exe' in file.filename:
                        print(f"✅ Extracting: {file.filename}")
                        with zip_ref.open(file) as source:
                            with open("ffmpeg/ffmpeg.exe", "wb") as target:
                                target.write(source.read())
                        ffmpeg_found = True
                        break
                
                if ffmpeg_found:
                    temp_zip.unlink()  # Clean up
                    working, _ = test_ffmpeg()
                    if working:
                        print("🎉 Successfully extracted and verified FFmpeg!")
                        return True
        except Exception as e:
            print(f"⚠️ Extraction failed: {e}")
    
    # STEP 2: Only proceed if there's an actual problem
    print()  # Add spacing
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
            return True
        else:
            print("❌ Still having issues after reinstall")
            print("💡 Manual installation may be required")
            return False
    else:
        print("❌ Download failed - check internet connection")
        return False

if __name__ == "__main__":
    main()
