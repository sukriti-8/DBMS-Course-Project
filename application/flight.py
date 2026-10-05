from application.database import get_connection


def add_flight(
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
            print("Flight number already exists.")
        else:
            print(f"Error adding flight: {e}")

        return False

    finally:
        cursor.close()
        connection.close()

def get_flights():
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
            print("Flight number already exists.")
        else:
            print(f"Error updating flight: {e}")

        return False

    finally:
        cursor.close()
        connection.close()

def delete_flight(flight_id):
    connection = get_connection()

    if connection is None:
        return False

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
        print(f"Error deleting flight: {e}")
        return False

    finally:
        cursor.close()
        connection.close()