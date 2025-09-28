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
        self.geometry("650x600")  # Made taller to ensure buttons are visible
        self.resizable(False, False)
        self.minsize(650, 600)  # Ensure minimum size
        
        # Center the dialog
        self.transient(parent)
        self.grab_set()
        
        # Center window on parent
        self._center_window()
        
        # Setup UI
        self._setup_ui()
        
        # Focus on this window
        self.focus()
    
    def _center_window(self):
        """Center the dialog window on parent"""
        # Get parent window position and size
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Calculate center position
        window_width = 650
        window_height = 600
        x = parent_x + (parent_width // 2) - (window_width // 2)
        y = parent_y + (parent_height // 2) - (window_height // 2)
        
        # Set position
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def _setup_ui(self):
        """Setup the settings UI"""
        # Main container
        main_frame = ctk.CTkFrame(self, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Configure grid layout to ensure buttons are always visible
        main_frame.grid_rowconfigure(0, weight=0)  # Title - fixed size
        main_frame.grid_rowconfigure(1, weight=1)  # Content - expandable
        main_frame.grid_rowconfigure(2, weight=0)  # Buttons - fixed size
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Settings", 
            font=("Arial", 28, "bold")
        )
        title_label.grid(row=0, column=0, pady=(20, 10), sticky="ew")
        
        # Content area (scrollable if needed)
        content_frame = ctk.CTkScrollableFrame(main_frame)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
        
        # Theme Section
        self._setup_theme_section(content_frame)
        
        # Path Section
        self._setup_path_section(content_frame)
        
        # Buttons - always at the bottom
        self._setup_buttons(main_frame)
    
    def _setup_theme_section(self, parent):
        """Setup theme selection section"""
        theme_frame = ctk.CTkFrame(parent)
        theme_frame.pack(fill="x", pady=(10, 20))
        
        # Theme label
        theme_label = ctk.CTkLabel(
            theme_frame, 
            text="Theme", 
            font=("Arial", 18, "bold")
        )
        theme_label.pack(anchor="w", padx=20, pady=(20, 15))
        
        # Theme selection container
        theme_options_frame = ctk.CTkFrame(theme_frame, fg_color="transparent")
        theme_options_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Theme selection
        self.theme_var = ctk.StringVar(value=user_settings.get_theme())
        
        self.dark_radio = ctk.CTkRadioButton(
            theme_options_frame,
            text="Dark Theme",
            variable=self.theme_var,
            value="dark",
            font=("Arial", 16),
            radiobutton_width=25,
            radiobutton_height=25
        )
        self.dark_radio.pack(anchor="w", padx=20, pady=8)
        
        self.light_radio = ctk.CTkRadioButton(
            theme_options_frame,
            text="Light Theme", 
            variable=self.theme_var,
            value="light",
            font=("Arial", 16),
            radiobutton_width=25,
            radiobutton_height=25
        )
        self.light_radio.pack(anchor="w", padx=20, pady=8)
    
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
        path_label.pack(anchor="w", padx=20, pady=(20, 15))
        
        # Path container for entry and button
        path_container = ctk.CTkFrame(path_frame, fg_color="transparent")
        path_container.pack(fill="x", padx=20, pady=(0, 20))
        
        # Current path display (editable)
        self.path_var = ctk.StringVar(value=user_settings.get_download_path())
        self.path_entry = ctk.CTkEntry(
            path_container,
            textvariable=self.path_var,
            height=45,
            font=("Arial", 12),
            corner_radius=8
        )
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Browse button
        browse_button = ctk.CTkButton(
            path_container,
            text="Browse",
            command=self._browse_folder,
            height=45,
            width=100,
            font=("Arial", 14, "bold"),
            corner_radius=8,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        browse_button.pack(side="right")
    
    def _setup_buttons(self, parent):
        """Setup dialog buttons - always at bottom"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent", height=80)
        button_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 20))
        button_frame.grid_propagate(False)  # Maintain fixed height
        button_frame.grid_columnconfigure(0, weight=1)  # Center the buttons
        
        # Buttons container
        buttons_container = ctk.CTkFrame(button_frame, fg_color="transparent")
        buttons_container.pack(expand=True, fill="both")
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            buttons_container,
            text="Cancel",
            command=self._cancel,
            height=50,
            width=120,
            font=("Arial", 16, "bold"),
            corner_radius=12,
            fg_color="#666666",
            hover_color="#555555"
        )
        cancel_button.pack(side="right", padx=(10, 20), pady=15)
        
        # Apply/Save button - make it more prominent
        apply_button = ctk.CTkButton(
            buttons_container,
            text="💾 Save Settings",
            command=self._apply_settings,
            height=50,
            width=180,
            font=("Arial", 18, "bold"),
            corner_radius=12,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        apply_button.pack(side="right", padx=(0, 10), pady=15)
    
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
        print("🔧 Save Settings button clicked!")  # Debug print
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
            if new_theme != old_theme:
                try:
                    # Apply theme immediately
                    import customtkinter as ctk
                    ctk.set_appearance_mode(new_theme)
                    
                    # Also call the callback if provided
                    if self.on_theme_change:
                        self.on_theme_change(new_theme)
                    
                    # Force update of all widgets
                    self.parent.update_idletasks()
                    
                except Exception as theme_error:
                    print(f"Theme application error: {theme_error}")

            # Show different message based on theme change
            if new_theme != old_theme:
                messagebox.showinfo(
                    "Settings Saved", 
                    f"Settings saved successfully!\n\nTheme changed to: {new_theme.title()}\n\nNote: Some UI elements may require an app restart to fully apply the new theme."
                )
            else:
                messagebox.showinfo("Settings Saved", "Your settings have been saved successfully!")
            
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def _cancel(self):
        """Cancel and close dialog"""
        self.destroy()