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
        self._display_to_raw = {}
    
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
            height=54,  # Taller combobox
            font=("Arial", 16),  # Larger font
            corner_radius=10,
            border_width=1,
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
            corner_radius=4,
            border_width=2,
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
        display_options = [self._format_quality_label(option) for option in options]
        self._display_to_raw = dict(zip(display_options, options))
        self.quality_combo.configure(values=display_options)
        
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
            self.quality_combo.set(self._format_quality_label(preferred))
    
    def get_selected_quality(self):
        """
        Get the currently selected quality
        
        Returns:
            str: Selected quality string
        """
        selected = self.quality_combo.get()
        return self._display_to_raw.get(selected, selected)
    
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
        self._display_to_raw = {}
        self.quality_combo.configure(values=[])
        self.quality_combo.set("")

    def _format_quality_label(self, option):
        """Add emoji to quality label for better clarity."""
        if option.startswith("4320p"):
            return f"🖥️ 8K • {option}"
        if option.startswith("2160p"):
            return f"✨ 4K • {option}"
        if option.startswith("1440p"):
            return f"🎯 2K • {option}"
        if option.startswith("1080p"):
            return f"✅ 1080p • {option}"
        if option.startswith("720p"):
            return f"📺 720p • {option}"
        if option.startswith("480p"):
            return f"📼 480p • {option}"
        if option.startswith("360p"):
            return f"📹 360p • {option}"
        if option.startswith("240p"):
            return f"📱 240p • {option}"
        if option.startswith("144p"):
            return f"📡 144p • {option}"
        return option
    
    def enable(self):
        """Enable the quality selector components"""
        self.quality_combo.configure(state="normal")
        self.audio_checkbox.configure(state="normal")
    
    def disable(self):
        """Disable the quality selector components"""
        self.quality_combo.configure(state="disabled")
        self.audio_checkbox.configure(state="disabled")