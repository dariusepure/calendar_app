import calendar
from event_manager import get_events_for_date, on_calendar_click
from styles import COLORS


def show_calendar(year, month, cal_table, month_label):
    try:
        if month < 1 or month > 12:
            month = max(1, min(12, month))
        if year < 1 or year > 9999:
            year = max(1, min(9999, year))
    except (TypeError, ValueError):
        from datetime import datetime
        today = datetime.now()
        year, month = today.year, today.month
    for row in cal_table.get_children():
        cal_table.delete(row)
    month_label.config(text=f"{calendar.month_name[month]} {year}", fg=COLORS['primary'])
    cal = calendar.monthcalendar(year, month)
    while cal and all(day == 0 for day in cal[0]):
        cal.pop(0)
    while cal and all(day == 0 for day in cal[-1]):
        cal.pop()
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, day in enumerate(days_of_week):
        cal_table.heading(str(i), text=day)
        cal_table.column(str(i), width=78, anchor="center", stretch=False)
    cal_table.configure(selectmode="none", show="headings")
    for week in cal:
        values = []
        for day in week:
            if day == 0:
                values.append("")
            else:
                values.append(str(day))
        cal_table.insert("", "end", values=values)
    cal_table.configure(height=len(cal))
    cal_table.bind("<Button-1>", lambda e: on_calendar_click(e, year, month, cal_table))

def prev_month(y, m):
    return (y - 1, 12) if m == 1 else (y, m - 1)

def next_month(y, m):
    return (y + 1, 1) if m == 12 else (y, m + 1)

def prev_year(y, m):
    return y - 1, m

def next_year(y, m):
    return y + 1, m