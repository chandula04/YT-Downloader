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
        Load a single YouTube video
        
        Args:
            url (str): YouTube video URL
            
        Returns:
            YouTube: YouTube object
            
        Raises:
            Exception: If video loading fails
        """
        try:
            self.current_video = YouTube(url)
            return self.current_video
        except Exception as e:
            raise Exception(f"Failed to load video: {str(e)}")
    
    def load_playlist(self, url):
        """
        Load a YouTube playlist
        
        Args:
            url (str): YouTube playlist URL
            
        Returns:
            Playlist: Playlist object
            
        Raises:
            Exception: If playlist loading fails
        """
        try:
            self.current_playlist = Playlist(url)
            return self.current_playlist
        except Exception as e:
            raise Exception(f"Failed to load playlist: {str(e)}")
    
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
        Get available quality options for a video
        
        Args:
            video (YouTube): YouTube video object
            
        Returns:
            list: List of quality options
        """
        streams = video.streams.filter(file_extension='mp4')
        quality_options = []
        
        # Get video-only streams (adaptive)
        adaptive_streams = streams.filter(adaptive=True, only_video=True)
        for stream in adaptive_streams:
            if stream.resolution:
                size_info = f" ({format_size(stream.filesize)})" if stream.filesize else ""
                quality_options.append(f"{stream.resolution} - Adaptive{size_info}")
        
        # Get progressive streams (with audio)
        prog_streams = streams.filter(progressive=True)
        for stream in prog_streams:
            if stream.resolution:
                size_info = f" ({format_size(stream.filesize)})" if stream.filesize else ""
                quality_options.append(f"{stream.resolution} - Progressive{size_info}")
        
        # Sort by resolution (highest first)
        quality_options.sort(key=resolution_key, reverse=True)
        
        return quality_options
    
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