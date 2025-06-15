import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
from logic.task_manager import get_tasks
from modules.base_module import BaseModule
from tkcalendar import Calendar

class Module(BaseModule):
    def _create_widgets(self):
        # Configure ttk styles for themed widgets
        style = ttk.Style()
        style.theme_use('clam') # Use a theme that allows background customization
        style.configure("TNotebook", background=self.app.bg_color, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.app.secondary_bg, foreground=self.app.fg_color, padding=[10, 5])
        style.map("TNotebook.Tab", 
                 background=[('selected', self.app.card_bg)], 
                 foreground=[('selected', self.app.fg_color)])
        style.configure("TFrame", background=self.app.card_bg)
        style.configure("TCombobox", 
                       fieldbackground=self.app.secondary_bg,
                       background=self.app.secondary_bg,
                       foreground=self.app.fg_color,
                       arrowcolor=self.app.neon_blue)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tabs (using ttk.Frame for theming)
        self.progress_tab = ttk.Frame(self.notebook)
        self.weekly_tab = ttk.Frame(self.notebook)
        self.monthly_tab = ttk.Frame(self.notebook)
        self.goals_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.progress_tab, text="Progress Overview")
        self.notebook.add(self.weekly_tab, text="Weekly Analysis")
        self.notebook.add(self.monthly_tab, text="Monthly Analysis")
        self.notebook.add(self.goals_tab, text="Goals Analysis")

        # Setup each tab
        self.setup_progress_overview()
        self.setup_weekly_overview()
        self.setup_monthly_overview()
        self.setup_goals_analysis()

        # Add refresh button
        refresh_button = tk.Button(
            self.frame,
            text="🔄 Refresh Analytics",
            command=self.refresh_analytics,
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
        refresh_button.pack(pady=10)

        # Start real-time updates
        self.schedule_updates()

    def schedule_updates(self):
        """Schedule periodic updates of the analytics"""
        self.refresh_analytics()
        # Update every 5 seconds
        self.frame.after(5000, self.schedule_updates)

    def setup_progress_overview(self):
        frame = tk.Frame(self.progress_tab, bg=self.app.card_bg)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a frame for the calendar and charts
        top_frame = tk.Frame(frame, bg=self.app.card_bg)
        top_frame.pack(fill=tk.X, pady=(0, 10))

        # Add calendar widget
        cal_frame = tk.Frame(top_frame, bg=self.app.card_bg)
        cal_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        self.calendar = Calendar(
            cal_frame,
            selectmode='day',
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day,
            background=self.app.card_bg,
            foreground=self.app.fg_color,
            selectbackground=self.app.neon_blue,
            selectforeground=self.app.fg_color,
            normalbackground=self.app.secondary_bg,
            normalforeground=self.app.fg_color,
            weekendbackground=self.app.secondary_bg,
            weekendforeground=self.app.fg_color,
            othermonthbackground=self.app.bg_color,
            othermonthforeground=self.app.fg_color,
            bordercolor=self.app.neon_blue,
            headersbackground=self.app.card_bg,
            headersforeground=self.app.fg_color
        )
        self.calendar.pack(padx=5, pady=5)
        self.calendar.bind('<<CalendarSelected>>', self.on_date_selected)

        # Goal selector with scrollbar
        goals_frame = tk.Frame(frame, bg=self.app.card_bg)
        goals_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            goals_frame,
            text="Select Goal:",
            font=("Helvetica", 10),
            bg=self.app.card_bg,
            fg=self.app.fg_color
        ).pack(side=tk.LEFT, padx=(0, 10))

        # Create a frame for combobox and scrollbar
        combo_frame = tk.Frame(goals_frame, bg=self.app.card_bg)
        combo_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.goal_selector = ttk.Combobox(
            combo_frame,
            values=["All Goals"] + list(get_tasks().keys()),
            state="readonly",
            width=30
        )
        self.goal_selector.set("All Goals")
        self.goal_selector.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.goal_selector.bind('<<ComboboxSelected>>', lambda e: self.refresh_analytics())

        # Create a fixed-size frame for the goal completion chart
        chart_frame = tk.Frame(frame, bg=self.app.card_bg, width=600, height=300)
        chart_frame.pack(fill=tk.X, pady=(0, 10))
        chart_frame.pack_propagate(False)  # Prevent frame from shrinking

        # Goal completion chart
        fig1, ax1 = plt.subplots(figsize=(6, 3))
        canvas1 = FigureCanvasTkAgg(fig1, master=chart_frame)
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.goal_completion_chart = (fig1, ax1, canvas1)

    def on_date_selected(self, event=None):
        selected_date = self.calendar.get_date()
        # Update charts to show data for the selected date
        self.refresh_analytics()

    def setup_weekly_overview(self):
        frame = tk.Frame(self.weekly_tab, bg=self.app.card_bg)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        fig, ax = plt.subplots(figsize=(6, 4))
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.weekly_chart = (fig, ax, canvas)

    def setup_monthly_overview(self):
        frame = tk.Frame(self.monthly_tab, bg=self.app.card_bg)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        fig, ax = plt.subplots(figsize=(6, 4))
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.monthly_chart = (fig, ax, canvas)

    def setup_goals_analysis(self):
        frame = tk.Frame(self.goals_tab, bg=self.app.card_bg)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Goals progress list
        self.goals_list = tk.Listbox(
            frame,
            width=50,
            height=10,
            font=("Helvetica", 10),
            bg=self.app.secondary_bg,
            fg=self.app.fg_color,
            selectbackground=self.app.neon_blue,
            selectforeground=self.app.fg_color,
            borderwidth=0, # Remove default border
            highlightthickness=0 # Remove highlight border
        )
        self.goals_list.pack(fill=tk.BOTH, expand=True, pady=10)

    def refresh_analytics(self):
        # Update goal selector values
        current_tasks = get_tasks()
        self.goal_selector['values'] = ["All Goals"] + list(current_tasks.keys())
        
        # Update all charts
        self.update_goal_completion_chart()
        self.update_weekly_chart()
        self.update_monthly_chart()
        self.update_goals_analysis()

    def update_goal_completion_chart(self):
        fig, ax, canvas = self.goal_completion_chart
        ax.clear()
        
        tasks = get_tasks()
        selected_goal = self.goal_selector.get()
        
        if selected_goal == "All Goals":
            goals = list(tasks.keys())
            completion_rates = []
            
            for goal in goals:
                goal_tasks = tasks[goal]
                completed = sum(1 for task in goal_tasks if isinstance(task, dict) and task.get('completed', False))
                total = len(goal_tasks)
                rate = (completed / total * 100) if total > 0 else 0
                completion_rates.append(rate)
            
            ax.bar(goals, completion_rates, color=self.app.neon_green)
        else:
            goal_tasks = tasks[selected_goal]
            completed = sum(1 for task in goal_tasks if isinstance(task, dict) and task.get('completed', False))
            total = len(goal_tasks)
            rate = (completed / total * 100) if total > 0 else 0
            
            ax.bar([selected_goal], [rate], color=self.app.neon_green)
        
        ax.set_title('Goal Completion Rates', color=self.app.fg_color)
        ax.set_ylabel('Completion Rate (%)', color=self.app.fg_color)
        ax.set_xlabel('Goal', color=self.app.fg_color)
        ax.tick_params(axis='x', colors=self.app.fg_color, rotation=45)
        ax.tick_params(axis='y', colors=self.app.fg_color)
        ax.set_facecolor(self.app.card_bg)
        fig.patch.set_facecolor(self.app.card_bg)
        ax.spines['bottom'].set_color(self.app.fg_color)
        ax.spines['left'].set_color(self.app.fg_color)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_ylim(0, 100)
        
        # Adjust layout to prevent label cutoff
        fig.tight_layout()
        
        # Ensure the chart stays within its frame
        canvas.draw()

    def update_weekly_chart(self):
        fig, ax, canvas = self.weekly_chart
        ax.clear()
        
        tasks = get_tasks()
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        days = [(week_start + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
        
        completions = [0] * 7
        for goal_tasks in tasks.values():
            for task in goal_tasks:
                if isinstance(task, dict) and task.get('completed', False):
                    completion_date = task.get('completion_date')
                    if completion_date in days:
                        completions[days.index(completion_date)] += 1
        
        ax.bar(days, completions, color=self.app.neon_pink)
        ax.set_title('Weekly Task Completion', color=self.app.fg_color)
        ax.set_xlabel('Date', color=self.app.fg_color)
        ax.set_ylabel('Tasks Completed', color=self.app.fg_color)
        ax.tick_params(axis='x', colors=self.app.fg_color, rotation=45)
        ax.tick_params(axis='y', colors=self.app.fg_color)
        ax.set_facecolor(self.app.card_bg) # Set plot background
        fig.patch.set_facecolor(self.app.card_bg) # Set figure background
        ax.spines['bottom'].set_color(self.app.fg_color)
        ax.spines['left'].set_color(self.app.fg_color)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        fig.tight_layout()
        canvas.draw()

    def update_monthly_chart(self):
        fig, ax, canvas = self.monthly_chart
        ax.clear()
        
        tasks = get_tasks()
        today = datetime.now()
        month_start = today.replace(day=1)
        days = [(month_start + timedelta(days=i)).strftime('%Y-%m-%d') 
                for i in range((today - month_start).days + 1)]
        
        completions = [0] * len(days)
        for goal_tasks in tasks.values():
            for task in goal_tasks:
                if isinstance(task, dict) and task.get('completed', False):
                    completion_date = task.get('completion_date')
                    if completion_date in days:
                        completions[days.index(completion_date)] += 1
        
        ax.plot(days, completions, marker='o', color=self.app.neon_green)
        ax.set_title('Monthly Task Completion', color=self.app.fg_color)
        ax.set_xlabel('Date', color=self.app.fg_color)
        ax.set_ylabel('Tasks Completed', color=self.app.fg_color)
        ax.tick_params(axis='x', colors=self.app.fg_color, rotation=45)
        ax.tick_params(axis='y', colors=self.app.fg_color)
        ax.set_facecolor(self.app.card_bg) # Set plot background
        fig.patch.set_facecolor(self.app.card_bg) # Set figure background
        ax.spines['bottom'].set_color(self.app.fg_color)
        ax.spines['left'].set_color(self.app.fg_color)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        fig.tight_layout()
        canvas.draw()

    def update_goals_analysis(self):
        self.goals_list.delete(0, tk.END)
        
        tasks = get_tasks()
        for goal, goal_tasks in tasks.items():
            completed = sum(1 for task in goal_tasks if isinstance(task, dict) and task.get('completed', False))
            total = len(goal_tasks)
            progress = (completed / total * 100) if total > 0 else 0
            
            self.goals_list.insert(tk.END, f"🎯 {goal}")
            self.goals_list.insert(tk.END, f"   Progress: {progress:.1f}% ({completed}/{total} tasks)")
            self.goals_list.insert(tk.END, "")  # Empty line for spacing 