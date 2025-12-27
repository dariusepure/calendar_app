FONT = ("Segoe UI", 11)
BUTTON_FONT = ("Segoe UI", 10, "bold")
TITLE_FONT = ("Segoe UI", 18, "bold")

# Light theme (default)
LIGHT_THEME = {
    'background': "#f8fafc",
    'sidebar': "#1e3a8a",
    'button_normal': "#3b82f6",
    'button_hover': "#60a5fa",
    'primary': "#2563eb",
    'success': "#22c55e",
    'danger': "#ef4444",
    'light_gray': "#dbeafe",
    'dark_gray': "#6b7280",
    'text_light': "#ffffff",
    'text_dark': "#1e293b",
    'calendar_bg': "#ffffff",
    'border': "#93c5fd",
    'card_bg': "#ffffff",
    'input_bg': "#ffffff",
    'scrollbar_bg': "#e2e8f0",
    'header_bg': "#f1f5f9",
}

# Dark theme
DARK_THEME = {
    'background': "#0f172a",
    'sidebar': "#1e293b",
    'button_normal': "#3b82f6",
    'button_hover': "#60a5fa",
    'primary': "#60a5fa",
    'success': "#4ade80",
    'danger': "#f87171",
    'light_gray': "#334155",
    'dark_gray': "#94a3b8",
    'text_light': "#f8fafc",
    'text_dark': "#cbd5e1",
    'calendar_bg': "#1e293b",
    'border': "#475569",
    'card_bg': "#1e293b",
    'input_bg': "#334155",
    'scrollbar_bg': "#475569",
    'header_bg': "#334155",
}

# Current theme (starts with light)
COLORS = LIGHT_THEME.copy()
BUTTON_COLORS = {
    'main': "#2563eb",
    'events': "#3b82f6",
    'weekday': "#3b82f6",
    'add': "#2563eb",
    'subtract': "#2563eb",
    'count': "#2563eb",
}

# Theme management functions
def set_light_theme():
    """Switch to light theme"""
    global COLORS
    COLORS.clear()
    COLORS.update(LIGHT_THEME)

def set_dark_theme():
    """Switch to dark theme"""
    global COLORS
    COLORS.clear()
    COLORS.update(DARK_THEME)

def toggle_theme():
    """Toggle between light and dark themes"""
    if COLORS['background'] == LIGHT_THEME['background']:
        set_dark_theme()
        return "dark"
    else:
        set_light_theme()
        return "light"

def get_current_theme():
    """Get current theme name"""
    return "dark" if COLORS['background'] == DARK_THEME['background'] else "light"