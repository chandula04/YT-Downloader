"""
Test script to verify local FFmpeg integration
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.ffmpeg_handler import FFmpegHandler


def test_ffmpeg_integration():
    """Test the local FFmpeg integration"""
    print("🔧 Testing FFmpeg Integration...")
    print("=" * 50)
    
    # Test FFmpeg path detection
    ffmpeg_path = FFmpegHandler.get_ffmpeg_path()
    print(f"FFmpeg Path: {ffmpeg_path}")
    
    # Check if local FFmpeg exists
    project_root = Path(__file__).parent
    local_ffmpeg = project_root / "ffmpeg" / "ffmpeg.exe"
    
    if local_ffmpeg.exists():
        print(f"✅ Local FFmpeg found: {local_ffmpeg}")
        print(f"   File size: {local_ffmpeg.stat().st_size / 1024 / 1024:.1f} MB")
    else:
        print("❌ Local FFmpeg not found!")
    
    # Test FFmpeg availability
    is_available = FFmpegHandler.is_available()
    print(f"FFmpeg Available: {'✅ Yes' if is_available else '❌ No'}")
    
    if is_available:
        # Try to get FFmpeg version
        import subprocess
        try:
            result = subprocess.run([ffmpeg_path, '-version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                print(f"FFmpeg Version: {version_line}")
                print("✅ FFmpeg is working correctly!")
            else:
                print("⚠️ FFmpeg returned an error code")
        except Exception as e:
            print(f"⚠️ Error getting FFmpeg version: {e}")
    
    print("=" * 50)
    print("🎯 Integration test completed!")


if __name__ == "__main__":
    test_ffmpeg_integration()