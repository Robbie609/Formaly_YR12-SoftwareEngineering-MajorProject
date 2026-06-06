# pages/planner/venue_suggestion_page.py

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

from utils.styles import (
    BG, CARD, ENTRY, PRIMARY, SECONDARY, SUCCESS, ERROR, BORDER,
    FONT, FONT_BOLD, TITLE, SUBTITLE, SMALL, PADDING_X, PADDING_Y
)
from utils.helpers import clear_frame, truncate_text

class VenueSuggestionPage(tk.Frame):
    def __init__(self, parent, user=None):
        super().__init__(parent, bg=BG)
        self.parent = parent
        self.user = user
        
        self.search_query = ""
        self.setup_layout()

    def setup_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar Component
        self.sidebar = tk.Frame(self, bg=CARD, width=260, bd=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        # Workspace Wrapper Panel
        self.main_content = tk.Frame(self, bg=BG)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=PADDING_X, pady=PADDING_Y)
        self.main_content.grid_rowconfigure(2, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)

        from pages.planner.planner_dashboard import PlannerDashboard
        PlannerDashboard.render_sidebar(self, "Venue Suggestions")
        self.render_venue_workspace()

    def render_venue_workspace(self):
        clear_frame(self.main_content)
        
        # Action Bar Top Section
        top_bar = tk.Frame(self.main_content, bg=BG)
        top_bar.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        # Matrix Grid Scroll Frame Wrapper Layout
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

        self.display_venues()

    def update_search(self, event):
        self.search_query = self.search_ent.get()
        self.display_venues()

    def display_venues(self):
        clear_frame(self.scroll_frame)
        self.scroll_frame.grid_columnconfigure((0, 1), weight=1, uniform="equal")

        conn = sqlite3.connect("database/formaly.db")
        cursor = conn.cursor()
        
        query = "SELECT id, name, address, capacity, estimated_cost, notes, status FROM venues WHERE 1=1"
        params = []

        if self.search_query:
            query += " AND (name LIKE ? OR address LIKE ? OR notes LIKE ?)"
            params.extend([f"%{self.search_query}%", f"%{self.search_query}%", f"%{self.search_query}%"])

        query += " ORDER BY id DESC"
        cursor.execute(query, params)
        venues = cursor.fetchall()
        conn.close()

        if not venues:
            empty_lbl = tk.Label(self.scroll_frame, text="No items logged in database indices.", font=SUBTITLE, fg=SECONDARY, bg=BG)
            empty_lbl.grid(row=0, column=0, columnspan=2, pady=60)
            return

        for idx, (vid, name, addr, cap, cost, notes, status) in enumerate(venues):
            r = idx // 2
            c = idx % 2
            
            card_border = tk.Frame(self.scroll_frame, bg=BORDER, padx=1, pady=1)
            card_border.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
            
            card = tk.Frame(card_border, bg=CARD, padx=16, pady=16)
            card.pack(fill="both", expand=True)
            card.grid_rowconfigure(3, weight=1)
            card.grid_columnconfigure(0, weight=1)

            # Header details
            title_row = tk.Frame(card, bg=CARD)
            title_row.pack(fill="x", pady=(0, 6))
            
            n_lbl = tk.Label(title_row, text=truncate_text(name, 22), font=FONT_BOLD, fg=PRIMARY, bg=CARD)
            n_lbl.pack(side="left", anchor="w")
            
            s_color = SUCCESS if status == "Approved" else (ERROR if status == "Rejected" else SECONDARY)
            s_badge = tk.Label(title_row, text=f" {status} ", font=SMALL, fg=CARD, bg=s_color, padx=4)
            s_badge.pack(side="right")

            a_lbl = tk.Label(card, text=truncate_text(addr, 40), font=SMALL, fg=SECONDARY, bg=CARD)
            a_lbl.pack(anchor="w", pady=(0, 10))

            # Numeric Spec Metrics
            specs_frame = tk.Frame(card, bg=BG, padx=10, pady=8)
            specs_frame.pack(fill="x", pady=(0, 10))
            
            cap_lbl = tk.Label(specs_frame, text=f"Capacity: {cap} guests", font=FONT, fg=PRIMARY, bg=BG)
            cap_lbl.pack(side="left")
            
            cost_lbl = tk.Label(specs_frame, text=f"${cost:,.2f}", font=FONT_BOLD, fg=SUCCESS, bg=BG)
            cost_lbl.pack(side="right")

            # Description notes block
            n_txt = tk.Label(card, text=truncate_text(notes, 120) if notes else "No notes logged for profile.",
                             font=FONT, fg=SECONDARY, bg=CARD, justify="left", wraplength=300)
            n_txt.pack(anchor="w", fill="both", expand=True, pady=(0, 14))

            # Control button layout split line
            sep = tk.Frame(card, bg=BORDER, height=1)
            sep.pack(fill="x", pady=(0, 12))

            actions_bar = tk.Frame(card, bg=CARD)
            actions_bar.pack(fill="x")

            edit_btn = tk.Button(
                actions_bar, text="Modify Profile", font=SMALL, fg=CARD, bg=PRIMARY,
                activebackground=BG, activeforeground=PRIMARY, bd=0, relief="flat", padx=10, pady=4,
                command=lambda val_id=vid, n=name, a=addr, cp=cap, cs=cost, nt=notes, st=status: self.open_venue_modal(val_id, n, a, cp, cs, nt, st)
            )
            edit_btn.pack(side="left", padx=2)

            del_btn = tk.Button(
                actions_bar, text="Delete", font=SMALL, fg=CARD, bg=ERROR,
                activebackground=BG, activeforeground=ERROR, bd=0, relief="flat", padx=10, pady=4,
                command=lambda val_id=vid: self.delete_venue(val_id)
            )
            del_btn.pack(side="right", padx=2)

    def delete_venue(self, venue_id):
        if messagebox.askyesno("Confirm Action", "Are you sure you want to remove this venue from records?"):
            conn = sqlite3.connect("database/formaly.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM venues WHERE id = ?", (venue_id,))
            conn.commit()
            conn.close()
            self.display_venues()

    def open_venue_modal(self, venue_id=None, name="", address="", capacity=100, cost=0.0, notes="", status="Under Review"):
        modal = tk.Toplevel(self)
        modal.title("Venue Matrix Profile Configuration Editor")
        modal.geometry("480x580")
        modal.configure(bg=BG)
        modal.transient(self)
        modal.grab_set()
        modal.resizable(False, False)

        container = tk.Frame(modal, bg=BG, padx=24, pady=24)
        container.pack(fill="both", expand=True)

        header_lbl = tk.Label(container, text="Venue Data Profile Workspace" if venue_id else "Register Venue Profile Asset", font=SUBTITLE, fg=PRIMARY, bg=BG)
        header_lbl.pack(anchor="w", pady=(0, 16))

        # Forms Setup
        tk.Label(container, text="Venue Title Designation Name", font=FONT_BOLD, fg=PRIMARY, bg=BG).pack(anchor="w", pady=(6, 2))
        n_border = tk.Frame(container, bg=BORDER, padx=1, pady=1)
        n_border.pack(fill="x")
        name_ent = tk.Entry(n_border, font=FONT, bg=ENTRY, fg=PRIMARY, bd=0)
        name_ent.pack(fill="x", padx=8, pady=6)
        name_ent.insert(0, name)

        tk.Label(container, text="Physical Address Info Location", font=FONT_BOLD, fg=PRIMARY, bg=BG).pack(anchor="w", pady=(10, 2))
        a_border = tk.Frame(container, bg=BORDER, padx=1, pady=1)
        a_border.pack(fill="x")
        addr_ent = tk.Entry(a_border, font=FONT, bg=ENTRY, fg=PRIMARY, bd=0)
        addr_ent.pack(fill="x", padx=8, pady=6)
        addr_ent.insert(0, address)

        numerical_row = tk.Frame(container, bg=BG)
        numerical_row.pack(fill="x", pady=(10, 0))
        numerical_row.grid_columnconfigure((0, 1), weight=1)

        cap_frame = tk.Frame(numerical_row, bg=BG)
        cap_frame.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        tk.Label(cap_frame, text="Max Occupancy Cap", font=FONT_BOLD, fg=PRIMARY, bg=BG).pack(anchor="w")
        cap_border = tk.Frame(cap_frame, bg=BORDER, padx=1, pady=1)
        cap_border.pack(fill="x", pady=4)
        cap_ent = tk.Entry(cap_border, font=FONT, bg=ENTRY, fg=PRIMARY, bd=0)
        cap_ent.pack(fill="x", padx=8, pady=6)
        cap_ent.insert(0, str(capacity))

        cost_frame = tk.Frame(numerical_row, bg=BG)
        cost_frame.grid(row=0, column=1, sticky="ew", padx=(6, 0))
        tk.Label(cost_frame, text="Estimated Cost Summary", font=FONT_BOLD, fg=PRIMARY, bg=BG).pack(anchor="w")
        cost_border = tk.Frame(cost_frame, bg=BORDER, padx=1, pady=1)
        cost_border.pack(fill="x", pady=4)
        cost_ent = tk.Entry(cost_border, font=FONT, bg=ENTRY, fg=PRIMARY, bd=0)
        cost_ent.pack(fill="x", padx=8, pady=6)
        cost_ent.insert(0, str(cost))

        tk.Label(container, text="Verification Workflow Evaluation Status", font=FONT_BOLD, fg=PRIMARY, bg=BG).pack(anchor="w", pady=(10, 2))
        s_var = tk.StringVar(value=status)
        s_cb = ttk.Combobox(container, textvariable=s_var, values=["Under Review", "Approved", "Rejected"], state="readonly")
        s_cb.pack(fill="x", pady=4)

        tk.Label(container, text="Profile Logs Review Description Notes", font=FONT_BOLD, fg=PRIMARY, bg=BG).pack(anchor="w", pady=(10, 2))
        nt_border = tk.Frame(container, bg=BORDER, padx=1, pady=1)
        nt_border.pack(fill="x")
        notes_txt = tk.Text(nt_border, font=FONT, bg=ENTRY, fg=PRIMARY, bd=0, height=3, highlightthickness=0)
        notes_txt.pack(fill="x", padx=8, pady=6)
        notes_txt.insert("1.0", notes)

        # Footer Button Layout Control Frame
        actions_panel = tk.Frame(container, bg=BG)
        actions_panel.pack(fill="x", side="bottom", pady=(16, 0))

        def commit_save():
            n_val = name_ent.get().strip()
            a_val = addr_ent.get().strip()
            nt_val = notes_txt.get("1.0", "end-1c").strip()
            s_val = s_var.get()
            
            try:
                cap_val = int(cap_ent.get().strip())
                cost_val = float(cost_ent.get().strip())
            except ValueError:
                messagebox.showerror("Validation Formatting Error", "Capacity must evaluate to integer, Cost must match structural decimal standard values.")
                return

            if not n_val:
                messagebox.showerror("Validation Error", "Venue Designation Title Field cannot resolve as blank.")
                return

            conn = sqlite3.connect("database/formaly.db")
            cursor = conn.cursor()
            if venue_id:
                cursor.execute("""
                    UPDATE venues SET name=?, address=?, capacity=?, estimated_cost=?, notes=?, status=? WHERE id=?
                """, (n_val, a_val, cap_val, cost_val, nt_val, s_val, venue_id))
            else:
                cursor.execute("""
                    INSERT INTO venues (name, address, capacity, estimated_cost, notes, status) VALUES (?, ?, ?, ?, ?, ?)
                """, (n_val, a_val, cap_val, cost_val, nt_val, s_val))
            conn.commit()
            conn.close()
            modal.destroy()
            self.display_venues()

        submit_btn = tk.Button(
            actions_panel, text="Publish Document Profile", font=FONT_BOLD, fg=CARD, bg=PRIMARY,
            activebackground=SECONDARY, activeforeground=CARD, bd=0, relief="flat", padx=16, pady=8,
            command=commit_save
        )
        submit_btn.pack(side="right")

        cancel_btn = tk.Button(
            actions_panel, text="Dismiss", font=FONT_BOLD, fg=PRIMARY, bg=BG,
            activebackground=BORDER, activeforeground=PRIMARY, bd=0, relief="flat", padx=16, pady=8,
            command=modal.destroy
        )
        cancel_btn.pack(side="right", padx=12)