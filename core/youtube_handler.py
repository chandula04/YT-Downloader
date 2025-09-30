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
            # Updated client strategies to handle YouTube's latest anti-bot measures  
            # Reordered to prioritize clients with better stream access
            clients_to_try = [
                # iOS client often bypasses restrictions and has good stream access
                {"use_oauth": False, "allow_oauth_cache": False, "client": "IOS"},
                # Android client with no cache - reliable for streams
                {"use_oauth": False, "allow_oauth_cache": False, "client": "ANDROID"},
                # Web client with different user agent - good stream support
                {"use_oauth": False, "allow_oauth_cache": False, "client": "WEB"},
                # Android Music client
                {"use_oauth": False, "allow_oauth_cache": False, "client": "ANDROID_MUSIC"},
                # Basic fallback
                {"use_oauth": False, "allow_oauth_cache": False},
                # TV Embed client bypasses restrictions but often has stream issues (last)
                {"use_oauth": False, "allow_oauth_cache": False, "client": "TV_EMBED"},
            ]
            
            last_error = None
            for i, client_config in enumerate(clients_to_try):
                try:
                    client_name = client_config.get("client", "DEFAULT")
                    print(f"🔄 Trying client {i+1}/{len(clients_to_try)}: {client_name}")
                    
                    self.current_video = YouTube(url, **client_config)
                    
                    # Test if we can access basic properties
                    title = self.current_video.title
                    length = self.current_video.length
                    
                    print(f"✅ Video loaded successfully with {client_name}")
                    print(f"📹 Title: {title[:50]}...")
                    print(f"⏱️ Duration: {length}s")
                    
                    # Test stream access (critical for download functionality)
                    try:
                        streams = self.current_video.streams.filter(file_extension='mp4')
                        if streams and len(streams) > 0:
                            print(f"🎬 {client_name} has {len(streams)} streams available")
                            return self.current_video
                        else:
                            print(f"⚠️ {client_name} loaded video but no streams found, trying next client...")
                            continue
                            
                    except Exception as stream_error:
                        print(f"❌ {client_name} video loaded but streams failed: {str(stream_error)[:50]}...")
                        # If this is TV_EMBED with stream issues, it's expected
                        if client_name == "TV_EMBED":
                            print(f"ℹ️ {client_name} has known stream access issues")
                        # Continue to next client for better stream access
                        continue
                    
                except Exception as e:
                    last_error = e
                    error_msg = str(e)
                    print(f"❌ {client_name} client failed: {error_msg[:100]}...")
                    
                    # Skip to next client
                    continue
            
            # If all clients fail, raise the last error with helpful message
            print("❌ All client strategies failed")
            print("💡 This might be due to:")
            print("   - YouTube's anti-bot measures")
            print("   - Video is private/restricted")
            print("   - Network connectivity issues")
            print("   - pytubefix needs updating")
            
            raise last_error or Exception("All client strategies failed to load video")
            
        except Exception as e:
            error_msg = f"Failed to load video: {str(e)}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
    
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
        # Use same improved client strategies as load_video
        clients_to_try = [
            {"use_oauth": False, "allow_oauth_cache": False, "client": "IOS"},
            {"use_oauth": False, "allow_oauth_cache": False, "client": "ANDROID"},
            {"use_oauth": False, "allow_oauth_cache": False, "client": "TV_EMBED"},
            {"use_oauth": False, "allow_oauth_cache": False, "client": "WEB"},
            {"use_oauth": False, "allow_oauth_cache": False, "client": "ANDROID_MUSIC"},
            {"use_oauth": False, "allow_oauth_cache": False},
        ]
        
        for i, client_config in enumerate(clients_to_try):
            try:
                client_name = client_config.get("client", "DEFAULT")
                print(f"🔄 Safe load trying {client_name}...")
                
                video = YouTube(video_url, **client_config)
                # Test if we can access basic properties
                _ = video.title  # This will fail if video is inaccessible
                
                print(f"✅ Safe load successful with {client_name}")
                return video
                
            except Exception as e:
                print(f"❌ Safe load {client_name} failed: {str(e)[:50]}...")
                continue
        
        print("❌ All safe load attempts failed")
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
            # First, try to get streams with the current video object
            streams = None
            try:
                streams = video.streams.filter(file_extension='mp4')
                print(f"📊 Found {len(streams)} total streams")
            except Exception as e:
                print(f"❌ Current client can't access streams: {e}")
                
                # If current client can't get streams, try other clients for stream data
                print("🔄 Trying alternative clients for stream data...")
                
                # Try different clients specifically for stream access
                stream_clients = [
                    {"use_oauth": False, "allow_oauth_cache": False, "client": "ANDROID"},
                    {"use_oauth": False, "allow_oauth_cache": False, "client": "IOS"}, 
                    {"use_oauth": False, "allow_oauth_cache": False, "client": "WEB"},
                    {"use_oauth": False, "allow_oauth_cache": False}
                ]
                
                for client_config in stream_clients:
                    try:
                        client_name = client_config.get("client", "DEFAULT")
                        print(f"🔄 Trying {client_name} for streams...")
                        
                        temp_video = YouTube(video.watch_url, **client_config)
                        streams = temp_video.streams.filter(file_extension='mp4')
                        
                        if streams and len(streams) > 0:
                            print(f"✅ {client_name} provided {len(streams)} streams")
                            video = temp_video  # Use this client's video object
                            break
                    except Exception as client_error:
                        print(f"❌ {client_name} streams failed: {str(client_error)[:50]}...")
                        continue
            
            quality_options = []
            
            # If we have streams, process them
            if streams and len(streams) > 0:
                try:
                    # Get video-only streams (adaptive) - ONLY these for best quality
                    adaptive_streams = streams.filter(adaptive=True, only_video=True)
                    print(f"📹 Found {len(adaptive_streams)} adaptive video streams")
                    
                    # Debug: Print all available resolutions
                    print("🔍 Available resolutions from streams:")
                    for stream in adaptive_streams:
                        if hasattr(stream, 'resolution') and stream.resolution:
                            bitrate_info = f" (bitrate: {stream.bitrate})" if hasattr(stream, 'bitrate') and stream.bitrate else ""
                            print(f"   • {stream.resolution}{bitrate_info}")
                    
                    # Create a dictionary to store best stream for each resolution
                    resolution_streams = {}
                    
                    for stream in adaptive_streams:
                        if hasattr(stream, 'resolution') and stream.resolution:
                            res = stream.resolution
                            print(f"🎯 Processing {res} stream...")
                            
                            # Keep the stream with highest bitrate for each resolution
                            if res not in resolution_streams:
                                resolution_streams[res] = stream
                            elif hasattr(stream, 'bitrate') and hasattr(resolution_streams[res], 'bitrate'):
                                if stream.bitrate and stream.bitrate > resolution_streams[res].bitrate:
                                    resolution_streams[res] = stream
                    
                    print(f"📊 Processed {len(resolution_streams)} unique resolutions")
                    
                    # Convert to quality options with file sizes
                    for resolution, stream in resolution_streams.items():
                        try:
                            size_info = ""
                            
                            print(f"🔍 Processing resolution: {resolution}")
                            
                            # Method 1: Try to get direct file size
                            if hasattr(stream, 'filesize') and stream.filesize and stream.filesize > 0:
                                size_info = f" ({format_size(stream.filesize)})"
                                print(f"✅ {resolution}: Direct size {size_info}")
                            
                            # Method 2: Try to force load file size by accessing stream properties
                            elif hasattr(stream, 'filesize'):
                                try:
                                    # Sometimes filesize is None until accessed
                                    _ = stream.url  # This can trigger size calculation
                                    if stream.filesize and stream.filesize > 0:
                                        size_info = f" ({format_size(stream.filesize)})"
                                        print(f"✅ {resolution}: Loaded size {size_info}")
                                except:
                                    pass
                            
                            # Method 3: Calculate approximate size using bitrate
                            if not size_info:
                                try:
                                    if (hasattr(video, 'length') and video.length and 
                                        hasattr(stream, 'bitrate') and stream.bitrate):
                                        # Calculate size: bitrate (bits/sec) * duration (sec) / 8 (bits to bytes)
                                        estimated_bytes = (stream.bitrate * video.length) // 8
                                        size_info = f" (~{format_size(estimated_bytes)})"
                                        print(f"🔢 {resolution}: Calculated size {size_info}")
                                except Exception as e:
                                    print(f"❌ Could not calculate size for {resolution}: {e}")
                            
                            # Method 4: Try alternative bitrate calculation
                            if not size_info:
                                try:
                                    # Try to get average bitrate based on resolution
                                    estimated_bitrate = self._estimate_bitrate_by_resolution(resolution)
                                    if estimated_bitrate and hasattr(video, 'length') and video.length:
                                        estimated_bytes = (estimated_bitrate * video.length) // 8
                                        size_info = f" (~{format_size(estimated_bytes)})"
                                        print(f"📊 {resolution}: Estimated size {size_info}")
                                except:
                                    pass
                            
                            # Create quality string with special 8K, 4K, 2K labels
                            quality_str = f"{resolution} - Adaptive{size_info}"
                            if resolution == "4320p":
                                quality_str = f"{resolution} - Adaptive{size_info} (8K)"
                            elif resolution == "2160p":
                                quality_str = f"{resolution} - Adaptive{size_info} (4K)"
                            elif resolution == "1440p":
                                quality_str = f"{resolution} - Adaptive{size_info} (2K)"
                            elif resolution == "1080p":
                                quality_str = f"{resolution} - Adaptive{size_info} (Full HD)"
                            elif resolution == "720p":
                                quality_str = f"{resolution} - Adaptive{size_info} (HD)"
                            elif resolution == "480p":
                                quality_str = f"{resolution} - Adaptive{size_info} (SD)"
                                
                            quality_options.append(quality_str)
                            print(f"✅ Added: {quality_str}")
                            
                        except Exception as e:
                            # Fallback without size info
                            quality_str = f"{resolution} - Adaptive"
                            if resolution == "4320p":
                                quality_str = f"{resolution} - Adaptive (8K)"
                            elif resolution == "2160p":
                                quality_str = f"{resolution} - Adaptive (4K)"
                            elif resolution == "1440p":
                                quality_str = f"{resolution} - Adaptive (2K)"
                            
                            quality_options.append(quality_str)
                            print(f"⚠️ Added without size: {quality_str}")
                            
                except Exception as e:
                    print(f"❌ Error processing adaptive streams: {e}")
            
            # If no streams or adaptive streams found, provide comprehensive defaults with sizes
            if not quality_options:
                print("📋 No streams found, using comprehensive defaults with estimated sizes...")
                try:
                    # Try to get video duration for size estimates
                    duration = getattr(video, 'length', 180)  # Default to 3 minutes if unknown
                    print(f"⏱️ Using duration: {duration}s for size estimates")
                    
                    # Comprehensive resolution list with 2K, 4K, 8K
                    fallback_options = [
                        ("4320p", "8K", 50000000),   # 8K Ultra HD
                        ("2160p", "4K", 25000000),   # 4K Ultra HD
                        ("1440p", "2K", 10000000),   # 2K Quad HD
                        ("1080p", "Full HD", 5000000), # Full HD
                        ("720p", "HD", 2500000),     # HD Ready
                        ("480p", "SD", 800000),      # Standard Definition
                        ("360p", "", 300000),        # Low Quality
                        ("240p", "", 150000),        # Very Low Quality
                        ("144p", "", 80000)          # Minimum Quality
                    ]
                    
                    for resolution, label, bitrate in fallback_options:
                        try:
                            estimated_bytes = (bitrate * duration) // 8
                            size_info = f" (~{format_size(estimated_bytes)})"
                            label_info = f" ({label})" if label else ""
                            quality_str = f"{resolution} - Adaptive{size_info}{label_info}"
                            quality_options.append(quality_str)
                            print(f"📋 Added fallback: {quality_str}")
                        except:
                            label_info = f" ({label})" if label else ""
                            quality_str = f"{resolution} - Adaptive{label_info}"
                            quality_options.append(quality_str)
                            print(f"📋 Added basic fallback: {quality_str}")
                            
                except Exception:
                    # Ultimate comprehensive fallback
                    quality_options = [
                        "4320p - Adaptive (8K)",
                        "2160p - Adaptive (4K)",
                        "1440p - Adaptive (2K)", 
                        "1080p - Adaptive (Full HD)",
                        "720p - Adaptive (HD)",
                        "480p - Adaptive (SD)",
                        "360p - Adaptive",
                        "240p - Adaptive",
                        "144p - Adaptive"
                    ]
                    print("📋 Using ultimate comprehensive fallback")
            
            # ALWAYS ensure 8K option is present (even if not actually available)
            has_8k = any("4320p" in option for option in quality_options)
            if not has_8k:
                print("🎯 Adding 8K option (may not be available for this video)")
                try:
                    duration = getattr(video, 'length', 180)
                    estimated_bytes = (50000000 * duration) // 8  # 50 Mbps for 8K
                    size_info = f" (~{format_size(estimated_bytes)})"
                    quality_options.insert(0, f"4320p - Adaptive{size_info} (8K)")
                except:
                    quality_options.insert(0, "4320p - Adaptive (8K)")
                    
            # ALWAYS ensure 4K option is present
            has_4k = any("2160p" in option for option in quality_options)
            if not has_4k:
                print("🎯 Adding 4K option (may not be available for this video)")
                try:
                    duration = getattr(video, 'length', 180)
                    estimated_bytes = (25000000 * duration) // 8  # 25 Mbps for 4K
                    size_info = f" (~{format_size(estimated_bytes)})"
                    # Insert after 8K if present, otherwise at the beginning
                    insert_pos = 1 if has_8k else 0
                    quality_options.insert(insert_pos, f"2160p - Adaptive{size_info} (4K)")
                except:
                    insert_pos = 1 if has_8k else 0
                    quality_options.insert(insert_pos, "2160p - Adaptive (4K)")
                    
            # ALWAYS ensure 2K option is present
            has_2k = any("1440p" in option for option in quality_options)
            if not has_2k:
                print("🎯 Adding 2K option (may not be available for this video)")
                try:
                    duration = getattr(video, 'length', 180)
                    estimated_bytes = (10000000 * duration) // 8  # 10 Mbps for 2K
                    size_info = f" (~{format_size(estimated_bytes)})"
                    # Insert after 4K
                    insert_pos = 2 if has_8k and has_4k else (1 if has_4k or has_8k else 0)
                    quality_options.insert(insert_pos, f"1440p - Adaptive{size_info} (2K)")
                except:
                    insert_pos = 2 if has_8k and has_4k else (1 if has_4k or has_8k else 0)
                    quality_options.insert(insert_pos, "1440p - Adaptive (2K)")
            
            # Sort by resolution (highest first) - updated to handle 4K/2K/8K properly
            try:
                quality_options.sort(key=resolution_key, reverse=True)
                print(f"🔄 Sorted {len(quality_options)} quality options")
            except Exception:
                print("⚠️ Sorting failed, keeping original order")
                pass  # Keep original order if sorting fails
            
            # Remove duplicates while preserving order
            seen = set()
            unique_options = []
            for option in quality_options:
                resolution = option.split(' ')[0]  # Get just the resolution part
                if resolution not in seen:
                    seen.add(resolution)
                    unique_options.append(option)
            
            print(f"✅ Final quality options: {len(unique_options)} unique resolutions")
            for option in unique_options:
                print(f"   • {option}")
            
            return unique_options
            
        except Exception as e:
            print(f"❌ Error getting quality options: {e}")
            
            # Handle specific throttling error
            if "throttling_function_name" in str(e) or "could not find match for multiple" in str(e):
                print("🚫 YouTube throttling detected!")
                print("💡 Suggested solutions:")
                print("   1. Wait a few minutes and try again")
                print("   2. Try a different video")
                print("   3. Check if pytubefix needs updating")
                print("   4. Use a VPN if available")
                
                # Return comprehensive fallback options for throttling with all resolutions
                print("🔄 Using comprehensive throttling fallback...")
                return [
                    "4320p - Adaptive (~15 GB) (8K)",
                    "2160p - Adaptive (~7.5 GB) (4K)",
                    "1440p - Adaptive (~3 GB) (2K)",
                    "1080p - Adaptive (~1.5 GB) (Full HD)",
                    "720p - Adaptive (~700 MB) (HD)",
                    "480p - Adaptive (~300 MB) (SD)",
                    "360p - Adaptive (~150 MB)",
                    "240p - Adaptive (~75 MB)",
                    "144p - Adaptive (~35 MB)"
                ]
            
            # Return comprehensive adaptive defaults with estimated sizes if all else fails
            try:
                # Assume 3 minute video for estimates
                print("📋 Using comprehensive error fallback with all resolutions...")
                fallback_with_sizes = []
                fallback_resolutions = [
                    ("4320p", "8K", 50000000),
                    ("2160p", "4K", 25000000),
                    ("1440p", "2K", 10000000), 
                    ("1080p", "Full HD", 5000000),
                    ("720p", "HD", 2500000),
                    ("480p", "SD", 800000),
                    ("360p", "", 300000),
                    ("240p", "", 150000),
                    ("144p", "", 80000)
                ]
                
                for resolution, label, bitrate in fallback_resolutions:
                    estimated_bytes = (bitrate * 180) // 8  # 3 minutes
                    size_info = f" (~{format_size(estimated_bytes)})"
                    label_info = f" ({label})" if label else ""
                    fallback_with_sizes.append(f"{resolution} - Adaptive{size_info}{label_info}")
                
                return fallback_with_sizes
                
            except:
                # Ultimate fallback with all resolutions
                return [
                    "4320p - Adaptive (8K)",
                    "2160p - Adaptive (4K)",
                    "1440p - Adaptive (2K)", 
                    "1080p - Adaptive (Full HD)",
                    "720p - Adaptive (HD)",
                    "480p - Adaptive (SD)",
                    "360p - Adaptive",
                    "240p - Adaptive", 
                    "144p - Adaptive"
                ]
    
    def get_simplified_quality_options(self, video):
        """
        Get simplified quality options for bulk selection (adaptive streams only)
        
        Args:
            video (YouTube): YouTube video object
            
        Returns:
            list: List of simplified quality options
        """
        try:
            streams = video.streams.filter(file_extension='mp4')
            available_resolutions = set()
            
            # Get all available resolutions from adaptive streams only (best quality)
            try:
                # Adaptive streams (video-only) - ONLY these for best quality
                adaptive_streams = streams.filter(adaptive=True, only_video=True)
                for stream in adaptive_streams:
                    if hasattr(stream, 'resolution') and stream.resolution:
                        available_resolutions.add(stream.resolution)
                        
            except Exception as e:
                print(f"Error getting adaptive streams: {e}")
            
            # Define the simplified quality options we want to show (comprehensive list)
            quality_mapping = {
                '8K': ['4320p', '8K'],
                '4K': ['2160p', '4K'],
                '2K': ['1440p', '2K'],
                '1080p': ['1080p'],
                '720p': ['720p'],
                '480p': ['480p'],
                '360p': ['360p'],
                '240p': ['240p'],
                '144p': ['144p']
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
                    if '4320' in resolution or '8K' in resolution.upper():
                        if '8K' not in simplified_options:
                            simplified_options.append('8K')
                    elif '2160' in resolution or '4K' in resolution.upper():
                        if '4K' not in simplified_options:
                            simplified_options.append('4K')
                    elif '1440' in resolution or '2K' in resolution.upper():
                        if '2K' not in simplified_options:
                            simplified_options.append('2K')
                    elif '1080' in resolution:
                        if '1080p' not in simplified_options:
                            simplified_options.append('1080p')
                    elif '720' in resolution:
                        if '720p' not in simplified_options:
                            simplified_options.append('720p')
                    elif '480' in resolution:
                        if '480p' not in simplified_options:
                            simplified_options.append('480p')
                    elif '360' in resolution:
                        if '360p' not in simplified_options:
                            simplified_options.append('360p')
                    elif '240' in resolution:
                        if '240p' not in simplified_options:
                            simplified_options.append('240p')
                    elif '144' in resolution:
                        if '144p' not in simplified_options:
                            simplified_options.append('144p')
            
            # If still no options found, provide comprehensive defaults
            if not simplified_options:
                simplified_options = ['4K', '2K', '1080p', '720p', '480p', '360p']
            
            # Sort by quality (highest first)
            quality_order = ['8K', '4K', '2K', '1080p', '720p', '480p', '360p', '240p', '144p']
            simplified_options.sort(key=lambda x: quality_order.index(x) if x in quality_order else 999)
            
            return simplified_options
            
        except Exception as e:
            print(f"Error getting simplified quality options: {e}")
            # Return comprehensive defaults if all else fails
            return ['4K', '2K', '1080p', '720p', '480p', '360p']
    
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
        Convert simplified quality (e.g., '720p', '2K', '4K') to best matching adaptive quality option
        
        Args:
            video (YouTube): YouTube video object  
            simplified_quality (str): Simplified quality (e.g., '720p', '1080p', '2K', '4K')
            
        Returns:
            str: Best matching adaptive quality option
        """
        try:
            # Get all adaptive quality options for this video
            detailed_options = self.get_quality_options(video)
            
            # Map simplified to resolution patterns (comprehensive mapping)
            resolution_mapping = {
                '8K': ['4320p', '8K'],
                '4K': ['2160p', '4K'],
                '2K': ['1440p', '2K'],
                '1080p': ['1080p'],
                '720p': ['720p'],
                '480p': ['480p'],
                '360p': ['360p'],
                '240p': ['240p'],
                '144p': ['144p']
            }
            
            target_resolutions = resolution_mapping.get(simplified_quality, [simplified_quality])
            
            # Find best adaptive match
            best_match = None
            
            # Look for exact matches first
            for option in detailed_options:
                if 'Adaptive' in option:
                    for target_res in target_resolutions:
                        if target_res in option:
                            best_match = option
                            break
                    if best_match:
                        break
            
            # If no exact match, find closest adaptive option based on quality hierarchy
            if not best_match and detailed_options:
                # Quality hierarchy (best to worst)
                quality_preference = ['2160p', '1440p', '1080p', '720p', '480p', '360p', '240p', '144p']
                
                # Find the target quality index
                target_index = None
                for target_res in target_resolutions:
                    if target_res in quality_preference:
                        target_index = quality_preference.index(target_res)
                        break
                
                if target_index is not None:
                    # Look for closest available quality
                    for i in range(len(quality_preference)):
                        # Check both directions from target
                        for direction in [0, 1, -1, 2, -2, 3, -3]:
                            check_index = target_index + direction
                            if 0 <= check_index < len(quality_preference):
                                check_res = quality_preference[check_index]
                                for option in detailed_options:
                                    if check_res in option and 'Adaptive' in option:
                                        best_match = option
                                        break
                                if best_match:
                                    break
                        if best_match:
                            break
                
                # If still no match, just take the first adaptive option available
                if not best_match:
                    for option in detailed_options:
                        if 'Adaptive' in option:
                            best_match = option
                            break
            
            # Return best match or fallback
            if best_match:
                return best_match
            else:
                # Create fallback adaptive option
                fallback_resolution = target_resolutions[0] if target_resolutions else simplified_quality
                return f"{fallback_resolution} - Adaptive"
                
        except Exception as e:
            print(f"Error converting simplified quality: {e}")
            # Fallback to adaptive version of input
            return f"{simplified_quality} - Adaptive"
    
    def _estimate_bitrate_by_resolution(self, resolution):
        """
        Estimate typical bitrate for a given resolution (adaptive streams)
        
        Args:
            resolution (str): Resolution like "1080p", "720p", etc.
            
        Returns:
            int: Estimated bitrate in bits per second
        """
        # Typical bitrates for adaptive video streams (bits per second)
        bitrate_estimates = {
            '144p': 80000,      # ~80 Kbps
            '240p': 150000,     # ~150 Kbps  
            '360p': 300000,     # ~300 Kbps
            '480p': 800000,     # ~800 Kbps
            '720p': 2500000,    # ~2.5 Mbps
            '1080p': 5000000,   # ~5 Mbps
            '1440p': 10000000,  # ~10 Mbps (2K)
            '2160p': 25000000,  # ~25 Mbps (4K)
            '4320p': 50000000,  # ~50 Mbps (8K)
        }
        
        return bitrate_estimates.get(resolution, 2000000)  # Default to 2 Mbps
    
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