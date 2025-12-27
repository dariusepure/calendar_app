import tkinter as tk
from datetime import datetime
from tkinter import ttk
from calendar_view import show_calendar, prev_month, next_month, prev_year, next_year
from ui_components import create_sidebar
from styles import COLORS, toggle_theme, get_current_theme
from calculators import (
    weekday_function, add_days_function, subtract_days_function,
    duration_function
)

current_year = datetime.now().year
current_month = datetime.now().month


def create_card(parent, title="", bg=COLORS['light_gray']):
    """Create a card with shadow effect"""
    card = tk.Frame(parent, bg=bg, relief="flat", bd=1)
    if title:
        tk.Label(card, text=title, bg=bg, font=("Segoe UI", 12, "bold"),
                 fg=COLORS['text_dark']).pack(pady=(8, 3))
    return card


def create_input_group(parent, label_text, spinbox_range=(1, 31), default_value=""):
    """Create a uniform input group"""
    frame = tk.Frame(parent, bg=COLORS['light_gray'])

    tk.Label(frame, text=label_text, bg=COLORS['light_gray'],
             font=("Segoe UI", 10), fg=COLORS['text_dark']).pack(anchor="w", padx=5)

    spinbox = tk.Spinbox(frame, from_=spinbox_range[0], to=spinbox_range[1],
                         width=10, font=("Segoe UI", 10),
                         bg=COLORS['input_bg'], bd=1, relief="solid")
    spinbox.delete(0, tk.END)

    # Validate default value
    try:
        default = int(default_value)
        if default < spinbox_range[0]:
            default = spinbox_range[0]
        elif default > spinbox_range[1]:
            default = spinbox_range[1]
        spinbox.insert(0, str(default))
    except (ValueError, TypeError):
        spinbox.insert(0, str(spinbox_range[0]))

    spinbox.pack(pady=2, padx=5, fill="x")

    return spinbox, frame


def create_blue_button(parent, text, command):
    """Create a uniform blue button"""
    return tk.Button(parent, text=text, command=command,
                     bg=COLORS['primary'], fg="white",
                     font=("Segoe UI", 11, "bold"),
                     bd=0, padx=20, pady=6,
                     cursor="hand2",
                     activebackground=COLORS['button_hover'])


def create_nav_button(parent, text, command):
    """Create a small navigation button"""
    return tk.Button(parent, text=text, command=command,
                     bg=COLORS['primary'], fg="white",
                     font=("Segoe UI", 10, "bold"),
                     bd=0, padx=8, pady=3,
                     cursor="hand2",
                     activebackground=COLORS['button_hover'])


