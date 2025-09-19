"""
Quality selector component for choosing download quality
"""

import customtkinter as ctk


class QualitySelector(ctk.CTkFrame):
    """Component for selecting video quality and download options"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self._setup_ui()
        self.quality_options = []
    
    def _setup_ui(self):
        """Set up the UI components"""
        # Quality selection
        self.quality_label = ctk.CTkLabel(
            self, 
            text="Quality:", 
            font=("Arial", 14)
        )
        self.quality_label.pack(anchor="w", pady=(0, 5))
        
        self.quality_combo = ctk.CTkComboBox(
            self, 
            values=[], 
            height=40, 
            font=("Arial", 14)
        )
        self.quality_combo.pack(fill="x", pady=(0, 15))
        
        # Audio option
        self.audio_var = ctk.BooleanVar()
        self.audio_checkbox = ctk.CTkCheckBox(
            self, 
            text="Download as MP3", 
            variable=self.audio_var, 
            font=("Arial", 14), 
            corner_radius=10
        )
        self.audio_checkbox.pack(anchor="w")
    
    def set_quality_options(self, options):
        """
        Set available quality options
        
        Args:
            options (list): List of quality option strings
        """
        self.quality_options = options
        self.quality_combo.configure(values=options)
        
        # Set default selection to highest quality
        if options:
            self.quality_combo.set(options[0])
    
    def get_selected_quality(self):
        """
        Get the currently selected quality
        
        Returns:
            str: Selected quality string
        """
        return self.quality_combo.get()
    
    def is_audio_only(self):
        """
        Check if audio-only download is selected
        
        Returns:
            bool: True if audio-only is selected, False otherwise
        """
        return self.audio_var.get()
    
    def clear_options(self):
        """Clear all quality options"""
        self.quality_options = []
        self.quality_combo.configure(values=[])
        self.quality_combo.set("")
    
    def enable(self):
        """Enable the quality selector components"""
        self.quality_combo.configure(state="normal")
        self.audio_checkbox.configure(state="normal")
    
    def disable(self):
        """Disable the quality selector components"""
        self.quality_combo.configure(state="disabled")
        self.audio_checkbox.configure(state="disabled")