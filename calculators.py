import calendar
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from styles import FONT, TITLE_FONT


def get_int_from_spinbox(spinbox, default=1):
    try:
        return int(spinbox.get())
    except ValueError:
        return default


def get_valid_date(day_spin, month_spin, year_spin):
    y = get_int_from_spinbox(year_spin, datetime.now().year)
    m = get_int_from_spinbox(month_spin, datetime.now().month)
    d = get_int_from_spinbox(day_spin, datetime.now().day)

    # Validate month range
    if m < 1 or m > 12:
        m = max(1, min(12, m))

    try:
        last_day = calendar.monthrange(y, m)[1]
        if d > last_day:
            d = last_day
        elif d < 1:
            d = 1
        return datetime(y, m, d), d
    except ValueError:
        # Fallback to current date if invalid
        today = datetime.now()
        return today, today.day


def get_week_of_year(date):
    return date.isocalendar()[1]


# Duration calculation
def calculate_duration_details(d1, d2):
    if d1 > d2:
        d1, d2 = d2, d1

    total_days = (d2 - d1).days
    years = d2.year - d1.year
    months = d2.month - d1.month

    if months < 0:
        years -= 1
        months += 12

    days = d2.day - d1.day
    if days < 0:
        months -= 1
        if months < 0:
            years -= 1
            months += 12

        prev_month = d2.month - 1 if d2.month > 1 else 12
        prev_year = d2.year if d2.month > 1 else d2.year - 1
        days_in_prev_month = calendar.monthrange(prev_year, prev_month)[1]
        days = days_in_prev_month - d1.day + d2.day

    weeks = total_days // 7
    remaining_days = total_days % 7

    # Calculate weekdays and weekends
    weekdays = 0
    weekends = 0
    current = d1
    while current <= d2:
        if current.weekday() < 5:
            weekdays += 1
        else:
            weekends += 1
        current += timedelta(days=1)

    return {
        'total_days': total_days,
        'years': years,
        'months': months,
        'days': days,
        'weeks': weeks,
        'remaining_days': remaining_days,
        'weekdays': weekdays,
        'weekends': weekends
    }


# Calculator functions
def weekday_function(frame_name, day_spin, month_spin, year_spin, result_label):
    try:
        d, corrected_day = get_valid_date(day_spin[frame_name], month_spin[frame_name], year_spin[frame_name])
        wd = d.strftime('%A')
        week_number = get_week_of_year(d)
        result_label.config(
            text=f"{d.strftime('%B %d, %Y')} is a {wd}\nWeek {week_number} of {d.year}",
            foreground="#27ae60"
        )
    except Exception as e:
        result_label.config(text=f"Error: Invalid date - {str(e)}", foreground="#e74c3c")


def add_days_function(frame_name, day_spin, month_spin, year_spin, days_entry, result_label):
    try:
        d, corrected_day = get_valid_date(day_spin[frame_name], month_spin[frame_name], year_spin[frame_name])
        add_text = days_entry[frame_name].get()
        if not add_text:
            raise ValueError("Days field is empty")
        add = int(add_text)
        if add < 0:
            raise ValueError("Days to add must be positive")
        new_date = d + timedelta(days=add)
        week_number = get_week_of_year(new_date)
        result_label.config(
            text=f"New date: {new_date.strftime('%A, %B %d, %Y')}\nWeek {week_number} of {new_date.year}\n({add} days added)",
            foreground="#27ae60"
        )
    except ValueError as e:
        result_label.config(text=f"Error: {str(e)}", foreground="#e74c3c")
    except Exception as e:
        result_label.config(text="Error: Please check the input", foreground="#e74c3c")


def subtract_days_function(frame_name, day_spin, month_spin, year_spin, days_entry, result_label):
    try:
        d, corrected_day = get_valid_date(day_spin[frame_name], month_spin[frame_name], year_spin[frame_name])
        sub_text = days_entry[frame_name].get()
        if not sub_text:
            raise ValueError("Days field is empty")
        sub = int(sub_text)
        if sub < 0:
            raise ValueError("Days to subtract must be positive")
        new_date = d - timedelta(days=sub)
        week_number = get_week_of_year(new_date)
        result_label.config(
            text=f"New date: {new_date.strftime('%A, %B %d, %Y')}\nWeek {week_number} of {new_date.year}\n({sub} days subtracted)",
            foreground="#27ae60"
        )
    except ValueError as e:
        result_label.config(text=f"Error: {str(e)}", foreground="#e74c3c")
    except Exception as e:
        result_label.config(text="Error: Please check the input", foreground="#e74c3c")


