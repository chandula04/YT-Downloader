"""
Update PyTubeFix to Latest Version
This script updates pytubefix to handle YouTube's latest anti-bot measures
"""

import subprocess
import sys

def update_pytubefix():
    """Update pytubefix to the latest version"""
    try:
        print("🔄 Updating pytubefix to latest version...")
        print("This may help resolve YouTube throttling issues.")
        print()
        
        # First, uninstall current version
        print("📤 Uninstalling current pytubefix...")
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "pytubefix", "-y"], 
                      check=True)
        
        # Install latest version
        print("📥 Installing latest pytubefix...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pytubefix"], 
                      check=True)
        
        print()
        print("✅ PyTubeFix updated successfully!")
        print()
        print("💡 Additional tips to avoid throttling:")
        print("   • Wait a few minutes between downloads")
        print("   • Try different video URLs if issues persist")
        print("   • Use VPN if available")
        print("   • Restart the application after update")
        print()
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to update pytubefix: {e}")
        print("💡 Try running as administrator or check internet connection")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("   PyTubeFix Updater")
    print("=" * 50)
    print()
    
    success = update_pytubefix()
    
    print()
    input("Press Enter to exit...")