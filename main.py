"""
YouTube Downloader - Main Entry Point

A modern YouTube video and playlist downloader with a clean GUI interface.
Features include video quality selection, audio-only downloads, progress tracking,
and support for both individual videos and entire playlists.
"""

import customtkinter as ctk
from config.settings import APPEARANCE_MODE, COLOR_THEME
from gui import MainWindow


def main():
    """Main application entry point"""
    # Configure CustomTkinter appearance
    ctk.set_appearance_mode(APPEARANCE_MODE)
    ctk.set_default_color_theme(COLOR_THEME)
    
    # Print startup information
    print("🚀 YouTube Downloader - Responsive Edition")
    print("✨ Window Features: Resizable, Minimize/Maximize, Auto-sizing")
    
    # Create and run the main window
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()