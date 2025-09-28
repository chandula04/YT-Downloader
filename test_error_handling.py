#!/usr/bin/env python3
"""
Test script for improved playlist error handling
"""

import customtkinter as ctk
from config.settings import APPEARANCE_MODE, COLOR_THEME
from gui import MainWindow

def main():
    """Test the improved playlist error handling"""
    # Configure CustomTkinter
    ctk.set_appearance_mode(APPEARANCE_MODE)
    ctk.set_default_color_theme(COLOR_THEME)
    
    print("🛡️ YouTube Downloader - Enhanced Error Handling")
    print("\n🔧 Improvements:")
    print("✅ Better handling of restricted/private videos")
    print("✅ Multiple client fallback strategies")
    print("✅ Progress indication during playlist loading")
    print("✅ Error placeholders for inaccessible videos")
    print("✅ Improved user feedback and warnings")
    print("✅ Non-blocking error handling")
    
    print("\n📋 Playlist Handling:")
    print("• Pre-filters inaccessible videos")
    print("• Shows progress while loading")
    print("• Displays error items with reasons")
    print("• Continues processing despite individual failures")
    print("• Provides clear success/failure statistics")
    
    print("\n🎯 Testing Tips:")
    print("• Try playlists with mixed content types")
    print("• Test with playlists containing music videos")
    print("• Test with playlists having private/restricted videos")
    print("• Watch console output for detailed progress")
    
    # Create and run the application
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()