"""
FFmpeg handling utilities for video/audio processing with auto-detection and download
"""

import subprocess
import os
import platform
import zipfile
import requests
import json
import shutil
from pathlib import Path
from config.settings import (
    FFMPEG_VIDEO_CODEC, FFMPEG_AUDIO_CODEC,
    FFMPEG_STRICT_EXPERIMENTAL, MERGE_TIMEOUT,
    FFMPEG_VIDEO_PRESET, FFMPEG_PIXEL_FORMAT, FFMPEG_MOVFLAGS,
    FFMPEG_TV_MAX_WIDTH, FFMPEG_TV_MAX_HEIGHT, FFMPEG_TV_CRF,
    FFMPEG_TV_VIDEO_PROFILE, FFMPEG_TV_VIDEO_LEVEL,
    FFMPEG_TV_AUDIO_BITRATE, FFMPEG_TV_AUDIO_CHANNELS,
    FFMPEG_TV_AUDIO_SAMPLERATE, FFMPEG_TV_VSYNC_MODE
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
            
            # Extract FFmpeg (ffmpeg.exe + required DLLs from bin directory)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                members = [f.filename for f in zip_ref.filelist]
                # Try to find ffmpeg.exe location (usually in .../bin/ffmpeg.exe)
                exe_member = None
                for name in members:
                    low = name.lower().replace('\\', '/')
                    if low.endswith('/bin/ffmpeg.exe') or low.endswith('ffmpeg.exe'):
                        exe_member = name
                        break
                if not exe_member:
                    print("❌ Could not locate ffmpeg.exe inside archive")
                    return False
                # Determine bin directory prefix
                norm = exe_member.replace('\\', '/')
                bin_prefix = norm.rsplit('/', 1)[0]  # path to .../bin
                # Ensure ends with '/'
                if not bin_prefix.endswith('/'):
                    bin_prefix = bin_prefix + '/'
                extracted_any = False
                for file in zip_ref.filelist:
                    name = file.filename.replace('\\', '/')
                    if name.startswith(bin_prefix) and not name.endswith('/'):
                        # Extract file into ffmpeg_dir using only the basename
                        target_path = ffmpeg_dir / Path(name).name
                        with zip_ref.open(file) as src, open(target_path, 'wb') as dst:
                            dst.write(src.read())
                            extracted_any = True
                if not extracted_any:
                    print("❌ Failed to extract FFmpeg bin files")
                    return False
            
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
        
        print(f"🔍 Checking local FFmpeg: {local_ffmpeg}")
        
        if local_ffmpeg.exists():
            print("✅ Local FFmpeg file exists")
            # Test if the local FFmpeg is compatible
            try:
                result = subprocess.run([str(local_ffmpeg), '-version'], 
                             capture_output=True, check=True, timeout=5,
                             creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
                print("✅ Local FFmpeg compatibility test passed")
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
                        print("✅ Downloaded compatible FFmpeg")
                        return str(local_ffmpeg)
        else:
            print("❌ Local FFmpeg not found")
            # No local FFmpeg, try to download it
            print("📥 FFmpeg not found, downloading compatible version...")
            if FFmpegHandler.download_compatible_ffmpeg():
                if local_ffmpeg.exists():
                    print("✅ Successfully downloaded FFmpeg")
                    return str(local_ffmpeg)
        
        print("⚠️ Falling back to system PATH")
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
                             capture_output=True, check=True, timeout=5,
                             creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
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
                         capture_output=True, check=True, timeout=5,
                         creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
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
                                 capture_output=True, check=True, timeout=5,
                                 creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
                    print("✅ Downloaded FFmpeg is working!")
                    return True
                except:
                    print("❌ Downloaded FFmpeg also failed")
        
        return False
    
    @staticmethod
    def merge_video_audio(video_path, audio_path, output_path, progress_callback=None, tv_optimized=True):
        """
        Merge video and audio files using FFmpeg with progress tracking
        
        Args:
            video_path (str): Path to video file
            audio_path (str): Path to audio file
            output_path (str): Path for output file
            progress_callback (callable): Optional callback for progress updates
                                        Signature: callback(percentage, stage)
            tv_optimized (bool): Whether to re-encode for TV compatibility
            
        Raises:
            FileNotFoundError: If FFmpeg is not installed
            subprocess.CalledProcessError: If FFmpeg fails
            subprocess.TimeoutExpired: If FFmpeg takes too long
        """
        ffmpeg_path = FFmpegHandler.get_ffmpeg_path()
        ffprobe_path = FFmpegHandler._get_ffprobe_path(ffmpeg_path)
        stream_info = FFmpegHandler._probe_video_stream(video_path, ffprobe_path)
        requested_tv_mode = bool(tv_optimized)
        auto_tv_required = not FFmpegHandler._is_stream_tv_ready(stream_info)
        force_tv_profile = requested_tv_mode or auto_tv_required
        attempt = 0
        last_error = None
        
        while True:
            attempt += 1
            cmd = FFmpegHandler._build_merge_command(
                ffmpeg_path,
                video_path,
                audio_path,
                output_path,
                force_tv_profile
            )
            stage_label = "TV optimized merge" if force_tv_profile else "Direct merge"
            try:
                FFmpegHandler._run_ffmpeg_command(cmd, progress_callback, stage_label)
            except FileNotFoundError:
                raise FileNotFoundError("FFmpeg is not installed or not in PATH")
            except subprocess.TimeoutExpired as timeout_error:
                raise timeout_error
            except subprocess.CalledProcessError as called_error:
                raise subprocess.CalledProcessError(
                    called_error.returncode,
                    called_error.cmd,
                    f"FFmpeg failed to merge the files: {called_error.stderr or called_error.output}"
                )
            
            # Validate codec if ffprobe is available
            stream_after = FFmpegHandler._probe_video_stream(output_path, ffprobe_path)
            codec_after = (stream_after.get('codec_name') or '').lower() if stream_after else ''
            if not stream_after or codec_after == 'h264':
                break  # success
            
            last_error = codec_after or 'unknown'
            if force_tv_profile:
                raise Exception(
                    "FFmpeg completed but output codec is still not H.264 (detected: "
                    f"{last_error}). Please delete the 'ffmpeg' folder and rerun setup."
                )
            # Retry with TV profile enabled
            force_tv_profile = True
            FFmpegHandler._safe_delete(Path(output_path))
            if progress_callback:
                progress_callback(0, "Retrying merge with TV profile...")
            if attempt >= 2:
                raise Exception(
                    "Unable to force H.264 output after retry."
                )
        
        if progress_callback:
            progress_callback(100, "FFmpeg merge completed!")

    @staticmethod
    def _build_merge_command(ffmpeg_path, video_path, audio_path, output_path, tv_profile_enabled):
        """Build FFmpeg command respecting optimization preferences."""
        cmd = [
            ffmpeg_path,
            '-hide_banner',
            '-i', video_path,
            '-i', audio_path,
            '-map', '0:v:0',
            '-map', '1:a:0'
        ]
        if tv_profile_enabled:
            cmd.extend(['-c:v', FFMPEG_VIDEO_CODEC])
            cmd.extend(['-tag:v', 'avc1'])
            if FFMPEG_TV_CRF is not None:
                cmd.extend(['-crf', str(FFMPEG_TV_CRF)])
            if FFMPEG_VIDEO_PRESET:
                cmd.extend(['-preset', FFMPEG_VIDEO_PRESET])
            if FFMPEG_TV_VIDEO_PROFILE:
                cmd.extend(['-profile:v', FFMPEG_TV_VIDEO_PROFILE])
            if FFMPEG_TV_VIDEO_LEVEL:
                cmd.extend(['-level:v', FFMPEG_TV_VIDEO_LEVEL])
            if FFMPEG_PIXEL_FORMAT:
                cmd.extend(['-pix_fmt', FFMPEG_PIXEL_FORMAT])

            filters = []
            max_height = int(FFMPEG_TV_MAX_HEIGHT) if FFMPEG_TV_MAX_HEIGHT else None
            max_width = int(FFMPEG_TV_MAX_WIDTH) if FFMPEG_TV_MAX_WIDTH else None
            if max_width and max_height:
                filters.append(
                    f"scale='if(gt(iw,{max_width})||gt(ih,{max_height}),{max_width},iw)':'if(gt(iw,{max_width})||gt(ih,{max_height}),{max_height},ih)':force_original_aspect_ratio=decrease"
                )
            elif max_height:
                filters.append(
                    f"scale='if(gt(ih,{max_height}),-2,iw)':'if(gt(ih,{max_height}),{max_height},ih)'"
                )
            elif max_width:
                filters.append(
                    f"scale='if(gt(iw,{max_width}),{max_width},iw)':'if(gt(iw,{max_width}),-2,ih)'"
                )
            if filters:
                filters.append('setsar=1')
                cmd.extend(['-vf', ','.join(filters)])

            cmd.extend(['-c:a', FFMPEG_AUDIO_CODEC])
            if FFMPEG_TV_AUDIO_BITRATE:
                cmd.extend(['-b:a', FFMPEG_TV_AUDIO_BITRATE])
            if FFMPEG_TV_AUDIO_CHANNELS:
                cmd.extend(['-ac', str(FFMPEG_TV_AUDIO_CHANNELS)])
            if FFMPEG_TV_AUDIO_SAMPLERATE:
                cmd.extend(['-ar', str(FFMPEG_TV_AUDIO_SAMPLERATE)])
            if FFMPEG_STRICT_EXPERIMENTAL:
                cmd.extend(['-strict', FFMPEG_STRICT_EXPERIMENTAL])
            if FFMPEG_TV_VSYNC_MODE:
                cmd.extend(['-vsync', FFMPEG_TV_VSYNC_MODE])
        else:
            cmd.extend(['-c:v', 'copy', '-c:a', 'copy'])

        if FFMPEG_MOVFLAGS:
            cmd.extend(['-movflags', FFMPEG_MOVFLAGS])
        cmd.extend(['-y', output_path])
        return cmd
    
    @staticmethod
    def cleanup_temp_files(*file_paths):
        """
        Clean up temporary files
        
        Args:
            *file_paths: Variable number of file paths to delete
        """
        for file_path in file_paths:
            if not file_path:
                continue
            try:
                path_obj = Path(file_path)
                if path_obj.exists():
                    path_obj.unlink()
            except PermissionError:
                try:
                    os.remove(file_path)
                except OSError:
                    pass

    @staticmethod
    def cleanup_default_temp_files(directory):
        """Remove default temp files (video_temp/audio_temp) inside directory."""
        if not directory:
            return
        dir_path = Path(directory)
        if not dir_path.exists():
            return
        for pattern in ("video_temp*", "audio_temp*"):
            for temp_file in dir_path.glob(pattern):
                try:
                    if temp_file.is_file():
                        temp_file.unlink()
                except OSError:
                    pass

    @staticmethod
    def _run_ffmpeg_command(cmd, progress_callback, stage_label):
        """Run FFmpeg command with consistent progress handling."""
        try:
            if progress_callback:
                progress_callback(0, f"Starting {stage_label}...")
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding='utf-8',
                    errors='ignore',
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )
                progress_callback(25, f"Processing streams ({stage_label})...")
                stdout, stderr = process.communicate(timeout=MERGE_TIMEOUT)
                progress_callback(75, f"Finalizing ({stage_label})...")
                if process.returncode != 0:
                    raise subprocess.CalledProcessError(process.returncode, cmd, stderr)
            else:
                subprocess.run(
                    cmd,
                    check=True,
                    capture_output=True,
                    timeout=MERGE_TIMEOUT,
                    text=True,
                    encoding='utf-8',
                    errors='ignore',
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )
        except subprocess.TimeoutExpired:
            raise subprocess.TimeoutExpired(cmd[0], MERGE_TIMEOUT, "FFmpeg took too long to process the video")

    @staticmethod
    def _safe_delete(path_obj):
        try:
            if path_obj and path_obj.exists():
                path_obj.unlink()
        except OSError:
            pass

    @staticmethod
    def _get_ffprobe_path(ffmpeg_path):
        """Return matching ffprobe binary path."""
        try:
            ffmpeg_path_obj = Path(ffmpeg_path)
            if ffmpeg_path_obj.exists():
                candidate = ffmpeg_path_obj.with_name(
                    'ffprobe.exe' if ffmpeg_path_obj.suffix.lower() == '.exe' else 'ffprobe'
                )
                if candidate.exists():
                    return str(candidate)
        except Exception:
            pass
        which = shutil.which('ffprobe')
        return which or 'ffprobe'

    @staticmethod
    def _probe_video_stream(file_path, ffprobe_path):
        """Probe video stream metadata using ffprobe."""
        if not file_path or not os.path.exists(file_path):
            return {}
        cmd = [
            ffprobe_path,
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=codec_name,pix_fmt,width,height',
            '-of', 'json',
            file_path
        ]
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            data = json.loads(result.stdout or '{}')
            streams = data.get('streams') or []
            return streams[0] if streams else {}
        except Exception:
            return {}

    @staticmethod
    def _is_stream_tv_ready(stream_info):
        """Determine if a video stream is already TV friendly."""
        if not stream_info:
            return False
        codec = (stream_info.get('codec_name') or '').lower()
        pix_fmt = (stream_info.get('pix_fmt') or '').lower()
        width = stream_info.get('width')
        height = stream_info.get('height')
        if codec != 'h264':
            return False
        if pix_fmt and pix_fmt != 'yuv420p':
            return False
        if FFMPEG_TV_MAX_WIDTH and width and width > FFMPEG_TV_MAX_WIDTH:
            return False
        if FFMPEG_TV_MAX_HEIGHT and height and height > FFMPEG_TV_MAX_HEIGHT:
            return False
        return True
