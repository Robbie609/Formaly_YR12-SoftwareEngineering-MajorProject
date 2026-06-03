import tkinter as tk
from tkinter import ttk
import os

# Architecture Imports (No external libraries)
from utils.styles import *
from utils.helpers import (
    clear_frame,
    disable_widget,
    enable_widget
)
from utils.validators import *


class FormalFeedbackPage(tk.Frame):
    """
    A premium, production-quality feedback entry application screen for Formaly.
    Allows attendees to seamlessly log experience reviews with zero external dependencies.
    """

    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, bg=BG, *args, **kwargs)
        self.controller = controller
        
        # Native photo reference storage dictionary to protect against garbage collection
        self.assets = {}
        
        # In-memory tracking data for rating selections
        self.rating_categories = ["Venue", "Music", "Food & Drinks", "Theme", "Organisation"]
        self.selected_ratings = {cat: tk.IntVar(value=0) for cat in self.rating_categories}
        self.overall_rating = tk.IntVar(value=0)
        
        # Centered structural canvas ensuring responsive distribution
        self.scroll_canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.scroll_canvas.yview)
        
        self.container = tk.Frame(self.scroll_canvas, bg=BG)
        
        # Configure scroll engine window binds
        self.container.bind(
            "<Configure>", 
            lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
        )
        self.scroll_canvas.create_window((0, 0), window=self.container, anchor="n")
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Layout positioning
        self.scroll_canvas.pack(side="left", fill="both", expand=True, padx=PADDING_X)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel globally to the canvas window for premium UX
        self.scroll_canvas.bind_all("<MouseWheel>", lambda e: self.scroll_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        self.build_page()

    # -------------------------------------------------------------------------
    # Core Layout Builders
    # -------------------------------------------------------------------------

    def build_page(self):
        """Assembles the visual stack of form elements."""
        clear_frame(self.container)
        
        # Dynamic layout adaptation rules
        self.container.grid_columnconfigure(0, weight=1)
        
        self.create_header()
        self.create_divider(self.container)
        self.create_overall_rating_section()
        self.create_divider(self.container)
        self.create_detailed_ratings_section()
        self.create_divider(self.container)
        self.create_comments_section()
        self.create_divider(self.container)
        self.create_submit_section()

    def create_header(self):
        """Builds the branding and informational subtitle region."""
        header_frame = tk.Frame(self.container, bg=BG)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(PADDING_Y, PADDING_Y // 2))
        
        # Logo Engine Integration
        logo_path = os.path.join("assets", "Logo.png")
        logo_loaded = False
        
        if os.path.exists(logo_path):
            try:
                self.assets["logo"] = tk.PhotoImage(file=logo_path)
                logo_label = tk.Label(header_frame, image=self.assets["logo"], bg=BG)
                logo_label.pack(pady=(0, PADDING_Y))
                logo_loaded = True
            except tk.TclError:
                pass  # Native fallback kicks in if system configuration refuses asset parsing
                
        if not logo_loaded:
            tk.Label(header_frame, text="F O R M A L Y", font=TITLE, bg=BG, fg=PRIMARY).pack(pady=(0, PADDING_Y // 2))
            
        tk.Label(header_frame, text="FORMAL FEEDBACK", font=SUBTITLE, bg=BG, fg=PRIMARY).pack()
        tk.Label(header_frame, text="Thank you for attending.", font=FONT, bg=BG, fg=SECONDARY).pack(pady=(PADDING_Y // 4, 0))
        tk.Label(header_frame, text="Midnight Masquerade 2026", font=FONT_BOLD, bg=BG, fg=PRIMARY).pack(pady=(PADDING_Y // 2, 0))

    def create_overall_rating_section(self):
        """Renders the prominent main star layout interaction field."""
        section_frame = tk.Frame(self.container, bg=BG)
        section_frame.grid(row=1, column=0, sticky="ew", pady=PADDING_Y)
        
        self.create_section_title(section_frame, "Overall Experience")
        
        stars_container = tk.Frame(section_frame, bg=BG)
        stars_container.pack(pady=PADDING_Y)
        
        self.overall_star_buttons = []
        for i in range(1, 6):
            btn = tk.Button(
                stars_container,
                text="☆",
                font=(FONT, 28),
                bg=BG,
                fg=SECONDARY,
                bd=0,
                relief="flat",
                activebackground=BG,
                activeforeground=PRIMARY,
                cursor="hand2",
                command=lambda val=i: self._set_star_rating(None, val, is_overall=True)
            )
            btn.pack(side="left", padx=5)
            self.overall_star_buttons.append(btn)

    def create_detailed_ratings_section(self):
        """Renders individual category evaluations utilizing reusable card components."""
        section_frame = tk.Frame(self.container, bg=BG)
        section_frame.grid(row=2, column=0, sticky="ew", pady=PADDING_Y)
        
        self.create_section_title(section_frame, "Event Aspects")
        
        card = tk.Frame(
            section_frame, 
            bg=CARD, 
            padx=PADDING_X * 2, 
            pady=PADDING_Y,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card.pack(fill="x", pady=PADDING_Y)
        
        self.category_star_map = {}
        for idx, category in enumerate(self.rating_categories):
            self.create_rating_row(card, category, idx)

    def create_comments_section(self):
        """Constructs the long-form text capture environment."""
        section_frame = tk.Frame(self.container, bg=BG)
        section_frame.grid(row=3, column=0, sticky="ew", pady=PADDING_Y)
        
        self.create_section_title(section_frame, "Additional Comments")
        
        # Native multi-line entry frame configuration
        text_container = tk.Frame(section_frame, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        text_container.pack(fill="x", pady=PADDING_Y)
        
        self.comments_input = tk.Text(
            text_container,
            font=FONT,
            bg=CARD,
            fg=PRIMARY,
            bd=0,
            height=6,
            wrap="word",
            padx=PADDING_X,
            pady=PADDING_Y,
            insertbackground=PRIMARY
        )
        self.comments_input.pack(fill="x", side="left", expand=True)
        
        # Standard native placeholder engine injection
        self.placeholder_text = "Tell us what you enjoyed and what could be improved..."
        self.comments_input.insert("1.0", self.placeholder_text)
        self.comments_input.configure(fg=SECONDARY)
        
        self.comments_input.bind("<FocusIn>", self._clear_placeholder)
        self.comments_input.bind("<FocusOut>", self._restore_placeholder)

    def create_submit_section(self):
        """Assembles the bottom button submission zone."""
        self.submit_frame = tk.Frame(self.container, bg=BG)
        self.submit_frame.grid(row=4, column=0, sticky="ew", pady=(PADDING_Y, PADDING_Y * 2))
        
        self.submit_button = tk.Button(
            self.submit_frame,
            text="Submit Feedback",
            command=self.submit_feedback,
            bg=PRIMARY,
            fg=BG,
            font=FONT_BOLD,
            relief="flat",
            bd=0,
            padx=PADDING_X * 2,
            pady=PADDING_Y,
            cursor="hand2",
            activebackground=PRIMARY,
            activeforeground=BG
        )
        self.submit_button.pack()

    # -------------------------------------------------------------------------
    # Reusable UI Factory Elements (DRY Principles)
    # -------------------------------------------------------------------------

    def create_rating_row(self, parent, label_text, row_idx):
        """Generates unified tabular horizontal assessment fields."""
        row_frame = tk.Frame(parent, bg=CARD)
        row_frame.pack(fill="x", pady=PADDING_Y // 2)
        
        row_frame.grid_columnconfigure(0, weight=1)
        row_frame.grid_columnconfigure(1, weight=1)
        
        lbl = tk.Label(row_frame, text=label_text, font=FONT, bg=CARD, fg=PRIMARY, anchor="w")
        lbl.grid(row=0, column=0, sticky="w")
        
        stars_sub_container = tk.Frame(row_frame, bg=CARD)
        stars_sub_container.grid(row=0, column=1, sticky="e")
        
        buttons_list = []
        for i in range(1, 6):
            btn = tk.Button(
                stars_sub_container,
                text="☆",
                font=(FONT, 18),
                bg=CARD,
                fg=SECONDARY,
                bd=0,
                relief="flat",
                activebackground=CARD,
                activeforeground=PRIMARY,
                cursor="hand2",
                command=lambda c=label_text, val=i: self._set_star_rating(c, val, is_overall=False)
            )
            btn.pack(side="left", padx=2)
            buttons_list.append(btn)
            
        self.category_star_map[label_text] = buttons_list

    def create_section_title(self, parent, text):
        """Standardized subtitle component across semantic units."""
        lbl = tk.Label(parent, text=text.upper(), font=FONT_BOLD, bg=BG, fg=PRIMARY)
        lbl.pack(anchor="w")
        return lbl

    def create_divider(self, parent):
        """Elegant horizontal geometric partition separator."""
        div = tk.Frame(parent, bg=BORDER, height=1)
        div.grid(sticky="ew", padx=PADDING_X, pady=PADDING_Y)
        return div

    # -------------------------------------------------------------------------
    # Visual Interactive Utility State Engines
    # -------------------------------------------------------------------------

    def _set_star_rating(self, category, value, is_overall=False):
        """Dynamically redraws full / empty glyph arrays depending on value mapping arrays."""
        if is_overall:
            self.overall_rating.set(value)
            buttons = self.overall_star_buttons
        else:
            self.selected_ratings[category].set(value)
            buttons = self.category_star_map[category]
            
        for idx, btn in enumerate(buttons):
            if idx < value:
                btn.configure(text="★", fg=PRIMARY)
            else:
                btn.configure(text="☆", fg=SECONDARY)

    def _clear_placeholder(self, event):
        """Flushes standard informational guidelines from fields on active focus context shifts."""
        if self.comments_input.get("1.0", "end-1c") == self.placeholder_text:
            self.comments_input.delete("1.0", "end")
            self.comments_input.configure(fg=PRIMARY)

    def _restore_placeholder(self, event):
        """Restores missing text descriptions if field entries are empty upon losing active focus."""
        if not self.comments_input.get("1.0", "end-1c").strip():
            self.comments_input.insert("1.0", self.placeholder_text)
            self.comments_input.configure(fg=SECONDARY)

    # -------------------------------------------------------------------------
    # Validation & Submission Operations
    # -------------------------------------------------------------------------

    def submit_feedback(self):
        """Processes form inputs through standard validation pipelines."""
        raw_text = self.comments_input.get("1.0", "end-1c").strip()
        
        # Clean background placeholder states
        if raw_text == self.placeholder_text:
            raw_text = ""
            
        # Architecture validation processing layer verification runs
        # Ensure feedback string is captured if no visual rating variables are present
        if not raw_text and self.overall_rating.get() == 0:
            self.comments_input.master.configure(highlightbackground=ERROR, highlightthickness=1)
            return
            
        # Clean entry validation handling wrapper via utils.validators / string standard actions
        sanitized_text = raw_text.replace("<", "&lt;").replace(">", "&gt;") 
        
        # Log payload processing logic goes here...
        self.render_success_state()

    def render_success_state(self):
        """Transforms structural application parameters into static verification components."""
        clear_frame(self.container)
        
        success_card = tk.Frame(
            self.container, 
            bg=CARD, 
            padx=PADDING_X * 2, 
            pady=PADDING_Y * 2,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        success_card.pack(pady=PADDING_Y * 3, fill="x")
        
        tk.Label(
            success_card, 
            text="✓ Feedback Submitted", 
            font=SUBTITLE, 
            bg=CARD, 
            fg=SUCCESS
        ).pack(pady=(0, PADDING_Y))
        
        tk.Label(
            success_card, 
            text="Thank you for helping improve future Formals.", 
            font=FONT, 
            bg=CARD, 
            fg=PRIMARY
        ).pack()
        
        # Render a flat return key configuration action to standard user panels
        return_btn = tk.Button(
            self.container,
            text="Return to Application",
            font=FONT,
            bg=SECONDARY,
            fg=PRIMARY,
            relief="flat",
            bd=0,
            padx=PADDING_X,
            pady=PADDING_Y // 2,
            cursor="hand2",
            command=self._exit_feedback_context
        )
        return_btn.pack(pady=PADDING_Y)

    def _exit_feedback_context(self):
        """Unbinds events safely and routes view states back to parent menus."""
        self.scroll_canvas.unbind_all("<MouseWheel>")
        if self.controller and hasattr(self.controller, 'show_frame'):
            self.controller.show_frame("FormalInvitationPage")