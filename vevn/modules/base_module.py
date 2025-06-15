import tkinter as tk

class BaseModule:
    def __init__(self, app):
        self.app = app
        self.frame = None
        self.initialized = False
        
    def initialize(self):
        """Initialize the module's UI and data"""
        if not self.initialized:
            self.frame = tk.Frame(self.app.content_frame, bg=self.app.bg_color)
            self._create_widgets()
            self.initialized = True
            
    def _create_widgets(self):
        """Create the module's widgets - to be implemented by subclasses"""
        pass
        
    def show(self):
        """Show the module's content"""
        self.initialize()
        self.frame.pack(fill=tk.BOTH, expand=True)
        
    def unload(self):
        """Unload the module's content"""
        if self.frame:
            self.frame.pack_forget()
            
    def refresh(self):
        """Refresh the module's data - to be implemented by subclasses"""
        pass 