import customtkinter as ctk
from tkinter import filedialog
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk
import os
import db_manager


class ManageVenuesPage:
    def __init__(self, master):
        self.master = master
        self.image_path = None
        self.uploaded_image = None
        self.assets_dir = "assets/venues"

        # Ensure the assets directory exists
        if not os.path.exists(self.assets_dir):
            os.makedirs(self.assets_dir)

        # Title
        title_label = ctk.CTkLabel(
            master,
            text="Manage Venues",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#144d94",
        )
        title_label.pack(pady=20)

        # Form Section
        form_frame = ctk.CTkFrame(master, fg_color="#f8f9fa", corner_radius=10)
        form_frame.pack(pady=10, padx=20, fill="x", expand=True)

        # Venue Name Entry
        self.venue_name_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="Enter venue name")
        self.venue_name_entry.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Image Display
        self.image_label = ctk.CTkLabel(form_frame, text="No Image Selected", font=ctk.CTkFont(size=14), text_color="gray")
        self.image_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Upload Image Button
        upload_button = ctk.CTkButton(
            form_frame, text="Upload Image", command=self.upload_image, fg_color="#07c4fc", width=120
        )
        upload_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        # Add Venue Button
        add_venue_button = ctk.CTkButton(
            form_frame, text="Add Venue", command=self.add_venue, fg_color="#144d94", width=120
        )
        add_venue_button.grid(row=1, column=2, padx=10, pady=10, sticky="e")

        # Existing Venues Section
        self.display_existing_venues()

    def upload_image(self):
        """Upload and display a venue image."""
        self.image_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=(("Image Files", "*.png;*.jpg;*.jpeg"), ("All Files", "*.*"))
        )
        if self.image_path:
            # Load and display the image
            image = Image.open(self.image_path)
            image.thumbnail((300, 300))  # Resize for display
            self.uploaded_image = ImageTk.PhotoImage(image)

            self.image_label.configure(image=self.uploaded_image, text="")
            messagebox.showinfo("Success", "Image selected successfully!")

    def add_venue(self):
        """Add a new venue with name and uploaded image."""
        venue_name = self.venue_name_entry.get()
        if not venue_name or not self.image_path:
            messagebox.showerror("Error", "Please provide both a venue name and an image.")
            return

        # Save the image in the assets directory
        image_filename = f"{venue_name.replace(' ', '_').lower()}.png"
        image_save_path = os.path.join(self.assets_dir, image_filename)
        try:
            with Image.open(self.image_path) as img:
                img.save(image_save_path)

            # Add venue to the database
            db_manager.add_venue(venue_name, image_save_path, 0)
            messagebox.showinfo("Success", f"Venue '{venue_name}' added successfully!")
            self.venue_name_entry.delete(0, "end")
            self.image_label.configure(image=None, text="No Image Selected")  # Reset image
            self.image_path = None
            self.display_existing_venues()  # Refresh venue table
        except Exception as e:
            messagebox.showerror("Error", f"Error saving venue image: {e}")

    def display_existing_venues(self):
        """Display a table of existing venues with consistent image sizes."""
        # Clear previous widgets
        for widget in self.master.winfo_children()[2:]:  # Skip title and form widgets
            widget.destroy()

        # Section Title
        section_title = ctk.CTkLabel(
            self.master, text="Existing Venues", font=ctk.CTkFont(size=20, weight="bold"), text_color="#144d94"
        )
        section_title.pack(pady=10)

        # Fetch existing venues
        venues = db_manager.get_all_venues()

        if not venues:
            no_venues_label = ctk.CTkLabel(
                self.master, text="No venues have been added yet.", font=ctk.CTkFont(size=14), text_color="gray"
            )
            no_venues_label.pack(pady=10)
            return

        # Scrollable Frame
        scrollable_frame = ctk.CTkScrollableFrame(self.master, fg_color="white", corner_radius=10)
        scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Venue Rows
        for venue in venues:
            venue_frame = ctk.CTkFrame(scrollable_frame, fg_color="#ffffff", corner_radius=10)
            venue_frame.pack(pady=5, padx=20, fill="x", expand=True)

            # Image
            img_label = ctk.CTkLabel(venue_frame, text="No Image")
            if venue[4] and os.path.exists(venue[4]):
                try:
                    img = Image.open(venue[4])
                    img = img.resize((300, 300))  # Force consistent size
                    img_display = ImageTk.PhotoImage(img)
                    img_label = ctk.CTkLabel(venue_frame, image=img_display, text="")
                    img_label.image = img_display  # Keep a reference to avoid garbage collection
                except Exception as e:
                    print(f"Error loading image for venue {venue[1]}: {e}")

            img_label.pack(side="left", padx=10)

            # Fetch Pending and Approved Bookings Count
            pending_count = db_manager.get_booking_count(venue[0], status=0)  # Pending bookings
            approved_count = db_manager.get_booking_count(venue[0], status=1)  # Approved bookings

            # Details
            venue_details = (
                f"Venue Name: {venue[1]}\n"
                f"Pending Bookings: {pending_count}\n"
                f"Approved Bookings: {approved_count}"
            )
            venue_label = ctk.CTkLabel(venue_frame, text=venue_details, font=ctk.CTkFont(size=12), text_color="black",
                                       justify="left")
            venue_label.pack(side="left", padx=10)

            # Delete Button
            delete_button = ctk.CTkButton(
                venue_frame, text="Delete", fg_color="#d9534f", command=lambda v=venue[0]: self.delete_venue(v)
            )
            delete_button.pack(side="right", padx=10)

        # Add empty frames for consistent spacing if venues < desired rows (e.g., 5 rows)
        desired_rows = 5
        empty_rows = max(desired_rows - len(venues), 0)
        for _ in range(empty_rows):
            empty_frame = ctk.CTkFrame(scrollable_frame, fg_color="white", height=150)
            empty_frame.pack(pady=5, padx=20, fill="x", expand=True)

    def delete_venue(self, venue_id):
        """Delete a venue and all related data."""
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this venue?")
        if confirm:
            try:
                # Get venue details
                venue = db_manager.get_venue_by_id(venue_id)
                if not venue:
                    messagebox.showerror("Error", "Venue not found.")
                    return

                # Remove the associated image file
                image_path = venue[4]  # Assuming the image path is the 5th column
                if image_path and os.path.exists(image_path):
                    os.remove(image_path)

                # Delete the venue and related bookings from the database
                db_manager.delete_venue(venue_id)
                messagebox.showinfo("Success", "Venue and related data deleted successfully!")
                self.display_existing_venues()  # Refresh venue table
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting venue: {e}")
