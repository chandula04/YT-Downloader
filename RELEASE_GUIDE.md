# How to Release New Versions (Auto-Update Guide)

This guide explains how to publish new versions so users can auto-update.

## 📦 Build Process

### 1. Update Version Number
Before building, update the version in:
```python
# config/settings.py
APP_VERSION = "2.1.0"  # Increment this!
```

### 2. Build the Application
```batch
# Run the build script
build_installer.bat
```

This creates:
- `dist\YouTube Downloader.exe` - Standalone executable
- `installer\Output\YouTubeDownloaderSetup.exe` - Windows installer (if Inno Setup installed)

## 🚀 GitHub Release Process

### 1. Create a New Release
1. Go to https://github.com/chandula04/YT-Downloader/releases
2. Click **"Draft a new release"**
3. Click **"Choose a tag"** → Type `v2.1.0` (match APP_VERSION) → Click **"Create new tag"**

### 2. Fill Release Information
- **Release title**: `YouTube Downloader v2.1.0`
- **Description**: Write what's new, example:
```markdown
## 🎉 What's New in v2.1.0

### ✨ New Features
- ✅ Real-time download progress at 60 FPS
- ✅ Auto-update system for application
- ✅ Animated footer branding
- ✅ Improved settings dialog

### 🐛 Bug Fixes
- Fixed video preview crash when clearing URL
- Fixed temp file cleanup
- Fixed cancel button functionality

### 🔧 Improvements
- Removed TV optimization feature
- Simplified FFmpeg to direct copy
- Enhanced progress tracking

Download and enjoy! 🎊
```

### 3. Upload the .exe File
- Click **"Attach binaries"** or drag & drop
- Upload: `dist\YouTube Downloader.exe` (the standalone .exe)
- **IMPORTANT**: The filename MUST end with `.exe` for auto-update to work!

### 4. Publish Release
- ✅ Check **"Set as the latest release"**
- Click **"Publish release"**

## 🔄 How Auto-Update Works

### For Users
1. User opens the app
2. App checks GitHub for latest release (on startup)
3. If new version found → Shows update dialog with release notes
4. User clicks "Download & Install Update"
5. App downloads the new .exe
6. App closes, replaces itself, and restarts with new version

### Technical Details
- **Version Check**: Compares `APP_VERSION` with GitHub release tag
- **Download**: Gets `.exe` from GitHub release assets
- **Install**: Batch script replaces old .exe and restarts
- **Works For**: Both portable .exe and installed versions

## 📝 Version Numbering

Use semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR** (2.0.0): Big changes, breaking features
- **MINOR** (2.1.0): New features, improvements
- **PATCH** (2.1.1): Bug fixes, small tweaks

Examples:
- Bug fix: `2.0.0` → `2.0.1`
- New feature: `2.0.1` → `2.1.0`
- Major overhaul: `2.1.0` → `3.0.0`

## ✅ Release Checklist

Before releasing:
- [ ] Update `APP_VERSION` in `config/settings.py`
- [ ] Update `Version=` in `PUBLISHER_INFO.ini` (optional)
- [ ] Test the build locally
- [ ] Run `build_installer.bat`
- [ ] Create GitHub release with tag matching version
- [ ] Upload the `.exe` file
- [ ] Write clear release notes
- [ ] Publish release

## 🎯 Where Files Go

### Portable Mode (.exe only)
- Downloaded to: `%TEMP%\YouTubeDownloader_v2.1.0.exe`
- Installed to: Same location as current .exe
- Settings saved to: Same folder as .exe

### Installed Mode
- Downloaded to: `%TEMP%\YouTubeDownloader_v2.1.0.exe`
- Installed to: `C:\Program Files\YouTube Downloader\`
- Settings saved to: `%APPDATA%\YouTubeDownloader\`

## ⚠️ Important Notes

1. **Always increment version** before building
2. **Tag must match version**: If `APP_VERSION = "2.1.0"`, tag must be `v2.1.0`
3. **Upload the .exe**: Must be in release assets with `.exe` extension
4. **Test before release**: Run the built .exe on a clean PC if possible
5. **Users need internet**: For auto-update to download new version

## 🔧 Troubleshooting

**Update not detected?**
- Check version numbers match (APP_VERSION vs tag)
- Ensure tag starts with `v` (e.g., `v2.1.0`)
- Verify .exe is uploaded to latest release

**Update download fails?**
- Check internet connection
- Verify GitHub release is public
- Check .exe file is accessible

**Update won't install?**
- User might need admin rights (installed mode)
- Antivirus might block update script
- Try updating manually

## 📞 Support

For issues with auto-update:
- Check version in Settings → About
- Manually download from: https://github.com/chandula04/YT-Downloader/releases/latest
- Report bugs: https://github.com/chandula04/YT-Downloader/issues
