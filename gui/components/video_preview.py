"""
Video preview component for displaying video information and thumbnail
"""

import customtkinter as ctk
from customtkinter import CTkImage
from utils.helpers import format_time
from utils.network import network_manager


def get_theme_colors():
    """Get colors based on current appearance mode"""
    appearance_mode = ctk.get_appearance_mode()
    
    if appearance_mode == "Light":
        return {
            'frame_bg': "#F0F0F0",           # Light frame background
            'secondary_bg': "#E0E0E0",       # Light secondary background
            'text_primary': "#000000",       # Dark text for light mode
            'text_secondary': "#666666",     # Secondary text for light mode
        }
    else:
        return {
            'frame_bg': "#2B2B2B",           # Dark frame background
            'secondary_bg': "#3B3B3B",       # Dark secondary background  
            'text_primary': "#FFFFFF",       # Light text for dark mode
            'text_secondary': "#AAAAAA",     # Secondary text for dark mode
        }


class VideoPreview(ctk.CTkFrame):
    """Video preview widget showing thumbnail and video information"""
    
    def __init__(self, parent, **kwargs):
        colors = get_theme_colors()
        super().__init__(parent, fg_color=colors['frame_bg'], corner_radius=10, **kwargs)
        
        # Initially hidden
        self.pack_forget()
        
        self._setup_ui()
        self._current_image = None
    
    def _setup_ui(self):
        """Set up the UI components"""
        colors = get_theme_colors()
        
        # Header with larger text
        self.preview_header = ctk.CTkLabel(
            self, text="Video Preview", 
            font=("Arial", 20, "bold"),  # Larger header
            text_color=colors['text_primary']  # Theme-aware text color
        )
        self.preview_header.pack(anchor="w", padx=25, pady=(20, 15))  # More padding
        
        # Content container with more spacing
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=25, pady=(0, 20))  # More padding
        
        # Thumbnail (much larger size for better visibility)
        self.thumbnail_label = ctk.CTkLabel(
            self.content_frame, 
            text="No video loaded", 
            width=200, height=150,  # Significantly larger thumbnail
            fg_color=colors['secondary_bg'],  # Theme-aware background
            corner_radius=12,
            font=("Arial", 14),
            text_color=colors['text_primary']  # Theme-aware text color
        )
        self.thumbnail_label.pack(side="left", padx=(0, 25))  # More spacing
        
        # Video info container
        self.info_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.info_frame.pack(side="left", fill="both", expand=True)
        
        # Video title with larger font
        self.title_label = ctk.CTkLabel(
            self.info_frame, 
            text="", 
            font=("Arial", 18, "bold"),  # Larger title font
            wraplength=600,  # Wider wrap
            anchor="w",
            justify="left",
            text_color=colors['text_primary']  # Theme-aware text color
        )
        self.title_label.pack(anchor="w", pady=(0, 10))  # More spacing
        
        # Channel and duration info with larger font
        self.channel_label = ctk.CTkLabel(
            self.info_frame, 
            text="", 
            font=("Arial", 16),  # Larger font
            text_color=colors['text_secondary'],  # Theme-aware secondary text
            anchor="w",
            justify="left"
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
    
    def refresh_theme(self):
        """Refresh colors when theme changes"""
        colors = get_theme_colors()
        
        # Update main frame background
        self.configure(fg_color=colors['frame_bg'])
        
        # Update header text color
        if hasattr(self, 'preview_header'):
            self.preview_header.configure(text_color=colors['text_primary'])
        
        # Update thumbnail background
        if hasattr(self, 'thumbnail_label'):
            self.thumbnail_label.configure(
                fg_color=colors['secondary_bg'],
                text_color=colors['text_primary']
            )
        
        # Update title text color
        if hasattr(self, 'title_label'):
            self.title_label.configure(text_color=colors['text_primary'])
        
        # Update channel text color
        if hasattr(self, 'channel_label'):
            self.channel_label.configure(text_color=colors['text_secondary'])
        
        # Force update
        self.update_idletasks()