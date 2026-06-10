# Imports
import tkinter as tk
from datetime import datetime

# This function centers a tkinter window on the screen by calculating the appropriate x and y coordinates based on the screen size and the desired window size.
def center_window(window, width, height):
    sw = window.winfo_screenwidth()
    sh = window.winfo_screenheight()
    x = (sw - width)  // 2
    y = (sh - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

# This function clears all child widgets
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# This function formats a date string from "YYYY-MM-DD" to "DD MMM YYYY" format
def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d %b %Y")
    except Exception:
        return date_str or ""

# This function checks if a value is empty (None, empty string, or only whitespace)
def truncate_text(text, max_length=40):
    text = str(text)
    return text if len(text) <= max_length else text[:max_length] + "..."

# This function formats a numeric value as a currency string with a dollar sign and two decimal places
def format_currency(value):
    try:
        return f"${float(value):,.2f}"
    except (TypeError, ValueError):
        return str(value)

# This function disables a widget by setting its state to "disabled"
def disable_widget(widget):
    try:
        widget.config(state="disabled")
    except Exception:
        pass

# This function enables a widget by setting its state to "normal"
def enable_widget(widget):
    try:
        widget.config(state="normal")
    except Exception:
        pass

# This class wraps a tk.Entry widget to provide placeholder text functionality, allowing the entry to show a placeholder when empty and clear it when focused.
class PlaceholderEntry:

    # This function initialises the PlaceholderEntry with the widget
    def __init__(self, widget, placeholder, fg_normal="#1A1A1A",
                 fg_placeholder="#888888", show_char=None):
        self.widget      = widget
        self.placeholder = placeholder
        self.fg_normal   = fg_normal
        self.fg_ph       = fg_placeholder
        self.show_char   = show_char   # "●" for password fields
        self._active     = True
        #Displaying the placeholder text
        widget.insert(0, placeholder)
        widget.config(fg=fg_placeholder)
        # Binding focus events to manage the placeholder
        widget.bind("<FocusIn>",  self._on_focus_in)
        widget.bind("<FocusOut>", self._on_focus_out)
    # Removing the placeholder text when the field gains focus
    def _on_focus_in(self, _event=None):
        if self._active:
            self.widget.delete(0, "end")
            self.widget.config(fg=self.fg_normal)
            # Enabling password masking if required
            if self.show_char:
                self.widget.config(show=self.show_char)
            self._active = False
    # Restoring the placeholder text when the field is empty
    def _on_focus_out(self, _event=None):
        if self.widget.get().strip() == "":
            self.widget.config(show="", fg=self.fg_ph)
            self.widget.insert(0, self.placeholder)
            self._active = True
    # Returning the entered value
    def get_value(self):
        return "" if self._active else self.widget.get()
    # Checking if the placeholder text is currently displayed
    def is_placeholder(self):
        return self._active