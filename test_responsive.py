#!/usr/bin/env python3
"""
Test script for responsive UI features
"""

import customtkinter as ctk
from config.settings import APPEARANCE_MODE, COLOR_THEME
from gui import MainWindow

def main():
    """Test the responsive main window"""
    # Configure CustomTkinter
    ctk.set_appearance_mode(APPEARANCE_MODE)
    ctk.set_default_color_theme(COLOR_THEME)
    
    print("🚀 Starting Responsive YouTube Downloader...")
    print("\n📋 New Features:")
    print("✅ Resizable window (drag corners/edges)")
    print("✅ Minimize/Maximize buttons in header")
    print("✅ Keyboard shortcuts:")
    print("   - F11: Toggle fullscreen")
    print("   - Ctrl+-: Minimize")
    print("   - Ctrl++: Maximize/Restore")
    print("   - Alt+F4: Close with confirmation")
    print("✅ Auto-adapts layout for screen size")
    print("✅ Remembers window state between sessions")
    print("✅ Responsive playlist panel")
    print("\n🎨 Window will auto-size for your screen!")
    
    # Create and run the application
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()