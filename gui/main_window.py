"""
Main application window for YouTube Downloader
"""

import customtkinter as ctk
import threading
from tkinter import messagebox
from config.settings import APP_TITLE, WINDOW_GEOMETRY, COLORS
from config.user_settings import user_settings
from core import file_manager, YouTubeHandler, DownloadManager
from gui.components import VideoPreview, PlaylistPanel, ProgressTracker, QualitySelector, SettingsDialog, LoadingPopup


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
        
        # Set up responsive window
        self.title(APP_TITLE)
        self._setup_responsive_window()
        self.resizable(True, True)  # Allow resizing
        
        # Set minimum and maximum window sizes
        self.minsize(800, 600)  # Minimum usable size
        
        # Bind window resize events for responsive layout
        self.bind("<Configure>", self._on_window_resize)
        
        # Add keyboard shortcuts for window management
        self.bind("<F11>", self._toggle_fullscreen)
        self.bind("<Control-minus>", self._minimize_window)
        self.bind("<Control-plus>", self._maximize_window)
        self.bind("<Alt-F4>", self._close_window)
        
        # Handle window close event
        self.protocol("WM_DELETE_WINDOW", self._close_window)
        
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
        self.last_window_state = "normal"
    
    def _setup_responsive_window(self):
        """Setup responsive window with proper sizing for different screen sizes"""
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Load saved window geometry if available
        saved_geometry = user_settings.get("window_geometry", "1400x800")
        
        try:
            # Parse saved geometry
            if "+" in saved_geometry:
                size_part, pos_part = saved_geometry.split("+", 1)
                width, height = map(int, size_part.split("x"))
                if "+" in pos_part:
                    x, y = map(int, pos_part.split("+"))
                else:
                    x, y = 100, 100
            else:
                width, height = map(int, saved_geometry.split("x"))
                x = (screen_width - width) // 2
                y = (screen_height - height) // 2
        except:
            # Default responsive sizing based on screen size
            width = min(1400, int(screen_width * 0.8))
            height = min(900, int(screen_height * 0.8))
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2
        
        # Ensure window fits on screen
        width = min(width, screen_width - 100)
        height = min(height, screen_height - 100)
        
        # Set window geometry
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        # Check if window was maximized in previous session
        if user_settings.get("window_maximized", False):
            self.state('zoomed')  # Maximize window on Windows
    
    def _on_window_resize(self, event):
        """Handle window resize events for responsive layout"""
        # Only handle resize events for the main window, not child widgets
        if event.widget != self:
            return
            
        # Save current window geometry
        try:
            geometry = self.geometry()
            user_settings.set("window_geometry", geometry)
            
            # Check if window is maximized
            current_state = self.state()
            is_maximized = current_state == 'zoomed'
            user_settings.set("window_maximized", is_maximized)
            
            # Update layout based on new size
            self._update_responsive_layout()
            
        except Exception:
            pass  # Ignore errors during resize
    
    def _update_responsive_layout(self):
        """Update layout based on current window size"""
        try:
            window_width = self.winfo_width()
            window_height = self.winfo_height()
            
            # Adjust layout based on window size
            if hasattr(self, 'main_container'):
                # Adjust container padding based on window size
                if window_width < 1000:
                    # Smaller padding for smaller windows
                    self.main_container.configure(corner_radius=8)
                    padding = 10
                else:
                    # Standard padding for larger windows
                    self.main_container.configure(corner_radius=15)
                    padding = 15
                
                self.main_container.pack_configure(padx=padding, pady=padding)
                
                # Adjust playlist panel visibility based on width
                if hasattr(self, 'playlist_panel') and self.is_playlist_loaded:
                    if window_width < 1200:
                        # Hide playlist panel on smaller screens, show toggle button instead
                        self._show_single_video_layout()
                        self._create_playlist_toggle()
                    else:
                        # Show playlist panel on larger screens
                        self._show_playlist_layout()
                        self._hide_playlist_toggle()
        except Exception:
            pass  # Ignore layout errors
    
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
        # Configure grid to split space: 50% main UI, 50% playlist panel
        self.main_container.grid_columnconfigure(0, weight=50)  # Left panel gets 50% space
        self.main_container.grid_columnconfigure(1, weight=50)  # Right panel gets 50% space
        
        # Show playlist panel
        self.playlist_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=0)
        
        # Update left frame padding to accommodate right panel
        self.left_frame.grid_configure(padx=(0, 5))
        
        # Force layout update
        self.main_container.update_idletasks()
        
    def _create_playlist_toggle(self):
        """Create a toggle button for playlist panel on smaller screens"""
        if not hasattr(self, 'playlist_toggle_button'):
            self.playlist_toggle_button = ctk.CTkButton(
                self.left_frame,
                text="📋 Show Playlist",
                command=self._toggle_playlist_panel,
                height=35,
                width=150,
                font=("Arial", 14, "bold"),
                corner_radius=8,
                fg_color="#4CAF50",
                hover_color="#45a049"
            )
        
        # Position the toggle button
        if hasattr(self, 'url_frame'):
            self.playlist_toggle_button.pack(in_=self.url_frame, side="right", padx=(10, 0))
    
    def _hide_playlist_toggle(self):
        """Hide the playlist toggle button"""
        if hasattr(self, 'playlist_toggle_button'):
            self.playlist_toggle_button.pack_forget()
    
    def _toggle_playlist_panel(self):
        """Toggle playlist panel visibility on smaller screens"""
        if hasattr(self, 'playlist_panel_visible') and self.playlist_panel_visible:
            # Hide playlist panel
            self.playlist_panel.place_forget()
            self.playlist_panel_visible = False
            self.playlist_toggle_button.configure(text="📋 Show Playlist")
        else:
            # Show playlist panel as overlay
            self._show_playlist_overlay()
            self.playlist_panel_visible = True
            self.playlist_toggle_button.configure(text="❌ Hide Playlist")
    
    def _show_playlist_overlay(self):
        """Show playlist panel as overlay on smaller screens"""
        # Get main container position and size
        x = self.main_container.winfo_x() + 50
        y = self.main_container.winfo_y() + 100
        width = min(400, self.winfo_width() - 100)
        height = self.winfo_height() - 200
        
        # Place playlist panel as overlay
        self.playlist_panel.place(x=x, y=y, width=width, height=height)
        self.playlist_panel.lift()  # Bring to front
        
    def _toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode (F11)"""
        current_state = self.state()
        if current_state == 'zoomed':
            self.state('normal')
        else:
            self.state('zoomed')
    
    def _minimize_window(self, event=None):
        """Minimize window (Ctrl+-)"""
        self.iconify()
    
    def _maximize_window(self, event=None):
        """Maximize/restore window (Ctrl++)"""
        current_state = self.state()
        if current_state == 'zoomed':
            self.state('normal')
        else:
            self.state('zoomed')
    
    def _close_window(self, event=None):
        """Close window with confirmation (Alt+F4)"""
        if self.download_manager.is_downloading():
            result = messagebox.askyesno(
                "Confirm Close",
                "A download is in progress. Are you sure you want to close the application?\n\nThis will cancel the current download."
            )
            if result:
                self.download_manager.cancel_download()
                self._save_window_state()
                self.quit()
        else:
            self._save_window_state()
            self.quit()
    
    def _save_window_state(self):
        """Save current window state before closing"""
        try:
            # Save window geometry and state
            geometry = self.geometry()
            user_settings.set("window_geometry", geometry)
            
            current_state = self.state()
            is_maximized = current_state == 'zoomed'
            user_settings.set("window_maximized", is_maximized)
        except Exception:
            pass  # Ignore save errors
        
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
        
        # Refresh theme-aware components
        if hasattr(self, 'playlist_panel'):
            self.playlist_panel.refresh_theme()
        
        if hasattr(self, 'video_preview'):
            self.video_preview.refresh_theme()
    
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
            text="⚙️ Settings", 
            width=120,  # Increased width
            height=45,  # Increased height
            font=("Arial", 14, "bold"), 
            command=self._open_settings,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.settings_button.pack(side="right")
    
    def _setup_url_input(self):
        """Set up URL input section"""
        self.url_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.url_frame.pack(fill="x", pady=(0, 25))  # Increased spacing
        
        url_label = ctk.CTkLabel(self.url_frame, text="YouTube URL:", font=("Arial", 16))  # Larger font
        url_label.pack(anchor="w", pady=(0, 8))  # Increased spacing
        
        self.url_entry = ctk.CTkEntry(self.url_frame, height=45, font=("Arial", 14))  # Larger height
        self.url_entry.pack(fill="x", pady=(0, 12))  # Increased spacing
        
        # Bind URL entry to detect changes and reset layout if empty
        self.url_entry.bind("<KeyRelease>", self._on_url_change)
        
        self.load_button = ctk.CTkButton(
            self.url_frame, 
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
        """Handle loading video or playlist with threading to prevent UI freeze"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        self.current_url = url
        
        # Disable load button and show loading state
        self.load_button.configure(text="Loading...", state="disabled")
        self.url_entry.configure(state="disabled")
        self.update_idletasks()
        
        # Start loading in background thread to prevent UI freeze
        threading.Thread(target=self._load_video_thread, args=(url,), daemon=True).start()
    
    def _load_video_thread(self, url):
        """Background thread for video loading to prevent UI freezing"""
        try:
            if self.youtube_handler.is_playlist(url):
                self._load_playlist_threaded(url)
            else:
                self._load_single_video_threaded(url)
                
        except Exception as e:
            # Schedule UI update on main thread
            self.after(0, lambda: self._handle_load_error(str(e)))
    
    def _handle_load_error(self, error_message):
        """Handle loading errors on main thread"""
        # Close loading popup if it exists
        if hasattr(self, 'loading_popup'):
            self.loading_popup.show_error(f"Failed to load: {error_message}")
            self.after(3000, self._close_loading_popup)
        else:
            messagebox.showerror("Error", f"Failed to load video: {error_message}")
        
        # On error, return to single video layout
        self._show_single_video_layout()
        self.is_playlist_loaded = False
        # Re-enable controls
        self.load_button.configure(text="Load Video", state="normal")
        self.url_entry.configure(state="normal")
    
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
        """Load a playlist with progress indication and error handling"""
        try:
            # Show loading message
            self.load_button.configure(text="Loading Playlist...", state="disabled")
            self.update_idletasks()
            
            # Load playlist
            playlist = self.youtube_handler.load_playlist(url)
            
            # Check if any videos were found
            video_count = len(list(playlist.videos)) if playlist.videos else 0
            if video_count == 0:
                messagebox.showwarning(
                    "No Accessible Videos", 
                    "This playlist contains no accessible videos. This might happen if:\n"
                    "• Videos are private or restricted\n"
                    "• Videos are age-restricted\n"
                    "• Videos are not available in your region\n"
                    "• The playlist is empty or deleted"
                )
                return
            
            # Switch to playlist layout (split panel view)
            self._show_playlist_layout()
            
            # Show playlist panel with quality options
            self.playlist_panel.show_playlist(playlist, self.youtube_handler)
            self.is_playlist_loaded = True
            
            # Show the "Download Selected" button
            self._update_download_buttons()
            
            # Load first video for preview
            if playlist.videos:
                try:
                    first_video = list(playlist.videos)[0]
                    video_info = self.youtube_handler.get_video_info(first_video)
                    thumbnail_image = self.youtube_handler.get_thumbnail_image(
                        video_info['thumbnail_url']
                    )
                    
                    # Update UI
                    self.video_preview.update_video_info(video_info, thumbnail_image)
                    
                    # Get quality options from first video
                    quality_options = self.youtube_handler.get_quality_options(first_video)
                    self.quality_selector.set_quality_options(quality_options)
                    
                except Exception as e:
                    print(f"Error loading first video preview: {e}")
                    # Don't fail the entire playlist load for this
            
            messagebox.showinfo(
                "Playlist Loaded", 
                f"Successfully loaded playlist with {video_count} accessible video(s).\n\n"
                "Note: Some videos may have been skipped due to access restrictions."
            )
            
        except Exception as e:
            messagebox.showerror(
                "Playlist Load Error", 
                f"Failed to load playlist:\n{str(e)}\n\n"
                "This might happen if:\n"
                "• The playlist URL is invalid\n"
                "• The playlist is private or deleted\n"
                "• There's a network connectivity issue\n"
                "• YouTube is blocking the request"
            )
        finally:
            # Re-enable the load button
            self.load_button.configure(text="Load Video", state="normal")
    
    def _load_single_video_threaded(self, url):
        """Load a single video in background thread"""
        try:
            # Load video (this runs in background thread)
            video = self.youtube_handler.load_video(url)
            
            # Get video info and thumbnail
            video_info = self.youtube_handler.get_video_info(video)
            thumbnail_image = self.youtube_handler.get_thumbnail_image(
                video_info['thumbnail_url']
            )
            
            # Get quality options
            quality_options = self.youtube_handler.get_quality_options(video)
            
            # Schedule UI updates on main thread
            self.after(0, lambda: self._update_single_video_ui(video_info, thumbnail_image, quality_options))
            
        except Exception as e:
            # Schedule error handling on main thread
            self.after(0, lambda: self._handle_load_error(str(e)))
    
    def _update_single_video_ui(self, video_info, thumbnail_image, quality_options):
        """Update UI for single video (called on main thread)"""
        # Switch to single video layout (full width main panel)
        self._show_single_video_layout()
        
        # Hide playlist panel and update state
        self.playlist_panel.hide_playlist()
        self.is_playlist_loaded = False
        
        # Update download buttons
        self._update_download_buttons()
        
        # Update UI
        self.video_preview.update_video_info(video_info, thumbnail_image)
        self.quality_selector.set_quality_options(quality_options)
        
        # Re-enable controls
        self.load_button.configure(text="Load Video", state="normal")
        self.url_entry.configure(state="normal")
    
    def _load_playlist_threaded(self, url):
        """Load a playlist in background thread with progress popup"""
        # Create and show loading popup on main thread
        self.after(0, lambda: self._show_playlist_loading_popup())
        
        try:
            # Load playlist (this runs in background thread)
            playlist = self.youtube_handler.load_playlist(url)
            
            # Check if any videos were found
            video_count = len(list(playlist.videos)) if playlist.videos else 0
            
            if video_count == 0:
                # Schedule warning on main thread
                self.after(0, lambda: self._show_playlist_warning())
                return
            
            # Schedule playlist processing on main thread with progress updates
            self.after(0, lambda: self._process_playlist_with_progress(playlist))
            
        except Exception as e:
            # Schedule error handling on main thread
            self.after(0, lambda: self._handle_load_error(str(e)))
    
    def _show_playlist_loading_popup(self):
        """Show the playlist loading popup"""
        self.loading_popup = LoadingPopup(
            self, 
            title="Loading Playlist", 
            message="Loading playlist videos..."
        )
        # Disable main window controls
        self.load_button.configure(state="disabled")
        self.url_entry.configure(state="disabled")
    
    def _process_playlist_with_progress(self, playlist):
        """Process playlist with progress updates in the popup"""
        try:
            # Set up progress tracking
            video_urls = list(playlist.video_urls)
            total_videos = len(video_urls)
            self.loading_popup.set_total_videos(total_videos)
            
            # Process playlist in background with progress updates
            threading.Thread(
                target=self._process_playlist_items, 
                args=(playlist, total_videos),
                daemon=True
            ).start()
            
        except Exception as e:
            self._handle_playlist_processing_error(str(e))
    
    def _process_playlist_items(self, playlist, total_videos):
        """Process playlist items in background thread"""
        try:
            successful_items = 0
            first_video_info = None
            thumbnail_image = None
            quality_options = []
            
            # Process each video with progress updates
            for i, video_url in enumerate(list(playlist.video_urls)):
                # Check for cancellation
                if hasattr(self, 'loading_popup') and self.loading_popup.is_cancelled():
                    self.after(0, lambda: self._handle_playlist_cancellation())
                    return
                
                try:
                    # Update progress
                    self.after(0, lambda idx=i: self.loading_popup.update_progress(
                        idx, f"Loading video {idx+1}/{total_videos}...", f"Video {idx+1}"
                    ))
                    
                    # Load video
                    video = self.youtube_handler.safe_load_video_from_url(video_url)
                    
                    if video is None:
                        continue
                    
                    # Get video info
                    video_info = self.youtube_handler.get_video_info(video)
                    
                    # Update progress with video title
                    self.after(0, lambda idx=i+1, title=video_info['title']: 
                              self.loading_popup.update_progress(
                                  idx, f"Processing video {idx}/{total_videos}...", title
                              ))
                    
                    # Store first video for preview
                    if successful_items == 0:
                        first_video_info = video_info
                        thumbnail_image = self.youtube_handler.get_thumbnail_image(
                            video_info['thumbnail_url']
                        )
                        quality_options = self.youtube_handler.get_quality_options(video)
                    
                    successful_items += 1
                    
                except Exception as e:
                    print(f"Error processing video {i+1}: {e}")
                    continue
            
            # Complete processing on main thread
            self.after(0, lambda: self._complete_playlist_processing(
                playlist, successful_items, total_videos, first_video_info, thumbnail_image, quality_options
            ))
            
        except Exception as e:
            self.after(0, lambda: self._handle_playlist_processing_error(str(e)))
    
    def _complete_playlist_processing(self, playlist, successful_items, total_videos, 
                                    first_video_info, thumbnail_image, quality_options):
        """Complete playlist processing on main thread"""
        try:
            # Update loading popup to show completion
            self.loading_popup.show_success(f"Successfully loaded {successful_items}/{total_videos} videos")
            
            # Switch to playlist layout
            self._show_playlist_layout()
            
            # Create progress callback for playlist panel
            def progress_callback(current, total, status, title):
                if hasattr(self, 'loading_popup') and not self.loading_popup.is_cancelled():
                    self.loading_popup.update_progress(current, status, title)
            
            # Show playlist panel - this will process and display videos
            self.playlist_panel.show_playlist(playlist, self.youtube_handler, progress_callback)
            self.is_playlist_loaded = True
            
            # Update download buttons
            self._update_download_buttons()
            
            # Update first video preview if available
            if first_video_info and thumbnail_image:
                self.video_preview.update_video_info(first_video_info, thumbnail_image)
                
            if quality_options:
                self.quality_selector.set_quality_options(quality_options)
            
            # Auto-close popup after 2 seconds
            self.after(2000, self._close_loading_popup)
            
            # Re-enable controls
            self.load_button.configure(text="Load Video", state="normal")
            self.url_entry.configure(state="normal")
            
        except Exception as e:
            self._handle_playlist_processing_error(str(e))
    
    def _handle_playlist_processing_error(self, error_message):
        """Handle playlist processing errors"""
        if hasattr(self, 'loading_popup'):
            self.loading_popup.show_error(f"Error: {error_message}")
            self.after(3000, self._close_loading_popup)
        
        # Re-enable controls
        self.load_button.configure(text="Load Video", state="normal")
        self.url_entry.configure(state="normal")
    
    def _handle_playlist_cancellation(self):
        """Handle playlist loading cancellation"""
        if hasattr(self, 'loading_popup'):
            self.loading_popup.close_popup()
            delattr(self, 'loading_popup')
        
        # Re-enable controls
        self.load_button.configure(text="Load Video", state="normal")
        self.url_entry.configure(state="normal")
    
    def _close_loading_popup(self):
        """Close the loading popup"""
        if hasattr(self, 'loading_popup'):
            self.loading_popup.close_popup()
            delattr(self, 'loading_popup')
    
    def _show_playlist_warning(self):
        """Show playlist warning (called on main thread)"""
        if hasattr(self, 'loading_popup'):
            self.loading_popup.show_error("This playlist contains no accessible videos")
            self.after(3000, self._close_loading_popup)
        else:
            messagebox.showwarning(
                "No Accessible Videos", 
                "This playlist contains no accessible videos. This might happen if:\n"
                "• Videos are private or restricted\n"
                "• Videos are age-restricted\n"
                "• Videos are not available in your region\n"
                "• The playlist is empty or deleted"
            )
        
        # Re-enable controls
        self.load_button.configure(text="Load Video", state="normal")
        self.url_entry.configure(state="normal")
    
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