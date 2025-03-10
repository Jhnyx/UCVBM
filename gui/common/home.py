import customtkinter as ctk
from PIL import Image
import os
import db_manager
from gui.common.book_venue import BookVenueWindow


class HomePage:
    def __init__(self, master, parent_window, user_id, is_admin=False):
        self.master = master  # Content area (CTkFrame)
        self.parent_window = parent_window  # Main window (Tk or Toplevel)
        self.user_id = user_id
        self.is_admin = is_admin

        # Title
        title_label = ctk.CTkLabel(
            master,
            text="Home (List of Venues)",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#144d94",
        )
        title_label.pack(pady=20)

        # Create Scrollable Frame
        scrollable_frame = ctk.CTkScrollableFrame(master, fg_color="white", corner_radius=10)
        scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Fetch venues
        venues = db_manager.get_all_venues()
        if not venues:
            no_venues_label = ctk.CTkLabel(
                scrollable_frame, text="No venues available.", font=ctk.CTkFont(size=14), text_color="black"
            )
            no_venues_label.pack(pady=10)
        else:
            # Venue Cards
            for venue in venues:
                frame = ctk.CTkFrame(scrollable_frame, fg_color="#f8f9fa", corner_radius=10)
                frame.pack(pady=10, padx=20, fill="x", expand=True)

                # Display Image
                img_label = ctk.CTkLabel(frame, text="No Image")
                if venue[4] and os.path.exists(venue[4]):
                    try:
                        img = Image.open(venue[4])
                        img.thumbnail((300, 300))
                        img_display = ctk.CTkImage(light_image=img, size=(300, 300))
                        img_label = ctk.CTkLabel(frame, image=img_display, text="")
                    except Exception as e:
                        print(f"Error loading image for venue {venue[1]}: {e}")

                img_label.pack(side="left", padx=10)

                # Venue Details
                venue_label = ctk.CTkLabel(frame, text=f"Venue Name: {venue[1]}", font=ctk.CTkFont(size=14), text_color="black")
                venue_label.pack(side="left", padx=10)

                # Book Button
                book_button = ctk.CTkButton(
                    frame, text="Book Venue", fg_color="#07c4fc", command=lambda v=venue[0]: self.book_venue(v)
                )
                book_button.pack(side="right", padx=10)

        # Add empty frames for consistent spacing if venues < desired number (e.g., 5 rows)
        desired_rows = 5
        empty_rows = max(desired_rows - len(venues), 0)

        for _ in range(empty_rows):
            empty_frame = ctk.CTkFrame(scrollable_frame, fg_color="white", height=150)
            empty_frame.pack(pady=10, padx=20, fill="x", expand=True)

    def book_venue(self, venue_id):
        """Open the Book Venue window."""
        self.parent_window.withdraw()  # Hide the current HomePage
        booking_window = ctk.CTkToplevel(self.parent_window)  # Open the booking window as Toplevel
        booking_window.state("zoomed")  # Maximize the booking window
        BookVenueWindow(booking_window, self.parent_window, self.user_id, venue_id)
