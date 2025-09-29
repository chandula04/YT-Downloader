# 🚀 Quick Installation Guide

## For Friends Without Python

### Option 1: Automatic Setup (Recommended)
1. **Download the project folder**
2. **Double-click `setup.bat`** - This will:
   - Check if Python is installed
   - Guide you through Python installation if needed
   - Install all required libraries automatically
   - Set up FFmpeg for video processing

3. **Run the application** with `run.bat`

### Option 2: Manual Setup
1. **Install Python**:
   - Go to [python.org/downloads](https://www.python.org/downloads/)
   - Download Python 3.10 or newer
   - **IMPORTANT**: Check "Add Python to PATH" during installation!

2. **Install libraries**:
   - Open Command Prompt (cmd)
   - Navigate to the project folder
   - Run: `pip install -r requirements.txt`

3. **Run the application**:
   - Double-click `run.bat` or run `python main.py`

## 🔧 Troubleshooting

### Common Issues:

**"Python is not recognized"**
- Python isn't installed or not in PATH
- Run `setup.bat` to fix this

**"No module named 'customtkinter'"**
- Libraries aren't installed
- Run `setup.bat` to install them

**"CTkComboBox error"** 
- CustomTkinter library issue
- Run `setup.bat` to reinstall with correct version

**FFmpeg errors**
- FFmpeg not found
- Run `setup.bat` to download FFmpeg automatically

## 🛠️ Utility Scripts

- **`setup.bat`** - Main setup script (run this first!)
- **`run.bat`** - Start the application (checks dependencies)
- **`check_dependencies.bat`** - Check what's installed
- **`setup_advanced.py`** - Advanced Python setup script

## 📋 Dependencies
- Python 3.10+ 
- customtkinter 5.2.0
- pytubefix 6.0.0
- Pillow (for image processing)
- requests (for web requests)
- FFmpeg (automatically downloaded)

## 🎯 Quick Test
Run `check_dependencies.bat` to verify everything is working!

---
**Need help?** All the batch files will guide you through any issues step by step.