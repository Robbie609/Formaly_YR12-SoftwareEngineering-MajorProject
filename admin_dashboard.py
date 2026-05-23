import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import os

import formaly_database
formaly_database.init_db()

# --- EXACT COLOR PALETTE ---
BG_COLOR = "#0B0B0B"
FG_PRIMARY = "#FFD24A"
FG_SECONDARY = "#C0C0C0"
BG_SECONDARY = "#1A1A1A"
BG_ENTRY = "#0A0A0A"

# --- TYPOGRAPHY ---
FONT_MAIN = ("Segoe UI", 11)
FONT_BOLD = ("Segoe UI", 11, "bold")
FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_H1 = ("Segoe UI", 22, "bold")
FONT_SMALL = ("Segoe UI", 9)

class HoverButton(tk.Frame):
    """Enhanced hover button with stronger visual lift + glow-like effect."""
    def __init__(self, parent, text, command=None,
                 bg=BG_SECONDARY, fg=FG_SECONDARY,
                 hover_bg="#3A3A3A", hover_fg="white",
                 font=FONT_MAIN, width=None, pad_y=10, **kwargs):
        
        super().__init__(parent, bg=bg, cursor="hand2", **kwargs)

        self.command = command
        self.bg = bg
        self.hover_bg = hover_bg
        self.hover_fg = hover_fg
        self.normal_fg = fg

        self.is_hover = False

        self.lbl = tk.Label(
            self,
            text=text,
            bg=bg,
            fg=fg,
            font=font
        )

        if width:
            self.lbl.config(width=width, anchor="w")

        self.lbl.pack(pady=pad_y, padx=20, fill="x", expand=True)

        # bindings
        for w in (self, self.lbl):
            w.bind("<Enter>", self.on_enter)
            w.bind("<Leave>", self.on_leave)
            w.bind("<Button-1>", self.on_click)

    def on_enter(self, e):
        self.is_hover = True
        self.config(bg=self.hover_bg)
        self.lbl.config(
            bg=self.hover_bg,
            fg=self.hover_fg,
            font=(self.lbl.cget("font").split()[0], 11, "bold")
        )

        # subtle "lift" effect
        self.lbl.pack_configure(pady=12)

    def on_leave(self, e):
        self.is_hover = False
        self.config(bg=self.bg)
        self.lbl.config(
            bg=self.bg,
            fg=self.normal_fg,
            font=FONT_MAIN
        )

        self.lbl.pack_configure(pady=10)

    def on_click(self, e):
        if self.command:
            self.command()

