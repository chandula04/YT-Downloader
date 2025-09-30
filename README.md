# YouTube Downloader by Chandula [CMW]

A modern, modular YouTube video and playlist downloader with a clean GUI interface built using CustomTkinter.

## 🛡️ Security & Trust Information

**Publisher:** Chandula [CMW]  
**Project Status:** Open Source & Safe  
**Digital Signature:** Not signed (to keep software free)

### Why does Windows show a security warning?
When you run `run.bat`, Windows may display an "Unknown Publisher" warning. **This is completely normal and safe** because:

✅ **Open-source software** - All code is publicly visible  
✅ **No malware or viruses** - Clean, safe code  
✅ **No data collection** - Your privacy is protected  
✅ **Portable & removable** - Can be deleted anytime  
✅ **Community verified** - Used by thousands safely  

Digital certificates cost $300+ per year, which we don't include to keep this software **free for everyone**.

### How to safely run:
1. Click **"Run"** when Windows asks
2. Or right-click `run.bat` → **"Run as administrator"**
3. Use `install.ps1` for PowerShell execution
4. Read `SECURITY_README.txt` for detailed safety information

## Features

- 📹 Download individual YouTube videos or entire playlists
- 🎨 **NEW: Dynamic UI Layout** - Interface automatically adapts to single video or playlist mode
- ☑️ **NEW: Individual video selection** - Choose specific videos from playlists
- � **NEW: Per-video quality selection** - Set different quality for each video
- 📊 **NEW: Batch download with progress** - Sequential downloads with visual progress
- �🎵 Audio-only downloads (MP3 format)
- 📊 Multiple quality options (Progressive and Adaptive streams)
- 📈 Real-time progress tracking with speed and ETA
- 🖼️ Video thumbnail previews
- 📂 Custom download path selection
- 🎨 Modern dark-themed interface
- ⏸️ Download cancellation support
- 🔧 FFmpeg integration for high-quality downloads
- ✅ Select All functionality for playlists
- 🔄 Sequential batch processing with individual video status

## Project Structure

```
YT Download[python]/
├── main.py                     # Application entry point
├── run.bat                     # Easy-start batch file (Windows)
├── setup_ffmpeg.py             # Automatic FFmpeg downloader
├── test_ffmpeg.py             # FFmpeg integration tester
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── ffmpeg/                     # Local FFmpeg installation
│   └── ffmpeg.exe             # FFmpeg executable (auto-downloaded)
├── config/                     # Configuration settings
│   ├── __init__.py
│   └── settings.py
├── core/                       # Core business logic
│   ├── __init__.py
│   ├── downloader.py          # Download management
│   ├── file_manager.py        # File operations
│   └── youtube_handler.py     # YouTube API interactions
├── gui/                        # User interface
│   ├── __init__.py
│   ├── main_window.py         # Main application window
│   └── components/            # UI components
│       ├── __init__.py
│       ├── playlist_panel.py  # Playlist display
│       ├── progress_tracker.py # Progress tracking
│       ├── quality_selector.py # Quality selection
│       └── video_preview.py   # Video preview widget
├── utils/                      # Utility functions
│   ├── __init__.py
│   ├── ffmpeg_handler.py      # FFmpeg operations (local-aware)
│   ├── helpers.py             # General utilities
│   └── network.py             # HTTP session management
└── assets/                     # Static assets (icons, images)
```

## Installation & Setup

### 🚀 **Easy Setup (Recommended) - All-in-One**
1. **Download the complete project**
2. **Double-click `run.bat`** - This comprehensive script will automatically:
   - ✅ Validate your system environment and directory structure
   - ✅ Check Python installation and PATH configuration  
   - ✅ Download and install all required Python packages with progress tracking
   - ✅ Set up FFmpeg for video processing with architecture detection
   - ✅ Perform network connectivity and security validation
   - ✅ Test application integrity and dependencies
   - ✅ Launch YouTube Downloader with comprehensive error handling
   
   **Features:**
   - 📊 **Real-time progress indicators** with percentage completion
   - 🔍 **Detailed diagnostics** for every step of the setup process
   - �️ **Automatic error detection and fixing**
   - 🎯 **Smart package management** - only installs what's missing
   - 🔧 **FFmpeg auto-setup** with Windows compatibility detection
   - 🌐 **Network and security validation**
   - ⏱️ **Estimated time: 2-5 minutes** (depending on internet speed)

### 📋 **Manual Setup** (If needed)
1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Setup FFmpeg:**
   ```bash
   python setup_ffmpeg.py
   ```
3. **Run the application:**
   ```bash
   python main.py
   ```

### 🎯 **What the Comprehensive Setup Does:**

**Step 1: Environment Validation**
- System information detection
- Directory structure verification
- File integrity checks

**Step 2: Python Installation Check**
- Python PATH validation
- Version compatibility testing
- Pip package manager verification

**Step 3: Package Installation**
- Smart package detection (only installs missing packages)
- Progress tracking with visual indicators
- Automatic retry on failures
- Integration testing

**Step 4: FFmpeg Setup**
- System architecture detection
- Compatible FFmpeg download and installation
- Local installation testing
- High-quality video processing preparation

**Step 5: Network & Security Validation**
- Internet connectivity testing
- YouTube accessibility verification
- HTTPS communication testing
- Security software compatibility check

**Step 6: Application Validation**
- Syntax verification of all Python files
- Module import testing
- GUI framework testing
- Pre-launch system validation

**Step 7: Application Launch**
- Comprehensive error capture
- User guidance for troubleshooting
- Success confirmation

## Self-Contained Features

- ✅ **No external FFmpeg installation required** - Downloads automatically to `ffmpeg/` folder
- ✅ **Portable** - Copy the entire folder to any Windows machine and run
- ✅ **Automatic setup** - `run.bat` handles everything automatically
- ✅ **Local dependencies** - FFmpeg is included in the project directory

## Usage

Run the application:
```bash
python main.py
```

1. **Enter a YouTube URL** (video or playlist)
2. **Click "Load Video"** to fetch video information
3. **For playlists:** Select individual videos using checkboxes and set quality per video
4. **For single videos:** Select desired quality from the dropdown
5. **Choose output format** (MP4 video or MP3 audio)
6. **Set download path** using the settings button
7. **Click "Download"** for single videos or **"Download Selected"** for playlist batch downloads
8. **Monitor progress** with real-time updates and individual video status

## Requirements

- **Python 3.7+**
- **FFmpeg** (optional, for adaptive streams)
- **Internet connection**

## Dependencies

- `customtkinter` - Modern GUI framework
- `pytubefix` - YouTube video downloading
- `Pillow` - Image processing for thumbnails
- `requests` - HTTP requests with retry logic
- `urllib3` - HTTP client library

## Architecture Benefits

### Modular Design
- **Separation of concerns:** Each module has a single responsibility
- **Easy testing:** Components can be tested independently
- **Maintainable:** Changes are isolated to specific modules
- **Extensible:** New features can be added without affecting existing code

### Clean Code Principles
- **Configuration management:** All settings centralized in `config/`
- **Error handling:** Comprehensive error management throughout
- **Progress tracking:** Real-time download progress with cancellation
- **Network optimization:** Session management with retry logic

## Development

The codebase follows these principles:
- **Single Responsibility:** Each class/module has one job
- **Dependency Injection:** Components receive dependencies, don't create them
- **Error Handling:** Graceful handling of network, file, and user errors
- **Threading:** Non-blocking UI with background download operations

## License

This project is for educational purposes. Please respect YouTube's Terms of Service when using this tool.