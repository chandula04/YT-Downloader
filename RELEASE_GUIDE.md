# 🚀 Complete Release Guide - YouTube Downloader

Comprehensive step-by-step guide to build and release your YouTube Downloader with auto-update.

---

## 📋 Table of Contents
1. [Prerequisites](#-prerequisites)
2. [Building the Application](#-building-the-application)
3. [Testing Before Release](#-testing-before-release)
4. [Creating GitHub Release](#-creating-github-release)
5. [Fixing "Can't Run on PC" Error](#-fixing-cant-run-on-your-pc-error)
6. [Troubleshooting](#-troubleshooting)

---

## 🔧 Prerequisites

### Required Software
- ✅ Python 3.13+ installed
- ✅ Git installed and configured
- ✅ GitHub account with YT-Downloader repository
- ✅ All dependencies installed:
  ```cmd
  pip install -r requirements.txt
  ```

### Optional
- Inno Setup (for creating installer) - [Download here](https://jrsoftware.org/isdl.php)

---

## 🏗️ Building the Application

### Step 1: Update Version Number

**IMPORTANT**: Always increment version before building!

Edit `config/settings.py`:
```python
APP_VERSION = "2.0.0"  # Change this to your new version
```

### Step 2: Run Build Script

Open Command Prompt in project folder and run:
```cmd
build_installer.bat
```

**What it does:**
1. Upgrades PyInstaller
2. Builds standalone `.exe` file
3. Packages all assets (ffmpeg, config, etc.)
4. Creates installer (if Inno Setup installed)

**Build Output:**
- `dist\YouTubeDownloader.exe` - **Use this for release sharing** (single-file portable app)
- `installer\Output\YouTubeDownloaderSetup.exe` - Optional installer

**Build Time**: ~2-5 minutes depending on your PC

---

## 🧪 Testing Before Release

### Checklist - Test Everything!

**Basic Tests:**
- [ ] Double-click `dist\YouTubeDownloader.exe` - app opens
- [ ] Load a video (paste YouTube URL)
- [ ] Preview shows correctly with thumbnail
- [ ] Quality options appear
- [ ] Download a video successfully
- [ ] Downloaded video plays without issues
- [ ] Settings dialog opens and saves
- [ ] Theme switching works (dark/light)
- [ ] Download path can be changed

**Advanced Tests:**
- [ ] Test on a different PC (if possible)
- [ ] Test with antivirus enabled
- [ ] Test playlist download
- [ ] Test audio-only download
- [ ] Test cancel button
- [ ] Check progress tracking works

**Critical**: If any test fails, fix it before releasing!

---

## 📦 Creating GitHub Release

### Step 1: Commit and Push Your Code

```cmd
git add .
git commit -m "Release v2.0.0 - Auto-update system and improvements"
git push origin main
```

### Step 2: Go to GitHub Releases

1. Open browser
2. Navigate to: `https://github.com/chandula04/YT-Downloader/releases`
3. Click **"Draft a new release"** (green button, top-right)

### Step 3: Create Release Tag

1. Click **"Choose a tag"** dropdown
2. Type: `v2.0.0` (MUST match APP_VERSION with 'v' prefix!)
3. Click **"Create new tag: v2.0.0 on publish"**

**Important**: Tag format is `v` + version number
- ✅ Correct: `v2.0.0`, `v2.1.0`, `v3.0.0`
- ❌ Wrong: `2.0.0`, `version-2.0`, `release-2.0.0`

### Step 4: Fill Release Information

**Release Title:**
```
YouTube Downloader v2.0.0
```

**Release Description** (Copy and modify this template):
```markdown
# 🎉 YouTube Downloader v2.0.0

## ✨ New Features

### 🔄 Auto-Update System
- Automatic update checking on startup
- One-click update installation  
- Notification bell with badge count
- Release notes displayed in app

### 🎨 UI Improvements
- Animated footer with CMW SOFTWARE branding
- Modern notification system
- Improved settings dialog
- 60 FPS real-time progress tracking

### 📚 Library Management (Dev Mode Only)
- Automatic library update checking
- Manual update from settings
- PyPI integration for latest versions

### ⚡ Performance
- Video caching for instant download start
- Faster load times
- Optimized progress updates

## 🐛 Bug Fixes
- Fixed download path not updating automatically
- Fixed 404 error when no releases exist
- Fixed progress bar not resetting on cancel
- Improved error handling throughout

## 📥 Installation

### Easy Setup (Recommended)
1. Download `YouTube Downloader.exe` below ⬇️
2. Double-click to run (no installation needed!)
3. Start downloading videos! 🎊

### If You Get "Windows Protected" Warning
1. Click **"More info"**
2. Click **"Run anyway"**
3. This is normal for new executables

## 🔄 Updating from v1.0.0

If you have v1.0.0:
- The app will automatically detect this update
- Notification bell will show (🔔 1)
- Click it and update with one button!

## 💡 System Requirements

- ✅ Windows 10/11 (64-bit or 32-bit)
- ✅ Internet connection
- ✅ ~35 MB disk space
- ✅ No Python, pip, FFmpeg, or separate Node.js installation needed

## 🆘 Troubleshooting

**"This app can't run on your PC"?**
- You might have wrong version (32-bit vs 64-bit)
- Download the correct version for your Windows

**Download not working?**
- Check internet connection
- Make sure download path exists
- Try running as administrator

**More help:** [README.md](https://github.com/chandula04/YT-Downloader#readme)

---

**Full Changelog**: [v1.0.0...v2.0.0](https://github.com/chandula04/YT-Downloader/compare/v1.0.0...v2.0.0)
```

### Step 5: Upload the Executable

1. Scroll down to **"Attach binaries by dropping them here or selecting them"**
2. **Drag and drop** `dist\YouTubeDownloader.exe` OR click to browse
3. Wait for upload to complete (you'll see progress bar)
4. Confirm file appears with green checkmark ✅

**CRITICAL**: The filename MUST end with `.exe` for auto-update to work!

### Step 6: Configure Release Settings

- ✅ Check **"Set as the latest release"**
- ⬜ Leave **"Set as a pre-release"** UNCHECKED (unless testing)
- ⬜ **"Create a discussion"** - Optional

### Step 7: Publish!

Click **"Publish release"** (green button at bottom)

🎉 **Congratulations! Your release is live!**

### Step 8: Verify Release

1. Go to: `https://github.com/chandula04/YT-Downloader/releases/latest`
2. Confirm:
   - ✅ Release title and tag are correct
   - ✅ Description looks good
   - ✅ .exe file is attached and downloadable
   - ✅ Share only `YouTubeDownloader.exe` for plug-and-play use

---

## 🛠️ Fixing "Can't Run on Your PC" Error

### What Does This Error Mean?

When your friend sees **"This app can't run on your PC"**, it means:
- ❌ Architecture mismatch (32-bit vs 64-bit)
- ❌ Missing dependencies (rare with PyInstaller)
- ❌ Corrupted download

### Check Windows Architecture

**Your Friend Should Check Their Windows Type:**

1. Right-click **"This PC"** on desktop
2. Click **"Properties"**
3. Look at **"System type"**:
   - **"64-bit operating system"** = Needs 64-bit exe ✅ (99% of users)
   - **"32-bit operating system"** = Needs 32-bit exe ⚠️ (rare)

### Solution 1: Build for Correct Architecture

**PyInstaller builds for YOUR system:**
- If you have 64-bit Windows → creates 64-bit exe
- If you have 32-bit Windows → creates 32-bit exe

**Most Common Setup:**
- You build on 64-bit Windows
- Most users have 64-bit Windows  
- Everyone is happy! ✅

**Problem:**
- You build on 64-bit Windows
- Friend has old 32-bit Windows
- Error appears ❌

### Solution 2: Create Both Versions (Advanced)

**For Maximum Compatibility:**

1. **Build 64-bit Version** (on 64-bit Windows):
   ```cmd
   build_installer.bat
   move "dist\YouTubeDownloader.exe" "dist\YouTubeDownloader_x64.exe"
   ```

2. **Build 32-bit Version** (on 32-bit Windows OR use 32-bit Python):
   ```cmd
   build_installer.bat
   move "dist\YouTubeDownloader.exe" "dist\YouTubeDownloader_x86.exe"
   ```

3. **Upload BOTH to GitHub Release**

4. **Update Release Description:**
   ```markdown
   ## 📥 Downloads
   
   Choose the right version for your Windows:
   
   - 🔷 **YouTube Downloader_x64.exe** - For Windows 10/11 (64-bit) ⬇️ **[RECOMMENDED - 99% of users]**
   - 🔶 **YouTube Downloader_x86.exe** - For older Windows (32-bit) ⬇️ [Rare]
   
   **Not sure which one?** Download x64 version - it works for almost everyone!
   
   **How to check:** Right-click "This PC" → Properties → See "System type"
   ```

### Solution 3: Quick Fixes

**If rebuilding isn't an option:**

1. **Install Visual C++ Redistributable:**
   - Download: [VC++ 2015-2022 (x64)](https://aka.ms/vs/17/release/vc_redist.x64.exe)
   - Install it
   - Try running exe again

2. **Run as Administrator:**
   - Right-click exe
   - "Run as administrator"

3. **Disable Antivirus Temporarily:**
   - Some antivirus blocks new executables
   - Whitelist your app

4. **Re-download:**
   - File might be corrupted
   - Download fresh copy from GitHub

### How to Know Which Version You Built

**Check YOUR Windows:**
```cmd
systeminfo | findstr /C:"System Type"
```

**Output:**
- `x64-based PC` = You built 64-bit exe
- `x86-based PC` = You built 32-bit exe

---

## 🔄 How Auto-Update Works

### User Experience

1. **User opens app**
2. **App checks GitHub** (in background, on startup)
3. **New version found**:
   - Notification bell shows badge: 🔔 1
   - Click bell to see update details
4. **User clicks "Update Now"**:
   - App downloads new exe
   - Shows progress bar
   - Installs automatically
5. **App restarts** with new version! ✨

### Technical Details

**Version Check:**
- Compares `APP_VERSION` with GitHub release tag
- Uses GitHub API: `/repos/chandula04/YT-Downloader/releases/latest`

**Download Process:**
- Downloads from release assets
- Shows real-time progress
- Saves to temp folder

**Installation:**
- Creates batch script
- Closes current app
- Replaces old exe with new one
- Launches new version
- Deletes batch script

### Requirements for Auto-Update to Work

- ✅ GitHub release is published (not draft)
- ✅ Tag matches version format (`v2.0.0`)
- ✅ .exe file is attached to release
- ✅ User has internet connection
- ✅ No antivirus blocking download

---

## 📝 Version Numbering Guide

Follow **[Semantic Versioning](https://semver.org/)**:

```
MAJOR.MINOR.PATCH
  │     │      │
  │     │      └─── Bug fixes only (2.0.0 → 2.0.1)
  │     └────────── New features, backwards compatible (2.0.1 → 2.1.0)
  └──────────────── Breaking changes, major rewrite (2.1.0 → 3.0.0)
```

**Examples:**

| Change Type | Old Version | New Version | Description |
|------------|-------------|-------------|-------------|
| Bug fix | 2.0.0 | 2.0.1 | Fixed crash on cancel |
| Small feature | 2.0.1 | 2.1.0 | Added playlist support |
| New feature | 2.1.0 | 2.2.0 | Added auto-update |
| Major rewrite | 2.2.0 | 3.0.0 | Complete UI redesign |

---

## ✅ Pre-Release Checklist

Before each release, verify:

- [ ] Version number updated in `config/settings.py`
- [ ] All features tested thoroughly
- [ ] No errors in console
- [ ] README.md updated (if needed)
- [ ] All code committed to Git
- [ ] Build completed successfully
- [ ] Executable tested on your PC
- [ ] Executable tested on different PC (if possible)
- [ ] File size is reasonable for the Python, yt-dlp, and FFmpeg self-contained build
- [ ] GitHub release tag matches version
- [ ] Release notes written clearly
- [ ] .exe uploaded to release
- [ ] Release published (not draft)
- [ ] Download link tested

---

## 🔧 Troubleshooting

### Build Issues

**❌ PyInstaller not found**
```cmd
pip install --upgrade pyinstaller
```

**❌ Build fails with errors**
```cmd
# Clean previous builds
rmdir /s /q build dist
del *.spec

# Try again
build_installer.bat
```

**❌ "Module not found" errors**
```cmd
# Reinstall all dependencies
pip install --upgrade -r requirements.txt
```

### Release Issues

**❌ Auto-update not detecting new version**

Check:
1. Tag format: Must be `v2.0.0` (with 'v')
2. Release is published (not draft)
3. Tag matches `APP_VERSION`
4. Release is marked as "latest"

**❌ Download link broken**

- Ensure .exe is uploaded to release assets
- Check file uploaded completely (full size)
- Verify public repository access

**❌ Update downloads but won't install**

- User might need admin rights
- Antivirus might be blocking
- Try disabling Windows Defender temporarily

### Runtime Issues

**❌ App crashes on startup**
```cmd
# Run from terminal to see errors
cd dist
"YouTube Downloader.exe"
```

**❌ Missing FFmpeg**
- Ensure `--add-data "ffmpeg;ffmpeg"` in build command
- Check ffmpeg folder exists in dist

**❌ "No module named 'config'"**
- Ensure `--add-data "config;config"` in build command
- Check config folder exists in dist

---

## 💡 Pro Tips

1. **Always test before releasing** - Save yourself embarrassment!

2. **Keep old versions** - In case you need to rollback

3. **Version incrementally** - Don't jump from 1.0.0 to 5.0.0

4. **Write good release notes** - Users appreciate knowing what changed

5. **Backup before building** - In case something goes wrong

6. **Test on multiple PCs** - Catch compatibility issues early

7. **Monitor user feedback** - Fix issues in next release

8. **Don't release on Friday** - No one to fix issues over weekend!

---

## 🎯 Quick Reference Commands

```cmd
# Build application
build_installer.bat

# Check Python version
python --version

# Install dependencies
pip install -r requirements.txt

# Update PyInstaller
pip install --upgrade pyinstaller

# Clean build files
rmdir /s /q build dist
del *.spec

# Push to GitHub
git add .
git commit -m "Release v2.0.0"
git push origin main

# Check Windows architecture
systeminfo | findstr /C:"System Type"
```

---

## 📞 Need Help?

- **GitHub Issues**: [Open an issue](https://github.com/chandula04/YT-Downloader/issues)
- **README**: Check [README.md](README.md) for general help
- **Previous Releases**: Review successful releases as examples

---

## 🎉 Congratulations!

You now know how to:
- ✅ Build standalone executables
- ✅ Create GitHub releases
- ✅ Fix compatibility issues
- ✅ Enable auto-updates
- ✅ Support your users

**Happy releasing!** 🚀

---

*Last updated: February 1, 2026*
*YouTube Downloader v2.0.0*
*Created by CMW SOFTWARE*


📝 Important Understanding:
❌ NEVER commit to Git:
build/ folder (temporary build files)
dist/ folder (your .exe file)
*.spec files (PyInstaller config)