"""
yt-dlp fallback downloader for robust handling of HTTP 403 and other YouTube restrictions.
"""

import os
from pathlib import Path
from config.settings import DEFAULT_HEADERS, MAX_RETRIES


class YtDlpHandler:
    """Wrapper around yt-dlp with progress hook mapped to app's progress callback."""

    @staticmethod
    def _build_format_for_height(height: int, is_audio: bool) -> str:
        if is_audio:
            return "bestaudio/best"
        if height and height > 0:
            # Prefer mp4 video + m4a audio within height cap, fall back sensibly
            return (
                f"bv*[ext=mp4][height<={height}]+ba[ext=m4a]/"
                f"b[ext=mp4][height<={height}]/"
                f"bestvideo*+bestaudio/best"
            )
        # Default best if no height
        return "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best"

    @staticmethod
    def _parse_height(quality_str: str) -> int:
        try:
            # Expect formats like "1080p - Adaptive (...)" or "720p"
            head = quality_str.split(' ')[0]
            if head.lower().endswith('p'):
                return int(head[:-1])
        except Exception:
            pass
        return 0

    @staticmethod
    def download_video(url: str, output_dir: str, quality_str: str, is_audio: bool, progress_callback=None, ffmpeg_path=None, cancel_callback=None) -> bool:
        """
        Download a single video using yt-dlp with progress mapping.

        Args:
            url: Video URL
            output_dir: Output directory
            quality_str: Requested quality string
            is_audio: Audio-only flag
            progress_callback: Optional callback(downloaded, total, pct, speedMBps, elapsed, text)
            ffmpeg_path: Optional full path to ffmpeg executable to aid merging

        Returns:
            True on success, False on failure
        """
        try:
            from yt_dlp import YoutubeDL
        except Exception as e:
            print(f"yt-dlp not available: {e}")
            return False

        height = YtDlpHandler._parse_height(quality_str)
        fmt = YtDlpHandler._build_format_for_height(height, is_audio)

        # Ensure output directory exists
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        import time
        start_time = time.time()

        def hook(d):
            if not progress_callback:
                return
            try:
                if cancel_callback and cancel_callback():
                    raise KeyboardInterrupt("Download cancelled by user")
                if d.get('status') == 'downloading':
                    downloaded = int(d.get('downloaded_bytes', 0) or 0)
                    total = int(d.get('total_bytes', d.get('total_bytes_estimate', 0)) or 0)
                    
                    # Calculate percentage from bytes (more reliable than parsing formatted string)
                    if total > 0:
                        pct = (downloaded / total) * 100.0
                    else:
                        # Fallback: try to parse _percent_str, stripping ANSI color codes
                        pct_str = d.get('_percent_str', '0').strip()
                        # Remove ANSI escape sequences (color codes like \x1b[0;94m)
                        import re
                        pct_str = re.sub(r'\x1b\[[0-9;]+m', '', pct_str)
                        pct_str = pct_str.replace('%', '').strip()
                        pct = float(pct_str) if pct_str else 0.0
                    
                    speed = d.get('speed', 0.0) or 0.0  # bytes/sec
                    speed_mbps = float(speed) / (1024 * 1024) if speed else 0.0
                    elapsed = int(time.time() - start_time)
                    # Call progress callback
                    progress_callback(downloaded, total, pct, speed_mbps, elapsed, None)
                elif d.get('status') == 'finished':
                    # Indicate merging stage
                    progress_callback(0, 0, 95, 0, 0, "Processing with FFmpeg...")
            except KeyboardInterrupt:
                # Re-raise cancellation
                raise
            except Exception:
                # Silently ignore hook errors to not break yt-dlp chain
                pass

        ydl_opts = {
            'quiet': True,  # Suppress console output
            'no_warnings': True,
            'noprogress': True,  # Suppress progress bar in console (we use hooks instead)
            'retries': MAX_RETRIES,
            'fragment_retries': MAX_RETRIES,
            'noplaylist': True,
            'outtmpl': str(out_dir / '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'format': fmt,
            'http_headers': DEFAULT_HEADERS.copy(),
            'progress_hooks': [hook],
        }

        if ffmpeg_path and Path(ffmpeg_path).exists():
            # Point yt-dlp to the bundled ffmpeg to ensure merging works
            ydl_opts['ffmpeg_location'] = str(Path(ffmpeg_path).parent)

        # Prefer m4a for audio-only
        if is_audio:
            ydl_opts['postprocessors'] = [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }
            ]

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            # Final completion update
            if progress_callback:
                progress_callback(0, 0, 100, 0, 0, "Completed")
            
            # Clean up any remaining temp/partial files
            from utils.ffmpeg_handler import FFmpegHandler
            FFmpegHandler.cleanup_default_temp_files(output_dir)
            
            return True
        except Exception as e:
            print(f"yt-dlp download failed: {e}")
            # Clean up partial downloads on failure
            from utils.ffmpeg_handler import FFmpegHandler
            FFmpegHandler.cleanup_default_temp_files(output_dir)
            return False
