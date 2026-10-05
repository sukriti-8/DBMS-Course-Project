from application.database import fetch_all, fetch_one, execute_query

def get_all_aircrafts():
    """Retrieve all aircraft records."""
    query = "SELECT * FROM Aircraft ORDER BY aircraft_id ASC"
    return fetch_all(query)

def get_aircraft_by_id(aircraft_id):
    """Retrieve aircraft by ID."""
    query = "SELECT * FROM Aircraft WHERE aircraft_id = %s"
    return fetch_one(query, (aircraft_id,))

def add_aircraft(aircraft_model, capacity):
    """Add a new aircraft."""
    query = """
        INSERT INTO Aircraft (aircraft_model, capacity)
        VALUES (%s, %s)
    """
    return execute_query(query, (aircraft_model.strip(), int(capacity)))
