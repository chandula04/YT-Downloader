"""
FFmpeg setup utility - Downloads and extracts FFmpeg for Windows
"""

import os
import sys
import zipfile
import requests
from pathlib import Path


def download_ffmpeg():
    """Download FFmpeg for Windows"""
    print("Setting up FFmpeg locally...")
    
    # FFmpeg download URL for Windows (static build)
    ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    
    project_root = Path(__file__).parent
    ffmpeg_dir = project_root / "ffmpeg"
    ffmpeg_zip = ffmpeg_dir / "ffmpeg.zip"
    
    # Create ffmpeg directory if it doesn't exist
    ffmpeg_dir.mkdir(exist_ok=True)
    
    print(f"Downloading FFmpeg to {ffmpeg_zip}...")
    
    try:
        # Download FFmpeg
        response = requests.get(ffmpeg_url, stream=True)
        response.raise_for_status()
        
        with open(ffmpeg_zip, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print("Download completed. Extracting...")
        
        # Extract FFmpeg
        with zipfile.ZipFile(ffmpeg_zip, 'r') as zip_ref:
            zip_ref.extractall(ffmpeg_dir)
        
        # Find the extracted folder
        extracted_folders = [d for d in ffmpeg_dir.iterdir() if d.is_dir() and d.name.startswith('ffmpeg-')]
        
        if extracted_folders:
            extracted_folder = extracted_folders[0]
            bin_folder = extracted_folder / "bin"
            
            if bin_folder.exists():
                # Move ffmpeg.exe to the main ffmpeg directory
                ffmpeg_exe = bin_folder / "ffmpeg.exe"
                if ffmpeg_exe.exists():
                    target_path = ffmpeg_dir / "ffmpeg.exe"
                    if target_path.exists():
                        target_path.unlink()
                    ffmpeg_exe.rename(target_path)
                    print(f"FFmpeg installed successfully at: {target_path}")
                else:
                    print("Error: ffmpeg.exe not found in the extracted files")
                    return False
            else:
                print("Error: bin folder not found in extracted files")
                return False
        else:
            print("Error: Could not find extracted FFmpeg folder")
            return False
        
        # Clean up
        ffmpeg_zip.unlink()
        
        # Remove extracted folder after moving ffmpeg.exe
        import shutil
        for folder in extracted_folders:
            shutil.rmtree(folder)
        
        print("✅ FFmpeg setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error setting up FFmpeg: {e}")
        return False


if __name__ == "__main__":
    success = download_ffmpeg()
    if not success:
        sys.exit(1)