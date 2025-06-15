import tkinter as tk
from tkinter import messagebox, ttk
import importlib
import threading
from datetime import datetime
import sys
import os

# Add the modules directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

class CareerSensei:
    def __init__(self, root):
        self.root = root
        self.root.title("Career Sensei")
        self.goal = None
        self.modules = {}
        self.active_module = None
        
        # Configure cyberpunk theme colors
        self.bg_color = "#0A0A0A"
        self.secondary_bg = "#1A1A1A"
        self.fg_color = "#FFFFFF"
        self.neon_green = "#00FF41"
        self.neon_pink = "#FF00FF"
        self.neon_blue = "#00FFFF"
        self.neon_yellow = "#FFFF00"
        self.card_bg = "#1E1E1E"
        self.highlight_bg = "#2A2A2A"
        self.accent_purple = "#B026FF"
        self.accent_orange = "#FF6B00"
        
        # Configure root window
        self.root.configure(bg=self.bg_color)
        self.root.geometry("1200x800")
        
        # Create main container
        self.main_container = tk.Frame(root, bg=self.bg_color, padx=20, pady=20)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create dashboard frame
        self.dashboard_frame = tk.Frame(self.main_container, bg=self.bg_color)
        self.dashboard_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title_label = tk.Label(
            self.dashboard_frame,
            text="Career Sensei",
            font=("Helvetica", 24, "bold"),
            fg=self.accent_purple,
            bg=self.bg_color
        )
        title_label.pack(side=tk.LEFT)
        
        # Navigation buttons
        nav_frame = tk.Frame(self.dashboard_frame, bg=self.bg_color)
        nav_frame.pack(side=tk.RIGHT)
        
        self.create_nav_button(nav_frame, "🎯 Goals", lambda: self.load_module('goals'), self.neon_green)
        self.create_nav_button(nav_frame, "🤖 AI Suggestions", lambda: self.load_module('ai_suggestions'), self.neon_pink)
        self.create_nav_button(nav_frame, "📊 Analytics", lambda: self.load_module('analytics'), self.neon_yellow)
        self.create_nav_button(nav_frame, "🔔 Notifications", lambda: self.load_module('notification'), self.accent_orange)
        
        # Progress indicator
        self.progress_label = tk.Label(
            self.dashboard_frame,
            text="🎯 Ready to help you achieve your goals!",
            font=("Helvetica", 10),
            fg=self.fg_color,
            bg=self.bg_color
        )
        self.progress_label.pack(side=tk.RIGHT, padx=20)
        
        # Create content frame
        self.content_frame = tk.Frame(self.main_container, bg=self.bg_color)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Load core module (goals) by default
        self.load_module('goals')

    def create_nav_button(self, parent, text, command, color):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Helvetica", 10, "bold"),
            bg=self.bg_color,
            fg=color,
            activebackground=self.secondary_bg,
            activeforeground=color,
            relief=tk.FLAT,
            padx=15,
            pady=5,
            borderwidth=2,
            highlightthickness=1,
            highlightbackground=color,
            highlightcolor=color
        )
        btn.pack(side=tk.LEFT, padx=5)
        return btn

    def load_module(self, module_name):
        try:
            # Unload current module if exists
            if self.active_module:
                self.modules[self.active_module].unload()
            
            # Load new module if not already loaded
            if module_name not in self.modules:
                # Import module dynamically
                module = importlib.import_module(f'{module_name}_module', package='modules')
                # Initialize module with app context
                self.modules[module_name] = module.Module(self)
            
            # Show the module's content
            self.modules[module_name].show()
            self.active_module = module_name
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load {module_name} module: {str(e)}")

    def update_progress(self):
        if hasattr(self, 'modules') and 'goals' in self.modules:
            self.modules['goals'].update_progress()

if __name__ == "__main__":
    root = tk.Tk()
    app = CareerSensei(root)
    
    # Set up window closing protocol
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
