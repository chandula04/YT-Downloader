# 🚀 YouTube Downloader - Quick Start Guide

## Super Easy Setup (Windows)

### Method 1: One-Click Start
1. **Double-click `run.bat`**
2. **Wait for automatic setup** (downloads FFmpeg if needed)
3. **Start downloading!** 🎉

### Method 2: Manual Setup
1. Open command prompt in this folder
2. Run: `pip install -r requirements.txt`
3. Run: `python setup_ffmpeg.py` (downloads FFmpeg locally)
4. Run: `python main.py`

## ✅ What Gets Set Up Automatically

- ✅ **Python Dependencies** - All required packages
- ✅ **FFmpeg** - Downloaded to `ffmpeg/` folder (167MB)
- ✅ **No System Installation** - Everything stays in this folder
- ✅ **Portable** - Copy entire folder to any Windows PC

## 🎯 Features Ready to Use

- **YouTube Videos** - Download any quality
- **Playlists** - Select individual videos
- **Audio Only** - MP3 extraction
- **Batch Downloads** - Multiple videos at once
- **Progress Tracking** - Real-time download status

## 📁 Folder Structure After Setup

```
YT Download[python]/
├── ffmpeg/
│   └── ffmpeg.exe          ← Auto-downloaded
├── main.py                 ← Run this
├── run.bat                 ← Or double-click this
└── ... (other files)
```

## 🔧 Troubleshooting

**If run.bat doesn't work:**
- Right-click → "Run as administrator"
- Or use Method 2 above

**If downloads fail:**
- Check internet connection
- Try a different YouTube URL
- FFmpeg will be downloaded automatically if missing

## 🎬 Ready to Download!

Just run the application and paste any YouTube URL to get started!