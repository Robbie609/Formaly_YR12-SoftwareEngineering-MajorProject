import tkinter as tk
from datetime import datetime


# ---------------- WINDOW HELPERS ----------------
def center_window(window, width, height):
    """Centers a Tkinter window on screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")


# ---------------- WIDGET HELPERS ----------------
def clear_frame(frame):
    """Destroys all widgets inside a frame."""
    for widget in frame.winfo_children():
        widget.destroy()


# ---------------- TEXT / FORMAT HELPERS ----------------
def format_date(date_str):
    """
    Converts YYYY-MM-DD → readable format.
    If invalid, returns original string.
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d %b %Y")
    except:
        return date_str


def truncate_text(text, max_length=40):
    """Shortens long text for UI display."""
    text = str(text)
    return text if len(text) <= max_length else text[:max_length] + "..."


# ---------------- SIMPLE UI HELPERS ----------------
def disable_widget(widget):
    try:
        widget.config(state="disabled")
    except:
        pass


def enable_widget(widget):
    try:
        widget.config(state="normal")
    except:
        pass