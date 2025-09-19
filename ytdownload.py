# DEPRECATED: This is the original single-file version
# Use main.py for the new modular version instead
# This file is kept only as a backup reference

import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import filedialog, messagebox
from pytubefix import YouTube, Playlist
import requests
from io import BytesIO
from PIL import Image
import os
import threading
import time
import subprocess
import re
import math
import socket
import urllib3
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

# Disable insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Global variables
download_path = ""
stop_flag = False
last_time = 0
last_bytes = 0
current_download_size = 0
current_download_thread = None

def safe_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name)

def format_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def set_download_path():
    global download_path
    folder = filedialog.askdirectory()
    if folder:
        download_path = folder
        path_label.configure(text=f"Download Path: {download_path}")

def create_session():
    """Create a requests session with retries and custom settings"""
    session = requests.Session()
    
    # Configure retries
    retry_strategy = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=10, pool_maxsize=10)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # Set longer timeouts
    session.timeout = 30
    
    return session

def get_headers():
    """Return headers that mimic a web browser"""
    return {
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

def load_video():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL")
        return

    try:
        # Create a session for this request
        session = create_session()
        
        # Check if it's a playlist
        if 'list=' in url.lower():
            pl = Playlist(url)
            
            # Update UI to show playlist on the right side
            right_frame.pack(side="right", fill="y", padx=(10, 0))
            playlist_header.configure(text=f"Playlist: {pl.title}")
            
            # Clear previous playlist items
            for widget in playlist_scroll.winfo_children():
                widget.destroy()
            
            # Add playlist items
            for i, video in enumerate(pl.videos):
                try:
                    item_frame = ctk.CTkFrame(playlist_scroll, fg_color="#2B2B2B", corner_radius=5, height=40)
                    item_frame.pack(fill="x", pady=(0, 5))
                    
                    # Add thumbnail for each video
                    try:
                        headers = get_headers()
                        thumb_response = session.get(video.thumbnail_url, headers=headers, timeout=10, verify=False)
                        thumb_data = BytesIO(thumb_response.content)
                        thumb_img = Image.open(thumb_data)
                        thumb_img = thumb_img.resize((40, 30), Image.LANCZOS)
                        thumb_ctk = CTkImage(light_image=thumb_img, dark_image=thumb_img, size=(40, 30))
                        thumb_label = ctk.CTkLabel(item_frame, image=thumb_ctk, text="", width=40, height=30)
                        thumb_label.image = thumb_ctk
                        thumb_label.pack(side="left", padx=(5, 10))
                    except:
                        # If thumbnail fails, just show a placeholder
                        thumb_placeholder = ctk.CTkLabel(item_frame, text="🎬", width=40, height=30)
                        thumb_placeholder.pack(side="left", padx=(5, 10))
                    
                    # Video info
                    info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
                    info_frame.pack(side="left", fill="both", expand=True)
                    
                    pl_title_label = ctk.CTkLabel(info_frame, text=f"{i+1}. {safe_filename(video.title)}", 
                                              font=("Arial", 11), anchor="w", justify="left")
                    pl_title_label.pack(anchor="w", fill="x")
                    
                    duration_label = ctk.CTkLabel(info_frame, text=f"{format_time(video.length)}", 
                                                 font=("Arial", 10), text_color="#AAAAAA", anchor="w")
                    duration_label.pack(anchor="w")
                    
                except Exception as e:
                    print(f"Error adding playlist item: {e}")
                    continue
            
            yt = pl.videos[0]
        else:
            # For single videos, hide the playlist panel
            right_frame.pack_forget()
            yt = YouTube(url)
        
        # Update video preview (for both single videos and playlist first video)
        preview_frame.pack(fill="x", pady=10)
        video_title_label.configure(text=yt.title)
        video_channel_label.configure(text=f"{yt.author} • {format_time(yt.length)}")
        
        # Load thumbnail with CTkImage to avoid warning
        try:
            headers = get_headers()
            response = session.get(yt.thumbnail_url, headers=headers, timeout=10, verify=False)
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            # Resize to larger thumbnail
            img = img.resize((120, 90), Image.LANCZOS)
            ctk_img = CTkImage(light_image=img, dark_image=img, size=(120, 90))
            thumbnail_label.configure(image=ctk_img, text="")
            thumbnail_label.image = ctk_img
        except Exception as e:
            print(f"Error loading thumbnail: {e}")
            thumbnail_label.configure(image=None, text="No thumbnail")

        # Get all available streams
        streams = yt.streams.filter(file_extension='mp4')
        quality_options = []
        
        # Get video-only streams (adaptive)
        adaptive_streams = streams.filter(adaptive=True, only_video=True)
        for stream in adaptive_streams:
            if stream.resolution:
                size_info = f" ({format_size(stream.filesize)})" if stream.filesize else ""
                quality_options.append(f"{stream.resolution} - Adaptive{size_info}")
        
        # Get progressive streams (with audio)
        prog_streams = streams.filter(progressive=True)
        for stream in prog_streams:
            if stream.resolution:
                size_info = f" ({format_size(stream.filesize)})" if stream.filesize else ""
                quality_options.append(f"{stream.resolution} - Progressive{size_info}")
        
        # Sort by resolution (highest first)
        def resolution_key(x):
            try:
                res = x.split(' ')[0]
                if 'p' in res:
                    return int(res.replace('p', ''))
                elif 'k' in res:
                    return int(res.replace('k', '')) * 1000
                return 0
            except:
                return 0
        
        quality_options.sort(key=resolution_key, reverse=True)
        
        quality_combo.configure(values=quality_options)
        if quality_options:
            quality_combo.set(quality_options[0])
            
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load video: {str(e)}")

def progress_callback(stream, chunk, bytes_remaining):
    global last_time, last_bytes, stop_flag, current_download_size
    if stop_flag:
        raise Exception("Download cancelled")
    
    current_time = time.time()
    bytes_downloaded = current_download_size - bytes_remaining
    percentage = (bytes_downloaded / current_download_size) * 100
    
    # Calculate download speed
    delta_time = current_time - last_time
    delta_bytes = bytes_downloaded - last_bytes
    
    if delta_time > 0:
        speed = delta_bytes / delta_time  # bytes per second
        speed_mbps = speed / (1024 * 1024)  # MB per second
    else:
        speed_mbps = 0
    
    elapsed = int(time.time() - last_time)
    
    # Update UI
    root.after(0, lambda: update_progress(
        bytes_downloaded, 
        current_download_size, 
        percentage, 
        speed_mbps,
        elapsed
    ))
    
    last_time = current_time
    last_bytes = bytes_downloaded

def update_progress(downloaded, total, percentage, speed, elapsed):
    progress_bar.set(percentage / 100)
    progress_info.configure(
        text=f"Elapsed: {format_time(elapsed)} Size: {format_size(total)} Speed: {speed:.1f} MB/s"
    )

def download():
    global current_download_thread, stop_flag
    
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL")
        return

    selected_quality = quality_combo.get()
    is_audio = audio_var.get()
    is_playlist = right_frame.winfo_ismapped()  # Check if playlist frame is visible

    global download_path
    stop_flag = False
    
    if not download_path:
        set_download_path()
        if not download_path:
            return

    progress_bar.set(0)
    cancel_button.pack(side="right", padx=(10, 0), fill="x", expand=True)
    download_button.pack_forget()

    # Start download in a new thread
    current_download_thread = threading.Thread(
        target=download_thread, 
        args=(url, selected_quality, is_audio, is_playlist), 
        daemon=True
    )
    current_download_thread.start()

def download_thread(url, selected_quality, is_audio, is_playlist):
    global last_time, last_bytes, stop_flag, current_download_size
    
    try:
        if is_playlist:
            playlist = Playlist(url)
            total_videos = len(playlist.videos)
            for i, video in enumerate(playlist.videos):
                if stop_flag:
                    raise Exception("Download cancelled")
                root.after(0, lambda: progress_info.configure(text=f"Downloading {i+1} of {total_videos}"))
                download_single(video, selected_quality, is_audio, download_path)
            root.after(0, lambda: messagebox.showinfo("Success", "Playlist download completed!"))
        else:
            yt = YouTube(url)
            download_single(yt, selected_quality, is_audio, download_path)
            root.after(0, lambda: messagebox.showinfo("Success", "Download completed!"))
    except Exception as e:
        error_msg = str(e)
        if error_msg == "Download cancelled":
            root.after(0, lambda: messagebox.showinfo("Cancelled", "Download cancelled"))
        elif "ffmpeg" in error_msg.lower():
            root.after(0, lambda: messagebox.showerror(
                "FFmpeg Error", 
                "FFmpeg is required but not found. Please install FFmpeg and add it to your PATH."
            ))
        else:
            root.after(0, lambda: messagebox.showerror("Error", f"Download failed: {error_msg}"))
    finally:
        root.after(0, lambda: progress_info.configure(text="Ready"))
        root.after(0, lambda: progress_bar.set(0))
        root.after(0, lambda: cancel_button.pack_forget())
        root.after(0, lambda: download_button.pack(side="left", padx=(0, 10), fill="x", expand=True))

def download_single(yt, quality_str, is_audio, path):
    global current_download_size, stop_flag
    
    # Parse quality string
    quality_parts = quality_str.split(' - ')
    resolution = quality_parts[0]
    stream_type = quality_parts[1] if len(quality_parts) > 1 else "Progressive"
    
    if is_audio:
        audio_stream = yt.streams.get_audio_only()
        if not audio_stream:
            raise Exception("No audio stream available")
        
        current_download_size = audio_stream.filesize
        yt.register_on_progress_callback(progress_callback)
        
        # Download audio directly as mp3
        output_filename = f"{safe_filename(yt.title)}.mp3"
        output_path = os.path.join(path, output_filename)
        
        # Download with progress
        audio_stream.download(output_path=path, filename=output_filename)
    else:
        if "Progressive" in stream_type:
            # Use progressive stream (no FFmpeg needed)
            prog_stream = yt.streams.filter(
                progressive=True, 
                file_extension='mp4', 
                res=resolution
            ).first()
            
            if not prog_stream:
                raise Exception(f"No progressive stream available for {resolution}")
            
            current_download_size = prog_stream.filesize
            yt.register_on_progress_callback(progress_callback)
            
            # Download directly
            output_filename = f"{safe_filename(yt.title)}.mp4"
            prog_stream.download(output_path=path, filename=output_filename)
        else:
            # Adaptive stream handling (requires FFmpeg)
            video_stream = yt.streams.filter(
                adaptive=True, 
                file_extension='mp4', 
                res=resolution,
                only_video=True
            ).first()
            
            audio_stream = yt.streams.filter(
                adaptive=True,
                only_audio=True
            ).order_by('abr').desc().first()
            
            if not video_stream or not audio_stream:
                raise Exception("No suitable streams available")
            
            # Download video
            current_download_size = video_stream.filesize
            yt.register_on_progress_callback(progress_callback)
            video_path = video_stream.download(output_path=path, filename="video_temp.mp4")
            
            # Check if cancelled during download
            if stop_flag:
                if os.path.exists(video_path):
                    os.remove(video_path)
                raise Exception("Download cancelled")
            
            # Download audio
            current_download_size = audio_stream.filesize
            yt.register_on_progress_callback(progress_callback)
            audio_path = audio_stream.download(output_path=path, filename="audio_temp.mp4")
            
            # Check if cancelled during download
            if stop_flag:
                if os.path.exists(video_path):
                    os.remove(video_path)
                if os.path.exists(audio_path):
                    os.remove(audio_path)
                raise Exception("Download cancelled")
            
            # Merge with FFmpeg
            output_filename = f"{safe_filename(yt.title)}.mp4"
            output_path = os.path.join(path, output_filename)
            
            try:
                # Use FFmpeg to merge video and audio with proper encoding handling
                result = subprocess.run([
                    'ffmpeg', '-i', video_path, '-i', audio_path, 
                    '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', 
                    '-y',  # Overwrite output file if it exists
                    output_path
                ], check=True, capture_output=True, timeout=300, 
                # Set encoding to ignore errors to prevent UnicodeDecodeError
                text=True, encoding='utf-8', errors='ignore')
                
            except FileNotFoundError:
                raise Exception("FFmpeg is not installed or not in PATH")
            except subprocess.CalledProcessError as e:
                # Extract error message safely
                error_msg = e.stderr if isinstance(e.stderr, str) else str(e)
                raise Exception(f"FFmpeg failed to merge the files: {error_msg}")
            except subprocess.TimeoutExpired:
                raise Exception("FFmpeg took too long to process the video")
            finally:
                # Clean up temporary files
                if os.path.exists(video_path):
                    os.remove(video_path)
                if os.path.exists(audio_path):
                    os.remove(audio_path)

def cancel_download():
    global stop_flag
    stop_flag = True
    progress_info.configure(text="Cancelling...")

# Create main window
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("YouTube Downloader")
root.geometry("1000x700")  # Wider window to accommodate side-by-side view

# Main container with side-by-side layout
main_container = ctk.CTkFrame(root)
main_container.pack(fill="both", expand=True, padx=20, pady=20)

# Left frame for video preview and controls
left_frame = ctk.CTkFrame(main_container)
left_frame.pack(side="left", fill="both", expand=True)

# Right frame for playlist (initially empty)
right_frame = ctk.CTkFrame(main_container, width=300)
right_frame.pack_forget()  # Initially hidden

# Header
header_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
header_frame.pack(fill="x", pady=(0, 20))

app_title_label = ctk.CTkLabel(header_frame, text="YouTube Downloader", font=("Arial", 24, "bold"))
app_title_label.pack(side="left")

settings_button = ctk.CTkButton(header_frame, text="⚙️", width=40, height=40, 
                               font=("Arial", 16), command=set_download_path)
settings_button.pack(side="right")

# URL Input
url_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
url_frame.pack(fill="x", pady=(0, 20))

url_label = ctk.CTkLabel(url_frame, text="YouTube URL:", font=("Arial", 14))
url_label.pack(anchor="w", pady=(0, 5))

url_entry = ctk.CTkEntry(url_frame, height=40, font=("Arial", 14))
url_entry.pack(fill="x", pady=(0, 10))

load_button = ctk.CTkButton(url_frame, text="Load Video", command=load_video, 
                           height=40, font=("Arial", 14))
load_button.pack(fill="x")

# Video Preview (initially empty)
preview_frame = ctk.CTkFrame(left_frame, fg_color="#2B2B2B", corner_radius=10)

preview_header = ctk.CTkLabel(preview_frame, text="Video Preview", font=("Arial", 16, "bold"))
preview_header.pack(anchor="w", padx=20, pady=(15, 10))

preview_content = ctk.CTkFrame(preview_frame, fg_color="transparent")
preview_content.pack(fill="x", padx=20, pady=(0, 15))

# Thumbnail (larger size)
thumbnail_label = ctk.CTkLabel(preview_content, text="No video loaded", width=120, height=90, 
                              fg_color="#3B3B3B", corner_radius=10)
thumbnail_label.pack(side="left", padx=(0, 15))

# Video info
info_frame = ctk.CTkFrame(preview_content, fg_color="transparent")
info_frame.pack(side="left", fill="both", expand=True)

video_title_label = ctk.CTkLabel(info_frame, text="", font=("Arial", 16, "bold"), wraplength=500, anchor="w")
video_title_label.pack(anchor="w", pady=(0, 5))

video_channel_label = ctk.CTkLabel(info_frame, text="", font=("Arial", 14), text_color="#AAAAAA", anchor="w")
video_channel_label.pack(anchor="w")

# Quality selection
quality_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
quality_frame.pack(fill="x", pady=(0, 15))

quality_label = ctk.CTkLabel(quality_frame, text="Quality:", font=("Arial", 14))
quality_label.pack(anchor="w", pady=(0, 5))

quality_combo = ctk.CTkComboBox(quality_frame, values=[], height=40, font=("Arial", 14))
quality_combo.pack(fill="x")

# Audio option
audio_var = ctk.BooleanVar()
audio_check = ctk.CTkCheckBox(left_frame, text="Download as MP3", variable=audio_var, 
                             font=("Arial", 14), corner_radius=10)
audio_check.pack(anchor="w", pady=(0, 20))

# Progress section
progress_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
progress_frame.pack(fill="x", pady=(0, 10))

progress_bar = ctk.CTkProgressBar(progress_frame, height=12, progress_color="#4CAF50")
progress_bar.pack(fill="x", pady=(0, 10))
progress_bar.set(0)

progress_info = ctk.CTkLabel(progress_frame, text="Ready to download", 
                            font=("Arial", 14), text_color="#AAAAAA")
progress_info.pack(anchor="w")

# Buttons
button_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
button_frame.pack(fill="x", pady=(10, 0))

download_button = ctk.CTkButton(button_frame, text="Download", command=download, height=45, 
                               font=("Arial", 16), fg_color="#4CAF50", hover_color="#45A049")
download_button.pack(side="left", padx=(0, 10), fill="x", expand=True)

cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=cancel_download, height=45, 
                             font=("Arial", 16), fg_color="#F44336", hover_color="#D32F2F")

# Download path
path_label = ctk.CTkLabel(left_frame, text="Download Path: Not set", 
                         font=("Arial", 12), text_color="#777777")
path_label.pack(anchor="w", pady=(15, 0))

# Right panel for playlist
playlist_header = ctk.CTkLabel(right_frame, text="Playlist", font=("Arial", 16, "bold"))
playlist_header.pack(anchor="w", padx=10, pady=(10, 5))

# Playlist items (scrollable)
playlist_scroll = ctk.CTkScrollableFrame(right_frame, fg_color="transparent")
playlist_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

root.mainloop()