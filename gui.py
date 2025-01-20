import tkinter as tk
from tkinter import messagebox
import mysql
from db_connection import connect_db
from login import validate_login
from user_dashboard import UserApps
from admin_dashboard import AdminApps
from guest_view import GuestApps
import re
from PIL import Image, ImageTk  # Importing PIL for handling images


ADMIN_KEY = "000"  # Admin key for registration
def resize_image(image, max_width, max_height):
    """
    Resizes the image while maintaining its aspect ratio, but keeps it as close to the original size as possible.
    """
    original_width, original_height = image.size
    aspect_ratio = original_width / original_height


    # Resize only if the image is larger than the screen dimensions
    if original_width > max_width or original_height > max_height:
        if aspect_ratio > 1:  # Landscape
            new_width = min(max_width, original_width)
            new_height = int(new_width / aspect_ratio)
        else:  # Portrait or square
            new_height = min(max_height, original_height)
            new_width = int(new_height * aspect_ratio)


        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        return resized_image
    else:
        # Return the original image if it fits the screen size
        return image




def show_registration_window(root):
    """
    Displays the registration window where users or admins can register.
    """
    registration_window = tk.Toplevel(root)
    registration_window.title("Register")
    registration_window.state('zoomed')  # Make the window full-screen

    # Load and set the background image for registration
    try:
        bg_image = Image.open("C:/Users/Mursalin/Downloads/res.jpg")  # Update path as needed

        # Resize the image proportionally to fit within the screen, without scaling down excessively
        bg_image = resize_image(bg_image, registration_window.winfo_screenwidth(), registration_window.winfo_screenheight())
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Make sure the image is not garbage collected by keeping a reference to it
        bg_label = tk.Label(registration_window, image=bg_photo)
        bg_label.place(relwidth=1, relheight=1)  # Make the background cover the entire window
        registration_window.bg_photo = bg_photo  # Keep a reference to the image

    except Exception as e:
        print(f"Error loading background image for registration: {e}")
        messagebox.showerror("Error", "Error loading background image.")
        

    # Create a frame for the registration form to keep it centered
    registration_frame = tk.Frame(registration_window, bg="white", padx=20, pady=20)
    registration_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

    # Registration form fields
    tk.Label(registration_frame, text="Username", bg="white", font=("Arial", 16)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
    username_entry = tk.Entry(registration_frame, font=("Arial", 16))
    username_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    tk.Label(registration_frame, text="Password", bg="white", font=("Arial", 16)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
    password_entry = tk.Entry(registration_frame, show="*", font=("Arial", 16))
    password_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    tk.Label(registration_frame, text="Email", bg="white", font=("Arial", 16)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
    email_entry = tk.Entry(registration_frame, font=("Arial", 16))
    email_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    tk.Label(registration_frame, text="Phone", bg="white", font=("Arial", 16)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
    phone_entry = tk.Entry(registration_frame, font=("Arial", 16))
    phone_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    tk.Label(registration_frame, text="Role (user/admin)", bg="white", font=("Arial", 16)).grid(row=4, column=0, padx=10, pady=5, sticky="e")
    role_var = tk.StringVar(value="user")
    tk.Radiobutton(registration_frame, text="User", variable=role_var, value="user", bg="white", font=("Arial", 14)).grid(row=4, column=1, padx=10, pady=5, sticky="w")
    tk.Radiobutton(registration_frame, text="Admin", variable=role_var, value="admin", bg="white", font=("Arial", 14)).grid(row=5, column=1, padx=10, pady=5, sticky="w")

    # Admin key input box, hidden initially
    admin_key_label = tk.Label(registration_frame, text="Admin Key", bg="white", font=("Arial", 16))
    admin_key_entry = tk.Entry(registration_frame, show="*", font=("Arial", 16))

    def show_admin_key_input():
        """
        Show the admin key input field when the user selects 'admin' role.
        """
        if role_var.get() == "admin":
            admin_key_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")
            admin_key_entry.grid(row=6, column=1, padx=10, pady=5, sticky="w")
        else:
            admin_key_label.grid_forget()
            admin_key_entry.grid_forget()

    role_var.trace("w", lambda *args: show_admin_key_input())

    def register_user():
        """
        Handles the registration process.
        """
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        email = email_entry.get().strip()
        phone = phone_entry.get().strip()
        role = role_var.get()
        admin_key = admin_key_entry.get().strip() if role == "admin" else None

        # Basic input validation
        if not username or not password or not email or not phone:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        # Validation for email, password, and phone
        if not re.match(r".+@(gmail\.com|email\.com|yahoo\.com)$", email):
            messagebox.showerror("Error", "Invalid email. Must end with @gmail.com, @email.com, or @yahoo.com.")
            return
        if len(password) < 6 or not any(char.isalpha() for char in password) or not any(char in "!@#$%^&*()-_+=" for char in password):
            messagebox.showerror("Error", "Password must be at least 6 characters long and contain at least one letter and special character.")
            return
        if not re.match(r"^01[3-9]\d{8}$", phone):
            messagebox.showerror("Error", "Invalid phone number. Must follow the Bangladeshi format.")
            return
        if role == "admin" and admin_key != ADMIN_KEY:
            messagebox.showerror("Error", "Invalid admin key.")
            return

        try:
            # Check if the password already exists
            connection = connect_db()
            if connection is None:
                messagebox.showerror("Error", "Failed to connect to the database.")
                return

            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE password = %s", (password,))
            existing_user = cursor.fetchone()

            if existing_user:
                messagebox.showerror("Error", "This password is already in use. Please choose a different one.")
                return

            # Add the new user to the database if the password is unique
            query = "INSERT INTO users (username, password, email, phone, role) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (username, password, email, phone, role))
            connection.commit()
            messagebox.showinfo("Success", "Registration successful!")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Database error: {err}")
        except Exception as e:
            messagebox.showerror("Error", f"Error during registration: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


    # Register and Back buttons
    tk.Button(registration_frame, text="Register", command=register_user, font=("Arial", 16)).grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")
    tk.Button(registration_frame, text="Back to Login", command=registration_window.destroy, font=("Arial", 16)).grid(row=8, column=0, columnspan=2, pady=5, sticky="ew")


def show_login_screen():
    """
    Displays the login screen for the application.
    """
    root = tk.Tk()
    root.title("Hotel Management System")
    root.state('zoomed')  # Make the window full-screen

    # Load and set the background image for login
    try:
        bg_image = Image.open("C:/Users/Mursalin/Downloads/log1.jpg")  # Update path as needed
       
        # Resize the image proportionally to fit within the screen
        bg_image = resize_image(bg_image, root.winfo_screenwidth(), root.winfo_screenheight())
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Make sure the image is not garbage collected by keeping a reference to it
        bg_label = tk.Label(root, image=bg_photo)
        bg_label.place(relwidth=1, relheight=1)  # Make the background cover the entire window
        root.bg_photo = bg_photo  # Keep a reference to the image

    except Exception as e:
        print(f"Error loading background image for login: {e}")
        messagebox.showerror("Error", "Error loading background image.")
        
    # Title at the top
    title_label = tk.Label(root, text="WELCOME TO HOTEL CALIFORNIA", font=("Arial", 20, "bold"), bg="white", fg="black")
    title_label.place(relx=0.5, rely=0.1, anchor="center")  # Center the title at the top

    # Create a frame for the login form to keep it centered
    login_frame = tk.Frame(root, bg="white", padx=20, pady=20)
    login_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

    # Login form fields
    tk.Label(login_frame, text="Username", bg="white", font=("Arial", 16)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
    username_entry = tk.Entry(login_frame, font=("Arial", 16))
    username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tk.Label(login_frame, text="Password", bg="white", font=("Arial", 16)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
    password_entry = tk.Entry(login_frame, show="*", font=("Arial", 16))
    password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
    

    def login():
        """
        Handles the login process and redirects to the appropriate dashboard.
        """
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        # Basic input validation
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        try:
            user = validate_login(username, password)
            if user:
                user_id = user[0]  # Get the user_id
                role = user[5]  # Access the role from the correct index (assuming it's the 6th column)

                print(f"Logged in as: {user}")  # Debugging line to print the user data

                root.destroy()  # Close the login screen

                if role == "admin":
                    admin_root = tk.Tk()
                    admin_app = AdminApps(admin_root)
                    admin_app.main_menu()  # Start the admin dashboard
                    admin_root.mainloop()
                elif role == "user":
                    show_user_dashboard(user_id)  # Show user dashboard and pass the user_id
                else:
                    messagebox.showerror("Error", "Unknown role. Please contact support.")
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        except Exception as e:
            messagebox.showerror("Error", f"Error during login: {e}")

    # Login and Register buttons
    tk.Button(login_frame, text="Login", command=login, font=("Arial", 16)).grid(row=2, column=0, columnspan=2, pady=20, sticky="ew")
    tk.Button(login_frame, text="Register", command=lambda: show_registration_window(root), font=("Arial", 16)).grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
    tk.Button(login_frame, text="See Our Offerings", command=lambda: show_guest_view(root), font=("Arial", 16)).grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

    root.mainloop()

    root.mainloop()




def show_user_dashboard(user_id):
    """
    Show the user dashboard upon successful login.
    """
    root = tk.Tk()
    user_dashboard = UserApps(root, user_id)  # Initialize the user dashboard with the user_id
    root.mainloop()
    
def show_guest_view(root):
    """
    Displays the guest view interface.
    """
    root.destroy()  # Close the current root window (login screen)
    guest_root = tk.Tk()
    guest_app = GuestApps(guest_root)  # Initialize the guest dashboard without a user_id
    guest_root.mainloop()






if __name__ == "__main__":
    show_login_screen()


