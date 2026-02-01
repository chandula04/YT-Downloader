"""
Download management and progress tracking
"""

import os
import time
import threading
from utils.helpers import safe_filename, parse_quality_string
from utils.ffmpeg_handler import FFmpegHandler
from core.youtube_handler import YouTubeHandler
from core.file_manager import file_manager
from config.user_settings import user_settings


class DownloadManager:
    """Manages download operations and progress tracking"""
    
    def __init__(self):
        self.youtube_handler = YouTubeHandler()
        self.ffmpeg_handler = FFmpegHandler()
        self.stop_flag = False
        self.current_thread = None
        
        # Progress tracking
        self.start_time = 0
        self.last_time = 0
        self.last_bytes = 0
        self.current_download_size = 0
        self.progress_callback = None
        
        # Batch download tracking
        self.batch_progress_callback = None
        self.current_video_index = -1
        self.total_videos_in_batch = 0
        
        # Video caching to prevent re-fetching
        self.cached_video = None
        self.cached_video_url = None
    
    def set_progress_callback(self, callback):
        """
        Set callback function for progress updates
        
        Args:
            callback (callable): Function to call with progress updates
        """
        self.progress_callback = callback
    
    def set_batch_progress_callback(self, callback):
        """
        Set callback function for batch progress updates
        
        Args:
            callback (callable): Function to call with batch progress updates
                                Signature: callback(video_index, status, video_title)
        """
        self.batch_progress_callback = callback
    
    def cancel_download(self):
        """Cancel the current download operation"""
        self.stop_flag = True
    
    def is_downloading(self):
        """
        Check if a download is currently in progress
        
        Returns:
            bool: True if downloading, False otherwise
        """
        return self.current_thread and self.current_thread.is_alive()
    
    def progress_tracker(self, stream, chunk, bytes_remaining):
        """
        Track download progress and call progress callback
        
        Args:
            stream: YouTube stream object
            chunk: Downloaded chunk
            bytes_remaining (int): Bytes remaining to download
        """
        if self.stop_flag:
            # Raise KeyboardInterrupt to force stop the download stream
            raise KeyboardInterrupt("Download cancelled by user")
        
        current_time = time.time()

        # Initialize timing if not set
        if not self.start_time:
            self.start_time = current_time
            self.last_time = current_time

        # Try to resolve total size if unknown
        if self.current_download_size <= 0:
            total = getattr(stream, 'filesize', None) or getattr(stream, 'filesize_approx', None)
            if total and total > 0:
                self.current_download_size = total
            elif bytes_remaining is not None:
                self.current_download_size = bytes_remaining + len(chunk) + self.last_bytes

        # Compute bytes downloaded safely
        if self.current_download_size > 0 and bytes_remaining is not None:
            bytes_downloaded = max(self.current_download_size - bytes_remaining, 0)
            percentage = (bytes_downloaded / self.current_download_size) * 100
        else:
            bytes_downloaded = self.last_bytes + len(chunk)
            percentage = 0
        
        # Calculate download speed
        delta_time = current_time - self.last_time
        delta_bytes = bytes_downloaded - self.last_bytes
        
        if delta_time > 0:
            speed = delta_bytes / delta_time  # bytes per second
            speed_mbps = speed / (1024 * 1024)  # MB per second
        else:
            speed_mbps = 0
        
        elapsed = int(current_time - self.start_time) if self.start_time else 0
        
        # Call progress callback immediately for real-time updates
        if self.progress_callback:
            self.progress_callback(
                bytes_downloaded, 
                self.current_download_size, 
                percentage, 
                speed_mbps,
                elapsed
            )
        
        self.last_time = current_time
        self.last_bytes = bytes_downloaded

    def _reset_progress_tracking(self, total_size):
        """Reset progress tracking for a new stream download."""
        self.current_download_size = total_size or 0
        self.start_time = time.time()
        self.last_time = self.start_time
        self.last_bytes = 0
    
    def download_single_video(self, video, quality_str, is_audio, output_path):
        """
        Download a single video using adaptive streams for best quality
        
        Args:
            video (YouTube): YouTube video object
            quality_str (str): Quality string (e.g., "1080p - Adaptive (1.5 GB)" or "720p")
            is_audio (bool): Whether to download as audio only
            output_path (str): Output directory path
        """
        if is_audio:
            self._download_audio(video, output_path)
        else:
            # All video downloads now use adaptive streams for best quality
            if ' - ' in quality_str and 'Adaptive' in quality_str:
                # Detailed adaptive quality string
                from utils.helpers import parse_quality_string
                resolution, stream_type = parse_quality_string(quality_str)
                self._download_adaptive(video, resolution, output_path)
            else:
                # Simplified quality string - get best adaptive stream
                best_stream = self.youtube_handler.get_best_stream_for_quality(video, quality_str)
                if not best_stream:
                    # Fallback to any available adaptive stream
                    streams = video.streams.filter(file_extension='mp4', adaptive=True, only_video=True)
                    best_stream = streams.first()
                
                if not best_stream:
                    raise Exception(f"No adaptive stream found for {quality_str}")
                
                # Always use adaptive download for best quality
                self._download_adaptive_stream(best_stream, video, output_path)
    
    def _download_audio(self, video, output_path):
        """Download audio only as MP3"""
        audio_stream = self.youtube_handler.get_audio_only_stream(video)
        if not audio_stream:
            raise Exception("No audio stream available")

        total_size = getattr(audio_stream, 'filesize', None) or getattr(audio_stream, 'filesize_approx', None) or 0
        self._reset_progress_tracking(total_size)
        video.register_on_progress_callback(self.progress_tracker)
        
        # Download audio directly as mp3
        output_filename = f"{safe_filename(video.title)}.mp3"
        full_output_path = os.path.join(output_path, output_filename)
        
        try:
            audio_stream.download(output_path=output_path, filename=output_filename)
        except KeyboardInterrupt:
            # User cancelled - propagate the cancellation
            raise
    
    def _download_adaptive(self, video, resolution, output_path):
        """Download adaptive streams and merge with FFmpeg"""
        # Get video and audio streams
        video_stream = self.youtube_handler.get_stream_by_quality(
            video, resolution, "Adaptive"
        )
        audio_stream = self.youtube_handler.get_best_audio_stream(video)
        
        if not video_stream or not audio_stream:
            raise Exception("No suitable streams available")
        
        # Download video
        total_size = getattr(video_stream, 'filesize', None) or getattr(video_stream, 'filesize_approx', None) or 0
        self._reset_progress_tracking(total_size)
        video.register_on_progress_callback(self.progress_tracker)
        
        try:
            video_path = video_stream.download(output_path=output_path, filename="video_temp.mp4")
        except KeyboardInterrupt:
            # User cancelled during video download - clean up and propagate
            self.ffmpeg_handler.cleanup_default_temp_files(output_path)
            raise
        
        # Check if cancelled between downloads
        if self.stop_flag:
            self.ffmpeg_handler.cleanup_temp_files(video_path)
            self.ffmpeg_handler.cleanup_default_temp_files(output_path)
            raise KeyboardInterrupt("Download cancelled")
        
        # Download audio
        total_size = getattr(audio_stream, 'filesize', None) or getattr(audio_stream, 'filesize_approx', None) or 0
        self._reset_progress_tracking(total_size)
        video.register_on_progress_callback(self.progress_tracker)
        
        try:
            audio_path = audio_stream.download(output_path=output_path, filename="audio_temp.mp4")
        except KeyboardInterrupt:
            # User cancelled during audio download - clean up and propagate
            self.ffmpeg_handler.cleanup_temp_files(video_path)
            self.ffmpeg_handler.cleanup_default_temp_files(output_path)
            raise
        
        # Check if cancelled before merging
        if self.stop_flag:
            self.ffmpeg_handler.cleanup_temp_files(video_path, audio_path)
            self.ffmpeg_handler.cleanup_default_temp_files(output_path)
            raise KeyboardInterrupt("Download cancelled")
        
        # Merge with FFmpeg with progress tracking
        output_filename = f"{safe_filename(video.title)}.mp4"
        final_output_path = os.path.join(output_path, output_filename)
        
        try:
            # Create FFmpeg progress callback
            def ffmpeg_progress(percentage, stage):
                if self.progress_callback:
                    # Call with proper signature: downloaded, total, percentage, speed, elapsed, custom_text
                    self.progress_callback(0, 0, percentage, 0, 0, f"🎬 {stage}")
            
            self.ffmpeg_handler.merge_video_audio(
                video_path,
                audio_path,
                final_output_path,
                ffmpeg_progress
            )
        except OSError as e:
            # Handle Windows compatibility errors specifically
            if "WinError 216" in str(e) or "not compatible with the version of Windows" in str(e):
                self.ffmpeg_handler.cleanup_temp_files(video_path, audio_path)
                self.ffmpeg_handler.cleanup_default_temp_files(output_path)
                raise Exception(
                    "FFmpeg compatibility error detected!\n\n"
                    "This happens when FFmpeg version doesn't match your Windows.\n\n"
                    "Solutions:\n"
                    "1. Close the app and run 'setup_ffmpeg.py' manually\n"
                    "2. Or delete the 'ffmpeg' folder and restart the app\n"
                    "3. The app will download the correct FFmpeg version\n\n"
                    "Your Windows system needs a different FFmpeg build."
                )
            else:
                self.ffmpeg_handler.cleanup_temp_files(video_path, audio_path)
                self.ffmpeg_handler.cleanup_default_temp_files(output_path)
                raise Exception(f"FFmpeg error: {str(e)}")
        except Exception as e:
            self.ffmpeg_handler.cleanup_temp_files(video_path, audio_path)
            self.ffmpeg_handler.cleanup_default_temp_files(output_path)
            # Check if it's a compatibility issue
            if "WinError 216" in str(e) or "not compatible" in str(e):
                raise Exception(
                    "Windows compatibility issue detected!\n\n"
                    "Your FFmpeg version is not compatible with your Windows.\n\n"
                    "Quick fix:\n"
                    "1. Close this app\n"
                    "2. Delete the 'ffmpeg' folder\n"
                    "3. Run the app again\n\n"
                    "The app will automatically download the correct version."
                )
            else:
                raise e
        finally:
            # Clean up temporary files
            self.ffmpeg_handler.cleanup_temp_files(video_path, audio_path)
            self.ffmpeg_handler.cleanup_default_temp_files(output_path)
    
    def _download_adaptive_stream(self, video_stream, video, output_path):
        """Download adaptive stream and merge with audio"""
        video_title = video.title
        safe_name = safe_filename(video_title)
        
        video_path = None
        audio_path = None
        try:
            # Download video stream
            total_size = getattr(video_stream, 'filesize', None) or getattr(video_stream, 'filesize_approx', None) or 0
            self._reset_progress_tracking(total_size)
            video.register_on_progress_callback(self.progress_tracker)
            video_path = video_stream.download(output_path=output_path, filename="video_temp.mp4")
            
            if self.stop_flag:
                self.ffmpeg_handler.cleanup_temp_files(video_path)
                self.ffmpeg_handler.cleanup_default_temp_files(output_path)
                raise Exception("Download cancelled")
            
            audio_stream = video.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
            if not audio_stream:
                audio_stream = video.streams.filter(only_audio=True).order_by('abr').desc().first()
            
            if audio_stream:
                self.current_download_size = audio_stream.filesize if hasattr(audio_stream, 'filesize') else 0
                audio_path = audio_stream.download(output_path=output_path, filename="audio_temp.mp4")
                
                if self.stop_flag:
                    self.ffmpeg_handler.cleanup_temp_files(video_path, audio_path)
                    self.ffmpeg_handler.cleanup_default_temp_files(output_path)
                    raise Exception("Download cancelled")
                
                output_file = os.path.join(output_path, safe_name + '.mp4')
                self.ffmpeg_handler.merge_video_audio(
                    video_path,
                    audio_path,
                    output_file
                )
                print(f"✅ Adaptive video merged: {output_file}")
            else:
                final_path = os.path.join(output_path, safe_name + '.mp4')
                try:
                    os.rename(video_path, final_path)
                    print(f"✅ Video-only file saved: {final_path}")
                except:
                    print(f"✅ Video saved: {video_path}")
                finally:
                    self.ffmpeg_handler.cleanup_default_temp_files(output_path)
        except OSError as e:
            if "WinError 216" in str(e) or "not compatible with the version of Windows" in str(e):
                raise Exception(
                    "FFmpeg Windows compatibility error!\n\n"
                    "Your FFmpeg version doesn't match your Windows.\n\n"
                    "Quick fix:\n"
                    "1. Close the app\n"
                    "2. Delete the 'ffmpeg' folder\n"
                    "3. Restart the app\n\n"
                    "A compatible FFmpeg will be downloaded automatically."
                )
            else:
                raise Exception(f"FFmpeg error: {str(e)}")
        finally:
            self.ffmpeg_handler.cleanup_temp_files(video_path, audio_path)
            self.ffmpeg_handler.cleanup_default_temp_files(output_path)
    
    def download_selected_videos(self, selected_videos, success_callback=None, error_callback=None):
        """
        Download selected videos from playlist with individual quality settings
        
        Args:
            selected_videos (list): List of video dictionaries with video, quality, index, title
            success_callback (callable): Called on successful completion
            error_callback (callable): Called on error
        """
        self.stop_flag = False
        
        if not file_manager.has_download_path():
            if not file_manager.set_download_path():
                return
        
        self.total_videos_in_batch = len(selected_videos)
        
        self.current_thread = threading.Thread(
            target=self._download_selected_videos_thread,
            args=(selected_videos, success_callback, error_callback),
            daemon=True
        )
        self.current_thread.start()
    
    def _download_selected_videos_thread(self, selected_videos, success_callback, error_callback):
        """Thread function for batch download of selected videos"""
        completed_count = 0
        
        try:
            for i, video_info in enumerate(selected_videos):
                if self.stop_flag:
                    raise KeyboardInterrupt("Download cancelled")
                
                self.current_video_index = video_info['index']
                video = video_info['video']
                quality_str = video_info['quality']
                title = video_info['title']
                
                # Notify batch progress callback - starting download
                if self.batch_progress_callback:
                    self.batch_progress_callback(
                        self.current_video_index, 
                        'downloading', 
                        title,
                        i + 1,
                        self.total_videos_in_batch
                    )
                
                # Update main progress
                if self.progress_callback:
                    self.progress_callback(
                        0, 0, 0, 0, 0, 
                        f"Downloading {i+1}/{self.total_videos_in_batch}: {title[:40]}..."
                    )
                
                # Download the video
                try:
                    self.download_single_video(
                        video, 
                        quality_str, 
                        False,  # Not audio-only for now
                        file_manager.get_download_path()
                    )
                    
                    completed_count += 1
                    
                    # Notify batch progress callback - completed
                    if self.batch_progress_callback:
                        self.batch_progress_callback(
                            self.current_video_index, 
                            'completed', 
                            title,
                            i + 1,
                            self.total_videos_in_batch
                        )
                        
                except Exception as video_error:
                    # Notify batch progress callback - error
                    if self.batch_progress_callback:
                        self.batch_progress_callback(
                            self.current_video_index, 
                            'error', 
                            f"{title} - Error: {str(video_error)}",
                            i + 1,
                            self.total_videos_in_batch
                        )
                    print(f"Error downloading {title}: {video_error}")
                    # Continue with next video instead of stopping entire batch
                    continue
            
            # Final success callback
            if success_callback:
                success_callback(f"Batch download completed! {completed_count}/{self.total_videos_in_batch} videos downloaded successfully.")
        
        except KeyboardInterrupt:
            # Clean up temp files from cancelled batch download
            self.ffmpeg_handler.cleanup_default_temp_files(file_manager.get_download_path())
            if error_callback:
                error_callback("Download cancelled")
        except Exception as e:
            if error_callback:
                error_callback(str(e))
    
    def download_playlist(self, playlist_url, quality_str, is_audio, success_callback=None, error_callback=None):
        """
        Download entire playlist
        
        Args:
            playlist_url (str): Playlist URL
            quality_str (str): Quality string
            is_audio (bool): Whether to download as audio only
            success_callback (callable): Called on successful completion
            error_callback (callable): Called on error
        """
        self.stop_flag = False
        
        if not file_manager.has_download_path():
            if not file_manager.set_download_path():
                return
        
        self.current_thread = threading.Thread(
            target=self._download_playlist_thread,
            args=(playlist_url, quality_str, is_audio, success_callback, error_callback),
            daemon=True
        )
        self.current_thread.start()
    
    def download_video(self, video_url, quality_str, is_audio, success_callback=None, error_callback=None):
        """
        Download single video
        
        Args:
            video_url (str): Video URL
            quality_str (str): Quality string
            is_audio (bool): Whether to download as audio only
            success_callback (callable): Called on successful completion
            error_callback (callable): Called on error
        """
        self.stop_flag = False
        
        if not file_manager.has_download_path():
            if not file_manager.set_download_path():
                return
        
        self.current_thread = threading.Thread(
            target=self._download_video_thread,
            args=(video_url, quality_str, is_audio, success_callback, error_callback),
            daemon=True
        )
        self.current_thread.start()
    
    def _download_playlist_thread(self, playlist_url, quality_str, is_audio, success_callback, error_callback):
        """Thread function for playlist download"""
        try:
            playlist = self.youtube_handler.load_playlist(playlist_url)
            total_videos = len(playlist.videos)
            
            for i, video in enumerate(playlist.videos):
                if self.stop_flag:
                    raise KeyboardInterrupt("Download cancelled")
                
                # Update progress info
                if self.progress_callback:
                    self.progress_callback(0, 0, 0, 0, 0, f"Downloading {i+1} of {total_videos}")
                
                self.download_single_video(video, quality_str, is_audio, file_manager.get_download_path())
            
            if success_callback:
                success_callback("Playlist download completed!")
        
        except KeyboardInterrupt:
            # Clean up temp files from cancelled playlist download
            self.ffmpeg_handler.cleanup_default_temp_files(file_manager.get_download_path())
            if error_callback:
                error_callback("Download cancelled")
        except Exception as e:
            if error_callback:
                error_callback(str(e))
    
    def _download_video_thread(self, video_url, quality_str, is_audio, success_callback, error_callback):
        """Thread function for single video download with enhanced error handling"""
        try:
            # Use cached video if available to speed up download start
            if self.cached_video and self.cached_video_url == video_url:
                video = self.cached_video
                print("⚡ Using cached video data for instant download")
            else:
                video = self.youtube_handler.load_video(video_url)
            
            self.download_single_video(video, quality_str, is_audio, file_manager.get_download_path())
            
            if success_callback:
                success_callback("Download completed!")
                
        except KeyboardInterrupt:
            # User cancelled the download - clean up all temp files
            self.ffmpeg_handler.cleanup_default_temp_files(file_manager.get_download_path())
            if error_callback:
                error_callback("Download cancelled")
            return
        except Exception as e:
            error_message = str(e)

            if self.stop_flag or "cancelled" in error_message.lower():
                if error_callback:
                    error_callback("Download cancelled")
                return
            
            # Handle specific HTTP 403 Forbidden error with retry
            if "403" in error_message or "Forbidden" in error_message:
                print("🔄 Detected 403 error, attempting download-optimized retry...")
                try:
                    # Try with download-optimized client strategies
                    video = self.youtube_handler.load_video_with_download_retry(video_url)
                    self.download_single_video(video, quality_str, is_audio, file_manager.get_download_path())
                    
                    if success_callback:
                        success_callback("Download completed!")
                    return
                
                except KeyboardInterrupt:
                    # User cancelled during retry - clean up
                    self.ffmpeg_handler.cleanup_default_temp_files(file_manager.get_download_path())
                    if error_callback:
                        error_callback("Download cancelled")
                    return
                    
                except Exception as retry_error:
                    print(f"❌ Download retry also failed: {retry_error}")
                    print("🛡️ Falling back to yt-dlp (robust mode)...")
                    try:
                        from utils.ytdlp_handler import YtDlpHandler
                        ffmpeg_path = self.ffmpeg_handler.get_ffmpeg_path()
                        ok = YtDlpHandler.download_video(
                            video_url,
                            file_manager.get_download_path(),
                            quality_str,
                            is_audio,
                            self.progress_callback,
                            ffmpeg_path,
                            cancel_callback=lambda: self.stop_flag
                        )
                        if ok:
                            if success_callback:
                                success_callback("Download completed!")
                            return
                        else:
                            raise Exception("yt-dlp fallback failed")
                    except KeyboardInterrupt:
                        # User cancelled during yt-dlp fallback - clean up
                        self.ffmpeg_handler.cleanup_default_temp_files(file_manager.get_download_path())
                        if error_callback:
                            error_callback("Download cancelled")
                        return
                    except Exception as yerr:
                        print(f"❌ yt-dlp fallback failed: {yerr}")
                        enhanced_error = (
                            "🚫 YouTube Access Blocked (HTTP 403: Forbidden)\n\n"
                            "We tried: standard clients, download-optimized clients, and yt-dlp fallback,\n"
                            "but all methods were blocked or failed.\n\n"
                            "💡 Try:\n"
                            "• Wait 5-10 minutes and try again\n"
                            "• Use a VPN or different network\n"
                            "• Try a different video (private/region-restricted videos may fail)\n"
                            "• Update and relaunch the app\n"
                        )
                        if error_callback:
                            error_callback(enhanced_error)
                        return
            
            # Handle other common YouTube errors
            elif "throttling" in error_message.lower():
                enhanced_error = (
                    "🐌 YouTube Throttling Detected\n\n"
                    "YouTube is slowing down download requests.\n\n"
                    "💡 Solutions:\n"
                    "1. Wait 15-30 minutes before trying again\n"
                    "2. Try a different video\n"
                    "3. Use a VPN if available\n"
                    "4. Check for pytubefix updates\n\n"
                    "This is temporary - try again later."
                )
                if error_callback:
                    error_callback(enhanced_error)
            elif "private" in error_message.lower() or "unavailable" in error_message.lower():
                enhanced_error = (
                    "🔒 Video Access Restricted\n\n"
                    "This video is private, deleted, or not available.\n\n"
                    "Possible reasons:\n"
                    "• Video is set to private\n"
                    "• Video has been deleted\n"
                    "• Video is region-restricted\n"
                    "• Video requires sign-in to view\n\n"
                    "Try a different video that is publicly accessible."
                )
                if error_callback:
                    error_callback(enhanced_error)
            else:
                # Generic error with original message
                if error_callback:
                    error_callback(f"Download failed: {error_message}")
                    
        except KeyboardInterrupt:
            if error_callback:
                error_callback("Download cancelled by user")