class TaskModal(tk.Toplevel):
    """Modal popup to Add or Edit tasks with expanded fields."""
    def __init__(self, parent, task=None, callback=None):
        super().__init__(parent)
        self.parent = parent
        self.task = task
        self.callback = callback
        
        self.title("Edit Task" if task else "Add New Task")
        self.geometry("450x650")
        self.configure(bg=BG_SECONDARY)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 225
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 325
        self.geometry(f"+{x}+{y}")
        
        self.build_ui()

    def build_ui(self):
        lbl_title = tk.Label(self, text="Edit Task" if self.task else "Add Task", bg=BG_SECONDARY, fg=FG_PRIMARY, font=FONT_TITLE)
        lbl_title.pack(pady=(20, 15), anchor="w", padx=30)

        def create_entry(label_text, is_text_area=False):
            tk.Label(self, text=label_text, bg=BG_SECONDARY, fg=FG_SECONDARY, font=FONT_BOLD).pack(anchor="w", padx=30, pady=(5,0))
            if is_text_area:
                widget = tk.Text(self, bg=BG_ENTRY, fg="white", font=FONT_MAIN, relief="flat", height=3, insertbackground=FG_PRIMARY)
                widget.pack(fill="x", padx=30, pady=5)
            else:
                widget = tk.Entry(self, bg=BG_ENTRY, fg="white", font=FONT_MAIN, relief="flat", insertbackground=FG_PRIMARY)
                widget.pack(fill="x", padx=30, pady=5, ipady=5)
            return widget

        self.title_entry = create_entry("Task Title:")
        self.desc_entry = create_entry("Description:", is_text_area=True)
        self.category_entry = create_entry("Category (e.g. Media, Catering):")
        self.due_date_entry = create_entry("Due Date (YYYY-MM-DD):")
        self.section_entry = create_entry("Assigned Section (e.g. Admin, Helpers):")

        tk.Label(self, text="Priority:", bg=BG_SECONDARY, fg=FG_SECONDARY, font=FONT_BOLD).pack(anchor="w", padx=30, pady=(10,0))
        self.priority_var = tk.StringVar(value="Medium")
        prio_frame = tk.Frame(self, bg=BG_SECONDARY)
        prio_frame.pack(fill="x", padx=30, pady=5)
        
        for p in ["High", "Medium", "Low"]:
            rb = tk.Radiobutton(prio_frame, text=p, variable=self.priority_var, value=p, bg=BG_SECONDARY, fg=FG_SECONDARY, 
                                selectcolor=BG_ENTRY, activebackground=BG_SECONDARY, activeforeground=FG_PRIMARY, font=FONT_MAIN)
            rb.pack(side="left", padx=(0, 10))

        if self.task:
            self.title_entry.insert(0, self.task['title'])
            self.desc_entry.insert("1.0", self.task['description'])
            self.category_entry.insert(0, self.task['category'] or "")
            self.due_date_entry.insert(0, self.task['due_date'] or "")
            self.section_entry.insert(0, self.task['assigned_section'] or "")
            self.priority_var.set(self.task['priority'])

        btn_save = HoverButton(self, "Save Task", command=self.save_task, bg=FG_PRIMARY, fg=BG_COLOR, hover_bg="#E5BA3D", font=FONT_BOLD)
        btn_save.pack(pady=20, padx=30, fill="x")

    def save_task(self):
        title = self.title_entry.get().strip()
        desc = self.desc_entry.get("1.0", "end-1c").strip()
        category = self.category_entry.get().strip()
        due_date = self.due_date_entry.get().strip()
        section = self.section_entry.get().strip()
        prio = self.priority_var.get()
        
        if not title:
            messagebox.showerror("Error", "Task Title is required.", parent=self)
            return
            
        if self.task:
            formaly_database.update_task(self.task['task_id'], title, desc, prio, category, due_date, section)
        else:
            formaly_database.add_task(title, desc, prio, category, due_date, section)
            
        if self.callback:
            self.callback()
        self.destroy()

class FormalyAdminApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # --- APP CONFIGURATION & INTRO ANIMATIONS ---
        self.title("Formaly - Admin Dashboard")
        self.geometry("1100x700")  # Expanded canvas footprint
        self.configure(bg=BG_COLOR)
        self.minsize(1000, 650)
        
        # Smooth window fade-in animation
        self.attributes("-alpha", 0.0)
        self.fade_in(0.0)
        
        self.current_user_role = "Administrator"
        self.sidebar_open = False
        self.sidebar_width = 240
        self.sidebar_x = -self.sidebar_width
        
        self.build_ui()
        self.refresh_tasks()

    def fade_in(self, alpha):
        alpha += 0.05
        self.attributes("-alpha", alpha)
        if alpha < 1.0:
            self.after(15, lambda: self.fade_in(alpha))

    def build_ui(self):
        self.build_navbar()
        
        self.content_frame = tk.Frame(self, bg=BG_COLOR)
        self.content_frame.pack(fill="both", expand=True)
        self.build_dashboard()
        
        self.build_sidebar()

    def build_navbar(self):
        navbar = tk.Frame(self, bg=BG_SECONDARY, height=65)
        navbar.pack(side="top", fill="x")
        navbar.pack_propagate(False)

        # High-end geometric hamburger menu icon
        self.btn_menu = tk.Label(navbar, text="☰", bg=BG_SECONDARY, fg=FG_PRIMARY, font=("Segoe UI", 22), cursor="hand2")
        self.btn_menu.pack(side="left", padx=25)
        self.btn_menu.bind("<Button-1>", lambda e: self.toggle_sidebar())
        self.btn_menu.bind("<Enter>", lambda e: self.btn_menu.config(fg="white"))
        self.btn_menu.bind("<Leave>", lambda e: self.btn_menu.config(fg=FG_PRIMARY))

        tk.Label(navbar, text="Formaly", bg=BG_SECONDARY, fg="white", font=FONT_TITLE).pack(side="left", padx=10)

        # Search Bar UI wrapper
        search_frame = tk.Frame(navbar, bg=BG_ENTRY, bd=0, padx=15, pady=8)
        search_frame.pack(side="left", expand=True, padx=60)
        
        tk.Label(search_frame, text="⌕", bg=BG_ENTRY, fg=FG_SECONDARY, font=("Segoe UI", 14)).pack(side="left", padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, bg=BG_ENTRY, fg=FG_SECONDARY, 
                                     relief="flat", font=FONT_MAIN, width=35, insertbackground=FG_PRIMARY)
        self.search_entry.pack(side="left", ipady=2)
        self.search_entry.insert(0, "Search tasks, budgets, venues...")
        
        def on_search_focus_in(e):
            if self.search_entry.get() == "Search tasks, budgets, venues...":
                self.search_entry.delete(0, "end")
                self.search_entry.config(fg="white")
                search_frame.config(bg="#151515")
                self.search_entry.config(bg="#151515")
                
        def on_search_focus_out(e):
            if not self.search_entry.get():
                self.search_entry.insert(0, "Search tasks, budgets, venues...")
                self.search_entry.config(fg=FG_SECONDARY)
                search_frame.config(bg=BG_ENTRY)
                self.search_entry.config(bg=BG_ENTRY)
                
        self.search_entry.bind("<FocusIn>", on_search_focus_in)
        self.search_entry.bind("<FocusOut>", on_search_focus_out)

        # Minimalist vector-style profile icons
        profile_icon = tk.Label(navbar, text="👤", bg=BG_SECONDARY, fg=FG_SECONDARY, font=("Segoe UI", 14), cursor="hand2")
        profile_icon.pack(side="right", padx=25)
        notif_icon = tk.Label(navbar, text="🔔", bg=BG_SECONDARY, fg=FG_SECONDARY, font=("Segoe UI", 14), cursor="hand2")
        notif_icon.pack(side="right", padx=10)

        for icon in (profile_icon, notif_icon):
            icon.bind("<Enter>", lambda e, w=icon: w.config(fg=FG_PRIMARY))
            icon.bind("<Leave>", lambda e, w=icon: w.config(fg=FG_SECONDARY))

    def navigate_to_page(self, page_name):
        """Python Dynamic File Router."""
        # Convert item names to expected python script paths (e.g., 'Decor Planning' -> 'decor_planning.py')
        filename = page_name.lower().replace(' ', '_') + ".py"
        
        if not os.path.exists(filename):
            messagebox.showwarning("Routing Error", f"Target file assignment missing:\nCould not locate '{filename}' in directory.")
            return

        subprocess.Popen(["python", filename])
        self.destroy()

    def build_sidebar(self):
        self.sidebar = tk.Frame(self, bg=BG_SECONDARY, width=self.sidebar_width)
        self.sidebar.place(x=self.sidebar_x, y=65, height=635) 

        menu_items = [
            "Dashboard", "Budget", "Venues", "Guest Management", 
            "Decor Planning", "Reports", "Settings"
        ]

        tk.Label(self.sidebar, text="ADMIN MENU", bg=BG_SECONDARY, fg=FG_PRIMARY, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20, pady=(25, 10))

        for item in menu_items:
            is_active = (item == "Dashboard")
            btn = HoverButton(
                self.sidebar, item, 
                command=lambda page=item: self.navigate_to_page(page),
                width=22, pad_y=12,
                fg="white" if is_active else FG_SECONDARY,
                bg="#2A2A2A" if is_active else BG_SECONDARY
            )
            btn.pack(fill="x")

        # Explicit route for Log out link
        logout_btn = HoverButton(
            self.sidebar, "Log out", 
            command=lambda: self.navigate_to_page("formaly_login"),
            fg="#FF6B6B", width=22, pad_y=12
        )
        logout_btn.pack(side="bottom", fill="x", pady=25)

    def toggle_sidebar(self):
        if self.sidebar_open:
            self.animate_sidebar(0, -self.sidebar_width)
            self.sidebar_open = False
        else:
            self.animate_sidebar(-self.sidebar_width, 0)
            self.sidebar_open = True

    def animate_sidebar(self, start_x, end_x):
        step = 40 if end_x > start_x else -40
        current_x = start_x + step
        
        if (step > 0 and current_x >= end_x) or (step < 0 and current_x <= end_x):
            self.sidebar.place(x=end_x)
            return
            
        self.sidebar.place(x=current_x)
        self.after(8, lambda: self.animate_sidebar(current_x, end_x))

    def build_dashboard(self):
        header_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        header_frame.pack(fill="x", padx=45, pady=(35, 15))
        
        tk.Label(header_frame, text="Formal Planning Tasks", bg=BG_COLOR, fg="white", font=FONT_H1).pack(side="left")
        
        if self.current_user_role in ["Administrator", "Planners"]:
            add_btn = HoverButton(header_frame, "+ Add Task", command=self.open_add_task, bg=FG_PRIMARY, fg=BG_COLOR, hover_bg="#E5BA3D", font=FONT_BOLD)
            add_btn.pack(side="right")

        self.canvas = tk.Canvas(self.content_frame, bg=BG_COLOR, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.content_frame, orient="vertical", command=self.canvas.yview)
        
        self.tasks_container = tk.Frame(self.canvas, bg=BG_COLOR)
        
        # Force container matrix to maintain two exact structural halves
        self.tasks_container.grid_columnconfigure(0, weight=1, uniform="dashboard_grid")
        self.tasks_container.grid_columnconfigure(1, weight=1, uniform="dashboard_grid")

        self.tasks_container.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.tasks_container, anchor="nw")
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True, padx=(45, 0), pady=10)
        self.scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 25))
        
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def refresh_tasks(self):
        for widget in self.tasks_container.winfo_children():
            widget.destroy()
            
        tasks = formaly_database.get_all_tasks()
        
        # Staggered/Cascading Card Entrance Animation loop
        for i, task in enumerate(tasks):
            row = i // 2
            col = i % 2
            self.after(60 * i, lambda t=task, r=row, c=col: self.create_task_card(t, r, c))

    def create_task_card(self, task, row, col):
        is_completed = task['status'] == 'Completed'
        
        if is_completed:
            border_color = "#252525"
            prio_color = "#555555"
            title_color = "#666666"
            bg_color = "#121212"
        else:
            bg_color = BG_SECONDARY
            if task['priority'] == "High":
                border_color = FG_PRIMARY 
                prio_color = FG_PRIMARY
                title_color = "white"
            elif task['priority'] == "Medium":
                border_color = "#444444" 
                prio_color = "#D4AF37" 
                title_color = "#E0E0E0"
            else:
                border_color = BG_SECONDARY 
                prio_color = FG_SECONDARY
                title_color = FG_SECONDARY

        card_border = tk.Frame(self.tasks_container, bg=border_color, padx=2, pady=2)
        # Structural Grid Mapping using 100% of spatial container allocations
        card_border.grid(row=row, column=col, sticky="nsew", padx=12, pady=12)

        card = tk.Frame(card_border, bg=bg_color, padx=20, pady=18)
        card.pack(fill="both", expand=True)
        
        def enter_card(e, c=card):
            if is_completed:
                return
            c.config(bg="#2E2E2E", highlightthickness=1, highlightbackground=FG_PRIMARY)
        def leave_card(e, c=card):
            c.config(bg=bg_color, highlightthickness=0)
            
        card.bind("<Enter>", enter_card)
        card.bind("<Leave>", leave_card)

        top_row = tk.Frame(card, bg=card['bg'])
        top_row.pack(fill="x")
        top_row.bind("<Enter>", enter_card)
        
        title_font = ("Segoe UI", 14, "overstrike") if is_completed else ("Segoe UI", 14, "bold")
        tk.Label(top_row, text=task['title'], bg=card['bg'], fg=title_color, font=title_font).pack(side="left", anchor="w")

        # Action Buttons Layout (Top Right Corner of Task Cards)
        actions_frame = tk.Frame(top_row, bg=card['bg'])
        actions_frame.pack(side="right")
        
        if self.current_user_role == "Administrator":
            if not is_completed:
                btn_complete = tk.Label(actions_frame, text="✔️", bg=card['bg'], fg="#51CF66", font=("Segoe UI", 14, "bold"), cursor="hand2")
                btn_complete.pack(side="left", padx=3)
                btn_complete.bind("<Button-1>", lambda e, tid=task['task_id']: self.mark_complete(tid))
                
            btn_edit = tk.Label(actions_frame, text="✏️", bg=card['bg'], fg=FG_PRIMARY, font=("Segoe UI", 14), cursor="hand2")
            btn_edit.pack(side="left", padx=6)
            btn_edit.bind("<Button-1>", lambda e, t=task: self.open_edit_task(t))
            
            btn_del = tk.Label(actions_frame, text="✖️", bg=card['bg'], fg="#FF6B6B", font=("Segoe UI", 14), cursor="hand2")
            btn_del.pack(side="left", padx=6)
            btn_del.bind("<Button-1>", lambda e, tid=task['task_id']: self.delete_task(tid))

        desc_color = "#555555" if is_completed else FG_SECONDARY
        tk.Label(card, text=task['description'], bg=card['bg'], fg=desc_color, font=FONT_MAIN, wraplength=400, justify="left").pack(anchor="w", pady=(10, 15))

        # Modern Horizontal Data Pill Row
        meta_frame = tk.Frame(card, bg=card['bg'])
        meta_frame.pack(anchor="w", fill="x")
        meta_frame.bind("<Enter>", enter_card)
        
        def add_meta_pill(symbol, label_text, custom_fg):
            lbl = tk.Label(meta_frame, text=f"{symbol}  {label_text}", bg=card['bg'], fg=custom_fg, font=FONT_SMALL)
            lbl.pack(side="left", padx=(0, 18))

        add_meta_pill("❕", f"{task['priority']}", prio_color)
        if task['category']: 
            add_meta_pill("📂", task['category'], desc_color)
        if task['due_date']: 
            add_meta_pill("🗓️", task['due_date'], desc_color)
        if task['assigned_section']: 
            add_meta_pill("👤", task['assigned_section'], desc_color)

    def open_add_task(self):
        TaskModal(self, callback=self.refresh_tasks)

    def open_edit_task(self, task):
        TaskModal(self, task=task, callback=self.refresh_tasks)

    def mark_complete(self, task_id):
        formaly_database.mark_task_complete(task_id)
        self.refresh_tasks()

    def delete_task(self, task_id):
        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to permanently delete this task?"):
            formaly_database.delete_task(task_id)
            self.refresh_tasks()

if __name__ == "__main__":
    app = FormalyAdminApp()
    app.mainloop()