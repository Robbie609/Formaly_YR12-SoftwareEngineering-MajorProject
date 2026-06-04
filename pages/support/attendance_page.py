import tkinter as tk
from tkinter import ttk
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from database.formaly_database_manager import (
    get_all_attendees, update_attendance, update_payment, update_plus_one
)

class AttendancePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_user = None
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = tk.Frame(self, padx=40, pady=40)
        main_frame.pack(fill="both", expand=True)
        
        # --- HEADER ---
        tk.Label(main_frame, text="Attendance Management", font=("Helvetica", 24, "bold")).pack(anchor="w")
        tk.Label(main_frame, text="Search and manage attendees", font=("Helvetica", 12), fg="gray").pack(anchor="w", pady=(0, 20))
        
        # --- SEARCH BAR ---
        search_frame = tk.Frame(main_frame)
        search_frame.pack(fill="x", pady=(0, 20))
        
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh_table())
        
        tk.Label(search_frame, text="Search:", font=("Helvetica", 10, "bold")).pack(side="left", padx=(0, 10))
        tk.Entry(search_frame, textvariable=self.search_var, width=40, font=("Helvetica", 12)).pack(side="left")
        ttk.Button(search_frame, text="Clear", command=lambda: self.search_var.set("")).pack(side="left", padx=10)

        # --- TREEVIEW TABLE ---
        columns = ("id", "name", "paid", "plus_one", "attendance")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=12)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("paid", text="Payment Status")
        self.tree.heading("plus_one", text="Plus One")
        self.tree.heading("attendance", text="Attendance")
        
        self.tree.column("id", width=0, stretch=tk.NO) # Hide ID column
        self.tree.column("name", anchor="w", width=250)
        self.tree.column("paid", anchor="center", width=120)
        self.tree.column("plus_one", anchor="center", width=100)
        self.tree.column("attendance", anchor="center", width=150)
        
        self.tree.pack(fill="x", pady=(0, 20))
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        # --- SELECTED USER PANEL ---
        self.action_frame = tk.LabelFrame(main_frame, text=" Selected Student Actions ", padx=20, pady=20, font=("Helvetica", 10, "bold"))
        self.action_frame.pack(fill="x")
        
        self.lbl_selected_name = tk.Label(self.action_frame, text="No student selected", font=("Helvetica", 12))
        self.lbl_selected_name.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 15))
        
        # Action Buttons
        self.btn_mark_present = ttk.Button(self.action_frame, text="Mark Present", command=lambda: self.toggle_status('attendance', 1))
        self.btn_remove_present = ttk.Button(self.action_frame, text="Remove Attendance", command=lambda: self.toggle_status('attendance', 0))
        
        self.btn_mark_paid = ttk.Button(self.action_frame, text="Mark Paid", command=lambda: self.toggle_status('paid', 1))
        self.btn_mark_unpaid = ttk.Button(self.action_frame, text="Mark Unpaid", command=lambda: self.toggle_status('paid', 0))
        
        self.btn_add_plus = ttk.Button(self.action_frame, text="Add Plus One", command=lambda: self.toggle_status('plus_one', 1))
        self.btn_remove_plus = ttk.Button(self.action_frame, text="Remove Plus One", command=lambda: self.toggle_status('plus_one', 0))

        # Grid Layout for Buttons
        self.btn_mark_present.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.btn_remove_present.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        
        self.btn_mark_paid.grid(row=1, column=1, padx=20, pady=5, sticky="ew")
        self.btn_mark_unpaid.grid(row=2, column=1, padx=20, pady=5, sticky="ew")
        
        self.btn_add_plus.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
        self.btn_remove_plus.grid(row=2, column=2, padx=5, pady=5, sticky="ew")
        
        self.set_buttons_state("disabled")

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.refresh_table()

    def refresh_table(self):
        """Clears and re-populates the Treeview from the database."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        query = self.search_var.get()
        for row in get_all_attendees(query):
            paid_text = "Paid" if row['paid'] else "Unpaid"
            plus_one_text = "Yes" if row['plus_one'] else "No"
            attendance_text = "Present" if row['attendance'] else "Not Checked In"
            
            self.tree.insert("", "end", values=(row['id'], row['name'], paid_text, plus_one_text, attendance_text))
            
        self.set_buttons_state("disabled")
        self.lbl_selected_name.config(text="No student selected")
        self.selected_user = None

    def on_row_select(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            values = self.tree.item(selected_item, "values")
            self.selected_user = {
                'id': values,
                'name': values,
                'attendance': 1 if values == "Present" else 0
            }
            status_text = "Present" if self.selected_user['attendance'] else "Not Checked In"
            self.lbl_selected_name.config(text=f"Selected: {self.selected_user['name']}   |   Status: {status_text}")
            self.set_buttons_state("normal")

    def set_buttons_state(self, state):
        for btn in [self.btn_mark_present, self.btn_remove_present, 
                    self.btn_mark_paid, self.btn_mark_unpaid, 
                    self.btn_add_plus, self.btn_remove_plus]:
            btn.config(state=state)

    def toggle_status(self, field, value):
        if not self.selected_user: return
        
        user_id = self.selected_user['id']
        if field == 'attendance':
            update_attendance(user_id, value)
        elif field == 'paid':
            update_payment(user_id, value)
        elif field == 'plus_one':
            update_plus_one(user_id, value)
            
        self.refresh_table()