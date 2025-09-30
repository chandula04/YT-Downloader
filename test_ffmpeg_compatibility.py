"""
FFmpeg Compatibility Tester
Diagnoses and fixes 16-bit application errors
"""

import os
import sys
import platform
import subprocess
from pathlib import Path


def test_system_compatibility():
    """Test system architecture and compatibility"""
    print("🔍 System Compatibility Test")
    print("=" * 40)
    
    # System info
    print(f"System: {platform.system()}")
    print(f"Version: {platform.version()}")
    print(f"Platform: {platform.platform()}")
    print(f"Machine: {platform.machine()}")
    print(f"Processor: {platform.processor()}")
    print(f"Architecture: {platform.architecture()}")
    
    # Environment variables
    env_arch = os.environ.get('PROCESSOR_ARCHITECTURE', 'Unknown')
    env_archw6432 = os.environ.get('PROCESSOR_ARCHITEW6432', 'Not set')
    print(f"PROCESSOR_ARCHITECTURE: {env_arch}")
    print(f"PROCESSOR_ARCHITEW6432: {env_archw6432}")
    
    # Determine if 64-bit
    is_64bit = any([
        platform.machine().lower() in ['amd64', 'x86_64', 'arm64'],
        '64bit' in str(platform.architecture()),
        'amd64' in env_arch.lower(),
        env_archw6432 != 'Not set'
    ])
    
    print(f"\n🎯 Detected: {'64-bit' if is_64bit else '32-bit'} system")
    return is_64bit


def test_ffmpeg_compatibility():
    """Test current FFmpeg for compatibility issues"""
    print("\n🧪 FFmpeg Compatibility Test")
    print("=" * 40)
    
    ffmpeg_path = Path("ffmpeg") / "ffmpeg.exe"
    
    if not ffmpeg_path.exists():
        print("❌ No FFmpeg found in ffmpeg/ffmpeg.exe")
        return False
    
    print(f"📁 Found FFmpeg at: {ffmpeg_path}")
    
    try:
        # Test basic execution
        print("🧪 Testing basic execution...")
        result = subprocess.run(
            [str(ffmpeg_path), '-version'], 
            capture_output=True, 
            timeout=10,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        
        if result.returncode == 0:
            print("✅ FFmpeg executes successfully")
            
            # Check output
            output = result.stdout.decode('utf-8', errors='ignore')
            if 'ffmpeg version' in output.lower():
                print("✅ FFmpeg version output looks correct")
                
                # Extract version info
                lines = output.split('\n')
                for line in lines[:3]:  # First few lines contain version info
                    if line.strip():
                        print(f"   {line.strip()}")
                
                return True
            else:
                print("⚠️ FFmpeg runs but output seems wrong")
                print(f"Output: {output[:200]}...")
                return False
        else:
            print(f"❌ FFmpeg failed with return code: {result.returncode}")
            stderr = result.stderr.decode('utf-8', errors='ignore')
            if stderr:
                print(f"Error: {stderr[:200]}...")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏱️ FFmpeg test timed out (may be hanging)")
        return False
        
    except Exception as e:
        error_str = str(e).lower()
        
        # Check for common compatibility errors
        if 'winerror 216' in error_str:
            print("🚫 ERROR: 16-bit application compatibility issue detected!")
            print("   This means FFmpeg is wrong architecture for your system")
            return False
        elif 'not compatible' in error_str or 'invalid win32' in error_str:
            print("🚫 ERROR: Application compatibility issue detected!")
            print("   FFmpeg version is incompatible with your Windows version")
            return False
        else:
            print(f"❌ Unexpected error: {e}")
            return False


def recommend_solution(is_64bit, ffmpeg_works):
    """Recommend solution based on test results"""
    print("\n💡 Recommendations")
    print("=" * 40)
    
    if ffmpeg_works:
        print("✅ FFmpeg is working correctly!")
        print("   No action needed.")
        return
    
    if is_64bit:
        print("🎯 You have a 64-bit system")
        print("📥 You need 64-bit FFmpeg (win64)")
        print("\n🔧 SOLUTION:")
        print("1. Delete the current ffmpeg folder")
        print("2. Run: python setup_ffmpeg.py")
        print("3. This will download the correct 64-bit version")
    else:
        print("🎯 You have a 32-bit system")
        print("📥 You need 32-bit FFmpeg (win32)")
        print("\n🔧 SOLUTION:")
        print("1. Delete the current ffmpeg folder")
        print("2. Run: python setup_ffmpeg.py")
        print("3. This will download the correct 32-bit version")
    
    print("\n🔗 Manual download links:")
    print("64-bit: https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip")
    print("32-bit: https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win32-gpl.zip")


def main():
    """Main compatibility test function"""
    print("🎬 FFmpeg Compatibility Diagnostic Tool")
    print("Fixes '16-bit application' errors")
    print("=" * 50)
    
    # Test system
    is_64bit = test_system_compatibility()
    
    # Test FFmpeg
    ffmpeg_works = test_ffmpeg_compatibility()
    
    # Provide recommendations
    recommend_solution(is_64bit, ffmpeg_works)
    
    print("\n" + "=" * 50)
    print("Test completed!")
    
    if not ffmpeg_works:
        print("\n⚠️  ACTION REQUIRED:")
        print("   Run 'python setup_ffmpeg.py' to fix FFmpeg compatibility")
    

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")