# Imports
import tkinter as tk
from tkinter import ttk


# Sets all the background colors
BG    = "#0D0D0D"          # page / window background
CARD  = "#1A1A1A"          # card background
ENTRY = "#252525"          # entry field / inner card background
BORDER = "#2E2E2E"         # dividers, widget borders

# Login page background colors
CREAM       = "#F0EAD6"    # right panel background
CREAM_FIELD = "#E4DCCA"    # entry field on cream panel

# Secondary colors
GOLD     = "#C9A227"       # primary gold
GOLD_HOV = "#A07D10"       # darker gold for hover

# Text
TEXT_LIGHT   = "#F0F0F0"   # primary text on dark backgrounds
TEXT_MUTED   = "#888888"   # secondary text on dark backgrounds
TEXT_DARK    = "#1A1A1A"   # primary text on light backgrounds
TEXT_ON_GOLD = "#FFFFFF"   # text sitting on a gold button

# Status colors
PRIMARY   = GOLD           
SECONDARY = TEXT_MUTED     
SUCCESS   = "#2E7D32"
ERROR     = "#C0392B"
WARNING   = "#E67E22"


# Headings
FONT_H1    = ("Georgia",   32, "bold")   # login/register 
FONT_H2    = ("Segoe UI",  20, "bold")   # dashboard welcome 
FONT_H3    = ("Segoe UI",  16, "bold")   # card title

# Body
FONT_BODY  = ("Segoe UI",  11)
FONT_BOLD  = ("Segoe UI",  11, "bold")
FONT_SMALL = ("Segoe UI",   9)

# Branding
FONT_BRAND = ("Georgia",   24, "bold")   # "Formaly"  label
FONT_STAT  = ("Segoe UI",  28, "bold")   # large stat numbers on cards

# Variable names for fonts
FONT     = FONT_BODY
TITLE    = FONT_H2
SUBTITLE = FONT_H3
SMALL    = FONT_SMALL

# Spacing
PADDING_X   = 20
PADDING_Y   = 15
CARD_RADIUS = 10 

# Role mapping for display
ROLE_MAP = {
    "Admin":   "admin",
    "Planner": "planner",
    "Support": "helper",
}

# This function applies the custom treeview style. 
def apply_treeview_style():
    style = ttk.Style()
    style.theme_use("default")

    # Custom style for Treeview widget used in Task pages
    style.configure(
        "Formaly.Treeview",
        background=ENTRY,
        foreground=TEXT_LIGHT,
        fieldbackground=ENTRY,
        rowheight=32,
        font=FONT_BODY,
    )

    # Custom style for headings
    style.configure(
        "Formaly.Treeview.Heading",
        background=CARD,
        foreground=GOLD,
        font=FONT_BOLD,
        relief="flat",
    )

    # Custom style for selected row
    style.map(
        "Formaly.Treeview",
        background=[("selected", GOLD)],
        foreground=[("selected", TEXT_ON_GOLD)],
    )

# This function creates a button with the specified text, command and style.
def make_button(parent, text, command, style="primary", **kw):
    colours = {
        "primary": (GOLD,     TEXT_ON_GOLD, GOLD_HOV),
        "dark":    (ENTRY,    TEXT_LIGHT,   BORDER),
        "danger":  (ERROR,    TEXT_ON_GOLD, "#922B21"),
        "ghost":   (BG,       TEXT_MUTED,   CARD),
    }
    bg, fg, hov = colours.get(style, colours["primary"])
    btn = tk.Button(
        parent, text=text, command=command,
        bg=bg, fg=fg, activebackground=hov, activeforeground=fg,
        font=FONT_BOLD, relief="flat", cursor="hand2", **kw
    )

    # Add hover effect
    btn.bind("<Enter>", lambda e: btn.config(bg=hov))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn

# This function disables a widget by setting its state to "disabled" which causes it to appear grayed out.
def make_label(parent, text, style="body", anchor="w", **kw):
    fonts = {
        "h1":    FONT_H1,
        "h2":    FONT_H2,
        "h3":    FONT_H3,
        "body":  FONT_BODY,
        "bold":  FONT_BOLD,
        "small": FONT_SMALL,
        "brand": FONT_BRAND,
        "stat":  FONT_STAT,
    }
    return tk.Label(
        parent, text=text, font=fonts.get(style, FONT_BODY),
        anchor=anchor, **kw
    )

# Creating a styled entry field
def make_entry(parent, show=None, width=30, **kw):
    return tk.Entry(
        parent,
        bg=ENTRY, fg=TEXT_LIGHT,
        insertbackground=TEXT_LIGHT,
        relief="flat", font=FONT_BODY,
        show=show, width=width,
        **kw
    )

#Creating a horizontal seperator
def make_separator(parent, orient="horizontal", colour=BORDER, thickness=1):
    if orient == "horizontal":
        return tk.Frame(parent, bg=colour, height=thickness)
    return tk.Frame(parent, bg=colour, width=thickness)