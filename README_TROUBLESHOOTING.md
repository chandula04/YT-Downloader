# YouTube Downloader

A modern, user-friendly YouTube video downloader with high-quality adaptive streaming support.

## 🚀 Quick Start

1. **Run the app**: Double-click `run.bat`
2. **Paste YouTube URL**: Copy any YouTube video/playlist URL
3. **Select quality**: Choose from 8K down to 144p with file sizes
4. **Download**: Click download and enjoy!

## ✨ Features

- **All Resolutions**: 8K, 4K, 2K, Full HD, HD, SD, and lower
- **File Size Display**: See estimated file sizes for each quality
- **Adaptive Streaming**: Highest quality downloads using video+audio merge
- **Playlist Support**: Download entire playlists at once
- **Smart Setup**: Automatically installs everything you need
- **VPN Compatible**: Works with VPN connections
- **Anti-Throttling**: Multiple YouTube client strategies

## 🔧 Troubleshooting

### FFmpeg Compatibility Error (WinError 216)

If you get an error like "This version of %1 is not compatible with the version of Windows":

**Quick Fix:**
1. Close the app
2. Double-click `fix_ffmpeg.bat`
3. Restart the app

**Alternative Fix:**
1. Delete the `ffmpeg` folder
2. Run `run.bat` again
3. The correct FFmpeg will be downloaded

### Other Common Issues

**Problem**: "pip is not recognized"
**Solution**: Run `run.bat` - it will install Python and pip automatically

**Problem**: Download fails with throttling errors
**Solution**: 
- Try a different video
- Wait a few minutes and retry
- Use a VPN if available
- Run `python update_pytubefix.py`

**Problem**: No 8K option for video
**Solution**: Many YouTube videos don't actually have 8K streams available, even if labeled as 8K

## 📁 Files

- `run.bat` - Main launcher (installs everything and starts app)
- `main.py` - Main application
- `fix_ffmpeg.bat` - Fix FFmpeg compatibility issues
- `update_pytubefix.py` - Update YouTube downloader library
- `setup_ffmpeg.py` - Install correct FFmpeg version

## 🎯 System Requirements

- **Windows**: 7, 8, 10, or 11 (32-bit or 64-bit)
- **Python**: Automatically installed by `run.bat`
- **Internet**: Required for downloads and setup

## 💡 Tips

- **High Quality**: Use adaptive streams (automatically selected) for best quality
- **File Sizes**: Actual download sizes may vary from estimates
- **Batch Downloads**: Paste playlist URLs to download multiple videos
- **Speed**: Download speed depends on your internet and YouTube's servers

## 🆘 Support

If you encounter issues:

1. Run `fix_ffmpeg.bat` for compatibility problems
2. Run `python update_pytubefix.py` for YouTube errors
3. Delete `ffmpeg` folder and restart for persistent issues
4. Check that you have internet connection
5. Try running `run.bat` as administrator

## 🔄 Updates

The app automatically updates its YouTube compatibility library. For manual updates:

```cmd
python update_pytubefix.py
```

## ⚖️ Legal

This tool is for downloading videos you have permission to download. Respect copyright laws and YouTube's terms of service.