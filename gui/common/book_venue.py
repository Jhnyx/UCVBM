import customtkinter as ctk
from tkcalendar import Calendar  # Install with `pip install tkcalendar`
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import db_manager


class BookVenueWindow:
    def __init__(self, master, parent_window, user_id, venue_id):
        self.master = master
        self.parent_window = parent_window  # Reference to the parent window (HomePage)
        self.user_id = user_id
        self.venue_id = venue_id

        self.master.title("Book Venue")
        self.master.state("zoomed")  # Maximize the booking form
        self.master.configure(bg="white")

        # Fetch venue details
        venue = db_manager.get_venue_by_id(self.venue_id)

        # Main Layout: Left for details, Right for form
        self.main_frame = ctk.CTkFrame(master, fg_color="white")
        self.main_frame.pack(padx=0, pady=0, fill="both", expand=True)

        # Add "Go Back" button at the top-right
        go_back_button = ctk.CTkButton(
            self.main_frame,
            text="Go Back",
            fg_color="#d9534f",
            command=self.go_back,
            width=100,
            height=30
        )
        go_back_button.pack(side="top", anchor="nw", padx=10, pady=10)

        # Venue Details (Left Side)
        self.venue_frame = ctk.CTkFrame(self.main_frame, fg_color="white", corner_radius=10, width=300)
        self.venue_frame.pack(side="left", padx=25, pady=25, fill="y")

        # Venue Image
        if venue[4] and os.path.exists(venue[4]):
            try:
                img = Image.open(venue[4])
                img.thumbnail((700, 700))
                img_display = ImageTk.PhotoImage(img)
                img_label = ctk.CTkLabel(self.venue_frame, image=img_display, text="")
                img_label.image = img_display  # Keep a reference to prevent garbage collection
                img_label.pack(pady=10)
            except Exception as e:
                print(f"Error loading image for venue: {e}")
                img_label = ctk.CTkLabel(self.venue_frame, text="No Image Available")
                img_label.pack(pady=10)
        else:
            img_label = ctk.CTkLabel(self.venue_frame, text="No Image Available")
            img_label.pack(pady=10)

        # Venue Name
        venue_name_label = ctk.CTkLabel(
            self.venue_frame,
            text=f"Venue Name: {venue[1]}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#144d94",
        )
        venue_name_label.pack(pady=10)

        # Booking Form (Right Side)
        self.form_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        self.form_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)

        # Event Name Entry
        self.event_name_entry = ctk.CTkEntry(self.form_frame, width=400, placeholder_text="Event Name")
        self.event_name_entry.pack(pady=5)

        # Purpose Entry
        self.purpose_entry = ctk.CTkEntry(self.form_frame, width=400, placeholder_text="Purpose")
        self.purpose_entry.pack(pady=5)

        # Group Start and End Date in a single frame
        date_frame = ctk.CTkFrame(self.form_frame, fg_color="white")
        date_frame.pack(pady=5, fill="y")

        start_date_label = ctk.CTkLabel(date_frame, text="Start Date:", font=ctk.CTkFont(size=14))
        start_date_label.grid(row=0, column=0, padx=10)
        self.start_calendar = Calendar(date_frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.start_calendar.grid(row=1, column=0, padx=10)

        end_date_label = ctk.CTkLabel(date_frame, text="End Date:", font=ctk.CTkFont(size=14))
        end_date_label.grid(row=0, column=1, padx=10)
        self.end_calendar = Calendar(date_frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.end_calendar.grid(row=1, column=1, padx=10)

        # Time Range
        time_frame = ctk.CTkFrame(self.form_frame, fg_color="white")
        time_frame.pack(pady=5, fill="y")

        start_time_label = ctk.CTkLabel(time_frame, text="Start Time:", font=ctk.CTkFont(size=14))
        start_time_label.grid(row=0, column=0, padx=10, pady=5)

        self.start_hour = ctk.StringVar(value="00")
        self.start_minute = ctk.StringVar(value="00")
        self.create_time_dropdowns(time_frame, self.start_hour, self.start_minute, row=0, col_offset=1)

        end_time_label = ctk.CTkLabel(time_frame, text="End Time:", font=ctk.CTkFont(size=14))
        end_time_label.grid(row=1, column=0, padx=10, pady=5)

        self.end_hour = ctk.StringVar(value="00")
        self.end_minute = ctk.StringVar(value="00")
        self.create_time_dropdowns(time_frame, self.end_hour, self.end_minute, row=1, col_offset=1)

        # Submit Button
        submit_button = ctk.CTkButton(
            self.form_frame, text="Submit", fg_color="#144d94", command=self.submit_booking
        )
        submit_button.pack(pady=10)

    def create_time_dropdowns(self, frame, hour_var, minute_var, row, col_offset):
        """Create hour and minute dropdowns for time selection."""
        hours = [f"{i:02d}" for i in range(24)]  # 00 to 23
        minutes = [f"{i:02d}" for i in range(0, 60, 15)]  # 00, 15, 30, 45

        hour_dropdown = ctk.CTkComboBox(frame, values=hours, variable=hour_var)
        hour_dropdown.grid(row=row, column=col_offset, padx=5, pady=5)

        colon_label = ctk.CTkLabel(frame, text=":", font=("Arial", 12))
        colon_label.grid(row=row, column=col_offset + 1)

        minute_dropdown = ctk.CTkComboBox(frame, values=minutes, variable=minute_var)
        minute_dropdown.grid(row=row, column=col_offset + 2, padx=5, pady=5)

    def submit_booking(self):
        """Handle booking submission."""
        start_date = self.start_calendar.get_date()
        end_date = self.end_calendar.get_date()
        start_time = f"{self.start_hour.get()}:{self.start_minute.get()}"
        end_time = f"{self.end_hour.get()}:{self.end_minute.get()}"
        purpose = self.purpose_entry.get()
        event_name = self.event_name_entry.get()

        # Validation
        if not purpose or not event_name:
            messagebox.showerror("Error", "Purpose and Event Name are required.")
            return

        if start_date > end_date:
            messagebox.showerror("Error", "Start date cannot be after end date.")
            return

        time_range = f"{start_date} {start_time} - {end_date} {end_time}"

        try:
            db_manager.book_venue(self.user_id, self.venue_id, start_date, time_range, purpose, event_name)
            messagebox.showinfo("Success", "Booking request submitted successfully.")
            self.master.destroy()  # Close the booking window
            self.parent_window.deiconify()  # Show the HomePage window again
            self.parent_window.state("zoomed")  # Maximize the HomePage window
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def go_back(self):
        """Return to the parent window."""
        self.master.destroy()  # Close the current window
        self.parent_window.deiconify()  # Reopen the parent window
        self.parent_window.state("zoomed")  # Maximize the parent window
