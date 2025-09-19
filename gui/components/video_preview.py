"""
Video preview component for displaying video information and thumbnail
"""

import customtkinter as ctk
from customtkinter import CTkImage
from utils.helpers import format_time
from utils.network import network_manager


class VideoPreview(ctk.CTkFrame):
    """Video preview widget showing thumbnail and video information"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="#2B2B2B", corner_radius=10, **kwargs)
        
        # Initially hidden
        self.pack_forget()
        
        self._setup_ui()
        self._current_image = None
    
    def _setup_ui(self):
        """Set up the UI components"""
        # Header
        self.preview_header = ctk.CTkLabel(
            self, text="Video Preview", 
            font=("Arial", 16, "bold")
        )
        self.preview_header.pack(anchor="w", padx=20, pady=(15, 10))
        
        # Content container
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Thumbnail (larger size)
        self.thumbnail_label = ctk.CTkLabel(
            self.content_frame, 
            text="No video loaded", 
            width=120, height=90, 
            fg_color="#3B3B3B", 
            corner_radius=10
        )
        self.thumbnail_label.pack(side="left", padx=(0, 15))
        
        # Video info container
        self.info_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.info_frame.pack(side="left", fill="both", expand=True)
        
        # Video title
        self.title_label = ctk.CTkLabel(
            self.info_frame, 
            text="", 
            font=("Arial", 16, "bold"), 
            wraplength=500, 
            anchor="w"
        )
        self.title_label.pack(anchor="w", pady=(0, 5))
        
        # Channel and duration info
        self.channel_label = ctk.CTkLabel(
            self.info_frame, 
            text="", 
            font=("Arial", 14), 
            text_color="#AAAAAA", 
            anchor="w"
        )
        self.channel_label.pack(anchor="w")
    
    def update_video_info(self, video_info, thumbnail_image=None):
        """
        Update the preview with video information
        
        Args:
            video_info (dict): Dictionary containing video information
            thumbnail_image (PIL.Image, optional): Thumbnail image
        """
        # Show the preview
        self.pack(fill="x", pady=10)
        
        # Update labels
        self.title_label.configure(text=video_info.get('title', 'Unknown Title'))
        
        author = video_info.get('author', 'Unknown')
        length = video_info.get('length', 0)
        duration_str = format_time(length) if length else "00:00"
        self.channel_label.configure(text=f"{author} • {duration_str}")
        
        # Update thumbnail
        if thumbnail_image:
            try:
                ctk_img = CTkImage(
                    light_image=thumbnail_image, 
                    dark_image=thumbnail_image, 
                    size=(120, 90)
                )
                self.thumbnail_label.configure(image=ctk_img, text="")
                # Keep reference to prevent garbage collection
                self._current_image = ctk_img
            except Exception as e:
                print(f"Error setting thumbnail: {e}")
                self.thumbnail_label.configure(image=None, text="No thumbnail")
        else:
            self.thumbnail_label.configure(image=None, text="No thumbnail")
    
    def clear_preview(self):
        """Clear the video preview"""
        self.pack_forget()
        self.title_label.configure(text="")
        self.channel_label.configure(text="")
        self.thumbnail_label.configure(image=None, text="No video loaded")
        self._current_image = None