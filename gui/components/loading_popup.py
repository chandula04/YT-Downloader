"""
Loading popup component for showing playlist loading progress
"""

import customtkinter as ctk
import threading
import time


class LoadingPopup(ctk.CTkToplevel):
    """Popup window for showing loading progress"""
    
    def __init__(self, parent, title="Loading", message="Loading videos..."):
        super().__init__(parent)
        
        self.parent = parent
        self.cancelled = False
        self._disabled_parent = False
        
        # Configure window
        self.title(title)
        self.geometry("400x250")
        self.resizable(False, False)
        
        # Make popup modal
        self.transient(parent)
        self.grab_set()
        # Also disable parent window to prevent accidental clicks causing freezes (Windows-specific)
        try:
            self.parent.attributes('-disabled', True)
            self._disabled_parent = True
        except:
            pass
        # When user clicks the X, treat as cancel and close
        try:
            self.protocol("WM_DELETE_WINDOW", self._on_close)
        except:
            pass
        
        # Center the popup
        self._center_window()
        
        # Keep on top
        self.lift()
        self.attributes('-topmost', True)
        
        # Setup UI
        self._setup_ui(message)
        
        # Variables for progress tracking
        self.current_video = 0
        self.total_videos = 0
        self.current_video_title = ""
        
    def _center_window(self):
        """Center the popup window on parent"""
        # Get parent window position and size
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Calculate center position
        popup_width = 400
        popup_height = 250
        x = parent_x + (parent_width - popup_width) // 2
        y = parent_y + (parent_height - popup_height) // 2
        
        self.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
    
    def _setup_ui(self, message):
        """Setup the popup UI"""
        # Main container
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Loading icon/animation
        self.loading_label = ctk.CTkLabel(
            main_frame,
            text="⏳",
            font=("Arial", 48),
            text_color="#4CAF50"
        )
        self.loading_label.pack(pady=(20, 10))
        
        # Main message
        self.message_label = ctk.CTkLabel(
            main_frame,
            text=message,
            font=("Arial", 16, "bold"),
            wraplength=350
        )
        self.message_label.pack(pady=(0, 10))
        
        # Progress info
        self.progress_label = ctk.CTkLabel(
            main_frame,
            text="Initializing...",
            font=("Arial", 12),
            text_color="#666666",
            wraplength=350
        )
        self.progress_label.pack(pady=(0, 5))
        
        # Current video info
        self.video_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=("Arial", 10),
            text_color="#888888",
            wraplength=350,
            height=40
        )
        self.video_label.pack(pady=(0, 15))
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(main_frame, width=300)
        self.progress_bar.pack(pady=(0, 15))
        self.progress_bar.set(0)
        
        # Cancel button
        self.cancel_button = ctk.CTkButton(
            main_frame,
            text="Cancel",
            command=self._cancel_loading,
            width=100,
            height=32,
            fg_color="#FF5722",
            hover_color="#E64A19"
        )
        self.cancel_button.pack()
        
        # Start loading animation
        self._start_loading_animation()
    
    def _start_loading_animation(self):
        """Start the loading animation"""
        self.animation_chars = ["⏳", "⌛", "⏳", "⌛"]
        self.animation_index = 0
        self._animate_loading()
    
    def _animate_loading(self):
        """Animate the loading icon"""
        if not self.cancelled and self.winfo_exists():
            try:
                self.loading_label.configure(text=self.animation_chars[self.animation_index])
                self.animation_index = (self.animation_index + 1) % len(self.animation_chars)
                self.after(500, self._animate_loading)
            except:
                pass  # Window might be destroyed
    
    def set_total_videos(self, total):
        """Set the total number of videos to process"""
        self.total_videos = total
        self.update_progress(0, f"Found {total} videos in playlist")
    
    def update_progress(self, current, status="", video_title=""):
        """Update the progress display"""
        if self.cancelled:
            return
            
        try:
            self.current_video = current
            self.current_video_title = video_title
            
            # Update progress bar
            if self.total_videos > 0:
                progress = current / self.total_videos
                self.progress_bar.set(progress)
            
            # Update progress label
            if self.total_videos > 0:
                self.progress_label.configure(
                    text=f"Processing video {current}/{self.total_videos}: {status}"
                )
            else:
                self.progress_label.configure(text=status)
            
            # Update current video info
            if video_title:
                # Truncate long titles
                display_title = video_title[:60] + "..." if len(video_title) > 60 else video_title
                self.video_label.configure(text=f"Loading: {display_title}")
            else:
                self.video_label.configure(text="")
            
            # Force update
            self.update_idletasks()
            
        except:
            pass  # Window might be destroyed
    
    def set_status(self, status):
        """Set a general status message"""
        try:
            self.progress_label.configure(text=status)
            self.update_idletasks()
        except:
            pass
    
    def _cancel_loading(self):
        """Cancel the loading process"""
        self.cancelled = True
        self.cancel_button.configure(text="Cancelling...", state="disabled")
        self.set_status("Cancelling playlist loading...")
        # Close immediately so user can continue; background thread sees the cancel flag
        self.close_popup()
    
    def is_cancelled(self):
        """Check if loading was cancelled"""
        return self.cancelled
    
    def close_popup(self):
        """Close the popup"""
        try:
            if self._disabled_parent:
                try:
                    self.parent.attributes('-disabled', False)
                except:
                    pass
            self.grab_release()
            self.destroy()
        except:
            pass

    def _on_close(self):
        """Handle window close (X button): cancel and close immediately"""
        try:
            if not self.cancelled:
                self.cancelled = True
            self.close_popup()
        except:
            pass
    
    def show_error(self, error_message):
        """Show error state in popup"""
        try:
            self.loading_label.configure(text="❌", text_color="#FF5722")
            self.message_label.configure(text="Error Loading Playlist")
            self.progress_label.configure(text=error_message)
            self.video_label.configure(text="")
            self.progress_bar.set(0)
            self.cancel_button.configure(text="Close", state="normal")
        except:
            pass
    
    def show_success(self, success_message):
        """Show success state in popup"""
        try:
            self.loading_label.configure(text="✅", text_color="#4CAF50")
            self.message_label.configure(text="Playlist Loaded Successfully!")
            self.progress_label.configure(text=success_message)
            self.video_label.configure(text="")
            self.progress_bar.set(1.0)
            self.cancel_button.configure(text="Close", state="normal")
        except:
            pass