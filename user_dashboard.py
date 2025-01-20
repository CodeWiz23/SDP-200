import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from db_connection import connect_db

class UserApps:
 def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("User Dashboard")

        # Set background image
        self.set_background_image()

        # Initialize main menu
        self.main_menu()

 def set_background_image(self):
        """Sets the background image."""
        try:
            self.bg_image = Image.open("C:/Users/Mursalin/Downloads/t.jpg")
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
    Creates the main menu of the User's Zone, with all buttons aligned in the center.
    """
    self.clear_window()

    # Create a frame for the menu buttons
    menu_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
    menu_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

    # Title
    tk.Label(menu_frame, text="USER'S ZONE", font=("Arial", 24, "bold"), bg="white").grid(row=0, column=0, pady=10, columnspan=2)

    # Buttons
    tk.Button(menu_frame, text="View Rooms", width=25, command=self.view_rooms, font=("Arial", 14)).grid(row=1, column=0, pady=10)
    tk.Button(menu_frame, text="Book Room", width=25, command=self.book_room, font=("Arial", 14)).grid(row=2, column=0, pady=10)
    tk.Button(menu_frame, text="View Extra Services", width=25, command=self.view_extra_services, font=("Arial", 14)).grid(row=3, column=0, pady=10)
    tk.Button(menu_frame, text="View Offer Packages", width=25, command=self.view_offer_packages, font=("Arial", 14)).grid(row=4, column=0, pady=10)
    tk.Button(menu_frame, text="View Booking History", width=25, command=self.view_booking_history, font=("Arial", 14)).grid(row=5, column=0, pady=10)
    tk.Button(menu_frame, text="View Policy", width=25, command=self.view_policy, font=("Arial", 14)).grid(row=6, column=0, pady=10)
    tk.Button(menu_frame, text="Logout", width=25, command=self.logout, font=("Arial", 14)).grid(row=7, column=0, pady=10)



 

 def view_rooms(self):
    self.clear_window()

    # Create a frame to center the elements
    menu_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
    menu_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

    # Add the title label
    tk.Label(menu_frame, text="Available Rooms", font=("Arial", 20), bg='white').grid(row=0, column=0, pady=10, padx=10, columnspan=2)

    # Add the listbox for rooms
    self.room_listbox = tk.Listbox(menu_frame, width=80, height=10, font=("Arial", 14))
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
        cursor.execute("SELECT room_number, room_size, price, offer_price, availability FROM rooms")
        rooms = cursor.fetchall()
        db.close()


        self.room_listbox.delete(0, tk.END)
        for room in rooms:
            room_details = f"Room {room[0]}: {room[1]} ,Room Price : {room[2]} USD, Offer Price : {room[3]} USD, {room[4]}"
            self.room_listbox.insert(tk.END, room_details)

 def book_room(self):
    self.clear_window()

    # Create a frame to center the elements
    menu_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
    menu_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

    # Add the title label
    tk.Label(menu_frame, text="Book Room", font=("Arial", 20), bg='white').grid(row=0, column=0, pady=10, padx=10, columnspan=2)

    # Add the listbox for rooms
    self.room_listbox = tk.Listbox(menu_frame, width=80, height=10, font=("Arial", 14))
    self.room_listbox.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

    # Add the "Load Rooms" button
    self.load_rooms_button = tk.Button(menu_frame, text="Load Rooms", font=("Arial", 14), command=self.load_rooms_for_booking)
    self.load_rooms_button.grid(row=2, column=0, pady=5, padx=5, columnspan=2)

    # Add the payment method label
    self.payment_method_label = tk.Label(menu_frame, text="Select Payment Method", font=("Arial", 14), bg='white')
    self.payment_method_label.grid(row=3, column=0, pady=10, padx=10, columnspan=2)

    # Add the payment method dropdown menu
    self.payment_method_var = tk.StringVar()
    self.payment_method_menu = tk.OptionMenu(menu_frame, self.payment_method_var, "Credit Card",  "Cash")
    self.payment_method_menu.config(font=("Arial", 14))
    self.payment_method_menu.grid(row=4, column=0, pady=10, padx=10, columnspan=2)

    # Add the "Book Room" button
    self.book_button = tk.Button(menu_frame, text="Book Room", font=("Arial", 14), command=self.submit_booking)
    self.book_button.grid(row=5, column=0, pady=5, padx=5, columnspan=2)

    # Add the "Back to Main Menu" button
    self.back_button = tk.Button(menu_frame, text="Back to Main Menu", font=("Arial", 14), command=self.main_menu)
    self.back_button.grid(row=6, column=0, pady=10, padx=10, columnspan=2)



 def load_rooms_for_booking(self):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT room_number, room_size, price, availability FROM rooms WHERE availability = 'available'")
        rooms = cursor.fetchall()
        db.close()


        self.room_listbox.delete(0, tk.END)
        for room in rooms:
            room_details = f"Room {room[0]}: {room[1]} , {room[2]} USD, {room[3]}"
            self.room_listbox.insert(tk.END, room_details)


 def submit_booking(self):
    selected_room = self.room_listbox.get(tk.ACTIVE)
    if selected_room:
        room_number = selected_room.split(":")[0].split()[1]
        payment_method = self.payment_method_var.get()

        if not payment_method:
            messagebox.showerror("Error", "Please select a payment method.")
            return

        # Ask user if they want to pay in Taka
        convert_to_taka = messagebox.askyesno(
            "Currency Conversion",
            f"Do you want to pay for Room {room_number} in Taka?"
        )

        if convert_to_taka:
            conversion_rate = 100  # Example rate; replace with real-time rate if needed
            amount_in_taka = 200  # Example price; replace with actual room price
            messagebox.showinfo("Amount in Taka", f"The total amount is {amount_in_taka:.2f} Taka.")
            currency = "TK"
            amount_to_pay = amount_in_taka
        else:
            currency = "USD"
            amount_to_pay = 200  # Example price; replace with actual room price

        # Confirm booking
        confirm = messagebox.askyesno(
            "Confirm Booking",
            f"Do you want to book Room {room_number} for {amount_to_pay:.2f} {currency} using {payment_method}?"
        )
        if confirm:
            try:
                self.book_room_in_db(room_number, payment_method, amount_to_pay, currency)
                messagebox.showinfo("Success", f"Room {room_number} booked successfully!")
                self.main_menu()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to book room: {e}")
    else:
        messagebox.showerror("Error", "Please select a room.")

 def book_room_in_db(self, room_number, payment_method, amount, currency):
    db = connect_db()
    cursor = db.cursor()

    try:
        cursor.execute("UPDATE rooms SET availability = 'booked' WHERE room_number = %s", (room_number,))
        cursor.execute("""
            INSERT INTO bookings (user_id, room_number, payment_method, amount, currency, status) 
            VALUES (%s, %s, %s, %s, %s, 'Confirmed')
        """, (self.user_id, room_number, payment_method, amount, currency))
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


 def show_payment_window(self, room_number):
        """Displays a payment window after booking."""
        for widget in self.root.winfo_children():
            widget.destroy()


        tk.Label(self.root, text=f"Payment for Room {room_number}", font=("Arial", 14)).pack(pady=20)


        payment_method_label = tk.Label(self.root, text="Select Payment Method:", font=("Arial", 12))
        payment_method_label.pack(pady=5)


        payment_methods = ["Credit Card", "Debit Card", "PayPal", "Cash"]
        self.payment_method_var = tk.StringVar()
        self.payment_method_var.set(payment_methods[0])  # Default option


        payment_menu = tk.OptionMenu(self.root, self.payment_method_var, *payment_methods)
        payment_menu.pack(pady=5)


        def process_payment():
            """Processes the payment."""
            selected_payment = self.payment_method_var.get()
            messagebox.showinfo("Payment Successful", f"Payment via {selected_payment} completed successfully!")
            self.main_menu()


        tk.Button(self.root, text="Confirm Payment", command=process_payment).pack(pady=5)
        tk.Button(self.root, text="Back to Main Menu", command=self.main_menu).pack(pady=5)


 

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

    # Add the listbox for offer packages
    self.package_listbox = tk.Listbox(menu_frame, width=100, height=10, font=("Arial", 14))
    self.package_listbox.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

    # Add the "Load Offer Packages" button
    self.load_offer_packages_button = tk.Button(menu_frame, text="Load Offer Packages", font=("Arial", 14), command=self.load_offer_packages)
    self.load_offer_packages_button.grid(row=2, column=0, pady=5, padx=5, columnspan=2)

    # Add the payment method label
    self.payment_method_label = tk.Label(menu_frame, text="Select Payment Method", bg='white', font=("Arial", 14))
    self.payment_method_label.grid(row=3, column=0, pady=10, padx=10, columnspan=2)

    # Add the payment method dropdown menu
    self.payment_method_var = tk.StringVar()
    self.payment_method_menu = tk.OptionMenu(menu_frame, self.payment_method_var, "Credit Card", "Cash")
    self.payment_method_menu.config(font=("Arial", 14))
    self.payment_method_menu.grid(row=4, column=0, pady=10, padx=10, columnspan=2)

    # Add the "Book Offer Package" button
    self.book_package_button = tk.Button(menu_frame, text="Book Offer Package", font=("Arial", 14), command=self.book_offer_package)
    self.book_package_button.grid(row=5, column=0, pady=5, padx=5, columnspan=2)

    # Add the "Back to Main Menu" button
    self.back_button = tk.Button(menu_frame, text="Back to Main Menu", font=("Arial", 14), command=self.main_menu)
    self.back_button.grid(row=6, column=0, pady=10, padx=10, columnspan=2)


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


 def book_offer_package(self):
    selected_package = self.package_listbox.get(tk.ACTIVE)
    if selected_package:
        package_id = selected_package.split(":")[0].split()[1]
        discounted_price = float(selected_package.split("Discounted Price: ")[1].split()[0])  # Extract price
        payment_method = self.payment_method_var.get()

        if not payment_method:
            messagebox.showerror("Error", "Please select a payment method.")
            return

        confirm_currency = messagebox.askyesno("Currency Conversion", "Would you like to pay in Taka?")
        if confirm_currency:
            discounted_price *= 110  # Assuming 1 USD = 110 Taka
            currency = "TK"
        else:
            currency = "USD"

        confirm = messagebox.askyesno(
            "Confirm Booking",
            f"Do you want to book Offer Package {package_id} for {discounted_price:.2f} {currency} using {payment_method}?"
        )

        if confirm:
            try:
                self.book_offer_package_in_db(package_id, payment_method, discounted_price, currency)
                messagebox.showinfo("Success", f"Offer Package {package_id} booked successfully!")
                self.main_menu()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to book offer package: {e}")
    else:
        messagebox.showerror("Error", "Please select a package.")


 def book_offer_package_in_db(self, package_id, payment_method, amount, currency):
    db = connect_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO package_bookings (user_id, package_id, payment_method, amount, currency, status) 
            VALUES (%s, %s, %s, %s, %s, 'Confirmed')
            """,
            (self.user_id, package_id, payment_method, amount, currency)
        )
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

        
        
        
        
        
 def view_extra_services(self):
    self.clear_window()

    # Create a frame to center the elements
    menu_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
    menu_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

    # Add the title label
    tk.Label(menu_frame, text="Available Extra Services", font=("Arial", 20), bg='white').grid(row=0, column=0, pady=10, padx=10, columnspan=2)

    # Add the listbox for extra services
    self.service_listbox = tk.Listbox(menu_frame, width=60, height=10, font=("Arial", 14))
    self.service_listbox.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

    # Add the "Load Extra Services" button
    self.load_services_button = tk.Button(menu_frame, text="Load Extra Services", font=("Arial", 14), command=self.load_extra_services)
    self.load_services_button.grid(row=2, column=0, pady=5, padx=5, columnspan=2)

    # Add the payment method label
    self.payment_method_label = tk.Label(menu_frame, text="Select Payment Method", bg='white', font=("Arial", 14))
    self.payment_method_label.grid(row=3, column=0, pady=10, padx=10, columnspan=2)

    # Add the payment method dropdown menu
    self.payment_method_var = tk.StringVar()
    self.payment_method_menu = tk.OptionMenu(menu_frame, self.payment_method_var, "Credit Card", "Cash")
    self.payment_method_menu.config(font=("Arial", 14))
    self.payment_method_menu.grid(row=4, column=0, pady=10, padx=10, columnspan=2)

    # Add the "Book Extra Service" button
    self.book_service_button = tk.Button(menu_frame, text="Book Extra Service", font=("Arial", 14), command=self.book_extra_service)
    self.book_service_button.grid(row=5, column=0, pady=5, padx=5, columnspan=2)

    # Add the "Back to Main Menu" button
    self.back_button = tk.Button(menu_frame, text="Back to Main Menu", font=("Arial", 14), command=self.main_menu)
    self.back_button.grid(row=6, column=0, pady=10, padx=10, columnspan=2)


 def load_extra_services(self):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT service_id, service_name, price FROM extra_services")
    services = cursor.fetchall()
    db.close()

    self.service_listbox.delete(0, tk.END)
    for service in services:
        service_details = f"Service {service[0]}: {service[1]}, Price: {service[2]} USD"
        self.service_listbox.insert(tk.END, service_details)

 def book_extra_service(self):
    selected_service = self.service_listbox.get(tk.ACTIVE)
    if selected_service:
        service_id = selected_service.split(":")[0].split()[1]
        service_price = float(selected_service.split(", Price: ")[1].split()[0])  # Extract price
        payment_method = self.payment_method_var.get()

        if not payment_method:
            messagebox.showerror("Error", "Please select a payment method.")
            return

        confirm_currency = messagebox.askyesno("Currency Conversion", "Would you like to pay in Taka?")
        if confirm_currency:
            service_price *= 110  # Assuming 1 USD = 110 Taka
            currency = "TK"
        else:
            currency = "USD"

        confirm = messagebox.askyesno(
            "Confirm Booking",
            f"Do you want to book Extra Service {service_id} for {service_price:.2f} {currency} using {payment_method}?"
        )

        if confirm:
            try:
                self.book_extra_service_in_db(service_id, payment_method, service_price, currency)
                messagebox.showinfo("Success", f"Extra Service {service_id} booked successfully!")
                self.main_menu()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to book extra service: {e}")
    else:
        messagebox.showerror("Error", "Please select a service.")

 def book_extra_service_in_db(self, service_id, payment_method, amount, currency):
    db = connect_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO extra_service_bookings (user_id, service_id, payment_method, amount, currency, status) 
            VALUES (%s, %s, %s, %s, %s, 'Confirmed')
            """,
            (self.user_id, service_id, payment_method, amount, currency)
        )
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

 def view_booking_history(self):
    self.clear_window()

    # Create a frame to center the elements
    menu_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
    menu_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

    # Add the title label
    tk.Label(menu_frame, text="Booking History", font=("Arial", 20), bg='white').grid(row=0, column=0, pady=10, padx=10, columnspan=2)

    # Add the listbox for booking history
    self.booking_listbox = tk.Listbox(menu_frame, width=60, height=10, font=("Arial", 14))
    self.booking_listbox.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

    # Add the "Load Bookings" button
    self.load_bookings_button = tk.Button(menu_frame, text="Load Bookings", font=("Arial", 14), command=self.load_bookings)
    self.load_bookings_button.grid(row=2, column=0, pady=5, padx=5, columnspan=2)

    # Add the "Cancel Booking" button
    self.cancel_booking_button = tk.Button(menu_frame, text="Cancel Booking", font=("Arial", 14), command=self.cancel_booking)
    self.cancel_booking_button.grid(row=3, column=0, pady=5, padx=5, columnspan=2)

    # Add the "Back to Main Menu" button
    self.back_button = tk.Button(menu_frame, text="Back to Main Menu", font=("Arial", 14), command=self.main_menu)
    self.back_button.grid(row=4, column=0, pady=10, padx=10, columnspan=2)



 def load_bookings(self):
    db = connect_db()
    cursor = db.cursor()

    query = """
        SELECT 'Room' AS type, room_number, payment_method, status, NULL AS amount, NULL AS currency 
        FROM bookings 
        WHERE user_id = %s
        UNION
        SELECT 'Service' AS type, service_id, payment_method, status, NULL AS amount, NULL AS currency 
        FROM extra_service_bookings 
        WHERE user_id = %s
        UNION
        SELECT 'Package' AS type, package_id, payment_method, status, amount, currency 
        FROM package_bookings 
        WHERE user_id = %s
    """
    cursor.execute(query, (self.user_id, self.user_id, self.user_id))
    bookings = cursor.fetchall()
    db.close()

    self.booking_listbox.delete(0, tk.END)
    for booking in bookings:
        if booking[0] == 'Room':
            booking_details = f"Room {booking[1]} - Payment: {booking[2]}, Status: {booking[3]}"
        elif booking[0] == 'Service':
            booking_details = f"Service {booking[1]} - Payment: {booking[2]}, Status: {booking[3]}"
        else:
            amount_display = f"{booking[4]} {booking[5]}"
            booking_details = f"Package {booking[1]} - Payment: {booking[2]}, Amount: {amount_display}, Status: {booking[3]}"
        self.booking_listbox.insert(tk.END, booking_details)

    # Clear the Listbox and insert bookings
    self.booking_listbox.delete(0, tk.END)
    for booking in bookings:
        booking_details = f"{booking[0]} Booking - ID: {booking[1]}, Payment: {booking[2]}, Status: {booking[3]}"
        self.booking_listbox.insert(tk.END, booking_details)

    db.close()

 def cancel_booking(self):
    selected_booking = self.booking_listbox.get(tk.ACTIVE)
    if selected_booking:
        try:
            # Parse booking details
            booking_parts = selected_booking.split(" - ID: ")
            booking_type = booking_parts[0].split(" ")[0]
            booking_id = booking_parts[1].split(",")[0]

            # Confirm cancellation
            confirm = messagebox.askyesno(
                "Confirm Cancellation",
                f"Do you want to cancel {booking_type} Booking with ID {booking_id}?"
            )
            if confirm:
                self.cancel_booking_in_db(booking_type, booking_id)
                messagebox.showinfo("Success", f"{booking_type} Booking with ID {booking_id} has been canceled!")
                self.load_bookings()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to cancel booking: {e}")
    else:
        messagebox.showerror("Error", "Please select a booking.")
 def cancel_booking_in_db(self, booking_type, booking_id):
    db = connect_db()
    cursor = db.cursor()

    try:
        if booking_type == "Room":
            # Cancel room booking
            cursor.execute("UPDATE rooms SET availability = 'available' WHERE room_number = %s", (booking_id,))
            cursor.execute("DELETE FROM bookings WHERE room_number = %s AND user_id = %s", (booking_id, self.user_id))
        
        elif booking_type == "Service":
            # Cancel extra service booking
            print(f"Deleting extra service: Booking ID = {booking_id}, User ID = {self.user_id}")
            cursor.execute("DELETE FROM extra_service_bookings WHERE service_id = %s AND user_id = %s", (booking_id, self.user_id))
        
        elif booking_type == "Package":
            # Cancel package booking
            cursor.execute("DELETE FROM package_bookings WHERE package_id = %s AND user_id = %s", (booking_id, self.user_id))

        db.commit()
        print(f"{booking_type} booking canceled successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error canceling {booking_type} booking: {e}")
        raise e
    finally:
        db.close()



 def logout(self):
    """
    Logs out the user with a thank-you message and exits the application completely.
    """
    messagebox.showinfo("Thank You", "Thank you for using our Hotel Management System!")
    self.root.destroy() 
    exit(0)  