def main():
    global current_year, current_month

    root = tk.Tk()
    root.title("CalendarApp")
    root.geometry("800x600")
    root.configure(bg=COLORS['background'])

    # Prevent resizing too small
    root.minsize(600, 500)

    # Main container with reduced padding
    main_container = tk.Frame(root, bg=COLORS['background'])
    main_container.pack(fill="both", expand=True, padx=8, pady=4)

    # Frame for content
    content_frame = tk.Frame(main_container, bg=COLORS['background'], width=600, height=580)
    content_frame.pack(side="left", fill="both", expand=True)
    content_frame.pack_propagate(False)

    widgets = {}

    # ==================== CALENDAR UI WITH COMPACT LAYOUT ====================
    def create_calendar_ui():
        for widget in content_frame.winfo_children():
            widget.destroy()

        # Main frame for calendar - COMPACT
        main_cal_frame = tk.Frame(content_frame, bg=COLORS['calendar_bg'])
        main_cal_frame.pack(fill="both", expand=True, padx=2, pady=2)

        # Frame for top navigation - VERY COMPACT
        nav_frame = tk.Frame(main_cal_frame, bg=COLORS['calendar_bg'])
        nav_frame.pack(fill="x", pady=(6, 2), padx=12)  # REDUCED bottom pady

        # Navigation functions
        def go_prev_year():
            global current_year, current_month
            current_year, current_month = prev_year(current_year, current_month)
            update_calendar()

        def go_prev_month():
            global current_year, current_month
            current_year, current_month = prev_month(current_year, current_month)
            update_calendar()

        def go_today():
            global current_year, current_month
            today = datetime.now()
            current_year, current_month = today.year, today.month
            update_calendar()

        def go_next_month():
            global current_year, current_month
            current_year, current_month = next_month(current_year, current_month)
            update_calendar()

        def go_next_year():
            global current_year, current_month
            current_year, current_month = next_year(current_year, current_month)
            update_calendar()

        # Left navigation buttons
        nav_left = tk.Frame(nav_frame, bg=COLORS['calendar_bg'])
        nav_left.pack(side="left")

        create_nav_button(nav_left, "◀◀", go_prev_year).pack(side="left", padx=1)
        create_nav_button(nav_left, "◀", go_prev_month).pack(side="left", padx=1)
        create_nav_button(nav_left, "Today", go_today).pack(side="left", padx=6)
        create_nav_button(nav_left, "▶", go_next_month).pack(side="left", padx=1)
        create_nav_button(nav_left, "▶▶", go_next_year).pack(side="left", padx=1)

        # Header (month and year) - centered COMPACT
        header = tk.Label(nav_frame, text="", font=("Segoe UI", 17, "bold"),
                          bg=COLORS['calendar_bg'], fg=COLORS['primary'])
        header.pack(side="left", expand=True, padx=15)

        # Frame for calendar - VERY COMPACT
        calendar_container = tk.Frame(main_cal_frame, bg=COLORS['calendar_bg'])
        calendar_container.pack(expand=True, fill="both", padx=10, pady=(0, 2))  # REDUCED bottom pady

        # Configure COMPACT style for Treeview
        style = ttk.Style()
        style.configure("Compact.Treeview",
                        background=COLORS['calendar_bg'],
                        fieldbackground=COLORS['calendar_bg'],
                        borderwidth=1,
                        relief="solid",
                        rowheight=28,  # REDUCED
                        padding=0)

        style.configure("Compact.Treeview.Heading",
                        background=COLORS['calendar_bg'],
                        relief="flat",
                        borderwidth=0,
                        padding=(0, 4, 0, 4))  # Reduced padding

        # Calendar with COMPACT style
        cal = ttk.Treeview(calendar_container,
                           columns=[str(i) for i in range(7)],
                           show="headings",
                           style="Compact.Treeview")

        # Set column widths
        for i in range(7):
            cal.heading(str(i), text="")
            cal.column(str(i), width=78, anchor="center", stretch=False)

        # PACK without expand to not fill empty space
        cal.pack(fill="both", padx=0, pady=0)

        def update_calendar():
            """Update calendar with current month and year"""
            show_calendar(current_year, current_month, cal, header)

            # Force compact layout
            calendar_container.update_idletasks()

            # Set exact needed height
            num_rows = len(cal.get_children())
            if num_rows > 0:
                # Total height = (num_rows * rowheight) + padding
                total_height = (num_rows * 28) + 5  # 28 = rowheight, 5 = padding
                cal.configure(height=num_rows)
                calendar_container.config(height=total_height)
                calendar_container.pack_propagate(False)

        # Initialize calendar
        update_calendar()

        widgets['main'] = {
            'header': header,
            'calendar': cal,
            'update_func': update_calendar
        }

    # ==================== WEEKDAY UI ====================
    def create_weekday_ui():
        for widget in content_frame.winfo_children():
            widget.destroy()

        main_card = create_card(content_frame, bg=COLORS['light_gray'])
        main_card.pack(fill="both", expand=True, padx=4, pady=4)

        tk.Label(main_card, text="📆 Weekday Calculator",
                 font=("Segoe UI", 16, "bold"), bg=COLORS['light_gray'],
                 fg=COLORS['text_dark']).pack(pady=(12, 12))

        input_card = create_card(main_card, bg=COLORS['light_gray'])
        input_card.pack(pady=8, padx=35, fill="x")

        inputs_frame = tk.Frame(input_card, bg=COLORS['light_gray'])
        inputs_frame.pack(pady=6)

        day_spin, day_frame = create_input_group(inputs_frame, "Day", (1, 31), datetime.now().day)
        day_frame.grid(row=0, column=0, padx=8, pady=4)

        month_spin, month_frame = create_input_group(inputs_frame, "Month", (1, 12), datetime.now().month)
        month_frame.grid(row=0, column=1, padx=8, pady=4)

        year_spin, year_frame = create_input_group(inputs_frame, "Year", (1900, 2100), datetime.now().year)
        year_frame.grid(row=0, column=2, padx=8, pady=4)

        button_frame = tk.Frame(main_card, bg=COLORS['light_gray'])
        button_frame.pack(pady=10)

        calc_btn = create_blue_button(button_frame, "Calculate Weekday",
                                      command=lambda: weekday_function('weekday',
                                                                       {'weekday': day_spin},
                                                                       {'weekday': month_spin},
                                                                       {'weekday': year_spin},
                                                                       result_label))
        calc_btn.pack()

        result_card = create_card(main_card, bg=COLORS['light_gray'])
        result_card.pack(fill="x", padx=35, pady=6)

        result_label = tk.Label(result_card, text="",
                                font=("Segoe UI", 11), bg=COLORS['light_gray'],
                                wraplength=400, justify="center",
                                fg=COLORS['text_dark'])
        result_label.pack(pady=10)

        widgets['weekday'] = {
            'day_spin': day_spin, 'month_spin': month_spin, 'year_spin': year_spin,
            'result_label': result_label
        }

    # ==================== ADD DAYS UI ====================
    def create_add_days_ui():
        for widget in content_frame.winfo_children():
            widget.destroy()

        main_card = create_card(content_frame, bg=COLORS['light_gray'])
        main_card.pack(fill="both", expand=True, padx=4, pady=4)

        tk.Label(main_card, text="➕ Add Days Calculator",
                 font=("Segoe UI", 16, "bold"), bg=COLORS['light_gray'],
                 fg=COLORS['text_dark']).pack(pady=(12, 12))

        date_card = create_card(main_card, "Start Date", bg=COLORS['light_gray'])
        date_card.pack(pady=8, padx=35, fill="x")

        inputs_frame = tk.Frame(date_card, bg=COLORS['light_gray'])
        inputs_frame.pack(pady=6)

        day_spin, day_frame = create_input_group(inputs_frame, "Day", (1, 31), datetime.now().day)
        day_frame.grid(row=0, column=0, padx=8, pady=4)

        month_spin, month_frame = create_input_group(inputs_frame, "Month", (1, 12), datetime.now().month)
        month_frame.grid(row=0, column=1, padx=8, pady=4)

        year_spin, year_frame = create_input_group(inputs_frame, "Year", (1900, 2100), datetime.now().year)
        year_frame.grid(row=0, column=2, padx=8, pady=4)

        days_card = create_card(main_card, "Days to Add", bg=COLORS['light_gray'])
        days_card.pack(pady=8, padx=35, fill="x")

        days_entry = tk.Entry(days_card, width=15, font=("Segoe UI", 10),
                              bg=COLORS['input_bg'], bd=1, relief="solid")
        days_entry.insert(0, "1")
        days_entry.pack(pady=8, padx=10)

        button_frame = tk.Frame(main_card, bg=COLORS['light_gray'])
        button_frame.pack(pady=10)

        calc_btn = create_blue_button(button_frame, "Calculate New Date",
                                      command=lambda: add_days_function('add',
                                                                        {'add': day_spin},
                                                                        {'add': month_spin},
                                                                        {'add': year_spin},
                                                                        {'add': days_entry},
                                                                        result_label))
        calc_btn.pack()

        result_card = create_card(main_card, bg=COLORS['light_gray'])
        result_card.pack(fill="x", padx=35, pady=6)

        result_label = tk.Label(result_card, text="",
                                font=("Segoe UI", 11), bg=COLORS['light_gray'],
                                wraplength=400, justify="center",
                                fg=COLORS['text_dark'])
        result_label.pack(pady=10)

        widgets['add'] = {
            'day_spin': day_spin,
            'month_spin': month_spin,
            'year_spin': year_spin,
            'days_entry': days_entry,
            'result_label': result_label
        }

    # ==================== SUBTRACT DAYS UI ====================
    def create_subtract_days_ui():
        for widget in content_frame.winfo_children():
            widget.destroy()

        main_card = create_card(content_frame, bg=COLORS['light_gray'])
        main_card.pack(fill="both", expand=True, padx=4, pady=4)

        tk.Label(main_card, text="➖ Subtract Days Calculator",
                 font=("Segoe UI", 16, "bold"), bg=COLORS['light_gray'],
                 fg=COLORS['text_dark']).pack(pady=(12, 12))

        date_card = create_card(main_card, "Start Date", bg=COLORS['light_gray'])
        date_card.pack(pady=8, padx=35, fill="x")

        inputs_frame = tk.Frame(date_card, bg=COLORS['light_gray'])
        inputs_frame.pack(pady=6)

        day_spin, day_frame = create_input_group(inputs_frame, "Day", (1, 31), datetime.now().day)
        day_frame.grid(row=0, column=0, padx=8, pady=4)

        month_spin, month_frame = create_input_group(inputs_frame, "Month", (1, 12), datetime.now().month)
        month_frame.grid(row=0, column=1, padx=8, pady=4)

        year_spin, year_frame = create_input_group(inputs_frame, "Year", (1900, 2100), datetime.now().year)
        year_frame.grid(row=0, column=2, padx=8, pady=4)

        days_card = create_card(main_card, "Days to Subtract", bg=COLORS['light_gray'])
        days_card.pack(pady=8, padx=35, fill="x")

        days_entry = tk.Entry(days_card, width=15, font=("Segoe UI", 10),
                              bg=COLORS['input_bg'], bd=1, relief="solid")
        days_entry.insert(0, "1")
        days_entry.pack(pady=8, padx=10)

        button_frame = tk.Frame(main_card, bg=COLORS['light_gray'])
        button_frame.pack(pady=10)

        calc_btn = create_blue_button(button_frame, "Calculate New Date",
                                      command=lambda: subtract_days_function('subtract',
                                                                             {'subtract': day_spin},
                                                                             {'subtract': month_spin},
                                                                             {'subtract': year_spin},
                                                                             {'subtract': days_entry},
                                                                             result_label))
        calc_btn.pack()

        result_card = create_card(main_card, bg=COLORS['light_gray'])
        result_card.pack(fill="x", padx=35, pady=6)

        result_label = tk.Label(result_card, text="",
                                font=("Segoe UI", 11), bg=COLORS['light_gray'],
                                wraplength=400, justify="center",
                                fg=COLORS['text_dark'])
        result_label.pack(pady=10)

        widgets['subtract'] = {
            'day_spin': day_spin,
            'month_spin': month_spin,
            'year_spin': year_spin,
            'days_entry': days_entry,
            'result_label': result_label
        }

    # ==================== DURATION UI ====================
    def create_duration_ui():
        for widget in content_frame.winfo_children():
            widget.destroy()

        main_card = create_card(content_frame, bg=COLORS['light_gray'])
        main_card.pack(fill="both", expand=True, padx=4, pady=4)

        tk.Label(main_card, text="📊 Duration Calculator",
                 font=("Segoe UI", 16, "bold"), bg=COLORS['light_gray'],
                 fg=COLORS['text_dark']).pack(pady=(12, 12))

        card1 = create_card(main_card, "First Date", bg=COLORS['light_gray'])
        card1.pack(pady=8, padx=35, fill="x")

        inputs_frame1 = tk.Frame(card1, bg=COLORS['light_gray'])
        inputs_frame1.pack(pady=6)

        day_spin1, day_frame1 = create_input_group(inputs_frame1, "Day", (1, 31), "1")
        day_frame1.grid(row=0, column=0, padx=8, pady=4)

        month_spin1, month_frame1 = create_input_group(inputs_frame1, "Month", (1, 12), "1")
        month_frame1.grid(row=0, column=1, padx=8, pady=4)

        year_spin1, year_frame1 = create_input_group(inputs_frame1, "Year", (1900, 2100), datetime.now().year)
        year_frame1.grid(row=0, column=2, padx=8, pady=4)

        card2 = create_card(main_card, "Second Date", bg=COLORS['light_gray'])
        card2.pack(pady=8, padx=35, fill="x")

        inputs_frame2 = tk.Frame(card2, bg=COLORS['light_gray'])
        inputs_frame2.pack(pady=6)

        day_spin2, day_frame2 = create_input_group(inputs_frame2, "Day", (1, 31), datetime.now().day)
        day_frame2.grid(row=0, column=0, padx=8, pady=4)

        month_spin2, month_frame2 = create_input_group(inputs_frame2, "Month", (1, 12), datetime.now().month)
        month_frame2.grid(row=0, column=1, padx=8, pady=4)

        year_spin2, year_frame2 = create_input_group(inputs_frame2, "Year", (1900, 2100), datetime.now().year)
        year_frame2.grid(row=0, column=2, padx=8, pady=4)

        button_frame = tk.Frame(main_card, bg=COLORS['light_gray'])
        button_frame.pack(pady=10)

        calc_btn = create_blue_button(button_frame, "Calculate Duration",
                                      command=lambda: duration_function('count',
                                                                        {'count': day_spin1},
                                                                        {'count': month_spin1},
                                                                        {'count': year_spin1},
                                                                        {'count': day_spin2},
                                                                        {'count': month_spin2},
                                                                        {'count': year_spin2},
                                                                        result_label))
        calc_btn.pack()

        result_card = create_card(main_card, bg=COLORS['light_gray'])
        result_card.pack(fill="x", padx=35, pady=6)

        result_label = tk.Label(result_card, text="",
                                font=("Segoe UI", 10), bg=COLORS['light_gray'],
                                wraplength=400, justify="left",
                                fg=COLORS['text_dark'])
        result_label.pack(pady=10, padx=8)

        widgets['count'] = {
            'day_spin1': day_spin1,
            'month_spin1': month_spin1,
            'year_spin1': year_spin1,
            'day_spin2': day_spin2,
            'month_spin2': month_spin2,
            'year_spin2': year_spin2,
            'result_label': result_label
        }

    # ==================== MAIN NAVIGATION FUNCTION ====================
    def show_frame(frame_name):
        if frame_name == "main":
            create_calendar_ui()
        elif frame_name == "weekday":
            create_weekday_ui()
        elif frame_name == "add":
            create_add_days_ui()
        elif frame_name == "subtract":
            create_subtract_days_ui()
        elif frame_name == "count":
            create_duration_ui()

    # ==================== SIDEBAR ====================
    sidebar_container = tk.Frame(main_container, bg=COLORS['sidebar'], width=180)
    sidebar_container.pack(side="right", fill="y")
    sidebar_container.pack_propagate(False)

    create_sidebar(sidebar_container, show_frame)

    # Initialize with calendar
    create_calendar_ui()

    # ==================== KEYBOARD NAVIGATION ====================
    def handle_key(event):
        if 'main' in widgets and widgets['main']:
            global current_year, current_month
            if event.keysym == "Left":
                current_year, current_month = prev_month(current_year, current_month)
            elif event.keysym == "Right":
                current_year, current_month = next_month(current_year, current_month)
            elif event.keysym == "Up":
                current_year, current_month = prev_year(current_year, current_month)
            elif event.keysym == "Down":
                current_year, current_month = next_year(current_year, current_month)
            else:
                return  # Ignore other keys

            widgets['main']['update_func']()

    root.bind("<Left>", handle_key)
    root.bind("<Right>", handle_key)
    root.bind("<Up>", handle_key)
    root.bind("<Down>", handle_key)

    # Bind Escape to quit
    root.bind("<Escape>", lambda e: root.quit())

    # Bind Ctrl+T to toggle theme
    def toggle_theme_shortcut(event):
        toggle_theme()
        # Refresh current view
        if 'main' in widgets:
            show_frame('main')
        else:
            # Update all colors dynamically
            for widget in root.winfo_children():
                widget.config(bg=COLORS['background'])

    root.bind("<Control-t>", toggle_theme_shortcut)
    root.bind("<Control-T>", toggle_theme_shortcut)

    root.mainloop()