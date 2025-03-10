import customtkinter as ctk
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk
import os
import db_manager


class ManageBookingsPage:
    def __init__(self, master, is_admin=False, user_id=None):
        self.master = master
        self.is_admin = is_admin
        self.user_id = user_id
        self.current_filter = "Pending"  # Default filter

        # Title
        title_label = ctk.CTkLabel(
            master,
            text="Manage Bookings" if is_admin else "My Bookings",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#144d94",
        )
        title_label.pack(pady=20)

        # Filter Section
        self.create_filter_section()

        # Scrollable Frame for bookings
        self.scrollable_frame = ctk.CTkScrollableFrame(master, fg_color="white", corner_radius=10)
        self.scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Display bookings based on the current filter
        self.display_bookings()

    def create_filter_section(self):
        """Create filter buttons for booking statuses."""
        self.filter_frame = ctk.CTkFrame(self.master, fg_color="white")
        self.filter_frame.pack(pady=10)

        self.pending_button = ctk.CTkButton(
            self.filter_frame, text="Pending", fg_color="#07c4fc",
            command=lambda: self.set_filter("Pending"), width=100
        )
        self.pending_button.grid(row=0, column=0, padx=5)

        self.approved_button = ctk.CTkButton(
            self.filter_frame, text="Approved", fg_color="#5cb85c",
            command=lambda: self.set_filter("Approved"), width=100
        )
        self.approved_button.grid(row=0, column=1, padx=5)

        self.denied_button = ctk.CTkButton(
            self.filter_frame, text="Denied", fg_color="#d9534f",
            command=lambda: self.set_filter("Denied"), width=100
        )
        self.denied_button.grid(row=0, column=2, padx=5)

        # Set the initial active state
        self.update_filter_colors()

    def set_filter(self, status):
        """Set the current filter and refresh bookings."""
        self.current_filter = status
        self.update_filter_colors()
        self.display_bookings()

    def update_filter_colors(self):
        """Update button colors based on the active filter."""
        # Reset all buttons to their default colors
        self.pending_button.configure(fg_color="#07c4fc" if self.current_filter != "Pending" else "#0056b3")
        self.approved_button.configure(fg_color="#5cb85c" if self.current_filter != "Approved" else "#3d8b3d")
        self.denied_button.configure(fg_color="#d9534f" if self.current_filter != "Denied" else "#b12a2a")

    def display_bookings(self):
        """Fetch and display bookings based on the filter."""
        # Clear previous widgets in the scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Fetch bookings based on the filter
        if self.is_admin:
            if self.current_filter == "Pending":
                bookings = db_manager.get_pending_bookings()
            elif self.current_filter == "Approved":
                bookings = db_manager.get_approved_bookings()
            elif self.current_filter == "Denied":
                bookings = db_manager.get_denied_bookings()
            elif self.current_filter == "Canceled":
                bookings = db_manager.get_canceled_bookings()
        else:
            bookings = db_manager.get_user_bookings(self.user_id)
            # Filter user bookings by status
            bookings = [
                booking for booking in bookings
                if (self.current_filter == "Pending" and booking[8] == 0) or
                   (self.current_filter == "Approved" and booking[8] == 1) or
                   (self.current_filter == "Denied" and booking[8] == -1) or
                   (self.current_filter == "Canceled" and booking[8] == -2)
            ]

        # Check if there are any bookings to display
        if not bookings:
            no_bookings_label = ctk.CTkLabel(
                self.scrollable_frame, text="No bookings found.", font=ctk.CTkFont(size=14), text_color="black"
            )
            no_bookings_label.pack(pady=10)
            return

        # Display each booking
        for booking in bookings:
            venue_image = booking[3]  # Image path from query
            venue_name = booking[2]  # Venue name from query

            frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#f8f9fa", corner_radius=10)
            frame.pack(pady=10, padx=20, fill="x", expand=True)

            # Display Venue Image
            img_label = ctk.CTkLabel(frame, text="No Image")
            if venue_image and os.path.exists(venue_image):
                try:
                    img = Image.open(venue_image)
                    img = img.resize((300, 300))  # Resize to consistent size without anti-aliasing
                    img_display = ImageTk.PhotoImage(img)
                    img_label = ctk.CTkLabel(frame, image=img_display, text="")
                    img_label.image = img_display  # Keep a reference to prevent garbage collection
                except Exception as e:
                    print(f"Error loading image for venue {venue_name}: {e}")

            img_label.pack(side="left", padx=10)

            # Safely handle the time_range field
            time_range_parts = booking[5].split(' - ') if booking[5] else ["Unknown", "Unknown"]
            start_date = time_range_parts[0] if len(time_range_parts) > 0 else "Unknown"
            end_date = time_range_parts[1] if len(time_range_parts) > 1 else "Unknown"

            # Booking Details
            details = (
                f"Venue Name: {venue_name}\n"
                f"Purpose: {booking[6]}\n"
                f"Date Started: {start_date}\n"
                f"Date Ended: {end_date}\n"
                f"Status: {self.current_filter}"
            )
            booking_label = ctk.CTkLabel(frame, text=details, font=ctk.CTkFont(size=12), justify="left")
            booking_label.pack(side="left", padx=10)

            if self.is_admin and self.current_filter == "Pending":
                # Admin Actions: Approve/Deny
                approve_button = ctk.CTkButton(
                    frame, text="Approve", fg_color="#5cb85c",
                    command=lambda b=booking[0]: self.approve_booking(b)
                )
                approve_button.pack(side="right", padx=5)

                deny_button = ctk.CTkButton(
                    frame, text="Deny", fg_color="#d9534f",
                    command=lambda b=booking[0]: self.deny_booking(b)
                )
                deny_button.pack(side="right", padx=5)
            elif not self.is_admin and self.current_filter == "Pending":
                # User Actions: Cancel
                cancel_button = ctk.CTkButton(
                    frame, text="Cancel Booking", fg_color="#d9534f",
                    command=lambda b=booking[0]: self.cancel_booking(b)
                )
                cancel_button.pack(side="right", padx=10)

        # Add empty frames for consistent spacing if bookings < desired number (e.g., 5 rows)
        desired_rows = 5
        empty_rows = max(desired_rows - len(bookings), 0)
        for _ in range(empty_rows):
            empty_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="white", height=150)
            empty_frame.pack(pady=10, padx=20, fill="x", expand=True)

    def approve_booking(self, booking_id):
        """Approve a pending booking."""
        db_manager.approve_booking(booking_id)
        messagebox.showinfo("Success", "Booking approved!")
        self.display_bookings()

    def deny_booking(self, booking_id):
        """Deny a pending booking."""
        db_manager.deny_booking(booking_id)
        messagebox.showinfo("Success", "Booking denied!")
        self.display_bookings()

    def cancel_booking(self, booking_id):
        """Cancel a user's booking."""
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to cancel this booking?")
        if confirm:
            db_manager.delete_booking(booking_id)
            messagebox.showinfo("Success", "Booking canceled!")
            self.display_bookings()
