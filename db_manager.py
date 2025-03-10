import os
import sqlite3

DB_PATH = 'db/venue_booking.db'


def connect_db():
    """Connect to the SQLite database."""
    if not os.path.exists('db'):
        os.makedirs('db')  # Ensure the 'db' directory exists
    return sqlite3.connect(DB_PATH)


def create_tables():
    """Create tables for users, venues, and bookings."""
    with connect_db() as conn:
        cursor = conn.cursor()

        # Users table
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )''')

        # Venues table
        cursor.execute('''CREATE TABLE IF NOT EXISTS venues (
            venue_id INTEGER PRIMARY KEY AUTOINCREMENT,
            venue_name TEXT UNIQUE NOT NULL,
            location TEXT DEFAULT '',
            capacity INTEGER DEFAULT 0,
            image TEXT DEFAULT ''
        )''')

        # Bookings table
        cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            venue_id INTEGER,
            booking_date TEXT,
            time_range TEXT,
            purpose TEXT,
            event_name TEXT,
            is_approved INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (venue_id) REFERENCES venues (venue_id)
        )''')

        # Default admin account
        cursor.execute('''INSERT OR IGNORE INTO users (username, password, is_admin)
                          VALUES ('admin', 'admin', 1)''')
        conn.commit()


# CRUD Functions

def register_user(username, password):
    """Register a new user in the database."""
    with connect_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Username already exists")


def login_user(username, password):
    """Log in a user by verifying credentials."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, is_admin FROM users WHERE username = ? AND password = ?", (username, password))
        return cursor.fetchone()


def add_venue(venue_name, image_path, capacity):
    """Add a new venue with an image."""
    with connect_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO venues (venue_name, location, capacity, image) VALUES (?, ?, ?, ?)",
                (venue_name, "Location not specified", capacity, image_path),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Venue already exists")


def get_all_venues():
    """Retrieve all venues."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT venue_id, venue_name, location, capacity, image FROM venues")
        return cursor.fetchall()


def get_venue_by_id(venue_id):
    """Retrieve a venue by ID."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT venue_id, venue_name, location, capacity, image FROM venues WHERE venue_id = ?", (venue_id,))
        return cursor.fetchone()


def delete_venue(venue_id):
    """Delete a venue and associated bookings."""
    with connect_db() as conn:
        cursor = conn.cursor()
        try:
            # Delete bookings tied to the venue
            cursor.execute("DELETE FROM bookings WHERE venue_id = ?", (venue_id,))
            # Delete the venue itself
            cursor.execute("DELETE FROM venues WHERE venue_id = ?", (venue_id,))
            conn.commit()
        except sqlite3.Error as e:
            raise ValueError(f"Error deleting venue: {e}")


def book_venue(user_id, venue_id, booking_date, time_range, purpose, event_name):
    """Book a venue."""
    with connect_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''INSERT INTO bookings (user_id, venue_id, booking_date, time_range, purpose, event_name, is_approved)
                              VALUES (?, ?, ?, ?, ?, ?, 0)''',
                           (user_id, venue_id, booking_date, time_range, purpose, event_name))
            conn.commit()
        except sqlite3.Error as e:
            raise ValueError(f"Error booking venue: {e}")


def get_user_bookings(user_id):
    """Retrieve bookings made by a specific user."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT b.booking_id, v.venue_id, v.venue_name, v.image, b.booking_date, b.time_range, b.purpose, b.event_name, b.is_approved
                          FROM bookings b
                          INNER JOIN venues v ON b.venue_id = v.venue_id
                          WHERE b.user_id = ?''', (user_id,))
        return cursor.fetchall()

def get_pending_bookings():
    """Retrieve all pending bookings for admin."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT b.booking_id, v.venue_id, v.venue_name, v.image, b.booking_date, b.time_range, b.purpose, b.event_name, b.is_approved
                          FROM bookings b
                          INNER JOIN venues v ON b.venue_id = v.venue_id
                          WHERE b.is_approved = 0''')
        return cursor.fetchall()


def get_approved_bookings():
    """Retrieve all approved bookings."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT b.booking_id, v.venue_id, v.venue_name, v.image, b.booking_date, b.time_range, b.purpose, b.event_name, b.is_approved
                          FROM bookings b
                          INNER JOIN venues v ON b.venue_id = v.venue_id
                          WHERE b.is_approved = 1''')
        return cursor.fetchall()


def get_denied_bookings():
    """Retrieve all denied bookings."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT b.booking_id, v.venue_id, v.venue_name, v.image, b.booking_date, b.time_range, b.purpose, b.event_name, b.is_approved
                          FROM bookings b
                          INNER JOIN venues v ON b.venue_id = v.venue_id
                          WHERE b.is_approved = -1''')
        return cursor.fetchall()


def get_canceled_bookings():
    """Retrieve all canceled bookings."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT b.booking_id, v.venue_id, v.venue_name, v.image, b.booking_date, b.time_range, b.purpose, b.event_name, b.is_approved
                          FROM bookings b
                          INNER JOIN venues v ON b.venue_id = v.venue_id
                          WHERE b.is_approved = -2''')
        return cursor.fetchall()

def approve_booking(booking_id):
    """Approve a booking."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE bookings SET is_approved = 1 WHERE booking_id = ?", (booking_id,))
        conn.commit()


def deny_booking(booking_id):
    """Deny a booking."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE bookings SET is_approved = -1 WHERE booking_id = ?", (booking_id,))
        conn.commit()


def delete_booking(booking_id):
    """Delete a booking."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bookings WHERE booking_id = ?", (booking_id,))
        conn.commit()
def get_booking_count(venue_id, status):
    """Get the count of bookings for a venue by status."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM bookings WHERE venue_id = ? AND is_approved = ?", (venue_id, status))
        return cursor.fetchone()[0]

def get_total_bookings(user_id):
    """Get the total number of bookings for a user."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM bookings WHERE user_id = ?", (user_id,))
        return cursor.fetchone()[0]

def get_total_bookings_by_status(user_id, status):
    """Get the total number of bookings for a user by status."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM bookings WHERE user_id = ? AND is_approved = ?", (user_id, status)
        )
        return cursor.fetchone()[0]
def get_all_users(exclude_admin=False):
    """Retrieve all users from the database. Optionally exclude admins."""
    with connect_db() as conn:
        cursor = conn.cursor()
        query = "SELECT user_id, username FROM users"
        if exclude_admin:
            query += " WHERE is_admin = 0"
        cursor.execute(query)
        return cursor.fetchall()
