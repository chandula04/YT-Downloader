#!/usr/bin/env python3
"""
Test script to verify settings dialog functionality
"""

import customtkinter as ctk
from config.settings import APPEARANCE_MODE, COLOR_THEME
from gui.components.settings_dialog import SettingsDialog
from config.user_settings import user_settings

def test_theme_change(theme):
    """Test callback for theme changes"""
    print(f"🎨 Theme changed to: {theme}")
    ctk.set_appearance_mode(theme)

def main():
    """Test the settings dialog"""
    # Configure CustomTkinter
    ctk.set_appearance_mode(APPEARANCE_MODE)
    ctk.set_default_color_theme(COLOR_THEME)
    
    # Create main window
    root = ctk.CTk()
    root.title("Settings Test")
    root.geometry("400x300")
    
    # Add test button
    def open_settings():
        settings_dialog = SettingsDialog(root, on_theme_change=test_theme_change)
    
    test_button = ctk.CTkButton(
        root,
        text="Open Settings Dialog",
        command=open_settings,
        font=("Arial", 16, "bold"),
        height=50
    )
    test_button.pack(expand=True)
    
    # Show current settings
    info_label = ctk.CTkLabel(
        root,
        text=f"Current Theme: {user_settings.get_theme()}\nCurrent Path: {user_settings.get_download_path()}",
        font=("Arial", 12)
    )
    info_label.pack(pady=20)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()