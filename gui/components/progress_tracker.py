"""
Progress tracking component for download progress display
"""

import customtkinter as ctk
from utils.helpers import format_size, format_time
from config.settings import COLORS


class ProgressTracker(ctk.CTkFrame):
    """Component for tracking and displaying download progress"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self._setup_ui()
        self.reset()
        
        # Batch download state
        self.is_batch_mode = False
        self.batch_info = {"current": 0, "total": 0, "current_title": ""}
    
    def _setup_ui(self):
        """Set up the UI components"""
        # Batch progress info (for multiple downloads)
        self.batch_info_label = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 12, "bold"),
            text_color=COLORS['primary']
        )
        # Initially hidden
        self.batch_info_label.pack_forget()
        
        # Current video info (for batch downloads)
        self.current_video_label = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 11),
            text_color=COLORS['text_secondary']
        )
        # Initially hidden
        self.current_video_label.pack_forget()
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self, 
            height=12, 
            progress_color=COLORS['primary']
        )
        self.progress_bar.pack(fill="x", pady=(5, 10))
        
        # Progress information
        self.info_label = ctk.CTkLabel(
            self, 
            text="Ready to download", 
            font=("Arial", 14), 
            text_color=COLORS['text_secondary']
        )
        self.info_label.pack(anchor="w")
    
    def set_batch_mode(self, enabled, current=0, total=0):
        """
        Enable or disable batch download mode
        
        Args:
            enabled (bool): Whether batch mode is enabled
            current (int): Current video number
            total (int): Total videos in batch
        """
        self.is_batch_mode = enabled
        self.batch_info = {"current": current, "total": total, "current_title": ""}
        
        if enabled:
            self.batch_info_label.pack(anchor="w", pady=(0, 5))
            self.current_video_label.pack(anchor="w", pady=(0, 5))
            self.update_batch_info(current, total)
        else:
            self.batch_info_label.pack_forget()
            self.current_video_label.pack_forget()
    
    def update_batch_info(self, current, total, current_title=""):
        """
        Update batch download information
        
        Args:
            current (int): Current video number
            total (int): Total videos in batch
            current_title (str): Title of current video
        """
        self.batch_info = {"current": current, "total": total, "current_title": current_title}
        
        if self.is_batch_mode:
            self.batch_info_label.configure(
                text=f"Batch Download: {current}/{total} videos"
            )
            
            if current_title:
                # Truncate long titles
                display_title = current_title if len(current_title) <= 50 else current_title[:47] + "..."
                self.current_video_label.configure(
                    text=f"Current: {display_title}"
                )
            else:
                self.current_video_label.configure(text="")
    
    def update_progress(self, downloaded, total, percentage, speed, elapsed, custom_text=None):
        """
        Update the progress display
        
        Args:
            downloaded (int): Bytes downloaded
            total (int): Total bytes to download
            percentage (float): Download percentage
            speed (float): Download speed in MB/s
            elapsed (int): Elapsed time in seconds
            custom_text (str, optional): Custom text to display instead of default
        """
        # Update progress bar
        self.progress_bar.set(percentage / 100)
        
        # Update info text
        if custom_text:
            self.info_label.configure(text=custom_text)
        elif total > 0:
            base_info = f"Elapsed: {format_time(elapsed)} Size: {format_size(total)} Speed: {speed:.1f} MB/s"
            
            # Add batch info if in batch mode
            if self.is_batch_mode and self.batch_info["current"] > 0:
                batch_prefix = f"[{self.batch_info['current']}/{self.batch_info['total']}] "
                self.info_label.configure(text=batch_prefix + base_info)
            else:
                self.info_label.configure(text=base_info)
        else:
            self.info_label.configure(text="Preparing download...")
    
    def reset(self):
        """Reset progress to initial state"""
        self.progress_bar.set(0)
        self.info_label.configure(text="Ready to download", text_color=COLORS['text_secondary'])
        self.set_batch_mode(False)
    
    def set_error(self, error_message):
        """
        Display error message
        
        Args:
            error_message (str): Error message to display
        """
        self.info_label.configure(
            text=f"Error: {error_message}", 
            text_color=COLORS['danger']
        )
    
    def set_success(self, success_message):
        """
        Display success message
        
        Args:
            success_message (str): Success message to display
        """
        self.progress_bar.set(1.0)  # Full progress
        self.info_label.configure(
            text=success_message, 
            text_color=COLORS['primary']
        )
    
    def set_status(self, status_text):
        """
        Set a custom status message
        
        Args:
            status_text (str): Status message to display
        """
        self.info_label.configure(text=status_text)