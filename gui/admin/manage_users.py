import customtkinter as ctk
import tkinter.messagebox as messagebox
import db_manager


class ManageUsersPage:
    def __init__(self, master):
        self.master = master

        # Title
        title_label = ctk.CTkLabel(
            master,
            text="Manage Users",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#144d94",
        )
        title_label.pack(pady=20)

        # Scrollable Frame for users
        self.scrollable_frame = ctk.CTkScrollableFrame(master, fg_color="white", corner_radius=10)
        self.scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Display users
        self.display_users()

    def display_users(self):
        """Fetch and display all users."""
        # Fetch users excluding admin
        users = db_manager.get_all_users(exclude_admin=True)

        # Check if users exist
        if not users:
            no_users_label = ctk.CTkLabel(
                self.scrollable_frame, text="No users found.", font=ctk.CTkFont(size=14), text_color="black"
            )
            no_users_label.pack(pady=10)
            return

        # Display each user with their stats
        for user in users:
            user_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#f8f9fa", corner_radius=10)
            user_frame.pack(pady=10, padx=20, fill="x", expand=True)

            # Fetch user statistics
            total_bookings = db_manager.get_total_bookings(user[0])
            total_approved = db_manager.get_total_bookings_by_status(user[0], 1)
            total_denied = db_manager.get_total_bookings_by_status(user[0], -1)

            # User Details
            user_details = (
                f"Username: {user[1]}\n"
                f"Total Bookings: {total_bookings}\n"
                f"Total Approved: {total_approved}\n"
                f"Total Denied: {total_denied}"
            )
            user_label = ctk.CTkLabel(user_frame, text=user_details, font=ctk.CTkFont(size=12), justify="left")
            user_label.pack(side="left", padx=10)

            # Delete Button
            delete_button = ctk.CTkButton(
                user_frame, text="Delete", fg_color="#d9534f", command=lambda u=user[0]: self.delete_user(u)
            )
            delete_button.pack(side="right", padx=10)

    def delete_user(self, user_id):
        """Delete a user."""
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this user?")
        if confirm:
            db_manager.delete_user(user_id)
            messagebox.showinfo("Success", "User deleted successfully!")
            self.display_users()  # Refresh the page
