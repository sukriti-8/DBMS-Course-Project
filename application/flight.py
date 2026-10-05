from application.database import fetch_all, fetch_one, execute_query

def get_all_flights():
    """Retrieve all flight records along with airport and aircraft details."""
    query = """
        SELECT 
            f.flight_id,
            f.flight_number,
            f.aircraft_id,
            ac.aircraft_model,
            f.departure_airport_id,
            dep.airport_code AS departure_code,
            dep.city AS departure_city,
            f.arrival_airport_id,
            arr.airport_code AS arrival_code,
            arr.city AS arrival_city,
            f.departure_datetime,
            f.arrival_datetime,
            f.status,
            f.base_fare
        FROM Flight f
        JOIN Aircraft ac ON f.aircraft_id = ac.aircraft_id
        JOIN Airport dep ON f.departure_airport_id = dep.airport_id
        JOIN Airport arr ON f.arrival_airport_id = arr.airport_id
        ORDER BY f.flight_id DESC
    """
    return fetch_all(query)

def get_flight_by_id(flight_id):
    """Retrieve a single flight by ID with full details."""
    query = """
        SELECT 
            f.*,
            ac.aircraft_model,
            dep.airport_code AS departure_code,
            arr.airport_code AS arrival_code
        FROM Flight f
        JOIN Aircraft ac ON f.aircraft_id = ac.aircraft_id
        JOIN Airport dep ON f.departure_airport_id = dep.airport_id
        JOIN Airport arr ON f.arrival_airport_id = arr.airport_id
        WHERE f.flight_id = %s
    """
    return fetch_one(query, (flight_id,))

def add_flight(flight_number, aircraft_id, departure_airport_id, arrival_airport_id, departure_datetime, arrival_datetime, status, base_fare):
    """Insert a new flight record."""
    query = """
        INSERT INTO Flight (
            flight_number, aircraft_id, departure_airport_id, arrival_airport_id,
            departure_datetime, arrival_datetime, status, base_fare
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    return execute_query(query, (
        flight_number.strip(),
        int(aircraft_id),
        int(departure_airport_id),
        int(arrival_airport_id),
        str(departure_datetime),
        str(arrival_datetime),
        status.strip(),
        float(base_fare)
    ))

<<<<<<< Updated upstream
def update_flight(flight_id, flight_number, aircraft_id, departure_airport_id, arrival_airport_id, departure_datetime, arrival_datetime, status, base_fare):
    """Update an existing flight record."""
    query = """
        UPDATE Flight
        SET flight_number = %s, aircraft_id = %s, departure_airport_id = %s,
            arrival_airport_id = %s, departure_datetime = %s, arrival_datetime = %s,
            status = %s, base_fare = %s
        WHERE flight_id = %s
    """
    return execute_query(query, (
        flight_number.strip(),
        int(aircraft_id),
        int(departure_airport_id),
        int(arrival_airport_id),
        str(departure_datetime),
        str(arrival_datetime),
        status.strip(),
        float(base_fare),
        int(flight_id)
    ))
=======
    if arrival_datetime <= departure_datetime:
        print("Arrival time must be after departure time.")
        return False

    if base_fare is None or base_fare < 0:
        print("Base fare cannot be negative.")
        return False

    connection = get_connection()

    if connection is None:
        return False

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO Flight (
                flight_number,
                aircraft_id,
                departure_airport_id,
                arrival_airport_id,
                departure_datetime,
                arrival_datetime,
                status,
                base_fare
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            flight_number,
            aircraft_id,
            departure_airport_id,
            arrival_airport_id,
            departure_datetime,
            arrival_datetime,
            status,
            base_fare
        )

        cursor.execute(query, values)
        connection.commit()

        print("Flight added successfully.")
        return True

    except Exception as e:
        connection.rollback()

        if "Duplicate entry" in str(e):
            raise Exception("Flight number already exists.")
        else:
            raise Exception(f"Database error: {str(e)}")

    finally:
        cursor.close()
        connection.close()

def get_total_flights_count():
    connection = get_connection()
    if connection is None:
        return 0
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as cnt FROM Flight")
        res = cursor.fetchone()
        return res['cnt'] if res else 0
    except Exception as e:
        print(f"Error: {e}")
        return 0
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_average_base_fare():
    connection = get_connection()
    if connection is None:
        return 0
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT AVG(base_fare) as avg_fare FROM Flight")
        res = cursor.fetchone()
        return res['avg_fare'] if res and res['avg_fare'] else 0
    except Exception as e:
        print(f"Error: {e}")
        return 0
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_all_flights():
    connection = get_connection()

    if connection is None:
        return []

    try:
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM Flight"
        cursor.execute(query)

        flights = cursor.fetchall()
        return flights

    except Exception as e:
        print(f"Error fetching flights: {e}")
        return []

    finally:
        cursor.close()
        connection.close()

def update_flight(
    flight_id,
    flight_number,
    aircraft_id,
    departure_airport_id,
    arrival_airport_id,
    departure_datetime,
    arrival_datetime,
    status,
    base_fare
):
    if not flight_number or not aircraft_id or not departure_airport_id or not arrival_airport_id:
        print("Required flight details are missing.")
        return False

    if not departure_datetime or not arrival_datetime or not status:
        print("Required flight details are missing.")
        return False

    if arrival_datetime <= departure_datetime:
        print("Arrival time must be after departure time.")
        return False

    if base_fare is None or base_fare < 0:
        print("Base fare cannot be negative.")
        return False

    connection = get_connection()

    if connection is None:
        return False

    try:
        cursor = connection.cursor()

        query = """
            UPDATE Flight
            SET flight_number = %s,
                aircraft_id = %s,
                departure_airport_id = %s,
                arrival_airport_id = %s,
                departure_datetime = %s,
                arrival_datetime = %s,
                status = %s,
                base_fare = %s
            WHERE flight_id = %s
        """

        values = (
            flight_number,
            aircraft_id,
            departure_airport_id,
            arrival_airport_id,
            departure_datetime,
            arrival_datetime,
            status,
            base_fare,
            flight_id
        )

        cursor.execute(query, values)

        if cursor.rowcount == 0:
            print("Flight not found.")
            return False

        connection.commit()

        print("Flight updated successfully.")
        return True

    except Exception as e:
        connection.rollback()

        if "Duplicate entry" in str(e):
            raise Exception("Flight number already exists.")
        else:
            raise Exception(f"Database error: {str(e)}")

    finally:
        cursor.close()
        connection.close()
>>>>>>> Stashed changes

def delete_flight(flight_id):
    """Delete a flight by ID."""
    query = "DELETE FROM Flight WHERE flight_id = %s"
    return execute_query(query, (int(flight_id),))

def get_total_flights_count():
    """Returns total flight count."""
    query = "SELECT COUNT(*) as count FROM Flight"
    res = fetch_one(query)
    return res['count'] if res else 0

<<<<<<< Updated upstream
def get_average_base_fare():
    """Returns average base fare of flights."""
    query = "SELECT AVG(base_fare) as avg_fare FROM Flight"
    res = fetch_one(query)
    return round(res['avg_fare'], 2) if res and res['avg_fare'] else 0.0
=======
    try:
        cursor = connection.cursor()

        query = "DELETE FROM Flight WHERE flight_id = %s"
        cursor.execute(query, (flight_id,))

        if cursor.rowcount == 0:
            print("Flight not found.")
            return False

        connection.commit()

        print("Flight deleted successfully.")
        return True

    except Exception as e:
        connection.rollback()
        raise Exception(f"Database error: {str(e)}")

    finally:
        cursor.close()
        connection.close()
>>>>>>> Stashed changes
