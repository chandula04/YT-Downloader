"""
File management utilities for download paths and file operations
"""

import os
from tkinter import filedialog


class FileManager:
    """Manages file operations and download paths"""
    
    def __init__(self):
        self._download_path = ""
    
    def set_download_path(self, path=None):
        """
        Set the download path, either from parameter or user selection
        
        Args:
            path (str, optional): Path to set. If None, opens file dialog
            
        Returns:
            bool: True if path was set successfully, False otherwise
        """
        if path:
            self._download_path = path
            return True
        else:
            folder = filedialog.askdirectory()
            if folder:
                self._download_path = folder
                return True
            return False
    
    def set_download_path_direct(self, path):
        """
        Set the download path directly without dialog
        
        Args:
            path (str): Path to set
        """
        self._download_path = path
    
    def get_download_path(self):
        """
        Get the current download path
        
        Returns:
            str: Current download path
        """
        return self._download_path
    
    def has_download_path(self):
        """
        Check if download path is set
        
        Returns:
            bool: True if download path is set, False otherwise
        """
        return bool(self._download_path)
    
    def create_output_path(self, filename):
        """
        Create full output path for a file
        
        Args:
            filename (str): Name of the file
            
        Returns:
            str: Full path to output file
        """
        return os.path.join(self._download_path, filename)
    
    def ensure_path_exists(self, path):
        """
        Ensure that the directory for the given path exists
        
        Args:
            path (str): File path
        """
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)


# Global file manager instance
file_manager = FileManager()