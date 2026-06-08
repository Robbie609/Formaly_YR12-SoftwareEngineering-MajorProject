import tkinter as tk
from utils.styles import (
    BG, CARD, ENTRY, BORDER, GOLD, GOLD_HOV,
    TEXT_LIGHT, TEXT_MUTED, TEXT_ON_GOLD,
    ERROR, SUCCESS, FONT_BODY, FONT_BOLD,
    FONT_H2, FONT_H3, FONT_SMALL, FONT_BRAND, FONT_STAT,
)

LOGO_PATH = "assets/Logo.png"
SIDEBAR_W = 200
HEADER_H  = 130
HDR_BG    = "#0B0B0B"


def build_sidebar(parent, nav_items, active, on_navigate, imgs):
    sb = tk.Frame(parent, bg=CARD, width=SIDEBAR_W)
    sb.pack(side="left", fill="y")
    sb.pack_propagate(False)

    logo_frame = tk.Frame(sb, bg=CARD, height=HEADER_H)
    logo_frame.pack(fill="x")
    logo_frame.pack_propagate(False)
    try:
        img = tk.PhotoImage(file=LOGO_PATH)
        imgs.append(img)
        tk.Label(logo_frame, image=img, bg=CARD).pack(expand=True)
    except tk.TclError:
        tk.Label(logo_frame, text="Formaly", bg=CARD, fg=GOLD,
                 font=FONT_BRAND).pack(expand=True)

    tk.Frame(sb, bg=GOLD, height=1).pack(fill="x")

    for label in nav_items:
        is_active = (label == active)
        row_bg = "#222222" if is_active else CARD
        row = tk.Frame(sb, bg=row_bg)
        row.pack(fill="x")
        if is_active:
            tk.Frame(row, bg=GOLD, width=4).pack(side="left", fill="y")
        lbl = tk.Label(row,
                       text=label.upper() if is_active else label,
                       bg=row_bg,
                       fg=GOLD if is_active else TEXT_LIGHT,
                       font=FONT_BOLD if is_active else FONT_BODY,
                       anchor="w", cursor="hand2")
        lbl.pack(side="left", fill="x", expand=True,
                 padx=(12 if is_active else 16, 0), pady=14)
        if not is_active:
            for w in (row, lbl):
                w.bind("<Button-1>", lambda e, t=label: on_navigate(t))
                w.bind("<Enter>",  lambda e, r=row, l=lbl: (r.config(bg="#222"), l.config(bg="#222")))
                w.bind("<Leave>",  lambda e, r=row, l=lbl: (r.config(bg=CARD),  l.config(bg=CARD)))

    tk.Frame(sb, bg=CARD).pack(fill="both", expand=True)
    tk.Frame(sb, bg=BORDER, height=1).pack(fill="x")

    lo_row = tk.Frame(sb, bg=CARD)
    lo_row.pack(fill="x")
    tk.Frame(lo_row, bg=ERROR, width=4).pack(side="left", fill="y")
    lo_lbl = tk.Label(lo_row, text="LOG OUT", bg=CARD, fg=ERROR,
                      font=FONT_BOLD, anchor="w", cursor="hand2")
    lo_lbl.pack(side="left", fill="x", expand=True, padx=12, pady=14)
    for w in (lo_row, lo_lbl):
        w.bind("<Button-1>", lambda e: on_navigate("logout"))
        w.bind("<Enter>",  lambda e, r=lo_row, l=lo_lbl: (r.config(bg="#2a0a0a"), l.config(bg="#2a0a0a")))
        w.bind("<Leave>",  lambda e, r=lo_row, l=lo_lbl: (r.config(bg=CARD),     l.config(bg=CARD)))


def build_header(parent, title, subtitle, imgs):
    bar = tk.Frame(parent, bg=HDR_BG, height=HEADER_H)
    bar.pack(fill="x")
    bar.pack_propagate(False)
    try:
        img = tk.PhotoImage(file="")
        imgs.append(img)
        tk.Label(bar, image=img, bg=HDR_BG).pack(side="left", padx=(20, 0))
    except tk.TclError:
        pass
    mid = tk.Frame(bar, bg=HDR_BG)
    mid.pack(side="left", padx=24, expand=True, fill="both")
    tk.Label(mid, text=title,    bg=HDR_BG, fg=GOLD,       font=FONT_H2,  anchor="w").pack(anchor="w", pady=(28, 0))
    tk.Label(mid, text=subtitle, bg=HDR_BG, fg=TEXT_LIGHT, font=FONT_BODY, anchor="w").pack(anchor="w")
    icons = tk.Frame(bar, bg=HDR_BG)
    icons.pack(side="right", padx=24)
    tk.Label(icons, text="🔔", bg=HDR_BG, fg=TEXT_LIGHT, font=("Segoe UI Emoji", 18)).pack(side="left", padx=6)
    tk.Label(icons, text="👤", bg=HDR_BG, fg=GOLD,       font=("Segoe UI Emoji", 22)).pack(side="left", padx=6)


