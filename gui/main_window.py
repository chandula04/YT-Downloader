"""
Main application window for YouTube Downloader
"""

import customtkinter as ctk
from tkinter import messagebox
from config.settings import APP_TITLE, WINDOW_GEOMETRY, COLORS
from config.user_settings import user_settings
from core import file_manager, YouTubeHandler, DownloadManager
from gui.components import VideoPreview, PlaylistPanel, ProgressTracker, QualitySelector, SettingsDialog


class MainWindow(ctk.CTk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Apply user theme
        self._apply_theme(user_settings.get_theme())
        
        # Initialize core components
        self.youtube_handler = YouTubeHandler()
        self.download_manager = DownloadManager()
        self.download_manager.set_progress_callback(self._on_progress_update)
        self.download_manager.set_batch_progress_callback(self._on_batch_progress_update)
        
        # Set up window
        self.title(APP_TITLE)
        self.geometry("1400x800")  # Fixed size window
        self.resizable(False, False)  # Fixed window mode - cannot resize
        
        # Initialize file manager with user's saved path
        file_manager.set_download_path_direct(user_settings.get_download_path())
        user_settings.ensure_download_path_exists()
        
        # Initialize UI
        self._setup_ui()
        
        # Start with single video layout (full width main panel)
        self._show_single_video_layout()
        
        # State variables
        self.current_url = ""
        self.is_playlist_loaded = False
    
    def _setup_ui(self):
        """Set up the main user interface"""
        # Main container
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Create main content area using grid for better control
        self.main_container.grid_columnconfigure(0, weight=1)  # Left panel (always visible)
        self.main_container.grid_columnconfigure(1, weight=0)  # Right panel (playlist) - initially hidden
        self.main_container.grid_rowconfigure(0, weight=1)
        
        # Left frame for main controls - takes full width initially
        self.left_frame = ctk.CTkFrame(self.main_container)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        # Right frame for playlist - positioned on the right, initially hidden
        self.playlist_panel = PlaylistPanel(self.main_container)
        # Initially hidden using grid_forget(), will be shown when playlist is loaded
        
        self._setup_left_panel()
    
    def _show_single_video_layout(self):
        """Configure UI layout for single video mode (full width main panel)"""
        # Hide playlist panel
        self.playlist_panel.grid_forget()
        
        # Configure grid to give full space to left panel
        self.main_container.grid_columnconfigure(0, weight=1)  # Left panel takes full width
        self.main_container.grid_columnconfigure(1, weight=0)  # Right panel gets no space
        
        # Update left frame to take full width with no right padding
        self.left_frame.grid_configure(padx=0)
        
        # Force layout update
        self.main_container.update_idletasks()
        
    def _show_playlist_layout(self):
        """Configure UI layout for playlist mode (split layout with playlist panel)"""
        # Configure grid to split space: 55% main UI, 45% playlist panel
        self.main_container.grid_columnconfigure(0, weight=55)  # Left panel gets 55% space
        self.main_container.grid_columnconfigure(1, weight=45)  # Right panel gets 45% space
        
        # Show playlist panel
        self.playlist_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=0)
        
        # Update left frame padding to accommodate right panel
        self.left_frame.grid_configure(padx=(0, 5))
        
        # Force layout update
        self.main_container.update_idletasks()
        
    def _on_url_change(self, event):
        """Handle URL entry changes to reset layout when empty"""
        url = self.url_entry.get().strip()
        if not url and self.is_playlist_loaded:
            # If URL is cleared and we're currently showing a playlist, switch back to single video mode
            self._show_single_video_layout()
            self.playlist_panel.hide_playlist()
            self.is_playlist_loaded = False
            # Also clear the video preview
            self.video_preview.pack_forget()
            
    def _apply_theme(self, theme_name):
        """Apply the selected theme"""
        if theme_name == "light":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")
    
    def _open_settings(self):
        """Open the settings dialog"""
        settings_dialog = SettingsDialog(self, on_theme_change=self._apply_theme)
        # Update path display after dialog closes
        self.after(100, self._update_path_display)
    
    def _update_path_display(self):
        """Update the path display label"""
        if hasattr(self, 'path_label'):
            current_path = user_settings.get_download_path()
            # Show only the last part of the path if it's too long
            display_path = current_path
            if len(current_path) > 50:
                display_path = "..." + current_path[-47:]
            self.path_label.configure(text=f"Download Path: {display_path}")
    
    def _setup_left_panel(self):
        """Set up the left panel with main controls"""
        # Header
        self._setup_header()
        
        # URL Input section
        self._setup_url_input()
        
        # Video preview
        self.video_preview = VideoPreview(self.left_frame)
        
        # Quality selector
        self.quality_selector = QualitySelector(self.left_frame)
        self.quality_selector.pack(fill="x", pady=(0, 25))  # Increased spacing
        
        # Progress tracker
        self.progress_tracker = ProgressTracker(self.left_frame)
        self.progress_tracker.pack(fill="x", pady=(0, 15))  # Increased spacing
        
        # Action buttons
        self._setup_buttons()
        
        # Download path display
        self._setup_path_display()
    
    def _setup_header(self):
        """Set up the application header"""
        header_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 25))  # Increased spacing
        
        self.title_label = ctk.CTkLabel(
            header_frame, 
            text=APP_TITLE, 
            font=("Arial", 26, "bold")  # Larger title
        )
        self.title_label.pack(side="left")
        
        self.settings_button = ctk.CTkButton(
            header_frame, 
            text="Settings", 
            width=100,  # Increased width
            height=45,  # Increased height
            font=("Arial", 14), 
            command=self._open_settings  # Use new settings dialog
        )
        self.settings_button.pack(side="right")
    
    def _setup_url_input(self):
        """Set up URL input section"""
        url_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        url_frame.pack(fill="x", pady=(0, 25))  # Increased spacing
        
        url_label = ctk.CTkLabel(url_frame, text="YouTube URL:", font=("Arial", 16))  # Larger font
        url_label.pack(anchor="w", pady=(0, 8))  # Increased spacing
        
        self.url_entry = ctk.CTkEntry(url_frame, height=45, font=("Arial", 14))  # Larger height
        self.url_entry.pack(fill="x", pady=(0, 12))  # Increased spacing
        
        # Bind URL entry to detect changes and reset layout if empty
        self.url_entry.bind("<KeyRelease>", self._on_url_change)
        
        self.load_button = ctk.CTkButton(
            url_frame, 
            text="Load Video", 
            command=self._load_video, 
            height=45, 
            font=("Arial", 16)  # Larger font
        )
        self.load_button.pack(fill="x")
    
    def _setup_buttons(self):
        """Set up action buttons"""
        self.button_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.button_frame.pack(fill="x", pady=(10, 0))
        
        self.download_button = ctk.CTkButton(
            self.button_frame, 
            text="Download", 
            command=self._download, 
            height=50,  # Increased height
            font=("Arial", 18),  # Larger font
            fg_color=COLORS['primary'], 
            hover_color=COLORS['primary_hover']
        )
        self.download_button.pack(side="left", padx=(0, 5), fill="x", expand=True)
        
        self.download_selected_button = ctk.CTkButton(
            self.button_frame, 
            text="Download Selected", 
            command=self._download_selected, 
            height=50,  # Increased height
            font=("Arial", 18),  # Larger font
            fg_color="#FF9800",  # Orange color for batch download
            hover_color="#F57C00"
        )
        # Initially hidden
        self.download_selected_button.pack_forget()
        
        self.cancel_button = ctk.CTkButton(
            self.button_frame, 
            text="Cancel", 
            command=self._cancel_download, 
            height=50,  # Increased height
            font=("Arial", 18),  # Larger font
            fg_color=COLORS['danger'], 
            hover_color=COLORS['danger_hover']
        )
        # Initially hidden
        self.cancel_button.pack_forget()
    
    def _setup_path_display(self):
        """Set up download path display"""
        current_path = user_settings.get_download_path()
        # Show only the last part of the path if it's too long
        display_path = current_path
        if len(current_path) > 50:
            display_path = "..." + current_path[-47:]
            
        self.path_label = ctk.CTkLabel(
            self.left_frame, 
            text=f"Download Path: {display_path}", 
            font=("Arial", 14),  # Larger font
            text_color=COLORS['text_disabled']
        )
        self.path_label.pack(anchor="w", pady=(20, 0))  # More spacing
    
    def _set_download_path(self):
        """Handle setting download path"""
        if file_manager.set_download_path():
            path = file_manager.get_download_path()
            self.path_label.configure(text=f"Download Path: {path}")
    
    def _load_video(self):
        """Handle loading video or playlist"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        self.current_url = url
        
        try:
            if self.youtube_handler.is_playlist(url):
                self._load_playlist(url)
            else:
                self._load_single_video(url)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load video: {str(e)}")
            # On error, return to single video layout
            self._show_single_video_layout()
            self.is_playlist_loaded = False
    
    def _load_single_video(self, url):
        """Load a single video"""
        # Switch to single video layout (full width main panel)
        self._show_single_video_layout()
        
        # Hide playlist panel and update state
        self.playlist_panel.hide_playlist()
        self.is_playlist_loaded = False
        
        # Update download buttons
        self._update_download_buttons()
        
        # Load video
        video = self.youtube_handler.load_video(url)
        
        # Get video info and thumbnail
        video_info = self.youtube_handler.get_video_info(video)
        thumbnail_image = self.youtube_handler.get_thumbnail_image(
            video_info['thumbnail_url']
        )
        
        # Update UI
        self.video_preview.update_video_info(video_info, thumbnail_image)
        
        # Get quality options
        quality_options = self.youtube_handler.get_quality_options(video)
        self.quality_selector.set_quality_options(quality_options)
    
    def _load_playlist(self, url):
        """Load a playlist"""
        # Load playlist
        playlist = self.youtube_handler.load_playlist(url)
        
        # Switch to playlist layout (split panel view)
        self._show_playlist_layout()
        
        # Show playlist panel with quality options
        self.playlist_panel.show_playlist(playlist, self.youtube_handler)
        self.is_playlist_loaded = True
        
        # Show the "Download Selected" button
        self._update_download_buttons()
        
        # Load first video for preview
        if playlist.videos:
            first_video = playlist.videos[0]
            video_info = self.youtube_handler.get_video_info(first_video)
            thumbnail_image = self.youtube_handler.get_thumbnail_image(
                video_info['thumbnail_url']
            )
            
            # Update UI
            self.video_preview.update_video_info(video_info, thumbnail_image)
            
            # Get quality options from first video
            quality_options = self.youtube_handler.get_quality_options(first_video)
            self.quality_selector.set_quality_options(quality_options)
    
    def _download(self):
        """Handle download button click"""
        if not self.current_url:
            messagebox.showerror("Error", "Please load a video first")
            return
        
        selected_quality = self.quality_selector.get_selected_quality()
        if not selected_quality:
            messagebox.showerror("Error", "Please select a quality")
            return
        
        is_audio = self.quality_selector.is_audio_only()
        
        # Check if download path is set
        if not file_manager.has_download_path():
            if not file_manager.set_download_path():
                return
            path = file_manager.get_download_path()
            self.path_label.configure(text=f"Download Path: {path}")
        
        # Update UI for download state
        self._set_download_state(True)
        
        # Start download
        if self.is_playlist_loaded:
            self.download_manager.download_playlist(
                self.current_url,
                selected_quality,
                is_audio,
                success_callback=self._on_download_success,
                error_callback=self._on_download_error
            )
        else:
            self.download_manager.download_video(
                self.current_url,
                selected_quality,
                is_audio,
                success_callback=self._on_download_success,
                error_callback=self._on_download_error
            )
    
    def _download_selected(self):
        """Handle download selected videos button click"""
        if not self.is_playlist_loaded:
            messagebox.showerror("Error", "No playlist loaded")
            return
        
        selected_videos = self.playlist_panel.get_selected_videos()
        if not selected_videos:
            messagebox.showerror("Error", "Please select at least one video to download")
            return
        
        # Check if download path is set
        if not file_manager.has_download_path():
            if not file_manager.set_download_path():
                return
            path = file_manager.get_download_path()
            self.path_label.configure(text=f"Download Path: {path}")
        
        # Update UI for batch download state
        self._set_download_state(True, batch_mode=True)
        self.progress_tracker.set_batch_mode(True, 0, len(selected_videos))
        
        # Start batch download
        self.download_manager.download_selected_videos(
            selected_videos,
            success_callback=self._on_download_success,
            error_callback=self._on_download_error
        )
    
    def _update_download_buttons(self):
        """Update visibility of download buttons based on current state"""
        if self.is_playlist_loaded:
            # Show both buttons for playlists
            self.download_button.pack(side="left", padx=(0, 5), fill="x", expand=True)
            self.download_selected_button.pack(side="left", padx=(5, 0), fill="x", expand=True)
        else:
            # Show only regular download button for single videos
            self.download_button.pack(side="left", fill="x", expand=True)
            self.download_selected_button.pack_forget()
    
    def _set_download_state(self, downloading, batch_mode=False):
        """
        Update UI for download/idle state
        
        Args:
            downloading (bool): Whether downloading is in progress
            batch_mode (bool): Whether this is a batch download
        """
        if downloading:
            self.download_button.pack_forget()
            self.download_selected_button.pack_forget()
            self.cancel_button.pack(side="right", padx=(10, 0), fill="x", expand=True)
            self.quality_selector.disable()
            self.load_button.configure(state="disabled")
        else:
            self.cancel_button.pack_forget()
            self._update_download_buttons()  # Restore appropriate buttons
            self.quality_selector.enable()
            self.load_button.configure(state="normal")
    
    def _on_batch_progress_update(self, video_index, status, video_title, current, total):
        """
        Handle batch progress updates
        
        Args:
            video_index (int): Index of current video
            status (str): Status ('downloading', 'completed', 'error')
            video_title (str): Title of current video
            current (int): Current video number
            total (int): Total videos in batch
        """
        # Update UI in main thread
        self.after(0, lambda: self._update_batch_ui(video_index, status, video_title, current, total))
    
    def _update_batch_ui(self, video_index, status, video_title, current, total):
        """Update UI for batch progress"""
        # Update progress tracker
        self.progress_tracker.update_batch_info(current, total, video_title)
        
        # Update playlist panel to show download status
        if self.is_playlist_loaded:
            if status == 'downloading':
                self.playlist_panel.set_downloading_state(video_index, True)
            elif status == 'completed':
                self.playlist_panel.set_downloading_state(video_index, False)
    
    def _cancel_download(self):
        """Handle cancel button click"""
        self.download_manager.cancel_download()
        self.progress_tracker.set_status("Cancelling...")
    
    def _on_progress_update(self, downloaded, total, percentage, speed, elapsed, custom_text=None):
        """
        Handle progress updates from download manager
        
        Args:
            downloaded (int): Bytes downloaded
            total (int): Total bytes
            percentage (float): Download percentage
            speed (float): Download speed in MB/s
            elapsed (int): Elapsed time in seconds
            custom_text (str, optional): Custom status text
        """
        # Update UI in main thread
        self.after(0, lambda: self.progress_tracker.update_progress(
            downloaded, total, percentage, speed, elapsed, custom_text
        ))
    
    def _on_download_success(self, message):
        """Handle successful download completion"""
        self.after(0, lambda: self._download_completed(message, success=True))
    
    def _on_download_error(self, error_message):
        """Handle download error"""
        self.after(0, lambda: self._download_completed(error_message, success=False))
    
    def _download_completed(self, message, success=True):
        """
        Handle download completion (success or error)
        
        Args:
            message (str): Completion message
            success (bool): Whether download was successful
        """
        # Update UI state
        self._set_download_state(False)
        
        # Show completion message
        if success:
            self.progress_tracker.set_success(message)
            messagebox.showinfo("Success", message)
        else:
            if message == "Download cancelled":
                messagebox.showinfo("Cancelled", message)
            elif "ffmpeg" in message.lower():
                messagebox.showerror(
                    "FFmpeg Error", 
                    "FFmpeg is required but not found. Please install FFmpeg and add it to your PATH."
                )
            else:
                messagebox.showerror("Error", f"Download failed: {message}")
        
        # Reset progress after a delay
        self.after(3000, self.progress_tracker.reset)