import tkinter as tk
from styles import COLORS, BUTTON_COLORS, BUTTON_FONT
from event_manager import show_all_events_window
from styles import toggle_theme, get_current_theme


class BlueButton(tk.Canvas):
    def __init__(self, parent, text, command, width=150, height=36):
        super().__init__(parent, width=width, height=height, bg=COLORS['sidebar'], highlightthickness=0)
        self.command = command

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

        self.button_id = self.create_rectangle(2, 2, width - 2, height - 2,
                                               fill=COLORS['primary'],
                                               outline=COLORS['button_hover'],
                                               width=1, tags="button")

        self.text_id = self.create_text(width // 2, height // 2, text=text, fill="white",
                                        font=BUTTON_FONT, tags="text")

    def on_enter(self, e):
        self.itemconfig("button", fill=COLORS['button_hover'])

    def on_leave(self, e):
        self.itemconfig("button", fill=COLORS['primary'])

    def on_click(self, e):
        if callable(self.command):
            self.command()


def create_sidebar(parent, show_frame, *_):
    sidebar = tk.Frame(parent, width=180, bg=COLORS['sidebar'])
    sidebar.pack(fill="both", expand=True)

    # Title
    tk.Label(sidebar, text="CalendarApp", bg=COLORS['sidebar'],
             fg="white", font=("Segoe UI", 14, "bold")).pack(pady=(20, 10))

    # Theme toggle button
    def update_theme_button():
        current = get_current_theme()
        theme_btn.config(text=f"🌓 {'Dark' if current == 'light' else 'Light'} Theme")

    def theme_toggle():
        toggle_theme()
        update_theme_button()
        # Update parent background
        parent.config(bg=COLORS['sidebar'])
        # Refresh all buttons (would need more complex update for full theme change)

    theme_btn = tk.Button(sidebar, text="🌓 Dark Theme", command=theme_toggle,
                          bg=COLORS['primary'], fg="white",
                          font=("Segoe UI", 10, "bold"),
                          bd=0, padx=10, pady=5,
                          cursor="hand2",
                          activebackground=COLORS['button_hover'])
    theme_btn.pack(pady=(0, 15))
    update_theme_button()

    # Navigation buttons
    tools = [
        ("📅 Calendar", "main"),
        ("📝 All Events", "events"),
        ("📆 Weekday", "weekday"),
        ("➕ Add Days", "add"),
        ("➖ Subtract Days", "subtract"),
        ("📊 Duration", "count"),
    ]

    for text, frame in tools:
        if frame == "events":
            BlueButton(
                sidebar, text,
                show_all_events_window,
                width=140, height=34
            ).pack(pady=5)
        else:
            # Use lambda with default argument to avoid late binding issues
            BlueButton(
                sidebar, text,
                lambda f=frame: show_frame(f),
                width=140, height=34
            ).pack(pady=5)

    # Exit button
    tk.Button(sidebar, text="🚪 Exit", command=parent.winfo_toplevel().quit,
              bg=COLORS['primary'], fg="white", font=("Segoe UI", 10, "bold"),
              height=2, bd=0, activebackground=COLORS['button_hover'],
              cursor="hand2").pack(side="bottom", fill="x", pady=20, padx=15)