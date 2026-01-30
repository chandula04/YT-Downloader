"""
Video preview component for displaying video information and thumbnail
"""

import customtkinter as ctk
from customtkinter import CTkImage
from PIL import ImageOps
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
            'border': "#C8C8C8",             # Light border
        }
    else:
        return {
            'frame_bg': "#2B2B2B",           # Dark frame background
            'secondary_bg': "#3B3B3B",       # Dark secondary background  
            'text_primary': "#FFFFFF",       # Light text for dark mode
            'text_secondary': "#AAAAAA",     # Secondary text for dark mode
            'border': "#4A4A4A",             # Dark border
        }


class VideoPreview(ctk.CTkFrame):
    """Video preview widget showing thumbnail and video information"""
    
    def __init__(self, parent, **kwargs):
        colors = get_theme_colors()
        self.thumbnail_size = (200, 150)
        super().__init__(
            parent,
            fg_color=colors['frame_bg'],
            corner_radius=10,
            border_width=1,
            border_color=colors['border'],
            **kwargs
        )
        
        # Initially hidden
        self.pack_forget()

        # Default pack options (can be overridden by parent layout)
        self._pack_options = {"fill": "x", "pady": 10}
        
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
        
        # Thumbnail container with border
        self.thumbnail_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=colors['secondary_bg'],
            corner_radius=8,
            border_width=1,
            border_color=colors['border'],
            width=self.thumbnail_size[0],
            height=self.thumbnail_size[1]
        )
        self.thumbnail_frame.pack(side="left", padx=(0, 25))  # More spacing
        self.thumbnail_frame.pack_propagate(False)

        # Thumbnail label inside bordered frame
        self.thumbnail_label = ctk.CTkLabel(
            self.thumbnail_frame,
            text="No video loaded",
            fg_color="transparent",
            font=("Arial", 14),
            text_color=colors['text_primary']  # Theme-aware text color
        )
        self.thumbnail_label.pack(fill="both", expand=True)
        
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
        self.pack(**self._pack_options)
        
        # Update labels
        self.title_label.configure(text=video_info.get('title', 'Unknown Title'))
        
        author = video_info.get('author', 'Unknown')
        length = video_info.get('length', 0)
        duration_str = format_time(length) if length else "00:00"
        self.channel_label.configure(text=f"{author} • {duration_str}")
        
        # Update thumbnail
        if thumbnail_image:
            try:
                fitted_image = ImageOps.contain(thumbnail_image, self.thumbnail_size)
                ctk_img = CTkImage(
                    light_image=fitted_image, 
                    dark_image=fitted_image, 
                    size=fitted_image.size
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
        self.configure(fg_color=colors['frame_bg'], border_color=colors['border'])
        
        # Update header text color
        if hasattr(self, 'preview_header'):
            self.preview_header.configure(text_color=colors['text_primary'])
        
        # Update thumbnail background
        if hasattr(self, 'thumbnail_frame'):
            self.thumbnail_frame.configure(
                fg_color=colors['secondary_bg'],
                border_color=colors['border']
            )
        if hasattr(self, 'thumbnail_label'):
            self.thumbnail_label.configure(
                text_color=colors['text_primary']
            )

    def set_pack_options(self, **options):
        """Set pack options for preview placement"""
        self._pack_options = options
