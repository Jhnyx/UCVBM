import customtkinter as ctk
import db_manager
from PIL import Image  # Importing PIL to load the image properly
import os
import tkinter.messagebox as messagebox  # Using tkinter's messagebox for alerts

ctk.set_appearance_mode("light")  # Light mode
ctk.set_default_color_theme("blue")  # Default color theme

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")
        self.master.configure(bg="white")

        # Main Frame for Login
        self.main_frame = ctk.CTkFrame(master, fg_color="white", corner_radius=20)
        self.main_frame.pack(pady=20, padx=20, expand=True, fill="both")

        # UC Logo
        try:
            image_path = os.path.join("assets", "uc-logo.jpg")
            if os.path.exists(image_path):
                image = Image.open(image_path)
                self.logo = ctk.CTkImage(light_image=image, size=(300, 200))
                self.logo_label = ctk.CTkLabel(self.main_frame, image=self.logo, text="", fg_color="white")
                self.logo_label.pack(pady=20)
        except Exception as e:
            print(f"Error loading image: {e}")

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Venue Booking",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#144d94"
        )
        self.title_label.pack(pady=10)

        # Username Entry
        self.entry_username = ctk.CTkEntry(
            self.main_frame, width=300, height=40, font=ctk.CTkFont(size=14), placeholder_text="Username"
        )
        self.entry_username.pack(pady=(30, 10))

        # Password Entry
        self.entry_password = ctk.CTkEntry(
            self.main_frame, width=300, height=40, font=ctk.CTkFont(size=14), show="*", placeholder_text="Password"
        )
        self.entry_password.pack(pady=10)

        # Login Button
        self.button_login = ctk.CTkButton(
            self.main_frame,
            text="Login",
            command=self.login,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="#144d94"
        )
        self.button_login.pack(pady=(40, 10))

        # Register Button
        self.button_register = ctk.CTkButton(
            self.main_frame,
            text="Register",
            command=self.open_registration,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="#07c4fc"
        )
        self.button_register.pack(pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        user = db_manager.login_user(username, password)

        if user:
            user_id, is_admin = user
            if is_admin:
                self.master.withdraw()  # Hide the login window
                admin_window = ctk.CTkToplevel(self.master)  # Create a new Toplevel for the admin window
                admin_window.state("zoomed")  # Maximize the admin window
                from gui.admin_window import AdminWindow
                AdminWindow(admin_window, self.master, user_id)  # Pass the user_id and login window as parent
            else:
                self.master.withdraw()  # Hide the login window
                user_window = ctk.CTkToplevel(self.master)  # Create a new Toplevel for the user window
                user_window.state("zoomed")  # Maximize the user window
                from gui.user_window import UserWindow
                UserWindow(user_window, self.master, user_id)  # Pass the user_id and login window as parent
        else:
            messagebox.showerror("Error", "Invalid username or password")  # Show error message using tkinter.messagebox


    def open_registration(self):
        self.master.withdraw()  # Hide the login window
        registration_window = ctk.CTkToplevel(self.master)  # Create a new Toplevel
        registration_window.state("zoomed")  # Maximize the registration window
        from gui.registration_window import RegistrationWindow
        RegistrationWindow(registration_window, self.master)  # Pass the login window as parent
