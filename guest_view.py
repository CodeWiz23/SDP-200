import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from db_connection import connect_db


class GuestApps:
 def __init__(self, root):
        self.root = root
        self.root.title("Guest View")

        # Set background image
        self.set_background_image()

        # Initialize main menu
        self.main_menu()

 def set_background_image(self):
        """Sets the background image."""
        try:
            self.bg_image = Image.open("C:/Users/Mursalin/Downloads/ttt.jpg")
            self.bg_image = self.bg_image.resize(
                (self.root.winfo_screenwidth(), self.root.winfo_screenheight()),
                Image.Resampling.LANCZOS
            )
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.bg_label = tk.Label(self.root, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load background image: {e}")

 def clear_window(self):
        """Clears all widgets except the background."""
        for widget in self.root.winfo_children():
            if widget != self.bg_label:
                widget.destroy()

 def main_menu(self):
        """
        Creates the main menu for Guest View.
        """
        self.clear_window()

        # Create a frame for the menu buttons
        menu_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
        menu_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

        # Title
        tk.Label(menu_frame, text="Guest View", font=("Arial", 24, "bold"), bg="white").grid(row=0, column=0, pady=10, columnspan=2)

        # Buttons
        tk.Button(menu_frame, text="View Rooms", width=25, command=self.view_rooms, font=("Arial", 14)).grid(row=1, column=0, pady=10)
        tk.Button(menu_frame, text="View Extra Services", width=25, command=self.view_extra_services, font=("Arial", 14)).grid(row=2, column=0, pady=10)
        tk.Button(menu_frame, text="View Offer Packages", width=25, command=self.view_offer_packages, font=("Arial", 14)).grid(row=3, column=0, pady=10)
        tk.Button(menu_frame, text="View Policy", width=25, command=self.view_policy, font=("Arial", 14)).grid(row=4, column=0, pady=10)
        tk.Button(menu_frame, text="Logout", width=25, command=self.logout, font=("Arial", 14)).grid(row=5, column=0, pady=10)

 def view_rooms(self):
        self.clear_window()

        # Create a frame to center the elements
        menu_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
        menu_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

        # Add the title label
        tk.Label(menu_frame, text="Available Rooms", font=("Arial", 20), bg='white').grid(row=0, column=0, pady=10, padx=10, columnspan=2)

        # Add the listbox for rooms
        self.room_listbox = tk.Listbox(menu_frame, width=60, height=10, font=("Arial", 14))
        self.room_listbox.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

        # Add the "Load Rooms" button
        self.load_rooms_button = tk.Button(menu_frame, text="Load Rooms", font=("Arial", 14), command=self.load_rooms)
        self.load_rooms_button.grid(row=2, column=0, pady=5, padx=5, columnspan=2)

        # Add the "Back to Main Menu" button
        self.back_button = tk.Button(menu_frame, text="Back to Main Menu", font=("Arial", 14), command=self.main_menu)
        self.back_button.grid(row=3, column=0, pady=10, padx=10, columnspan=2)

 def load_rooms(self):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT room_number, room_size, price, availability FROM rooms")
        rooms = cursor.fetchall()
        db.close()

        self.room_listbox.delete(0, tk.END)
        for room in rooms:
            room_details = f"Room {room[0]}: {room[1]} sq ft, {room[2]} USD, {room[3]}"
            self.room_listbox.insert(tk.END, room_details)

 def view_policy(self):
    """Fetch and display the hotel policy."""
    db = connect_db()
    if db is None:
        return  # Exit if the connection fails

    cursor = db.cursor()
    try:
        # Corrected query to fetch the most recent policy based on the 'updated_at' column
        cursor.execute("SELECT policy_description FROM hotel_policy ORDER BY updated_at DESC LIMIT 1")
        policy = cursor.fetchone()

        if policy:
            self.clear_window()

            # Create a frame to center the elements
            menu_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
            menu_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

            # Create a canvas with a scrollbar to make the policy text scrollable
            canvas = tk.Canvas(menu_frame, width=500, height=300)
            canvas.grid(row=1, column=0, pady=10, padx=10, columnspan=2)

            scrollbar = tk.Scrollbar(menu_frame, orient="vertical", command=canvas.yview)
            scrollbar.grid(row=1, column=2, sticky="ns", pady=10, padx=10)

            canvas.config(yscrollcommand=scrollbar.set)

            # Create a frame inside the canvas to hold the policy text
            policy_frame = tk.Frame(canvas, bg="white")
            canvas.create_window((0, 0), window=policy_frame, anchor="nw")

            # Display the title
            tk.Label(menu_frame, text="Hotel Policy", font=("Arial", 20, 'bold'), bg='white').grid(row=0, column=0, pady=10, padx=10, columnspan=2)

            # Display the policy description
            policy_text = policy[0]  # Assuming policy text is the first column in the fetched row
            policy_label = tk.Label(policy_frame, text=policy_text, wraplength=450, justify="left", bg='white', font=("Arial", 14))
            policy_label.grid(row=0, column=0, pady=10, padx=10, columnspan=2)

            # Update the scroll region to the size of the inner frame
            policy_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

            # Add the "Back to Main Menu" button
            self.back_button = tk.Button(menu_frame, text="Back to Main Menu", font=("Arial", 14), command=self.main_menu)
            self.back_button.grid(row=2, column=0, pady=10, padx=10, columnspan=2)
        else:
            messagebox.showerror("Error", "No policy found.")

    except Exception as e:
        print(f"Error fetching policy: {e}")
        messagebox.showerror("Error", "An error occurred while fetching the policy.")

    finally:
        db.close()


 def view_offer_packages(self):
        self.clear_window()

        # Create a frame to center the elements
        menu_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
        menu_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

        # Add the title label
        tk.Label(menu_frame, text="Available Offer Packages", font=("Arial", 20), bg='white').grid(row=0, column=0, pady=10, padx=10, columnspan=2)

        # Add the listbox for packages
        self.package_listbox = tk.Listbox(menu_frame, width=60, height=10, font=("Arial", 14))
        self.package_listbox.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

        # Add the "Load Offer Packages" button
        self.load_offer_packages_button = tk.Button(menu_frame, text="Load Offer Packages", font=("Arial", 14), command=self.load_offer_packages)
        self.load_offer_packages_button.grid(row=2, column=0, pady=5, padx=5, columnspan=2)
    
        # Add the "Back to Main Menu" button
        self.back_button = tk.Button(menu_frame, text="Back to Main Menu", font=("Arial", 14), command=self.main_menu)
        self.back_button.grid(row=3, column=0, pady=10, padx=10, columnspan=2)

 def load_offer_packages(self):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT package_id, package_name, original_price, discount_percentage, discounted_price FROM packages")
        packages = cursor.fetchall()
        db.close()

        self.package_listbox.delete(0, tk.END)
        for package in packages:
            package_details = f"Package {package[0]}: {package[1]}, Original Price: {package[2]} USD, Discount: {package[3]}%, Discounted Price: {package[4]} USD"
            self.package_listbox.insert(tk.END, package_details)

 def view_extra_services(self):
        self.clear_window()

        # Create a frame to center the elements
        menu_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
        menu_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

        # Add the title label
        tk.Label(menu_frame, text="Available Extra Services", font=("Arial", 20), bg='white').grid(row=0, column=0, pady=10, padx=10, columnspan=2)

        # Add the listbox for services
        self.service_listbox = tk.Listbox(menu_frame, width=60, height=10, font=("Arial", 14))
        self.service_listbox.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

        # Add the "Load Extra Services" button
        self.load_services_button = tk.Button(menu_frame, text="Load Extra Services", font=("Arial", 14), command=self.load_extra_services)
        self.load_services_button.grid(row=2, column=0, pady=5, padx=5, columnspan=2)

        # Add the "Back to Main Menu" button
        self.back_button = tk.Button(menu_frame, text="Back to Main Menu", font=("Arial", 14), command=self.main_menu)
        self.back_button.grid(row=3, column=0, pady=10, padx=10, columnspan=2)

 def load_extra_services(self):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT service_id,service_name, description, price FROM extra_services")
        services = cursor.fetchall()
        db.close()

        self.service_listbox.delete(0, tk.END)
        for service in services:
            service_details = f"{service[0]}: {service[1]}, Price: {service[2]} USD"
            self.service_listbox.insert(tk.END, service_details)

 def logout(self):
    """
    Logs out the user with a thank-you message and exits the application completely.
    """
    messagebox.showinfo("Thank You", "Thank you for using our Hotel Management System!")
    self.root.destroy()  
    exit(0) 


