import customtkinter as ctk
import tkinter.messagebox as messagebox
from gui.admin.manage_venues import ManageVenuesPage
from gui.admin.manage_users import ManageUsersPage
from gui.common.home import HomePage
from gui.common.manage_bookings import ManageBookingsPage


class AdminWindow:
    def __init__(self, master, parent, user_id):
        self.master = master
        self.parent = parent  # Reference to the login window
        self.user_id = user_id  # Add user_id attribute for proper initialization

        self.master.title("Admin Dashboard - Venue Booking")
        self.master.configure(bg="white")

        # Main Layout: Sidebar + Content
        self.sidebar = ctk.CTkFrame(self.master, width=200, corner_radius=0, fg_color="#144d94")
        self.sidebar.pack(side="left", fill="y")

        self.content = ctk.CTkFrame(self.master, fg_color="white")
        self.content.pack(side="right", fill="both", expand=True)

        # Sidebar Buttons
        self.create_sidebar()

        # Default Page: Home
        self.show_home_page()

    def create_sidebar(self):
        """Create buttons for the left sidebar."""
        # App Title
        title_label = ctk.CTkLabel(
            self.sidebar, text="Admin Menu", font=ctk.CTkFont(size=20, weight="bold"), text_color="white"
        )
        title_label.pack(pady=20)

        # Home Button
        home_button = ctk.CTkButton(
            self.sidebar, text="Home", command=self.show_home_page, fg_color="#07c4fc", width=180, height=40
        )
        home_button.pack(pady=10)

        # Manage Venues Button
        manage_venues_button = ctk.CTkButton(
            self.sidebar, text="Manage Venues", command=self.show_manage_venues, fg_color="#07c4fc", width=180, height=40
        )
        manage_venues_button.pack(pady=10)

        # Manage Bookings Button
        manage_bookings_button = ctk.CTkButton(
            self.sidebar, text="Manage Bookings", command=self.show_manage_bookings, fg_color="#07c4fc", width=180,
            height=40
        )
        manage_bookings_button.pack(pady=10)

        # Manage Users Button
        manage_users_button = ctk.CTkButton(
            self.sidebar, text="Manage Users", command=self.show_manage_users, fg_color="#07c4fc", width=180, height=40
        )
        manage_users_button.pack(pady=10)

        # Logout Button
        logout_button = ctk.CTkButton(
            self.sidebar, text="Logout", command=self.logout, fg_color="#d9534f", width=180, height=40
        )
        logout_button.pack(pady=10)

    def show_home_page(self):
        """Show the Home Page."""
        self.clear_content()
        HomePage(self.content, self.master, self.user_id, is_admin=True)

    def show_manage_venues(self):
        """Show the Manage Venues Page."""
        self.clear_content()
        ManageVenuesPage(self.content)

    def show_manage_bookings(self):
        """Show the Manage Bookings Page."""
        self.clear_content()
        ManageBookingsPage(self.content, is_admin=True)

    def show_manage_users(self):
        """Show the Manage Users Page."""
        self.clear_content()
        ManageUsersPage(self.content)

    def clear_content(self):
        """Clear the content area."""
        for widget in self.content.winfo_children():
            widget.destroy()

    def logout(self):
        """Logout the admin and return to the login screen."""
        confirm = messagebox.askyesno("Logout", "Are you sure you want to log out?")
        if confirm:
            self.master.destroy()  # Close the admin window
            self.parent.state("zoomed")  # Maximize and show the login window
            self.parent.deiconify()
