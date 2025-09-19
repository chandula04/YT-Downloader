"""
Playlist panel component for displaying playlist information with selection controls
"""

import customtkinter as ctk
from customtkinter import CTkImage
from utils.helpers import safe_filename, format_time, resolution_key
from utils.network import network_manager


class PlaylistPanel(ctk.CTkFrame):
    """Panel for displaying playlist information and items with selection controls"""
    
    def __init__(self, parent, width=700, **kwargs):  # Increased to match user's marked area
        super().__init__(parent, width=width, **kwargs)
        
        # Initially hidden using grid_forget instead of pack_forget
        self.grid_forget()
        
        # Selection state
        self.video_items = []  # List of video item widgets
        self.select_all_var = ctk.BooleanVar()
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the UI components"""
        # Header
        self.header_label = ctk.CTkLabel(
            self, 
            text="Playlist", 
            font=("Arial", 18, "bold")  # Larger header
        )
        self.header_label.pack(anchor="w", padx=15, pady=(15, 10))  # Increased padding
        
        # Selection controls
        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.pack(fill="x", padx=15, pady=(0, 15))  # Increased padding
        
        # Select All checkbox (larger)
        self.select_all_checkbox = ctk.CTkCheckBox(
            self.controls_frame,
            text="Select All",
            variable=self.select_all_var,
            command=self._on_select_all,
            font=("Arial", 14, "bold")  # Larger font
        )
        self.select_all_checkbox.pack(side="left")
        
        # Selected count label (larger and more prominent)
        self.count_label = ctk.CTkLabel(
            self.controls_frame,
            text="0 selected",
            font=("Arial", 12),  # Larger font
            text_color="#CCCCCC"  # Brighter color
        )
        self.count_label.pack(side="right")
        
        # Scrollable frame for playlist items
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))  # Increased padding
    
    def show_playlist(self, playlist, youtube_handler):
        """
        Show playlist with all its videos and quality options
        
        Args:
            playlist: YouTube Playlist object
            youtube_handler: YouTubeHandler instance for getting quality options
        """
        # Show the panel on the right side using grid (as per user's markup)
        self.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=0)
        
        # Update header
        self.header_label.configure(text=f"Playlist: {playlist.title}")
        
        # Clear previous items
        self.clear_items()
        
        # Add playlist items
        session = network_manager.get_session()
        headers = network_manager.get_headers()
        
        for i, video in enumerate(playlist.videos):
            try:
                quality_options = youtube_handler.get_quality_options(video)
                self._add_playlist_item(video, i, session, headers, quality_options)
            except Exception as e:
                print(f"Error adding playlist item {i}: {e}")
                continue
        
        self._update_selection_count()
    
    def _add_playlist_item(self, video, index, session, headers, quality_options):
        """
        Add a single playlist item with selection and quality controls
        
        Args:
            video: YouTube video object
            index (int): Video index in playlist
            session: HTTP session for thumbnail download
            headers (dict): HTTP headers
            quality_options (list): Available quality options for this video
        """
        # Main item container (increased height for better readability)
        item_frame = ctk.CTkFrame(
            self.scroll_frame, 
            fg_color="#2B2B2B", 
            corner_radius=5, 
            height=110  # Increased from 80 to 110
        )
        item_frame.pack(fill="x", pady=(0, 10))  # Increased padding between items
        item_frame.pack_propagate(False)  # Maintain fixed height
        
        # Top row: Checkbox, thumbnail, and video info
        top_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        top_frame.pack(fill="x", padx=8, pady=(8, 5))  # Increased padding
        
        # Selection checkbox
        select_var = ctk.BooleanVar()
        select_checkbox = ctk.CTkCheckBox(
            top_frame,
            text="",
            variable=select_var,
            width=20,
            command=self._on_item_selection_change
        )
        select_checkbox.pack(side="left", padx=(0, 8))  # Increased spacing
        
        # Thumbnail (larger size)
        try:
            thumb_response = session.get(
                video.thumbnail_url, 
                headers=headers, 
                timeout=10, 
                verify=False
            )
            from io import BytesIO
            from PIL import Image
            
            thumb_data = BytesIO(thumb_response.content)
            thumb_img = Image.open(thumb_data)
            thumb_img = thumb_img.resize((60, 45), Image.LANCZOS)  # Increased from 40x30 to 60x45
            thumb_ctk = CTkImage(
                light_image=thumb_img, 
                dark_image=thumb_img, 
                size=(60, 45)
            )
            
            thumb_label = ctk.CTkLabel(
                top_frame, 
                image=thumb_ctk, 
                text="", 
                width=60, 
                height=45
            )
            thumb_label.image = thumb_ctk  # Keep reference
            thumb_label.pack(side="left", padx=(0, 12))  # Increased spacing
            
        except Exception:
            # Fallback to placeholder if thumbnail fails
            thumb_placeholder = ctk.CTkLabel(
                top_frame, 
                text="VIDEO", 
                width=60,   # Increased size
                height=45,  # Increased size
                font=("Arial", 10),  # Larger font
                fg_color="#3B3B3B"
            )
            thumb_placeholder.pack(side="left", padx=(0, 12))
        
        # Video information container
        info_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)
        
        # Title (longer and with wrapping)
        title_text = f"{index + 1}. {safe_filename(video.title)}"
        # Don't truncate - let it wrap instead
            
        title_label = ctk.CTkLabel(
            info_frame, 
            text=title_text, 
            font=("Arial", 12, "bold"),  # Larger and bold font
            anchor="w", 
            justify="left",
            wraplength=350  # Allow text wrapping
        )
        title_label.pack(anchor="w", fill="x", pady=(0, 5))
        
        # Duration and more info
        duration_str = format_time(video.length)
        info_text = f"Duration: {duration_str}"
        if hasattr(video, 'views') and video.views:
            info_text += f" • Views: {video.views:,}"
            
        duration_label = ctk.CTkLabel(
            info_frame, 
            text=info_text, 
            font=("Arial", 10), 
            text_color="#AAAAAA", 
            anchor="w"
        )
        duration_label.pack(anchor="w")
        
        # Bottom row: Quality selector
        bottom_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=8, pady=(5, 8))  # Increased padding
        
        # Quality label and selector
        quality_label = ctk.CTkLabel(
            bottom_frame,
            text="Quality:",
            font=("Arial", 11, "bold"),  # Larger and bold
            text_color="#CCCCCC"  # Brighter color
        )
        quality_label.pack(side="left", padx=(88, 10))  # Align with video title
        
        # Quality combo box (much larger)
        quality_combo = ctk.CTkComboBox(
            bottom_frame,
            values=quality_options,
            height=32,     # Increased from 25 to 32
            width=250,     # Increased from 150 to 250
            font=("Arial", 11)  # Larger font
        )
        quality_combo.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Set default to best quality
        if quality_options:
            quality_combo.set(quality_options[0])
        
        # Store item data
        item_data = {
            'frame': item_frame,
            'video': video,
            'index': index,
            'selected': select_var,
            'quality_combo': quality_combo,
            'checkbox': select_checkbox
        }
        
        self.video_items.append(item_data)
    
    def clear_items(self):
        """Clear all playlist items"""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.video_items = []
        self.select_all_var.set(False)
        self._update_selection_count()
    
    def hide_playlist(self):
        """Hide the playlist panel"""
        self.grid_forget()  # Use grid_forget instead of pack_forget
        self.clear_items()
        self.header_label.configure(text="Playlist")
    
    def _on_select_all(self):
        """Handle Select All checkbox"""
        select_all = self.select_all_var.get()
        for item in self.video_items:
            item['selected'].set(select_all)
        self._update_selection_count()
    
    def _on_item_selection_change(self):
        """Handle individual item selection change"""
        selected_count = sum(1 for item in self.video_items if item['selected'].get())
        total_count = len(self.video_items)
        
        # Update Select All checkbox state
        if selected_count == 0:
            self.select_all_var.set(False)
        elif selected_count == total_count:
            self.select_all_var.set(True)
        
        self._update_selection_count()
    
    def _update_selection_count(self):
        """Update the selection count display"""
        selected_count = sum(1 for item in self.video_items if item['selected'].get())
        total_count = len(self.video_items)
        self.count_label.configure(text=f"{selected_count}/{total_count} selected")
    
    def get_selected_videos(self):
        """
        Get list of selected videos with their quality settings
        
        Returns:
            list: List of dictionaries containing video, quality, and index
        """
        selected = []
        for item in self.video_items:
            if item['selected'].get():
                selected.append({
                    'video': item['video'],
                    'quality': item['quality_combo'].get(),
                    'index': item['index'],
                    'title': item['video'].title
                })
        return selected
    
    def has_selected_videos(self):
        """
        Check if any videos are selected
        
        Returns:
            bool: True if at least one video is selected
        """
        return any(item['selected'].get() for item in self.video_items)
    
    def set_downloading_state(self, video_index, is_downloading=True):
        """
        Update UI to show which video is currently downloading
        
        Args:
            video_index (int): Index of video being downloaded
            is_downloading (bool): Whether download is in progress
        """
        for item in self.video_items:
            if item['index'] == video_index:
                checkbox = item['checkbox']
                if is_downloading:
                    checkbox.configure(text="DOWN", text_color="#4CAF50", font=("Arial", 8))  # Downloading indicator
                else:
                    checkbox.configure(text="DONE", text_color="#4CAF50", font=("Arial", 8))   # Completed indicator
                break