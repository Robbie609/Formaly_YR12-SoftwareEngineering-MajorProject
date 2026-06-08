import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from utils.styles import (
    BG, CARD, ENTRY, BORDER, GOLD, GOLD_HOV,
    TEXT_LIGHT, TEXT_MUTED, ERROR, SUCCESS,
    FONT_BODY, FONT_BOLD, FONT_H3, FONT_SMALL,
)
from utils.widgets import build_subpage_header, scrollable_frame, make_modal, modal_field, navigate
from utils.helpers import truncate_text, clear_frame

_PRIORITY_COL = {"High": "#E53935", "Medium": "#FB8C00", "Low": "#43A047"}
_STATUS_COL   = {"Pending": "#888888", "In Progress": GOLD, "Completed": SUCCESS}


class TaskPage(tk.Frame):
    def __init__(self, parent, controller=None, user=None):
        super().__init__(parent, bg=BG)
        self.parent = parent
        self.user   = user
        self._imgs  = []
        self._filter_priority = "All"
        self._filter_status   = "All"
        self._sort_by         = "Due Date"
        self._build()

    def _back(self):
        navigate(self, self.parent, "planner", self.user)

    def _build(self):
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        header_container = tk.Frame(self, bg=BG)
        header_container.pack(fill="x")
        build_subpage_header(header_container, "TASKS DIRECTORY", self._back, self._imgs)

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)
        body.rowconfigure(1, weight=1)
        body.columnconfigure(0, weight=1)

        # Filter bar
        fbar = tk.Frame(body, bg=BG)
        fbar.grid(row=0, column=0, sticky="ew", padx=24, pady=14)

        tk.Label(fbar, text="SORT BY", bg=BG, fg=TEXT_LIGHT,
                 font=FONT_BOLD).pack(side="left", padx=(0, 20))

        self._make_dropdown(fbar, "Priority:", ["All","High","Medium","Low"], "_filter_priority")
        self._make_dropdown(fbar, "Status:",   ["All","Pending","In Progress","Completed"], "_filter_status")
        self._make_dropdown(fbar, "Sort:",     ["Due Date","Priority"], "_sort_by")

        tk.Button(fbar, text="+ Create Task", bg=GOLD, fg=TEXT_LIGHT,
                  font=FONT_BOLD, relief="flat", cursor="hand2",
                  activebackground=GOLD_HOV, padx=16, pady=6,
                  command=self._open_modal).pack(side="right")

        # Scrollable task list
        self._scroll_inner = scrollable_frame(body)
        self._scroll_inner.columnconfigure(0, weight=1)
        self._refresh()

    def _make_dropdown(self, parent, label, choices, attr):
        tk.Label(parent, text=label, bg=BG, fg=TEXT_MUTED, font=FONT_SMALL).pack(side="left", padx=(12, 4))
        var = tk.StringVar(value=getattr(self, attr))
        cb = ttk.Combobox(parent, textvariable=var, values=choices, state="readonly", width=11)
        cb.pack(side="left", padx=(0, 8))
        def _on(e):
            setattr(self, attr, var.get())
            self._refresh()
        cb.bind("<<ComboboxSelected>>", _on)

    def _refresh(self):
        clear_frame(self._scroll_inner)

        q = "SELECT task_id, title, description, priority, category, status, due_date FROM tasks WHERE 1=1"
        p = []
        if self._filter_priority != "All":
            q += " AND priority=?"; p.append(self._filter_priority)
        if self._filter_status != "All":
            q += " AND status=?";   p.append(self._filter_status)
        q += (" ORDER BY due_date ASC" if self._sort_by == "Due Date"
              else " ORDER BY CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END")

        conn = sqlite3.connect("database/formaly.db")
        cur  = conn.cursor()
        cur.execute(q, p)
        tasks = cur.fetchall()
        conn.close()

        if not tasks:
            tk.Label(self._scroll_inner, text="No tasks found.", bg=BG, fg=TEXT_MUTED,
                     font=FONT_H3).pack(pady=60)
            return

        for task_id, title, desc, priority, category, status, due in tasks:
            card = tk.Frame(self._scroll_inner, bg=CARD)
            card.pack(fill="x", padx=24, pady=6)

            top = tk.Frame(card, bg=CARD)
            top.pack(fill="x", padx=16, pady=(12, 4))
            tk.Label(top, text=title, bg=CARD, fg=GOLD,
                     font=FONT_BOLD).pack(side="left")

            edit_btn = tk.Button(top, text="Edit", bg=GOLD, fg=TEXT_LIGHT,
                                 font=FONT_SMALL, relief="flat", cursor="hand2",
                                 activebackground=GOLD_HOV, padx=12, pady=4,
                                 command=lambda tid=task_id, t=title, d=desc,
                                         pr=priority, du=due, s=status, c=category:
                                         self._open_modal(tid, t, d, pr, c, du, s))
            edit_btn.pack(side="right", padx=(4, 0))
            del_btn = tk.Button(top, text="Delete", bg=ERROR, fg=TEXT_LIGHT,
                                font=FONT_SMALL, relief="flat", cursor="hand2",
                                padx=12, pady=4,
                                command=lambda tid=task_id: self._delete(tid))
            del_btn.pack(side="right")

            tk.Label(card, text=desc or "", bg=CARD, fg=TEXT_MUTED,
                     font=FONT_BODY, anchor="w",
                     wraplength=900).pack(fill="x", padx=16, pady=(0, 8))

            meta = tk.Frame(card, bg=CARD)
            meta.pack(fill="x", padx=16, pady=(0, 12))
            p_col = _PRIORITY_COL.get(priority, BORDER)
            s_col = _STATUS_COL.get(status, BORDER)
            tk.Label(meta, text=f"Priority: {priority}", bg=p_col, fg=TEXT_LIGHT,
                     font=FONT_SMALL, padx=8, pady=3).pack(side="left")
            tk.Label(meta, text=f"Status: {status}", bg=s_col, fg=CARD,
                     font=FONT_SMALL, padx=8, pady=3).pack(side="left", padx=6)
            tk.Label(meta, text=f"Due: {due or '—'}", bg=CARD, fg=TEXT_MUTED,
                     font=FONT_SMALL).pack(side="left", padx=4)

    def _open_modal(self, task_id=None, title="", desc="", priority="Medium",
                    category="", due="", status="Pending"):
        from datetime import date
        m = make_modal(self, "Edit Task" if task_id else "Create Task", 460, 520)
        f = tk.Frame(m, bg=BG, padx=22, pady=22)
        f.pack(fill="both", expand=True)

        t_ent  = modal_field(f, "Title",       title)
        d_ent  = modal_field(f, "Description", desc, height=3)

        row = tk.Frame(f, bg=BG)
        row.pack(fill="x", pady=(10, 0))
        row.columnconfigure((0, 1), weight=1)

        tk.Label(row, text="Priority", bg=BG, fg=GOLD, font=FONT_BOLD).grid(row=0, column=0, sticky="w")
        p_var = tk.StringVar(value=priority)
        ttk.Combobox(row, textvariable=p_var, values=["High","Medium","Low"],
                     state="readonly").grid(row=1, column=0, sticky="ew", padx=(0, 6), pady=4)

        tk.Label(row, text="Status", bg=BG, fg=GOLD, font=FONT_BOLD).grid(row=0, column=1, sticky="w")
        s_var = tk.StringVar(value=status)
        ttk.Combobox(row, textvariable=s_var, values=["Pending","In Progress","Completed"],
                     state="readonly").grid(row=1, column=1, sticky="ew", padx=(6, 0), pady=4)

        due_ent = modal_field(f, "Due Date (YYYY-MM-DD)", due or str(date.today()))

        def _save():
            t = t_ent.get().strip()
            if not t:
                messagebox.showerror("Error", "Title is required."); return
            d_val  = d_ent.get("1.0", "end-1c").strip() if hasattr(d_ent, "get") and callable(getattr(d_ent, "get")) else d_ent.get().strip()
            conn   = sqlite3.connect("database/formaly.db")
            cur    = conn.cursor()
            if task_id:
                cur.execute("UPDATE tasks SET title=?,description=?,priority=?,status=?,due_date=?,category=? WHERE task_id=?",
                            (t, d_val, p_var.get(), s_var.get(), due_ent.get().strip(), category, task_id))
            else:
                cur.execute("INSERT INTO tasks (title,description,priority,category,status,due_date,assigned_section) VALUES (?,?,?,?,?,?,?)",
                            (t, d_val, p_var.get(), category, s_var.get(), due_ent.get().strip(), ""))
            conn.commit(); conn.close()
            m.destroy(); self._refresh()

        btns = tk.Frame(f, bg=BG)
        btns.pack(fill="x", pady=(16, 0))
        tk.Button(btns, text="Save", bg=GOLD, fg=TEXT_LIGHT, font=FONT_BOLD,
                  relief="flat", cursor="hand2", activebackground=GOLD_HOV,
                  padx=16, pady=8, command=_save).pack(side="right")
        tk.Button(btns, text="Cancel", bg=ENTRY, fg=TEXT_LIGHT, font=FONT_BODY,
                  relief="flat", cursor="hand2",
                  padx=16, pady=8, command=m.destroy).pack(side="right", padx=(0, 8))

    def _delete(self, task_id):
        if messagebox.askyesno("Delete", "Delete this task?"):
            conn = sqlite3.connect("database/formaly.db")
            conn.execute("DELETE FROM tasks WHERE task_id=?", (task_id,))
            conn.commit(); conn.close()
            self._refresh()