def build_subpage_header(parent, title, on_back, imgs):
    bar = tk.Frame(parent, bg=HDR_BG, height=HEADER_H)
    bar.pack(fill="x")
    bar.pack_propagate(False)
    back = tk.Frame(bar, bg="#1A1A1A", width=100)
    back.pack(side="left", fill="y")
    back.pack_propagate(False)
    tk.Button(back, text="←", bg="#1A1A1A", fg=TEXT_LIGHT,
              font=("Segoe UI", 20, "bold"), relief="flat", cursor="hand2",
              command=on_back, activebackground="#252525",
              activeforeground=GOLD).place(relx=0.5, rely=0.5, anchor="center")
    mid = tk.Frame(bar, bg=HDR_BG)
    mid.pack(side="left", padx=24, expand=True, fill="both")
    tk.Label(mid, text=title, bg=HDR_BG, fg=GOLD,
             font=("Segoe UI", 22, "bold"), anchor="w").pack(anchor="w", pady=(36, 0))
    icons = tk.Frame(bar, bg=HDR_BG)
    icons.pack(side="right", padx=24)
    tk.Label(icons, text="🔔", bg=HDR_BG, fg=TEXT_LIGHT, font=("Segoe UI Emoji", 18)).pack(side="left", padx=6)
    tk.Label(icons, text="👤", bg=HDR_BG, fg=GOLD,       font=("Segoe UI Emoji", 22)).pack(side="left", padx=6)


def stat_card(parent, label, value, col, total_cols, pad=10):
    card = tk.Frame(parent, bg=CARD)

    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0 if col == 0 else pad,
              0 if col == total_cols - 1 else pad)
    )

    tk.Label(
        card,
        text=label,
        bg=CARD,
        fg=TEXT_LIGHT,
        font=FONT_BODY,
        anchor="w"
    ).pack(anchor="w", padx=18, pady=(18, 4))

    tk.Label(
        card,
        text=str(value),
        bg=CARD,
        fg=GOLD,
        font=FONT_STAT,
        anchor="w"
    ).pack(anchor="w", padx=18, pady=(0, 18))

    return card


def scrollable_frame(parent, bg=None):
    bg = bg or BG
    outer = tk.Frame(parent, bg=bg)
    canvas = tk.Canvas(outer, bg=bg, bd=0, highlightthickness=0)
    sb = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    inner = tk.Frame(canvas, bg=bg)
    inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    win = canvas.create_window((0, 0), window=inner, anchor="nw")
    canvas.configure(yscrollcommand=sb.set)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width=e.width))
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    canvas.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")
    outer.pack(fill="both", expand=True)
    return inner


def make_modal(parent, title_text, w=460, h=500):
    m = tk.Toplevel(parent)
    m.title(title_text)
    m.configure(bg=BG)
    m.transient(parent)
    m.grab_set()
    m.resizable(False, False)
    sw, sh = m.winfo_screenwidth(), m.winfo_screenheight()
    m.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
    return m


def modal_field(parent, label, initial="", show=None, height=None):
    tk.Label(parent, text=label, bg=BG, fg=GOLD, font=FONT_BOLD, anchor="w").pack(fill="x", pady=(10, 2))
    border = tk.Frame(parent, bg=BORDER, padx=1, pady=1)
    border.pack(fill="x")
    if height:
        w = tk.Text(border, font=FONT_BODY, bg=ENTRY, fg=TEXT_LIGHT,
                    bd=0, height=height, insertbackground=TEXT_LIGHT)
        w.pack(fill="x", padx=6, pady=5)
        if initial:
            w.insert("1.0", initial)
    else:
        w = tk.Entry(border, font=FONT_BODY, bg=ENTRY, fg=TEXT_LIGHT,
                     bd=0, show=show or "", insertbackground=TEXT_LIGHT)
        w.pack(fill="x", padx=6, pady=5)
        if initial:
            w.insert(0, initial)
    return w


def navigate(current_frame, parent, target, user=None):
    current_frame.destroy()
    if target == "logout":
        for child in parent.winfo_children():
            child.destroy()
        if hasattr(parent, "_build"):
            parent._build()
        elif hasattr(parent, "build_ui"):
            parent.build_ui()
        return
    page_map = {
        "tasks":      ("pages.planner.task_page",        "TaskPage",            {"user": user}),
        "venues":     ("pages.planner.venue_page",        "VenueSuggestionPage", {"user": user}),
        "attendance": ("pages.support.attendance_page",   "AttendancePage",      {"user": user}),
        "reports":    ("pages.admin.reports_page",        "ReportsPage",         {"user": user}),
        "admin":      ("pages.admin.admin_dashboard",     "AdminDashboard",      {"user": user}),
        "planner":    ("pages.planner.planner_dashboard", "PlannerDashboard",    {"user": user}),
        "support":    ("pages.support.support_dashboard", "SupportDashboard",    {"user": user}),
        "invitation": ("pages.attendee.attendee_dashboard","FormalInvitationPage",{"user": user}),
        "feedback":   ("pages.attendee.feedback_page",    "FormalFeedbackPage",  {"user": user}),
    }
    if target not in page_map:
        return
    module_path, class_name, kwargs = page_map[target]
    import importlib
    mod = importlib.import_module(module_path)
    cls = getattr(mod, class_name)
    page = cls(parent, **kwargs)
    page.place(relwidth=1, relheight=1)
    page.lift()