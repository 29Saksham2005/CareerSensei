import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import random
from modules.base_module import BaseModule
from logic.task_manager import get_tasks

class Module(BaseModule):
    def __init__(self, app):
        super().__init__(app)
        self.notification_window = None
        self.check_interval = 60000  # Check every minute
        self.motivational_messages = [
            "🎯 Every small step brings you closer to your goals!",
            "💪 You've got this! Keep pushing forward!",
            "✨ Your future self will thank you for today's efforts!",
            "🚀 Success is built one task at a time!",
            "🌟 Believe in yourself and your abilities!",
            "🎉 Every completed task is a victory!",
            "💫 Stay focused, stay motivated!",
            "🌈 Your dedication will lead to amazing results!",
            "🎯 Small progress is still progress!",
            "💪 Keep going, you're doing great!"
        ]

    def _create_widgets(self):
        # Create notification settings frame
        settings_frame = tk.LabelFrame(
            self.frame,
            text="Notification Settings",
            font=("Helvetica", 12, "bold"),
            fg=self.app.neon_blue,
            bg=self.app.card_bg,
            padx=15,
            pady=15
        )
        settings_frame.pack(fill=tk.X, pady=(0, 20))

        # Reminder settings
        reminder_frame = tk.Frame(settings_frame, bg=self.app.card_bg)
        reminder_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            reminder_frame,
            text="Reminder Settings:",
            font=("Helvetica", 10, "bold"),
            fg=self.app.fg_color,
            bg=self.app.card_bg
        ).pack(anchor=tk.W)

        # Enable/disable reminders
        self.reminder_var = tk.BooleanVar(value=True)
        reminder_check = tk.Checkbutton(
            reminder_frame,
            text="Enable Task Reminders",
            variable=self.reminder_var,
            font=("Helvetica", 10),
            fg=self.app.fg_color,
            bg=self.app.card_bg,
            selectcolor=self.app.secondary_bg,
            activebackground=self.app.card_bg,
            activeforeground=self.app.fg_color
        )
        reminder_check.pack(anchor=tk.W, pady=(5, 0))

        # Reminder time settings
        time_frame = tk.Frame(reminder_frame, bg=self.app.card_bg)
        time_frame.pack(fill=tk.X, pady=(5, 0))

        tk.Label(
            time_frame,
            text="Remind me before deadline:",
            font=("Helvetica", 10),
            fg=self.app.fg_color,
            bg=self.app.card_bg
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.reminder_time = ttk.Combobox(
            time_frame,
            values=["1 hour", "2 hours", "4 hours", "1 day", "2 days"],
            state="readonly",
            width=10
        )
        self.reminder_time.set("1 day")
        self.reminder_time.pack(side=tk.LEFT)

        # Motivational messages settings
        msg_frame = tk.Frame(settings_frame, bg=self.app.card_bg)
        msg_frame.pack(fill=tk.X, pady=(10, 0))

        tk.Label(
            msg_frame,
            text="Motivational Messages:",
            font=("Helvetica", 10, "bold"),
            fg=self.app.fg_color,
            bg=self.app.card_bg
        ).pack(anchor=tk.W)

        # Enable/disable motivational messages
        self.motivation_var = tk.BooleanVar(value=True)
        motivation_check = tk.Checkbutton(
            msg_frame,
            text="Show Daily Motivational Messages",
            variable=self.motivation_var,
            font=("Helvetica", 10),
            fg=self.app.fg_color,
            bg=self.app.card_bg,
            selectcolor=self.app.secondary_bg,
            activebackground=self.app.card_bg,
            activeforeground=self.app.fg_color
        )
        motivation_check.pack(anchor=tk.W, pady=(5, 0))

        # Message frequency settings
        freq_frame = tk.Frame(msg_frame, bg=self.app.card_bg)
        freq_frame.pack(fill=tk.X, pady=(5, 0))

        tk.Label(
            freq_frame,
            text="Show messages every:",
            font=("Helvetica", 10),
            fg=self.app.fg_color,
            bg=self.app.card_bg
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.message_freq = ttk.Combobox(
            freq_frame,
            values=["2 hours", "4 hours", "6 hours", "8 hours", "12 hours"],
            state="readonly",
            width=10
        )
        self.message_freq.set("4 hours")
        self.message_freq.pack(side=tk.LEFT)

        # Save settings button
        save_button = tk.Button(
            settings_frame,
            text="💾 Save Settings",
            command=self.save_settings,
            font=("Helvetica", 10, "bold"),
            bg=self.app.bg_color,
            fg=self.app.neon_blue,
            activebackground=self.app.secondary_bg,
            activeforeground=self.app.neon_blue,
            relief=tk.FLAT,
            padx=20,
            pady=5,
            borderwidth=2,
            highlightthickness=1,
            highlightbackground=self.app.neon_blue,
            highlightcolor=self.app.neon_blue
        )
        save_button.pack(pady=(10, 0))

        # Start notification checks
        self.check_notifications()

    def save_settings(self):
        # Save notification settings
        # This would typically save to a configuration file
        self.show_notification("Settings Saved", "Your notification preferences have been updated! 🎉")

    def check_notifications(self):
        if self.reminder_var.get():
            self.check_task_reminders()
        
        if self.motivation_var.get():
            self.show_motivational_message()
        
        # Schedule next check
        self.frame.after(self.check_interval, self.check_notifications)

    def check_task_reminders(self):
        tasks = get_tasks()
        current_time = datetime.now()
        reminder_time = self.get_reminder_time_delta()

        for goal, goal_tasks in tasks.items():
            for task in goal_tasks:
                if isinstance(task, dict) and not task.get('completed', False):
                    due_date = task.get('due_date')
                    if due_date:
                        try:
                            due = datetime.strptime(due_date, "%Y-%m-%d")
                            time_until_due = due - current_time
                            
                            if timedelta(0) <= time_until_due <= reminder_time:
                                self.show_notification(
                                    "Task Reminder",
                                    f"Task '{task['description']}' is due {self.format_time_until_due(time_until_due)}!"
                                )
                        except ValueError:
                            continue

    def get_reminder_time_delta(self):
        reminder_setting = self.reminder_time.get()
        if reminder_setting == "1 hour":
            return timedelta(hours=1)
        elif reminder_setting == "2 hours":
            return timedelta(hours=2)
        elif reminder_setting == "4 hours":
            return timedelta(hours=4)
        elif reminder_setting == "1 day":
            return timedelta(days=1)
        elif reminder_setting == "2 days":
            return timedelta(days=2)
        return timedelta(days=1)  # Default

    def format_time_until_due(self, time_delta):
        if time_delta.days > 0:
            return f"in {time_delta.days} days"
        hours = time_delta.seconds // 3600
        if hours > 0:
            return f"in {hours} hours"
        minutes = (time_delta.seconds % 3600) // 60
        return f"in {minutes} minutes"

    def show_motivational_message(self):
        message = random.choice(self.motivational_messages)
        self.show_notification("Daily Motivation", message)

    def show_notification(self, title, message):
        if self.notification_window:
            self.notification_window.destroy()

        self.notification_window = tk.Toplevel(self.app.root)
        self.notification_window.title(title)
        self.notification_window.geometry("300x150")
        self.notification_window.configure(bg=self.app.card_bg)
        
        # Make window stay on top
        self.notification_window.attributes('-topmost', True)
        
        # Center the window
        self.notification_window.update_idletasks()
        width = self.notification_window.winfo_width()
        height = self.notification_window.winfo_height()
        x = (self.notification_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.notification_window.winfo_screenheight() // 2) - (height // 2)
        self.notification_window.geometry(f'{width}x{height}+{x}+{y}')

        # Message label
        message_label = tk.Label(
            self.notification_window,
            text=message,
            font=("Helvetica", 10),
            fg=self.app.fg_color,
            bg=self.app.card_bg,
            wraplength=280,
            justify=tk.CENTER
        )
        message_label.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Close button
        close_button = tk.Button(
            self.notification_window,
            text="Close",
            command=self.notification_window.destroy,
            font=("Helvetica", 10, "bold"),
            bg=self.app.bg_color,
            fg=self.app.neon_blue,
            activebackground=self.app.secondary_bg,
            activeforeground=self.app.neon_blue,
            relief=tk.FLAT,
            padx=20,
            pady=5,
            borderwidth=2,
            highlightthickness=1,
            highlightbackground=self.app.neon_blue,
            highlightcolor=self.app.neon_blue
        )
        close_button.pack(pady=(0, 10))

        # Auto-close after 5 seconds
        self.notification_window.after(5000, self.notification_window.destroy) 