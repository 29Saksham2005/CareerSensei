import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from logic.task_manager import Goal, Task, get_tasks, save_tasks
from modules.base_module import BaseModule

class Module(BaseModule):
    def _create_widgets(self):
        goal_frame = tk.LabelFrame(
            self.frame,
            text="Goal Tracking",
            font=("Helvetica", 12, "bold"),
            fg=self.app.neon_green,
            bg=self.app.card_bg,
            padx=15,
            pady=15
        )
        goal_frame.pack(fill=tk.BOTH, expand=True)

        # Goal selection frame
        goal_selection_frame = tk.Frame(goal_frame, bg=self.app.card_bg)
        goal_selection_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            goal_selection_frame,
            text="Select Goal:",
            font=("Helvetica", 10),
            fg=self.app.fg_color,
            bg=self.app.card_bg
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.goal_var = tk.StringVar()
        self.goal_dropdown = ttk.Combobox(
            goal_selection_frame,
            textvariable=self.goal_var,
            state="readonly",
            width=30,
            font=("Helvetica", 10)
        )
        self.goal_dropdown.pack(side=tk.LEFT, padx=(0, 10))
        self.goal_dropdown.bind('<<ComboboxSelected>>', self.on_goal_selected)

        # Goal creation
        goal_input_frame = tk.Frame(goal_frame, bg=self.app.card_bg)
        goal_input_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            goal_input_frame,
            text="Create New Goal:",
            font=("Helvetica", 10),
            fg=self.app.fg_color,
            bg=self.app.card_bg
        ).pack(anchor=tk.W)

        goal_entry_frame = tk.Frame(goal_input_frame, bg=self.app.card_bg)
        goal_entry_frame.pack(fill=tk.X, pady=(5, 0))

        self.goal_title_entry = tk.Entry(
            goal_entry_frame,
            width=30,
            font=("Helvetica", 10),
            bg=self.app.secondary_bg,
            fg=self.app.fg_color,
            insertbackground=self.app.fg_color
        )
        self.goal_title_entry.pack(side=tk.LEFT, padx=(0, 10))

        create_goal_button = tk.Button(
            goal_entry_frame,
            text="🎯 Create Goal",
            command=self.create_goal,
            font=("Helvetica", 10, "bold"),
            bg=self.app.bg_color,
            fg=self.app.neon_green,
            activebackground=self.app.secondary_bg,
            activeforeground=self.app.neon_green,
            relief=tk.FLAT,
            padx=15,
            pady=5,
            borderwidth=2,
            highlightthickness=1,
            highlightbackground=self.app.neon_green,
            highlightcolor=self.app.neon_green
        )
        create_goal_button.pack(side=tk.LEFT)

        # Task input
        task_input_frame = tk.Frame(goal_frame, bg=self.app.card_bg)
        task_input_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            task_input_frame,
            text="Add Task:",
            font=("Helvetica", 10),
            fg=self.app.fg_color,
            bg=self.app.card_bg
        ).pack(anchor=tk.W)

        self.task_desc_entry = tk.Entry(
            task_input_frame,
            width=40,
            font=("Helvetica", 10),
            bg=self.app.secondary_bg,
            fg=self.app.fg_color,
            insertbackground=self.app.fg_color
        )
        self.task_desc_entry.pack(fill=tk.X, pady=(5, 5))

        date_subtask_frame = tk.Frame(task_input_frame, bg=self.app.card_bg)
        date_subtask_frame.pack(fill=tk.X)

        tk.Label(
            date_subtask_frame,
            text="Due Date:",
            font=("Helvetica", 10),
            fg=self.app.fg_color,
            bg=self.app.card_bg
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.due_date_entry = tk.Entry(
            date_subtask_frame,
            width=15,
            font=("Helvetica", 10),
            bg=self.app.secondary_bg,
            fg=self.app.fg_color,
            insertbackground=self.app.fg_color
        )
        self.due_date_entry.pack(side=tk.LEFT, padx=(0, 15))

        tk.Label(
            date_subtask_frame,
            text="Subtasks:",
            font=("Helvetica", 10),
            fg=self.app.fg_color,
            bg=self.app.card_bg
        ).pack(side=tk.LEFT)

        self.subtask_entry = tk.Entry(
            date_subtask_frame,
            width=25,
            font=("Helvetica", 10),
            bg=self.app.secondary_bg,
            fg=self.app.fg_color,
            insertbackground=self.app.fg_color
        )
        self.subtask_entry.pack(side=tk.LEFT, padx=(5, 0))

        add_task_button = tk.Button(
            task_input_frame,
            text="➕ Add Task",
            command=self.add_task,
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
        add_task_button.pack(pady=(5, 0))

        # Task list
        self.task_listbox = tk.Listbox(
            goal_frame,
            width=40,
            height=8,
            font=("Helvetica", 10),
            bg=self.app.secondary_bg,
            fg=self.app.fg_color,
            selectbackground=self.app.neon_blue,
            selectforeground=self.app.fg_color,
            activestyle=tk.NONE
        )
        self.task_listbox.pack(fill=tk.BOTH, expand=True, pady=(10, 10))

        # Button frame for task actions
        task_buttons_frame = tk.Frame(goal_frame, bg=self.app.card_bg)
        task_buttons_frame.pack(fill=tk.X, pady=(0, 5))

        complete_button = tk.Button(
            task_buttons_frame,
            text="✅ Mark Complete",
            command=self.complete_task,
            font=("Helvetica", 10, "bold"),
            bg=self.app.bg_color,
            fg=self.app.neon_green,
            activebackground=self.app.secondary_bg,
            activeforeground=self.app.neon_green,
            relief=tk.FLAT,
            padx=20,
            pady=5,
            borderwidth=2,
            highlightthickness=1,
            highlightbackground=self.app.neon_green,
            highlightcolor=self.app.neon_green
        )
        complete_button.pack(side=tk.LEFT, padx=(0, 10))

        delete_button = tk.Button(
            task_buttons_frame,
            text="🗑️ Delete Task",
            command=self.delete_task,
            font=("Helvetica", 10, "bold"),
            bg=self.app.bg_color,
            fg=self.app.neon_pink,
            activebackground=self.app.secondary_bg,
            activeforeground=self.app.neon_pink,
            relief=tk.FLAT,
            padx=20,
            pady=5,
            borderwidth=2,
            highlightthickness=1,
            highlightbackground=self.app.neon_pink,
            highlightcolor=self.app.neon_pink
        )
        delete_button.pack(side=tk.LEFT)

        # Load initial goals
        self.load_goals()

    def load_goals(self):
        saved_tasks = get_tasks()
        if saved_tasks:
            self.goal_dropdown['values'] = list(saved_tasks.keys())
            first_goal = next(iter(saved_tasks))
            self.goal_var.set(first_goal)
            self.goal = Goal(first_goal)
            for task_data in saved_tasks[first_goal]:
                if isinstance(task_data, dict):
                    task = Task.from_dict(task_data)
                else:
                    task = Task(description=task_data)
                self.goal.add_task(task)
            self.refresh_task_list()
            self.update_progress()

    def on_goal_selected(self, event):
        selected_goal = self.goal_var.get()
        if selected_goal:
            saved_tasks = get_tasks()
            if selected_goal in saved_tasks:
                self.goal = Goal(selected_goal)
                for task_data in saved_tasks[selected_goal]:
                    if isinstance(task_data, dict):
                        task = Task.from_dict(task_data)
                    else:
                        task = Task(description=task_data)
                    self.goal.add_task(task)
                self.refresh_task_list()
                self.update_progress()

    def update_progress(self):
        if self.goal and self.goal.tasks:
            completed = sum(1 for task in self.goal.tasks if task.completed)
            total = len(self.goal.tasks)
            progress = (completed / total) * 100
            self.app.progress_label.config(
                text=f"🎯 Progress: {completed}/{total} tasks completed ({progress:.0f}%)"
            )
        else:
            self.app.progress_label.config(text="🎯 Ready to help you achieve your goals!")

    def create_goal(self):
        title = self.goal_title_entry.get().strip()
        if title:
            self.goal = Goal(title)
            self.task_listbox.delete(0, tk.END)
            
            current_goals = list(self.goal_dropdown['values'])
            if title not in current_goals:
                self.goal_dropdown['values'] = current_goals + [title]
            self.goal_var.set(title)
            
            tasks = get_tasks()
            tasks[title] = []
            save_tasks(tasks)
            
            messagebox.showinfo("Goal Created", f"🎯 New goal set: {title}")
            self.goal_title_entry.delete(0, tk.END)
            self.update_progress()
        else:
            messagebox.showwarning("Missing Title", "Please enter a goal title.")

    def add_task(self):
        if not self.goal:
            messagebox.showerror("No Goal", "Please create a goal first.")
            return

        desc = self.task_desc_entry.get().strip()
        due = self.due_date_entry.get().strip()
        subtasks = [s.strip() for s in self.subtask_entry.get().split(",") if s.strip()]

        if desc:
            task = Task(description=desc, due_date=due, subtasks=subtasks)
            self.goal.add_task(task)
            tasks = get_tasks()
            if self.goal.title not in tasks:
                tasks[self.goal.title] = []
            tasks[self.goal.title].append(task.to_dict())
            save_tasks(tasks)
            self.refresh_task_list()
            self.update_progress()
            
            self.task_desc_entry.delete(0, tk.END)
            self.due_date_entry.delete(0, tk.END)
            self.subtask_entry.delete(0, tk.END)
            
            messagebox.showinfo("Success", "✨ Task added successfully!")
        else:
            messagebox.showwarning("Missing Description", "Task must have a description.")

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for idx, task in enumerate(self.goal.tasks):
            if not task.completed:
                status = "⏳"
                overdue = "⚠️ Overdue" if task.is_overdue() else ""
                self.task_listbox.insert(
                    tk.END,
                    f"{idx+1}. {task.description} [{status}] Due: {task.due_date or 'N/A'} {overdue}"
                )
                if task.subtasks:
                    for st in task.subtasks:
                        self.task_listbox.insert(tk.END, f"   ↳ {st}")

    def complete_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            task_index = 0
            count = 0
            for task in self.goal.tasks:
                if count == index:
                    task.toggle_complete()
                    if task.completed:
                        task.completion_date = datetime.now().strftime('%Y-%m-%d')
                        # Remove completed subtasks
                        task.subtasks = []
                    tasks = get_tasks()
                    if self.goal.title in tasks and task_index < len(tasks[self.goal.title]):
                        tasks[self.goal.title][task_index] = task.to_dict()
                        save_tasks(tasks)
                    break
                count += 1 + len(task.subtasks)
            self.refresh_task_list()
            self.update_progress()
            
            if task.completed:
                messagebox.showinfo("Success", "🎉 Task completed! Keep up the good work!")

    def delete_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            task_index = 0
            visible_index = 0
            for task in self.goal.tasks:
                if not task.completed:
                    if visible_index == index:
                        self.goal.tasks.pop(task_index)
                        tasks = get_tasks()
                        if self.goal.title in tasks:
                            tasks[self.goal.title].pop(task_index)
                            save_tasks(tasks)
                        break
                    visible_index += 1
                task_index += 1
            
            self.task_listbox.selection_clear(0, tk.END)
            self.refresh_task_list()
            self.update_progress()
            messagebox.showinfo("Success", "🗑️ Task deleted successfully!") 