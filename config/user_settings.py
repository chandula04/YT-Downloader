"""
User settings management with local storage
"""

import json
import os
from pathlib import Path


class UserSettings:
    """Manages user settings with local storage per machine"""
    
    def __init__(self):
        # Create settings directory in user's local app data
        self.settings_dir = Path.home() / ".youtube_downloader"
        self.settings_file = self.settings_dir / "settings.json"
        
        # Create directory if it doesn't exist
        self.settings_dir.mkdir(exist_ok=True)
        
        # Default settings
        self.default_settings = {
            "theme": "dark",  # dark or light
            "download_path": str(Path.home() / "Downloads" / "YouTube"),
            "window_geometry": "1400x800",
            "auto_create_download_folder": True
        }
        
        # Load or create settings
        self.settings = self._load_settings()
    
    def _load_settings(self):
        """Load settings from file or create with defaults"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                # Merge with defaults to ensure all keys exist
                merged_settings = self.default_settings.copy()
                merged_settings.update(settings)
                return merged_settings
            else:
                # Create new settings file with defaults
                self._save_settings(self.default_settings)
                return self.default_settings.copy()
        except Exception:
            # If any error occurs, return defaults
            return self.default_settings.copy()
    
    def _save_settings(self, settings=None):
        """Save settings to file"""
        try:
            settings_to_save = settings or self.settings
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings_to_save, f, indent=2, ensure_ascii=False)
        except Exception:
            pass  # Fail silently if can't save
    
    def get(self, key, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set a setting value and save"""
        self.settings[key] = value
        self._save_settings()
    
    def get_theme(self):
        """Get current theme"""
        return self.get("theme", "dark")
    
    def set_theme(self, theme):
        """Set theme (dark or light)"""
        if theme in ["dark", "light"]:
            self.set("theme", theme)
    
    def get_download_path(self):
        """Get download path"""
        return self.get("download_path", str(Path.home() / "Downloads" / "YouTube"))
    
    def set_download_path(self, path):
        """Set download path"""
        self.set("download_path", str(path))
    
    def ensure_download_path_exists(self):
        """Create download path if it doesn't exist"""
        try:
            download_path = Path(self.get_download_path())
            download_path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False


# Global settings instance
user_settings = UserSettings()