#!/usr/bin/env python3
"""
Quick FFmpeg Fix - Solves the repeated download problem
"""

import os
import zipfile
from pathlib import Path

def quick_fix():
    """Quick fix to extract FFmpeg from existing temp.zip"""
    print("🔧 Quick FFmpeg Fix Tool")
    print("=" * 25)
    
    # Check if temp.zip exists
    temp_zip = Path("ffmpeg/temp.zip")
    if not temp_zip.exists():
        print("❌ No temp.zip found - run normal setup")
        return False
    
    print("📦 Found existing temp.zip, extracting...")
    
    try:
        with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
            # Show what's in the zip
            all_files = [f.filename for f in zip_ref.filelist]
            print(f"🔍 Archive contains {len(all_files)} files")
            
            # Look for ffmpeg.exe
            ffmpeg_found = False
            for file in zip_ref.filelist:
                if 'ffmpeg.exe' in file.filename and 'bin/' in file.filename:
                    print(f"✅ Found: {file.filename}")
                    with zip_ref.open(file) as source:
                        with open("ffmpeg/ffmpeg.exe", "wb") as target:
                            target.write(source.read())
                    ffmpeg_found = True
                    break
            
            if not ffmpeg_found:
                print("🔍 Trying broader search...")
                for file in zip_ref.filelist:
                    if file.filename.endswith('ffmpeg.exe'):
                        print(f"✅ Found: {file.filename}")
                        with zip_ref.open(file) as source:
                            with open("ffmpeg/ffmpeg.exe", "wb") as target:
                                target.write(source.read())
                        ffmpeg_found = True
                        break
        
        if ffmpeg_found:
            # Test it
            import subprocess
            try:
                result = subprocess.run(['ffmpeg/ffmpeg.exe', '-version'], 
                                       capture_output=True, timeout=5, text=True)
                if result.returncode == 0 and 'ffmpeg version' in result.stdout.lower():
                    print("✅ FFmpeg working perfectly!")
                    # Clean up temp file
                    temp_zip.unlink()
                    print("🧹 Cleaned up temp.zip")
                    return True
                else:
                    print("❌ FFmpeg extracted but not working")
                    return False
            except Exception as e:
                print(f"❌ Test failed: {e}")
                return False
        else:
            print("❌ Could not find ffmpeg.exe in archive")
            print("📋 First 10 files in archive:")
            for i, filename in enumerate(all_files[:10]):
                print(f"  {i+1}. {filename}")
            return False
            
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        return False

if __name__ == "__main__":
    if quick_fix():
        print("\n🎉 SUCCESS! FFmpeg is now ready!")
        print("🚀 You can now run your YouTube Downloader!")
    else:
        print("\n❌ Quick fix failed. Try running the full setup_ffmpeg.py")