def duration_function(frame_name, day_spin, month_spin, year_spin, day_spin2, month_spin2, year_spin2, result_label):
    try:
        d1, corrected_day1 = get_valid_date(day_spin[frame_name], month_spin[frame_name], year_spin[frame_name])
        d2, corrected_day2 = get_valid_date(day_spin2[frame_name], month_spin2[frame_name], year_spin2[frame_name])

        duration = calculate_duration_details(d1, d2)
        week1 = get_week_of_year(d1)
        week2 = get_week_of_year(d2)

        result_text = (
            f"Duration between {d1.strftime('%d/%m/%Y')} and {d2.strftime('%d/%m/%Y')}:\n\n"
            f"Week {week1} of {d1.year} → Week {week2} of {d2.year}\n"
            f"• {duration['total_days']} total days\n"
            f"• {duration['years']} years, {duration['months']} months, {duration['days']} days\n"
            f"• {duration['weeks']} weeks and {duration['remaining_days']} days\n"
            f"• {duration['weekdays']} weekdays\n"
            f"• {duration['weekends']} weekend days"
        )

        result_label.config(text=result_text, foreground="#27ae60")
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}", foreground="#e74c3c")


def working_days_function(frame_name, day_spin, month_spin, year_spin, day_spin2, month_spin2, year_spin2,
                          result_label):
    try:
        d1, corrected_day1 = get_valid_date(day_spin[frame_name], month_spin[frame_name], year_spin[frame_name])
        d2, corrected_day2 = get_valid_date(day_spin2[frame_name], month_spin2[frame_name], year_spin2[frame_name])

        if d1 > d2:
            d1, d2 = d2, d1

        duration = calculate_duration_details(d1, d2)
        week1 = get_week_of_year(d1)
        week2 = get_week_of_year(d2)

        result_text = (
            f"Business Days Calculation:\n\n"
            f"• Period: {d1.strftime('%d/%m/%Y')} (Week {week1}) to {d2.strftime('%d/%m/%Y')} (Week {week2})\n"
            f"• Total days: {duration['total_days'] + 1}\n"
            f"• Business days: {duration['weekdays']}\n"
            f"• Weekend days: {duration['weekends']}\n"
            f"• Duration: {duration['weeks']} weeks, {duration['remaining_days']} days"
        )

        result_label.config(text=result_text, foreground="#27ae60")
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}", foreground="#e74c3c")


def week_calculator_function(frame_name, day_spin, month_spin, year_spin, weeks_spin, extra_days_spin, result_label,
                             add=True):
    try:
        d, corrected_day = get_valid_date(day_spin[frame_name], month_spin[frame_name], year_spin[frame_name])
        weeks = get_int_from_spinbox(weeks_spin[frame_name], 1)
        extra_days = get_int_from_spinbox(extra_days_spin[frame_name], 0)

        if weeks < 0:
            raise ValueError("Weeks must be positive")
        if extra_days < 0:
            raise ValueError("Extra days must be positive")

        total_days = weeks * 7 + extra_days

        if add:
            new_date = d + timedelta(days=total_days)
            operation = f"Added {weeks} weeks"
            if extra_days > 0:
                operation += f" and {extra_days} days"
        else:
            new_date = d - timedelta(days=total_days)
            operation = f"Subtracted {weeks} weeks"
            if extra_days > 0:
                operation += f" and {extra_days} days"

        original_week = get_week_of_year(d)
        new_week = get_week_of_year(new_date)

        result_label.config(
            text=f"{operation}\n"
                 f"Original date: {d.strftime('%B %d, %Y')} (Week {original_week})\n"
                 f"New date: {new_date.strftime('%A, %B %d, %Y')} (Week {new_week})",
            foreground="#27ae60"
        )
    except ValueError as e:
        result_label.config(text=f"Error: {str(e)}", foreground="#e74c3c")
    except Exception as e:
        result_label.config(text="Error: Please check the input", foreground="#e74c3c")


def show_week_number_function(frame_name, day_spin, month_spin, year_spin, result_label):
    try:
        d, corrected_day = get_valid_date(day_spin[frame_name], month_spin[frame_name], year_spin[frame_name])
        week_number = get_week_of_year(d)
        start_of_week = d - timedelta(days=d.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        result_label.config(
            text=f"Week Information:\n\n"
                 f"• Date: {d.strftime('%A, %B %d, %Y')}\n"
                 f"• Week {week_number} of {d.year}\n"
                 f"• Week period: {start_of_week.strftime('%B %d')} - {end_of_week.strftime('%B %d, %Y')}\n"
                 f"• Days in week {week_number}: 7",
            foreground="#27ae60"
        )
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}", foreground="#e74c3c")