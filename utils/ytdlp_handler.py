"""
yt-dlp downloader for robust handling of YouTube video downloads and metadata extraction.
"""

import os
import shutil
import sys
from pathlib import Path
from config.settings import DEFAULT_HEADERS, MAX_RETRIES
from config.user_settings import user_settings


class YtDlpHandler:
    """Wrapper around yt-dlp with progress hook mapped to app's progress callback."""

    @staticmethod
    def _get_node_path():
        """Find the system Node.js runtime if available."""
        return shutil.which("node")

    class _ProgressState:
        """Keep yt-dlp's per-file progress stable across format downloads."""

        def __init__(self):
            self.files = {}

        def update(self, data):
            filename = data.get('filename') or data.get('tmpfilename') or '<download>'
            state = self.files.setdefault(filename, {'downloaded': 0, 'total': 0})

            downloaded = int(data.get('downloaded_bytes', 0) or 0)
            state['downloaded'] = max(state['downloaded'], downloaded)

            # Estimates can change on every fragment. Lock the first useful
            # value so the displayed denominator does not jump while downloading.
            if state['total'] <= 0:
                total = int(
                    data.get('total_bytes')
                    or data.get('total_bytes_estimate')
                    or data.get('info_dict', {}).get('filesize', 0)
                    or 0
                )
                if total > 0:
                    state['total'] = total

            downloaded_total = sum(item['downloaded'] for item in self.files.values())
            known_totals = [item['total'] for item in self.files.values() if item['total'] > 0]
            total = sum(known_totals)
            return downloaded_total, total

    @staticmethod
    def _build_format_for_height(height: int, is_audio: bool, tv_format: bool = False) -> str:
        if is_audio:
            return "bestaudio/best"
        if height and height > 0:
            if tv_format:
                return (
                    f"bv*[height<={height}]+ba/"
                    f"b[height<={height}]/"
                    f"bestvideo*+bestaudio/best"
                )
            # Prefer mp4 video + m4a audio within height cap, fall back sensibly
            return (
                f"bv*[ext=mp4][height<={height}]+ba[ext=m4a]/"
                f"b[ext=mp4][height<={height}]/"
                f"bestvideo*+bestaudio/best"
            )
        # Default best if no height
        if tv_format:
            return "bv*+ba/b/best"
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
    def extract_info(url: str):
        """
        Extract video information and available formats using yt-dlp.
        Returns dict with title, duration, author, thumbnail_url, views, quality_options.
        """
        try:
            from yt_dlp import YoutubeDL
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'skip_download': True,
                'noplaylist': True,
                'extractor_args': {
                    'youtube': {
                        'skip': ['dash', 'hls', 'translated_subs', 'comments']
                    }
                },
                'http_headers': DEFAULT_HEADERS.copy(),
            }
            node_path = YtDlpHandler._get_node_path()
            if node_path:
                ydl_opts['js_runtimes'] = {'node': {'path': node_path}}

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info:
                    return None

                formats = info.get('formats') or []
                heights = set()
                for f in formats:
                    h = f.get('height')
                    if h and isinstance(h, int) and h >= 144:
                        heights.add(h)

                sorted_heights = sorted(list(heights), reverse=True)
                quality_options = []
                for h in sorted_heights:
                    if h >= 2160:
                        label = f"{h}p - Adaptive (4K)"
                    elif h >= 1440:
                        label = f"{h}p - Adaptive (2K)"
                    elif h >= 1080:
                        label = f"{h}p - Adaptive (Full HD)"
                    elif h >= 720:
                        label = f"{h}p - Adaptive (HD)"
                    elif h >= 480:
                        label = f"{h}p - Adaptive (SD)"
                    else:
                        label = f"{h}p - Adaptive"
                    quality_options.append(label)

                if not quality_options:
                    quality_options = [
                        "1080p - Adaptive (Full HD)",
                        "720p - Adaptive (HD)",
                        "480p - Adaptive (SD)",
                        "360p - Adaptive"
                    ]

                return {
                    'title': info.get('title') or 'Unknown Title',
                    'duration': int(info.get('duration') or 0),
                    'author': info.get('uploader') or info.get('channel') or 'Unknown Channel',
                    'thumbnail_url': info.get('thumbnail') or '',
                    'views': int(info.get('view_count') or 0),
                    'quality_options': quality_options,
                    'raw_info': info
                }
        except Exception as e:
            print(f"yt-dlp extract_info error: {e}")
            return None

    @staticmethod
    def download_video(url: str, output_dir: str, quality_str: str, is_audio: bool, progress_callback=None, ffmpeg_path=None, cancel_callback=None, tv_format: bool = None) -> bool:
        """
        Download a single video using yt-dlp with progress mapping and TV/MKV support.

        Args:
            url: Video URL
            output_dir: Output directory
            quality_str: Requested quality string
            is_audio: Audio-only flag
            progress_callback: Optional callback(downloaded, total, pct, speedMBps, elapsed, text)
            ffmpeg_path: Optional full path to ffmpeg executable to aid merging
            cancel_callback: Optional callback returning True if download was cancelled
            tv_format: Optional boolean flag for TV format (MKV). If None, uses user_settings.

        Returns:
            True on success, False on failure
        """
        try:
            from yt_dlp import YoutubeDL
        except Exception as e:
            print(f"yt-dlp not available: {e}")
            return False

        if tv_format is None:
            tv_format = user_settings.get_tv_format()

        height = YtDlpHandler._parse_height(quality_str)
        fmt = YtDlpHandler._build_format_for_height(height, is_audio, tv_format=tv_format)

        # Ensure output directory exists
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        import time
        start_time = time.time()
        progress_state = YtDlpHandler._ProgressState()

        def hook(d):
            if not progress_callback:
                return
            try:
                if cancel_callback and cancel_callback():
                    raise KeyboardInterrupt("Download cancelled by user")
                if d.get('status') == 'downloading':
                    downloaded, total = progress_state.update(d)
                    
                    if total > 0:
                        pct = min((downloaded / total) * 100.0, 100.0)
                    else:
                        pct = 0.0
                    
                    speed = d.get('speed', 0.0) or 0.0  # bytes/sec
                    speed_mbps = float(speed) / (1024 * 1024) if speed else 0.0
                    elapsed = int(time.time() - start_time)
                    progress_callback(downloaded, total, pct, speed_mbps, elapsed, None)
                elif d.get('status') == 'finished':
                    stage_msg = "Merging to MKV with FFmpeg..." if (tv_format and not is_audio) else "Processing with FFmpeg..."
                    progress_callback(0, 0, 95, 0, 0, stage_msg)
            except KeyboardInterrupt:
                raise
            except Exception:
                pass

        use_mkv = bool(tv_format and not is_audio)
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'noprogress': True,
            'retries': MAX_RETRIES,
            'fragment_retries': MAX_RETRIES,
            'noplaylist': True,
            'outtmpl': str(out_dir / '%(title)s.%(ext)s'),
            'merge_output_format': 'mkv' if use_mkv else 'mp4',
            'format': fmt,
            'http_headers': DEFAULT_HEADERS.copy(),
            'progress_hooks': [hook],
            'remote_components': ['ejs:github'],
        }

        # If TV format is requested for video, ensure remuxing/conversion to MKV occurs even for single streams
        if use_mkv:
            ydl_opts['remux_video'] = 'mkv'
            ydl_opts['postprocessors'] = [
                {
                    'key': 'FFmpegVideoRemuxer',
                    'preferedformat': 'mkv',
                }
            ]

        node_path = YtDlpHandler._get_node_path()
        if node_path:
            ydl_opts['js_runtimes'] = {'node': {'path': node_path}}

        if ffmpeg_path and Path(ffmpeg_path).exists():
            ydl_opts['ffmpeg_location'] = str(Path(ffmpeg_path).parent)

        # Audio-only extraction to mp3
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
            
            if progress_callback:
                progress_callback(0, 0, 100, 0, 0, "Completed")
            
            from utils.ffmpeg_handler import FFmpegHandler
            FFmpegHandler.cleanup_default_temp_files(output_dir)
            
            return True
        except Exception as e:
            print(f"yt-dlp download failed: {e}")
            from utils.ffmpeg_handler import FFmpegHandler
            FFmpegHandler.cleanup_default_temp_files(output_dir)
            raise RuntimeError(f"yt-dlp download failed: {e}") from e
