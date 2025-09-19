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


class DownloadManager:
    """Manages download operations and progress tracking"""
    
    def __init__(self):
        self.youtube_handler = YouTubeHandler()
        self.ffmpeg_handler = FFmpegHandler()
        self.stop_flag = False
        self.current_thread = None
        
        # Progress tracking
        self.last_time = 0
        self.last_bytes = 0
        self.current_download_size = 0
        self.progress_callback = None
        
        # Batch download tracking
        self.batch_progress_callback = None
        self.current_video_index = -1
        self.total_videos_in_batch = 0
    
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
            raise Exception("Download cancelled")
        
        current_time = time.time()
        bytes_downloaded = self.current_download_size - bytes_remaining
        percentage = (bytes_downloaded / self.current_download_size) * 100
        
        # Calculate download speed
        delta_time = current_time - self.last_time
        delta_bytes = bytes_downloaded - self.last_bytes
        
        if delta_time > 0:
            speed = delta_bytes / delta_time  # bytes per second
            speed_mbps = speed / (1024 * 1024)  # MB per second
        else:
            speed_mbps = 0
        
        elapsed = int(current_time - self.last_time)
        
        # Call progress callback if set
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
    
    def download_single_video(self, video, quality_str, is_audio, output_path):
        """
        Download a single video
        
        Args:
            video (YouTube): YouTube video object
            quality_str (str): Quality string (e.g., "1080p - Progressive")
            is_audio (bool): Whether to download as audio only
            output_path (str): Output directory path
        """
        resolution, stream_type = parse_quality_string(quality_str)
        
        if is_audio:
            self._download_audio(video, output_path)
        else:
            if "Progressive" in stream_type:
                self._download_progressive(video, resolution, output_path)
            else:
                self._download_adaptive(video, resolution, output_path)
    
    def _download_audio(self, video, output_path):
        """Download audio only as MP3"""
        audio_stream = self.youtube_handler.get_audio_only_stream(video)
        if not audio_stream:
            raise Exception("No audio stream available")
        
        self.current_download_size = audio_stream.filesize
        video.register_on_progress_callback(self.progress_tracker)
        
        # Download audio directly as mp3
        output_filename = f"{safe_filename(video.title)}.mp3"
        full_output_path = os.path.join(output_path, output_filename)
        
        audio_stream.download(output_path=output_path, filename=output_filename)
    
    def _download_progressive(self, video, resolution, output_path):
        """Download progressive stream (no FFmpeg needed)"""
        prog_stream = self.youtube_handler.get_stream_by_quality(
            video, resolution, "Progressive"
        )
        
        if not prog_stream:
            raise Exception(f"No progressive stream available for {resolution}")
        
        self.current_download_size = prog_stream.filesize
        video.register_on_progress_callback(self.progress_tracker)
        
        # Download directly
        output_filename = f"{safe_filename(video.title)}.mp4"
        prog_stream.download(output_path=output_path, filename=output_filename)
    
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
        self.current_download_size = video_stream.filesize
        video.register_on_progress_callback(self.progress_tracker)
        video_path = video_stream.download(output_path=output_path, filename="video_temp.mp4")
        
        # Check if cancelled during download
        if self.stop_flag:
            self.ffmpeg_handler.cleanup_temp_files(video_path)
            raise Exception("Download cancelled")
        
        # Download audio
        self.current_download_size = audio_stream.filesize
        video.register_on_progress_callback(self.progress_tracker)
        audio_path = audio_stream.download(output_path=output_path, filename="audio_temp.mp4")
        
        # Check if cancelled during download
        if self.stop_flag:
            self.ffmpeg_handler.cleanup_temp_files(video_path, audio_path)
            raise Exception("Download cancelled")
        
        # Merge with FFmpeg
        output_filename = f"{safe_filename(video.title)}.mp4"
        final_output_path = os.path.join(output_path, output_filename)
        
        try:
            self.ffmpeg_handler.merge_video_audio(video_path, audio_path, final_output_path)
        finally:
            # Clean up temporary files
            self.ffmpeg_handler.cleanup_temp_files(video_path, audio_path)
    
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
                    raise Exception("Download cancelled")
                
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
                
        except Exception as e:
            if error_callback:
                error_callback(str(e))
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
                    raise Exception("Download cancelled")
                
                # Update progress info
                if self.progress_callback:
                    self.progress_callback(0, 0, 0, 0, 0, f"Downloading {i+1} of {total_videos}")
                
                self.download_single_video(video, quality_str, is_audio, file_manager.get_download_path())
            
            if success_callback:
                success_callback("Playlist download completed!")
                
        except Exception as e:
            if error_callback:
                error_callback(str(e))
    
    def _download_video_thread(self, video_url, quality_str, is_audio, success_callback, error_callback):
        """Thread function for single video download"""
        try:
            video = self.youtube_handler.load_video(video_url)
            self.download_single_video(video, quality_str, is_audio, file_manager.get_download_path())
            
            if success_callback:
                success_callback("Download completed!")
                
        except Exception as e:
            if error_callback:
                error_callback(str(e))