import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from db_connection import connect_db


class AdminApps:
 def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard")
       
        # Set background image
        self.set_background_image()
       
        # Create the main menu after setting the background image
        self.main_menu()


 def set_background_image(self):
        # Load image
        self.bg_image = Image.open("C:/Users/Mursalin/Downloads/PP.jpg")
        self.bg_image = self.bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)


        # Create a label with the image as the background
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)


 def main_menu(self):
    """
    Creates the main menu of the Admin Dashboard, with all buttons aligned in the center.
    """
    self.clear_window()

    # Create a frame for the menu buttons
    menu_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
    menu_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

    # Title
    tk.Label(menu_frame, text="Admin Dashboard", font=("Arial", 24, "bold"), bg="white").grid(row=0, column=0, pady=10, columnspan=2)

    # Buttons
    tk.Button(menu_frame, text="Add Rooms", width=25, command=self.add_room, font=("Arial", 14)).grid(row=1, column=0, pady=10)
    
    tk.Button(menu_frame, text="Update Room", width=25, command=self.update_room, font=("Arial", 14)).grid(row=5, column=0, pady=10)
    
    tk.Button(menu_frame, text="Add Extra Services", width=25, command=self.view_extra_services, font=("Arial", 14)).grid(row=4, column=0, pady=10)
    tk.Button(menu_frame, text="Add Package Room", width=25, command=self.package_room, font=("Arial", 14)).grid(row=3, column=0, pady=10)
    tk.Button(menu_frame, text="Manage Employee", width=25, command=self.view_employees, font=("Arial", 14)).grid(row=6, column=0, pady=10)
    tk.Button(menu_frame, text="Manage Users", width=25, command=self.manage_users, font=("Arial", 14)).grid(row=7, column=0, pady=10)
    tk.Button(menu_frame, text="Update Hotel Policy", width=25, command=self.update_policy, font=("Arial", 14)).grid(row=8, column=0, pady=10)
    tk.Button(menu_frame, text="Logout", width=25, command=self.logout, font=("Arial", 14)).grid(row=9, column=0, pady=10)


 def clear_window(self):
        """Clear all widgets except the background"""
        for widget in self.root.winfo_children():
            if widget != self.bg_label:  # Don't clear the background label
                widget.destroy()


 def add_room(self):
    self.clear_window()

    # Create a frame to hold all widgets and center them
    form_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
    form_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

    # Room Type
    tk.Label(form_frame, text="Room Type", bg='white', font=("Arial", 12)).grid(row=0, column=0, pady=10, padx=10, sticky='e')
    self.room_size_entry = tk.Entry(form_frame, width=40)
    self.room_size_entry.grid(row=0, column=1, pady=10, padx=10)

    # Price
    tk.Label(form_frame, text="Price (in USD/TK)", bg='white', font=("Arial", 12)).grid(row=1, column=0, pady=10, padx=10, sticky='e')
    self.price_entry = tk.Entry(form_frame, width=40)
    self.price_entry.grid(row=1, column=1, pady=10, padx=10)

    # Availability
    tk.Label(form_frame, text="Availability", bg='white', font=("Arial", 12)).grid(row=2, column=0, pady=10, padx=10, sticky='e')
    self.availability_var = tk.StringVar()
    self.availability_combobox = ttk.Combobox(form_frame, textvariable=self.availability_var, 
                                              values=["Available", "Booked"], state="readonly", width=38)
    self.availability_combobox.grid(row=2, column=1, pady=10, padx=10)
    self.availability_combobox.set("Available")  # Default value

    # Offer Price
    tk.Label(form_frame, text="Offer Price (Leave blank if no offer)", bg='white', font=("Arial", 12)).grid(row=3, column=0, pady=10, padx=10, sticky='e')
    self.offer_price_entry = tk.Entry(form_frame, width=40)
    self.offer_price_entry.grid(row=3, column=1, pady=10, padx=10)

    # Submit Button
    self.submit_button = tk.Button(form_frame, text="Add Room", command=self.submit_add_room, font=("Arial", 12))
    self.submit_button.grid(row=4, column=0, columnspan=2, pady=20)

    # Back to Main Menu Button
    self.back_button = tk.Button(form_frame, text="Back to Main Menu", command=self.main_menu, font=("Arial", 12))
    self.back_button.grid(row=5, column=0, columnspan=2, pady=10)



 def submit_add_room(self):
    room_size = self.room_size_entry.get()
    price = self.price_entry.get()
    availability = self.availability_var.get()  # Fixed this line
    offer_price = self.offer_price_entry.get()

    if room_size and price and availability:
        try:
            # Ensure offer_price is a valid number or None
            offer_price = float(offer_price) if offer_price else None

            self.add_or_update_room(room_size, price, availability, offer_price)
            messagebox.showinfo("Success", "Room has been added!")
            self.main_menu()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add room: {str(e)}")
    else:
        messagebox.showerror("Error", "Please fill out all required fields.")

 
 def add_or_update_room(self, room_size, price, availability, offer_price=None):
    db = connect_db()
    cursor = db.cursor()

    try:
        # Make sure offer_price is handled properly
        if offer_price is not None:  # If there is an offer price
            cursor.execute(
                "INSERT INTO rooms (room_size, price, availability, offer_price) VALUES (%s, %s, %s, %s)",
                (room_size, price, availability, offer_price)
            )
        else:  # If there is no offer price, set it as NULL
            cursor.execute(
                "INSERT INTO rooms (room_size, price, availability, offer_price) VALUES (%s, %s, %s, NULL)",
                (room_size, price, availability)
            )
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error inserting room: {e}")  # Debugging line
        raise e
    finally:
        db.close()
 


   
 def update_room(self):
    self.clear_window()

    # Create a frame to center the elements
    menu_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
    menu_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

    # Add the title label with consistent font and styling
    tk.Label(
        menu_frame,
        text="Update Room",
        font=("Arial", 22, "bold"),
        bg="white",
    ).grid(row=0, column=0, pady=15, padx=10, columnspan=2)

    # Add the listbox for rooms with consistent font and size
    self.room_listbox = tk.Listbox(menu_frame, width=90, height=12, font=("Arial", 14))
    self.room_listbox.grid(row=1, column=0, columnspan=2, pady=15, padx=10)

    # Add the "Load Rooms" button with consistent font and padding
    self.load_rooms_button = tk.Button(
        menu_frame,
        text="Load Rooms",
        font=("Arial", 14),
        bg="white",
        command=self.load_rooms_for_update,
    )
    self.load_rooms_button.grid(row=2, column=0, pady=10, padx=10, columnspan=2)

    # Add the "Update Selected Room" button with consistent font and padding
    self.update_button = tk.Button(
        menu_frame,
        text="Update Selected Room",
        font=("Arial", 14),
       bg="white",
        command=self.update_selected_room,
    )
    self.update_button.grid(row=3, column=0, pady=10, padx=10, columnspan=2)

    # Add the "Back to Main Menu" button with consistent font and padding
    self.back_button = tk.Button(
        menu_frame,
        text="Back to Main Menu",
        font=("Arial", 14),
        bg="white",
        command=self.main_menu,
    )
    self.back_button.grid(row=4, column=0, pady=10, padx=10, columnspan=2)




 def load_rooms_for_update(self):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT room_number, room_size, price, availability, offer_price FROM rooms")
        rooms = cursor.fetchall()
        db.close()


        self.room_listbox.delete(0, tk.END)
        for room in rooms:
            room_details = f"Room {room[0]}: {room[1]} sq ft, {room[2]} USD, {room[3]}, Offer Price: {room[4] if room[4] else 'None'}"
            self.room_listbox.insert(tk.END, room_details)


 def update_selected_room(self):
    selected_room = self.room_listbox.get(self.room_listbox.curselection())
    room_number = selected_room.split(":")[0].split()[1]

    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT room_size, price, availability, offer_price FROM rooms WHERE room_number = %s", (room_number,))
    room = cursor.fetchone()
    db.close()

    self.clear_window()

    room_size, price, availability, offer_price = room

    # Create a frame to hold all widgets and center them
    form_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
    form_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

    # Room Type
    tk.Label(form_frame, text="Room Type", bg="white", font=("Arial", 12)).grid(row=0, column=0, pady=5, padx=5, sticky='e')
    self.room_size_entry = tk.Entry(form_frame, width=40)
    self.room_size_entry.insert(0, room_size)
    self.room_size_entry.grid(row=0, column=1, pady=5, padx=5)

    # Price
    tk.Label(form_frame, text="Price (in USD)", bg="white", font=("Arial", 12)).grid(row=1, column=0, pady=5, padx=5, sticky='e')
    self.price_entry = tk.Entry(form_frame, width=40)
    self.price_entry.insert(0, price)
    self.price_entry.grid(row=1, column=1, pady=5, padx=5)

    # Availability
    tk.Label(form_frame, text="Availability (available/booked)", bg="white", font=("Arial", 12)).grid(row=2, column=0, pady=5, padx=5, sticky='e')
    self.availability_entry = tk.Entry(form_frame, width=40)
    self.availability_entry.insert(0, availability)
    self.availability_entry.grid(row=2, column=1, pady=5, padx=5)

    # Offer Price
    tk.Label(form_frame, text="Offer Price (Leave blank if no offer)", bg="white", font=("Arial", 12)).grid(row=3, column=0, pady=5, padx=5, sticky='e')
    self.offer_price_entry = tk.Entry(form_frame, width=40)
    self.offer_price_entry.insert(0, offer_price if offer_price else "")
    self.offer_price_entry.grid(row=3, column=1, pady=5, padx=5)

    # Update Room Button
    self.submit_button = tk.Button(form_frame, text="Update Room", command=lambda: self.submit_update_room(room_number), font=("Arial", 12))
    self.submit_button.grid(row=4, column=1, pady=10)

    # Back Button
    self.back_button = tk.Button(form_frame, text="Back to Manage Rooms", command=self.manage_rooms, font=("Arial", 12))
    self.back_button.grid(row=5, column=1, pady=10)



 def submit_update_room(self, room_number):
        room_size = self.room_size_entry.get()
        price = self.price_entry.get()
        availability = self.availability_entry.get()
        offer_price = self.offer_price_entry.get()


        if room_size and price and availability:
            try:
                self.update_room_in_db(room_number, room_size, price, availability, offer_price)
                messagebox.showinfo("Success", f"Room {room_number} has been updated!")
                self.update_room()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update room: {str(e)}")
        else:
            messagebox.showerror("Error", "Please fill out all required fields.")


 def update_room_in_db(self, room_number, room_size, price, availability, offer_price=None):
        db = connect_db()
        cursor = db.cursor()


        try:
            if offer_price:
                cursor.execute(
                    "UPDATE rooms SET room_size = %s, price = %s, availability = %s, offer_price = %s WHERE room_number = %s",
                    (room_size, price, availability, offer_price, room_number)
                )
            else:
                cursor.execute(
                    "UPDATE rooms SET room_size = %s, price = %s, availability = %s, offer_price = NULL WHERE room_number = %s",
                    (room_size, price, availability, room_number)
                )
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()



 def manage_users(self):
    self.clear_window()

    # Create a centered frame for the form
    form_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
    form_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

    # Title
    tk.Label(form_frame, text="Manage Registered Users", font=("Arial", 16, "bold"), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

    # User List Section
    tk.Label(form_frame, text="Registered Users", bg='white', font=("Arial", 10)).grid(row=1, column=0, columnspan=2, pady=5, sticky="w")
    self.user_listbox = tk.Listbox(form_frame, width=100, height=12, font=("Arial", 10))
    self.user_listbox.grid(row=2, column=0, columnspan=2, pady=10, padx=10)

    # Load Users Button
    self.load_users_button = tk.Button(form_frame, text="Load Users", command=self.load_users, font=("Arial", 10))
    self.load_users_button.grid(row=3, column=0, columnspan=2, pady=5)

    # View User Details Button
    self.view_user_button = tk.Button(form_frame, text="View User Details", command=self.view_user_details, font=("Arial", 10))
    self.view_user_button.grid(row=4, column=0, columnspan=2, pady=5)

    # Delete User Button
    self.delete_user_button = tk.Button(form_frame, text="Delete User", command=self.delete_user, font=("Arial", 10))
    self.delete_user_button.grid(row=5, column=0, columnspan=2, pady=5)

    # Back to Main Menu Button
    self.back_button = tk.Button(form_frame, text="Back to Main Menu", command=self.main_menu, font=("Arial", 10))
    self.back_button.grid(row=6, column=0, columnspan=2, pady=10)



 def load_users(self):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT user_id, username, email, phone, role, created_at FROM users")
    users = cursor.fetchall()
    db.close()

    self.user_listbox.delete(0, tk.END)
    for user in users:
        user_details = f"User {user[0]}: {user[1]}, Email: {user[2]}, Phone: {user[3]}, Role: {user[4]}, Created At: {user[5]}"
        self.user_listbox.insert(tk.END, user_details)

 def view_user_details(self):
    selected_user = self.user_listbox.get(tk.ACTIVE)
    if selected_user:
        user_id = selected_user.split(":")[0].split()[1]
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT user_id, username, password, email, phone, role, created_at FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        db.close()

        if user:
            self.clear_window()
            
            # Create a frame to center the content
            form_frame = tk.Frame(self.root, bg='white', padx=20, pady=20)
            form_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

            # Title
            tk.Label(form_frame, text=f"User {user[0]} Details", font=("Arial", 22), bg='white').grid(row=0, column=0, pady=10, padx=10, columnspan=2)

            # User details
            tk.Label(form_frame, text=f"Username: {user[1]}", bg='white', font=("Arial", 14)).grid(row=1, column=0, pady=5, padx=5, sticky="w")
            tk.Label(form_frame, text=f"Password: {user[2]}", bg='white', font=("Arial", 14)).grid(row=2, column=0, pady=5, padx=5, sticky="w")
            tk.Label(form_frame, text=f"Email: {user[3]}", bg='white', font=("Arial", 14)).grid(row=3, column=0, pady=5, padx=5, sticky="w")
            tk.Label(form_frame, text=f"Phone: {user[4]}", bg='white', font=("Arial", 14)).grid(row=4, column=0, pady=5, padx=5, sticky="w")
            tk.Label(form_frame, text=f"Role: {user[5]}", bg='white', font=("Arial", 14)).grid(row=5, column=0, pady=5, padx=5, sticky="w")
            tk.Label(form_frame, text=f"Created At: {user[6]}", bg='white', font=("Arial", 14)).grid(row=6, column=0, pady=5, padx=5, sticky="w")

            # Back button
            self.back_button = tk.Button(form_frame, text="Back to User Management", command=self.manage_users, font=("Arial", 14))
            self.back_button.grid(row=7, column=0, pady=10, padx=10, columnspan=2)
        else:
            messagebox.showerror("Error", "User not found.")
    else:
        messagebox.showerror("Error", "Please select a user.")


 def delete_user(self):
    selected_user = self.user_listbox.get(tk.ACTIVE)
    if selected_user:
        user_id = selected_user.split(":")[0].split()[1]
        db = connect_db()
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            db.commit()
            messagebox.showinfo("Success", "User deleted successfully.")
            self.load_users()  # Refresh the list
        except Exception as e:
            db.rollback()
            messagebox.showerror("Error", f"Failed to delete user: {str(e)}")
        finally:
            db.close()
    else:
        messagebox.showerror("Error", "Please select a user to delete.")


        self.user_listbox.delete(0, tk.END)
        for user in user:
            user_details = f"User ID: {user[0]}, Username: {user[1]}"
            self.user_listbox.insert(tk.END, user_details)
   
 def update_policy(self):
    self.clear_window()

    # Fetch current policy from the database
    policy = self.get_policy_from_db()

    # Create a frame to center the content and increase its size
    form_frame = tk.Frame(self.root, bg='white', padx=40, pady=40)  # Increased padding
    form_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

    # Title
    tk.Label(form_frame, text="Update Hotel Policy", font=("Arial", 22), bg='white').grid(row=0, column=0, pady=10, padx=10, columnspan=2)

    # Policy Text Area
    tk.Label(form_frame, text="Current Policy:", bg='white', font=("Arial", 14)).grid(row=1, column=0, pady=10, padx=10, sticky='e')
    
    # Make the white text box bigger by increasing width and height
    self.policy_text = tk.Text(form_frame, width=100, height=20, wrap=tk.WORD)  # Increased width and height
    self.policy_text.grid(row=1, column=1, pady=10, padx=10)
    self.policy_text.insert(tk.END, policy)

    # Save and Back Buttons
    self.save_policy_button = tk.Button(form_frame, text="Save Policy", command=self.save_policy_to_db, font=("Arial", 14))
    self.save_policy_button.grid(row=2, column=1, pady=20, padx=10)

    self.back_button = tk.Button(form_frame, text="Back to Main Menu", command=self.main_menu, font=("Arial", 14))
    self.back_button.grid(row=3, column=1, pady=20, padx=10)


 def get_policy_from_db(self):
        """Retrieve the current hotel policy from the database."""
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT policy_description FROM hotel_policy WHERE policy_id = 1")
        policy = cursor.fetchone()
        db.close()

        return policy[0] if policy else "No policy available. Please add one."

 def save_policy_to_db(self):
        """Save the updated policy to the database."""
        new_policy = self.policy_text.get("1.0", tk.END).strip()

        if not new_policy:
            messagebox.showerror("Error", "Policy text cannot be empty.")
            return

        db = connect_db()
        cursor = db.cursor()
        try:
            # Update or insert policy
            cursor.execute(
                "INSERT INTO hotel_policy (policy_id, policy_description) VALUES (1, %s) ON DUPLICATE KEY UPDATE policy_description = %s",
                (new_policy, new_policy)
            )
            db.commit()
            messagebox.showinfo("Success", "Policy updated successfully!")
            self.main_menu()
        except Exception as e:
            db.rollback()
            messagebox.showerror("Error", f"Failed to update policy: {str(e)}")
        finally:
            db.close()

 def clear_window(self):
        """Clear all widgets except the background"""
        for widget in self.root.winfo_children():
            if widget != self.bg_label:  # Don't clear the background label
                widget.destroy()

 def package_room(self):
    self.clear_window()

    # Create a frame for the menu buttons
    menu_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
    menu_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

    tk.Label(menu_frame, text="Manage Packages", font=("Arial", 20), bg='white').grid(row=0, column=0, pady=10, padx=10, columnspan=2)

    # Create a frame for the Listbox
    listbox_frame = tk.Frame(menu_frame, bg="white")
    listbox_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

    # Create the Listbox with adjusted width and height
    self.package_listbox = tk.Listbox(listbox_frame, width=90, height=12, font=("Arial", 14), selectmode=tk.SINGLE)
    self.package_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Load packages and add buttons for each operation
    self.load_packages_button = tk.Button(menu_frame, text="Load Packages", font=("Arial", 14), command=self.load_packages)
    self.load_packages_button.grid(row=2, column=0, pady=5, padx=5)

    self.add_package_button = tk.Button(menu_frame, text="Add Package", font=("Arial", 14), command=self.add_package)
    self.add_package_button.grid(row=2, column=1, pady=5, padx=5)

    self.update_package_button = tk.Button(menu_frame, text="Update Package", font=("Arial", 14), command=self.update_package)
    self.update_package_button.grid(row=3, column=0, pady=5, padx=5)

    self.delete_package_button = tk.Button(menu_frame, text="Delete Package", font=("Arial", 14), command=self.delete_package)
    self.delete_package_button.grid(row=3, column=1, pady=5, padx=5)

    # Back to Main Menu button
    self.back_button = tk.Button(menu_frame, text="Back to Main Menu", font=("Arial", 14), command=self.main_menu)
    self.back_button.grid(row=4, column=0, pady=10, padx=10, columnspan=2)




 def load_packages(self):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT package_id, package_name, original_price, discount_percentage, discounted_price FROM packages")
    packages = cursor.fetchall()
    db.close()

    self.package_listbox.delete(0, tk.END)
    for package in packages:
        package_details = f"Package {package[0]}: {package[1]}, Original Price: {package[2]} USD, Discount: {package[3]}%, Discounted Price: {package[4]} USD"
        self.package_listbox.insert(tk.END, package_details)

 def add_package(self):
    # Create a new window to add a package
    self.package_window = tk.Toplevel(self.root)
    self.package_window.title("Add Package")

    tk.Label(self.package_window, text="Package Name:").grid(row=0, column=0, padx=10, pady=5)
    self.package_name_entry = tk.Entry(self.package_window)
    self.package_name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(self.package_window, text="Original Price (USD):").grid(row=1, column=0, padx=10, pady=5)
    self.original_price_entry = tk.Entry(self.package_window)
    self.original_price_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(self.package_window, text="Discount Percentage:").grid(row=2, column=0, padx=10, pady=5)
    self.discount_percentage_entry = tk.Entry(self.package_window)
    self.discount_percentage_entry.grid(row=2, column=1, padx=10, pady=5)

    self.submit_button = tk.Button(self.package_window, text="Add Package", command=self.submit_add_package)
    self.submit_button.grid(row=3, column=0, columnspan=2, pady=10, padx=10)

 def submit_add_package(self):
    package_name = self.package_name_entry.get()
    original_price = self.original_price_entry.get()
    discount_percentage = self.discount_percentage_entry.get()

    if package_name and original_price and discount_percentage:
        try:
            original_price = float(original_price)
            discount_percentage = float(discount_percentage)

            # Calculate the discounted price
            discounted_price = original_price - (original_price * discount_percentage / 100)

            self.add_package_to_db(package_name, original_price, discount_percentage, discounted_price)
            messagebox.showinfo("Success", "Package has been added!")
            self.package_window.destroy()
            self.manage_packages()  # Reload the packages list
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numerical values for original price and discount percentage.")
    else:
        messagebox.showerror("Error", "Please fill out all required fields.")

 def add_package_to_db(self, package_name, original_price, discount_percentage, discounted_price):
    db = connect_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO packages (package_name, original_price, discount_percentage, discounted_price) VALUES (%s, %s, %s, %s)",
            (package_name, original_price, discount_percentage, discounted_price)
        )
        db.commit()
    except Exception as e:
        db.rollback()
        messagebox.showerror("Error", f"Failed to add package: {str(e)}")
    finally:
        db.close()

 def update_package(self):
    selected_package = self.package_listbox.curselection()
    if selected_package:
        package_details = self.package_listbox.get(selected_package)
        package_id = package_details.split(":")[0].split()[1]  # Extract package_id from the string
        
        # Create a new window to update the package
        self.package_window = tk.Toplevel(self.root)
        self.package_window.title(f"Update Package {package_id}")
        
        # Fetch package data from the database
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT package_name, original_price, discount_percentage FROM packages WHERE package_id = %s", (package_id,))
        package = cursor.fetchone()
        db.close()

        # Populate fields with current data
        tk.Label(self.package_window, text="Package Name:").grid(row=0, column=0, padx=10, pady=5)
        self.package_name_entry = tk.Entry(self.package_window)
        self.package_name_entry.insert(0, package[0])
        self.package_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.package_window, text="Original Price (USD):").grid(row=1, column=0, padx=10, pady=5)
        self.original_price_entry = tk.Entry(self.package_window)
        self.original_price_entry.insert(0, package[1])
        self.original_price_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.package_window, text="Discount Percentage:").grid(row=2, column=0, padx=10, pady=5)
        self.discount_percentage_entry = tk.Entry(self.package_window)
        self.discount_percentage_entry.insert(0, package[2])
        self.discount_percentage_entry.grid(row=2, column=1, padx=10, pady=5)

        self.submit_button = tk.Button(self.package_window, text="Update Package", command=lambda: self.submit_update_package(package_id))
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=10, padx=10)
    else:
        messagebox.showwarning("No Selection", "Please select a package to update.")




 def submit_update_package(self, package_id):
    package_name = self.package_name_entry.get()
    original_price = self.original_price_entry.get()
    discount_percentage = self.discount_percentage_entry.get()

    if package_name and original_price and discount_percentage:
        try:
            original_price = float(original_price)
            discount_percentage = float(discount_percentage)

            # Calculate the discounted price
            discounted_price = original_price - (original_price * discount_percentage / 100)

            self.update_package_in_db(package_id, package_name, original_price, discount_percentage, discounted_price)
            messagebox.showinfo("Success", "Package has been updated!")
            self.package_window.destroy()
            self.manage_packages()  # Reload the packages list
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numerical values for original price and discount percentage.")
    else:
        messagebox.showerror("Error", "Please fill out all required fields.")

 def update_package_in_db(self, package_id, package_name, original_price, discount_percentage, discounted_price):
    db = connect_db()
    cursor = db.cursor()

    try:
        cursor.execute("""
            UPDATE packages
            SET package_name = %s, original_price = %s, discount_percentage = %s, discounted_price = %s
            WHERE package_id = %s
        """, (package_name, original_price, discount_percentage, discounted_price, package_id))
        db.commit()
    except Exception as e:
        db.rollback()
        messagebox.showerror("Error", f"Failed to update package: {str(e)}")
    finally:
        db.close()

 def delete_package(self):
    selected_package = self.package_listbox.curselection()
    if selected_package:
        package_details = self.package_listbox.get(selected_package)
        package_id = package_details.split(":")[0].split()[1]  # Extract package_id
        
        # Confirmation dialog
        confirm = messagebox.askyesno("Delete Package", f"Are you sure you want to delete package {package_id}?")
        if confirm:
            self.delete_package_from_db(package_id)
            messagebox.showinfo("Success", "Package has been deleted!")
            self.manage_packages()  # Reload the packages list
    else:
        messagebox.showwarning("No Selection", "Please select a package to delete.")

 def delete_package_from_db(self, package_id):
    db = connect_db()
    cursor = db.cursor()

    try:
        cursor.execute("DELETE FROM packages WHERE package_id = %s", (package_id,))
        db.commit()
    except Exception as e:
        db.rollback()
        messagebox.showerror("Error", f"Failed to delete package: {str(e)}")
    finally:
        db.close()


 def view_employees(self):
    self.clear_window()

    # Create a frame for the menu buttons
    menu_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
    menu_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

    tk.Label(menu_frame, text="Employee Management", font=("Arial", 18), bg='white').grid(row=0, column=0, pady=10, padx=10, columnspan=2)

    self.employee_listbox = tk.Listbox(menu_frame, width=100, height=15, font=("Arial", 12))  # Adjusted size and font
    self.employee_listbox.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

    self.load_employees_button = tk.Button(menu_frame, text="Load Employees", command=self.load_employees, font=("Arial", 12))
    self.load_employees_button.grid(row=2, column=0, pady=5, padx=5)

    self.add_employee_button = tk.Button(menu_frame, text="Add Employee", command=self.add_employee, font=("Arial", 12))
    self.add_employee_button.grid(row=2, column=1, pady=5, padx=5)

    self.update_employee_button = tk.Button(menu_frame, text="Update Employee", command=self.update_employee, font=("Arial", 12))
    self.update_employee_button.grid(row=3, column=0, pady=5, padx=5)

    self.delete_employee_button = tk.Button(menu_frame, text="Delete Employee", command=self.delete_employee, font=("Arial", 12))
    self.delete_employee_button.grid(row=3, column=1, pady=5, padx=5)

    self.back_button = tk.Button(menu_frame, text="Back to Main Menu", command=self.main_menu, font=("Arial", 12))
    self.back_button.grid(row=4, column=0, pady=10, padx=10, columnspan=2)

    # Method for loading employees into the listbox
 def load_employees(self):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT employee_id, name, role, email, phone, salary FROM employees")
        employees = cursor.fetchall()
        db.close()

        self.employee_listbox.delete(0, tk.END)
        for employee in employees:
            employee_details = f"ID: {employee[0]}, Name: {employee[1]}, Role: {employee[2]}, Email: {employee[3]}, Phone: {employee[4]}, Salary: {employee[5]} USD"
            self.employee_listbox.insert(tk.END, employee_details)

    # Method to add a new employee
 def add_employee(self):
        # Create a new window to add employee details
        add_employee_window = tk.Toplevel(self.root)
        add_employee_window.title("Add New Employee")
        
        tk.Label(add_employee_window, text="Name").grid(row=0, column=0, pady=5, padx=5)
        name_entry = tk.Entry(add_employee_window)
        name_entry.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(add_employee_window, text="Role").grid(row=1, column=0, pady=5, padx=5)
        role_entry = tk.Entry(add_employee_window)
        role_entry.grid(row=1, column=1, pady=5, padx=5)
        
        tk.Label(add_employee_window, text="Email").grid(row=2, column=0, pady=5, padx=5)
        email_entry = tk.Entry(add_employee_window)
        email_entry.grid(row=2, column=1, pady=5, padx=5)
        
        tk.Label(add_employee_window, text="Phone").grid(row=3, column=0, pady=5, padx=5)
        phone_entry = tk.Entry(add_employee_window)
        phone_entry.grid(row=3, column=1, pady=5, padx=5)
        
        tk.Label(add_employee_window, text="Salary").grid(row=4, column=0, pady=5, padx=5)
        salary_entry = tk.Entry(add_employee_window)
        salary_entry.grid(row=4, column=1, pady=5, padx=5)

        def submit_employee():
            name = name_entry.get()
            role = role_entry.get()
            email = email_entry.get()
            phone = phone_entry.get()
            salary = salary_entry.get()

            db = connect_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO employees (name, role, email, phone, salary) VALUES (%s, %s, %s, %s, %s)", 
                           (name, role, email, phone, salary))
            db.commit()
            db.close()
            
            add_employee_window.destroy()
            self.load_employees()

        submit_button = tk.Button(add_employee_window, text="Submit", command=submit_employee)
        submit_button.grid(row=5, column=0, columnspan=2, pady=10, padx=10)

    # Method to update an employee
 def update_employee(self):
        selected_employee = self.employee_listbox.get(tk.ACTIVE)
        if selected_employee:
            employee_id = selected_employee.split(",")[0].split(":")[1].strip()

            update_employee_window = tk.Toplevel(self.root)
            update_employee_window.title("Update Employee")

            # Populate the fields for updating
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM employees WHERE employee_id = %s", (employee_id,))
            employee = cursor.fetchone()
            db.close()

            tk.Label(update_employee_window, text="Name").grid(row=0, column=0, pady=5, padx=5)
            name_entry = tk.Entry(update_employee_window)
            name_entry.insert(0, employee[1])
            name_entry.grid(row=0, column=1, pady=5, padx=5)

            tk.Label(update_employee_window, text="Role").grid(row=1, column=0, pady=5, padx=5)
            role_entry = tk.Entry(update_employee_window)
            role_entry.insert(0, employee[2])
            role_entry.grid(row=1, column=1, pady=5, padx=5)

            tk.Label(update_employee_window, text="Email").grid(row=2, column=0, pady=5, padx=5)
            email_entry = tk.Entry(update_employee_window)
            email_entry.insert(0, employee[3])
            email_entry.grid(row=2, column=1, pady=5, padx=5)

            tk.Label(update_employee_window, text="Phone").grid(row=3, column=0, pady=5, padx=5)
            phone_entry = tk.Entry(update_employee_window)
            phone_entry.insert(0, employee[4])
            phone_entry.grid(row=3, column=1, pady=5, padx=5)

            tk.Label(update_employee_window, text="Salary").grid(row=4, column=0, pady=5, padx=5)
            salary_entry = tk.Entry(update_employee_window)
            salary_entry.insert(0, employee[5])
            salary_entry.grid(row=4, column=1, pady=5, padx=5)

            def submit_update():
                name = name_entry.get()
                role = role_entry.get()
                email = email_entry.get()
                phone = phone_entry.get()
                salary = salary_entry.get()

                db = connect_db()
                cursor = db.cursor()
                cursor.execute("UPDATE employees SET name = %s, role = %s, email = %s, phone = %s, salary = %s WHERE employee_id = %s", 
                               (name, role, email, phone, salary, employee_id))
                db.commit()
                db.close()

                update_employee_window.destroy()
                self.load_employees()

            submit_button = tk.Button(update_employee_window, text="Update", command=submit_update)
            submit_button.grid(row=5, column=0, columnspan=2, pady=10, padx=10)

        else:
            messagebox.showerror("Error", "Please select an employee to update.")

    # Method to delete an employee
 def delete_employee(self):
        selected_employee = self.employee_listbox.get(tk.ACTIVE)
        if selected_employee:
            employee_id = selected_employee.split(",")[0].split(":")[1].strip()
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM employees WHERE employee_id = %s", (employee_id,))
            db.commit()
            db.close()
            self.load_employees()
        else:
            messagebox.showerror("Error", "Please select an employee to delete.")
 def view_extra_services(self):
    self.clear_window()

    # Create a frame for the menu buttons
    menu_frame = tk.Frame(self.root, bg="white", padx=100, pady=20)
    menu_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

    # Add the title label with consistent font and styling
    tk.Label(
        menu_frame,
        text="Extra Services Management",
        font=("Arial", 22, "bold"),
        bg='white'
    ).grid(row=0, column=0, pady=10, padx=10, columnspan=2)

    # Create the listbox for extra services with consistent font and size
    self.services_listbox = tk.Listbox(menu_frame, width=100, height=15, font=("Arial", 14))
    self.services_listbox.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

    # Add the "Load Extra Services" button with consistent font and padding
    self.load_services_button = tk.Button(
        menu_frame,
        text="Load Extra Services",
        font=("Arial", 14),
        command=self.load_extra_services
    )
    self.load_services_button.grid(row=2, column=0, pady=5, padx=5)

    # Add the "Add New Service" button with consistent font and padding
    self.add_service_button = tk.Button(
        menu_frame,
        text="Add New Service",
        font=("Arial", 14),
        command=self.add_service
    )
    self.add_service_button.grid(row=2, column=1, pady=5, padx=5)

    # Add the "Update Service" button with consistent font and padding
    self.update_service_button = tk.Button(
        menu_frame,
        text="Update Service",
        font=("Arial", 14),
        command=self.update_service
    )
    self.update_service_button.grid(row=3, column=0, pady=5, padx=5)

    # Add the "Delete Service" button with consistent font and padding
    self.delete_service_button = tk.Button(
        menu_frame,
        text="Delete Service",
        font=("Arial", 14),
        command=self.delete_service
    )
    self.delete_service_button.grid(row=3, column=1, pady=5, padx=5)

    # Add the "Back to Main Menu" button with consistent font and padding
    self.back_button = tk.Button(
        menu_frame,
        text="Back to Main Menu",
        font=("Arial", 14),
        command=self.main_menu
    )
    self.back_button.grid(row=4, column=0, pady=10, padx=10, columnspan=2)

 def load_extra_services(self):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT service_id, service_name, description, price FROM extra_services")
    services = cursor.fetchall()
    db.close()

    # Clear listbox before adding items
    self.services_listbox.delete(0, tk.END)
    for service in services:
        service_details = f"Service {service[0]}: {service[1]}, Description: {service[2]}, Price: {service[3]} USD"
        self.services_listbox.insert(tk.END, service_details)

 def add_service(self):
    # Create a new window to add a service
    self.add_service_window = tk.Toplevel(self.root)
    self.add_service_window.title("Add Extra Service")
    self.add_service_window.configure(bg="white")

    # Title
    tk.Label(
        self.add_service_window,
        text="Add Extra Service",
        font=("Arial", 18),
        bg="white",
    ).grid(row=0, column=0, columnspan=2, pady=10)

    # Create fields for service name, description, and price
    tk.Label(
        self.add_service_window,
        text="Service Name:",
        font=("Arial", 12),
        bg="white",
    ).grid(row=1, column=0, padx=10, pady=5, sticky="e")
    self.service_name_entry = tk.Entry(self.add_service_window, font=("Arial", 12), width=30)
    self.service_name_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(
        self.add_service_window,
        text="Description:",
        font=("Arial", 12),
        bg="white",
    ).grid(row=2, column=0, padx=10, pady=5, sticky="e")
    self.description_entry = tk.Entry(self.add_service_window, font=("Arial", 12), width=30)
    self.description_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(
        self.add_service_window,
        text="Price:",
        font=("Arial", 12),
        bg="white",
    ).grid(row=3, column=0, padx=10, pady=5, sticky="e")
    self.price_entry = tk.Entry(self.add_service_window, font=("Arial", 12), width=30)
    self.price_entry.grid(row=3, column=1, padx=10, pady=5)

    # Button to submit the new service
    self.submit_button = tk.Button(
        self.add_service_window,
        text="Add Service",
        command=self.submit_new_service,
        font=("Arial", 12),
        bg="white",
        padx=10,
        pady=5,
    )
    self.submit_button.grid(row=4, column=0, columnspan=2, pady=10)

    # Configure grid weights for better layout
    self.add_service_window.grid_columnconfigure(0, weight=1)
    self.add_service_window.grid_columnconfigure(1, weight=1)


 def submit_new_service(self):
    # Get the input values from the entry fields
    service_name = self.service_name_entry.get()
    description = self.description_entry.get()
    price = self.price_entry.get()

    # Validate inputs
    if service_name and description and price:
        db = connect_db()
        cursor = db.cursor()

        try:
            cursor.execute("INSERT INTO extra_services (service_name, description, price) VALUES (%s, %s, %s)",
                           (service_name, description, float(price)))
            db.commit()
            messagebox.showinfo("Success", "New service added successfully.")
            self.add_service_window.destroy()
            self.load_extra_services()  # Reload the services list
        except Exception as e:
            db.rollback()
            messagebox.showerror("Error", f"Failed to add service: {str(e)}")
        finally:
            db.close()
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

 def update_service(self):
    # Get the selected service ID from the listbox
    selected_service = self.services_listbox.curselection()
    if selected_service:
        service_details = self.services_listbox.get(selected_service)
        service_id = service_details.split(':')[0].split(' ')[1]  # Extract service_id from the string

        # Create a new window to update the service
        self.update_service_window = tk.Toplevel(self.root)
        self.update_service_window.title(f"Update Service {service_id}")

        # Get current service details from the database
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT service_name, description, price FROM extra_services WHERE service_id = %s", (service_id,))
        service = cursor.fetchone()
        db.close()

        # Populate the fields with current data
        tk.Label(self.update_service_window, text="Service Name:").grid(row=0, column=0, padx=10, pady=5)
        self.update_service_name_entry = tk.Entry(self.update_service_window)
        self.update_service_name_entry.insert(0, service[0])
        self.update_service_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.update_service_window, text="Description:").grid(row=1, column=0, padx=10, pady=5)
        self.update_description_entry = tk.Entry(self.update_service_window)
        self.update_description_entry.insert(0, service[1])
        self.update_description_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.update_service_window, text="Price:").grid(row=2, column=0, padx=10, pady=5)
        self.update_price_entry = tk.Entry(self.update_service_window)
        self.update_price_entry.insert(0, service[2])
        self.update_price_entry.grid(row=2, column=1, padx=10, pady=5)

        # Button to submit the updated service
        self.submit_update_button = tk.Button(self.update_service_window, text="Update Service", command=lambda: self.submit_update_service(service_id))
        self.submit_update_button.grid(row=3, column=0, columnspan=2, pady=10, padx=10)

 def submit_update_service(self, service_id):
    # Get the updated input values from the entry fields
    service_name = self.update_service_name_entry.get()
    description = self.update_description_entry.get()
    price = self.update_price_entry.get()

    # Validate inputs
    if service_name and description and price:
        db = connect_db()
        cursor = db.cursor()

        try:
            cursor.execute("""
                UPDATE extra_services
                SET service_name = %s, description = %s, price = %s
                WHERE service_id = %s
            """, (service_name, description, float(price), service_id))
            db.commit()
            messagebox.showinfo("Success", "Service updated successfully.")
            self.update_service_window.destroy()
            self.load_extra_services()  # Reload the services list
        except Exception as e:
            db.rollback()
            messagebox.showerror("Error", f"Failed to update service: {str(e)}")
        finally:
            db.close()
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

 def delete_service(self):
    # Get the selected service ID from the listbox
    selected_service = self.services_listbox.curselection()
    if selected_service:
        service_details = self.services_listbox.get(selected_service)
        service_id = service_details.split(':')[0].split(' ')[1]  # Extract service_id from the string

        # Ask for confirmation before deleting
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete Service {service_id}?")
        if confirm:
            db = connect_db()
            cursor = db.cursor()

            try:
                cursor.execute("DELETE FROM extra_services WHERE service_id = %s", (service_id,))
                db.commit()
                messagebox.showinfo("Success", "Service deleted successfully.")
                self.load_extra_services()  # Reload the services list
            except Exception as e:
                db.rollback()
                messagebox.showerror("Error", f"Failed to delete service: {str(e)}")
            finally:
                db.close()


 def logout(self):
    """
    Logs out the user with a thank-you message and exits the application completely.
    """
    messagebox.showinfo("Thank You", "Thank you for using our Hotel Management System!")
    self.root.destroy()  
    exit(0) 

  
