"""
Settings dialog window for user configuration
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from config.user_settings import user_settings


class SettingsDialog(ctk.CTkToplevel):
    """Settings dialog window"""
    
    def __init__(self, parent, on_theme_change=None):
        super().__init__(parent)
        
        self.parent = parent
        self.on_theme_change = on_theme_change
        
        # Window setup
        self.title("Settings")
        self.geometry("500x400")
        self.resizable(False, False)
        
        # Center the dialog
        self.transient(parent)
        self.grab_set()
        
        # Setup UI
        self._setup_ui()
        
        # Focus on this window
        self.focus()
    
    def _setup_ui(self):
        """Setup the settings UI"""
        # Main container
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Settings", 
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Theme Section
        self._setup_theme_section(main_frame)
        
        # Path Section
        self._setup_path_section(main_frame)
        
        # Buttons
        self._setup_buttons(main_frame)
    
    def _setup_theme_section(self, parent):
        """Setup theme selection section"""
        theme_frame = ctk.CTkFrame(parent)
        theme_frame.pack(fill="x", pady=(0, 20))
        
        # Theme label
        theme_label = ctk.CTkLabel(
            theme_frame, 
            text="Theme", 
            font=("Arial", 18, "bold")
        )
        theme_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Theme selection
        self.theme_var = ctk.StringVar(value=user_settings.get_theme())
        
        self.dark_radio = ctk.CTkRadioButton(
            theme_frame,
            text="Dark Theme",
            variable=self.theme_var,
            value="dark",
            font=("Arial", 14)
        )
        self.dark_radio.pack(anchor="w", padx=40, pady=5)
        
        self.light_radio = ctk.CTkRadioButton(
            theme_frame,
            text="Light Theme", 
            variable=self.theme_var,
            value="light",
            font=("Arial", 14)
        )
        self.light_radio.pack(anchor="w", padx=40, pady=(5, 20))
    
    def _setup_path_section(self, parent):
        """Setup download path section"""
        path_frame = ctk.CTkFrame(parent)
        path_frame.pack(fill="x", pady=(0, 20))
        
        # Path label
        path_label = ctk.CTkLabel(
            path_frame, 
            text="Download Path", 
            font=("Arial", 18, "bold")
        )
        path_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Current path display
        self.path_var = ctk.StringVar(value=user_settings.get_download_path())
        self.path_entry = ctk.CTkEntry(
            path_frame,
            textvariable=self.path_var,
            height=40,
            font=("Arial", 12),
            state="readonly"
        )
        self.path_entry.pack(fill="x", padx=20, pady=(0, 10))
        
        # Browse button
        browse_button = ctk.CTkButton(
            path_frame,
            text="Browse Folder",
            command=self._browse_folder,
            height=40,
            font=("Arial", 14)
        )
        browse_button.pack(anchor="w", padx=20, pady=(0, 20))
    
    def _setup_buttons(self, parent):
        """Setup dialog buttons"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", pady=(10, 0))
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self._cancel,
            height=40,
            font=("Arial", 14),
            fg_color="#666666",
            hover_color="#555555"
        )
        cancel_button.pack(side="right", padx=(10, 0))
        
        # Apply button
        apply_button = ctk.CTkButton(
            button_frame,
            text="Apply",
            command=self._apply_settings,
            height=40,
            font=("Arial", 14)
        )
        apply_button.pack(side="right")
    
    def _browse_folder(self):
        """Browse for download folder"""
        folder = filedialog.askdirectory(
            title="Select Download Folder",
            initialdir=user_settings.get_download_path()
        )
        
        if folder:
            self.path_var.set(folder)
    
    def _apply_settings(self):
        """Apply the settings"""
        try:
            # Save theme
            new_theme = self.theme_var.get()
            old_theme = user_settings.get_theme()
            user_settings.set_theme(new_theme)
            
            # Save path
            new_path = self.path_var.get()
            user_settings.set_download_path(new_path)
            
            # Ensure download path exists
            if not user_settings.ensure_download_path_exists():
                messagebox.showwarning(
                    "Warning", 
                    "Could not create the download folder. Please check the path."
                )
            
            # Apply theme change if needed
            if new_theme != old_theme and self.on_theme_change:
                self.on_theme_change(new_theme)
            
            messagebox.showinfo("Success", "Settings saved successfully!")
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def _cancel(self):
        """Cancel and close dialog"""
        self.destroy()