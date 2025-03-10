import customtkinter as ctk
import tkinter.messagebox as messagebox
from gui.common.home import HomePage
from gui.common.manage_bookings import ManageBookingsPage


class UserWindow:
    def __init__(self, master, parent, user_id):
        self.master = master
        self.parent = parent  # Reference to the login window
        self.user_id = user_id

        self.master.title("User Home - Venue Booking")
        self.master.configure(bg="white")

        # Main Layout: Sidebar + Content
        self.sidebar = ctk.CTkFrame(self.master, width=200, corner_radius=0, fg_color="#144d94")
        self.sidebar.pack(side="left", fill="y")

        self.content = ctk.CTkFrame(self.master, fg_color="white")
        self.content.pack(side="right", fill="both", expand=True)

        # Sidebar Buttons
        self.create_sidebar()

        # Default Page: Home (List of Venues)
        self.show_home_page()

    def create_sidebar(self):
        """Create buttons for the left sidebar."""
        # App Title
        title_label = ctk.CTkLabel(
            self.sidebar, text="Menu", font=ctk.CTkFont(size=20, weight="bold"), text_color="white"
        )
        title_label.pack(pady=20)

        # Home Button
        home_button = ctk.CTkButton(
            self.sidebar, text="Home", command=self.show_home_page, fg_color="#07c4fc", width=180, height=40
        )
        home_button.pack(pady=10)

        # My Bookings Button
        my_bookings_button = ctk.CTkButton(
            self.sidebar, text="My Bookings", command=self.show_my_bookings, fg_color="#07c4fc", width=180, height=40
        )
        my_bookings_button.pack(pady=10)

        # Logout Button
        logout_button = ctk.CTkButton(
            self.sidebar, text="Logout", command=self.logout, fg_color="#d9534f", width=180, height=40
        )
        logout_button.pack(pady=10)

    def show_home_page(self):
        """Show the Home Page."""
        self.clear_content()
        HomePage(self.content, self.master, self.user_id, is_admin=False)

    def show_my_bookings(self):
        """Show the user's bookings."""
        self.clear_content()
        ManageBookingsPage(self.content, is_admin=False, user_id=self.user_id)

    def clear_content(self):
        """Clear the content area."""
        for widget in self.content.winfo_children():
            widget.destroy()

    def logout(self):
        """Logout the user and return to the login screen."""
        confirm = messagebox.askyesno("Logout", "Are you sure you want to log out?")
        if confirm:
            self.master.destroy()  # Close the user window
            self.parent.state("zoomed")  # Maximize and show the login window
            self.parent.deiconify()
