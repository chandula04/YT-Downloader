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
            
            # Don't pre-filter, let the UI handle errors during iteration
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
        Extract video information with error handling
        
        Args:
            video (YouTube): YouTube video object
            
        Returns:
            dict: Video information dictionary
        """
        try:
            return {
                'title': getattr(video, 'title', 'Unknown Title'),
                'author': getattr(video, 'author', 'Unknown Author'),
                'length': getattr(video, 'length', 0),
                'thumbnail_url': getattr(video, 'thumbnail_url', '')
            }
        except Exception as e:
            print(f"Error getting video info: {e}")
            return {
                'title': 'Error Loading Video',
                'author': 'Unknown',
                'length': 0,
                'thumbnail_url': ''
            }
    
    def safe_load_video_from_url(self, video_url):
        """
        Safely load a video from URL with multiple client strategies
        
        Args:
            video_url (str): YouTube video URL
            
        Returns:
            YouTube: YouTube object or None if failed
        """
        clients_to_try = [
            {"use_oauth": False, "allow_oauth_cache": False},
            {"client": "ANDROID"},
            {"client": "TV_EMBED"},
        ]
        
        for client_config in clients_to_try:
            try:
                video = YouTube(video_url, **client_config)
                # Test if we can access basic properties
                _ = video.title  # This will fail if video is inaccessible
                return video
            except Exception:
                continue
        
        return None  # All clients failed
    
    def get_quality_options(self, video):
        """
        Get adaptive quality options for a video with sizes (highest quality)
        
        Args:
            video (YouTube): YouTube video object
            
        Returns:
            list: List of adaptive quality options only
        """
        try:
            streams = video.streams.filter(file_extension='mp4')
            quality_options = []
            
            # Get video-only streams (adaptive) - ONLY these for best quality
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
            
            # If no adaptive streams found, try alternative approach
            if not quality_options:
                try:
                    # Try to get any available video-only streams
                    video_only_streams = video.streams.filter(only_video=True, file_extension='mp4')
                    for stream in video_only_streams:
                        if hasattr(stream, 'resolution') and stream.resolution:
                            quality_options.append(f"{stream.resolution} - Adaptive")
                except Exception as e:
                    print(f"Error getting fallback adaptive streams: {e}")
            
            # If still no options, provide adaptive defaults
            if not quality_options:
                quality_options = ["1080p - Adaptive", "720p - Adaptive", "480p - Adaptive"]
            
            # Sort by resolution (highest first)
            try:
                quality_options.sort(key=resolution_key, reverse=True)
            except Exception:
                pass  # Keep original order if sorting fails
            
            return quality_options
            
        except Exception as e:
            print(f"Error getting quality options: {e}")
            # Return adaptive defaults if all else fails
            return ["1080p - Adaptive", "720p - Adaptive", "480p - Adaptive"]
    
    def get_simplified_quality_options(self, video):
        """
        Get simplified quality options for bulk selection
        
        Args:
            video (YouTube): YouTube video object
            
        Returns:
            list: List of simplified quality options
        """
        try:
            streams = video.streams.filter(file_extension='mp4')
            available_resolutions = set()
            
            # Get all available resolutions from both adaptive and progressive streams
            try:
                # Adaptive streams (video-only)
                adaptive_streams = streams.filter(adaptive=True, only_video=True)
                for stream in adaptive_streams:
                    if stream.resolution:
                        available_resolutions.add(stream.resolution)
                
                # Progressive streams (video+audio)
                prog_streams = streams.filter(progressive=True)
                for stream in prog_streams:
                    if stream.resolution:
                        available_resolutions.add(stream.resolution)
                        
            except Exception as e:
                print(f"Error getting streams: {e}")
            
            # Define the simplified quality options we want to show
            quality_mapping = {
                '144p': ['144p'],
                '360p': ['360p'],
                '480p': ['480p'],
                '720p': ['720p'],
                '1080p': ['1080p'],
                '2K': ['1440p', '2K'],
                '4K': ['2160p', '4K']
            }
            
            simplified_options = []
            
            # Check which simplified options are available
            for display_quality, possible_resolutions in quality_mapping.items():
                # Check if any of the possible resolutions are available
                if any(res in available_resolutions for res in possible_resolutions):
                    simplified_options.append(display_quality)
            
            # If no specific resolutions found, check what's actually available and map them
            if not simplified_options and available_resolutions:
                for resolution in available_resolutions:
                    # Extract numeric part for mapping
                    if '144' in resolution:
                        simplified_options.append('144p')
                    elif '360' in resolution:
                        simplified_options.append('360p')
                    elif '480' in resolution:
                        simplified_options.append('480p')
                    elif '720' in resolution:
                        simplified_options.append('720p')
                    elif '1080' in resolution:
                        simplified_options.append('1080p')
                    elif '1440' in resolution:
                        simplified_options.append('2K')
                    elif '2160' in resolution:
                        simplified_options.append('4K')
            
            # Remove duplicates and sort
            simplified_options = list(set(simplified_options))
            
            # Define sort order
            quality_order = {'144p': 1, '360p': 2, '480p': 3, '720p': 4, '1080p': 5, '2K': 6, '4K': 7}
            simplified_options.sort(key=lambda x: quality_order.get(x, 0), reverse=True)
            
            # If still no options, provide defaults
            if not simplified_options:
                simplified_options = ['720p', '480p', '360p']
            
            return simplified_options
            
        except Exception as e:
            print(f"Error getting simplified quality options: {e}")
            # Return default options if all else fails
            return ['720p', '480p', '360p']
    
    def get_best_stream_for_quality(self, video, target_quality):
        """
        Get the best adaptive stream that matches the target quality
        
        Args:
            video (YouTube): YouTube video object
            target_quality (str): Target quality (e.g., '720p', '1080p', '2K', '4K')
            
        Returns:
            Stream: Best matching adaptive stream or None
        """
        try:
            streams = video.streams.filter(file_extension='mp4')
            
            # Map simplified quality to actual resolutions
            resolution_mapping = {
                '144p': ['144p'],
                '360p': ['360p'],
                '480p': ['480p'],
                '720p': ['720p'],
                '1080p': ['1080p'],
                '2K': ['1440p'],
                '4K': ['2160p']
            }
            
            target_resolutions = resolution_mapping.get(target_quality, [target_quality])
            
            # Look for adaptive streams only (best quality)
            for target_res in target_resolutions:
                adaptive_stream = streams.filter(adaptive=True, only_video=True, resolution=target_res).first()
                if adaptive_stream:
                    return adaptive_stream
            
            # If no exact match, find closest adaptive quality
            # Get all available adaptive streams with resolutions
            available_streams = []
            adaptive_streams = streams.filter(adaptive=True, only_video=True)
            for stream in adaptive_streams:
                if stream.resolution:
                    available_streams.append(stream)
            
            if not available_streams:
                # Fallback: try any video-only stream
                video_only_streams = streams.filter(only_video=True)
                for stream in video_only_streams:
                    if stream.resolution:
                        available_streams.append(stream)
            
            if not available_streams:
                return None
            
            # Find closest resolution
            quality_values = {'144p': 144, '360p': 360, '480p': 480, '720p': 720, '1080p': 1080, '2K': 1440, '4K': 2160}
            target_value = quality_values.get(target_quality, 720)
            
            best_stream = None
            best_diff = float('inf')
            
            for stream in available_streams:
                res = stream.resolution
                if res:
                    # Extract numeric value from resolution
                    try:
                        res_value = int(res.replace('p', ''))
                        diff = abs(res_value - target_value)
                        if diff < best_diff:
                            best_diff = diff
                            best_stream = stream
                    except:
                        continue
            
            return best_stream
            
        except Exception as e:
            print(f"Error finding best adaptive stream for {target_quality}: {e}")
            return None
    
    def convert_simplified_to_detailed_quality(self, video, simplified_quality):
        """
        Convert simplified quality (e.g., '720p') to best matching adaptive quality option
        
        Args:
            video (YouTube): YouTube video object  
            simplified_quality (str): Simplified quality (e.g., '720p', '1080p', '2K', '4K')
            
        Returns:
            str: Best matching adaptive quality option
        """
        try:
            # Get all adaptive quality options for this video
            detailed_options = self.get_quality_options(video)
            
            # Map simplified to resolution patterns
            resolution_mapping = {
                '144p': '144p',
                '360p': '360p', 
                '480p': '480p',
                '720p': '720p',
                '1080p': '1080p',
                '2K': '1440p',
                '4K': '2160p'
            }
            
            target_resolution = resolution_mapping.get(simplified_quality, simplified_quality)
            
            # Find best adaptive match
            best_match = None
            
            for option in detailed_options:
                if target_resolution in option and 'Adaptive' in option:
                    best_match = option
                    break  # Take the first (best) adaptive match
            
            # If no exact match, find closest adaptive option
            if not best_match and detailed_options:
                # Just return the best available adaptive option
                for option in detailed_options:
                    if 'Adaptive' in option:
                        best_match = option
                        break
                
                # If still no adaptive found, return the first option
                if not best_match:
                    best_match = detailed_options[0]
            
            return best_match or f"{simplified_quality} - Adaptive"
            
        except Exception as e:
            print(f"Error converting quality: {e}")
            return f"{simplified_quality} - Adaptive"
    
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