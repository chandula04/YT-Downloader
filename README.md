<div align="center">

# 🎬 YouTube Downloader v2.0.0

### *A Modern, Feature-Rich YouTube Video & Playlist Downloader*

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/chandula04/YT-Downloader/releases)
[![Python](https://img.shields.io/badge/python-3.7+-brightgreen.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

![YouTube Downloader Banner](assets/banner.png)

---

### ✨ Created by **CMW SOFTWARE** ✨
*Professional Tools for Modern Content Creators*

</div>

---

## 📖 Table of Contents

- [🌟 Overview](#-overview)
- [🎯 Key Features](#-key-features)
- [🚀 Quick Start](#-quick-start)
- [💎 Feature Highlights](#-feature-highlights)
- [🎨 User Interface](#-user-interface)
- [⚙️ Settings & Customization](#️-settings--customization)
- [🔔 Smart Notifications](#-smart-notifications)
- [🔄 Auto-Update System](#-auto-update-system)
- [📥 Download Features](#-download-features)
- [🛠️ Technical Details](#️-technical-details)
- [📦 Installation](#-installation)
- [🏗️ Building from Source](#️-building-from-source)
- [🔐 Security & Privacy](#-security--privacy)
- [❓ Troubleshooting](#-troubleshooting)
- [📝 Changelog](#-changelog)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👨‍💻 Author](#-author)

---

## 🌟 Overview

**YouTube Downloader v2.0.0** is a cutting-edge desktop application designed to download YouTube videos and playlists with ease. Built with modern Python technologies and featuring a sleek dark-themed interface, it offers a seamless downloading experience with real-time progress tracking, automatic updates, and intelligent quality selection.

### 🎯 Why Choose This Downloader?

- **🚄 Lightning Fast**: 60 FPS real-time progress tracking with multi-threaded downloads
- **🤖 Auto-Update Everything**: App and libraries update automatically from GitHub & PyPI
- **🔔 Smart Notifications**: Bell icon system alerts you to new updates instantly
- **🎨 Beautiful UI**: Modern CustomTkinter interface with smooth animations
- **📋 Playlist Support**: Download entire playlists with batch progress tracking
- **🎬 Live Preview**: See video thumbnails and metadata before downloading
- **⚡ FFmpeg Integration**: Professional video/audio merging for best quality
- **💾 No Installation**: Portable executable runs anywhere on Windows

---

## 🎯 Key Features

### 🎥 **Download Capabilities**
- ✅ **Single Video Downloads**: Any YouTube video in multiple quality options
- ✅ **Full Playlist Downloads**: Download entire playlists with one click
- ✅ **Audio-Only Mode**: Extract MP3 audio from videos
- ✅ **Multiple Quality Options**: 4K, 1080p, 720p, 480p, 360p, and more
- ✅ **Smart Quality Selection**: Auto-select best available quality
- ✅ **Custom Output Paths**: Choose where to save your downloads

### 🖥️ **User Interface**
- ✅ **Modern Dark Theme**: Easy on the eyes with professional styling
- ✅ **Responsive Design**: Resizable window that adapts to your screen
- ✅ **Real-Time Progress**: 60 FPS live updates with speed and ETA
- ✅ **Video Preview Panel**: Thumbnail, title, duration, and channel info
- ✅ **Playlist Panel**: Expandable side panel showing all videos
- ✅ **Animated Footer**: Beautiful CMW SOFTWARE branding with color glow effect
- ✅ **Loading Animations**: Smooth loading indicators during operations

### 🔄 **Auto-Update System** *(NEW in v2.0.0)*
- ✅ **Application Auto-Update**: Checks GitHub releases on startup
- ✅ **Library Auto-Update**: pytubefix and yt-dlp stay current automatically
- ✅ **One-Click Install**: Download and install updates with single button
- ✅ **Notification Bell**: Shows update count badge in real-time
- ✅ **Version Display**: Always shows current app version in notifications
- ✅ **Release Notes**: View changelog before updating
- ✅ **Safe Updates**: Automatic backup of current version before update

### 🔔 **Smart Notifications**
- ✅ **Bell Icon Badge**: Shows number of available updates (app + libraries)
- ✅ **Notification Panel**: Click bell to see all available updates
- ✅ **App Version Display**: Current version always visible in panel
- ✅ **Quick Update Buttons**: Update app or libraries directly from panel
- ✅ **Auto-Check on Startup**: Checks for updates when you launch the app

### ⚙️ **Advanced Features**
- ✅ **Settings Dialog**: Comprehensive settings with theme options
- ✅ **Download Path Memory**: Remembers your preferred save location
- ✅ **Cancel Downloads**: Force-stop any download with temp file cleanup
- ✅ **Error Recovery**: Automatic retry with backoff for failed downloads
- ✅ **Temp File Cleanup**: Removes incomplete downloads automatically
- ✅ **Keyboard Shortcuts**: F11 fullscreen, Ctrl+Plus/Minus window control
- ✅ **Thread-Safe Operations**: No UI freezing during downloads

---

## 🚀 Quick Start

### Option 1: Portable Executable (Recommended)

1. **Download** the latest `YouTube Downloader.exe` from [Releases](https://github.com/chandula04/YT-Downloader/releases)
2. **Run** the executable (no installation needed!)
3. **Paste** a YouTube URL and click "Load Video"
4. **Select** your preferred quality
5. **Download** and enjoy! 🎉

### Option 2: Run from Source

```bash
# Clone the repository
git clone https://github.com/chandula04/YT-Downloader.git
cd YT-Downloader

# Install dependencies
pip install -r requirements.txt

# Install Node.js LTS separately if it is not already installed. yt-dlp uses it
# to solve YouTube's current JavaScript player challenge.

# Run the application
python main.py
```

---

## 💎 Feature Highlights

### 🎬 Download Videos with Style

```
1. Paste URL → 2. Load Video → 3. Choose Quality → 4. Download!
```

The app features a beautiful video preview panel that shows:
- **📸 Thumbnail**: High-quality video thumbnail
- **📝 Title**: Full video title
- **⏱️ Duration**: Video length
- **👤 Channel**: Uploader name
- **📊 Views**: View count
- **👍 Likes**: Like count

### 📋 Playlist Downloads Made Easy

Click "Load Playlist" to see:
- Complete list of all videos in the playlist
- Individual video thumbnails and details
- Batch download with progress tracking
- Resume capability for interrupted downloads

### ⚡ Lightning-Fast Progress Tracking

Our **60 FPS refresh system** shows:
- **Real-time percentage**: Updated every 16ms
- **Download speed**: MB/s with smooth averaging
- **Time remaining**: Accurate ETA calculation
- **File size**: Downloaded / Total size
- **Visual progress bar**: Smooth animated bar

---

## 🎨 User Interface

### Main Window Layout

```
┌─────────────────────────────────────────────────────────────┐
│  🎬 YouTube Downloader v2.0.0          🔔(2) 📁 Settings   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [    Paste YouTube URL Here    ] [ Load Video ]           │
│                                                             │
│  ┌─────────────────────┐  ┌────────────────────────────┐   │
│  │                     │  │  🎥 Video Preview          │   │
│  │   Video/Playlist    │  │  Title: Amazing Video      │   │
│  │   Quality Selector  │  │  Duration: 10:30           │   │
│  │                     │  │  Channel: Creator Name     │   │
│  │   [Download Video]  │  │  Views: 1.2M | Likes: 50K  │   │
│  └─────────────────────┘  └────────────────────────────┘   │
│                                                             │
│  Progress: ████████████░░░░░░░░ 65%                        │
│  Speed: 5.2 MB/s | ETA: 00:45 | Size: 89.5 MB / 137 MB     │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│          ✨ Created by CMW SOFTWARE ✨                      │
└─────────────────────────────────────────────────────────────┘
```

### 🎨 Theme Options

- **Dark Mode** (Default): Professional dark theme
- **Light Mode**: Clean light theme
- **System Mode**: Follow Windows theme

---

## ⚙️ Settings & Customization

Access settings via the **Settings** button in the top-right corner:

### 📁 **Download Settings**
- Choose default download folder
- Remember last used path
- Auto-create folders if missing

### 🎨 **Appearance**
- Toggle Dark/Light/System theme
- Color scheme selection
- Window size preferences

### 🔄 **App Updates**
- Check for app updates (GitHub releases)
- Install new versions with one click
- View current version and changelog

### 📚 **Library Updates**
- Check for library updates (pytubefix, yt-dlp)
- Update download libraries manually
- Auto-update on startup (optional)

### 🔧 **Advanced**
- Network timeout settings
- Retry attempts configuration
- FFmpeg merge timeout

---

## 🔔 Smart Notifications

### Notification Bell System

The **bell icon** (🔔) in the top-right shows:
- **Badge count**: Number of available updates
- **Example**: 🔔(2) means 2 updates available

**Click the bell** to open the notification panel:

```
┌─────────────────────────────────────┐
│  📢 Notifications                   │
├─────────────────────────────────────┤
│  ℹ️ Current App Version: 2.0.0      │
│                                     │
│  ✅ App Update Available!           │
│  Version 2.1.0 is ready             │
│  [Update Now]                       │
│                                     │
│  ✅ Library Updates Available!      │
│  pytubefix, yt-dlp need updates     │
│  [Update Libraries]                 │
└─────────────────────────────────────┘
```

### Auto-Check Features
- ✅ Checks for updates on app startup
- ✅ Updates badge count automatically
- ✅ Shows notifications non-intrusively
- ✅ One-click update from panel

---

## 🔄 Auto-Update System

### How It Works

**YouTube Downloader v2.0.0** features a revolutionary auto-update system:

#### 📱 **Application Updates** (GitHub Releases)
1. App checks GitHub on startup
2. Compares current version with latest release
3. Downloads new `.exe` if available
4. Creates update batch script
5. Installs update and restarts app automatically
6. Backs up old version as `.backup`

#### 📚 **Library Updates** (PyPI)
1. Checks pytubefix and yt-dlp versions on startup
2. Compares with latest PyPI versions
3. One-click update via Settings or Notification panel
4. Updates libraries using pip
5. No restart required!

### Manual Update Options

**Via Settings Dialog:**
- Go to Settings → App Updates section
- Click "Check for App Updates" to scan GitHub
- Click "Install Update" to download and install
- Libraries section lets you update download libraries

**Via Notification Panel:**
- Click bell icon (🔔) when badge shows updates
- Click "Update Now" for app updates
- Click "Update Libraries" for library updates

### Update Safety
- ✅ **Version Verification**: Semantic version comparison (2.0.0 → 2.1.0)
- ✅ **Automatic Backup**: Old version saved before update
- ✅ **Safe Installer**: Batch script waits for app to close
- ✅ **Error Handling**: Shows errors if update fails

---

## 📥 Download Features

### Supported Video Types
- ✅ Regular YouTube videos
- ✅ Age-restricted videos
- ✅ Live stream recordings
- ✅ Private/Unlisted videos (with link)
- ✅ Shorts
- ✅ 4K/8K videos

### Quality Options

**Video Quality:**
- 🎥 **4K** (2160p) - Ultra HD
- 🎥 **1080p** - Full HD
- 🎥 **720p** - HD
- 🎥 **480p** - SD
- 🎥 **360p** - Mobile
- 🎥 **144p** - Low bandwidth

**Audio Quality:**
- 🎵 **Audio Only** - Best audio quality (M4A/WebM)
- 🎵 **MP3** - Converted audio format

### Smart Download Features

**Automatic Best Quality:**
- Selects highest available quality when "Best" is chosen
- Merges video + audio for best results
- Uses FFmpeg for professional merging

**Resume Support:**
- Detects interrupted downloads
- Option to resume or restart
- Cleans up incomplete files

**Batch Downloads:**
- Download entire playlists
- Progress for each video
- Overall batch progress
- Pause/Resume/Cancel support

---

## 🛠️ Technical Details

### Architecture

```
YouTube Downloader v2.0.0
│
├── 🖥️ GUI Layer (CustomTkinter)
│   ├── Main Window (1400x800 responsive)
│   ├── Video Preview Panel
│   ├── Playlist Panel
│   ├── Progress Tracker (60 FPS refresh)
│   ├── Settings Dialog
│   └── Update Dialog
│
├── 🎯 Core Logic
│   ├── YouTube Handler (pytubefix)
│   ├── Download Manager (threading)
│   ├── File Manager (path handling)
│   └── Progress System (thread-safe)
│
├── 🔧 Utilities
│   ├── App Updater (GitHub API)
│   ├── Library Updater (PyPI)
│   ├── FFmpeg Handler (merging)
│   ├── Network Helper (requests)
│   └── yt-dlp Handler (fallback)
│
└── ⚙️ Configuration
    ├── Settings (app config)
    └── User Settings (persistence)
```

### Technologies Used

| Technology | Purpose | Version |
|-----------|---------|---------|
| **Python** | Core runtime | 3.7+ |
| **CustomTkinter** | Modern UI framework | Latest |
| **pytubefix** | YouTube download library | Auto-updated |
| **yt-dlp** | Fallback downloader | Auto-updated |
| **FFmpeg** | Video/audio merging | 7.1+ |
| **Requests** | HTTP client for updates | Latest |
| **Threading** | Async operations | Built-in |
| **PyInstaller** | Executable builder | Latest |

### Performance Features

- **60 FPS Progress Updates**: 16ms refresh rate for smooth UI
- **Multi-threading**: Separate threads for download, UI, and updates
- **Thread-safe Data**: Lock-protected progress data storage
- **Efficient Memory**: Streams large files without loading fully
- **Smart Caching**: Caches video metadata to avoid re-fetching
- **Connection Pooling**: Reuses HTTP connections for speed

---

## 📦 Installation

### Requirements

**For Running Executable:**
- ✅ Windows 10 or later (64-bit)
- ✅ 100 MB free disk space
- ✅ Internet connection
- ✅ FFmpeg (included in build)

**For Running from Source:**
```
Python 3.7+
customtkinter
pytubefix
yt-dlp
requests
Pillow
```

### Step-by-Step Installation

#### 📥 Method 1: Portable Executable (No Installation)

1. Go to [Releases](https://github.com/chandula04/YT-Downloader/releases)
2. Download `YouTube Downloader.exe` from latest release
3. Run the `.exe` file directly
4. Allow Windows Firewall if prompted
5. Start downloading! 🎉

**Note:** Windows may show a SmartScreen warning. Click "More info" → "Run anyway" to proceed.

#### 🔧 Method 2: Run from Source

```bash
# 1. Clone repository
git clone https://github.com/chandula04/YT-Downloader.git
cd YT-Downloader

# 2. Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # On Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup FFmpeg (automatic)
python setup_ffmpeg.py

# 5. Run application
python main.py
```

---

## 🏗️ Building from Source

Want to build your own executable? Follow these steps:

### Prerequisites
```bash
pip install pyinstaller
```

### Build Process

1. **Prepare Build Environment**
```bash
# Clean previous builds
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue
```

2. **Run PyInstaller**
```bash
# Option 1: Use batch script (Windows)
.\build_installer.bat

# Option 2: Manual PyInstaller command
pyinstaller --name "YouTube Downloader" ^
    --onefile ^
    --windowed ^
    --icon=assets/icon.ico ^
    --add-data "assets;assets" ^
    --add-data "ffmpeg;ffmpeg" ^
    --hidden-import customtkinter ^
    --hidden-import pytubefix ^
    --hidden-import yt_dlp ^
    main.py
```

3. **Find Your Build**
- Executable will be in `dist/YouTube Downloader.exe`
- File size: ~50-100 MB (includes all dependencies)

### Creating GitHub Releases

To enable auto-update functionality:

1. **Build the executable** (see above)

2. **Create GitHub Release**
```bash
# Tag version
git tag v2.0.0
git push origin v2.0.0

# Create release on GitHub
# - Go to repository → Releases → Draft new release
# - Tag: v2.0.0
# - Title: YouTube Downloader v2.0.0
# - Description: Add changelog
```

3. **Upload Executable**
- Attach `YouTube Downloader.exe` to the release
- Publish the release

4. **Users Get Auto-Update!**
- App checks this release on startup
- Users get notification when v2.0.0 is available
- One-click update downloads and installs

---

## 🔐 Security & Privacy

### Data Privacy
- ✅ **No Data Collection**: App doesn't collect or send any user data
- ✅ **No Analytics**: No tracking or telemetry
- ✅ **Local Storage Only**: All settings saved locally
- ✅ **No Ads**: Completely ad-free experience

### Update Security
- ✅ **GitHub Verified**: Updates only from official repository
- ✅ **HTTPS Only**: Encrypted connections for all downloads
- ✅ **Version Verification**: Semantic versioning check before update
- ✅ **Backup System**: Automatic backup before updates

### Windows SmartScreen Warning

When running the executable for the first time, Windows may show:
```
"Windows protected your PC"
```

**This is normal** for unsigned executables. To proceed:
1. Click **"More info"**
2. Click **"Run anyway"**

The app is safe and open-source. You can review the code anytime!

---

## ❓ Troubleshooting

### Common Issues & Solutions

#### 🚫 **"Unable to fetch video information"**
**Cause**: Network issue, age restriction, or region block
**Solutions:**
- Check your internet connection
- Try updating libraries via Settings
- Use VPN if region-blocked
- Check if video URL is valid

#### ⏸️ **Download stuck or not progressing**
**Cause**: Network timeout or server issue
**Solutions:**
- Click Cancel and try again
- Check internet stability
- Try different quality option
- Restart the application

#### 📁 **"FFmpeg not found" error**
**Cause**: FFmpeg not in correct location
**Solutions:**
- Run `python setup_ffmpeg.py`
- Check `ffmpeg/` folder exists
- Re-download FFmpeg manually
- Reinstall application

#### 🔄 **Update fails to install**
**Cause**: Permissions or file lock issue
**Solutions:**
- Close all instances of the app
- Run as administrator
- Check antivirus isn't blocking
- Download update manually from releases

#### 🖼️ **Video preview not showing**
**Cause**: Network issue or invalid thumbnail
**Solutions:**
- Check internet connection
- Try loading another video
- Clear browser cache if using
- Restart application

#### 💾 **"Cannot save file" error**
**Cause**: Insufficient permissions or disk space
**Solutions:**
- Choose different download folder
- Check disk space available
- Run as administrator
- Check folder permissions

### Getting Help

Still having issues? Get help here:

- 📧 **Email**: chandulawijesekara4@gmail.com
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/chandula04/YT-Downloader/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/chandula04/YT-Downloader/discussions)
- 📚 **Documentation**: Check this README thoroughly

When reporting bugs, include:
- Windows version
- App version (shown in notification panel)
- Error message (screenshot)
- Steps to reproduce

---

## 📝 Changelog

### Version 2.0.0 (Latest) - February 2026

#### 🎉 Major Features
- ✨ **Auto-Update System**: App checks GitHub releases and updates automatically
- 🔔 **Smart Notifications**: Bell icon with badge count for available updates
- 📚 **Library Auto-Update**: pytubefix and yt-dlp update automatically
- ⚡ **60 FPS Progress**: Real-time progress tracking with 16ms refresh rate
- 🎨 **Animated Footer**: Beautiful CMW SOFTWARE branding with color glow
- 🔄 **Update Dialog**: Comprehensive update UI with progress and release notes

#### 🔧 Improvements
- Improved progress tracking accuracy
- Enhanced error handling and recovery
- Better temp file cleanup
- Optimized memory usage
- Faster startup time
- Smoother UI animations

#### 🐛 Bug Fixes
- Fixed video preview crash on URL clear
- Fixed settings save issues
- Fixed cancel button functionality
- Removed TV optimization (legacy code)
- Fixed Git repository large file issues

#### 🗑️ Removals
- Removed TV optimization feature
- Removed automatic library updates switch (now always checks)
- Cleaned up legacy code

---

### Version 1.0.0 - Initial Release

#### Features
- Basic video downloading
- Playlist support
- Quality selection
- Dark theme UI
- Progress tracking
- Settings dialog
- FFmpeg integration

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Ways to Contribute

1. **🐛 Report Bugs**
   - Use [GitHub Issues](https://github.com/chandula04/YT-Downloader/issues)
   - Include detailed description and steps to reproduce

2. **💡 Suggest Features**
   - Open a feature request issue
   - Explain use case and benefits

3. **🔧 Submit Pull Requests**
   - Fork the repository
   - Create feature branch (`git checkout -b feature/AmazingFeature`)
   - Commit changes (`git commit -m 'Add AmazingFeature'`)
   - Push to branch (`git push origin feature/AmazingFeature`)
   - Open Pull Request

4. **📚 Improve Documentation**
   - Fix typos or unclear sections
   - Add examples or tutorials
   - Translate to other languages

### Development Setup

```bash
# Clone your fork
git clone https://github.com/chandula04/YT-Downloader.git
cd YT-Downloader

# Add upstream remote
git remote add upstream https://github.com/chandula04/YT-Downloader.git

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Make your changes and test
python main.py
```

### Code Style
- Follow PEP 8 guidelines
- Add docstrings to functions
- Comment complex logic
- Keep functions focused and small

---

## 📄 License

This project is licensed under the **MIT License** - see below for details:

```
MIT License

Copyright (c) 2024-2026 Chandula Wijesekara (CMW SOFTWARE)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👨‍💻 Author

<div align="center">

### **Chandula Wijesekara**
*Founder & Lead Developer at CMW SOFTWARE*

[![GitHub](https://img.shields.io/badge/GitHub-chandula04-181717?style=for-the-badge&logo=github)](https://github.com/chandula04)
[![Email](https://img.shields.io/badge/Email-chandulawijesekara4@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:chandulawijesekara4@gmail.com)

📍 **Based in Sri Lanka** 🇱🇰

---

### About CMW SOFTWARE

CMW SOFTWARE specializes in creating professional, user-friendly desktop applications for content creators, developers, and everyday users. We believe in:

- ✨ **Beautiful Design**: Every pixel matters
- ⚡ **Performance**: Fast, responsive, and efficient
- 🔒 **Privacy**: Your data stays yours
- 🆓 **Open Source**: Transparent and community-driven

---

</div>

## 🙏 Acknowledgments

Special thanks to:

- **pytubefix** - Excellent YouTube downloading library
- **yt-dlp** - Powerful fallback downloader
- **CustomTkinter** - Modern tkinter library
- **FFmpeg** - Industry-standard media processing
- **GitHub** - Code hosting and release platform
- **Python Community** - Amazing ecosystem
- **Users & Contributors** - Your feedback makes this better!

---

<div align="center">

### ⭐ Star this repository if you find it useful!

**Made with ❤️ by CMW SOFTWARE**

*Empowering creators, one download at a time*

---

![Footer Banner](assets/footer.png)

**© 2024-2026 CMW SOFTWARE. All Rights Reserved.**

</div>