"""
Playlist panel component for displaying playlist information with selection controls
"""

import customtkinter as ctk
from customtkinter import CTkImage
from utils.helpers import safe_filename, format_time, resolution_key
from utils.network import network_manager


def get_theme_colors():
    """Get colors based on current appearance mode"""
    appearance_mode = ctk.get_appearance_mode()
    
    if appearance_mode == "Light":
        return {
            'frame_bg': "#EBEBEB",           # Light frame background
            'item_bg': "#F0F0F0",            # Light item background  
            'secondary_bg': "#E0E0E0",       # Light secondary background
            'text_primary': "#000000",       # Dark text for light mode
            'text_secondary': "#666666",     # Secondary text for light mode
            'text_accent': "#333333",        # Accent text for light mode
            'dropdown_hover': "#D0D0D0",     # Light dropdown hover
            'button_hover': "#1F538D"        # Keep button hover consistent
        }
    else:
        return {
            'frame_bg': "#2B2B2B",           # Dark frame background
            'item_bg': "#2B2B2B",            # Dark item background
            'secondary_bg': "#3B3B3B",       # Dark secondary background  
            'text_primary': "#FFFFFF",       # Light text for dark mode
            'text_secondary': "#AAAAAA",     # Secondary text for dark mode
            'text_accent': "#CCCCCC",        # Accent text for dark mode
            'dropdown_hover': "#2B2B2B",     # Dark dropdown hover
            'button_hover': "#1F538D"        # Keep button hover consistent
        }


