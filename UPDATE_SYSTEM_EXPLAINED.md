# How Auto-Update Works for Users

## 🚀 **For Portable .exe Users (Recommended)**

### What Happens When You Update:

1. **You click "Download & Install Update"**
2. **New version downloads** to your temp folder
3. **App creates update script** that will:
   - Wait for current app to close
   - **Backup your old .exe** (renamed to `YouTube Downloader.exe.backup`)
   - **Replace old .exe with new .exe** (same location, same filename)
   - Start the new version automatically
   - Clean up temp files

### Result:
✅ **Same location** - App stays where it is  
✅ **Same name** - `YouTube Downloader.exe`  
✅ **Settings preserved** - All your settings remain  
✅ **Old version backed up** - As `.backup` in case you need it  
✅ **No duplicates** - Only one app file  

### Example:
```
Before Update:
📁 D:\My Apps\
  └─ YouTube Downloader.exe  (v2.0.0)

During Update:
📁 D:\My Apps\
  ├─ YouTube Downloader.exe.backup  (v2.0.0 - backup)
  └─ YouTube Downloader.exe  (v2.1.0 - new!)

After Update:
📁 D:\My Apps\
  ├─ YouTube Downloader.exe.backup  (optional - can delete)
  └─ YouTube Downloader.exe  (v2.1.0 - running!)
```

---

## 🏢 **For Installed Version Users (Inno Setup)**

### What Happens When You Update:

1. **Download the new installer** from GitHub releases
2. **Run the installer**
3. **Installer detects existing version** and offers to:
   - Uninstall old version (recommended)
   - Install alongside (creates new folder)
4. **Settings are preserved** in AppData

### Recommended: Use Portable
The **portable .exe** is simpler for updates because:
- ✅ One-click update (no installer needed)
- ✅ Automatic replacement
- ✅ Faster download (smaller file)
- ✅ Works from anywhere (USB drive, Desktop, Downloads)

---

## 📋 **What Gets Preserved During Updates**

### ✅ Kept (No matter what):
- Download path setting
- Theme preference (Dark/Light)
- Window size and position
- Downloaded videos (in your download folder)
- Library versions (pytubefix, yt-dlp)

### 🔄 Updated:
- Application code (bug fixes, new features)
- UI improvements
- Performance enhancements

---

## 🔔 **Auto-Check on Startup**

### What Happens When You Open the App:

1. **App checks GitHub** for new releases (takes ~1-2 seconds)
2. **App checks PyPI** for library updates (pytubefix, yt-dlp)
3. **Notification badge shows count** if updates available
4. **Click 🔔 bell** to see:
   - App version (current vs available)
   - Library updates (if any)
   - One-click update buttons

### Real-Time Updates:
- ✅ Checks run in background (doesn't slow startup)
- ✅ Notification updates immediately when check completes
- ✅ No manual refresh needed

---

## 🛡️ **Safety Features**

### Backup System:
- Old .exe backed up before replacement
- If update fails, you can:
  1. Delete new .exe
  2. Rename `.backup` to remove the extension
  3. Continue using old version

### Rollback:
```batch
# If something goes wrong, manually rollback:
1. Delete: YouTube Downloader.exe
2. Rename: YouTube Downloader.exe.backup → YouTube Downloader.exe
```

---

## 💡 **Best Practice Recommendations**

### For You (Developer):
1. **Always use portable .exe** for releases
2. **Test updates** before publishing to GitHub
3. **Write clear release notes** (users see these!)
4. **Increment version properly**: 2.0.0 → 2.1.0 → 3.0.0
5. **Keep releases on GitHub** (free hosting, automatic updates work)

### For Your Users:
1. **Use portable .exe** (not installer) for easier updates
2. **Keep app in a permanent location** (not Downloads folder)
3. **Don't delete .backup** until you verify new version works
4. **Check notification bell** occasionally for updates

---

## 🎯 **Summary: Portable vs Installer**

| Feature | Portable .exe | Installer (Inno Setup) |
|---------|---------------|------------------------|
| Auto-update | ✅ One-click | ❌ Manual download needed |
| File size | 🟢 ~50-80 MB | 🟡 ~80-120 MB |
| Installation | ✅ Just run | 🟡 Install wizard |
| Updates | ✅ Automatic in-place | 🟡 Download + Run installer |
| Portability | ✅ Run from anywhere | ❌ Tied to install location |
| Uninstall | ✅ Just delete | 🟡 Need uninstaller |
| Recommended | ✅✅✅ YES | 🟡 Optional |

---

## 🚀 **Recommendation**

**Release the portable .exe** for these reasons:
1. Users get automatic updates
2. Simpler for everyone
3. Smaller download
4. More flexible (USB drive, any folder)
5. Your update system is built for this!

The installer is nice for "professional" feel, but the portable .exe with auto-update is actually **more user-friendly**! 🎉
