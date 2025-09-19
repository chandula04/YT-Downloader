# Git LFS Setup Guide for YouTube Downloader

## What is Git LFS?

Git LFS (Large File Storage) is a Git extension that helps manage large files (like our 167MB FFmpeg executable) more efficiently. Instead of storing the actual large files in the Git repository, it stores pointers to the files and keeps the actual files on a separate server.

## Current Setup

✅ **Git LFS is configured for:**
- `ffmpeg/*.exe` - FFmpeg executables
- `*.zip` - ZIP archive files  
- `*.7z` - 7-Zip archive files

## How It Works

1. **Large files are tracked by LFS** - The actual FFmpeg file is stored on GitHub's LFS servers
2. **Git stores pointers** - The repository contains small pointer files instead of the full binary
3. **Downloads on demand** - Users get the actual files when they clone or pull
4. **Version control** - All versions of large files are still tracked properly

## For Users Cloning the Repository

### First Time Setup
```bash
# Clone the repository (LFS files download automatically)
git clone https://github.com/chandula04/YT-Downloader.git

# If LFS files didn't download automatically:
git lfs pull
```

### Verify LFS Files
```bash
# Check which files are tracked by LFS
git lfs ls-files

# Should show: ffmpeg/ffmpeg.exe
```

## For Contributors

### Adding New Large Files
```bash
# Track new file types with LFS
git lfs track "*.large-extension"

# Add the .gitattributes changes
git add .gitattributes

# Add your large file
git add path/to/large-file

# Commit and push
git commit -m "Add large file with LFS"
git push origin main
```

### Working with Existing LFS Files
- **Modify LFS files normally** - Git LFS handles the complexity
- **Push/pull as usual** - LFS operations happen automatically
- **Check LFS status** - Use `git lfs status` to see LFS file states

## Troubleshooting

### If FFmpeg is Missing After Clone
```bash
# Download LFS files manually
git lfs pull

# Or run the setup script
python setup_ffmpeg.py
```

### If Push Fails Due to Large Files
```bash
# Check LFS tracking
git lfs track

# Ensure large files are tracked
git lfs track "path/to/large-file"

# Re-add and push
git add .
git commit -m "Fix LFS tracking"
git push origin main
```

### Check LFS Usage
```bash
# See LFS file status
git lfs status

# See LFS file list
git lfs ls-files

# Check LFS configuration
cat .gitattributes
```

## Benefits

✅ **Faster clones** - Initial repository download is much smaller
✅ **Version control** - Large files are still properly versioned  
✅ **Bandwidth efficient** - Only download large files when needed
✅ **No size limits** - GitHub LFS supports very large files
✅ **Automatic handling** - Works transparently with normal Git operations

## Current LFS Configuration

The `.gitattributes` file contains:
```
ffmpeg/*.exe filter=lfs diff=lfs merge=lfs -text
*.zip filter=lfs diff=lfs merge=lfs -text
*.7z filter=lfs diff=lfs merge=lfs -text
```

This ensures that:
- All FFmpeg executables in the `ffmpeg/` folder are tracked by LFS
- Any ZIP or 7-Zip archives are automatically tracked by LFS
- Future large files of these types will be handled properly