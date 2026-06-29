# CalendarApp

A desktop calendar and time management utility built in Python using **Tkinter** for the graphical user interface. It provides an intuitive layout to track events and perform quick date-time calculations.

##  Features & Modular Architecture

The application is structured into modular Python files, keeping a clean separation of concerns:

- **`main.py` & `frame_manager.py`:** Coordinated the main application loop, layout switching, and key bindings (e.g., keyboard arrow navigation through months).
- **`calendar_view.py`:** Handles the grid rendering of the calendar month tables.
- **`event_manager.py`:** Manages the CRUD lifecycle of personal events (Add, View, Delete), saving them persistently in a local `calendar_events.json` file.
- **`calculators.py`:** Contains quick date utilities, including finding the weekday of a date, adding/subtracting days, and calculating precise durations.
- **`ui_components.py` & `styles.py`:** Defines the modern, custom sidebar navigation interface and unifies the blue-accent color palette.

##  How to Run

1. Open this project folder in your preferred Python environment (like VS Code or PyCharm).
2. Ensure you have Python 3.x installed.
3. Run the **`main.py`** script to launch the graphical window:
   ```bash
   python main.py
