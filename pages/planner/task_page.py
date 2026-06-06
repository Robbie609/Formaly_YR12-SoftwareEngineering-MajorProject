# pages/planner/task_page.py

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

from utils.styles import (
    BG, CARD, ENTRY, PRIMARY, SECONDARY, SUCCESS, ERROR, BORDER,
    FONT, FONT_BOLD, TITLE, SUBTITLE, SMALL, PADDING_X, PADDING_Y
)
from utils.helpers import clear_frame, truncate_text

class TaskPage(tk.Frame):
    def __init__(self, parent, user=None):
        super().__init__(parent, bg=BG)
        self.parent = parent
        self.user = user

        self.search_query = ""
        self.filter_priority = "All"
        self.filter_status = "All"
        self.sort_by = "Due Date"

        self.setup_layout()

    def setup_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar Component
        self.sidebar = tk.Frame(self, bg=CARD, width=260, bd=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        # Main Layout Frame
        self.main_content = tk.Frame(self, bg=BG)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=PADDING_X, pady=PADDING_Y)
        self.main_content.grid_rowconfigure(2, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)

        from pages.planner.planner_dashboard import PlannerDashboard
        PlannerDashboard.render_sidebar(self, "Tasks")
        self.render_task_workspace()

    def render_task_workspace(self):
        clear_frame(self.main_content)
        
        # Action Bar Top Section
        top_bar = tk.Frame(self.main_content, bg=BG)
        top_bar.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        title_lbl = tk.Label(top_bar, text="Tasks Directory", font=TITLE, fg=PRIMARY, bg=BG)
        title_lbl.pack(side="left", anchor="w")
        
        add_btn = tk.Button(
            top_bar, text="+ Create Task", font=FONT_BOLD, fg=CARD, bg=PRIMARY,
            activebackground=SECONDARY, activeforeground=CARD, bd=0, relief="flat",
            padx=16, pady=8, command=self.open_task_modal
        )
        add_btn.pack(side="right")

        # Filters Bar Configuration
        filter_bar = tk.Frame(self.main_content, bg=BG)
        filter_bar.grid(row=1, column=0, sticky="ew", pady=(0, 16))

        # Filters dropdown setup using standard modern layout wrappers
        self.create_filter_dropdown(filter_bar, "Priority:", ["All", "High", "Medium", "Low"], "filter_priority")
        self.create_filter_dropdown(filter_bar, "Status:", ["All", "Pending", "In Progress", "Completed"], "filter_status")
        self.create_filter_dropdown(filter_bar, "Sort:", ["Due Date", "Priority Code"], "sort_by")

        # Dynamic Grid Scroll Container
        canvas_container = tk.Frame(self.main_content, bg=BG)
        canvas_container.grid(row=2, column=0, sticky="nsew")
        canvas_container.grid_rowconfigure(0, weight=1)
        canvas_container.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(canvas_container, bg=BG, bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_container, orient="vertical", command=self.canvas.yview)
        
        self.scroll_frame = tk.Frame(self.canvas, bg=BG)
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))

        self.display_tasks()

    def create_filter_dropdown(self, parent, label_text, choices, target_attr):
        lbl = tk.Label(parent, text=label_text, font=SMALL, fg=SECONDARY, bg=BG)
        lbl.pack(side="left", padx=(8, 4))
        
        val_var = tk.StringVar(value=getattr(self, target_attr))
        cb = ttk.Combobox(parent, textvariable=val_var, values=choices, state="readonly", width=12)
        cb.pack(side="left", padx=(0, 12))
        
        def on_change(e):
            setattr(self, target_attr, val_var.get())
            self.display_tasks()
            
        cb.bind("<<ComboboxSelected>>", on_change)

    def update_search(self, event):
        self.search_query = self.search_ent.get()
        self.display_tasks()

    def display_tasks(self):
        clear_frame(self.scroll_frame)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        conn = sqlite3.connect("database/formaly.db")
        cursor = conn.cursor()
        
        query = "SELECT task_id, title, description, priority, due_date, status FROM tasks WHERE 1=1"
        params = []

        if self.search_query:
            query += " AND (title LIKE ? OR description LIKE ?)"
            params.extend([f"%{self.search_query}%", f"%{self.search_query}%"])
            
        if self.filter_priority != "All":
            query += " AND priority = ?"
            params.append(self.filter_priority)
            
        if self.filter_status != "All":
            query += " AND status = ?"
            params.append(self.filter_status)

        if self.sort_by == "Due Date":
            query += " ORDER BY due_date ASC"
        else:
            query += " ORDER BY CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 WHEN 'Low' THEN 3 END ASC"

        cursor.execute(query, params)
        tasks = cursor.fetchall()
        conn.close()

        if not tasks:
            empty_lbl = tk.Label(self.scroll_frame, text="No matching records tracked.", font=SUBTITLE, fg=SECONDARY, bg=BG)
            empty_lbl.pack(pady=60)
            return

        for task_id, title, desc, priority, due, status in tasks:
            card_border = tk.Frame(self.scroll_frame, bg=BORDER, padx=1, pady=1)
            card_border.pack(fill="x", pady=6)
            
            card = tk.Frame(card_border, bg=CARD, padx=16, pady=16)
            card.pack(fill="x")
            
            # Left Section Info Layout
            left_section = tk.Frame(card, bg=CARD)
            left_section.pack(side="left", fill="both", expand=True)
            
            t_lbl = tk.Label(left_section, text=title, font=FONT_BOLD, fg=PRIMARY, bg=CARD)
            t_lbl.pack(anchor="w")
            
            d_lbl = tk.Label(left_section, text=truncate_text(desc, 100), font=FONT, fg=SECONDARY, bg=CARD)
            d_lbl.pack(anchor="w", pady=(4, 6))
            
            meta_bar = tk.Frame(left_section, bg=CARD)
            meta_bar.pack(anchor="w")
            
            p_color = ERROR if priority == "High" else (SECONDARY if priority == "Medium" else SUCCESS)
            p_badge = tk.Label(meta_bar, text=f" Priority: {priority} ", font=SMALL, fg=CARD, bg=p_color, padx=4)
            p_badge.pack(side="left")
            
            s_color = SUCCESS if status == "Completed" else (PRIMARY if status == "In Progress" else SECONDARY)
            s_badge = tk.Label(meta_bar, text=f" Status: {status} ", font=SMALL, fg=CARD, bg=s_color, padx=4)
            s_badge.pack(side="left", padx=12)
            
            due_lbl = tk.Label(meta_bar, text=f"Due: {due}", font=SMALL, fg=SECONDARY, bg=CARD)
            due_lbl.pack(side="left")

            # Right Section Interactive Controls Layout
            right_section = tk.Frame(card, bg=CARD)
            right_section.pack(side="right", fill="y", padx=(16, 0))
            
            if status != "Completed":
                done_btn = tk.Button(
                    right_section, text="Complete", font=SMALL, fg=CARD, bg=SUCCESS,
                    activebackground=BG, activeforeground=SUCCESS, bd=0, relief="flat", padx=8, pady=4,
                    command=lambda tid=task_id: self.mark_complete(tid)
                )
                done_btn.pack(side="left", padx=4)
                
            edit_btn = tk.Button(
                right_section, text="Edit", font=SMALL, fg=CARD, bg=PRIMARY,
                activebackground=BG, activeforeground=PRIMARY, bd=0, relief="flat", padx=8, pady=4,
                command=lambda tid=task_id, t=title, d=desc, p=priority, du=due, s=status: self.open_task_modal(tid, t, d, p, du, s)
            )
            edit_btn.pack(side="left", padx=4)
            
            del_btn = tk.Button(
                right_section, text="Delete", font=SMALL, fg=CARD, bg=ERROR,
                activebackground=BG, activeforeground=ERROR, bd=0, relief="flat", padx=8, pady=4,
                command=lambda tid=task_id: self.delete_task(tid)
            )
            del_btn.pack(side="left", padx=4)

    def mark_complete(self, task_id):
        conn = sqlite3.connect("database/formaly.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = 'Completed' WHERE task_id = ?", (task_id,))
        conn.commit()
        conn.close()
        self.display_tasks()

    def delete_task(self, task_id):
        if messagebox.askyesno("Confirm Action", "Are you sure you want to remove this task?"):
            conn = sqlite3.connect("database/formaly.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
            conn.commit()
            conn.close()
            self.display_tasks()

    def open_task_modal(self, task_id=None, title="", desc="", priority="Medium", due="", status="Pending"):
        modal = tk.Toplevel(self)
        modal.title("Task Workspace Data Editor")
        modal.geometry("460x520")
        modal.configure(bg=BG)
        modal.transient(self)
        modal.grab_set()
        modal.resizable(False, False)

        container = tk.Frame(modal, bg=BG, padx=24, pady=24)
        container.pack(fill="both", expand=True)

        header_lbl = tk.Label(container, text="Task Details Editor" if task_id else "New Task Creation", font=SUBTITLE, fg=PRIMARY, bg=BG)
        header_lbl.pack(anchor="w", pady=(0, 20))

        # Field Inputs
        tk.Label(container, text="Title", font=FONT_BOLD, fg=PRIMARY, bg=BG).pack(anchor="w", pady=(8, 2))
        t_border = tk.Frame(container, bg=BORDER, padx=1, pady=1)
        t_border.pack(fill="x")
        title_ent = tk.Entry(t_border, font=FONT, bg=ENTRY, fg=PRIMARY, bd=0)
        title_ent.pack(fill="x", padx=8, pady=6)
        title_ent.insert(0, title)

        tk.Label(container, text="Description", font=FONT_BOLD, fg=PRIMARY, bg=BG).pack(anchor="w", pady=(12, 2))
        d_border = tk.Frame(container, bg=BORDER, padx=1, pady=1)
        d_border.pack(fill="x")
        desc_txt = tk.Text(d_border, font=FONT, bg=ENTRY, fg=PRIMARY, bd=0, height=4, highlightthickness=0)
        desc_txt.pack(fill="x", padx=8, pady=6)
        desc_txt.insert("1.0", desc)

        dropdowns_frame = tk.Frame(container, bg=BG)
        dropdowns_frame.pack(fill="x", pady=(12, 0))
        dropdowns_frame.grid_columnconfigure((0, 1), weight=1)

        # Dropdown Option Menus
        p_frame = tk.Frame(dropdowns_frame, bg=BG)
        p_frame.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        tk.Label(p_frame, text="Priority", font=FONT_BOLD, fg=PRIMARY, bg=BG).pack(anchor="w")
        p_var = tk.StringVar(value=priority)
        p_cb = ttk.Combobox(p_frame, textvariable=p_var, values=["High", "Medium", "Low"], state="readonly")
        p_cb.pack(fill="x", pady=4)

        s_frame = tk.Frame(dropdowns_frame, bg=BG)
        s_frame.grid(row=0, column=1, sticky="ew", padx=(6, 0))
        tk.Label(s_frame, text="Status", font=FONT_BOLD, fg=PRIMARY, bg=BG).pack(anchor="w")
        s_var = tk.StringVar(value=status)
        s_cb = ttk.Combobox(s_frame, textvariable=s_var, values=["Pending", "In Progress", "Completed"], state="readonly")
        s_cb.pack(fill="x", pady=4)

        tk.Label(container, text="Due Date (YYYY-MM-DD)", font=FONT_BOLD, fg=PRIMARY, bg=BG).pack(anchor="w", pady=(12, 2))
        due_border = tk.Frame(container, bg=BORDER, padx=1, pady=1)
        due_border.pack(fill="x")
        due_ent = tk.Entry(due_border, font=FONT, bg=ENTRY, fg=PRIMARY, bd=0)
        due_ent.pack(fill="x", padx=8, pady=6)
        if due:
            due_ent.insert(0, due)
        else:
            from datetime import date
            due_ent.insert(0, date.today().strftime("%Y-%m-%d"))

        # Footer Action Control Panel
        actions_panel = tk.Frame(container, bg=BG)
        actions_panel.pack(fill="x", side="bottom", pady=(24, 0))

        def save_changes():
            t_val = title_ent.get().strip()
            d_val = desc_txt.get("1.0", "end-1c").strip()
            p_val = p_var.get()
            s_val = s_var.get()
            due_val = due_ent.get().strip()

            if not t_val:
                messagebox.showerror("Validation Error", "Title is a required attribute field.")
                return

            conn = sqlite3.connect("database/formaly.db")
            cursor = conn.cursor()
            if task_id:
                cursor.execute("""
                    UPDATE tasks SET title=?, description=?, priority=?, due_date=?, status=? WHERE task_id=?
                """, (t_val, d_val, p_val, due_val, s_val, task_id))
            else:
                cursor.execute("""
                    INSERT INTO tasks (title, description, priority, due_date, status) VALUES (?, ?, ?, ?, ?)
                """, (t_val, d_val, p_val, due_val, s_val))
            conn.commit()
            conn.close()
            modal.destroy()
            self.display_tasks()

        submit_btn = tk.Button(
            actions_panel, text="Save Records", font=FONT_BOLD, fg=CARD, bg=PRIMARY,
            activebackground=SECONDARY, activeforeground=CARD, bd=0, relief="flat", padx=16, pady=8,
            command=save_changes
        )
        submit_btn.pack(side="right")

        cancel_btn = tk.Button(
            actions_panel, text="Dismiss", font=FONT_BOLD, fg=PRIMARY, bg=BG,
            activebackground=BORDER, activeforeground=PRIMARY, bd=0, relief="flat", padx=16, pady=8,
            command=modal.destroy
        )
        cancel_btn.pack(side="right", padx=12)