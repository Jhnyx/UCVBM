import db_manager
import tkinter as tk
from gui.login_window import LoginWindow

if __name__ == "__main__":
    # Ensure that the database and tables are set up
    db_manager.create_tables()

    # Launch the application with the login window
    root = tk.Tk()
    root.state("zoomed")  # Ensure the main window starts maximized
    root.title("UC Venue Booking Management")
    login_window = LoginWindow(root)
    root.mainloop()
