import tkinter as tk
from tkinter import messagebox, ttk
import json
import re
from modules.base_module import BaseModule

class Module(BaseModule):
    def _create_widgets(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create frames for each tab
        self.career_frame = ttk.Frame(self.notebook)
        self.goal_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.career_frame, text="Career Suggestions")
        self.notebook.add(self.goal_frame, text="Goal Suggestions")

        # Setup each tab
        self.setup_career_suggestions()
        self.setup_goal_suggestions()

    def setup_career_suggestions(self):
        # Career suggestions display
        suggestions_display_frame = tk.Frame(self.career_frame, bg=self.app.card_bg)
        suggestions_display_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        tk.Label(
            suggestions_display_frame,
            text="Career Path Suggestions:",
            font=("Helvetica", 10),
            fg=self.app.fg_color,
            bg=self.app.card_bg
        ).pack(anchor=tk.W)

        self.career_suggestions_box = tk.Text(
            suggestions_display_frame,
            height=10,
            width=50,
            font=("Helvetica", 10),
            bg=self.app.secondary_bg,
            fg=self.app.fg_color,
            wrap=tk.WORD
        )
        self.career_suggestions_box.pack(fill=tk.BOTH, expand=True, pady=(5, 5))

        # Generate career suggestions button
        generate_button = tk.Button(
            suggestions_display_frame,
            text="🤖 Generate Career Suggestions",
            command=self.get_career_suggestions,
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
        generate_button.pack(pady=(5, 0))

    def setup_goal_suggestions(self):
        # Goal suggestions display
        suggestions_display_frame = tk.Frame(self.goal_frame, bg=self.app.card_bg)
        suggestions_display_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        tk.Label(
            suggestions_display_frame,
            text="Suggested Goals and Tasks:",
            font=("Helvetica", 10),
            fg=self.app.fg_color,
            bg=self.app.card_bg
        ).pack(anchor=tk.W)

        self.goal_suggestions_box = tk.Text(
            suggestions_display_frame,
            height=10,
            width=50,
            font=("Helvetica", 10),
            bg=self.app.secondary_bg,
            fg=self.app.fg_color,
            wrap=tk.WORD
        )
        self.goal_suggestions_box.pack(fill=tk.BOTH, expand=True, pady=(5, 5))

        # Generate goal suggestions button
        generate_button = tk.Button(
            suggestions_display_frame,
            text="🤖 Generate Goal Suggestions",
            command=self.get_goal_suggestions,
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
        generate_button.pack(pady=(5, 0))

        # Apply suggestions button
        apply_button = tk.Button(
            suggestions_display_frame,
            text="✨ Apply Selected Suggestions",
            command=self.apply_suggestions,
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
        apply_button.pack(pady=(5, 0))

        # Initialize suggestions storage
        self.current_suggestions = None

    def get_career_suggestions(self):
        try:
            # Simulate AI response for career suggestions
            response = self.simulate_career_suggestions()
            
            # Display suggestions
            self.career_suggestions_box.delete("1.0", tk.END)
            self.career_suggestions_box.insert(tk.END, response)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate career suggestions: {str(e)}")

    def get_goal_suggestions(self):
        try:
            # Simulate AI response
            response = self.simulate_ai_response()
            
            # Parse the response
            try:
                suggestions = json.loads(response)
            except json.JSONDecodeError:
                # Try to extract JSON from the response if it's not clean
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    suggestions = json.loads(json_match.group())
                else:
                    raise ValueError("Could not parse AI response as JSON")

            # Store suggestions
            self.current_suggestions = suggestions

            # Display suggestions
            self.goal_suggestions_box.delete("1.0", tk.END)
            self.goal_suggestions_box.insert(tk.END, json.dumps(suggestions, indent=2))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate goal suggestions: {str(e)}")

    def apply_suggestions(self):
        if not self.current_suggestions:
            messagebox.showwarning("No Suggestions", "Please generate suggestions first.")
            return

        try:
            # Add the suggested goals and tasks to the task manager
            from logic.task_manager import get_tasks, save_tasks
            tasks = get_tasks()

            for goal in self.current_suggestions.get("goals", []):
                goal_title = goal["title"]
                if goal_title not in tasks:
                    tasks[goal_title] = []
                
                for task in goal["tasks"]:
                    tasks[goal_title].append({
                        "description": task["description"],
                        "due_date": task["due_date"],
                        "subtasks": task.get("subtasks", []),
                        "completed": False
                    })

            save_tasks(tasks)
            messagebox.showinfo("Success", "Suggestions applied successfully!")
            
            # Clear current suggestions
            self.current_suggestions = None
            self.goal_suggestions_box.delete("1.0", tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply suggestions: {str(e)}")

    def simulate_career_suggestions(self):
        # This is a placeholder for the actual AI integration
        return """Here are some career path suggestions:

1. Software Development Path
   • Current demand: High
   • Required skills: Programming, Problem-solving
   • Growth potential: Excellent
   • Entry level positions: Junior Developer, QA Engineer
   • Mid-level positions: Senior Developer, Team Lead
   • Senior positions: Technical Architect, Engineering Manager

2. Data Science Path
   • Current demand: Very High
   • Required skills: Statistics, Python, Machine Learning
   • Growth potential: Excellent
   • Entry level positions: Data Analyst, Business Intelligence Analyst
   • Mid-level positions: Data Scientist, Machine Learning Engineer
   • Senior positions: Lead Data Scientist, AI Research Scientist

3. Product Management Path
   • Current demand: High
   • Required skills: Communication, Strategic thinking
   • Growth potential: Very Good
   • Entry level positions: Associate Product Manager
   • Mid-level positions: Product Manager
   • Senior positions: Senior Product Manager, Product Director"""

    def simulate_ai_response(self):
        # This is a placeholder for the actual AI integration
        return """{
            "goals": [
                {
                    "title": "Learn Python Programming",
                    "tasks": [
                        {
                            "description": "Complete Python basics course",
                            "due_date": "2024-04-01",
                            "subtasks": ["Install Python", "Learn syntax", "Practice basic exercises"]
                        },
                        {
                            "description": "Build a simple project",
                            "due_date": "2024-04-15",
                            "subtasks": ["Choose project idea", "Design architecture", "Implement features"]
                        }
                    ]
                },
                {
                    "title": "Improve Data Analysis Skills",
                    "tasks": [
                        {
                            "description": "Learn Pandas library",
                            "due_date": "2024-04-10",
                            "subtasks": ["Study documentation", "Practice with sample datasets"]
                        },
                        {
                            "description": "Create data visualization project",
                            "due_date": "2024-04-20",
                            "subtasks": ["Select dataset", "Create visualizations", "Write analysis report"]
                        }
                    ]
                }
            ]
        }""" 