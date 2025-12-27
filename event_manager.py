import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json, os
from styles import COLORS

EVENTS_FILE = "calendar_events.json"
open_event_windows = {}


# ==================== BASIC EVENT FUNCTIONS ====================

def load_events():
    """Load all events from file"""
    if not os.path.exists(EVENTS_FILE):
        return {}

    try:
        with open(EVENTS_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            if not content.strip():
                return {}
            return json.loads(content)
    except json.JSONDecodeError:
        messagebox.showerror("Error", f"Events file '{EVENTS_FILE}' is corrupted. Creating new file.")
        return {}
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load events: {str(e)}")
        return {}


def save_events(events):
    """Save events to file"""
    try:
        with open(EVENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(events, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save events: {str(e)}")
        return False


def add_event(date_str, text):
    """Add an event for a specific date"""
    if not text.strip():
        return False

    events = load_events()

    # Get next available ID for this date
    existing_events = events.get(date_str, [])
    next_id = max([e['id'] for e in existing_events], default=0) + 1

    events.setdefault(date_str, []).append({
        "id": next_id,
        "text": text.strip(),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    return save_events(events)


def get_events_for_date(date_str):
    """Return events for a specific date"""
    events = load_events()
    return events.get(date_str, [])


def get_all_events():
    """Return all events sorted by date (newest first)"""
    events = load_events()
    all_events = []

    # Parse dates once and cache
    date_cache = {}

    for date_str, event_list in events.items():
        if date_str not in date_cache:
            try:
                date_cache[date_str] = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                continue  # Skip invalid dates

        date_obj = date_cache[date_str]

        for event in event_list:
            try:
                created_time = datetime.strptime(event['created_at'], "%Y-%m-%d %H:%M")
            except ValueError:
                created_time = datetime.now()

            all_events.append({
                'date': date_str,
                'date_obj': date_obj,
                'text': event.get('text', ''),
                'created': created_time.strftime("%Y-%m-%d %H:%M"),
                'created_obj': created_time
            })

    all_events.sort(key=lambda x: (x['date_obj'], x['created_obj']), reverse=True)
    return all_events


def delete_event(date_str, event_index):
    """Delete an event for a specific date"""
    events = load_events()

    if date_str not in events:
        return False

    if 0 <= event_index < len(events[date_str]):
        # Remove the event
        deleted_event = events[date_str].pop(event_index)

        # If no events left for this date, remove the date entirely
        if not events[date_str]:
            del events[date_str]
        else:
            # Re-index IDs for remaining events (optional but good for consistency)
            for i, event in enumerate(events[date_str]):
                event['id'] = i + 1

        return save_events(events)

    return False


def cleanup_closed_windows():
    """Cleanup any windows that have been closed without calling on_close"""
    closed_windows = []
    for date_str, win in list(open_event_windows.items()):
        try:
            if not win.winfo_exists():
                closed_windows.append(date_str)
        except:
            closed_windows.append(date_str)

    for date_str in closed_windows:
        if date_str in open_event_windows:
            del open_event_windows[date_str]


# ==================== EVENT DIALOG FOR SPECIFIC DATE ====================

def show_event_dialog(date_str, date_obj):
    """Open window to add/view events for a specific date"""
    # Cleanup any closed windows first
    cleanup_closed_windows()

    if date_str in open_event_windows:
        win = open_event_windows[date_str]
        try:
            if win.winfo_exists():
                win.lift()
                win.focus_force()
                return
        except:
            pass  # Window might be in weird state

    win = tk.Toplevel()
    win.title(f"📅 Events for {date_obj.strftime('%A, %d %B %Y')}")
    win.geometry("400x450")
    win.configure(bg=COLORS['background'])

    # Center the window
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry(f'{width}x{height}+{x}+{y}')

    open_event_windows[date_str] = win

    def on_close():
        if date_str in open_event_windows:
            try:
                del open_event_windows[date_str]
            except KeyError:
                pass
        win.destroy()

    win.protocol("WM_DELETE_WINDOW", on_close)

    # Main frame
    main_frame = tk.Frame(win, bg=COLORS['background'])
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Title
    tk.Label(main_frame, text=f"Events for {date_obj.strftime('%d %B %Y')}",
             font=("Segoe UI", 14, "bold"), bg=COLORS['background'],
             fg=COLORS['primary']).pack(pady=(0, 15))

    # Frame for existing events
    events_frame = tk.Frame(main_frame, bg=COLORS['card_bg'], relief="solid", bd=1)
    events_frame.pack(fill="both", expand=True, pady=(0, 15))

    events_list = get_events_for_date(date_str)

    if events_list:
        # Canvas with scrollbar for events
        canvas = tk.Canvas(events_frame, bg=COLORS['card_bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(events_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['card_bg'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        tk.Label(scrollable_frame, text="Existing Events:",
                 font=("Segoe UI", 10, "bold"), bg=COLORS['card_bg']).pack(anchor="w", padx=10, pady=5)

        for i, e in enumerate(events_list):
            event_frame = tk.Frame(scrollable_frame, bg=COLORS['card_bg'])
            event_frame.pack(fill="x", padx=10, pady=2)

            # Blue bullet
            tk.Label(event_frame, text="•", fg=COLORS['primary'],
                     bg=COLORS['card_bg'], font=("Segoe UI", 12)).pack(side="left")

            # Event text
            tk.Label(event_frame, text=f" {e['text']}",
                     bg=COLORS['card_bg'], font=("Segoe UI", 9), wraplength=250).pack(side="left", padx=5, fill="x", expand=True)

            # Delete button
            del_btn = tk.Button(event_frame, text="✕",
                                command=lambda d=date_str, idx=i: delete_and_refresh(d, idx),
                                bg="#fee2e2", fg="#dc2626",
                                font=("Segoe UI", 8, "bold"),
                                bd=0, width=2, height=1,
                                cursor="hand2")
            del_btn.pack(side="right", padx=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    else:
        tk.Label(events_frame, text="No events for this date",
                 font=("Segoe UI", 9, "italic"), bg=COLORS['card_bg'],
                 fg=COLORS['dark_gray']).pack(expand=True, pady=20)

    def delete_and_refresh(del_date_str, del_index):
        """Delete an event and reload the window"""
        if delete_event(del_date_str, del_index):
            messagebox.showinfo("Success", "Event deleted!")
            on_close()
            # Reopen window with updated list
            show_event_dialog(date_str, date_obj)
        else:
            messagebox.showerror("Error", "Failed to delete event!")

    # Frame for adding new event
    add_frame = tk.Frame(main_frame, bg=COLORS['card_bg'], relief="solid", bd=1)
    add_frame.pack(fill="x", pady=(0, 15))

    tk.Label(add_frame, text="Add New Event:",
             font=("Segoe UI", 10, "bold"), bg=COLORS['card_bg']).pack(anchor="w", padx=10, pady=5)

    # Entry for text
    entry = tk.Entry(add_frame, width=35, font=("Segoe UI", 10),
                     bg=COLORS['input_bg'], bd=1, relief="solid")
    entry.pack(pady=5, padx=10)

    # Info message
    tk.Label(add_frame, text="Event will be saved for this date",
             font=("Segoe UI", 8, "italic"), bg=COLORS['card_bg'],
             fg=COLORS['dark_gray']).pack(pady=2)

    def add():
        """Add a new event"""
        text = entry.get().strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter event text!")
            entry.focus_set()
            return

        if add_event(date_str, text):
            messagebox.showinfo("Success", "Event added successfully!")
            on_close()
            # Reopen window with updated list
            show_event_dialog(date_str, date_obj)
        else:
            messagebox.showerror("Error", "Failed to add event!")

    # Add button
    add_btn = tk.Button(main_frame, text="➕ Add Event", command=add,
                        bg=COLORS['primary'], fg="white",
                        font=("Segoe UI", 10, "bold"),
                        bd=0, padx=20, pady=5,
                        cursor="hand2")
    add_btn.pack(pady=10)

    # Close button
    close_btn = tk.Button(main_frame, text="Close", command=on_close,
                          bg=COLORS['light_gray'], fg=COLORS['text_dark'],
                          font=("Segoe UI", 9),
                          bd=0, padx=15, pady=3,
                          cursor="hand2")
    close_btn.pack()

    # Bind Enter key to add event
    entry.bind('<Return>', lambda e: add())

    # Focus on entry
    entry.focus_set()


# ==================== CALENDAR HANDLERS ====================

def on_calendar_click(event, year, month, cal_table):
    """Handle click on a day in the calendar"""
    # Identify the row and column clicked
    item = cal_table.identify_row(event.y)
    column = cal_table.identify_column(event.x)

    if not item or column == "#0":
        return

    # Get value from that cell
    try:
        col_idx = int(column[1]) - 1
        values = cal_table.item(item, "values")

        if col_idx >= len(values) or not values[col_idx]:
            return

        day = int(values[col_idx])
        date_str = f"{year}-{month:02d}-{day:02d}"
        date_obj = datetime(year, month, day)

        # Open event dialog
        show_event_dialog(date_str, date_obj)
    except (ValueError, IndexError):
        pass  # Click was not on a valid day cell


# ==================== ALL EVENTS WINDOW ====================

def show_all_events_window():
    """Open a window with all events"""
    # Cleanup closed windows first
    cleanup_closed_windows()

    # Check if window already exists
    for win in tk._default_root.winfo_children():
        if isinstance(win, tk.Toplevel) and win.title() == "📋 All Events":
            try:
                win.lift()
                win.focus_force()
                return
            except:
                pass

    win = tk.Toplevel()
    win.title("📋 All Events")
    win.geometry("700x500")
    win.configure(bg=COLORS['background'])

    # Center the window
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry(f'{width}x{height}+{x}+{y}')

    # Main frame
    main_frame = tk.Frame(win, bg=COLORS['background'])
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Title
    tk.Label(main_frame, text="📋 All Events",
             font=("Segoe UI", 18, "bold"), bg=COLORS['background'],
             fg=COLORS['primary']).pack(pady=(0, 15))

    # Statistics
    all_events = get_all_events()
    events_dict = load_events()
    total_events = sum(len(events) for events in events_dict.values())
    unique_dates = len(events_dict)

    stats_frame = tk.Frame(main_frame, bg=COLORS['light_gray'], relief="solid", bd=1)
    stats_frame.pack(fill="x", pady=(0, 15))

    tk.Label(stats_frame, text="📊 Statistics:",
             font=("Segoe UI", 11, "bold"), bg=COLORS['light_gray']).pack(anchor="w", padx=10, pady=5)

    stats_text = tk.Frame(stats_frame, bg=COLORS['light_gray'])
    stats_text.pack(fill="x", padx=10, pady=5)

    tk.Label(stats_text, text=f"• Total events: {total_events}",
             font=("Segoe UI", 10), bg=COLORS['light_gray'], fg=COLORS['text_dark']).pack(anchor="w")
    tk.Label(stats_text, text=f"• Dates with events: {unique_dates}",
             font=("Segoe UI", 10), bg=COLORS['light_gray'], fg=COLORS['text_dark']).pack(anchor="w")

    if total_events > 0:
        # Frame for events list
        list_frame = tk.Frame(main_frame, bg=COLORS['card_bg'], relief="solid", bd=1)
        list_frame.pack(fill="both", expand=True, pady=(0, 15))

        # Canvas with scrollbar
        canvas = tk.Canvas(list_frame, bg=COLORS['card_bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['card_bg'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Header
        header_frame = tk.Frame(scrollable_frame, bg=COLORS['header_bg'])
        header_frame.pack(fill="x", pady=(5, 2), padx=5)

        tk.Label(header_frame, text="Date", width=12,
                 font=("Segoe UI", 9, "bold"), bg=COLORS['header_bg'],
                 fg=COLORS['text_dark']).pack(side="left", padx=5)
        tk.Label(header_frame, text="Event", width=45,
                 font=("Segoe UI", 9, "bold"), bg=COLORS['header_bg'],
                 fg=COLORS['text_dark']).pack(side="left", padx=5)
        tk.Label(header_frame, text="Added", width=10,
                 font=("Segoe UI", 9, "bold"), bg=COLORS['header_bg'],
                 fg=COLORS['text_dark']).pack(side="left", padx=5)

        # Separator
        tk.Frame(scrollable_frame, bg=COLORS['border'], height=1).pack(fill="x", pady=2)

        # Events list
        for event in all_events:
            event_frame = tk.Frame(scrollable_frame, bg=COLORS['card_bg'])
            event_frame.pack(fill="x", pady=2, padx=5)

            # Date (blue for events)
            date_label = tk.Label(event_frame,
                                  text=event['date_obj'].strftime("%d %b %Y"),
                                  font=("Segoe UI", 9), bg=COLORS['card_bg'],
                                  fg=COLORS['primary'], width=12)
            date_label.pack(side="left", padx=5)

            # Event
            event_label = tk.Label(event_frame, text=event['text'],
                                   font=("Segoe UI", 9), bg=COLORS['card_bg'],
                                   fg=COLORS['text_dark'], width=45,
                                   wraplength=350, justify="left")
            event_label.pack(side="left", padx=5, fill="x", expand=True)

            # Time added
            created_time = event['created_obj'] if 'created_obj' in event else datetime.now()
            time_label = tk.Label(event_frame,
                                  text=created_time.strftime("%H:%M"),
                                  font=("Segoe UI", 8), bg=COLORS['card_bg'],
                                  fg=COLORS['dark_gray'], width=10)
            time_label.pack(side="left", padx=5)

            # Delete button
            del_btn = tk.Button(event_frame, text="🗑️",
                                command=lambda d=event['date'], txt=event['text']: delete_event_from_all(d, txt, win),
                                bg="#fee2e2", fg="#dc2626",
                                font=("Segoe UI", 8),
                                bd=0, width=3,
                                cursor="hand2")
            del_btn.pack(side="right", padx=5)

        canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")
    else:
        # No events message
        no_events_frame = tk.Frame(main_frame, bg=COLORS['card_bg'], relief="solid", bd=1)
        no_events_frame.pack(fill="both", expand=True, pady=(0, 15))

        tk.Label(no_events_frame, text="📭 No events yet!",
                 font=("Segoe UI", 12, "italic"), bg=COLORS['card_bg'],
                 fg=COLORS['dark_gray']).pack(expand=True, pady=20)

        tk.Label(no_events_frame, text="Click on dates in the calendar to add events",
                 font=("Segoe UI", 9), bg=COLORS['card_bg'],
                 fg=COLORS['dark_gray']).pack(pady=10)

    def refresh_window():
        win.destroy()
        show_all_events_window()

    # Button frame
    button_frame = tk.Frame(main_frame, bg=COLORS['background'])
    button_frame.pack(fill="x", pady=10)

    refresh_btn = tk.Button(button_frame, text="🔄 Refresh", command=refresh_window,
                            bg=COLORS['button_hover'], fg="white",
                            font=("Segoe UI", 10),
                            bd=0, padx=15, pady=5,
                            cursor="hand2")
    refresh_btn.pack(side="left", padx=5)

    close_btn = tk.Button(button_frame, text="Close", command=win.destroy,
                          bg=COLORS['light_gray'], fg=COLORS['text_dark'],
                          font=("Segoe UI", 10),
                          bd=0, padx=20, pady=6,
                          cursor="hand2")
    close_btn.pack(side="right", padx=5)


def delete_event_from_all(date_str, event_text, parent_window):
    """Delete an event from the all events list"""
    events = load_events()
    if date_str in events:
        for i, event in enumerate(events[date_str]):
            if event.get('text') == event_text:
                if delete_event(date_str, i):
                    messagebox.showinfo("Success", "Event deleted!")
                    parent_window.destroy()
                    # Reopen window with updated list
                    show_all_events_window()
                    return
    messagebox.showerror("Error", "Failed to delete event!")