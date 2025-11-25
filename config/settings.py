"""
Configuration settings for YouTube Downloader
"""

# Application settings
APP_TITLE = "YouTube Downloader"
APP_VERSION = "1.0.0"
WINDOW_GEOMETRY = "1400x800"  # Increased size for better playlist visibility

# UI Theme settings
APPEARANCE_MODE = "dark"
COLOR_THEME = "blue"

# Download settings
DEFAULT_DOWNLOAD_PATH = ""
MAX_RETRIES = 3
RETRY_BACKOFF_FACTOR = 0.5
REQUEST_TIMEOUT = 30
MERGE_TIMEOUT = 300

# Network settings
POOL_CONNECTIONS = 10
POOL_MAX_SIZE = 10

# UI Colors
COLORS = {
    'primary': "#4CAF50",
    'primary_hover': "#45A049",
    'danger': "#F44336",
    'danger_hover': "#D32F2F",
    'background': "#2B2B2B",
    'text_secondary': "#AAAAAA",
    'text_disabled': "#777777"
}

# HTTP Headers to mimic web browser
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
}

# Status force list for retries
RETRY_STATUS_CODES = [429, 500, 502, 503, 504]

# File size units
SIZE_UNITS = ["B", "KB", "MB", "GB", "TB"]

# FFmpeg settings
FFMPEG_VIDEO_CODEC = 'libx264'
FFMPEG_VIDEO_PRESET = 'faster'
FFMPEG_PIXEL_FORMAT = 'yuv420p'
FFMPEG_MOVFLAGS = '+faststart'
FFMPEG_AUDIO_CODEC = 'aac'
FFMPEG_STRICT_EXPERIMENTAL = 'experimental'

# TV optimized output defaults (kept conservative for playback compatibility)
FFMPEG_TV_MAX_WIDTH = 1920
FFMPEG_TV_MAX_HEIGHT = 1080
FFMPEG_TV_CRF = 20
FFMPEG_TV_VIDEO_PROFILE = 'high'
FFMPEG_TV_VIDEO_LEVEL = '4.1'
FFMPEG_TV_AUDIO_BITRATE = '192k'
FFMPEG_TV_AUDIO_CHANNELS = 2
FFMPEG_TV_AUDIO_SAMPLERATE = 48000
FFMPEG_TV_VSYNC_MODE = '1'