class PlaylistPanel(ctk.CTkFrame):
    """Panel for displaying playlist information and items with selection controls"""
    
    def __init__(self, parent, width=700, **kwargs):  # Increased to match user's marked area
        # Get theme colors
        colors = get_theme_colors()
        
        # Apply theme-aware frame color
        super().__init__(parent, width=width, fg_color=colors['frame_bg'], **kwargs)
        
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
        
        # Top row controls
        top_controls = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        top_controls.pack(fill="x", pady=(0, 10))
        
        # Select All checkbox (larger)
        self.select_all_checkbox = ctk.CTkCheckBox(
            top_controls,
            text="Select All",
            variable=self.select_all_var,
            command=self._on_select_all,
            font=("Arial", 14, "bold")  # Larger font
        )
        self.select_all_checkbox.pack(side="left")
        
        # Selected count label (larger and more prominent)
        self.count_label = ctk.CTkLabel(
            top_controls,
            text="0 selected",
            font=("Arial", 12),  # Larger font
            text_color=get_theme_colors()['text_accent']  # Theme-aware color
        )
        self.count_label.pack(side="right")
        
        # Bottom row - bulk quality controls
        bottom_controls = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        bottom_controls.pack(fill="x")
        
        # Bulk quality label
        bulk_quality_label = ctk.CTkLabel(
            bottom_controls,
            text="Set Quality for All:",
            font=("Arial", 12, "bold")
        )
        bulk_quality_label.pack(side="left")
        
        # Bulk quality selector
        self.bulk_quality_var = ctk.StringVar(value="Select Quality")
        self.bulk_quality_combo = ctk.CTkComboBox(
            bottom_controls,
            variable=self.bulk_quality_var,
            values=["Select Quality"],
            width=150,
            height=28,
            font=("Arial", 11),
            command=self._on_bulk_quality_change
        )
        self.bulk_quality_combo.pack(side="left", padx=(10, 0))
        
        # Apply button for bulk quality
        self.apply_bulk_button = ctk.CTkButton(
            bottom_controls,
            text="Apply to Selected",
            width=120,
            height=28,
            font=("Arial", 11),
            command=self._apply_bulk_quality
        )
        self.apply_bulk_button.pack(side="right")
        
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
        # Note: Grid positioning is now handled by the main window layout methods
        
        # Update header
        self.header_label.configure(text=f"Playlist: {playlist.title}")
        
        # Clear previous items
        self.clear_items()
        
        # Add playlist items
        session = network_manager.get_session()
        headers = network_manager.get_headers()
        
        # Collect all unique quality options for bulk selector
        all_quality_options = set()
        
        # Add progress tracking - use video_urls instead of videos to avoid errors
        try:
            video_urls = list(playlist.video_urls)
            total_videos = len(video_urls)
        except Exception as e:
            print(f"Error getting playlist URLs: {e}")
            total_videos = 0
            video_urls = []
        
        print(f"📋 Processing {total_videos} videos in playlist...")
        successful_items = 0
        
        for i, video_url in enumerate(video_urls):
            try:
                print(f"📝 Loading video {i+1}/{total_videos}...")
                
                # Safely load video using the new method
                video = youtube_handler.safe_load_video_from_url(video_url)
                
                if video is None:
                    raise Exception("Video is not accessible")
                
                # Get video info safely
                video_info = youtube_handler.get_video_info(video)
                print(f"📝 Processing: {video_info['title'][:50]}...")
                
                quality_options = youtube_handler.get_quality_options(video)
                all_quality_options.update(quality_options)
                self._add_playlist_item(video, i, session, headers, quality_options)
                successful_items += 1
                print(f"✅ Added video {i+1}")
                
            except Exception as e:
                print(f"❌ Error with video {i+1}: {str(e)[:100]}...")
                # Add error placeholder item
                self._add_error_playlist_item(i, str(e))
                continue
        
        print(f"🎯 Successfully processed {successful_items}/{total_videos} videos")
        
        # Update bulk quality selector with common options
        if all_quality_options:
            sorted_options = sorted(list(all_quality_options), key=lambda x: self._quality_sort_key(x))
            self.bulk_quality_combo.configure(values=sorted_options)
        
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
        # Main item container (increased height for better readability and dropdown space)
        item_frame = ctk.CTkFrame(
            self.scroll_frame, 
            fg_color=get_theme_colors()['item_bg'],  # Theme-aware background
            corner_radius=5, 
            height=120  # Increased from 110 to 120 for more space
        )
        item_frame.pack(fill="x", pady=(0, 15))  # Increased padding between items for dropdown space
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
                fg_color=get_theme_colors()['secondary_bg'],  # Theme-aware background
                text_color=get_theme_colors()['text_primary']  # Theme-aware text
            )
            thumb_placeholder.pack(side="left", padx=(0, 12))
        
        # Video information container with fixed height to prevent overlap
        info_frame = ctk.CTkFrame(top_frame, fg_color="transparent", height=50)
        info_frame.pack(side="left", fill="x", expand=True)
        info_frame.pack_propagate(False)  # Prevent frame from shrinking
        
        # Title (controlled height to prevent overlap)
        title_text = f"{index + 1}. {safe_filename(video.title)}"
        # Truncate long titles to prevent layout issues
        if len(title_text) > 60:
            title_text = title_text[:57] + "..."
            
        title_label = ctk.CTkLabel(
            info_frame, 
            text=title_text, 
            font=("Arial", 12, "bold"),  # Larger and bold font
            anchor="w", 
            justify="left",
            height=25  # Fixed height
        )
        title_label.pack(anchor="w", fill="x", pady=(2, 0))
        
        # Duration and more info
        duration_str = format_time(video.length)
        info_text = f"Duration: {duration_str}"
        if hasattr(video, 'views') and video.views:
            info_text += f" • Views: {video.views:,}"
            
        duration_label = ctk.CTkLabel(
            info_frame, 
            text=info_text, 
            font=("Arial", 10), 
            text_color=get_theme_colors()['text_secondary'],  # Theme-aware secondary text
            anchor="w",
            height=20  # Fixed height
        )
        duration_label.pack(anchor="w", pady=(0, 3))
        
        # Bottom row: Quality selector with proper spacing
        bottom_frame = ctk.CTkFrame(item_frame, fg_color="transparent", height=40)
        bottom_frame.pack(fill="x", padx=8, pady=(8, 8))  # Increased top padding
        bottom_frame.pack_propagate(False)  # Prevent frame from shrinking
        
        # Quality label and selector
        quality_label = ctk.CTkLabel(
            bottom_frame,
            text="Quality:",
            font=("Arial", 11, "bold"),  # Larger and bold
            text_color=get_theme_colors()['text_accent']  # Theme-aware accent text
        )
        quality_label.pack(side="left", padx=(88, 10))  # Align with video title
        
        # Quality combo box (improved positioning)
        quality_combo = ctk.CTkComboBox(
            bottom_frame,
            values=quality_options,
            height=32,     # Increased from 25 to 32
            width=250,     # Increased from 150 to 250
            font=("Arial", 11),  # Larger font
            dropdown_hover_color=get_theme_colors()['dropdown_hover'],  # Theme-aware hover
            button_hover_color=get_theme_colors()['button_hover']       # Better visibility
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
            # Skip error items (they don't have selectable checkboxes)
            if item.get('error', False):
                continue
                
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
        return any(item['selected'].get() for item in self.video_items if not item.get('error', False))
    
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
    
    def _add_error_playlist_item(self, index, error_message):
        """Add a placeholder item for videos that couldn't be processed"""
        colors = get_theme_colors()
        
        # Main item container with error styling
        error_bg = "#4A1F1F" if ctk.get_appearance_mode() == "Dark" else "#FFE6E6"  # Theme-aware error background
        item_frame = ctk.CTkFrame(
            self.scroll_frame, 
            fg_color=error_bg,  # Theme-aware error background
            corner_radius=5, 
            height=80
        )
        item_frame.pack(fill="x", pady=(0, 10))
        item_frame.pack_propagate(False)
        
        # Error content
        error_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        error_frame.pack(fill="both", expand=True, padx=8, pady=8)
        
        # Error icon and message
        error_text_color = "#FF6B6B" if ctk.get_appearance_mode() == "Dark" else "#CC0000"  # Theme-aware error text
        error_label = ctk.CTkLabel(
            error_frame,
            text=f"❌ Video {index+1}: Access Restricted",
            font=("Arial", 14, "bold"),
            text_color=error_text_color  # Theme-aware error text color
        )
        error_label.pack(anchor="w")
        
        # Error details
        short_error = error_message[:60] + "..." if len(error_message) > 60 else error_message
        details_label = ctk.CTkLabel(
            error_frame,
            text=f"Reason: {short_error}",
            font=("Arial", 10),
            text_color=get_theme_colors()['text_secondary']  # Theme-aware secondary text
        )
        details_label.pack(anchor="w", pady=(5, 0))
        
        # Add to items list but mark as error
        self.video_items.append({
            'frame': item_frame,
            'checkbox': None,
            'select_var': None,
            'quality_combo': None,
            'video': None,
            'index': index,
            'error': True
        })
                
    def _quality_sort_key(self, quality_string):
        """
        Generate sort key for quality options
        
        Args:
            quality_string (str): Quality option string
            
        Returns:
            tuple: Sort key (resolution_num, is_adaptive)
        """
        try:
            if "p" in quality_string:
                resolution = int(quality_string.split("p")[0].split()[-1])
                is_adaptive = "Adaptive" in quality_string
                return (resolution, is_adaptive)
            else:
                return (0, False)
        except:
            return (0, False)
    
    def _on_bulk_quality_change(self, selected_quality):
        """Handle bulk quality selector change"""
        pass  # No immediate action needed
    
    def _apply_bulk_quality(self):
        """Apply the selected bulk quality to all selected videos"""
        bulk_quality = self.bulk_quality_var.get()
        
        if bulk_quality == "Select Quality":
            return
        
        # Apply to all selected videos
        applied_count = 0
        for item in self.video_items:
            if item['selected'].get():
                # Check if this quality is available for this video
                available_qualities = item['quality_combo'].cget("values")
                if bulk_quality in available_qualities:
                    item['quality_combo'].set(bulk_quality)
                    applied_count += 1
        
        if applied_count > 0:
            # Show feedback
            self.apply_bulk_button.configure(text=f"Applied to {applied_count}")
            self.after(2000, lambda: self.apply_bulk_button.configure(text="Apply to Selected"))
    
    def refresh_theme(self):
        """Refresh colors when theme changes"""
        colors = get_theme_colors()
        
        # Update main frame background
        self.configure(fg_color=colors['frame_bg'])
        
        # Update header text color
        if hasattr(self, 'header_label'):
            self.header_label.configure(text_color=colors['text_primary'])
        
        # Update count label text color  
        if hasattr(self, 'count_label'):
            self.count_label.configure(text_color=colors['text_accent'])
        
        # Update all video item colors
        for item in self.video_items:
            if item.get('error', False):
                # Error items
                error_bg = "#4A1F1F" if ctk.get_appearance_mode() == "Dark" else "#FFE6E6"
                item['frame'].configure(fg_color=error_bg)
            else:
                # Normal items
                item['frame'].configure(fg_color=colors['item_bg'])
        
        # Force update
        self.update_idletasks()