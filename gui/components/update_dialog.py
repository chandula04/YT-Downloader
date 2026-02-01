"""
Update notification dialog for application updates
"""

import customtkinter as ctk
from tkinter import messagebox
import threading


class UpdateDialog(ctk.CTkToplevel):
    """Dialog to notify users about available updates"""
    
    def __init__(self, parent, current_version, new_version, release_notes, updater):
        super().__init__(parent)
        
        print(f"🎨 UpdateDialog initializing...")
        print(f"   - Current version: {current_version}")
        print(f"   - New version: {new_version}")
        print(f"   - Updater: {updater}")
        print(f"   - Updater download_url: {getattr(updater, 'download_url', 'NOT SET')}")
        
        self.parent = parent
        self.current_version = current_version
        self.new_version = new_version
        self.release_notes = release_notes
        self.updater = updater
        self.downloaded_file = None
        
        # Verify updater has download URL
        if not hasattr(updater, 'download_url') or not updater.download_url:
            print("⚠️ WARNING: Updater has no download_url!")
        
        # Window setup
        self.title("Update Available")
        self.geometry("600x500")
        self.resizable(False, False)
        
        # Center on parent
        self.transient(parent)
        self.grab_set()
        self._center_window()
        
        # Setup UI
        self._setup_ui()
        
        self.focus()
        print("✅ UpdateDialog initialized successfully")
    
    def _center_window(self):
        """Center dialog on parent"""
        self.update_idletasks()
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        width = 600
        height = 500
        
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def _setup_ui(self):
        """Setup the dialog UI"""
        # Header
        header = ctk.CTkFrame(self, fg_color="#4CAF50", corner_radius=0)
        header.pack(fill="x", pady=(0, 20))
        
        icon_label = ctk.CTkLabel(
            header,
            text="🔔",
            font=("Arial", 48)
        )
        icon_label.pack(pady=(20, 10))
        
        title_label = ctk.CTkLabel(
            header,
            text="Update Available!",
            font=("Arial", 24, "bold"),
            text_color="white"
        )
        title_label.pack(pady=(0, 20))
        
        # Content
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        # Version info
        version_frame = ctk.CTkFrame(content_frame)
        version_frame.pack(fill="x", pady=(0, 15))
        
        current_label = ctk.CTkLabel(
            version_frame,
            text=f"Current Version: {self.current_version}",
            font=("Arial", 14),
            anchor="w"
        )
        current_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        new_label = ctk.CTkLabel(
            version_frame,
            text=f"New Version: {self.new_version}",
            font=("Arial", 16, "bold"),
            text_color="#4CAF50",
            anchor="w"
        )
        new_label.pack(anchor="w", padx=20, pady=(5, 15))
        
        # Release notes
        notes_label = ctk.CTkLabel(
            content_frame,
            text="What's New:",
            font=("Arial", 16, "bold"),
            anchor="w"
        )
        notes_label.pack(anchor="w", pady=(0, 10))
        
        self.notes_box = ctk.CTkTextbox(
            content_frame,
            height=150,
            font=("Arial", 12),
            wrap="word"
        )
        self.notes_box.pack(fill="both", expand=True, pady=(0, 15))
        self.notes_box.insert("1.0", self.release_notes)
        self.notes_box.configure(state="disabled")
        
        # Progress bar (initially hidden)
        self.progress_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="",
            font=("Arial", 12)
        )
        self.progress_label.pack(pady=(0, 5))
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.pack(fill="x")
        self.progress_bar.set(0)
        
        # Buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        self.update_button = ctk.CTkButton(
            button_frame,
            text="⬇️ Download & Install Update",
            command=self._start_update,
            height=45,
            font=("Arial", 14, "bold"),
            fg_color="#4CAF50",
            hover_color="#45a049",
            corner_radius=8
        )
        self.update_button.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Later",
            command=self.destroy,
            height=45,
            width=120,
            font=("Arial", 14),
            fg_color="#666666",
            hover_color="#555555",
            corner_radius=8
        )
        cancel_button.pack(side="right")
    
    def _start_update(self):
        """Start the update process"""
        print("🔄 Update button clicked - starting download...")
        self.update_button.configure(state="disabled", text="Downloading...")
        self.progress_frame.pack(fill="x", pady=(0, 15), before=self.update_button.master)
        
        # Force UI update
        self.update_idletasks()
        
        # Start download in background thread
        threading.Thread(target=self._download_and_install, daemon=True).start()
    
    def _download_and_install(self):
        """Download and install update (background thread)"""
        try:
            print("📥 Starting download thread...")
            # Download with progress callback
            def progress_callback(downloaded, total, percentage):
                self.after(0, lambda d=downloaded, t=total, p=percentage: self._update_progress(d, t, p))
            
            print(f"⬇️ Calling updater.download_update()...")
            downloaded_file = self.updater.download_update(progress_callback)
            print(f"📦 Download result: {downloaded_file}")
            
            if downloaded_file:
                self.downloaded_file = downloaded_file
                self.after(0, self._install_update)
            else:
                self.after(0, self._download_failed)
        except Exception as e:
            print(f"❌ Download exception: {e}")
            import traceback
            traceback.print_exc()
            self.after(0, lambda: self._download_failed_with_error(str(e)))
    
    def _update_progress(self, downloaded, total, percentage):
        """Update progress bar"""
        self.progress_bar.set(percentage / 100)
        size_mb = downloaded / (1024 * 1024)
        total_mb = total / (1024 * 1024)
        self.progress_label.configure(
            text=f"Downloading: {size_mb:.1f} MB / {total_mb:.1f} MB ({percentage:.1f}%)"
        )
    
    def _install_update(self):
        """Install the downloaded update"""
        self.progress_label.configure(text="✅ Download complete! Installing...")
        self.update_button.configure(text="Installing...")
        
        # Auto-install without confirmation for smoother UX
        self.after(500, self._do_install)
    
    def _do_install(self):
        """Perform the actual installation"""
        # Apply update (this will close the app)
        success = self.updater.apply_update(self.downloaded_file)
        if success:
            # Show brief success message
            self.progress_label.configure(text="✨ Update installed! Restarting...")
            self.update_idletasks()
            # Close the entire application after brief delay
            self.after(1000, self.parent.quit)
        else:
            messagebox.showerror(
                "Update Failed",
                "Failed to install update. Please try updating manually.",
                parent=self
            )
            self.destroy()
    
    def _download_failed(self):
        """Handle download failure"""
        print("❌ Download failed - no file returned")
        self.update_button.configure(state="normal", text="⬇️ Download & Install Update")
        self.progress_frame.pack_forget()
        
        messagebox.showerror(
            "Download Failed",
            "Failed to download the update.\n\n"
            "Please check your internet connection and try again,\n"
            "or download manually from GitHub.",
            parent=self
        )
    
    def _download_failed_with_error(self, error_msg):
        """Handle download failure with specific error"""
        print(f"❌ Download failed with error: {error_msg}")
        self.update_button.configure(state="normal", text="⬇️ Download & Install Update")
        self.progress_frame.pack_forget()
        
        messagebox.showerror(
            "Download Failed",
            f"Failed to download the update.\n\n"
            f"Error: {error_msg}\n\n"
            "Please check your internet connection and try again,\n"
            "or download manually from GitHub.",
            parent=self
        )
