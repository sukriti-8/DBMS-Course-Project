import os
import sqlite3
import mysql.connector
from mysql.connector import Error

# Default connection settings for MySQL
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'database': os.getenv('MYSQL_DATABASE', 'airline_reservation_db'),
    'port': int(os.getenv('MYSQL_PORT', 3306))
}
# Connection mode tracking ('mysql' or 'sqlite')
_db_mode = None
def get_db_connection():
    """
    Establishes and returns a connection to MySQL database.
    If MySQL server is unreachable, falls back to local SQLite database with identical schema and data.
    """
    global _db_mode
    # Try MySQL first
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        if conn.is_connected():
            _db_mode = 'mysql'
            return conn, 'mysql'
    except Error as e:
        # Fall back to SQLite gracefully
        pass
    except Exception:
        pass

    # SQLite fallback
    db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'airline_reservation.db')
    db_path = os.path.abspath(db_path)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    _db_mode = 'sqlite'
    
    # Initialize SQLite schema if tables don't exist
    init_sqlite_if_needed(conn)
    return conn, 'sqlite'

def init_sqlite_if_needed(conn):
    """Initializes SQLite schema and sample data if tables don't exist."""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Passenger'")
    if cursor.fetchone() is None:
        # Tables don't exist, create them
        sql_schema = """
        CREATE TABLE IF NOT EXISTS Passenger (
            passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            passport_no TEXT NOT NULL UNIQUE
        );
        CREATE TABLE IF NOT EXISTS Airport (
            airport_id INTEGER PRIMARY KEY AUTOINCREMENT,
            airport_code TEXT NOT NULL UNIQUE,
            airport_name TEXT NOT NULL,
            city TEXT NOT NULL,
            country TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS Aircraft (
            aircraft_id INTEGER PRIMARY KEY AUTOINCREMENT,
            aircraft_model TEXT NOT NULL,
            capacity INTEGER NOT NULL CHECK (capacity > 0)
        );
        CREATE TABLE IF NOT EXISTS Flight (
            flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_number TEXT NOT NULL UNIQUE,
            aircraft_id INTEGER NOT NULL,
            departure_airport_id INTEGER NOT NULL,
            arrival_airport_id INTEGER NOT NULL,
            departure_datetime TEXT NOT NULL,
            arrival_datetime TEXT NOT NULL,
            status TEXT NOT NULL,
            base_fare REAL NOT NULL CHECK (base_fare >= 0),
            FOREIGN KEY (aircraft_id) REFERENCES Aircraft(aircraft_id),
            FOREIGN KEY (departure_airport_id) REFERENCES Airport(airport_id),
            FOREIGN KEY (arrival_airport_id) REFERENCES Airport(airport_id)
        );
        CREATE TABLE IF NOT EXISTS Seat (
            seat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            aircraft_id INTEGER NOT NULL,
            seat_number TEXT NOT NULL,
            seat_class TEXT NOT NULL,
            FOREIGN KEY (aircraft_id) REFERENCES Aircraft(aircraft_id),
            UNIQUE (aircraft_id, seat_number)
        );
        CREATE TABLE IF NOT EXISTS Reservation (
            reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            passenger_id INTEGER NOT NULL,
            flight_id INTEGER NOT NULL,
            booking_date TEXT NOT NULL,
            reservation_status TEXT NOT NULL,
            FOREIGN KEY (passenger_id) REFERENCES Passenger(passenger_id),
            FOREIGN KEY (flight_id) REFERENCES Flight(flight_id)
        );
        CREATE TABLE IF NOT EXISTS Payment (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            reservation_id INTEGER NOT NULL UNIQUE,
            amount REAL NOT NULL CHECK (amount >= 0),
            payment_method TEXT NOT NULL,
            payment_status TEXT NOT NULL,
            payment_date TEXT NOT NULL,
            FOREIGN KEY (reservation_id) REFERENCES Reservation(reservation_id)
        );
        """
        cursor.executescript(sql_schema)
        
        # Insert sample data
        sample_data_sql = """
        INSERT INTO Airport (airport_code, airport_name, city, country) VALUES
        ('HYD', 'Rajiv Gandhi International Airport', 'Hyderabad', 'India'),
        ('DEL', 'Indira Gandhi International Airport', 'Delhi', 'India'),
        ('BOM', 'Chhatrapati Shivaji Maharaj International Airport', 'Mumbai', 'India'),
        ('BLR', 'Kempegowda International Airport', 'Bangalore', 'India'),
        ('MAA', 'Chennai International Airport', 'Chennai', 'India');

        INSERT INTO Aircraft (aircraft_model, capacity) VALUES
        ('Airbus A320', 180),
        ('Boeing 737-800', 189),
        ('Airbus A321', 220),
        ('Boeing 787-9', 296),
        ('Airbus A350-900', 325);

        INSERT INTO Passenger (name, email, phone, passport_no) VALUES
        ('Rahul Sharma', 'rahul.sharma@gmail.com', '9876543210', 'P1234567'),
        ('Priya Reddy', 'priya.reddy@gmail.com', '9876543211', 'P1234568'),
        ('Arjun Mehta', 'arjun.mehta@gmail.com', '9876543212', 'P1234569'),
        ('Ananya Singh', 'ananya.singh@gmail.com', '9876543213', 'P1234570'),
        ('Vikram Rao', 'vikram.rao@gmail.com', '9876543214', 'P1234571');

        INSERT INTO Seat (aircraft_id, seat_number, seat_class) VALUES
        (1, '1A', 'Business'),
        (1, '1B', 'Business'),
        (2, '10A', 'Economy'),
        (2, '10B', 'Economy'),
        (3, '15A', 'Economy');

        INSERT INTO Flight (flight_number, aircraft_id, departure_airport_id, arrival_airport_id, departure_datetime, arrival_datetime, status, base_fare) VALUES
        ('AI101', 1, 1, 2, '2026-10-10 08:00:00', '2026-10-10 10:15:00', 'Scheduled', 5500.00),
        ('6E202', 2, 2, 3, '2026-10-11 11:30:00', '2026-10-11 13:45:00', 'Scheduled', 4800.00),
        ('UK303', 3, 3, 4, '2026-10-12 15:00:00', '2026-10-12 17:00:00', 'Scheduled', 5200.00),
        ('AI404', 4, 4, 5, '2026-10-13 18:30:00', '2026-10-13 20:45:00', 'Scheduled', 6200.00),
        ('6E505', 5, 5, 1, '2026-10-14 06:30:00', '2026-10-14 09:00:00', 'Scheduled', 5800.00);

        INSERT INTO Reservation (passenger_id, flight_id, booking_date, reservation_status) VALUES
        (1, 1, '2026-09-20', 'Confirmed'),
        (2, 2, '2026-09-21', 'Confirmed'),
        (3, 3, '2026-09-22', 'Confirmed'),
        (4, 4, '2026-09-23', 'Pending'),
        (5, 5, '2026-09-24', 'Confirmed');

        INSERT INTO Payment (reservation_id, amount, payment_method, payment_status, payment_date) VALUES
        (1, 5500.00, 'UPI', 'Paid', '2026-09-20'),
        (2, 4800.00, 'Card', 'Paid', '2026-09-21'),
        (3, 5200.00, 'UPI', 'Paid', '2026-09-22'),
        (4, 6200.00, 'Card', 'Pending', '2026-09-23'),
        (5, 5800.00, 'Net Banking', 'Paid', '2026-09-24');
        """
        cursor.executescript(sample_data_sql)
        conn.commit()

