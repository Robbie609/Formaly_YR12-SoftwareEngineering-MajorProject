import tkinter as tk
import os

# Architecture Imports (No external libraries)
from utils.styles import *
from utils.helpers import (
    center_window, 
    clear_frame, 
    format_date, 
    truncate_text, 
    disable_widget, 
    enable_widget
)
from utils.validators import *


class FormalInvitationPage(tk.Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, bg=BG, *args, **kwargs)
        self.controller = controller
        
        # Native Tkinter image reference to prevent garbage collection
        self.logo_image = None
        
        # Center the visual invitation canvas inside the parent frame
        self.container = tk.Frame(self, bg=BG)
        self.container.pack(expand=True, padx=PADDING_X, pady=PADDING_Y)
        
        self.build_page()

    # -------------------------------------------------------------------------
    # Core Layout Builders
    # -------------------------------------------------------------------------

    def build_page(self):
        """Assembles the full invitation utilizing structural visual components."""
        clear_frame(self.container)  # Clean the frame dynamically using architecture helper
        
        self.create_header_with_logo()
        self.create_hero_section()
        self.create_divider(self.container)
        self.create_invitation_card()
        self.create_divider(self.container)
        self.create_rsvp_section()
        self.create_feedback_section()

    def create_header_with_logo(self):
        """Constructs the top header area with the formal invitation title and logo."""
        header_frame = tk.Frame(self.container, bg=BG)
        tk.Label(
            header_frame, 
            text="Official Formal Invitation", 
            font=SMALL, 
            bg=BG, 
            fg=SECONDARY
        ).pack()

    def create_hero_section(self):
        """Highlights the hosting school and the prestigious theme title."""
        hero_frame = tk.Frame(self.container, bg=BG)
        hero_frame.pack(fill="x", pady=PADDING_Y)
        
        # Prominent School Presenter Text
        tk.Label(
            hero_frame, 
            text="EPPING BOYS HIGH SCHOOL", 
            font=SUBTITLE, 
            bg=BG,
            fg=PRIMARY
        ).pack()
        
        tk.Label(
            hero_frame, 
            text="Presents", 
            font=FONT, 
            bg=BG,
            fg=SECONDARY
        ).pack(pady=PADDING_Y // 2)
        
        # Main Formal Title Event Focal Point
        tk.Label(
            hero_frame, 
            text="EPPING FORMAL 2026", 
            font=TITLE, 
            bg=BG,
            fg=PRIMARY
        ).pack(pady=PADDING_Y)

    def create_invitation_card(self):
        """Constructs the formal detail card wrapper."""
        card_frame = tk.Frame(
            self.container, 
            bg=CARD, 
            padx=PADDING_X * 2, 
            pady=PADDING_Y * 2,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card_frame.pack(fill="x", pady=PADDING_Y)
        
        self.create_section_title(card_frame, "EVENT INFORMATION")

        # Utilize format_date helper to render localized elegant date formatting
        formal_date = format_date("2026-12-12") if "format_date" in globals() else "12 December 2026"
        
        details = [
            ("Venue", "Curzon Hall, Sydney"),
            ("Date", formal_date),
            ("Time", "7:00 PM – 11:30 PM"),
        ]
        
        for label, value in details:
            self.create_detail_row(card_frame, label, value)

    def create_rsvp_section(self):
        """Creates the primary call-to-action button workflow area."""
        rsvp_frame = tk.Frame(self.container, bg=BG)
        rsvp_frame.pack(fill="x", pady=PADDING_Y)
        
        self.rsvp_button = self.create_action_button(
            parent=rsvp_frame, 
            text="Accept Invitation", 
            command=self.accept_invitation, 
            is_primary=True
        )
        self.rsvp_button.pack(pady=PADDING_Y)

    def create_feedback_section(self):
        """Places a clean, non-obtrusive post-event interaction area at the bottom."""
        feedback_frame = tk.Frame(self.container, bg=BG)
        feedback_frame.pack(fill="x", pady=(PADDING_Y * 2, 0))
        
        tk.Label(
            feedback_frame, 
            text="After the formal has concluded, we would love to hear your feedback.", 
            font=SMALL, 
            bg=BG, 
            fg=SECONDARY
        ).pack(pady=(0, PADDING_Y))
        
        self.create_action_button(
            parent=feedback_frame, 
            text="Leave Feedback", 
            command=self.open_feedback_page, 
            is_primary=True
        ).pack()

    # -------------------------------------------------------------------------
    # Reusable Component Utilities (DRY Compliance)
    # -------------------------------------------------------------------------

    def create_detail_row(self, parent, label_text, value_text):
        """Generates structured detail pairs perfectly balanced with layout grid weights."""
        row = tk.Frame(parent, bg=CARD)
        row.pack(fill="x", pady=PADDING_Y // 3)
        
        row.grid_columnconfigure(0, weight=1)
        row.grid_columnconfigure(1, weight=2)
        
        tk.Label(
            row, 
            text=label_text.upper(), 
            font=FONT_BOLD, 
            bg=CARD, 
            fg=SECONDARY,
            anchor="e"
        ).grid(row=0, column=0, sticky="e", padx=(0, PADDING_X))
        
        tk.Label(
            row, 
            text=value_text, 
            font=FONT, 
            bg=CARD,
            fg=PRIMARY,
            anchor="w"
        ).grid(row=0, column=1, sticky="w")

    def create_section_title(self, parent, text):
        """Draws standard elegant headers for content structures."""
        tk.Label(
            parent, 
            text=text, 
            font=FONT_BOLD, 
            bg=CARD,
            fg=PRIMARY
        ).pack(pady=(0, PADDING_Y))

    def create_divider(self, parent):
        """Generates fine horizontal geometric design rules."""
        divider = tk.Frame(parent, bg=BORDER, height=1)
        divider.pack(fill="x", padx=PADDING_X * 2, pady=PADDING_Y)

    def create_action_button(self, parent, text, command, is_primary=True):
        """Factory configuration for building standard application actions."""
        bg_color = PRIMARY if is_primary else SECONDARY
        fg_color = BG if is_primary else PRIMARY
        font_style = FONT_BOLD if is_primary else FONT
        
        btn = tk.Button(
            parent, 
            text=text, 
            command=command, 
            bg=bg_color, 
            fg=fg_color,
            font=font_style, 
            relief="flat",
            bd=0,
            padx=PADDING_X * 1.5 if is_primary else PADDING_X,
            pady=PADDING_Y,
            cursor="hand2",
            activebackground=PRIMARY if is_primary else SECONDARY,
            activeforeground=fg_color
        )
        return btn

    # -------------------------------------------------------------------------
    # Behavioral Event Interactivity Logic
    # -------------------------------------------------------------------------

    def accept_invitation(self):
        """Executes invitation updates cleanly while adhering to system helpers."""
        self.rsvp_button.configure(
            text="✓ Attendance Confirmed",
            bg=SUCCESS,
            fg=BG,
            cursor="arrow"
        )
        # Leverage built-in architecture method to transition control states safely
        disable_widget(self.rsvp_button)
# Link this button to the feedback page
    def open_feedback_page(self):
        """Triggers targeted view context router navigation callbacks."""
        if self.controller and hasattr(self.controller, 'show_frame'):
            self.controller.show_frame("FormalFeedbackPage")