from application.database import fetch_all, fetch_one, execute_query

def get_all_passengers():
    """Retrieve all passenger records from the database."""
    query = "SELECT * FROM Passenger ORDER BY passenger_id DESC"
    return fetch_all(query)

def get_passenger_by_id(passenger_id):
    """Retrieve a single passenger record by ID."""
    query = "SELECT * FROM Passenger WHERE passenger_id = %s"
    return fetch_one(query, (passenger_id,))

def add_passenger(name, email, phone, passport_no):
    """Insert a new passenger record into the database."""
    query = """
        INSERT INTO Passenger (name, email, phone, passport_no)
        VALUES (%s, %s, %s, %s)
    """
    return execute_query(query, (name.strip(), email.strip(), phone.strip(), passport_no.strip()))

def update_passenger(passenger_id, name, email, phone, passport_no):
    """Update an existing passenger's details."""
    query = """
        UPDATE Passenger
        SET name = %s, email = %s, phone = %s, passport_no = %s
        WHERE passenger_id = %s
    """
    return execute_query(query, (name.strip(), email.strip(), phone.strip(), passport_no.strip(), passenger_id))

def delete_passenger(passenger_id):
    """Delete a passenger by ID."""
    query = "DELETE FROM Passenger WHERE passenger_id = %s"
    return execute_query(query, (passenger_id,))

def get_total_passengers_count():
    """Returns total count of passengers in the database."""
    query = "SELECT COUNT(*) as count FROM Passenger"
    res = fetch_one(query)
    return res['count'] if res else 0
