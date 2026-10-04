from application.database import fetch_all, fetch_one, execute_query

def get_all_airports():
    """Retrieve all airports."""
    query = "SELECT * FROM Airport ORDER BY airport_name ASC"
    return fetch_all(query)

def get_airport_by_id(airport_id):
    """Retrieve airport by ID."""
    query = "SELECT * FROM Airport WHERE airport_id = %s"
    return fetch_one(query, (airport_id,))

def add_airport(airport_code, airport_name, city, country):
    """Add a new airport."""
    query = """
        INSERT INTO Airport (airport_code, airport_name, city, country)
        VALUES (%s, %s, %s, %s)
    """
    return execute_query(query, (airport_code.strip(), airport_name.strip(), city.strip(), country.strip()))
