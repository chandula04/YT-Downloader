# 🎬 YouTube Downloader by Chandula [CMW]

A modern YouTube video and playlist downloader with a clean GUI interface and smart features.

## 🚀 Quick Start

**Windows Users:** Just double-click `run_new.bat` - it handles everything automatically!

**Manual Setup:**
```bash
pip install -r requirements.txt
python main.py
```

## ✨ Key Features

### 📹 **Smart Downloads**
- 🎵 **Individual Videos** - Download any YouTube video
- 📂 **Full Playlists** - Download entire playlists with selection control
- 🎵 **Audio Only** - Extract MP3 audio from videos
- 📊 **Quality Options** - Multiple quality choices (only shows available options)

### 🎯 **User Experience** 
- ✅ **Responsive Interface** - No more freezing during loading
- 📈 **Progress Tracking** - Real-time download progress with ETA
- 🎬 **Video Previews** - See thumbnails before downloading
- ⏸️ **Cancel Downloads** - Stop downloads anytime
- 📂 **Custom Paths** - Choose your download location

### � **Smart Technology**
- 🛡️ **Error Recovery** - Automatic retry system for failed downloads
- ⚡ **FFmpeg Integration** - High-quality video processing with progress
- 🔄 **Background Processing** - Interface stays responsive
- 📱 **Loading Popups** - Clear progress feedback for playlist loading

## 🎯 How to Use

1. **Start the app** - Run `run_new.bat` or `python main.py`
2. **Paste YouTube URL** - Video or playlist link
3. **Click "Load Video"** - App fetches video information
4. **Select Quality** - Choose your preferred quality
5. **Choose Videos** (playlists) - Select which videos to download
6. **Click Download** - Watch the progress in real-time!

## � What You Get

- **Videos**: High-quality MP4 files
- **Audio**: Clean MP3 audio files  
- **Thumbnails**: Video preview images
- **Batch Downloads**: Multiple videos processed sequentially
- **Progress Reports**: Detailed download status

## 🔧 Latest Improvements

### ✅ **Fixed UI Freezing**
- No more "Not Responding" during playlist loading
- Background processing keeps interface smooth
- Loading popups show real-time progress

### ✅ **Smart Quality Detection** 
- Only shows qualities actually available for each video
- No more fake 8K options on 720p videos

### ✅ **Enhanced Error Handling**
- 85% success rate with automatic retry system
- Clear error messages with solutions
- Multiple client strategies for blocked videos

### ✅ **FFmpeg Progress Tracking**
- Real-time progress during video/audio merging
- Clear status messages: "Processing streams...", "Finalizing..."

### ✅ **Fixed FFmpeg Compatibility Issues** 
- Automatic detection and fix for "16-bit application" errors
- Smart architecture detection (32-bit vs 64-bit Windows)
- Automatic download of compatible FFmpeg version
- Enhanced compatibility testing and error recovery

## 🛡️ Security Information

**Publisher:** Chandula [CMW] - Open Source & Safe  
**Why Windows warns:** No expensive digital certificate (keeps software free)  
**Safety:** ✅ Open source ✅ No malware ✅ Community verified

## 📋 Requirements

- **Windows 10/11** (Primary support)
- **Python 3.7+** 
- **Internet connection**
- **FFmpeg** (auto-installed)

---

## 🛠️ Troubleshooting & Error Handling

### Common Issues & Solutions

#### 🚫 **"HTTP Error 403: Forbidden"**
**What it means:** YouTube is blocking download requests  
**Solutions:**
- ✅ App automatically tries 5 different client strategies
- Wait 5-10 minutes and try again
- Try a different video first
- Use VPN if persistent
- This affects ~15% of videos, most work fine

#### ⚠️ **"FFmpeg not found" or "16-bit application" error**
**What it means:** FFmpeg is missing or incompatible with your system architecture  
**Solutions:**
- ✅ **NEW FIX**: App automatically detects and downloads compatible version
- Run `python test_ffmpeg_compatibility.py` to diagnose the issue
- Delete the `ffmpeg` folder and restart app to re-download correct version
- The app now detects 32-bit vs 64-bit Windows automatically
- **Most Common Fix**: Run `python setup_ffmpeg.py` for automatic repair

#### 🔄 **UI Becomes Unresponsive**  
**What it means:** Interface freezing during loading
**Solutions:**
- ✅ **Fixed** - All loading now happens in background
- Loading popups show progress
- Interface stays responsive

#### 📊 **Wrong Quality Options Shown**
**What it means:** Quality menu shows unavailable options
**Solutions:**
- ✅ **Fixed** - Dynamic quality filtering implemented
- Only shows qualities actually available for each video

#### 🐌 **Slow Downloads or Timeouts**
**What it means:** Network or YouTube throttling
**Solutions:**
- Wait 15-30 minutes before trying again
- Try downloading individual videos instead of large playlists
- Check internet connection stability
- YouTube may be limiting requests from your IP

#### 🔒 **"Video Unavailable" or Private Videos**
**What it means:** Video is private, deleted, or region-restricted
**Solutions:**
- Try different public videos
- Check if video exists by opening in browser
- Some playlist videos may be private (app will skip them)

#### 📱 **Playlist Loading Issues**
**What it means:** Can't load playlist or videos
**Solutions:**
- ✅ **Improved** - Better progress tracking and error handling
- Ensure playlist is public
- Try loading individual videos from playlist
- Large playlists (100+ videos) may take several minutes

### Error Messages Explained

| Error | Meaning | Action |
|-------|---------|---------|
| **Throttling Detected** | YouTube rate limiting | Wait 15-30 minutes |
| **Region Restricted** | Video not available in your country | Try VPN |
| **Age Restricted** | Video requires age verification | Try different video |
| **Private/Deleted** | Video no longer accessible | Skip this video |
| **Network Timeout** | Internet connection issue | Check connection |
| **16-bit Application** | FFmpeg architecture mismatch | Run compatibility fix |

### Getting Help

1. **Check this troubleshooting section first**
2. **Try the automatic fixes** (app retries most issues)
3. **Wait a few minutes** (many issues are temporary)
4. **Try different videos** (test if it's video-specific)
5. **Restart the app** (clears any stuck states)

### Technical Details

- **Success Rate:** ~85% of videos download successfully
- **Retry System:** Automatic retries with 5 different client strategies
- **Error Recovery:** Smart handling of YouTube's changing restrictions
- **Performance:** Background processing keeps UI responsive

---

**Version:** Enhanced with latest YouTube compatibility  
**Last Updated:** September 2025  
**Repository:** [YT-Downloader](https://github.com/chandula04/YT-Downloader)