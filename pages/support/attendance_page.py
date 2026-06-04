import tkinter as tk
from tkinter import ttk
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from database.formaly_database_manager import (
    get_all_attendees, update_attendance, update_plus_one
)
from utils.styles import *


class AttendancePage(tk.Frame):
    def __init__(self, parent, controller=None, user=None):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.user = user
        self.selected_user = None
        self.setup_ui()

    def setup_ui(self):
        root = tk.Frame(self, bg=BG)
        root.pack(fill="both", expand=True)

        # =========================
        # SIDEBAR NAVIGATION
        # =========================
        sidebar = tk.Frame(root, bg=CARD, width=240)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="FORMALY",
            bg=CARD,
            fg=PRIMARY,
            font=TITLE
        ).pack(anchor="w", padx=20, pady=(30, 5))

        tk.Label(
            sidebar,
            text="Support",
            bg=CARD,
            fg=SECONDARY,
            font=SMALL
        ).pack(anchor="w", padx=20, pady=(0, 30))

        # Navigation Buttons
        self.nav_button(sidebar, "📊 Dashboard", lambda: self.controller.show_frame("SupportDashboard") if self.controller else None)
        self.nav_button(sidebar, "👥 Attendance")

        # Spacer
        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=15, pady=20)

        # Logout
        self.nav_button(sidebar, "🚪 Logout", self.logout, danger=True)

        # =========================
        # MAIN CONTENT AREA
        # =========================
        main = tk.Frame(root, bg=BG)
        main.pack(side="left", fill="both", expand=True)

        # Header Section
        header = tk.Frame(main, bg=BG)
        header.pack(fill="x", padx=40, pady=(35, 10))

        tk.Label(
            header,
            text="Attendance Management",
            bg=BG,
            fg="white",
            font=TITLE
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Update attendance and plus-one status for attendees",
            bg=BG,
            fg=SECONDARY,
            font=FONT
        ).pack(anchor="w", pady=(5, 0))

        # Content Frame
        content = tk.Frame(main, bg=BG)
        content.pack(fill="both", expand=True, padx=40, pady=30)

        # =========================
        # ATTENDANCE TABLE
        # =========================
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', background=CARD, foreground="white", fieldbackground=CARD, font=FONT)
        style.configure('Treeview.Heading', background=ENTRY, foreground=PRIMARY, font=FONT_BOLD)
        style.map('Treeview', background=[('selected', PRIMARY)])
        style.map('Treeview', foreground=[('selected', 'black')])

        columns = ("name", "attendance", "plus_one")
        self.tree = ttk.Treeview(content, columns=columns, show="headings", height=16, style='Treeview')

        self.tree.heading("name", text="Attendee Name")
        self.tree.heading("attendance", text="Check-In Status")
        self.tree.heading("plus_one", text="Plus One")

        self.tree.column("name", anchor="w", width=300)
        self.tree.column("attendance", anchor="center", width=150)
        self.tree.column("plus_one", anchor="center", width=120)

        self.tree.pack(fill="both", expand=True, pady=(0, 20))
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        # =========================
        # ACTION PANEL
        # =========================
        action_frame = tk.Frame(
            content,
            bg=CARD,
            highlightthickness=1,
            highlightbackground=BORDER
        )
        action_frame.pack(fill="x", padx=0, pady=0)

        action_header = tk.Frame(action_frame, bg=CARD)
        action_header.pack(fill="x", padx=20, pady=(18, 15))

        tk.Label(
            action_header,
            text="Quick Actions",
            bg=CARD,
            fg="white",
            font=FONT_BOLD
        ).pack(anchor="w", side="left")

        self.lbl_selected = tk.Label(
            action_header,
            text="Select an attendee to perform actions",
            bg=CARD,
            fg=SECONDARY,
            font=SMALL
        )
        self.lbl_selected.pack(anchor="e", side="right")

        # Action Buttons
        btn_frame = tk.Frame(action_frame, bg=CARD)
        btn_frame.pack(fill="x", padx=20, pady=(0, 18))

        self.btn_mark_present = tk.Button(
            btn_frame,
            text="✓ Mark Present",
            command=lambda: self.toggle_attendance(1),
            bg=SUCCESS,
            fg="black",
            font=FONT_BOLD,
            relief="flat",
            padx=15,
            pady=10,
            cursor="hand2",
            activebackground="#5FFF85",
            state="disabled"
        )
        self.btn_mark_present.pack(side="left", padx=(0, 12))

        self.btn_remove_attendance = tk.Button(
            btn_frame,
            text="✗ Mark Absent",
            command=lambda: self.toggle_attendance(0),
            bg=ERROR,
            fg="white",
            font=FONT_BOLD,
            relief="flat",
            padx=15,
            pady=10,
            cursor="hand2",
            activebackground="#FF8585",
            state="disabled"
        )
        self.btn_remove_attendance.pack(side="left", padx=(0, 12))

        self.btn_add_plus = tk.Button(
            btn_frame,
            text="➕ Add Plus One",
            command=lambda: self.toggle_plus_one(1),
            bg=PRIMARY,
            fg="black",
            font=FONT_BOLD,
            relief="flat",
            padx=15,
            pady=10,
            cursor="hand2",
            activebackground="#FFE27A",
            state="disabled"
        )
        self.btn_add_plus.pack(side="left", padx=(0, 12))

        self.btn_remove_plus = tk.Button(
            btn_frame,
            text="➖ Remove Plus One",
            command=lambda: self.toggle_plus_one(0),
            bg=ENTRY,
            fg="white",
            font=FONT_BOLD,
            relief="flat",
            padx=15,
            pady=10,
            cursor="hand2",
            activebackground=PRIMARY,
            state="disabled"
        )
        self.btn_remove_plus.pack(side="left")

    def nav_button(self, parent, text, command=None, danger=False):
        """Create a navigation button."""
        def on_enter(e):
            btn.config(bg=PRIMARY if not danger else ERROR, fg="black" if not danger else "white")

        def on_leave(e):
            btn.config(bg=ENTRY, fg="white")

        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=ENTRY,
            fg="white",
            font=FONT,
            relief="flat",
            anchor="w",
            padx=15,
            pady=12,
            cursor="hand2",
            activebackground=PRIMARY
        )
        btn.pack(fill="x", padx=12, pady=5)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.refresh_table()

    def refresh_table(self):
        """Refresh the attendance table from database."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        attendees = get_all_attendees()

        for row in attendees:
            attendance_text = "✓ Present" if row['attendance'] else "✗ Absent"
            plus_one_text = "✓ Yes" if row['plus_one'] else "✗ No"

            self.tree.insert("", "end", values=(row['name'], attendance_text, plus_one_text))

        self.disable_buttons()
        self.lbl_selected.config(text="Select an attendee to perform actions")
        self.selected_user = None

    def on_row_select(self, event):
        """Handle row selection."""
        selected_item = self.tree.focus()
        if selected_item:
            values = self.tree.item(selected_item, "values")
            # values[0] = name, values[1] = attendance, values[2] = plus_one

            # Get full user data from database
            all_attendees = get_all_attendees()
            for attendee in all_attendees:
                if attendee['name'] == values[0]:
                    self.selected_user = attendee
                    break

            if self.selected_user:
                self.lbl_selected.config(
                    text=f"Selected: {self.selected_user['name']} | Status: {values[1]}"
                )
                self.enable_buttons()

    def enable_buttons(self):
        """Enable action buttons."""
        for btn in [self.btn_mark_present, self.btn_remove_attendance, self.btn_add_plus, self.btn_remove_plus]:
            btn.config(state="normal")

    def disable_buttons(self):
        """Disable action buttons."""
        for btn in [self.btn_mark_present, self.btn_remove_attendance, self.btn_add_plus, self.btn_remove_plus]:
            btn.config(state="disabled")

    def toggle_attendance(self, status):
        """Update attendance status (0 = absent, 1 = present)."""
        if not self.selected_user:
            return

        update_attendance(self.selected_user['id'], status)

        if self.controller and hasattr(self.controller, 'refresh_dashboard'):
            self.controller.refresh_dashboard()

        self.refresh_table()

    def toggle_plus_one(self, status):
        """Update plus-one status (0 = no, 1 = yes)."""
        if not self.selected_user:
            return

        update_plus_one(self.selected_user['id'], status)

        if self.controller and hasattr(self.controller, 'refresh_dashboard'):
            self.controller.refresh_dashboard()

        self.refresh_table()

    def logout(self):
        """Logout and return to login."""
        if self.controller and hasattr(self.controller, 'logout'):
            self.controller.logout()

