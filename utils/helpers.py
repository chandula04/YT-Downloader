"""
Helper utility functions for the YouTube Downloader
"""

import re
import math
from config.settings import SIZE_UNITS


def safe_filename(name):
    """
    Convert unsafe filename characters to safe ones
    
    Args:
        name (str): Original filename
        
    Returns:
        str: Safe filename with invalid characters replaced
    """
    return re.sub(r'[<>:"/\\|?*]', '_', name)


def format_size(size_bytes):
    """
    Format file size in bytes to human readable format
    
    Args:
        size_bytes (int): Size in bytes
        
    Returns:
        str: Human readable size (e.g., "1.5 GB")
    """
    if size_bytes == 0:
        return "0B"
    
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {SIZE_UNITS[i]}"


def format_time(seconds):
    """
    Format seconds into MM:SS format
    
    Args:
        seconds (int): Time in seconds
        
    Returns:
        str: Formatted time string (MM:SS)
    """
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"


def resolution_key(quality_string):
    """
    Extract numeric resolution for sorting quality options
    
    Args:
        quality_string (str): Quality string like "1080p - Adaptive (1.5 GB)" or "2160p - Adaptive (4K)"
        
    Returns:
        int: Numeric resolution for sorting
    """
    try:
        # Get the first part (resolution)
        res = quality_string.split(' ')[0]
        
        if 'p' in res:
            # Handle standard resolutions like 1080p, 720p, 2160p, 1440p, 4320p
            return int(res.replace('p', ''))
        elif 'k' in res.lower():
            # Handle 4K, 2K, 8K format
            num = res.lower().replace('k', '')
            if num == '8':
                return 4320  # 8K = 4320p
            elif num == '4':
                return 2160  # 4K = 2160p
            elif num == '2':
                return 1440  # 2K = 1440p
            else:
                return int(num) * 1000 if num.isdigit() else 0
        return 0
    except:
        return 0


def parse_quality_string(quality_str):
    """
    Parse quality string into resolution and stream type
    
    Args:
        quality_str (str): Quality string like "1080p - Progressive"
        
    Returns:
        tuple: (resolution, stream_type)
    """
    quality_parts = quality_str.split(' - ')
    resolution = quality_parts[0]
    stream_type = quality_parts[1] if len(quality_parts) > 1 else "Progressive"
    return resolution, stream_type