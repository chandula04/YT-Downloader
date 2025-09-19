"""
FFmpeg handling utilities for video/audio processing
"""

import subprocess
import os
from pathlib import Path
from config.settings import (
    FFMPEG_VIDEO_CODEC, FFMPEG_AUDIO_CODEC, 
    FFMPEG_STRICT_EXPERIMENTAL, MERGE_TIMEOUT
)


class FFmpegHandler:
    """Handles FFmpeg operations for video and audio merging"""
    
    @staticmethod
    def get_ffmpeg_path():
        """
        Get the path to FFmpeg executable
        
        Returns:
            str: Path to FFmpeg executable (local first, then system PATH)
        """
        # First, try the local FFmpeg installation
        project_root = Path(__file__).parent.parent
        local_ffmpeg = project_root / "ffmpeg" / "ffmpeg.exe"
        
        if local_ffmpeg.exists():
            return str(local_ffmpeg)
        
        # Fallback to system PATH
        return "ffmpeg"
    
    @staticmethod
    def is_available():
        """
        Check if FFmpeg is available (local or system PATH)
        
        Returns:
            bool: True if FFmpeg is available, False otherwise
        """
        ffmpeg_path = FFmpegHandler.get_ffmpeg_path()
        try:
            subprocess.run([ffmpeg_path, '-version'], 
                         capture_output=True, check=True, timeout=5)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
            return False
    
    @staticmethod
    def merge_video_audio(video_path, audio_path, output_path):
        """
        Merge video and audio files using FFmpeg
        
        Args:
            video_path (str): Path to video file
            audio_path (str): Path to audio file
            output_path (str): Path for output file
            
        Raises:
            FileNotFoundError: If FFmpeg is not installed
            subprocess.CalledProcessError: If FFmpeg fails
            subprocess.TimeoutExpired: If FFmpeg takes too long
        """
        ffmpeg_path = FFmpegHandler.get_ffmpeg_path()
        
        try:
            # Use FFmpeg to merge video and audio with proper encoding handling
            result = subprocess.run([
                ffmpeg_path, '-i', video_path, '-i', audio_path, 
                '-c:v', FFMPEG_VIDEO_CODEC, 
                '-c:a', FFMPEG_AUDIO_CODEC, 
                '-strict', FFMPEG_STRICT_EXPERIMENTAL, 
                '-y',  # Overwrite output file if it exists
                output_path
            ], check=True, capture_output=True, timeout=MERGE_TIMEOUT, 
            # Set encoding to ignore errors to prevent UnicodeDecodeError
            text=True, encoding='utf-8', errors='ignore')
            
        except FileNotFoundError:
            raise FileNotFoundError("FFmpeg is not installed or not in PATH")
        except subprocess.CalledProcessError as e:
            # Extract error message safely
            error_msg = e.stderr if isinstance(e.stderr, str) else str(e)
            raise subprocess.CalledProcessError(
                e.returncode, e.cmd, 
                f"FFmpeg failed to merge the files: {error_msg}"
            )
        except subprocess.TimeoutExpired:
            raise subprocess.TimeoutExpired(
                ffmpeg_path, MERGE_TIMEOUT, 
                "FFmpeg took too long to process the video"
            )
    
    @staticmethod
    def cleanup_temp_files(*file_paths):
        """
        Clean up temporary files
        
        Args:
            *file_paths: Variable number of file paths to delete
        """
        for file_path in file_paths:
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except OSError:
                    pass  # Ignore errors when cleaning up