def fetch_all(query, params=()):
    """Executes a SELECT query and returns all records as a list of dicts."""
    conn, mode = get_db_connection()
    try:
        if mode == 'sqlite':
            query_mod = query.replace('%s', '?')
            cursor = conn.cursor()
            cursor.execute(query_mod, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        else:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
            rows = cursor.fetchall()
            cursor.close()
            return rows
    finally:
        conn.close()

def fetch_one(query, params=()):
    """Executes a SELECT query and returns a single record as a dict."""
    conn, mode = get_db_connection()
    try:
        if mode == 'sqlite':
            query_mod = query.replace('%s', '?')
            cursor = conn.cursor()
            cursor.execute(query_mod, params)
            row = cursor.fetchone()
            return dict(row) if row else None
        else:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
            row = cursor.fetchone()
            cursor.close()
            return row
    finally:
        conn.close()

def execute_query(query, params=()):
    """Executes an INSERT, UPDATE, or DELETE query and commits changes."""
    conn, mode = get_db_connection()
    try:
        if mode == 'sqlite':
            query_mod = query.replace('%s', '?')
            cursor = conn.cursor()
            cursor.execute(query_mod, params)
            conn.commit()
            last_id = cursor.lastrowid
            return last_id
        else:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            last_id = cursor.lastrowid
            cursor.close()
            return last_id
    finally:
        conn.close()
