import customtkinter as ctk
import tkinter.messagebox as messagebox
import db_manager

class RegistrationWindow:
    def __init__(self, master, parent):
        self.master = master
        self.parent = parent  # Reference to the login window
        self.master.title("Register")
        self.master.configure(bg="white")

        # Main Frame for Registration
        self.main_frame = ctk.CTkFrame(master, fg_color="white", corner_radius=20)
        self.main_frame.pack(pady=20, padx=20, expand=True, fill="both")  # Ensure it stretches to fill the window

        # Title Label
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Register",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#144d94"
        )
        self.title_label.pack(pady=(50, 20))

        # Username Entry
        self.entry_username = ctk.CTkEntry(
            self.main_frame,
            width=400,
            height=50,
            font=ctk.CTkFont(size=16),
            placeholder_text="Username"
        )
        self.entry_username.pack(pady=(20, 10))

        # Password Entry
        self.entry_password = ctk.CTkEntry(
            self.main_frame,
            width=400,
            height=50,
            font=ctk.CTkFont(size=16),
            show="*",
            placeholder_text="Password"
        )
        self.entry_password.pack(pady=(10, 10))

        # Confirm Password Entry
        self.entry_confirm_password = ctk.CTkEntry(
            self.main_frame,
            width=400,
            height=50,
            font=ctk.CTkFont(size=16),
            show="*",
            placeholder_text="Confirm Password"
        )
        self.entry_confirm_password.pack(pady=(10, 20))

        # Register Button
        self.button_register = ctk.CTkButton(
            self.main_frame,
            text="Register",
            command=self.register,
            width=250,
            height=50,
            font=ctk.CTkFont(size=16),
            fg_color="#144d94"
        )
        self.button_register.pack(pady=(20, 10))

        # Back to Login Button
        self.button_back = ctk.CTkButton(
            self.main_frame,
            text="Back to Login",
            command=self.back_to_login,
            width=250,
            height=50,
            font=ctk.CTkFont(size=16),
            fg_color="#07c4fc"
        )
        self.button_back.pack(pady=10)

    def register(self):
        """Handle the registration logic."""
        username = self.entry_username.get()
        password = self.entry_password.get()
        confirm_password = self.entry_confirm_password.get()

        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        try:
            db_manager.register_user(username, password)
            messagebox.showinfo("Success", "Registration successful!")
            self.back_to_login()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def back_to_login(self):
        self.master.destroy()  # Close the registration window
        self.parent.state("zoomed")  # Ensure the login window is maximized
        self.parent.deiconify()  # Show the login window again
