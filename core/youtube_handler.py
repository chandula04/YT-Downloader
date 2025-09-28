"""
YouTube API handling and video information retrieval
"""

from pytubefix import YouTube, Playlist
from utils.helpers import safe_filename, format_size, resolution_key
from utils.network import network_manager
from io import BytesIO
from PIL import Image


class YouTubeHandler:
    """Handles YouTube video and playlist operations"""
    
    def __init__(self):
        self.current_video = None
        self.current_playlist = None
    
    def load_video(self, url):
        """
        Load a single YouTube video with multiple client fallbacks
        
        Args:
            url (str): YouTube video URL
            
        Returns:
            YouTube: YouTube object
            
        Raises:
            Exception: If video loading fails
        """
        try:
            # Try multiple client strategies for better compatibility
            clients_to_try = [
                {"use_oauth": False, "allow_oauth_cache": False},
                {"client": "ANDROID"},
                {"client": "TV_EMBED"},
            ]
            
            last_error = None
            for client_config in clients_to_try:
                try:
                    print(f"🔄 Trying client: {client_config}")
                    self.current_video = YouTube(url, **client_config)
                    # Test if we can access basic properties
                    _ = self.current_video.title
                    _ = self.current_video.length
                    print("✅ Video loaded successfully")
                    return self.current_video
                except Exception as e:
                    last_error = e
                    print(f"❌ Client failed: {str(e)[:100]}...")
                    continue
            
            # If all clients fail, raise the last error
            raise last_error or Exception("All client strategies failed")
            
        except Exception as e:
            raise Exception(f"Failed to load video: {str(e)}")
    
    def load_playlist(self, url):
        """
        Load a YouTube playlist with error handling
        
        Args:
            url (str): YouTube playlist URL
            
        Returns:
            Playlist: Playlist object
            
        Raises:
            Exception: If playlist loading fails
        """
        try:
            # Use different client strategies for better compatibility
            from pytubefix import Playlist
            self.current_playlist = Playlist(url)
            
            # Pre-filter accessible videos to avoid errors during iteration
            self.current_playlist = self._filter_accessible_videos(self.current_playlist)
            
            return self.current_playlist
        except Exception as e:
            raise Exception(f"Failed to load playlist: {str(e)}")
    
    def _filter_accessible_videos(self, playlist):
        """
        Filter out inaccessible videos from playlist
        
        Args:
            playlist: Original playlist object
            
        Returns:
            Playlist: Filtered playlist with accessible videos only
        """
        try:
            # Test access to videos and filter out problematic ones
            accessible_videos = []
            total_videos = len(list(playlist.video_urls))
            print(f"📋 Checking {total_videos} videos in playlist...")
            
            for i, video_url in enumerate(playlist.video_urls):
                try:
                    # Quick test to see if video is accessible
                    test_video = YouTube(video_url, use_oauth=False, allow_oauth_cache=False)
                    # Test if we can get basic info
                    _ = test_video.title
                    _ = test_video.length
                    accessible_videos.append(video_url)
                    print(f"✅ Video {i+1}/{total_videos}: OK")
                except Exception as e:
                    print(f"❌ Video {i+1}/{total_videos}: Skipped - {str(e)[:100]}...")
                    continue
            
            print(f"🎯 {len(accessible_videos)}/{total_videos} videos are accessible")
            
            # Create a new playlist with only accessible videos
            if accessible_videos:
                # Override the video URLs in the playlist
                playlist._video_urls = accessible_videos
                playlist._videos = None  # Reset cached videos
            
            return playlist
            
        except Exception as e:
            print(f"Error filtering playlist: {e}")
            return playlist  # Return original if filtering fails
    
    def is_playlist(self, url):
        """
        Check if URL is a playlist
        
        Args:
            url (str): YouTube URL
            
        Returns:
            bool: True if URL is a playlist, False otherwise
        """
        return 'list=' in url.lower()
    
    def get_video_info(self, video):
        """
        Extract video information
        
        Args:
            video (YouTube): YouTube video object
            
        Returns:
            dict: Video information dictionary
        """
        return {
            'title': video.title,
            'author': video.author,
            'length': video.length,
            'thumbnail_url': video.thumbnail_url
        }
    
    def get_quality_options(self, video):
        """
        Get available quality options for a video with error handling
        
        Args:
            video (YouTube): YouTube video object
            
        Returns:
            list: List of quality options
        """
        try:
            streams = video.streams.filter(file_extension='mp4')
            quality_options = []
            
            # Get video-only streams (adaptive)
            try:
                adaptive_streams = streams.filter(adaptive=True, only_video=True)
                for stream in adaptive_streams:
                    if stream.resolution:
                        try:
                            size_info = f" ({format_size(stream.filesize)})" if stream.filesize else ""
                            quality_options.append(f"{stream.resolution} - Adaptive{size_info}")
                        except Exception:
                            # Fallback without size info
                            quality_options.append(f"{stream.resolution} - Adaptive")
            except Exception as e:
                print(f"Error getting adaptive streams: {e}")
            
            # Get progressive streams (with audio)
            try:
                prog_streams = streams.filter(progressive=True)
                for stream in prog_streams:
                    if stream.resolution:
                        try:
                            size_info = f" ({format_size(stream.filesize)})" if stream.filesize else ""
                            quality_options.append(f"{stream.resolution} - Progressive{size_info}")
                        except Exception:
                            # Fallback without size info
                            quality_options.append(f"{stream.resolution} - Progressive")
            except Exception as e:
                print(f"Error getting progressive streams: {e}")
            
            # If no streams found, try alternative approach
            if not quality_options:
                try:
                    # Try to get any available streams
                    all_streams = video.streams.filter(file_extension='mp4')
                    for stream in all_streams:
                        if hasattr(stream, 'resolution') and stream.resolution:
                            quality_options.append(f"{stream.resolution} - Available")
                except Exception as e:
                    print(f"Error getting fallback streams: {e}")
            
            # If still no options, provide a default
            if not quality_options:
                quality_options = ["720p - Default", "480p - Default", "360p - Default"]
            
            # Sort by resolution (highest first)
            try:
                quality_options.sort(key=resolution_key, reverse=True)
            except Exception:
                pass  # Keep original order if sorting fails
            
            return quality_options
            
        except Exception as e:
            print(f"Error getting quality options: {e}")
            # Return default options if all else fails
            return ["720p - Default", "480p - Default", "360p - Default"]
    
    def get_thumbnail_image(self, thumbnail_url, size=(120, 90)):
        """
        Download and process thumbnail image
        
        Args:
            thumbnail_url (str): URL of the thumbnail
            size (tuple): Target size (width, height)
            
        Returns:
            PIL.Image: Processed thumbnail image
        """
        try:
            session = network_manager.get_session()
            headers = network_manager.get_headers()
            response = session.get(thumbnail_url, headers=headers, timeout=10, verify=False)
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img = img.resize(size, Image.LANCZOS)
            return img
        except Exception as e:
            print(f"Error loading thumbnail: {e}")
            return None
    
    def get_stream_by_quality(self, video, resolution, stream_type):
        """
        Get specific stream by quality and type
        
        Args:
            video (YouTube): YouTube video object
            resolution (str): Video resolution (e.g., "1080p")
            stream_type (str): Stream type ("Progressive" or "Adaptive")
            
        Returns:
            Stream: YouTube stream object
        """
        if "Progressive" in stream_type:
            return video.streams.filter(
                progressive=True, 
                file_extension='mp4', 
                res=resolution
            ).first()
        else:
            return video.streams.filter(
                adaptive=True, 
                file_extension='mp4', 
                res=resolution,
                only_video=True
            ).first()
    
    def get_best_audio_stream(self, video):
        """
        Get the best available audio stream
        
        Args:
            video (YouTube): YouTube video object
            
        Returns:
            Stream: Best audio stream
        """
        return video.streams.filter(
            adaptive=True,
            only_audio=True
        ).order_by('abr').desc().first()
    
    def get_audio_only_stream(self, video):
        """
        Get audio-only stream for MP3 download
        
        Args:
            video (YouTube): YouTube video object
            
        Returns:
            Stream: Audio-only stream
        """
        return video.streams.get_audio_only()