import tkinter as tk
from tkinter import messagebox

from database.formaly_database_manager import (
    get_all_tasks,
    add_task,
    update_task,
    delete_task,
    mark_task_complete
)

from utils.styles import *
from utils.helpers import clear_frame, center_window
from utils.validators import validate_task


class AdminDashboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Formaly - Admin Dashboard")
        self.configure(bg=BG)
        self.geometry("1100x700")

        center_window(self, 1100, 700)

        self.selected_task = None

        self.build_ui()
        self.load_tasks()

    # ---------------- UI ----------------
    def build_ui(self):
        # Header
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=20, pady=15)

        tk.Label(
            header,
            text="Admin Dashboard - Tasks",
            bg=BG,
            fg="white",
            font=TITLE
        ).pack(side="left")

        tk.Button(
            header,
            text="Add Task",
            bg=PRIMARY,
            fg="black",
            font=FONT_BOLD,
            command=self.open_add_form
        ).pack(side="right")

        # Task area
        self.task_frame = tk.Frame(self, bg=BG)
        self.task_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # ---------------- LOAD TASKS ----------------
    def load_tasks(self):
        clear_frame(self.task_frame)

        tasks = get_all_tasks()

        for task in tasks:
            self.create_task_card(task)

    # ---------------- TASK CARD ----------------
    def create_task_card(self, task):
        card = tk.Frame(self.task_frame, bg=CARD, padx=15, pady=10)
        card.pack(fill="x", pady=8)

        title = tk.Label(
            card,
            text=task["title"],
            bg=CARD,
            fg="white",
            font=FONT_BOLD
        )
        title.pack(anchor="w")

        desc = tk.Label(
            card,
            text=task["description"],
            bg=CARD,
            fg=SECONDARY,
            font=FONT,
            wraplength=900
        )
        desc.pack(anchor="w", pady=5)

        # Buttons
        btns = tk.Frame(card, bg=CARD)
        btns.pack(anchor="e", pady=5)

        tk.Button(
            btns,
            text="Complete",
            command=lambda t=task["task_id"]: self.complete_task(t)
        ).pack(side="left", padx=5)

        tk.Button(
            btns,
            text="Edit",
            command=lambda t=task: self.edit_task(t)
        ).pack(side="left", padx=5)

        tk.Button(
            btns,
            text="Delete",
            fg="red",
            command=lambda t=task["task_id"]: self.remove_task(t)
        ).pack(side="left", padx=5)

    # ---------------- ACTIONS ----------------
    def open_add_form(self):
        self.task_form()

    def task_form(self, task=None):
        popup = tk.Toplevel(self)
        popup.title("Task Form")
        popup.geometry("400x400")
        popup.configure(bg=BG)

        tk.Label(popup, text="Title", bg=BG, fg=SECONDARY).pack()
        title_entry = tk.Entry(popup)
        title_entry.pack()

        tk.Label(popup, text="Description", bg=BG, fg=SECONDARY).pack()
        desc_entry = tk.Entry(popup)
        desc_entry.pack()

        if task:
            title_entry.insert(0, task["title"])
            desc_entry.insert(0, task["description"])

        def save():
            title = title_entry.get()
            desc = desc_entry.get()

            valid, msg = validate_task(title)
            if not valid:
                messagebox.showerror("Error", msg)
                return

            if task:
                update_task(task["task_id"], title, desc, task["priority"],
                            task["category"], task["due_date"], task["assigned_section"])
            else:
                add_task(title, desc, "Medium", "", "", "")

            popup.destroy()
            self.load_tasks()

        tk.Button(
            popup,
            text="Save",
            bg=PRIMARY,
            command=save
        ).pack(pady=20)

    # ---------------- TASK ACTIONS ----------------
    def complete_task(self, task_id):
        mark_task_complete(task_id)
        self.load_tasks()

    def remove_task(self, task_id):
        if messagebox.askyesno("Delete", "Are you sure?"):
            delete_task(task_id)
            self.load_tasks()

    def edit_task(self, task):
        self.task_form(task)