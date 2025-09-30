"""
FFmpeg handling utilities for video/audio processing with auto-detection and download
"""

import subprocess
import os
import platform
import zipfile
import requests
from pathlib import Path
from config.settings import (
    FFMPEG_VIDEO_CODEC, FFMPEG_AUDIO_CODEC, 
    FFMPEG_STRICT_EXPERIMENTAL, MERGE_TIMEOUT
)


class FFmpegHandler:
    """Handles FFmpeg operations for video and audio merging with smart setup"""
    
    @staticmethod
    def detect_system_architecture():
        """
        Detect the system architecture and Windows version
        
        Returns:
            tuple: (architecture, windows_version)
        """
        arch = platform.machine().lower()
        system = platform.system()
        version = platform.version()
        
        print(f"🔍 System Info: {system} {version}")
        print(f"🔍 Architecture: {arch}")
        
        # Determine if 32-bit or 64-bit
        is_64bit = arch in ['amd64', 'x86_64', 'arm64']
        
        return ('x64' if is_64bit else 'x86', system)
    
    @staticmethod
    def download_compatible_ffmpeg():
        """
        Download and setup FFmpeg compatible with the current system
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            arch, system = FFmpegHandler.detect_system_architecture()
            
            if system != "Windows":
                print("❌ Auto-download only supports Windows. Please install FFmpeg manually.")
                return False
            
            print(f"📥 Downloading FFmpeg for Windows {arch}...")
            
            # FFmpeg download URLs for different architectures
            download_urls = {
                'x64': 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip',
                'x86': 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win32-gpl.zip'
            }
            
            if arch not in download_urls:
                print(f"❌ No compatible FFmpeg found for architecture: {arch}")
                return False
            
            url = download_urls[arch]
            
            # Create ffmpeg directory
            project_root = Path(__file__).parent.parent
            ffmpeg_dir = project_root / "ffmpeg"
            ffmpeg_dir.mkdir(exist_ok=True)
            
            # Download FFmpeg
            print("📥 Downloading FFmpeg...")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            zip_path = ffmpeg_dir / "ffmpeg.zip"
            
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print("📦 Extracting FFmpeg...")
            
            # Extract FFmpeg
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Find ffmpeg.exe in the archive
                for file_info in zip_ref.filelist:
                    if file_info.filename.endswith('ffmpeg.exe'):
                        # Extract only ffmpeg.exe to the ffmpeg directory
                        file_info.filename = 'ffmpeg.exe'
                        zip_ref.extract(file_info, ffmpeg_dir)
                        break
            
            # Clean up zip file
            zip_path.unlink(missing_ok=True)
            
            # Verify installation
            ffmpeg_exe = ffmpeg_dir / "ffmpeg.exe"
            if ffmpeg_exe.exists():
                print("✅ FFmpeg downloaded and installed successfully!")
                return True
            else:
                print("❌ FFmpeg extraction failed")
                return False
                
        except Exception as e:
            print(f"❌ Failed to download FFmpeg: {e}")
            return False
    
    @staticmethod
    def get_ffmpeg_path():
        """
        Get the path to FFmpeg executable with auto-setup
        
        Returns:
            str: Path to FFmpeg executable (local first, then system PATH)
        """
        # First, try the local FFmpeg installation
        project_root = Path(__file__).parent.parent
        local_ffmpeg = project_root / "ffmpeg" / "ffmpeg.exe"
        
        if local_ffmpeg.exists():
            # Test if the local FFmpeg is compatible
            try:
                subprocess.run([str(local_ffmpeg), '-version'], 
                             capture_output=True, check=True, timeout=5)
                return str(local_ffmpeg)
            except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError) as e:
                print(f"⚠️ Local FFmpeg incompatible: {e}")
                print("🔄 Attempting to download compatible version...")
                
                # Remove incompatible version
                try:
                    local_ffmpeg.unlink()
                except:
                    pass
                
                # Download compatible version
                if FFmpegHandler.download_compatible_ffmpeg():
                    if local_ffmpeg.exists():
                        return str(local_ffmpeg)
        else:
            # No local FFmpeg, try to download it
            print("📥 FFmpeg not found, downloading compatible version...")
            if FFmpegHandler.download_compatible_ffmpeg():
                if local_ffmpeg.exists():
                    return str(local_ffmpeg)
        
        # Fallback to system PATH
        return "ffmpeg"
    
    @staticmethod
    def is_available():
        """
        Check if FFmpeg is available with auto-setup if needed
        
        Returns:
            bool: True if FFmpeg is available, False otherwise
        """
        # First, try the local FFmpeg installation
        project_root = Path(__file__).parent.parent
        local_ffmpeg = project_root / "ffmpeg" / "ffmpeg.exe"
        
        if local_ffmpeg.exists():
            try:
                result = subprocess.run([str(local_ffmpeg), '-version'], 
                             capture_output=True, check=True, timeout=5)
                print("✅ Local FFmpeg is working!")
                return True
            except Exception as e:
                print(f"⚠️ Local FFmpeg test failed: {e}")
                # Only remove if it's actually broken
                if "WinError 216" in str(e) or "not compatible" in str(e):
                    print("🗑️ Removing incompatible FFmpeg...")
                    try:
                        local_ffmpeg.unlink()
                    except:
                        pass
                else:
                    # Don't remove if it's just a timeout or other temporary issue
                    print("� Temporary FFmpeg issue, keeping file")
                    return False
        
        # Try system FFmpeg
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                         capture_output=True, check=True, timeout=5)
            print("✅ System FFmpeg is working!")
            return True
        except:
            print("❌ No system FFmpeg found")
        
        # Only download if no working FFmpeg found
        print("📥 No working FFmpeg found, downloading...")
        if FFmpegHandler.download_compatible_ffmpeg():
            if local_ffmpeg.exists():
                try:
                    subprocess.run([str(local_ffmpeg), '-version'], 
                                 capture_output=True, check=True, timeout=5)
                    print("✅ Downloaded FFmpeg is working!")
                    return True
                except:
                    print("❌ Downloaded FFmpeg also failed")
        
        return False
    
    @staticmethod
    def merge_video_audio(video_path, audio_path, output_path, progress_callback=None):
        """
        Merge video and audio files using FFmpeg with progress tracking
        
        Args:
            video_path (str): Path to video file
            audio_path (str): Path to audio file
            output_path (str): Path for output file
            progress_callback (callable): Optional callback for progress updates
                                        Signature: callback(percentage, stage)
            
        Raises:
            FileNotFoundError: If FFmpeg is not installed
            subprocess.CalledProcessError: If FFmpeg fails
            subprocess.TimeoutExpired: If FFmpeg takes too long
        """
        ffmpeg_path = FFmpegHandler.get_ffmpeg_path()
        
        if progress_callback:
            progress_callback(0, "Starting FFmpeg merge...")
        
        try:
            if progress_callback:
                # Use Popen for real-time progress tracking
                process = subprocess.Popen([
                    ffmpeg_path, '-i', video_path, '-i', audio_path, 
                    '-c:v', FFMPEG_VIDEO_CODEC, 
                    '-c:a', FFMPEG_AUDIO_CODEC, 
                    '-strict', FFMPEG_STRICT_EXPERIMENTAL, 
                    '-progress', 'pipe:1',  # Output progress to stdout
                    '-y',  # Overwrite output file if it exists
                    output_path
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                text=True, encoding='utf-8', errors='ignore')
                
                # Track progress from FFmpeg output
                FFmpegHandler._track_merge_progress(process, progress_callback)
                
            else:
                # Use the original simple method without progress tracking
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
            
        if progress_callback:
            progress_callback(100, "FFmpeg merge completed!")
    
    @staticmethod
    def _track_merge_progress(process, progress_callback):
        """Track FFmpeg merge progress from stdout"""
        duration = None
        current_time = 0
        
        try:
            progress_callback(10, "Analyzing video...")
            
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                    
                line = line.strip()
                
                # Parse duration from FFmpeg output
                if 'Duration:' in line and duration is None:
                    try:
                        # Extract duration in format "Duration: 00:03:45.67"
                        import re
                        duration_match = re.search(r'Duration: (\d+):(\d+):(\d+)', line)
                        if duration_match:
                            hours, minutes, seconds = map(int, duration_match.groups())
                            duration = hours * 3600 + minutes * 60 + seconds
                            progress_callback(20, f"Video duration: {duration}s")
                    except:
                        pass
                
                # Parse current time from progress output
                if line.startswith('out_time_us='):
                    try:
                        microseconds = int(line.split('=')[1])
                        current_time = microseconds / 1000000  # Convert to seconds
                        
                        if duration and duration > 0:
                            percentage = min(90, 20 + (current_time / duration) * 70)  # 20-90% range
                            progress_callback(int(percentage), f"Merging... {int(current_time)}s/{duration}s")
                        else:
                            # Fallback progress without duration
                            progress_callback(50, f"Merging... {int(current_time)}s")
                    except:
                        pass
            
            # Wait for process to complete
            process.wait()
            
            if process.returncode != 0:
                stderr_output = process.stderr.read()
                raise subprocess.CalledProcessError(
                    process.returncode, process.args, 
                    f"FFmpeg failed: {stderr_output}"
                )
                
        except Exception as e:
            process.terminate()
            raise e
    
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