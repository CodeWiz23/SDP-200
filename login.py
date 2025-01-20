from db_connection import connect_db


def validate_login(username, password):
    # Ensure username and password are provided
    if not username or not password:
        raise ValueError("Username and password are required!")


    try:
        # Connect to the database
        db = connect_db()
        cursor = db.cursor()


        # Use parameterized queries to prevent SQL injection
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()


        # If a user is found, return the user data (assuming user data is stored in the returned row)
        if user:
            return user  # Return the user data


        # If no user is found, return None
        return None


    except Exception as e:
        # Handle any database errors
        print(f"Error during login validation: {e}")
        raise ValueError("An error occurred while validating login.")
