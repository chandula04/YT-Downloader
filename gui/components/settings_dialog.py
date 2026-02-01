"""
Settings dialog window for user configuration
"""

import sys
import customtkinter as ctk
import threading
from tkinter import filedialog, messagebox
from config.user_settings import user_settings
from config.settings import COLORS, APP_VERSION
from utils.update_manager import update_download_libraries_stream
from utils.app_updater import AppUpdater


class SettingsDialog(ctk.CTkToplevel):
    """Settings dialog window"""
    
    def __init__(self, parent, on_theme_change=None, on_settings_saved=None, on_library_update_complete=None):
        super().__init__(parent)
        
        self.parent = parent
        self.on_theme_change = on_theme_change
        self.on_settings_saved = on_settings_saved
        self.on_library_update_complete = on_library_update_complete
        
        # Detect if running in portable mode (frozen exe)
        self.is_portable = getattr(sys, 'frozen', False)
        
        # Window setup
        self.title("Settings")
        self.geometry("760x700")  # Wider and taller for clarity
        self.resizable(False, False)
        self.minsize(760, 700)  # Ensure minimum size
        
        # Center the dialog
        self.transient(parent)
        self.grab_set()
        
        # Center window on parent
        self._center_window()
        
        # Setup UI
        self._setup_ui()
        
        # Auto-check for app updates when settings opens
        self.after(100, self._check_app_update)
        
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
        window_width = 760
        window_height = 700
        x = parent_x + (parent_width // 2) - (window_width // 2)
        y = parent_y + (parent_height // 2) - (window_height // 2)
        
        # Set position
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def _setup_ui(self):
        """Setup the settings UI"""
        # Main container
        main_frame = ctk.CTkFrame(self, corner_radius=0, border_width=0)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
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
        
        # App Updates Section (at the top)
        self._setup_app_update_section(content_frame)
        
        # Theme Section
        self._setup_theme_section(content_frame)
        
        # Path Section
        self._setup_path_section(content_frame)
        
        # Library Updates Section (only in development mode, not portable)
        if not self.is_portable:
            self._setup_update_section(content_frame)
        
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
    
    def _setup_app_update_section(self, parent):
        """Setup application updates section"""
        app_update_frame = ctk.CTkFrame(parent, fg_color="#2B5329", border_width=2, border_color="#4CAF50")
        app_update_frame.pack(fill="x", pady=(10, 20))
        
        section_label = ctk.CTkLabel(
            app_update_frame,
            text="🚀 App Updates",
            font=("Arial", 18, "bold"),
            text_color="#81C784"
        )
        section_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Current version display
        version_label = ctk.CTkLabel(
            app_update_frame,
            text=f"Current Version: {APP_VERSION}",
            font=("Arial", 14),
            text_color="white"
        )
        version_label.pack(anchor="w", padx=20, pady=(0, 10))
        
        # Status label
        self.app_update_status = ctk.CTkLabel(
            app_update_frame,
            text="Checking for updates...",
            font=("Arial", 12),
            text_color="#A0A0A0"
        )
        self.app_update_status.pack(anchor="w", padx=20, pady=(0, 15))
        
        # Button row
        button_row = ctk.CTkFrame(app_update_frame, fg_color="transparent")
        button_row.pack(fill="x", padx=20, pady=(0, 10))
        
        self.check_app_update_button = ctk.CTkButton(
            button_row,
            text="🔄 Check for Updates",
            height=40,
            width=180,
            font=("Arial", 14, "bold"),
            corner_radius=8,
            fg_color="#4CAF50",
            hover_color="#45a049",
            command=self._check_app_update
        )
        self.check_app_update_button.pack(side="left")
        
        self.install_app_update_button = ctk.CTkButton(
            button_row,
            text="⬇️ Install Update",
            height=40,
            width=160,
            font=("Arial", 14, "bold"),
            corner_radius=8,
            fg_color="#FF9800",
            hover_color="#F57C00",
            command=self._start_download
        )
        # Initially hidden
        
        # Progress bar (hidden initially)
        self.update_progress_frame = ctk.CTkFrame(app_update_frame, fg_color="transparent")
        
        self.update_progress_label = ctk.CTkLabel(
            self.update_progress_frame,
            text="",
            font=("Arial", 12),
            text_color="#A0A0A0"
        )
        self.update_progress_label.pack(pady=(0, 5))
        
        self.update_progress_bar = ctk.CTkProgressBar(self.update_progress_frame)
        self.update_progress_bar.pack(fill="x", padx=20, pady=(0, 10))
        self.update_progress_bar.set(0)
        
        # Restart button (hidden initially)
        self.restart_button = ctk.CTkButton(
            app_update_frame,
            text="🔄 Restart Now",
            height=45,
            font=("Arial", 16, "bold"),
            corner_radius=8,
            fg_color="#4CAF50",
            hover_color="#45a049",
            command=self._restart_app
        )
        
        self.app_updater = None
        self.app_update_info = None
        self.downloaded_file = None
    
    def _check_app_update(self):
        """Check for application updates"""
        self.check_app_update_button.configure(state="disabled", text="Checking...")
        self.app_update_status.configure(text="Checking for updates...", text_color="#A0A0A0")
        
        def worker():
            try:
                updater = AppUpdater()
                has_update, new_version, release_notes = updater.check_for_updates()
                self.after(0, lambda: self._show_app_update_result(has_update, new_version, release_notes, updater))
            except Exception as e:
                self.after(0, lambda: self._show_app_update_error(str(e)))
        
        threading.Thread(target=worker, daemon=True).start()
    
    def _show_app_update_result(self, has_update, new_version, release_notes, updater):
        """Show app update check result"""
        self.check_app_update_button.configure(state="normal", text="🔄 Check for Updates")
        
        if has_update:
            self.app_updater = updater
            self.app_update_info = {'version': new_version, 'notes': release_notes}
            self.app_update_status.configure(
                text=f"✨ New version available: v{new_version}",
                text_color="#81C784"
            )
            self.install_app_update_button.pack(side="left", padx=(10, 0))
        else:
            self.app_update_status.configure(
                text=f"✅ You're up to date! (v{APP_VERSION})",
                text_color="#81C784"
            )
            self.install_app_update_button.pack_forget()
    
    def _show_app_update_error(self, error):
        """Show app update check error"""
        self.check_app_update_button.configure(state="normal", text="🔄 Check for Updates")
        self.app_update_status.configure(
            text=f"❌ Failed to check for updates: {error}",
            text_color="#F44336"
        )
    
    def _start_download(self):
        """Start downloading update in Settings"""
        if not self.app_updater or not self.app_update_info:
            print("❌ No updater or update info available")
            return
        
        if not self.app_updater.download_url:
            messagebox.showerror(
                "Error",
                "Download URL not available.\n\nPlease check for updates again.",
                parent=self
            )
            return
        
        # Hide buttons, show progress
        self.check_app_update_button.pack_forget()
        self.install_app_update_button.pack_forget()
        self.update_progress_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.app_update_status.configure(text="Downloading update...", text_color="#FF9800")
        
        # Start download in thread
        threading.Thread(target=self._download_update, daemon=True).start()
    
    def _download_update(self):
        """Download update in background thread"""
        try:
            print("📥 Starting download thread...")
            
            def progress_callback(downloaded, total, percentage):
                self.after(0, lambda d=downloaded, t=total, p=percentage: 
                          self._update_download_progress(d, t, p))
            
            downloaded_file = self.app_updater.download_update(progress_callback)
            
            if downloaded_file:
                self.downloaded_file = downloaded_file
                self.after(0, self._download_complete)
            else:
                self.after(0, self._download_failed)
        except Exception as e:
            print(f"❌ Download exception: {e}")
            import traceback
            traceback.print_exc()
            self.after(0, lambda: self._download_failed(str(e)))
    
    def _update_download_progress(self, downloaded, total, percentage):
        """Update progress bar in Settings"""
        self.update_progress_bar.set(percentage / 100)
        size_mb = downloaded / (1024 * 1024)
        total_mb = total / (1024 * 1024)
        self.update_progress_label.configure(
            text=f"Downloading: {size_mb:.1f} MB / {total_mb:.1f} MB ({percentage:.1f}%)"
        )
    
    def _download_complete(self):
        """Handle download completion"""
        self.app_update_status.configure(text="✅ Download complete! Ready to install.", text_color="#81C784")
        self.update_progress_label.configure(text="✨ Update downloaded successfully!")
        self.update_progress_bar.set(1.0)
        
        # Hide progress, show restart button
        self.update_progress_frame.pack_forget()
        self.restart_button.pack(fill="x", padx=20, pady=(10, 20))
    
    def _download_failed(self, error=None):
        """Handle download failure"""
        # Show buttons again, hide progress
        self.update_progress_frame.pack_forget()
        self.check_app_update_button.pack(side="left")
        self.install_app_update_button.pack(side="left", padx=(10, 0))
        
        error_msg = f"Failed to download update.\n\n{error}" if error else "Failed to download update."
        self.app_update_status.configure(
            text=f"❌ {error_msg}",
            text_color="#F44336"
        )
        
        messagebox.showerror(
            "Download Failed",
            f"{error_msg}\n\nPlease check your internet connection and try again.",
            parent=self
        )
    
    def _restart_app(self):
        """Install update and restart app"""
        if not self.downloaded_file:
            return
        
        self.app_update_status.configure(text="Installing update...", text_color="#FF9800")
        self.restart_button.configure(state="disabled", text="Installing...")
        
        # Apply update
        success = self.app_updater.apply_update(self.downloaded_file)
        if success:
            # Close everything and let batch script restart
            self.master.quit()
        else:
            messagebox.showerror(
                "Update Failed",
                "Failed to install update. Please try updating manually.",
                parent=self
            )
            self.restart_button.configure(state="normal", text="🔄 Restart Now")
    
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
            corner_radius=8,
            border_width=0
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
            border_width=0,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        browse_button.pack(side="right")

    def _setup_update_section(self, parent):
        """Setup library updates section"""
        update_frame = ctk.CTkFrame(parent)
        update_frame.pack(fill="x", pady=(0, 20))

        section_label = ctk.CTkLabel(
            update_frame,
            text="Library Updates",
            font=("Arial", 18, "bold")
        )
        section_label.pack(anchor="w", padx=20, pady=(20, 10))

        auto_update_hint = ctk.CTkLabel(
            update_frame,
            text="Libraries are checked automatically on startup. Use the button below to update manually.",
            font=("Arial", 12),
            text_color="#A0A0A0",
            wraplength=680,
            justify="left"
        )
        auto_update_hint.pack(anchor="w", padx=20, pady=(0, 15))

        button_row = ctk.CTkFrame(update_frame, fg_color="transparent")
        button_row.pack(fill="x", padx=20, pady=(0, 10))

        self.update_button = ctk.CTkButton(
            button_row,
            text="🔄 Update Now",
            height=36,
            width=140,
            font=("Arial", 14, "bold"),
            corner_radius=8,
            command=self._run_library_update
        )
        self.update_button.pack(side="left")

        self.update_status = ctk.CTkLabel(
            button_row,
            text="",
            font=("Arial", 12),
            text_color="#A0A0A0"
        )
        self.update_status.pack(side="left", padx=(12, 0))

        self.update_log = ctk.CTkTextbox(update_frame, height=120)
        self.update_log.pack(fill="x", padx=20, pady=(0, 20))
        self.update_log.insert("end", "Ready to update libraries.\n")
        self.update_log.configure(state="disabled")

    def _run_library_update(self):
        """Run library update and stream output to the log."""
        self.update_button.configure(state="disabled")
        self.update_status.configure(text="Updating...")

        self.update_log.configure(state="normal")
        self.update_log.delete("1.0", "end")
        self.update_log.insert("end", "Starting update...\n")
        self.update_log.configure(state="disabled")

        def append_log(line: str):
            def _append():
                self.update_log.configure(state="normal")
                self.update_log.insert("end", line + "\n")
                self.update_log.see("end")
                self.update_log.configure(state="disabled")
            self.after(0, _append)

        def worker():
            ok, message = update_download_libraries_stream(progress_callback=append_log)

            def _done():
                self.update_status.configure(text=message)
                self.update_button.configure(state="normal")
                # Clear library notifications after successful update
                if ok and self.on_library_update_complete:
                    self.on_library_update_complete()
            self.after(0, _done)

        threading.Thread(target=worker, daemon=True).start()
    
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
            corner_radius=8,
            border_width=0,
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
            corner_radius=8,
            border_width=0,
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
            
            # Call the callback to update path display
            if self.on_settings_saved:
                self.on_settings_saved()
            
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def _cancel(self):
        """Cancel and close dialog"""
        self.destroy()