import json
import os
from datetime import datetime, date

# Update the path to use the data directory in the root
TASKS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "tasks.json")

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return {}
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(goal, task_text):
    tasks = load_tasks()
    if goal not in tasks:
        tasks[goal] = []
    tasks[goal].append(task_text)
    save_tasks(tasks)

def get_tasks():
    return load_tasks()  # Return the full dictionary: {goal: [task strings]}

def save_task_state(goal_title, task_index, task_description):
    tasks = load_tasks()
    if goal_title in tasks and 0 <= task_index < len(tasks[goal_title]):
        tasks[goal_title][task_index] = task_description
        save_tasks(tasks)

# === Models used in main.py ===

class Task:
    def __init__(self, description, due_date=None, subtasks=None):
        self.description = description
        self.due_date = due_date
        self.subtasks = subtasks or []
        self.completed = False

    def toggle_complete(self):
        self.completed = not self.completed

    def is_overdue(self):
        if not self.due_date:
            return False
        try:
            due = datetime.strptime(self.due_date, "%Y-%m-%d").date()
            return not self.completed and date.today() > due
        except ValueError:
            return False

    def to_dict(self):
        return {
            'description': self.description,
            'due_date': self.due_date,
            'subtasks': self.subtasks,
            'completed': self.completed
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(
            description=data['description'],
            due_date=data.get('due_date'),
            subtasks=data.get('subtasks', [])
        )
        task.completed = data.get('completed', False)
        return task

class Goal:
    def __init__(self, title):
        self.title = title
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
