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
        # Quality selection with more prominent styling
        self.quality_label = ctk.CTkLabel(
            self, 
            text="Quality:", 
            font=("Arial", 18, "bold")  # Larger, bold font
        )
        self.quality_label.pack(anchor="w", pady=(0, 10))  # More spacing
        
        self.quality_combo = ctk.CTkComboBox(
            self, 
            values=[], 
            height=50,  # Taller combobox
            font=("Arial", 16),  # Larger font
            corner_radius=10,
            button_color="#4CAF50",  # Green button
            button_hover_color="#45a049"
        )
        self.quality_combo.pack(fill="x", pady=(0, 25))  # More spacing
        
        # Audio option with better styling
        self.audio_var = ctk.BooleanVar()
        self.audio_checkbox = ctk.CTkCheckBox(
            self, 
            text="Download as MP3 (Audio Only)", 
            variable=self.audio_var, 
            font=("Arial", 16, "bold"),  # Larger, bold font
            corner_radius=12,
            checkbox_width=24,  # Larger checkbox
            checkbox_height=24
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
        
        if options:
            preferred = None
            targets = ["1080p", "2160p", "1440p", "720p"]
            for target in targets:
                for option in options:
                    if option.startswith(target):
                        preferred = option
                        break
                if preferred:
                    break
            if not preferred:
                preferred = options[0]
            self.quality_combo.set(preferred)
    
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