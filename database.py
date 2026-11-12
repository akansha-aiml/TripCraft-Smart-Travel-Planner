
import sqlite3

DB_NAME = "tripcraft.db"


def connect_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Trips table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trips (
            trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_name TEXT NOT NULL,
            destination TEXT NOT NULL,
            start_date TEXT,
            end_date TEXT,
            budget REAL,
            travelers INTEGER
        )
    """)

    # Destinations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS destinations (
            destination_id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER NOT NULL,
            place_name TEXT NOT NULL,
            category TEXT,
            notes TEXT,
            FOREIGN KEY (trip_id) REFERENCES trips(trip_id)
            ON DELETE CASCADE
        )
    """)

    # Daily itinerary table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itinerary (
            itinerary_id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER NOT NULL,
            plan_date TEXT NOT NULL,
            plan_time TEXT,
            activity TEXT NOT NULL,
            location TEXT,
            notes TEXT,
            FOREIGN KEY (trip_id) REFERENCES trips(trip_id)
            ON DELETE CASCADE
        )
    """)

    # Expenses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER NOT NULL,
            category TEXT,
            description TEXT,
            amount REAL NOT NULL,
            expense_date TEXT,
            FOREIGN KEY (trip_id) REFERENCES trips(trip_id)
            ON DELETE CASCADE
        )
    """)

    # Packing checklist table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS packing_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER NOT NULL,
            item TEXT NOT NULL,
            packed INTEGER DEFAULT 0,
            FOREIGN KEY (trip_id) REFERENCES trips(trip_id)
            ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
